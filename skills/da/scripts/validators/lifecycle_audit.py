#!/usr/bin/env python3
"""
lifecycle_audit.py - scan a project for evidence of all 7 delivery-lifecycle phases.

Encodes the lifecycle-audit rubric: per phase, look for an artifact (by filename) AND a
content signal, then score PRESENT / PARTIAL / MISSING by presence-proof (not "I remember
doing it"). Heuristic by nature - it reads filenames + text content; a human confirms.
Phases + the rubric: references/delivery-lifecycle.md + references/lifecycle-execution-rules.md.

Verdict (count PRESENT of 7): 7 -> Ship (mature) | 5-6 -> Fix | 3-4 -> Fix-heavy/Rebuild
process | <3 -> Rebuild (ad-hoc). This is the operational arm of review Sub-mode E.

Usage:
  python lifecycle_audit.py <project-dir>
  python lifecycle_audit.py <project-dir> --json

Exit 0 always (it reports; it does not gate). Pair with /prof-DA:review Sub-mode E.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TEXT_EXT = {".md", ".py", ".sql", ".yml", ".yaml", ".json", ".txt", ".ipynb", ".r", ".html", ".toml"}
CODE_EXT = {".py", ".sql", ".ipynb", ".r"}
MAX_BYTES = 600_000
TEST_RE = re.compile(r"(^test_|_test\.|\btests?\b|\.test\.|conftest)", re.I)

# phase -> (filename-regex, content-regex). DELIVER is special-cased (code + tests).
PHASES = [
    ("1 DISCOVER", r"(charter|brief|intent|readme|planning|product.?brief|frame|00.?index|scope)",
     r"(problem statement|outcome|success metric|out.?of.?scope|business intent|objective)"),
    ("2 MODEL", r"(schema|model|entit|data.?dict|grain|mart|dimension|erd)",
     r"(grain|primary.?key|1 row =|\bentity\b|cardinality|relationship)"),
    ("3 SPECIFY", r"(spec|requirement|srs|acceptance)",
     r"(acceptance criteria|given.{0,40}when.{0,40}then|\bac:|definition of done|\bdod\b|\bdor\b|non.?functional)"),
    ("4 REVIEW", r"(review|decision|\badr\b|alternativ)",
     r"(decision log|alternative|rejected|sign.?off|trade.?off|considered|second perspective)"),
    ("5 DELIVER", None, None),   # special: code + tests
    ("6 VALIDATE", r"(valid|eval|backtest|result|report|verif|audit)",
     r"(ac pass|validator|\bmet\b|\bmissed\b|evidence|parity|test.{0,12}pass|groundedness|reconcile)"),
    ("7 LEARN", r"(retro|changelog|lesson|digest|learn)",
     r"(retro|lesson|root.?cause|what.{0,20}learned|next.{0,12}iteration|backlog)"),
]
GAP_ACTION = {
    "1 DISCOVER": "add a charter/brief: problem statement (no solution) + measurable outcome + scope",
    "2 MODEL": "add a domain/schema model: entities + grain (1 row = ?) + business rules + edge cases",
    "3 SPECIFY": "add a spec with acceptance criteria (Given-When-Then / checklist) per use case",
    "4 REVIEW": "record a decision log: >=1 alternative considered + why chosen + sign-off",
    "5 DELIVER": "add tests next to the code; commit per task (1 task = 1 commit) with a verify gate",
    "6 VALIDATE": "show evidence each AC passes (run output / validator exit 0); reconcile vs requirements",
    "7 LEARN": "capture a retro + codify the lesson (changelog / rule / template) for the next loop",
}
ORDER = {"PRESENT": 2, "PARTIAL": 1, "MISSING": 0}


def collect(project):
    files = []
    has_code = has_tests = False
    for p in Path(project).rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXT:
            continue
        if p.suffix.lower() in CODE_EXT:
            has_code = True
        if TEST_RE.search(p.name) or "test" in {part.lower() for part in p.parts}:
            has_tests = True
        try:
            if p.stat().st_size > MAX_BYTES:
                files.append((p.name.lower(), ""))
                continue
            files.append((p.name.lower(), p.read_text(encoding="utf-8", errors="replace").lower()))
        except OSError:
            continue
    return files, has_code, has_tests


def verdict_for(name_rx, content_rx, files):
    name_hit = any(re.search(name_rx, nm) for nm, _ in files)
    content_hit = any(re.search(content_rx, txt) for _, txt in files)
    if name_hit and content_hit:
        return "PRESENT"
    if name_hit or content_hit:
        return "PARTIAL"
    return "MISSING"


def audit(project):
    files, has_code, has_tests = collect(project)
    rows = []
    for phase, name_rx, content_rx in PHASES:
        if phase == "5 DELIVER":
            v = "PRESENT" if (has_code and has_tests) else ("PARTIAL" if (has_code or has_tests) else "MISSING")
        else:
            v = verdict_for(name_rx, content_rx, files)
        rows.append((phase, v))
    present = sum(1 for _, v in rows if v == "PRESENT")
    if present == 7:
        overall = "Ship (mature)"
    elif present >= 5:
        overall = "Fix (close the gaps)"
    elif present >= 3:
        overall = "Fix-heavy / consider Rebuild process"
    else:
        overall = "Rebuild (ad-hoc, no spine)"
    gaps = [(ph, v, GAP_ACTION[ph]) for ph, v in rows if v != "PRESENT"]
    return {"project": str(project), "files_scanned": len(files),
            "present": present, "verdict": overall,
            "scorecard": [{"phase": ph, "state": v} for ph, v in rows],
            "gaps": [{"phase": ph, "state": v, "action": a} for ph, v, a in gaps]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not Path(a.project).exists():
        sys.exit(f"error: project not found: {a.project}")
    r = audit(a.project)
    if a.json:
        print(json.dumps(r, indent=2))
        return 0
    print(f"== lifecycle_audit: {r['project']} ({r['files_scanned']} files) ==")
    for row in r["scorecard"]:
        mark = {"PRESENT": "[x]", "PARTIAL": "[~]", "MISSING": "[ ]"}[row["state"]]
        print(f"  {mark} {row['phase']:12} {row['state']}")
    print(f"-- {r['present']}/7 PRESENT  ->  VERDICT: {r['verdict']}")
    if r["gaps"]:
        print("-- gap worklist:")
        for g in r["gaps"]:
            print(f"   ({g['phase']}, {g['state']}) {g['action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
