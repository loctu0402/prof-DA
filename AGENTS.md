# AGENTS.md - prof-DA orchestration contract

Guidance for ANY AI coding/analyst agent (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI,
Antigravity, OpenCode) working with this repository. The platform-specific invocation lives in each
platform's own directory (see `docs/portability-architecture.md`); THIS file is the universal contract
every platform reads.

## What prof-DA is

A data-analyst + analytics-engineer harness: 12 routable modes over one engine (references + scripts +
validator gates + rules). The mode CONTENT (`skills/da/references/`, `skills/da/scripts/`) is
platform-agnostic and carried verbatim everywhere; only the invocation + the gate TRIGGER are per-platform.

## Three composable layers

- SKILLS (`skills/<mode>/SKILL.md` -> `skills/da/references/mode-*.md`) - the workflows. The HOW.
- SCRIPTS + VALIDATORS (`skills/da/scripts/`) - executable logic + gates that block. Statistics ALWAYS
  run in a vetted script, never guessed inline.
- COMMANDS / INVOCATION (per platform) - the entry points. The WHEN.

The user (or a slash command) is the orchestrator. Do not build a router persona that calls other
personas. Keep delegation flat (depth 1): a spawned subagent gets READ + one narrow task and returns a
structured result; the parent integrates, QCs, and is the only writer of shared state / outward effects.

## Intent -> mode mapping (universal, same on every platform)

```
scope a vague ask / metric / kickoff        -> frame
design schema / mart / dbt / DWH            -> model
pull data / breakdown / trend / NL-to-SQL   -> query
EDA / clean / features / forecast / ML      -> process
why X / root cause / diagnostic             -> insight
schedule / pipeline / fail-alert / backfill -> automate
stakeholder report / dashboard / slide      -> report
build it autonomously, chunk + commit       -> deliver   (wraps a build mode with the 7-gate loop)
finalize + submit a recurring report        -> submit
audit / review / "is it good"               -> review
broken pipeline / wrong number              -> fix
organize / scaffold / index the workspace   -> workspace
```

Read the matching `skills/da/references/mode-*.md` (and `build-auto.md` for deliver) before acting. If a
task spans modes, read all relevant references first.

## The gate contract (mechanism parity)

Before declaring ANY deliverable done, prove it. The portable gate is:

```
python -m gate <project>/.prof-da/pending-validation.json     # or: python adapters/gate.py <receipt>
```

It checks each named deliverable EXISTS, is NON-EMPTY, and (for code) carries a proof marker; exit 0 =
proven, nonzero = not done. On Claude Code this runs automatically as a Stop hook; on every other
platform run it as a git pre-commit / a CI step / the final tool call (see `docs/portability-architecture.md`).
A task is not done until this passes (the evidence ladder: `skills/da/references/evidence-based-done.md`).

## Non-negotiable behaviors

- Verify, don't assume; surface assumptions; push back on a flawed plan; touch only what the ask traces
  to (`skills/da/references/execution-discipline.md`).
- Fork a locked template for reports; never freestyle.
- Never auto-send / publish a stakeholder deliverable; emit + hand to the user.
- Full English for agent-read docs; Vietnamese with diacritics for stakeholder output only.

## Per-platform setup

See `docs/portability-architecture.md` (the 4-layer model + the per-platform checklist matrix) and the
`adapters/` directory. The per-platform invocation files (`.gemini/`, `.github/`, `.cursor/`, `commands/`)
are placeholders in this design pass and are built later.
