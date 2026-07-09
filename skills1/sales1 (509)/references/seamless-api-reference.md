# Seamless.AI API Reference

## Overview

- **Base URL**: `https://api.seamless.ai/api/client/v1`
- **Auth**: API key (`Token: API_KEY` header) or OAuth 2.0 (`Authorization: Bearer ACCESS_TOKEN`)
- **Content-Type**: `application/json` for all requests and responses
- **Rate Limit**: 60 requests per minute per endpoint (default). This is an **org-level shared quota** — all API keys and users in your organization share it. Contact sales/your AE for higher limits. (Verified 2026-06-13 against docs.seamless.ai/rate-limits-and-credits.)
- **Plan availability**: As of 2026-05-11 the public API is generally available on **every plan, including free** — free-tier users get an API key on signup and API calls draw from the plan's existing credit balance. API usage consumes **Universal Credits only** (not search credits).
- **OpenAPI spec / Postman**: An OpenAPI spec is published at `https://docs.seamless.ai/openapi.json` (import into Postman).
- **MCP server**: Seamless also exposes an MCP server at `https://mcp.seamless.ai/mcp` (54 tools across 11 domains — search, research, campaigns, calls, email, lists, tasks, templates, etc.), authenticated via OAuth 2.1 or API key. See the MCP section below.

### Rate Limit Headers

| Header | Description |
|---|---|
| `X-RateLimit-Limit` | Maximum requests allowed in current window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Unix epoch time when window resets |
| `X-PublicAPI-Credits` | Remaining credits for requests |

## Authentication

### API Key

Include in the request header:

```
Token: YOUR_API_KEY
```

API keys are persistent and managed in Seamless.AI Settings > API.

### OAuth 2.0

**Authorization endpoint**: `https://login.seamless.ai/oauth/authorize` (params: `client_id`, `redirect_uri`, optional `state` for CSRF)
**Token endpoint**: `POST https://api.seamless.ai/api/client/v1/oauth/accessToken`

**Grant types**: `authorization_code`, `refresh_token`

**Token response**: `access_token`, `refresh_token`, `expires_at` (Unix timestamp).
**Note**: Both the `authorization_code` and `refresh_token` token requests include `redirect_uri` (in addition to `client_id`/`client_secret`).

**Exchange authorization code for access token**:

```http
POST /oauth/accessToken
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "code": "AUTH_CODE",
  "redirect_uri": "YOUR_REDIRECT_URI",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

**Refresh token**:

```http
POST /oauth/accessToken
Content-Type: application/json

