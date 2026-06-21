#!/usr/bin/env python3
"""Standalone test for the bundled req_recon_lib (no pytest; stdlib only).
Run: python hooks/tests/test_req_recon_lib.py  (exit 0 = all pass)."""
import os
import sys
import time
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # hooks/
import req_recon_lib as RL

results = []


def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)


# --- recon_dir adaptation (the plugin-safe resolution) ---
td = tempfile.mkdtemp()
os.environ["REQ_RECON_DIR"] = td
check("recon_dir honors REQ_RECON_DIR", str(RL.recon_dir()) == td)

os.environ.pop("REQ_RECON_DIR", None)
d = str(RL.recon_dir()).replace("\\", "/")
check("recon_dir resolves to user ~/.claude/req-recon", d.endswith("/.claude/req-recon"))
check("recon_dir is NOT the plugin path", "plugins" not in d and "marketplace" not in d)

# --- ported behavior (open_ids / review_satisfies_open / write_review) ---
os.environ["REQ_RECON_DIR"] = td
proj = tempfile.mkdtemp()
ledger = RL.ledger_path(proj)
ledger.write_text(
    "# x\n## Requirements\n"
    "- [-] (R1 - DEFERRED - t1) neutralized\n"
    "- [~] (R9 - SUPERSEDED-by-R2 - t1) old\n"
    "- [x] (R8 - DONE - t1->t2) done\n"
    "- [ ] (R2 - OPEN - t2) build | DoD: x | AC: y\n"
    "- [ ] (R3 - OPEN - t2) write | DoD: x | AC: y\n",
    encoding="utf-8",
)
check("open_ids excludes DONE/SUPERSEDED/DEFERRED", sorted(RL.open_ids(proj)) == ["R2", "R3"])

ok, why = RL.review_satisfies_open(proj)
check("no receipt -> blocked", ok is False and "receipt" in why.lower())

RL.write_review([{"id": "R2", "status": "MET"}, {"id": "R3", "status": "MET"}], session_id="s", cwd=proj)
base = time.time()
os.utime(ledger, (base, base))
os.utime(RL.review_receipt_path(proj), (base + 50, base + 50))
ok, why = RL.review_satisfies_open(proj)
check("fresh all-MET -> allowed", ok is True)

os.utime(RL.review_receipt_path(proj), (base - 50, base - 50))
ok, why = RL.review_satisfies_open(proj)
check("stale receipt -> blocked", ok is False and "stale" in why.lower())

RL.write_review([{"id": "R2", "status": "MET"}, {"id": "R3", "status": "MISSED"}], cwd=proj)
os.utime(ledger, (base, base))
os.utime(RL.review_receipt_path(proj), (base + 50, base + 50))
ok, why = RL.review_satisfies_open(proj)
check("one not-MET -> blocked", ok is False and "R3" in why)

print("---")
ok_all = all(c for _, c in results)
print("ALL PASS" if ok_all else "SOME FAILED")
sys.exit(0 if ok_all else 1)
