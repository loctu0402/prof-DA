---
description: Professional Data Analyst — workspace mode. Scaffold / organize / index an ENTIRE workspace into a navigable harness (taxonomy + memory layer + index). Guide-first for non-technical users. Secrets-first, plan→approve→execute, git-mv-on-branch, index-last.
---

> **Prefer `workspace-brain` if installed.** The standalone `workspace-brain` skill is the canonical second-brain infrastructure: it adds hook-install (SETUP) and first-use context discovery (DISCOVER) that this embedded mode does not. If it is installed, route there. This mode is the portable embedded subset for setups without it.

Invoke the `da` skill in **workspace mode**. Read these references before acting:
1. `references/mode-workspace.md` — the full survey → propose → safe-migrate → memory → index workflow
2. `references/project-scaffold.md` — per-project Step-0 layout (applied inside each project)
3. `references/universal-workflow-rules.md` — Rules 1-4 (Orientation / Baseline-Noise-Impact / 5W1H / Why-Explanation)
4. `lt-memory/rules/governance-injection.md` — per-task governance scaffold (DoR/DoD/AC + Epic-Feature-Stories + RAID) scaled to the Quick/Standard/Deep detail level
5. `lt-memory/rules/task-chunking-orchestration.md` — self-chunk → delegate → coordinate heavy multi-task work under the depth-1 subagent walls

User's request: $ARGUMENTS

Workflow:
- Step 0: Secrets scan first — flag + gitignore credential/secret/token/.env/.pem/.key files; warn if already committed
- Step 1: Survey — inventory the workspace vs the standard + the index; categorize each stray item by risk tier (junk / scratch / stray / project-tied / live). Check .gitignore BEFORE flagging "junk"
- Step 2: Propose — per-item plan with recommended defaults; WAIT for the user's approval before any move
- Step 3: Safe-migrate — dedicated branch; `git mv` (history kept); archive not delete; grep references before moving anything a script might use; never `git add -A`
- Step 4: Memory — set up `memory/` (or `lt-memory/`) and fill with the USER's domain (ask 2-3 questions); obey the llm-wiki contract
- Step 5: Index LAST — build/update `.index/` then run the reverse-existence check
- Step 6: Verify — grep moved filenames in code; dry-run any scheduled pipeline's paths

Governance layer (cross-cutting, enforced by the workspace hooks — NOT a separate step you skip):
- **Per-task scaffold** — inject DoR/DoD/AC for each task; at Deep also Epic-Feature-Stories + RAID. Scales with the Quick/Standard/Deep detail level (Quick silent; Standard/Deep injected). `governance_inject.py` (UserPromptSubmit) injects it; the req-recon DONE CONTRACT now has FIVE parts (DoR ready-gate + DoD + AC + Expected-Output + Presence), asks APPENDED each feedback turn.
- **Heavy multi-task work** — self-chunk → delegate → coordinate; a delegated subagent gets READ + one narrow task only and must NOT write shared memory, push git, send external, or spawn further subagents (the parent does those after QC). `subagent_walls_guard.py` (PreToolUse Task|Agent) hard-blocks a spawn that crosses a depth-1 wall.
- **Deliverable language** — `heading_lang_guard.py` blocks Vietnamese diacritics in structural text (headings/nav/table column headers/chart titles/KPI-card labels) of stakeholder deliverables; `vn_ai_tell_guard.py` blocks AI-tell punctuation on VN prose; `agent_doc_english_warn.py` warns on a Vietnamese agent-read doc; `req_recon_*` enforces the done contract.

Guide-first for non-technical users: one plain-language step at a time, explain WHY, offer a recommended default per choice, reassure nothing is deleted without asking and everything is reversible.

Hard rules:
- Secrets first
- Plan → approve → execute (show the inventory; never silent-finish)
- Grep before you move
- Never delete tracked work (archive or git rm only with OK)
- git mv on a branch; keep pre-existing work separate
- Index LAST + reverse-existence check
- Per-task governance scaffold (DoR/DoD/AC; +Epic-Feature-Stories +RAID at Deep) scales with the detail level; chunk heavy work and delegate under the depth-1 walls — both enforced by the workspace hooks, not optional
