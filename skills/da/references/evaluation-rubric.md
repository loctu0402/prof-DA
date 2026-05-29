# Report Evaluation Rubric (C-level / DA-grade)

> The single front-door scoring rubric for auditing any stakeholder deliverable. Composes the existing
> rule infrastructure (`self-check-protocol.md`, `quality-criteria.md`, `rubric_audit.py`,
> `mode-review.md`) into one **BA/PM-grade scorecard** with a weighted grade and a binding must-fix gate.
> Use in `mode-review` Sub-mode A/B and as the target spec for the C3 validator.

## How to read

- 6 scored categories (weights sum to 100) + 1 synthesis category (the verdict).
- Each criterion: *what GOOD looks like · what BAD looks like · default severity if failed · covered-by*.
- Score each criterion 0-3 → category score = mean of its criteria → weighted total → letter grade.
- `[GATE]` criteria are hard-stops: any `[GATE]` failure = **not shippable** regardless of grade.
- This rubric does NOT re-define mechanics — it points to the file that owns each check (cross-link, never re-paste).

## Scoring scale (every criterion)

| Score | Meaning |
|-------|---------|
| 0 | Blocker — cannot ship (auto must-fix gate) |
| 1 | Major gap — ship only with caveat, fix next cycle |
| 2 | Minor gap — acceptable, polish later |
| 3 | Exemplary — no action |

## Category weights

| # | Category | Weight | Lens |
|---|----------|--------|------|
| 1 | Framing & Logic | 15 | BA problem-analysis |
| 2 | Data Integrity & Rigor | 22 | DA |
| 3 | Insight Quality | 22 | DA / consulting |
| 4 | Visual & Design | 13 | Brand + SWD |
| 5 | Language & Tone | 12 | Stakeholder comms |
| 6 | Delivery & Project Management | 16 | PM |
| — | Overall C-level Verdict | (synthesis) | Decision-readiness |

---

## 1. Framing & Logic (weight 15)

| Criterion | GOOD | BAD | Sev | Covered by |
|-----------|------|-----|-----|------------|
| 1.1 Orientation block | SCQR (written) / 3-line intro (dashboard) / "How to read" (multi-tab) at top | Jumps into charts with no frame | BLOCKER `[GATE]` | self-check A; `orientation_block.py` |
| 1.2 Report flow | Section order = Setup → Observation → Diagnostic → Decision; headings tell the story standalone | Recommendations before analysis; methodology dump first | MAJOR | quality-criteria #5; self-check A2 |
| 1.3 Metric choice | Metric fits the question; NSM/driver hierarchy explicit; right denominator | Vanity metric; driver shown as if co-equal to NSM | MAJOR | `metric-framework.md` |
| 1.4 Rationale (Why) | Every method/threshold/chart choice has an inline Why (Causal/Empirical/Comparative/Theoretical/Operational) | "We used X" with no reason | MAJOR | Rule 4; self-check E2; `rubric_audit.py` |

## 2. Data Integrity & Rigor (weight 22)

| Criterion | GOOD | BAD | Sev | Covered by |
|-----------|------|-----|-----|------------|
| 2.1 Numbers reconcile | Same metric matches across cards/tables/charts; headline back-derived from source | Card says 2.9T, table says 296B, unexplained | BLOCKER `[GATE]` | self-check D |
| 2.2 No hallucination | Every figure traceable to a query/source; sources named | Number with no provenance | BLOCKER `[GATE]` | this rubric |
| 2.3 No empty-as-finding | No `N/A`/`null`/`—`/`0`/`TODO` rendered as a real result | KPI card shows "N/A" styled as a finding | BLOCKER `[GATE]` | this rubric |
| 2.4 Reproducible | Runnable `.sql`/scripts + idempotent pipeline; one source of truth | SQL only as prose; numbers hardcoded in HTML JS, separate from the data doc | MAJOR | mode-review B Pass 1 |
| 2.5 No ambiguity | Denominators explicit, time window stated, terms pinned | "46% rút sớm" with no base, no period, no definition | MAJOR | self-check G; style-rules |
| 2.6 Baseline-Noise-Impact | Headline numbers pass the 3-rung ladder visible to the reader | Bare delta "X giảm 5%" | MAJOR | Rule 2; self-check B |

