#!/usr/bin/env python3
"""
Shared helpers for the PROJECT-KEYED requirement monitor (req_recon_intake.py +
req_recon_check.py). Re-keys the req-recon ledger from chat-session UUID to a stable
project key, so a multi-session task keeps one living append-only checklist.

SCD2 line schema (append-only; status changes edit the tag only, text is never removed):
  - [ ] (R7 - OPEN - t12) <ask> | DoD: ... | AC: ...
  - [x] (R3 - DONE - t4->t9) <ask>
  - [~] (R5 - SUPERSEDED-by-R7 - t6) <old ask>     # context only, not active work
  - [-] (R2 - DEFERRED - t3) <ask>

Everything here is fail-safe: any error returns a benign default so a hook never crashes.
Spec: lt-memory/rules/requirement-monitor.md
"""
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path


def _atomic_write(p, content):
    """Write `content` to `p` atomically: a per-pid temp file in the same dir + os.replace. A
    killed/interrupted write (hook 10s timeout, a concurrent session) then NEVER leaves a
    truncated / 0-byte file - the observed torn-write that wiped a shared project ledger.
    os.replace is atomic on Windows + POSIX when source and dest share a directory. Best-effort."""
    tmp = None
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + f".tmp{os.getpid()}")
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, p)
        return True
    except Exception:
        try:
            if tmp is not None and tmp.exists():
                tmp.unlink()
        except Exception:
            pass
        return False


def recon_dir():
    """Resolve <claude_dir>/req-recon robustly (Git Bash strips USERPROFILE; Path.home() can
    raise). Derive from this file's own location first."""
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


