# Output format — HTML artifact (SPA / dashboard / diagram / plan) design contract

The HTML RENDERER of the same Theme-Token Contract the charts and spreadsheets use
(`<your-workspace>/shared/templates/_contract/`). One design language across every archetype — an HTML
report, dashboard, system diagram, or plan is not exempt. A hard-coded-hex, single-theme, un-toggleable
HTML artifact is a DEFECT, the same way a naked `openpyxl` grid or an off-brand chart is.

## The rule (enforced)

Any HTML deliverable you author — a report SPA, a dashboard, a flow / architecture diagram, a plan — is
NOT done until it follows the EFFECTIVE-HTML standard: it re-skins from ONE token swap, carries a
light/dark toggle, and its diagram geometry survives a theme change. Fork the boilerplate; never freestyle
a bespoke hard-coded-hex page (the root cause of style drift, the same `fork-or-fail` gate the report
templates use).

Concrete standard + the fork artifact (author once, then fork for every HTML artifact thereafter):

```
<your-workspace>/shared/templates/_contract/EFFECTIVE-HTML-STANDARD.md       (the full standard)
<your-workspace>/shared/templates/_contract/effective-html.boilerplate.html  (the fork)
```

## The three load-bearing rules (if you read nothing else)

1. **Geometry in the markup, colour in the tokens, state in the classes.** A node's position/size lives in
   the SVG/HTML; every colour is a `var(--token)`, never a literal hex; interactive state (lit / dimmed /
   active) is a CSS class, never an inline style. So one token swap re-skins the whole artifact and a theme
   change cannot break the layout.
2. **One theme system, two orthogonal axes on `<html>`.** `data-theme` (the brand palette) and `data-mode`
   (light | dark) on `documentElement`; an apply-before-paint inline `<script>` in `<head>` BEFORE the
   stylesheet (no FOUC) reads localStorage and sets both. Tokens: base on `:root`, brand by
   `[data-theme=...]`, dark by `[data-mode=dark]`. Dark mode is a TOGGLE OPTION, never the only mode.
3. **Every element traces to the content; nothing leaks build context.** Each node/section maps to a real
   part of the report or process; no internal build/provenance notes, file paths, or author meta in a
   stakeholder artifact.

## SVG-via-CSS — the theme-following diagram

A diagram (flow / architecture / mind-map) is styled by CSS CLASSES that read `var()` tokens, NEVER a
hard-coded `fill="#..."`. Marker (arrowhead) fills use `style="fill:var(--token)"`. Node variants are
classes (e.g. `.node.gate / .store / .do / .ext`); an interactive flow = dim-others + a `.lit` highlight
with a numbered sequence. So the diagram re-skins with the page and dark mode just works — the fix for the
"hollow boxes, unclear flow, hard-coded colours" failure mode.

## Toggle UI + interactivity

- A brand `<select>` (the `data-theme` axis) + a light/dark `<button>` (the `data-mode` axis), both
  persisting to localStorage. Themes are DA-selectable; never force a single brand colour.
- Interactivity (a node detail card, a flow highlight, a tab) is CSS-class-driven state, prerendered +
  offline-first — never a runtime-only effect that breaks when the file is opened from disk.

## Per-artifact adoption

| Artifact | Apply |
|---|---|
| Report / dashboard SPA | full: tokens + both axes + the toggle UI + per-chart takeaway |
| System / flow / architecture diagram, mind-map | full: SVG-via-CSS classes + the flow-highlight grammar |
| Plan / one-pager | tokens + light/dark toggle (add a diagram if it has any flow) |
| Email HTML | tokens inlined; FORCE light mode (mail clients ignore the toggle) — see the email rule |

Verify (the same `preview_eval` structural inspection the report skill already runs): the artifact carries
zero hard-coded hex in the stage, re-skins on a `data-theme` swap, and survives a `data-mode=dark` toggle
with no overlap and no leaked build context.

## Cross-links

- The xlsx renderer of the same contract: `output-xlsx.md`.
- The slide-deck renderer: `output-slide-deck.md`.
- The full standard + the boilerplate fork: `<your-workspace>/shared/templates/_contract/EFFECTIVE-HTML-STANDARD.md`.
