# Build-Auto (chunked autonomous delivery for DA pipelines)

> The execution loop the `deliver` mode runs: a heavy approved build executed as a sequence of tasks,
> each committed and verified, stopping on failure / risk. Distilled from addyosmani/agent-skills
> `/build auto`. Self-contained. Companions: `evidence-based-done.md` (the per-task proof gate),
> `execution-discipline.md` (the mindset), `planning-protocol.md` (the upstream charter / contract).

## Grain and scope
One unit = one delivery run of an approved DA build (a pipeline, a multi-table model, a multi-section
report, an automation). In scope: the 7-gate loop + the stop conditions. Out of scope: an ad-hoc single
query (-> query mode), schema design (-> model mode), a one-shot chart.

## When to read (routing triggers)
- IF executing an approved multi-step DA build as a sequence of tasks -> this loop.
- IF a single query / one chart / a quick fix -> do it inline; this loop has overhead.
- DO NOT use this to decide WHAT to build (that is frame / the charter).

## The 7 gates
0. Spec / contract or STOP. Require a frame charter OR a metric contract OR a section contract on disk. Absent -> STOP and route to `/frame` or `/report`. Do not invent requirements.
1. Clean baseline. `git status` clean (or an explicit dirty-ack); existing validators green before starting. Do not absorb unrelated local work into per-task commits.
2. Plan into tasks. Decompose into atomic tasks, each with a one-line verify check.
3. Single approval. Present the whole task list ONCE; the user approves the batch (not each task). A hedged reply is NOT approval. This is the only human gate after this point.
4. Per-task RED -> GREEN -> build -> commit. RED = write the failing check (a validator / acceptance test / a baseline-noise-impact threshold / a parallel-trends test that currently fails). GREEN = make it pass. build = render the artifact / run the pipeline step. commit = 1 task = 1 commit; stage only that task's files; never `git add -A`.
5. Per-task verify gate. Run the task's check (`evidence-based-done.md`). A red gate STOPS the loop; do not advance.
6. Stop-on-failure / risk / irreversible. Halt and surface (do not push through) on a check that will not pass without an obvious fix, an ambiguous spec, a materialized RAID risk, or an irreversible step ahead (the DA stop-list below). After the user resolves, resume from the next pending task.
7. Doubt pass + Summarize. Before the ledger, run a doubt pass on the headline claims (`execution-discipline.md` section 6: CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP, bias-to-disprove, no doubt-theater) - the adversarial complement to the per-task evidence gate. Then write an honest evidence ledger (tasks completed, checks added, commits made, anything downgraded by the doubt pass or flagged), not a green-washed summary.

## The DA irreversibility stop-list
Any of these requires an explicit confirm + the proof gate BEFORE acting:
- a production table write or a schema cutover / migration;
- a billed backfill larger than ~1 month;
- auto-send / publish of a stakeholder report (NEVER auto-send: emit + hand to the user);
- a cache wipe that destroys regenerable-only-with-cost state;
- git push to a shared / live branch; force-push; delete / rename a referenced file.

## Receipt integration
The deliver mode drops `<project>/.prof-da/pending-validation.json` naming each committed artifact, so
the plugin Stop hook (`stop_gate.py`) validates the deliverables with no extra wiring. The per-task
proof marker is what `evidence-based-done.md` rung 4-5 requires.
