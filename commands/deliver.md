---
description: Professional Data Analyst, deliver mode. The chunked autonomous build loop (build-auto) that wraps any build mode with execution discipline: require a spec/charter or STOP, clean baseline, single batch approval, then per-task RED -> GREEN -> build -> commit with a verify gate, stop-on-failure/risk/irreversible, and an evidence summary. Orthogonal to process/report/model/automate (it is the HOW, not the WHAT).
---

Invoke the `da` skill in **deliver mode**. Read these references before acting:
1. `references/build-auto.md` the 7-gate execution loop + the DA irreversibility stop-list
2. `references/evidence-based-done.md` the per-task proof gate (the evidence ladder + Presence-proof)
3. `references/execution-discipline.md` the anti-rationalization + verify-don't-assume mindset
4. `references/delivery-lifecycle.md` where DELIVER sits in the 7-phase spine

User's deliver request: $ARGUMENTS

## Hard principle (state it, then follow it)
- deliver is execution CONTROL, not a content generator. It wraps a build mode (process / report / model
  / automate) with the gates. It NEVER skips the verify gate, NEVER does an irreversible step without an
  explicit confirm, and produces an honest evidence ledger (not a green-washed summary).

## Workflow (full detail: `references/build-auto.md`)
0. Gate 0: require a charter / metric contract / section contract on disk. Absent -> STOP, route to `/frame` or `/report`.
1. Gate 1: clean `git status` (or an explicit dirty-ack); existing validators green.
2. Gate 2: decompose into atomic tasks, each with a one-line verify check.
3. Gate 3: present the whole task list ONCE, get an unambiguous batch approval. A hedged reply is NOT approval.
4. Gate 4: per task RED -> GREEN -> build -> commit (1 task = 1 commit; stage only that task's files; never `git add -A`).
5. Gate 5: run the task's verify check; a red gate STOPS the loop.
6. Gate 6: stop-on-failure / risk / irreversible (the DA stop-list); surface and wait, then resume from the next task.
7. Gate 7: drop `<project>/.prof-da/pending-validation.json` naming each committed artifact; run `scripts/validators/artifact_presence_check.py` on it; summarize (tasks, checks, commits, anything flagged).

## Hard rules
- NEVER auto-send / publish a stakeholder deliverable (same discipline as report mode); emit + hand to the user.
- A production write / billed backfill > 1 month / schema cutover / cache wipe / force-push needs an explicit confirm first.
- Run the global pre-ship layer too (`scripts/validators/self_check.py`) when the build is a report.
