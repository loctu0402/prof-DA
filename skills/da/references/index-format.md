# Workspace Index Format — Progressive-Disclosure Retrieval

> The index is the layer that makes a workspace **navigable by lookup, not by guessing**. Read it first each session; follow one link; read only the range you need. This file is the format spec for the workspace `.index/` AND the rule for when a deep folder earns its own local index.

## Progressive disclosure — the contract every index obeys

An index is worthless if it is as expensive to read as the thing it indexes. Five rules keep it cheap (adapt names to the workspace; keep the shape):

1. **Index ≤ 200 lines · 1 line per entry · ≤ 150 chars/line.** An entry is `[label](path) — gist under 150 chars`. If it overflows, split by category into a sub-index — never let an index grow into a document.
2. **Atom = 1 topic · ≤ 300 lines.** The detail lives in the linked file, not the index. A file covering 2+ topics gets split.
3. **Cross-link, never re-paste.** Reference by relative path or wikilink; copy only the 1-line gist. Lifting paragraphs across files is drift waiting to happen.
4. **Read pattern: index → link → targeted range.** Load the index, identify the topic, follow the link, read only the needed lines (`file.md L80-100`). Never brute-force grep/glob before checking the index.
5. **Enforce at write-time.** If the workspace has an anti-bloat hook, it rejects an over-threshold index entry or atom at Write/Edit — not at a session-end audit.

## The workspace index — `.index/` at the root

Four files, read in this order. Optional `_skills.md` / `_mcp.md` when the workspace has many of either.

### `_root.md` — entry point (read FIRST)
```markdown
# WorkspaceIndex — Entry Point
> Read FIRST every session. Last rebuilt: YYYY-MM-DD

## Retrieval Strategies
| Query type | Description          | Load                          |
|------------|----------------------|-------------------------------|
| Single-hop | Direct entity lookup | _entities.md → file:line       |
| Multi-hop  | Cross-file reasoning | _graph.md → follow cluster     |
| Global     | Structural overview  | _tree.md → scan section        |

## Workspace Stats
- X projects, Y knowledge atoms, Z templates, ...
```

### `_tree.md` — folder hierarchy (target ~150 lines)
```markdown
## folder-name/
### subfolder/
- `file.md` (SIZE) — 1-line description
- `script.py` — 1-line gist from its docstring
```
- Skip `.git`, `.venv`, `__pycache__`, `node_modules`, vendored caches.
- Flag files > 50 KB with size (expensive reads).
- Group any folder of 10+ similar files by prefix (`txn-* | 26 files | orders, refunds, payouts…`) instead of listing each.

### `_graph.md` — semantic connections
```markdown
## Clusters
### Cluster name
- file_a <-> file_b (relationship)
## Navigation Shortcuts
| If you need... | Start here | Then follow to... |
```
Connection types: schema <-> knowledge · config <-> resource · input -> output (script → generated file) · shared-entity cross-reference.

### `_entities.md` — entity → `file:line` map (target ~200 lines)
```markdown
## Aliases
| Alias | Canonical            |
|-------|----------------------|
| MAU   | Monthly Active Users |

## Category
| Entity        | File              | Lines    | Context                       |
|---------------|-------------------|----------|-------------------------------|
| status column | domains/orders.md | L118-122 | enum: new / active / churned  |
```
- **Line ranges are required** — they are the whole point of the entity map. Validate every range against the real file; never fabricate one.
- Include aliases for acronyms and alternate names; group by category.

## Recursive / per-folder index — when a sub-folder earns its own `_index.md`

The root `.index/` covers the whole workspace at one level. That is enough until a sub-tree becomes a **knowledge collection navigated on its own terms** — a set of atom notes (a memory layer, a domain hub, a notes vault, a project's `docs/`) that someone reads *into* directly, numerous or deep enough that listing every leaf in the root index would blow the ≤200-line / 1-line-per-entry budget.

When that happens, give the folder its own local `_index.md` and let the root index point at the **local index, not the leaves**:

```
.index/_root.md                      # workspace level — points to the memory layer's index
  memory/_index.md                   # subsystem level — points to each knowledge area
    domains/_index.md                # collection level — points to each hub
      domains/<topic>/_index.md      # hub level — points to its atoms (tables / kpis / edge-cases)
```

Each hop is one thin index (same contract: ≤200 lines, 1 line per entry, cross-link not re-paste). The reader takes one hop to the sub-index, a second to the atom — instead of one giant flat index that costs as much as the corpus.

**Earns a local index** — a knowledge area read independently with many atoms:
- the memory layer and its sub-collections (rules, decisions, per-topic hubs),
- a notes/PKM vault and any deep note-cluster inside it,
- a knowledge-dense corner of a single project (e.g. its `docs/`).

**Does NOT earn one** — pure containers; the root `_tree.md` already covers them:
- the `projects/` parent (index each project's *contents* if dense, not the parent),
- `output/`, `shared/`, a top-level `reference/` drop.

The test is **information role + atom count**, not raw file count: a folder of 30 generated CSVs is a container (one tree line); a folder of 12 linked knowledge notes earns an index.

## Build · update · rebuild

- **build / update** — incremental: reflect new / moved / deleted files, refresh the `_root` timestamp. Cheap; no benchmark.
- **rebuild** — full: regenerate all index files from scratch. Optionally benchmark retrieval (brute-force vs indexed) on 3 generated queries (single-hop / multi-hop / global) and save the before/after as a dated report.
- Always: validate `_entities.md` line ranges against real files, run the reverse-existence check (below), obey the contract above.

## Reverse-existence check — run after EVERY build/update

Forward "addition detection" (scan for new files) is **blind to moves, deletes, and renames** inside folders that still exist. So also run the reverse pass:

1. Extract every path and `file:line` pointer already in `_entities.md`, `_tree.md`, `_graph.md`.
2. For each, confirm the file still exists AND (for `_entities.md`) the cited range still resolves to the right content.
3. Repoint or remove dead pointers. Never leave a pointer that 404s; never fabricate a line range to "fix" one — open the file and read it.

Do this **in code** (Python / a glob API), not a shell `while`/`case` loop — on Windows, CRLF line endings corrupt shell loops silently. Touch only the dead rows; leave live ones alone.
