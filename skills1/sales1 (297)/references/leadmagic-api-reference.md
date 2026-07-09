# LeadMagic API Reference

## Overview

| Property | Value |
|----------|-------|
| Base URL | `https://api.leadmagic.io` |
| Auth | API key via `X-API-Key` header |
| Response format | JSON |
| Response times | <200ms average |
| Uptime | 99.9% |
| Credits | Pay-per-result — failed lookups (null) cost 0 credits |
| Docs | leadmagic.io/docs/v1/introduction |
| OpenAPI spec | github.com/LeadMagic/leadmagic-openapi |
| MCP Server | github.com/LeadMagic/leadmagic-mcp |

> **Re-verified 2026-06-13** against live docs (leadmagic.io/docs). The endpoint surface has grown to 20+ endpoints, including new V3 search endpoints (People Search, Company Search, Job Search). Rate limits are now documented globally (see Rate Limits below). Webhooks now exist for async/batch enrichment.

## Rate Limits

Per the [Making API Calls](https://leadmagic.io/docs/v1/making-api-calls) guide and per-endpoint reference pages:

- **Default: 300 requests/minute** (~5 req/sec burst) on most endpoints (Email Finder, Email Validation, Mobile Finder, etc.).
- **100 requests/minute** (~2 req/sec burst) on **Profile Search** and **Company Search**.
- Analytics/credit checks: no documented limit.
- Rate limits are subject to change; custom limits available on Enterprise plans.

Responses include rate-limit and credit headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, plus `X-Credits-Remaining` and `X-Credits-Cost`.

## Authentication

All requests require an `X-API-Key` header:

```bash
curl -X POST "https://api.leadmagic.io/v1/people/email-finder" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "last_name": "Doe", "company_name": "acme.com"}'
```

Get your API key from: Sign up at app.leadmagic.io → Settings → API

## Endpoints by Category

### Credits

```
GET /v1/credits
```

**Credits**: 0 (free)

**Returns**: Current credit balance.

---

### People Data

#### Email Finder

```
POST /v1/people/email-finder
```

**Credits**: 1 per valid result (0 if not found)

**Rate limit**: 300 requests/minute (~5 req/sec burst)

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `first_name` | Conditional | Contact's first name (required if `full_name` not provided) |
| `last_name` | Conditional | Contact's last name (required if `full_name` not provided) |
| `full_name` | Conditional | Full name (alternative to first/last) |
| `domain` | Preferred | Company website domain (most accurate) |
| `company_name` | Conditional | Company name (use if domain unavailable) |

**Returns**: Verified work email address. 97% accuracy claimed.

#### Email Validation

```
POST /v1/people/email-validation
```

**Credits**: 0.25 per validation

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `email` | Yes | Email address to validate |

**Returns**: Validation status (`valid`, `invalid`, `unknown`), catch-all detection, deliverability score. Real-time SMTP verification.

#### Mobile Finder

```
POST /v1/people/mobile-finder
```

**Credits**: 5 per valid result (0 if not found)

**Parameters:** (at least one identifier required)
| Parameter | Required | Description |
|-----------|----------|-------------|
| `profile_url` | Conditional | Professional profile URL — highest match rate |
| `work_email` | Conditional | Professional/work email address |
| `personal_email` | Conditional | Personal email address |

Profile URL provides the highest match rate; combine with email for best results.

**Returns**: Direct dial mobile number.

#### Profile Search

```
POST /v1/people/profile-search
```

**Credits**: 1

**Rate limit**: 100 requests/minute (~2 req/sec burst)

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `profile_url` | Yes | Professional profile URL or username (accepts full URL or just username) |
| `extended_response` | No | Boolean (default false) — include profile image URL in response |

**Returns**: Work history, education, skills, current role, and professional details.

#### Email to Profile

```
POST /v1/people/b2b-profile
```

**Credits**: 10 per result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `email` | Yes | Work email address |

**Returns**: B2B profile URL and professional details.

#### Profile to Email (B2B Social to Email)

```
POST /v1/people/b2b-profile-email
```

**Credits**: 1-2 per valid result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | LinkedIn or B2B profile URL |

**Returns**: Verified work email address.

#### Personal Email Finder

```
POST /v1/people/personal-email-finder
```

**Credits**: 1-2 per valid result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | B2B profile URL |

**Returns**: Personal email address (Gmail, Outlook, etc.).

#### Role Finder

```
POST /v1/people/role-finder
```

**Credits**: 1-2 per result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `company_name` | Yes | Company domain or name |
| `role` | Yes | Role/title to search for (e.g., "VP Sales") |

**Returns**: Contact(s) matching the role at the specified company.

#### Employee Finder

```
POST /v1/people/employee-finder
```

**Credits**: 0.05 per employee

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `company_name` | Yes | Company domain or name |

**Returns**: List of employees at the company. Low-cost bulk discovery endpoint.

#### Job Change Detector

```
POST /v1/people/job-change
```

**Credits**: 3 per result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `email` | Conditional | Contact's email |
| `url` | Conditional | Contact's LinkedIn URL |

**Returns**: Whether the contact has changed jobs, new company and role details.

---

### Company Data

#### Company Search

```
POST /v1/companies/company-search
```

**Credits**: 1 per company found (0 if not found)

**Rate limit**: 100 requests/minute (~2 req/sec burst)

**Parameters:** (at least one identifier required)
| Parameter | Required | Description |
|-----------|----------|-------------|
| `company_domain` | Conditional | Company website domain (most accurate) |
| `company_name` | Conditional | Company name (less precise, may match similar names) |
| `profile_url` | Conditional | Professional company profile URL or slug |

This is the simpler V1 "Enrich Company" path for domain-driven enrichment of a single known company. For criteria-based discovery across many companies, use **Company Search (V3)** below.

**Returns**: Firmographics (name, ID, industry, employee count, founding year, HQ location, revenue range, funding), social profiles, description, specialties, and competitor information.

#### Company Funding

```
POST /v1/companies/company-funding
```

**Credits**: 4 per result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `company_name` | Conditional | Company name |
| `domain` | Conditional | Company domain |

**Returns**: Funding rounds, investors, amounts, dates, and total funding.

---

### Jobs

#### Jobs Finder

```
POST /v1/jobs/jobs-finder
```

**Credits**: 1 per job result

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | Job search keywords |
| `country` | No | Country filter (use GET /v1/jobs/countries for options) |
| `job_type` | No | Job type filter (use GET /v1/jobs/job-types for options) |

**Returns**: Job listings matching the search criteria.

#### Job Countries Reference

```
GET /v1/jobs/countries
```

**Credits**: 0 (free)

**Returns**: List of available countries for job search filtering.

#### Job Types Reference

```
GET /v1/jobs/job-types
```

**Credits**: 0 (free)

**Returns**: List of available job type filters.

---

### Ads Intelligence

#### Google Ads Search

```
POST /v1/ads/google-ads-search
```

**Credits**: 1 per ad returned

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `domain` | Yes | Company domain to search ads for |

**Returns**: Google search ads — ad copy, keywords, landing page URLs.

#### Meta Ads Search

```
POST /v1/ads/meta-ads-search
```

**Credits**: 1 per ad returned

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `domain` | Yes | Company domain to search ads for |

**Returns**: Facebook/Instagram ads — creative, ad copy, engagement metrics.

#### B2B Ads Search

```
POST /v1/ads/b2b-ads-search
```

**Credits**: 1 per ad returned

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `domain` | Yes | Company domain to search ads for |

**Returns**: B2B display and social advertising campaigns.

#### B2B Ad Details

```
POST /v1/ads/b2b-ads-details
```

**Credits**: 1

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `ad_id` | Yes | Ad ID from B2B Ads Search results |

**Returns**: Detailed information about a specific B2B ad.

---

### V3 Search Endpoints (added 2026)

LeadMagic introduced unified V3 search endpoints for criteria-based discovery (single-target lookup OR broad multi-target search in one call). The older V1 enrich endpoints above remain available for simple single-record enrichment.

#### People Search (V3)

```
POST /v3/people/search
```

**Credits**: 1 per returned person (0 if no results). `+1` credit per returned raw email and `+5` per returned raw mobile when `include_contact_details: true`.

**Parameters:** Either a single company identifier (`company_domain`, `company_name`, or `linkedin_url`) OR `company_filters` for multi-company searches, plus optional people intent terms (`titles`, `roles`, `query`), people filters, and contactability requirements (`include_contact_details`). Supports `limit`/`offset` pagination.

**Notes**: This single endpoint replaces older V3 people variants (mixed search, ICP search, employees, by-title, people lookalike).

#### Company Search (V3)

```
POST /v3/companies/search
```

**Credits**: 1 per company returned (0 if no matches)

**Rate limit**: 100 requests/minute (~2 req/sec burst)

**Parameters:** Single lookup (`company_domain`, `website`, `company_name`, or `linkedin_url`) OR bulk discovery via `company_filters` (`company_domains`, `country_codes`, `industries`, `headcount_ranges`, technographics, funding stages, etc.). Supports `limit`/`offset` pagination and `preview: true` (returns counts without spending credits).

**Notes**: Single-target lookups return root-level legacy fields (`found`, `company`, `companyName`); broad searches return a `companies` array.

#### Job Search (V3)

```
POST /v3/jobs/search
```

Alias: `POST /v3/jobs-search` (simplified request shape; new integrations should use `/v3/jobs/search`).

**Credits**: 1 per returned job/signal (0 if no results)

**Parameters:** Filters for titles (include/exclude), occupation taxonomy (3 levels), companies, locations (countries/regions/states/cities), tags, salary ranges, seniority, languages, remote preference, job types, industries, company size, posting dates, plus pagination. Features include semantic title matching (`titles.vector: true`), facet aggregation (`includeFacets: true`), broad text matching (`mode: "deep"`), and auto-resolution of filter IDs (`autoResolve: true`).

## MCP Server

LeadMagic provides an official MCP (Model Context Protocol) server exposing the full enrichment toolset (all 20+ endpoints):

```bash
# Install and run
npx leadmagic-mcp

# Or configure in Claude Code / Cursor / Windsurf
# Environment variable: LEADMAGIC_API_KEY=your_key
```

**Supported clients**: Claude Code, Cursor, Windsurf, VS Code, Continue.dev, ChatGPT

**GitHub**: github.com/LeadMagic/leadmagic-mcp

## CLI

LeadMagic offers a command-line interface for terminal-based lookups:

```bash
# GitHub: github.com/LeadMagic/cold-email-cli
```

## Credit System

| Endpoint | Credits |
|----------|---------|
| Email Finder | 1 |
| Email Validation | 0.25 |
| Profile Search | 1 |
| Profile to Email | 1-2 |
| Personal Email Finder | 1-2 |
| Role Finder | 1-2 |
| Company Search | 1 |
| Employee Finder | 0.05 |
| Job Change Detector | 3 |
| Company Funding | 4 |
| Mobile Finder | 5 |
| Email to Profile | 10 |
| Ads endpoints | 1 per result |
| Get Credits | 0 |
| Job Countries/Types | 0 |

**Key rule**: You only pay for valid results. `not_found` / `null` results cost 0 credits.

## Error Handling

Standard error format:
```json
{"error": "error_type", "message": "Human-readable description"}
```

| Status | Meaning |
|--------|---------|
| 200 | Success — data returned |
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — invalid or missing API key |
| 403 | Forbidden — insufficient credits or access |
| 404 | Not Found — no data for this lookup (0 credits charged) |
| 429 | Rate Limited — throttle requests (300/min default; 100/min on Profile Search & Company Search) |
| 500 | Server Error — retry with backoff |

## Webhooks (async / batch enrichment)

As of 2026, LeadMagic supports webhooks for **asynchronous enrichment completion** (batch processing) — they fire when enrichment results are ready, ideal for large batches. Webhooks are configured from the **enrichment history dashboard**: open webhook settings, pick an integration platform (e.g. Clay, Smartlead, Instantly), add your webhook URL, and connect. Webhook delivery is included at no extra cost.

Note: synchronous single-record API calls remain request/response. The webhook surface is geared to batch/async flows and dashboard integrations rather than a general event bus. HMAC signing / signature verification of webhook payloads is **not documented** at the source pages reviewed — verify before relying on signature validation.

## Gaps & Limitations

- **Response schema inconsistencies**: Field naming mixes snake_case and camelCase across endpoints. Use the OpenAPI spec (github.com/LeadMagic/leadmagic-openapi) for exact field names.
- **Webhook payload/signing undocumented**: Webhooks exist for async/batch flows (see above), but the public docs reviewed do not specify event types, payload schema, or HMAC signing.
- **No native CRM write-back**: Results go to your application/pipeline. For CRM sync, use Clay, Zapier, Make, n8n, or the dashboard webhook integrations as middleware.
- **Credit costs for some endpoints are ranges (1-2)**: Exact credit consumption may depend on data completeness or source. Monitor via the `X-Credits-Remaining` / `X-Credits-Cost` response headers.
