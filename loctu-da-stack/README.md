# loctu-da-stack

> A companion plugin to prof-DA that wires your DA workflow MCP connectors. It ships no credentials: it teaches Claude how to walk you through logging in and registering each MCP, so they are connected before you analyze.

`v0.1.0` · MIT · companion to prof-DA · guided setup, no bundled secrets

## Why this exists

prof-DA does the analysis, but it can only use the data and tools your machine is connected to. Wiring those connectors by hand is easy to get wrong or forget: which command, which gateway, where the API key goes, and which ones are claude.ai connectors versus `claude mcp add`. This plugin turns that into a guided flow. Claude checks what is missing, then walks you (or a fresh machine) through each step, with a placeholder for every secret so nothing sensitive is ever shipped.

It covers the five connectors a <organization> DA workflow uses: <organization> Data Portal (org data), exa (web search), Google Drive + Gmail (the automation-report flow), and Playwright/Chrome (browser review, on-demand).

## Install

```bash
/plugin marketplace add loctu0402/prof-DA        # same marketplace as prof-DA (once per machine)
/plugin install loctu-da-stack@loctu-marketplace
```

## Use

```
/setup-stack        # or just ask: "set up my MCP stack" / "kết nối <org-data-mcp> + exa"
```

Claude runs `claude mcp list`, then walks you through only the connectors that are missing. Full per-connector steps live in [skills/setup-stack/SKILL.md](skills/setup-stack/SKILL.md); placeholder configs are in [mcp/example-stack-mcp.json](mcp/example-stack-mcp.json).

## What it does NOT do

It does not bundle or auto-start any MCP server. That would duplicate the servers you already run at user scope and auto-fail when off-VPN. It guides; you authenticate locally, and secrets stay on your machine.

## License

MIT.

## Author

Loc Tu (loctu), 2026. Companion to the prof-DA plugin.
