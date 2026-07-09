<!-- Source: https://data.g2.com/api/v2/docs/index.html and https://documentation.g2.com/docs/developer-portal -->
<!-- Re-verified 2026-06-13 against documentation.g2.com (developer-portal, g2-api-information, g2-mcp-server, buyer-intent-data-reference). Current docs front the v2 API; v1 paths are legacy/partner. -->

# G2 API Reference

## Overview

The G2 API provides programmatic access to G2's product, category, and review data. Built on the JSON:API specification (`application/vnd.api+json`).

## Authentication

### Developer Portal Setup
1. Navigate to the G2 Developer Portal
2. Create an account and verify email
3. Enter Organization Name and choose a unique Organization Slug
4. Portal URL: `https://my.g2.com/developers/{your-slug}`

### Access Tokens
- Generated in the Developer Portal → Access Tokens tab
- Scoped to individual users or organizations
- Configure endpoint permissions via Access dropdown
- **Tokens expire after one year** — must be regenerated

### OAuth Apps
- Register apps in Developer Portal → OAuth Apps tab
- Provide: name, privacy policy URL, terms of service URL, redirect URL
- Select the **Confidential** checkbox if the app can securely store the client secret (server-side); leave unchecked for public clients (mobile/browser)
- Receive: Client ID and Client Secret. The OpenID Connect Details panel provides the Auth URL and Access Token URL
- Redirect URLs must match exactly
- OAuth2 scopes (current docs example): `openid profile products.read products.reviews.read` — scopes must match the permissions enabled on the token; an invalid/unknown/malformed scope returns "requested scope is invalid, unknown, or malformed"
- (Note: earlier docs referenced scopes like `buyer_intent.read` / `screenshots.read`; the developer portal now documents the `products.*` / `openid profile` scope family. Confirm the exact scope string for an endpoint in the live API reference.)

### Free-tier access
- The partner developer page advertises getting started with **1,000 API calls per month** on the free tier, plus a sandbox environment for testing. (Source: partner.g2.com/developer)

### Postman Testing
- Register OAuth app with callback URL: `https://oauth.pstmn.io/v1/browser-callback`
- Configure OAuth 2.0 with app credentials and scopes

## Base URLs

- **v1 API**: `https://data.g2.com/api/v1/`
- **v2 API**: `https://data.g2.com/api/v2/`
- **Syndication API**: `https://data.g2.com/api/2018-01-01/syndication/`

## Rate Limiting

- **Global limit**: 100 requests per second
- Exceeding triggers a **60-second access block**

## Pagination

- Parameters: `page[size]` and `page[number]`
- Default size: 10 items
- Maximum size: 100 (varies by endpoint)
- Response includes:
  - `links`: `self`, `prev`, `first`, `next`, `last`
  - `meta`: `record_count`, `page_count`

## Date Format

RFC3339: `2019-10-02T15:00:00Z`

## Common Filters

- `updated_at_gt` — records updated after timestamp
- `updated_at_lt` — records updated before timestamp
- Resource-specific filters per endpoint

## Response Structure

```json
{
  "data": [],
  "links": {
    "self": "...",
    "prev": "...",
    "first": "...",
    "next": "...",
    "last": "..."
  },
  "meta": {
    "record_count": 100,
    "page_count": 10
  }
}
```

Headers include `X-Request-ID` for tracking.

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 429 | Rate limit exceeded (60-second block) |
| 500 | Server error |

## v1 Endpoints

### Products
- `GET /api/v1/products` — List products
- Filters: resource-specific

### Reviews (Survey Responses)
- `GET /api/v1/survey-responses` — List reviews
- Includes: ratings, text, verified status, timestamps

### Categories
- `GET /api/v1/categories` — List G2 categories

### Questions
- `GET /api/v1/questions` — List discussion questions

### Answers
- `GET /api/v1/answers` — List question answers

### Buyer Intent
- `GET /api/v1/ahoy/` — Intent activity data
- `GET /api/v1/intent-history` — Historical intent data

