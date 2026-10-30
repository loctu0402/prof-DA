# Glass dashboard standard: the hero + tabs + glass cards layout

> How a dashboard or a recurring report looks and reads. It adds a layout and a surface style on top of the
> Theme-Token Contract and the EFFECTIVE-HTML standard (`output-effective-html.md`). Tokens, themes and the
> light/dark toggle still come from those. This file sets layout, surfaces, text budget and chart grammar.
> Adopted 2026-10-30 from a daily product dashboard rebuilt as a Claude Dashboard artifact; it applies to every
> HTML dashboard and report and to BI builds (Sigma, Looker Studio, Metabase). A workspace may keep a forked
> reference build at `<your-workspace>/shared/templates/_contract/glass-dashboard.reference.html`.

## 0. The five rules (if you read nothing else)

1. **One number opens the page.** A hero card holds the outcome metric in a large serif, its date, two or three
   signed change chips, a forecast chip when a forecast exists, and a sparkline that carries the forecast band.
   Four secondary stats sit in one row under it, each with its own comparison.
2. **Sections are tabs, not scroll.** A sticky pill-shaped segmented control switches between three to five
   pages. Each page answers one area (cash flow, users, mix, acquisition). A page never holds more than
   about five cards.
3. **Few words.** A card title is two to four words. One grey note at the top right says the window and the
   unit ("60 days, USD m"). No section leads, no takeaways under charts, no method paragraphs on the
   canvas. One footnote line at the page foot names the source and the export date.
4. **Every number carries a comparison, and only change carries color.** Signed deltas are green when better,
   red when worse. Everything else uses one accent series color and muted grey. Red never means anything
   other than worse.
5. **Glass is a surface, not decoration.** Translucent panels over a soft colored backdrop, one hairline, one
   inner highlight, one soft shadow. No gradients on text, no glow on numbers, no animation on data.

## 1. Page anatomy, top to bottom

| Zone | What it holds | Rules |
|---|---|---|
| Hero | eyebrow (metric name + as-of date), big number + unit, 2 to 3 chips, sparkline, stats row | one outcome metric; chips are vs prior day, vs start of month, forecast; sparkline 45 to 60 days plus the forecast horizon |
| Stats row | 4 secondary metrics inside the hero, under a hairline | label, serif value, one delta line; compact notation (3.1M) |
| Tab bar | segmented control, sticky at the top | 3 to 5 tabs, nouns in English, the selected tab is a raised pill |
| Page | cards in an auto-fit grid, two per row when there is room | first card is the most decision-relevant; a full-width card for forecasts and tables |
| Card | title left, note right, optional legend, chart or table | title is a noun phrase; the note is window + unit only |
| Footnote | one centered caption line | source system, export or refresh date, what is left out |

Order inside a tab: the trend of the outcome first, then the flow that drives it, then the breakdown table.

## 2. Surface tokens (glass)

Write these as CSS on top of the contract tokens. No literal hex except inside `color-mix` with
`white`/`black` for highlight and shadow.

```css
.page { position: relative; isolation: isolate; padding: var(--pad-lg); border-radius: calc(var(--radius) * 3); overflow: hidden; }
.page::before { content: ""; position: absolute; inset: 0; z-index: -1; background:
  radial-gradient(40rem 22rem at 8% -4%,  color-mix(in srgb, var(--series-1) 30%, transparent), transparent 70%),
  radial-gradient(34rem 20rem at 96% 6%,  color-mix(in srgb, var(--series-2) 24%, transparent), transparent 70%),
  radial-gradient(40rem 26rem at 60% 110%, color-mix(in srgb, var(--series-3) 18%, transparent), transparent 70%),
  var(--bg); }
.glass { background: color-mix(in srgb, var(--panel) 62%, transparent);
  backdrop-filter: blur(22px) saturate(170%); -webkit-backdrop-filter: blur(22px) saturate(170%);
  border: 1px solid color-mix(in srgb, var(--fg) 9%, transparent); border-radius: calc(var(--radius) * 2.5);
  box-shadow: 0 1px 0 color-mix(in srgb, white 35%, transparent) inset, 0 12px 32px -18px color-mix(in srgb, black 35%, transparent); }
```

- Backdrop glows use the first three series colors of the active theme at 18 to 30 percent. They are the only
  place more than one hue appears outside charts.
- Panels stay at 55 to 70 percent opacity. Below that, text contrast fails in dark mode.
- Hairlines inside a card (table rows, the stats divider) are `--fg` at 6 to 10 percent.
- Dark mode needs no extra rule: every value above is a token or a `color-mix` of one.
- Email cannot render `backdrop-filter`: an email renderer uses a solid `--panel` card and keeps the layout.

## 3. Type and numbers

| Element | Font | Size | Notes |
|---|---|---|---|
| Hero number | serif, weight 400 | `clamp(2.6rem, 7vw, 4.2rem)`, line-height 1 | letter-spacing -0.02em, unit in sans at heading size, muted |
| Stat value | serif, weight 400 | title size | compact notation from 10,000 |
| Card title | sans, medium | heading size | sentence case |
| Notes, ticks, chips | sans | caption size | muted color |

