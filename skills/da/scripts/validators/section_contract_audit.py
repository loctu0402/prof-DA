#!/usr/bin/env python3
"""Section Contract Audit — per-section definition-of-done gate for recurring reports.

Complements rubric_audit.py (which checks GLOBAL skill rules). This script checks a populated
report against a bespoke SECTION CONTRACT: every required section present, non-empty, free of
unrendered placeholders, with each definition-of-done (DoD) item heuristically evident — and emits
a per-section quality_check worksheet for the judgment half the machine cannot decide.

Contract format (JSON), see references/recurring-report-contract.md:
  {
    "report": "...", "cadence": "bi-weekly", "version": 3,
    "sections": [
      {"key": "business_overview", "title": "Business Overview", "required": true,
       "dod": ["AUM actual vs target", "MFU actual vs target", "projection to end of month"]}
    ],
    "carry_forward": [{"section_key": "...", "note": "..."}]
  }

Usage:
  python section_contract_audit.py <report.md|.html|.txt> --contract report-contract.json
  python section_contract_audit.py <report> --contract <c.json> --json                  # JSON (default)
  python section_contract_audit.py <report> --contract <c.json> --worksheet              # markdown quality_check worksheet
  python section_contract_audit.py <report> --contract <c.json> --payload --author Name  # submit_contribution-shaped JSON payload

Exit:
  0 = all required sections present, non-empty, no placeholder
  1 = at least one required-section gate failed
  2 = file / contract error

Pure stdlib (re, json, argparse, pathlib, sys). No external deps.

— part of prof-DA · Loc Tu, 2026
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER_RX = re.compile(r"\{\{.*?\}\}|\bTODO\b|\bN/?A\b|\bnull\b|\bNaN\b|\bTBD\b", re.I)
# Heading detector: markdown (#..######) or HTML (<h1>..<h6>). Captures heading text.
MD_HEADING_RX = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
HTML_HEADING_RX = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.I | re.S)
STOPWORDS = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "vs", "with", "by", "over",
    "recent", "current", "actual", "from", "its", "each", "per", "is", "are", "be", "as", "at",
}


def load(path: Path) -> str:
    # utf-8-sig tolerates a Windows BOM (PowerShell Out-File, Notepad) and plain utf-8 alike.
    return path.read_text(encoding="utf-8-sig", errors="replace")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip().lower()


def find_headings(text: str) -> list[tuple[int, str, int]]:
    """Return [(level, heading_text_lower, char_offset)] in document order, md + html."""
    out: list[tuple[int, str, int]] = []
    for m in MD_HEADING_RX.finditer(text):
        out.append((len(m.group(1)), norm(m.group(2)), m.start()))
    for m in HTML_HEADING_RX.finditer(text):
        out.append((int(m.group(1)), norm(m.group(2)), m.start()))
    out.sort(key=lambda t: t[2])
    return out


def section_body(text: str, headings: list, idx: int) -> str:
    """Body from heading idx up to the next heading of same-or-higher level (or EOF)."""
    level, _, start = headings[idx]
    # body starts after the heading line/tag
    body_start = text.find("\n", start)
    body_start = body_start + 1 if body_start != -1 else start
    end = len(text)
    for j in range(idx + 1, len(headings)):
        nlvl, _, npos = headings[j]
        if nlvl <= level:
            end = npos
            break
    return text[body_start:end]


def keywords(dod_item: str) -> list[str]:
    toks = re.findall(r"[a-z0-9][a-z0-9\-]+", dod_item.lower())
    return [t for t in toks if t not in STOPWORDS and len(t) > 2]


def dod_present(body_norm: str, dod_item: str) -> bool:
    """Heuristic: >=60% of the DoD item's content keywords appear in the section body."""
    kw = keywords(dod_item)
    if not kw:
        return True
    hits = sum(1 for k in kw if k in body_norm)
    return hits / len(kw) >= 0.6


def match_section(headings: list, sec: dict) -> int | None:
    """Find a heading matching the section title or key. Returns heading index or None."""
    title = norm(sec.get("title", ""))
    key = sec.get("key", "").replace("_", " ").lower()
    for i, (_, htext, _) in enumerate(headings):
        if title and (title == htext or title in htext or htext in title):
            return i
        if key and (key in htext or htext in key):
            return i
    return None


def audit(report_text: str, contract: dict) -> dict:
    headings = find_headings(report_text)
    results = []
    missing_required = []
    for sec in contract.get("sections", []):
        key = sec.get("key", "")
        title = sec.get("title", key)
        required = bool(sec.get("required", True))
        dod = sec.get("dod", []) or []
        hidx = match_section(headings, sec)
        entry = {"key": key, "title": title, "required": required, "found": hidx is not None}
        if hidx is None:
            entry["status"] = "MISSING" if required else "absent (optional)"
            entry["dod"] = [{"item": d, "present": False} for d in dod]
            if required:
                missing_required.append(key)
            results.append(entry)
            continue
        body = section_body(report_text, headings, hidx)
        body_norm = norm(body)
        empty = len(body_norm) < 40
        placeholders = sorted(set(m.group(0) for m in PLACEHOLDER_RX.finditer(body)))
        dod_status = [{"item": d, "present": dod_present(body_norm, d)} for d in dod]
        missing_dod = [d["item"] for d in dod_status if not d["present"]]
        entry.update({
            "empty": empty,
            "placeholders": placeholders,
            "dod": dod_status,
            "dod_missing": missing_dod,
        })
        if empty:
            entry["status"] = "EMPTY"
            if required:
                missing_required.append(key)
        elif placeholders:
            entry["status"] = "PLACEHOLDER"
            if required:
                missing_required.append(key)
        elif missing_dod:
            entry["status"] = "DOD_GAP"  # advisory: not a hard fail, surfaced for the worksheet
        else:
            entry["status"] = "OK"
        results.append(entry)

    # carry-forward: re-surface open items whose section still exists in the contract
    contract_keys = {s.get("key") for s in contract.get("sections", [])}
    carry = []
    for cf in contract.get("carry_forward", []) or []:
        sk = cf.get("section_key")
        carry.append({
            "section_key": sk,
            "note": cf.get("note", ""),
            "section_in_contract": sk in contract_keys,
        })

    overall_pass = len(missing_required) == 0
    return {
        "report": contract.get("report", ""),
        "version": contract.get("version"),
        "sections": results,
        "missing_required": missing_required,
        "dod_gaps": {r["key"]: r.get("dod_missing", []) for r in results if r.get("dod_missing")},
        "carry_forward_open": carry,
        "overall_pass": overall_pass,
    }


