### Tomba REST API — Comprehensive Reference

**Base URL**: `https://api.tomba.io/v1/`
**Docs**: https://docs.tomba.io/
**Developer portal**: https://developer.tomba.io/ (redirects to docs.tomba.io)

---

## Authentication

All requests require two headers:

| Header | Format | Description |
|---|---|---|
| `X-Tomba-Key` | `ta_xxxx` | Your API key |
| `X-Tomba-Secret` | `ts_xxxx` | Your API secret |

**Where to find**: Manage keys at `app.tomba.io/api`

**Example**:
```bash
curl -H "X-Tomba-Key: ta_xxxx" \
     -H "X-Tomba-Secret: ts_xxxx" \
     "https://api.tomba.io/v1/domain-search?domain=stripe.com"
```

---

## SDKs

13+ official client libraries:

| Language | Package |
|---|---|
| JavaScript/Node | `tomba` |
| Python | `tomba` |
| PHP | `tomba/tomba` |
| Ruby | `tomba` |
| Go | `github.com/tomba-io/go` |
| Rust | `tomba` |
| C# | `Tomba` |
| Dart | `tomba` |
| Elixir | `tomba` |
| Lua | `tomba` |
| Perl | `Tomba` |
| R | `tomba` |

SDK initialization pattern (all languages follow this):
```javascript
const Tomba = require("tomba");
const client = new Tomba();
client.setKey("ta_xxxx").setSecret("ts_xxxx");
```

---

## Response Format

All successful responses return HTTP 200 with JSON.

### Error Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request — missing or invalid parameters |
| 429 | Rate limit exceeded — back off and retry (see Rate Limits below) |

---

## Core Endpoints

### Domain Search

Find all email addresses at a domain.

```
GET /v1/domain-search
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes* | Domain to search (e.g., `stripe.com`) |
| `company` | string | Yes* | Company name (3-75 chars) — alternative to domain |
| `page` | integer | No | Page number (default: 1) |
| `limit` | enum | No | Results per page: `10`, `20`, `50` (default: `10`) |
| `department` | enum | No | Filter by department: engineering, sales, finance, hr, it, marketing, operations, management, executive, legal, support, communication, software, security, pr, warehouse, diversity, administrative, facilities, accounting |
| `type` | enum | No | Filter by `personal` or `generic` email addresses (per official docs) |
| `country` | string | No | Two-letter country code *(not listed in current official param table — verify)* |
| `enrich_mobile` | boolean | No | Include phone numbers in results *(not listed in current official param table — verify)* |
| `webhook_url` | string | No | URL to receive async results *(not listed in current official param table — verify)* |

*Provide either `domain` or `company`. Current official docs (docs.tomba.io/api/domain-search) list params as: `domain`, `page`, `limit`, `department`, `type`. Path verified as `GET /v1/domain-search/?domain=:domain`.

**Response** (200):
```json
{
  "data": {
    "organization": {
      "website_url": "stripe.com",
      "organization": "Stripe",
      "location": { ... },
      "social_links": { "twitter_url": "...", "linkedin_url": "..." },
      "industries": "Financial Services",
      "founded": "2010",
      "company_size": "1001-5000",
      "company_type": "privately held",
      "revenue": "$1B+",
      "description": "...",
      "pattern": "{first}.{last}",
      "total_similar": 50,
      "keywords": ["payments", "fintech"],
      "ranking": 150,
      "whois": { ... },
      "last_updated": "2026-01-15"
    },
    "emails": [
      {
        "email": "john.doe@stripe.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "gender": "male",
        "phone_number": "+1...",
        "type": "personal",
        "country": "US",
        "position": "Software Engineer",
        "department": "engineering",
        "seniority": "senior",
        "twitter": "johndoe",
        "linkedin": "https://linkedin.com/in/johndoe",
        "score": 90,
        "verification": { "status": "valid" },
        "sources": [{ "uri": "https://...", "extracted_on": "2025-06-01" }]
      }
    ]
  },
  "meta": {
    "total": 250,
    "pageSize": 10,
    "current": 1,
    "total_pages": 25,
    "params": { "domain": "stripe.com" }
  }
}
```

---

### Email Finder

Find a specific person's email from their name and company.

```
GET /v1/email-finder
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes* | Company domain |
| `company` | string | Yes* | Company name |
| `full_name` | string | Yes* | Person's full name |
| `first_name` | string | Yes* | First name |
| `last_name` | string | Yes* | Last name |
| `enrich_mobile` | boolean | No | Include phone number |
| `webhook_url` | string | No | Async callback URL |

