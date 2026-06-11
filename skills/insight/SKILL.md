---
name: insight
description: Diagnostic analysis — why did X happen, what's the mechanism, what should we do. Use this skill whenever the user asks for explanation, root cause, mechanism, or recommendation after seeing data. Auto-fires on natural Vietnamese + English. Natural triggers include "điều gì xảy ra", "tại sao X giảm/tăng", "vì sao X", "X đột biến", "why is X dropping/rising", "what's happening", "what changed", "root cause", "nguyên nhân", "mechanism", "explain X", "giải thích vì sao", "diagnostic", "hypothesis validation", "phân tích sâu", "deep dive", "phân tích insight", "stakeholder hỏi tại sao", "đề xuất action", "recommend gì", "next step gì", "tìm phương pháp tính", "đo lượng tiềm năng", "potential size", "opportunity sizing", "MFU cohort", "user cohort", "phân tích trên tập user", "tập user là", "có yếu tố mùa vụ không", "seasonal pattern", "decompose trend/seasonality", "A/B test có significant không", "ý nghĩa thống kê", "correlation", "tương quan", or explicit /prof-DA:insight. Runs 9-phase workflow: Scope+Hypothesize → Data Collection → Diagnostic Method Matching (DiD/Event Study/RDD/Synthetic Control/PSM/IV) → Statistical Methodology → Self-Evaluation → Anti-Bias Protocol → 5-Stage Reasoning Chain → Hypothesis Verdicts → Recommendations. Enforces causal rigor (falsification, robustness, multiple-testing correction).
---

# Insight Mode — Why + Mechanism + Recommendation

For any "why did this happen?" / "what's the mechanism?" / "what should we do?" question.

## 4 Universal Rules
1. Orientation Block (SCQR for written, 3-line for dashboard)
2. Baseline → Noise → Impact ladder for every numeric finding
3. 8-field Action Brief for every recommendation
4. Why-Explanation on every method choice (DiD over Pearson? Why. Bootstrap vs parametric? Why.)

Full: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.

## Mode workflow (9 phases)

1. Scope & Hypothesize (3-5 hypotheses + validation criteria)
2. Data Collection (internal + market + competitor)
3. Diagnostic Techniques (match method to situation — DiD / Event Study / RDD / Synthetic Control / PSM / IV)
4. Statistical Methodology (Pearson, effect size, CV vs MDE, α vs FDR, 3 hypothesis traps)
5. Self-Evaluation (methodology / proxy / sample / confounding / direction / consistency audit)
6. Anti-Bias Protocol (counter-arguments, multi-dimensional, structural vs cyclical)
7. Reasoning Output (5-stage chain: Fact → Mechanism → Behavior → Impact → Evidence)
8. Hypothesis Verdicts (ĐÚNG / MỘT PHẦN / KHÔNG)
9. Recommendations (8-field brief, C-level tone)

Full workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-insight.md`.

## Method specs
Causal inference: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/causal-inference-toolkit.md` (decision table) + `methods/<name>.md` (full spec per method).
Validation: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/validation-evaluation-methods.md` + `methods/<name>.md`.

## Hard rules
- Wrong method → wrong causal claim. Match method to data setup before estimating.
- Heavy-tail outcomes (median≈0, SD/mean>3×) → Wilcoxon + winsorize + median Δ
- Multiple testing: K > 1 → Bonferroni or BH-FDR correction
- Never claim causal without falsification test
- Connect-the-Dots: never state-the-fact alone

## Cross-references
- Full mode workflow: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-insight.md`
- Quality criteria: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/quality-criteria.md`
- Self-check: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/self-check-protocol.md`
