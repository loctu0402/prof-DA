---
name: workspace
description: Workspace governance mode — scaffold, organize, and index an ENTIRE Claude Code workspace into a navigable, self-documenting harness. Use whenever a workspace is messy / files scattered everywhere, when setting up a new workspace's folder + memory + index from scratch, when cleaning or reorganizing an existing workspace safely without breaking pipelines, or when building / rebuilding the workspace index. GUIDE-FIRST for non-technical users — walks one plain-language step at a time (survey → propose → approve → migrate → index). Auto-fires on natural Vietnamese + English. Natural triggers include "workspace bừa", "dọn workspace", "sắp xếp lại thư mục", "file nằm khắp nơi", "tổ chức lại workspace", "hệ thống lại workspace", "set up workspace", "scaffold workspace", "organize my workspace", "tidy up folders", "my files are everywhere", "memory/folder governance", "build index", "rebuild index", "update index", or explicit /prof-DA:workspace. Distinct from frame (project planning), project-scaffold reference (one project's layout), and governance reference (data governance).
---

# Workspace Mode — Scaffold, Organize & Index

Workspace-LEVEL governance: turn a scattered workspace into a navigable harness — clean taxonomy + a memory layer + an index. Distinct from per-project scaffold (`project-scaffold.md`) and data governance (`governance.md`); this mode operates on the whole workspace and invokes project-scaffold per project.

## 4 Universal Rules (apply to all output)

1. **Orientation Block** — every inventory/plan opens with current-state + target + reading order.
2. **Baseline → Noise → Impact** — quantify the mess (N stray, M unindexed) vs the standard.
3. **Question → Goal → 5W1H** — the migration plan is an action brief, approved before execution.
4. **Why-Explanation (META)** — every move/delete/archive states its tier-why.

Full rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow — the loop

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-workspace.md`.

| Step | Output | Confirm with user |
|------|--------|-------------------|
| **0 — Secrets first** | credential/secret files flagged + gitignored | Found secrets? rotate? |
| **1 — Survey** | inventory categorized by risk tier (junk/scratch/stray/project-tied/live) | Is this the right read of the mess? |
| **2 — Propose** | per-item plan (move/archive/delete) with recommended defaults | Approve, or change which items? |
| **3 — Safe-migrate** | moves done on a branch (`git mv`, archive not delete) | — |
| **4 — Memory** | `memory/` layer set up + filled with USER's domain | What domains do you work on? |
| **5 — Index LAST** | `.index/` built + reverse-existence check | — |
| **6 — Verify** | grep moved paths in code; dry-run pipeline paths | — |

## Hard rules (golden)

- **Secrets first** — before anything else.
- **Plan → approve → execute** — never hand over a reorganization the user didn't approve.
- **Grep before you move** — a script may reference the file by hard-coded path.
- **Never delete tracked work** — archive to `_archive/` or `git rm` only with the user's OK.
- **`git mv` on a dedicated branch** — keep pre-existing uncommitted work separate; never `git add -A`.
- **Index LAST** — after moves settle, then reverse-existence check.
- **Guide-first for non-technical users** — one plain-language step at a time, recommended defaults, reassure reversibility.

## Cross-references
- Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-workspace.md`
- Per-project layout (Step-0): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/project-scaffold.md`
- Universal rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`
