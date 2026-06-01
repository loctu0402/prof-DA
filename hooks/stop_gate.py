#!/usr/bin/env python3
"""
prof-DA Stop validation gate (receipt-targeted, hard-block, loop-bounded).

WHY a receipt and not a file scan: a Stop hook that picked the "most recently
modified .md/.html" would block on non-reports (a README, a REVIEW, a scratch
note) because self_check.py expects report structure. So this gate does NOTHING
unless `report` mode left a receipt naming the deliverable(s) it must validate.

Flow:
  1. report mode saves a deliverable AND writes <project>/.prof-da/pending-validation.json
     {"deliverables": ["output/reports/foo.html"], "attempts": 0}
  2. On Stop, this gate walks up from cwd to find that receipt.
     - no receipt            -> exit 0 (silent; not a prof-DA report session)
  3. With a receipt, it runs the REPORT CONSISTENCY hard-gate on each listed deliverable
     (report_consistency_audit via self_check.py, with the markdown-doc checks
     orientation_block / action_brief / ai_tell_scan skipped - those false-fail rendered
     HTML reports, which would trap every report, not just bad ones).
     - all pass              -> delete the receipt, exit 0 (stop allowed)
     - any fail              -> exit 2 with the failures on stderr (stop BLOCKED;
                                Claude must fix, then the gate clears itself)
  4. Loop bound: each block increments receipt.attempts; past MAX_ATTEMPTS the gate
     stops blocking (loud warning, stop allowed) so a truly stuck session is never trapped.

Fail-open: ANY internal error -> exit 0. A buggy hook must never brick a session.

Stdin: the Stop-hook JSON ({"cwd": ..., "stop_hook_active": ...}). Safe if absent.

- part of prof-DA . Loc Tu, 2026
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

RECEIPT_REL = Path(".prof-da") / "pending-validation.json"
MAX_ATTEMPTS = 5
SELF_CHECK = Path(__file__).resolve().parent.parent / "skills" / "da" / "scripts" / "validators" / "self_check.py"
RCA = SELF_CHECK.parent / "report_consistency_audit.py"


def find_receipt(start: Path) -> Path | None:
    cur = start.resolve()
    for d in [cur, *cur.parents]:
        cand = d / RECEIPT_REL
        if cand.is_file():
            return cand
    return None


def main() -> int:
    try:
        raw = sys.stdin.read()
    except Exception:
        return 0
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    cwd = Path(data.get("cwd") or ".")
    receipt_path = find_receipt(cwd)
    if receipt_path is None:
        return 0  # not a prof-DA report session -> silent

    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except Exception:
        return 0  # unreadable receipt -> never trap

    deliverables = receipt.get("deliverables") or []
    if not deliverables or not SELF_CHECK.is_file():
        return 0  # nothing to validate / cannot validate -> fail-open

    project_dir = receipt_path.parent.parent  # <project>/.prof-da/<receipt> -> <project>

    failures = []
    for rel in deliverables:
        target = project_dir / rel          # absolute rel overrides project_dir in pathlib
        if not target.is_file():
            target = Path(rel)
        if not target.is_file():
            failures.append(f"{rel}: file not found")
            continue
        try:
            res = subprocess.run(
                [sys.executable, str(SELF_CHECK), str(target),
                 "--skip", "orientation", "--skip", "action-brief", "--skip", "ai-tell"],
                capture_output=True, text=True, encoding="utf-8",
            )
        except Exception:
            return 0  # runner error -> fail-open
        if res.returncode != 0:
            detail = ""
            try:
                summ = json.loads(res.stdout)
                fc = summ.get("failed_checks") or []
                if fc:
                    detail = f" (failed: {', '.join(fc)})"
            except Exception:
                pass
            failures.append(f"{rel}{detail}")

    if not failures:
        try:
            receipt_path.unlink()           # passed -> clear, allow stop
        except Exception:
            pass
        return 0

    attempts = int(receipt.get("attempts", 0)) + 1
    receipt["attempts"] = attempts
    try:
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

    if attempts > MAX_ATTEMPTS:
        sys.stderr.write(
            f"[prof-DA gate] self_check STILL failing after {MAX_ATTEMPTS} attempts: "
            f"{'; '.join(failures)}. Allowing stop to avoid a trap, but the deliverable is "
            f"UNVALIDATED. Receipt kept at {receipt_path}.\n"
        )
        return 0

    sys.stderr.write(
        "[prof-DA gate] BLOCKED - a report deliverable failed the report consistency gate: "
        f"{'; '.join(failures)}. Run  python \"{RCA}\" <deliverable>  , fix the HIGH findings "
        "(empty-as-finding / missing scaffold / missing portal receipt / dropped diacritics), then finish. "
        f"The gate clears itself once the consistency gate passes. [attempt {attempts}/{MAX_ATTEMPTS}]\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
