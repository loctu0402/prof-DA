# prof-DA

> A Claude Code plugin that makes Claude work like a disciplined data analyst: ask for a number, a chart, or "why did X drop" in plain Vietnamese or English, and it runs a structured analyst workflow instead of improvising.

`v3.5.0` · MIT · engine-agnostic (BigQuery / Postgres / Snowflake / Redshift / DuckDB) · auto-fires on natural language

## Why prof-DA exists

Ask a stock LLM for "số liệu X" and it free-styles. It guesses which metric you meant, writes SQL against a schema it never checked, hands back a bare number with no sense of whether the move is real or noise, and formats the report a different way every time. Across a team nothing is reproducible, and no two deliverables look alike.

prof-DA replaces that with a fixed analyst process. Before touching data it confirms what you actually want and how deep to go. It discovers the real schema before writing a query. It runs statistics in audited scripts rather than guessing them inline. It checks every number for signal versus noise. And it ships a deliverable with the same structure every time. The point is simple: any Claude session, on any engine, produces work that reads like the same senior analyst made it.

It is built for data analysts and analytics engineers who live in Claude Code and want rigor and consistency instead of improvisation.

**Jump to:** [Install](#install) · [First run](#first-run) · [The 9 modes](#the-9-modes) · [What it enforces](#what-it-enforces) · [What is inside](#what-is-inside) · [Configuration](#configuration)

## Install

Claude Code marketplaces use a 2-step pattern (like `apt-add-repository` then `apt install`):

```bash
# Step 1 - register the marketplace (once per machine)
/plugin marketplace add loctu0402/prof-DA

# Step 2 - install the plugin from it
/plugin install prof-DA@loctu-marketplace

# Verify
/plugin list      # prof-DA 3.5.0 should appear
```

Both steps are required. If Step 2 returns `Marketplace "loctu-marketplace" not found`, Step 1 was skipped.

```bash
/plugin update prof-DA@loctu-marketplace       # update
/plugin uninstall prof-DA                       # remove the plugin
/plugin marketplace remove loctu-marketplace    # optional: drop the registry too
```

Upgrading from the old `prof-data-analyst` package (v3.3 or earlier)? Uninstall it first, then install `prof-DA`; the namespace and repo were both renamed. Details in [CHANGELOG.md](CHANGELOG.md).

## First run

You usually do not type a command. Just ask, in Vietnamese or English:

```
cho mình tỷ lệ user mới giữ lại sau 30 ngày, tháng vừa rồi
why did AUM drop last week?
build báo cáo doanh thu cho stakeholder
```

prof-DA detects the request, confirms intent and a detail level (Quick / Standard / Deep), routes to the right mode, and runs. To start explicitly, use the entry command:

```
/prof-DA:da     # confirm intent + detail level, then route to a mode
```

## The 9 modes

The standard lifecycle runs left to right; `review` and `fix` are orthogonal and run any time.

`frame -> model -> query -> process -> insight -> automate -> report`  +  `review` / `fix`

| Mode | What it does | Sample natural triggers |
|------|--------------|------------------------|
| **frame** | Scope a vague ask into a locked plan: business understanding, metric contract, data plan. Outputs `PLANNING.md`. | "không biết bắt đầu", "stakeholder muốn", "metric nào phù hợp", "tính tiềm năng" |
| **model** | Design the warehouse: Kimball star, dbt staging-to-marts, Medallion, or DuckDB layered, with table contracts. | "design DWH", "build mart", "dbt project", "chia bảng thế nào" |
| **query** | Natural language to SQL with schema discovery, a cost-safety check, and a logic card. | "cho mình số liệu", "lấy data", "tỷ lệ X", "breakdown theo Y", "compare X vs Y" |
| **process** | Raw to staged to cleaned to mart, with 6-step EDA and a summary per phase. | "EDA notebook", "data quality", "kiểm tra data", "feature engineering" |
| **insight** | Hypothesis to diagnostic to recommendation: matches the right causal method and guards against bias. | "điều gì xảy ra", "tại sao X giảm", "root cause", "vì sao", "phân tích sâu" |
| **automate** | Wire a scheduled pipeline with fail-alerts and cache discipline. | "automation", "schedule job", "chạy hàng ngày", "alert khi lỗi" |
| **report** | Build a stakeholder deliverable from a locked template: storyline, chart anatomy, dual-comparison KPIs, portal publish. | "build báo cáo", "làm report", "build dashboard" |
| **review** | Audit a deliverable or a whole project. 3 sub-modes: delivery refine, full project audit, stakeholder questioning. | "review report", "OK chưa", "audit project", "góp ý" |
| **fix** | Surgically debug a pipeline or report, with a patch-ceiling escalation rule. | "fix pipeline", "report sai", "wrong number", "pipeline fail" |

Each mode auto-fires on phrases like these, so a command is rarely needed; the full trigger lists live in each mode's `SKILL.md`. For the deeper structure, `frame` runs 4 planning gates and `model` offers 4 warehouse patterns: see [mode-frame](skills/da/references/mode-frame.md) and [mode-model](skills/da/references/mode-model.md).

## What it enforces

Every deliverable passes 4 universal rules plus an entry gate. This is what keeps output consistent and rigorous across sessions.

1. **Orientation block:** every deliverable opens with a short framing (SCQR, a 3-line intro, or a module docstring) so the reader gets the point before the detail.
2. **Baseline, noise, impact:** every number is stated against a baseline, checked for whether it is real or noise, then given an impact verdict. No bare figures.
3. **5W1H action brief:** every recommendation fills 8 fields (question, goal, what, why, who, when, where, how) so it is actionable, not vague.
4. **Why-explanation:** every action, method, threshold, and tool choice carries an inline reason (causal, empirical, comparative, theoretical, or operational). A circular "X because X" is rejected.

The **Detail-Level Gate** sits in front of all four: every mode confirms Quick / Standard / Deep before running. Depth is the lever you control. The plugin deliberately does not surface time estimates, because LLMs routinely mis-estimate duration.

On top of the rules sit a 5-criteria quality check and a 5-gate quality pipeline (scope -> data -> analysis -> visuals -> review). Stakeholder visuals follow Storytelling-with-Data discipline (action titles, grey plus one accent, no pie or 3D): see [storytelling-with-data](skills/da/references/storytelling-with-data.md).

## What is inside

prof-DA is one root skill plus thin per-mode stubs, a script stdlib, method specs, and 3 support agents. The deep material lives in the linked files; this README stays a map.

```
skills/
  da/                      root skill: rules, protocols, references
    references/            deep docs (modes, methods, governance, SWD, schema)
    scripts/               16 stdlib scripts (run, never inline, statistics)
  frame, model, query ...  9 thin mode stubs that load the root skill
commands/                  10 slash commands (1 entry + 9 modes)
agents/                    3 support sub-agents
```

- **16 stdlib scripts** (`skills/da/scripts/`): stats (effect size, significance, MDE, bootstrap CI, multiple testing), causal (DiD / event study, parallel-trends), formatting, and validators (orientation, action brief, AI-tell scan, rubric audit, method-maturity audit, report consistency, self-check). Script-over-agent-compute is a hard rule: statistics always run in a vetted script, never guessed inline. See [scripts-guide](skills/da/references/scripts-guide.md).
- **14 method specs** (`skills/da/references/methods/`): DiD, event study, RDD, synthetic control, PSM, IV, bootstrap CI, robustness, sensitivity, falsification, multiple testing, post-hoc power, cross-validation, pre-registration. Each cites a primary source. See [methods/_index](skills/da/references/methods/_index.md).
- **3 support sub-agents** (`agents/`), spawned only when value beats cost: `da-orchestrator` (intent + plan + final-review gate), `da-context-tracer` (multi-file reads for big-project review), `da-method-auditor` (causal-method judgment).

## Configuration

prof-DA is engine-agnostic and ships no credentials. It adapts to:

| Layer | Options |
|-------|---------|
| SQL engine | BigQuery, Postgres, Snowflake, Redshift, DuckDB |
| Semantic layer | Cube.js, dbt-metrics, LookML, or org-specific |
| Notifications | SMTP, Slack, Teams, PagerDuty, internal module |
| Scheduler | Airflow, Dagster, Prefect, cron, GitHub Actions |

Schema discovery follows a 5-tier hierarchy (owner-curated tag -> catalog API -> access-aware metadata -> INFORMATION_SCHEMA -> sampling): see [schema-source-hierarchy](skills/da/references/schema-source-hierarchy.md). Workspace-specific settings (project IDs, credentials, brand themes) live outside the plugin.

**<organization> users:** an optional extension bundles the Semantic Cube, the <org-data-mcp> and <org-catalog> MCPs, and OpenMetadata curation. See [org-extensions](skills/da/references/org-extensions.md). Everyone else can ignore it.

## Versioning

Current version `3.5.0`. Full history, including the v3.4 rename from `prof-data-analyst`, is in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).

## Author

Method by Loc Tu (loctu), 2026. Distilled from personal practice.