{
  "grant_type": "refresh_token",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "redirect_uri": "YOUR_REDIRECT_URI",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

**Header format**: `Authorization: Bearer ACCESS_TOKEN`

## Endpoints

### Contact Search

Search for contacts matching specified criteria.

```http
POST /search/contacts
Content-Type: application/json
Token: API_KEY

{
  "filters": {
    "company": ["Acme Corp"],
    "location": {
      "city": "San Francisco",
      "state": "CA",
      "country": "US"
    },
    "department": ["engineering", "sales"],
    "industry": ["technology"],
    "seniority": ["vp", "director", "c_level"],
    "keywords": ["product management"],
    "news": ["funding"]
  },
  "limit": 50,
  "nextToken": null
}
```

**Note on filter field names**: the live OpenAPI uses flat, camelCase filter keys at the request top level (not nested under a `filters` object as shown above). Confirmed keys include: `companyName`, `companyNameSearchType`, `companyDomain`, `contactState`, `contactCountry`, `contactZipCode`, `locationType`, `department`, `industry`, `fullName`, `contactKeyword`, `jobTitle`, `seniority`, `companyFoundedOn`, `companySize`, `companyRevenue`, `technologies`, `technologiesIsOr`, `jobChanges`, `pastCompany`, `companyType`, `lastModifiedAfter`, `lastModifiedBefore`, `newsTypes`, `newsTypeDates`, `companyLatestFundingDates`, `companyLatestFundingClassifications`, `companyLatestFundingTotals`. (Verified 2026-06-13.)

**Response**:

```json
{
  "data": [
    {
      "searchResultId": "...",
      "name": "Jane Smith",
      "title": "VP Engineering",
      "company": "Acme Corp",
      "department": "engineering",
      "seniority": "vp",
      "domain": "acme.com",
      "city": "San Francisco",
      "state": "CA",
      "country": "US",
      "liUrl": "linkedin.com/in/janesmith",
      "industries": ["technology"],
      "companyRevenue": "...",
      "employeeSizeRange": "..."
    }
  ],
  "supplementalData": {
    "isMore": true,
    "total": 150,
    "perPage": 50,
    "nextToken": "eyJhbGciOiJIUzI1NiJ9..."
  }
}
```

Each search-result row carries a `searchResultId` — pass it to the research endpoints to enrich (reveal email/phone). Search results do NOT include verified email/phone; those come back from research.

**Pagination**: Use the `nextToken` from `supplementalData.nextToken` in subsequent requests; `supplementalData.isMore` indicates whether more pages remain.

### Company Search

Search for companies matching specified criteria.

```http
POST /search/companies
Content-Type: application/json
Token: API_KEY

{
  "filters": {
    "name": "Acme",
    "domain": "acme.com",
    "location": {
      "city": "San Francisco",
      "state": "CA",
      "country": "US"
    },
    "industry": ["technology"],
    "employeeCount": {
      "min": 50,
      "max": 500
    },
    "revenue": {
      "min": 10000000,
      "max": 100000000
    },
    "technologies": ["Salesforce", "React"]
  },
  "limit": 50,
  "nextToken": null
}
```

**Response**: Similar structure to Contact Search with company-level fields (domain, employee count, revenue, industry, technologies, location).

### Contact Research (Enrichment)

Initiate enrichment for contacts. This is an async operation — results are delivered via polling or webhook.

**Option 1 — Enrich from search results** (`searchResultIds`, max 100 per call):

```http
POST /contacts/research
Content-Type: application/json
Token: API_KEY

{
  "searchResultIds": ["...", "..."]
}
```

**Option 2 — Enrich from direct contact identifiers** (`contacts` array). Each contact must supply one valid identifier combination: `contactName` + `companyName`, `contactName` + `domain`, a standalone `email`, or a LinkedIn URL (`liProfileUrl`, `liSalesNavUrl`, or `liRecruiterUrl`):

```http
POST /contacts/research
Content-Type: application/json
Token: API_KEY

{
  "contacts": [
    { "email": "jane.smith@acme.com" }
  ]
}
```

**Optional request flags**:
- `isJobChange` (boolean) — run job-change research on the identifiers.
- `skipDeduplicationCheck` (boolean) — bypass duplicate detection (otherwise an already-researched record returns a `duplicate`/`contact-already-researched` status instead of re-charging credits).

**Response** (202 Accepted):

```json
{
  "success": true,
  "requestIds": ["...", "..."]
}
```

Use the returned `requestIds` to poll `/contacts/research/poll`, or receive results via webhook.

### Contact Research Poll

Check the status of a contact research request.

```http
GET /contacts/research/poll?requestIds=req_abc123,req_def456
Token: API_KEY
```

`requestIds` is a comma-separated list of the request IDs returned from `/contacts/research`.

**Response**:

```json
{
  "data": [
    {
      "requestId": "...",
      "status": "done",
      "contact": {
        "fullName": "Jane Smith",
        "title": "VP Engineering",
        "company": "Acme Corp",
        "email": "jane.smith@acme.com",
        "phones": ["+14155551234"],
        "linkedInProfileUrl": "linkedin.com/in/janesmith"
      }
    }
  ]
}
```

**Statuses** (verified 2026-06-13): `queued`, `researching`, `done`, `error`, `missing`, `duplicate`, `not found`, `contact-already-researched`, `No license or credits available`. The docs note additional values may be added over time, so treat unknown statuses as non-terminal/ignore rather than failing hard. A `duplicate` / `contact-already-researched` status means the record was already researched — do **not** resubmit the same `searchResultId`.

### Company Research (Enrichment)

Initiate enrichment for companies. Async — results via polling or webhook.

```http
POST /companies/research
Content-Type: application/json
Token: API_KEY

{
  "searchResultIds": ["company_789"]
}
```

**Response**: Returns `requestIds` for polling.

### Company Research Poll

```http
GET /companies/research/poll?requestIds=req_ghi789
Token: API_KEY
```

**Response**: Returns enriched company data including 50+ intelligence URLs and structured metrics (employee count, revenue, industry, technologies, funding, etc.).

### Organization Contacts

Retrieve contacts from your organization's Seamless.AI account.

```http
GET /contacts?startDate=2026-01-01T00:00:00Z&endDate=2026-03-28T00:00:00Z&page=1&limit=500
Token: API_KEY
```

**Parameters** (verified 2026-06-13):
- `startDate` (**required**): ISO8601 date-time string — start of the lookback period
- `endDate` (**required**): ISO8601 date-time string — end of the lookback period
- `page` (optional, default `1`): page number to retrieve
- `limit` (optional, default `500`, max `500`): results per page

### Organization Companies

Retrieve companies from your organization's account.

```http
GET /companies
Token: API_KEY
```

## Webhooks

Seamless.AI supports webhook delivery for async research results. (Verified 2026-06-13 against docs.seamless.ai/receive-research-results-with-webhooks.)

**Configuration**: Webhooks are created in the dashboard at **Settings → Webhooks**. When creating a webhook you select the event type and provide your HTTPS endpoint URL plus a shared secret.

**Event types** (exact names):
- `contact-researched` — fires when contact enrichment completes
- `company-researched` — fires when company enrichment completes

**Verification**: Seamless sends an `x-seamless-webhook-secret` request header containing the shared secret you configured. Verify by **constant-time string comparison** to your stored secret and reject on mismatch. This is a shared-secret check, **not** HMAC body signing — there is no signature over the payload.

**Required response**: Return a `2xx` status to acknowledge. Any non-`2xx` is treated as a delivery failure and may be retried (the docs do not publish a specific retry schedule or max-attempt count).

**Correlation**: The payload's `apiResearchId` corresponds to the `requestId` from the original research submission — use it to match the delivery back to your request.

### Contact Research Webhook

When contact research completes, Seamless.AI POSTs the enriched contact to your configured webhook URL.

**Payload** (field names verified 2026-06-13):

```json
{
  "fullName": "Jane Smith",
  "title": "VP Engineering",
  "company": "Acme Corp",
  "email": "jane.smith@acme.com",
  "apiResearchId": "...",
  "phones": ["+14155551234"],
  "linkedInProfileUrl": "linkedin.com/in/janesmith"
}
```

### Company Research Webhook

Delivers enriched company data. **Payload** (field names verified 2026-06-13) includes `name`, `domain`, `apiResearchId`, `phones`, `staffCountRange`, `revenueRange`, `linkedInProfileUrl`, plus additional intelligence URLs and structured metrics.

## MCP Server (NEW)

Seamless ships a hosted MCP server for agentic/LLM clients (Claude Desktop, Claude Code, Cursor, ChatGPT, VS Code, Windsurf, Gemini CLI, Amazon Bedrock/Q, etc.). Verified 2026-06-13 against docs.seamless.ai/mcp-docs.

- **Endpoint**: `https://mcp.seamless.ai/mcp`
- **Auth**: OAuth 2.1 or API key
- **Tools**: 54 tools across 11 domains — search (`search_contacts`, `search_companies`), research (`research_contacts`, `research_companies`, poll tools), activity, campaigns, calls, email, lists, saved searches, tasks, templates, user/credits.
- **Resources**: read-only `seamless://` URIs for credits and configuration.
- **Risk tiers / access control**: tools are labeled read / write / destructive, and access is gated by license per tool domain.
- **Quickstart**: docs.seamless.ai/mcp/quickstart (connect from Claude Desktop in ~60s).

## Pagination

All search endpoints use opaque token pagination:

1. First request: omit `nextToken` or set to `null`
2. Response includes `supplementalData.nextToken`
3. Subsequent requests: include the `nextToken` value
4. When `nextToken` is `null`, you've reached the end

Default `limit`: 50 results per page.

## Error Handling

| Status Code | Meaning | Action |
|---|---|---|
| `200` | Success | Process response |
| `202` | Accepted (async) | Poll for results |
| `401` | Unauthorized | Check API key or refresh OAuth token |
| `422` | Insufficient credits or missing license | Check credit balance; may need plan upgrade |
| `429` | Rate limited | Back off; check `X-RateLimit-Reset` header |
| `500` | Server error | Retry with exponential backoff |

## Credit Consumption

- Contact search/browse: **Free** (no credits consumed)
- Contact reveal (email/phone): **1 credit per contact**
- Company research: **Credits vary by plan**
- API research requests consume credits the same as UI reveals
- API usage draws from **Universal Credits only** (not search credits), and consumes the plan's existing credit balance — there is no separate API charge on top of the subscription. (Verified 2026-06-13.)

Monitor remaining credits via the `X-PublicAPI-Credits` response header.

## Best Practices

1. **Search before revealing**: Use search endpoints to browse results without consuming credits. Only call research endpoints on contacts you'll actually reach out to.
2. **Use webhooks for research**: The research/poll pattern adds latency. Configure webhooks for faster async delivery of enriched data.
3. **Respect rate limits**: 60 requests/minute per endpoint is the documented default, shared org-wide across all keys/users. Parse `X-RateLimit-Reset` and wait until that timestamp before retrying on a 429; when polling, use a 2–5s interval rather than tight looping. Contact your AE for higher org limits.
4. **Batch research requests**: Submit multiple `searchResultIds` in a single research call rather than one-at-a-time.
5. **Monitor credits**: Check `X-PublicAPI-Credits` in responses to avoid hitting zero mid-workflow.
