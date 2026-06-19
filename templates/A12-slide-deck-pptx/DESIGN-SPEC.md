# A12 — Slide Deck (HTML + PPTX)

Archetype for live presentation decks that export to editable slide software.
The HTML file renders as a self-contained, navigable browser deck;
the same slide markup can be captured by a headless exporter into editable PPTX.

---

## §1 One-Idea-Per-Slide Rule

Each slide carries **exactly one idea**, expressed as an **action title**:
a complete sentence, active voice, that states the insight or recommendation directly.
The title sequence, read alone, tells the entire story.

> Good: "Retention drops sharply in the first 7 days after activation"
> Not: "Retention analysis" or "Q3 results"

Supporting content (evidence cards, tables, bullets) exists only to defend the title.
If content requires two ideas, split into two slides.

---

## §2 Slide Types

| # | Class(es) | Purpose | One per deck? |
|---|-----------|---------|---------------|
| 1 | `.cover` | Opening bookend: title, subtitle, ask, metadata | Yes (first) |
| 2 | `.agenda` | Agenda / section overview | Yes |
| 3 | `.divider` | Section transition marker | One per section |
| 4 | `.body-fill` | Generic content: text, bullets, charts | Many |
| 5 | `.scqr` | Situation / Complication / Question / Answer narrative frame | As needed |
| 6 | `.ev-grid` | Three evidence cards (key numbers side by side) | As needed |
| 7 | `.stat-grid` + `.anchor` | Stat / NSM anchor — large number(s) with context | As needed |
| 8 | `.body-fill` + `table.tbl` | Data table | As needed |
| 9 | `.swim` | Swimlane process diagram | As needed |
| 10 | `.raci` + `table.raci-tbl` | RACI responsibility matrix | As needed |
| 11 | `.map-tbl` | Two-column mapping table | As needed |
| 12 | `.ask-next` | Closing bookend: recommendation + next steps | Yes (last) |

---

## §2.1 Bookends (Cover + Ask)

Both bookend slides use `var(--primary-deep)` as background — a deep, saturated
variant of the brand primary. Fork this token to your organization's brand color;
never hardcode a hex value directly in slide content.

**Cover** must include: title (`.cover-display`), optional subtitle (`.cover-sub`),
one-sentence ask (`.cover-ask`), and metadata row (`.cover-foot`): author, team, date.

**Ask / Closing** must include: recommendation heading, next-steps numbered list
(owner + due date per item), and a contact block. Restate the recommendation first.

---

## §2.2 SCQR Slide

Pyramid-principle narrative: Situation (agreed fact) → Complication (what changed)
→ Question (what the audience now needs to know) → Answer (your recommendation).

The action title on the slide IS the Answer. The four-quadrant grid elaborates.
Every row in SCQR must fit without scrolling — keep each cell to 2–3 lines.

---

## §2.3 Swimlane Diagram

Structure: `.swim-lane` rows stacked vertically. Each row has a `.swim-lane-label`
(role or system name) and `.swim-lane-cells` containing `.swim-cell` boxes and
`.swim-arrow` connectors.

Authoring rules:
- Each cell = one atomic step, short noun phrase.
- Arrows (`→`) are plain Unicode; do not use image or SVG for connectors.
- Meaning must live in text, not in arrow direction alone
  (describe the handoff in the receiving cell if it is non-obvious).
- 3–5 lanes maximum for projection legibility.

---

## §2.4 RACI Matrix

Every activity row must have **exactly one A** (Accountable).
Use `.raci-pill` classes `R`, `A`, `C`, `I` — do not invent new codes.
Include the legend row at the bottom of every RACI slide.
Keep to ≤8 activity rows and ≤6 role columns for readability at 1920×1080.

---

## §2.5 Two-Column Mapping Table

Use for side-by-side comparisons: current vs. proposed, problem vs. solution,
input vs. output, old vs. new. Each mapped pair must have a clear pairing rule
stated in the action title or a short subtitle below the heading.

---

## §3 Canvas and Type Scale

Design canvas: **1920 × 1080 px** (16:9). `deck-stage.js` scales to viewport.
All font sizes use token variables; the values below are the defaults for a
1920×1080 canvas. **Floor is 24 px** — nothing smaller is legible at projection.

| Token | Default | Use |
|-------|---------|-----|
| `--type-display` | 86px | Cover title, section divider title |
| `--type-title` | 54px | Slide action title (h1/h2 in `.head`) |
| `--type-subtitle` | 38px | Cover subtitle, SCQR answer cell |
| `--type-body` | 30px | Body text, table cells, bullets |
| `--type-small` | 26px | Secondary body, mapping table text |
| `--type-label` | 24px | Eyebrows, table headers, chip text |
| `--type-chip` | 24px | Status pills, RACI pills |

Spacing anchors:

| Token | Default | Use |
|-------|---------|-----|
| `--pad-x` | 104px | Horizontal page margin |
| `--pad-top` | 80px | Top page margin |
| `--pad-bottom` | 76px | Bottom page margin |

---

## §4 Token System

All colors are CSS custom properties (`var(--token)`).
**Never place a hardcoded color value in slide content** — use only the tokens
defined in the `:root` block of `boilerplate.html`.

