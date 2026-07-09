# Clay API & Integration Reference

## Overview

| Property | Value |
|----------|-------|
| Auth | No traditional CRUD API auth — webhook-based integration. Inbound webhooks support an optional auth token header. HTTP API actions (outbound) support Bearer / `X-API-Key` / Basic / JWT auth on the *external* API you call. |
| API style | Webhooks (inbound/outbound) + HTTP API actions (outbound) + official MCP server |
| REST API | No public CRUD REST API for table/data management. A versioned surface exists at `api.clay.com/v3` but is currently exposed only as the MCP endpoint (`https://api.clay.com/v3/mcp`), not as documented CRUD endpoints. |
| Clay API key | Found in Settings → Account → API key. Used for Clay-*native* lookup integrations (e.g., look up a single/multiple rows in another Clay table) — NOT a general public REST API. |
| Enterprise API | People & Company API (Enterprise plan only) |
| Rate limit | Configurable per HTTP API action (e.g., 10 requests/1000ms) |
| Plan gates | HTTP API actions and outbound webhook automations require Growth plan ($446+/mo). MCP server available on Launch/Growth/Enterprise (company/contact lookups free for free/trial). |
| Docs | university.clay.com/docs |

**Important**: Clay does not have a traditional public CRUD REST API for programmatically managing tables/rows. Integration is webhook-based — you push data into Clay via inbound webhooks and pull data out via HTTP API actions, native integrations, or the MCP server. A Clay API key exists but is for Clay-native cross-table lookups, not external CRUD. The Enterprise plan includes a lightweight People & Company API for lookups.

## Inbound Webhooks

Push data into a Clay table by POSTing JSON to the table's unique webhook URL.

### Getting the webhook URL

1. Open your Clay workbook
2. Click **+ Add** → search for **Webhooks** → **Monitor webhook**
3. Copy the unique webhook URL (format: `https://app.clay.com/webhook/...`)
4. (Optional) Generate an **authentication token** to secure the webhook. Per Clay's docs you can only view/copy this token once, so save it immediately.

### Sending data

```bash
curl -X POST "https://app.clay.com/webhook/{table_webhook_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "company": "Acme Corp",
    "email": "jane@acme.com"
  }'
```

