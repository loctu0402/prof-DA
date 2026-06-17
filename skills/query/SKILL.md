---
name: query
description: Adhoc data fetch — request intake (Step 0) → SQL → verify. Use this skill when the user asks for any numeric data, breakdowns by dimension, comparisons across cohorts, trends over time, or "give me the numbers for X". Auto-fires on conversational requests in Vietnamese or English. Natural triggers include "cho mình số liệu", "lấy data về X", "check số liệu X", "số liệu của X", "data của X tháng/tuần", "tỷ lệ X", "tỷ lệ phê duyệt", "tỷ lệ giải ngân", "X có bao nhiêu", "tổng X", "trung bình X", "breakdown theo Y", "split theo Y", "chia theo Y", "X theo New/Reloan", "X theo lender / channel / region / tier", "compare X vs Y", "so sánh X với Y", "X tăng/giảm bao nhiêu", "pull data", "show me data", "get the numbers", "fetch", "query", "viết SQL", "NL→SQL", or explicit /prof-DA:query. ALWAYS runs Step 0 Request Intake before SQL, restating the question + surfacing 2-4 implicit choices (grain / cohort / aggregation / dedup / window / comparison / breakdown) + propose calculation logic in plain language + suggest 1-2 extensions + user-confirm gate. Enforces engine-agnostic safety (5-tier schema discovery, BQ Safety Protocol 5-gate, Query Logic Card audit trail, cache verification, read-only enforcement).
---

# Query Mode — Adhoc Data Fetch

For any stakeholder DM that boils down to "give me the numbers for X".

## ALWAYS Step 0 FIRST — Request Intake

Before writing any SQL, run the 5-substep intake (full detail in `references/mode-query.md`):

1. **Restate the question** in one sentence
2. **Surface implicit choices** (grain / cohort / aggregation / dedup / window / comparison / breakdown) — pick the 2-4 that matter, propose defaults
3. **Propose calculation logic** in plain English (NOT SQL)
4. **Suggest 1-2 extensions** the user probably wants (sibling metric / DoD comparison / Top-K / quality caveat)
5. **User confirms** → proceed

Skip Step 0 only if: user pasted explicit SQL, query is repeat of one earlier in session, request is pipeline-internal, or fully-atomic ask with zero implicit choices.

## 4 Quality Rules (apply to output)

1. Orientation Block at top
2. Baseline → Noise → Impact ladder per numeric statement
3. 5W1H Action Brief per recommendation
4. Why-Explanation per choice (method / threshold / engine)

Full: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow

Full 8-step workflow (Step 0 intake → Step 1 engine → ... → Step 7 verification): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-query.md`.

## Hard rules
- Script > Agent compute: NEVER inline statistical work
- Read-only at SQL-parse layer (reject DROP/DELETE/UPDATE/INSERT/ALTER/CREATE)
- For BQ specifically: > 1 month backfill = mandatory dry-run + $ report to user
- For any billed engine: 5-gate BQ Safety Protocol (partition / partition filter / dry-run / cost / unpartitioned warn)

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-query.md`
- Schema-source hierarchy (5-tier): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/schema-source-hierarchy.md`
- Style rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/style-rules.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
