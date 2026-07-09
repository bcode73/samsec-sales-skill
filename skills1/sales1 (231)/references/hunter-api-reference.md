# Hunter.io API Reference (v2)

## Overview

- **Base URL**: `https://api.hunter.io/v2/`
- **Authentication**: Three methods supported:
  - Query parameter: `?api_key=YOUR_API_KEY`
  - Header: `X-API-KEY: YOUR_API_KEY`
  - Header: `Authorization: Bearer YOUR_API_KEY`
- **Rate limits**: Limits are **per endpoint** (requests/second AND requests/minute), NOT per plan. Verified against live docs 2026-06-13:
  - Domain Search: 15 req/sec, 500 req/min
  - Email Finder: 15 req/sec, 500 req/min
  - Email Verifier: 10 req/sec, 300 req/min
  - Email Count: 15 req/sec
  - Enrichment (`/people/find`, `/companies/find`, `/combined/find`): 15 req/sec, 500 req/min
  - Discover: 5 req/sec, 50 req/min
  - (Earlier per-plan numbers of 150/300/600 req/min were not confirmed by current official docs; the docs publish per-endpoint limits as above.)
- **Test key**: `test-api-key` validates parameters and returns a fixed dummy response without consuming credits (works on Domain Search, Email Finder, Email Verifier).
- **Response format**: JSON. Responses use `data`, `meta`, and optional `errors` fields.
- **Credit system**: Hunter uses a single monthly **credit pool** (no separate search vs verification pools). 1 credit = 1 email found (Domain Search / Email Finder); 0.5 credit = 1 email verified (Email Verifier). Credits reset on billing date. Searches that return no results are not charged.

## Endpoints

### Domain Search

Find all email addresses associated with a domain.

**`GET /domain-search`**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes (or `company`) | Target company domain |
| `company` | string | Yes (or `domain`) | Company name (domain preferred for accuracy) |
| `limit` | integer | No | Max results to return (default 10) |
| `offset` | integer | No | Number of results to skip (for pagination) |
| `type` | string | No | `personal` or `generic` |
| `seniority` | string | No | Comma-separated: `junior`, `senior`, `executive` |
| `department` | string | No | Comma-separated: `executive`, `it`, `finance`, `management`, `sales`, `legal`, `support`, `hr`, `marketing`, `communication`, `education`, `design`, `health`, `operations` |
| `required_field` | string | No | Comma-separated fields that must be present: `full_name`, `position`, `phone_number` |

**Response** (key fields):
```json
{
  "data": {
    "domain": "stripe.com",
    "disposable": false,
    "webmail": false,
    "accept_all": false,
    "pattern": "{first}",
    "organization": "Stripe",
    "emails": [
      {
        "value": "patrick@stripe.com",
        "type": "personal",
        "confidence": 91,
        "first_name": "Patrick",
        "last_name": "Collison",
        "position": "CEO",
        "seniority": "executive",
        "department": "executive",
        "sources": [...],
        "verification": { "status": "valid", "date": "2025-01-15" }
      }
    ],
    "linked_domains": []
  },
  "meta": {
    "results": 150,
    "limit": 10,
    "offset": 0,
    "params": { "domain": "stripe.com" }
  }
}
```

**Credit cost**: 1 credit per email returned (live docs 2026-06-13 describe the credit model as 1 credit = 1 email found). Note: older Hunter documentation described "1 credit per 10 results" — the current unified-credit model charges per email found.

> Domain Search also accepts **POST** in addition to GET (current docs list `GET/POST /domain-search`), which is useful when you need to pass a long parameter set in the body.

---

### Email Finder

Find a specific person's email address.

**`GET /email-finder`**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes (or `company`) | Company domain |
| `company` | string | Yes (or `domain`) | Company name |
| `first_name` | string | Yes (or `full_name`) | First name |
| `last_name` | string | Yes (or `full_name`) | Last name |
| `full_name` | string | Yes (or first+last) | Full name |
| `max_duration` | integer | No | Max seconds to wait (for real-time lookup) |

