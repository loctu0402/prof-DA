# prof-DA v3.4.1

> Professional Data Analyst + Analytics Engineer workflow as a Claude Code plugin. **9 routable modes** that auto-fire on natural Vietnamese + English DA requests (no need to memorize slash commands). 14 stdlib scripts, 14 method specs (causal + validation), 4 mandatory universal rules + **Detail Level Gate** (Quick / Standard / Deep) + **Proactive Suggestion at Mode Exit**, planning protocol (TH1/TH2), 4 data modeling patterns, 6-section governance, 5 orchestration patterns, 5-tier schema-source hierarchy, portable semantic-layer recipe, visualization discipline (SWD), 8-category suggestion protocol. 1-stop-shop end-to-end DA harness.

## What changed in v3.4 (BREAKING)

- **Plugin renamed**: `prof-data-analyst` → `prof-DA` (shorter slash command namespace).
- **Skill names lost the `da-` prefix**: invocation is now `/prof-DA:query` instead of `/prof-data-analyst:da-query`.
- **Auto-fire descriptions rewritten** with extensive natural-language trigger phrases (Vietnamese + English) so the plugin invokes itself on conversational requests like "cho mình số liệu của X", "điều gì xảy ra với Y", "tìm phương pháp tính tiềm năng", "MFU cohort sizing".
- **Detail Level Gate**: every mode entry asks Quick / Standard / Deep before executing (NO time estimates — Claude routinely under-estimates duration).

**To upgrade from `prof-data-analyst` (v3.3 or earlier)**:
```bash
/plugin uninstall prof-data-analyst
/plugin install prof-DA@loctu-marketplace
```

## Install

Claude Code marketplaces follow a **2-step pattern** (analogous to `apt-add-repository` then `apt install`):

```bash
# Step 1 — Register the marketplace (once per machine)
/plugin marketplace add loctu0402/prof-DA

# Step 2 — Install the plugin from that marketplace
/plugin install prof-DA@loctu-marketplace

# Verify
/plugin list
# → prof-DA v3.4.1 should appear
```

> Repo renamed from `loctu0402/prof-data-analyst` → `loctu0402/prof-DA` in v3.4.1. If you previously added the old marketplace path, remove + re-add it: `/plugin marketplace remove loctu-marketplace` then `/plugin marketplace add loctu0402/prof-DA`.

**Both steps required.** If `/plugin install` returns `Marketplace "loctu-marketplace" not found`, Step 1 was skipped — re-run it first.

**Update**:
```bash
/plugin update prof-DA@loctu-marketplace
```

**Uninstall**:
```bash
/plugin uninstall prof-DA
/plugin marketplace remove loctu-marketplace   # optional, drops the registry too
```

## Slash commands

After install, the 10 slash commands are namespaced under `/prof-DA:`:

```
/prof-DA:da             # entry — confirm intent + detail level, route to mode
/prof-DA:frame          # Business Understanding → Metric Define → Data Plan
/prof-DA:model          # Data modeling (Kimball / dbt / Medallion / DuckDB)
/prof-DA:query          # Engine-agnostic NL→SQL + Step 0 Request Intake
/prof-DA:process        # Raw → staged → cleaned → mart → ML-ready
/prof-DA:insight        # Hypothesis → diagnostic → recommendation
/prof-DA:automate       # Pipeline + fail-alert (Airflow/dbt/cron/GHA)
/prof-DA:report         # Stakeholder deliverable + storyline + chart anatomy
/prof-DA:review         # 3 sub-modes (A Delivery / B Full / C Stakeholder Q)
/prof-DA:fix            # Surgical pipeline / report debug
```

**You usually don't need to type these.** The skills auto-fire on natural Vietnamese + English DA requests — see the trigger phrases in each mode's SKILL.md frontmatter.

## 9-mode workflow tour

Standard end-to-end DA flow: **Frame → Model → Query → Process → Insight → Automate → Report**, plus orthogonal **Review** + **Fix**.

