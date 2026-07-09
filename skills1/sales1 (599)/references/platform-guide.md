# TexAu Platform Reference

<!-- Best-effort from research (2026-06). Pricing and plan gates shift — verify against the live pricing page and docs.texau.com. -->

## Overview

TexAu is a GTM (go-to-market) automation platform. It exists in two overlapping forms: (1) the **classic Cloud/Desktop product** — a no-code LinkedIn + web automation and scraping tool (a PhantomBuster-style "automations"/recipe runner billed in automation hours), and (2) the **V3 GTM data platform** — a spreadsheet-style table with right-click waterfall enrichment, an AI Column, CRM sync, and a credit-based REST API + MCP server. Target users: solopreneurs/founders doing their own outbound, SDR/RevOps teams, agencies, and GTM engineers who want programmatic enrichment from Claude/Cursor or a custom backend.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| Cloud/Desktop automations ("recipes") | Pre-built LinkedIn, Sales Navigator, Twitter/X, and web automations chained into workflows; scheduled runs | UI (Cloud/Desktop); some flows mirrored by API endpoints |
| LinkedIn enrichment | `enrich_profile`, `enrich_company` + bulk variants (by URN/company id, ≤50/call) | API-accessible, MCP |
| People / lead discovery | `people_search` (700M+ cached index), `profile_search` (live), `lead_search` (30+ filters, Sales Nav URL, `recentlyChangedJobs`, sessionId pagination) | API-accessible, MCP |
| Email finding & verification | `email_finding`, `email_verification` — **async jobs** with webhook delivery + inquiry polling | API-accessible (async), MCP |
| Web scraping | `web_scrape`, `web_meta_tags`, `web_json_ld`, `web_pixels`, `web_tech_stack`, `web_emails`, `web_sitemap`, `web_social_links`, `website_intelligence` | API-accessible, MCP |
| LinkedIn posts/ads | `post_keyword_search`, `post_details`, `profile_activities`, `ad_search`, `ad_details` | API-accessible, MCP |
| Directory / social scraping | `directory_yellowpages`, `youtube_*`, `slack_channel_members` | API-accessible, MCP |
| AI Column | Per-row prompt-driven scoring/personalization on the V3 table | UI; MCP for row-aware reasoning |
| CRM sync | Bidirectional sync to HubSpot, Salesforce, Pipedrive, Zoho, GoHighLevel | UI (plan-gated); API for record push |
| MCP server | Exposes the endpoints as Claude/Cursor tools at `mcp.texau.com/mcp` | MCP (OAuth, no key needed for the Claude connector) |

## Pricing, limits & plan gates

*All best-effort — TexAu has been mid-repricing; confirm on the live page.*

**V3 GTM platform (credit model):**
- **Free**: 50 credits on signup, no card.
- **Solo** ~$79/mo: ~2,500 credits/mo, 1 seat, one-way daily CRM sync. (API/webhooks generally NOT on this tier.)
- **Starter** ~$199/mo: ~8,000 credits/mo, 3 seats, **API + webhooks included**, credits roll over up to 2× the monthly balance.
- **Teams** ~$549/mo: ~25,000 credits/mo, 5 seats, bidirectional hourly CRM sync, premium data, intent alerts.
- **Enterprise**: custom — SSO/SAML, SLA, EU data residency.
- Extra seats ~$99/mo each.

**Classic Cloud automation (hours model):** Starter/Teams/Agency tiers billed in **monthly automation hours/minutes that do NOT roll over** (e.g. ~30 / ~100 / ~250 hours). This is the model older reviews describe; it is separate from the credit model above.

**Desktop:** **$1,499 one-time** (scheduled to rise to $1,999) — unlimited hours, runs locally.

**API & MCP:** a separate pay-as-you-go product, lower per-credit rate at volume (~40% discount vs UI credits), from ~$99/mo. **Pay-on-match**: failed lookups return `billed: false` and refund the credit.

**Credit costs (per MCP catalog, indicative):** `enrich_profile`/`enrich_company` 1/call · bulk variants 1/result (≤50) · `people_search`/`profile_search` 0.1/result · `lead_search` 0.5/result · `search_reference_data` free · `ad_search` 0.2/result · `ad_details` 2/call · `post_keyword_search` 6/call · `profile_activities` 2/call · `post_details` 1/call · email finding 2/person found · email verification 0.5/email · status/poll endpoints free.

**Rate limits:** ~100,000 calls/month per endpoint; per-minute 30–3,000 and per-day 800–1,000,000 depending on action. `GET /health` requires no auth.

## Integrations