**Eat-your-own-dog-food rule:** the reviewer MUST verify before claiming a defect. Re-derive the number from
source first (e.g. an HTML `data-countup="2964" data-fmt="tenth"` renders **296.4**, not 2,964 — not a 10×
bug). An unverified "defect" in the review is itself a 2.2 violation of the review.

## 3. Insight Quality (weight 22)

| Criterion | GOOD | BAD | Sev | Covered by |
|-----------|------|-----|-----|------------|
| 3.1 Diagnostic not descriptive | Connect-the-Dots: Fact → Mechanism → Behavior → Impact → Evidence | "MBB grew from 26% to 70%" with no why; flagged "cần confirm" but never investigated | MAJOR | self-check C; mode-insight |
| 3.2 External / market context | Cross-period or competitive analysis cites market data + benchmarks (rates, gold, VNI, competitor) | Purely internal numbers when context is needed | MAJOR | mode-report checklist |
| 3.3 Non-obvious finding | Each major section surfaces something not inferable from the metric name | Every section restates the chart title | MAJOR | quality-criteria #3 |
| 3.4 Anti-bias | Negative findings get a counter-argument/recovery signal; structural vs cyclical distinguished | One-sided doom or one-sided hype | MINOR | mode-report checklist |

## 4. Visual & Design (weight 13)

| Criterion | GOOD | BAD | Sev | Covered by |
|-----------|------|-----|-----|------------|
| 4.1 Brand fidelity | Implements the locked template + canonical palette/fonts; no per-report freestyle | Each report a new palette (e.g. `#A50064` one day, `#d82d8b` another), bespoke CSS | MAJOR `[GATE if a locked template exists]` | `project-scaffold.md`; A2 fork-or-fail |
| 4.2 Chart choice | SWD discipline: action titles, grey + 1 accent, no pie / no 3D, horizontal logic | Pie chart, rainbow series, vague titles | MINOR | `storytelling-with-data.md` |
| 4.3 Per-chart takeaway | Inline `takeaway` verdict under every chart (drop/negligible/candidate/strong) | Chart with no callout | MINOR | style-rules; self-check H |
| 4.4 Interaction & readability | "How to read" present; data-card-on-hover shows full underlying data; email forces light-mode | Hover shows nothing; email breaks in dark mode | MINOR | mode-report HTML pattern |
| 4.5 Polish & highlight | Critical values highlighted WITH a why annotation; clear hierarchy | Wall of equal-weight numbers | MINOR | mode-report checklist |

## 5. Language & Tone (weight 12)

| Criterion | GOOD | BAD | Sev | Covered by |
|-----------|------|-----|-----|------------|
| 5.1 Natural Vietnamese | Reads like a Vietnamese analyst wrote it; tone fits audience | Word-by-word machine translation; literal calques; wrong register | MAJOR | this rubric |
| 5.2 Business-language over jargon | <product-b>/z-score/σ/p-value translated to VN business terms in UI labels | Raw statistical jargon in stakeholder-facing labels | MAJOR | `business-language` rule; style-rules |
| 5.3 Diacritics complete | All `ệ ỉ ổ à ă` correct | "rut som", "tang truong" | MAJOR `[GATE]` | self-check F |
| 5.4 No AI-tells | No `===`, `-----`, em-dash, `≈`, `→`; no generic "AI-dashboard" phrasing | Em-dash glue, arrow-soup, "comprehensive overview" filler | MAJOR `[GATE]` | `ai_tell_scan.py` |

**5.1 test:** read 5 sentences aloud. If any sounds translated-from-English (literal idiom, English word
order, no Vietnamese discourse particles where natural), score ≤1. This is the user's top recurring pain —
weight it.

## 6. Delivery & Project Management (weight 16)

