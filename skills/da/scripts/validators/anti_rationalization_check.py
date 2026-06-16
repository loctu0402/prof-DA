#!/usr/bin/env python3
"""Anti-Rationalization Check, a plan / task-list gate for the deliver mode.

Heuristically flags the shortcuts that make a chunked build skip a hard step (see
references/execution-discipline.md). It checks a plan or task list for:
  1. a task with no verify / check / test / acceptance line (a task you cannot prove done);
  2. an irreversible action (push / send / publish / delete / drop / backfill / cutover / migrate /
     force-push) with no STOP / confirm / gate marker nearby (build-auto Gate 6);
  3. a red-flag rationalization phrase in the plan prose.

Usage:
  python anti_rationalization_check.py <plan-or-tasklist.md>
  python anti_rationalization_check.py <plan.md> --json

Exit:
  0 = no findings
  1 = at least one finding
  2 = file / argument error

Pure stdlib (argparse, json, re, sys, pathlib). No external deps.

— part of prof-DA · Loc Tu, 2026
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TASK_RX = re.compile(r"^\s*(?:[-*]\s*\[[ x]\]|\d+[.)]|task\s+\d+|gate\s+\d+)\s+(.*)$", re.I | re.M)
VERIFY_RX = re.compile(r"\b(verify|test|check|assert|acceptance|AC\b|validator|render-verify|exit 0|count\b|proof)\b", re.I)
IRREVERSIBLE_RX = re.compile(r"\b(push|send|publish|email|delete|remove|drop\s+table|backfill|cutover|migrat|force-?push|deploy|overwrite)\b", re.I)
STOP_RX = re.compile(r"\b(stop|confirm|approval|approve|gate|ask the user|one-way|irreversible|do not auto)\b", re.I)
REDFLAGS = [
    "it looks right", "seems right", "should work", "should be fine", "i'll test it later",
    "test at the end", "too simple to test", "skip the test", "just to be safe", "trivial so",
    "the subagent said", "glob is proof", "i'll update the template later", "mock data is fine",
]


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def split_blocks(text: str):
    matches = list(TASK_RX.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((m.group(1).strip()[:80], text[start:end]))
    return blocks


def audit(text: str):
    findings = []
    for title, body in split_blocks(text):
        if not VERIFY_RX.search(body):
            findings.append(("NO_VERIFY", title, "task has no verify/test/acceptance line"))
        if IRREVERSIBLE_RX.search(body) and not STOP_RX.search(body):
            findings.append(("IRREVERSIBLE_NO_STOP", title, "irreversible action with no STOP/confirm/gate marker"))
    low = text.lower()
    for phrase in REDFLAGS:
        if phrase in low:
            findings.append(("RED_FLAG", phrase, "rationalization phrase in the plan prose"))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Anti-rationalization check for a deliver plan / task list.")
    ap.add_argument("plan", help="plan or task-list markdown file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    p = Path(args.plan)
    if not p.exists():
        print(f"ERROR: not found: {args.plan}", file=sys.stderr)
        return 2
    try:
        text = load(p)
    except Exception as e:
        print(f"ERROR: cannot read: {e}", file=sys.stderr)
        return 2

    findings = audit(text)
    if args.json:
        print(json.dumps({"clean": not findings,
                          "findings": [{"type": t, "where": w, "detail": d} for t, w, d in findings]}, indent=2))
    else:
        if not findings:
            print("clean: no rationalizations / missing verify gates found")
        else:
            for t, w, d in findings:
                print(f"[{t}] {w} - {d}")
            print(f"\n{len(findings)} finding(s). Resolve before running the build (references/execution-discipline.md).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
