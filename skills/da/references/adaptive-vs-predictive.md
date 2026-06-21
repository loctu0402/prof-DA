# Adaptive (Agile/Scrum) vs Predictive (BABOK) - two tracks

> Two philosophies, not two vocabularies. Companions: `lifecycle-execution-rules.md` (the hybrid
> spine), `delivery-lifecycle.md` (the router).

## The two philosophies
- **Predictive (BABOK / plan-driven):** understand and specify enough before building; the plan is a
  contract; progress = signed phase gates; change is controlled. Heritage: IIBA BABOK, requirements
  engineering. Guards against building the wrong thing before you understood it.
- **Adaptive (Agile/Scrum):** build a small running increment, learn from feedback, change cheaply;
  the plan is a hypothesis; progress = a working increment each sprint; change is embraced. Heritage:
  Agile Manifesto, Scrum, XP. Guards against freezing the wrong plan too early.

Neither means what people assume. Predictive is not "heavy waterfall docs" (it can be lean). Adaptive
is not "no plan / no docs" (it keeps a governed backlog, AC, DoD). They differ on *when requirements
are fixed* and *whether change is cheap or expensive*.

## The decision rule (choose per-decision, not per-project)
Score the decision against five factors; lean to whichever side wins the majority:

| Factor | Lean Predictive | Lean Adaptive |
|---|---|---|
| Requirement | stable, known up front | vague, emerges while doing |
| Cost of change | expensive / irreversible (prod, money, contract) | cheap, quick to redo |
| Compliance | regulated, needs audit trail + sign-off | internal, free |
| Feedback latency | slow, must be right first time | fast, learn from user/data each loop |
| Stakeholders | many, need consensus + sign-off | few, you + one sponsor |

Most real projects are hybrid: the contract part goes predictive, the discovery part goes adaptive.
DA examples: a daily-report pipeline cutover to dbt leans predictive (contract right before cutover,
parity gate, sign-off, RTM legacy->dbt); an exploratory forecast/root-cause leans adaptive (method
emerges - try DiD, placebo fails, switch to RD = inspect-and-adapt).

## Track Predictive (BABOK) - artifacts + execution rules
- **BACCM** (6 concepts) - analyse a change from all angles before fixing a solution; a blank lens is
  an elicitation gap.
- **Elicitation** - structured requirement gathering (interview, document analysis, observation,
  workshop); record each requirement's source.
- **BRD / FRD / SRS** - full spec of what-it-must-do + quality; lean IEEE 830; each requirement atomic,
  testable, numbered for trace.
- **RACI** - one Accountable per item; Responsible can be many.
- **RTM (requirements traceability matrix)** - link each requirement to design/code/test; no orphan
  requirement, every requirement has >=1 test.
- **Phase gate / sign-off** - explicit entry + exit criteria + a named signer per stage.
- **Change control** - post-baseline changes go through impact assessment + re-approval, never silent edits.

Mindset: baseline the plan; measure change against the baseline. Strong when errors are expensive and
many stakeholders must agree. Weak when requirements are vague (you specify the wrong thing confidently).

## Track Adaptive (Agile/Scrum) - artifacts + execution rules
- **Product backlog** - prioritized, emergent queue ordered by value + risk; refined continuously.
- **User story** - smallest unit of value, delivered in one pass; Connextra + INVEST + 3C; each has AC.
- **Sprint** - fixed timebox producing a running increment; scope locked within the sprint.
- **Sprint planning / daily standup / review-demo / retro** - planning takes only DoR-ready stories;
  standup surfaces blockers fast; review runs a real demo ("not running = not done"); retro yields one
  keep + one fix with an owner.
- **DoR / DoD** - the entry and exit gates; defined once, reused.
- **Velocity / burndown** - forecast the next sprint; never a tool to judge people.

Mindset: the plan is a hypothesis, each increment an experiment. Strong when requirements are vague and
feedback is fast. Weak when you must be right first time (no learning loop before the consequence).
Solo adaptation: sprint-of-one, WIP=1, story = one Claude task unit verified by AC.

## The hybrid spine (Lean Spec Delivery)
The 7 phases fuse both: predictive front (DISCOVER, SPECIFY), adaptive middle/back (DELIVER, VALIDATE,
LEARN), both at MODEL/REVIEW/Ship. Phase-to-track mapping lives in `lifecycle-execution-rules.md`.
Principle: enough predictive to not build the wrong thing, enough adaptive to not freeze the wrong
plan. This is "each phase leans the way its uncertainty demands", not
"pick one methodology".

## Common mistakes
- "Agile means no docs" - false; adaptive keeps backlog, AC, DoD.
- "BABOK is rigid waterfall" - false; BABOK can be lean, it just fixes requirements earlier when error
  is expensive.
- Mixing vocabulary without the mindset - calling it a "sprint" while change-controlling every line is
  predictive in adaptive clothing. Ask "is this change cheap or expensive?" to know the track.
- Choosing a track for the whole project - choose per decision instead.
