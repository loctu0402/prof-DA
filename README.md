# prof-DA

**prof-DA turns Claude Code into a disciplined data analyst that anyone can drive, analyst or not.** Ask for a number, a chart, a root cause, or a stakeholder report, in Vietnamese or English, and it runs a fixed, governed analyst workflow instead of improvising, so the answer is consistent, checkable, and reads the same every time.

- **What it is:** a Claude Code plugin that wraps Claude in 12 analyst modes (`frame -> model -> query -> process -> insight -> automate -> report`, plus `deliver` / `submit` / `review` / `fix` / `workspace`) behind one natural-language entry point.
- **Who it's for:** not only data analysts and analytics engineers. It is built so **business stakeholders and non-technical users can self-serve data** and still get an analyst-grade result, and so the experts get rigor and consistency instead of improvisation. The aim is **consistent, high-quality, trustworthy self-serve output**, first and foremost for <organization> stakeholders.
- **The problem it kills:** a stock LLM guesses which metric you meant, queries a schema it never checked, returns a bare number with no signal-vs-noise read, and formats every report differently. Plausible-but-wrong answers slip through. Nothing is reproducible.
- **The guarantee:** any session, on any engine, driven by anyone, produces work that reads like the same senior analyst made it.

`v3.17.0` · MIT · engine-agnostic: BigQuery / Postgres / Snowflake / Redshift / DuckDB

## The whole system on one page

![prof-DA architecture: 6 nested loops from per-request to cross-session](docs/prof-da-architecture.svg)

Read it like a clock: a request flows down the lanes (intent gate -> grounding -> mode run -> gate stack -> cycle contract), the learning loop writes what it learned back into the second brain, and the next request starts deeper than the last. The compound chain is the product.

**New here?** [docs/GUIDE.md](docs/GUIDE.md) is the full written walkthrough — every mode, the enforcement spine, how it auto-fires, and the self-operating maintenance loops (curator / hard memory budget / anti-drift / subagent walls) derived from studying Hermes Agent.

## Why this matters now

Anthropic's own write-up, [How Anthropic enables self-service data analytics with Claude](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude), shows Claude can already automate roughly 95% of business analytics queries, but **only once the foundation exists**: canonical data, a semantic source-of-truth, encoded skills, and validation. The same piece names the parts that stay hard: **concept-entity ambiguity** (a question maps to "hundreds of viable options"), **data staleness** ("definitions and schemas change constantly"), **retrieval failure**, and **silent failures**, the plausible answers that are simply wrong, which it flags as still unsolved.

So the differentiator is no longer "can the agent query data." Vanilla Claude can run the steps. prof-DA is the layer that **operationalizes that blueprint for a real org**: it ships the skills, the validation, the consistency, and the grounding so you do not rebuild them every session, and so a non-expert's self-serve answer is one you can actually trust. The three things it adds beyond vanilla Claude are next.

## What makes prof-DA different

Three layers vanilla Claude leaves you to build yourself. Each maps onto a failure mode above.

### 1. The build-once-lock report protocol: 12 archetypes, fork-or-fail

Every deliverable **forks one of 12 locked report archetypes (A1-A12) 1:1** and swaps in data; it never freestyles a layout. The set covers the full DA surface: **A1** deep-dive, **A2** ops dashboard, **A3** editorial paper, **A4** daily email, **A5** Google Chat card, **A6** slide deck (the IA pin), **A7** exec one-pager, **A8** idea-verification, **A9** training, **A10** data-quality, **A11** projection, and **A12** slide-deck / editable-PPTX. They share one design contract: a token palette, the verdict vocabulary, the chart-choice matrix, and the AI-tell bans, all governed by a build-once-then-lock playbook.

Why it matters: per-report style drift is the tell of an untrustworthy self-serve tool. When every output reads like the same senior analyst made it, a business stakeholder can trust it at a glance, with no analyst in the loop. `report` mode enforces fork-or-fail (a README-only template stub triggers a design handoff, never a freestyle). See [storytelling-with-data](skills/da/references/storytelling-with-data.md) and [output-slide-deck](skills/da/references/output-slide-deck.md); the locked archetype library lives in your workspace's `shared/templates/` (the A1-A12 set is <organization>'s reference instantiation).

### 2. The workspace second brain

`workspace` mode **builds** a second brain (a clean taxonomy, a memory layer of your domains, metrics, conventions, and past decisions, and a navigable index), and **every other mode reads it on entry** before acting. The agent starts grounded in your real entities instead of guessing them.

Why it matters: this is the direct answer to the blog's three open problems. Grounding in curated domain memory collapses **concept-entity ambiguity**; the index makes the right context **retrievable** instead of lost; a maintained memory plus freshness discipline fights **staleness**. Division of labor: the standalone `workspace-brain` skill builds and seeds the brain, prof-DA consumes it. See [mode-workspace](skills/da/references/mode-workspace.md).

### 3. The enforcement layer: the silent-failure killer

