# A2 · Ops Dashboard — Design Spec

Archetype for single-page operations dashboards. Structure: fixed sidebar scroll-spy,
KPI hero section at top, one section per operational area, Plotly charts inline.
Use for monitoring-at-a-glance then drilling in.

## When to use A2

Use A2 when the report answers: "What happened yesterday, is anything off, and where do I drill?"

Qualifying signals:
- Recurring (daily / weekly) operational snapshot
- One primary KPI (the NSM) with 2–5 contributing areas beneath it
- Audience needs both a headline read and the ability to drill into each area
- Data is a single T-1 (or T-N) snapshot — not a multi-period comparison report

Do NOT use A2 for:
- Long-form editorial analysis (use A3)
- Pure trend / forecast reports with no operational breakdown (use A1)
- Cross-product benchmarking (use A5)

## Section order (canonical)

```
top ─ story headline (h1) + how-to-read orientation
    ─ family-snapshot (executive row — one card per area, click → jump)
    ─ § 01  NSM anchor          (hero cards with data-hover tooltip)
    ─ § 02  Primary flow        (waterfall + expected overlay chart)
    ─ § 03  Users / audience    (stat grid + line chart + driver table)
    ─ § 04  Channel / cohort A  (stat grid + sorted bar chart)
    ─ § 05  Quality / satisfaction (stat grid + line chart)
    ─ § 06  Segment / sub-group (scatter chart)
    ─ § 07  External / context  (stat grid + heatmap)
    ─ footer (run timestamp, methodology link, version)
```

Add or remove sections freely. Keep the story-headline → family-snapshot → NSM order fixed.
Section numbering is display-only (§ 01 … § 0N) — renumber after adding/removing sections.

## Fork procedure

1. Copy the entire `A2-ops-dashboard/` folder. Never edit in place.
2. Open `boilerplate.html`. Replace placeholder text:
   - Every `<span class="ph">[ descriptive-key ]</span>` → real rendered value.
   - Every `data-bind="key"` attribute → your data-binding key or remove the attribute.
   - Every `data-hover='{"label":"[ … ]", …}'` → real actual / expected / gap / z / verdict.
   - Plotly placeholder arrays (`WATERFALL_Y`, `USER_MAU`, etc.) → real data fetched at render time.
3. Replace section titles and nav labels with your product's operational areas.
4. Remove sections that have no data; remove the corresponding nav link.
5. Update the footer run timestamp and methodology link.
6. Do NOT retheme (no new `:root` values); only the token contract may supply color hex values.
7. Leak-check before shipping: grep for any hardcoded brand hex, brand name, locale-specific unit, or private path, and remove them.

## Token rules (hard)

- Colors: `var(--token)` only. No hardcoded hex anywhere.
- Banned: any hardcoded brand hex anywhere in components. Keep colors in `var(--token)` so the palette stays swappable; brand values live only in the `:root` block.
- Plotly trace colors: use `var(--accent)` resolved at runtime, or the neutral palette constants defined in the `<script>` block (`ACCENT`, `GREY`, `SUCCESS`, `WARN`, `DANGER`). Never pass a banned hex into a Plotly config.
- To retheme: swap only the `:root` block at the top of `<style>`. Every component resolves tokens — no other change needed.

## Language rules

- English only in all structural text: headings, labels, nav items, chart axis titles, legend text, badge text, table column headers, `.ph` placeholder keys.
- Body prose (takeaways, insight text, orientation paragraph) may be in the report's delivery language but must not appear in this skeleton.
- No locale-specific language, diacritics, or currency units in the skeleton; keep it English and unit-neutral.

## Chart vocabulary for A2

| Chart type | Use for | Banned alternative |
|---|---|---|
| Waterfall + expected overlay | Flow breakdown by channel / category | Stacked bar with dual-Y |
| Line + shaded expected band | Time-series KPI trend | Area-only (no line) |
| Sorted horizontal bar | Driver ranking by impact (z or delta) | Pie / donut |
| Scatter (bubble) | Segment positioning on 2 axes | 3D scatter |
| Heatmap (week × day) | Day-of-week seasonality pattern | Calendar chart |

Banned chart types (never use in A2): pie > 2 slices, 3D, gauge-for-KPI, dual-Y with
unrelated units, rainbow colorscale, bars with non-zero baseline.

Every chart must have: x-axis title, y-axis title, a takeaway sentence above the plot,
a source line below the plot.

## Honest-interactivity classification

Tag every interactive element in comments with one of three classes:

| Class | What it means | Examples in this skeleton |
|---|---|---|
| `truly_interactive` | Recomputes or redraws from baked inline data | Segment-filter checkboxes updating the by-segment bar |
| `snapshot_explainer` | Shows a tooltip / modal explaining a pre-computed value; no recompute | data-hover cards, date picker showing snapshot message |
| `metadata_action` | Operates on the page or session, not on data | Save view, Share link, Export PDF, Reset |

Never label a snapshot_explainer as truly_interactive in docs or tooltips.

## Responsive breakpoints

| Breakpoint | Behavior |
|---|---|
| > 1100 px | 240 px fixed sidebar + content area (default) |
| ≤ 1100 px | Sidebar collapses to inline; no fixed column |
| ≤ 900 px | Hero grid, stat grids → single column; driver table hides Expected + Reading columns |
| ≤ 700 px | Family-snapshot grid → 2 columns |
| print | Sidebar hidden; page-break-avoid on cards and charts |

## Data-hover tooltip contract

Every `.nsm-card` and `.stat` element must carry a `data-hover` JSON attribute with these keys:

```json
{
  "label":    "[ Metric name ]",
  "actual":   "[ formatted actual value ]",
  "expected": "[ formatted expected value ]",
  "gap":      "[ ±X.X% ]",
  "z":        "[ ±X.X ]",
  "verdict":  "[ Normal | Watch | Investigate now | … ]",
  "cls":      "success | warn | danger | neutral"
}
```

The `z` key must always be the primary alert signal (not `gap`) for net-flow or near-zero
baseline metrics where `%gap` is mechanically noisy.

## Verdict severity system

| cls value | Token pair | Meaning |
|---|---|---|
| `success` | `--success` / `--success-soft` | Within expected range |
| `neutral` | `--neutral` / `--neutral-soft` | No baseline or within noise |
| `warn` | `--warn` / `--warn-soft` | Elevated; monitor |
| `danger` | `--danger` / `--danger-soft` | Out of range; action required |
