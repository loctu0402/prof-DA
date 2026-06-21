# Mode — Review / Refine

Invoke when user asks: "review report", "refine deliverable", "audit project", "kiểm tra bài", "check against skill rules", "stakeholder questions", "brainstorm stakeholder", "/prof-DA:review".

## Six Sub-Modes (tier-based; user picks detail level)

User picks ONE at invocation. The flow is different for each. Tier choice solves the "overbloat" concern: many reviews just need a snapshot, not a full audit.

| Sub-mode | Scope | When to pick | Effort |
|----------|-------|--------------|--------|
| **A0 — Brief (Snapshot)** | 5-min snapshot verdict: rubric_audit + outline check + 1-paragraph Ship/Fix/Rebuild verdict | User chỉ cần elevator-pitch verdict; "OK chưa?" / "có ship được không?"; non-academic stakeholder context | Snapshot (~5 min, 1 file) |
| **A — Delivery Refine** | Single deliverable: presentation, wording, format, charts, layout, checklist | Report đã có đủ thông tin / approach OK; cần polish + verify checklist | Lightweight (~15-30 min, 1 file) |
| **B — Full Project Refine** | Whole project: workflow + cache + logic + approach + method + advanced/academic + fact-check + code-check | Cần audit tổng thể; muốn biết approach có đủ rigor, method có advance được không, miss gì không | Heavyweight (~1-3 hours, multi-file context tracing) |
| **C — Stakeholder Questioning** | Question set for an upcoming meeting / requirements gathering | Chuẩn bị họp stakeholder; cần formulate đúng câu hỏi BEFORE analyse | Lightweight (~10-15 min) |
| **D — Staleness Trace** | After a change to one asset, trace + sync every dependent asset (doc, plan, AC/DoD, output, sibling diagram) so the project stays consistent | User just edited/changed something (a direction, an input, a result, a diagram flow) and wants all related assets brought in sync | Lightweight-to-medium (scales with dependent count) |
| **E — Lifecycle Compliance** | Scan a whole project for evidence of all 7 delivery-lifecycle phases (DISCOVER..LEARN): a PRESENT/PARTIAL/MISSING scorecard + gap worklist + Ship/Fix/Rebuild verdict | User wants "did this project follow the full lifecycle / what is missing"; a process-maturity or onboarding audit (process-completeness axis, not quality) | Lightweight (~10 min, `lifecycle_audit.py` + a read) |

### Why five sub-modes (not one "review")