| Mode | What it does | Sample natural triggers |
|------|--------------|------------------------|
| **frame** | Business Understanding → Metric Define → Data Plan (TH1 schema-exists / TH2 brainstorm-modeling) → Lock in PLANNING.md | "không biết bắt đầu", "stakeholder muốn", "metric nào phù hợp", "tìm phương pháp tính tiềm năng", "MFU cohort sizing" |
| **model** | 4 patterns (Kimball / dbt staging→marts / Medallion / DuckDB layered) + Table Contracts + governance hooks | "design DWH", "build mart", "dbt project", "chia bảng thế nào" |
| **query** | Engine-agnostic NL→SQL with Step 0 Request Intake + 5-tier schema discovery + BQ Safety Protocol + Query Logic Card | "cho mình số liệu", "lấy data", "tỷ lệ X", "breakdown theo Y", "compare X vs Y" |
| **process** | Raw → staged → cleaned → mart with 6-step EDA + Executive Summary per phase | "EDA notebook", "data quality", "kiểm tra data", "feature engineering" |
| **insight** | Causal-method matching (DiD / Event Study / RDD / SC / PSM / IV) + 5-stage reasoning chain + anti-bias | "điều gì xảy ra", "tại sao X giảm/tăng", "root cause", "vì sao", "phân tích sâu" |
| **automate** | Pipeline + fail-alert wiring + cache discipline + scheduler choice (Airflow/dbt+GHA/cron/GitHub Actions) | "automation", "schedule job", "chạy hàng ngày", "alert khi pipeline lỗi" |
| **report** | Stakeholder report from template + chart anatomy + dual-comparison KPIs + storyline pattern | "build báo cáo", "làm report", "stakeholder report", "build dashboard" |
| **review** | 3 sub-modes — A Delivery refine / B Full project audit / C Stakeholder Q formulation | "review report", "OK chưa", "audit project", "góp ý" |
| **fix** | Surgical pipeline / report debug with patch-ceiling escalation | "fix pipeline", "report sai", "wrong number", "pipeline fail" |

### Front-of-workflow planning

```
[frame]
  Gate 1: Business Understanding (5W1H + stake + audience)
  Gate 2: Metric Define (pick framework: NSM/OMTM/Growth Loop/HEART + 10-field contract)
  Gate 3: Data Plan
    TH1 (data exists)        → verify schema + sample query < $0.10
    TH2 (data missing)       → domain discovery + pick modeling pattern
  Gate 4: Lock PLANNING.md + route to next mode

[model]  (only if TH2 in Gate 3, or existing pipeline lacks structure)
  Pattern 1: Kimball Star/Snowflake     (cloud DWH, BI workload)
  Pattern 2: dbt staging → marts        (modular SQL, tests + lineage built-in)
  Pattern 3: Medallion Bronze/Silver/Gold (lakehouse, full audit trail)
  Pattern 4: DuckDB layered             (local files, rapid prototyping)
  → Schema documentation (Table Contracts) MANDATORY per table
  → Governance hooks planned (6-section practical framework)
```

## 5 mandatory universal rules

1. **Orientation Block** — every deliverable opens with SCQR / 3-line intro / module docstring
2. **Baseline → Noise → Impact Ladder** — every numeric statement passes 3 rungs (baseline + noise check + impact verdict)
3. **5W1H Action Brief** — every recommendation has 8 fields filled
4. **Why-Explanation (META)** — every action / method / threshold / tool choice has inline Why (Causal / Empirical / Comparative / Theoretical / Operational)
5. **Detail Level Gate** *(v3.4)* — every mode entry confirms Quick / Standard / Deep before executing. NO time estimates surfaced — Claude under-estimates duration; depth is the lever the user controls.

## 14 stdlib scripts

```
scripts/
├── stats/      effect_size, significance, mde_sample_size, baseline_noise_impact, bootstrap_ci, multiple_testing
├── causal/     did_event_study, parallel_trends_test
├── format/     number_format
└── validators/ orientation_block, action_brief, ai_tell_scan, rubric_audit, method_maturity_audit, self_check
```

Script-over-agent-compute is a hard rule: NEVER inline statistical work, always call a script.

## 14 method specs

