# A4 Daily Email — DESIGN SPEC

> Archetype: A4 · Channel: Email HTML body · Constraint: email-safe (no CSS vars, no JS, table layout, inline styles)
> Skeleton: `boilerplate.html` · Contract: `../_contract/THEME-TOKEN-CONTRACT.html`
> Library version: v1.0 · Org-neutral

A compact daily snapshot email that delivers the day's headline KPIs and verdict to a stakeholder's inbox in a 30-second skim. Links out to a portal for depth. The email-safe channel is the defining constraint: every styling decision derives from it.

---

## 0. When to Use

Use A4 when:
- The delivery channel is **email** (Gmail, Outlook, Apple Mail).
- The audience needs a **daily cadence** summary — one date, one verdict, 2–4 KPIs.
- The report is a **gateway**: the email carries the headline, the portal carries the depth.
- The reader skims on mobile (dark mode possible) and decides in 30 seconds whether to drill in.

Do **not** use A4 when:
- The audience needs interactive filtering or drill-down (use A2 Ops Dashboard).
- The report is weekly/monthly with long narrative (use A3 Editorial Paper).
- The context is a web page or internal portal (CSS variables work there — no need for this archetype's inline overhead).

---

## 1. Email-Safe Constraints (hard rules)

| Constraint | Rule |
|---|---|
| **No CSS variables** | Email clients strip `var(--token)`. Inline hex values directly on every element. |
| **No `<style>` layout** | Gmail and Outlook strip `<style>` blocks for layout. Use `<style>` only for the force-light 3-layer override (dark-mode reset, `@media` query). All layout and color = inline `style=""`. |
| **Table-based layout** | Every layout region is a `<table role="presentation">` with `cellpadding="0" cellspacing="0" border="0"`. No CSS grid, no flexbox. |
| **No JavaScript** | Email clients strip all scripts. No interactivity, no hover reveals, no motion. |
| **Charts as `<img>`** | Use `src="[ chart-image-url-or-cid ]"`. Preferred: base64 `data:image/png;base64,...` (self-contained) or CID reference (`cid:chartname.png`) for MIME multipart. No external URLs — clients block them. 1–2 images max. |
| **Force-light 3-layer** | Three coexisting overrides in `<head><style>`: (1) `:root` color-scheme declaration, (2) `[data-ogsc]/[data-ogsb]` Outlook dark-mode hack, (3) `@media (prefers-color-scheme: dark)` reset for Apple Mail / Gmail mobile. |
| **Web-safe fonts** | `'Segoe UI', Arial, Helvetica, sans-serif`. No web fonts — clients block external font loads. |
| **Max 80 KB total** | Gmail clips emails above ~102 KB. Keep the full rendered email (HTML + base64 image) under 80 KB. Size the chart PNG at @2x then constrain with `width` attribute, and compress before embedding. |
| **Mobile CTA** | CTA button minimum 44px tall (`padding:13px 28px`). Use bulletproof table-wrapped `<a>` pattern. |

---

## 2. Palette (inline, no variables)

Derived from the neutral slate `:root` in `../_contract/THEME-TOKEN-CONTRACT.html`.
These are the only hex values that belong in this archetype. Do **not** add brand-specific colors at fork time without updating the contract first.

| Role | Hex |
|---|---|
| Page background | `#f4f5f7` |
| Card / surface | `#ffffff` |
| Surface alt (soft rows, intro band) | `#f7f8fa` |
| Ink (primary text) | `#1d2126` |
| Ink-2 (body, secondary text) | `#434a52` |
| Ink-3 (labels, muted) | `#79818b` |
| Ink-4 (very muted, footer) | `#a6adb6` |
| Border | `#e2e5e9` |
| Border strong | `#cdd2d8` |
| Primary (accent dot, CTA, verdict stripe) | `#3a5a78` |
| Accent (links, insight lead) | `#2f6f8f` |
| Success fg / bg | `#2e6442` / `#dbe5dc` |
| Warn fg / bg | `#9a6a1a` / `#efe6cb` |
| Danger fg / bg | `#a8362c` / `#f0dad5` |
| Neutral fg / bg | `#74706a` / `#e7e3db` |

---

## 3. Section Order (Information Architecture)

Single 720px-max centered `<table>` column. Fixed top-to-bottom order:

| # | Section | Purpose |
|---|---|---|
| 1 | **Header** | Product name + accent dot + report date + "T−1 snapshot" subline. |
| 2 | **3-line intro** | Orientation sentence: embeds the primary KPI value + delta + the "what's driving it?" question. |
| 3 | **NSM strip** | 2 headline metrics side-by-side, each with a verdict pill (success / warn / danger / neutral). Top border color signals severity. |
| 4 | **KPI strip** | 3–4 secondary KPIs in a row; each cell shows value + DoD delta + vs-7d delta with directional color. |
| 5 | **Breakdown table** | Channel or segment rows; columns: segment, value, DoD, vs-7d, status pill. |
| 6 | **Chart block** | One `<img>` placeholder (base64 or CID). Renderer replaces the placeholder `<table>` block. One-line insight caption above the image. |
| 7 | **Verdict summary + takeaways** | One bold verdict sentence + 2 bullet takeaways, in a left-bordered box. |
| 8 | **CTA button** | Bulletproof table-wrapped link to the full portal report. |
| 9 | **Footer** | Run timestamp + system name + methodology link + unsubscribe link. |

**Reading path:** Header → NSM strip → Verdict summary covers the 30-second skim. CTA carries the reader to depth.

---

## 4. Fork Rules

1. **Copy `boilerplate.html` 1:1** into your project — never edit the archetype skeleton directly.
2. **Replace every `[ placeholder-key ]`** with renderer output or static text. No placeholder should survive into a production send.
3. **Palette**: use the slate hex values in Section 2 as-is, or swap them for your organization's brand tokens — but swap consistently (find-replace the hex, do not mix palettes). Update the comment block at the top of `<style>` to document the active palette.
4. **Force-light 3-layer** in `<head><style>`: keep all three layers. If you change the page/card/CTA hex values, update the corresponding hex in all three layers.
5. **Chart slot**: replace the placeholder `<table>` block (the dashed-border slot) with a real `<img>` tag. Keep `style="display:block;border:0;max-width:100%;height:auto"` on the `<img>` for mobile scaling.
6. **Segment rows**: add or remove breakdown table rows to match your data. Keep the column order (segment | value | DoD | vs-7d | status pill) for consistency.
7. **Verdict pills**: use the four semantic combinations only — success (`#2e6442`/`#dbe5dc`), warn (`#9a6a1a`/`#efe6cb`), danger (`#a8362c`/`#f0dad5`), neutral (`#74706a`/`#e7e3db`). Do not invent new severity colors.
8. **Size check**: before sending, verify the rendered HTML (with base64 image) is under 80 KB.

---

## 5. Components Not Present in A4

The following archetype atoms are explicitly excluded from the email channel:

- 6-layer diagnostic block (too heavy for email)
- Plotly / interactive charts (clients strip JS)
- Hover reveal / tooltips (no JS, no CSS `:hover` in email)
- Sidebar layout (single column only)
- Web fonts (clients block external font loads)
- CSS custom properties / `var()` (clients strip them)
- `<style>` layout rules (clients strip them; layout is table + inline only)