### RESThooks (Webhooks)
- `GET /api/v1/resource-subscriptions` — Manage webhook subscriptions
- Subscribe to events: new reviews, intent signals, etc.

### Syndication
- `GET /api/2018-01-01/syndication/` — Review syndication data

## v2 Endpoints

**Current docs front the v2 API** (`https://data.g2.com/api/v2/`). The developer-portal "test endpoint" example is `GET /api/v2/products`. The interactive reference (`data.g2.com/api/v2/docs/index.html`) is JS-rendered; authenticate with a token there to enumerate the live endpoint list.

The v2 API uses an OLAP-style query language with:
- **Dimensions**: fields to group by
- **Measures**: aggregation functions
- **Filters**: operators include `_eq`, `_cont`, `_gt`, `_lt`, etc.
- **Cursor-based pagination**

### Buyer Intent (v2)
- Sandbox and production environments
- Product-specific and global intent endpoints
- Buyer Intent record fields (per the data dictionary, ~20+ fields): `product_id`, `product_name`, `category_id`, `company_id`, `company_name`, `visit_url`, `visit_title`, `visit_type`, `visit_date`, `company_domain`, `visitor_region`, `visitor_country`, `company_state`, `company_country`, `company_employees`, `org_employees_range`, `company_sector`, `company_industry_group`, `company_industry`, `company_sub_industry`, `total_page_views`, `last_seen`, `activity_level`, `buying_stage`
- No contact/email/phone fields — company-level only (confirmed in the buyer-intent data reference)

### Screenshots
- Manage product screenshots
- OAuth2 scope: `screenshots.read`

### Product Features & Categories
- Query product features and category assignments

### Market Signals
- Market trend and signal data

### Credit Account
- Manage review incentive credit balances

## SDKs

- The partner developer page lists support "for Python, JavaScript, and more" — confirm current SDK availability in the developer portal.
- An older Ruby wrapper exists at [g2crowd/g2crowd-ruby](https://github.com/g2crowd/g2crowd-ruby), but it has **no published releases** and unclear recent maintenance — verify compatibility with the v2 API before relying on it.

## G2 MCP Server

G2 ships an official **MCP (Model Context Protocol) Server** for connecting G2 data to AI assistants (Claude, Cursor, etc.).
- **Auth**: OAuth — connecting G2 MCP opens a browser window to sign in to your G2 account and authorize access. Requires a valid G2 account with appropriate permissions and products registered on G2.
- **Datasets exposed**: Buyer Intent Signals, Product Reviews, Product Catalog, Category Taxonomy (plus competitive signals, buying-stage, activity-level, and customer-sentiment data).
- **Rate limit**: shares the G2 API global limit — 100 requests/second, then a 60-second block.
- **Setup in Claude**: `+` below the chat box → Connectors → Manage Connectors → search/select **G2 MCP** → complete OAuth → start a new chat with G2 MCP enabled.
- **Partner AI integrations**: HubSpot (Breeze Agents), Gong (AI workflows), AirOps (Playbooks) — all require an active G2 subscription.
- Source: https://documentation.g2.com/docs/g2-mcp-server

## Lead-delivery webhooks (distinct from API RESThooks)

Separate from the API's RESThook resource subscriptions, G2 offers **lead-form delivery webhooks** that push leads captured on your G2 product profile page into your CRM:
- **HubSpot**: posts as Form Data to `https://forms.hubspot.com/uploads/form/v2/:portal_id/:form_guid` (portal_id + form_guid from your HubSpot embed code). Source: https://documentation.g2.com/docs/hubspot-webhook
- **Salesforce**: posts as Form Data to Web-to-Lead (`https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8`) using your 15-digit `oid` as a hidden field. Source: https://documentation.g2.com/docs/salesforce-crm-webhook
- These carry lead-form fields (standard + custom), not API review/intent payloads, and the docs do not document HMAC signing for them.

## Integration Notes

- Account permissions determine which endpoints are accessible
- Contact your G2 Account Executive for additional endpoint access
- The API is designed for custom workflows and advanced use cases
- For standard CRM/marketing connections, use native integrations (Salesforce, HubSpot, Zapier) instead
