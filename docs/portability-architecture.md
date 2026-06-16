# prof-DA Portability Architecture (mechanism-parity across agent platforms)

> DESIGN doc + a placeholder scaffold. How to carry prof-DA's mechanism (scripts + validator GATES +
> the references library + rules) to Claude Code, Codex, GitHub Copilot, Cursor, Gemini CLI,
> Antigravity, and OpenCode WITHOUT flattening the skill to plain markdown. This session ships the
> design + a placeholder tree; the functional per-platform mirrors are built later. Self-contained.

## What this IS / is NOT

- IS: a 4-layer model + a concrete scaffold (with `[FILL]` / `[PORT FROM]` placeholders) so the
  per-platform mirrors can be generated next session, preserving mechanism parity.
- IS NOT: a build. Nothing here is wired or released. `adapters/gate_core.py` and `adapters/gate.py`
  are marked stubs; the `.gemini/`, `.github/`, `.cursor/` files are placeholders.

## The mechanism-parity requirement (binding)

A skill is NOT just markdown. prof-DA carries: a references library (~48 docs), 19 stdlib scripts
(stats / causal / format / validators), validator GATES that block (exit 2), a receipt-driven Stop hook,
and rules. The portability requirement is that ALL of these run on every platform, identically. Plain
markdown-only ports (Addy's baseline) are REJECTED for prof-DA: they would drop the scripts, the gates,
and the hook, which are most of the value.

## Prior art (addyosmani/agent-skills)

Addy proved the split: skill CONTENT is platform-agnostic markdown in `skills/<name>/`, while the
INVOCATION layer is mirrored per platform (`.claude/commands/`, `.gemini/commands/`, `commands/` for
Antigravity, `.github/copilot-instructions.md` + `.github/agents/*.agent.md`, `.cursor/rules/`, the
OpenCode skill tool) plus a universal `AGENTS.md` orchestration contract; the intent->skill mapping is
universal. prof-DA extends this with two layers Addy does not need (the GATE adapter and the TOOL-NAME
map), because prof-DA's skills carry executable gates and tool-specific instructions.

## The 4-Layer Portability Model

### Layer 1 - ENGINE (portable verbatim, zero change)

Carried byte-identical to every platform: `skills/da/references/` (all docs) + `skills/da/scripts/`
(all stats / causal / format / validators - pure Python stdlib, no platform API) + the rule docs. A
reference is markdown; a validator is `python script.py <file> -> exit code`. Both are already
platform-neutral. This is most of the plugin and most of the value, and it is FREE on every platform.

### Layer 2 - INVOCATION ADAPTER (per platform)

The same `references/mode-*.md` + the same intent->mode map, exposed through each platform's trigger surface.

| Platform | Invocation surface | Adapter file contains |
|----------|--------------------|-----------------------|
| Claude Code | `commands/*.md` (already present) | `/prof-DA:<mode>` slash commands |
| Gemini CLI | `.gemini/commands/*.toml` | command name + a prompt that loads `references/mode-*.md` |
| Antigravity | `commands/*.md` (root) | mirror of the Claude commands |
| GitHub Copilot | `.github/copilot-instructions.md` + `.github/agents/<mode>.agent.md` | intent->mode routing + a per-mode agent file |
| Cursor | `.cursor/rules/*.mdc` (frontmatter description + globs) | a rule that pulls in the mode reference on match |
| OpenCode | OpenCode skill-tool manifest | skill registration pointing at `skills/da/` |
| Codex / OpenAI | `AGENTS.md` + a `.codex/` prompt | the orchestration contract + the tool map |

Universal across all: `AGENTS.md` at the repo root = the orchestration contract (intent->skill->mode)
that every platform reads. This is Addy's pattern, extended with the gate contract line.

### Layer 3 - GATE / HOOK ADAPTER (the mechanism-parity guarantee)

The hard part. Claude Code uses settings.json hooks (Stop / PreToolUse, exit 2 = block, receipt files).
Other platforms have no turn-level Stop hook. The fix: refactor the gate into a platform-neutral core +
thin per-platform adapters.

- `adapters/gate_core.py` - `gate_core(receipt_path) -> Verdict{passed, failures, attempts}`. This is
  `hooks/stop_gate.py`'s receipt-walk + self_check invocation + attempt counting, with the Claude-specific
  stdin / exit-2 stripped out. A pure importable function, platform-free.
- `adapters/gate.py` - `python -m gate <receipt>` (exit 0/2). The single CLI every non-Claude platform
  calls. The receipt JSON (report / deliver mode drops `.prof-da/pending-validation.json`) is already
  platform-neutral, so the SAME gate logic blocks everywhere; only the TRIGGER differs.

| Platform | Gate trigger | Adapter |
|----------|-------------|---------|
| Claude Code | settings.json Stop hook, exit 2 | `hooks/stop_gate.py` imports `gate_core` (current behavior preserved) |
| Any (git) | `pre-commit` / `pre-push` | `adapters/git/pre-commit` runs `python -m gate <receipt>`, nonzero aborts |
| CI (GH Actions / GitLab) | a CI step | `adapters/ci/gate-step.yml` runs `python -m gate <receipt>`, nonzero = red build |
| Cursor | a rule with `alwaysApply: true` | `.cursor/rules/gate.mdc` instructs running `python -m gate` before claiming done |
| Copilot | pre-merge check | `.github/workflows/gate.yml` (the same CI step) |
| Gemini / Antigravity / OpenCode | final tool call / post-run | the agent runs `python -m gate <receipt>` as the last step |

Honest limit: only Claude Code has a native turn-level Stop hook. Elsewhere the SAME gate logic runs, but
at commit / merge / final-tool-call time, not turn-end. That is mechanism-parity at the best available
trigger, stated plainly rather than hidden.

### Layer 4 - TOOL-NAME MAP (per platform)

A reference per platform mapping prof-DA's tool vocabulary (Skill / Agent / Bash / Read / Edit / Write /
TodoWrite) to the platform's tool names, so a mode reference that says "use Edit, not Write" or "spawn an
Agent" translates. Lives in `adapters/toolmaps/` (this design ships the matrix in `_toolmap.md`).