- **A0 vs A vs B is a detail-level continuum:** A0 = "is this shippable, yes/no?" / A = "polish this before ship" / B = "audit the rigor of the whole project". User picks based on stake + time available.
- **A0 solves overbloat:** previously every review defaulted to A or B; A B over-engineered the simple "is this OK" question. A0 gives a 5-min verdict for non-academic / low-stakes cases.
- **C is a different artifact entirely** (a question set, not a deliverable review) but lives in the same mode because it shares the stakeholder-empathy lens.
- **D is change-propagation, not quality** (A0/A/B judge ONE artifact's quality; D checks CONSISTENCY across many after a change). It lives here because it is still a "is the project in good shape" review, just along the sync axis instead of the quality axis.

### Command invocation

When user runs `/prof-DA:review` without arguments, agent MUST ask which sub-mode + which target:

```
Bạn muốn review theo tier nào? (A0 / A / B / C / D / E)
  A0 : Brief (Snapshot), 5-min Ship/Fix/Rebuild verdict (rubric + outline)
  A  : Delivery Refine, polish 1 deliverable (presentation, wording, format, checklist)
  B  : Full Project Refine, audit toàn bộ project (workflow, method, fact-check, code-check)
  C  : Stakeholder Questioning, chuẩn bị câu hỏi cho stakeholder meeting
  D  : Staleness Trace, vừa sửa xong 1 thứ thì sync mọi asset liên quan (doc, plan, AC/DoD, output)
  E  : Lifecycle Compliance, scan project xem đủ 7 phase chưa, ra scorecard PRESENT/PARTIAL/MISSING + gap worklist + verdict Ship/Fix/Rebuild

Target nào? (file path / project folder / mô tả ngắn, tôi sẽ tìm)
```

If user gives only sub-mode, ask for target. If user gives only target, infer sub-mode from target type + stake:
- Single file + "quick check" / "OK chưa": A0
- Single file + wants polish: A
- Folder / multiple files: B
- User vừa thay đổi 1 thứ / cho path mới sửa / "sửa xong sync giúp": D
Confirm before proceeding.

If target not locatable from description → glob/grep candidates, list 3 closest matches, ask which one.

## Sub-mode A0 — Brief (Snapshot, 5 min)

### Goal
Give user a fast Ship/Fix/Rebuild verdict on a single deliverable. NO multi-pass audit. NO comprehensive critique. Just: does this clear the bar?

### When this is enough (not overkill)
- User says "OK chưa?", "có ship được không?", "snapshot xem có lỗi gì lớn không"
- Stakeholder context is non-academic (manager / business / non-technical)
- Time budget: 5 min; output: 1-paragraph verdict + top-3 issues if any

### Phase 1 — Mechanical audit only
```bash
python scripts/validators/self_check.py <deliverable-path>   # .html/.md: includes the consistency gate
python scripts/validators/rubric_audit.py <deliverable-path>
```
Read TSV + JSON. Count BLOCKER + HIGH, plus any consistency `[GATE]` fail (scaffold / portal / AI-tell / diacritics / empty-as-finding). That's the data point.

### Phase 2 — Outline / Story Flow Check (60 sec)
- Extract all headings + section opening lines from the deliverable
- Read standalone (without body content): does the outline tell a coherent story?
- If outline alone is followable → PASS. If not → flag as the #1 issue.

### Phase 3 — One-paragraph verdict

Format:
```
**Verdict: <Ship / Fix-Then-Ship / Rebuild>**

<2-3 sentences explaining why>

Top issues (if any):
1. <severity>: <issue> — <file:line>
2. <severity>: <issue> — <file:line>
3. <severity>: <issue> — <file:line>

Significance check (if numerical claim present):
"<claim>" — significant @ α=0.05? <yes/no>, plain-language reading: "<1 sentence non-academic explanation>"
```

### Verdict decision rule
- **Ship**: 0 BLOCKER + ≤2 HIGH + outline check PASS
- **Fix-Then-Ship**: 0 BLOCKER + 3-5 HIGH OR outline check borderline → list top fixes; estimate <30 min
- **Rebuild**: ≥1 BLOCKER OR outline check FAIL OR fundamental approach issue → recommend Sub-mode A or B instead

### Advanced-method confirmation (when applicable)
If the deliverable uses an advanced method (DiD / bootstrap / significance test / etc.), A0 confirms ONE thing only:
- Method is named + the threshold cited (e.g., "p < 0.05 → reject H0")
- Plain-language reading present for non-academic stakeholder (e.g., "với CI [12.3, 18.7] 95%, chúng ta tin true value nằm trong đó với độ tin cậy 95%" NOT raw "CI [12.3, 18.7], p=0.03")

If method named without plain-language reading → flag as HIGH.

### What A0 explicitly does NOT do
- NOT deep critique (skip to A)
- NOT method-vs-claim audit (skip to B Pass 3)
- NOT fact-check against domain data (skip to B Pass 2)
- NOT code review (skip to B Pass 5)
- NOT rework plan (skip to A or B)

A0 ships in 5 min or escalates to a higher tier. No middle ground.

## Sub-mode A — Delivery Refine (lightweight, single deliverable)

### Goal
Polish 1 deliverable (report / dashboard / notebook / SQL file) for shipping. Combines mechanical rule-compliance + judgment-critique on the surface. Does NOT trace back to method choice / data pipeline / domain accuracy — that's Sub-mode B.

### When this is enough (not overkill)
- The report is already drafted and the approach/method is settled
- User wants confidence that delivery is rule-compliant + polished
- Time budget: 15-30 minutes; output: gap table + suggested fixes

### Phase 1 — Read the artifact end to end
- Don't skim. Read every line.
- Note implicit assumptions the author made
- Spot AI-tell symbols, missing baselines, bare metrics, layout inconsistency

### Phase 2 — Run the mechanical audit
```bash
python scripts/validators/self_check.py <deliverable-path>               # orientation + ai-tell + action-brief + consistency gate
python scripts/validators/rubric_audit.py <deliverable-path>             # ~30 Rules 1-4 + style + code checks
python scripts/validators/report_consistency_audit.py <deliverable-path> # scaffold / portal / palette / diacritics / empty-as-finding
```

Bundles ~30 checks (Rules 1-4 + style + code + output-path) plus the consistency hard-gate. Output: TSV/JSON gap table with `rule_id | severity | location | what_missing | how_to_fix | why_it_matters`. Then SCORE the result against `references/evaluation-rubric.md` — the 7-category weighted C-level grade + must-fix gate is the standard scorecard every review session must produce (so verdicts are comparable across sessions).

Severity assignment:

| Severity | Definition | Examples |
|----------|------------|----------|
| BLOCKER | Cannot ship | Missing Orientation, bare metric without baseline, fabricated credential, auto-email enabled |
| HIGH | Ship with caveat, fix next cycle | Missing per-chart takeaway, missing denominator, missing Why on a method choice |
| MEDIUM | Polish | AI-tell in margin text, number format inconsistent, comment over-noted |
| LOW | Nice-to-fix | Diacritic missing on one term, unit space inconsistency |

Why severity matters — without it the gap table is "all equally bad" and the user fixes easy ones first instead of dangerous ones.

### Phase 3 — Human pass (semantic checks the script cannot do)
Read the deliverable critically, focus on:

For numbers (Rule 2 ladder):
- Does every headline have a baseline?
- Is the noise check appropriate (Pearson vs Event Study vs effect size)?
- Is the business-impact verdict quantified?
- Cross-card numerical consistency — back-derive each headline

For reasoning:
- Every finding a 5-stage chain (Fact → Mechanism → Behavior → Impact → Evidence)?
- Any label-glue masquerading as causation?
- Any obvious-by-definition statements?
- Counter-arguments / recovery signals for negative findings?

For style + delivery polish:
- AI-tell symbols in stakeholder text?
- Vietnamese diacritics correct if stakeholder-facing?
- Per-chart inline `→ takeaway` verdict?
- "Reading in business terms" column on number tables?
- Mermaid (BAN — use ASCII)?
- Chart theme consistent? Brand colors correct?
- Layout: tab order, reading flow, "How to read" intro present?

For code (if deliverable includes code):
- Karpathy 4 principles (think-before / simplicity / surgical / goal-driven)?
- Comments only where WHY is non-obvious?
- Edit vs Write discipline (no full-file rewrite for small change)?
- Emoji-free?

### Phase 4 — Deliver the refine

Format:
1. **Headline verdict** — ship / fix-then-ship / rebuild
2. **BLOCKER list** — must-fix before ship, with concrete fix
3. **HIGH list** — fix next cycle
4. **MEDIUM / LOW** — polish bucket
5. **Per gap row**: `[severity] rule_id | location | what_missing | fix suggestion | why it matters`

End with one-line verdict. If patch-ceiling triggers (≥3 distinct bugs in same artifact across patches) → flag "consider rebuild" rather than another patch round.

### Phase 3.5 — Outline / Story Flow Check (mandatory at review)

Before moving to Phase 4 (Deliver the refine), run the Outline / Story Flow Check per `self-check-protocol.md` Section A2:
1. Extract all headings / sub-headings / 1-line section summaries
2. Read outline standalone (no body)
3. Verify big-picture / logic-flow / step-traceability
4. If any fails → add structural finding (heading rename / section reorder / missing bridge section) to gap table, NOT body-patching

Why this is its own phase — Phase 2's mechanical audit + Phase 3's human pass both miss outline-level issues. The outline check interrogates heading skeleton, not body content. Documented case: outline check caught a misplaced milestone section that body-level audit had passed (heading order broke the narrative even though every section was individually fine).

### Phase 5 — User approval + apply fixes
After deliver, ask user: "Approve fixes? Or revise?"
- Approve → switch to mode-fix-pipeline (if code) or mode-report (if narrative) and execute the fix list
- Revise → user adjusts list, agent re-confirms

### Iteration ceiling (max 3 review rounds)

If the same deliverable comes back through Sub-mode A for a 4th review cycle, STOP iterating in-place. Surface to user with options: (a) rebuild the section under contention, (b) handoff to a different reviewer / tool, (c) accept current state with documented limitations. Per `feedback_patch_ceiling_escalate_rebuild.md` — patch-cycle thrash signals design vs polish problem, no number of additional reviews fixes it.

## Sub-mode B — Full Project Refine (heavyweight, multi-file audit)

### Goal
Deep audit of a whole project: workflow integrity + cache discipline + business logic + approach maturity + method appropriateness + advanced-method opportunities + academic/scientific rigor + domain accuracy + fact-check + code-check. Multi-pass review. Returns a structured rework plan, awaits user approval, executes.

> When the audited target IS an agent package (a skill / workflow / plugin / hook / generator), also run the package security scan: `python scripts/validators/skill_security_scan.py <package> --fail-on critical`. A CRITICAL verdict (prompt-injection, embedded secret, pipe-to-shell, eval/exec) is a BLOCKER. Detail: `references/skill-workflow-security.md`.

> The audit IS a doubt pass at project scale (`execution-discipline.md` section 6): run it bias-to-disprove, not bias-to-confirm. For each headline claim and method choice, actively try to BREAK it (confound, stale source, miscount, cherry-picked window, wrong grain); a pass that finds nothing on a complex project is itself a red flag (no doubt theater). The context-tracer + method-auditor sub-agents are the fresh-context skeptics that make the doubt real.

### When to pick this (not A)
- User unsure if approach itself is right, or if method choice is appropriate to the question
- User wants to know "can this be more advanced / more rigorous?"
- Project crosses multiple files (SQL + notebook + py scripts + HTML + cache + brief)
- Domain accuracy or fact-check is in scope (numbers cited from external sources, bank rates, market data)

### Phase 1 — Target disambiguation
Agent confirms project boundary:
- Path to project root (e.g., `output/projects/<case>/` or `projects/<case>/`)
- Headline artifact (HTML / report / notebook)
- Backing data sources (CSV / SQL queries / raw exports)
- Method source files (notebook cells / py scripts)
- Related brief / PRD / hypothesis matrix

If user gives only headline file → agent traces upward: `git log <file>`, sibling files in same folder, imports in code → propose project tree → confirm with user before proceeding.

### Phase 2 — Context-tracing read
Agent reads (or at least globs + heads) all project files in this order:
1. Brief / PRD / hypothesis matrix (if present) — what was the question?
2. Data source files — what data backs the analysis?
3. Method source — what was the approach (DiD / regression / EDA / etc.)?
4. Cache / output — what was actually produced?
5. Headline artifact — the deliverable itself

Output: a 1-page **Project Understanding Summary** stating:
- Question being answered
- Data scope + freshness
- Method actually used
- Output artifacts
- Hand-off / shipping state

Show this summary to user BEFORE auditing. User confirms or corrects. Why — auditing the wrong understanding wastes the audit.

### Phase 3 — Multi-pass audit

Run ALL of the following passes. Each pass produces findings rows.

#### Pass 1 — Workflow integrity
- Pipeline reproducible? Can someone clone the repo and re-run?
- Cache discipline: CSV cache vs DuckDB DWH; staleness gate; idempotent re-run; preserve history on incremental update
- Output discipline: saved under `output/` not workspace root; named with date stamp
- Pre-commit checks / CI passing
- Auto-send safety: no stakeholder auto-email; pipeline fail-alert wired

#### Pass 2 — Business logic + domain accuracy
- Cite-check every external number (bank rates / market prices / industry benchmarks): verified vs canonical source, dated
- Domain terms used correctly (product acronyms, channel names, account types not confused with one another)
- Cohort definitions consistent across cards
- Currency / unit / time-zone consistent
- "Obvious by definition" statements flagged (e.g., a tier defined as "heavy withdrawers" being labeled "withdraws a lot")

#### Pass 3 — Method maturity (the rigor pass)
Compare method-actually-used vs the decision table in `references/causal-inference-toolkit.md`:

| If the analysis claims... | Method should be... | Falsification required |
|---------------------------|---------------------|------------------------|
| "X caused Y" with treated + control + pre/post | DiD or Event Study | Parallel-trends test |
| "X caused Y" with sharp cutoff | RDD | McCrary density, covariate balance |
| "X caused Y" with single treated unit | Synthetic Control | In-space placebo |
| "X caused Y" with observational + confounders | PSM | Covariate balance + Rosenbaum bounds |
| Endogenous treatment + valid instrument | IV | First-stage F ≥ 10, overid J-test |
| Continuous correlation, n ≥ 83 | Pearson r | (none for correlation) |
| Step-function variable | Event Study (NOT Pearson) | Pre-event leads zero |

If method used ≠ method indicated by data setup → flag as method mismatch with concrete upgrade path.

Then validation stacking check (per `references/validation-evaluation-methods.md`):
- Bootstrap CI run if n < 30 or non-normal? If missing → recommend `scripts/stats/bootstrap_ci.py`
- Robustness across ≥3 specifications? If missing → recommend running varied controls/subsamples
- Sensitivity across parameter ranges? If missing → recommend varying bandwidth/window/threshold
- Multiple-testing correction if K > 1? If missing → recommend `scripts/stats/multiple_testing.py` (Bonferroni or BH-FDR)
- Falsification test appropriate to method? If missing → recommend the relevant script
- Pre-registration / locked-plan documented? If missing → recommend a 5-line pre-reg in the notebook

#### Pass 4 — Advanced-method opportunities
Look for places where a more advanced method would strengthen the claim:
- Heavy-tail outcome (median ≈ 0, SD/mean > 3×)? → switch to Wilcoxon + winsorize + median Δ (3-5× power recovery — see `feedback_heavy_tail_kills_mean_did_power`)
- Staggered treatment timing in DiD? → use Callaway-Sant'Anna or Sun-Abraham (TWFE biased)
- Time-series outcome? → Bayesian structural time-series or causal-impact lib
- Survival outcome (time-to-event)? → Cox regression, Kaplan-Meier
- High-dimensional confounders? → Double-ML / LASSO + IV
- Each suggestion ships with: when this advance is justified, when it's overkill

Why this pass — Sub-mode A would not catch these; they require knowing the causal-inference toolkit + scanning method-mismatch patterns. This is the "có advance hơn được không" capability.

#### Pass 5 — Code & reproducibility check
- Tests: any unit / integration / regression tests? Pipeline gate?
- Environment: `requirements.txt` / `pyproject.toml` pinning? Python version stated?
- Secrets: no creds in code (grep for `api_key=`, `password=`, `BEARER`)
- Logging: pipeline has structured logs with timestamps / severities?
- Idempotency: re-running the pipeline gives same result?
- Karpathy 4 principles applied (think-before / simplicity / surgical / goal-driven)?

#### Pass 6 — Delivery surface (includes the full A-flow + outline check)
Run mechanical `rubric_audit.py --project <dir>` across all narrative files in the project → roll up findings.

Additionally, run the Outline / Story Flow Check per `self-check-protocol.md` Section A2 on the project's PRIMARY deliverable artifact. Project-level audit without outline check = body-deep, narrative-blind.

### Fresh-session review discipline (Sub-mode B specific)

When Sub-mode B spawns a sub-agent for context tracing (Phase 2) or method audit (Pass 3), the prompt MUST follow `references/subagent-prompt-discipline.md`:
- The review agent gets ZERO context from the generator (no prior chain-of-thought leakage)
- Brief uses context-packet pattern (file paths + 1-line purpose, NOT file contents)
- Bake positive + negative examples in the prompt; ban heuristic shortcuts

Why mandatory — review agents anchored on generator's reasoning produce confirmation bias. The whole point of an independent review pass is to catch what the generator missed.

### Phase 4 — Deliver the audit + rework plan

The deliverable is NOT just a gap table — it is a structured **rework plan** with user approval gate.

Format:

```
PROJECT AUDIT — <project name> — <date>

Verdict: ship / fix-then-ship / rebuild

Top findings (BLOCKER first, then HIGH):

[BLOCKER] Method mismatch: claim "campaign X caused +12% retention" 
  uses naive pre/post comparison. Treated + control groups available 
  in data; should run DiD with parallel-trends falsification.
  Effort: 2 hours (DiD + parallel-trends + write-up)
  Why: Pre/post alone confounds treatment with secular trend; not a 
  causal claim until DiD passes parallel-trends.

[BLOCKER] Bank rate 5.5% cited as Techcom Q1 2026 — actual verified 
  rate is 5.2% (source: Techcom website 2026-04). Drift detected.
  Effort: 30 min (re-pull + update report numbers)
  Why: Stakeholder distrust scales on cite errors; one wrong number 
  contaminates all other claims.

[HIGH] No bootstrap CI on median-Δ ratio with n=21.
  Effort: 30 min (bootstrap_ci.py + add to report)
  Why: Parametric CI assumes normal sampling; for n=21 and skewed 
  ratio, bootstrap is the honest CI.

[HIGH] Multiple-testing not corrected across 6 hypotheses tested. 
  Bonferroni adjustment changes 2 "significant" findings to NS.
  Effort: 15 min (multiple_testing.py + update verdicts)
  Why: FWER at α=0.05 across K=6 tests is 27% — far above stated 5%.

[MEDIUM] HTML report missing per-chart inline takeaway on 4 charts. 
  Effort: 20 min.
  
[Polish bucket — 5 items, total ~30 min]

REWORK PLAN (sorted by impact × effort):
1. Fix bank rate cite — 30 min, BLOCKER ⟶ fix-pipeline mode
2. Add Bonferroni correction — 15 min, HIGH ⟶ insight mode
3. Re-run DiD with parallel-trends — 2 hours, BLOCKER ⟶ insight mode
4. Add bootstrap CI — 30 min, HIGH ⟶ insight mode
5. Add per-chart takeaway — 20 min, MEDIUM ⟶ report mode
6. Polish bucket — 30 min, LOW ⟶ report mode

Total effort estimate: ~4 hours.

APPROVE? [Y/N/Revise]
```

### Phase 5 — User approval → execute plan

- **Approve** → agent executes plan top-to-bottom; for each item switches into the right mode (fix-pipeline / insight / report) and reports progress
- **Revise** → user adjusts plan; agent re-confirms
- **Reject** → audit-only output; user takes the plan offline

### Anti-patterns for Sub-mode B

- Running Pass 1-6 BEFORE getting the Project Understanding confirmed in Phase 2 — risks auditing wrong scope
- Marking method-maturity finding as BLOCKER when the project doesn't actually claim causality — be precise about what the report is claiming
- Pretending to fact-check without actually pulling the canonical source — note "could not verify; recommend user check" if source unreachable
- Skipping the rework-plan output and dropping a gap table — user wanted plan-then-rework, not just diagnosis

## Sub-mode C — Stakeholder Questioning

### Goal
Help formulate the RIGHT questions to ask stakeholders BEFORE starting analysis. Anti-pattern: build first, ask later → rebuild.

### Step 1 — Map the stakeholder
- Who? (role, level — IC / manager / VP / CEO)
- What do they care about? (revenue / cost / risk / users / compliance)
- What language do they speak? (business terms vs technical metrics)
- What's their decision authority? (approve / advise / inform)

### Step 2 — Frame the question set (use 5W1H + Goal)

For every uncertainty in the brief, ask:
- **Question**: what exactly are we trying to answer?
- **Goal**: what's the measurable outcome that closes this question?
- **Why**: what's at stake (revenue, deadline, risk)?
- **What**: scope — what's in / out of this question?
- **Who**: who owns the decision + who provides the data?
- **When**: when does the answer need to be ready?
- **Where**: which system / region / cohort?
- **How**: what's the first data source / step?

### Step 3 — Anti-patterns to catch
- **Approval-ask masquerading as question**: "Mình có thể proceed không?" → reframe as directive: "Mình sẽ proceed với approach X. Confirm nếu khác."
- **Vague scope question**: "What should I focus on?" → reframe with options: "Should I prioritize T1 cohort, T3 drain, or MP growth? Each takes ~2 days."
- **Yes/no when you need a number**: "Is the drop significant?" → ambiguous. Ask: "Is a 5% drop in AUM over 24 days enough to trigger Tier-3 intervention review?"
- **Missing acceptance criteria**: "Want me to investigate Tier 3?" → no clear "done" state. Add: "...with deliverable = top-2 mechanisms by date X, criterion = each mechanism has p<0.05 evidence and reproducible cohort."

### Step 4 — Suggest the output form
For each question, suggest the deliverable form upfront:
- 1-line answer in chat?
- Quick chart in Slack?
- Half-day mini-report?
- Multi-day deep dive?

Mismatched form expectation = rework. Confirm before starting.

### Step 5 — Compile the brief
```
Stakeholder: <name, role>
Decision they need to make: <decision>
Top 3 questions you should ask before starting:
1. <Q1> — closes if: <criterion>
2. <Q2> — closes if: <criterion>
3. <Q3> — closes if: <criterion>
Suggested form: <chat / chart / mini-report / deep dive>
Suggested timeline: <T+1 / T+3 / T+7>
```

## Sub-mode D — Staleness Trace

### Goal
After a change to ONE asset, find and sync every DEPENDENT asset so the project stays consistent. A0/A/B
judge one artifact's quality; D checks consistency ACROSS many after a change. This is change-propagation
(BA: requirements traceability), not a quality critique.

### When
The user just changed a direction, an input, a result, or a diagram flow, and wants all related assets
(doc, plan, AC/DoD, output, sibling diagrams, README) brought in line with the new state.

### Two entry paths (the gate offers both)
1. User names the changed asset (a path) plus a one-line description of what changed. Preferred (precise).
2. No path given: agent AUTO-DETECTS the change from the action log: `git -C <project> status` + `git log -5`
   + recent file mtimes, lists the candidate changed source(s), and confirms with the user before tracing.

### Workflow
0. Identify the SOURCE asset + the specific change (the concept/flow/number/input that moved). `[GATE]`
1. Build the dependent set:
   - If the project has a trace manifest (`.trace.json` mapping source to dependents + concept tags), read it.
   - Else grep the project for the source filename AND the change's concept terms (node names, the metric,
     the flow label) across doc / plan / spec / AC-DoD / output / sibling diagrams. Glob the project tree so
     nothing is missed. State that grep-by-concept is heuristic (it can miss paraphrases).
