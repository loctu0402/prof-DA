# <organization> Stakeholder Extensions

This reference bundles the <organization>-specific tooling (Semantic Cube, <org-data-mcp> MCP, <org-sql-agent> tags, OpenMetadata curation) that make this plugin a **complete harness for <organization> DA stakeholders**. The rest of the plugin is portable across companies; this file is the org-specific layer.

**Audience**: Loc Tu + any <organization> DA / AE / PO using this skill in the <organization> workspace. Non-<organization> users can ignore this file entirely — the plugin's portable behavior is unaffected.

## What <organization> adds on top of the portable plugin

| Capability | <organization> tool | Plugin reference (generic) |
|-----------|-----------|---------------------------|
| Semantic layer | Semantic Cube (<semantic-tech> + Cube.js) at `<semantic-layer-host>` | `references/semantic-layer-setup.md` |
| Schema catalog | OpenMetadata at `<data-catalog-host>` | `references/schema-source-hierarchy.md` T1 |
| LLM-grade schema tag | `<org-catalog>.*` tag namespace | `references/schema-source-hierarchy.md` T0 |
| MCP gateway | `<org-data-mcp>` MCP (gateway: `mdp-mcp-gateway.<internal-host>`) | (none — <organization>-only) |
| NL→SQL agent | <org-sql-agent> (via MCP `<org-sql-agent>`) | `references/mode-query.md` Step 2 semantic-first |
| event-tracking | Mini-app event explorer | (none — <organization>-only) |
| Data Portal | Documentation governance | (none — <organization>-only) |
| Journey Data | User journey analytics | (none — <organization>-only) |

## 1. Semantic Cube (<semantic-tech> + Cube.js)

<organization>'s semantic layer = <semantic-tech> (open-source fork) + Cube.js core + Hasura (metadata GraphQL) + React UI (Explore / Models / Dictionary / Settings).

**Onboarding**: see full reference at `<workspace>/notes/loctu-pkm/1-notes/semantic-cube-reference.md` (833 lines, covers spec + 5-step workflow + 23 interview Q&A + 6-phase build recipe).

