---
name: deliver
description: DESIGN PLACEHOLDER - prof-DA deliver mode for GitHub Copilot (the build-auto execution loop). Build deferred.
---

[FILL when building] Copilot agent files MUST use the `.agent.md` suffix and are invoked via `@deliver`.
Mirror the deliver mode: load `skills/da/references/build-auto.md` + `evidence-based-done.md` +
`execution-discipline.md`; run the 7-gate loop (spec-or-STOP, clean baseline, single batch approval,
per-task RED -> GREEN -> build -> commit + verify gate, stop-on-error/risk, evidence summary). Before done,
the gate runs in CI (`.github/workflows/gate.yml`). Tool names: `adapters/toolmaps/_toolmap.md` (Copilot column).
