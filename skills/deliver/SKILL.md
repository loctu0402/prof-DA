---
name: deliver
description: Chunked autonomous build loop (build-auto) that wraps any build mode with execution discipline. Require a spec/charter or STOP, clean baseline, single batch approval, then per-task RED -> GREEN -> build -> commit with a verify gate, stop-on-failure/risk/irreversible, and an honest evidence summary. Orthogonal to process/report/model/automate (the HOW execution-control layer, not the WHAT). Distilled from addyosmani agent-skills /build auto. Use when executing a heavy approved DA build as a sequence of tasks, or on "build it autonomously", "chunk and commit per task", "deliver this end to end", "/build auto", or explicit /prof-DA:deliver.
---

# Deliver Mode, Chunked Autonomous Build Loop

Execution CONTROL for a heavy approved build. It does not decide WHAT to build (that is frame); it runs
the build as a sequence of tasks, each committed and verified, stopping on failure or risk. The
force-multiplier for autonomous work that does NOT drop the verification.

> `/process` etc. build the thing · `/deliver` runs the build with gates so any stopping point is a clean,
> proven, single-commit rollback.

## Hard principle
deliver ORCHESTRATES the build; it never skips the per-task verify gate and never takes an irreversible
step without an explicit confirm.

## Workflow (full detail: `references/build-auto.md`)
0. **Spec / contract or STOP** `[GATE]`: a charter / metric contract / section contract on disk, else STOP and route to `/frame` or `/report`.
1. **Clean baseline** `[GATE]`: `git status` clean (or explicit dirty-ack); existing validators green.
2. **Plan into tasks**: atomic tasks, each with a one-line verify check.
3. **Single approval** `[GATE]`: present the whole list ONCE; an unambiguous batch yes (a hedge is not approval).
4. **Per-task RED -> GREEN -> build -> commit**: RED = the failing validator/acceptance check; 1 task = 1 commit; stage only that task's files; never `git add -A`.
5. **Per-task verify gate** `[GATE]`: run the check; a red gate STOPS the loop.
6. **Stop-on-failure / risk / irreversible** `[GATE]`: the DA stop-list (prod write, billed backfill > 1 month, auto-send, schema cutover, force-push); surface, wait, resume.
7. **Doubt pass + Summarize** `[GATE]`: run a doubt pass on the headline claims (`references/execution-discipline.md` section 6: CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP, bias-to-disprove); drop `<project>/.prof-da/pending-validation.json`, run `artifact_presence_check.py`, give an honest evidence ledger (note anything the doubt pass downgraded).

## Hard rules
- NEVER auto-send / publish a stakeholder deliverable; emit + hand to the user.
- 1 task = 1 commit; never sweep unrelated work into a task commit.
- An irreversible step needs an explicit confirm + the proof gate first.
- Run the global pre-ship layer (`self_check.py`) when the build is a report.
- If the build must be reproducible / scale / run elsewhere (a harness / pipeline / eval), its DoD is code + unit test + a CLI + a cross-machine/model proof — NEVER a markdown "flow" (`references/evidence-based-done.md` reproducible-form gate).

## Cross-references
- Execution loop: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/build-auto.md`
- Proof gate: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/evidence-based-done.md`
- Mindset: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/execution-discipline.md`
- Where DELIVER sits: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/delivery-lifecycle.md`
- Presence validator: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/scripts-guide.md`, see `artifact_presence_check.py`
