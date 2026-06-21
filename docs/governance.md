# prof-DA Governance — the agent as your second brain

prof-DA's differentiator is not a smarter answer; it is a **work environment that remembers and
verifies**. An ordinary agent answers from a blank context, calls it done, and forgets your correction
by the next session. prof-DA turns the agent into a persistent second brain with three guarantees:

1. **Capture** — every ask is written down at intake, verbatim, before work starts.
2. **Never forget** — the asks live in an append-only ledger that survives across chat sessions; a new
   session continues them instead of restarting blank.
3. **Independent done-review** — work is not "done" until a separate review pass confirms every ask was
   met against the artifacts on disk — not the same context that did the work ticking its own boxes.

## The requirement monitor (the load-bearing piece)

A **project-keyed, append-only SCD2 requirement ledger** at `~/.claude/req-recon/<project-key>.md`.

- **Capture (intake).** On a multi-task prompt, the `req_recon_intake` hook seeds the ledger with each
  detected ask as an `OPEN` item. It skips harness-injected turns (a task-notification, a slash-command
  expansion) so it never logs a non-ask.
- **SCD2 status, never deleted.** Each item carries a status tag — `OPEN` / `DONE` / `SUPERSEDED-by-Rn`
  / `DEFERRED`. A reversed ask is tagged `SUPERSEDED`, never erased, so the ledger is the project's full
  audit trail of what changed and why.
- **Survives sessions.** It is keyed by PROJECT, not chat session, so a task spanning many sessions
  keeps one living checklist. On SessionStart the open items are surfaced into context, so a fresh
  session picks them up instead of dropping them at the session boundary.
- **Independent done-review gate.** The Stop hook blocks a turn from ending while any `OPEN` item lacks
  a **fresh, all-MET review receipt** (`<project-key>.review.json`). That receipt is written by
  `/req-recon check`, which spawns a SEPARATE read-only review that diffs each ask against `git diff` +
  the on-disk artifacts and records MET / PARTIAL / MISSED. Ticking boxes does not clear the gate — only
  a genuine independent verdict does. Freshness is judged by the receipt file's mtime vs the ledger, so
  appending a new ask after a review re-arms the gate.
- **Durable under concurrency.** Atomic writes (temp + `os.replace`) and append-mode item writes mean
  concurrent sessions sharing the project ledger never lose or truncate it; a 0-byte ledger self-heals.

## Portable enforcement (every platform, not just Claude Code)

The monitor's enforcement is carried by the platform-neutral **gate** so it runs everywhere:

```
python adapters/gate.py [<receipt>]    -> exit 0 = done, 2 = not done
```

`adapters/gate_core.py` runs the requirement-monitor check (OPEN items must be cleared by a fresh
all-MET receipt) alongside the report-consistency check. On **Claude Code** the full loop is automated
by hooks (seed → surface → Stop-gate). On a **hookless platform** (Codex, Gemini, Cursor) there is no
per-turn hook, so the agent maintains the ledger as instructed by `AGENTS.md` and the gate enforces it
at the best available trigger — a git pre-commit, a CI step, or the final tool call. Same contract,
different automation level; the README and `AGENTS.md` do not over-claim live enforcement off Claude.

## Detect-and-defer (no double-gating)

If the host workspace already runs this monitor (a `~/.claude/hooks/req_recon_check.py` is installed,
e.g. by the `workspace-brain` system), prof-DA's bundled hooks stay silent and defer to the host — the
same host-detection `feedback_capture.py` uses for the memory loop. A user without that host gets the
full monitor from prof-DA alone.

## The rest of the governance suite (augmented, not replaced)

The monitor is the new flagship; it sits beside the existing layer:

- **`stop_gate`** — the report-consistency gate (a `report`-mode deliverable must pass `self_check`).
- **`feedback_capture` + `correction_detector`** — the learning loop: a correction you give becomes a
  permanent rule, captured in real time and at session end (deferring to a host memory loop if present).
- **The per-task contract** — DoR / DoD / AC injected by depth, layered specs, 1-task-1-commit chunked
  delivery, verify-don't-assume + the anti-rationalization checklist (`skills/da/references/`).

Together: an agent that captures what you asked, keeps it across sessions, computes (never eyeballs) its
numbers, forks a locked report template, and refuses to call any of it done until an independent pass
proves it — on whichever agent platform you run.
