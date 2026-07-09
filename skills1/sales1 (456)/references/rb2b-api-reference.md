# RB2B API Reference

## Overview

| Property | Value |
|----------|-------|
| Product | RB2B Identity Resolution API ("APIs V2", separate from pixel product) |
| Base URL | `https://api.rb2b.com/api/v1` |
| API account / docs / key portal | `https://ui.api.rb2b.com` |
| Auth | API key in `Api-Key` request header |
| HTTP method | **POST** with JSON body (not GET with query params) |
| Pricing | Credit-based, prepaid, credits never expire; per-endpoint credit cost varies (1–4) |
| Rate limit | **50 requests/second per endpoint** |
| Response format | JSON |
| MCP server | Official `@rb2b/rb2b-apis-mcp` (npm) — `npx -y @rb2b/rb2b-apis-mcp init` |

**Important**: The RB2B API is a **separate product** from the pixel-based visitor identification. It is the "APIs V2" / API Partner Program with its own account, unified credit balance, and per-endpoint credit costs. Sign up and manage keys at `https://ui.api.rb2b.com`.

## Authentication

All requests are **POST** with a JSON body and require an API key passed in the `Api-Key` header:

```bash
curl -X POST https://api.rb2b.com/api/v1/ip_to_company \
  -H "Api-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "203.0.113.42"}'
```

Obtain your API key from your RB2B API account at `https://ui.api.rb2b.com`. An invalid key returns `401`.

## Endpoints (APIs V2)

All endpoints are **POST** to `https://api.rb2b.com/api/v1/{endpoint}` with a JSON body and the `Api-Key` header. The input field name is shown per endpoint. Endpoint names and credit costs below are taken from RB2B's official `@rb2b/rb2b-apis-mcp` package (v1.1.7) and the `rb2b.com/apis` product page.

| Endpoint (path) | JSON input field | Output | Credits |
|-----------------|------------------|--------|---------|
| `/ip_to_company` | `ip_address` | Company domain / firmographics behind the IP | 1 |
| `/ip_to_hem` | `ip_address` | Hashed emails (MD5 + SHA256) for the IP | 1 |
| `/ip_to_maid` | `ip_address` | Mobile Advertising IDs (MAIDs) for the IP | 1 |
| `/email_to_linkedin_slug`* | `email` | LinkedIn slug / vanity URL for a plain-text email | 1 |
| `/email_to_best_linkedin`* | `email` | Best-matching LinkedIn URL for an email | 1 |
| `/email_to_business_profile`* | `email` | Business/company profile (employer, title) for an email | 2 |
| `/email_to_maid`* | `email` | MAIDs for an email | 1 |
| `/hem_to_linkedin` (slug) | `md5` | LinkedIn slug for a hashed email (MD5) | 1 |
| `/hem_to_best_linkedin` | `md5` | Best-matching LinkedIn URL for a hashed email | 1 |
| `/hem_to_business_profile` | `md5` | Business/company profile for a hashed email | 2 |
| `/hem_to_maid` | `md5` | MAIDs for a hashed email | 1 |
| `/linkedin_to_hashed_emails` | `linkedin_slug` | All hashed emails (HEMs) for a LinkedIn profile | 1 |
| `/linkedin_to_best_personal_email` | `linkedin_slug` | Best personal email for a LinkedIn profile | 1 |
| `/linkedin_to_personal_email` | `linkedin_slug` | All personal emails for a LinkedIn profile | 1 |
| `/linkedin_to_mobile_phone` | `linkedin_slug` | Mobile phone number for a LinkedIn profile | 3 |
| `/linkedin_to_business_profile` | `linkedin_slug` | Business/company profile for a LinkedIn profile | 4 |
| `/credits` | (none) | Remaining credit balance | 0 |

\* The official MCP client routes the `email_to_*` tools through the corresponding `/hem_to_*` paths, passing the plain-text address as `email`; treat `email_to_*` as the logical operation and `hem_to_*` as the underlying path.

