---
name: process
description: Raw → staged → cleaned → mart → ML-ready pipeline + standalone Data Quality Audit + standalone Cleaning. Layered tables (stg_/clean_/mart_/ml_/pred_) per Medallion + dbt-style. DuckDB-first for case studies. 7-check + 6-step EDA + Executive Summary per phase. Use this skill whenever the user needs data wrangling, EDA, ML case study, feature engineering, quality audit, or cleaning. Auto-fires on natural Vietnamese + English. Natural triggers include "process data", "xử lý data", "wrangle", "ML case study", "M1 / M2 / M3", "feature engineering", "EDA notebook", "EDA", "explore data", "khám phá data", "data dictionary", "DWH", "DWH-first", "data audit", "data quality", "quality check", "kiểm tra data", "kiểm tra chất lượng", "data quality issue", "missing values", "anomaly", "outlier", "clean data", "data cleaning", "preprocess", "tiền xử lý", "feature selection", "feature importance", "univariate", "bivariate", "Cramer's V", "Cohen's d", or explicit /prof-DA:process.
---

# Process Mode — Raw → Mart → ML-Ready

Transformation engine from raw input through staged → cleaned → mart → analysis/ML-ready output. Also covers standalone Data Quality Audit (Phase 2 only — output is a quality report) and standalone Cleaning (Phase 2 + Phase 3 — output is one cleaned table).

## 4 Universal Rules
1. Orientation Block at top of every deliverable
2. Baseline → Noise → Impact ladder for every numeric statement
3. 5W1H Action Brief for every recommendation
4. Why-Explanation on every framework / threshold / encoding / split choice

Full: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow

5 phases with acceptance gates:
- Phase 1 — Ingest & Data Dictionary
- Phase 2 — Data Quality Audit (7-check + 6-step EDA sequence S1 dtype → S2 univariate → S3 anomaly → S4 bivariate → S5 ranking → S6 patterns)
- Phase 3 — Feature / Mart Construction
- Phase 4 — Model / Analysis
- Phase 5 — Evaluation & Report

Per-phase Executive Summary table (Terminology / Assumption / Q&A descriptive / Q&A diagnostic / Multi-feature combo / Final belief / Rule-based filter / Traps / Next action).

DuckDB-first when raw input is CSV / Parquet / mart-export for case studies. Bronze→Silver→Gold layered tables per Medallion architecture; prefix convention matches dbt staging.

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-process.md`.

## Hard rules
- Layered prefix convention enforced: stg_/clean_/mart_/ml_/pred_
- High-cardinality columns flagged as rule-based pre-filter, NEVER ship to ML
- Source-pending: stub `stg_<source>_PENDING`, continue downstream design
- Univariate vs Bivariate role split (no duplicate t-test)
- Per-chart inline takeaway (drop / negligible / candidate / strong)

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-process.md`
- Coding discipline: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/coding-discipline.md`
- Style + AI-tells: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/style-rules.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