**Response** (key fields):
```json
{
  "data": {
    "first_name": "Patrick",
    "last_name": "Collison",
    "email": "patrick@stripe.com",
    "score": 91,
    "domain": "stripe.com",
    "accept_all": false,
    "position": "CEO",
    "company": "Stripe",
    "sources": [...],
    "verification": { "status": "valid", "date": "2025-01-15" }
  }
}
```

**Credit cost**: 1 credit per successful find. No charge if no email found.

---

### Email Verifier

Verify deliverability of an email address.

**`GET /email-verifier`**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to verify |

**Response** (key fields):
```json
{
  "data": {
    "email": "patrick@stripe.com",
    "result": "deliverable",
    "score": 95,
    "status": "valid",
    "regexp": true,
    "gibberish": false,
    "disposable": false,
    "webmail": false,
    "mx_records": true,
    "smtp_server": true,
    "smtp_check": true,
    "accept_all": false,
    "block": false,
    "sources": [...]
  }
}
```

**Verification statuses**: `valid`, `invalid`, `accept_all`, `webmail`, `disposable`, `unknown`

**Async behavior (verified 2026-06-13)**: If the verifier cannot finish within ~20 seconds it returns HTTP **202** instead of 200. Poll the same `GET /email-verifier?email=...` endpoint until it returns 200 with the final result. Build retry/polling into any integration that verifies in real time.

**Credit cost**: 0.5 credit per verification (current unified-credit model: 0.5 credit = 1 email verified).

---

### Email Count

Get the number of email addresses Hunter knows for a domain or company. Free (no credits) and does not require authentication for the public count.

**`GET /email-count`**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes (or `company`) | Target domain |
| `company` | string | Yes (or `domain`) | Company name |
| `type` | string | No | `personal` or `generic` to count a single type |

**Rate limit**: 15 req/sec.

---

### Enrichment (People / Company / Combined)

Retrieve enriched data about a person and/or their company. (Verified present in current API docs 2026-06-13.)

**`GET /people/find`** — Email Enrichment: pass an `email` to retrieve person information (name, role, social profiles, etc.).

**`GET /companies/find`** — Company Enrichment: pass a `domain` to retrieve company information (size, industry, location, tech stack, etc.).

**`GET /combined/find`** — Combined Enrichment: pass an `email` to retrieve both the person and their company in one call.

**Rate limit**: 15 req/sec, 500 req/min for each enrichment endpoint.

---

### Leads

Manage leads saved in your Hunter account.

**`GET /leads`** — List all leads

| Parameter | Type | Required | Description |
|---|---|---|---|
| `offset` | integer | No | Pagination offset |
| `limit` | integer | No | Results per page (max 100) |
| `lead_list_id` | integer | No | Filter by lead list |
| `email` | string | No | Filter by email |
| `company` | string | No | Filter by company |

**`POST /leads`** — Create a lead

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address |
| `first_name` | string | No | First name |
| `last_name` | string | No | Last name |
| `position` | string | No | Job title |
| `company` | string | No | Company name |
| `company_industry` | string | No | Industry |
| `company_size` | string | No | Employee count range |
| `phone_number` | string | No | Phone number |
| `twitter` | string | No | Twitter handle |
| `linkedin_url` | string | No | LinkedIn profile URL |
| `notes` | string | No | Notes |
| `leads_list_id` | integer | No | Lead list to add to |
| `source` | string | No | Lead source |

**`GET /leads/{id}`** — Get a specific lead

**`PUT /leads/{id}`** — Update a lead

**`DELETE /leads/{id}`** — Delete a lead

---

### Leads Lists

Manage lead list collections.

**`GET /leads_lists`** — List all lead lists

**`POST /leads_lists`** — Create a lead list

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | List name |

**`GET /leads_lists/{id}`** — Get a specific list

**`PUT /leads_lists/{id}`** — Update a list

**`DELETE /leads_lists/{id}`** — Delete a list

---

### Campaigns (Sequences API)

Manage cold email campaigns. In the current docs this is the **Sequences API** ("campaigns" and "sequences" are used interchangeably; the path is still `/campaigns`). The documented capabilities are: list sequences, check status/targeting, list recipients, add a recipient, cancel scheduled emails to a recipient, and start a sequence.

