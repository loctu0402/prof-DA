---
name: frame
description: Front-of-workflow planning mode — turn a vague stakeholder ask into a locked plan (5W1H + Metric Contract + Data Plan + Next-Mode Routing). Use this skill whenever the user starts a new analysis, doesn't know where to begin, asks for a metric to track an outcome, or wants to scope / kickoff a project. Auto-fires on natural Vietnamese + English. Natural triggers include "không biết bắt đầu", "không biết bắt đầu từ đâu", "kickoff", "kickoff project mới", "frame project", "scope project", "scope lại", "stakeholder muốn", "stakeholder hỏi", "stakeholder yêu cầu", "metric nào phù hợp", "metric define", "đo lượng X", "đo lường X", "tìm phương pháp tính", "tìm phương pháp đo", "tính tiềm năng", "potential size", "opportunity sizing", "MFU cohort sizing", "user cohort sizing", "xét trên tập user", "tập user là", "feature mới", "tính năng mới", "mình mới tiếp nhận", "mình mới được giao", "plan hướng phân tích", "đề xuất framework", "đo bằng metric gì", "dimension nào nên dùng", "vấn đề là gì", or explicit /prof-DA:frame. Runs 4 gates with user-confirm checkpoints (Business Understanding → Metric Define → Data Plan TH1/TH2 → Lock & Hand-off → routes to next mode). Outputs a PLANNING.md doc that downstream modes consume.
---

# Frame Mode — Plan Before Analysis

The front of the DA workflow. Translate a vague stakeholder ask into a locked plan with metrics + data strategy + next-mode routing.

## 4 Quality Rules (apply to all output)

1. **Orientation Block** — PLANNING.md opens with SCQR.
2. **Baseline → Noise → Impact Ladder** — metric contract MUST specify comparability baseline.
3. **Question → Goal → 5W1H Action Brief** — Gate 1 outputs the 5W1H table.
4. **Why-Explanation (META)** — every metric choice + framework choice has 1-line Why.

Full rules: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow — 4 Gates

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-frame.md` + `${CLAUDE_PLUGIN_ROOT}/skills/da/references/planning-protocol.md`.

| Gate | Output | What to confirm with user |
|------|--------|---------------------------|
| **Gate 1 — Business Understanding** | 5W1H + stake + audience + reversibility | Is this the right question, audience, stake? |
| **Gate 2 — Metric Define** | Metric contract(s) per chosen framework | Are these the metrics that decide success? |
| **Gate 3 — Data Plan** | TH1 schema-verified OR TH2 modeling-pattern-chosen | Do we know what data + table + grain? |
| **Gate 4 — Lock & Hand-off** | `PLANNING.md` written + route to next mode | OK to execute, switch to which mode next? |

## Hard rules

- **Each gate has user-confirm checkpoint** — don't proceed without explicit OK
- **TH1 vs TH2 explicit choice** at Gate 3 — don't pretend data exists when it doesn't
- **Metric contract MUST include 10 fields** (see `metric-framework.md` Step 10)
- **Output is a doc (`PLANNING.md`), not chat** — future sessions read it
- **Cost ceilings respected at Gate 3** ($0.01 schema scan / $0.10 sample / $1.00 validation)

## Phase routing (after Gate 4)

Based on `Next Mode` field in `PLANNING.md`:

| Next mode | When |
|-----------|------|
| `/prof-DA:query` | Schema known, SQL needed |
| `/prof-DA:process` | Data wrangling / EDA needed |
| `/prof-DA:model` | New pipeline modeling needed (TH2 path) |
| `/prof-DA:insight` | Hypothesis framed, ready for diagnostic |
| `/prof-DA:automate` | Pipeline needs scheduling |
| `/prof-DA:report` | Stakeholder deliverable needs structure |

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-frame.md`
- Planning protocol (gates detailed): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/planning-protocol.md`
- Metric framework selection: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/metric-framework.md`
- Domain discovery (TH2 path): `${CLAUDE_PLUGIN_ROOT}/skills/da/references/domain-discovery-protocol.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
