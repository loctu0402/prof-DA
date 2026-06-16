# Tool-name map (Layer 4) - DESIGN reference

Maps prof-DA's tool vocabulary to each platform's tool names, so a mode reference that says "use Edit,
not Write" or "spawn an Agent" translates. `[FILL]` = confirm the exact name from that platform's docs
when building the mirror.

| prof-DA tool | Claude Code | Codex / OpenAI | GitHub Copilot | Cursor | Gemini CLI | OpenCode |
|--------------|-------------|----------------|----------------|--------|-----------|----------|
| Skill | Skill | (prompt include) | agent file | rule include | command | skill tool |
| Agent (subagent) | Task / Agent | sub-agent prompt | `@agent` file | composer agent | sub-agent | agent |
| Bash | Bash | shell | terminal | terminal | shell | bash |
| Read | Read | read_file `[FILL]` | read | read | read_file `[FILL]` | read |
| Edit | Edit | apply_patch `[FILL]` | edit | edit | edit | edit |
| Write | Write | create_file `[FILL]` | create | create | write_file `[FILL]` | write |
| TodoWrite | TodoWrite | (plan) | (issue) | (todo) | (plan) | todo |

When building a platform mirror, split this into `toolmaps/<platform>-tools.md` (one column each) if the
mode references need a per-platform include.
