<!-- Source: docs.syncgtm.com (intro + /mcp_server + /core_concepts/api_key) and syncgtm.com (fetched 2026-06). The MCP server setup/endpoint/auth is verbatim from the docs; the REST API base/auth and webhook surface are best-effort (the per-endpoint docs are behind the docs portal's JS nav) — confirm exact endpoints at docs.syncgtm.com. -->

# SyncGTM API / MCP Reference

## What SyncGTM exposes

SyncGTM ("B2D Data Engine for AI-native GTM") exposes three programmatic surfaces:
1. **MCP server** — the headline: let an AI agent (Claude Code, Cursor, ChatGPT, …) call SyncGTM's enrichment + signals directly. Best-documented; covered first.
2. **REST API** — base `api.syncgtm.com`, API-key auth, for app/server integrations.
3. **Webhooks** + **40+ native integrations** (HubSpot, Salesforce, Slack, Attio, HTTP API) + a browser extension.

---

## MCP server (recommended for AI agents)

**Endpoint:**

```
https://api.syncgtm.com/mcp
```

(Allow outbound HTTPS to `api.syncgtm.com`.)

**Auth — OAuth browser sign-in (no token):** the first time your AI client connects, it opens your browser to the SyncGTM authorization page; you sign in + approve, and the client stores the session and reconnects automatically. **No long-lived API token / Authorization header** is required (so nothing to leak). Revoke a client's access anytime from the SyncGTM dashboard.

**Setup (2 steps, verbatim):**
1. Create an account at **app.syncgtm.com** — the **free plan gives immediate MCP access**.
2. Add **`https://api.syncgtm.com/mcp`** as an MCP server in your AI client (Claude Code, Cursor, ChatGPT, Gemini CLI, Codex, Manus, …). Approve the browser OAuth on first connect.

**What the MCP tools do:** enrich people + companies, find **verified emails and phone numbers**, pull **LinkedIn data**, and **read buying signals** — directly from your AI agent. (Tool catalog: `docs.syncgtm.com/mcp_server/tools`.)

Example (Claude Code MCP config):

```json
{ "mcpServers": { "syncgtm": { "url": "https://api.syncgtm.com/mcp" } } }
```

---

## REST API

- **Base:** `https://api.syncgtm.com` (REST). **Auth:** an **API key** generated in-app (docs: `/core_concepts/api_key`) — pass per the docs (header/key). Keep server-side.
- **Capabilities (map to the product):** enrichment (people/company — waterfall across 40+ providers / 20+ databases), verified email + mobile + personal-email lookup, firmographics/techstack/revenue/headcount, **signals** (read buying-intent indicators), **lead scoring** (0–100 vs ICP → HOT/WARM/COOL/COLD), and triggering **Workflow Builder** automations.
- Per-endpoint paths, params, pagination, and rate limits live in the docs portal (JS-rendered) — pull them from `docs.syncgtm.com` when implementing.

## Webhooks

Webhooks fire on platform events (e.g. a **new/qualifying signal**, a lead crossing a score threshold, an enrichment completing) so you can push into your stack in real time. Also supports **HTTP API webhooks** as an outbound action inside the Workflow Builder. Confirm the event catalog + any signature/secret in the docs; treat the endpoint as secret and dedupe.

## Signals (the core data)

Prospect- and account-level buying-intent indicators:

```
job changes · promotions · headcount growth · funding rounds · product launches ·
LinkedIn posts (prospect + company) · website-traffic shifts · tech-stack adoption ·
custom signals defined via AI
```

These feed **lead scoring** (AI scores each lead 0–100 against your ICP) and **workflows** (auto-enrich + outreach when a signal fires).

## Integrations & automation (non-API)

- **Native (40+):** HubSpot, Salesforce, Slack, Attio, email-sequencing tools, communication tools, **HTTP API webhooks**, custom API-key support for select data providers.
- **Browser extension** for LinkedIn.
- **Workflow Builder** — no-code orchestration (signal → enrich → score → outreach).

## Pricing (best-effort)

**Free** (includes MCP access + 40+ enrichment sources, AI research agents, scrapers, workflows) → **~$99/mo** (deeper waterfall enrichment, signal-driven outbound, flexible CRM integrations) → **Enterprise**. Credits-based; a "credits estimator" exists. Verify on `syncgtm.com/pricing`.

## Notes / gaps

- The **MCP server** is fully documented (endpoint, OAuth, setup, tools). The **REST API** per-endpoint reference + webhook event catalog are in the JS-rendered docs portal — confirm exact paths/auth/events at `docs.syncgtm.com` before coding against REST/webhooks.
- For AI-agent use (this repo's audience), prefer the **MCP server** — it's token-free and purpose-built.
