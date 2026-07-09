# CreatorIQ API Reference (ExchangeIQ)

Enterprise API for integrating CreatorIQ data with CRM, BI tools, data lakes, and custom workflows. CreatorIQ describes ExchangeIQ as a **bi-directional, JSON-based API** that "simplifies the way businesses connect, exchange, and integrate data across platforms" — you can both read CreatorIQ data and post external data (e.g., attribution, sales, commission, paid-media) back against creators, posts, and campaigns.

## Authentication

- **Method**: API key in request header (referred to in the docs as the "CreatorIQ Premium API")
- **Header**: `x-api-key: YOUR_API_KEY`
- **Provisioning**: Provided by your CreatorIQ contact — reach out to your CreatorIQ rep or email support@creatoriq.com. No self-serve key generation.
- **Encryption**: JSON-based API, communications encrypted via SSL/TLS

## Base URLs

| API | Base URL |
|---|---|
| **Main API docs** | apidocs.creatoriq.com (public-apidoc.creatoriq.com 301-redirects here) |
| **Link-Tracking / Attribution** | linktracking-apidoc.creatoriq.com |

These are documentation hosts (Stoplight). The runtime API base host is provided to you with your API key; the docs require authentication for the full reference.

## Format

- **Request/Response**: JSON
- **Documentation platform**: Stoplight (JS-rendered — may require browser access)

## Data model

Per the official docs, a CreatorIQ customer has a dedicated CRM containing data for **Publishers/Influencers, Campaigns, Social Accounts, Lists, One-Sheet**, etc. The API resources map onto these core objects.

## Key API Categories

*Note: Full endpoint paths and request/response schemas are behind the authenticated, JS-rendered docs at apidocs.creatoriq.com. The resource families and operations below are confirmed from the official docs index; exact paths and params are not re-typed here.*

### CRM Publishers API

Manage creator (publisher/influencer) records in the CRM. The docs state you can **add a NEW creator record and retrieve, update, and delete an EXISTING creator record** — i.e., create/read/update/delete operations on publisher records:
- Creator profile data (demographics, social handles, audience metrics)
- Relationship and pipeline stage data

### CRM Lists API

Separate resource for managing CRM Lists (curated creator lists/segments) programmatically.

### Post Campaign Activity

Endpoint for posting activity/data against campaigns (part of the bi-directional "post additional data tied to creators, posts, or campaigns" capability).

### Campaign Data

- Campaign creation and configuration
- Campaign performance metrics (impressions, reach, engagement, conversions)
- Content tracking and post detection data
- Creator assignments and deliverable status

### Social Platform Data

Platform-specific endpoints for connected social accounts:
- Instagram metrics and content
- TikTok metrics and content
- YouTube metrics and content
- Facebook, Snapchat data

### Link-Tracking / Attribution

Separate API for ecommerce attribution:
- Affiliate link generation and tracking
- Coupon code performance
- Conversion attribution data
- Revenue and ROAS reporting

### Reporting

- Custom report generation
- Performance dashboards data export
- BenchmarkIQ competitive data (may be plan-gated)

## Rate Limits

Not publicly documented. Contact your CreatorIQ representative for rate limit details based on your plan tier.

## Webhooks

**Webhooks are supported.** The official docs state: *"CreatorIQ uses webhooks to notify your application when an event happens to campaign or creator's data."* The docs index also exposes a **Webhooks management API** (subscribe/manage webhook endpoints) alongside the data APIs.

- **Trigger model**: event-driven notifications fired when campaign or creator data changes (the exact list of event types and payload schema is in the authenticated docs and is not re-typed here).
- **Management**: webhook subscriptions are created/managed via the Webhooks management API.
- **Not yet verified from official quotes**: signing/signature-verification scheme, retry policy, and the full event-type catalog. Confirm these in the authenticated reference before relying on them.

## Gaps

- Full endpoint paths, request/response schemas, and pagination details are behind authenticated, JS-rendered docs at apidocs.creatoriq.com.
- Rate limits are not publicly documented — contact your CreatorIQ rep for limits based on your plan tier.
- Webhook payload schema, signing, and retry behavior are not publicly quotable (existence and the campaign/creator-data event model are confirmed).
- Whether ExchangeIQ also exposes a GraphQL surface is hinted by some third-party catalogs but not confirmed in the official Overview, which describes a JSON resource API — treat GraphQL as unverified.
- API access may be plan-gated — confirm with your CreatorIQ rep which endpoints your plan includes.
