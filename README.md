# prof-DA

**prof-DA turns Claude Code into a disciplined data analyst.** Ask for a number, a chart, or "why did X drop", in Vietnamese or English, and it runs a fixed analyst workflow instead of improvising.

- **What it is:** a Claude Code plugin that wraps Claude in 9 analyst modes (`frame -> model -> query -> process -> insight -> automate -> report`, plus `review` / `fix`) behind one natural-language entry point.
- **Who it's for:** data analysts and analytics engineers who work in Claude Code and want rigor and consistency, not improvisation.
- **The problem it kills:** a stock LLM guesses which metric you meant, queries a schema it never checked, returns a bare number with no signal-vs-noise read, and formats every report differently. Nothing is reproducible.
- **The guarantee:** any session, on any engine, produces work that reads like the same senior analyst made it.

`v3.8.0` · MIT · engine-agnostic: BigQuery / Postgres / Snowflake / Redshift / DuckDB

## How it works

prof-DA runs the same fixed process on every request: confirm intent and depth before touching data, discover the real schema before querying, run statistics in audited scripts (never inline guesses), judge every number for signal versus noise, and ship a same-shape deliverable each time. The 10 modes below cover the analyst lifecycle; the 4 universal rules are what keep each step rigorous and consistent across sessions.

**Jump to:** [Why not vanilla Claude?](#why-not-just-vanilla-claude-code) · [Install](#install) · [First run](#first-run) · [The 10 modes](#the-10-modes) · [What it enforces](#what-it-enforces) · [What is inside](#what-is-inside) · [Configuration](#configuration)

## Why not just vanilla Claude Code?

Plain Claude Code can write SQL and charts, but nothing makes it consistent or checkable. prof-DA adds the enforcement layer:

| Vanilla Claude Code | prof-DA |
|---------------------|---------|
| Guesses which metric you meant; queries a schema it never checked | Confirms intent, then discovers the real schema (5-tier) before any query |
| Eyeballs significance inline | Runs statistics in 16 audited scripts (effect size, MDE, bootstrap CI, DiD), never guessed |
| Formats every report differently | Reports fork one of 11 build-once-locked templates 1:1, so style drift is gone |
| "Looks done," trusted on faith | A Stop-hook blocks the turn from ending until the report passes the consistency gate |
| Forgets your corrections next session | A learning loop captures corrections and updates the rule the agent reads next time |

## Install

Claude Code marketplaces use a 2-step pattern (like `apt-add-repository` then `apt install`):

```bash
# Step 1 - register the marketplace (once per machine)
/plugin marketplace add loctu0402/prof-DA

# Step 2 - install the plugin from it
/plugin install prof-DA@loctu-marketplace

# Verify
/plugin list      # prof-DA 3.8.0 should appear
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

## The 10 modes

The standard lifecycle runs left to right; `review`, `fix`, and `workspace` are orthogonal and run any time.

`frame -> model -> query -> process -> insight -> automate -> report`  +  `review` / `fix` / `workspace`

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
| **workspace** | Scaffold, organize, and index a whole workspace into a navigable harness (taxonomy + memory layer + index). Guide-first for non-technical users; secrets-first, safe `git mv` on a branch, index last. | "dọn workspace", "sắp xếp lại thư mục", "file nằm khắp nơi", "organize my workspace", "rebuild index" |

Each mode auto-fires on phrases like these, so a command is rarely needed; the full trigger lists live in each mode's `SKILL.md`. For the deeper structure, `frame` runs 4 planning gates and `model` offers 4 warehouse patterns: see [mode-frame](skills/da/references/mode-frame.md) and [mode-model](skills/da/references/mode-model.md).

## What it enforces

Every deliverable passes 4 universal rules plus an entry gate. This is what keeps output consistent and rigorous across sessions.

1. **Orientation block:** every deliverable opens with a short framing (SCQR, a 3-line intro, or a module docstring) so the reader gets the point before the detail.
2. **Baseline, noise, impact:** every number is stated against a baseline, checked for whether it is real or noise, then given an impact verdict. No bare figures.
3. **5W1H action brief:** every recommendation fills 8 fields (question, goal, what, why, who, when, where, how) so it is actionable, not vague.
4. **Why-explanation:** every action, method, threshold, and tool choice carries an inline reason (causal, empirical, comparative, theoretical, or operational). A circular "X because X" is rejected.

The **Detail-Level Gate** sits in front of all four: every mode confirms Quick / Standard / Deep before running. Depth is the lever you control. The plugin deliberately does not surface time estimates, because LLMs routinely mis-estimate duration.

On top of the rules sit a 5-criteria quality check and a 5-gate quality pipeline (scope -> data -> analysis -> visuals -> review). Stakeholder visuals follow Storytelling-with-Data discipline (action titles, grey plus one accent, no pie or 3D): see [storytelling-with-data](skills/da/references/storytelling-with-data.md).

Two mechanisms make these non-optional rather than advisory. A **Stop-hook** blocks a `report`-mode turn from ending until the deliverable passes the consistency gate (the model cannot quietly skip validation). A **learning loop** captures your corrections at session end and updates the rule the agent reads next time, so a repeated mistake becomes a permanent fix instead of a recurring one.

## What is inside

prof-DA is one root skill plus thin per-mode stubs, a script stdlib, method specs, and 3 support agents. The deep material lives in the linked files; this README stays a map.

```
skills/
  da/                      root skill: rules, protocols, references
    references/            deep docs (modes, methods, governance, SWD, schema)
    scripts/               16 stdlib scripts (run, never inline, statistics)
  frame, model, query ...  10 thin mode stubs that load the root skill
commands/                  11 slash commands (1 entry + 10 modes)
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

Current version `3.8.0`. Full history, including the v3.4 rename from `prof-data-analyst`, is in [CHANGELOG.md](CHANGELOG.md).

## Contributing

Issues and pull requests are welcome at [loctu0402/prof-DA](https://github.com/loctu0402/prof-DA). prof-DA is distilled from one analyst's daily practice, so real-world gaps and counter-examples are the most useful feedback.

## License

MIT. See [LICENSE](LICENSE).

## Author

Method by Loc Tu (loctu), 2026. Distilled from personal practice.
