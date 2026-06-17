---
name: review
description: 5 sub-modes for review work. Sub-mode A0 Brief (5-min snapshot Ship/Fix/Rebuild verdict). Sub-mode A Delivery Refine (lightweight polish). Sub-mode B Full Project Refine (heavyweight audit of workflow + method maturity + advanced + fact-check + rework plan + user approval gate). Sub-mode C Stakeholder Questioning (formulate questions before analysis). Sub-mode D Staleness Trace (after a change to one asset, trace + sync every dependent asset like doc / plan / AC-DoD / output). Use this skill whenever the user wants to critique, audit, refine, sanity-check, or re-sync existing work after a change. Auto-fires on natural Vietnamese + English. Natural triggers include "review report", "review bài", "review code", "refine deliverable", "audit project", "audit lại", "kiểm tra bài", "kiểm tra report", "OK chưa", "đã ổn chưa", "có thiếu gì không", "bài này được chưa", "góp ý", "feedback bài này", "stakeholder questions", "câu hỏi cho stakeholder", "hỏi gì stakeholder", "snapshot review", "method maturity", "advanced method gì", "có nên dùng DiD", "method này đủ rigor chưa", or explicit /prof-DA:review.
---

# Review Mode — Audit + Refine

5 sub-modes for review work. User picks ONE at invocation.

## 4 Quality Rules (applied to critique itself)
1. Orientation Block at top (verdict + summary)
2. Baseline → Noise → Impact when citing metrics in the critique
3. 8-field Action Brief for any "should fix" recommendation
4. Why-Explanation on every finding (why does this matter, why this fix, why this severity)

Full: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Sub-modes

### Sub-mode A0 — Brief (snapshot, 5 min)
Phases: mechanical audit (self_check.py + rubric_audit.py), outline/story-flow check, one-paragraph Ship/Fix-Then-Ship/Rebuild verdict. Escalate to A or B on a blocker.

### Sub-mode A — Delivery Refine (lightweight, single deliverable)
Phases: read end-to-end → rubric_audit.py → human pass → outline / story flow check → deliver gap table with severity → user approval → apply fixes.

### Sub-mode B — Full Project Refine (heavyweight, multi-file audit)
Phases: target disambiguation → context-tracing read → project understanding summary (user confirm) → 6-pass audit (workflow / business+domain / method maturity / advanced-method / code+repro / delivery surface) → deliver audit + rework plan → user approval → execute plan top-to-bottom.

### Sub-mode C — Stakeholder Questioning
Phases: map stakeholder → frame Q set with 5W1H+Goal → catch anti-patterns (approval-ask, vague scope, yes/no when need number) → suggest output form → compile brief.

### Sub-mode D — Staleness Trace (change-propagation after an edit)
Phases: identify the changed SOURCE + the specific change (user gives a path, or agent auto-detects from the action log: git status / git log / recent mtimes) → build the dependent set (trace manifest if present, else grep the project by filename + concept across doc/plan/AC-DoD/output/sibling diagrams) → diff each dependent vs the new source (IN-SYNC / STALE) → user approval → update each stale dependent (one dependent = one commit; flag the ones needing user input) → independent re-read audit → drop a done-receipt. Not a quality critique; a consistency sync.

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-review.md`.

## Hard rules
- Iteration ceiling: max 3 review rounds; after 4th, escalate (rebuild / handoff / accept-with-limitations)
- Fresh-session review discipline: sub-agent for context-tracing gets ZERO generator context (anti-bias)
- Outline / Story Flow Check mandatory at Phase 3.5 (Sub-mode A) and Pass 6 (Sub-mode B)
- Method maturity check (Sub-mode B Pass 3): compare method-used vs causal-inference-toolkit decision table
- Rework plan in Sub-mode B awaits user approval BEFORE execution

## Sub-agent integration
- `da-context-tracer` (Haiku) — Sub-mode B Phase 2 when project ≥ 5 files
- `da-method-auditor` (Sonnet) — Sub-mode B Pass 3 when causal claims present

Sub-agent prompt discipline: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/subagent-prompt-discipline.md`.

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-review.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
- Quality criteria: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/quality-criteria.md`
- Method specs: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/methods/_index.md`
