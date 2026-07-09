# PhantomBuster Platform Guide

Full reference for the `sales-phantombuster` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — support docs + reviews (the marketing site is JS-rendered). Verify in-account.*

## What PhantomBuster is

A **code-free web/LinkedIn automation + scraping + lead-gen** platform. You pick a **Phantom** (a pre-built automation/scraper), configure it, and it runs **in the cloud** producing CSV/JSON output. Chain Phantoms into **Flows/Workflows**, add **AI Agents** (LLM steps), and store leads in the **LinkedIn Leads database**. Beloved by **growth hackers, solo founders, B2B SaaS sales, and agencies** — and exposed via a clean REST API + webhooks.

**Scraper/automator, not a CRM or sequencer.** It *sources* leads; pipe them to your CRM/sequencer (or Clay) and design outreach via `/sales-cadence`.

## Core concepts

| Term | What it is |
|---|---|
| **Phantom** | A pre-built automation/scraper (LinkedIn Search Export, Profile Scraper, Auto-Connect, Email Finder, …). |
| **Agent ID** | Identifies a Phantom; **persistent** across runs. |
| **Container ID** | Identifies a **single launch/run** of a Phantom (its logs + result). |
| **Flow / Workflow** | Chains Phantoms into a multi-step pipeline. |
| **AI Agent** | Adds LLM steps (research/classification) to a flow. |
| **Slot** | A concurrency unit — how many Phantoms can be active at once. |
| **Execution time** | Monthly run-hours your Phantoms/flows consume. |

## Surface map

| Capability | Surface | Notes |
|---|---|---|
| Launch / configure / list Phantoms | **REST API** | `/agent/{id}/launch`, `/agents/fetch-all`, `/agent/{id}` |
| Run status + scraped results | **REST API** | `/containers/fetch`, `/containers/fetch-result-object` |
| LinkedIn Leads DB (lists, sync, delete) | **REST API (Storage)** | manage leads + lists |
| Run-finished notifications | **Webhook (per agent)** | secret query param, 11s timeout |
| Phantom catalog / Flow builder / AI Agents | **UI** | configure in-app |
| iPaaS | **Zapier / Make / n8n** | no-code triggers/actions |

## Pricing & limits (best-effort)

Billed by **execution time** + **Phantom slots** (+ **email credits** for email-finder Phantoms):

| Plan | ~Price (annual) | Exec hrs/mo | Slots | Email credits |
|---|---|---|---|---|
| **Start** | ~$56/mo | 20 | 5 | 500 |
| **Grow** | mid | 80 | 15 | 2,500 |
| **Scale** | ~$439/mo | 300 | 50 | 10,000 |

**API access is on all paid plans** (+ unlimited CSV/JSON exports, up to 100 workspace members). Annual saves ~19–20%. Verify on phantombuster.com/pricing.

## Quick-start recipes

### Recipe 1 — Launch a Phantom and fetch results (async: agent → container → result)

```bash
KEY="$PHANTOMBUSTER_API_KEY"; H="X-Phantombuster-Key-1: $KEY"

# 1. launch -> returns a containerId (the run isn't done yet)
CID=$(curl -s -X POST "https://phantombuster.com/api/v2/agent/$AGENT_ID/launch" \
  -H "$H" -H "Content-Type: application/json" -d '{"output":"first-result-object"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["data"]["containerId"])')

# 2. poll status until finished (or use a webhook instead — see Recipe 2)
curl -s "https://phantombuster.com/api/v2/containers/fetch?id=$CID" -H "$H"

# 3. fetch the structured leads
curl -s "https://phantombuster.com/api/v2/containers/fetch-result-object?id=$CID" -H "$H"
```

Responses are **JSend** (`{status:"success", data:{…}}`). Keep the key **server-side**.

### Recipe 2 — Get notified on completion (webhook)

In the agent's **setup → Advanced Notification Settings**, set your webhook URL + a **`secret`**. Handler:

```python
@app.post("/pb-webhook")
def pb_webhook(request):
    # webhooks can't send custom headers -> verify the secret QUERY param
    if request.args.get("secret") != PB_WEBHOOK_SECRET:
        return Response(status_code=401)
    # MUST return 200 within 11s -> ack now, process async
    enqueue_fetch_results(request.json.get("containerId"))
    return {"ok": True}   # then fetch /containers/fetch-result-object out-of-band
```

The **11-second timeout** is the #1 trap — don't fetch results inline; ack and process asynchronously.

### Recipe 3 — Stay within slots + safe LinkedIn limits

- Don't launch more concurrent Phantoms than your **slots** (5/15/50); queue the rest.
- Long scrapes eat **execution hours** — narrow searches, scrape only what you need.
- LinkedIn Phantoms run with **your `li_at` session cookie** (acting as you): keep daily volumes human, space launches, refresh the cookie when it expires, and warm new accounts. For account-safety strategy use `/sales-linkedin`.

## When to route out

- Prospect-list / lead-sourcing **strategy** across tools → `/sales-prospect-list`
- **Enrichment** strategy across vendors → `/sales-enrich`
- Outbound **sequence/cadence** for scraped leads → `/sales-cadence`
- LinkedIn **account-safety** strategy → `/sales-linkedin`
