"""Security-scan a skill / workflow package before packaging or install.

A curated, stdlib-only port of the high-value SkillSpector checks (prompt injection,
data exfiltration, system-prompt leakage, excessive agency, supply-chain, tool misuse,
MCP least-privilege, secret hardcode). Two engines:
  1. regex/content - scans every text file for dangerous content patterns;
  2. AST/behavioral - parses .py files for dangerous calls (exec/eval, subprocess,
     os.system, os.environ iteration, dynamic import, pickle.loads).

Scoring (SkillSpector-style): per-finding points CRITICAL 50 / HIGH 25 / MEDIUM 10 /
LOW 5; total x1.3 if the package ships executable code (.py/.sh); clamped 0-100.
Bands: LOW 0-20, MEDIUM 21-50, HIGH 51-80, CRITICAL 81-100. The package VERDICT is the
worse of the score band and the single most-severe finding (so one CRITICAL is never
hidden by a low total).

Usage:
  python skill_security_scan.py <path>                  # terminal report
  python skill_security_scan.py <path> --json           # machine report
  python skill_security_scan.py <path> --fail-on high   # exit 1 if verdict >= high (gate)
  python skill_security_scan.py <path> --quiet          # one summary line

Exit: 0 = pass (verdict below --fail-on), 1 = fail (verdict >= --fail-on), 2 = usage error.

This is a Stage-1 static scanner: HIGH RECALL, moderate precision (the SkillSpector design;
its Stage-2 LLM pass that lifts precision to ~87% is not ported). Findings are a TRIAGE list
for a human, not an oracle. Legitimate code triggers some checks (a subprocess running `bq`,
a doc that mentions `eval`). Mark a reviewed-safe line with a trailing `# nosec` comment and the
scanner drops every finding on that line - that is how a real package reaches a clean gate.
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path

SEV = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
POINTS = {"LOW": 5, "MEDIUM": 10, "HIGH": 25, "CRITICAL": 50}
BANDS = [(80, "CRITICAL"), (50, "HIGH"), (20, "MEDIUM"), (0, "LOW")]

TEXT_EXT = {".md", ".py", ".sh", ".bash", ".json", ".yaml", ".yml", ".txt", ".toml", ".cfg", ".ini"}
MAX_BYTES = 1_000_000
SNIPPET_MAX = 140

# Regex content checks. applies: "all" = every text file; "non-py" = skip .py (AST covers it).
REGEX_CHECKS = [
    # Prompt injection
    ("PI1", "prompt-injection", "CRITICAL", "all",
     r"(?i)\bignore\s+(all\s+|the\s+)?(previous|prior|above|earlier|system)\b.{0,24}(instruction|prompt|rule|guardrail)",
     "instruction-override phrase"),
    ("PI2", "prompt-injection", "CRITICAL", "all",
     r"(?i)\b(disregard|forget|override|bypass)\s+(your|all|the|any)\s+(rule|instruction|guardrail|policy|system\s*prompt)",
     "rule-override phrase"),
    ("PI3", "prompt-injection", "HIGH", "all",
     "[\u200b\u200c\u200d\u2060\ufeff]",
     "zero-width / hidden unicode character"),
    # System-prompt leakage
    ("SPL1", "system-prompt-leak", "HIGH", "all",
     r"(?i)\b(reveal|print|show|repeat|output|dump|leak|expose)\b.{0,24}(system\s*prompt|your\s+instructions?|everything\s+above|the\s+prompt\s+above|initial\s+prompt)",
     "system-prompt exfiltration phrase"),
    ("SPL2", "system-prompt-leak", "MEDIUM", "all",
     r"(?i)what\s+(were|are)\s+you\s+(told|instructed|programmed)",
     "instruction-probing phrase"),
    # Data exfiltration (env iteration handled by AST for .py)
    ("EX1", "data-exfiltration", "HIGH", "non-py",
     r"(os\.environ\s*\.\s*(items|keys|values)\s*\(|for\s+\w+\s*,?\s*\w*\s+in\s+os\.environ)",
     "environment-variable harvesting"),
    ("EX2", "data-exfiltration", "MEDIUM", "all",
     r"(?i)(requests\.post|httpx\.post|urllib\.request\.urlopen|urlopen|fetch)\s*\(",
     "outbound network call (verify it does not send local data/secrets)"),
    ("EX3", "data-exfiltration", "MEDIUM", "all",
     r"""(?i)open\s*\(\s*['"][^'"]*\.env""",
     "reads a .env file"),
    ("EX4", "data-exfiltration", "MEDIUM", "all",
     r"(?i)(curl|wget)\b[^\n]*\b(--data|--data-binary|-d\b|-F\b|--upload-file)",
     "shell upload of data"),
    # Excessive agency / dangerous shell
    ("EA1", "excessive-agency", "HIGH", "all",
     r"(?i)\brm\s+-[rf]{1,2}\s+(/|~|\$|\*)",
     "recursive force delete"),
    ("EA2", "excessive-agency", "HIGH", "non-py",
     r"shell\s*=\s*True",
     "subprocess with shell=True"),
    ("EA3", "excessive-agency", "HIGH", "non-py",
     r"os\.system\s*\(",
     "os.system shell call"),
    ("EA4", "excessive-agency", "MEDIUM", "all",
     r"(?i)(^|[^\w])sudo\s+",
     "privilege escalation (sudo)"),
    # Supply chain
    ("SC1", "supply-chain", "CRITICAL", "all",
     r"(?i)(curl|wget)\s+[^\n|]*\|\s*(sudo\s+)?(bash|sh|zsh|python\d?)",
     "pipe-to-shell remote execution"),
    ("SC2", "supply-chain", "MEDIUM", "all",
     r"(?i)pip\s+install\s+(git\+|https?://)",
     "pip install from a URL / VCS"),
    ("SC3", "supply-chain", "LOW", "all",
     r"(?i)pip\s+install\s+(?!-r\b)(?![^\n]*==)[a-z][a-z0-9_.\-]+(\s|$)",
     "unpinned pip dependency (no ==version)"),
    # Tool misuse (eval/exec/compile/import/pickle handled by AST for .py)
    ("TM1", "tool-misuse", "CRITICAL", "non-py",
     r"\b(eval|exec)\s*\(",
     "dynamic code execution"),
    ("TM2", "tool-misuse", "HIGH", "non-py",
     r"\bcompile\s*\(",
     "code compilation"),
    ("TM3", "tool-misuse", "HIGH", "non-py",
     r"__import__\s*\(",
     "dynamic import"),
    ("TM4", "tool-misuse", "MEDIUM", "non-py",
     r"pickle\s*\.\s*loads?\s*\(",
     "pickle deserialization"),
    # Secret hardcode
    ("SEC1", "secret-hardcode", "HIGH", "all",
     r"""(?i)\b(api[_-]?key|secret|token|password|passwd|access[_-]?key)\b\s*[:=]\s*['"][A-Za-z0-9_\-/+]{16,}['"]""",
     "hardcoded credential"),
    ("SEC2", "secret-hardcode", "CRITICAL", "all",
     r"\bAKIA[0-9A-Z]{16}\b",
     "hardcoded AWS access key"),
    ("SEC3", "secret-hardcode", "HIGH", "all",
     r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}",
     "hardcoded JWT"),
    ("SEC4", "secret-hardcode", "CRITICAL", "all",
     r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----",
     "embedded private key"),
    ("SEC5", "secret-hardcode", "CRITICAL", "all",
     r"\b(glpat-[A-Za-z0-9_\-]{20}|ghp_[A-Za-z0-9]{36})\b",
     "hardcoded GitLab/GitHub token"),
    # MCP least-privilege (manifests)
    ("MCP1", "mcp-least-privilege", "MEDIUM", "all",
     r'(?i)"(tools|permissions|allow|scopes)"\s*:\s*\[\s*"\*"',
     "wildcard tool/permission grant"),
]
REGEX_COMPILED = [(cid, cat, sev, ap, re.compile(pat), why) for cid, cat, sev, ap, pat, why in REGEX_CHECKS]


