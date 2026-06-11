---
name: submit
description: Final acceptance gate before submitting a recurring report to a team's manager or submission system (e.g. <report-mcp> MCP). Checks the finished deliverable against the team's acceptance contract (required sections plus per-section definition-of-done), actions missing sections by routing to the builder, runs the per-section quality_check, and emits a ready-to-paste submission payload. Distinct from /review (which judges quality); submit judges COMPLETENESS, ACCEPTABILITY, and submit-readiness. First team profile is the savings product  bi-weekly. Use this skill whenever the user is about to submit or finalize a recurring report into a system, or asks "da du muc chua", "fit yeu cau quan ly chua", "finalize truoc khi submit", "submit report", "duyet lan cuoi truoc khi nop", or explicit /prof-DA:submit.
---

# Submit Mode, Final Acceptance Gate

The LAST gate before a recurring report goes to the team manager or submission system. NOT a quality
refine (that is `/review`); this verifies the report is **complete plus acceptable per the manager's
external contract** and **ready to push**, then hands the user a fill-ready submission payload.

> `/review` asks: is this GOOD? · `/submit` asks: is this COMPLETE, ACCEPTABLE, and READY to submit?

## Hard principle
The gate **orchestrates, it does not generate.** A missing section is routed to the existing builder
(`/report` or the team pipeline) then re-audited; submit never drafts report content itself, and
never calls the submission MCP itself (submission is the user's explicit action after they connect).

## Workflow (full detail: `references/mode-submit.md`)

0. **Identify team plus load contract** `[GATE]`: default offer is <product> bi-weekly. Load `report-contract.json` (team's required sections plus DoD). Profiles: `references/submit-profiles/`.
1. **Structure audit** `[GATE]`: `section_contract_audit.py <report> --contract <c.json>`. MISSING / EMPTY / PLACEHOLDER on a required section is a hard fail; DOD_GAP is advisory.
2. **Gap punch-list plus ROUTE**: for each fail, one-line punch item, route to `/report` (build section) or `/query` (pull data); re-run Step 1 until `overall_pass: true`. NEVER draft here.
3. **quality_check**: `--worksheet`, certify per-section how content meets each DoD item (the submission system's required self-check, offline).
4. **Carry-forward**: confirm open items addressed or re-deferred.
5. **Build payload**: `--payload --author "<name>"`, emits `submit_contribution`-shaped JSON (author plus sections plus quality_check) to fill then paste into the MCP call.
6. **Readiness checklist** `[GATE]` then **STOP plus hand payload to user**: gate green, no placeholder, diacritics plus no AI-tells, all quality_check filled, keys map 1:1 to MCP guidance, MCP reachable. Do NOT submit.

## <product> weekly (concrete profile)
- Contract: `references/submit-profiles/example-team.report-contract.json` (7 sections, guidance v3).
- Target: <report-mcp> MCP `submit_contribution` (keys 1:1). <organization> web-filter may block `<mcp-host>`; flag it, the user submits from a reachable network.
- Missing sections routed to the <product> weekly-report pipeline; submit does not draft them.

## Hard rules
- Distinct from `/review`: do not re-run quality critique here; assume the report was built plus reviewed. Submit checks acceptance, completeness, and readiness only.
- Orchestrate, never generate; route missing sections to the builder, re-audit.
- NEVER call the submission MCP: emit the payload, stop, hand to the user (same discipline as report mode NEVER-auto-send).
- Run the global layer too (`self_check.py`); submit's contract audit is the per-section layer, not a replacement.

## Cross-references
- Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-submit.md`
- Contract pattern: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/recurring-report-contract.md`
- Audit/payload script: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/scripts-guide.md`, see `section_contract_audit.py`
- <product> profile: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/submit-profiles/example-team.report-contract.json`
- Global pre-ship gates: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/report-standard-checklist.md`
