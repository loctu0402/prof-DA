# prof-DA — The Complete Guide

> One document to understand the whole plugin: what it is, every mode, what it enforces, how it auto-fires, and the self-operating maintenance loops it adds on top of a workspace. The [README](../README.md) is the one-page map; this is the full read. The [architecture poster](prof-da-architecture.svg) is the visual.

---

## 1. What prof-DA is, in one breath

prof-DA turns Claude Code into a **disciplined data analyst that anyone can drive**. Ask for a number, a chart, a root cause, a forecast, or a stakeholder report — in Vietnamese or English — and instead of improvising, it runs a fixed, governed analyst workflow. The result is consistent, checkable, and reads like the same senior analyst made it every time.

It is built so **non-technical stakeholders can self-serve** and still get analyst-grade output, and so experts get rigor instead of improvisation.

**The problem it kills:** a stock LLM guesses which metric you meant, queries a schema it never checked, returns a bare number with no signal-vs-noise read, and formats every report differently. Plausible-but-wrong answers slip through. Nothing is reproducible. prof-DA is the layer that closes each of those gaps.

---

## 2. The shape: one root skill, 12 modes, an enforcement spine

```
You ask (plain VN/EN)
   -> intent gate (confirm WHAT + a Detail Level: Quick / Standard / Deep)
   -> grounding (read the workspace second brain; discover schema 5-tier)
   -> route to 1 of 12 modes
   -> the mode runs (statistics in audited scripts, never eyeballed)
   -> gate stack (4 quality rules + fork-or-fail templates + a Stop-hook gate)
   -> deliver
   -> the learning loop turns your correction into a permanent rule
```

You rarely type a command — prof-DA auto-fires on natural language (see §6). To start explicitly: `/prof-DA:da` (confirms intent + detail level, then routes).

---

## 3. The 12 modes

The standard lifecycle runs left to right; `deliver` / `submit` / `review` / `fix` / `workspace` are orthogonal and run any time.

`frame -> model -> query -> process -> insight -> automate -> report` + `deliver` / `submit` / `review` / `fix` / `workspace`

| Mode | What it does | When it fires |
|------|--------------|---------------|
| **frame** | Turn a vague ask into a locked plan: business understanding, Metric Contract, data plan. Outputs `PLANNING.md`. | "không biết bắt đầu", "metric nào phù hợp", "tính tiềm năng", project kickoff |
| **model** | Design the warehouse SCHEMA: Kimball star / dbt staging-to-marts / Medallion / DuckDB layered, with Table Contracts. (Schema design only — forecasting/ML routes to `process`.) | "design DWH", "build mart", "dbt project", "chia bảng thế nào" |
| **query** | Natural language to SQL with semantic-first discovery, a 5-tier schema hierarchy, a cost-safety check, and a logic card. | "cho mình số liệu", "lấy data", "tỷ lệ X", "breakdown theo Y", "compare X vs Y" |
| **process** | Raw -> staged -> cleaned -> mart -> ML-ready. EDA, data-quality audit, cleaning, feature engineering. **Home of predictive modeling**: forecast / time-series / seasonality / churn / scoring / segmentation -> `ml_`/`pred_` layers. | "EDA", "data quality", "feature engineering", "dự đoán", "forecast", "seasonal", "SARIMA / Prophet", "churn prediction" |
| **insight** | Hypothesis -> diagnostic -> recommendation. Matches the right causal method, guards against bias. | "tại sao X giảm", "root cause", "vì sao", "deep dive", "correlation" |
| **automate** | Wire a scheduled pipeline with fail-alerts and cache discipline. Engine-agnostic (Airflow / Dagster / Prefect / cron / GitHub Actions). | "automation", "schedule job", "chạy hàng ngày", "alert khi lỗi", "backfill" |
| **report** | Build a stakeholder deliverable from a locked template: storyline, chart anatomy, dual-comparison KPIs, portal publish. HTML / PDF / email / Gchat / slides / editable PPTX. | "build báo cáo", "làm dashboard", "làm slide", "convert sang PPTX" |
| **deliver** | Run an approved build as a gated autonomous loop (build-auto): spec-or-STOP, clean baseline, single batch approval, then per-task RED -> GREEN -> build -> commit + verify gate, stop-on-error/risk, evidence summary. Wraps any build mode (the HOW, not the WHAT). | "build it autonomously", "chunk and commit per task", "deliver end to end", "/build auto" |
| **submit** | **Final acceptance gate** before a recurring report goes to a team's submission system: completeness audit vs the team's section contract, route gaps to the builder, per-section quality_check, emit a ready-to-paste payload. Distinct from review (judges quality); submit judges completeness + acceptability + readiness. Ships a <product> bi-weekly profile. | "submit report", "finalize trước khi nộp", "đã đủ mục chưa", "fit yêu cầu quản lý chưa" |
| **review** | Audit a deliverable or a whole project. 6 tiers: A0 brief / A delivery polish / B full project audit / C stakeholder questioning / D staleness trace / E lifecycle compliance (scan a project for all 7 lifecycle phases). | "review report", "OK chưa", "audit project", "góp ý", "sửa xong sync giúp" |
| **fix** | Surgically debug a pipeline or report. Bug triage tree, cache verify, patch-ceiling escalation. Never edits the generator for an HTML patch (overlay instead). | "fix pipeline", "report sai", "wrong number", "pipeline fail" |
| **workspace** | Scaffold, organize, and index a whole workspace into a navigable second brain — plus the self-operating maintenance loops in §5. | "dọn workspace", "sắp xếp lại thư mục", "organize my workspace", "rebuild index" |

