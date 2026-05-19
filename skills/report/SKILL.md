---
name: report
description: Build stakeholder deliverable from template (HTML SPA / PDF / email / Gchat / slides). SCQR + Key Terms + Impact Cards skeleton. Chart 7-anatomical-elements. Dual-comparison KPIs. Sentiment color with context override. HTML SPA structural inspection. Use this skill whenever the user needs to produce a stakeholder-facing report, dashboard, slide deck, executive summary, or share-out. Auto-fires on natural Vietnamese + English. Natural triggers include "build báo cáo", "làm báo cáo", "làm report", "viết report", "stakeholder report", "report cho stakeholder", "báo cáo cho sếp", "executive summary", "exec summary", "build dashboard", "làm dashboard", "build slide", "làm slide", "deck cho", "share-out", "HTML report", "HTML SPA", "PDF report", "email blast", "Gchat card", "<organization> brand", "biểu đồ", "chart cho stakeholder", "trình bày kết quả", or explicit /prof-DA:report.
---

# Report Mode — Stakeholder Deliverable

Stakeholder-facing deliverable build, polish, and verify.

## 4 Universal Rules
1. Orientation Block at top (SCQR for written, 3-line intro for dashboard, "How to read" for multi-tab HTML)
2. Baseline → Noise → Impact ladder for every numeric statement
3. 8-field Action Brief for every recommendation
4. Why-Explanation for every method / threshold / chart-type / framework choice

Full: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow

8 steps + 7.5 HTML SPA verification:
1. Confirm audience + output format
2. Fork template (NEVER edit source)
3. Wire data (verify freshness)
4. Apply Orientation Block (SCQR / 3-line / How to read)
5. Populate body with Baseline-Noise-Impact ladder + per-chart takeaway + dual-comparison KPIs + chart anatomy 7-element
6. Recommendations section with 8-field Action Brief
7. Self-check (run rubric_audit.py + outline / story flow check)
7.5. HTML SPA structural inspection via preview_eval (catches what screenshot misses)
8. Save to output/projects/ or output/reports/ (NEVER root)

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-report.md`.

Narrative template (SCQR + Key Terms + Impact Cards): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/narrative-template.md`.

## Hard rules
- AI-tells BANNED in stakeholder text: ===, -----, em-dash, ≈, → (use comma/period/leads-to)
- Vietnamese full diacritics for stakeholder output (ệ / ỉ / ổ / à / ă)
- Every KPI dual-comparison (DoD + 7d avg) — single delta = noise
- Chart 7-anatomical-elements: Figure N + title + axes + legend + total cards + insight line + notes + download
- Sentiment color context-aware: cashout↑ = RED for AUM context, may flip for liquidity context (document override)
- NEVER auto-send stakeholder reports
- NEVER edit generator for HTML patch (use update_report_vN.py overlay)

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-report.md`
- Narrative template: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/narrative-template.md`
- Style + AI-tells: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/style-rules.md`
- Quality criteria: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/quality-criteria.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
