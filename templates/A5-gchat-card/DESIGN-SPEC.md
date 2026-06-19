# A5 — Google Chat Card · Design Spec

Channel: Google Chat `cardsV2` JSON (not HTML, not email).
Skeleton: `card.json`

---

## 0. When to Use

Use A5 when the delivery channel is a Google Chat space and the job is a short KPI digest: headline metrics + verdict, linking out to a full report or portal. Not suitable for rich visuals, tables, or long narrative — those belong in an HTML or email archetype.

---

## 1. Structure

One `cardsV2` entry. Sections in order:

1. **Card header** — title (product name + period label) + subtitle (date + generation time) + optional icon.
2. **Section: Summary** — 2–4 `decoratedText` widgets for the most important metrics; each carries a verdict inline.
3. **Section: Key Metrics** — up to 6 additional `decoratedText` rows. Keep section total at or below 10 widgets.
4. **Section: Legend** — one `textParagraph` listing all verdict tiers. Mandatory; never omit.
5. **Section: CTA** — a `buttonList` with a single button linking to the full report.

Widget limit: **10 widgets per section maximum** (Google Chat platform constraint).

---

## 2. Verdict Vocabulary

Verdicts are driven by a z-score or a robust deviation band, not a raw percentage gap.

| Verdict     | Signal                          | Inline label         |
|-------------|----------------------------------|----------------------|
| `normal`    | within the usual range (|z| < 1) | `✓ normal`           |
| `watch`     | mild deviation (1 ≤ |z| < 2)    | `⚠ watch`            |
| `attention` | notable deviation (2 ≤ |z| < 3) | `⚠ attention`        |
| `abnormal`  | strong deviation (|z| ≥ 3)      | `🚨 abnormal`        |

The legend section at the bottom must reproduce this table in plain text so the card is self-documenting.

Inline color codes are desaturated status tones (neutral gray, muted amber, muted red). Use sparingly via `<font color="#…">` — the only HTML that Chat text widgets support alongside `<b>` and `\n`.

---

## 3. Text Widget Constraints

Google Chat renders only three markup constructs inside `text` / `textParagraph` fields:

- `<b>…</b>` — bold
- `<font color="#rrggbb">…</font>` — inline color
- `\n` — line break

No tables, no images, no full HTML. Avoid constructing prose in text widgets; keep each widget to a single metric line.

---

## 4. Fork Rules

1. Copy `card.json` into the target report's output folder.
2. Replace every `[ placeholder ]` value with renderer-supplied runtime values. Never leave a literal placeholder in a sent card.
3. Remove sections not needed (e.g., drop the Key Metrics section for a one-metric digest). The Legend and CTA sections are non-negotiable.
4. Keep each section under 10 widgets. If more metrics are needed, add a section rather than exceeding the limit.
5. The `cardId` field must be unique per integration; set it to a stable identifier for the report.
6. Do not embed images in `decoratedText` icon fields using proprietary or brand asset URLs. Use `knownIcon` enum values or a publicly accessible generic icon URL.

---

## 5. Success Criteria

- Valid `cardsV2` JSON (passes schema validation).
- Legend section present and lists all four verdict tiers.
- Every section has 10 or fewer widgets.
- All metric values are runtime-supplied (no hardcoded numbers).
- CTA button links to a reachable report URL.
- Verdict labels in metric rows match the Legend section exactly.