A non-technical user never learns these names: they ask in plain language and prof-DA routes.

---

## 3b. Inside each mode — the intentional sub-flows

A mode is not a single script. Each is a small designed workflow with **named sub-flows you can steer** — picked by depth, by data situation, or by output target. They are deliberate; this table surfaces them so the design is visible at a glance instead of buried in the reference files. Knowing them is how you use a mode to its full depth, not just its default path.

| Mode | Sub-flows (the designed mini-workflows inside it) |
|------|---------------------------------------------------|
| **frame** | 4 confirm-gates: Business Understanding -> Metric Define -> Data Plan (**TH1** reuse existing data / **TH2** new model needed) -> Lock & Hand-off. Outputs `PLANNING.md`. |
| **model** | Pick 1 of **4 warehouse patterns** via a decision flow — Kimball star/snowflake · dbt staging->marts · Medallion bronze/silver/gold · DuckDB layered — then write a Table Contract per table and a safe schema-evolution plan (rename / drop / grain-change). |
| **query** | Semantic-first discovery -> **5-tier schema resolution** -> cost-safety check -> NL-to-SQL -> **self-correction loop** (run, read the error, fix) -> a logic card that explains the query back to you. |
| **process** | Milestones **M1 -> M5**: raw -> staged -> cleaned -> mart -> `ml_`/`pred_`. Two standalone sub-flows you can call alone: **Data-Quality Audit** (7-check) and **Cleaning**. 6-step EDA per phase. **Predictive modeling lives here** (forecast / time-series / seasonality / scoring / segmentation / churn). |
| **insight** | Hypothesis -> diagnostic -> recommendation, with the anti-bias protocol, **causal-method matching** (DiD / event-study / RDD / ...), market-correlation, and turning-point analysis. |
| **automate** | Build the scheduled pipeline -> wire **fail-alert** (email / Gchat) -> cache discipline -> **backfill** flow. Engine-agnostic: Airflow / Dagster / Prefect / cron / GitHub Actions. |
| **report** | **10 steps** (3 are hard `[GATE]`s): 0 scaffold `[GATE]` · 1 audience+format · 2 fork a locked template — fork-or-fail `[GATE]` · 3 wire data · 4 orientation block · 5 body (baseline-noise-impact + 7-element chart anatomy) · 6 recommendations · 7 self-check · 7.5 HTML-SPA structural inspect · 8 save + validation receipt · 9 portal publish `[GATE]`. **Output channels:** HTML SPA / PDF / email / Gchat card / slide deck / editable PPTX. |
| **deliver** | **7-gate build-auto loop:** 0 spec/charter-or-STOP `[GATE]` · 1 clean baseline · 2 plan into tasks · 3 single batch approval `[GATE]` · 4 per-task RED/GREEN/build/commit · 5 per-task verify gate · 6 stop-on-failure/risk/irreversible · 7 evidence summary. One task = one commit; drops a validation receipt. Wraps any build mode. |
| **submit** | **Steps 0 -> 6:** identify team + load contract `[GATE]` · structure audit · gap punch-list + route to the builder · per-section quality_check · carry-forward check · build payload · readiness checklist `[GATE]` -> hand off (never auto-submits). |
| **review** | **6 tiers, pick by depth:** A0 quick brief · A delivery polish · B full project audit (spawns the context-tracer + method-auditor sub-agents) · C stakeholder questioning · D staleness trace (after a change, sync every dependent asset) · E lifecycle compliance (presence-proof scan of all 7 phases -> Ship/Fix/Rebuild). |
| **fix** | Bug-triage decision tree -> cache verify -> numerical / silent-data-layer debug -> patch via **overlay** (never edit the generator) -> **patch-ceiling escalation** after 3 patches -> wire email-on-fail. |
| **workspace** | **7 sub-modes:** GUIDE (orchestrates the rest) · SCAFFOLD (fresh) · ORGANIZE (existing mess) · INDEX (**build / update / rebuild** + reverse-existence check) · SETUP (install hooks) · DISCOVER (seed memory) · CURATOR (periodic consolidation). Plus the self-operating loops in §5. |

