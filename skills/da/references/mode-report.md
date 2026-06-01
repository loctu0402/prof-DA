# Mode — Build Report from Template

Invoke when user asks: "build báo cáo", "làm report", "stakeholder report", "/prof-DA:report".

## Decision Tree — Pick Template

```
What is the report for?
  │
  ├─ Daily ops snapshot (product / fraud / app performance)
  │   └─ shared/templates/daily-email/
  │
  ├─ Idea / scheme verification (gross yield, breakeven, tier proposal)
  │   └─ shared/templates/idea-verification-compact/
  │
  ├─ Deep dive WHY (AUM decline, net cash, user churn diagnostic)
  │   └─ Use deep-dive-analysis SKILL (separate skill)
  │
  ├─ App / dashboard performance monitoring
  │   └─ shared/templates/app-dashboard/
  │
  ├─ Presentation deck (academic, training, leadership update)
  │   └─ shared/templates/presentation/
  │
  ├─ Google Chat webhook notification
  │   └─ shared/templates/gchat-webhook/
  │
  └─ Custom one-off
      └─ Confirm intent → choose closest template → fork
```

Full template catalog: `<your-workspace>/shared/templates/_catalog.md` (or equivalent index file in your workspace). If you don't have a template catalog yet, start by saving one report you're happy with under `<your-workspace>/shared/templates/<name>/` and document it in the catalog.

## Workflow

### Step 0 — Detect or create project scaffold (BEFORE any output)
Run the Step-0 protocol in `project-scaffold.md`: glob the target project dir; align to an existing layout, or
create the standard one (`queries/ scripts/ cache/ data/ output/{reports,charts,data}/` + `README.md`) and move
artifacts in. Never dump the deliverable flat next to source files. Announce the scaffold in one line.
`[GATE]` — `scripts/validators/report_consistency_audit.py` flags `scaffold_missing`.

### Step 1 — Confirm Audience & Output Format
- Audience: team / manager / cross-functional / C-level?
- Format: HTML SPA / PDF / email body / Gchat / slides?
- Language: Vietnamese with diacritics (stakeholder) or English (internal docs)?
- Length: 1-page summary or multi-section?

### Step 2 — Fork a locked template (fork-or-fail, NEVER freestyle)
- Pick the template from the Decision Tree; read its `_index.md`; copy it to the project's `output/`.
- NEVER edit the template source during a build — fork first.
- **Fork-or-fail — do NOT invent a bespoke visual.** Claude Code is biased to "ship something working" and
  produces a generic per-report design; that is the root cause of "every report a different style". If the
  chosen template is a README-only stub with no forkable HTML/CSS, STOP and do ONE of:
  (a) reuse the closest real template + its canonical theme (`shared/themes/<organization>_chart_theme.py`: pink
  `#d82d8b`, cream `#fdf6ee`, teal `#00b4a0`);
  (b) prepare a `DESIGN_HANDOFF_REQUEST.md` per `claude-design-handoff-not-freestyle` and wait for the spec;
  (c) flag that the template library needs this archetype built (Phase B), then implement 1:1 once locked.
  `[GATE]` — `report_consistency_audit.py` flags `freestyle_palette` when a build defines a bespoke palette
  with no reference to a locked template/theme.

### Step 3 — Wire Data
- For daily snapshots: pipeline already populated CSV / JSON cache → load and render
- For ad-hoc: write query (see mode-query) → cache result → render
- Verify data freshness: T-1 typical, T-2 on holidays; flag if older

### Step 4 — Apply Orientation Block
- SCQR at top for written reports
- 3-line intro for HTML dashboards
- "How to read" guide for multi-tab artifacts
- Terminology Block if niche / multi-meaning terms appear

### Step 5 — Populate Body (with Baseline-Noise-Impact + Storyline + SWD discipline)
- Every numeric statement passes 3 rungs (see `universal-workflow-rules.md`)
- Every chart follows visualization discipline → `references/storytelling-with-data.md` (action title, grey + 1 accent, no pie / no 3D, clutter checklist, horizontal logic)
- Every chart has inline `→ takeaway` verdict
- Every table sorted DESC if "Top X"
- Organization brand theme applied (loaded from `<your-workspace>/shared/themes/` or your equivalent module)
- Number formatting: K / M / B / T per scale; 2 decimals; comma-separated people count

#### Storyline > Dashboard (Consulting pattern)

**Why this matters (Empirical):** consulting firms (McKinsey/BCG/Bain) consistently use storyline-driven slides because senior decision-makers spend 10 seconds per slide. Dashboard-style slides (2-4 generic info clusters with vague titles) force readers to interpret charts themselves; storyline-style slides deliver the message directly.