2. Diff each dependent against the NEW source state: is it still consistent, or does it still assert the OLD
   value? Classify each IN-SYNC or STALE, with the specific stale line.
3. Present the trace table (dependent | what it still asserts | new source value | IN-SYNC / STALE) and the
   sync plan. `[GATE]` user approves before edits.
4. Update each STALE dependent to match the new source. One dependent = one commit (chunked-delivery). For a
   dependent that needs the user's domain input to resolve, FLAG it as an open item rather than guessing.
5. Independent audit: confirm each updated dependent is now consistent (read it back, or spawn one read-only
   checker for a large set, mirroring the req-recon check). Do not claim synced without re-reading.
6. Drop a done-receipt (`evidence-based-done.md`) naming every updated dependent, so the Stop gate verifies
   the sync actually landed.

### Output
A sync report: the source change, the dependent set, per-dependent IN-SYNC/STALE/updated, and any open items
needing user input. Plus the synced files (each its own commit).

### What NOT to do
Do not silently re-scope the change. Do not skip a dependent because it "probably still fits" (diff it). Do
not mark synced on "looks right" (re-read, evidence-based-done). Heuristic grep is a floor, not a proof, so a
trace manifest is the reliable path for a recurring project.

## Brainstorming Sub-Mode (when user is exploring)

