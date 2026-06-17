# Changelog

All notable changes to `prof-DA` plugin (formerly `prof-data-analyst` through v3.3).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [3.18.2] - 2026-06-17

### Changed
- **README.md** - renamed the second mode group from "Steward modes" to **"Governance modes"** (the binding-rules + review-discipline + workspace-systematization layer; it reads better and aligns with the workspace governance terminology). Label-only: the five modes (deliver / submit / review / fix / workspace) are unchanged.

## [3.18.1] - 2026-06-16

Count-consistency sweep. 3.17.0 (deliver mode) and 3.18.0 (review staleness sub-mode) added modes/scripts but left several docs at the old counts. No new functionality; documentation accuracy only (PATCH).

### Changed
- **docs/prof-da-architecture.svg** - 11 -> 12 modes (added `deliver` to the orthogonal list), 17 -> 19 stdlib scripts, "11 modes - 12 slash commands" -> "12 modes - 13 slash commands"; both version stamps v3.16.1 -> v3.18.1.
- **docs/GUIDE.md** - added the `deliver` mode (modes table + the sub-flows table), review 4 -> 5 tiers (added D Staleness Trace), and count fixes (11 -> 12 modes, 17 -> 19 scripts, 12 -> 13 commands) the feature commits missed.
- **skills/da/SKILL.md** - the frontmatter `description` said "11 modes" and OMITTED `deliver` from its trigger surface; fixed to 12 modes including deliver; the body "into 7 routable modes" -> 12.
- **README.md** - rewrote the two stale capability sections to convey the full layer, not a report-only framing. "The workspace second brain" now describes the consolidate + freshness + reconcile maintenance loop (a current, de-duplicated, per-task knowledge layer), not just a static memory. "The enforcement layer" + "What it enforces" now describe the rule-governed, PM-grade per-task contract (DoR / DoD / AC injected by depth, layered specs, a work-done/WIP disk cache, verify-don't-assume + anti-rationalization, an independent reconcile pass, 1-task-1-commit chunked delivery, and continuous staleness-trace) and correct "4 universal rules" -> "5 universal rules (4 quality + Detail-Level gate)". This is the cutting-edge discipline a blank-context agent lacks, previously under-described.
- **README.md** - reorganized "The 12 modes" into two labelled groups (Execution = the 6-phase analysis lifecycle ask/prepare/process/analyze/share/act mapped to frame/model/query/process/insight/report/automate; Steward = the cross-cutting deliver/submit/review/fix/workspace cluster for review, finalize, fix, and second-brain stewardship); previously a flat list. Added a "Where prof-DA fits the blueprint" section mapping prof-DA onto Anthropic's 4-tier self-serve stack: prof-DA = the Skills + Validation tiers (enabler / executioner); Data Foundations + Sources-of-Truth (semantic layer, ground truth, domain KB) are consumed-not-built today (a separate AE process), with a stated roadmap to close that loop end-to-end.

### Fixed
- **Invalid YAML frontmatter** (a `: ` colon-space inside an unquoted `description` makes strict YAML read it as a nested mapping and throw "mapping values are not allowed in this context"). Removed the offending colon-spaces from 6 files: `skills/review/SKILL.md` (audit: / asset:), `skills/deliver/SKILL.md` (automate:), `skills/query/SKILL.md` (SQL:), `skills/insight/SKILL.md` (workflow:), `commands/review.md` (sub-modes:), `commands/deliver.md` (discipline:). Verified by parsing all 26 skill + command frontmatter blocks with PyYAML (all valid). Some were pre-existing; the review/deliver ones were introduced this session.

### Why
The deliver mode + the review staleness sub-mode shipped, but the architecture SVG, the GUIDE walkthrough, and (most importantly) the da SKILL.md description trigger surface still advertised 11 modes / 17 scripts / 4 review tiers, and the description did not list `deliver` at all. A full count-consistency sweep across every file caught and fixed all of them. The same pass found GitHub-flagged YAML frontmatter errors (colon-space in descriptions) and fixed them, verified with a real YAML parser rather than a grep heuristic.

## [3.18.0] - 2026-06-16

Adds a **staleness-trace** sub-mode to /review (change-propagation after an edit) and a **recurring-report product blueprint** that makes frame propose the full end-to-end flow instead of routing to one siloed mode. Plus a reference-staleness audit fix.

### Added
- **`skills/da/references/mode-review.md` Sub-mode D (Staleness Trace)** + the entry-gate option + the "why five sub-modes" note. After a change to one asset, trace + sync every dependent (doc/plan/AC-DoD/output/sibling diagram): two entry paths (user names the changed path, or agent auto-detects from the action log via git status/log + mtimes), then build the dependent set (trace manifest if present, else grep by filename + concept), diff each (IN-SYNC/STALE), update (one dependent = one commit), independent re-read audit, drop a done-receipt.
- **`skills/da/references/recurring-report-blueprint.md`** - the cross-mode end-to-end recipe for a recurring automated report product (ideation -> metric -> model -> design -> predict -> deliverables+channels -> schedule -> validate -> learn), mapped to modes + concrete outputs, with a worked savings-product daily-report example + how-to-prompt. frame PROPOSES this whole chain (one batch approval) then executes phases under /deliver, so the modes stop feeling siloed.

### Changed
- **/review is now 5 sub-modes** (was inconsistently documented as 3): reconciled the count across `skills/review/SKILL.md` (+ added the missing A0 + new D entries), `commands/review.md`, `commands/da.md`, `skills/da/SKILL.md` (4 tiers -> 5 tiers). mode-review.md heading + table + gate updated.
- **`skills/da/references/mode-frame.md`** - new "End-to-end recurring-report product" section: on a full-product request, load the blueprint and propose the chain rather than picking one Next Mode; cross-refs added.
- **`skills/da/references/delivery-lifecycle.md`** + **`skills/da/SKILL.md` (frame router + Where-to-Read)** - wire the blueprint trigger.
- **`skills/da/references/mode-fix-pipeline.md`** - removed a dangling `See <memory-atom>.md` pointer in the bug catalog (the named atom has no standalone file; the bug+fix is self-described inline). From a reference-staleness audit: prof-DA was found essentially IN-SYNC with the current reference-project state (anonymized pattern-level distillation, no baked versions), this dead pointer was the one real prof-DA defect.
- **version** 3.17.0 -> 3.18.0 (`plugin.json` + `marketplace.json` + README).

### Why
Two gaps surfaced in use: (1) after editing one asset, dependent assets (doc/plan/AC-DoD/output) drift silently with no built-in way to re-sync them, and (2) the modes felt siloed for a "build the whole recurring report product" request, with no single place that proposes the end-to-end flow. Sub-mode D gives /review a change-propagation axis; the blueprint gives frame an end-to-end product chain to propose. Both reuse the existing engine (evidence-based-done receipt, the /deliver gated loop, the lifecycle map).

## [3.17.0] - 2026-06-16

New **`deliver` mode** (the 12th mode) plus the Lean Spec Delivery lifecycle map and a senior-engineer execution-discipline layer, distilled from the Lean Spec Delivery post + addyosmani/agent-skills. Additive: the build half (process/report/model/automate) is unchanged; `deliver` wraps any of them with execution gates, and the new references give the plugin its own self-contained copy of the honesty/verification discipline.

### Added
- **`skills/deliver/SKILL.md` + `commands/deliver.md`** - the `deliver` mode + `/prof-DA:deliver`. The build-auto execution loop: require a spec/charter or STOP, clean baseline, single batch approval, then per-task RED -> GREEN -> build -> commit with a verify gate, stop-on-failure/risk/irreversible, and an honest evidence summary. Orthogonal to the build modes (it is the HOW, not the WHAT). Drops `<project>/.prof-da/pending-validation.json` so the existing Stop hook validates it with zero hook changes.
- **`references/build-auto.md`** - the 7-gate loop + the DA irreversibility stop-list (prod write, billed backfill > 1 month, auto-send, schema cutover, force-push).
- **`references/execution-discipline.md`** - the anti-rationalization table (the excuses that skip a hard step + the disciplined move), core operating behaviors, verify-don't-assume, scope discipline. Self-contained (no external pointers).
- **`references/evidence-based-done.md`** - the proof gate: the evidence ladder (seems-right banned -> validator-exit-0 -> corrected-real-number), Presence-proof, the built-but-unrun trap, DA evidence types.
- **`references/delivery-lifecycle.md`** - the 7-phase Lean Spec Delivery lifecycle (DISCOVER -> MODEL -> SPECIFY -> REVIEW -> DELIVER -> VALIDATE -> LEARN) mapped to the prof-DA modes + the gate each produces.
- **`scripts/validators/artifact_presence_check.py`** - the evidence-based-done presence gate (exists + non-empty + non-stub + code proof marker); reads a receipt or `--deliverables`; exit 0/1/2; pure stdlib.
- **`scripts/validators/anti_rationalization_check.py`** - a plan/task-list gate: flags a task with no verify line, an irreversible action without a STOP marker, or a red-flag phrase; exit 0/1/2; pure stdlib.

### Changed
- **Wiring:** `skills/da/SKILL.md` (deliver registered in the mode router + a new "Delivery lifecycle + execution discipline" block in Where-to-Read-Next), `commands/da.md` (deliver under orthogonal helpers; 11 -> 12 modes), `skills/da/references/scripts-guide.md` (the 2 new validator usage blocks).
- **README** - 11 -> 12 modes everywhere (headline, modes table + deliver row, "What is inside" tree, script count 17 -> 19, command count 12 -> 13).
- **version** 3.16.1 -> 3.17.0 (`plugin.json` + `marketplace.json` + README).

### Why
prof-DA had the build modes and the per-section / report gates, but not a single execution-control loop that makes an autonomous multi-step build safe (commit-per-task + verify-per-task + stop-on-risk) nor a first-class anti-rationalization + evidence-ladder layer to stop a hard step being skipped. `deliver` + the four references add exactly that, distilled from the Lean Spec Delivery 7-phase spine and addyosmani/agent-skills. Ported in-plugin (self-contained) so the plugin does not depend on the author's private workspace.

## [3.16.1] - 2026-06-16

### Changed
- **commands/workspace.md + skills/da/references/mode-workspace.md** - wired the workspace governance layer into the /workspace mode: per-task DoR/DoD/AC scaffold (plus Epic-Feature-Stories + RAID at Deep) scaled to the Quick/Standard/Deep detail level, self-chunk then delegate then coordinate under the depth-1 delegation walls, and the deliverable-language guards. Points to lt-memory/rules/governance-injection.md + task-chunking-orchestration.md.
- **skills/da/references/universal-workflow-rules.md + skills/da/SKILL.md** - reconciled the universal-rule count (4 quality rules + Rule 5 Detail-Level Gate = 5) and noted that Quick/Standard/Deep depth now also drives the governance scaffold injection.
- **commands/da.md** - fixed the routable-mode count (10 to 11) to match the actual mode list.
- **docs/prof-da-architecture.svg** - fixed the stale version stamp (v3.13.0 to v3.16.1) and added a "Governance enforcement (hooks)" annotation.
- **README + plugin.json + marketplace.json** - version + universal-rule-count consistency.

## [3.16.0] - 2026-06-15

### Added
- **`skills/da/references/report-flow.md`** — Solve-by-cluster detail-body flow for deep-dive / solution-after-problem reports. The opener (Exec Summary + SCQA + Overview) is unchanged; the detail body becomes a sequence of self-contained insight clusters, each a "raise -> prove -> solve" unit: Insight -> Data (in %, common scale) -> noise-vs-signal gate -> multi-layer cross-filter drill-down (Layer 1 overall, Layer 2 filter the extreme group cut by a suspected factor, confirm the link; caution that SUM can hide Layer 1) -> hypothesis -> conclusion (name the subject if it is a paradox) -> suggestion (number + target group + that group's traits + why) -> expected result (lift X% to reach YYY). Two assembly directions (bottom-up cluster-first, top-down suggestion-first tracing each suggestion back to shared evidence). Lead with the ONE significant insight as headline. Composes existing refs (narrative-template, universal-workflow-rules, mode-insight, storytelling-with-data) without duplicating.

### Changed
- **`skills/report/SKILL.md`** + **`skills/insight/SKILL.md`**: cross-reference `report-flow.md`; report Step 5 notes that deep-dive / solution reports structure the body as solve-by-cluster.

## [3.15.0] - 2026-06-11

### Added
- **`templates/proposal-walkthrough/`** (HTML + spec MD + README): reusable proposal / PoC-walkthrough template for a stakeholder proposal that goes general -> detail: Epic / Feature / Connextra user-story, per-step Acceptance-Criteria + Definition-of-Done, RAID, a 2-layer output (the UI deliverable AND the infra scaffold beneath, idempotent), and a linking-key-highlight discipline (color each cross-step key so the reader sees how info connects between tools/steps). Distilled from the looker-extract walkthrough. Fork `PROPOSAL-TEMPLATE.html`, fill the `[ ... ]` slots. Author: Loc Tu.

## [3.14.0] - 2026-06-11

Auto-trigger overhaul: prof-DA now fires on natural prompts the way superpowers does, with three stacked layers instead of frontmatter descriptions alone. Driven by a real miss: "có sẵn template thực hiện các bài toán dự đoán dựa vào seasonal effect không" produced a generic workspace search instead of routing into the plugin.

### Added
- **`hooks/session_start_dispatch.py` (SessionStart):** injects a standing dispatch protocol into every session: the 1%-rule (any DA-shaped request -> invoke `prof-DA:da` BEFORE responding), an 11-mode map with natural VN + EN phrases, and a rationalization red-flag list ("just a quick question" / "I'll search the workspace first"). Same mechanism superpowers uses; keeps working even when a crowded skill list drops frontmatter descriptions.
- **`hooks/da_intent_detector.py` (UserPromptSubmit):** deterministic keyword floor under the probabilistic description matching: folds the prompt to diacritic-free lowercase ("dự đoán" == "du doan"), scans ~150 mode-grouped signals with left-word-boundary matching, and injects a `[prof-DA dispatch]` nudge naming the matched keywords + likely mode. Silent on slash commands, prof-DA meta-talk, and non-DA prompts; fail-open, never blocks.

### Changed
- **Trigger vocabulary gap closed (the root cause of the miss):** no skill description contained the prediction family (forecast / dự đoán / dự báo / seasonal / time series / SARIMA / Prophet / churn prediction / scoring / segmentation / clustering / regression / A/B test); it lived only in references, invisible to the trigger surface. Added to `da` (master) + `process` (now the declared home of predictive modeling -> ml_/pred_ layers) + `insight` (seasonality diagnosis). `model`'s description + the mode-router table now disambiguate explicitly (schema design only; forecast / ML prediction asks route to process), so the router stops improvising "model mode includes forecasting templates".
- **`da` description:** also catches capability questions ("có sẵn template/framework/notebook cho bài toán X không", "cách tiếp cận bài toán X") and says 11 modes (was stale at 10).
- **Hook stdin decode hardened:** `da_intent_detector.py` + `correction_detector.py` read stdin as bytes + explicit UTF-8 decode; on Windows, Python otherwise decodes hook stdin per locale (cp1252) and Vietnamese prompts arrive as mojibake, silently missing every diacritic signal.
- **version** 3.13.0 -> 3.14.0 (`plugin.json` + `marketplace.json` + README).

### Why
Keyword auto-fire was the weakest link: users who don't know `/prof-DA:da` exists got vanilla behavior on clearly DA-shaped Vietnamese prompts. Descriptions are necessary but not sufficient, because the host can drop them from a crowded skill list and the agent can rationalize past them. The superpowers lesson is that reliable triggering needs a standing per-session protocol plus a deterministic per-prompt catch; v3.14 ships both, with the trigger vocabulary fixed underneath.

## [3.13.0] - 2026-06-11

New **`submit` mode** (the 11th mode): a final acceptance gate that checks a finished recurring report against a team's external acceptance contract (required sections + per-section definition-of-done), routes gaps to the builder, runs the per-section quality_check, and emits a ready-to-paste submission payload. Distilled from the <organization> <product> bi-weekly `<report-mcp>` MCP (versioned guidance + per-section quality_check + carry-forward follow-ups), ported offline so the plugin stays engine-agnostic and server-independent.

### Added
- **`skills/submit/SKILL.md` + `commands/submit.md`** — the submit mode + `/prof-DA:submit` slash command. Orchestrates, never generates: a missing section is routed to `/report` or `/query` and re-audited; submit never drafts content and never calls the submission MCP (the user submits after connecting). Distinct from `/review` (which judges quality); submit judges COMPLETENESS, ACCEPTABILITY, and submit-readiness.
- **`references/mode-submit.md`** — the Step 0-6 gate workflow (identify team + load contract, structure audit, gap punch-list + route, quality_check, carry-forward, build payload, readiness checklist), the `/review`-vs-`/submit` distinction, and the thin per-team profile model.
- **`references/recurring-report-contract.md`** — the methodology: section contract + per-section DoD + carry-forward follow-ups, the `report-contract.json` format, engine-agnostic.
- **`scripts/validators/section_contract_audit.py`** — per-section DoD gate (vs `rubric_audit.py`'s GLOBAL rules): every required section present, non-empty, no unrendered placeholder, each DoD item heuristically evident. Three modes: audit (JSON, exit 0/1/2), `--worksheet` (per-section quality_check), `--payload --author` (a `submit_contribution`-shaped JSON). Pure stdlib, BOM-tolerant (`utf-8-sig`).
- **`references/submit-profiles/example-team.report-contract.json`** — the concrete <product> bi-weekly acceptance contract (7 sections, guidance v3: business_overview / satisfaction / cross_sell / segment_a_contribution / segment_b_contribution / segment_c_contribution / new_initiatives), section keys 1:1 with the <report-mcp> `submit_contribution` guidance.

### Added (docs)
- **`docs/prof-da-architecture.svg`** — one-page architecture poster (6 nested loops by time scale: intent gate / grounding / mode run / gate stack / cycle contract / learning loop, plus the compound chain, real numbers, and a vs-vanilla panel), embedded at the top of the README. Poster idiom follows the Hermes Agent (NousResearch) architecture diagram.

### Changed
- **Wiring (30 insertions):** `skills/da/SKILL.md` (submit registered in the mode table), `commands/da.md` (submit under orthogonal helpers), `planning-protocol.md` (Gate 2.4: lock a Section Contract beside the Metric Contract for recurring reports), `report-standard-checklist.md` (optional section-contract gate), `scripts-guide.md` (`section_contract_audit.py` usage), `skills/report/SKILL.md` (cross-reference to the recurring-report contract).
- **`references/mode-report.md`** — fork-or-fail now points at the workspace design-token contract (`shared/templates/_contract/THEME-TOKEN-CONTRACT.html`) as the token source when present, instead of re-deriving hexes per report.
- **README** — 10 -> 11 modes everywhere (headline, modes table + submit row, lifecycle line, "What is inside" tree, script count 16 -> 17); a recurring-report paragraph added to "What it enforces".
- **version** 3.12.0 -> 3.13.0 (`plugin.json` + `marketplace.json` + README).

### Why
Recurring team reports (the <product> bi-weekly business review) are graded against a manager's fixed section template with a per-section definition-of-done — a contract the global validators (`rubric_audit`, `self_check`) do not check, because they grade the report's universal shape, not each section against its own bespoke rubric. Without a per-section gate, recurring reports drift section content silently and get bounced at submission. `submit` is the gate that catches it and hands over a paste-ready payload, so a self-serve report finalizes to the team's standard on the first try. The pattern is ported offline (not a live dependency on the `<report-mcp>` worker, which the <organization> web-filter blocks at the system layer) so the plugin stays portable; <product> is just the first profile.

## [3.12.0] - 2026-06-07

Merge of two parallel development lines that had each independently reused versions 3.10.0 and 3.11.0. Brings the **refine-protocol** feature onto `main` alongside the **A12 slide-deck / PPTX** channel. The refine line (worksheet MVP + Tier 3 inline annotation) was developed off-main and force-removed from `main` before the A12 release; it had self-numbered 3.10.0 / 3.11.0 on its own branch. Those parallel numbers are folded into this entry; the 3.11.0 (A12) and 3.10.0 (second-brain) entries below are the `main` line.

### Added (refine-protocol, merged in)
- **`references/refine-worksheet.md`** — 3-tier feedback protocol (prompt / worksheet / inline annotation), anchor system, apply flow, fresh-session handoff.
- **`scripts/refine/generate_worksheet.py`** — report HTML to a non-technical per-section worksheet (stdlib only).
- **`scripts/refine/parse_feedback.py`** — filled worksheet to a JSON change-set.
- **`scripts/refine/parse_comments.py`** — `comments.json` to the same change-set shape (so the apply step consumes both).
- **`scripts/refine/annotate_overlay.js`** — self-contained browser select-and-comment widget; exports `comments.json`.
- **`scripts/refine/wrap_annotation_harness.py`** — injects the overlay into a report copy (`<report>.annotate.html`); the shipped report is untouched.
- **`scripts/refine/tests/`** — unit tests for the worksheet / feedback / comments / harness scripts.

### Changed (refine-protocol wiring)
- `mode-report.md` (Step 8b refine loop), `mode-review.md`, `mode-fix-pipeline.md`, `universal-workflow-rules.md` (trigger rule), `skills/da/SKILL.md` (refine scripts registered in the Bundled Scripts tree). No new mode.
- **version** 3.11.0 -> 3.12.0 (`plugin.json` + `marketplace.json` + README).

### Why
Two devices advanced prof-DA in parallel and both bumped to 3.10.0 then 3.11.0 with different features; `main` ended up carrying only the A12 line. Rather than lose the refine-protocol work (a full feature with tests), this release merges it onto `main` and resolves the numbering collision at 3.12.0.

## [3.11.0] - 2026-06-07

Slide-deck / editable-PPTX output channel: `report` mode can now project any analysis into a presented deck or an editable PPTX handoff, with the deck-authoring contract that survives the export.

### Added
- **`references/output-slide-deck.md`** — portable deck-authoring + editable-PPTX contract: one-message-per-slide / action titles, the 24px legibility floor, real `<table>` for native tabular export, capture-safe CSS, static-HTML-slide-bodies, no-AI-tell glyphs, entrance-end-state-is-base. Plus the report-archetype to deck-shape projection map and the **two export paths**: `gen_pptx` editable mode (claude.ai / Claude cowork) and the `pptx` skill's `html2pptx.js` (Claude Code CLI — a different per-slide contract). Tool-specific export params stay in the house template's DESIGN-SPEC, not in this portable file.

### Changed
- **`references/mode-report.md`** — decision tree gains a "Presentation deck / editable PPTX" branch; Step 1 (format) + Step 5 (storyline) + Reading-Order-Recap point at `output-slide-deck.md`; the storyline section now splits slide CONTENT (there) from deck FORM + export (the new reference).
- **`skills/report/SKILL.md`** — cross-reference + hard-rule for the deck / PPTX path; auto-fire triggers add `pptx` / `convert sang PPTX` / `editable deck` / `Google Slides`.
- **`references/coding-discipline.md`** — the stakeholder-file "use the template builder" rule now points at `output-slide-deck.md` for the HTML-deck case.
- **`references/suggestion-protocol.md`** — the format-expansion (convert-to-PPTX) suggestion cites the deck reference.
- **`references/org-extensions.md`** — new §8 "Slide-deck / PPTX house template (A12)": the concrete `shared/templates/A12-slide-deck-pptx/` template, the Trầm / magenta / IBM Plex house skin, the swimlane / RACI / mapping hero components, the MOAT reference deck, and the cowork-only `gen_pptx` note.
- **version** 3.10.0 -> 3.11.0 (`plugin.json` + `marketplace.json` + README); CHANGELOG backfilled for 3.10.0 (below).

### Why
The library renders scrolling HTML reports; nothing guaranteed a deck that reads at the back of a room AND survives an editable-PPTX export with native text boxes + tables. A12 (designed in the report-template library, now locked into `shared/templates/`) is that output channel. This release teaches `report` mode to author A12-compliant decks and routes the export correctly: `gen_pptx` exists only in cowork, while in CC-CLI the path is the `pptx` skill — wiring the two as if interchangeable was the latent foot-gun this documents away.

## [3.10.0] - 2026-06-04

Second-brain context consumption: every mode now reads the host workspace's memory + index on entry to ground in the user's real domains and data. (Reconstructed entry — v3.10.0 shipped a `plugin.json` version bump without a CHANGELOG record; sourced from commit `1f96dc4`.)

### Added
- **"Second-Brain Context" core principle in `skills/da/SKILL.md`** — if the workspace has a `memory/` or `lt-memory/` layer plus a `.index/`, modes READ `.index/_root.md` + the relevant memory hub FIRST, before running; if absent and the task would benefit, suggest the standalone `workspace-brain` skill once. Division of labor: **workspace-brain builds + seeds the brain; prof-DA consumes it.**

### Changed
- **`commands/workspace.md` + `skills/workspace/SKILL.md`** — prefer the standalone `workspace-brain` skill when installed (canonical infra: hook-install + first-use discovery); the embedded workspace mode is the portable fallback subset.
- **`references/suggestion-protocol.md`** — second-brain grounding added as a valid cross-cutting mode-exit suggestion.
- **version** 3.9.0 -> 3.10.0 (`plugin.json` only at the time; `marketplace.json` + README were not bumped, reconciled to 3.11.0 in this release).

## [3.9.0] - 2026-06-03

Workspace mode — progressive-disclosure indexing: `/prof-DA:workspace` now teaches recursive, per-folder indexing (a deep knowledge folder earns its own local `_index.md`) and ships the index format it referenced.

### Added
- **`references/index-format.md`** — the workspace index spec the mode pointed at but never shipped (the reference was dangling). Covers the 4-file root `.index/` format, the progressive-disclosure contract (index ≤200 lines / atoms ≤300 / cross-link never re-paste / read index → link → targeted range), the **recursive per-folder index rule**, build/update/rebuild, and the reverse-existence check.
- **`mode-workspace.md` — run-safe gotchas block:** author batch moves/index in code not a shell loop (CRLF corrupts shell loops on Windows); a sandboxed `git push/fetch` can falsely report `Host key verification failed`; an orphaned `160000` gitlink (not in `.gitmodules`) with uncommitted content must be pushed before untracking.

### Changed
- **`mode-workspace.md` Step 5** — expanded from a one-line "build `.index/`" into progressive disclosure + the recursive per-folder index rule (a knowledge collection read on its own terms earns a local `_index.md`; pure containers do not). Marked the mode self-contained; attributed the pattern to the BookRAG concept.
- **`skills/workspace/SKILL.md`** — Step-5 row + a progressive-disclosure hard rule + index-format cross-reference.
- **`README.md`** — opening summary corrected 9 -> 10 modes (`workspace` was missing from the headline list).
- **version** 3.8.0 -> 3.9.0.

### Why
The mode could organize a workspace and build one top-level index, but its headline claim — navigable by lookup, not guessing — breaks once any sub-tree grows into a knowledge collection: a flat root index either omits the leaves or blows its line budget. Recursive per-folder indexing keeps lookup cheap at any depth, and it was the one piece the mode described but never shipped (the `index-format.md` reference 404'd).

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
