---
name: automate
description: Engine-agnostic pipeline + scheduling + fail-alert workflow. Works with Airflow / Dagster / Prefect / crontab / GitHub Actions. Use this skill whenever the user needs to schedule a job, automate a pipeline, set up a recurring run, or wire fail-alerts. Auto-fires on natural Vietnamese + English. Natural triggers include "automation", "automate", "tự động hóa", "pipeline tự động", "schedule job", "set up cron", "cronjob", "Airflow DAG", "Dagster", "Prefect", "GitHub Actions schedule", "chạy hàng ngày", "chạy hàng tuần", "chạy hàng tháng", "recurring", "daily pipeline", "weekly pipeline", "alert khi pipeline lỗi", "fail-alert", "email on fail", "Gchat on fail", "backfill", "backfill từ ngày", "rerun từ", or explicit /prof-DA:automate.
---

# Automate Mode — Pipeline Scheduling

Pipeline automation with fail-alert + cache discipline + no auto-send safety.

## 4 Quality Rules
1. Orientation Block (docstring for pipeline modules)
2. Baseline → Noise → Impact for any monitoring metric
3. 8-field Action Brief for scheduling change
4. Why-Explanation on scheduler choice + alert channel + cache strategy

Full: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow

1. Decision tree pick scheduling layer (cron / Airflow / Dagster / Prefect / GitHub Actions)
2. Wire pipeline.py with try/except + send_failure_email
3. Cache discipline: incremental MUST NOT clip lower bound; preserve history on update
4. Fail-alert config: channel + recipient + natural-language reason in team's primary language
5. No auto-send to stakeholder (only oncall on fail)

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-automation.md`.

## Hard rules
- Pipeline FAIL alert wired to configured oncall recipient (auto-send by design)
- Stakeholder reports NEVER auto-sent (default: save to output/, show preview link, wait for "send" command)
- SEND uses SMTP (`smtplib` + a config file: host / port / sender / app-password); it sends for real and attaches files. A draft-only mail connector (e.g. a "create_draft" MCP) is NOT a send path; never conclude "cannot send / no attachment". Full mechanism: `mode-automation.md`
- Reason in natural Vietnamese ("Pipeline daily lỗi khi đọc mart — chưa có data ngày YYYY-MM-DD"), NOT stacktrace
- Backfill > 1 month on billed engine → dry-run + $ report to user first

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-automation.md`
- Coding discipline: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/coding-discipline.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
