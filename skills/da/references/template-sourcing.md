# Template Sourcing & Read-Classification (binding)

> The forcing-function behind fork-or-fail. It makes report / build modes fork a report's STRUCTURE from a
> locked template only, and draws the hard line between reading a project for FACTS (allowed) and inheriting a
> project's PROCESS / FORMAT (forbidden). Without this rule an agent reconstructs a report by reading an old
> project's `generate_*.py`, re-importing that project's ad-hoc style drift while calling it "reading for
> knowledge". This file names the boundary so that excuse becomes falsifiable.

## 1. The locked template is the ONLY source of report structure

A report's layout / sections / CSS / build sequence come from a LOCKED template — never invented per-report,
never copied from another project's output. Resolve the fork source in this precedence order:

1. **Workspace override** — `<your-workspace>/shared/templates/<A>/` when the user's workspace ships an
   org-branded locked library. Org branding wins when it exists.
2. **Plugin default** — `${CLAUDE_PLUGIN_ROOT}/templates/<A>/` — the bundled org-neutral archetype set, ALWAYS
   present (catalog `templates/README.md`, DNA `templates/_contract/THEME-TOKEN-CONTRACT.html`). Fork this when
   the workspace has no library, then re-theme by swapping the `:root` tokens.
3. **Neither fits** — STOP. Register a NEW locked template (fork-or-fail path (c)): build it 1:1 against a
   `DESIGN-SPEC.md`, add it to the catalog, THEN fork. Never freestyle; never clone a project's generated report
   as the template.

Resolution rule: to fork archetype `A2`, look for `shared/templates/A2-*` first; if absent, use
`${CLAUDE_PLUGIN_ROOT}/templates/A2-*`. The Decision Tree in `mode-report.md` names archetype IDs; those IDs
resolve through THIS precedence, not a hard `shared/templates/` path.

Why (Causal): the whole point of a locked library is that every report reads like the same analyst made it. A
report whose structure is sourced ad-hoc — freestyled OR lifted from a one-off project — re-introduces the
per-report style drift the library exists to kill.

## 2. Read-Classification: FACT (allowed) vs PROCESS (forbidden)

report / frame / deliver / fix modes routinely read an existing `projects/<x>/` dir or a live pipeline. Every
such read is one of two kinds — classify it BEFORE you open the file:

| Kind | What you read it for | Verdict |
|------|----------------------|---------|
| **FACT** | metric definition, column / schema, where the data lives, a cached number, a domain edge-case, a business rule | ALLOWED — this is grounding. Read freely. |
| **PROCESS** | a project's `generate_*.py` / report generator, its HTML layout, its CSS, its section order — read to reconstruct or copy the report's FORMAT or build sequence | FORBIDDEN as a source. Structure comes from the locked template (§1), not another project's ad-hoc output. |

**Falsifiability clause.** If you open a file under `projects/` (or any existing generator) during a build,
state in one line which it is: `FACT read: <what fact>` or `PROCESS read: <what>`. A PROCESS read taken to
source the report's shape is a DEFECT — the same class of failure as freestyling a bespoke visual. "I was
reading it for knowledge" only holds when the knowledge is a FACT (domain / data); it is never a valid cover
for lifting the process or format.

Why (Causal): an old project's generator is un-templated, often built ad-hoc before the template standard
existed, and may have drifted. Inheriting its process re-imports exactly the non-standard structure §1 forbids —
and the "reading for knowledge" framing keeps the leak invisible unless the FACT/PROCESS line is drawn out loud.

## 3. Where this binds

- `mode-report.md` Step 2 (fork-or-fail): the "closest real template" you reuse MUST be a LOCKED template
  (workspace override or bundled default), NEVER a project's generated report or its generator.
- `mode-report.md` Step 3 (Wire Data): reading a project's cache / pipeline is a FACT read (load the numbers);
  it is not a licence to lift the generator's layout.
- `mode-frame.md` / `recurring-report-blueprint.md`: "reproduce an existing report" means reproduce its DATA +
  INTENT through the template system — trace the old pipeline for FACTS (metrics, sources), then build the new
  report from a locked template. It does NOT mean fork the old generator.
- `build-auto.md`: a build task that sources report structure from a project generator fails the verify gate.
- `report-standard-checklist.md`: the `[GATE]` Brand-fidelity check (locked template required) also requires the
  template to resolve through §1 precedence, with no PROCESS read feeding the structure.

Why this rule exists (meta): the plugin already SHIPS the template library and the fork-or-fail rule, yet the
reported failure still happened — the agent walked past the bundled templates into a project's generator and
framed it as grounding. The missing piece was never more templates; it was the explicit boundary + precedence
that makes "which template" unambiguous and "reading the old generator for the format" a nameable defect.
