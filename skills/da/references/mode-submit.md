# Submit Mode — Final Acceptance Gate before MCP Submission

> The LAST gate before a recurring report leaves for the team's manager / submission system.
> Checks a finished deliverable against the team's **acceptance contract** (the manager's required
> sections + definition-of-done) and the **submission system's process**, then hands the user a
> ready-to-paste submission payload. The user connects the MCP and submits; this mode does not.

## What submit is (and how it differs from /review)

| | `/prof-DA:review` | `/prof-DA:submit` |
|---|---|---|
| Question | Is this report **GOOD**? (quality, rigor, method maturity, polish) | Is this report **COMPLETE + ACCEPTABLE** per the manager's external contract, and **READY to push** to the system? |
| Bound to | prof-DA's own quality rules (Rules 1-4, rubric) | the **team's acceptance contract** (external — set by the manager / submission guidance) |
| Output | critique + rework worksheet | gap punch-list + filled **submission payload** + readiness checklist |
| When | mid-build, iterating | final, right before connecting the MCP and submitting |

Run `/review` to make it good; run `/submit` to confirm it is shippable to the manager and emit the payload. They do not overlap.

## Hard principle — the gate ORCHESTRATES, it does not GENERATE

A missing section is **routed to the existing builder, then re-audited** — `/submit` never drafts
report content itself (that would make it a second report builder colliding with `/report`). The
gate's job: precise punch-list → route to the right filler → re-run the audit → emit payload.

## Inputs

1. The finished report (`output/.../<report>.md` or `.html`).
2. The team's **acceptance contract** `report-contract.json` (section keys + per-section DoD + `submit_target`). Profiles ship in `references/submit-profiles/`; <product> = `example-team.report-contract.json`.
3. The submission system's process (for <product>: <report-mcp> MCP `submit_contribution` = author + sections + quality_check).

## Workflow

### Step 0 — Identify team + load contract `[GATE]`
- Ask which team / which submission (default offered: **<product> bi-weekly**).
- Load the team's `report-contract.json`. If the user's project has its own copy, prefer that; else copy the shipped profile into the project and confirm the manager's guidance hasn't changed (bump `version` if it has).
- Confirm the report file to gate.

### Step 1 — Structure completeness audit `[GATE]`
```bash
python scripts/validators/section_contract_audit.py <report> --contract report-contract.json
```
Reads the per-section result:
- `MISSING` / `EMPTY` / `PLACEHOLDER` on a required section → **hard fail** (in `missing_required`).
- `DOD_GAP` → advisory (a DoD item not keyword-evident) — surface, judge by eye, fix if real.
- `OK` → section present + complete.

### Step 2 — Gap punch-list + ROUTE to filler (NOT draft here)
For every hard-fail / real DoD-gap, write a one-line punch item and route:
- Missing/empty section, data exists → `/prof-DA:report` (build the section from cache/pipeline) or the team's report pipeline (<product>: the weekly-report builder).
- Missing because data isn't pulled → `/prof-DA:query` to pull it first.
- Placeholder unresolved → wire the real value.
Then **re-run Step 1** until `overall_pass: true`. Do not proceed to submit with a red gate.

### Step 3 — quality_check (per-section self-certification)
```bash
python scripts/validators/section_contract_audit.py <report> --contract report-contract.json --worksheet
```
For each section, write one line on HOW the content satisfies each DoD item (this is the submission
system's required `quality_check`, done offline). Auto-flags ([x]/[ ]) seed it; the analyst certifies.

### Step 4 — Carry-forward check
If the contract has open `carry_forward[]` items, confirm each is addressed in its section (or re-defer with a note). Open items that silently dropped = a submit blocker.

### Step 5 — Build the submission payload
```bash
python scripts/validators/section_contract_audit.py <report> --contract report-contract.json --payload --author "<name>"
```
Emits a `submit_contribution`-shaped JSON (author + sections{key: content} + quality_check{key: justification}). Fill the `<FILL>` justifications + author; resolve any `<MISSING>` (means Step 2 isn't done). This is the artifact the user pastes into the MCP call.

### Step 6 — Submission readiness checklist `[GATE]` (then hand off — do NOT submit)
- [ ] Gate `overall_pass: true` (Step 1 re-run clean).
- [ ] No unrendered placeholder / `N/A` / `TODO` in any section.
- [ ] Vietnamese diacritics complete for stakeholder text; no AI-tells (run `self_check.py` for the global layer too).
- [ ] Every `quality_check` justification filled (no `<FILL>` left).
- [ ] Carry-forward items addressed or re-deferred.
- [ ] Numbers reconcile vs source (no hallucinated figure).
- [ ] Payload `sections` keys == contract keys == MCP guidance keys (1:1).
- [ ] **MCP reachable** — the user can connect the submission server (for <product>: <report-mcp>; note the <organization> web-filter may block `<mcp-host>` at the system layer — see `your workspace reference` in the workspace).

Then **STOP and hand the payload to the user.** `/submit` never calls the MCP `submit_contribution` itself — submission is the user's explicit action after they connect. (Same discipline as report mode's NEVER-auto-send.)

## <product> weekly — the concrete profile

- Contract: `references/submit-profiles/example-team.report-contract.json` (7 sections, guidance v3: business_overview / satisfaction / cross_sell / segment_a_contribution / segment_b_contribution / segment_c_contribution / new_initiatives).
- Submit target: <report-mcp> MCP `submit_contribution` (keys map 1:1).
- **Cadence note:** the <report-mcp> acceptance contract runs **bi-weekly** (e.g. cycle W24 = 2 weeks). If the team also has a separate *weekly* artifact with different sections, point submit at that report file but keep this contract as the acceptance criteria unless the manager's guidance differs — then bump `version`.
- Section builders live in the <product> report pipeline (`projects/automated-report-flow/` weekly build); route missing sections there, do not draft in submit.

## Adding another team (thin — no speculative machinery)

1. Drop `references/submit-profiles/<team>.report-contract.json` (section keys = the team's submission-system guidance keys; DoD per section).
2. Note the team's `submit_target` (which MCP / channel + payload shape).
3. The Step 0-6 workflow is identical; only the contract + target change. Do not build per-team code.

## Cross-references
- The contract pattern + DoD + carry-forward: `recurring-report-contract.md`
- The audit/worksheet/payload script: `scripts-guide.md` → `section_contract_audit.py`
- Planning the contract (Section Contract beside Metric Contract): `planning-protocol.md` Gate 2.4
- Global quality layer (run alongside): `self-check-protocol.md`, `report-standard-checklist.md`
- <report-mcp> submission process + tool schemas: `your workspace reference/` in the workspace

— part of prof-DA · Loc Tu, 2026
