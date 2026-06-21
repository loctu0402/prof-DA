# Lifecycle Execution Rules (7 phases, what each one actually does)

> Companion to `delivery-lifecycle.md` (the router: phase -> principle -> output -> rule ->
> mode). This file adds the EXECUTION depth the router defers: per phase, the artifact produced, the
> step procedure, the aspects to cover, and the done-gate.
> Each phase still defers its binding enforcement to the linked rule.

## Contract per phase
Every phase carries five parts and none may be blank: (a) **Produces** the artifact, (b) **Procedure**
the ordered steps, (c) **Aspects** the cover-checklist, (d) **Done-gate** the pass/fail, plus a
a good-vs-bad example. A phase is not done because it "feels" addressed; it is done when its
gate passes.

---

## Phase 1 - DISCOVER (intent, goals, scope)
- **Produces:** Business Intent doc / charter: problem statement (no solution), measurable outcome
  metric with a baseline, scope (in / out / defer), stakeholders + decision-rights, constraints, an
  opened RAID log.
- **Procedure:** (1) Elicit the real problem (5-Whys, not the proposed solution). (2) Write the
  problem statement `[who] + [problem] + [context] + [consequence]`, no solution words. (3) Fix the
  outcome metric (behaviour/number from X to Y, baseline X required). (4) Fill BACCM 6 lenses; a blank
  lens is an elicitation gap. (5) List stakeholders + who decides. (6) Draw scope: in / out (written) /
  defer. (7) Open RAID with the top assumptions and risks.
- **Aspects:** problem-not-solution, measurable outcome + baseline, stakeholders + decision-rights,
  explicit out-of-scope, constraints (time/budget/tech/compliance), success definition, surfaced assumptions.
- **Done-gate:** problem stated in one sentence with no solution named; outcome is a measurable change
  with a baseline; out-of-scope written; top assumptions logged. Any "no" -> not ready for MODEL.

## Phase 2 - MODEL (actors, rules, domain, edge cases)
- **Produces:** domain model (entities + attributes + grain + relationships), actor list with
  triggers, business-rule list (always/never), edge-case catalog, the bounded-context boundary.
- **Procedure:** (1) Event-storming lite (list the events in order). (2) Identify actors (who triggers
  what). (3) Identify entities + keys + **grain** (1 row = ?) + cardinality. (4) Write testable
  business rules. (5) Enumerate edge cases (empty/duplicate/out-of-range/concurrent/missing) with
  intended behaviour. (6) Mark the bounded context (in-system vs upstream/downstream, owned by whom).
- **Aspects:** actors + triggers, entities + counted grain + keys, relationships/cardinality, testable
  rules, edge cases + behaviour, context boundary, sources + their grain.
- **Done-gate:** every entity states its grain; every rule is testable; top edge cases have defined
  behaviour. For data work the grain is COUNTED, not assumed (`COUNT(*) = COUNT(DISTINCT key)`).

## Phase 3 - SPECIFY (BR -> UC -> Entity -> AC -> API)
- **Produces:** a layered spec walking `BR -> UC -> Entity/Data model -> AC -> API/interface contract`,
  plus NFRs.
- **Procedure:** (1) BR: the why, traced to the DISCOVER outcome. (2) UC: who does what, main +
  alternate/exception flows. (3) Entity/data model: concrete schema from MODEL. (4) AC: Given-When-Then
  or checklist per UC. (5) API/interface contract: inputs/outputs/errors. (6) NFRs: numbered, testable.
  Just-enough docs, updated often - neither big-upfront nor superficial.
- **Aspects:** traceability (each spec line -> a BR -> the outcome), AC per UC, data contract,
  interface contract, numbered NFRs, restated out-of-scope, alternate/exception flows (not only happy path).
- **Done-gate:** every UC has >=1 user-facing testable AC; data + interface contract explicit; a
  stranger can build from the spec without asking you = DoR met.

