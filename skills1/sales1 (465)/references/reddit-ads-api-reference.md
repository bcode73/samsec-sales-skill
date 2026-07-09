# Reddit Ads API v3 Reference

## Overview

The Reddit Ads API allows programmatic management of campaigns, ad groups, ads, and reporting. It is **not self-serve** — access requires whitelisting by a Reddit sales representative.

> Note (access model): live third-party docs disagree on this — some say v3 removed whitelisting and the API is now open to all developers who register an app, while others say campaign-management writes still require allow-list approval from Reddit's ads/partner team. The official help article could not be fetched directly to settle it, so the "not self-serve" claim above is left as-is and flagged as unverified. The Conversions API (CAPI) is separately granted to most advertisers regardless of full Ads API allow-listing.

- **Base URL**: `https://ads-api.reddit.com/api/v3` (verified against live docs 2026-06-13)
- **Documentation**: `https://ads-api.reddit.com/docs/v3/`
- **Official help article**: `https://business.reddithelp.com/s/article/Reddit-Ads-API`

## Authentication

- **Method**: OAuth 2.0
- **Flow**: `authorization_code` and `client_credentials` grants are both supported (Client ID + Client Secret → access token)
- **Token endpoint**: `https://www.reddit.com/api/v1/access_token` (standard Reddit OAuth endpoint)
- **Bearer header**: send `Authorization: Bearer <access_token>` on every Ads API request
- **Scopes**: `adsread` (read account/campaign data), `adsedit` (campaign management writes), `adsconversions` (Conversions API). Add `duration=permanent` at authorization to receive a refresh token.

## Access requirements

1. Create a Reddit account and developer application at reddit.com/prefs/apps
2. Register for Ads API access through your Reddit sales representative
3. Reddit reviews and whitelists your application
4. Use Client ID and Client Secret to obtain access tokens

## Key functional areas

The API covers these domains (specific endpoint paths require whitelisted access to view full docs):

### Accounts
- List ad accounts
- Get account details
- Account-level settings and permissions

### Campaigns
- Create, read, update, delete campaigns
- Set objectives, budgets, schedules
- Campaign status management (active, paused, archived)

### Ad Groups
- Create, read, update, delete ad groups
- Targeting configuration (communities, interests, keywords, custom audiences)
- Bid strategy and placement settings
- Frequency caps

### Ads
- Create, read, update, delete ads
- Creative upload and management
- CTA configuration (13 available CTAs: Shop Now, Sign Up, Download, Install, Learn More, etc.)
- Ad review status

### Product Catalogs
- Manage product feeds for dynamic Product Ads
- Product data upload and sync

### Audiences
- Create and manage custom audiences
- Website visitor audiences (via Pixel)
- Customer list upload (hashed emails)
- Engagement audiences
- Lookalike audience creation

### Reporting
- Campaign, ad group, and ad-level performance reports
- Flexible metrics and breakdowns
- Date range selection

## Data format

- All timestamps in **UTC**
- JSON request and response bodies
- Standard REST conventions

## Rate limits

Exact thresholds are not publicly documented and are enforced per-account. On limit, the API returns **HTTP 429** with `X-RateLimit-Remaining` and `X-RateLimit-Reset` response headers — but **no `Retry-After` header** — so implement exponential backoff (with jitter) off those headers. Contact your Reddit sales representative for specifics. (verified against live docs 2026-06-13)

## Webhook support

Not documented in the Ads API. Use Zapier integration for event-driven workflows (Lead Gen Ads → CRM).

## Conversions API (CAPI)

Server-side event tracking on the same `ads-api.reddit.com` host:

- **Endpoint**: `POST https://ads-api.reddit.com/api/v2.0/conversions/events/{PIXEL_ID}` (the Conversions API path is on the `v2.0` base; the pixel/conversion-events ID goes in the path). Configure / find the token under Events Manager → Conversions API in Reddit Ads Manager. (verified 2026-06-13)
- **Auth**: a non-expiring **conversion access token** sent as `Authorization: Bearer <token>` (generated in Events Manager)
- **Events** (Reddit's standard event names): `Page Visit`, `View Content`, `Search`, `Add to Cart`, `Add to Wishlist`, `Purchase`, `Lead`, `Sign Up`, `Custom` (verified 2026-06-13 — note Reddit uses `Page Visit`, not `PageView`)
- **Match keys**: email (hashed), IP address, user agent, Reddit click ID
- **Deduplication**: pass a **Conversion ID** (unique per event) and the conversion event name; Reddit dedupes Pixel vs CAPI by matching conversion ID + event name

## Third-party tools

- **Postman collection**: [Reddit Ads API v3 on Postman](https://www.postman.com/reddit-ads-api/reddit-ads-api-v3/overview) — pre-built requests for testing
- **MCP servers**: Community-built MCP servers exist for read-only access (listing campaigns, ad groups, ads, performance reports)
- **Salesforce Marketing Cloud**: Native Reddit Ads API connector for data streams
- **Adobe Experience Platform**: Reddit Conversions API extension for server-side event forwarding

## Gaps

- Full endpoint paths and request/response schemas require whitelisted access
- Rate limit specifics not publicly available
- Webhook support not documented
- SDK/client libraries not officially provided by Reddit (community wrappers available via Windsor.ai for Python and R)
