# Lean-Spec Delivery Lifecycle (phase -> prof-DA mode map)

> The A-Z spine for a whole DA engagement. The 7-phase Lean Spec Delivery lifecycle mapped to the
> prof-DA mode(s) that execute each phase and the gate each produces. A router map; follow the named
> mode reference for the binding behavior. Self-contained. Distilled from the Lean Spec Delivery post.

## Grain and scope
One unit = a whole DA engagement (kickoff to ship to learn). In scope: the 7 phases -> modes -> gates.
Out of scope: the per-mode mechanics (those live in each `mode-*.md`).

## The 7 principles (one line each)
Intent First (why + value + measure before "build this") · Collaborative Discovery (agree actors / rules
/ edge cases first) · Layered Specifications (just-enough docs, updated often) · AI as Accelerator (AI
proposes, the human is accountable) · Traceable Delivery (from code find the spec, from spec the intent)
· Acceptance-driven Validation (tests + AC are the contract with AI) · Continuous Learning (the spec is a
living document).

## Phase -> mode -> gate
| Phase | Intent | prof-DA mode(s) | Gate produced |
|---|---|---|---|
| DISCOVER | understand the ask, the value, the scope | frame | a charter (business understanding) |
| MODEL | metric + data plan + schema | frame, model, query | a metric contract, a DWH/mart design |
| SPECIFY | lock the plan / spec | frame (planning-protocol), report (template spec), submit (section contract) | a locked spec / contract |
| REVIEW | a second perspective before building | review | plan approved |
| DELIVER | build it | deliver (build-auto), process, query, report, automate | committed artifacts + a receipt |
| VALIDATE | prove it against AC | submit, review, fix + the Stop hook | validators green, deliverable proven |
| LEARN | capture the lesson | workspace | a rule / template / memory update |

## IF / DO-NOT routing (which phase am I in -> which mode)
- IF "I do not know where to start / what metric": DISCOVER -> `/frame`.
- IF "design the schema / mart / dbt model": MODEL -> `/model`.
- IF "pull the data / breakdown / trend": MODEL or DELIVER -> `/query`.
- IF "build the pipeline / features / forecast": DELIVER -> `/process` (run it under `/deliver` for the gated loop).
- IF "build the stakeholder report / dashboard": DELIVER -> `/report`.
- IF "is it good / audit it": REVIEW -> `/review`. IF "is it complete + submit-ready": VALIDATE -> `/submit`.
- IF "it is broken / wrong number": VALIDATE -> `/fix`.
- DO NOT treat the whole engagement as one mode; route each phase.

## The SPECIFY ladder
BR (why) -> UC (who does what) -> Entity / Data Model (with which concepts) -> AC (how we know it is
right) -> API / interface contract (if any). The binding DoR / DoD / AC scaffold + the per-section unit
discipline live in `planning-protocol.md` + `recurring-report-contract.md`.

## The feedback loop (LEARN spans all phases)
Every bug, new feature, and piece of feedback updates the spec so it stays the source of truth: a shipped
stable result is codified into a template; a correction becomes a rule / profile. The lifecycle is a loop.
