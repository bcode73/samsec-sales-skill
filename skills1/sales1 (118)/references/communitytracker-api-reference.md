<!-- Source: https://www.communitytracker.ai/api-documentation (technical reference) + https://www.communitytracker.ai/api-integration (marketing) -->
<!-- Re-verified 2026-06-13 against live official docs. -->

# CommunityTracker API Reference

## Authentication

API-key authentication via the `X-API-Key` header (NOT `Authorization: Bearer`). Generate keys from the dashboard: Settings → API → Generate API Key. Keys use the format `ct_live_` followed by 32 random characters and are SHA-256 hashed server-side (plaintext never stored).

```
X-API-Key: ct_live_your_key_here
```

**Plan gate:** Trial/no-API-access plans receive `403 PLAN_NO_API_ACCESS`. API access requires Pro ($99/mo) or higher.

## Base URL

The official docs show the host as a `<your-base-url>` placeholder in examples; combine it with the paths below. The historically documented host is:

```
https://api.communitytracker.ai/
```

Endpoints are mounted at `/api-posts` and `/api-intelligence` (no `/v1/` prefix in the current technical docs).

## Rate limits

A single daily allowance of **5,000 requests** applies, with an hourly reset. Every response includes:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Daily allowance (5000) |
| `X-RateLimit-Remaining` | Requests left in the window |
| `X-RateLimit-Reset` | When the window resets |

Exceeding the limit returns HTTP 429 with error code `RATE_LIMIT_EXCEEDED`.

> Note: the marketing `/api-integration` page describes a per-plan model (Pro 1,000/day, Advanced 5,000/day). The technical `/api-documentation` page shows a single 5,000/day limit with rate-limit headers. Treat the rate-limit headers as the source of truth at runtime.

## Endpoints

### GET /api-posts

Fetch AI-scored community posts by keyword, with optional filtering by source, score threshold, intent, or date range.

**Request:**

```bash
curl -H "X-API-Key: ct_live_your_key_here" \
  "https://api.communitytracker.ai/api-posts?keyword=AI+tools&source=reddit&min_score=7&from=2026-03-28&limit=20"
```

**Parameters:**

| Param | Type | Required | Description |
|---|---|---|---|
| `keyword` | string | yes | Search term (omitting it returns `400 MISSING_KEYWORD`) |
| `source` | string | no | Filter by platform (e.g. `reddit`, `hackernews`, `producthunt`) |
| `min_score` | integer | no | AI score threshold (1–10) |
| `intent` | string | no | One of `buying`, `pain_point`, `question`, `comparison` |
| `from` | string | no | Start date `YYYY-MM-DD` |
| `to` | string | no | End date `YYYY-MM-DD` |
| `limit` | integer | no | Results per page (default 50, max 100) |
| `offset` | integer | no | Pagination offset |

**Response fields (per post):**

| Field | Description |
|---|---|
| `url` | Direct link to the conversation |
| `title` | Post/thread title |
| `body` | Post content |
| `author` | Author handle |
| `source` | Source platform |
| `kind` | Item type (post/comment/etc.) |
| `posted_at` | Timestamp |
| `ai_score` | AI relevance score (1–10) |
| `ai_reason` | Why the AI scored it this way |
| `intent` | `buying` / `pain_point` / `question` / `comparison` |
| `urgency` | Urgency assessment |
| `buying_stage` | Where the author is in the buying journey |
| `action_type` | Recommended action |
| `suggested_play` | Recommended next move |
| `competitor_named` | Whether a competitor was named |
| `buying_signals` | Detected buying signals |
| `engagement_status` | Engagement state |
| `subreddit` | Subreddit (Reddit only) |

### GET /api-intelligence

Access Share of Voice intelligence snapshots.

**Parameters:**

| Param | Type | Description |
|---|---|---|
| `query_id` | UUID | Required to retrieve data (omitting it returns `400 MISSING_QUERY_ID`) |
| `date` | string | Specific snapshot date `YYYY-MM-DD` |
| `from` | string | Range start `YYYY-MM-DD` |
| `to` | string | Range end `YYYY-MM-DD` |
| `limit` | integer | Max snapshots (default 30) |

**Behavior:**
- Called with no parameters → HTTP 400 plus a list of the account's active query IDs (use this to discover `query_id` values).
- With `query_id` only → latest snapshot.
- With `query_id` + date range → array of snapshots.

## Error codes

| HTTP | Code | Meaning |
|---|---|---|
| 401 | `MISSING_API_KEY` | No `X-API-Key` header provided |
| 401 | `INVALID_API_KEY` | Key invalid or revoked |
| 403 | `PLAN_NO_API_ACCESS` | Plan lacks API access (upgrade to Pro+) |
| 400 | `MISSING_KEYWORD` | Required for `/api-posts` |
| 400 | `MISSING_QUERY_ID` | Required for `/api-intelligence` |
| 404 | `QUERY_NOT_FOUND` | Query ID doesn't exist |
| 404 | `SNAPSHOT_NOT_FOUND` | No snapshot for the given date |
| 429 | `RATE_LIMIT_EXCEEDED` | Daily limit exceeded |
| 500 | `INTERNAL_ERROR` | Server error |

## SDKs

No official native SDKs. The docs provide copy-paste examples in Python (`requests`) and JavaScript/Node.js (`fetch`).

## Content generation (`/generate`)

The marketing `/api-integration` page references a `/generate` endpoint for AI-crafted posts (LinkedIn posts, newsletters, Twitter threads) feeding n8n / Make.com / Zapier workflows. This endpoint is NOT listed on the technical `/api-documentation` page (which documents only `/api-posts` and `/api-intelligence`). Treat `/generate` as marketing-described but technically unconfirmed — verify against the live API before relying on it.

## Webhooks

The marketing `/api-integration` page lists "Webhook push for real-time signals" (Pro+). The technical `/api-documentation` page does NOT document any webhook events, payloads, or signing. Webhook payload schema and signing remain officially undocumented — test with webhook.site and implement idempotent endpoints.

## Gaps

- Literal API host shown as `<your-base-url>` placeholder in official examples; `api.communitytracker.ai` is the historically documented host but not re-confirmed verbatim in the current doc.
- `/generate` endpoint named only on the marketing page, absent from the technical reference.
- Webhook event list, payload schema, and signing not officially documented.
- `/api-intelligence` snapshot response shape not field-by-field documented.
- No OpenAPI/Swagger spec found.
