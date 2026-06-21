#!/usr/bin/env python3
"""Standalone test for the bundled intake + check hooks: detect-and-defer (both directions) and
the Windows stdin-utf-8 fix. No pytest. Run: python hooks/tests/test_monitor_hooks.py."""
import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1]
CHECK = HOOKS / "req_recon_check.py"
INTAKE = HOOKS / "req_recon_intake.py"
SID = "11111111-2222-3333-4444-555555555555"
results = []


def check(name, cond):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name)


def make_env(host_present):
    """ledger dir (REQ_RECON_DIR) and the host-detection home (USERPROFILE) are independent."""
    ledger_dir = tempfile.mkdtemp()
    home = tempfile.mkdtemp()
    env = dict(os.environ)
    env["REQ_RECON_DIR"] = ledger_dir
    env["USERPROFILE"] = home
    env.pop("PYTHONIOENCODING", None)
    if host_present:
        hd = Path(home) / ".claude" / "hooks"
        hd.mkdir(parents=True)
        (hd / "req_recon_check.py").write_text("# host sentinel\n", encoding="utf-8")
    return env


def ledger_path(env, cwd):
    out = subprocess.run(
        [sys.executable, "-c",
         f"import sys; sys.path.insert(0, r'{HOOKS}'); import req_recon_lib as RL; print(RL.ledger_path())"],
        cwd=cwd, env=env, capture_output=True, text=True)
    return out.stdout.strip()


def is_block(out):
    try:
        return json.loads(out.stdout.strip()).get("decision") == "block"
    except Exception:
        return False


# 1. host ABSENT + OPEN + no receipt -> check.py BLOCKS
proj = tempfile.mkdtemp(); env = make_env(host_present=False)
open(ledger_path(env, proj), "w", encoding="utf-8").write("## Requirements\n- [ ] (R2 - OPEN - t1 - sess:11111111) x\n")
out = subprocess.run([sys.executable, str(CHECK)], cwd=proj, env=env,
                     input=json.dumps({"session_id": SID}), capture_output=True, text=True)
check("host absent + OPEN + no receipt -> block", is_block(out))

# 2. host PRESENT -> check.py defers (silent) even with OPEN
proj = tempfile.mkdtemp(); env = make_env(host_present=True)
open(ledger_path(env, proj), "w", encoding="utf-8").write("## Requirements\n- [ ] (R2 - OPEN - t1 - sess:11111111) x\n")
out = subprocess.run([sys.executable, str(CHECK)], cwd=proj, env=env,
                     input=json.dumps({"session_id": SID}), capture_output=True, text=True)
check("host present -> check defers (no block)", out.stdout.strip() == "" and out.returncode == 0)

# 3. intake VN prompt (host absent) -> correct UTF-8 in the ledger, not mojibake
proj = tempfile.mkdtemp(); env = make_env(host_present=False)
lp = ledger_path(env, proj)
prompt = "Làm các việc:\n1. sửa parser tiếng Việt\n2. thêm test\n3. cập nhật README rồi push"
payload = json.dumps({"prompt": prompt, "session_id": SID}, ensure_ascii=False).encode("utf-8")
subprocess.run([sys.executable, str(INTAKE)], cwd=proj, env=env, input=payload, capture_output=True)
raw = open(lp, "rb").read()
check("intake VN -> correct UTF-8 (e1 bb ad = u)", b"\xe1\xbb\xad" in raw)
check("intake VN -> no mojibake (c3 a1 c2 bb)", b"\xc3\xa1\xc2\xbb" not in raw)

# 4. intake host PRESENT -> defers (no seeding, no ledger file)
proj = tempfile.mkdtemp(); env = make_env(host_present=True)
lp = ledger_path(env, proj)
subprocess.run([sys.executable, str(INTAKE)], cwd=proj, env=env, input=payload, capture_output=True)
check("intake host present -> defers (no ledger)", not os.path.exists(lp))

print("---")
ok = all(c for _, c in results)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
