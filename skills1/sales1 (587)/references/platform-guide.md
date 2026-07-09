# SyncGTM Platform Guide

Full reference for the `sales-syncgtm` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — the marketing site + docs. The REST per-endpoint docs are JS-rendered; verify in-account.*

## What SyncGTM is

An **AI-native GTM data engine** that bundles, in one workspace: **buying signals** + **waterfall enrichment** + **AI lead scoring** + **AI research/writing** + a **no-code Workflow Builder** (and outbound). Positioned as "signal-driven outbound at ~85% less cost" vs incumbents. Aimed at **Sales, RevOps, agencies, startups, and GTM Engineers** (logos incl. Cloudflare/GitLab). Active (2026; ships an MCP server).

**Engine, not strategy.** It executes the signals→enrich→score→act loop; for *which signals / how to act* across tools, use `/sales-intent`.

## Surface map — MCP vs REST vs UI

| Capability | Surface | Notes |
|---|---|---|
| Agent access (enrich, signals, email/phone, LinkedIn) | **MCP server** | `api.syncgtm.com/mcp`, OAuth, free-plan |
| Enrichment / signals / scoring (programmatic) | **REST API** | base `api.syncgtm.com`, API key |
| Signal monitoring | **UI + REST + webhooks** | prospect + account level |
| AI lead scoring (0–100 vs ICP) | **AI (automatic)** | HOT/WARM/COOL/COLD |
| Workflow Builder (signal→enrich→write→push) | **UI (no-code)** | orchestration |
| AI research agents / AI email writer | **UI** | 20+ prompt templates |
| Events (signal fired / score threshold) | **Webhooks + native** | HubSpot/Salesforce/Slack |
| 40+ integrations | **Native + HTTP API** | CRM, comms, sequencers |
| LinkedIn capture | **Browser extension** | — |

## The core loop

```
Signals (job change, funding, hiring, LinkedIn post, web traffic, custom AI)
   → AI lead scoring (0–100 vs your ICP → HOT/WARM/COOL/COLD)
   → Workflow: waterfall enrich (verified email/mobile, 40+ providers)
   → AI message → push to CRM / sequencer  (or webhook to your stack)
```

Configure the ICP + which signals count; everything downstream keys off the score.

## Pricing & credits (best-effort)

- **Free** — includes **MCP access**, 40+ enrichment sources, AI research agents, scrapers, and workflows. Genuinely usable.
- **~$99/mo** — deeper waterfall enrichment (20+ providers), signal-driven outbound, flexible CRM integrations, transparent pricing.
- **Enterprise** — custom.
- **Credit-based** — waterfall enrichment consumes credits per record; a **credits estimator** exists. Scope enrichment to scored leads. Verify on `syncgtm.com/pricing`.

## Quick-start recipes

### Recipe 1 — Connect the MCP server to Claude Code (token-free)

```jsonc
// add to your MCP client config (Claude Code, Cursor, …)
{ "mcpServers": { "syncgtm": { "url": "https://api.syncgtm.com/mcp" } } }
```

1. Create a free account at **app.syncgtm.com** (free plan includes MCP).
2. Add `https://api.syncgtm.com/mcp` as an MCP server.
3. On first connect your **browser opens** for SyncGTM OAuth — sign in + approve; the client stores the session. **No API token / Authorization header.**

Now the agent can call SyncGTM tools to enrich a person/company, find a **verified email/phone**, pull **LinkedIn data**, and **read buying signals** inline. Revoke access anytime from the dashboard. (Allow outbound HTTPS to `api.syncgtm.com`.)

### Recipe 2 — Enrich + read signals via the REST API

```bash
# base api.syncgtm.com; API key from Settings -> API (docs: /core_concepts/api_key)
curl "https://api.syncgtm.com/<enrich-endpoint>" \
  -H "Authorization: Bearer $SYNCGTM_API_KEY" \
  -d '{"email":"jane@example.com"}'
```

Confirm the exact endpoint paths/params + webhook event names in `docs.syncgtm.com` (JS-rendered portal). Use it for batch enrichment, signal reads, and scoring; gate enrichment on the ICP score to save credits.

### Recipe 3 — Act on a signal automatically (Workflow Builder / webhook)

In the **Workflow Builder**: trigger = a **signal** (e.g. account raised funding) + a **score gate** (HOT/WARM only) → **waterfall enrich** → **AI message** → **push to HubSpot** (native) or **HTTP webhook** to your endpoint. Dedupe on the lead/account id; design the *outreach sequence* itself via `/sales-cadence`.

## When to route out

- Buyer-signal / intent **strategy** across tools (which signals, how to act) → `/sales-intent`
- **Prospect-list** building across tools → `/sales-prospect-list`
- **Enrichment** strategy across vendors → `/sales-enrich`
- Outbound **sequence/cadence** design for the outreach step → `/sales-cadence`
- Email **deliverability** for the sending side → `/sales-deliverability`