When user says "brainstorm" or "discuss" without a specific deliverable in mind:
- Surface 3-5 angles on the problem
- For each angle: pros / cons / data requirements / time cost
- DO NOT pick — present options, let user choose
- Time-box: 15 minutes of brainstorm → user decides direction → switch to execution mode

See `superpowers:brainstorming` skill for the formal flow if scope is large.

## Critique Quality Checklist (before sending review back)

- [ ] Every BLOCKER has `file:line` reference (or for Sub-mode B: `path:section`)
- [ ] Every finding has a concrete fix suggested (not "improve this")
- [ ] Every finding has Why (per Rule 4) — Causal / Empirical / Comparative / Theoretical / Operational
- [ ] Severity assigned, not "all equally bad"
- [ ] Verdict is one of: ship / fix-then-ship / rebuild
- [ ] No bandwagon agreement — push back if user's hypothesis is weak
- [ ] No bandwagon disagreement — accept user's valid choices even if unconventional
- [ ] (Sub-mode B only) Project Understanding Summary was confirmed by user BEFORE audit started
- [ ] (Sub-mode B only) Rework Plan presented for approval BEFORE executing fixes

## Connect to Other Modes

For multi-point or repeated feedback, switch to the refine protocol (`references/refine-worksheet.md`) instead of free-form prompts.

