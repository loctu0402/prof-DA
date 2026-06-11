---
description: Professional Data Analyst, submit mode. Final acceptance gate before submitting a recurring report to a team's manager or system (e.g. <report-mcp> MCP). Audits structure completeness vs the team's acceptance contract, routes missing sections to the builder, runs per-section quality_check, emits a ready-to-paste submission payload. Distinct from /review.
---

Invoke the `da` skill in **submit mode**. Read these references before acting:
1. `references/mode-submit.md` the gate workflow (Step 0-6), team-profile model, /review distinction
2. `references/recurring-report-contract.md` the section-contract + DoD + carry-forward pattern
3. `references/report-standard-checklist.md` the global pre-ship gates (run alongside)
4. `references/scripts-guide.md` `section_contract_audit.py` usage (audit / worksheet / payload)

User's submit request: $ARGUMENTS

## Step 1, disambiguate team + report (MANDATORY)

If $ARGUMENTS is empty or vague, ASK:

```
Bạn muốn finalize/submit cho team nào, và file report nào?

  <product> (the savings product) bi-weekly  [default, profile sẵn có: example-team.report-contract.json]
  Team khác                     [cần report-contract.json của team đó, hoặc mình giúp tạo]

File report cần duyệt: <đường dẫn>
```

## Hard principle (state it, then follow it)
- This is a FINAL GATE, not a builder and not a quality review. It ORCHESTRATES: detect missing/incomplete sections, route to `/report` or `/query` to fill, re-audit. It NEVER drafts report content itself, and NEVER calls the submission MCP (the user submits after connecting).

## Workflow
- Load the team's `report-contract.json` (<product>: `references/submit-profiles/example-team.report-contract.json`).
- `python scripts/validators/section_contract_audit.py <report> --contract <contract.json>` until `overall_pass: true`. Route every MISSING/EMPTY/PLACEHOLDER required section to the builder, re-audit. Judge DOD_GAP by eye.
- `--worksheet` to certify per-section quality_check (how content meets each DoD item).
- Confirm carry-forward items addressed.
- `--payload --author "<name>"` to emit the `submit_contribution`-shaped JSON; fill `<FILL>` slots.
- Run `scripts/validators/self_check.py <report>` for the global layer (orientation, AI-tell, action-brief, consistency).
- Run the Step 6 readiness checklist, then STOP and hand the payload to the user. Do NOT submit.
