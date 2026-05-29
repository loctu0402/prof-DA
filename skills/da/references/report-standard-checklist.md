# Report Standard Checklist (binding pre-ship gate)

> The single binding checklist every report/dashboard deliverable passes before "done". `[GATE]` = hard-stop
> (mechanical, machine-checkable via `scripts/validators/report_consistency_audit.py` + `self_check.py`).
> `[ADVISORY]` = scored by a human / `evaluation-rubric.md`, not auto-blocked. Same list every session ⇒
> every Claude session ships the same shape. The user may append items; the baseline below is mandatory.

## Run order

```bash
python scripts/validators/self_check.py <deliverable>        # orientation + ai-tell + action-brief + consistency
python scripts/validators/report_consistency_audit.py <file> # detail on the consistency gate
python scripts/validators/rubric_audit.py <file>             # ~30 rule checks (Rules 1-4 + style)
```
Any `[GATE]` failure ⇒ not shippable. Fix, re-run, then declare done.

## `[GATE]` — mechanical hard-stops

- [ ] **Orientation** present (SCQR / 3-line intro / How-to-read). — `orientation_block.py`
- [ ] **Numbers reconcile** across cards / tables / charts (back-derive headline from source). Verify the
      *rendered* value, not raw attributes (e.g. `data-countup="2964" data-fmt="tenth"` ⇒ 296.4 — not a bug).
- [ ] **No hallucinated number** — every figure traceable to a named query/source.
- [ ] **No empty-as-finding** — no `N/A` / `null` / `NaN` / `TODO` / unrendered `{{placeholder}}` in the body. — `report_consistency_audit.py`
- [ ] **Vietnamese diacritics** complete for stakeholder output (`ệ ỉ ổ à ă`). — `report_consistency_audit.py`
- [ ] **No AI-tells** — `===`, `-----`, em-dash, `≈`, `→` absent from stakeholder prose. — `ai_tell_scan.py`
- [ ] **Brand fidelity** — implemented from a locked template in `shared/templates/` (canonical palette/fonts);
      no per-report freestyle CSS when a locked template exists. — `project-scaffold.md`, mode-report A2
- [ ] **Project scaffold** exists (`queries/ cache/ scripts/ output/ data/`); deliverable not dumped flat. — `report_consistency_audit.py`
- [ ] **Portal published** — pushed via `shared/portal_upload.py` (72h TTL, stable UUID); receipt
      `latest_portal_url.json` saved. — mode-report Step 9 (skip only if user explicitly says "no link").
- [ ] **Output location** — under `output/` or `projects/<name>/output/`, never workspace root.
- [ ] **No auto-send** — saved + link shown; wait for explicit "send".

## `[ADVISORY]` — scored, not auto-blocked (evaluation-rubric.md)

- [ ] **Report flow** logical (Setup → Observation → Diagnostic → Decision); headings tell the story standalone.
- [ ] **Metric choice** fits the question; NSM vs drivers hierarchy explicit.
- [ ] **Why-Explanation** on every method / threshold / chart-type / framework choice (Rule 4).
- [ ] **Baseline → Noise → Impact** ladder on every headline number (Rule 2).
- [ ] **Diagnostic not descriptive** — Connect-the-Dots (Fact → Mechanism → Behavior → Impact → Evidence);
      hot spots investigated, not just flagged "cần confirm".
- [ ] **External / market context** when cross-period or competitive (rates, gold, VNI, competitor benchmark).
- [ ] **Per-chart takeaway** verdict under every chart; chart choice follows SWD (no pie / no 3D, action titles).
- [ ] **Interaction** — data-card-on-hover shows full underlying data; email forces light-mode.
- [ ] **Natural Vietnamese tone** — reads native, not word-by-word machine translation; register fits audience.
- [ ] **Business-language over jargon** — <product-b> / z-score / σ translated to VN business terms in UI labels.
- [ ] **Anti-bias** — negative findings carry a counter-argument / recovery signal; structural vs cyclical split.
- [ ] **Idempotency** — re-run gives same result; single source of truth (no `.md`-vs-`.html` number drift).

## Verdict

Compute the `evaluation-rubric.md` weighted grade + write the 1-paragraph Ship / Fix-then-ship / Rebuild
verdict. `[GATE]` PASS is necessary but not sufficient — a grade-D report can pass every gate and still need
rework.

## Cross-references
- Scored rubric → `evaluation-rubric.md`
- Pre-ship sections A-N → `self-check-protocol.md`
- Scaffold / portal / design-handoff → `project-scaffold.md`, `mode-report.md`