```
references/methods/
├── _template.md           # canonical W/H/W/W/W/W structure
├── _index.md              # router
├── did.md                 # Difference-in-Differences
├── event_study.md         # Event Study
├── rdd.md                 # Regression Discontinuity
├── synthetic_control.md   # Synthetic Control
├── psm.md                 # Propensity Score Matching
├── iv.md                  # Instrumental Variable / 2SLS
├── bootstrap_ci.md        # Bootstrap CI
├── robustness_checks.md   # Robustness across specs
├── sensitivity_analysis.md # Sensitivity to parameter
├── falsification_tests.md # Placebo / zero-effect
├── multiple_testing.md    # Bonferroni / BH-FDR
├── post_hoc_power.md      # Power at MDE
├── cross_validation.md    # K-fold CV
└── pre_registration.md    # Lock plan before EDA
```

Each spec follows a 12-section template and cites a primary source (Angrist-Pischke, Imbens-Rubin, Efron-Tibshirani, Benjamini-Hochberg, etc.).

## 3 sub-agents (LEAN architecture)

Sub-agents are spawned only when value > cost. Most work runs in the main agent + the loaded mode skill.

- **da-orchestrator** (Sonnet) — session-start intent confirmation + plan review + final-review gate
- **da-context-tracer** (Haiku) — multi-file reads for `/prof-DA:review` Sub-mode B Phase 2 (when project ≥ 5 files)
- **da-method-auditor** (Sonnet) — `/prof-DA:review` Sub-mode B Pass 3 causal-method judgment (when causal claims present)

## Quality framework

- **5 Quality Criteria** (Interconnect / Compact / Insightful / Sufficient / Logical Reason) at review gate
- **5-Gate Quality Pipeline** (Scope → Data → Analysis → Viz+Story → Review) with max 3 retries per gate
- **Outline / Story Flow Check** at every review pass (extract headings standalone, verify story is followable)
- **Sub-agent prompt discipline** (anti-shortcut + handoff drift + fresh-session + context-packet)

## Visualization discipline (SWD)

Every chart / dashboard / slide goes through a 6-lesson framework + 5-rule cheatsheet + 10 anti-pattern checklist:
1. **Action title** — chart title states a conclusion, not a topic
2. **Grey + 1 accent** — neutral grey default; one accent on focal entity
3. **No pie, no 3D** — horizontal bar > pie; 2D > 3D; slopegraph for 2-point trends
4. **Clutter checklist** — strip border / heavy gridlines / redundant legend / 3D / shadow / gradient
5. **Horizontal logic** — page titles read in order form a Setup → Conflict → Resolution story

Full reference: `skills/da/references/storytelling-with-data.md`.

## Schema discovery + semantic layer

5-tier hierarchy for table schema + access discovery: **T0** owner-curated LLM tag → **T1** catalog tool direct API → **T2** access-aware metadata MCPs → **T3** INFORMATION_SCHEMA + brainstorm with user → **T4** sampling. See `skills/da/references/schema-source-hierarchy.md`.

Portable 6-phase recipe for building a semantic layer from scratch (engine-agnostic — Cube.js / dbt-metrics / LookML / MetricFlow): `skills/da/references/semantic-layer-setup.md`.

## Engine-agnostic by design

- SQL engine: BQ / Postgres / Snowflake / Redshift / DuckDB
- Semantic layer: Cube.js / dbt-metrics / LookML / org-specific
- Notification channel: SMTP / Slack / Teams / PagerDuty / internal module
- Cron / scheduler: Airflow / Dagster / Prefect / crontab / GitHub Actions / Claude /loop

Workspace-specific configuration (project IDs, credentials, brand themes) lives OUTSIDE the plugin.

## Optional org-specific extensions

For users at <organization>: a dedicated reference + example MCP config bundle access to Semantic Cube, <org-data-mcp> MCP, <org-catalog> MCP, and OpenMetadata curation. See `skills/da/references/org-extensions.md` and `mcp/example-org-mcp.json`. Non-<organization> users can ignore.

## License

MIT — see `LICENSE`.

## Author

Method by **Loc Tu** (loctu) · 2026. Distilled from personal practice.
