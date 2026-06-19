# A8 Idea-Verification — DESIGN SPEC

> Archetype: **A8 Idea-Verification** · Channel: single-file HTML · Density: compact
> Purpose: economics pre-check for a proposed scheme, tier, or incentive before launch.
> Spec-only — no boilerplate produced here.

---

## 0. Frame

**Job-to-be-done:** Let a decision-maker accept, reject, or conditionally approve a proposed
scheme by seeing its economics and challenging every assumption.

**Signature:** transparent math + explicit, challengeable assumptions — the reader must be
able to reproduce every number from the spec without asking the author.

**Not this archetype:** exploratory dashboards, trend reports, KPI monitors. Use A8 only
when the output is a single Go / No-go / Conditional verdict on a well-defined proposal.

---

## 1. Information Architecture

| # | Section | Purpose |
|---|---------|---------|
| 1 | Hypothesis statement | The proposal in one sentence + the decision it informs. |
| 2 | Assumptions + rationale table | Each input assumption, its source, rationale, and sensitivity flag. |
| 3 | Transparent formula + worked calculation | Every formula visible; every computed row has a plain-language reading. |
| 4 | Go / No-go / Conditional verdict | Explicit verdict chip + the trigger conditions that could change it. |
| 5 | Sensitivity table (worst / base / best) | Outcome under three assumption sets. |

Reading path: top-down. A skeptic reads the assumptions table and the math before the
verdict, not after.

---

## 2. Section Specifications

### 2.1 Hypothesis Statement

One declarative sentence stating:
- What is being proposed (the scheme, tier, rule, or incentive).
- What outcome it is expected to produce (the predicted effect, with magnitude if known).
- What decision this analysis informs (launch, reject, redesign, pilot).

Format: action-title voice, no hedge words ("might", "could possibly").

Example structure (generic):
> "Proposed [scheme type] targeting [segment] is expected to produce [outcome metric] of
> [target magnitude] over [time horizon], informing a launch / no-launch decision by
> [decision date]."

### 2.2 Assumptions + Rationale Table

Every numeric input to the model must appear here. No assumption is silent.

Required columns:

| Column | Content |
|--------|---------|
| Assumption | The variable name and value used in the base-case calculation. |
| Source | Where the value comes from (historical average, benchmarked range, expert estimate, regulatory constraint). |
| Rationale | One sentence: why this value and not another. |
| Sensitivity flag | HIGH / MED / LOW — how much the verdict changes if this assumption is wrong. Flag = HIGH when a 10% move in this assumption changes the verdict. |

Rules:
- Every assumption flagged HIGH must appear in the sensitivity table (Section 2.5).
- "Internal assumption" is not an acceptable source. Name the data, the period, and the method.
- No assumption may carry a value that is more optimistic than any comparable historical observation without a documented rationale for the exception.

### 2.3 Transparent Formula + Worked Calculation

Display the formula, then the substitution with actual base-case values, then the result.
Each row also carries a plain-language reading so a non-technical reader can verify the
logic without knowing the formula.

Required structure per computed quantity:

```
Formula:     [variable] = [expression]
Substituted: [variable] = [value_A] × [value_B] − [value_C]
Result:      [variable] = [number] [unit]
Reading:     "In plain terms: [one sentence describing what this number means]."
```

Rules:
- Every formula is shown explicitly. No opaque totals.
- Units are stated on every numeric output.
- The worked calculation uses base-case values. Scenario variants appear in Section 2.5.
- Breakeven quantities (if applicable) are solved explicitly:
  `Breakeven [X] = [cost term] ÷ [margin term]` with a plain reading of the threshold.
- Do not round intermediate values; round only the final display figure, and note rounding.

### 2.4 Go / No-go / Conditional Verdict

A single prominent verdict chip followed by the evidence and the trigger conditions.

Verdict options:

| Verdict | Meaning |
|---------|---------|
| **Go** | Base-case economics are positive; worst-case remains above breakeven; no blocking uncertainty. |
| **No-go** | Base-case or worst-case economics are negative; or a blocking assumption cannot be validated before launch. |
| **Conditional** | Base-case is positive but depends on one or more conditions that are not yet confirmed. List each condition explicitly. |

Required fields:
- Verdict chip (Go / No-go / Conditional).
- Primary evidence: the one or two numbers from Section 2.3 that drive the verdict.
- Trigger conditions (Conditional only): the specific assumptions or external facts that, if
  confirmed, convert Conditional to Go or No-go.