- `font-variant-numeric: tabular-nums` on every number.
- Signed changes always show the sign: `+12.3`, `-17.2`, `+3.1%`.
- Units sit in the note or the column header, never repeated in each cell.
- Dates read `dd/mm` on axes and `dd/mm/yyyy` in tooltips and the eyebrow.

## 4. Text budget

| Place | Allowed | Not allowed |
|---|---|---|
| Hero | metric name, date, unit, chip phrases ("vs prior day") | sentences, explanations |
| Tab label | one or two English nouns | status words, numbers |
| Card title | 2 to 4 words, noun phrase or a short question | numbers, formulas, table names |
| Card note | window and unit | definitions, method, caveats |
| Legend | swatch + 1 to 3 words | sentences |
| Footnote | source, as-of date, what is out of scope | audit notes, author meta |

A definition the reader needs goes in the tooltip or the data source panel, not on the canvas. This
overrides the SCQR and reading-guide parts of the report writing standard for dashboards only. Written reports
(paper, email body, deck) keep the full writing standard.

## 5. Chart grammar

- **Line.** 2px, round caps and joins, an area fill that fades from 26 percent to 0 at the baseline. An end
  label prints the last value. No marker on every point.
- **Forecast.** The forecast line starts at the last actual point, is dashed (`4 4`) in the same accent color,
  and sits over a band at 12 percent opacity for the forecast range (state the confidence in the legend, for
  example "90% forecast range"). A dashed vertical reference line marks the last actual day. The forecast comes
  from the pipeline's own forecast log, never from a fit made inside the page.
- **Diverging bars.** Positive in the accent color, negative in the critical status color, zero line in the
  axis color. Bars at most 32px wide, radius 2px.
- **Two periods on one chart.** The current period in the accent color, the prior period in the muted color,
  x-axis is day of period. Legend sits above the chart.
- **Tooltip.** A popover with the date first in secondary text, then one line per series with a swatch when
  there is more than one series. A dot on the hovered point and a vertical rule for multi-series charts.
- **Axes.** 4 y ticks, x ticks spaced by width (about one per 80px), margins measured from the widest label as
  drawn. One y-axis per chart.
- **Height.** 220 to 240px for cards, 150px for the hero sparkline. Each chart box keeps a `min-height` equal to
  its drawn height so loading states do not move the page.

## 6. Tables

- Right-aligned numbers, left-aligned first column, header in caption size and muted.
- Share columns carry an in-cell bar: a 5rem pill track at 8 percent `--fg` with an accent fill.
- Signed change columns use the good and bad colors; zero stays default.
- A total row is bold. Secondary columns (prior period values) hide below 40rem width.
- Keys stay raw on the row (`data-key`) when the shown label is translated.

## 7. States

| State | Show |
|---|---|
| Loading | skeleton bar in the element's box, no spinner, no words |
| Failed | one centered line: a small red dot and "Failed to load" in caption size |
| Empty value | transparent text, the box keeps its size |
| Refreshing | the element at 50 percent opacity |

## 8. Renderers

| Surface | How this standard applies |
|---|---|
| Claude Dashboard artifact | full standard. Page opens with `<meta name="dash-one-writer">`; every value is a `data-draw` element marked with its dataset; computed figures are `dash.calc`; glass tokens map to `--color-panel`, `--color-fg`, `--color-bg` and `dash.colors[0..2]`. See the reference build if your workspace keeps one |
| Standalone HTML report or dashboard | full standard on top of EFFECTIVE-HTML: keep the `data-theme` and `data-mode` toggle; the backdrop glows use the active theme's series tokens |
| Email HTML | layout and text budget only; solid panels, light mode forced, sparkline as a static image |
| Sigma workbook | see section 9 |
| Matplotlib / Plotly static charts | chart grammar only (section 5) through your theme module |

## 9. Sigma translation (same idea for any BI tool)

Sigma has no blur or translucency, so the glass becomes a clean light card; the layout and grammar carry over.

| Standard | Sigma build |
|---|---|
| Hero | a full-width row: one large KPI chart for the outcome metric with `periodComparison` and its trend, then four smaller KPI cards in one row |
| Forecast chip and band | a forecast series from the warehouse forecast table drawn dashed beside the actual series; the range as two dashed `refMarks` or an area series at low opacity |
| Tab bar | a `tabbed-container`, one tab per area, three to five tabs |
| Card title + note | element title as a noun phrase; window and unit in the (i) description, not as a visible line |
| One accent | one series color for actuals, grey for prior periods, red only for worse |
| Footnote | one text element at the page foot with the source and refresh time |
| States | Sigma handles them; no work |

Where a team has its own dashboard rulings (titles, filters, text on canvas), those rulings win over this
section, and this standard only fills what they leave open.

## 10. Pre-publish check

1. The hero has one outcome number, its date, at least two signed chips and a sparkline.
2. Every stat and every KPI has a comparison with a sign and a good or bad color.
3. Tabs are 3 to 5; each tab page has at most about five cards.
4. No card has a sentence on its canvas beyond the note; the footnote names source and as-of date.
5. Only change carries red or green; charts use one accent plus muted grey.
6. Forecasts are dashed with a band and a last-actual marker, and they come from the pipeline's own log.
7. Light and dark both read; no literal hex outside highlight and shadow mixes; layout holds at 400px width.
8. No number is typed into markup: every figure comes from data.