- **CRMs (bidirectional read/write):** HubSpot, Pipedrive, Salesforce, Zoho, GoHighLevel.
- **Outbound senders (writes leads into):** Smartlead, Instantly, Lemlist, HeyReach, Expandi, Reply.io.
- **Data providers (TexAu reads from, waterfall):** Apollo, Hunter, Snov, RocketReach, Clearbit, and more (32+ sources).
- **iPaaS / automation:** native **n8n community nodes** (`n8n-nodes-texau-v3-api`), webhooks, Zapier/Make-style flows, plus the MCP server for Claude/Cursor.

## Data model

Endpoints return provider-merged JSON. Enrichment responses include the winning provider, per-provider execution logs, and latency. Two shapes you'll handle most:

**Enrich profile request/response (sync):**
```json
// POST /enrich_profile
{ "url": "https://www.linkedin.com/in/williamhgates/", "useCache": "true" }
```
```json
// 200 — fields merged from the waterfall (shape varies by provider)
{
  "fullName": "Bill Gates",
  "headline": "Co-chair, Bill & Melinda Gates Foundation",
  "location": "Seattle, Washington",
  "currentCompany": { "name": "Bill & Melinda Gates Foundation", "linkedinId": "1586" },
  "provider": "linkedin",
  "billed": true
}
```
<!-- Constructed from docs — verify against live API -->

**Async email-finding job:**
```json
// POST /email_finding
{
  "webhook": "https://your-app.com/hooks/texau",
  "data": [ { "refId": "row-1", "firstname": "Ada", "lastname": "Lovelace", "domain": "example.com" } ]
}
```
The call returns a job id; the per-person result (email + verification + `billed`) is delivered to `webhook` and is also fetchable via `GET /email_finding_inquiry/{id}`.

## Quick-start recipes

### Recipe 1 — Enrich a LinkedIn profile (sync)
Trigger: you have a LinkedIn URL and want structured person data.
```bash
curl -X POST https://v3-api.texau.com/api/v1/enrich_profile \
  -H "x-api-key: $TEXAU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.linkedin.com/in/williamhgates/","useCache":"true"}'
```
```python
import requests, os
r = requests.post(
    "https://v3-api.texau.com/api/v1/enrich_profile",
    headers={"x-api-key": os.environ["TEXAU_API_KEY"]},
    json={"url": "https://www.linkedin.com/in/williamhgates/", "useCache": "true"},
)
print(r.json())  # check `billed` — false means no charge (no match)
```
Gotcha: `useCache` defaults to `true`. Pass `"false"` when you need fresh data.

### Recipe 2 — Find emails in bulk, collect via webhook (async)
Trigger: a list of names + company domains; you want verified emails back in your app.
```bash
curl -X POST https://v3-api.texau.com/api/v1/email_finding \
  -H "x-api-key: $TEXAU_API_KEY" -H "Content-Type: application/json" \
  -d '{"webhook":"https://your-app.com/hooks/texau",
       "data":[{"refId":"r1","firstname":"Ada","lastname":"Lovelace","domain":"example.com"}]}'
```
Then either listen on `webhook` or poll:
```bash
curl https://v3-api.texau.com/api/v1/email_finding_inquiry/<jobId> \
  -H "x-api-key: $TEXAU_API_KEY"
```
Gotcha: the POST response is NOT the result — it's a job handle. Billing is 2 credits per person *found*.

### Recipe 3 — Advanced lead search with job-change filter
Trigger: build a list of recently-promoted decision-makers in an ICP.
```bash
curl -X POST https://v3-api.texau.com/api/v1/lead_search \
  -H "x-api-key: $TEXAU_API_KEY" -H "Content-Type: application/json" \
  -d '{"currentJobTitles":["VP Sales","Head of Sales"],
       "industries":["Software Development"],
       "recentlyChangedJobs":true,"page":1}'
```
Use `GET /search_reference_data` (free) first to get valid labels for `seniority`, `industries`, `functions`, `companySize`, `profileLanguages`. Paginate with the `sessionId` returned in the response (or pass a Sales Navigator URL via `salesNavUrl`).

## Integration patterns

- **CRM sync:** the platform's native bidirectional connectors handle field mapping; for custom flows, enrich via the API then push records to your CRM's API. Conflict resolution and sync frequency are plan-gated (Solo = one-way daily; Teams = bidirectional hourly).
- **Webhook listeners (async jobs):** email finding/verification deliver per-record results to your `webhook`. Make the endpoint idempotent on `refId`, and reconcile by polling `*_inquiry/{id}` if a delivery is missed.
- **Batch pipelines:** prefer `*_bulk` and `per_result` endpoints (≤50/call) to amortize cost; check `/usage?month=YYYY-MM` for remaining credits; treat `billed:false` as a free miss and back off on 429 using the `limit`/`current` fields in the response.
- **Agent/Claude runs:** connect the MCP server at `https://mcp.texau.com/mcp` (OAuth via the Claude connector — no API key in the prompt) to let Claude call `enrich_profile`, `people_search`, `find_emails`, etc. as tools.
