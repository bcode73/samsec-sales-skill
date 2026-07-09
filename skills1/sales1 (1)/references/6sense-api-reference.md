# 6sense API Reference

> Re-verified 2026-06-13 against the public 6sense API Portal (https://api.6sense.com/docs/) and support docs (https://support.6sense.com/docs/). Most detailed API docs have moved from the support portal to the API Portal, which is now publicly accessible.

## Overview

| Property | Value |
|----------|-------|
| Auth | `Authorization: Token {api_token}` — 40-character alphanumeric, org-level |
| Rate limit | 100 requests/minute general; People APIs (Enrichment, Search) 20 queries/second per customer; limits adjustable in integration settings |
| Response format | JSON (POST requests accept `application/x-www-form-urlencoded` or `application/json`) |
| Credits | Company Identification = 1 credit per matched response; Enrichment APIs share a credit pool; People Search and Lead Scoring deduct no credits |
| Docs | https://api.6sense.com/docs/ (public API Portal); https://support.6sense.com/docs/ (public support docs) |

**Note**: As of the 2026-06-13 re-verification, the core API docs are publicly viewable at the 6sense API Portal (api.6sense.com/docs). Some org-specific settings (which segments/score configs are published for API consumption) still live in the authenticated platform settings.

## Authentication

All requests use an API token passed as a header:

```bash
curl https://epsilon.6sense.com/v3/company/details?ip=8.8.8.8 \
  -H "Authorization: Token your_api_token"
```

- **Token format**: 40-character random alphanumeric key.
- **Generation**: Settings > Integration > API Token Management > "Generate New API token". Select an API Group (token type), a Token Name (max 26 chars), and an Integration platform. "Allowed domains" can be set for the Company Identification API token only. The token is shown once on generation — copy it immediately.
- **Scope**: Tokens are provisioned at the org level (not per-user). Create separate tokens per integration for isolation. Best practice: rotate every 90 days.
- **Token types**: (1) Company Identification API, (2) Enrichment APIs (People Enrichment, Company Firmographics, Lead Scoring & Firmographics), (3) Lead Scoring API, (4) Segments API, (5) Sales Intelligence App.
- **Security**: Only the Company Identification API token is designed for client-side use (via WebTag). Enrichment/Lead Scoring tokens must be kept server-side only — never expose them in client code.

## Endpoints by Category

### Company Identification API

Identify companies visiting your website by IP address.

```
GET https://epsilon.6sense.com/v3/company/details
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `ip` | Yes | IPv4 address to resolve |

**Returns**: Company match status, company ID, domain, industry, country/state/city, employee count, revenue range, SIC/NAICS codes, segment membership, confidence level. Similar to Clearbit Reveal or RB2B Company-Level ID.

**Rate limit**: 100 requests/minute. **Credits**: 1 API credit per matched response (repeat lookups of the same IP within a contract year are deduplicated).

**Use case**: Install via WebTag (JavaScript snippet) on your website, or call directly from your backend to identify anonymous visitors. This is the only API token type designed for client-side use.

### People Enrichment API

Enrich contacts with professional data. **This endpoint moved off `scribe.6sense.com` to the `api.6sense.com` host (v2).**

```
POST https://api.6sense.com/v2/enrichment/people
```

**Parameters** (provide at least one identifier per record):
| Parameter | Required | Description |
|-----------|----------|-------------|
| `peopleId` | Conditional | 6sense people ID |
| `email` | Conditional | Email address to enrich |
| `linkedinUrl` | Conditional | LinkedIn profile URL |
| `referenceKeys` | Optional | Custom metadata object for tracking/attribution |

**Batch**: Up to 25 queries (records) in a single API call. **Rate limit**: 20 queries/second per customer.

**Returns**: Contact ID, email (with confidence level), full/first/last name, title, education, skills, professional experience, location, social profiles, and associated company firmographics.

### Company Firmographics API

Enrich a company by email or domain.

```
POST https://api.6sense.com/v1/enrichment/company   (v3)
POST https://scribe.6sense.com/v2/people/enrichment  (v2, legacy)
```

**Parameters**: `email` OR `domain` required (email prioritized when both supplied). Optional: `country`, `company`, `industry`, `title`, `role`, `firstname`, `lastname`, `leadsource`.

**Returns**: Company ID, domain, name, region/country/state/city, address, postal code, phone, industry, employee/revenue ranges, SIC/NAICS data, segment IDs and names.

### Lead Scoring & Full Firmographics API

Get complete contact + company data with predictive scores.

```
POST https://scribe.6sense.com/v2/people/full
```

**Parameters**: `email` and `country` required. Optional: `website`, `company`, `title`, `leadsource`, `firstname`, `lastname`, `role`, `industry`.

**Returns**: Company data, product-level scores (intent score, buying stage, profile score, profile fit), contact-level scores (intent score, grade, profile score, profile fit), and segment membership (for segments published for APIs).

### Lead Scoring API

Returns predictive scores only (no firmographic enrichment). **Deducts no API credits.**

```
POST https://scribe.6sense.com/v2/people/score
```

**Parameters**: Same as Lead Scoring & Full Firmographics (`email` + `country` required).

**Returns**: Product-level company scores (intent / buying stage / profile metrics) and contact-level scores (intent / grade / profile metrics).

### People Search API

Search for contacts within organizations (by domain) with filters. Verifies whether an email/phone is available but does not return the actual contact details. **Deducts no API credits.**

```
POST https://api.6sense.com/v2/search/people   (v2)
POST https://api.6sense.com/v1/search/people   (v1, legacy)
```

**Batch**: Up to 25 queries per request. **Rate limit**: 20 queries/second per customer.

Use the **People Search Dictionary API** (`GET https://api.6sense.com/v2/search/dictionary`) to retrieve valid filter values.

### Segments API

Check which segments a company belongs to and get scoring data.

```
GET https://scribe.6sense.com/v2/company/segments
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `domain` | Conditional | Company domain |
| `company_name` | Conditional | Company name |

**Returns**: Segment membership, buying stage, intent scores, profile fit score, and 6QA status for the matched company. Useful for real-time personalization (website, email, ad targeting).

### API Settings: Segments and Score Configurations

Configure which segments and scoring models are available via API in the 6sense platform under Settings > API Configuration. You can publish multiple segments for API consumption, allowing different applications to query different audience definitions.

## WebTag (Company Identification JavaScript)

Install on your website for automatic visitor identification:

```html
<script>
  // 6sense WebTag 2.0
  // Installed via Google Tag Manager or directly in <head>
  // Configuration in 6sense platform settings
</script>
```

**Setup options**:
- Direct installation in `<head>` tag
- Google Tag Manager (GTM) — recommended for most teams
- GA4 integration for combined analytics

WebTag identifies companies visiting your site and feeds data into 6sense segments, workflows, and CRM in real-time.

## Credit System

- **Company Identification API**: 1 API credit per matched response. Re-enriching the same IP address within a contract year does not deduct additional credits.
- **Enrichment APIs** (People Enrichment, Company Firmographics, Lead Scoring & Firmographics): share a single Enrichment API Credit pool. Exporting the same record multiple times within the current calendar month is not charged again.
- **No-cost APIs**: People Search and Lead Scoring (`/v2/people/score`) deduct no credits.
- **Overage**: usage beyond your purchased quota is billable.
- Monitor usage in Settings > Integration > API Token Management.

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | OK — data returned |
| 201 | Created |
| 204 | No content |
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — invalid or expired API token |
| 402 | Quota exhausted — API credit allocation depleted |
| 403 | Forbidden — endpoint not provisioned for your org |
| 404 | Not Found — no match for this lookup |
| 422 | Validation error — request body failed validation |
| 429 | Too many requests — rate limit exceeded |
| 50X | Internal server error — retry with backoff |

Throttled requests fail outright rather than queuing; no documented `Retry-After` header, so implement your own exponential backoff.

## AI Email Agents API (Conversational Email)

The Conversational Email / AI Email Agents product (formerly Saleswhale) exposes its own API documented at https://docs.saleswhale.com/ (v2 at docs.saleswhale.com/#v2). Operations include create/delete a lead, list sales reps, list campaigns, show/cancel a conversation, and custom attributes. Webhooks are available on this product. This is a separate add-on with separate pricing and is not part of the core enrichment/identification API surface above.

## Gaps & Limitations

- **Some org-specific config still in-platform**: Which segments and score configurations are published for API consumption is set in the authenticated platform settings (Settings > API Configuration), not in the public API Portal.
- **Response schemas summarized**: Field lists above are from the public API Portal; use the portal's interactive docs (api.6sense.com/docs) for the full per-field schema.
- **No public SDKs**: 6sense does not publish official client libraries. Use direct HTTP requests.
- **Core-platform webhooks unclear**: The AI Email (Saleswhale) product supports webhooks; webhook events from the core ABM/intent platform are not documented on the public portal — check your integration settings.
- **Configurable rate limits**: The 100 req/min general limit can be adjusted in integration settings; confirm your org's effective limit before high-throughput batch jobs.