The hardest unsolved problem is the plausible wrong answer. prof-DA makes validation non-optional: **4 universal rules** (orientation, baseline-noise-impact, action brief, why-explanation), **17 audited statistics scripts** (significance, effect size, bootstrap CI, DiD, run in code and never eyeballed inline), a **Stop-hook** that blocks a `report` turn from ending until the deliverable passes the consistency gate, and a **learning loop** that turns each correction you give into a permanent rule. A wrong-but-pretty answer has to survive all of it. Detail in [What it enforces](#what-it-enforces).

## Why not just vanilla Claude Code?

Same questions, sharpened against the failure modes Anthropic's blog names:

| The hard part | Vanilla Claude Code | prof-DA |
|---|---|---|
| Concept-entity ambiguity | Guesses which metric you meant | Confirms intent, grounds in the workspace second brain, discovers the real schema (5-tier) before any query |
| Data staleness | No freshness notion | Freshness governance + a maintained memory/index; stale sources are flagged, not trusted |
| Silent failures (plausible-but-wrong) | "Looks done," trusted on faith | Audited stat scripts + a Stop-hook consistency gate; no bare numbers (baseline-noise-impact on every figure) |
| Style drift / inconsistency | Formats every report differently | Forks one of 12 build-once-locked archetypes 1:1 |
| Forgets corrections | Repeats the mistake next session | Learning loop turns a correction into a permanent rule |

## Install

Claude Code marketplaces use a 2-step pattern (like `apt-add-repository` then `apt install`):

```bash
# Step 1 - register the marketplace (once per machine)
/plugin marketplace add loctu0402/prof-DA

# Step 2 - install the plugin from it
/plugin install prof-DA@loctu-marketplace

# Verify
/plugin list      # prof-DA 3.17.0 should appear
```

Both steps are required. If Step 2 returns `Marketplace "loctu-marketplace" not found`, Step 1 was skipped.

```bash
/plugin update prof-DA@loctu-marketplace        # update
/plugin uninstall prof-DA                        # remove the plugin
/plugin marketplace remove loctu-marketplace     # optional: drop the registry too
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

## The 12 modes

The standard lifecycle runs left to right; `deliver`, `submit`, `review`, `fix`, and `workspace` are orthogonal and run any time.

`frame -> model -> query -> process -> insight -> automate -> report`  +  `deliver` / `submit` / `review` / `fix` / `workspace`

| Mode | What it does | Sample natural triggers |
|------|--------------|------------------------|
| **frame** | Scope a vague ask into a locked plan: business understanding, metric contract, data plan. Outputs `PLANNING.md`. | "không biết bắt đầu", "stakeholder muốn", "metric nào phù hợp", "tính tiềm năng" |
| **model** | Design the warehouse: Kimball star, dbt staging-to-marts, Medallion, or DuckDB layered, with table contracts. | "design DWH", "build mart", "dbt project", "chia bảng thế nào" |
| **query** | Natural language to SQL with schema discovery, a cost-safety check, and a logic card. | "cho mình số liệu", "lấy data", "tỷ lệ X", "breakdown theo Y", "compare X vs Y" |
| **process** | Raw to staged to cleaned to mart, with 6-step EDA and a summary per phase. | "EDA notebook", "data quality", "kiểm tra data", "feature engineering" |
| **insight** | Hypothesis to diagnostic to recommendation: matches the right causal method and guards against bias. | "điều gì xảy ra", "tại sao X giảm", "root cause", "vì sao", "phân tích sâu" |
| **automate** | Wire a scheduled pipeline with fail-alerts and cache discipline. | "automation", "schedule job", "chạy hàng ngày", "alert khi lỗi" |
| **report** | Build a stakeholder deliverable from a locked template: storyline, chart anatomy, dual-comparison KPIs, portal publish. | "build báo cáo", "làm report", "build dashboard", "làm slide", "convert sang PPTX" |
| **deliver** | Build-auto execution loop wrapping any build mode: spec-or-STOP, clean baseline, single batch approval, per-task RED to GREEN to build to commit + verify gate, stop-on-error/risk, evidence summary. | "build it autonomously", "chunk and commit per task", "deliver end to end", "/build auto" |
| **submit** | Final acceptance gate before a recurring report goes to a team's submission system: completeness audit vs the team's section contract, route gaps to the builder, per-section quality_check, emit a ready-to-paste payload. Ships a <product> bi-weekly profile. | "submit report", "finalize trước khi nộp", "đã đủ mục chưa", "fit yêu cầu quản lý chưa" |
| **review** | Audit a deliverable or a whole project. 3 sub-modes: delivery refine, full project audit, stakeholder questioning. | "review report", "OK chưa", "audit project", "góp ý" |
| **fix** | Surgically debug a pipeline or report, with a patch-ceiling escalation rule. | "fix pipeline", "report sai", "wrong number", "pipeline fail" |
| **workspace** | Scaffold, organize, and index a whole workspace into the second brain above (taxonomy + memory layer + index). Guide-first for non-technical users; secrets-first, safe `git mv` on a branch, index last. | "dọn workspace", "sắp xếp lại thư mục", "file nằm khắp nơi", "organize my workspace", "rebuild index" |

A non-technical user never has to learn these modes or their jargon: they ask in plain language and prof-DA routes, confirms intent, and runs the right one. Each mode auto-fires on phrases like these, so a command is rarely needed; the full trigger lists live in each mode's `SKILL.md`. For the deeper structure, `frame` runs 4 planning gates and `model` offers 4 warehouse patterns: see [mode-frame](skills/da/references/mode-frame.md) and [mode-model](skills/da/references/mode-model.md).

## What it enforces

Every deliverable passes 4 universal rules plus an entry gate. This is what keeps output consistent and rigorous across sessions and across whoever is driving.

1. **Orientation block:** every deliverable opens with a short framing (SCQR, a 3-line intro, or a module docstring) so the reader gets the point before the detail.
2. **Baseline, noise, impact:** every number is stated against a baseline, checked for whether it is real or noise, then given an impact verdict. No bare figures.
3. **5W1H action brief:** every recommendation fills 8 fields (question, goal, what, why, who, when, where, how) so it is actionable, not vague.
4. **Why-explanation:** every action, method, threshold, and tool choice carries an inline reason (causal, empirical, comparative, theoretical, or operational). A circular "X because X" is rejected.

The **Detail-Level Gate** sits in front of all four: every mode confirms Quick / Standard / Deep before running. Depth is the lever you control. The plugin deliberately does not surface time estimates, because LLMs routinely mis-estimate duration.

On top of the rules sit a 5-criteria quality check and a 5-gate quality pipeline (scope -> data -> analysis -> visuals -> review). Stakeholder visuals follow Storytelling-with-Data discipline (action titles, grey plus one accent, no pie or 3D): see [storytelling-with-data](skills/da/references/storytelling-with-data.md).

For recurring, structured reports (weekly / bi-weekly / monthly), an optional **section contract** pins the required sections and grades each against its own definition-of-done; the `submit` mode runs that gate and emits the submission payload before the report leaves for the team manager or system. The shipped <product> bi-weekly profile is the worked instantiation. See [recurring-report-contract](skills/da/references/recurring-report-contract.md).

Two mechanisms make these non-optional rather than advisory. A **Stop-hook** blocks a `report`-mode turn from ending until the deliverable passes the consistency gate (the model cannot quietly skip validation). A **learning loop** captures your corrections at session end and updates the rule the agent reads next time, so a repeated mistake becomes a permanent fix instead of a recurring one.

## What is inside

prof-DA is one root skill plus thin per-mode stubs, a script stdlib, method specs, and 3 support agents. The deep material lives in the linked files; this README stays a map.

```
skills/
  da/                      root skill: rules, protocols, references
    references/            deep docs (modes, methods, governance, SWD, schema)
    scripts/               19 stdlib scripts (run, never inline, statistics)
  frame, model, query ...  12 thin mode stubs that load the root skill
commands/                  13 slash commands (1 entry + 12 modes)
agents/                    3 support sub-agents
```

- **19 stdlib scripts** (`skills/da/scripts/`): stats (effect size, significance, MDE, bootstrap CI, multiple testing), causal (DiD / event study, parallel-trends), formatting, and validators (orientation, action brief, AI-tell scan, rubric audit, method-maturity audit, report consistency, section-contract, artifact-presence, anti-rationalization, self-check). Script-over-agent-compute is a hard rule: statistics always run in a vetted script, never guessed inline. See [scripts-guide](skills/da/references/scripts-guide.md).
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

**<organization> users:** an optional extension bundles the Semantic Cube, the <org-data-mcp> and <org-catalog> MCPs, OpenMetadata curation, and the A1-A12 house slide/report skin. See [org-extensions](skills/da/references/org-extensions.md). Everyone else can ignore it.

## A reference standard

prof-DA hard-codes no engine, schema, or brand, and ships no credentials. The <organization> stack (Semantic Cube, the <org-data-mcp> and <org-catalog> MCPs, OpenMetadata, the A1-A12 house templates) is the **first instantiation**, isolated in [org-extensions](skills/da/references/org-extensions.md); everything else is portable.

The intent is bigger than one plugin. prof-DA is meant as a **reference blueprint for the canonical agentic data workflow** (intent-gating, schema discovery, audited statistics, grounded memory, locked deliverables, enforced validation) that any future agentic data assistant, on any stack and for any org, can adopt and instantiate. <organization> is where it was proven first; the workflow is the part meant to outlive it.

## Versioning

Current version `3.17.0`. Full history, including the v3.4 rename from `prof-data-analyst`, is in [CHANGELOG.md](CHANGELOG.md).

## Contributing

Issues and pull requests are welcome at [loctu0402/prof-DA](https://github.com/loctu0402/prof-DA). prof-DA is distilled from one analyst's daily practice, so real-world gaps and counter-examples are the most useful feedback.

## License

MIT. See [LICENSE](LICENSE).

## Author

Method by Loc Tu (loctu), 2026. Distilled from personal practice.
