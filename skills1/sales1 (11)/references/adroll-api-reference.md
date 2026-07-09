# AdRoll / NextRoll API Reference

## Overview

AdRoll's APIs are provided by NextRoll, the parent company. The API suite covers campaign management, reporting, audience management, geotargeting, and conversion tracking. Current official docs: https://apidocs.nextroll.com/ (also mirrored at developers.nextroll.com).

**Base URL (CRUD / core REST API)**: `https://services.adroll.com/api/v1/`

The GraphQL Reporting API and the Server-to-Server API use **different hosts** — see those sections below.

**Authentication**: OAuth 2.0 or Personal Access Tokens (PAT)
- **OAuth 2.0**: Standard authorization code flow. Register an app in the NextRoll developer portal. Scopes ("Supported Scopes") control access to specific resources.
- **Personal Access Token (PAT)**: A simple way to make API calls in scripts where OAuth isn't practical. Generate in the AdRoll dashboard. The token is sent in the `Authorization` header with the **`Token`** scheme (NOT `Bearer`), and you ALSO pass your application's client ID in the **`apikey` query parameter** on every request. The `apikey` is always in the URL query string regardless of HTTP method.

Example (PAT):
```
curl --header 'Authorization: Token YOUR_TOKEN' \
  'https://services.adroll.com/api/v1/organization/get_advertisables?apikey=MYAPIKEY'
```

> **Gotcha**: The auth header scheme is `Token`, not `Bearer`. The `apikey` query param is required separately from the token and identifies the application, not the user. Omitting either returns an auth error.

## API Suite

NextRoll documents the following services: CRUD API, GraphQL Reporting API, Audience API, User Lists API, Prospecting API, Automated Campaigns API, Universal Campaigns API, Geotargeting API, Site Traffic Revealer, and the Server-to-Server (S2S) API.

### 1. CRUD API
Core resource management for campaigns, ad groups, ads, and advertisables. Endpoints are **action/RPC-style** (verb in the path), not REST-style `/{resource}/{id}` collections.

**Base**: `https://services.adroll.com/api/v1/`

**Advertisable endpoints**:
- `/advertisable/get` — Get advertiser details
- `/advertisable/get_campaigns` — List campaigns
- `/advertisable/get_adgroups` — List ad groups
- `/advertisable/get_ads` — List ads
- `/advertisable/create`, `/advertisable/edit`
- `/organization/get_advertisables` — List advertisables under an organization

**Campaign endpoints**:
- `/campaign/create`, `/campaign/edit`, `/campaign/get`
- `/campaign/get_adgroups`
- `/campaign/pause`, `/campaign/unpause`
- `/campaign/pause_ads`, `/campaign/unpause_ads`

**Ad group endpoints**:
- `/adgroup/create`, `/adgroup/edit`, `/adgroup/get`
- `/adgroup/get_ads`
- `/adgroup/add_segments`, `/adgroup/remove_segments`
- `/adgroup/select_ads`, `/adgroup/deselect_ads`
- `/adgroup/pause`, `/adgroup/unpause`

**Ad endpoints**:
- `/ad/create`, `/ad/clone`, `/ad/edit`, `/ad/get`

### 2. GraphQL Reporting API
Cross-channel analytics and performance data. **Single GraphQL endpoint** on a different host from the CRUD API.

**Endpoint**: `POST https://app.adroll.com/reporting/api/v1/query` (append `?apikey=YOUR_CLIENT_ID` when needed)

**GraphiQL explorer** (schema browser + query testing): `https://app.adroll.com/reporting/graphiql`

> The legacy (non-GraphQL) Reporting API exists but NextRoll publishes a "Migrate from the Reporting API" guide steering integrations to the GraphQL endpoint.

**Capabilities**:
- Campaign, ad group, and ad-level performance metrics
- Cross-channel attribution (display, social, email, CTV)
- Date range queries with daily/weekly/monthly granularity
- Metrics: impressions, clicks, conversions, revenue, ROAS, CPA, CTR, viewability

**Example query**:
```graphql
{
  campaign(eid: "CAMPAIGN_EID") {
    name
    metrics(dateRange: {start: "2024-01-01", end: "2024-01-31"}) {
      impressions
      clicks
      conversions
      revenue
      cost
    }
  }
}
```

### 3. Audience API
Create and update CRM segments and other segment types.

**Segment types**: crm, composite, custom, impression, user_events, user_attributes, crosschannel_lal (cross-channel lookalike).

### 4. User Lists API
Retrieve the size of your audiences / manage CRM contact lists for targeting.

**Match rate**: Typically 40-60% for email lists. Higher for hashed email matching.

### 5. Prospecting API
Find new audiences similar to your existing customers ("Prospecting attracts new audiences").

### 6. Automated Campaigns API
Manage automated/triggered campaign rules.

### 7. Universal Campaigns API
Cross-channel campaign management — create campaigns that span display, social, native, CTV.

### 8. Geotargeting API
Search for geotargeting EIDs that are used when setting geotargets on your campaigns.

### 9. Site Traffic Revealer
A JavaScript API that provides firmographic data about a site visitor (company-level identification). Used in B2B/RollWorks flows.

### 10. Pixel JavaScript API
Client-side pixel API for firing page-view and conversion events from the browser. Documented under Guides → "Pixel JavaScript API".

### 11. Server-to-Server (S2S) API
Send user events and conversions directly from your servers to complement pixel and MMP events. **Under active development** — generally stable but may change.

**Endpoint**: `POST https://srv.adroll.com/api?advertisable=<ADVERTISABLE_EID>`
- **Required query param**: `advertisable` — the EID of the advertisable you are sending the event to.
- **Optional query param**: `dry_run=true` — validates and logs the payload without affecting audiences or attribution.
- A single request can send more than one event (docs advise no more than ~100 events per request).

**Authentication**: Uses a **Server Access Token (SAT)** sent via the `Authorization` header with the `Token` scheme. SATs are obtained by contacting your account manager (shared securely, e.g. via 1Password) — they are distinct from PATs.

**Use cases**: Backend purchase events, phone orders, offline conversions, privacy-compliant tracking without client-side cookies.

## Rate limits

**Default quota: 100 API requests per service per day.** Quota is applied per service (CRUD, Reporting, etc.). You can request a quota increase by contacting NextRoll support.

> This is a low default — design integrations to batch where possible and cache reporting pulls. Do not assume per-minute limits; the documented limit is a daily per-service quota.

## Webhooks

No documented webhook/callback system. Use polling via the GraphQL Reporting API for near-real-time data, or the S2S API for event-based server-side integration.

## SDKs and tools

- **No official SDKs** — APIs are HTTP-based; use any HTTP client (REST/RPC for CRUD, GraphQL for reporting).
- **Shopify App**: Handles pixel, product feed, and conversion tracking automatically
- **BigCommerce App**: Native integration
- **WooCommerce Plugin**: WordPress plugin for integration

## Notes

- All entity IDs (eids) are string-based unique identifiers
- Three distinct hosts are in play: `services.adroll.com` (CRUD/core), `app.adroll.com` (GraphQL reporting), and `srv.adroll.com` (S2S events)
- API documentation lives at https://apidocs.nextroll.com/ (mirror: developers.nextroll.com)
- RollWorks (B2B/ABM) is covered by the same NextRoll API surface — see the "AdRoll ABM API Documentation" guide
- API access may be plan-gated — verify with AdRoll support
