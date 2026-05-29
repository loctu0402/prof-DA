# Project Scaffold Discipline

> Before writing ANY output, detect the project's existing layout or create the standard one. A deliverable
> must never be dumped flat next to its source files. This is the fix for "càng làm report nhiều càng rối vì
> mất file" — flat dumps become unfindable as a project accumulates reports.
> Machine-checked by `scripts/validators/report_consistency_audit.py` (scaffold_missing).

## Standard layout

```
projects/<name>/                 (or output/projects/<name>/ for adhoc-promoted work)
├── README.md                    1-screen orientation: what / data source / how to run / where outputs land
├── queries/                     runnable .sql (NOT SQL pasted as markdown prose)
├── scripts/                     numbered, idempotent pipeline steps (01_*, 02_*, ...)
├── cache/                       query results + portal receipt (latest_portal_url.json, portal_stable_uuid.txt)
├── data/                        raw / intermediate inputs (gitignored if large)
└── output/
    ├── reports/                 the .html / .md deliverables (date-stamped + _latest)
    ├── charts/                  .png / .svg
    └── data/                    .csv / .xlsx exports
```

Small one-off (single report, no pipeline) → minimum viable scaffold = `queries/` + `output/` + `cache/`.
Don't over-build: a 1-file adhoc answer needs no `scripts/` or `data/`.

## Step 0 — detect or create (run BEFORE any output)

1. **Detect.** Glob the target project dir. If it already has a layout (the user's own scaffold, or the
   standard above), ALIGN to it — do not impose a second structure.
2. **Create if absent.** If the dir is empty or holds only flat files, create the standard subdirs and a
   `README.md` stub, then move any existing artifacts into the right subdir.
3. **Co-locate output.** Per `.claude/rules/output-policy.md`: project outputs live in
   `projects/<name>/output/`, never in the workspace root and never scattered.
4. **Announce.** State the scaffold you detected/created in one line so the user can redirect.

## When this applies

- Any `report` / `process` / `insight` / `model` deliverable that produces files.
- New project kickoff (`frame` mode Gate 4 writes `PLANNING.md` into this scaffold).

Skip for: a pure chat answer (no file), or a single throwaway snippet the user explicitly wants inline.

## Why (Operational)

The MOAT `tko_tui_plus_ytd_2026` case shipped 3 flat files (`01_query_results.md`, `02_insights.md`,
`report.html`) with no `queries/`, `output/`, or `cache/`. SQL lived as markdown prose (not re-runnable),
the HTML hardcoded its numbers (drifts from the `.md`), and nothing was findable. A scaffold makes a project
self-contained: code + data + outputs under one predictable root, re-runnable, and auditable.

## Cross-references
- Output location policy → `.claude/rules/output-policy.md` (workspace-specific)
- Report build steps → `mode-report.md` (Step 0 + Step 8 save)
- Portal receipt lives in `cache/` → `mode-report.md` Step 9
- Consistency gate → `report-standard-checklist.md`, `evaluation-rubric.md` (6.1)