def project_root(cwd=None):
    """The project root = git toplevel of cwd, else cwd. cwd defaults to the process cwd
    (hooks run with cwd = the workspace the user is in)."""
    base = Path(cwd) if cwd else Path.cwd()
    try:
        out = subprocess.run(
            ["git", "-C", str(base), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip())
    except Exception:
        pass
    return base


def project_key(cwd=None):
    """Stable per-project key = the project root path with [:\\/. ] -> '-' (the SAME
    convention Claude Code uses for ~/.claude/projects/<hash>/). Same project -> same key
    in every session, which is what makes the monitor survive across chats."""
    root = str(project_root(cwd))
    # replace EACH separator char (not runs) so ":\\" -> "--", matching the convention
    # Claude Code uses for ~/.claude/projects/<hash>/ (e.g. C--Users-<u>-Desktop-<ws>).
    key = re.sub(r"[:\\/.\s]", "-", root).strip("-")
    return key or "unknown-project"


def ledger_path(cwd=None):
    return recon_dir() / f"{project_key(cwd)}.md"


def review_receipt_path(cwd=None):
    return recon_dir() / f"{project_key(cwd)}.review.json"


# --- SCD2 parsing -----------------------------------------------------------
OPEN_RE = re.compile(r"(?mi)^\s*-\s*\[\s\]\s*\(R\d+\s*-\s*OPEN\b")
# bare unchecked box (the agent/skill may write plain "- [ ]" without the tag yet)
BARE_UNCHECKED_RE = re.compile(r"(?m)^\s*-\s*\[\s\]")
DONE_RE = re.compile(r"(?mi)^\s*-\s*\[x\]")
RECON_SECTION_RE = re.compile(r"(?mi)^\s*#{1,6}\s*Reconcil")
ID_RE = re.compile(r"\(R(\d+)\b")


def read_ledger(cwd=None):
    p = ledger_path(cwd)
    if not p.exists():
        return None
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def count_open(cwd=None, session_id=None):
    """Number of OPEN items, session-scoped when session_id is given (None if no ledger)."""
    if read_ledger(cwd) is None:
        return None
    return len(open_ids(cwd, session_id))


def has_reconciliation(cwd=None):
    text = read_ledger(cwd)
    return bool(text and RECON_SECTION_RE.search(text))


def has_done(cwd=None):
    text = read_ledger(cwd)
    return bool(text and DONE_RE.search(text))


def next_id(cwd=None):
    text = read_ledger(cwd) or ""
    ids = [int(m) for m in ID_RE.findall(text)]
    return (max(ids) + 1) if ids else 1


def ensure_ledger(cwd=None, title=None):
    """Create the project ledger with a header if missing, OR self-heal it if a torn write left
    it 0-byte (restores structure so later appends have a section; cannot recover lost lines).
    Returns the path."""
    p = ledger_path(cwd)
    try:
        missing_or_empty = (not p.exists()) or p.stat().st_size == 0
    except Exception:
        missing_or_empty = not p.exists()
    if missing_or_empty:
        try:
            root = project_root(cwd)
            header = (
                f"# Requirement monitor - {title or root.name}\n\n"
                f"> Project: `{root}`  -  key: `{project_key(cwd)}`\n"
                f"> Append-only (SCD2). Statuses: OPEN / DONE / SUPERSEDED-by-Rn / DEFERRED. "
                f"Never delete an item; tag it. Spec: lt-memory/rules/requirement-monitor.md\n\n"
                f"## Requirements\n"
            )
            _atomic_write(p, header)
            _touch_projects_index(cwd)
        except Exception:
            pass
    return p


def bump_turn(cwd=None):
    """Monotonic per-project turn counter (a `<key>.turns` file). Used to tag when each ask
    was captured. Returns the new turn number; fail-safe to 0."""
    try:
        rd = recon_dir(); rd.mkdir(parents=True, exist_ok=True)
        p = rd / f"{project_key(cwd)}.turns"
        n = 0
        if p.exists():
            try:
                n = int(p.read_text(encoding="utf-8").strip() or "0")
            except Exception:
                n = 0
        n += 1
        _atomic_write(p, str(n))
        return n
    except Exception:
        return 0


def append_items(asks, turn, cwd=None, session_id=None):
    """Append each ask as a new OPEN item with a fresh id. Uses O_APPEND (mode 'a') instead of a
    read-modify-write of the whole file, so a CONCURRENT session's append is never lost and a
    torn write can never truncate the ledger (the observed 0-byte wipe of a project-shared
    ledger). Concurrent appends may collide on the id counter (cosmetic duplicate Rn) but never
    drop content. asks = list[str]; returns the ids written. No-op-safe on any error."""
    if not asks:
        return []
    try:
        ensure_ledger(cwd)               # creates header, or self-heals a 0-byte ledger, ending in \n
        p = ledger_path(cwd)
        nid = next_id(cwd)
        lines, written = [], []
        sess = f" - sess:{session_id[:8]}" if session_id else ""
        for ask in asks:
            ask1 = " ".join(str(ask).split())[:300]
            lines.append(f"- [ ] (R{nid} - OPEN - t{turn}{sess}) {ask1} | DoD: [fill] | AC: [fill]")
            written.append(nid)
            nid += 1
        block = "\n".join(lines) + "\n"
        with open(p, "a", encoding="utf-8") as f:
            f.write(block)               # atomic append; the ledger invariant (ends in \n) holds by construction
        return written
    except Exception:
        return []


def _touch_projects_index(cwd=None):
    """Maintain ~/.claude/req-recon/_projects.md : key -> path, so monitored projects are
    discoverable."""
    try:
        rd = recon_dir()
        rd.mkdir(parents=True, exist_ok=True)
        idx = rd / "_projects.md"
        key, root = project_key(cwd), project_root(cwd)
        line = f"- `{key}` -> `{root}`\n"
        if idx.exists():
            cur = idx.read_text(encoding="utf-8", errors="ignore")
            if key in cur:
                return
            _atomic_write(idx, cur.rstrip("\n") + "\n" + line)
        else:
            _atomic_write(idx, "# Monitored projects (req-recon, project-keyed)\n\n" + line)
    except Exception:
        pass


# --- review receipt (the Stop-gate's done proof) ---------------------------
# The project Stop gate (req_recon_check.py) blocks while any OPEN item exists AND no fresh,
# all-MET review receipt is present. The receipt is written by `/req-recon check` after a
# SEPARATE read-only subagent diffs each OPEN ask against git + on-disk artifacts. Schema:
#   {"project_key": "...", "reviewed_at": "YYYY-MM-DD HH:MM", "session_id": "...",
#    "verdict": "ALL_MET" | "GAPS",
#    "items": [{"id": "R3", "status": "MET|PARTIAL|MISSED", "evidence": "..."}]}
# Freshness is judged by the receipt FILE's mtime vs the ledger's mtime, not a self-reported
# timestamp, so the working agent cannot back-date a receipt to beat a later edit.
OPEN_ID_RE = re.compile(r"(?mi)^\s*-\s*\[\s\]\s*\(R(\d+)\s*-\s*OPEN\b")


def ledger_mtime(cwd=None):
    """mtime of the project ledger file, or None if absent."""
    p = ledger_path(cwd)
    try:
        return p.stat().st_mtime if p.exists() else None
    except Exception:
        return None


SESS_RE = re.compile(r"sess:([0-9A-Za-z-]{4,})")


def _line_is_session(line, session_id):
    """True if an OPEN line is tagged for THIS session. An untagged legacy line is NOT this session's
    -> excluded from the gate (grandfathered), which stops a parallel session's debt from blocking you."""
    sm = SESS_RE.search(line)
    return bool(sm and session_id.startswith(sm.group(1)))


def open_ids(cwd=None, session_id=None):
    """Currently-OPEN requirement ids. With session_id, only items tagged `sess:<id>` for THIS session
    count (untagged legacy items are grandfathered = excluded) so the GATE blocks only on the current
    session's asks. Without session_id (SessionStart surfacing) ALL OPEN items return (cross-session)."""
    text = read_ledger(cwd)
    if text is None:
        return []
    ids = []
    for i, line in enumerate(text.splitlines()):
        m = OPEN_ID_RE.match(line)
        if m:
            if session_id is None or _line_is_session(line, session_id):
                ids.append("R" + m.group(1))
        elif session_id is None and BARE_UNCHECKED_RE.match(line) and not re.search(r"\(R\d+", line):
            ids.append(f"bare-{i}")
    return ids


def read_review(cwd=None):
    """Parse the project review receipt <key>.review.json, or None on absence / parse error."""
    p = review_receipt_path(cwd)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def review_satisfies_open(cwd=None, session_id=None):
    """Does the on-disk review receipt clear the project gate? Returns (ok: bool, reason: str).
    ok=True only when a receipt exists, is FRESH (its file mtime is newer than the ledger's, so
    the review ran after the last requirement change), and reports EVERY currently-OPEN id as
    MET. Any untagged bare '- [ ]' line keeps the gate closed (it cannot be matched by id)."""
    open_set = open_ids(cwd, session_id)
    if not open_set:
        return True, "no open items"
    rec = read_review(cwd)
    if rec is None:
        return False, "no review receipt on file (run /req-recon check)"
    try:
        rmt = review_receipt_path(cwd).stat().st_mtime
        lmt = ledger_mtime(cwd) or 0
        if rmt < lmt:
            return False, "review receipt is stale (the ledger changed after the last review)"
    except Exception:
        return False, "cannot compare receipt/ledger mtimes"
    bare = [x for x in open_set if x.startswith("bare-")]
    if bare:
        return False, (f"{len(bare)} untagged '- [ ]' line(s) cannot be verified by id; "
                       f"refine them into (R<n> - OPEN) items first")
    status_by_id = {}
    for it in (rec.get("items") or []):
        rid = str(it.get("id", "")).strip()
        if rid:
            status_by_id[rid] = str(it.get("status", "")).strip().upper()
    missing = [rid for rid in open_set if status_by_id.get(rid) != "MET"]
    if missing:
        return False, f"{len(missing)} open item(s) not MET in the receipt: {', '.join(missing[:8])}"
    return True, "all open items MET in a fresh receipt"


def _now_str():
    try:
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def write_review(items, session_id=None, cwd=None):
    """Write the project review receipt (<key>.review.json) that clears the Stop gate. `items` =
    list of {"id","status","evidence"} from the INDEPENDENT /req-recon check review. Freshness is
    judged by this file's mtime vs the ledger's, so writing it stamps 'now'. Returns the path."""
    p = review_receipt_path(cwd)
    norm = [{"id": str(i.get("id", "")).strip(),
             "status": str(i.get("status", "")).strip().upper(),
             "evidence": str(i.get("evidence", ""))[:500]} for i in (items or [])]
    payload = {
        "project_key": project_key(cwd),
        "reviewed_at": _now_str(),
        "session_id": session_id or "",
        "verdict": "ALL_MET" if norm and all(i["status"] == "MET" for i in norm) else "GAPS",
        "items": norm,
    }
    _atomic_write(p, json.dumps(payload, ensure_ascii=False, indent=2))
    return p
