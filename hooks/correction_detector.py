#!/usr/bin/env python3
"""
prof-DA learning loop - UserPromptSubmit hook: real-time correction catch.

The Stop hook (feedback_capture.py) is end-of-session. This one is the REAL-TIME catch the
host loop has no equivalent for: when the user's current message looks like a correction of a
previously-established practice ("you forgot", "we always do X", "dù đã làm nhiều lần"), it
injects a non-blocking note telling the agent to resolve it AND persist it IMMEDIATELY (not
wait for session end) so the same forgetting cannot recur.

It only ADDS context (never blocks). Fail-open: any error -> add nothing, never disrupt the
prompt. Silent unless the prompt actually contains a correction signal.

- part of prof-DA . Loc Tu, 2026
"""
from __future__ import annotations
import json
import sys

# Correction signals in the CURRENT user message (high context precision) - lowercased.
SIGNALS = [
    "you forgot", "forgot to", "we always", "we usually", "always do it",
    "as i told you", "i already told", "i told you", "like last time",
    "remember we", "remember to", "you keep forgetting",
    "sai rồi", "sai r", "không phải vậy", "không phải thế", "khong phai",
    "luôn làm", "luon lam", "lâu nay", "lau nay", "đã làm nhiều lần", "da lam nhieu lan",
    "dù đã", "du da", "lần nào cũng", "lan nao cung", "nhắc lại", "nhac lai",
    "sao lại quên", "sao lai quen", "quên rồi à", "từ giờ", "tu gio",
    "phải nhớ", "phai nho", "ghi nhớ", "ghi nho",
]

NOTE = (
    "[prof-DA learning] The user's message looks like a correction of a previously-established "
    "practice or a forgotten convention. After you resolve the request: (1) persist the corrected "
    "fact / convention / preference to memory IMMEDIATELY - do not wait for session end; (2) if it is "
    "a forgotten established practice, update the relevant skill / instruction / CLAUDE.md via a "
    "visible Edit so it cannot recur. See references/learning-protocol.md. Skip silently if this is "
    "not actually a correction."
)


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    prompt = (data.get("prompt") or "").lower()
    if not prompt or not any(s in prompt for s in SIGNALS):
        return 0   # not a correction -> add nothing

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": NOTE,
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
