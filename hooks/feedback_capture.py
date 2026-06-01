#!/usr/bin/env python3
"""
prof-DA learning loop - Stop hook: remind the agent to capture this session's feedback.

DETECT-AND-DEFER (the key design choice): if the host already runs its OWN memory loop
(e.g. ~/.claude/hooks/session_end_sync.py or memory_store_reminder.py), this hook stays
SILENT. The host's loop owns memory capture; prof-DA must not double-remind. For a user
WITHOUT such a loop, this is the only one - it nudges the agent to persist any feedback /
new rule / corrected fact / "you forgot X" from the session so future runs personalise.

The hook NEVER writes memory itself (a shell script cannot distill a conversation). It
NAMES the best memory target and BLOCKS with a reminder; the AGENT does the distillation
and the edit (see references/learning-protocol.md). This mirrors the host session_end_sync
pattern exactly: hook injects a checklist, agent executes.

Targeted + low-noise: fires when the transcript shows a high-precision correction phrase,
else a 1-in-4 catch-all. Dedup per session, stop_hook_active guard, fail-open (any error
-> allow the stop; a buggy hook must never trap a session).

- part of prof-DA . Loc Tu, 2026
"""
from __future__ import annotations
import json
import os
import random
import sys
from pathlib import Path

HOME = Path.home()
# Host already has its own memory loop -> defer (stay silent).
HOST_LOOP_SIGNALS = [
    HOME / ".claude" / "hooks" / "session_end_sync.py",
    HOME / ".claude" / "hooks" / "memory_store_reminder.py",
]
DEFER_SENTINEL = HOME / ".claude" / ".prof-da-no-learning-loop"   # manual opt-out
STATE_FILE = HOME / ".claude" / "prof_da_learning_state.json"
CATCH_ALL_PROBABILITY = 1 / 4

# HIGH-PRECISION correction phrases (rare in normal flow) - lowercased substring match.
STRONG_SIGNALS = [
    "you forgot", "we always do", "we usually do", "as i already told",
    "i told you before", "like last time", "lan nao cung", "lần nào cũng",
    "dù đã làm", "du da lam", "đã làm nhiều lần", "da lam nhieu lan",
    "luôn làm", "luon lam", "sao lại quên", "sao lai quen",
]


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict) -> None:
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def host_loop_present() -> bool:
    if DEFER_SENTINEL.exists():
        return True
    return any(p.exists() for p in HOST_LOOP_SIGNALS)


def transcript_has_strong_signal(path: str) -> bool:
    if not path or not os.path.exists(path):
        return False
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return False
    return any(s in text for s in STRONG_SIGNALS)


def memory_target(cwd: Path) -> str:
    for d in [cwd, *cwd.parents]:
        if (d / "lt-memory").is_dir():
            return str(d / "lt-memory" / "feedback") + "  (your lt-memory feedback dir)"
    cm = HOME / ".claude" / "CLAUDE.md"
    if cm.exists():
        return str(cm) + "  (user CLAUDE.md)"
    return str(cwd / ".prof-da" / "learned") + "  (project-local; create it)"


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    if data.get("stop_hook_active"):
        return 0
    if host_loop_present():
        return 0   # host owns memory capture -> defer, stay silent

    session_id = data.get("session_id", "unknown")
    state = load_state()
    if state.get("last_session_id") == session_id:
        return 0   # already reminded this session

    fire = transcript_has_strong_signal(data.get("transcript_path", "")) or random.random() < CATCH_ALL_PROBABILITY
    if not fire:
        return 0

    state["last_session_id"] = session_id
    save_state(state)

    target = memory_target(Path(data.get("cwd") or "."))
    reason = (
        "[prof-DA learning] Before finishing, capture anything durable from this session so it "
        "personalises future runs (you do the distillation - this is a reminder, not an auto-writer):\n"
        f"  1. Persist any new rule / corrected fact / preference to: {target}\n"
        "     Keep it tight, deduped, cross-linked. Qualify hard - do NOT bloat memory.\n"
        "  2. If the user pointed out a FORGOTTEN established practice (\"we always do X\", \"you forgot\"), "
        "ALSO update the relevant skill / instruction / CLAUDE.md via a visible Edit so it cannot recur.\n"
        "  3. See references/learning-protocol.md for what qualifies + how.\n"
        "If nothing here is durable, say 'Nothing worth storing.' and finish."
    )
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