**Quick links**:
- Production: `https://<semantic-layer-host>/docs/intro`
- the standard specification (mandatory): `https://<semantic-layer-host>/docs/basic/data_modeling/cubejs_model_specification`
- Support: Google Chat group ["Claude With <organization> Data"](https://chat.google.com/app/chat/AAQAokD9l24)

**Workflow (5 steps, abbreviated)**:
1. **Create Team** — ping `son.hua1@` or `chinh.nguyen2@` with team name + admin list (1 business day)
2. **Create Data Source** — BQ / Lakehouse (Hive) / StarRocks (MySQL connector). BQ needs Service Account + Billing Project ID (request via `hai.nguyen1@`)
3. **Build Model (Cube)** — write YAML manually or auto-generate from `catalog.dataset.table`; MUST follow the standard specification; prefer Git-versioned YAML
4. **Test via Explore** — measures + dimensions interactively; check generated SQL + result sanity
5. **Deliver** — Looker Studio / Ad-hoc Explore / Claude Desktop (MCP) / REST API / Alert

**Critical rules from the standard specification**:
- Cube name = file name (snake_case)
- Cube MUST have `description` (Dictionary indexing)
- Meta block MANDATORY (author, email, dates, publicMcp, maintainers, tags)
- Cube MUST have `count` measure (`type: count`) — Looker bar-chart fails without it
- Joined cubes MUST set `primary_key: true` on dim id — prevents chasm/fan trap
- BQ time dim MUST wrap `TIMESTAMP({CUBE}.col, 'Asia/Ho_Chi_Minh')`
- NO `GROUP BY` in cube `sql:` — Cube re-aggregates from row level
- `publicMcp: true` only after AI access approved

For building a brand-new semantic layer (anywhere, not just <organization>), use the portable recipe in `references/semantic-layer-setup.md`.

## 2. <org-data-mcp> MCP — the gateway

<organization> runs a unified MCP gateway at `https://mdp-mcp-gateway.<internal-host>/servers/<server_id>/mcp` exposing multiple data tools through one HTTP MCP server. The plugin user adds it to their MCP config (see `<plugin_root>/mcp/example-org-mcp.json`) to unlock these tools.

### Tool groups bundled in `<org-data-mcp>` MCP

| Tool group | Prefix | What it does |
|-----------|--------|--------------|
| Semantic Cube | `semantic-*` | Query Semantic Cube programmatically (3-step: team → meta → load) |
| Data Portal | `data-portal-*` | Read/list/upload documentation entities (folders, documents, attachments, versions, feedback) |
| Journey Data | `journey-data-journey-*` | User journey analytics (list / detail / conversion / comparison / duration) |
| <event-system> (mini-apps) | `event-*` | Mini-app event tracking + tracking search / validate (events, mini-apps, filters) |

### Semantic Cube tools (3-step query)

```
1. semantic-get-team-data        → returns teams + datasource_id list
2. semantic-fetch-meta-by-id(id) → returns cubes + measures + dimensions
3. semantic-load(query)          → executes cube query, returns rows
```

Optional: `semantic-greet`, `semantic-get-datasource-by-name`, `semantic-fetch-meta-by-id` for finer discovery.

### Data Portal tools (documentation governance)

Use when the analysis needs to reference or update documentation:
- `data-portal-list-folders` / `data-portal-list-documents` → browse
- `data-portal-get-folder` / `data-portal-get-document` / `data-portal-get-document-versions` → read
- `data-portal-search-documents` / `data-portal-search-document-content` → grep
- `data-portal-upload-attachment` / `data-portal-rename-document` / `data-portal-restore-document-version` → write
- `data-portal-submit-feedback` / `data-portal-list-feedback` → feedback loop

### Journey Data tools (user journey analytics)

Pre-built journey-analytics queries that would otherwise require complex window-function SQL:
- `journey-data-journey-list` → list available journey definitions
- `journey-data-journey-get-data` / `journey-data-journey-get-detail` → fetch step-by-step events
- `journey-data-journey-get-conversion` → conversion funnel
- `journey-data-journey-get-comparison` → A/B journey comparison
- `journey-data-journey-get-duration` → time-spent-per-step

### <event-system> tools (mini-app event tracking)

For mini-app analytics:
- `event-execute-explorer-with-filters` / `event-execute-explorer-with-filter-groups` → ad-hoc explorer with filters
- `event-execute-extended-explorer` → richer query
- `event-get-all-events` / `event-get-mini-apps` / `event-get-allowed-filter-columns` → discovery
- `event-tracking-search-events` / `event-tracking-search-mini-apps` → search
- `event-tracking-validate-event` / `event-tracking-validate-mini-app` → validate tracking config

### When to use which group

| Question | Use |
|----------|-----|
| "<product> AUM tháng 4?" | semantic-* (cube already has metric) |
| "Cấu trúc folder bài MoAT là gì?" | data-portal-list-folders |
| "Conversion rate flow signup → first_cashin?" | journey-data-journey-get-conversion |
| "Mini-app X có event Y không?" | event-tracking-search-events |

## 3. <org-sql-agent> — the NL→SQL agent + tag

<org-sql-agent> is two things at <organization>:

### 3a. <org-sql-agent> as MCP (`<org-sql-agent>` MCP)

A separate MCP server (`<org-sql-agent>`) exposes an NL→SQL agent specialized for <organization>'s BQ schemas. Add to MCP config (`<plugin_root>/mcp/example-org-mcp.json`).

Tools (when registered, schema differs from `<org-data-mcp>`):
- `execute_sql` — run SQL against <organization> BQ with cost guardrails
- `get_domain_schema` — fetch schema for a domain (uses <org-sql-agent> tag if present, else INFORMATION_SCHEMA)
- `glob_search` — search tables matching a pattern

Use <org-sql-agent> MCP when the question is "give me data X" and you don't want to write SQL yourself. For tighter control or learning purposes, write SQL directly with the patterns in `references/mode-query.md`.

### 3b. <org-sql-agent> as a tag namespace (T0 schema source)

Within OpenMetadata (`<data-catalog-host>`), the tag namespace `<org-catalog>.*` flags tables that owners have **deliberately curated for LLM / AI agent consumption**. Tagged tables typically have:

- Rich plain-language descriptions per column (not just type)
- Sample query patterns
- Business meaning + edge cases
- Cross-references to related tables

**Example**: the <product> mart `daily_user_mart` carries tag `<org-catalog>.<domain-tag>` (URL: `https://<data-catalog-host>/tag/<org-catalog>.<domain-tag>`). When you encounter a table with a `<org-catalog>.*` tag, **read the tag content FIRST** — it's the highest-quality schema source available (T0 in the schema-source-hierarchy ladder).

**Discovery flow**:
```python
import requests
H = {"Authorization": f"Bearer {PAT}"}
tbl = requests.get(
    f"https://<data-catalog-host>/api/v1/tables/name/bigquery.<data-project>.<dataset>.<table>?fields=tags,columns,description",
    headers=H,
).json()
<org-catalog>_tags = [t for t in tbl.get("tags", []) if t["tagFQN"].startswith("<org-catalog>.")]
if <org-catalog>_tags:
    # T0 hit — read tag content for LLM-grade schema
    for tag in <org-catalog>_tags:
        tag_info = requests.get(
            f"https://<data-catalog-host>/api/v1/tags/name/{tag['tagFQN']}",
            headers=H,
        ).json()
        # tag_info has owner-curated content
```

## 4. OpenMetadata workflow (T1 schema source + curation)

OpenMetadata (`<data-catalog-host>`) is <organization>'s canonical data catalog. Two layers:
1. **Auto-ingested** (column names, types, partition keys synced from BQ) — never edit
2. **Curated** (table desc, column desc, tags, ownership, lineage) — humans + agents own this

Full playbook (fetch → audit → dry-run → push → cross-validate) lives at `<workspace>/lt-memory/setup/openmetadata-workflow.md` (~242 lines). Key API mechanics:

### Auth + endpoints

```python
BASE = "https://<data-catalog-host>"
PAT = "<bearer_token>"   # rotate weekly via OM UI → user settings → access tokens
H = {"Authorization": f"Bearer {PAT}"}

# Read by FQN
GET {BASE}/api/v1/tables/name/bigquery.<data-project>.<dataset>.<table>?fields=columns,description,tags,version

# Read by UUID
GET {BASE}/api/v1/tables/{uuid}?fields=columns,description,tags,version

# PATCH (JSON Patch RFC 6902)
PATCH {BASE}/api/v1/tables/{uuid}
Headers: Content-Type: application/json-patch+json  # ← MANDATORY, NOT application/json
Body: [{"op": "add", "path": "/columns/0/description", "value": "<new>"}, ...]
```

### 5-phase curation pattern

When refactoring schema descriptions (e.g. HTML→markdown cleanup, content fix, bi-ref insertion):

1. **Discovery** — fetch full schema, dump to UTF-8 file for diffability, count cols, scan formats
2. **Audit** (read-only) — compare against `lt-memory/domains/<X>/tables.md` if exists; spot-check 5-10 cols; categorize issues (format / content / structural)
3. **Build** (dry-run) — write script with `--push` flag (default = dry-run); output old vs new side-by-side
4. **Push** — single PATCH with batched ops array (atomic); patch only changed cols; verify version bumped
5. **Cross-validate + record** — verify sibling tables (daily ↔ monthly) consistent; update local `lt-memory/domains/<X>/tables.md`

### Hard rules (learned from 2026-05-15 <product> mart curation)

| Rule | Why |
|------|-----|
| `Content-Type: application/json-patch+json` MANDATORY | Wrong Content-Type → 400 with cryptic error |
| `json.dumps(patches, ensure_ascii=False).encode("utf-8")` for Vietnamese | Default ASCII encoding stores escaped `ả` etc. |
| Column index `/columns/N` is array position OM returned, NOT alphabetical | Always fetch first, iterate, use the index you read |
| `"op": "add"` works as upsert; `"replace"` only if path exists | Use `add` to avoid surprises |
| Format-only push vs content push — DON'T MIX | A "format" push that touches content reads as authority claim under cover |
| Auto-derive across siblings is DANGEROUS | Source can have content bugs (`cashin_gmv` literally said "cashout"); auto-adapt propagates the bug |
| Bi-directional sibling reference MANDATORY | "For monthly grain → `<monthly>` (30× cheaper)" + reverse; without this, 30× cost incurred silently |
| Dry-run to file, READ IT, then push | Don't trust transformation function from samples alone |
| Advisor checkpoint before push when scope expands beyond mechanical | 191-column "auto-adapt" plan caught pre-push by advisor |

### When to push T1 fix vs flag for owner

| Situation | Action |
|-----------|--------|
| Column description has typo / format issue | Push fix (mechanical) |
| Column description factually wrong (swap, wrong unit, wrong grain) | Flag for table owner; if you ARE owner, fix |
| Column description missing entirely | Push initial draft, ping owner to review |
| Description is rich but cube layer (T2) contradicts | Flag both, request alignment from semantic team |

## 5. Schema source preference for <organization> work

Putting the 5-tier ladder + <organization> tools together (instantiates `references/schema-source-hierarchy.md` for <organization>):

```
Question: schema of daily_user_mart? Do I have access? What's the business meaning?

T0 — Check OpenMetadata for <org-catalog>.* tag (owner-curated LLM-grade)
     → GET /api/v1/tables/name/bigquery.<data-project>.<dataset>.daily_user_mart?fields=tags
     → tag <org-catalog>.<domain-tag> present
     → Fetch tag content → if covers question, STOP

T1 — OpenMetadata catalog DIRECT API (full curated layer, admin visibility)
     → GET /api/v1/tables/name/bigquery.<data-project>.<dataset>.daily_user_mart
        ?fields=columns,description,tags,version
     → 94 columns, all with markdown descriptions, bi-ref to monthly ✓
     → If sufficient AND you know you have BQ access, STOP

T2 — Access-aware MCPs (per-user scope, semantic cube, data portal docs)
     2a. <org-catalog> MCP — get_domain_schema('daily_user_mart')
         → Returns schema FILTERED to your BQ access scope + domain-knowledge layer
         → Confirms access AND adds analyst-written domain context catalog doesn't have
     2b. <org-data-mcp> MCP — semantic cube check
         → semantic-get-team-data → datasource_id
         → semantic-fetch-meta-by-id(datasource_id) → list cubes
         → If <product> cube wraps this table → read measures + dimensions (business logic encoded)
     2c. <org-data-mcp> MCP — data portal docs about this table
         → data-portal-search-document-content('daily_user_mart')
         → Find any prior analyst docs / handoff notes / known gotchas
     → If T2 covers question + confirms access, STOP

T3 — INFORMATION_SCHEMA fallback + brainstorm with user
     → SELECT column_name, data_type, is_nullable, partitioning_column FROM
       `<data-project>.<dataset>.INFORMATION_SCHEMA.COLUMNS` WHERE table_name='daily_user_mart'
     → Then ask the human user (domain expert):
        "94 columns found — sentinels you know about?"
        "Any column deprecated since YYYY-MM-DD?"
        "Sibling table preferred for monthly grain (it's `monthly_user_mart`)?"

T4 — Sample 5 rows (only if T0–T3 still leave gaps about ACTUAL DATA values)
     → SELECT * FROM `<data-project>.<dataset>.daily_user_mart` WHERE date='2026-05-15' LIMIT 5
     → MUST include partition filter; check sentinel values, NULL conventions, format quirks
```

**For non-<organization> tables**: drop T0 (<org-sql-agent>-specific) and T2 (<organization> MCPs). Proceed T1 → T3 → T4 with whichever catalog tool + access-aware MCP (if any) your org runs.

**Key principle**: T2 sits ABOVE T3 because access-aware MCPs (a) confirm what you can actually query — no permission denied surprise mid-analysis, (b) bundle catalog + semantic cube + data portal docs in one user-scoped view, (c) often have richer schema notes + business glossary than raw catalog API alone.

## 6. MCP setup for <organization> stakeholders

Example MCP config snippet (`<plugin_root>/mcp/example-org-mcp.json`) provides ready-to-paste config for adding all 3 <organization> MCPs at user scope:

```bash
# Install <org-data-mcp> MCP (gateway)
claude mcp add -s user <org-data-mcp> -- cmd /c npx -y mcp-remote https://mdp-mcp-gateway.<internal-host>/servers/<server_id>/mcp

# Install <org-sql-agent> MCP (NL→SQL)
claude mcp add -s user <org-sql-agent> -- <path-to-<org-catalog>-mcp-launcher>

# Install powerbi-modeling MCP (PowerBI Desktop integration, if used)
claude mcp add -s user powerbi-modeling -- <path-to-vscode-ext-server>
```

See `<plugin_root>/mcp/example-org-mcp.json` for the JSON form (drop-in for `~/.claude.json` user scope).

## 7. Cross-references

**Within this plugin**:
- Schema tier ladder → `references/schema-source-hierarchy.md`
- Building a semantic layer (portable) → `references/semantic-layer-setup.md`
- Query mode discovery step → `references/mode-query.md` Step 2
- Data modeling patterns → `references/mode-model.md`
- Governance → `references/governance.md`
- MCP suggestion at mode-exit → `references/suggestion-protocol.md` (MCP-tooling expansion category)

**External (require workspace access)**:
- Full Semantic Cube reference → `<workspace>/notes/loctu-pkm/1-notes/semantic-cube-reference.md`
- OpenMetadata curation playbook → `<workspace>/lt-memory/setup/openmetadata-workflow.md`
- <product> domain knowledge → `<workspace>/lt-memory/domains/<product>/`
- AAA reference (read-only) → `<workspace>/lt-memory/domains/aaa-reference/_index.md`

**External (docs)**:
- Semantic Cube: `https://<semantic-layer-host>/docs/intro`
- OpenMetadata Swagger: `https://<data-catalog-host>/swagger`
- Cube.js core docs: `https://cube.dev/docs`
- <semantic-tech>: `https://<semantic-tech>.org`

## Why this file exists

The portable plugin is engine-agnostic (deliberately so), but <organization> DAs need one-stop access to <organization>-specific tooling (Semantic Cube, <org-data-mcp> MCP, <org-sql-agent> tag, OpenMetadata curation). Without this file, every new <organization> session re-discovers "wait, what MCP do I use for that?". This file consolidates the 5 <organization>-specific entry points (Cube + MCP + tag + catalog + portal) into one reference, hooked into the portable plugin's schema-discovery ladder. Adding a new <organization>-only feature → extend this file, not the portable references.
