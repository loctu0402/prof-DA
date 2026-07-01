# Keyed-Snapshot Record (KSR) — persistence contract

The universal contract for HOW every mode persists what it produces. A cache, a computed table,
an event/eval/log store, a model manifest, a pipeline step - each is a RECORD with identity and
time, never a throwaway print or a silently-overwritten blob. Cross-cutting: it binds Query,
Process, Model, Automation, Report, Fix - any mode that writes an artifact.

## The 4 invariants

Every artifact a mode emits MUST satisfy all four:

1. **Structured** - a schema'd table/object, not a loose print. A reader enumerates its fields
   without guessing.
2. **Keyed** - every record addressable by an explicit stable key (`id` / `entity_id` /
   `event_id` / a date-key like `report_date` / `target_date`). Joins are deterministic.
3. **Snapshotted** - stamped as-of a time/version, NOT silently overwritten. Past states replay
   and diff. A value that changes over time keeps a dated history, it does not overwrite.
4. **Step-persisted** - each pipeline step writes its OWN artifact (raw -> staged -> cleaned ->
   mart / feature). No step folded into a later one so its output can't be inspected alone.

Consequence: **provenance is always traceable** - any number traces to its keyed, dated source,
any past run is reconstructable.

## The three patterns (pick one; do not invent a fourth per file)

- **A - keyed append-log.** An accumulating series (forecasts, events, runs). One growing file;
  each entry keyed + dated; appended, never rewritten. Exemplar shape: `{_meta{schema_version,
  key, updated_at, n_entries}, entries:[{run_date, target_date, metric, horizon, forecast,
  actual, actual_updated_at}, ...]}` - bitemporal, fully replayable. Use for anything that
  accretes over time.
- **B - latest-pointer + dated-history-store.** A snapshot recomputed each run that must replay.
  A `*_latest` pointer carrying its own `as_of` / `fetch_date`, PLUS a `*_history` store keyed by
  date (`{_meta, by_date:{"<date>":{...}}}`). The dated history is the source of truth; the
  pointer is convenience.
- **C - dated immutable manifest.** A rich per-run snapshot (a model run, a report build). One
  IMMUTABLE file per as-of day, the date IN the filename; inside, `report_date` + `generated_at`
  + a `*_snapshot` of inputs used. Never re-touched.

## The `_meta` provenance block (required on every KSR file)

`_meta{ schema_version:int, key:[...], as_of:<logical date>, generated_at:<iso>, source:<script /
query / upstream table> }`. Keep a domain's own `report_date` / `fetch_date` too, but always set
the canonical `as_of` alias.

## The anti-pattern this kills

"Show the number then lose it" - a lone `*_latest.json` overwritten each run (yesterday's exact
state gone), a report number untraceable to a keyed dated source, pipeline steps collapsed into
one "run once, show final" blob. If persisting a value that changes over time, never a lone
overwrite - append-log or latest+history.

## Routing

- IF a mode writes a cache / output / event / eval / log table -> it MUST be a KSR record; pick
  A / B / C. (Automation cache discipline, Model table contracts, Report data caches all bind.)
- IF a genuine throwaway scratch you will delete -> KSR is overkill; do not over-engineer.
- A KSR artifact on disk (keyed + dated) IS the evidence-based-done receipt for that step.

## Why this matters

Causal - the "an soi" overwrite loses provenance + history, so a wrong number can't be traced and
a past run can't be reproduced; a keyed dated record makes both mechanical. Empirical - the report
pipeline already proved the shapes work (a bitemporal forecast append-log, a date-keyed market
history, dated model manifests) then drifted to `_latest`; KSR restores the proven pattern instead
of re-deciding per file.
