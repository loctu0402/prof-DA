#!/usr/bin/env python3
"""
UserPromptSubmit hook: requirement-reconciliation intake nudge (tier A of req-recon).

On a prompt that looks multi-task (heuristic), this hook:
- writes ~/.claude/req-recon/<session_id>.flag (so the Stop hook can soft-remind if
  no requirements get captured), and
- injects a one-line nudge to run /req-recon start.

It NEVER blocks. The heuristic has real false positives/negatives, so this is only a
soft nudge; the Stop hook (req_recon_check.py) is the actual backstop. Any error exits 0.
"""
import json
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")   # else json.load(stdin) decodes a VN prompt as cp1252 -> mojibake
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
LONG_PROMPT = 800
NUMBERED_RE = re.compile(r"(?m)^\s*\d+[.)]\s")
BULLET_RE = re.compile(r"(?m)^\s*[-*]\s")
CONNECTORS = [
    "sau đó", "tiếp theo", "tiếp đó", "ngoài ra", "thêm nữa", "thêm vào đó",
    "đồng thời", "cuối cùng", "đầu tiên", "thứ nhất", "thứ hai", "thứ ba",
    "bên cạnh đó", "song song", "rồi thì",
    "then", "also", "additionally", "next", "finally", "first", "second",
    "third", "furthermore", "moreover",
]

# Harness-injected turns are NOT user asks. Seeding from one is the R1 garbage-capture bug (a
# <task-notification> got logged as a requirement). Strip closed blocks; skip a turn that is
# entirely / predominantly such content.
SYSTEM_TAG_RE = re.compile(
    r"(?is)<(task-notification|system-reminder|command-name|command-message|command-args|"
    r"local-command-stdout|local-command-stderr)\b.*?(</\1>|$)")
SYSTEM_LEAD_RE = re.compile(
    r"(?i)^\s*<(task-notification|local-command-stdout|local-command-stderr|command-name|"
    r"command-message|command-args)\b")


def strip_system_blocks(text):
    """Remove harness-injected tag blocks so only genuine user text drives detection + seeding."""
    return SYSTEM_TAG_RE.sub(" ", text)


def is_system_injected(prompt):
    """True when the turn is a harness injection (background task-notification, slash-command
    expansion, local-command output), not a user ask - so the monitor must not seed from it."""
    if SYSTEM_LEAD_RE.match(prompt):
        return True
    return len(strip_system_blocks(prompt).strip()) < 8


def count_connectors(low):
    n = 0
    for c in CONNECTORS:
        if c.isascii() and " " not in c:
            if re.search(rf"\b{re.escape(c)}\b", low):
                n += 1
        elif c in low:
            n += 1
    return n


def detect_signals(prompt):
    signals = []
    if len(prompt) > LONG_PROMPT:
        signals.append("long")
    if NUMBERED_RE.search(prompt):
        signals.append("numbered-list")
    if len(BULLET_RE.findall(prompt)) >= 2:
        signals.append("bullets")
    if count_connectors(prompt.lower()) >= 3:
        signals.append("connectors")
    return signals


ASK_NUM_RE = re.compile(r"(?m)^\s*\d+[.)]\s+(.+)$")
ASK_BUL_RE = re.compile(r"(?m)^\s*[-*]\s+(.+)$")


def parse_asks(prompt):
    """Conservative split of a multi-task prompt into candidate asks (a SEED the agent
    refines). Numbered list wins; else bullets; else the whole prompt as one item."""
    asks = [m.strip() for m in ASK_NUM_RE.findall(prompt) if m.strip()]
    if not asks:
        asks = [m.strip() for m in ASK_BUL_RE.findall(prompt) if m.strip()]
    if not asks:
        asks = [" ".join(prompt.split())[:200]]
    return asks[:12]


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

    prompt = data.get("prompt", "") or ""
    session_id = data.get("session_id", "")
    if not prompt or not session_id:
        sys.exit(0)

    # Skip harness-injected turns (task-notification / slash-command expansion / command output);
    # they are not user asks and must never seed the monitor (the R1 garbage-capture).
    if is_system_injected(prompt):
        sys.exit(0)
    user_prompt = strip_system_blocks(prompt)   # drive detection + seeding off the user text only

    signals = detect_signals(user_prompt)
    if not signals:
        sys.exit(0)

    # Write the flag so the Stop hook can soft-remind if nothing gets captured.
    try:
        RECON_DIR.mkdir(parents=True, exist_ok=True)
        (RECON_DIR / f"{session_id}.flag").write_text(
            json.dumps({"signals": signals, "len": len(prompt)}), encoding="utf-8"
        )
    except Exception:
        pass

    # PROJECT-KEYED MONITOR: seed the project ledger with the detected asks (write-enforced,
    # not just a nudge). Append-only; the agent refines the seeded items. Fail-open.
    seeded = []
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import req_recon_lib as RL
        turn = RL.bump_turn()
        seeded = RL.append_items(parse_asks(user_prompt), turn)
    except Exception:
        seeded = []

    if seeded:
        nudge = (
            f"[req-recon] Multi-task prompt detected ({', '.join(signals)}). I SEEDED "
            f"{len(seeded)} ask(s) into this PROJECT's monitor ledger "
            f"(~/.claude/req-recon/<project-key>.md, append-only, survives across sessions). "
            f"Now: REFINE each seeded item (verbatim ask + DoD + AC), and as feedback arrives "
            f"APPEND new asks + tag any reversed one SUPERSEDED-by-Rn (never delete). Reconcile "
            f"via /req-recon check before claiming done. Rule: lt-memory/rules/requirement-monitor.md."
        )
    else:
        nudge = (
            f"[req-recon] Multi-task prompt detected ({', '.join(signals)}). MANDATORY before "
            f"substantive work: run /req-recon start to capture EACH discrete ask verbatim into the "
            f"ledger, each with its DoR + DoD + AC + Expected + Presence. On every later feedback turn, "
            f"APPEND new asks to the same ledger (never replace); reconcile before claiming done "
            f"(rules: lt-memory/rules/requirement-reconciliation.md + governance-injection.md)."
        )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": nudge,
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
