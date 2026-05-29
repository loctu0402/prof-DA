#!/usr/bin/env python3
"""Report Consistency Audit — hard-gate the mechanical consistency items that rubric_audit.py
does not cover: empty-as-finding, Vietnamese diacritics, self-defined (freestyle) palette,
project scaffold, and portal-publish receipt.

This is the machine-checkable subset of evaluation-rubric.md Categories 2/4/5/6. Qualitative
items (insight depth, Vietnamese tone, narrative flow) stay ADVISORY — a human / the rubric
scores those.

DELIBERATELY NOT IMPLEMENTED: automated number-reconcile across cards. A naive ">10x mismatch"
flag false-positives on legitimate encodings (e.g. HTML `data-countup="2964" data-fmt="tenth"`
renders 296.4, not 2964). Cross-card reconciliation stays a human check — self-check-protocol.md
Section D.

Checks (severity):
  empty_as_finding   BLOCKER  N/A / null / NaN / TODO / unrendered {{placeholder}} in visible body
  diacritics_missing BLOCKER  Vietnamese-intended doc with no diacritics at all
  diacritics_partial HIGH     common Vietnamese words rendered without marks
  scaffold_missing   HIGH     project deliverable dumped flat (no queries/ output/ scripts/ ...)
  portal_missing     HIGH     no portal-publish receipt found up the tree
  freestyle_palette  MEDIUM   self-defined palette not referencing a locked template/theme (advisory)

Exit:
  0 = clean or MEDIUM/LOW only
  1 = at least one BLOCKER or HIGH (hard gate)
  2 = file error

Usage:
  python report_consistency_audit.py <deliverable.html|.md>
  python report_consistency_audit.py <file> --json

Pure stdlib. — part of prof-DA · Loc Tu, 2026
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


SEVERITIES = ("BLOCKER", "HIGH", "MEDIUM", "LOW")
SCAFFOLD_DIRS = {"queries", "sql", "output", "cache", "scripts", "data", "notebooks", "pipeline"}
PORTAL_RECEIPTS = ("latest_portal_url.json", "portal_stable_uuid.txt")

# An element whose ENTIRE trimmed content is one of these = empty-as-finding (broken render).
# Scanned per-cell (between tags / between table pipes), NOT anywhere in text, so a SQL label
# like "mfu_100k IS NOT NULL" or prose "data was N/A in Feb" does not false-positive.
EXACT_EMPTY = re.compile(r"^(N/?A|NULL|NaN|undefined|#REF!|#DIV/0!|TODO|FIXME)$", re.I)
DEV_PLACEHOLDER = re.compile(r"(?<![A-Za-z])(TODO|FIXME|Lorem ipsum)(?![A-Za-z])", re.I)
UNRENDERED_PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}|\$\{[^}]+\}")

# Vietnamese diacritic characters (precomposed sample — enough as a presence signal).
VN_DIACRITICS = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
VN_DIACRITICS += VN_DIACRITICS.upper()

# Common Vietnamese words that, when seen WITHOUT marks in a VN-intended doc, signal stripped diacritics.
VN_UNACCENTED_DENYLIST = [
    "khong", "nguoi dung", "nguoi", "thang", "tai khoan", "tang truong", "tang", "giam",
    "rut som", "tien gui", "ngan hang", "trung binh", "bao cao", "phan tich", "khach hang",
]


class Finding(NamedTuple):
    check_id: str
    severity: str
    location: str
    what: str
    fix: str
    why: str


def strip_html_noise(html: str) -> str:
    """Return visible text only: drop script/style/comments, then tags."""
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&[a-zA-Z#0-9]+;", " ", html)
    return re.sub(r"\s+", " ", html)


def strip_md_code(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"`[^`\n]*`", " ", md)
    return md


def visible_text(text: str, ext: str) -> str:
    if ext == ".html":
        return strip_html_noise(text)
    return strip_md_code(text)


def is_vietnamese(text: str, raw: str) -> bool:
    if re.search(r'lang\s*=\s*"vi"', raw, re.I):
        return True
    if sum(text.count(c) for c in set(VN_DIACRITICS)) > 0:
        return True
    return False


def check_empty_as_finding(raw: str, vis: str, ext: str, name: str) -> list[Finding]:
    out: list[Finding] = []
    cells = re.findall(r">([^<>]*)<", raw) if ext == ".html" else re.findall(r"\|([^|\n]*)\|", raw)
    empties = sorted({t.strip() for c in cells if (t := c.strip()) and EXACT_EMPTY.match(t)})
    if empties:
        out.append(Finding(
            "empty_as_finding", "BLOCKER", name,
            f"Element(s) render to only an empty token: {', '.join(empties)[:80]}.",
            "Compute the real value or remove the card/row. Never ship N/A / NaN / TODO as a finding.",
            "An empty value shown as a result destroys trust and signals a broken pipeline (rubric 2.3).",
        ))
    placeholders = UNRENDERED_PLACEHOLDER.findall(vis)
    if placeholders:
        out.append(Finding(
            "empty_as_finding", "BLOCKER", name,
            f"Unrendered template placeholder(s) in visible body: {placeholders[:3]}.",
            "Resolve all template variables before publishing.",
            "A literal {{placeholder}} means the render step failed silently (rubric 2.3).",
        ))
    devs = sorted({(d if isinstance(d, str) else d[0]) for d in DEV_PLACEHOLDER.findall(vis)})
    if devs:
        out.append(Finding(
            "empty_as_finding", "HIGH", name,
            f"Dev placeholder text in visible body: {', '.join(devs)[:60]}.",
            "Remove TODO / FIXME / Lorem ipsum before shipping to stakeholders.",
            "Dev scaffolding text in a stakeholder deliverable signals unfinished work (rubric 2.3).",
        ))
    return out


def check_diacritics(vis: str, raw: str, name: str) -> list[Finding]:
    out: list[Finding] = []
    if not is_vietnamese(vis, raw):
        return out
    diac = sum(vis.count(c) for c in set(VN_DIACRITICS))
    words = len(re.findall(r"[A-Za-zÀ-ỹ]+", vis)) or 1
    if diac == 0:
        out.append(Finding(
            "diacritics_missing", "BLOCKER", name,
            "Document is Vietnamese-intended (lang=vi) but contains zero diacritics.",
            "Restore full Vietnamese diacritics across all stakeholder-facing text.",
            "Vietnamese without marks reads as broken/foreign and is unacceptable for stakeholders (rubric 5.3).",
        ))
        return out
    hits = sorted({w for w in VN_UNACCENTED_DENYLIST if re.search(rf"(?<![A-Za-zÀ-ỹ]){re.escape(w)}(?![A-Za-zÀ-ỹ])", vis, re.I)})
    if hits:
        out.append(Finding(
            "diacritics_partial", "HIGH", name,
            f"Common Vietnamese words appear without diacritics: {', '.join(hits[:6])}.",
            "Add the missing marks (e.g. 'khong'->'không', 'tang truong'->'tăng trưởng').",
            "Partial diacritics signal copy/paste from a stripped source; inconsistent marks erode polish (rubric 5.3).",
        ))
    return out


def check_freestyle_palette(raw: str, ext: str, name: str) -> list[Finding]:
    if ext != ".html":
        return []
    defines_palette = bool(re.search(r":root\s*\{[^}]*--\w+\s*:\s*#", raw, re.S))
    hexes = set(m.lower() for m in re.findall(r"#[0-9a-fA-F]{6}", raw))
    references_locked = bool(re.search(r"shared/templates|<organization>_chart_theme|<organization>_plotly_theme|_catalog", raw, re.I))
    if (defines_palette or len(hexes) > 8) and not references_locked:
        return [Finding(
            "freestyle_palette", "MEDIUM", name,
            f"Self-defined palette ({len(hexes)} distinct hexes, inline :root) with no reference to a locked template/theme.",
            "Implement from a locked template in shared/templates/ (mode-report A2) instead of bespoke CSS, so brand stops drifting per report.",
            "Per-report freestyle is the root cause of 'every report looks different' (rubric 4.1).",
        )]
    return []


def find_up(start: Path, names: tuple[str, ...], max_levels: int = 5) -> Path | None:
    """Search each ancestor dir AND ancestor/cache for any of `names`."""
    cur = start
    for _ in range(max_levels):
        for n in names:
            if (cur / n).exists():
                return cur / n
            if (cur / "cache" / n).exists():
                return cur / "cache" / n
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def check_scaffold(path: Path, name: str) -> list[Finding]:
    # Output locations are downstream; scaffold belongs to the project root elsewhere.
    if any(part.lower() == "output" for part in path.parts):
        return []
    parent = path.parent
    subdirs = {p.name.lower() for p in parent.iterdir() if p.is_dir()} if parent.exists() else set()
    if subdirs & SCAFFOLD_DIRS:
        return []
    sibling_files = [p for p in parent.iterdir() if p.is_file()] if parent.exists() else []
    if len(sibling_files) >= 2:  # a real deliverable dumped flat with other artifacts
        return [Finding(
            "scaffold_missing", "HIGH", name,
            f"Project deliverable sits flat in '{parent.name}/' with {len(sibling_files)} files and no standard subdirs.",
            "Create the standard scaffold (queries/ cache/ scripts/ output/ data/) per project-scaffold.md and move artifacts in.",
            "Flat dumps make files unfindable as reports accumulate (rubric 6.1).",
        )]
    return []


def check_portal_receipt(path: Path, name: str) -> list[Finding]:
    receipt = find_up(path.parent, PORTAL_RECEIPTS)
    if receipt is None:
        return [Finding(
            "portal_missing", "HIGH", name,
            "No portal-publish receipt (latest_portal_url.json / portal_stable_uuid.txt) found up the tree.",
            "Publish via `python shared/portal_upload.py upload <file> --duration 72` (or replace_or_create for recurring) and save the receipt. mode-report Step 9.",
            "The 72h portal link is the deliverable's shareable form; skipping it is the user's #1 forgotten step (rubric 6.3).",
        )]
    return []


def audit(path: Path) -> list[Finding]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    ext = path.suffix.lower()
    vis = visible_text(raw, ext)
    findings: list[Finding] = []
    findings += check_empty_as_finding(raw, vis, ext, path.name)
    findings += check_diacritics(vis, raw, path.name)
    findings += check_freestyle_palette(raw, ext, path.name)
    findings += check_scaffold(path, path.name)
    findings += check_portal_receipt(path, path.name)
    return findings


def headline(findings: list[Finding]) -> str:
    n_block = sum(1 for f in findings if f.severity == "BLOCKER")
    n_high = sum(1 for f in findings if f.severity == "HIGH")
    if n_block:
        return f"FAIL - {n_block} BLOCKER + {n_high} HIGH. Not shippable."
    if n_high:
        return f"FAIL - {n_high} HIGH (hard gate). Fix before ship."
    if findings:
        return f"PASS-with-notes - {len(findings)} advisory item(s)."
    return "PASS - consistency gate clean."


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.file.is_file():
        print(json.dumps({"error": f"not a file: {args.file}"}), file=sys.stderr)
        return 2

    findings = audit(args.file)
    sev_order = {s: i for i, s in enumerate(SEVERITIES)}
    findings = sorted(findings, key=lambda f: sev_order.get(f.severity, 99))

    if args.json:
        print(json.dumps({
            "file": str(args.file),
            "findings": [f._asdict() for f in findings],
            "headline": headline(findings),
            "pass": not any(f.severity in ("BLOCKER", "HIGH") for f in findings),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"# report_consistency_audit: {args.file}")
        for f in findings:
            print(f"[{f.severity}] {f.check_id} | {f.location}\n    what: {f.what}\n    fix:  {f.fix}\n    why:  {f.why}")
        print(f"\n# headline: {headline(findings)}")

    return 0 if not any(f.severity in ("BLOCKER", "HIGH") for f in findings) else 1


if __name__ == "__main__":
    sys.exit(main())
