# A7 Exec One-Pager — Design Spec

Archetype for the prof-DA plugin. Org-neutral skeleton — fork for your brand by swapping the `:root` token block in `boilerplate.html`.

---

## 0. Purpose

A single-screen executive brief. The reader gets the decision, the evidence, and the actions in under one minute — no scrolling, no diagnostic chain, no methodology.

Distinct from A3 (editorial paper): A7 drops the 6-layer info block, the diagnostic chain, and methodology sections entirely. What remains is the irreducible minimum for a board-level decision read.

---

## 1. Structure (fixed — do not add sections)

```
┌─────────────────────────────────────────────────────┐
│ MASTHEAD   report name · badge · date               │
├─────────────────────────────────────────────────────┤
│ BLUF       one-sentence conclusion (highlighted)    │
│            Situation · Question · Answer  (3 cells) │
├──────────────────────┬──────────────────────────────┤
│ LEFT COLUMN          │ RIGHT COLUMN                 │
│  North Star Metrics  │  The One Chart               │
│  (2 NSM cards)       │  (headline visual)           │
│                      │                              │
│  Directive Recs      │  KPI Cards (2 × 2)           │
│  (2–3 items)         │                              │
├──────────────────────┴──────────────────────────────┤
│ FOOTER   run stamp · full-report link               │
└─────────────────────────────────────────────────────┘
```

Constraint: fits one viewport at 1180 px wide. If content requires scrolling on desktop, the report is too dense — cut or promote to A3.

---

## 2. Sections

### BLUF
- Eyebrow label: "Decision" (or the domain equivalent).
- `h1`: one sentence stating the conclusion. The key phrase is highlighted via `.hl` (accent underlay, no hardcoded color).
- Three-cell SCQR strip below: **Situation** (what changed), **Question** (the decision asked), **Answer** (recommendation, stated first and bolded).

### North Star Metrics (exactly 2 cards)
- Card 1 uses `.nsm-card.primary-accent` (accent top border) for the primary NSM.
- Card 2 is plain `.nsm-card`.
- Each card: label · verdict pill (`.vd`) · large value · two comparator slots (vs prior period, vs 7-day average).
- Color the `.big` value with `.warn` only when the metric is in a caution state; default to `var(--ink)`.

### The One Chart
- Exactly one chart. A second chart means the report should be A3.
- Wrap in `.chart-card`. Required anatomy: conclusion title (`.ttl`), legend note (`.leg`), one-line insight (`.insight` with `<b>Key insight:</b>`), the chart body (inline SVG or Plotly), source line (`.src`).
- The placeholder SVG shows a band + line pattern. Replace with the actual series for your use case.

### KPI Cards (2 × 2 grid)
- Four supporting metrics that contextualize the NSM cards and chart.
- Each `.kpi`: label (`.cap`) · value (`.v`) · comparator row (`.cmp`) with up/dn/warn color classes.

### Directive Recommendations (2–3 items)
- Use `.recs` with `.rec` children. Three-field layout per item: **when** (time horizon) · **owner** · **action** (imperative sentence) + **rationale** (one line).
- Voice: directive, not options. "Reduce X by Y" not "Consider reducing X."
- Cap at 3 items. More than 3 belongs in the full report.

---

## 3. Theming

All colors resolve through `var(--token)` only. The `:root` block at the top of `boilerplate.html` is the single swap surface.

To re-theme: copy the `:root` block, replace the hex values with your brand palette, keep every token name unchanged. The neutral slate defaults render standalone without any brand configuration.

Do not inline any hardcoded color values anywhere in the HTML — not in `style=` attributes, not in SVG `fill`/`stroke`, not in class overrides. Every color must go through a token.

---

## 4. Placeholders

Every runtime value must be wrapped in `<span class="ph" data-bind="key">[ label ]</span>` (numeric) or `<span class="ph txt" data-bind="key">[ label ]</span>` (text). The `data-bind` key is the contract between the template and the data layer.

Required binds (minimum set):

| Key | Content |
|-----|---------|
| `runtime.report_date` | Report date |
| `brand.name` | Report / product name |
| `bluf.statement` | BLUF one-sentence conclusion |
| `bluf.because` | Highlighted key reason |
| `bluf.situation` | Situation cell |
| `bluf.question` | Question cell |
| `bluf.answer` | Answer cell |
| `nsm1.*` / `nsm2.*` | NSM label, value, unit, verdict, deltas |
| `chart.title` | Chart conclusion title |
| `chart.insight` | One-line chart takeaway |
| `chart.source` | Data source attribution |
| `kpi0–3.*` | KPI label, value, unit, deltas |
| `rec0–2.*` | When, owner, action, rationale per rec |
| `runtime.run_time` | Generation timestamp |
| `foot.full_report_url` | Link to full report |

---

## 5. Responsive and print

- Below 900 px: two-column grid collapses to single column. Scrolling acceptable on mobile.
- Print: `break-inside: avoid` on cards; white background; color-adjust enabled.
- Budget: single self-contained file, no external assets beyond optional web fonts.

---

## 6. What this archetype is not

- Not a diagnostic report (no z-score tables, no methodology section) — use A3.
- Not an ops dashboard (no live refresh, no drill-down) — use A2.
- Not a deep-dive paper (no 6-layer info block) — use A1 or A3.

If the one-chart constraint feels too tight, the answer is not a second chart — it is promoting the deliverable to A3.

---

## 7. Fork checklist

- [ ] Swap `:root` token block for brand palette (hex values only; keep token names).
- [ ] Fill all `data-bind` placeholders from the data layer.
- [ ] Replace placeholder SVG with the actual chart for the use case.
- [ ] Confirm: one chart only, no scroll on a 1180 px desktop viewport.
- [ ] Confirm: all colors via `var(--token)` — no any hardcoded color values.
- [ ] Confirm: all text is in the target language — no locale-specific units or currency symbols baked into the template.
- [ ] Remove this spec file from the deliverable; ship only `boilerplate.html` (forked).
