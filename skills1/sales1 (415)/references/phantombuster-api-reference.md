<!-- Source: hub.phantombuster.com/docs/api + /reference, support.phantombuster.com (Using PhantomBuster's API, webhooks), and phantombuster.com pricing (fetched 2026-06). Auth/base-URL/endpoint groups/JSend/webhook specifics are verbatim from the docs; the marketing homepage is JS-rendered (thin to WebFetch) so feature/pricing detail is from support + review sources. -->

# PhantomBuster API Reference

## What it automates

PhantomBuster is a **code-free automation + web/LinkedIn scraping** platform. A **Phantom** is a pre-built automation (e.g. "LinkedIn Search Export", "Profile Scraper"); you configure it, it runs in the cloud (using your session cookie for sites like LinkedIn), and produces output (CSV/JSON). **Flows/Workflows** chain Phantoms; **AI Agents** add LLM steps. The API lets you launch Phantoms and fetch their results programmatically.

## Base URL & version

```
https://phantombuster.com/api/v2/<path>
```

Current version **v2** (timestamps in **milliseconds**; v1 used seconds). 

## Authentication

Put your API key in the **`X-Phantombuster-Key-1`** HTTP header (or the **`key`** query parameter) on every request:

```bash
curl "https://phantombuster.com/api/v2/agents/fetch-all" \
  -H "X-Phantombuster-Key-1: $PHANTOMBUSTER_API_KEY"
```

The key lives in **Workspace settings** (navbar → Workspace settings). It's **shown once on creation** — copy it. **Anyone with the key can launch your agents** — keep it server-side; rotate (generate new + delete old) if leaked.

## Response format (JSend)

- **2XX:** `{ "status": "success", "data": { … } }`
- **4XX/5XX:** `{ "status": "error", "message": "…" }`

## Key concepts

- **Agent ID** — identifies a **Phantom**; **persistent** across runs.
- **Container ID** — identifies a **single launch/run** of a Phantom (its logs + result live here).

So: launch an **agent** → get a **container** → fetch that container's output/result.

## Endpoints (grouped)

### Agents (create / launch / update / fetch a Phantom)
- `GET /agents/fetch-all` — list all Phantoms in the workspace
- `GET /agent/{id}` — fetch one Phantom's config
- `POST /agent/{id}/launch` — **add the agent to the launch queue** (returns the new **container id**). The **`output`** parameter matters — choose how/what output you want; you can also pass runtime `argument` overrides.
- `GET /agent/{id}/fetch-output` — fetch the agent's console/output

### Containers (a single run)
- `GET /containers/fetch?id={containerId}` — run metadata/status/logs
- `GET /containers/fetch-result-object?id={containerId}` — the **structured result** (the leads/data the Phantom produced)

### Storage (LinkedIn Leads database)
- Manage the LinkedIn Leads DB: delete leads, manage **lists**, and **sync** data with external tools. (See the live `/reference` for exact paths.)

**CONSTRUCTED flow example** (launch → poll → get results; verify exact params in `/reference`):

```bash
# 1. launch the Phantom -> returns a containerId
curl -X POST "https://phantombuster.com/api/v2/agent/$AGENT_ID/launch" \
  -H "X-Phantombuster-Key-1: $KEY" -H "Content-Type: application/json" \
  -d '{"output":"first-result-object"}'
# -> { "status":"success", "data": { "containerId": "1234567890" } }

# 2. poll the container until finished
curl "https://phantombuster.com/api/v2/containers/fetch?id=1234567890" -H "X-Phantombuster-Key-1: $KEY"

# 3. fetch the structured results (the scraped leads)
curl "https://phantombuster.com/api/v2/containers/fetch-result-object?id=1234567890" -H "X-Phantombuster-Key-1: $KEY"
```

Prefer a **webhook** (below) over tight polling so you're notified when the run finishes.

## Webhooks (run finished)

Set the webhook URL **per agent**: setup agent page → settings → **Advanced Notification Settings**. PhantomBuster POSTs to it when the agent run completes.

- **Auth is a `secret` via query parameter** — webhooks **don't support custom request headers**, so verify the `secret` you configured (don't rely on a header signature).
- **11-second timeout** — if your endpoint takes longer than 11s, the request is cancelled and treated as a server error. **Return 200 fast** (ack immediately, process async).

## Slots, execution time & limits

- **Execution time** — monthly hours your Phantoms/Workflows can run (20 / 80 / 300 by tier). Long scrapes burn it.
- **Phantom slots** — how many automations can be **active simultaneously** (5 / 15 / 50 by tier).
- **Email credits** for email-finder Phantoms (500 / 2,500 / 10,000 by tier).
- **API access is on all paid plans** (+ unlimited CSV/JSON exports, up to 100 workspace members).

## Pricing (best-effort)

**Start ~$56–69/mo** (20 exec hrs, 5 slots, 500 email credits) · **Grow** (80 hrs, 15 slots, 2,500 credits) · **Scale ~$439/mo** (300 hrs, 50 slots, 10,000 credits). Annual saves ~19–20%. Verify on phantombuster.com/pricing.

## Gotchas (technical)

- **Scraping uses your session cookie** (e.g. LinkedIn `li_at`) — runs act as *you*; respect platform limits/ToS, and rotate/refresh cookies (they expire).
- **Async model:** launch returns immediately with a container id; the data isn't ready until the container finishes — webhook or poll `containers/fetch`.
- **v1 vs v2 timestamps** differ (s vs ms) — use v2.
