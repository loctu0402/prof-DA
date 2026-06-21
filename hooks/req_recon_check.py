#!/usr/bin/env python3
"""
Stop hook: requirement reconciliation enforcement (tier B of req-recon).

Reads ONLY on-disk markers under ~/.claude/req-recon/ (compaction-proof):
- <session_id>.md          : requirements checklist; an unchecked "- [ ]" line = unreconciled
- <session_id>.state.json  : {block_count, soft_reminded, deferred}
- <session_id>.flag        : intake heuristic flag (written by req_recon_intake.py)

Behavior:
- deferred set               -> one-shot pass (clear it), allow stop
- requirements unreconciled  -> HARD-BLOCK, capped at BLOCK_CAP per episode
- flag but no requirements   -> SOFT-REMIND once (dismissable)
- otherwise                  -> allow (and reset the episode block counter)

Loop safety: the block_count cap guarantees termination independent of
stop_hook_active (which the other Stop hook, session_end_sync, can consume first).
Any error exits 0 so the session is never trapped.
"""
import json
import os
import re
import sys
from pathlib import Path

# Windows cp1252 stdout fix (same pattern as session_end_sync.py)
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")   # else json.load(stdin) decodes a non-ASCII payload as cp1252
    os.environ["PYTHONIOENCODING"] = "utf-8"

def _recon_dir():
    """Resolve <claude_dir>/req-recon robustly. Under Git Bash (how run_hook.sh runs hooks)
    USERPROFILE is stripped and HOME points to the MSYS home, so Path.home() raises and would
    crash the hook at import. Derive the dir from this hook's own location instead."""
    env = os.environ.get("REQ_RECON_DIR")
    if env:
        return Path(env)
    up = os.environ.get("USERPROFILE")   # plugin-safe: user home, never the plugin dir
    if up:
        return Path(up) / ".claude" / "req-recon"
    hd, hp = os.environ.get("HOMEDRIVE", ""), os.environ.get("HOMEPATH", "")
    if hp:
        return Path(hd + hp) / ".claude" / "req-recon"
    try:
        return Path.home() / ".claude" / "req-recon"
    except Exception:
        return Path.cwd() / ".claude" / "req-recon"


RECON_DIR = _recon_dir()
BLOCK_CAP = 2                 # cap once a real reconciliation verdict exists (items may legitimately remain blocked/out-of-scope)
NEVER_RECONCILED_CAP = 4      # higher cap when NO reconciliation was ever attempted (the "ticked / claimed-done without checking" case)
PROJECT_BLOCK_CAP = 3         # project-gate cap: clearing it needs a real independent review, so allow a few blocks before fail-open
KEEP_SESSIONS = 50
# session ids are UUIDs; project ledgers are path-munged keys. prune must touch ONLY session
# files, never the durable (append-only) project ledger / _projects index / review receipts.
UUID_RE = re.compile(r"(?i)^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
UNCHECKED_RE = re.compile(r"(?m)^\s*-\s*\[\s\]")
CHECKED_RE = re.compile(r"(?mi)^\s*-\s*\[x\]")
RECON_SECTION_RE = re.compile(r"(?mi)^\s*#{1,6}\s*Reconcil")


def load_state(session_id):
    p = RECON_DIR / f"{session_id}.state.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"block_count": 0, "soft_reminded": False, "deferred": False}


def save_state(session_id, state):
    try:
        RECON_DIR.mkdir(parents=True, exist_ok=True)
        (RECON_DIR / f"{session_id}.state.json").write_text(
            json.dumps(state), encoding="utf-8"
        )
    except Exception:
        pass


def count_unchecked(session_id):
    """Return number of unchecked '- [ ]' lines, or None if no requirements file."""
    p = RECON_DIR / f"{session_id}.md"
    if not p.exists():
        return None
    try:
        return len(UNCHECKED_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))
    except Exception:
        return None


