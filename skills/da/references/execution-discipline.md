# Execution Discipline (anti-rationalization, verify-don't-assume, scope)

> The honesty + verification layer for every mode. `coding-discipline.md` is coding CRAFT; this is
> HONESTY: do not rationalize past a hard step. Distilled from addyosmani/agent-skills. Self-contained
> (no external pointers). Companions in this plugin: `evidence-based-done.md` (the proof gate),
> `build-auto.md` (the execution loop), `universal-workflow-rules.md` (Rule 2 numeric rigor).

## Grain and scope
One unit = one agent decision-point during a DA task (assume vs check, claim-done vs prove, fold-in vs
flag). In scope: the mindset every mode applies. Out of scope: chart style, SQL dialect, sample sizing.

## When to read (routing triggers)
- IF about to write "done / fixed / passing / shipped" -> read this + `evidence-based-done.md` first.
- IF about to assume a column, a grain, a freshness, that a file is complete -> verify, do not assume.
- IF tempted to skip a validator / a template fork / a check because it is "quick" -> the table below.
- DO NOT use this for: how to format a chart, which SQL engine, how to size a sample.

## 1. Core operating behaviors (non-negotiable)
1. Surface assumptions before any non-trivial build; let the user correct them. Silent assumption-filling is the top failure mode.
2. Manage confusion actively: on an inconsistency, STOP, name it, present the tradeoff or question, wait. No guessing forward.
3. Push back, no sycophancy: name a concrete problem, give the downside, propose an alternative, accept an informed override.
4. Enforce simplicity: fewer lines, fewer abstractions; would a senior say "why didn't you just...".
5. Scope discipline: touch only what the captured ask traces to; flag an out-of-scope find as a separate task.
6. Verify, don't assume: a task is not complete until verification passes; "seems right" is never enough (see section 2).

## 2. Verify, don't assume (DA evidence)
- Schema is checked, never assumed (owner-tag -> catalog -> cube -> INFORMATION_SCHEMA -> sample). A column "should exist" is a guess until queried.
- Grain is counted: `COUNT(*) = COUNT(DISTINCT key)` proves one-row-per-key; a glob of files is not proof.
- Freshness is read from the data (mart lag is real), not assumed.
- Ran is not correct: a query returning rows is not a validated number; the strongest proof is correcting a real wrong number on live data (before / after).
- Cache is not source: verify a cached value against the mart before reuse.

## 3. Scope discipline
One request = one scope. The surgical-change test: every changed line traces to the captured ask. An
adjacent improvement gets FLAGGED, never folded into the current diff (it inflates the diff and breaks review).

## 4. Anti-rationalization table
Each row: the excuse used to skip a hard step, why it is wrong, the disciplined move.

| The excuse | Why it is wrong | The disciplined move |
|---|---|---|
| "The script / packager exists, so the artifact is built." | A packager existing is not a packaged artifact. | RUN it, open the output, count files. See `evidence-based-done.md` (built-but-unrun). |
| "The query ran and returned rows, so the number is validated." | Rows are not correctness. | Validate by correcting a real wrong number on live data (before / after). |
| "I inferred the grain / the column is surely there." | Inference is a guess until counted / queried. | `COUNT(*) = COUNT(DISTINCT key)`; check the schema source. Glob is not proof. |
| "The subagent reported done, so it is done." | The same context that drops a thing is blind to the drop. | Verify the real file / repo; never let a subagent summary override the user's explicit instruction. |
| "The Vietnamese prose has plenty of diacritics, presence-check passed." | Presence-count misses half-diacritized files. | Token-scan (strip code, count khong/duoc/cua/...); restore before ship. |
| "I cloned the repo, so I have all the in-scope files." | A sparse / partial clone silently drops in-scope files. | Full clone; corroborate scope against the architecture doc, not whatever files exist. |
| "It is a small ask, I can skip the gate." | Past turn 3 / multi-ask, silent drops are exactly where this bites. | Capture the ask; reconcile before done. |
| "I will just design the report myself, it is faster." | Freestyle ships a generic off-brand dashboard. | Fork a locked archetype; implement the approved visual 1:1. |
| "Mock / sample data is fine to show the flow." | Mock-data-as-real is an over-claim. | Scale real caches or label it explicitly; never present fabricated as live. |
| "Files exist, so the handoff is ready." | Exists is not discoverable / self-contained. | Update the index; keep the package self-contained (no pointer to a private store). |
| "I rendered it / read the file, it looks right." | "Looks right" is not evidence for a visual. | Rasterize headless (absolute path) or inspect geometry; route the looks-good call to the user. |
| "The email draft is created, so it is sent." | A draft is not a send. | Use the real send path with attachments; confirm recipients (sending is a one-way door). |
| "I will improve this adjacent thing while I am here." | Out-of-scope edits inflate the diff. | Flag it as a separate task; touch only what the ask traces to. |

## 5. Red flags (stop and re-check)
"glob is proof" / "the script exists so it ran" / "presence-count passed" / "the subagent said done" /
"the sparse clone looks complete" / "I will update the template later" / "run the build again to be sure"
(after a clean run with no code change, repeating adds nothing).

## 6. Doubt pass (adversarial self-review before a high-stakes claim)

The anti-rationalization table catches the excuse; the doubt pass catches the wrong-but-confident result.
It is the adversarial COMPLEMENT to `evidence-based-done.md`: evidence asks "do I have proof at the rung I
claim" (positive); the doubt pass asks "did I actively try to DISPROVE this" (negative). Adopted from the
addyosmani/agent-skills doubt-driven-development device.

Run it before a decision-driving number, a causal conclusion, a stakeholder deliverable, or the deliver-mode
Gate 7 (before the evidence summary). Five steps:

1. **CLAIM** - state the exact thing you are about to ship as true/done ("AUM dropped 12% because the scheme ended").
2. **EXTRACT** - break it into the specific checkable sub-claims (the number, the grain, the freshness, the causal link, the completeness).
3. **DOUBT** - for EACH sub-claim, switch to a fresh-context skeptic and try to BREAK it: what would make this wrong? what did I assume? a confound, a stale source, a miscount, a cherry-picked window, a missing cohort? Default to "doubted" when you cannot refute the doubt.
4. **RECONCILE** - keep what survives; FIX or DOWNGRADE what does not (e.g. "X caused Y" -> "X correlates with Y; causation unverified"); flag the open items.
5. **STOP** - bounded to <=3 doubt cycles; converge or escalate. Do not loop forever.

**Anti "doubt theater":** a pass that rubber-stamps every claim is itself a failure. Each sub-claim needs a
concrete refutation ATTEMPT, not a nod. If a complex claim survives with nothing found, that is suspicious -
doubt harder or get a second pass. In review mode this is Sub-mode B's adversarial core; in deliver mode it
runs at Gate 7; for a single number it is one quick CLAIM->DOUBT->RECONCILE.

## Validator
`python scripts/validators/anti_rationalization_check.py <plan-or-task-list.md>` flags a task missing a
verify check, an irreversible action without a STOP marker, or a red-flag phrase in agent-authored prose.
