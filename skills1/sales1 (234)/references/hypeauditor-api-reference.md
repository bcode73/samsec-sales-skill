# HypeAuditor API Reference

## Overview

HypeAuditor provides a REST API for programmatic access to influencer discovery, analytics reports, campaign management, lists, market analysis, media planning, and recruitment.

**Base URL**: `https://hypeauditor.com/api/method/%endpoint%` — most endpoints sit under `/api/method/`. Exception: the Instagram Competitor Analysis (Market Analysis) endpoint lives under `/api/marketanalysis/` instead.
**Docs**: https://hypeauditor.readme.io/ (machine index at https://hypeauditor.readme.io/llms.txt)
**Auth**: Header-based — `X-Auth-Id` (client ID) + `X-Auth-Token` (API token)
**Rate limit**: less than 100 requests per minute (HTTP 429 if exceeded)
**Response format**: JSON (`Content-Type: application/json`)
**Versioning**: Optional `v` parameter (string). Pass `v=2`; v1 was deprecated August 1, 2024. Current version string returned when omitting it: `2019-10-18`.

## Authentication

Every request must include:

```
X-Auth-Id: {your_client_id}
X-Auth-Token: {your_api_token}
```

Contact HypeAuditor support to obtain credentials.

## Response structure

**Success**:
```json
{
  "result": {
    "...data...",
    "restTokens": 500,
    "validUntil": 1735689600
  }
}
```

**Error**:
```json
{
  "error": {
    "description": "Error message"
  }
}
```

## HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 202 | Report processing — includes `retryTtl` (seconds to wait before retrying) |
| 400 | Bad request — invalid parameters |
| 402 | Insufficient credits |
| 403 | Invalid token or private account |
| 404 | User/resource not found |
| 429 | Rate limit exceeded (100 req/min) |
| 500 | Server unavailable |

## Endpoints by category

### Suggester API

Find influencers by name or account handle.

**`GET /auditor.suggester`**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search` | string | Yes | Search keyword (name or handle) |
| `st` | string | No | Social network: `instagram`, `youtube`, `tiktok`, `twitter`, `twitch`, `snapchat` |
| `exclSt` | string | No | Comma-separated networks to exclude |

### Discovery API

Search for influencers with filters.

**`POST /auditor.search/`**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `social_network` | string | Yes | `instagram`, `youtube`, `tiktok`, `twitter`, `twitch` |
| `search` | array | No | Keywords to search anywhere |
| `search_content` | array | No | Keywords in content |
| `search_description` | array | No | Keywords in bio/description |
| `niche_search` | string | No | Niche phrase for semantic matching |

**Audience filters** (all optional):
- `audience_geo` — audience location
- `audience_age` — audience age range
- `audience_gender` — audience gender split
- `audience_lang` — audience language

**Performance / account filters** (all optional — verified names per live docs 2026-06-13):
- `subscribers_count` — follower/subscriber range (the live docs use `subscribers_count`, not `followers_from`/`followers_to`)
- `er` — engagement rate filter (live docs use `er`, not `engagement_rate_from`/`engagement_rate_to`)
- `account_geo` — creator's own location
- `growth` — follower growth rate
- `last_media_time` — recency of last post
- `verified` — verification status
- Platform-specific filters such as `twitch_games`, `twitter_likes`

**Sorting**: `sort` — by subscribers, engagement, or username.

**Pagination**: 20 results per page, max `page` value 500 (10,000 rows total). Use `page` parameter (default 1).
**Credits**: each page costs 1 Discovery Call.
**Response includes**: `queries_left` field for remaining calls.

**Sandbox**: `POST /auditor.searchSandbox/` — same parameters, for testing.

### Reports API

Get detailed analytics for a specific creator. Endpoint paths per network (verified 2026-06-13 against the live ReadMe docs — note these are NOT the `*Report` names earlier versions of this file used):

| Network | By username/handle | By user/channel ID |
|---------|--------------------|--------------------|
| Instagram | `GET /auditor.report/?username={username}` | `GET /auditor.reportByUserId/?user_id={user_id}` |
| YouTube | `GET /auditor.youtube/?channel={channel}` | — (`channel` accepts ID or handle) |
| TikTok | `GET /auditor.tiktok/?channel={channel}` | `GET /auditor.tiktokByUserId/?user_id={user_id}` |
| Twitter (X) | `GET /auditor.twitter/?channel={channel}` | — |
| Twitch | `GET /auditor.twitch/?channel={channel}` | — |
| Snapchat | `GET /auditor.snapchat/?channel={channel}` | — |

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` / `channel` / `user_id` | string | Yes | Creator identifier (username without `@`, or channel/user ID) |
| `type` | string | No | `report` (mini report, 1 mini-report credit) or `advanced_report` (full report, 1 report credit). **Defaults to `advanced_report`** if omitted |
| `features` | string | No | Comma-separated feature list (e.g. `ranking,mentions`) for additional data |
| `v` | string | No | API version. Pass `v=2` — v1 is deprecated (Aug 1, 2024). Current version string: `2019-10-18` |

