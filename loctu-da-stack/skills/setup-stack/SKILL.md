---
name: setup-stack
description: Guided setup for the DA workflow MCP stack - walks the user through connecting <organization> Data Portal (<org-data-mcp>), exa web search, Google Drive + Gmail, and on-demand Playwright/Chrome. Ships no credentials; uses placeholders + local login. Use when the user wants to install, connect, wire, re-auth, or troubleshoot MCP connectors, or onboard a new machine. Triggers on "set up MCP", "connect MCP", "kết nối MCP", "cài MCP", "add <org-data-mcp>", "add exa", "wire my data stack", "MCP không hiện", "MCP not showing", "onboard máy mới", or /setup-stack.
---

# Setup the DA workflow MCP stack

This skill is a SETUP FLOW, not a server bundle. It ships no credentials. It tells you (and Claude) exactly how to register and authenticate each MCP the DA workflow needs, so they appear in `claude mcp list` and `/mcp` before you start working. Every secret is a placeholder you fill locally.

## Orientation: what you are wiring

| MCP | Purpose in the workflow | Setup type | Auth |
|-----|------------------------|-----------|------|
| <organization> Data Portal (`<org-data-mcp>`) | Org data: semantic cube, data portal, journey, <event-system> | `claude mcp add` (mcp-remote) | browser OAuth + <organization> VPN |
| exa | Web search / research | `claude mcp add` (HTTP) | API key (in URL) |
| Google Drive | Read/write Drive for the automation-report flow | claude.ai connector | Google OAuth |
| Gmail | Send/read mail for the automation-report flow | claude.ai connector | Google OAuth |
| Playwright / Chrome | Browser review tool | `claude mcp add` (ON-DEMAND) | none |

Two rules baked in: Drive + Gmail are claude.ai NATIVE connectors (enabled in connector settings, not `claude mcp add`). Playwright/Chrome spawn Chromium (~200MB) -> add ON-DEMAND only, never auto-start.

## Step 0 - see what is already wired

```bash
claude mcp list
```

Each healthy server shows `- Connected`. Anything missing, `Needs authentication`, or `Pending approval` is what this flow fixes. Skip any step whose server is already Connected - do not re-add a working server (it creates duplicate tools).

## 1. <organization> Data Portal (`<org-data-mcp>`)

The unified <organization> gateway (semantic cube + data portal + journey + <event-system>). The gateway host is stable; the per-team `<SERVER_ID>` is the only variable.

Prereq: be on your org VPN, and get your team `<SERVER_ID>` from your data-platform team. Never commit a real SERVER_ID.

```bash
claude mcp add -s user <org-data-mcp> -- cmd /c npx -y mcp-remote https://<MCP_GATEWAY_HOST>/servers/<SERVER_ID>/mcp
```

Then trigger the one-time login:

```bash
claude        # on first connect, mcp-remote opens a browser for OAuth; approve, token caches in ~/.mcp-auth
```

Notes: the connector was rebranded "<organization> Data Portal MCP" (2026-05-26) - the `claude mcp add` key, gateway, and OAuth are all unchanged, so this recipe still holds. On mac/linux, drop `cmd /c` and call `npx` directly.

## 2. exa (web search)

```bash
claude mcp add -s user --transport http exa "https://mcp.exa.ai/mcp?exaApiKey=<EXA_API_KEY>"
```

Get `<EXA_API_KEY>` from the exa dashboard (exa.ai -> API keys). Security: the key sits in the URL in plaintext in your config -> treat it as a secret, do not commit it, rotate if it leaks.

## 3. Google Drive + Gmail (claude.ai connectors)

These are NOT `claude mcp add` servers. Enable them as claude.ai connectors:

1. Open Claude settings -> Connectors (or the connector picker in the composer).
2. Enable "Google Drive" and "Gmail".
3. Click Connect on each -> sign in with Google OAuth -> grant scope.
4. If `claude mcp list` later shows "Needs authentication", re-connect to refresh the token.

These power the automation-report flow: read source docs from Drive, deliver the report by mail.

## 4. Playwright / Chrome (browser review - ON-DEMAND)

Heavy (spawns Chromium). Add only when doing browser-based review work, and remove when done:

```bash
claude mcp add -s user playwright -- npx -y @playwright/mcp@latest
```

Do NOT keep this always-on. Per the on-demand-browser rule, wire it for the task, not the session. Chrome-control connectors follow the same on-demand discipline.

## 5. Verify

```bash
claude mcp list        # every target server shows - Connected
```

Inside a session, `/mcp` lists the active servers and their tools. prof-DA's modes then see `<org-data-mcp>` + `exa` automatically.

## Advanced - bundle with userConfig (optional, usually skip)

If you ever want a server to install + prompt for its value AS PART OF a plugin (instead of `claude mcp add`), a plugin can ship a `.mcp.json` using `${user_config.*}` placeholders plus a `userConfig` block (prompted at enable time). See `mcp/example-stack-mcp.json` for the exact shape. Caveat: bundled servers auto-start with the plugin, cannot be disabled individually, and would DUPLICATE any server you already registered at user scope. That is why this companion deliberately uses the guide approach above instead of force-binding live servers.

## Why a guide, not a bundle

Your `<org-data-mcp>` and `exa` are already registered at user scope and working; Drive/Gmail can only be claude.ai connectors; Playwright must stay on-demand. Bundling would duplicate tools and auto-fail off-VPN. So the robust design is: Claude reads this flow and walks you (or a fresh machine) through the exact steps. No secrets ship; you authenticate locally.