def _read_md(session_id):
    p = RECON_DIR / f"{session_id}.md"
    if not p.exists():
        return None
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def has_reconciliation(session_id):
    """True if the requirements file carries a '## Reconciliation' verdict section."""
    text = _read_md(session_id)
    return bool(text and RECON_SECTION_RE.search(text))


def has_checked(session_id):
    """True if the file has at least one completed '- [x]' item (real requirements exist)."""
    text = _read_md(session_id)
    return bool(text and CHECKED_RE.search(text))


def load_proj_state(RL):
    """Project-gate state (<project-key>.state.json) - separate from session state so the two
    block counters never collide."""
    try:
        p = RECON_DIR / f"{RL.project_key()}.state.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"block_count": 0}


def save_proj_state(RL, state):
    try:
        RECON_DIR.mkdir(parents=True, exist_ok=True)
        (RECON_DIR / f"{RL.project_key()}.state.json").write_text(json.dumps(state), encoding="utf-8")
    except Exception:
        pass


def prune(current_session_id):
    """Keep the newest KEEP_SESSIONS *session* requirement files (UUID-stemmed) only. NEVER
    touch a project ledger (<project-key>.md), the _projects index, or review receipts - the
    project monitor is append-only and must survive across sessions."""
    try:
        mds = [p for p in RECON_DIR.glob("*.md") if UUID_RE.match(p.stem)]
        mds.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        for old in mds[KEEP_SESSIONS:]:
            sid = old.stem
            if sid == current_session_id:
                continue
            for ext in (".md", ".state.json", ".flag", ".turns"):
                (RECON_DIR / f"{sid}{ext}").unlink(missing_ok=True)
    except Exception:
        pass