- Expiry: the date or event after which this analysis must be re-run (assumption staleness).

### 2.5 Sensitivity Table (Worst / Base / Best)

Shows the outcome metric for three assumption sets. Every HIGH-flag assumption from
Section 2.2 must vary across at least two of the three scenarios.

Required columns:

| Column | Content |
|--------|---------|
| Scenario | Worst / Base / Best |
| [Assumption A] | Value used in this scenario |
| [Assumption B] | Value used in this scenario |
| ... | (one column per HIGH-flag assumption) |
| Outcome metric | The primary KPI (revenue, cost, net margin, adoption rate, etc.) |
| vs. breakeven | Absolute and percent distance from the breakeven threshold |
| Verdict | Go / No-go / Conditional under this scenario |

Rules:
- Worst case: all HIGH-flag assumptions at their least favorable plausible value
  (not an extreme tail, but a realistic downside supported by historical range).
- Best case: all HIGH-flag assumptions at their most favorable plausible value
  (not a ceiling, but a realistic upside).
- Base case: the values from Section 2.3.
- The analyst must be able to defend each scenario boundary with the same rigor as
  Section 2.2 (source + rationale).

---

## 3. Visual and Layout

- Compact single-screen layout; math section may scroll.
- Theme tokens from the locked token contract (`shared/templates/_contract/THEME-TOKEN-CONTRACT.html`).
  Fork the token set 1:1; do not re-derive colors.
- Verdict chip uses status-tinted pill: success tone for Go, danger tone for No-go,
  warn tone for Conditional.
- Sensitivity flag column uses a desaturated status ramp: HIGH = danger-desaturated,
  MED = warn-desaturated, LOW = neutral.
- Accent color (from the forked theme) restrained to: section headings, the verdict chip,
  and the highest-sensitivity row in the assumptions table.
- All other structure (tables, cards, mono blocks) uses surface and border tokens only.

---

## 4. Interaction

Static by default. One optional behavior: collapsible formula derivation — a real
disclosure that shows the algebraic steps behind a non-obvious formula. Not decorative;
only include if the derivation is genuinely needed to challenge the result. No motion.

---

## 5. Fork Rules

When forking this archetype for a specific analysis:

1. **Do not change the IA order** (Sections 1–5). Additions go after Section 5 or as
   sub-sections within an existing section.
2. **Rename placeholders**: replace `[scheme type]`, `[segment]`, `[outcome metric]`,
   `[time horizon]` with the specific analysis values.
3. **Token fork**: copy from `THEME-TOKEN-CONTRACT.html`; choose one theme variant;
   do not mix token sets from different themes.
4. **Every assumption must pass the source test**: if you cannot name the data source
   and period, the assumption must be marked `[ESTIMATE — source needed]` and the
   verdict must be Conditional until it is resolved.
5. **Do not remove the Sensitivity table**: even if only one assumption is HIGH-flag,
   the table is required. It is the primary audit trail for the verdict.
6. **Breakeven is mandatory when the proposal has a cost**: no verdict without an
   explicit breakeven threshold and a plain reading of what it requires.

---

## 6. When to Use This Archetype

Use A8 when:
- A new scheme, tier, incentive, or rule change is being evaluated before launch.
- The decision is binary (or ternary: Go / No-go / Conditional).
- The economics can be expressed as a formula with identifiable assumptions.
- The audience includes at least one non-technical stakeholder who must be able to
  challenge the math.

Do not use A8 when:
- The goal is ongoing monitoring (use a dashboard archetype).
- The analysis is exploratory without a specific proposal to evaluate.
- The outcome cannot be quantified (use a qualitative decision memo instead).

---

## 7. Done-of-Definition (for spec validation)

A forked A8 instance passes review when:
- [ ] Every numeric input appears in the Assumptions table with source + rationale + flag.
- [ ] Every formula is shown with substituted base-case values and a plain-language reading.
- [ ] Breakeven is solved explicitly (where a cost exists).
- [ ] The verdict chip matches the base-case economics.
- [ ] The Sensitivity table covers all HIGH-flag assumptions across worst / base / best.
- [ ] Trigger conditions are listed for any Conditional verdict.
- [ ] Token set is forked from the contract (no freestyle hex values).
- [ ] No assumption is more optimistic than historical range without a documented rationale.
