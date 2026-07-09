# Sprout Social API Reference

## Overview

The Sprout Social API provides programmatic access to analytics, publishing, messaging, listening, media, and case data. **Requires the Advanced plan** (with API Permissions granted by an Account Owner). Not available on Essentials, Standard, or Professional.

## Authentication

The API supports **both OAuth 2.0 and API tokens** (verified against official docs 2026-06-13). Both use the same header format.

- **Header**: `Authorization: Bearer <OAuth access token OR API token>`
- **OAuth 2.0 (recommended)** — Sprout issues short-lived JWT access tokens. Two flows:
  - **Machine-to-Machine** (custom integrations): exchange Client ID + Client Secret for a token via `POST https://identity.sproutsocial.com/oauth2/{app_id}/v1/token` (client_credentials grant).
  - **User-Based**: for apps that require a user to log in to Sprout.
- **API tokens (alternative)** — Users with the API Permissions entitlement generate an account-scoped token in Settings → Global Features → API, then paste it into requests. Either token type works interchangeably in the `Authorization: Bearer` header.
- **Permissions**: API access requires the **Advanced plan**, and the user generating/using the token must have API Permissions granted by an Account Owner.

## Base URL

```
https://api.sproutsocial.com
```

OAuth token endpoint: `https://identity.sproutsocial.com/oauth2/{app_id}/v1/token`

## Key endpoints

All endpoints are under `/v1`. `<customer ID>` is obtained from the `/v1/metadata/client` call. (Endpoint list verified against official docs 2026-06-13.)

### Metadata

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/metadata/client` | Client-level metadata — retrieve your customer IDs and names |
| GET | `/v1/{customerId}/metadata/customer` | Customer profile metadata — connected profiles (includes `network_metadata` with `address`/`store_code` as of Jan 2026) |
| GET | `/v1/{customerId}/metadata/customer/tags` | Message tags |
| GET | `/v1/{customerId}/metadata/customer/groups` | Profile groups |
| GET | `/v1/{customerId}/metadata/customer/users` | Active users (team members and roles; `email` field included) |
| GET | `/v1/{customerId}/metadata/customer/topics` | Listening topics |
| GET | `/v1/{customerId}/metadata/customer/teams` | Teams |
| GET | `/v1/{customerId}/metadata/customer/queues` | Case queues |

### Analytics

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/{customerId}/analytics/posts` | Post-level analytics — engagement, impressions, clicks, video views |
| POST | `/v1/{customerId}/analytics/profiles` | Profile-level analytics — audience growth, engagement trends |

### Messages

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/{customerId}/messages` | Query message data with filters (`group_id`, `customer_profile_id`, `message_id`, `created_time`, `action_last_update_time`, `post_type`, `tag_id`, `language_code`, `from.guid`), `fields`, `limit` (default 50, max 100), `timezone`, `sort`, `page_cursor`. Note: querying messages is a **POST with a request body**, not a GET. |

### Listening (requires Listening add-on)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/{customerId}/listening/topics/{topicId}/messages` | Topic messages |
| POST | `/v1/{customerId}/listening/topics/{topicId}/metrics` | Topic aggregated metrics |

### Publishing

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/{customerId}/publishing/posts` | Create draft publishing posts |
| GET | `/v1/{customerId}/publishing/posts/{publishing_post_id}` | Retrieve a publishing post |

### Media upload

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/{customerId}/media/` | Upload media < 50MB |
| POST | `/v1/{customerId}/media/submission` | Start multipart upload (large media) |
| POST | `/v1/{customerId}/media/submission/{submissionId}/part/{partNumber}` | Continue multipart upload |
| GET | `/v1/{customerId}/media/submission/{submissionId}` | Complete multipart upload |

### Cases

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/{customerId}/cases/filter` | Retrieve cases with filtering (cursor-paginated) |

## Data models

### Post metrics
- `impressions` — total times content was displayed
- `engagements` — total interactions (likes, comments, shares, clicks)
- `video_views` — video view count
- `video_view_time` — total video watch time (Instagram)
- `lifetime.video_view_time` / `lifetime.video_view_time_per_view` — Instagram lifetime video-view metrics (added Apr 8, 2026)
- `is_boosted` — whether the post was boosted/promoted
- `clickthrough_link` — destination URL

### Message fields
- `case_id` — linked support case ID
- `sent` — timestamp
- `inbox_permalink` — direct link to message in Smart Inbox
- `publishing_post_id` — the Sprout Publishing Calendar post ID for sent messages published via the Sprout publishing workflow (added Apr 15, 2026)

### Network metadata
Returned in the `network_metadata` object on customer profile metadata (added Jan 13, 2026):
- `address` — location data for profiles with physical locations
- `store_code` — store identifier for multi-location businesses

## Pagination

(Verified against official docs 2026-06-13.)

- **Analytics endpoints** — index-based via `page` and `limit` (default page size 1000 for profiles, 50 for posts; 1-indexed `page`).
- **Messages endpoint** — cursor-based via `page_cursor` (forward navigation only); `limit` default 50, max 100.
- **Cases endpoint** — cursor-based via `page_cursor`.
- **Listening Messages** — index-based via `page` and `limit`.
- **Listening Metrics** — no pagination; returns all data in a single response.

## Rate limits

(Verified against official docs 2026-06-13.)

- **60 requests per minute**
- **250,000 requests per month**

## Webhooks

Not available. No webhook functionality is documented. Use polling to check for new messages or analytics updates.

## SDK / client libraries

No official SDKs. Use HTTP client libraries in your language of choice. Postman collection available on the Postman API Network (Sprout Social workspace).

## Changelog

Sprout maintains an API changelog at `https://api.sproutsocial.com/docs/changelog/` documenting endpoint additions, field changes, and deprecations.

## Limitations

- **No implementation support** — Sprout's support team can troubleshoot API behavior but won't help build integrations.
- **Plan-gated** — requires Advanced ($399/seat/mo) or Enterprise plan.
- **Read-heavy** — the API is strongest for reading analytics and messages. Publishing capabilities are more limited than the UI.
- **No real-time** — no WebSocket or streaming endpoints. Polling only.
