#!/usr/bin/env python3
"""
prof-DA dispatch layer 1/2 - SessionStart hook: standing skill-dispatch protocol.

Skill descriptions alone are a probabilistic trigger surface: in sessions with a crowded
skill list the host may drop descriptions, and the agent may rationalize "this is just a
quick question" and hand-answer DA work. This hook injects a compact dispatch protocol
into EVERY session (the same mechanism superpowers uses) so the agent is primed to route
DA-shaped requests through prof-DA before responding.

Layer 2/2 is da_intent_detector.py (UserPromptSubmit) - the deterministic per-prompt catch.

Fail-open: any error -> print nothing, never disrupt session start.

- part of prof-DA . Loc Tu, 2026
"""
from __future__ import annotations
import sys

PROTOCOL = """<prof-DA-dispatch>
prof-DA plugin is installed. It is the standing entry point for ALL data-analyst-shaped work in this session.

THE RULE: if there is even a 1% chance the user's request involves data, numbers, metrics, SQL, analysis, prediction / forecasting, reporting, dashboards, pipelines, or data quality -> invoke Skill(prof-DA:da) BEFORE responding (it confirms scope + detail level cheaply, then routes). Do NOT hand-answer DA work without it. An explicit /prof-DA:<mode> call skips the router.

Mode map (what fires where):
- frame     -- kickoff / scope project / "metric nao phu hop" / khong biet bat dau tu dau
- model     -- SCHEMA design: dbt / Kimball / Medallion / mart / table contract (NOT statistical models)
- query     -- lay so lieu / breakdown / so sanh / trend / viet SQL / pull data
- process   -- EDA / clean / data quality / feature engineering / ML case study / FORECAST + du doan + time series + seasonal + churn prediction + scoring + segmentation
- insight   -- tai sao X tang/giam / root cause / hypothesis / deep dive / correlation
- automate  -- schedule job / cron / Airflow / backfill / fail-alert
- report    -- bao cao / dashboard / slide / executive summary
- deliver   -- build it autonomously / chunk + commit per task / "/build auto" (the build-auto execution loop wrapping any build mode)
- submit    -- finalize + nop recurring report vs team acceptance contract
- review    -- audit / "OK chua" / gop y / method maturity
- fix       -- pipeline loi / so sai / missing data / patch report
- workspace -- don dep / scaffold / index workspace

Rationalizations that mean a trigger is about to be MISSED (stop and invoke prof-DA:da):
- "This is just a lookup / quick question" -> questions about data ARE DA work.
- "I'll search the workspace for a template / example first" -> the skill knows where templates live; invoke first.
- "The user didn't say analyze / report" -> conversational Vietnamese counts ("cho minh so lieu", "co san template du doan khong").
- "I can answer from general knowledge" -> prof-DA grounds answers in the user's real context (memory/ + .index/).

When a [prof-DA dispatch] note is attached to a user prompt, treat it as a hard routing signal, not a suggestion.
</prof-DA-dispatch>"""


def main() -> int:
    try:
        print(PROTOCOL)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