def block(reason):
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main():
    # detect-and-defer: the host already runs the monitor -> stay silent (no double-gating)
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from _host_detect import host_monitor_present
        if host_monitor_present():
            sys.exit(0)
    except Exception:
        pass
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if not isinstance(data, dict):   # valid JSON but not the expected object -> fail-open
        sys.exit(0)

    session_id = data.get("session_id", "")
    if not session_id:
        sys.exit(0)

    state = load_state(session_id)
    unchecked = count_unchecked(session_id)  # None = no file, int = unchecked count
    flag_exists = (RECON_DIR / f"{session_id}.flag").exists()

    # 1. One-shot defer escape (pausing to ask the user / not done yet)
    if state.get("deferred"):
        state["deferred"] = False
        save_state(session_id, state)
        print("[req-recon] Deferred once - allowing stop. Reconcile when the task is actually done.", file=sys.stderr)
        prune(session_id)
        sys.exit(0)

    # 1b. PROJECT-KEYED GATE (the durable cross-session monitor). Runs before the legacy
    # session gate: block while THIS project's ledger has OPEN items and no fresh, all-MET
    # review receipt on file. The receipt is written by /req-recon check (an independent
    # review), so this cannot be cleared by self-ticking. Fail-open: any error here must never
    # trap the session, so the whole block is wrapped and block()'s SystemExit propagates out.
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import req_recon_lib as RL
        p_open = RL.count_open()          # None when this cwd has no project ledger
        gate_clear = True
        if p_open:
            ok, why = RL.review_satisfies_open()
            if not ok:
                gate_clear = False
                pstate = load_proj_state(RL)
                if pstate.get("block_count", 0) >= PROJECT_BLOCK_CAP:
                    print(f"[req-recon] project monitor: {p_open} OPEN item(s) still un-reviewed "
                          f"after {PROJECT_BLOCK_CAP} blocks - allowing stop. This is NOT a clean "
                          f"done; tell the user which asks remain open and why.", file=sys.stderr)
                else:
                    pstate["block_count"] = pstate.get("block_count", 0) + 1
                    save_proj_state(RL, pstate)
                    block(
                        f"[req-recon] PROJECT monitor: {p_open} OPEN requirement(s) in this "
                        f"project's ledger are not cleared - {why}. This ledger survives across "
                        f"chat sessions (asks may have been captured in an earlier session). Run "
                        f"/req-recon check to spawn the INDEPENDENT review that diffs each OPEN ask "
                        f"vs git + the on-disk artifacts and writes the all-MET receipt clearing "
                        f"this gate; or /req-recon defer to pause once. Ledger: {RL.ledger_path()}"
                    )
        # gate genuinely clear (no open items, or a fresh all-MET receipt) -> reset the project
        # block counter so a future episode starts fresh. A cap-allow does NOT reset (stays capped).
        if gate_clear:
            pstate = load_proj_state(RL)
            if pstate.get("block_count"):
                pstate["block_count"] = 0
                save_proj_state(RL, pstate)
    except Exception:
        pass  # fail-open: a monitor bug must never trap the session

    has_recon = has_reconciliation(session_id)

    # 2. Hard condition: captured requirements not yet reconciled (unchecked items remain)
    if unchecked is not None and unchecked > 0:
        cap = BLOCK_CAP if has_recon else NEVER_RECONCILED_CAP
        if state.get("block_count", 0) >= cap:
            print(f"[req-recon] {unchecked} requirement(s) still unreconciled after {cap} blocks - allowing stop. "
                  f"This is NOT a clean done: those asks remain open. Tell the user which, and why.", file=sys.stderr)
            prune(session_id)
            sys.exit(0)
        state["block_count"] = state.get("block_count", 0) + 1
        save_state(session_id, state)
        if has_recon:
            block(
                f"[req-recon] {unchecked} requirement(s) still show '- [ ]' after your reconciliation. "
                f"Resolve each (do the work, or strike out-of-scope with a one-line reason), or /req-recon defer "
                f"if genuinely pausing. File: ~/.claude/req-recon/{session_id}.md"
            )
        else:
            block(
                f"[req-recon] {unchecked} captured requirement(s) are NOT reconciled, and NO independent "
                f"reconciliation has run. Do not claim done on ticked boxes alone - that is the "
                f"'70%-done-reported-as-done' failure this guards. Run /req-recon check now: spawn the independent "
                f"subagent to diff the asks in ~/.claude/req-recon/{session_id}.md against `git diff` + the artifacts "
                f"on disk, then record a per-ask MET / PARTIAL / MISSED verdict. If genuinely pausing, /req-recon defer. "
                f"(Hard cap {NEVER_RECONCILED_CAP}.)"
            )

    # 2b. Anti-gaming: every box ticked but no independent reconciliation verdict on file.
    if unchecked == 0 and has_checked(session_id) and not has_recon and not state.get("recon_nudged"):
        state["recon_nudged"] = True
        save_state(session_id, state)
        block(
            f"[req-recon] All boxes are checked, but there is no '## Reconciliation' verdict on file. A clean done "
            f"needs the independent /req-recon check (diff vs `git diff` + artifacts on disk), not just ticked boxes. "
            f"Record the per-ask MET / PARTIAL / MISSED verdict in ~/.claude/req-recon/{session_id}.md, or stop again "
            f"to dismiss if you already verified by hand."
        )

    # 3. Soft condition: heuristic flagged multi-task but nothing was captured
    if unchecked is None and flag_exists and not state.get("soft_reminded"):
        state["soft_reminded"] = True
        save_state(session_id, state)
        block(
            "[req-recon] This session's prompt looked multi-task but no requirements were captured. "
            "If it was multi-task, run /req-recon start to track the asks so they can be reconciled before "
            "you finish. If it was actually single-task, just stop again - you will not be reminded twice."
        )

    # 4. Clean / reconciled / no requirements -> reset the episode block counter, allow
    if state.get("block_count"):
        state["block_count"] = 0
        save_state(session_id, state)
    prune(session_id)
    sys.exit(0)


if __name__ == "__main__":
    main()
