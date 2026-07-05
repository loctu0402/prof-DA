# Evidence-Based Done

> The proof gate for every mode exit + the `build-auto.md` Gate 7. Defines what counts as PROOF that a
> deliverable is done. Self-contained. Companions: `execution-discipline.md` (the verify mindset),
> `build-auto.md` (the per-task gate), `report-standard-checklist.md` (the report pre-ship gates).

## Grain and scope
One unit = one moment of claiming a deliverable done. In scope: the evidence ladder, Presence-proof,
the built-but-unrun trap, DA evidence types. Out of scope: the per-section recurring-report contract
(that is `recurring-report-contract.md`), the global style audit (`self-check-protocol.md`).

## When to read (routing triggers)
- IF about to say "done / fixed / passing / shipped" on an artifact -> read this first.
- IF the deliverable is a file / commit / report / URL -> the Presence gate below is mandatory.
- DO NOT use this to define the section contract (that is recurring-report-contract.md).

## The evidence ladder (weakest to strongest)
Claim only at the rung you have evidence for:
1. "looks done" / "seems right" - BANNED as a done-claim.
2. "code written" - the file exists. NOT done (it may never run).
3. "code ran" - executed without error. Necessary, not sufficient (may produce wrong output).
4. "acceptance check passed" - a named validator / test returned exit 0.
5. "validator exit 0 + output shown" - the check passed AND the output is captured.
6. "corrected a real wrong number on live data" (before / after) - the strongest DA proof.

Never assert above the rung you can show. "All tests pass" with no test run is a rung-1 claim wearing a rung-4 label.

## Presence-proof (mandatory for artifact deliverables)
A requirement whose deliverable is a file / report / commit / URL CANNOT be MET on "I described it" or
"I planned it". Presence = the artifact EXISTS at the named path, is NON-EMPTY (not a stub), and
RAN / RENDERED (not just generated). Cite where it exists. If you cannot point to it, the verdict is
MISSED, not MET.

## The built-but-unrun trap
These are all rung-2 ("written"), routinely mislabeled done:
- Generating `generate_report.py` is NOT a rendered report.
- Writing a test is NOT a passing test.
- A query string is NOT executed data.
- A packager existing is NOT a packaged artifact.
The fix: RUN it end to end, OPEN the output, COUNT what came out, then claim.

## DA-specific evidence types
| Deliverable | The proof |
|---|---|
| A number / metric | re-run live; correct a real wrong value (before / after) |
| Grain of a table | `COUNT(*) = COUNT(DISTINCT key)` equal |
| An HTML / chart report | render-verify: rasterize headless (absolute path) or inspect geometry; route looks-good to the user |
| A migration / cutover | parallel-run diff: row count -> hash -> money 0.1% / count 0.5% |
| A pipeline | run with the live date, inspect the tail rows landed |
| A sent email | the send call returned ok (a draft is not a send) |

## Reproducible-deliverable form gate (harness / pipeline / eval / "process")
If the deliverable must be **reproducible / scale to many users / run on another machine or a different agent**,
Presence is NOT enough — the FORM matters. It must be **tested code + a CLI + a versioned contract**, NEVER a
prompt-driven agent or a markdown "flow". A markdown "flow" describing what an agent should do is a rung-1 claim;
the process is the runnable artifact + a passing test. Put the bar in the DoD as an EXECUTABLE acceptance
criterion (only code can meet it, so it forces a harness, not a prompt). The 5 forcing functions:

1. **DoD is an executable artifact** — "a `test_x.py` PROVES the property" (e.g. the extractor cannot emit the gold), not a requirement sentence.
2. **Cross-portability proof** — "another person clones + runs the CLI with ZERO code edits"; "runs on 1 non-Claude model via an env-selected per-role endpoint resolver, not `claude -p`".
3. **Reproducibility proof** — "it is a CLI; same input -> same output; unit tests per component".
4. **Fail-closed BY CONSTRUCTION** — a whitelist that can only emit N fields (a bug degrades to a missing field, never a leaked answer), not a prompt saying "please don't leak".
5. **Force iteration** — run -> deliberately break -> harden -> add a regression test. One-shot = no rigor.

HARD form-rule: never accept a markdown "flow" as "the process"; accept the runnable artifact + a passing test.
Applies to the `deliver` / `build-auto` / `model` modes when the build must scale or run elsewhere.
Canonical rule (workspace): `lt-memory/rules/build-reproducible-as-tested-code-not-prompt.md` (+ the 7 harness
best-practices); enforced by the workspace Stop hook `reproducible_artifact_gate.py`.

## How to apply (before any done-claim)
1. Name the rung you claim; confirm you have evidence at it.
2. For an artifact: prove Presence (path + non-empty + ran).
3. For code: a named validator / test at exit 0, output captured.
4. For a reproducible / harness / eval deliverable: the form gate above — code + test + CLI + a portability proof, not a markdown flow.
5. If you cannot prove it, do not claim done; say what is missing.

## Validator + receipt
`python scripts/validators/artifact_presence_check.py <project>/.prof-da/pending-validation.json`
(or `--deliverables a,b,c`) checks each artifact exists + non-empty + non-stub and reports the rung it
reached. The report and build-auto modes drop that receipt so the plugin Stop hook (`stop_gate.py`)
validates the named deliverables.
