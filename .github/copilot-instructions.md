<!-- DESIGN PLACEHOLDER - GitHub Copilot invocation adapter (Layer 2). Build deferred. -->
# prof-DA (GitHub Copilot)

[FILL when building] Copilot reads this file as repo custom instructions. Mirror the universal contract:

- Intent -> mode mapping: see `AGENTS.md` (frame / model / query / process / insight / automate / report /
  deliver / submit / review / fix / workspace). Load the matching `skills/da/references/mode-*.md` before acting.
- Engine (Layer 1) is verbatim: use `skills/da/references/` + run `skills/da/scripts/` (statistics always in a
  vetted script, never inline).
- Gate (Layer 3): before declaring a deliverable done, the evidence gate runs in CI - see
  `.github/workflows/gate.yml`. Locally run `python -m gate <project>/.prof-da/pending-validation.json`.
- Per-mode agents: `.github/agents/<mode>.agent.md` (must use the `.agent.md` suffix; invoke via `@<mode>`).
- Tool names: `adapters/toolmaps/_toolmap.md` (Copilot column).
