# prof-DA

**prof-DA turns your AI coding agent into a disciplined data analyst that anyone can drive, analyst or not.** Ask for a number, a chart, a root cause, or a stakeholder report, in Vietnamese or English, and it runs a fixed, governed analyst workflow instead of improvising, so the answer is consistent, checkable, and reads the same every time.

- **What it is:** a plugin that wraps your agent (Claude Code, Codex, Gemini CLI, GitHub Copilot, or Cursor) in 12 analyst modes (`frame -> model -> query -> process -> insight -> automate -> report`, plus `deliver` / `submit` / `review` / `fix` / `workspace`) behind one natural-language entry point.
- **Who it's for:** not only data analysts and analytics engineers. It is built so **business stakeholders and non-technical users can self-serve data** and still get an analyst-grade result, and so the experts get rigor and consistency instead of improvisation. The aim is **consistent, high-quality, trustworthy self-serve output**, first and foremost for <organization> stakeholders.
- **The problem it kills:** a stock LLM guesses which metric you meant, queries a schema it never checked, returns a bare number with no signal-vs-noise read, and formats every report differently. Plausible-but-wrong answers slip through. Nothing is reproducible.
- **The guarantee:** any session, on any engine, driven by anyone, produces work that reads like the same senior analyst made it.

`v3.20.0` · MIT · runs on Claude Code / Codex / Gemini CLI / GitHub Copilot / Cursor · engine-agnostic: BigQuery / Postgres / Snowflake / Redshift / DuckDB

## The whole system on one page

![prof-DA architecture: 6 nested loops from per-request to cross-session](docs/prof-da-architecture.svg)

Read it like a clock: a request flows down the lanes (intent gate -> grounding -> mode run -> gate stack -> cycle contract), the learning loop writes what it learned back into the second brain, and the next request starts deeper than the last. The compound chain is the product.

**New here?** [docs/GUIDE.md](docs/GUIDE.md) is the full written walkthrough — every mode, the enforcement spine, how it auto-fires, and the self-operating maintenance loops (curator / hard memory budget / anti-drift / subagent walls) derived from studying Hermes Agent.

## Why this matters now

Anthropic's own write-up, [How Anthropic enables self-service data analytics with Claude](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude), shows Claude can already automate roughly 95% of business analytics queries, but **only once the foundation exists**: canonical data, a semantic source-of-truth, encoded skills, and validation. The same piece names the parts that stay hard: **concept-entity ambiguity** (a question maps to "hundreds of viable options"), **data staleness** ("definitions and schemas change constantly"), **retrieval failure**, and **silent failures**, the plausible answers that are simply wrong, which it flags as still unsolved.

So the differentiator is no longer "can the agent query data." Vanilla Claude can run the steps. prof-DA is the layer that **operationalizes that blueprint for a real org**: it ships the skills, the validation, the consistency, and the grounding so you do not rebuild them every session, and so a non-expert's self-serve answer is one you can actually trust. The three things it adds beyond vanilla Claude are next.

## Where prof-DA fits the blueprint

The blog's stack has four tiers: **Data Foundations** (modeled, tested, fresh tables), **Sources of Truth** (the semantic layer, lineage, and a business knowledge base, i.e. the ground truth), **Skills** (the encoded procedural knowledge that actually runs an analysis), and **Validation** (the checks that catch the plausible-but-wrong answer).

**prof-DA is the Skills + Validation layer, the enabler and executioner.** It ships the encoded skills (the 12 modes) and the validation spine (the universal rules, the audited scripts, the gates, the reconcile pass) so a non-expert's self-serve answer runs to one standard and can be trusted, without rebuilding any of it per session. This is the layer the blog calls the source of the 21% -> 95% accuracy jump.

**What prof-DA does NOT build yet, by design:** the foundation tiers, Data Foundations and the Sources of Truth (the semantic layer, the ground truth, the domain knowledge base). prof-DA **consumes** them through the workspace second brain when they exist (it reads your curated memory + index to ground every mode), but standing them up is a separate data-modeling / analytics-engineering process today, not part of prof-DA.

**Roadmap:** close the loop end to end, so a DA/AE can build the domain knowledge base and the semantic source-of-truth **with** prof-DA, not just consume a pre-built one, turning it from the executioner of the blueprint into a partner for standing the whole blueprint up.

## What makes prof-DA different

Three layers vanilla Claude leaves you to build yourself. Each maps onto a failure mode above.

### 1. The build-once-lock report protocol: 12 archetypes, fork-or-fail

Every deliverable **forks one of 12 locked report archetypes (A1-A12) 1:1** and swaps in data; it never freestyles a layout. The set covers the full DA surface: **A1** deep-dive, **A2** ops dashboard, **A3** editorial paper, **A4** daily email, **A5** Google Chat card, **A6** slide deck (the IA pin), **A7** exec one-pager, **A8** idea-verification, **A9** training, **A10** data-quality, **A11** projection, and **A12** slide-deck / editable-PPTX. They share one design contract: a token palette, the verdict vocabulary, the chart-choice matrix, and the AI-tell bans, all governed by a build-once-then-lock playbook.

