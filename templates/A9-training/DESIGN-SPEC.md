# A9 Training Material — Design Spec

Archetype: pedagogical cheatsheet / teaching slides (single-scroll static HTML page).
Skeleton: `boilerplate.html` · Library: prof-DA report archetype library

---

## 0. Frame

**Job-to-be-done:** teach a concept or method so a learner can *do something* afterward.
This archetype is intentionally free of live data atoms (no metric snapshots, no verdict
ramps, no waterfall components). It teaches; it does not report.

**Inherited from the token contract:** all colors resolve via `var(--token)`. The `:root`
block in `boilerplate.html` is the sole swap surface — replace palette values there to
re-theme the whole file; keep token *names* unchanged so component CSS continues resolving.

**What this archetype does not include (hard — do not bolt on):**
- Metric headline blocks
- Verdict / deviation ramp tables
- Waterfall or dual-comparison KPI panels
- Sentiment scales
- Market-context or forecast components

---

## 1. Information Architecture

Five sections in order:

1. **Learning Objectives** (`§ 01`) — checklist of measurable outcomes; what the learner
   will be able to do, not topics they will have heard about.
2. **Core Concepts** (`§ 02`) — 2/3/4-up definition card grid; each card: term label +
   concept name + plain-language definition + one concrete example line.
3. **Worked Example** (`§ 03`) — numbered steps + a dark-background code block (the one
   dark surface); walks through the method end-to-end.
4. **Check Your Understanding** (`§ 04`) — practice question cards with `<details>` reveal;
   must be a *real* disclosure, not a dead toggle.
5. **Recap / Cheatsheet** (`§ 05`) — dense key-term grid; the one-screen handout takeaway.
   Optional chip strip above it for quick status legend.

---

## 2. Components

| Component | Class(es) | Notes |
|-----------|-----------|-------|
| Learning objectives box | `.objectives` | Left accent border; 2-col checklist; tick via `::before` |
| Concept card | `.concept` inside `.concept-grid` | Term label (uppercase, letter-spaced) + name + def + example |
| Worked example | `.worked` | `.step` rows with numbered index badge; see code block below |
| Code block | `.code` | **The one dark surface** — dark background, mono, minimal syntax spans |
| Check card | `.check` | `<details>` / `<summary>` reveal; accent color on summary label |
| Status chip | `.chip-x .cx-*` | Four states: success / warn / danger / neutral |
| Recap grid | `.recap` → `.rgrid` → `.ri` | Two-column key/value rows; mono key, body value |

All components use `var(--token)` exclusively. The code block background is set via
`--code-bg` / `--code-ink` defined in `:root` — not a hardcoded value.

---

## 3. Visual

- **Type:** system sans-serif stack (body), `ui-monospace` (code, labels, badges).
  Swap for a brand typeface by adding a `@font-face` or `<link>` and updating `body`
  and `.mono` font-family declarations.
- **Accent usage:** accent color (`var(--accent)`) on section index labels, objective
  tick marks, step index badges, check-card reveal labels, recap key labels, and
  the `.ph` placeholder underline. Restrained — not on headings or body text.
- **Section headings:** `var(--primary)` — visually quieter than accent.
- **One dark surface:** the code block only (`--code-bg` / `--code-ink`). Do not add
  additional dark surfaces.
- **Density:** tighter than a report archetype — cheatsheet convention. Uppercase
  letter-spaced micro-labels throughout.

---

## 4. Interaction

Static HTML. The only interactive element is the `<details>` / `<summary>` reveal in
check-understanding cards. No decorative motion, no metrics interactivity.

---

## 5. Placeholders

All variable content is wrapped in `<span class="ph" data-bind="key">[ key ]</span>`
(monospace keys) or `<span class="ph txt" data-bind="key">[ description ]</span>`
(prose). Renderers replace these by `data-bind` key. Never leave a bare "N/A" or empty
string — the placeholder style signals "unfilled" to reviewers.

---

## 6. Responsive and Print

| Breakpoint | Behavior |
|------------|----------|
| ≤ 900 px | Objectives list → 1 col; concept grid → 2 col; check grid → 1 col; recap → 1 col |
| ≤ 620 px | Concept grid → 1 col; lede font scales down |
| Print | White background enforced; color-adjust exact; cards set to `break-inside: avoid` |

Code blocks scroll horizontally on narrow viewports (`overflow-x: auto`).

---

## 7. Fork Checklist

- [ ] Swap `:root` token values to match your brand palette (keep token *names*)
- [ ] Replace all `<span class="ph">` / `<span class="ph txt">` content
- [ ] Update `data-bind` keys to match your renderer's data schema
- [ ] Add or remove `.concept` cards in `§ 02` (grid reflows automatically)
- [ ] Add or remove `.step` rows in `§ 03`
- [ ] Add or remove `.check` cards in `§ 04`
- [ ] Add or remove `.ri` rows in the recap grid (`§ 05`)
- [ ] Verify no hardcoded color values were introduced (all colors must be `var(--...)`)
- [ ] Verify no organization-specific names, paths, or locale-specific content remain

---

## 8. Review Log

- **Structure gates:** objectives + concept grid + worked example + check-understanding + recap present.
- **Token gate:** zero hardcoded color values; all colors via `var(--token)`.
- **Content gate:** zero real data; zero organization-specific names; zero locale-specific content; placeholders only.
- **Dark-surface gate:** exactly one dark surface (code block); no others.
- **Sign-off:** pending.
