# prof-DA bundled templates

Org-neutral starter templates the plugin ships so `report` mode is self-contained: fork one of these instead of freestyling a layout. They carry NO brand palette and NO sample data - the shared design DNA lives in [`_contract/THEME-TOKEN-CONTRACT.html`](_contract/THEME-TOKEN-CONTRACT.html), and every skeleton references `var(--token)` so re-theming is one `:root` swap. Replace the palette with your organization's brand tokens; keep the token NAMES.

## What is here

| Item | Kind | Use |
|------|------|-----|
| [`_contract/THEME-TOKEN-CONTRACT.html`](_contract/THEME-TOKEN-CONTRACT.html) | design DNA | The token set + base + core components (verdict scale, metric block, status chips) every archetype forks. The single re-theme surface. |
| [`proposal-walkthrough/`](proposal-walkthrough/) | forkable HTML | A project / feature proposal walkthrough (general to detail, Epic-Feature-Story + RAID + DoD/AC + provenance framing). |

## The A1-A12 archetype library (the report fork set)

`report` mode forks one archetype 1:1 and swaps data only - never freestyles. This is what fixes per-report style drift: every output reads like the same analyst made it. The 12 archetypes cover the full report surface (each is a folder with a `boilerplate.html` skeleton + a `DESIGN-SPEC.md`, or spec-only where noted):

| # | Archetype | Channel | Forks for |
|---|-----------|---------|-----------|
| A1 | Deep-Dive | portal HTML | a WHY diagnostic (SCQR + Fact / Mechanism / Impact chain) |
| A2 | Ops Dashboard | portal HTML | a scan/drill dashboard with sidebar scroll-spy |
| A3 | Editorial Paper | portal HTML / print / email | a 5-minute C-level read (the system source archetype) |
| A4 | Daily Email | email | a daily KPI email, force-light, inline charts |
| A5 | Google Chat card | Google Chat | a short KPI digest (`card.json`, cardsV2) |
| A6 | Slide Deck | slides | the slide IA reference (spec-only; A12 is the built form) |
| A7 | Exec One-Pager | portal HTML | BLUF + 2 NSM + 1 chart + directive recs |
| A8 | Idea Verification | portal HTML | hypothesis, transparent math, Go / No-go (spec-only) |
| A9 | Training Material | portal HTML | objectives, concept grids, worked examples |
| A10 | Data-Quality | portal HTML | per-column profile + severity issues + missingness |
| A11 | Projection | portal HTML | delta-flat band + scenario table (an A1 variant) |
| A12 | Slide Deck / PPTX | slides / editable PPTX | present live or hand off an editable deck |

> All 12 archetype folders are bundled: A1/A2/A3/A4/A7/A9/A10/A11 ship a `boilerplate.html` + `DESIGN-SPEC.md`, A5 ships `card.json` + `DESIGN-SPEC.md`, A12 ships `boilerplate.html` + `deck-stage.js` + `DESIGN-SPEC.md`, and A6/A8 are spec-only (`DESIGN-SPEC.md` — A12 is the built form for A6; A8 is a numeric-verification spec). Every skeleton is org-neutral (neutral slate tokens, English, `.ph` placeholders, no data) and forks the `_contract/` token set. `report` mode's fork-or-fail rule still holds: a spec-only stub triggers a 1:1 build against its `DESIGN-SPEC.md`, never a freestyle.

## Fork workflow

1. Copy the archetype folder (or `_contract/THEME-TOKEN-CONTRACT.html` as the base) into your project's `output/`.
2. Read the folder's `DESIGN-SPEC.md` first. Keep ONE `:root` theme block; delete the rest.
3. Fill the `.ph` placeholders (each carries a `data-bind` key). Never ship a bare number - the verdict scale + the metric block want absolute units + a z-score or a robust band, not a raw %gap.
4. Re-theme by swapping the `:root` token values to your brand; never inline a brand hex in a component.

## Adding an archetype

1. Create `<A-folder>/` with `boilerplate.html` (or `card.json`) + `DESIGN-SPEC.md`.
2. Reference `var(--token)` from `_contract/` only; no inlined hexes, no sample data (use `.ph` placeholders), org-neutral.
3. Add a row to the catalog above.
