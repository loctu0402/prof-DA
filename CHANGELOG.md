# Changelog

All notable changes to `prof-DA` plugin (formerly `prof-data-analyst` through v3.3).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [3.11.0] - 2026-06-03

Tier 3 inline annotation: completes the 3-tier refine menu with a browser-based select-and-comment harness.

### Added
- `scripts/refine/annotate_overlay.js` - self-contained vanilla JS widget: text selection -> "Them gop y" button -> comment popup -> pinned marker -> Export button downloads `comments.json` and mirrors into `#comments-out` textarea.
- `scripts/refine/wrap_annotation_harness.py` - injects the overlay into a copy of the report (`<report>.annotate.html`); the final shipped report is never touched.
- `scripts/refine/parse_comments.py` - `comments.json` -> `[{section, title, anchors, feedback}]` change-set; identical output shape to `parse_feedback.py` so the existing apply step consumes both without modification.

### Changed
- `references/refine-worksheet.md` - Tier 3 section updated from "not yet built" to the real flow.
- `skills/da/SKILL.md` - three new refine scripts registered in the Bundled Scripts tree.

## [3.10.0] - 2026-06-03

Refine protocol (worksheet MVP): a trigger-gated, per-section feedback loop that replaces long imprecise re-prompts and doubles as a fresh-session handoff (context-bloat fix).

### Added
- `references/refine-worksheet.md` - 3-tier feedback protocol (prompt / worksheet / inline), anchor system, apply flow, fresh-session handoff. Tier 3 (inline annotation) is a follow-up.
- `scripts/refine/generate_worksheet.py` - report HTML -> non-tech per-section worksheet (stdlib only).
- `scripts/refine/parse_feedback.py` - filled worksheet -> JSON of filled sections (mechanical extraction).

### Changed
- `mode-report.md` (Step 8b refine loop), `mode-review.md`, `mode-fix.md`, `universal-workflow-rules.md` (trigger rule). No new mode.

## [3.8.0] - 2026-06-02

Workspace governance release: a 10th mode that scaffolds, organizes, and indexes an ENTIRE workspace into a navigable harness — the workspace-level counterpart to the per-project `project-scaffold` discipline. Guide-first for non-technical users.

### Added
- **`/prof-DA:workspace` mode** — `skills/workspace/SKILL.md` (stub) + `commands/workspace.md` + `references/mode-workspace.md`. The survey -> propose -> safe-migrate -> memory -> index loop, generic and domain-neutral (works for a data, marketing, or research workspace). Hard rules: secrets-first, plan->approve->execute, grep-before-move, archive-don't-delete, `git mv` on a branch, index-LAST + reverse-existence check. Includes a guide sub-flow that walks a non-technical user one plain-language step at a time.

### Changed
- **`skills/da/SKILL.md`** — mode router + description: 9 -> 10 modes (added `workspace` as an orthogonal helper); reading-order brace list updated.
- **`commands/da.md`, `README.md`** — mode count 9 -> 10, `workspace` listed; README modes table + structure map updated.
- **`.claude-plugin/plugin.json` + `marketplace.json`** — version 3.7.0 -> 3.8.0; description 9 -> 10 modes.