After Sub-mode A or B delivers, fix flow goes through:
- Issues are code-only → mode-fix-pipeline
- Issues are reasoning / method → mode-insight (re-run analysis correctly)
- Issues are template / structure → mode-report
- Issues are data pipeline → mode-automation
- Issues are EDA / feature engineering → mode-process

Sub-mode B explicitly orchestrates this hand-off as part of Phase 5.

## Universal Rules Reminder

Critique itself is a deliverable. Apply all 4 quality rules:
- **Rule 1** — Orientation Block at top (verdict + summary)
- **Rule 2** — Baseline-Noise-Impact when citing metrics in the critique
- **Rule 3** — 5W1H Action Brief for any "should fix" recommendation
- **Rule 4** — Why-Explanation on every finding (why does this matter, why this fix, why this severity)

AI-tell ban applies to critique text.

---

## Sub-mode E — Lifecycle Compliance (did the project follow all 7 phases?)

### Goal
Scan a whole project for evidence of each delivery-lifecycle phase (DISCOVER -> MODEL -> SPECIFY -> REVIEW
-> DELIVER -> VALIDATE -> LEARN) and return a PRESENT / PARTIAL / MISSING scorecard + a gap worklist + a
Ship/Fix/Rebuild verdict. It answers "did this follow the full lifecycle, and what is missing?" - a
process-completeness / onboarding audit, NOT a quality critique (that is Sub-mode B).

### How
```bash
python scripts/validators/lifecycle_audit.py <project-dir>        # scorecard + gap worklist
python scripts/validators/lifecycle_audit.py <project-dir> --json # machine report
```
It scores each phase by presence-proof (an artifact by filename AND a content signal), never by "I
remember doing it". It is heuristic - confirm the scorecard by reading the flagged files. Phase
definitions + the rubric: `references/delivery-lifecycle.md` + `references/lifecycle-execution-rules.md`.

### Verdict
Count PRESENT of 7: 7 -> Ship (mature) | 5-6 -> Fix (close the gaps) | 3-4 -> Fix-heavy / consider
Rebuild process | <3 -> Rebuild (ad-hoc, no spine). Each PARTIAL/MISSING phase carries a concrete close-the-gap action.

### When to pick this (not B)
"Did this project follow the process / which phase is missing?" (E, completeness axis) vs "is the analysis
rigorous / can the method be more advanced?" (B, quality axis). Cheap to run; pair with B when both the
process and the rigor are in question.