def band(score):
    for floor, name in BANDS:
        if score > floor:
            return name
    return "LOW"


def worse(a, b):
    return a if SEV[a] >= SEV[b] else b


def snippet(line):
    s = line.strip()
    return s[:SNIPPET_MAX] + ("..." if len(s) > SNIPPET_MAX else "")


def scan_text(rel, lines, is_py, findings):
    for i, line in enumerate(lines, 1):
        if "nosec" in line.lower():          # bandit-style per-line suppression (reviewed-safe)
            continue
        for cid, cat, sev, ap, rx, why in REGEX_COMPILED:
            if ap == "non-py" and is_py:
                continue
            if rx.search(line):
                findings.append({"id": cid, "category": cat, "severity": sev,
                                 "file": rel, "line": i, "snippet": snippet(line), "why": why})


AST_NAME_CALLS = {"eval": ("CRITICAL", "dynamic code execution (eval)"),
                  "exec": ("CRITICAL", "dynamic code execution (exec)"),
                  "compile": ("HIGH", "code compilation"),
                  "__import__": ("HIGH", "dynamic import")}


def scan_py_ast(rel, text, lines, findings):
    try:
        tree = ast.parse(text, filename=rel)
    except (SyntaxError, ValueError):
        return  # not valid python; regex stage still covered it as text
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        ln = getattr(node, "lineno", 0)
        if 0 < ln <= len(lines) and "nosec" in lines[ln - 1].lower():
            continue
        f = node.func
        # bare name calls: eval/exec/compile/__import__
        if isinstance(f, ast.Name) and f.id in AST_NAME_CALLS:
            sev, why = AST_NAME_CALLS[f.id]
            _add_ast(findings, "AST-EXEC", "tool-misuse", sev, rel, node, why)
        # attribute calls: os.system, subprocess.*, os.environ.items, pickle.loads, importlib.import_module
        elif isinstance(f, ast.Attribute):
            root = _root_name(f.value)
            attr = f.attr
            if root == "os" and attr == "system":
                _add_ast(findings, "AST-OSSYS", "excessive-agency", "HIGH", rel, node, "os.system shell call")
            elif root == "subprocess" and attr in {"run", "call", "Popen", "check_call", "check_output"}:
                shell_true = any(isinstance(k, ast.keyword) and k.arg == "shell"
                                 and isinstance(k.value, ast.Constant) and k.value.value is True
                                 for k in node.keywords)
                sev = "HIGH" if shell_true else "LOW"
                why = "subprocess with shell=True (shell-injection risk)" if shell_true else \
                    "subprocess invocation (review the command; common in legit tooling)"
                _add_ast(findings, "AST-SUBPROC", "excessive-agency", sev, rel, node, why)
            elif attr in {"items", "keys", "values"} and _is_os_environ(f.value):
                _add_ast(findings, "AST-ENVITER", "data-exfiltration", "HIGH", rel, node,
                         "environment-variable harvesting")
            elif root == "pickle" and attr in {"loads", "load"}:
                _add_ast(findings, "AST-PICKLE", "tool-misuse", "MEDIUM", rel, node, "pickle deserialization")
            elif root == "importlib" and attr == "import_module":
                _add_ast(findings, "AST-DYNIMP", "tool-misuse", "MEDIUM", rel, node, "dynamic import")