Why it matters: per-report style drift is the tell of an untrustworthy self-serve tool. When every output reads like the same senior analyst made it, a business stakeholder can trust it at a glance, with no analyst in the loop. `report` mode enforces fork-or-fail (a README-only template stub triggers a design handoff, never a freestyle). See [storytelling-with-data](skills/da/references/storytelling-with-data.md) and [output-slide-deck](skills/da/references/output-slide-deck.md); the locked archetype library lives in your workspace's `shared/templates/` (the A1-A12 set is <organization>'s reference instantiation).

### 2. The workspace second brain: consolidated, current, per-task

`workspace` mode **builds and maintains** a second brain: a clean taxonomy, a memory layer of your domains, metrics, conventions, and past decisions, and a navigable index that **every other mode reads on entry**. The agent starts grounded in your real entities instead of guessing them.

But a memory that only grows rots, so the brain is kept **current and consolidated**, not written once and forgotten. A curator pass merges duplicate notes and surfaces orphans; freshness and staleness checks flag knowledge that has drifted from its source; the index is rebuilt as files move; and a reconcile loop confirms what actually changed. The result is one up-to-date, de-duplicated knowledge layer the agent can trust on every task, instead of a growing pile of stale notes. The conventions, rules, and hooks that govern how work is filed and retrieved are part of this layer too, so the workspace stays operated to one standard rather than ad-hoc per session.

Why it matters: this is the direct answer to the blog's three open problems. Grounding in curated domain memory collapses **concept-entity ambiguity**; the index makes the right context **retrievable** instead of lost; the maintain + consolidate + freshness loop fights **staleness** continuously, not once. Division of labor: the standalone `workspace-brain` skill builds, seeds, and curates the brain; prof-DA consumes it on every mode entry. See [mode-workspace](skills/da/references/mode-workspace.md).

### 3. The enforcement layer: a rule-governed, PM-grade work environment

