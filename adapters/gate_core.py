"""Platform-neutral gate core (Layer 3 mechanism-parity anchor).

The single neutral function every platform's gate adapter calls (git pre-commit, a CI step, a Cursor
rule, the agent's final tool call). No stdin, no exit, no print - it returns a Verdict and the
per-platform adapter decides how to block. `gate.py` is the CLI wrapper.

Two checks, merged:
  1. requirement-monitor  - the project's append-only SCD2 ledger has no OPEN item left un-cleared by a
     fresh all-MET review receipt (req_recon_lib). This is the portable half of prof-DA's "2nd brain".
  2. report-consistency   - if a report receipt (.prof-da/pending-validation.json) names deliverables,
     each passes self_check (ported from hooks/stop_gate.py's loop; stop_gate stays the Claude Stop
     adapter and is NOT modified - a later pass can DRY the two).

Fail-open everywhere: any internal error -> passed (a buggy gate must never brick a commit/session).
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

RECEIPT_REL = Path(".prof-da") / "pending-validation.json"
SELF_CHECK = Path(__file__).resolve().parent.parent / "skills" / "da" / "scripts" / "validators" / "self_check.py"


@dataclass
class Verdict:
    passed: bool
    failures: list = field(default_factory=list)
    attempts: int = 0


def find_receipt(start):
    """Walk up from `start` for a report receipt, or None."""
    try:
        cur = Path(start).resolve()
        for d in [cur, *cur.parents]:
            cand = d / RECEIPT_REL
            if cand.is_file():
                return cand
    except Exception:
        pass
    return None


def requirement_monitor_verdict(cwd=None) -> Verdict:
    """Verdict from the project requirement-monitor: passed unless an OPEN item lacks a fresh all-MET
    review receipt. Fail-open (passed) if the monitor lib is unavailable."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
        import req_recon_lib as RL
        ok, why = RL.review_satisfies_open(cwd)
        return Verdict(passed=bool(ok), failures=[] if ok else [f"requirement-monitor: {why}"])
    except Exception:
        return Verdict(passed=True)


def report_consistency_verdict(receipt_path) -> Verdict:
    """Port of hooks/stop_gate.py's deliverable validation, platform-free (no stdin/exit). Runs
    self_check on each named deliverable. Fail-open on any runner/parse error."""
    try:
        receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    except Exception:
        return Verdict(passed=True)
    deliverables = receipt.get("deliverables") or []
    attempts = int(receipt.get("attempts", 0))
    if not deliverables or not SELF_CHECK.is_file():
        return Verdict(passed=True, attempts=attempts)
    project_dir = Path(receipt_path).parent.parent
    failures = []
    for rel in deliverables:
        target = project_dir / rel
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
            return Verdict(passed=True, attempts=attempts)  # runner error -> fail-open
        if res.returncode != 0:
            detail = ""
            try:
                fc = json.loads(res.stdout).get("failed_checks") or []
                if fc:
                    detail = f" (failed: {', '.join(fc)})"
            except Exception:
                pass
            failures.append(f"{rel}{detail}")
    return Verdict(passed=not failures, failures=failures, attempts=attempts)


def gate_core(receipt_path=None, cwd=None) -> Verdict:
    """The merged neutral gate: requirement-monitor (always) + report-consistency (when a receipt is
    given or found by walking up from cwd). Platform-free. Fail-open on any internal error."""
    try:
        failures = []
        attempts = 0
        rv = requirement_monitor_verdict(cwd)
        failures += rv.failures
        rp = receipt_path or find_receipt(cwd or ".")
        if rp:
            cv = report_consistency_verdict(rp)
            failures += cv.failures
            attempts = cv.attempts
        return Verdict(passed=not failures, failures=failures, attempts=attempts)
    except Exception:
        return Verdict(passed=True)
