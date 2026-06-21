#!/usr/bin/env python3
"""Standalone test for the functional gate_core requirement-monitor check (no pytest).
Run: python adapters/tests/test_gate_core.py."""
import os
import sys
import time
import tempfile
from pathlib import Path

ADAPTERS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ADAPTERS))
sys.path.insert(0, str(ADAPTERS.parent / "hooks"))
import gate_core
import req_recon_lib as RL

results = []


def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)


def seeded(open_item=True):
    td = tempfile.mkdtemp()
    os.environ["REQ_RECON_DIR"] = td
    proj = tempfile.mkdtemp()
    body = "## Requirements\n" + ("- [ ] (R2 - OPEN - t1) x\n" if open_item else "- [x] (R2 - DONE - t1) x\n")
    RL.ledger_path(proj).write_text(body, encoding="utf-8")
    return proj


# 1. OPEN + no receipt -> requirement verdict fails
proj = seeded(True)
v = gate_core.requirement_monitor_verdict(cwd=proj)
check("OPEN + no receipt -> requirement fails", v.passed is False and bool(v.failures))

# 2. OPEN + fresh all-MET receipt -> requirement passes
proj = seeded(True)
RL.write_review([{"id": "R2", "status": "MET"}], cwd=proj)
base = time.time()
os.utime(RL.ledger_path(proj), (base, base))
os.utime(RL.review_receipt_path(proj), (base + 50, base + 50))
v = gate_core.requirement_monitor_verdict(cwd=proj)
check("OPEN + fresh all-MET -> requirement passes", v.passed is True)

# 3. gate_core (no report receipt) merges requirement verdict -> blocked when OPEN
proj = seeded(True)
v = gate_core.gate_core(receipt_path=None, cwd=proj)
check("gate_core OPEN + no-receipt -> not passed", v.passed is False)

# 4. gate_core all clear (no open items) -> passed
proj = seeded(False)
v = gate_core.gate_core(receipt_path=None, cwd=proj)
check("gate_core no-open -> passed", v.passed is True)

print("---")
ok = all(c for _, c in results)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