**`GET /campaigns`** — List all campaigns/sequences (verified 2026-06-13)

**`GET /campaigns/{id}`** — Get campaign details

> **UNVERIFIED (2026-06-13)**: `POST /campaigns` (create), `PUT /campaigns/{id}` (update), and `DELETE /campaigns/{id}` (delete) are not confirmed in current official docs — the documented Sequences API exposes read + recipient management + start, but not full CRUD on the campaign object itself. Treat campaign creation/editing as a UI operation unless Hunter confirms an endpoint.

#### Campaign Recipients

**`GET /campaigns/{campaign_id}/recipients`** — List recipients (verified 2026-06-13). Each recipient includes `email`, `first_name`, `last_name`, `position`, `company`, `website`, `sending_status`, and `lead_id`.

**`POST /campaigns/{campaign_id}/recipients`** — Add a recipient to the sequence (verified 2026-06-13)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `emails` | array | Yes | Array of email objects with optional fields (first_name, last_name, company, etc.) |

**`DELETE /campaigns/{campaign_id}/recipients/{id}`** — Cancel scheduled emails to a recipient (verified 2026-06-13)

#### Start a sequence

**`POST /campaigns/{campaign_id}/start`** — Start the sequence so scheduled emails begin sending (the docs list "Start a sequence" as an available method).

> **UNVERIFIED (2026-06-13)**: `GET /campaigns/{campaign_id}/sends` (send history with open/click/reply tracking) is not confirmed in current official docs. Recipient `sending_status` (from the recipients endpoint) is the confirmed way to read per-recipient send state.

---

### Discover

Search for companies matching specific criteria. Accepts a natural-language `query` plus structured filter objects.

**`POST /discover`** (verified 2026-06-13 — this endpoint is a **POST**, not GET; parameters are sent in the JSON body, including filter objects such as `headquarters_location` and `industry`)

Example body:
```json
{
  "query": "US-based Software companies",
  "headquarters_location": { ... },
  "industry": { ... }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | No | Natural-language search (e.g., "US-based Software companies") |
| `headquarters_location` | object | No | Location filter |
| `industry` | object | No | Industry filter |
| `size` | object/string | No | Employee count range |
| `technology` | object/string | No | Technology stack filter (Hunter now extracts tech from job postings; 1,800+ technologies) |

**Rate limit**: 5 req/sec, 50 req/min.

**Response**: Returns company objects with domain, description, industry, size, location, and social profiles.

**Credit cost**: Credits consumed per company returned (Discover is part of the unified credit model). Domain Search / Email Finder on results consume additional credits for emails.

---

### TechLookup / technology filtering

Find companies using a specific technology.

> **UNVERIFIED (2026-06-13)**: A dedicated `GET /technology-lookup` REST endpoint is **not confirmed** in current official API docs. As of 2026, Hunter exposes technographic data primarily as a **filter inside Discover** (`POST /discover`, `technology` filter) and as company tech-stack data in **Domain Search** results (Hunter extracts technologies from job postings; 1,800+ technologies covered). TechLookup also exists as a standalone web tool at `hunter.io/techlookup` with free CSV downloads. Prefer the Discover `technology` filter for programmatic technographic prospecting; leave the standalone endpoint below unused unless Hunter documents it.

**`GET /technology-lookup`** (unverified — may not exist as a public API endpoint)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `technology` | string | Yes | Technology name (e.g., "Salesforce", "React", "Shopify") |
| `limit` | integer | No | Max results |
| `offset` | integer | No | Pagination offset |

---

### Account

**`GET /account`** — Get account information including plan, credits remaining, and usage.

---

### Bulk Operations

> **UNVERIFIED (2026-06-13)**: The dedicated bulk REST endpoints below (`/domain-search/bulk`, `/email-finder/bulk`, `/email-verifier/bulk`) are **not confirmed** in current official API docs. Hunter offers Bulk tasks (Bulk Domain Search, Bulk Email Finder, Bulk Email Verifier — up to 25,000 domains/items per bulk) primarily through the **Bulk section of the dashboard** and the **Data Platform**; the dashboard processes them asynchronously. If you need programmatic bulk, confirm endpoint availability with Hunter or loop the single-record endpoints within the per-endpoint rate limits. Endpoint shapes below are retained from prior research and may not match a real API.

#### Bulk Domain Search

**`POST /domain-search/bulk`** — Submit bulk domain search job

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domains` | array | Yes | Array of domain strings |