*Provide domain or company, plus full_name or first_name+last_name.

**Response** (200): Person object with email, confidence score, verification status, sources, and enriched profile data.

---

### Email Verifier

Validate an email address for deliverability.

```
GET /v1/email-verifier/:email
```

The email is passed as a **path segment**, not a query parameter (e.g. `GET /v1/email-verifier/b.mohamed@tomba.io`). Verified against docs.tomba.io.

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `email` | string (path) | Yes | Email address to verify (URL path segment) |

**Response** (200): Verification result with status (valid, invalid, accept_all, unknown), disposable check, webmail check, and detailed validation results.

---

### Email Enrichment

Enrich an email with person and company data.

```
GET /v1/enrich
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to enrich |
| `enrich_mobile` | boolean | No | Include phone data |
| `webhook_url` | string | No | Async callback URL |

**Response** (200): Person object with full name, title, company, social profiles, location, and phone data.

---

### Author Finder

Find the author of an online article.

```
GET /v1/author-finder
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | Article URL |
| `webhook_url` | string | No | Async callback URL |

**Response** (200): Person object with author's email, name, company, position, verification status, and sources.

---

### LinkedIn Finder

Find an email from a LinkedIn profile URL.

```
GET /v1/linkedin
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | LinkedIn profile URL |
| `enrich_mobile` | boolean | No | Include phone data |
| `full` | boolean | No | Return all associated emails |
| `webhook_url` | string | No | Async callback URL |

**Response** (200): Person object or array (if `full=true`) with email(s) and comprehensive profile data.

---

### Email Count

Get a count overview of emails at a domain.

```
GET /v1/email-count
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | Domain to count |

**Response** (200):
```json
{
  "data": {
    "total": 1250,
    "personal_emails": 1100,
    "generic_emails": 150,
    "department": {
      "engineering": 400,
      "sales": 200,
      "marketing": 150,
      "hr": 50,
      "finance": 75,
      "it": 100,
      "management": 80,
      "operations": 50,
      "legal": 30,
      "support": 65,
      "communication": 50
    },
    "seniority": {
      "junior": 500,
      "senior": 550,
      "executive": 200
    }
  }
}
```

---

### Email Format

Get the email pattern(s) used at a domain.

```
GET /v1/email-format
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | Domain to check |

**Response** (200):
```json
{
  "data": [
    { "format": "{first}.{last}", "percentage": 85 },
    { "format": "{first}", "percentage": 10 },
    { "format": "{f}{last}", "percentage": 5 }
  ]
}
```

---

### Phone Finder

Find phone data for a contact. Per current official docs the lookup is **based on an email address** (passed as a path segment), not a domain.

```
GET /v1/phone/:email
```

Example: `GET /v1/phone/someone@zapier.com`. Verified against docs.tomba.io.

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `email` | string (path) | Yes | Email address to look up phone data for (URL path segment) |

**Response** (200): Phone object with `email`, `valid` (bool), and formatted numbers: `local_format`, `intl_format`, `e164_format`, `rfc3966_format`.

---

## Utility Endpoints

### Email Sources

Find where an email address appears on the web.

```
GET /v1/email-sources/:email
```

The email is passed as a **path segment** (e.g. `GET /v1/email-sources/b.mohamed@tomba.io`). Verified against docs.tomba.io.

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `email` | string (path) | Yes | Email to find sources for (URL path segment) |

**Response** (200):
```json
{
  "email": "m@wordpress.org",
  "data": [
    {
      "uri": "https://example.com/about",
      "extracted_on": "2025-03-15",
      "last_seen_on": "2026-01-20",
      "still_on_page": true,
      "website_url": "example.com"
    }
  ]
}
```

---

### Domain Status

Check if a domain is webmail or disposable.

```
GET /v1/domain-status
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | Domain to check |

