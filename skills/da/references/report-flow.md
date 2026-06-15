# Report Flow — Solve-by-Cluster (detail body)

How the DETAIL body of a deep-dive / solution-after-problem report is structured so it always
presents a result and then goes and solves it, cluster by cluster.

## When to use

- Deep-dive reports and solution-after-problem reports (surface a problem, then solve it).
- NOT for a quick lookup or a flat metric dump.
- The opener is UNCHANGED and still required: Executive Summary + SCQA (Orientation Block) +
  Overview (5-second scan). This flow governs the detail body AFTER the overview.
  Opener template: `${CLAUDE_PLUGIN_ROOT}/skills/da/references/narrative-template.md`.

## Core idea

The detail body is a sequence of self-contained **insight clusters**. Each cluster is one
"raise a problem -> prove it -> solve it" unit. A reader can act on any single cluster, and the
clusters roll up into one suggestion set.

## Per-cluster chain (8 steps)

1. **Insight** — the cluster's headline claim, one sentence.
2. **Data / observed fact** — the evidence. Express comparisons in **% / normalized terms as the
   common scale**; avoid raw absolutes unless the absolute is the point. One reference frame lets
   every metric and insight be compared on one basis.
3. **Noise-vs-signal gate** — before concluding, ask: is the gap real or noise? A tiny spread or
   inconsistent pattern is noise -> drop it; a clear, consistent, sizeable gap is signal -> keep.
   Label which is which. This is the noise rung of the Baseline -> Noise -> Impact ladder in
   `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.
4. **Deep-dive cross-filter (multi-layer drill-down)** — do not stop at one chart. Layer 1: the
   overall pattern. Layer 2: filter into the extreme group (highest / lowest) and cut by a
   suspected factor to see what trait that group carries. Conclusion: confirm whether the factors
   are actually linked (interaction / effect link), e.g. compare in-group correlation vs overall.
   Caution: **SUM can hide Layer 1** — a small group sums low even when its average is high, so use
   averages/medians. Tooling: cross-filter or drill-through; when presenting, click the filter live.
5. **Hypothesis** — why the pattern exists. (Diagnostic depth:
   `${CLAUDE_PLUGIN_ROOT}/skills/da/references/mode-insight.md`.)
6. **Conclusion** — what it means. If it is a paradox, **name the subject explicitly** (who/what
   the paradox is about); never let the audience guess.
7. **Suggestion** — tied to a concrete number + which group to target + that group's traits + why.
   Use the 8-field Action Brief in
   `${CLAUDE_PLUGIN_ROOT}/skills/da/references/universal-workflow-rules.md`.
8. **Expected result** — set a quantified expectation: lift X% to reach YYY (revenue, +metric,
   etc.). A suggestion without an expected number is half-finished.

## Two assembly directions (pick per report)

- **Bottom-up (cluster-first):** each cluster ends with its own suggestion; link
  suggestion <-> insight <-> reason; the cluster is self-contained. Default for analysis reports.
- **Top-down (suggestion-first):** collect all suggestions, then trace each back to the insight(s)
  / data that support it; group suggestions that share evidence and present them together. Use when
  the deliverable leads with "here are the actions" and evidence is shared across actions.

## Headline rule

Pick the ONE significant insight and make it the headline (exec summary / overview action title).
A topic-noun page title ("Overview", "Marketing") is not a headline; an insight sentence is.

## Composes existing references (do not duplicate)

| Step / part | Reference |
|-------------|-----------|
| Opener (SCQR + Key Terms + Impact Cards) | `narrative-template.md` |
| Numeric rigor (noise rung) + 8-field Action Brief | `universal-workflow-rules.md` |
| Diagnostic depth (Descriptive -> Diagnostic -> Prescriptive) | `mode-insight.md` |
| Chart self-containment + storytelling | `storytelling-with-data.md` |
| Full report workflow | `mode-report.md` |

## Worked example (the drill-down)

Anxiety by school policy looked flat on SUM (Strict Ban summed lowest because it had the fewest
students). On AVERAGE, Strict Ban anxiety was highest (4.95 vs ~4.2). Layer 2: filter into Strict
Ban, cut by AI dependency -> anxiety rose Low 4.15, Mid 5.46, High 8.34. Conclusion: the ban's cost
lands on AI-dependent students (in-group correlation 0.48 vs overall 0.27). That is one full
cluster: insight -> data(%) -> noise gate -> drill-down -> hypothesis -> conclusion -> suggestion
(target high-dependency students with a transition plan) -> expected result.
