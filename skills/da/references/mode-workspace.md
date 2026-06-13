# Workspace Mode — Scaffold, Organize & Index a Whole Workspace

> WORKSPACE-LEVEL governance: turn a scattered workspace into a navigable, self-documenting harness — clean folder taxonomy + a memory layer + an index. Distinct from `project-scaffold.md` (one project's Step-0 layout) and `governance.md` (data governance). This mode operates on the whole workspace; it INVOKES project-scaffold per project. Self-contained — it needs nothing outside prof-DA. The pattern (treat a workspace as a structured document with a tree, a graph, and an entity map) follows the BookRAG concept (arXiv:2512.03413).

## When to use

- A workspace where files are scattered everywhere / accumulated without a system.
- Setting up a new workspace's structure + memory + index from scratch.
- Cleaning / reorganizing an existing in-use workspace safely.
- Building / rebuilding the workspace index.

**Why (Operational):** an unsystematized workspace gets slower and riskier over time — files become unfindable, the assistant re-learns context every session, and there is no index so every lookup is a brute-force read. This mode pays that debt down once and keeps it down.

## 4 Universal Rules application

1. **Orientation Block** — every plan/inventory you present opens with a 1-line statement of current state + target + reading order.
2. **Baseline → Noise → Impact** — when reporting the mess, quantify it (N stray files, M unindexed folders) against the standard, not vaguely.
3. **Question → Goal → 5W1H** — the migration plan is an action brief: what moves where, why, with the user's approval.
4. **Why-Explanation (META)** — every move/delete/archive decision states why (junk / scratch / project-tied / live).

## The standard (target shape)

A healthy workspace has five parts. Adapt names to the user's domain; keep the shape (it is domain-neutral — works for a data team, a marketing/reporting team, a research vault).

1. `projects/<name>/` — each project self-contained: code AND its `output/` together (per-project internal layout → apply `project-scaffold.md`).
2. `output/` (top level) — adhoc one-off assets only, in `charts/ data/ reports/ exports/ misc/`. Project work never lands here.
3. A **memory layer** (`memory/` or `lt-memory/`) — durable facts/decisions/domain knowledge as small linked notes, so the assistant doesn't re-learn each session.
4. `.index/` — the workspace index (`_root _tree _graph _entities`), read first each session for cheap navigation.
5. `CLAUDE.md` at root — the rules the assistant reads every turn; points at the index + memory layer.

Plus `shared/` (reusable templates/themes/utilities), `notes/` (documents), `reference/` (read-only external), `<name>/_archive/` (retired work — archived, never deleted blindly).

## The loop

Survey → Propose → (approve) → Safe-migrate → Memory → Index → Verify. For a non-technical user, run it in **guide mode** (one plain-language step at a time; see the bottom section).

### Step 0 — Secrets first (ALWAYS, before anything)
Scan for credential/secret files: names matching `credential*`, `*secret*`, `token*`, `*.pem`, `*.key`, `*-service-account*.json`, `*.env`. For each: if git-tracked, check `git ls-files` and warn loudly (advise rotation); add to `.gitignore`; never print contents.
**Why (Causal):** an exposed `credentials.txt` at the root is the single highest-severity, most domain-neutral problem — fixing it first is non-negotiable.

### Step 1 — Survey (don't move yet)
Compare the filesystem against the standard AND the existing `.index/` if any. The delta is the mess.
**Check `.gitignore` BEFORE flagging "junk".** A mature workspace often already gitignores its cruft — those are on-disk clutter, not git problems. Distinguish on-disk-junk (delete to declutter) from tracked-misplaced (needs `git mv`, higher care). Categorize each stray item into a risk tier:

| Tier | What | Action | Risk |
|------|------|--------|------|
| Junk | OS cruft, tool caches, accidental-redirect files (`nul`, `=4.2.0`, a `${VAR}` folder), empty dirs | delete from disk | none |
| Scratch | one-off probes, throwaway results, `_tmp_*` | archive → `output/_archive/` | low |
| Stray | adhoc scripts/screenshots at root | relocate (grep refs first) | low |
| Project-tied | outputs belonging to a project | grep refs; move to `projects/<name>/output/` only if 0 refs | medium |
| Live | files a scheduled pipeline reads/writes | DO NOT move | high |

### Step 2 — Propose (get approval)
Present the inventory as a table: each item → current → proposed action → why. Mark genuine judgment calls (delete vs archive, which project owns this) with YOUR recommended default. **Wait for the user's yes before any move.**
**Why (Operational):** silently handing over a finished reorganization the user never agreed to is the failure mode — surface the plan, let them redirect.

### Step 3 — Safe-migrate (by risk tier, lowest first)
- Git repo → work on a dedicated branch, commit a clean baseline, keep pre-existing uncommitted work separate (stage only your own paths; never `git add -A`).
- Tracked file → `git mv` (preserves history). Untracked relocate → filesystem move + `git add` if it should now track.
- Live pipelines → confirm scheduled jobs; never move their files unless you fix every reference in the same step.
- Archive, don't delete tracked work; delete only true junk, and only with the user's OK.

### Step 4 — Memory layer
Create/align `memory/` (or `lt-memory/`): `_index.md` (1 line per note) + `rules/ knowledge/ decisions/` + optional `domains/<topic>/` L1/L2/L3 hubs. Fill it with the USER's domain (ask 2-3 questions) — never pre-fill with someone else's content. Obey the llm-wiki contract (index ≤200 lines, atom ≤300 lines, cross-link never re-paste).

### Step 5 — Index LAST (progressive disclosure)
Only after moves settle, build/update the root `.index/` (`_root _tree _graph _entities`). The index is **read-first, navigable by lookup** — keep it cheap: index ≤200 lines, 1 line per entry, atoms ≤300 lines, cross-link never re-paste, read index → link → targeted range.
**Recursive / per-folder index:** when a sub-folder becomes a knowledge collection read on its own terms (a memory layer, a domain hub, a notes vault, a project's `docs/`) — deep or numerous enough that listing every leaf would blow the index budget — give it its **own local `_index.md`** and point the root index at that sub-index, not the leaves. Pure containers (`projects/` parent, `output/`, `shared/`) do not earn one; the root tree already covers them. The test is information role + atom count, not raw file count.
Then run the **reverse-existence check**: every pointer already in the index still resolves on disk (moves create dead pointers forward-only scans miss).
Full format + the recursive rule: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/index-format.md`.

### Step 6 — Verify
Grep the codebase for moved filenames — a match inside the moved file is fine; a match in a pipeline script is a break to fix. Dry-run any scheduled job's paths. Report exactly what moved / was deleted vs archived, and the verification result.

## Hard rules (the golden rules)

1. Secrets first.
2. Plan → approve → execute (show the inventory).
3. Grep before you move.
4. Never delete tracked work — archive or `git rm` only with the user's OK.
5. `git mv` on a dedicated branch; keep pre-existing work separate.
6. Index LAST + reverse-existence check.

## Run-safe gotchas (hard-won)

- **Author batch moves and index builds in code, not a shell loop.** On Windows, CRLF line endings corrupt `while`/`case` shell loops silently — use Python or a glob API.
- **A failed `git push`/`fetch` under a tool sandbox can lie.** It may report `Host key verification failed` even when SSH and the network are fine — the sandbox blocked it before git reached SSH. Distinguish from a real block (which fails earlier, at key exchange), retry outside the sandbox, and don't chase VPN / known_hosts / config first.
- **Orphaned gitlink.** A `160000` tree entry that is NOT in `.gitmodules` is an embedded repo added without registering a submodule. If it carries its own uncommitted content, push/clean it inside that repo first; never `git rm --cached` it blindly — that strands unpushed work.

## Self-operating loops (Hermes-derived) — keep the workspace alive, not just tidy-once

Scaffold + organize + index is a one-time setup. A workspace that is governed but never maintained still rots. These four loops keep it healthy on a cadence; each maps to a primitive the host already has (a hook, a scheduled run, a standing rule). The standalone `workspace-brain` skill ships the live hooks + the curator script; this is the portable, engine-neutral statement of the loops.

1. **Curator (periodic consolidation).** On a cadence (weekly) or on demand: merge near-duplicate notes into one class-level note, surface orphan atoms (in no index, cross-linked nowhere), flush the log → digest backlog, re-validate index pointers. Invariants, non-negotiable: **never auto-delete (archive only, recoverable); pinned items bypass; candidates need human approval; read-only scan, propose-then-apply.** A maintenance pass that finds nothing prints a silent no-op, not noise. (`workspace-brain` ships `scripts/curator_scan.py` + `references/curator-mode.md`.)

2. **Hard memory budget (consolidate, don't append).** Index / memory files are read every session, so unbounded growth taxes every load. Enforce the contract AT WRITE TIME: a write that grows an over-cap index/memory file is rejected with a "consolidate" instruction (index ≤ 200 lines, atom ≤ 300, 1 line per entry), not a soft warning. Shrinking/flat rewrites and an explicit `allow-oversize: <reason>` escape are allowed, so it never traps an already-oversize file.

3. **After any context compaction / summarization.** The summary is background reference, NOT active instructions; the latest user message WINS over it; reverse signals ("stop", "undo", "just verify", "never mind", a new topic) end in-flight summarized work immediately; persistent memory stays authoritative; re-read any open requirements/checklist after compaction (a summary can drop an open ask — the "70% done, reported done" failure).

4. **Subagent hard walls.** A spawned subagent must NOT write shared memory, push git / send external messages / publish, or spawn further subagents. The parent centralizes stateful writes after QC and is accountable for what ships. Give the child READ + its one narrow task only.

These are the loops that turn a static harness into a self-improving one: the index/memory stay lean, knowledge consolidates instead of sprawling, long sessions don't drift, and delegation can't corrupt the shared layer.

## Guide mode (non-technical user)

One question at a time. Plain language ("folder" not "directory"; "back up first" not "git stash"). Explain WHY before each step. Offer a recommended default for every choice. Reassure: nothing deleted without asking, everything reversible (branch + archive). Narrate the same loop above, but each step is a simple question the user answers. End with 3 maintenance habits (new project → ask to scaffold it · finished one-off → goes to `output/` · periodically → "update the index" + "run the curator").

## Cross-references
- Index format + progressive disclosure + recursive per-folder rule: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/index-format.md`
- Per-project internal layout (Step-0): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/project-scaffold.md`
- Output location policy: `.claude/rules/output-policy.md` (or this mode creates one)
- Data governance (different concern — metrics/grain/quality): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/governance.md`
- Universal rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`

— part of prof-DA · Loc Tu, 2026
