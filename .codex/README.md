# prof-DA on Codex / OpenAI

Codex reads `AGENTS.md` at the repo root as its standing contract - that IS the prof-DA router for Codex
(intent -> mode -> load `skills/da/references/mode-*.md`; the gate contract; the non-negotiables). No
per-mode files are needed here; this note records the wiring.

- Intent -> mode: frame (scope / metric / kickoff) | model (schema / dbt / mart) | query (pull data / SQL / breakdown / trend) | process (EDA / clean / features / forecast / ML) | insight (why X / root cause) | automate (schedule / pipeline / backfill) | report (stakeholder report / dashboard / slide) | deliver (autonomous build: 1 task = 1 commit + verify gate) | submit (finalize a recurring report) | review (audit / is-it-good) | fix (broken pipeline / wrong number) | workspace (scaffold / index)  (full contract: `../AGENTS.md`).
- Engine (Layer 1) verbatim: `skills/da/references/` + `skills/da/scripts/` (stats only via a script).
- Tool names: `../adapters/toolmaps/_toolmap.md` (Codex / OpenAI column: apply_patch for edits, shell for
  reads/bash, update_plan for the task plan).
- Gate (Layer 3): Codex has no turn Stop hook, so run the gate at the final tool call OR as a git
  pre-commit (`../adapters/git/pre-commit`):  python adapters/gate.py .prof-da/pending-validation.json
  exit 0 = deliverables proven + requirements reconciled; nonzero = not done.
- Maintain the requirement ledger yourself (Codex has no UserPromptSubmit hook): capture each ask as
  OPEN in `~/.claude/req-recon/<project-key>.md`; the gate enforces it at commit (see `../docs/governance.md`).
