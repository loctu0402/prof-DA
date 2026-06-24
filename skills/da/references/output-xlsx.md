# Output format — Spreadsheet (.xlsx) design contract

The spreadsheet RENDERER of the same Theme-Token Contract the HTML reports and charts use
(`<your-workspace>/shared/templates/_contract/`). One design language across every archetype —
a `.xlsx` is not exempt. A naked `openpyxl` grid (default font, no fills, no freeze, no
autosize) is a DEFECT, the same way an off-brand chart or an un-tokened HTML report is.

## The rule (enforced)

A generated data spreadsheet is NOT done until it has been styled through the workspace xlsx
theme module. Implementation home (create it once, mirroring the chart-theme module
`<your-workspace>/shared/themes/<organization>_chart_theme.py`):

```
<your-workspace>/shared/themes/<organization>_xlsx_theme.py
```

If that module does not exist yet, author it from this contract (the three helpers below are
the API), then reuse it for every spreadsheet thereafter — never re-style ad hoc per file.

## Themes — selectable, never force one

Fork the SAME themes as the Theme-Token Contract (tokens forked verbatim, not re-derived).
Offer the DA a choice; default to the muted / neutral-dark theme (warm-dark, high text
contrast, easy to read) — do NOT hard-code a single brand color. Typical set:

| key | use | header fill | key-column block |
|-----|-----|-------------|------------------|
| `muted` (default) | chill, warm-dark, readable | deep neutral slate | warm cream |
| `brand` | brand-forward | the brand primary-deep | brand-soft / gold |
| `formal` | executive / external | a deep formal tone (burgundy / ink) | warm gold |

## What the styler MUST enforce (presentation contract)

- **Header row**: deep primary fill + white bold (~11pt) + centered + wrapped + taller row +
  FROZEN.
- **Key-output columns** (the columns that matter — e.g. the answer / result / verdict): a
  distinct accent block fill so they stand apart from context columns.
- **Code columns** (SQL / formulas): tinted block + monospace + smaller size, separated from prose.
- **Zebra striping**: surface / surface-alt alternation on data rows.
- **Semantic color-coding**: map a categorical column to status tokens (e.g. a difficulty /
  severity / status column → success=green, warn=amber, danger=red).
- **Freeze panes**: through the id column, or through a whole leading meta block, so the key
  columns + header stay visible when scrolling right.
- **Auto-size**: column WIDTH content-aware (longest line, capped — narrow for ids, wide for
  text/code) AND row HEIGHT wrap-aware (estimated wrapped-line count × line-height, capped at
  Excel's 409pt max), full wrap + vertical-top. No overflow, no truncation, no lopsided cells.
- **Borders**: thin grid in the theme's grid token.

> Excel hard limit: a single cell holding 30+ lines (e.g. full SQL) hits the 409pt row cap and
> the tail clips visually (text intact, visible in the formula bar). When full per-line
> readability matters, render the long text line-by-line across rows in a dedicated sheet
> rather than cramming one cell.

## API shape (the three helpers)

```python
import sys; sys.path.insert(0, "<your-workspace>/shared/themes")
import <organization>_xlsx_theme as xt

xt.style_table(ws, theme="muted", id_col="<id-header>",
               color_code={"<status-header>": "<difficulty|status>"},
               key_cols=["<answer-col>", "<result-col>"], code_cols=["<sql-col>"],
               freeze_through="<last-meta-header>")
xt.add_index_sheet(wb, headers, rows, title="Index", theme="muted",
                   id_col="<id-header>", at=0)      # progressive-navigation sheet
xt.add_legend_sheet(wb, [(col, description), ...], title="Legend", theme="muted")  # dictionary
```

## Companion sheets (progressive-index pattern)

Every multi-row / multi-section workbook SHOULD carry:
- an **Index** sheet first — a one-glance navigation map (id + the categorical meta + the
  question/title + snapshot/window), and
- a **Legend** sheet — a column dictionary (each column + what it means + who fills it).

This mirrors the index-first / dictionary-map convention so a reader orients before diving
into the wide data sheet.