The default `:root` block defines an org-neutral slate palette.
To apply your organization's brand: copy the `:root` block into your fork and
replace token values with your brand's equivalents. No other CSS changes are needed.

Token categories:

| Category | Tokens |
|----------|--------|
| Surfaces | `--bg`, `--surface`, `--surface-alt`, `--surface-sunk` |
| Ink / text | `--ink`, `--ink-2`, `--ink-3`, `--ink-4` |
| Borders | `--border`, `--border-strong`, `--grid` |
| Brand | `--primary`, `--primary-deep`, `--primary-soft`, `--accent`, `--accent-soft` |
| Semantic | `--success*`, `--warn*`, `--danger*`, `--neutral*` (base + `-soft` variant) |
| Data series | `--series-teal`, `--series-blue` (charts/diagrams only; not UI chrome) |
| Elevation | `--shadow-sm`, `--shadow-md` |

---

## §5 Placeholder Convention

All demo values in `boilerplate.html` use bracket text: `[ key ]`

Numeric or data placeholders that will be filled programmatically:

```html
<span class="ph">[ value ]</span>
```

`.ph` renders with a monospace font and a dotted underline so placeholders are
immediately visible during review. Remove the class when replacing with real data.

Do not use real organization names, product names, codenames, or private paths
in any template file — including comments.

---

## §6 Entrance Animations

End-state is the **base style** (no animation properties). Animations are layered
on top via `@keyframes` gated on two conditions:

1. `[data-deck-active]` — the slide is currently displayed.
2. `@media (prefers-reduced-motion: no-preference)` — user has not opted out of motion.

This ensures print / PDF and reduced-motion environments always show the finished
slide state without JavaScript or animation running.

Available entrance classes: `.enter-fade`, `.enter-up`.
Stagger delays for lists and evidence cards are defined in the `:root` stylesheet.

---

## §7 PPTX Export Contract

A headless exporter (e.g., Puppeteer / Playwright) renders each slide at the
design canvas size (1920×1080) and converts the static DOM into editable PPTX shapes.

**10 rules for PPTX-compatible slide authoring:**

1. **Static slide bodies** — slide content must render correctly with no JavaScript
   (headless capture fires before JS animations settle). Structure in HTML; style in CSS.
2. **Real `<table>` for tabular data** — `<div>` grids do not convert to editable cells.
3. **Text ≥ 24 px** — text below 24 px may not be captured as editable text.
4. **No meaning in `::before` / `::after`** — pseudo-element content is not exported.
5. **No AI-tell glyphs** — avoid em-dash `—`, right-arrow `→` as semantic separators,
   ellipsis `…` as truncation, en-dash `–` as a minus sign; use plain equivalents.
   (Exception: `→` inside swimlane connector `.swim-arrow` is a layout element, not prose.)
6. **Entrance gated on `[data-deck-active]` + reduced-motion** — see §6.
7. **IBM Plex fonts** (Sans / Serif / Mono) — available in Google Slides' font picker;
   loaded via Google Fonts in `boilerplate.html`.
8. **Attribute `noscale`** on `<deck-stage>` disables the viewport transform so the
   exporter captures unscaled geometry. Add it before export; remove it for presentation.
9. **One slide per `<section>`** — do not nest sections or use JavaScript to split content.
10. **Speaker notes** in `<script type="application/json" id="speaker-notes">` as a
    JSON array (0-indexed by slide). The exporter reads this array and writes notes
    into the PPTX notes pane.

---

## §8 Fork Rules

To create a deck from this archetype:

1. Copy the entire `A12-slide-deck-pptx/` folder into your project's output directory.
2. Rename `boilerplate.html` to a descriptive project name (e.g., `q3-review-deck.html`).
3. Update the `:root` token block with your organization's brand tokens.
4. Replace `[ bracket text ]` placeholders and `.ph` spans with real content.
5. Delete slide types you do not need (or keep as hidden `data-deck-skip` sections).
6. Do not modify `deck-stage.js` unless fixing a navigation bug — style changes
   belong in the slide CSS, not the component.

**Do not freestyle layout outside these slide types** without adding a corresponding
entry to this spec. Consistency across slides is what makes the PPTX export reliable
and the deck scannable as a sequence.

---

## §9 Review Checklist (Done criteria before sharing)

- [ ] Title sequence (slide action titles) tells the complete story when read alone.
- [ ] Every slide has exactly one idea; no slide requires scrolling.
- [ ] All placeholder text (`[ ]` and `.ph` spans) replaced with real content.
- [ ] All colors come from `var(--token)` — no hardcoded hex anywhere in slide markup.
- [ ] No text below 24 px.
- [ ] No meaning lives in `::before` / `::after` or JavaScript-only content.
- [ ] Every `<table>` uses real `<table>` markup (not CSS grid).
- [ ] RACI matrix: each activity row has exactly one A.
- [ ] Speaker notes array length matches slide count.
- [ ] Deck tested at target projector resolution (1920×1080 or 1280×720).
- [ ] Deck tested with `noscale` attribute for PPTX export capture.
- [ ] Print to PDF (Ctrl+P) produces one slide per page at design size.
