---
name: workspace
description: Workspace governance mode — scaffold, organize, and index an ENTIRE Claude Code workspace into a navigable, self-documenting harness. Use whenever a workspace is messy / files scattered everywhere, when setting up a new workspace's folder + memory + index from scratch, when cleaning or reorganizing an existing workspace safely without breaking pipelines, or when building / rebuilding the workspace index. GUIDE-FIRST for non-technical users — walks one plain-language step at a time (survey → propose → approve → migrate → index). Auto-fires on natural Vietnamese + English. Natural triggers include "workspace bừa", "dọn workspace", "sắp xếp lại thư mục", "file nằm khắp nơi", "tổ chức lại workspace", "hệ thống lại workspace", "set up workspace", "scaffold workspace", "organize my workspace", "tidy up folders", "my files are everywhere", "memory/folder governance", "build index", "rebuild index", "update index", or explicit /prof-DA:workspace. Distinct from frame (project planning), project-scaffold reference (one project's layout), and governance reference (data governance).
---

# Workspace Mode — Scaffold, Organize & Index

Workspace-LEVEL governance: turn a scattered workspace into a navigable harness — clean taxonomy + a memory layer + an index. Distinct from per-project scaffold (`project-scaffold.md`) and data governance (`governance.md`); this mode operates on the whole workspace and invokes project-scaffold per project.

> **Prefer `workspace-brain` if installed.** The standalone `workspace-brain` skill is the canonical second-brain infrastructure: it adds hook-install (SETUP) and first-use context discovery (DISCOVER) this embedded mode does not. Route there when present; this mode is the portable embedded subset.

## 4 Quality Rules (apply to all output)

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
| **5 — Index LAST** | root `.index/` + a local `_index.md` per deep/knowledge-dense folder; reverse-existence check | — |
| **6 — Verify** | grep moved paths in code; dry-run pipeline paths | — |

## Hard rules (golden)

- **Secrets first** — before anything else.
- **Plan → approve → execute** — never hand over a reorganization the user didn't approve.
- **Grep before you move** — a script may reference the file by hard-coded path.
- **Never delete tracked work** — archive to `_archive/` or `git rm` only with the user's OK.
- **`git mv` on a dedicated branch** — keep pre-existing uncommitted work separate; never `git add -A`.
- **Index LAST** — after moves settle, then reverse-existence check.
- **Progressive disclosure** — index ≤200 lines (1 line/entry), atoms ≤300 lines, cross-link never re-paste; deep knowledge folders get their own local `_index.md`.
- **Guide-first for non-technical users** — one plain-language step at a time, recommended defaults, reassure reversibility.

## Self-operating maintenance (after the one-time setup)

Scaffold + organize + index is the one-time setup; a governed workspace still rots without upkeep. This mode also carries the **self-operating loops** (Hermes-derived) that keep it alive on a cadence — full spec in `mode-workspace.md`:

- **Curator** (weekly or on-demand): merge near-duplicate notes into class-level umbrellas, surface orphan atoms, flush the log-to-digest backlog, re-validate index pointers. Read-only scan, propose, approve; archive-never-delete; pinned-bypass.
- **Hard memory budget**: a write that grows an over-cap index/memory file is rejected with a consolidate instruction (index 200 lines, atom 300 lines), not a soft warning.
- **Post-compaction discipline** (latest user message wins over the summary) + **subagent hard walls** (depth-1 delegation; only the parent writes shared memory / pushes).
- **Per-task governance** (DoR / DoD / AC scaled to Quick / Standard / Deep), hook-enforced.

The standalone `workspace-brain` ships the live hooks + `scripts/curator_scan.py`; this mode is the portable, engine-neutral statement of the same loops. Full detail + invariants: `mode-workspace.md` sections "Self-operating loops" and "Governance layer".

## Cross-references
- Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-workspace.md`
- Index format + progressive disclosure + recursive per-folder rule: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/index-format.md`
- Per-project layout (Step-0): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/project-scaffold.md`
- Universal rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`
