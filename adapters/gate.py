"""DESIGN STUB - the portable gate CLI (Layer 3). `python -m gate <receipt>` (or `python adapters/gate.py`).

The single command every non-Claude platform calls to enforce evidence-based-done (git pre-commit, a CI
step, a Cursor alwaysApply rule, or the agent's final tool call). Wraps gate_core; exit 0 = proven,
2 = not done. Thin: no logic of its own.

[FILL when built]: argparse for <receipt>; call gate_core(receipt); print failures to stderr;
sys.exit(0 if verdict.passed else 2). Build deferred (depends on gate_core, which is also a stub).
"""
from __future__ import annotations

import sys


def main() -> int:
    raise NotImplementedError(
        "DESIGN STUB - wrap adapters/gate_core.py: parse <receipt>, call gate_core, exit 0/2. "
        "For a working presence check today, use skills/da/scripts/validators/artifact_presence_check.py."
    )


if __name__ == "__main__":
    sys.exit(main())