**WRONG (Dashboard pattern):**
```
Slide title: "Business Update Q2 2026"
[Chart 1: Revenue 2023-2025] (vague title, no message)
[Chart 2: Top 5 Projects]
[Chart 3: Cost breakdown]
[Chart 4: Key Challenges]
```
Reader has to: parse 4 charts → infer relationships → guess what matters → potentially reach wrong conclusion. Cost: 60s/slide minimum, often misread.

**RIGHT (Storyline pattern):**
```
Slide title: "Revenue growth is slowing — 2025 added only ₫3B vs ₫5B in 2024"
[Chart: Revenue 2023=10, 2024=15, 2025=18, with growth-rate annotations]
Sub-headline: "Two drivers: enterprise renewal slowdown + SMB churn rising"
[Supporting evidence chart × 2]
Sub-headline: "Recommendation: invest in renewal team Q3, defer SMB acquisition"
```
Reader gets the message in 10s; chart supports rather than carries the story.

**Question-based framing FIRST (mandatory pre-step):**

Before writing storyline titles, draft the SECTION QUESTION the slide answers. Each storyline title is the ANSWER to a question stakeholder would actually ask. This makes:
- (a) **Why the slide exists** legible (without the question, slide is just decoration)
- (b) **Predicted result** visible BEFORE building the chart — easier to plan
- (c) **Action implied** clear because the question is decision-shaped

Pattern per section:
```
[Q]  <question stakeholder would ask> (1 line, simple)
[A]  <complete-sentence storyline title that answers it> (your slide title)
[Why this section]  <1-line Why per Rule 4 — Causal/Empirical/Comparative/Theoretical/Operational>
```

Worked example (weekly sales report):
```
Section 1
[Q]  "Doanh thu tuần này có healthy không?"
[A]  "Doanh thu tăng 8% WoW lên ₫4.2B — vượt 4-week avg 12%"
[Why]  Operational — manager Monday review cần snapshot trước khi diễnh đi sâu

Section 2
[Q]  "Tăng trưởng đến từ đâu?"
[A]  "Tăng đến từ Premium tier (+18%); Basic flat (+1%)"
[Why]  Causal — không break-down driver thì recommendation thiếu specificity

Section 3
[Q]  "Có anomaly nào cần flag không?"
[A]  "Region Bắc giảm 5% — nghi do campaign expired thứ 4"
[Why]  Empirical — pattern khớp timing của campaign expiry, đáng investigate

Section 4
[Q]  "Vậy bây giờ phải làm gì?"
[A]  "Khuyến nghị: gia hạn campaign Bắc + amplify Premium"
[Why]  Operational — manager cần action item rõ ràng để approve trong Monday meeting
```

The [Q] [A] [Why] triplet stays in YOUR working notes; only [A] appears on the slide. But agent MUST produce all 3 internally before writing the slide. If you can't write [Q], the slide doesn't belong in this report.

**Storyline checklist per slide / per section:**
- [ ] Section Question drafted (the [Q] the slide answers — kept in working notes)
- [ ] Title is a **complete sentence** that answers [Q] (not "Revenue Trend"; instead "Revenue grew 15% YoY, decelerating in Q4")
- [ ] Headline conveys **the conclusion**, not the topic
- [ ] Chart **supports** the headline (chart caption echoes the message)
- [ ] Sub-headlines split into **2-3 supporting points** at most
- [ ] Recommendation / next-step is **explicit**, not implied
- [ ] Why-Explanation logged for each section per Rule 4 (Causal/Empirical/Comparative/Theoretical/Operational)

**Integration with SCQR (Orientation Block):**
- S (Situation) → opening slide / section intro
- C (Complication) → "but here's what changed" headline
- Q (Question) → the analytical question being answered ← question-based framing maps directly here
- R (Resolution) → the recommendation as a complete-sentence slide title

SCQR is the document-level frame; storyline is the per-slide / per-section frame. Question-based framing is the bridge — each section's [Q] is a sub-Q of the document's Q in SCQR.

**Why question-based framing (Empirical):** consulting playbook (McKinsey/BCG/Bain) trains junior consultants to draft the question FIRST, then the answer, then the chart. Skipping the question → analyst builds charts looking for something interesting → slide titles become topics ("Cost analysis") not conclusions ("Costs grew 23% in Q3, driven by 2 vendors"). Decks read clearer when [Q] is explicit even though the stakeholder only sees [A].

