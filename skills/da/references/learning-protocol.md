# Learning Protocol — capture feedback + kill recurring forgetting

prof-DA personalises itself from conversation. Two bundled hooks trigger this; **you (the agent) do the work** (a hook is a shell script, it cannot distill a conversation). This doc is what you follow when a hook fires, or any time you notice a durable signal.

## The two triggers
- **`hooks/correction_detector.py` (UserPromptSubmit, real-time):** fires the moment the user's message looks like a correction ("you forgot", "we always do X", "dù đã làm nhiều lần"). Act on it IMMEDIATELY (step 2 below), do not wait for session end.
- **`hooks/feedback_capture.py` (Stop, session-end):** a catch-all reminder to persist anything durable before finishing. **Detect-and-defer:** it stays silent when the host already runs its own memory loop (e.g. `~/.claude/hooks/session_end_sync.py`) — that host loop owns capture, prof-DA must not double-remind.

## Step 0 — find the memory target (detect, don't assume)
prof-DA ships no memory of its own and assumes no fixed path. Resolve in this order:
1. An existing **`lt-memory/`** up the tree → write a feedback/knowledge atom there (follow that repo's llm-wiki contract).
2. Else a **`CLAUDE.md`** (project root, then `~/.claude/CLAUDE.md`) → add a tight rule line.
3. Else **`<project>/.prof-da/learned/`** → create it and write a dated note.
If a host memory system clearly owns this (its own hooks/skills), **defer to it** — use its workflow, don't fork a parallel store.

## Step 1 — qualify HARD (the anti-bloat bar)
Persist only what is **reusable, recurring, and non-obvious**. A durable signal is one of:
- a **rule / preference** the user stated ("always force light-mode email", "đỏ đô theme for X"),
- a **corrected fact** (a metric grain, a schema gotcha, a tool recipe),
- a **forgotten established practice** the user had to remind you of.
Do NOT store: transient task chatter, one-off values, anything already in memory, or "lessons" that are generic best-practice. When unsure, it is not durable. If nothing qualifies, say "Nothing worth storing." and move on.

## Step 2 — persist + (for forgetting) fix the instruction
- **Distill** to one tight atom/line: what + why + a one-line case. Dedup against what exists; cross-link, never re-paste (llm-wiki contract). Keep atoms small.
- **If it was a FORGOTTEN established practice, memory is not enough** — the forgetting will recur unless the *instruction* changes. So ALSO update the place the agent reads next time: the relevant `SKILL.md` / mode reference / `CLAUDE.md`. **Make that edit yourself, via the normal visible Edit flow** (reversible, reviewable) — never let a hook blind-write an instruction file. Example: "user keeps getting PPT when the convention is HTML slides" → add "slides = HTML, never .pptx (unless asked)" to the relevant skill/project CLAUDE.md, not just a memory note.

## Step 3 — confirm in one line
Report what you stored + where, in one line (e.g. "Stored: email always force-light-mode → lt-memory/feedback/…; also added the rule to mode-report Step 1."). No essay.

## Why instruction-fix, not just memory
Memory that is only *recalled* can still be missed; an *instruction* in the skill the agent loads for that task is read every time. A recurring forgetting (the same correction twice) is the signal that the fix belongs in the instruction layer, not only the memory layer. Persist the fact AND close the path that let it recur.

## Boundaries
- The hooks are **reminders + real-time flags**, not auto-writers. You decide what is durable and you make every edit.
- On any doubt about the memory target or whether a host loop owns capture, ask the user once rather than forking a parallel memory store.