| Criterion | GOOD | BAD | Sev | Covered by |
|-----------|------|-----|-----|------------|
| 6.1 Project scaffold | Standard layout (`queries/ cache/ scripts/ output/ data/` + README); files findable | 3 flat files dumped at project root | MAJOR `[GATE for project deliverables]` | `project-scaffold.md` |
| 6.2 Idempotency | Re-run gives same result; single source of truth | `.md` and `.html` hold the numbers separately and can drift | MAJOR | mode-review B Pass 1 |
| 6.3 Portal published | Pushed via `portal_upload.py` (72h TTL, stable UUID); receipt saved (`latest_portal_url.json`) | Report saved locally, link never created | MAJOR `[GATE when delivery expected]` | mode-report Step 9 |
| 6.4 Naming & versioning | Date-stamped + `_latest` pointer; old versions archived | `report_final_v3_real.html` chaos | MINOR | self-check K |
| 6.5 Output location | Under `output/` or `projects/<name>/output/`, never workspace root | Saved to repo root | MINOR | output-policy; self-check K |

## 7. Overall C-level Verdict (synthesis)

Compute the weighted grade, apply the gate, then write a one-paragraph verdict answering the only question
that matters: **could a C-level make a decision from this without a round of back-and-forth?**

### Weighted grade

`overall = Σ(category_mean × weight) / 100`, mapped:

| Grade | Range | Action |
|-------|-------|--------|
| A | 2.7–3.0 | Ship as-is |
| B | 2.2–2.69 | Ship after minor polish |
| C | 1.7–2.19 | Fix-then-ship |
| D | 1.0–1.69 | Major rework |
| F | <1.0 **or any `[GATE]` fail** | Rebuild |

### Must-fix gate (any one → not shippable, overrides grade)

- Any criterion scored 0.
- 2.1 numbers don't reconcile · 2.2 unsourced number · 2.3 empty-as-finding.
- 1.1 no orientation · 5.3 diacritics broken · 5.4 AI-tells present.
- 6.1 no scaffold (project deliverable) · 6.3 portal not published (when delivery expected).
- 4.1 freestyled visual when a locked template exists.

---

## How to apply (fill this per review)

```
EVALUATION — <deliverable> — <date> — reviewer: <agent/Loc>

[Orientation] SCQR of the review itself (what / why reviewing / verdict preview).

Per-category scorecard:
| Cat | Criterion | Score 0-3 | Evidence (quote + file:line) | Severity | Fix |
| 1   | 1.1 ...   | 2         | "..." (report.html:165)      | minor    | ... |
... (all criteria)

Category means: 1=__ 2=__ 3=__ 4=__ 5=__ 6=__
Weighted overall = __ → Grade __

Must-fix gate: [PASS / FAIL → list triggered items]

Verdict (1 paragraph): Ship / Fix-then-ship / Rebuild — could a C-level decide from this? why/why not.

Must-fix before ship (ordered by impact × effort):
1. [sev] item — fix — effort
...
```

The "must-fix before ship" list is the **binding contract** the user asked for: every reviewing session
produces the same scorecard shape and the same gate, so verdicts are comparable across Claude sessions.

## Why this rubric exists (Rule 4 meta)

The plugin already enforces *rules* (orientation, ladder, AI-tells) but reports still drift in **visual
consistency, project structure, and Vietnamese tone** — the parts no single existing check scores. This
rubric is the whole-artifact, BA-decision-matrix lens (per `nab-tech-interview/02_analysis-skill.md`:
weighted decision matrix + gap analysis) that makes "is this C-level ready?" a reproducible score, not a vibe.

## Cross-references

- Mechanical ~30-check audit → `scripts/validators/rubric_audit.py` + the C3 consistency gate.
- Pre-ship line-checklist → `report-standard-checklist.md`.
- Whole-artifact 5 criteria → `quality-criteria.md`.
- Pre-ship sections A–N → `self-check-protocol.md`.
- Review workflow (sub-modes, severities, rework plan) → `mode-review.md`.
- Scaffold + portal + design-handoff standards → `project-scaffold.md`, `mode-report.md`.
