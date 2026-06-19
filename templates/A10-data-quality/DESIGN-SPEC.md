# A10 Data-Quality Profile — Design Spec

> Archetype: A10 · Channel: single-file HTML (offline, no external deps) · Emitted by: `process` mode before analysis begins

A fit-for-analysis verdict on a dataset, produced before any modeling or reporting work starts. The signature is a per-column profile table with inline sparklines, a severity-sorted issues list, and a CSS-grid missingness heatmap — not full charts.

---

## 0. Purpose

Tell an analyst whether a dataset is fit for analysis, and exactly what is wrong, before they build on it. Reader is the DA and a reviewer. Output is a scan artifact, not a stakeholder deliverable.

---

## 1. Information Architecture

Six sections, in order:

| # | Section | Purpose |
|---|---------|---------|
| §01 | Dataset overview | Row count, column count, grain, date range, source |
| §02 | Missingness heatmap | Missing % per column x time-bucket — shows drift over time |
| §03 | Per-column profile table | Type, null %, cardinality, min/max, distribution sparkline, sentinel flags |
| §04 | Quality issues | Severity-sorted (Critical → Warn → Info), recommended fix per issue |
| §05 | Rule-based flags | High-cardinality ID, constant column, leakage risk, stale partition |
| §06 | Verdict | Fit for analysis? Ready / Ready-with-caveats / Blocked + blocker list |

---

## 2. Components

### Overview strip — `.ov-grid`
Five stat cells in a row: row count, column count, grain, date range, source. Monospaced numerics. All values are `<span class="ph">` placeholders with `data-bind` keys.

### Missingness heatmap — `.missmap` + `.mm-grid`
A CSS grid: one row per column, one cell per time-bucket (week, month, or partition — set at render time). Cell tint class `mm-0` … `mm-5` maps missing % to a six-step desaturated ramp from `var(--success-soft)` to `var(--danger)`. No JS. Scrolls horizontally at narrow widths.

### Per-column profile table — `.prof`
Grid-display table. Columns: severity stripe (3px left border) · column name (serif) · null % · distinct count · min/max (mono) · inline SVG sparkline (grey bars, single accent bar at anomaly bucket) · data type (mono) · flag chips.

Stripe color encodes worst flag severity: red = critical, amber = warn, green = OK, grey = no issue.

Flag chips (`.fchip`): `red` / `amber` / `green` / `neutral` — match the severity ramp. Common flags: `sentinel -N`, `N% null`, `high-cardinality ID`, `low cardinality`, `leakage risk`, `OK`.

At viewport ≤ 900 px: distinct, min/max, and sparkline columns are hidden; the table stays readable on tablet.

### Issues table — `.issues`
Four-column grid: severity chip · issue description · affected columns (mono) · recommended fix (italic, business-language voice — no statistical jargon in the fix text). Rows must be ordered Critical first, then Warn, then Info. Never alphabetical or insertion-ordered.

Severity chips (`.sev`): `critical` / `warn` / `info` — use the corresponding token tints.

### Rule flags — `.flags-list`
Two-column card grid (`.rule`). Four standard rules: high-cardinality identifier, constant column, leakage risk, stale partition. Add rows for project-specific rules. Each card has a rule name and a one-line plain-language description.

### Verdict block — `.vblock`
Large status chip (`.vchip`) on the left: `ready` (success tint), `caveat` (warn tint), or `blocked` (danger tint). Right side: bulleted list of conditions or blockers. Toggle the chip class at render time based on the worst issue severity.

---

## 3. Token Usage

All colors via `var(--token)`. The severity ramp drives meaning:

| Severity | Background token | Foreground token |
|----------|-----------------|-----------------|
| Critical | `--danger-soft` | `--danger` |
| Warn | `--warn-soft` | `--warn` |
| Info / neutral | `--neutral-soft` | `--neutral` |
| OK / ready | `--success-soft` | `--success` |

Accent (`--accent` / `--accent-soft`) is used for: the masthead dot, section-index labels, sparkline anomaly bars, placeholder underlines, and blocker bullet markers. It is not used as a data-meaning color.

Restate the full `:root` token block at the top of `<style>` so the file renders standalone without any external stylesheet. Replace token values with the organization's brand palette; keep all token names unchanged.

---

## 4. Placeholder Convention

Every data-bound value uses `<span class="ph" data-bind="key">[ descriptive default ]</span>`. Text values use `.ph.txt`. The `data-bind` attribute is the hook for any template engine or Python renderer that populates the skeleton.

Column names in placeholder content use generic labels (`col_1`, `col_2`, etc.). Issue descriptions, fix text, and rule descriptions use plain bracketed prose — no real entity names, no locale-specific terms.

---

## 5. Sparklines

Inline SVG, `viewBox="0 0 90 26"`, `preserveAspectRatio="none"`. Bars are `fill="var(--ink-4)"` (grey). The anomaly bucket gets `fill="var(--accent)"`. Flat-line sparklines (for ID columns with no meaningful distribution) use a single short rect. The SVG is decorative; no `<title>` or `<desc>` needed at skeleton stage.

---

## 6. Responsive and Print

- At ≤ 900 px: overview grid collapses to 2 columns; profile table hides cardinality, min/max, and sparkline columns; issues and flags go single-column; verdict stacks vertically.
- Print: `background: #fff`; `print-color-adjust: exact` to preserve tints; all cards set `break-inside: avoid`.

---

## 7. Atoms Not Used in This Archetype

The following components from the broader report library are intentionally excluded: the headline-metric anchor block, the deviation-verdict table, waterfall chart, dual-comparison KPI strip, multi-layer balance block, market-context panel, and multi-label sentiment ramp. This archetype is diagnostic and tabular; it does not carry trend or business-performance narratives.

---

## 8. Authoring Checklist

- [ ] `:root` token block present at top of `<style>` (no external stylesheet dependency)
- [ ] All colors via `var(--token)` — no inline hex values
- [ ] All data-bound values wrapped in `.ph` with `data-bind` key
- [ ] Placeholder column names generic (col_1, col_2 style)
- [ ] Issues table ordered Critical → Warn → Info
- [ ] Verdict chip class matches worst severity (`ready` / `caveat` / `blocked`)
- [ ] Missingness heatmap tint classes `mm-0` … `mm-5` (no inline hex)
- [ ] Responsive rules present (`@media (max-width:900px)` + `@media print`)
- [ ] No content in any language other than English
- [ ] No organization-specific names, codenames, paths, or locale tokens anywhere in the file
