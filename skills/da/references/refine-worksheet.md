# Refine Protocol - structured per-section report feedback

Turns the report-refine loop from long imprecise prompts into a per-section, user-chosen feedback flow. Externalizes content so a fresh session can resume (kills >400k context decay).

## When this fires (trigger)
- Keyword: the user says "gop y tung phan", "tao worksheet", "refine tung phan", or invokes refine explicitly.
- Rule: after 2-3 CONSECUTIVE rounds where the user's message is an output-fix on the same deliverable, OR a single feedback round listing 3+ distinct change points -> offer the menu. One or two small fixes stay on plain prompt (Tier 1).

## The menu (user picks per round)
1. **Prompt** - user types fixes in chat; Claude maps to anchor(s) and applies. For 1-2 small fixes.
2. **Worksheet** - run `scripts/refine/generate_worksheet.py <report>.html > <project>/refine/worksheet.txt` (add `--docx` for a Word table form). User fills the "SUA DOI / FEEDBACK" field per section; blank = section OK. Then `scripts/refine/parse_feedback.py <project>/refine/worksheet.txt` -> JSON of filled sections; Claude applies each feedback to that section's anchors and re-renders.
3. **Inline annotation** - `scripts/refine/wrap_annotation_harness.py <report>.html` -> open `<report>.annotate.html` in a browser -> select text and comment -> Export -> `comments.json`; then `scripts/refine/parse_comments.py comments.json` -> change-set -> Claude applies (same apply step as Tier 2) and re-renders a CLEAN report (the harness is only on the `.annotate.html`, never the final).

## Anchor system (shared backbone)
Every addressable unit in a forked template carries `data-bind="<dotted.path>"` (e.g. `f0.aum.takeaway`, `drivers[0].reading`). The dotted prefix (`f0.aum`, `drivers[0]`, `scqr`) is the SECTION; the full key is the ANCHOR. All tiers resolve to `{anchor -> change}` and feed one apply step.

## Apply flow
For each filled section in the parsed JSON: read `feedback`; if it rewrites prose -> replace the section's text anchor (`.takeaway`/`.reading`/`.note`); if it corrects a number -> set that numeric anchor; if it is an instruction ("doi thanh bang") -> apply structurally within the locked template. Sections with empty feedback are untouched (per-section sign-off). Re-render from {locked template + data + applied changes}.

## Fresh-session handoff (context-bloat fix)
`worksheet.txt` (or the parsed JSON) + the data + the locked template are a complete handoff. When context exceeds ~300-400k, start a NEW session: it reads only those artifacts, applies, re-renders - no conversation carryover. Each refine round runs on clean context.

## Honest-degrade
A number the user corrects changes the RENDERED report only; if it implies an upstream data/pipeline bug, flag it - do not silently edit the pipeline.
