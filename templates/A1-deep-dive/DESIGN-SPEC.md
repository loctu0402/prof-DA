# A1 Deep-Dive — Design Spec

Archetype: causal "WHY" diagnostic report.
Answers one question: why did metric X move?
Graded on whether every hot spot is *investigated*, not merely flagged.

---

## When to use

Use A1 when:
- A metric has deviated meaningfully from its expected range and the audience needs a defensible causal explanation.
- Stakeholders will challenge the finding — the report must carry its own evidence.
- The investigation spans multiple driver families (structural causes AND cyclical causes, separated).
- Recommendations need a cited KPI target, not a rough aspiration.

Do NOT use A1 for:
- Routine daily/weekly monitoring snapshots (use A2 or A3).
- Forward-looking projections (use A5).
- Executive summary without evidence chains (use A6).

---

## Section order

| # | Section | Purpose |
|---|---------|---------|
| — | Masthead | Product / topic label, edition badge, run timestamp. |
| — | Causal question title | The single why-question, displayed as a large heading before any evidence. |
| — | SCQR frame | Situation / Complication / Question / Resolution — the answer stated before the evidence, so the reader knows where the report is going. |
| §01 | North-Star Metric anchor | Primary metric as a 6-layer block (value, deltas, deviation score, takeaway, verdict); two driver-family blocks below in a 2-col grid. |
| §02 | Market context | Macro signals (indices, rates, competitor benchmark) fetched live, never hard-coded; one impact-news item. |
| §03 | Observation ladder | Per headline number: Baseline (how the reference was set) → Noise/Signal (CI, p-value) → Impact (effect size in business terms). Three horizontal stages with a connector arrow. The decisive stage gets the accent-soft background. |
| §04 | Diagnostic chains | The core. One card per hot spot: hot-spot question + structural/cyclical tag, then the 5-step chain (Fact → Mechanism → Behavior → Impact → Evidence), then a mandatory counter-argument callout, then one Plotly evidence chart. |
| §05 | Recommendations | One card per action: title as a directive, 8-field grid (Question / Goal / Why / What / Who / When / Where / How), KPI = Base × (1+Lift) row with a cited precedent. |
| §06 | Methodology appendix | The ONLY place statistical notation (deviation score, CI, sigma, p-value) appears. Four definition rows: deviation score, CI/sigma, effect size, structural/cyclical criteria. |
| — | Footer | One-sentence causal signal + two portal links (dashboard, methodology) + run metadata. |

Reading path: SCQR Resolution + §01 = the answer up front; §03–§04 = the defense; §05 = the action; §06 = the proof for those who need it.

---

## Fork rules

1. **Copy boilerplate.html into your report folder** (do not edit the skeleton in place).
2. **Swap the `:root` block** with your organization's brand tokens. Keep the token NAMES (`--bg`, `--accent`, `--danger`, etc.) unchanged — all components resolve from them. Only the hex values change.
3. **Replace every `.ph` placeholder** (marked `data-bind="..."`) with live data. Never leave a bare N/A; use a styled `.ph` span until data is ready.
4. **Replace the Plotly skeleton data** in the `<script>` block with real series. The skeleton arrays are illustrative only.
5. **Do not add new hardcoded hex colors.** If a new semantic color is needed, add a new `--token` to the `:root` block and reference it via `var(--token)`.
6. **Language:** structural text (headings, labels, column headers, nav, badges) stays English. Body prose and insight copy goes in your organization's language.
7. **Counter-argument is mandatory** on every negative diagnostic finding. Remove the `.counter` div only for positive/neutral findings.

---

## Chart types that fit A1

| Chart | Use case | Notes |
|-------|----------|-------|
| Line (actual vs expected) | Primary evidence for a single metric deviation over time | Highlight the investigation day with a larger, accent-colored marker. |
| Waterfall | Decompose a net movement into signed driver contributions | Effective in §04 to show which driver contributed what share of the total delta. |
| Sorted bar | Compare driver magnitudes at a point in time | Sort descending by absolute contribution; color by direction (success/danger). |
| Scatter + fit line | Show a relationship between two variables claimed in the mechanism | Include the fit line and the R-squared or p-value in the chart annotation. |

Banned: pie / donut (part-to-whole distortion), area-stack without a clear additive story, 3-D charts of any kind.

One evidence chart per diagnostic chain; maximum three Plotly charts per report (keep the file under 1 MB).
Each chart must have both axis titles. Axis labels and legend entries use plain business language, not formula notation.

---

## Observation ladder rules

- The **decisive stage** (the one that settles signal vs noise) gets `class="lstage decisive"` which applies the `--accent-soft` background.
- Deviation score values are colored by severity: `.sv.success` (within range), `.sv.warn` (watch/attention), `.sv.danger` (abnormal).
- State the p-value explicitly in the Noise/Signal stage description. If unavailable, state the confidence interval in the same slot.
- The Impact stage states the effect size in business units, not in sigma.

---

## Diagnostic chain rules

- Tag each chain `structural` or `cyclical`. The tag drives the pill color (`--neutral-soft` / `--warn-soft`).
- The 5 steps (Fact, Mechanism, Behavior, Impact, Evidence) must all be present. Evidence without a Mechanism is a flag, not a chain.
- The counter-argument (`<div class="counter">`) is the intellectual honesty gate. It states what would be true if the alternative explanation were correct, then shows why the data rules it out.
- Severity flag on the card: `flag-red` (danger), `flag-amber` (warn), `flag-neutral` (informational).

---

## Responsive behavior

- Below 900 px: driver grid, ladder stages, and brief grid collapse to single column; market card stacks vertically; ladder arrows rotate to point down.
- Below 820 px: SCQR collapses from 4-col to 2-col.
- Print: `break-inside: avoid` on every block, ladder card, diagnostic chain, brief, and method card. Shadows stripped. Padding reduced. This archetype is designed to print cleanly — test before delivery.
