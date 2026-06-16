# Recurring Automated Report Product (end-to-end blueprint)

> The cross-mode recipe for building a recurring automated report PRODUCT from scratch (ideation to a
> scheduled, self-sending report), the savings-product daily-report shape. This is what connects the otherwise-siloed
> modes into one proposed flow. Self-contained. Companions: `delivery-lifecycle.md` (the 7-phase spine),
> `build-auto.md` (the gated execution loop), `mode-frame.md` (where this is proposed).

## Grain and scope
One unit = one recurring report product (daily/weekly/bi-weekly/monthly, auto-pulled, auto-rendered,
auto-sent, monitored). In scope: the full chain ideation to schedule. Out of scope: a one-off report
(use `/report` alone), an ad-hoc query (`/query`).

## When to use (trigger recognition for frame mode)
When a user asks to "build a recurring/automated report like X", "set up a daily/weekly report product",
"reproduce an existing daily automated report", "tu dong hoa bao cao dinh ky", or describes wanting the WHOLE
thing (data + report + delivery + schedule), do NOT drop them into a single mode. Recognize it as a PRODUCT
build and PROPOSE this end-to-end flow as an action plan first, then execute it (under `/deliver`).

## The end-to-end chain (propose this as the action plan)

| # | Phase | Mode(s) | What gets decided/built | Concrete output |
|---|-------|---------|--------------------------|-----------------|
| 1 | DISCOVER | frame | intent, stakeholder + their decision, the ONE question the report answers, scope, out-of-scope | a charter (PLANNING.md) |
| 2 | METRIC | frame | metric-choice framework (NSM / OMTM / HEART / AARRR / Diagnostic / counter-metric); the headline + driver metrics | a metric contract |
| 3 | MODEL | model, query | data sources, the mart/DWH, the metric SQL (verified, grain-checked) | DWH/mart design + runnable queries |
| 4 | DESIGN | report | fork an A1-A12 archetype (never freestyle); sections, chart anatomy, dual-comparison KPIs; pick deliverable format(s) (HTML SPA / PDF / email / Gchat card / slide) | a report spec + the locked template |
| 5 | PREDICT (if any) | process | the forecast/prediction model if the report needs one (time-series / an expected-value blend / scoring); backtest + PI | a model + metrics.json |
| 6 | DELIVERABLES + CHANNELS | report, automate | choose what ships + where: email (SMTP), Google Chat webhook, Slack, Google Sheets write, a portal link | the send mechanism wired (NEVER auto-send in dev) |
| 7 | SCHEDULE | automate | the scheduler (cron / Windows Task / Airflow DAG / GitHub Actions / Apps Script) + fail-alert + cache discipline + backfill | a scheduled job + email-on-fail |
| 8 | VALIDATE | submit, review, fix | test vs AC, render-verify the report, dry-run the send, parallel-run before promotion | validators green, a dry-run proof |
| 9 | LEARN | workspace | codify to a template, set up freshness monitoring, write the runbook | a reusable template + monitor |

The build (phases 3-8) runs under `/deliver` (the build-auto loop: 1 task = 1 commit + verify gate +
stop-on-error/risk; never auto-send is on the irreversibility stop-list).

## How frame proposes it
At kickoff, frame lays out the table above filled with THIS product's specifics (the metric, the sources,
the chosen archetype, the channels, the cadence), as a single proposed action plan with a DoR/DoD/AC per
phase, and asks the user to approve the plan (one batch approval), then routes phase by phase. This is the
"design the full flow and propose" behavior: the modes stop feeling siloed because frame owns the chain.

## How to prompt (examples the user can give)
- "Build a daily automated report cho product X: pull AUM + MAU, forecast 7 ngay, gui email +
  Gchat luc 9h sang." -> frame proposes the 9-phase plan, then `/deliver` executes it.
- "Reproduce an existing daily report flow tu dau cho product Y." -> frame loads this blueprint, fills it for Y.
- "Set up a weekly report product: metric, report, send, schedule." -> same chain, cadence = weekly.

## Worked example (a savings-product daily report)
1. DISCOVER: stakeholder = wealth lead; question = "is AUM on track vs expected today". Scope = daily snapshot.
2. METRIC: NSM = AUM total; drivers = netcash, MAU/MFU (MTD distinct), balance/user; counter = churn.
3. MODEL: sources = the savings marts; queries grain-checked (COUNT(*) = COUNT(DISTINCT user)).
4. DESIGN: fork the daily-report archetype; dual deliverable (editorial paper + ops dashboard); NSM-anchored.
5. PREDICT: an expected-value blend (Expected = trend x (1+weekly seasonal) x (1+daily seasonal) x intervention index), per-metric dynamic weights, 7-day forecast, PI.
6. CHANNELS: Gmail SMTP (send_report with attachments + CID images); optional Gchat card.
7. SCHEDULE: Windows Task / cron daily ~9-11h; email-on-fail; cache + gap-detect; backfill path.
8. VALIDATE: render-verify (headless rasterize), dry-run send to self, parallel-run vN beside vN-1 before promote.
9. LEARN: lock the report template; freshness manifest + anomaly monitor; runbook.

## Hard rules
- PROPOSE the whole chain before building; do not silently build one phase and stop.
- Fork an archetype for the report (phase 4); never freestyle the design.
- NEVER auto-send in dev (phase 6/8): dry-run to self or emit + hand to the user; confirm recipients.
- Run phases 3-8 under `/deliver` so each phase is committed + verified + stop-on-risk.
- Every metric is grain-checked and freshness-verified (`evidence-based-done.md`).
