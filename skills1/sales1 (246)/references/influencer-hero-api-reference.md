# Influencer Hero API Reference

## Overview

Influencer Hero provides a REST API for managing influencer collaborations, tracking affiliate performance, and automating key tasks. All requests and responses are JSON. Separate API products are available for influencer data access (see Data APIs below).

**Documentation**: https://docs.influencer-hero.com/ (public; downloadable OpenAPI spec available as `ih_api.json` / `ih_api.yaml`)
**Base URL**: `https://api.influencer-hero.com` — all platform endpoints use the `/v1/` path prefix.

## Authentication

All authenticated API requests require an API key passed via the `X-API-KEY` header:

```
X-API-KEY: your-api-key
```

Find your API key and webhook signing secret under `https://app.influencer-hero.com/api_integration` (only visible if you have API access — API access is plan-gated; see Rate limits).

## Rate limits

Universal across all endpoints; no burst policy currently implemented.

| Plan | Rate limit |
|---|---|
| **Pro** | 4 requests/second (240 requests/minute) |
| **Business** | 8 requests/second (480 requests/minute) |

Higher limits are available as an add-on (e.g. "+10 additional requests per second" for $1,000/month per the API pricing page).

## Platform API

### Test endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/v1/public/hello` | Public — verify the API is reachable without authentication |
| GET | `/v1/account/hello` | Authenticated — verify your API key / credentials |

### CRM endpoints

| Method | Path | What it does |
|---|---|---|
| POST | `/v1/search/identify_influencers` | Identify influencers from a list of contact emails; matched influencers appear in the "Your customers" tab of the influencer finder. Each request returns up to 10 influencers; costs 1 search credit per new influencer seen. Body includes `influencer_list` (array of emails), `brand_id`, `source_type`. |
| GET | `/v1/crm/get_deal_details` | Retrieve information about a specific deal |
| POST | `/v1/crm/create_deal` | Create a deal |

### Affiliate Tracking endpoints (server-side)

Advanced server-side endpoints for tracking affiliate actions and performance. For most use cases the client-side tracking script is sufficient; these are for server-side attribution (e.g. increasing tracked clicks on an influencer's deal page).

| Method | Path | What it does |
|---|---|---|
| POST | `/v1/crm/new_influencer_click` | Record an affiliate click server-side |
| POST | `/v1/crm/new_influencer_referral` | Record an affiliate referral/conversion server-side |

### Account endpoints

| Method | Path / operation | What it does |
|---|---|---|
| GET | `/v1/account/search_dealflows` (Dealflow Search) | Retrieve all dealflows in the user's account |
| GET | `/v1/account/search_brands` (Brand ID Search) | Retrieve / search for brands in the user's account |
| POST | Create Webhook | Register a webhook (target URL + type) |
| DELETE | Delete Webhook | Remove a registered webhook |

### Webhook events

A webhook has a target URL and a `type`. The `type` is one of the following (exact slugs):

| Event type | Trigger |
|---|---|
| `new_payout_request` | Influencer requests commission payout |
| `new_max_bid` | New (max) bid received on a deal |
| `update_discount_code` | Discount code created, modified, or deactivated |
| `update_custom_link` | Custom tracking link modified |
| `product_sent` | Product sent/shipped to influencer |
| `new_email_sent` | Outreach email sent to influencer |
| `new_influencer_reply` | Influencer replies to outreach |
| `new_influencer_post` | Influencer publishes content tied to your brand |

### Webhook signing / verification

Webhooks are secured with HMAC-SHA256 signatures so only legitimate requests from Influencer Hero reach your server. To verify:

1. Read the timestamp from the `X-InfluencerHero-Timestamp` header.
2. Read the signature from the `X-InfluencerHero-Signature` header.
3. Read the raw request body as bytes.
4. Compute the HMAC-SHA256 of the raw body using your webhook signing secret (from `app.influencer-hero.com/api_integration`).
5. Compare your computed signature against `X-InfluencerHero-Signature` using a timing-safe comparison.
6. Optional: reject requests whose `X-InfluencerHero-Timestamp` is outside an acceptable window (e.g. 5 minutes) to prevent replay attacks.

The docs include Python and PHP verification code examples. See https://docs.influencer-hero.com/verifying_webhooks

## Data APIs (separate products)

Influencer Hero also offers standalone data APIs for building custom integrations:

### Discovery API

Search influencers using advanced filters like audience demographics, location, engagement, and niche. Access to 450M+ creator profiles across Instagram, TikTok, and YouTube, with 20+ granular filters, fake-follower / fraud detection, and lookalike search. (A separate ~200M+ opt-in pool exists with compliant contact information.)

### Raw API

Access core influencer data and metrics directly — follower counts, engagement rates, audience demographics, content history. Build custom workflows and tools.

### Brand Collaborations API

Retrieve structured data on influencer–brand partnerships and sponsored content activity. Detect which brands influencers have worked with.

### AI Search API

Use natural language queries to discover influencers and posts across social platforms. Returns semantically relevant results.

## Technical details

- **Architecture**: RESTful API; JSON request/response
- **Data freshness**: Daily updates
- **Infrastructure**: Engineered for scale — high volume, low latency
- **Plan gating**: API access is plan-gated. Custom API integrations are listed on the Business plan; the Pro plan may have API access at lower request limits. Data-API access is sold separately (see API pricing).

## Data API pricing (separate product, public)

Per `influencer-hero.com/api-pricing` (verified 2026-06-13):

- Standard $279/mo · Pro $519/mo · Business $960/mo · Agency/Enterprise custom (quarterly = 20% off)
- Usage examples: 100 influencer profiles retrieved = $1.50; 10,000 email addresses checked = $5
- Analytics report credits: bulk from $1.00/report (1,000 units) down to $0.09/report (500,000 units)
- API access included with Business; Pro may have access at lower request limits

## Gaps

- Full request/response field schemas for each endpoint are summarized here from the public docs; consult the OpenAPI spec (`ih_api.json` / `ih_api.yaml`) on docs.influencer-hero.com for complete field-level detail
- Pagination method not explicitly documented for list endpoints
- No published per-endpoint error-code reference
