# Recurring Report Contract — Section Template + Per-Section Definition-of-Done

> For **recurring, structured, often multi-author reports** (bi-weekly business review, monthly
> stakeholder update, weekly ops report) where the SAME section skeleton must be filled EVERY cycle
> and each section has an explicit "what a complete answer contains".
>
> This complements — does not replace — the one-shot deliverable flow. `narrative-template.md` gives
> the SCQR/Impact-Card *shape* of a single report; this file gives the *contract* that pins a
> recurring report's sections and grades each section against its own definition-of-done (DoD).
>
> Engine-agnostic. No server, no dependency. Pattern distilled from a periodic-report MCP tool
> (versioned guidance + per-section `quality_check` + carry-forward follow-ups), ported offline.

## When to use this (and when NOT)

| Use the contract | Skip it (use plain report flow) |
|------------------|--------------------------------|
| Same report ships every cycle (weekly/bi-weekly/monthly) | One-off ad-hoc analysis |
| Multiple contributors fill different sections | Single author, single narrative |
| A reviewer expects fixed sections each time | Free-form exploratory write-up |
| You keep re-explaining "what goes in section X" | Section content obvious from the question |

If it's a one-shot report, this is over-engineering — stop here and use `mode-report.md`.

## The three patterns ported

### 1. Section Contract = versioned section template with DoD

A recurring report is a **fixed list of sections**, each carrying its own **definition-of-done**:
the enumerated `(1)(2)(3)` parts a complete submission must contain. The DoD text doubles as the
**validation rubric** — both the author's checklist and the auditor's gate.

This is the planning artifact. It belongs with the **Metric Contract** (`planning-protocol.md`
Gate 2): the Metric Contract pins *what numbers mean*; the Section Contract pins *what the report
must say, section by section*. Lock it once; reuse it every cycle; version it when the report's
shape changes (bump `version`, keep the old one for audit).

Contract format (`<project>/report-contract.json`):
```json
{
  "report": "<product> Bi-weekly Business Review",
  "cadence": "bi-weekly",
  "version": 3,
  "sections": [
    {
      "key": "business_overview",
      "title": "Business Overview",
      "required": true,
      "dod": ["AUM actual vs target", "MFU actual vs target", "projection to end of month"]
    },
    {
      "key": "segment_a_contribution",
      "title": "AUM Contribution from MFU",
      "required": true,
      "dod": [
        "current AUM from MFU",
        "AUM trend over recent cycles",
        "cash-in and cash-out behavior",
        "explanation of significant fluctuations",
        "actions: done, in progress, planned"
      ]
    }
  ],
  "carry_forward": [
    {"section_key": "new_initiatives", "note": "Resolve onboarding blocker raised last cycle"}
  ]
}
```

Authoring rule: write each `dod` item as a **concrete deliverable**, not a vague topic — `"AUM trend
over recent cycles"` not `"trends"`. The items become the per-section gate; vague items can't be
checked. A common recurring shape for a metric-contribution section is the 5-part ladder:
**current value → trend → vs target → driver/fluctuation (the why) → actions (done/in-progress/planned)**.

### 2. quality_check = per-section self-validation gate

Before a section ships, the author must answer, **for each DoD item, how the content satisfies it**.
Not "is there an orientation block" (that is the global `rubric_audit.py` job) but "does *this*
section contain *its* required parts". This is the gap the global validators don't cover: they grade
the report's universal shape, not each section against its bespoke contract.

`section_contract_audit.py` runs the mechanical half (section present, non-empty, no placeholder,
DoD keyword heuristic) and emits a **quality_check worksheet** for the judgment half (the author
writes one line per DoD item justifying coverage). Mechanical findings catch the obvious misses;
the worksheet forces the author to self-certify the rest — same discipline as the source tool's
required `quality_check`, offline.

### 3. Carry-forward follow-ups = open items survive the cycle

Action items raised in one cycle's review are **section-scoped** and **carried forward** until
resolved — they re-surface in the next cycle's report under the same section, so nothing silently
drops. This is a *discipline to document in the contract*, not a system to build: keep open items in
`report-contract.json → carry_forward[]`; the audit re-lists any open item whose section still
exists, so the next cycle's author sees "still open from last cycle" and must address or re-defer it.

> Do NOT build cycle/member/auth machinery in the plugin. The contract file + the audit script are
> the whole port. Cadence, deadlines, and "who submitted" are the stakeholder's tracker's job, not
> the analyst workflow's.

## Workflow

1. **Define once (frame mode).** Draft `report-contract.json` alongside the Metric Contract in
   `PLANNING.md`. Confirm sections + DoD with the stakeholder. Version it.
2. **Fill each cycle (report mode).** Populate the report against the contract; every required
   section, every DoD item.
3. **Gate before ship (report mode self-check).** Run the audit; fix missing/empty sections; fill
   the quality_check worksheet; address carry-forward items.
4. **Carry forward (close of cycle).** Move unresolved review notes into `carry_forward[]` for the
   next cycle.

```bash
# Mechanical gate: every required section present, non-empty, no placeholder, DoD parts evident
python scripts/validators/section_contract_audit.py output/report.md --contract report-contract.json

# Print the per-section quality_check worksheet to fill (judgment half)
python scripts/validators/section_contract_audit.py output/report.md --contract report-contract.json --worksheet
```

Pairs with the standard pre-ship chain (`self_check.py`, `rubric_audit.py`) — the contract audit is
the **per-section** layer; the others are the **global** layer. Run both.

## Cross-references
- Planning home (Metric Contract sits beside the Section Contract): `planning-protocol.md` Gate 2
- One-shot report shape (SCQR / Impact Cards): `narrative-template.md`
- Global pre-ship gates: `report-standard-checklist.md`, `self-check-protocol.md`
- The audit script: `scripts-guide.md` → `section_contract_audit.py`

— part of prof-DA · Loc Tu, 2026
