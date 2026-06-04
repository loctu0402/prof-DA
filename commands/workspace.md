---
description: Professional Data Analyst — workspace mode. Scaffold / organize / index an ENTIRE workspace into a navigable harness (taxonomy + memory layer + index). Guide-first for non-technical users. Secrets-first, plan→approve→execute, git-mv-on-branch, index-last.
---

> **Prefer `workspace-brain` if installed.** The standalone `workspace-brain` skill is the canonical second-brain infrastructure: it adds hook-install (SETUP) and first-use context discovery (DISCOVER) that this embedded mode does not. If it is installed, route there. This mode is the portable embedded subset for setups without it.

Invoke the `da` skill in **workspace mode**. Read these references before acting:
1. `references/mode-workspace.md` — the full survey → propose → safe-migrate → memory → index workflow
2. `references/project-scaffold.md` — per-project Step-0 layout (applied inside each project)
3. `references/universal-workflow-rules.md` — Rules 1-4 (Orientation / Baseline-Noise-Impact / 5W1H / Why-Explanation)

User's request: $ARGUMENTS

Workflow:
- Step 0: Secrets scan first — flag + gitignore credential/secret/token/.env/.pem/.key files; warn if already committed
- Step 1: Survey — inventory the workspace vs the standard + the index; categorize each stray item by risk tier (junk / scratch / stray / project-tied / live). Check .gitignore BEFORE flagging "junk"
- Step 2: Propose — per-item plan with recommended defaults; WAIT for the user's approval before any move
- Step 3: Safe-migrate — dedicated branch; `git mv` (history kept); archive not delete; grep references before moving anything a script might use; never `git add -A`
- Step 4: Memory — set up `memory/` (or `lt-memory/`) and fill with the USER's domain (ask 2-3 questions); obey the llm-wiki contract
- Step 5: Index LAST — build/update `.index/` then run the reverse-existence check
- Step 6: Verify — grep moved filenames in code; dry-run any scheduled pipeline's paths

Guide-first for non-technical users: one plain-language step at a time, explain WHY, offer a recommended default per choice, reassure nothing is deleted without asking and everything is reversible.

Hard rules:
- Secrets first
- Plan → approve → execute (show the inventory; never silent-finish)
- Grep before you move
- Never delete tracked work (archive or git rm only with OK)
- git mv on a branch; keep pre-existing work separate
- Index LAST + reverse-existence check