**Anti-patterns:**
- Generic slide titles ("Business Update", "Q2 Review", "Cost Analysis") → readers don't know the point
- Multiple charts on one slide with no unifying message → cognitive overload
- Headline ≠ what the chart shows → chart undermines headline (or vice versa)
- "We will discuss X" as headline → tell the conclusion, not the agenda

### Step 6 — Recommendations Section (with 8-field Action Brief)
Per recommendation:
| Hành động | Lý do (cite section) | KPI | Timeline | Reference |

OR full prose with 8 fields (Question, Goal, Why, What, Who, When, Where, How).

### Step 7 — Self-Check (run the hybrid gate)
Run the gate first, then the protocol:
```bash
python scripts/validators/self_check.py <deliverable>   # orientation + ai-tell + action-brief + consistency
```
Any `[GATE]` failure in `references/report-standard-checklist.md` blocks "done" (scaffold, portal, AI-tells,
diacritics, empty-as-finding, orientation). Then walk `references/self-check-protocol.md`. Top blockers for reports:
- Numbers reconcile across cards / tables / charts
- AI-tell symbols absent (`===`, `-----`, em-dash, `≈`, `→`)
- Vietnamese diacritics complete
- Per-chart takeaway present
- "Reading in business terms" column on number / formula tables
- Highlighted significant records with WHY annotation
- No auto-send hooked (file is saved to `output/`, NOT emailed yet)
- Outline / Story Flow Check passes (extract headings standalone, see `self-check-protocol.md` Section A2)
- Every KPI card shows DUAL comparison (DoD + 7d avg) — single delta = noise (see `style-rules.md`)
- Every chart has ALL 7 anatomical elements (Figure / title / axes / legend / total cards / insight line / notes / download)
- Sentiment color matches the dashboard context (override mapping documented if non-default — see `style-rules.md`)

**Enforced by a Stop hook (v3.6):** the bundled `hooks/stop_gate.py` blocks your turn from ending while a
pending report deliverable fails the consistency gate. It is RECEIPT-DRIVEN: it acts ONLY if Step 8 wrote
`<project>/.prof-da/pending-validation.json`, and is silent on every non-report session. For rendered
HTML/dashboard deliverables, `orientation_block` / `action_brief` inside `self_check` are ADVISORY (the
orientation lives in the layout, recommendations in the Recommendations section); the HARD gate the hook
enforces is `report_consistency_audit` (scaffold / portal receipt / empty-as-finding / dropped diacritics).
Run that one to see exactly what the gate will check:
```bash
python scripts/validators/report_consistency_audit.py <deliverable>
```

### Step 7.5 — HTML SPA verification (when screenshot unreliable)

For HTML report deliverables: a screenshot in a constrained preview pane may miss layout issues (clipped content, hidden tabs, empty cells, broken scroll). Substitute structural JS inspection.

Inspection checks to run via `preview_eval` (or equivalent):
- Document height vs viewport (sanity: not 0, not absurdly large)
- Document scrollWidth vs clientWidth (horizontal overflow signal)
- Empty cells across major tables (`document.querySelectorAll('td:empty')`)
- Tab counts (`document.querySelectorAll('.tab')` — does it match the spec?)
- Bounding boxes of section blocks (any with zero height?)

What inspection catches that screenshot misses: structural integrity. What it does NOT catch: aesthetic correctness — for that, escalate to a separate screenshot pass at full viewport.

See `feedback_inspection_audit_when_screenshot_unreliable.md` for the past incident pattern.

### Step 8 — Save to output/
- `output/reports/` for generic reports
- `output/projects/<project>/` for project-tied output
- Filename: `<topic>_<YYYY-MM-DD>.html` (e.g., `daily_snapshot_2026-05-08.html`)
- Also write `<topic>_latest.html` symlink / copy for stakeholder bookmark
- **Drop the validation receipt (this is what arms the Stop-hook gate):** write
  `<project>/.prof-da/pending-validation.json` =
  `{"deliverables": ["<saved report path, relative to project root>"], "attempts": 0}`.
  The bundled Stop hook then blocks finishing until the report passes `report_consistency_audit`, and
  deletes the receipt automatically on pass. Without this receipt the gate stays silent, so report mode
  MUST write it; that is what makes Step 7 non-skippable for a report deliverable.

### Step 9 — Publish to portal (the always-forgotten step)
After save + verify, publish the deliverable to a shareable 72h link. This is NOT auto-sending to people
(that still waits for "send") — it produces the LINK form of the deliverable, which the user needs almost
every time (especially daily auto-reports) and the agent routinely forgets.