## Phase 4 - REVIEW (PO value, tech-lead, BA check)
- **Produces:** an approved spec (sign-off), surfaced options/risks, a decision log, updated RAID.
- **Procedure:** (1) PO/value lens (highest-value? serves the outcome?). (2) Tech-lead lens (sound,
  simplest-that-works, architectural risk?). (3) BA lens (complete, consistent, testable, traceable?).
  (4) Push back: surface alternatives, name assumptions, challenge scope. (5) Decision log (choice +
  why + rejected alternatives). (6) Update RAID.
- **Aspects:** value-fit, technical soundness + simplicity, requirement completeness/consistency/
  testability, >=1 genuine alternative considered, named risks, decision log.
- **Done-gate:** >=1 alternative genuinely considered and the choice justified; no blocking ambiguity;
  spec signed-off. For agent work: assumptions surfaced, not silently chosen.

## Phase 5 - DELIVER (AI writes, human finishes, review)
- **Produces:** code + unit tests + docs in chunked commits (1 task = 1 commit), each tracing to a spec line.
- **Procedure (chunked-delivery loop):** (0) spec-or-STOP; (1) clean baseline; (2) plan into tasks; (3)
  one approval checkpoint; (4) per task RED -> GREEN -> build -> commit (surgical, never `git add -A`);
  (5) per-task verify gate (red = stop); (6) stop-on-error / stop-on-risk (irreversibility stop-list);
  (7) summarize. AI proposes/writes to pattern; the human decides and is accountable.
- **Aspects:** 1 task = 1 commit, test-first, verify each task, no adjacent-code edits, stop at
  irreversible actions, keep the spec->code trace.
- **Done-gate:** every task's verify is green; each commit traces to a spec line; no drive-by changes;
  the stop-list was honoured.

## Phase 6 - VALIDATE (test vs AC, integration, regression)
- **Produces:** evidence that AC pass (quality verified), at the right rung of the evidence ladder.
- **Procedure:** (1) run each AC as a test (pass/fail); (2) integration test on real input; (3)
  regression; (4) for AI/RAG: evals (groundedness, hallucination, retrieval hit-rate); (5) evidence at
  the right rung (run output / rendered artifact / corrected real number) - "looks right" is banned;
  (6) independent reconcile: diff delivered vs each captured requirement (MET/PARTIAL/MISSED).
- **Aspects:** every AC has evidence, integration on real data, regression, NFRs measured not assumed,
  evidence rung >=4 (validator exit 0 + output shown), independent requirement diff, presence-proof.
- **Done-gate:** every AC has evidence at rung >=4; no requirement MISSED in the independent diff;
  every artifact has presence-proof (exists on disk/URL).

## Phase 7 - LEARN (feedback, update the spec)
- **Produces:** an evolved spec + a durably codified lesson (template/rule/memory) + a retro action +
  next-loop backlog.
- **Procedure:** (1) collect feedback from 3 loops (user/data/system); (2) root-cause each gap (not the
  symptom); (3) update the spec so it stays source-of-truth; (4) codify (stable result -> template;
  correction -> rule/memory); (5) retro (one keep, one fix); (6) feed the next-loop backlog; the loop
  returns to DISCOVER.
- **Aspects:** feedback from all 3 loops, root-cause not symptom, spec updated, lesson codified durably,
  retro action, next-loop backlog.
- **Done-gate:** the spec reflects what was learned; >=1 durable artifact updated; the loop is closed
  (feedback -> change -> verified).

---

## Track lean per phase (which methodology flavour)
DISCOVER + SPECIFY lean **predictive** (understand/specify before building). DELIVER + VALIDATE + LEARN
lean **adaptive** (iterate, demo, learn). MODEL + REVIEW use both. The fork and decision rule are in
`adaptive-vs-predictive.md`. The 7 phases are the hybrid spine that fuses the two tracks; this is
not "choose one methodology", it is "each phase leans the way its uncertainty demands".
