"""The portable gate CLI (Layer 3): `python adapters/gate.py [<receipt>]` (or `python -m gate` from
adapters/). The single command every non-Claude platform calls to enforce evidence-based-done (a git
pre-commit, a CI step, a Cursor rule, or the agent's final tool call). Exit 0 = proven, 2 = not done.

Thin wrapper over gate_core - no logic of its own. The receipt arg is optional: with it, the report
receipt is checked explicitly; without it, gate_core walks up from cwd for one AND always runs the
requirement-monitor check. Fail-open: any error here -> exit 0 (a buggy gate must never block a commit).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_core import gate_core


def main() -> int:
    try:
        receipt = sys.argv[1] if len(sys.argv) > 1 else None
        verdict = gate_core(receipt_path=receipt, cwd=os.getcwd())
        if not verdict.passed:
            sys.stderr.write(
                "[prof-DA gate] BLOCKED - not done:\n  - " + "\n  - ".join(verdict.failures) + "\n"
            )
            return 2
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
