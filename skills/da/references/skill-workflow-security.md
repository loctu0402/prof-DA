# Reference — Skill / Workflow Security Scan

> When this plugin authors or audits an agent package (a skill, workflow, plugin, hook, or generator),
> run a security scan before shipping it. Authoring agent packages is a real attack surface: a SKILL.md
> can carry prompt-injection, a script can harvest `os.environ` and POST it out, a manifest can
> over-grant tools. Scanner: `skills/da/scripts/validators/skill_security_scan.py` (stdlib, no deps).

## What it checks (8 curated categories)
A high-value subset of the SkillSpector catalog, two engines (regex content + Python AST):

| Category | Catches |
|---|---|
| prompt-injection | instruction-override phrases, hidden/zero-width characters |
| system-prompt-leak | "reveal / print / repeat your system prompt / everything above" |
| data-exfiltration | env harvesting, outbound posts of local data, reading `.env`, shell upload |
| excessive-agency | `rm -rf`, `shell=True`, `os.system`, `sudo` |
| supply-chain | pipe-to-shell (`curl ... | bash`), pip-from-URL, unpinned deps |
| tool-misuse | `eval` / `exec` / `compile` / `__import__` / `pickle.loads` |
| secret-hardcode | AWS/GitLab/GitHub/Slack/Google tokens, JWT, private keys, `api_key="..."` |
| mcp-least-privilege | a wildcard tool/permission grant in a manifest |

## Run it
```bash
python skills/da/scripts/validators/skill_security_scan.py <package-folder>            # terminal report
python skills/da/scripts/validators/skill_security_scan.py <folder> --json             # machine report
python skills/da/scripts/validators/skill_security_scan.py <folder> --fail-on critical # gate
```

## Reading the result (a TRIAGE tool, not an oracle)
Stage-1 static scanning is high recall, moderate precision by design (the SkillSpector Stage-2 LLM pass
is not ported). Two numbers, decoupled on purpose:
- **score / band (0-100)** = accumulated risk SURFACE - informational. Legit subprocess calls inflate it.
- **verdict** = the single most-severe finding - what a gate acts on, tunable via `--fail-on`.

Legitimate code triggers checks (a workflow that runs a CLI via subprocess, a doc that mentions `eval`).
Triage each finding; for a confirmed-safe line add a trailing `# nosec` comment and the scanner drops
every finding on that line. A package reaches a clean gate when no UNSUPPRESSED finding sits at or above
the `--fail-on` threshold (use `--fail-on critical` to block only on eval/exec, embedded keys,
pipe-to-shell, prompt-injection - never ship those).

## Where to invoke
- After authoring a skill / workflow / plugin / hook (the `deliver` / `workspace` modes): scan before
  declaring done; resolve or `# nosec` every finding at or above the gate threshold.
- In `review` mode when the target is an agent package: a HIGH/CRITICAL verdict = do not ship until reviewed.
- Before installing a third-party skill: scan the unpacked folder first.

## Honest limits
It detects PATTERNS, not intent - it will both miss a cleverly obfuscated payload and flag benign code.
It is one layer, not a guarantee. `# nosec` is a human attestation, only as good as the review behind it.
