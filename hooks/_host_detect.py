#!/usr/bin/env python3
"""Detect-and-defer: is the HOST workspace already running the project requirement-monitor?

If so, the bundled prof-DA monitor hooks stay SILENT (no double-gating) - the same host-detection
pattern feedback_capture.py uses for the memory loop. Resolution keys on the user-level host hooks
dir (~/.claude/hooks), never a plugin path, so the bundled copy cannot detect itself.
"""
import os
from pathlib import Path


def _host_hooks_dir():
    up = os.environ.get("USERPROFILE")
    if up:
        return Path(up) / ".claude" / "hooks"
    hd, hp = os.environ.get("HOMEDRIVE", ""), os.environ.get("HOMEPATH", "")
    if hp:
        return Path(hd + hp) / ".claude" / "hooks"
    return Path.home() / ".claude" / "hooks"


def host_monitor_present():
    """True when a host-installed monitor (~/.claude/hooks/req_recon_check.py) exists, so the
    bundled copy must defer. Fail-safe to False (run the bundled monitor) on any error."""
    try:
        cand = _host_hooks_dir() / "req_recon_check.py"
        return cand.exists() and "plugins" not in str(cand).replace("\\", "/")
    except Exception:
        return False