**Response** (200): Object with webmail and disposable boolean flags.

---

### Similar Domains

Find similar/competitor domains.

```
GET /v1/similar
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | Domain to find similar matches |

**Response** (200):
```json
{
  "data": [
    { "website_url": "competitor.com", "name": "Competitor Inc" }
  ]
}
```

---

### Technology Detection

Detect the tech stack of a domain. Verified against docs.tomba.io (`GET /v1/technology`).

```
GET /v1/technology
```

**Parameters**:

| Param | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | Domain to analyze |

**Response** (200):
```json
{
  "domain": "tomba.io",
  "data": [
    {
      "slug": "google-analytics",
      "name": "Google Analytics",
      "icon": "...",
      "website": "https://analytics.google.com",
      "categories": [{ "id": 1, "slug": "analytics", "name": "Analytics" }]
    }
  ]
}
```

---

## Account, Usage & Logs Endpoints

These are documented in current official docs (docs.tomba.io) and were previously flagged as gaps.

### Account

```
GET /v1/me
```

Retrieve account info: name, email, subscription/plan, `expired_subscription`, available credit counts (e.g. `available_email_count`), and a `requests` usage object.

### Usage

```
GET /v1/usage
```

Returns usage data points (`usage`, `created_at`, `name`) plus a `total` block. Tracks API consumption over time.

### Logs

```
GET /v1/logs
```

Returns recent requests: `uri`, `user_agent`, `cost` (bool — `false` = free, `true` = 1 request charged), `ip_address`, `created_at`, `country`. The dashboard shows up to 1,000 recent requests from the past 90 days and offers CSV download.

### API Keys

```
GET    /v1/keys           # list API keys
POST   /v1/keys           # create a key
GET    /v1/keys/:id       # get a key
PUT    /v1/keys/:id       # update a key
DELETE /v1/keys/:id       # delete a key
```

---

## Leads & Lead Lists Endpoints

Full CRUD for leads, lead lists, and lead attributes is documented in current official docs (docs.tomba.io/api/leads). Previously flagged as a gap — now confirmed.

### Leads

```
GET    /v1/leads            # paginated list of leads (optional ?domain= filter)
POST   /v1/leads            # create a lead
GET    /v1/leads/:id        # get a lead
PUT    /v1/leads/:id        # update a lead
DELETE /v1/leads/:id        # delete a lead
```

### Lead Lists

```
GET    /v1/leads_lists      # list lead lists
POST   /v1/leads_lists      # create a lead list
GET    /v1/leads_lists/:id  # get a lead list
PUT    /v1/leads_lists/:id  # update a lead list
DELETE /v1/leads_lists/:id  # delete a lead list
```

Note the path uses an **underscore**: `leads_lists`, not `lead-lists`.

### Lead Attributes

```
GET /v1/attributes          # list lead attributes
GET /v1/attributes/:id      # get a specific lead attribute
```

Access enriched metadata for leads (e.g. `attributes/38`, `attributes/41`).

---

## Bulk Operations

All core endpoints have bulk equivalents for processing thousands of records. Bulk jobs are asynchronous — use the `webhook_url` parameter to receive results when processing completes.

- **Email Verifier Bulk**: Up to 10,000 emails per batch
- **Email Finder Bulk**: Batch name+domain lookups
- **Domain Search Bulk**: Batch domain searches
- **LinkedIn Finder Bulk**: Batch LinkedIn URL lookups
- **Email Enrichment Bulk**: Batch email enrichment
- **Phone Finder Bulk**: Batch phone lookups

*Note: Bulk endpoint documentation is incomplete in the public docs. Check https://docs.tomba.io/ for the latest bulk API specifications.*

---

## Webhooks

Several endpoints support a `webhook_url` parameter for asynchronous result delivery:

- Domain Search (when processing large domains)
- Email Finder
- Author Finder
- LinkedIn Finder
- Email Enrichment
- Bulk operations

When provided, the API returns immediately and POSTs results to your webhook URL when processing completes.

*Note (re-verified 2026-06-13): A webhooks feature and the `webhook_url` parameter are NOT documented anywhere in current official docs (docs.tomba.io) — no webhooks page, and `webhook_url` is absent from the published param tables (e.g. domain-search lists only domain/page/limit/department/type). The webhook claims here (including any Pro-plan gating) are UNVERIFIED against current docs and may be outdated. Do not build webhook-dependent workflows without confirming directly with Tomba support.*

---

## Rate Limits

The API returns `429 Too Many Requests` when rate limits are exceeded. Current official docs (docs.tomba.io/rate-limits) publish **per-endpoint** limits:

| Endpoint(s) | Per second | Per minute |
|---|---|---|
| Domain Search, Email Finder, Similar, Technology | 15 | 900 |
| Enrichment, Reveal Search | 5 | 300 |
| Author Finder, Email Verifier | 2.5 | 150 |
| LinkedIn Email Finder | 1.67 | 100 |

Every response carries these headers:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Total requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests left in the current window |
| `X-RateLimit-Reset` | Seconds until the limit resets |

On a `429`, wait the number of seconds in `X-RateLimit-Reset` before retrying. Paid plans come with higher monthly limits.

**Best practices**:
- Honor `X-RateLimit-Reset` (and use exponential backoff as a fallback) on 429 responses
- Use bulk endpoints instead of looping individual calls
- Cache results to avoid redundant lookups
- Monitor your usage at `app.tomba.io/usage` or via `GET /v1/usage`

---

## Pagination

List endpoints (Domain Search) support pagination:

| Param | Default | Description |
|---|---|---|
| `page` | 1 | Page number |
| `limit` | 10 | Results per page (10, 20, or 50) |

Response includes `meta` with `total`, `pageSize`, `current`, and `total_pages`.

---

## Integrations

### MCP (Model Context Protocol)
Tomba provides an MCP server for AI agent integration:
- **Local server**: Run on your machine for development
- **Remote server**: Cloud-hosted for production use

### Zapier
Available triggers and actions for automation workflows connecting Tomba to 8,000+ apps.

### Additional
Make, n8n, Apify, Steampipe, Pipedream, Maltego — see https://docs.tomba.io/introduction for the full list.

---

## Gaps (flagged for manual review)

- **Webhooks**: No webhook feature or `webhook_url` parameter appears in current official docs (docs.tomba.io has no webhooks/`webhook_url` page). The webhook claims in this skill are UNVERIFIED against current docs — treat with caution and confirm before building webhook-dependent workflows.
- **Bulk operations**: bulk endpoint paths and request formats not detailed in current public docs.
- The `country` and `enrich_mobile` parameters on domain-search are not listed in the current official domain-search param table (verify before relying on them).

**Resolved since last capture** (now documented in current official docs):
- Per-endpoint rate limits + `X-RateLimit-*` headers (see Rate Limits above)
- Account (`GET /v1/me`), Usage (`GET /v1/usage`), Logs (`GET /v1/logs`), API Keys (`/v1/keys` CRUD)
- Lead management CRUD: `/v1/leads`, `/v1/leads_lists`, `/v1/attributes`
