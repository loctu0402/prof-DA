# mcp/ — wiring your DA workflow's connectors

prof-DA does the analysis, but it can only use the data and tools your machine is connected to as MCP
servers. This folder is the connector-setup section:

- **`README.md`** (this file) — the guided, credential-free setup flow.
- **`example-org-mcp.json`** — a drop-in placeholder config for `~/.claude.json` (user scope): the org data
  gateway + NL->SQL agent, with CLI install commands. Placeholders only; never commit a real SERVER_ID or key.

This is a SETUP FLOW, not a server bundle: it ships NO credentials and tells you (and Claude) how to register
and authenticate each MCP so they show up in `claude mcp list` / `/mcp` before you analyze. Every secret is a
placeholder you fill locally. Engine-agnostic: the five connectors below are a TYPICAL DA workflow stack —
substitute the ones your org actually uses.

## Orientation — what you are wiring

| Connector (example) | Purpose in the workflow | Setup type | Auth |
|---------------------|-------------------------|-----------|------|
| Org data gateway (`<org-data-mcp>`) | Org data: semantic cube, data portal, journey, event tracking | `claude mcp add` (mcp-remote) | browser OAuth + org VPN |
| Web search (e.g. exa) | Research / web lookup | `claude mcp add` (HTTP) | API key (in URL) |
| Google Drive | Read/write Drive for an automation-report flow | claude.ai connector | Google OAuth |
| Gmail | Send/read mail for an automation-report flow | claude.ai connector | Google OAuth |
| Playwright / Chrome | Browser review tool | `claude mcp add` (ON-DEMAND) | none |

Two rules baked in: Drive + Gmail are claude.ai NATIVE connectors (enabled in connector settings, not
`claude mcp add`). Playwright/Chrome spawn Chromium (~200MB) so add ON-DEMAND only, never auto-start.

## Step 0 — see what is already wired

```bash
claude mcp list
```

Each healthy server shows `- Connected`. Skip any step whose server is already Connected — re-adding a working
server creates duplicate tools. Fix anything `Needs authentication` / `Pending approval`.

## 1. Org data gateway (`<org-data-mcp>`)

The unified gateway (semantic cube + data portal + journey + event tracking). The host is stable; the per-team
`<SERVER_ID>` is the only variable. Prereq: be on your org VPN, get your `<SERVER_ID>` from your data-platform
team. Never commit a real SERVER_ID.

```bash
claude mcp add -s user <org-data-mcp> -- cmd /c npx -y mcp-remote https://<MCP_GATEWAY_HOST>/servers/<SERVER_ID>/mcp
```

Then trigger the one-time login:

```bash
claude        # on first connect, mcp-remote opens a browser for OAuth; approve, token caches in ~/.mcp-auth
```

On mac/linux, drop `cmd /c` and call `npx` directly. The JSON drop-in form is in `example-org-mcp.json`.

## 2. Web search (e.g. exa)

```bash
claude mcp add -s user --transport http exa "https://mcp.exa.ai/mcp?exaApiKey=<EXA_API_KEY>"
```

Get `<EXA_API_KEY>` from the provider dashboard. Security: the key sits in the URL in plaintext in your config,
so treat it as a secret, do not commit it, rotate if it leaks.

## 3. Google Drive + Gmail (claude.ai connectors)

NOT `claude mcp add` servers. Enable as claude.ai connectors: open Claude settings -> Connectors, enable
"Google Drive" and "Gmail", click Connect on each, sign in with Google OAuth, grant scope. If `claude mcp list`
later shows "Needs authentication", re-connect to refresh the token. These power an automation-report flow:
read source docs from Drive, deliver the report by mail.

## 4. Playwright / Chrome (browser review — ON-DEMAND)

Heavy (spawns Chromium). Add only when doing browser-based review, remove when done:

```bash
claude mcp add -s user playwright -- npx -y @playwright/mcp@latest
```

Do NOT keep this always-on. Wire it for the task, not the session.

## 5. Verify

```bash
claude mcp list        # every target server shows - Connected
```

Inside a session, `/mcp` lists the active servers and their tools. prof-DA's modes then see the data + search
connectors automatically.

## Advanced — bundle with userConfig (optional, usually skip)

If you ever want a server to install + prompt for its value AS PART OF a plugin (instead of `claude mcp add`),
a plugin can ship a `.mcp.json` using `${user_config.*}` placeholders plus a `userConfig` block (prompted at
enable time). Caveat: bundled servers auto-start with the plugin, cannot be disabled individually, and would
DUPLICATE any server already registered at user scope. That is why the robust default is the guide above.

## Why a guide, not a bundle

Your org data + web-search servers are typically already registered at user scope and working; Drive/Gmail can
only be claude.ai connectors; Playwright must stay on-demand. Bundling would duplicate tools and auto-fail
off-VPN. So the robust design is a guide: Claude reads this flow and walks you (or a fresh machine) through the
exact steps. No secrets ship; you authenticate locally.