**Response includes**: AQS score, audience demographics, engagement metrics, brand safety, rankings, historical data, branded mentions.

**Credits**: An advanced report costs 1 report credit; a mini report costs 1 mini-report credit. Credits are refunded if generation fails because of account restrictions (a test account like `littlebig` / `nasa` is available without cost).

**Async processing**: May return 202 with `result.retryTtl` — wait the specified seconds then retry. Both report endpoints return the report if ready, or request it if not yet generated.

### Account Media

**Instagram**: `GET /auditor.instagramAccountMedia/?username={username}`
**YouTube**: `GET /auditor.youtubeAccountMedia/?channel_id={id}`
**TikTok**: `GET /auditor.tiktokAccountMedia/?username={username}`

Returns recent posts/videos with performance metrics.

### Metrics History

**Instagram**: `GET /auditor.instagramMetricsHistory/?username={username}`
**TikTok**: `GET /auditor.tiktokMetricsHistory/?username={username}`
**Twitter**: `GET /auditor.twitterMetricsHistory/?username={username}`
**Twitch**: `GET /auditor.twitchMetricsHistory/?username={username}`

Returns follower growth, engagement trends, and performance over time.

### Branded Mentions

**Instagram**: `GET /auditor.instagramBrandedMentions/?username={username}`
**YouTube**: `GET /auditor.youtubeBrandedMentions/?channel_id={id}`
**TikTok**: `GET /auditor.tiktokBrandedMentions/?username={username}`

Returns brand mentions and sponsored content detected in creator's posts.

### Lists Management API

Organize creators into lists for campaign management.

**Create list**: `POST /auditor.lists.create/`
**Get lists**: `GET /auditor.lists/`
**Add to list**: `POST /auditor.lists.addReports/`
**Remove from list**: `POST /auditor.lists.removeReports/`

### Campaign Management API

Two versions available (v1.0 and v2.0). Use v2.0 for new integrations.

**Endpoints**: Campaign CRUD, brief management, creator assignments, content approval workflows, performance tracking.

Full documentation: https://hypeauditor.com/swagger/campaign-management/

### Market Analysis API (Instagram Competitor Analysis)

Competitor analysis and industry benchmarking. **Instagram-only** in the API, and it lives on a different base path than the `auditor.*` methods (verified 2026-06-13):

**`POST https://hypeauditor.com/api/marketanalysis/instagramCompetitorAnalysis`**

Generates a competitor report including engagement metrics, reach data, sponsored-content analysis, and hashtag performance. Request parameters include `username` and `hashtags`.

*Plan-gated*: PRO and Enterprise only.

### Media Plan API v1.0

Creates branded, presentation-ready media plans for Instagram and YouTube influence campaigns, automatically calculating campaign metrics and KPIs. Documented under the public Swagger spec: `https://hypeauditor.com/swagger/public-api/v1/#/Media%20Plan` (exact request/response paths are in the Swagger doc).

### Recruitment API

Automated creator outreach and recruitment.

**Version**: v1.0

Covers campaign-based recruitment workflows, brief distribution, and application management.

### Creator Profile Info

Lists the influencer profiles whose reports your account has unlocked.

**`GET /auditor.creators`**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | int | No | 1-100 results per request |
| `report_unlocked_from` | date | No | Start of unlock window, ISO datetime `YYYY-MM-DDTHH:MM:SS±HH:MM` (live docs now use ISO datetime, not bare `yyyy-mm-dd`) |
| `report_unlocked_to` | date | No | End of unlock window, ISO datetime `YYYY-MM-DDTHH:MM:SS±HH:MM` |
| `cursor` | string | No | Pagination cursor — pass the `next_cursor` value from the previous page |

### Plan / quota info (Reports and Requests Left)

**`GET /auditor.planInfo/`**

Returns remaining quota for an API subscription:
- `reports.credits` (int) — report credits left, plus `reports.plan` (plan name)
- `discovery.requests` (int) — discovery requests left, plus `discovery.plan` (plan name)

API-subscription accounts only.

### Reference data endpoints

Lookup tables used to populate Discovery and report filters:
- **Taxonomy v1**: `GET /auditor.taxonomy/` — returns all available thematics/categories grouped by social network. The docs point here to "get all available thematics/categories," so Categories is served through this endpoint.
- **Languages**: the docs publish a list of supported language codes used for the `audience_lang` / language filters (consult the Languages reference page for the current code list).

## Pagination

All list endpoints use cursor-based pagination:
- Response includes `next_cursor` field
- Pass `cursor={next_cursor}` in next request
- Empty or null `next_cursor` means no more results

## PDF Export

Reports can be exported as PDF for client reporting. Use the `export` parameter on report endpoints.

## Rate limiting

- **100 requests per minute** maximum
- HTTP 429 returned when exceeded
- Implement exponential backoff for batch operations
- Monitor `restTokens` in responses to track remaining API credits

## Webhooks

No webhook support documented. Use polling for async operations (check `retryTtl` on 202 responses).
