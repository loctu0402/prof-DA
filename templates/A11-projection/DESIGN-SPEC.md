# A11 Projection — Design Spec

> Delta of A1 (deep-dive). States only what changes or is new. Read A1's spec first.
> Archetype: single-file HTML · theme tokens via `:root` swap · org-neutral skeleton.
> Skeleton: `boilerplate.html`

---

## 0. Purpose

Project a metric forward with an honest, non-alarming uncertainty band and the
assumptions that would change the call. The reader should leave knowing:

1. Where the metric is expected to land (base projection + confidence band).
2. What model was used and why the band width is that wide.
3. What would need to change for the projection to be wrong.

---

## 1. Signature constraint — delta-flat band

The band **must have constant vertical width** across the entire forecast horizon.

- Width = sigma computed over the lookback window, held flat at every x-position.
- A widening cone is the wrong shape: it gives absurd far-horizon ranges and reads
  as worst-case fear rather than steady-state uncertainty.
- Mandatory business note inline on the chart: state that the band represents
  steady-state uncertainty, not a worst-case scenario.
- Review gate: if the rendered band widens at any x > today, reject and rebuild.

Band geometry reference (SVG inline or Plotly `tonexty` fill):

```
upper_y - lower_y  ==  constant  at every forecast x
```

---

## 2. Information architecture (delta vs A1)

Sections added or changed; A1 sections not listed here are either inherited or dropped.

| # | Section | Status |
|---|---------|--------|
| 01 | Method note (model, lookback, PI method, backtest, assumptions) | **New** — up front, not appendix |
| 02 | Projection chart — history + delta-flat band + today divider | **New** (extends A3 band pattern) |
| 03 | Scenario table — low / base / high with driving assumption per row | **New** |
| 04 | Assumptions table — each assumption with documented rationale | **New** |
| 05 | Deviation verdict scale — z-score or robust band, never raw % | **Carried from A1** |
| 06 | Confidence framing — invalidation triggers + re-forecast cadence | **New** |

Dropped from A1: diagnostic chain, observation ladder, field briefs,
monitoring overlay (unless backtesting). NSM anchor is optional.

---

## 3. Component details

### 3.1 Headline block

Shows the projected end-of-horizon value, band low/high, and sigma.
One-line business takeaway in plain language. No z-score in the headline —
the z-scale lives in §05 for when actuals arrive.

### 3.2 Method note (§01)

A left-accented card above the chart. Rows: model · lookback · prediction-interval
method · backtest summary · key assumptions. Mono keys, prose values.
Required because readers evaluate projection credibility from the method, not
the chart alone.

### 3.3 Projection chart (§02)

Preferred renderer: Plotly CDN (`plotly-2.27.0.min.js`) for hover and
responsiveness. Fallback: inline SVG (zero-JS, fully controlled geometry).

Color contract (token-based):

| Element | Token / style |
|---------|--------------|
| Historical actuals | `var(--ink-2)` solid line |
| Forward centerline | `var(--accent)` dashed |
| Band fill | `var(--accent-soft)` at low opacity via `tonexty` or SVG fill |
| Today divider | `var(--border-strong)` dashed vertical |
| Grid lines | `var(--grid)` |

Never use literal hex values inside the rendered chart; use the neutral hex
equivalents that correspond to the `:root` slate tokens when the charting
library cannot consume CSS variables directly. Update these hex equivalents
when re-theming the `:root` block.

### 3.4 Scenario table (§03)

Three rows: High / Base / Low. Each row has a left stripe (color from token set),
projected value, driving assumption, and deviation from a reference expressed as z.
Base row has a light accent-soft background to anchor the eye.

Deviation column rule: show z-score where a distributional baseline exists.
Show directional label (above / in-line / below) where no stable baseline exists.
Never show raw percentage gap as the primary deviation signal.

### 3.5 Assumptions table (§04)

Every assumption that materially affects the projection gets one row:
label (mono), value or direction, and a rationale column. Rationale must
reference a source or explicit reasoning — "assumed" alone is not acceptable.
Ungrounded assumptions are flagged with a `.flag` pill.

### 3.6 Deviation verdict scale (§05)

Inherited from the token contract. Driven by z-score or an equivalent robust
band (e.g. IQR-based). Scale: on-track / watch / attention / abnormal.
Used when actuals arrive and must be compared to the projection band.

### 3.7 Confidence framing (§06)

A grid of invalidation triggers (what would make the projection wrong) and a
re-forecast cadence statement. Minimum two triggers; four is the expected count.
Cadence is either time-based (weekly), event-based (trigger activation), or both.

---

## 4. Visual rules

- All colors via `var(--token)`. No literal brand hex anywhere in the skeleton.
  The `:root` block in `boilerplate.html` is the single swap surface for re-theming.
- Accent token drives: today-divider dot, method-note left border, forward centerline,
  band fill (accent-soft), section index numbers, placeholder underline.
- Section headings use `var(--primary)`.
- Verdict pills use the four semantic tokens: success / warn / warn / danger.
- Font stack: system sans-serif (body), system monospace (numeric / keys / placeholders).
  Swap to brand typefaces in the `:root` / body rule; do not hardcode font names
  in component classes.

---

## 5. Placeholder convention

All data positions use `<span class="ph" data-bind="dot.path">[ label ]</span>`.
Text-weight placeholders add `.txt` to the class. The renderer replaces inner
content at the `data-bind` key. No raw values, company names, product names,
metric names, or locale-specific units appear in the skeleton.

---

## 6. Responsive and print

- `max-width: 1180px` centered wrap with side padding.
- Below 900px: scenario table drops the assumption column to a sub-line;
  method-note rows stack single-column; confidence trigger grid goes single-column.
- Print: white background, `break-inside: avoid` on all cards, no box-shadows.
- Single-file budget: keep below 1 MB including any inline chart data.

---

## 7. Fork instructions

1. Copy `boilerplate.html` into the report's output folder.
2. Replace the `:root` token values with the org's brand palette.
   Keep all token **names** unchanged so component classes keep resolving.
3. If using a brand typeface, update the `font-family` in the `body` rule.
4. Fill every `data-bind` attribute with rendered values.
5. For the chart: replace placeholder arrays with real data; update the
   neutral hex values inside the Plotly script to match the swapped `:root` tokens.
6. Verify the band geometry lock: `upper_y - lower_y` is constant across
   all forecast x-positions before publishing.

---

## 8. Review checklist

- [ ] Band is constant-width (same pixel height at t=0 and t=horizon)
- [ ] Steady-state note is present on the chart
- [ ] Method note is above the chart, not in an appendix
- [ ] Every assumption row has a rationale (not blank, not "assumed")
- [ ] Deviation column in scenario table shows z, not raw %
- [ ] All colors are `var(--token)` references (no literal hex in component CSS)
- [ ] No brand names, product names, locale tokens, or private paths in the file
- [ ] All placeholder text is wrapped in `<span class="ph" data-bind="...">[ ... ]</span>`
- [ ] Plotly neutral hex values are documented as `:root` equivalents (update on re-theme)
- [ ] File is self-contained and renders standalone in a browser without external assets
  beyond the Plotly CDN script
