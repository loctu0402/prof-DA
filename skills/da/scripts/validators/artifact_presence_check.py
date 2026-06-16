#!/usr/bin/env python3
"""Artifact Presence Check, the evidence-based-done proof gate (presence layer).

A thin PRESENCE gate (not a content gate): proves a claimed deliverable reached the "ran" rung, not
just "written". Complements self_check.py / report_consistency_audit.py (which check report CONTENT).
The deliver + report modes drop a receipt; this checks each named artifact EXISTS, is NON-EMPTY, is not
a bare stub, and (for kind=code) carries a proof marker from a passing test/build.

Receipt format (JSON), see references/evidence-based-done.md:
  {
    "root": "<optional base for relative paths>",
    "deliverables": [
      {"path": "output/reports/x_latest.html", "kind": "doc",  "min_bytes": 200},
      {"path": "models/metrics.json",          "kind": "data", "min_bytes": 50},
      {"path": "pipeline/03_forecast.py",       "kind": "code", "proof": ".prof-da/proof/forecast.ok"}
    ]
  }

Usage:
  python artifact_presence_check.py <receipt.json>
  python artifact_presence_check.py --deliverables out/a.html,out/b.csv   # quick check, kind=doc
  python artifact_presence_check.py <receipt.json> --json

Exit:
  0 = every deliverable present, non-empty, (code) proven
  1 = at least one missing / empty / stub / unproven
  2 = receipt / argument error

Pure stdlib (argparse, json, sys, pathlib). No external deps.

— part of prof-DA · Loc Tu, 2026
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_MIN_BYTES = 50
STUB_MARKERS = ("[TODO]", "{{", "TBD", "PLACEHOLDER")


def resolve(path: str, root: str | None) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return (Path(root) / p) if root else (Path.cwd() / p)


def looks_stub(target: Path) -> bool:
    if target.suffix.lower() not in (".md", ".html", ".txt", ".json"):
        return False
    try:
        head = target.read_text(encoding="utf-8-sig", errors="replace")[:400]
    except Exception:
        return False
    return any(m in head for m in STUB_MARKERS) and len(head.strip()) < 300


def check_one(d: dict, root: str | None) -> tuple[str, str, str]:
    path = d.get("path", "")
    kind = d.get("kind", "doc")
    min_bytes = d.get("min_bytes", DEFAULT_MIN_BYTES)
    target = resolve(path, root)
    if not target.exists():
        return path, "MISSING", "not on disk (rung: not even written)"
    try:
        size = target.stat().st_size
    except Exception:
        size = 0
    if size < min_bytes:
        return path, "EMPTY", f"{size}b < {min_bytes} (rung: stub, not ran)"
    if looks_stub(target):
        return path, "STUB", "placeholder markers + tiny body (rung: written, not ran)"
    if kind == "code":
        proof = d.get("proof")
        if not proof:
            return path, "UNPROVEN", "no proof marker named (rung: ran? unproven)"
        pt = resolve(proof, root)
        if not pt.exists() or pt.stat().st_size == 0:
            return path, "UNPROVEN", f"proof marker missing: {proof} (rung: written, not proven)"
        return path, "PROVEN", "present + proof marker (rung: validator exit 0)"
    return path, "PRESENT", f"present, {size}b (rung: ran)"


def main() -> int:
    ap = argparse.ArgumentParser(description="Artifact presence / proof gate (evidence-based-done).")
    ap.add_argument("receipt", nargs="?", help="receipt JSON path")
    ap.add_argument("--deliverables", help="comma-separated paths (quick check, kind=doc)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    if args.deliverables:
        root = None
        items = [{"path": p.strip(), "kind": "doc"} for p in args.deliverables.split(",") if p.strip()]
    elif args.receipt:
        rp = Path(args.receipt)
        if not rp.exists():
            print(f"ERROR: receipt not found: {args.receipt}", file=sys.stderr)
            return 2
        try:
            receipt = json.loads(rp.read_text(encoding="utf-8-sig"))
        except Exception as e:
            print(f"ERROR: bad receipt JSON: {e}", file=sys.stderr)
            return 2
        root = receipt.get("root")
        items = receipt.get("deliverables", [])
    else:
        ap.error("pass a receipt JSON path or --deliverables")
        return 2

    if not items:
        print("ERROR: no deliverables to check", file=sys.stderr)
        return 2

    results = [check_one(d, root) for d in items]
    ok_states = {"PROVEN", "PRESENT"}
    passed = all(verdict in ok_states for _, verdict, _ in results)

    if args.json:
        print(json.dumps({
            "overall_pass": passed,
            "results": [{"path": p, "verdict": v, "detail": d} for p, v, d in results],
        }, indent=2))
    else:
        for p, v, d in results:
            print(f"[{v:8}] {p} - {d}")
        print(f"\noverall: {'PASS' if passed else 'FAIL'} ({sum(v in ok_states for _, v, _ in results)}/{len(results)} proven/present)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
