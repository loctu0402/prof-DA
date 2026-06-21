# adapters/ - the portability layer (BUILT, v3.20.0)

The per-platform layer that carries prof-DA's mechanism (scripts + gates + references + rules) to
non-Claude agents WITHOUT flattening to plain markdown. See `../docs/portability-architecture.md` for
the 4-layer model. Everything here is a PLACEHOLDER this design pass (`[FILL]` / `[PORT FROM]` markers);
the functional mirrors are built later.

## The 4 layers (recap)

- L1 ENGINE - `skills/da/references/` + `skills/da/scripts/` carry verbatim to every platform (no adapter).
- L2 INVOCATION - per-platform trigger files: `.gemini/commands/`, `.github/`, `.cursor/rules/`, `commands/`.
- L3 GATE - `gate_core.py` (neutral core) + `gate.py` (`python -m gate <receipt>`), called by each platform's
  trigger (git pre-commit, CI step, Cursor alwaysApply rule, final tool call). This file's job.
- L4 TOOL-NAME MAP - `toolmaps/_toolmap.md` (Skill/Agent/Bash/Read/Edit/Write/TodoWrite per platform).

## To add a platform

1. Add an L2 invocation file (a command / rule / agent that loads `skills/da/references/mode-*.md`).
2. Wire the L3 gate at the best available trigger: `python -m gate <receipt>` (pre-commit / CI / final tool call).
3. Add the platform's column to `toolmaps/_toolmap.md` (L4).
4. L1 is already done (the engine is verbatim).

Author: Loc Tu (loc.tu@mservice.com.vn).
