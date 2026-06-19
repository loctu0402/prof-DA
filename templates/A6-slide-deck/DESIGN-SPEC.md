# A6 Slide Deck — DESIGN SPEC (IA reference · spec-only)

> This file defines the slide information architecture (IA) for the A6 archetype.
> A6 is **spec-only**: it pins the IA contract, slide order, and narrative rules.
> The forkable, production-ready skeleton lives in **A12 Slide Deck** — fork A12 when
> you need a built slide deck, not A6.

---

## 0. When to use A6 / A12 (vs. a portal report)

| Situation | Pick |
|-----------|------|
| Live presenter-led session; audience follows one argument in real time | A12 (built form of A6) |
| Editable PPTX handoff after the session | A12 (exports to PPTX) |
| Projecting an A1–A11 portal finding to an exec audience | A12 |
| Async stakeholder read; audience self-navigates | A1 / A3 / A7 (portal report) |
| Defining or auditing the IA contract without building a deck | A6 (this spec) |

**Key distinction:** a slide deck is a presenter's script made visual — one message per
slide, live-paced. A portal report is a self-service artifact — dense, scannable,
anchored by a table of contents. Never compress a portal into slides or expand slides
into a portal; they serve different modes of consumption.

---

## 1. Slide Order (Information Architecture)

| # | Slide type | Purpose |
|---|-----------|---------|
| 1 | **Title** | Deck title as a thesis sentence (not a topic label) + presenter name + date. The thesis sentence is the single claim the deck proves. |
| 2 | **Agenda** | 3–5 sections, each phrased as the question this section answers. Not a topic list. |
| — | **Section divider** | One per section. Contains the section's one-line claim + section index. Accent color + muted background. No data on this slide. |
| N | **Content slides** | One message per slide (see §2). The bulk of the deck. |
| — | **Summary / ask** | Restates the thesis. Closes with an explicit decision or call-to-action. No new data. |
| — | **Appendix** | Methodology detail, backup tables, caveats. The only place technical jargon is permitted. Does not appear during the live presentation; available on request. |

**Horizontal-logic rule:** read only the slide titles, in order. They must tell the
complete argument without any body content. If the title sequence does not form a
coherent storyline, the IA is broken.

---

## 2. One-Idea-Per-Slide Rule

Each content slide carries exactly one message. Violations:

- Two charts on a single slide → split into two slides.
- A title that is a topic label ("Revenue") rather than a claim ("Revenue grew 8% WoW,
  exceeding the four-week average") → rewrite the title.
- A "dashboard slide" with a KPI grid → move to a portal report or appendix; it belongs
  in a self-service artifact, not a live deck.

The test: cover the body area. The slide title alone must be a complete, falsifiable
statement. If it reads as a label or heading, it fails.

---

## 3. Title / Body / Takeaway Pattern

Every content slide follows this three-layer structure:

```
┌─────────────────────────────────────────────────────┐
│  TITLE  —  the takeaway sentence (action title)     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  BODY  —  the single proof element                 │
│           (chart · diagram · table · quote)         │
│                                                     │
├─────────────────────────────────────────────────────┤
│  TAKEAWAY LINE  —  one sentence; "So what?"         │
└─────────────────────────────────────────────────────┘
```

- **Title (action title):** a complete declarative sentence stating the insight. Verb
  required. Written for the audience, not the analyst ("Cost per acquisition dropped 22%
  after the channel mix shift" not "CPA by channel").
- **Body:** one proof element only. Chart selection follows the design system's
  chart-choice matrix (defined in `_contract/`). No multi-chart grids.
- **Takeaway line:** explicitly answers "so what?" in one sentence. Bridges from the
  evidence to the recommendation or the next slide's question. Label it visually as
  distinct from the body (lighter weight, subtle background, or footnote zone).

---

## 4. Narrative Arc

The full deck must follow the Situation → Complication → Question → Answer (SCQA)
structure, which maps to the slide order as:

| Arc stage | Slide(s) |
|-----------|---------|
| **Situation** — shared context the audience already accepts | Opening content slides (section 1). Establish common ground fast; do not over-explain. |
| **Complication** — the tension, gap, or change that makes action necessary | Middle content slides. This is where data lands. Each slide surfaces one piece of evidence. |
| **Insight / recommendation** — what the data implies; the answer | Final content slides before the summary. One insight per slide. |
| **Ask** | Summary / ask slide. The single explicit call-to-action. |

The agenda slide should foreshadow this arc. Each section divider's claim should be
readable as a step in the argument.

A simpler arc is acceptable for short decks (fewer than 8 content slides):

```
Situation → Insight → Recommendation
```

Do not use a flat "topic 1 / topic 2 / topic 3" agenda if the deck is making an
argument. A topic-list agenda signals a report being read aloud, not a deck.

---

## 5. What A12 adds (the built form)

A12 provides the production skeleton:

- Fixed-canvas slide stage with viewport scaling (`deck-stage.js`).
- Theme tokens wired to the design system's token contract (`_contract/`).
- Theme-swap mechanism: replace one `@import` in `theme.css` to switch the palette.
- PPTX export path.
- Slide shell components: action-title zone, body zone, takeaway-line zone, section
  divider shell, appendix shell.

Fork A12, not A6. A6 only pins the IA rules above. Modifying A6 is an IA governance
action (update the rules); building a deck is always done via A12.

---

## 6. Review checklist

Before presenting or handing off an A12 deck built against this IA:

- [ ] Titles read in sequence tell the complete argument (horizontal-logic test).
- [ ] Every content slide has exactly one proof element in the body zone.
- [ ] Every content slide has a takeaway line.
- [ ] The deck ends with an explicit ask or decision, not a data slide.
- [ ] Appendix slides are excluded from the live presentation flow.
- [ ] The agenda slide phrases each section as a question, not a topic.

---

## 7. Spec status

- **Type:** IA reference · spec-only (no skeleton files in this folder).
- **Built form:** A12 (`shared/templates/A12-slide-deck/`).
- **Governed by:** design system contract at `shared/templates/_contract/`.
- **Sign-off:** pending.
