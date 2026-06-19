# A3 · Editorial Paper — Design Spec

## When to use

A3 is the **5-minute C-level editorial read** — a single-scroll narrative that presents one primary metric, explains its drivers, shows a projection, and closes with decisions. Use it when the audience is senior leadership and the output must be both scannable and authoritative.

Choosing A3 vs other archetypes:

| Signal | Archetype |
|--------|-----------|
| Narrative first, numbers supporting | **A3 (this file)** |
| Numbers grid first, narrative optional | A1 |
| Operations / alerts dashboard | A2 |
| Drill-down comparison table | A4 |

A3 is the single most polished format. Reserve it for recurring executive reports, not ad-hoc data pulls.

## Section order (fixed)

1. **Masthead** — product name, report date, edition stamp
2. **SCQR orientation** — 4-cell grid: Situation / Complication / Question / Resolution
3. **Hero story + mood dial** — serif headline, lede paragraph, decorative SVG gauge
4. **§01 Primary metric** — 6-layer `.block` (L1 caption → L2 big number → L3 facts row → L4 takeaway → L5 note → L6 verdict pill + cite)
5. **§02 Diagnostics** — `.drv` driver table; subordinate to §01, never co-equal
6. **§03 Projection** — inline SVG delta-flat constant-width ±sigma band; zero JS
7. **§04 Market context** — `.market-card` with indicator chips and news feed
8. **§05 Recommendations** — `.rec-timeline` directive list (who / when / action / why / KPI target)
9. **Footer** — closing signal sentence, links, run stamp

Order is fixed. Do not reorder or skip sections.

## Fork rules

### 1. Copy the boilerplate, never freestyle

```
cp templates/A3-editorial-paper/boilerplate.html reports/my-report.html
```

Do not build A3 from scratch. The boilerplate's CSS is the single source of layout truth.

### 2. Swap the :root block for your brand tokens

Replace the `html[data-theme="slate"]` block in `<style>` with your brand's token values. Keep all `--token-name` keys identical — component classes resolve against names, not values.

### 3. Replace placeholders, never remove `.ph` spans

Every `<span class="ph">[ key ]</span>` is a named bind point. Replace its text content with a rendered value. Keep the `data-bind` attribute for traceability. Remove the `.ph` class only when the value is confirmed real.

### 4. No hardcoded hex values

All colors must resolve through `var(--token)`. A hex that bypasses the token system breaks theme-swapping and org-neutrality. Check with:

```
grep -nE '#[0-9a-fA-F]{3,6}' my-report.html
```

Result must be empty outside the `:root` block.

### 5. English structural text, delivery language for body prose

Section headings, column headers, KPI labels, nav elements = English.
Body sentences, takeaways, news summaries = your delivery language.

### 6. Zero JS — inline SVG only for charts

The only chart in A3 is the §03 projection SVG. No charting library, no canvas, no script tags for rendering. The SVG polyline points are written by the generator at render time.

### 7. One hero chart per report

A3 has exactly one chart (§03). If you need additional charts, promote to A4 (tabular) or a multi-section A1 layout instead.

## 6-layer block quick reference

The `.block` is the signature component of A3. Every metric in §01 is a block.

| Layer | Class | Purpose |
|-------|-------|---------|
| L1 | `.lc` | Caption + column key tag |
| L2 | `.lb` | Big number (serif, 56px) |
| L3 | `.lf` | Facts row — 3-up grid (vs prior day / vs 7d avg / vs expectation) |
| L4 | `.lt` | Takeaway — ▸ tick + business-language sentence |
| L5 | `.ln` | Note — metric definition in plain language |
| L6 | `.lv` | Verdict pill — one of: `.red` `.amber` `.green` `.neutral` |
|    | `.cite` | Source + z-score stamp |

Flag the block border-top by anomaly severity: `.flag-red` / `.flag-amber` / `.flag-green` / `.flag-neutral`.

## Verdict scale

| Class | Token | When |
|-------|-------|------|
| `.red` | `--danger` | Significant deviation — review now |
| `.amber` | `--warn` | Watch — early signal |
| `.green` | `--success` | On track or positive deviation |
| `.neutral` | `--neutral` | Within normal range |

Verdict is driven by z-score, not percentage gap. Net-flow or near-zero-baseline metrics must use z only (percentage gap explodes mechanically on these).

## Projection band rule

The §03 band is a **constant-width delta-flat ±sigma band**. It does NOT widen over time (no cone). The SVG band path uses fixed y-coordinates for both endpoints of the forward segment. Sigma is computed from a fixed lookback window, not from cumulative forecast error.

## Responsive breakpoints

- `≤900px` — all multi-column grids collapse to `1fr`; driver table hides type/reading columns
- `≤820px` — SCQR collapses from 4 to 2 columns
- Print — `break-inside:avoid` on blocks, no shadows, tighter padding