**How to steer a sub-flow:** just name it — "rebuild the index" (not just update), "review tier B / full audit", "model with Medallion", "submit for <product>", "data-quality audit only". The router picks the variant; an explicit `/prof-DA:<mode>` drops you straight in.

---

## 4. What it enforces (the rigor that makes it trustworthy)

Every deliverable passes **4 quality rules** plus an entry gate:

1. **Orientation block** — every deliverable opens with a short framing (SCQR / 3-line intro / docstring) so the reader gets the point before the detail.
2. **Baseline -> Noise -> Impact** — every number is stated against a baseline, checked for real-or-noise, then given an impact verdict. No bare figures.
3. **5W1H action brief** — every recommendation fills 8 fields (question / goal / what / why / who / when / where / how) so it is actionable.
4. **Why-explanation** — every action, method, threshold, and tool choice carries an inline reason. A circular "X because X" is rejected.

In front of all four sits the **Detail-Level Gate** (Quick / Standard / Deep) — depth is the lever you control.

Three mechanisms make these non-optional rather than advisory:

- **Stop-hook gate** — a `report`-mode turn cannot end until the deliverable passes the consistency audit; and the workspace-brain `evidence_done_gate` blocks a turn until a claimed artifact is proven present. The model cannot quietly skip validation.
- **Doubt pass** — before a high-stakes claim ships, an adversarial self-review (CLAIM -> EXTRACT -> DOUBT -> RECONCILE, bias-to-disprove, no rubber-stamp) actively tries to break the result. It is the negative complement to the positive evidence ladder + the anti-rationalization checklist (`references/execution-discipline.md`). Runs at deliver Gate 7 and is review Sub-mode B at project scale.
- **Learning loop** — your corrections are captured at session end and become the rule the agent reads next time, so a repeated mistake becomes a permanent fix.

Plus: **23 audited stdlib scripts** (statistics always run in code, never guessed inline), **14 cited causal-method specs** (DiD, event study, RDD, synthetic control, PSM, IV, bootstrap CI, robustness, sensitivity, falsification, multiple testing, post-hoc power, cross-validation, pre-registration), the **12 locked report archetypes (A1-A12)** every deliverable forks 1:1 (never freestyles), and Storytelling-with-Data visual discipline.

---

## 5. The self-operating loops (Hermes-derived) — what keeps a workspace alive

