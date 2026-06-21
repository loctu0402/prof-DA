# Tool-name map (Layer 4)

Maps prof-DA's tool vocabulary to each platform's tool names so a mode reference that says "use Edit,
not Write" or "spawn an Agent" translates. Confident names are filled; a `~` marks a name to confirm
against that platform's current docs when wiring (the platform's own tooling is the source of truth).

| prof-DA tool | Claude Code | Codex / OpenAI | GitHub Copilot | Cursor | Gemini CLI |
|--------------|-------------|----------------|----------------|--------|-----------|
| Skill (mode) | Skill | AGENTS.md routing (prompt) | copilot-instructions routing | .cursor/rules routing | /prof-da command |
| Agent (subagent) | Task / Agent | sequential prompt (no native subagent) | `@agent` file | composer agent | sub-agent ~ |
| Bash / shell | Bash | shell | terminal | terminal | run_shell_command |
| Read | Read | shell (`cat`/`sed`) | read | read | read_file |
| Edit | Edit | apply_patch | edit (str-replace) ~ | edit | replace |
| Write | Write | apply_patch (add) | create | create | write_file |
| Plan / todo | TodoWrite | update_plan | (issue/checklist) | (todo) | (plan) ~ |

The Layer-1 engine (`skills/da/references/`, `skills/da/scripts/`) is platform-neutral and carried
verbatim; only the invocation surface and these tool names differ per platform.