def _root_name(node):
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def _is_os_environ(node):
    return isinstance(node, ast.Attribute) and node.attr == "environ" and _root_name(node) == "os"


def _add_ast(findings, cid, cat, sev, rel, node, why):
    findings.append({"id": cid, "category": cat, "severity": sev, "file": rel,
                     "line": getattr(node, "lineno", 0), "snippet": f"<{cid}>", "why": why})


def scan(target):
    target = Path(target)
    if not target.exists():
        sys.exit(f"error: target not found: {target}")
    files = [target] if target.is_file() else sorted(
        p for p in target.rglob("*") if p.is_file() and p.suffix in TEXT_EXT)
    findings, scanned, has_exec = [], 0, False
    for p in files:
        if p.suffix in {".py", ".sh", ".bash"}:
            has_exec = True
        try:
            if p.stat().st_size > MAX_BYTES:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(p.relative_to(target)) if target.is_dir() else p.name
        lines = text.splitlines()
        scanned += 1
        scan_text(rel, lines, p.suffix == ".py", findings)
        if p.suffix == ".py":
            scan_py_ast(rel, text, lines, findings)
    # de-dup exact (file,line,id)
    seen, uniq = set(), []
    for f in findings:
        k = (f["file"], f["line"], f["id"])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    raw = sum(POINTS[f["severity"]] for f in uniq)
    score = min(100, round(raw * (1.3 if has_exec else 1.0)))
    # score/band = accumulated RISK SURFACE (informational). verdict = the single most-severe
    # finding = what a gate acts on (tunable via --fail-on). Decoupled so a pile of legit
    # subprocess calls inflates the surface but does not auto-fail a gate set to --fail-on critical.
    verdict = "LOW"
    for f in uniq:
        verdict = worse(verdict, f["severity"])
    uniq.sort(key=lambda f: (-SEV[f["severity"]], f["file"], f["line"]))
    counts = {s: sum(1 for f in uniq if f["severity"] == s) for s in SEV}
    return {"target": str(target), "files_scanned": scanned, "raw_points": raw,
            "score": score, "band": band(score), "verdict": verdict,
            "counts": counts, "findings": uniq}


def print_report(r, quiet):
    if quiet:
        print(f"{r['verdict']} score={r['score']} findings={len(r['findings'])} target={r['target']}")
        return
    print(f"== skill_security_scan: {r['target']} ==")
    print(f"files scanned: {r['files_scanned']}")
    if not r["findings"]:
        print("no findings.")
    for f in r["findings"]:
        print(f"[{f['severity']:8} {f['id']:10}] {f['category']:20} {f['file']}:{f['line']}")
        print(f"    {f['why']}  ::  {f['snippet']}")
    c = r["counts"]
    print(f"-- score {r['score']}/100 (band {r['band']}) "
          f"| CRIT {c['CRITICAL']} HIGH {c['HIGH']} MED {c['MEDIUM']} LOW {c['LOW']}")
    install = "DO NOT INSTALL" if SEV[r["verdict"]] >= SEV["HIGH"] else (
        "CAUTION" if r["verdict"] == "MEDIUM" else "SAFE")
    print(f"-- VERDICT: {r['verdict']} ({install})")


def main():
    try:  # snippets may carry zero-width / non-cp1252 chars; never let printing crash the scan
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="Security-scan a skill/workflow package.")
    ap.add_argument("path", help="skill/workflow folder or single file")
    ap.add_argument("--json", action="store_true", help="emit JSON report")
    ap.add_argument("--quiet", action="store_true", help="one summary line")
    ap.add_argument("--fail-on", default="high", choices=["low", "medium", "high", "critical"],
                    help="exit 1 if verdict >= this severity (default: high)")
    a = ap.parse_args()
    r = scan(a.path)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print_report(r, a.quiet)
    return 1 if SEV[r["verdict"]] >= SEV[a.fail_on.upper()] else 0


if __name__ == "__main__":
    sys.exit(main())