```bash
# one-off:
python shared/portal_upload.py upload <report>.html --duration 72
# recurring report (keep the SAME link across days — reuse stored UUID):
python shared/portal_upload.py replace-or-create <stable_uuid> <report>.html --duration 72
```
- Save the receipt in the project's `cache/`: `latest_portal_url.json` + `portal_stable_uuid.txt`. For
  recurring/daily reports, reuse the stable UUID so stakeholders' saved links keep working (content replaced, URL unchanged).
- Constraints: file `≤ 1MB`; `.html`/`.md` only; `duration ∈ {1,6,12,24,48,72}` (72 = max). Dashboard > 1MB
  → trim / inline-minify before publish.
- Give the user the returned `https://a01preview.web.app/view/<uuid>` link.
- Skip ONLY if the user explicitly says "no link". `[GATE]` — `report_consistency_audit.py` flags `portal_missing`.

## Master Checklist Items (top-of-mind)

Distilled from financial-product reporting context, but the items apply to any stakeholder report:

- [ ] Tab 1 (Insights & Summary) answers ALL questions standalone — reader doesn't need to open other tabs
- [ ] Market Context section (if cross-period analysis): VNI, Gold, Oil, USD/VND, Bank rates, RON95 — pulled from live cache, NOT hardcoded
- [ ] Competitor benchmark (if CASA-related): Techcom 5.5%, LPBank 4.5%, MSB 4.2%, Cake 3.6% (Q1 2026 — refresh if stale)
- [ ] Behavioral segmentation (not daily-snapshot tiers): classify by accumulated behavior
- [ ] Correlation analysis: Pearson with n ≥ 83 for p < 0.05 at |r| ≥ 0.22
- [ ] Cross-period comparison: same month last year + recent stable + pre-event
- [ ] Anti-bias: every negative finding has a counter-argument or recovery signal
- [ ] Structural vs cyclical: explicitly distinguish in conclusions
- [ ] Avoid obvious statements (e.g., "Tier 3 rút nhiều" — they're defined as 80%+ cashout)
- [ ] Highlight standard: pink background `#fce4ec` for critical values, bold for top changes, red border for anomalies — EVERY highlight has WHY text

## HTML Generator Pattern (when building HTML reports)

- Read baseline CSS from existing template FIRST (don't rewrite from scratch)
- File < 10KB usually = CSS mismatch / missing styles
- Chart.js 4.4.7 + chartjs-plugin-datalabels for charts
- Tab-based SPA for multi-section
- Embed data inline (no external fetch) for portable HTML

### NEVER edit generator for HTML patch
When user reports "the HTML has bug X":
- Do NOT modify `generate_report.py`
- CREATE `update_report_vN.py` that loads the HTML, patches it, writes a new file
- Why: generator is the next-day pipeline source. Patching it side-channels into next-day output without review.
- See `feedback_never_edit_generator_for_html_patch.md`

## No Auto-Send

Default: generate report → save to `output/` → show preview link to user → WAIT for "send" command.

Exceptions:
- Pipeline FAIL email to configured oncall recipient only (by design, auto-sent)
- Cron-scheduled daily reports (configured upfront, user pre-approved cadence)

## Style Quick Reference

Full list: `references/style-rules.md`. Top:
- Vietnamese diacritics for stakeholder content
- AI-tell ban: `===`, `-----`, em-dash, `≈`, `→`
- Numbers: K/M/B/T units, 2 decimals, RED/GREEN sentiment
- Top X sorted DESC always
- <organization> theme: pink `#d82d8b`, cream `#fdf6ee`, teal `#00b4a0`
- Per-chart inline `→ takeaway`
- Tables of numbers → "Reading in business terms" column

## Stabilize-to-Template (post-ship)

When a one-off report stabilizes (used 3+ times, structure feels final):
1. Extract reusable parts → `<your-workspace>/shared/templates/<name>/`
2. Write `_index.md` with usage notes
3. Update `<your-workspace>/shared/templates/_catalog.md`
4. Drift-check: if source file is also a template, update both same session — never defer

See `feedback_stabilize_to_template.md`.

## Reading Order Recap

Before building any report:
1. `references/universal-workflow-rules.md` — Orientation + Ladder + Action Brief
2. `references/project-scaffold.md` — Step 0 layout (detect or create)
3. `references/style-rules.md` — style polish
4. THIS file — template choice + workflow (Step 0 scaffold → … → Step 9 portal)
5. `references/report-standard-checklist.md` — the binding pre-ship gate (`[GATE]` / `[ADVISORY]`)
6. `references/self-check-protocol.md` — pre-ship checks
7. `references/evaluation-rubric.md` — how the result will be scored (7-category C-level grade)