## Scaffold tree (placeholders, build deferred)

NEW nodes marked `[NEW]`; everything else exists today.

```
prof-DA-plugin/
  .claude-plugin/                 plugin.json, marketplace.json            (existing)
  AGENTS.md                       [NEW] universal orchestration contract (intent->skill->mode + gate line)
  skills/da/references/           ENGINE Layer 1 - verbatim everywhere     (existing)
  skills/da/scripts/              ENGINE Layer 1 - verbatim everywhere     (existing)
  commands/                       Layer 2 - Claude + Antigravity           (existing)
  hooks/stop_gate.py              Layer 3 - becomes a thin Claude adapter importing gate_core (deferred)
  adapters/                       [NEW] the whole portability layer
    README.md                     [NEW] what adapters/ is + how to add a platform
    gate_core.py                  [NEW][STUB] platform-neutral gate_core(receipt)->verdict  [PORT FROM hooks/stop_gate.py]
    gate.py                       [NEW][STUB] `python -m gate <receipt>` portable CLI (exit 0/2)
    git/pre-commit                [NEW][PLACEHOLDER] -> python -m gate
    git/pre-push                  [NEW][PLACEHOLDER]
    ci/gate-step.yml              [NEW][PLACEHOLDER]
    toolmaps/_toolmap.md          [NEW] the Layer-4 matrix (per-platform tool names)
  .gemini/commands/<mode>.toml    [NEW][PLACEHOLDER] per-mode invocation
  .github/copilot-instructions.md [NEW][PLACEHOLDER] intent->mode routing
  .github/agents/<mode>.agent.md  [NEW][PLACEHOLDER] per-mode agent
  .github/workflows/gate.yml      [NEW][PLACEHOLDER] pre-merge gate
  .cursor/rules/prof-da.mdc       [NEW][PLACEHOLDER] intent->mode rule
  .cursor/rules/gate.mdc          [NEW][PLACEHOLDER] alwaysApply gate-before-done
  docs/portability-architecture.md [NEW] this doc
```

## Portability checklist matrix

| Platform | Carries verbatim (L1) | Add invocation (L2) | Add gate (L3) | Add toolmap (L4) | Not yet supported |
|----------|-----------------------|---------------------|---------------|-------------------|-------------------|
| Claude Code | references + scripts + rules | already `commands/` | refactor `stop_gate.py` to import `gate_core` | claude | reference impl |
| Codex / OpenAI | references + scripts + rules | `AGENTS.md` + `.codex/` | `python -m gate` as final tool call | codex | native blocking hook; auto-receipt |
| GitHub Copilot | references + scripts + rules | `.github/copilot-instructions.md` + `.github/agents/` | `.github/workflows/gate.yml` (pre-merge) | copilot | in-editor real-time block |
| Cursor | references + scripts + rules | `.cursor/rules/*.mdc` | `.cursor/rules/gate.mdc` + `python -m gate` | cursor | hard block (rule is advisory) |
| Gemini CLI | references + scripts + rules | `.gemini/commands/*.toml` | `python -m gate` post-run | gemini | native Stop hook; auto-receipt |
| Antigravity | references + scripts + rules | `commands/` (root) | `python -m gate` call | reuse | native hook; auto-receipt |
| OpenCode | references + scripts + rules | skill-tool manifest | `python -m gate` call | opencode | native hook; auto-receipt |

Reading: Layer 1 (the bulk) is free everywhere. The cost is L2 (a few invocation files) + L3 (one neutral
`gate.py` + thin adapters). The hard-block guarantee is honest in the last column: only Claude Code blocks
per-turn; others get the same gate logic at commit / merge / final-tool-call time.

## Design-only vs build-this-session

- BUILD this session: this doc + the placeholder tree (files with `[FILL]` / `[PORT FROM]` markers only).
- DEFERRED: functional per-platform mirrors, the real `gate_core.py` extraction (touches `hooks/` -
  apply-after-coordination when built so it does not collide with the governance hooks), any release of
  the portability layer.

## Why this architecture

Mechanism parity is the user's binding constraint: the scripts, gates, references, and rules that make
prof-DA enforce discipline must survive the port, or the port is a hollow markdown copy. The 4-layer
model isolates the one genuinely platform-specific thing (the gate TRIGGER) behind one neutral CLI
(`python -m gate`), so everything else carries verbatim and the discipline holds on every platform.
