"""DESIGN STUB - platform-neutral gate core (Layer 3 mechanism-parity anchor).

The single neutral function every platform's gate adapter calls. This is the receipt-walk + per-deliverable
check + attempt counting from hooks/stop_gate.py, with the Claude-specific stdin / exit-2 stripped out.

[PORT FROM hooks/stop_gate.py]:
  - find the receipt (<project>/.prof-da/pending-validation.json) by walking up from a start dir
  - for each named deliverable run the presence/proof check (reuse
    skills/da/scripts/validators/artifact_presence_check.py logic) + the report consistency audit
  - count attempts (fail-open after MAX_ATTEMPTS), return a Verdict (do NOT exit/print here - the
    per-platform adapter decides how to block)

Once built, hooks/stop_gate.py becomes a thin Claude adapter that imports this (apply-after-coordination
with the governance hooks). Until then this raises so a caller cannot mistake the stub for a working gate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Verdict:
    passed: bool
    failures: list = field(default_factory=list)
    attempts: int = 0


def gate_core(receipt_path: str | Path) -> Verdict:
    """Return a Verdict for the deliverables named in the receipt. Platform-free (no stdin, no exit)."""
    raise NotImplementedError(
        "DESIGN STUB - port the receipt-walk + per-deliverable check from hooks/stop_gate.py "
        "and skills/da/scripts/validators/artifact_presence_check.py. Build deferred."
    )