**Key shape notes** (verified from the official MCP client):
- Inputs use snake_case: `ip_address`, `email`, `md5` (MD5-hashed email), and `linkedin_slug` (the vanity slug, e.g. `john-doe-123`, not a full URL).
- Hashed-email endpoints take the **MD5** hash as `md5`. `ip_to_hem` returns both MD5 and SHA256.
- Credit cost is **per endpoint** (1–4), not a flat 1 per lookup.

### Mobile Ad ID status

- `IP → MAID` (`/ip_to_maid`) and `HEM → MAID` (`/hem_to_maid`) are **live**.
- `MAID → HEM` (reverse) is still marked **Coming Soon** on the `rb2b.com/apis` page and is **not** exposed by the official MCP client.

### Credits check

```bash
curl -X POST https://api.rb2b.com/api/v1/credits \
  -H "Api-Key: your_api_key" \
  -H "Content-Type: application/json"
```

Returns the remaining credit balance (`credits_remaining`). Costs 0 credits.

## Pixel Webhooks

The pixel product (separate from the API) can push visitor data via webhooks:

**Webhook payload** (when a visitor is identified):
```json
{
  "event": "visitor_identified",
  "visitor": {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "linkedin_url": "https://linkedin.com/in/janesmith",
    "title": "VP of Marketing",
    "company": "Example Corp",
    "city": "San Francisco",
    "state": "CA"
  },
  "visit": {
    "page_url": "https://yoursite.com/pricing",
    "timestamp": "2025-01-15T14:30:00Z",
    "referrer": "https://google.com",
    "hot_page": true
  },
  "company": {
    "name": "Example Corp",
    "domain": "example.com",
    "industry": "Technology",
    "employee_count": 500,
    "revenue_range": "$50M-$100M"
  }
}
```

Configure webhook URL in RB2B dashboard under Settings → Integrations → Webhooks.

## Credit Pricing

Credit batches are prepaid and **never expire**. Larger batches lower the per-credit cost. Tiers shown on the `rb2b.com/apis` page (illustrative — see the live page for the full ladder):

| Credits | Price | Per-credit cost |
|---------|-------|-----------------|
| 100 | $9 | $0.090 |
| 3,000 | $149 | ~$0.050 |
| 50,000 | $999 | ~$0.020 |
| 500,000 | $4,999 | ~$0.010 |
| 5,250,000 | $49,999 | ~$0.0095 |

**Per-endpoint cost varies** (1–4 credits) — see the endpoints table above. Business-profile lookups cost 2, `linkedin_to_mobile_phone` costs 3, and `linkedin_to_business_profile` costs 4. The credit balance is **unified across all API endpoints**.

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success — data returned |
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — invalid API key |
| 402 | Payment Required — insufficient credits |
| 404 | Not Found — no match for this lookup |
| 429 | Rate Limited — too many requests |
| 500 | Server Error — retry with backoff |

## Gaps & Limitations

- **API documentation is sparse**: Full response schemas are not publicly documented. The endpoint list, paths, input fields, and credit costs above are taken from RB2B's official `@rb2b/rb2b-apis-mcp` package (v1.1.7) and the `rb2b.com/apis` product page — actual response fields may differ.
- **MAID partially live**: `ip_to_maid` and `hem_to_maid` are live; the reverse `MAID → HEM` is still marked "Coming Soon" and is not in the official MCP client.
- **Rate limit**: 50 requests/second per endpoint (per RB2B's MCP client and `/apis` help text). A `429` indicates the limit was exceeded — back off and retry.
- **US-focused**: Like the pixel product, the API's person-level resolution has higher match rates for US-based data.
- **Official MCP server**: `@rb2b/rb2b-apis-mcp` (npm) exposes the endpoints above as MCP tools for Claude Code / Claude Desktop. Run `npx -y @rb2b/rb2b-apis-mcp init`; the key is stored in `~/.rb2b/config.json`. There is no documented language SDK; otherwise use direct HTTP requests.
- **Webhook schema is estimated**: The pixel-product webhook payload structure below is inferred from integration descriptions and may not exactly match the actual payload format. RB2B added webhook error reporting (timeouts/connection errors/bad response codes, Mar 2026) and redirect handling (Oct 2025) but does not publicly document the payload or signing.