Scaffold + organize + index is a one-time setup. A workspace that is governed but never maintained still rots: the index bloats, notes duplicate, long sessions drift off the original ask, and delegated subagents corrupt the shared layer. These four loops are the **maintenance layer**, distilled from studying the [Hermes Agent](https://github.com/NousResearch/hermes-agent) self-improvement loops. The `workspace` mode documents the portable statement; the standalone `workspace-brain` skill ships the live enforcement (hooks + scripts).

1. **Curator (periodic consolidation).** On a cadence or on demand: merge near-duplicate notes into one class-level note, surface orphan atoms (in no index, cross-linked nowhere), flush the log -> digest backlog, re-validate index pointers. **Invariants (non-negotiable): never auto-delete (archive only, recoverable); pinned items bypass; candidates need human approval; the scan is read-only.** A pass that finds nothing prints a silent no-op, not noise.

2. **Hard memory budget (consolidate, don't append).** Index/memory files are read every session, so unbounded growth taxes every load. The contract is enforced AT WRITE TIME: a write that grows an over-cap index/memory file is rejected with a "consolidate" instruction (index <= 200 lines, atom <= 300, one line per entry), not a soft warning — with a flat/shrink allowance and an `allow-oversize: <reason>` escape so it never traps an already-oversize file.

3. **After any context compaction.** The summary is background reference, NOT active instructions; the **latest user message wins** over it; reverse signals ("stop", "undo", "just verify", "never mind", a new topic) end in-flight summarized work immediately; persistent memory stays authoritative; re-read any open requirements after compaction (a summary can drop an open ask — the "70% done, reported done" failure).

4. **Subagent hard walls.** A spawned subagent must NOT write shared memory, push git / send external messages / publish, or spawn further subagents. The parent centralizes stateful writes after QC and is accountable for what ships. Give the child READ + its one narrow task only.

5. **Index-first retrieval.** Navigation is by map, not by scan: a session-start hook loads `.index/_root.md` first, a guard nudges checking the BookRAG index before any brute-force grep/glob (progressive disclosure), a write-time hook flags the index stale after structural changes, and a Stop-time check blocks on a stale index. Plus the scaffold pre-check guard that nudges classify-type + grep-duplicate before a new project folder is created.

There is also an **opt-in post-session self-review** (Hermes loop 3, adapted): after a session, a restricted background pass can extract durable preferences/techniques into memory. It is **default-off** because it spends tokens every session; the user turns it on explicitly. (Lives in `workspace-brain`, not this plugin.)

> Why this framing matters: studying Hermes clarified that **Claude Code already has the primitives** (subagents, compaction, scheduled tasks, skill files). What it lacked was the **wiring** — triggers that fire those primitives automatically to feed each other. These loops are that wiring, applied with safety invariants (never-delete, budget-gated writes, blocked-tools walls, fail-open).

---

## 6. How it auto-fires (you rarely type a command)

Three stacked layers make prof-DA fire on natural prompts (added v3.14):

1. **SessionStart dispatch** — a standing protocol injected each session: any DA-shaped request invokes `prof-DA:da` before responding, with a 12-mode map and a rationalization red-flag list.
2. **Per-prompt intent detector** — a deterministic keyword floor under the probabilistic matching: it folds the prompt to diacritic-free lowercase ("dự đoán" == "du doan"), scans mode-grouped signals, and nudges with the matched keywords + likely mode. Silent on slash commands and non-DA prompts; fail-open.
3. **Mode descriptions** — natural VN + EN trigger phrases per mode.

To force a specific mode, type `/prof-DA:<mode>` — it skips the router.

---

## 7. Configuration (engine-agnostic, ships no credentials)

| Layer | Options |
|-------|---------|
| SQL engine | BigQuery, Postgres, Snowflake, Redshift, DuckDB |
| Semantic layer | Cube.js, dbt-metrics, LookML, or org-specific |
| Notifications | SMTP, Slack, Teams, PagerDuty, internal module |
| Scheduler | Airflow, Dagster, Prefect, cron, GitHub Actions |

Schema discovery follows a **5-tier hierarchy** (owner-curated tag -> catalog API -> access-aware metadata -> INFORMATION_SCHEMA -> sampling). The **semantic layer is the mandatory default path** — query mode resolves the metric there first and falls back to raw SQL only when necessary, which is what collapses concept-entity ambiguity before any SQL is written.

A workspace second brain, when present (`memory/` + `.index/`), is read on entry to ground every mode in your real domains. The standalone `workspace-brain` skill builds and seeds it; prof-DA consumes it.

**<organization> users:** an optional extension bundles the Semantic Cube, the <org-data-mcp> + <org-catalog> MCPs, OpenMetadata curation, and the A1-A12 house skin. Everyone else can ignore it.

---

## 8. Where everything lives

```
README.md                  the one-page map
docs/GUIDE.md              this document
docs/prof-da-architecture.svg   the visual (6 nested loops by time scale)
CHANGELOG.md               version history
skills/da/                 root skill: rules, protocols, references, scripts
  references/              deep docs (per mode, 14 methods, governance, SWD, schema, the self-operating loops)
  scripts/                 23 stdlib scripts (stats / causal / format / validators)
skills/{frame,...,workspace}/   12 thin mode stubs that load the root skill
commands/                  13 slash commands (1 entry + 12 modes)
agents/                    3 support sub-agents (orchestrator / context-tracer / method-auditor)
```

Deeper references worth reading next: `skills/da/references/mode-workspace.md` (the workspace mode + the self-operating loops), `skills/da/references/recurring-report-contract.md` (the submit-mode methodology), `skills/da/references/storytelling-with-data.md` (the visual discipline).

---

## 9. A reference standard, not just a plugin

prof-DA hard-codes no engine, schema, or brand and ships no credentials. The <organization> stack is the **first instantiation**; everything else is portable. The intent is a **reference blueprint for the canonical agentic data workflow** — intent-gating, schema discovery, audited statistics, grounded memory, locked deliverables, enforced validation, and now self-operating maintenance — that any agentic data assistant, on any stack and for any org, can adopt.

---

*Method by Loc Tu, 2026. MIT. Issues and PRs welcome at [loctu0402/prof-DA](https://github.com/loctu0402/prof-DA).*
