---
name: da-query
description: Engine-agnostic NL→SQL workflow with RECALL→EXPLORE→LEARN loop, BQ Safety Protocol 5-gate, Query Logic Card audit trail, cache verification. Triggers on "viết SQL", "query data", "lấy data", "NL→SQL", or /da-query.
---

# DA Query Mode

Engine-agnostic NL→SQL workflow for any DA task that needs data from a warehouse.

## 4 Universal Rules (apply to all output)

1. **Orientation Block** — every deliverable opens with SCQR / 3-line intro / module docstring.
2. **Baseline → Noise → Impact Ladder** — every numeric statement passes 3 rungs (baseline + noise check + impact verdict). Use `scripts/stats/baseline_noise_impact.py`.
3. **Question → Goal → 5W1H Action Brief** — every recommendation has 8 fields. Use `scripts/validators/action_brief.py`.
4. **Why-Explanation (META)** — every action / method / threshold / tool choice has 1-line Why (Causal / Empirical / Comparative / Theoretical / Operational).

Full rules: `${CLAUDE_PLUGIN_ROOT}/skills/prof-data-analyst/references/universal-workflow-rules.md`.

## Mode workflow

Full workflow (7 steps with BQ Safety Protocol + Query Logic Card): `${CLAUDE_PLUGIN_ROOT}/skills/prof-data-analyst/references/mode-query.md`.

Key points:
- RECALL existing memory before writing SQL
- Semantic-first discovery (Cube.js / dbt-metrics / <org-sql-agent> / LookML) before raw SQL
- Self-correction loop with error_count ≤ 3
- BQ Safety Protocol: partition check → query w/ filter → dry-run → cost gate → unpartitioned warn
- Append Query Logic Card to project query_log.md after success

## Hard rules
- Script > Agent compute: NEVER inline statistical work
- Read-only at SQL-parse layer (reject DROP/DELETE/UPDATE/INSERT/ALTER/CREATE)
- For BQ specifically: > 1 month backfill = mandatory dry-run + $ report to user

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/prof-data-analyst/references/mode-query.md`
- Style rules: `${CLAUDE_PLUGIN_ROOT}/skills/prof-data-analyst/references/style-rules.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/prof-data-analyst/references/self-check-protocol.md`