**`GET /domain-search/bulk/{id}`** — Check bulk job status and retrieve results

#### Bulk Email Finder

**`POST /email-finder/bulk`** — Submit bulk email finder job

| Parameter | Type | Required | Description |
|---|---|---|---|
| `items` | array | Yes | Array of objects with `domain`, `first_name`, `last_name` |

**`GET /email-finder/bulk/{id}`** — Check bulk job status and retrieve results

#### Bulk Email Verifier

**`POST /email-verifier/bulk`** — Submit bulk verification job

| Parameter | Type | Required | Description |
|---|---|---|---|
| `emails` | array | Yes | Array of email strings |

**`GET /email-verifier/bulk/{id}`** — Check bulk job status and retrieve results

---

## Webhooks

> **UNVERIFIED (2026-06-13)**: The current official Hunter API reference does **not** document a webhooks system or event payload signing. The campaign-event list below is retained from prior research and could not be confirmed against live docs — do not rely on it without verifying in Hunter's docs/settings. For real-time campaign events, check the campaign/sequence settings in the Hunter dashboard.

Previously documented (unconfirmed) campaign events:
- Email sent
- Email opened
- Link clicked
- Reply received
- Bounce detected

Webhook payloads were said to include campaign ID, recipient details, and event-specific data.

---

## Pagination

- Use `offset` and `limit` parameters for paginated endpoints
- Default `limit` varies by endpoint (typically 10-20)
- `meta` object in response includes total `results` count

## Error Handling

Standard HTTP status codes (verified 2026-06-13):
- `200` — Success
- `201` — Created (e.g., a resource was created)
- `202` — Accepted but not complete (Email Verifier still processing — poll the same endpoint)
- `204` — No Content (e.g., successful delete)
- `400` — Bad request (invalid parameters)
- `401` — Unauthorized (invalid API key)
- `403` — Forbidden (insufficient credits or plan)
- `404` — Not found
- `422` — Unprocessable Entity (validation failed)
- `429` — Too Many Requests (rate limit exceeded)
- `451` — Unavailable for Legal Reasons
- `5XX` — Server error

Error responses include an `errors` array with descriptive messages.

## MCP Server

Hunter.io provides an official **Remote MCP Server** for AI agent integration (verified 2026-06-13).

> **DEPRECATED**: The old local Python package (`hunter-io/hunter-mcp`, `pip install hunter-mcp`) is **no longer maintained**. The GitHub README states: "⚠️ Deprecated - Please Switch to Hunter's Remote MCP Server ⚠️ This repository is no longer maintained. All functionality has moved to Hunter's Remote MCP Server." Do not recommend the pip install path.

**Remote MCP Server (current):**
- **Streamable HTTP endpoint**: `https://mcp.hunter.io/mcp` (recommended for OpenAI Responses API and modern MCP clients)
- **SSE endpoint**: `https://mcp.hunter.io/sse` (for clients using Server-Sent Events, e.g. Claude Desktop via `mcp-remote`)
- **Authentication**: pass your Hunter API key in request headers — either `Authorization: Bearer HUNTER_API_KEY` or `X-API-KEY: HUNTER_API_KEY`
- **Docs**: `https://hunter.io/api-documentation#mcp`
- **Capabilities**: exposes Hunter's B2B data tools (email finding, verification, enrichment, company insights) to MCP clients; integrates with OpenAI, Anthropic, and Google platforms.

## Rate Limit Headers

Responses include rate limit headers:
- `X-RateLimit-Limit` — requests allowed per minute
- `X-RateLimit-Remaining` — requests remaining in current window
- `X-RateLimit-Reset` — seconds until rate limit resets