The plausible-but-wrong answer is the hardest problem, and an ordinary agent has no defense: it answers from a blank context, calls it done, and moves on. prof-DA runs **every task the way a project manager would** - a per-task DoR / DoD / AC contract (injected, not optional, depth-scaled), a just-enough spec with a durable work cache so a compacted session never drops an ask, the 5 universal rules + 23 audited scripts on the deliverable, and a verify -> doubt -> reconcile gate before "done" (an evidence ladder + an anti-rationalization checklist + an adversarial doubt pass + an independent MET / PARTIAL / MISSED reconcile). Multi-step builds run 1 task = 1 commit, stopping on the first failure or irreversible step. Hooks make it non-skippable; prof-DA ships its own gates and consumes the `workspace-brain` governance layer for the rest. Full detail: **[What it enforces](#what-it-enforces)**.

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
/plugin list      # prof-DA 3.20.0 should appear
```

Both steps are required (if Step 2 says `Marketplace ... not found`, Step 1 was skipped). Update with `/plugin update prof-DA@loctu-marketplace`, uninstall with `/plugin uninstall prof-DA`. Upgrading from the old `prof-data-analyst` package (v3.3 or earlier)? Uninstall it first - the namespace and repo were renamed ([CHANGELOG.md](CHANGELOG.md)).

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

## The 12 modes, in two groups

Two layers. **Execution modes** run the analysis along the six-phase lifecycle; **Governance modes** are cross-cutting (enforce the rules + review-discipline, fix, finalize to a contract, systematize the workspace into a second brain). A non-technical user never learns the names: they ask in plain language and prof-DA routes.

- **Execution (the 6-phase pipeline):** `frame` (ask: scope + metric contract) -> `model` + `query` (prepare: schema design + NL-to-SQL) -> `process` (process: clean / EDA / predictive modeling) -> `insight` (analyze: diagnostic + causal method) -> `report` (share: stakeholder deliverable from a locked template) -> `automate` (act: scheduled pipeline + fail-alerts).
- **Governance (run any time):** `deliver` (gated build-auto loop), `submit` (recurring-report acceptance gate), `review` (6-tier audit + staleness re-sync), `fix` (surgical debug), `workspace` (scaffold + index + consolidate the second brain).

The full per-mode table, the auto-fire trigger phrases, and each mode's sub-flows (`frame`'s 4 planning gates, `model`'s 4 warehouse patterns, the 5 `review` tiers) are in **[GUIDE section 3](docs/GUIDE.md)**.

## What it enforces

Every deliverable passes **5 universal rules** (4 quality - orientation block, baseline-noise-impact, 5W1H action brief, why-explanation - behind a Detail-Level Quick/Standard/Deep gate), and every task runs under a **per-task governance contract** (DoR / DoD / AC, scaled by depth; Epic -> Feature -> Story + RAID at Deep) - the PM-grade discipline a blank-context agent lacks. Intent is pinned in a just-enough spec; work-in-progress is cached to disk so nothing drops across a compaction.

A task is "done" only on **evidence** (a run, a rendered artifact on disk, a corrected number, never "seems right"), defended by an anti-rationalization checklist and a **doubt pass** (an adversarial self-review that tries to DISPROVE the result, not confirm it); then an **independent reconcile** diffs delivered work against the captured asks (MET / PARTIAL / MISSED). Multi-step builds run 1 task = 1 commit with a per-task verify gate, stopping on the first failure or irreversible step; when one asset changes, a staleness-trace re-syncs its dependents.

**Hooks make all of this non-optional, not advisory:** a per-prompt pass injects the contract; Stop-hooks block a turn until the deliverable passes its consistency gate, the asks reconcile, and a claimed artifact is proven present; index-first retrieval + an llm-wiki size budget + a curator consolidation pass + subagent depth-1 walls keep the workspace healthy; a learning loop turns each correction into a permanent rule. prof-DA **ships** its own gates (report-consistency Stop-gate, intent dispatch + auto-fire, learning capture) and **consumes** the standalone `workspace-brain` governance layer for the rest, with in-plugin copies of the discipline so the behavior holds even when run alone. The requirements ledger is **project-keyed and append-only**, surviving across chat sessions (a new session continues your open asks instead of restarting blank), and the done-gate clears only on an **independent review receipt**, not self-ticked boxes; that enforcement is portable via `python adapters/gate.py`, so the same "2nd brain" discipline runs on Codex, Gemini, Cursor, and Copilot, not only Claude Code. See [Governance - the agent as your second brain](docs/governance.md).

Full detail (the 5 rules, the contract, the loops, the hooks): **[GUIDE sections 4-5](docs/GUIDE.md)** + the `execution-discipline` / `evidence-based-done` / `build-auto` references. For recurring reports, an optional **section contract** grades each section against its definition-of-done (`submit` mode); stakeholder visuals follow Storytelling-with-Data discipline.

## What is inside

prof-DA is one root skill plus thin per-mode stubs, a script stdlib, method specs, and 3 support agents. The deep material lives in the linked files; this README stays a map.

```
skills/
  da/                      root skill: rules, protocols, references
    references/            deep docs (modes, methods, governance, SWD, schema)
    scripts/               23 stdlib scripts (run, never inline, statistics)
  frame, model, query ...  12 thin mode stubs that load the root skill
commands/                  13 slash commands (1 entry + 12 modes)
agents/                    3 support sub-agents
```

- **23 stdlib scripts** (`skills/da/scripts/`): stats (effect size, significance, MDE, bootstrap CI, multiple testing), causal (DiD / event study, parallel-trends), formatting, and validators (orientation, action brief, AI-tell scan, rubric audit, method-maturity audit, report consistency, section-contract, artifact-presence, anti-rationalization, self-check, skill-security scan, PII classification + gate, lifecycle audit). Script-over-agent-compute is a hard rule: statistics always run in a vetted script, never guessed inline. See [scripts-guide](skills/da/references/scripts-guide.md).
- **14 method specs** (`skills/da/references/methods/`): DiD, event study, RDD, synthetic control, PSM, IV, bootstrap CI, robustness, sensitivity, falsification, multiple testing, post-hoc power, cross-validation, pre-registration. Each cites a primary source. See [methods/_index](skills/da/references/methods/_index.md).
- **3 support sub-agents** (`agents/`), spawned only when value beats cost: `da-orchestrator` (intent + plan + final-review gate), `da-context-tracer` (multi-file reads for big-project review), `da-method-auditor` (causal-method judgment).
- **Governance + quality tooling** (mirrored into the modes): a skill/workflow **security scanner** (`review` / package targets), **PII detection + 4-tier data-classification** (`model` governance), the per-phase **lifecycle execution-rules** + the **Agile-vs-BABOK** track fork (`delivery-lifecycle`), and review **Sub-mode E - Lifecycle Compliance** (presence-proof scan of all 7 phases -> Ship/Fix/Rebuild verdict).

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

Current version `3.20.0`. Full history, including the v3.4 rename from `prof-data-analyst`, is in [CHANGELOG.md](CHANGELOG.md).

## Contributing

Issues and pull requests are welcome at [loctu0402/prof-DA](https://github.com/loctu0402/prof-DA). prof-DA is distilled from one analyst's daily practice, so real-world gaps and counter-examples are the most useful feedback.

## License

MIT. See [LICENSE](LICENSE).

## Author

Method by Loc Tu (loctu), 2026. Distilled from personal practice.
