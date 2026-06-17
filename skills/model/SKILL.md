---
name: model
description: Data modeling pipeline mode — pick from 4 patterns (Kimball Star/Snowflake / dbt staging→marts / Medallion Bronze-Silver-Gold / DuckDB layered) + design schema + write Table Contracts + plan governance hooks. Use this skill whenever the user needs to design tables, schema, mart, or pipeline structure. Auto-fires on natural Vietnamese + English. Natural triggers include "data model", "data modeling", "design schema", "design DWH", "build DWH", "build mart", "setup mart", "build pipeline mới", "build pipeline mới từ đầu", "dbt project", "dbt staging", "Kimball star", "Medallion", "Bronze Silver Gold", "Bronze/Silver/Gold", "DuckDB layered", "DWH layered", "stg_ clean_ mart_", "table contract", "grain", "schema này có nên", "chia bảng thế nào", "nên build mart gì", "model lại dữ liệu", or explicit /prof-DA:model. Schema design only — statistical / ML prediction asks (forecast, dự đoán, time series, seasonal, churn scoring) belong to /prof-DA:process. Outputs Table Contracts (grain + PK + partition + SLA + owner + downstream + metric coverage) + routes to governance + orchestration.
---

# Model Mode — Pipeline Schema Design

Design the data modeling layer of a pipeline. 4 industry-standard patterns; pick based on infrastructure + scale.

## 4 Quality Rules (apply to all output)

1. **Orientation Block** — schema doc (Table Contract) opens with business definition.
2. **Baseline → Noise → Impact Ladder** — applies when validating mart output (test row counts vs baseline).
3. **Question → Goal → 5W1H Action Brief** — modeling decisions need Why.
4. **Why-Explanation (META)** — pattern choice + grain choice + materialization choice each have 1-line Why.

Full rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-model.md`.

### 4 Modeling Patterns

| Pattern | When to pick |
|---------|--------------|
| **Kimball Star/Snowflake** | Cloud DWH (BQ/Snowflake/Redshift); BI workload; multiple business processes |
| **dbt staging → marts** | dbt project; modular SQL; dbt-skilled team; need built-in tests + lineage |
| **Medallion (Bronze/Silver/Gold)** | Lakehouse (Databricks/Delta/Iceberg); multi-stage ELT; need full audit trail |
| **DuckDB Layered** | Local file-based (CSV/Excel); rapid prototyping; single-user analyst |

### Decision flow
```
Have cloud DWH?
├── YES + dbt skill → dbt staging→marts
├── YES + no dbt → Kimball direct
└── NO
    ├── Have lakehouse? → Medallion
    └── NO → DuckDB layered
```

Hybrid common: prototype in DuckDB → promote to dbt when recurring + scaling.

## Hard rules

- **Schema documentation MANDATORY** — every table needs a Table Contract (business def + grain + PK + partition + SLA + owner + downstream + metric coverage)
- **Grain explicit** — every table's doc states "1 row = X × Y × Z"
- **Naming convention enforced** — `stg_`, `int_`, `fct_`, `dim_`, `agg_` prefixes
- **Tests defined alongside model** — dbt schema tests OR equivalent assertions
- **Governance hook required** — after modeling, route to `governance.md` for quality + ownership + access setup

## Phase routing (after modeling)

| Next mode | When |
|-----------|------|
| `/prof-DA:automate` | Pipeline needs scheduling |
| `/prof-DA:process` | Initial mart needs EDA / quality audit |
| `/prof-DA:query` | Schema ready, ad-hoc query needs |
| `/prof-DA:report` | Stakeholder needs dashboard built on new mart |

Governance setup (NOT a separate mode) → read `governance.md` and pick 5 implementations to ship.

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-model.md`
- Governance after modeling: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/governance.md`
- Orchestration for the pipeline: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/orchestration-patterns.md`
- Quality gates per layer: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/quality-pipeline.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