### Why
The plugin had `project-scaffold.md` (one project's Step-0 layout) and `governance.md` (data governance), but nothing covered the WHOLE-workspace concern: a workspace that accumulated scattered files, has no memory layer, and no index. That is the most common real starting state — especially for non-technical users who began without a system. The mode encodes the safe-migration protocol (distinguish on-disk junk that `.gitignore` already handles from tracked-misplaced files; never move a live-pipeline file without fixing its references) so reorganizing an in-use workspace doesn't silently break scheduled jobs.

## [3.7.0] - 2026-06-01

Self-improving release: a bundled learning loop that captures feedback + corrections from conversation so prof-DA personalises itself, mirroring the host's session-end memory hooks.

### Added
- **`hooks/feedback_capture.py` (Stop) + `hooks/correction_detector.py` (UserPromptSubmit) + `references/learning-protocol.md`.** The agent does the distillation; the hooks are reminders + a real-time flag (a shell script cannot distill a conversation).
  - `correction_detector` is the REAL-TIME catch: when the user's message looks like a correction of an established practice ("you forgot", "we always do X", "dù đã làm nhiều lần") it injects a note to resolve + persist IMMEDIATELY and, for a forgotten practice, fix the instruction so it cannot recur.
  - `feedback_capture` is the session-end catch-all. **Detect-and-defer:** it stays silent when the host already runs its own memory loop (e.g. `~/.claude/hooks/session_end_sync.py`), so it never double-reminds; for users without one it is the only loop. Dedup per session, `stop_hook_active` guard, fail-open.
  - `learning-protocol.md`: detect the memory target (lt-memory / CLAUDE.md / project-local), qualify hard (anti-bloat), and for a FORGOTTEN practice update the instruction layer via a visible agent Edit (never a hook blind-write), not just a memory note.

### Why
prof-DA enforced rules but did not LEARN from being corrected. A recurring forgetting (the same correction twice) is the signal that the fix belongs in the instruction the agent reads next time, not only in recalled memory. This loop closes that path. It defers entirely to a host that already has a memory system, and is the whole loop for users who do not.

## [3.6.0] - 2026-06-01

Enforcement + companion release: a Stop-hook validation gate that makes the report consistency check non-skippable, plus the `loctu-da-stack` companion plugin for guided MCP setup. README rewritten overview-to-detail.

### Added
- **`hooks/stop_gate.py` + `hooks/hooks.json`** - a receipt-targeted, hard-block Stop hook. `report` mode drops `<project>/.prof-da/pending-validation.json`; on Stop the gate runs `report_consistency_audit` on the listed deliverable(s) and BLOCKS the turn from ending until it passes (clearing the receipt on pass). Loop-bounded (attempts <= 5) and fail-open (any internal error allows the stop). Silent on every non-report session (no receipt, no action), so it never false-blocks a README / REVIEW / scratch edit. Gates on `report_consistency_audit` only: the markdown-doc checks (`orientation_block` / `action_brief` / `ai_tell_scan`) false-fail rendered HTML and would trap every report. Verified: silent on no-receipt, BLOCKS the MOAT report (scaffold + portal missing), PASSES + clears on a good v9 report.
- **`loctu-da-stack`** - second plugin in the marketplace (source `./loctu-da-stack`): a guided-setup skill for the DA workflow MCP stack (<organization> Data Portal / exa / Google Drive + Gmail / on-demand Playwright). Ships no credentials; placeholders + local login. A guide, not a bundle (bundling would duplicate user-scope servers + auto-fail off-VPN).

### Changed
- **`mode-report.md` + `skills/report/SKILL.md`** - Step 8 drops the `.prof-da/pending-validation.json` receipt that arms the Stop gate; Step 7 documents the gate + that the doc-checks are advisory for rendered HTML.
- **`README.md`** - rewritten overview-to-detail (tagline, why, install, modes, internals); changelog demoted to a link; stale `v3.4.1` corrected to `3.6.0`; script count corrected 14 to 16.
- **`plugin.json` + `marketplace.json`** - version `3.6.0`; script count 14 to 16; a stray registry em-dash cleaned.

### Why
prof-DA enforced rules in skill text but nothing made the validation step non-skippable: a model could finish a report without ever running the gate. The Stop hook closes that. Receipt-targeting (not file mtime) is what makes it precise: it fires exactly when report mode produced a deliverable, and never otherwise.

## [3.5.0] — 2026-05-29

Report standardization release: a binding C-level evaluation rubric + hybrid consistency gate, project-scaffold discipline, mandatory portal publish (the always-forgotten step), fork-or-fail template discipline, and recent-rule sync.

### Added
- **`references/evaluation-rubric.md`** — single front-door C-level / DA-grade scorecard. 7 weighted categories (Framing & Logic / Data Integrity / Insight Quality / Visual & Design / Language & Tone / Delivery & PM / Verdict), per-criterion GOOD/BAD/score/severity, weighted grade A-F + must-fix gate. Composes existing rules (cross-links, no duplication); grounded in the BA weighted-decision-matrix framework.
- **`references/report-standard-checklist.md`** — the binding pre-ship checklist with `[GATE]` (hard-stop, machine-checked) vs `[ADVISORY]` (scored) items. Same list every session → consistent deliverable shape across Claude sessions.
- **`references/project-scaffold.md`** — Step 0 detect-or-create standard layout (`queries/ scripts/ cache/ data/ output/`); fixes flat-file dumps.
- **`scripts/validators/report_consistency_audit.py`** — hybrid hard-gate validator: empty-as-finding, Vietnamese diacritics, project scaffold, portal-publish receipt; freestyle-palette advisory. Number-reconcile deliberately NOT automated (a naive >10× flag false-positives on legit encodings like `data-countup="2964" data-fmt="tenth"` → 296.4). Wired into `self_check.py` for `.html/.md`.

### Changed
- **`mode-report.md`** — added Step 0 (scaffold), Step 9 (portal publish via `shared/portal_upload.py`, 72h TTL, stable UUID), fork-or-fail at Step 2 (never freestyle a bespoke visual when the template is a README-only stub), consistency gate at Step 7. Reading-order updated. `skills/report/SKILL.md` stub synced.
- **`mode-review.md`** — Sub-mode A0/A now run the consistency gate + score against `evaluation-rubric.md`.
- **`mode-frame.md` / `mode-process.md`** — scaffold-first pointer added.
- **`style-rules.md`** — recent report conventions: business-language-over-jargon (UI), email force-light-mode, data-card-on-hover, projection delta-change flat band (not random-walk cone), editorial-paper-vs-ops-dashboard dual archetype.
- **`style-rules.md` + gate (`commands/da.md`, `universal-workflow-rules.md`)** — added **No Meta-Leak** rule: the user's notes/meta-instructions to the agent and the agent's own directives (e.g. "no time estimate") must NEVER appear in any audience-facing output. Fixes a gate bug where `(không ước lượng thời gian)` leaked into the Detail-Level question shown to the user.
- **`org-extensions.md`** — OM curation: large/rich-Vietnamese batch PATCH (~20+ ops) must push `--one-at-a-time` (a single big array 400s with a misleading "Invalid name" error) — corrects the prior "single atomic batch" advice. Added §7 <organization> reporting conventions (AUM/Balance NSM anchor, MAU/MFU calendar-month, waterfall <product-b> overlay, CRM sentiment VN labels).
- **`SKILL.md`** — registered the new validator + reference docs.

### Why
Real use on the MOAT `tko_tui_plus_ytd_2026` deep-dive surfaced the gaps: every report drifted in visual style (README-only template stubs → freestyle), files dumped flat (no scaffold), the portal link was never published, and recent memory rules (design-handoff, OM batch-patch, projection band, etc.) weren't encoded. The plugin enforced *rules* but not *visual consistency, project structure, or delivery*. v3.5.0 makes those a hybrid gate (hard-stop mechanical + advisory qualitative) so any Claude session produces the same deliverable shape. Validated: the gate FAILs the MOAT report (scaffold + portal missing) and PASSes a `generate_v9.py` output.

## [3.4.1] — 2026-05-19

**BREAKING — GitHub repo renamed.** `loctu0402/prof-data-analyst` → `loctu0402/prof-DA`. Marketplace registration command + remote URL in `marketplace.json` updated. Existing users must `/plugin marketplace remove loctu-marketplace` then `/plugin marketplace add loctu0402/prof-DA` to clear the stale cache.

### Why
v3.4.0 plugin install failed with `Plugin "prof-DA" not found in marketplace "loctu-marketplace"` on machines that had `loctu-marketplace` cached from a `prof-data-analyst` marketplace add. The cache held the old plugin identifier and didn't auto-refresh. Renaming the repo + bumping version forces a full cache invalidation.

### Changed
- **`marketplace.json` source URL** → `https://github.com/loctu0402/prof-DA.git`
- **`marketplace.json` + `plugin.json` version** → `3.4.1`
- **README install commands** — `loctu0402/prof-data-analyst` → `loctu0402/prof-DA`. Removed the v3.4.0 footnote that claimed "repo name unchanged" (no longer true).

## [3.4.0] — 2026-05-19

**BREAKING — major UX refactor.** Plugin rename + skill auto-fire overhaul + Detail Level Gate. To upgrade: `/plugin uninstall prof-data-analyst` then `/plugin install prof-DA@loctu-marketplace`.

### Changed (BREAKING)
- **Plugin renamed** `prof-data-analyst` → `prof-DA`. Shorter slash command namespace (`/prof-DA:query` instead of `/prof-data-analyst:da-query`). `package.json` + `marketplace.json` + `plugin.json` `name` fields updated.
- **Skill folder + name `da-` prefix dropped** for all 9 modes: `skills/da-frame/` → `skills/frame/`, `skills/da-query/` → `skills/query/`, …, `skills/da-fix/` → `skills/fix/`. Root skill folder `skills/prof-data-analyst/` → `skills/da/`. Slash commands renamed accordingly (`commands/da-query.md` → `commands/query.md`).
- **All 10 SKILL.md frontmatter `description` fields rewritten** with aggressive natural Vietnamese + English auto-fire triggers. Real-world failing prompts that motivated this change include "cho mình số liệu của Vay Nhanh 17 ngày đầu tiên của tháng 5..." and "the savings product có tính năng nạp tiền tự động... tìm phương pháp tính cho tôi lượng tiền tiềm năng ở <organization>, xét trên tập user MFU..." — neither triggered the v3.3 descriptions. New descriptions include literal natural phrases like "cho mình số liệu", "lấy data", "tỷ lệ X", "breakdown theo Y", "điều gì xảy ra", "tại sao X", "tìm phương pháp tính", "đo lượng X", "potential size", "MFU cohort", "user cohort", "xét trên tập user", "kickoff", "không biết bắt đầu", "stakeholder muốn", etc.

### Added
- **Rule 5 — Detail Level Gate** added to `references/universal-workflow-rules.md`. Every mode entry confirms Quick / Standard / Deep before executing. NO time estimates surfaced — Claude routinely under-estimates duration; the user controls depth as the lever instead. Hooked into `commands/da.md` and the root `skills/da/SKILL.md` mode router.
- **README "What changed in v3.4" + upgrade-from-v3.3 instructions** with the explicit uninstall-then-install commands.

### Why
v3.3 auto-fire descriptions used jargon phrases ("viết SQL", "NL→SQL", "phân tích insight") that real stakeholder DM prompts never contain. Two stakeholder-shaped prompts tested live, neither invoked the plugin. Root cause: trigger-phrase mismatch between description vocabulary and how users actually phrase data asks. v3.4 inverts the design — descriptions now mirror conversational Vietnamese + English DA vocabulary; jargon stays in the body where it belongs. Detail Level Gate solves the orthogonal complaint that "Standard" workflow occasionally exceeds what a quick stakeholder ping needs (and conversely, advanced cases want falsification / robustness / sensitivity stacked).

## [3.3.0] — 2026-05-18

Minor release: schema-discovery hierarchy + portable semantic-layer recipe + visualization discipline + optional org-specific extensions.

### Added
- **`references/schema-source-hierarchy.md`** — 5-tier ladder: T0 owner-curated LLM tag → T1 catalog tool direct API → T2 access-aware metadata MCPs (per-user-access-filtered) → T3 INFORMATION_SCHEMA + brainstorm with user → T4 sampling. Decision tree, per-tier rationale, audit-vs-trust matrix. T2 placement rationale: T1 catalog API and T3 INFORMATION_SCHEMA both show what the org has, not what the current user can use; access-aware MCPs bridge that gap and bundle multiple metadata sources (catalog + semantic cube + documentation) in one user-scoped interface.
- **`references/semantic-layer-setup.md`** — Portable 6-phase recipe (Discovery → Architecture → Foundation cube template → Layered modeling → Pre-aggregation → Delivery+Governance → Operate). Engine-agnostic (Cube.js / dbt-metrics / LookML / MetricFlow).
- **`references/storytelling-with-data.md`** — Visualization discipline: 6 lessons (Context / Visual / Clutter / Focus / Designer / Story) + 5-rule cheatsheet (action title, grey + 1 accent, no pie / no 3D, clutter checklist, horizontal logic) + preattentive attribute cookbook + Z-pattern + Gestalt application + 10 anti-patterns + per-chart and per-deck pre-ship checklists.
- **`references/org-extensions.md`** — Optional org-specific extension file: Semantic Cube (<semantic-tech> + Cube.js), <organization> unified data MCP gateway (semantic / data-portal / journey / <event-system> tool groups), <org-sql-agent> NL→SQL MCP + tag namespace, OpenMetadata API+PAT curation playbook. Non-<organization> users ignore.
- **`mcp/example-org-mcp.json`** — Drop-in MCP server config snippet for `~/.claude.json` user scope (<org-data-mcp> + <org-sql-agent>). CLI install commands included.

### Changed
- **`references/mode-query.md` Step 0 — Request Intake** (NEW) — Pre-flight phase BEFORE schema discovery. Restate question + surface implicit choices (grain / cohort / aggregation / dedup / window / comparison / breakdown) + propose calculation logic in plain language + suggest 1-2 extensions + user-confirm gate. Documents skip conditions (explicit SQL provided, repeat query, pipeline-internal, fully-atomic ask). Encodes the senior-DA pattern of "structure the question before structuring the answer".
- **`references/mode-query.md` Step 2** — Discovery refactored to 5-tier schema-source hierarchy with cross-reference to new references.
- **`references/mode-report.md` Step 5** — Hooked SWD discipline into body-population: every chart follows action title + grey + 1 accent + clutter checklist + horizontal logic.
- **`references/style-rules.md`** — Added "Visualization discipline (Storytelling with Data)" callout above Chart Anatomy section. 5-rule cheatsheet inline + pointer to full reference.
- **`references/mode-process.md`** — Documented 3 entry granularities: Full pipeline / Quality Audit only / Cleaning only. Trigger phrases expanded to cover "data audit", "data quality", "quality check", "kiểm tra data", "clean data", "data cleaning". Process mode is now the standard discoverable entry for standalone data quality work.
- **`references/mode-frame.md`** — Added "Mid-stream Gate 2 standalone" sub-mode. Allows running Gate 2 (Metric Define) alone when project context already exists and only the metric question needs resolving, without forcing a full 4-gate Frame run.
- **`references/mode-model.md`** — Added "Schema Evolution" section. 9-row safe-migration recipe (add column / rename / drop / split / merge / type change / grain change / partition-key change) with 7 discipline rules + 4 anti-patterns.
- **`references/mode-automation.md`** — Added "Backfill Workflow" section. Decision tree (why → cost → idempotency → lower-bound preservation → cross-validation), 4 execution patterns (`--backfill-from` / chunked / shadow / full rebuild) + 5 anti-patterns.
- **`SKILL.md` "Where to Read Next" + mode router** — Added pointers to schema-source-hierarchy, semantic-layer-setup, org-extensions, storytelling-with-data. Process mode router row updated with data quality trigger phrases.
- **`commands/prof-DA:process.md`** — Updated to surface 3 entry granularities at command-invocation time.
- **`README.md`** — Bumped to v3.3; added Visualization discipline section + Schema discovery + semantic layer section + Optional org-specific extensions section.

## [3.2.2] — 2026-05-15

Patch release: storyline pattern refinement (question-based framing pre-step).

### Added
- **Question-based framing pre-step in `mode-report.md` Step 5 storyline section** — agent drafts `[Q] [A] [Why]` triplet per section BEFORE writing slide title. [Q] = stakeholder question the section answers; [A] = the storyline title that answers it; [Why] = 1-line rationale per Rule 4 (Causal/Empirical/Comparative/Theoretical/Operational). Only [A] appears on slide; [Q] and [Why] stay in working notes. Updated storyline checklist to require Section Question drafted + Why-Explanation logged per section.

### Why
Storyline titles without explicit question framing risk being decoration rather than communication. Question-based pre-step makes (a) why-the-slide-exists legible, (b) predicted result visible before chart-building, (c) action implied because the question is decision-shaped. Aligns with consulting practice (draft question first, then answer, then chart).

## [3.2.1] — 2026-05-15

Patch release: 2 foundational additions. No new modes / agents / breaking changes.

### Added — Section 0 in `metric-framework.md` (KPI Framework foundation)
- `0.1 Definition + Formula`: KPI = Metric × Goal
- `0.2 5-criterion "must"` checklist (tied to business goal / influences decisions / drives action / clear owner / tracked consistently)
- `0.3 From Data to KPI` 4-step protocol
- `0.4 Good vs Bad KPIs` (Vanity vs Actionable)
- `0.5 Think Like a Data Analyst` (4 design principles)
- `0.6 KPI Stress Test` — 3 archetype questions for self-audit (Product Thinking / KPI Judgment / Problem Solving 5-step diagnostic descent)
- `0.7 Workflow plug-in points` (`da-frame` Gate 2, `da-review` Sub-mode B Pass 2, pre-ship stress test)

### Added — Multi-domain dbt project layout in `orchestration-patterns.md` Pattern 2
Portable multi-domain pattern. No proprietary code or credentials.

- 4-layer per domain: `sources → staging (stg_*) → warehouse (fct_*/dim_*) → datamart (agg_*/metric_*)`
- Project-level `vars:` for execute_date (T, T-1, T-3) + partition_date + multi-day sliding-window lists + alert hooks (prod / staging separated)
- Default test ownership via `+meta: PIC: <owner>`
- Phased `dbt run` (build_staging → build_warehouse → build_datamart → run_tests) in DAG config, NOT in dbt itself
- Incremental mart pattern: `insert_overwrite + partition_by + cluster_by + on_schema_change="append_new_columns"` + sliding window via `overwrite_days` set var
- DAG sensor pattern for cross-pipeline dependency
- 6 anti-patterns added (manual dbt run vs build / no source freshness / full-refresh daily / flat models folder / tests without owner / hardcoded dates)

### Changed
- `metric-framework.md` "Overview" updated to mention 4 sections (KPI Framework foundation / decision table / per-framework deep dive / design protocol)
- Plugin v3.2.0 → v3.2.1

## [3.2.0] — 2026-05-15

Additive release: proactive capability discovery — plugin suggests extensions at mode exit instead of waiting for the user to read overview docs.

### Added
- **`references/suggestion-protocol.md`** — 3-step Suggestion Loop: detect context (mode + data source + output format + available MCPs + stakeholder hints) → map to 8 extension categories (data source / automation / quality validation / method upgrade / audience / format / downstream / MCP tooling) → propose with opt-in phrasing. Includes 3 worked examples + per-mode default top-3 fallback.
- **`orchestration-patterns.md` Pattern 5 — Google Apps Script** — Sheet-driven HTML dashboard with auto-refresh. Starter `Code.gs` + `Dashboard.html` template. GCP project + API setup guide + step-by-step manual deploy. Pros / cons / anti-patterns / graduation-path documented.
- **`SKILL.md` new Core Operating Principle: "Proactive Suggestion at Mode Exit"** — codified alongside Script-over-Agent-Compute / Progressive Disclosure / Portable First.
- **`agents/da-orchestrator.md` Exit Suggestion gate** — after final-review verdict (SHIP / FIX / REBUILD), orchestrator runs Suggestion Loop with hard rules (MAX 3 / cite trigger / 1-line Why per Rule 4 / effort estimate / explicit OUT path).

### Changed
- Plugin description: "5 orchestration patterns" (was 4) + "proactive capability discovery" added
- Marketplace description updated to highlight suggestion protocol
- `orchestration-patterns.md` decision table now lists 5 patterns + hybrid note about Apps Script for stakeholder dashboards
- SKILL.md "Where to Read Next" adds "Proactive capability discovery" subsection
- New keywords: `apps-script`, `google-sheets`, `proactive-suggestion`, `capability-discovery`

### Why
Users cannot discover full plugin capability by passively reading overview docs. Proactive suggestion at mode exit (vs. dumping all features upfront) lets the user see relevant options when they have working context to evaluate them. Pattern adapted from consulting: after deliverable, propose "what's next" rather than handing over and walking away.

## [3.1.0] — 2026-05-15

Additive release: front-of-workflow planning + data engineering hooks + brief-tier review.

### Added
- **2 new modes:** `da-frame` (Business Understanding → Metric Define → Data Plan TH1/TH2 → Lock & Hand-off) + `da-model` (4 data modeling patterns: Kimball / dbt staging→marts / Medallion / DuckDB layered)
- **6 new reference files:**
  - `references/mode-frame.md` — Frame mode (4-gate workflow)
  - `references/mode-model.md` — Model mode (4 patterns + Table Contract template + governance hooks)
  - `references/planning-protocol.md` — Gate-by-gate protocol: Business Understanding / Metric Define / Data Plan TH1 (schema-exists) vs TH2 (brainstorm + modeling) / Lock & Hand-off
  - `references/metric-framework.md` — 8 frameworks (NSM / OMTM / Growth Loop / HEART / Diagnostic / Counter-metric / AARRR / Unit Economics) + 10-step KPI design protocol
  - `references/governance.md` — 6-section practical framework (Metric & Definition / Modeling & Grain / Quality & Validation / Access & Privacy / Reporting & Consumption / Mindset) + STAR example + 5-implementation starter checklist
  - `references/orchestration-patterns.md` — 4 patterns (Airflow with TaskGroup + DagSensor + alerts / dbt + Cloud or GitHub Actions / Cron / GitHub Actions) + hybrid pattern + decision table
- **Sub-mode A0 (Brief tier)** in `/prof-DA:review`: 5-min snapshot — rubric_audit + outline check + 1-paragraph Ship / Fix / Rebuild verdict. Solves review overbloat (previously every review defaulted to A or B; A0 gives quick verdict for low-stakes / non-academic case).
- **Storytelling pattern** added to `mode-report.md` Step 5: storyline > dashboard; complete-sentence slide titles; conclusion-led headlines.
- **Orchestration pointer** added to `mode-automation.md` Schedule Layers: decision table + cross-ref to `orchestration-patterns.md`.
- **2 new commands:** `/prof-data-analyst:da-frame` + `/prof-data-analyst:da-model`.

### Changed
- Plugin description updated to "Professional Data Analyst + Analytics Engineer plugin — 9 routable modes"
- Mode router in `SKILL.md` updated: 7 → 9 modes (added Frame + Model); review mode now lists 4 tiers (A0 Brief / A Polish / B Full / C Stakeholder Q)
- Where to Read Next section organized: Core / Quality / Narrative / Methods / Front-of-workflow planning / Data engineering hooks / Sub-agent / Mode-specific

### Fixed
- `scripts/validators/method_maturity_audit.py` CLI error message: distinguished "path doesn't exist" vs "file passed instead of directory" with friendly hints.

### Architecture decisions
- **LEAN agents unchanged** (3 max): orchestrator + context-tracer + method-auditor. No new agents for new modes — modes are SKILLS, not agents.
- **Tier-based review** solves overbloat without removing capability — user picks detail level per task.
- **Frame + Model as 1 continuum** (planning → modeling), not 2 isolated modes.
- **References > separate files for thin topics**: storytelling stays inside `mode-report.md`; schema-doc stays inside `mode-model.md`; no fragmentation.

## [3.0.0] — 2026-05-14

First plugin-format release.

### Added
- Plugin manifest at `.claude-plugin/plugin.json` + marketplace entry at `.claude-plugin/marketplace.json`
- ROOT skill `prof-data-analyst` with 4 universal rules (Orientation / Baseline-Noise-Impact / 5W1H / Why-Explanation META) + 14 stdlib scripts
- 7 mode skills: `da-query` / `da-process` / `da-insight` / `da-automate` / `da-report` / `da-review` / `da-fix`
- 3 sub-agents: `da-orchestrator` (Sonnet, session-start + final-review gate) + `da-context-tracer` (Haiku, multi-file reads for Sub-mode B Phase 2) + `da-method-auditor` (Sonnet, Sub-mode B Pass 3 causal-method judgment)
- 8 slash commands: `/prof-data-analyst:da` + 7 mode-specific commands
- 5 new reference files: `subagent-prompt-discipline.md`, `quality-criteria.md` (5 Quality Criteria framework), `quality-pipeline.md` (5-Gate Quality Pipeline), `narrative-template.md` (SCQR + Key Terms + Impact Cards), `domain-discovery-protocol.md` (L1/L2/L3 hub generation)
- 14 method spec files under `references/methods/`: causal family (DiD, Event Study, RDD, Synthetic Control, PSM, IV) + validation family (Bootstrap CI, Robustness Checks, Sensitivity Analysis, Falsification Tests, Multiple Testing, Post-Hoc Power, Cross-Validation, Pre-Registration). Each follows canonical `_template.md` structure with primary source citations.
- `methods/_template.md` canonical W/H/W/W/W/W structure + `methods/_index.md` router
- LICENSE (MIT) + README + CHANGELOG

### Changed
- Refactored `causal-inference-toolkit.md` to decision table + 1-paragraph per method + pointer to `methods/<name>.md`
- Refactored `validation-evaluation-methods.md` to decision table + summary + pointer
- `/prof-DA:review` split into 3 sub-modes (Sub-mode A Delivery Refine, Sub-mode B Full Project Refine, Sub-mode C Stakeholder Questioning) with explicit option choice at invocation
- Added Outline / Story Flow Check to self-check-protocol Section A2 + mode-review Phase 3.5 + Sub-mode B Pass 6
- Added BQ Safety Protocol (5-gate) + Query Logic Card audit trail to `mode-query`
- Added 6-Step EDA Sequence + Source-pending discipline to `mode-process`
- Added Hypothesis 3 traps (n_T verification, multi-outcome DiD, wrong-sign reframe) to `mode-insight`
- Added Dual-Comparison Mandate + Chart Anatomy 7-element + Sentiment Color context override to `style-rules`
- Added Code Output ≠ Professional Deliverable rule to `coding-discipline`
- Added OLS anomaly window special case to `validation-evaluation-methods`
- Added HTML SPA structural inspection (Step 7.5) to `mode-report`
- Added Max 3 iteration ceiling + Fresh-session review discipline to `mode-review`

### Architecture decisions
- LEAN agent architecture (3 agents max). Workflow lives in SKILLS, not agents. Sub-agents spawned only when value > cost.
- Skills do the workflow; agents support specific gates (orchestration / context-tracing / method-auditing).
- Engine-agnostic SQL workflow (BQ / Postgres / Snowflake / Redshift / DuckDB).
- Progressive disclosure: SKILL.md lean; mode references load on demand; method specs load on demand.