def worksheet(result: dict) -> str:
    """Render the per-section quality_check worksheet (judgment half) as markdown."""
    lines = [f"# quality_check worksheet — {result.get('report','')}"]
    if result.get("version") is not None:
        lines.append(f"_contract version {result['version']}_")
    lines.append("")
    lines.append("For each DoD item, write one line on HOW the section content satisfies it.")
    lines.append("Mechanical flags: [x] = keyword-evident, [ ] = not evident (justify or fix).")
    lines.append("")
    for r in result["sections"]:
        tag = r["status"]
        lines.append(f"## {r['title']}  ({'required' if r['required'] else 'optional'}) — {tag}")
        if not r["found"]:
            lines.append("- SECTION NOT FOUND in report. Add it.")
            lines.append("")
            continue
        if r.get("placeholders"):
            lines.append(f"- Unrendered placeholders: {', '.join(r['placeholders'])} — resolve.")
        for d in r.get("dod", []):
            box = "x" if d["present"] else " "
            lines.append(f"- [{box}] {d['item']} — quality_check: ____")
        lines.append("")
    if result["carry_forward_open"]:
        lines.append("## Carry-forward (still open from last cycle)")
        for cf in result["carry_forward_open"]:
            mark = "" if cf["section_in_contract"] else "  (section no longer in contract!)"
            lines.append(f"- [{cf['section_key']}] {cf['note']}{mark}")
        lines.append("")
    verdict = "PASS" if result["overall_pass"] else "FAIL"
    lines.append(f"**Gate: {verdict}**" + (
        "" if result["overall_pass"] else f" — missing/empty required: {', '.join(result['missing_required'])}"))
    return "\n".join(lines)


def build_payload(report_text: str, contract: dict, author: str = "") -> dict:
    """Build a submit_contribution-shaped payload from the report + contract.

    Mirrors the <report-mcp> `submit_contribution` schema: author + sections{key: content} +
    quality_check{key: justification}. Section content is the extracted body (FOUND) or a
    MISSING marker; quality_check is a per-DoD template with auto-presence flags for the user
    to complete before pasting into the MCP call.
    """
    headings = find_headings(report_text)
    sections: dict[str, str] = {}
    quality_check: dict[str, str] = {}
    for sec in contract.get("sections", []):
        key = sec.get("key", "")
        dod = sec.get("dod", []) or []
        hidx = match_section(headings, sec)
        if hidx is None:
            sections[key] = f"<MISSING: add section '{sec.get('title', key)}' — build it in report mode, do not draft here>"
            qc_items = "; ".join(f"[ ] {d}" for d in dod)
            quality_check[key] = f"<SECTION MISSING — fill after building>. DoD: {qc_items}"
            continue
        body = section_body(report_text, headings, hidx).strip()
        sections[key] = body
        body_norm = norm(body)
        flags = "; ".join(f"[{'x' if dod_present(body_norm, d) else ' '}] {d}" for d in dod)
        quality_check[key] = f"<FILL: how this section satisfies each DoD item>. Auto-flags: {flags}"
    payload = {"author": author or "<FILL: your name>", "sections": sections, "quality_check": quality_check}
    return payload


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", type=Path, help="Populated report (.md / .html / .txt)")
    p.add_argument("--contract", type=Path, required=True, help="report-contract.json")
    p.add_argument("--worksheet", action="store_true", help="Print markdown quality_check worksheet instead of JSON")
    p.add_argument("--payload", action="store_true", help="Print a submit_contribution-shaped JSON payload (author + sections + quality_check) to fill then paste into the MCP call")
    p.add_argument("--author", default="", help="Author name to pre-fill in --payload")
    args = p.parse_args()

    if not args.path.is_file():
        print(json.dumps({"error": f"not a file: {args.path}"}), file=sys.stderr)
        return 2
    if not args.contract.is_file():
        print(json.dumps({"error": f"contract not found: {args.contract}"}), file=sys.stderr)
        return 2
    try:
        contract = json.loads(load(args.contract))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"bad contract JSON: {e}"}), file=sys.stderr)
        return 2

    report_text = load(args.path)
    result = audit(report_text, contract)
    if args.payload:
        print(json.dumps(build_payload(report_text, contract, args.author), indent=2, ensure_ascii=False))
    elif args.worksheet:
        print(worksheet(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