**Behavior**:
- Each POST creates a new row in the table
- JSON keys map to column names (auto-created if they don't exist)
- Enrichments configured on the table run automatically on new rows
- **Optional authentication**: Clay's webhook docs state you "can include an authentication token in the header of your request" to secure the webhook. If you generate one, the sending system must include that token header. If you don't, the URL is unauthenticated and relies on URL obscurity — so generate the token for any sensitive inbound source. (Note: community sources reference `x-clay-webhook-auth` / `x-clay-signature` HMAC-SHA256 headers, but the exact header names and signing scheme are not spelled out on the official webhook page — verify in the Clay UI when you generate the token.)

**Use cases**:
- Form submissions → Clay enrichment
- CRM triggers → Clay enrichment → push back to CRM
- Zapier/Make → Clay for enrichment middleware
- Custom apps → Clay for data enrichment

## HTTP API Action (Outbound)

Call external APIs from within Clay table workflows. Available on Growth plan and above.

### Configuration

In your Clay table:
1. Click **Add enrichment** → search for **HTTP API**
2. Configure:
   - **Method**: GET, POST, PUT, DELETE
   - **Endpoint**: The external API URL
   - **Headers**: Authorization, Content-Type, custom headers
   - **Query parameters**: Key-value pairs appended to URL
   - **Body**: JSON payload (can use dynamic column values)
   - **Field path**: JSONPath to extract specific fields from the response

### Auth schemes for the external API

Clay's HTTP API action supports several ways to authenticate against the *external* API you're calling:
- **Bearer token**: header `Authorization: Bearer YOUR_TOKEN_HERE`
- **API key header**: header `X-API-Key: YOUR_API_KEY_HERE`
- **Basic auth**: header `Authorization: Basic <base64(username:password)>`
- **JWT (dynamic token)**: a separate "HTTP API with JWT authentication" mode where Clay calls your token endpoint with stored username/password, receives a JWT, injects it as `Authorization: Bearer <token>`, and auto-refreshes it (~every 55 minutes). The token's location in the response is set via dot-notation (e.g., `access_token`, `data.token`); the header name and prefix are customizable.

Credentials can be saved at the workspace level in an **HTTP API (Headers)** account and reused across enrichments rather than hardcoded per call.

### Rate limiting

Configure per-action:
- **Request limit**: Number of requests per duration window
- **Duration (ms)**: Time window for the request limit
- Example: `10 requests / 1000ms` = 10 requests per second

### Example: Push enriched data to a webhook

```
Method: POST
Endpoint: https://your-app.com/api/enriched-leads
Headers:
  Authorization: Bearer YOUR_TOKEN
  Content-Type: application/json
Body:
{
  "email": {{Work Email}},
  "company": {{Company Name}},
  "revenue": {{Company Revenue}},
  "enriched_at": {{_timestamp}}
}
```

Dynamic values use `{{Column Name}}` syntax to reference table columns.

## Enterprise People & Company API

Available only on Enterprise plans. Lightweight lookup API for basic profile and company data.

### Capabilities

- **People lookup**: Send an email or LinkedIn URL → get basic profile info (name, title, company, location)
- **Company lookup**: Send a domain → get company details (name, industry, size, location)
- **Limitations**: Does not include deep data like verified emails, phone numbers, or revenue figures. For those, use Clay's table-based waterfall enrichment.

### Details

No public documentation available for endpoint URLs, authentication, or response schemas. Contact Clay sales or your dedicated Growth Strategist for Enterprise API access and documentation.

## Clay MCP Server

Clay publishes an **official MCP (Model Context Protocol) server** that turns Clay into a context layer LLMs can call — letting reps run enrichments and custom **Functions** (workflows built by RevOps) directly inside Claude, ChatGPT, or other MCP clients without opening Clay.

### Capabilities
- Default enrichment data points (headcount growth, recent news, tech stack, email, work history, etc.)
- Run custom **Functions** built by RevOps for the team to consume
- Company / contact lookups across providers
- Generate personalized outreach at scale

### Connecting from Claude
- Easiest path: connect via the Claude Connectors page (`https://claude.com/connectors/clay`) — an OAuth-style flow; existing Clay users connect immediately, new users get an account created during setup. No paid Claude plan required; first connection grants 500 complimentary credits. On a Claude Enterprise plan, an admin must add the Clay connector first.
- Direct MCP endpoint (for clients configured by URL): `https://api.clay.com/v3/mcp`.

### Plan gate
- Available on Launch, Growth, and Enterprise (modern and legacy).
- Company/contact lookups remain available to free and trial users.
- Credit budgets per MCP user are set on the **MCP Users settings** page; Function permissions on the **Function settings** page.

> Note: This is distinct from **Claygent connecting to other tools' MCP servers** (Salesforce, Gong, Google Docs, Notion). The Clay MCP server exposes *Clay* to outside LLM clients; Claygent's MCP support lets Clay *consume* external MCP servers.

## Native CRM Integrations

### Salesforce

| Action | Description |
|--------|------------|
| Import | Pull leads, contacts, accounts, opportunities into Clay tables |
| Create | Create new records in Salesforce from enriched Clay data |
| Update | Update existing records with enriched fields |
| Lookup | Search Salesforce for matching records |

**Setup**: Connect via OAuth in Clay → Integrations → Salesforce. Requires Growth plan.

### HubSpot

| Action | Description |
|--------|------------|
| Import | Pull contacts, companies, deals into Clay tables |
| Create object | Create new CRM records |
| Update object | Update existing records |
| Create association | Link records together |
| Lookup object | Search for matching records |

**Setup**: Connect via OAuth or HubSpot Marketplace app. Requires Growth plan.

### Dynamics 365

| Action | Description |
|--------|------------|
| Create | Create new records |
| Update | Update existing records |
| Lookup | Search for matching records |

**Setup**: Connect via OAuth. Requires Growth plan.

## Zapier Integration

### Triggers (Clay → Zapier)

- **New row added** — fires when a new row appears in a Clay table
- **Row updated** — fires when a row is modified (enrichment complete, manual edit)

### Actions (Zapier → Clay)

- **Add row** — push data into a Clay table via webhook
- **Update row** — modify an existing row

### Setup

Use Clay's webhook URL as the endpoint in Zapier's webhook action, or use the native Clay app in Zapier.

## Make (Integromat) Integration

Clay has a native Make app supporting:
- Webhook triggers (new/updated rows)
- Table row creation
- HTTP API actions for custom workflows

## Ad Sync Destinations

Push Clay Audiences to advertising platforms:

| Platform | Sync type | Notes |
|----------|----------|-------|
| LinkedIn Ads | Matched Audiences | Company + contact targeting |
| Meta Ads | Custom Audiences | Email-based matching |
| Google Ads | Customer Match | Email-based matching |

**Plan gate**: Growth plan (1 audience) or Enterprise (2 audiences).

## Credit System

| Credit type | What it covers | Rollover |
|-------------|---------------|----------|
| **Actions** | Enrichments, Claygent runs, HTTP calls, CRM writes | No — resets monthly |
| **Data Credits** | Provider-specific enrichment lookups | Yes — up to 2x monthly allocation |

- Different providers cost different amounts of Data Credits
- Waterfall enrichment consumes credits for each provider attempted (not just successful matches)
- "Only if empty" logic prevents redundant lookups and saves credits
- Additional credits available at ~30% premium on paid plans

## Error Handling

### Webhook errors

| Scenario | Behavior |
|----------|---------|
| Invalid JSON | Row not created, no error response (fire-and-forget) |
| Table deleted | 404 response |
| Rate limited | 429 response — retry with backoff |

### HTTP API action errors

| Status | Meaning |
|--------|---------|
| 200-299 | Success — response data extracted per field path config |
| 400 | Bad request — check body/params configuration |
| 401/403 | Auth error — check headers/token |
| 404 | Endpoint not found |
| 429 | Rate limited — Clay respects the configured rate limit |
| 500+ | Server error — Clay retries automatically |

## Gaps & Limitations

- **No public CRUD REST API**: Clay does not expose documented endpoints for programmatic table management, row CRUD, or enrichment triggering outside of webhooks. A versioned `api.clay.com/v3` surface exists but is currently exposed only as the MCP endpoint, not as documented CRUD endpoints. For LLM-driven access, use the official MCP server. The Clay API key in Settings is for Clay-native cross-table lookups, not external CRUD.
- **Enterprise API undocumented**: The People & Company API (Enterprise only) has no public documentation. Contact Clay for specs.
- **Webhook security**: Inbound webhooks now support an optional authentication token in the request header — generate one for sensitive sources rather than relying on URL obscurity. The exact header name (community references `x-clay-webhook-auth`) and any HMAC signature scheme (`x-clay-signature`) are not fully documented on the official webhook page; verify in the Clay UI.
- **Credit costs per provider not public**: Exact Data Credit costs for each of the 150+ providers are not publicly documented. Check within the Clay UI when configuring enrichments.
- **No official SDKs**: Clay does not publish client libraries. Use direct HTTP requests for webhook and HTTP API integration, or the MCP server for LLM clients.
