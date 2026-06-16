---
description: prof-DA — master entry. Confirms intent + Detail Level (Quick / Standard / Deep), then routes to 1 of 12 modes.
---

Invoke the `da` skill. The user typed `/prof-DA:da` without a mode — confirm intent + detail level, then route to one of the 12 modes:

**Front-of-workflow:**
- `/prof-DA:frame` — Business Understanding → Metric Define → Data Plan (PLANNING.md)
- `/prof-DA:model` — Data modeling (Kimball / dbt / Medallion / DuckDB layered)

**Standard DA flow:**
- `/prof-DA:query` — Engine-agnostic NL→SQL + 5-tier schema discovery + Step 0 Request Intake
- `/prof-DA:process` — Raw → staged → cleaned → mart → ML-ready (6-step EDA, ExecSum per phase)
- `/prof-DA:insight` — Hypothesis → diagnostic (causal-method matching) → recommendation
- `/prof-DA:automate` — Pipeline setup + email-on-fail + cache discipline
- `/prof-DA:report` — Build stakeholder report from template + chart anatomy + storyline

**Orthogonal helpers:**
- `/prof-DA:deliver` — Build-auto execution loop wrapping any build mode: spec-or-STOP, clean baseline, single batch approval, per-task RED → GREEN → build → commit + verify gate, stop-on-error/risk, evidence summary
- `/prof-DA:submit` — Final acceptance gate before submitting a recurring report to a team system (e.g. <report-mcp> MCP): structure-completeness audit vs the team contract, route missing sections to the builder, per-section quality_check, emit submission payload. <product> profile shipped. Distinct from review.
- `/prof-DA:review` — 3 sub-modes (A Delivery / B Full Project / C Stakeholder Q)
- `/prof-DA:fix` — Surgical pipeline / report debug + patch-ceiling escalation
- `/prof-DA:workspace` — Scaffold / organize / index a whole workspace (guide-first, secrets-first, git-mv-on-branch, index-last)

User's optional context for routing: $ARGUMENTS

**Detail Level Gate** — before routing, ask the user the desired depth using ONLY the option names below. (Agent directives — do NOT echo into the question shown to the user: never surface time estimates; never paste this parenthetical. See style-rules "No Meta-Leak".)
- **Quick** — fastest path, single-pass, minimal validators. Use when speed > completeness.
- **Standard** *(default)* — full workflow, all hard rules, scripts called, validators run.
- **Deep** — Standard + extra validators, falsification, robustness, sensitivity, advanced methods, multi-pass review.

If user's intent maps clearly to one mode, propose it + suggested detail level, ask user to confirm. Otherwise ask 1 question to disambiguate, then invoke.
