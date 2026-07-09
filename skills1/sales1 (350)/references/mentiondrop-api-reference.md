<!-- Source: https://www.mentiondrop.com/openapi/mentiondrop-v1.json, https://www.mentiondrop.com/docs/api -->

# MentionDrop API Reference

## Overview

HTTP API for AI-processed web mentions. Supports read and write operations: list/get mentions, save relevance feedback, list/create/update keywords, get a grouped digest, and generate reply drafts. Authenticate with an API key from the MentionDrop dashboard (Settings → API Key).

- **Base URL:** `https://www.mentiondrop.com/api/v1`
- **OpenAPI spec:** `https://www.mentiondrop.com/openapi/mentiondrop-v1.json` (OpenAPI 3.1, info.title "MentionDrop API")
- **API docs:** `https://www.mentiondrop.com/docs/api`
- **API version:** 1.0.0

## Authentication

Two methods supported (use either):

| Method | Header | Example |
|---|---|---|
| Bearer token | `Authorization: Bearer <key>` | `Authorization: Bearer sk_live_abc123` |
| API key header | `X-API-Key: <key>` | `X-API-Key: sk_live_abc123` |

Create your API key in the MentionDrop dashboard under **Settings**.

### Auth quick-start

```bash
# Verify your API key works
curl -s "https://www.mentiondrop.com/api/v1/mentions?limit=1" \
  -H "X-API-Key: your_api_key_here" | jq .
```

## Endpoints

The API surface covers reads and writes. As of 2026-06-13 the OpenAPI spec defines:

| Method | Path | operationId | Purpose |
|---|---|---|---|
| GET | `/api/v1/me` | `getCurrentAccount` | Validate API key, return plan + capability metadata |
| GET | `/api/v1/mentions` | `listMentions` | List processed mentions with filters + pagination |
| GET | `/api/v1/mentions/{id}` | `getMention` | Fetch one mention owned by the account |
| PATCH | `/api/v1/mentions/{id}` | `updateMentionFeedback` | Save relevant / not-relevant feedback on a mention |
| GET | `/api/v1/keywords` | `listKeywords` | List monitored keywords |
| POST | `/api/v1/keywords` | `createKeyword` | Create a monitored keyword |
| PATCH | `/api/v1/keywords/{id}` | `updateKeyword` | Update keyword role, context, relevance threshold, active state, filters |
| GET | `/api/v1/digest` | `getDigest` | Grouped digest (owned-brand / competitor / demand / reply-worthy) |
| POST | `/api/v1/reply-drafts` | `createReplyDraft` | Generate a reply or outreach draft for a mention |

> The API is **no longer read-only** — keyword creation/update, mention feedback, and reply-draft generation are writeable. (Earlier docs described a single read-only `/mentions` endpoint; that is now superseded.)

### GET /api/v1/mentions

Retrieve processed mentions with optional filtering.

**Query parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `keyword` | UUID | No | — | Filter by keyword UUID. **Repeatable** — pass multiple `keyword=uuid1&keyword=uuid2` |
| `source` | string | No | — | Enum: `firehose`, `reddit`, `brave`, `google_news`, `serper` |
| `sentiment` | string | No | — | Enum: `positive`, `neutral`, `negative` |
| `content_type` | string | No | — | Enum: `article`, `comment`, `job_posting`, `cv`, `course`, `documentation`, `other` |
| `contact_found` | boolean | No | — | Filter to mentions where contact info was found |
| `from` | datetime | No | — | ISO-8601 with offset (e.g., `2026-05-01T00:00:00Z`) |
| `to` | datetime | No | — | ISO-8601 with offset |
| `page` | integer | No | 1 | Page number (minimum: 1) |
| `limit` | integer | No | 20 | Results per page (range: 1-100) |

**Response — 200 OK:**

The list response wraps mentions in a `mentions` array plus a `pagination` object (not flat top-level `page`/`limit`/`total`). An optional `redditLockedCount` reports Reddit results hidden behind plan limits.

```json
{
  "mentions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "url": "https://reddit.com/r/SaaS/comments/abc123/...",
      "title": "Looking for a lightweight project management tool",
      "summary": "User is frustrated with Asana's complexity and asking for simpler alternatives for a 5-person remote team.",
      "sentiment": "negative",
      "relevance_score": 0.87,
      "suggested_action": "respond",
      "source": "reddit",
      "source_domain": "reddit.com",
      "matched_at": "2026-05-06T14:34:12Z",
      "keywords": {
        "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "keyword": "TaskFlow",
        "role": "own_brand",
        "context": "TaskFlow is a project management SaaS tool",
        "is_active": true,
        "min_relevance": 60,
        "mention_count_30d": 12
      }
    }
  ],
  "pagination": { "page": 1, "limit": 20, "hasNext": true, "hasPrev": false },
  "redditLockedCount": 0
}
```

**Mention object fields (per OpenAPI spec):** `id`, `url`, `title` (nullable), `summary` (nullable), `sentiment` (nullable enum), `relevance_score` (nullable), `suggested_action` (nullable), `source` (nullable), `source_domain` (nullable), `matched_at` (nullable datetime), `keywords` (embedded Keyword object). The earlier flat `keyword_id`, `content_type`, `published_at`, and `created_at` fields are not in the current spec response (`content_type` survives as a query filter; the keyword is embedded under `keywords`; timestamps are `matched_at`).

**Error responses:** spec defines `400` (bad request), `401` (unauthorized), `403` (forbidden), `404` (not found), `409` (conflict — e.g., keyword already exists, on `POST /keywords`), `422` (unprocessable entity).

### GET /api/v1/me

Validate an API key and return plan + capability metadata.

```json
{
  "user": { "id": "uuid", "email": "you@example.com", "plan": "starter" },
  "capabilities": { }
}
```

The `plan` field is an enum of internal plan codes `free`, `starter`, `pro` (these are the API-side codes; the public pricing page brands the paid tiers **Monitor** and **Radar** — see platform-guide.md).

### PATCH /api/v1/mentions/{id}

Save relevance feedback on a mention. Request body (`MentionFeedbackInput`): `verdict` (enum `relevant` | `not_relevant` | null), `user_feedback` (enum `relevant` | `not_relevant` | null). Returns `200`.

### GET /api/v1/keywords  ·  POST /api/v1/keywords  ·  PATCH /api/v1/keywords/{id}

Keywords are now manageable via API (previously dashboard-only).

- **`POST /keywords`** body (`CreateKeywordInput`): `keyword` (string, 2–100 chars, **required**), `context` (string/null, max 300 chars), `role` (enum `own_brand` | `competitor` | `industry`). Returns `201`; `409` if the keyword already exists.
- **`PATCH /keywords/{id}`** body (`PatchKeywordInput`): `is_active` (boolean), `context` (string/null), `role` (enum), `excluded_content_types` (array of ContentType enums), `exclusion_terms` (array of strings, max 20), `min_relevance` (integer 0–100). Returns `200`.

**Keyword object:** `id` (UUID), `keyword` (string), `role` (enum), `context` (string/null), `is_active` (boolean), `min_relevance` (integer), `mention_count_30d` (integer/null). Required: `id`, `keyword`, `role`, `is_active`.

### GET /api/v1/digest

Returns a `DigestResponse` with a `sections` object containing four arrays of mention objects — `owned_brand_mentions`, `competitor_signals`, `demand_signals`, `conversations_worth_replying_to` — plus a `pagination` object.

### POST /api/v1/reply-drafts

Generate an AI reply or outreach draft for a processed mention. Body (`CreateReplyDraftInput`): `mention_id` (UUID, **required**), `draft_intent` (enum `reply` | `outreach_email`, default `reply`). Returns `201`.

## Pagination

Offset-based via `page` and `limit`. The list response returns a `pagination` object with `page`, `limit`, `hasNext`, and `hasPrev` (no `total` count in the spec). Loop while `pagination.hasNext` is true (or until the `mentions` array is empty / shorter than `limit`).

```bash
# Page 1 (default)
curl -s "https://www.mentiondrop.com/api/v1/mentions?limit=100&page=1" \
  -H "X-API-Key: your_key"

# Page 2
curl -s "https://www.mentiondrop.com/api/v1/mentions?limit=100&page=2" \
  -H "X-API-Key: your_key"
```

## Rate limits

Rate limit details are not documented in the OpenAPI spec. Monitor response headers for `X-RateLimit-*` or `Retry-After` headers. If you encounter 429 responses, implement exponential backoff:

```python
import time
import requests

def fetch_with_backoff(url, headers, params, max_retries=3):
    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 429:
            wait = 2 ** attempt
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise Exception("Rate limited after max retries")
```

## Discovery endpoints

| Endpoint | Purpose |
|---|---|
| `/.well-known/api-catalog` | RFC 9727 API catalog |
| `/openapi/mentiondrop-v1.json` | OpenAPI 3.1 specification |
| `/.well-known/openid-configuration` | OIDC discovery (Clerk auth) |
| `/.well-known/oauth-protected-resource` | RFC 9728 resource metadata |

## Gaps

- **Webhook payload schema not documented.** Webhooks are a real product feature ("Webhook delivery" is listed on both paid pricing tiers) but the OpenAPI spec defines no webhook events, payload, or signing. Capture POST payloads via webhook.site before building integrations.
- **Rate limits not documented.** No published rate limit policy or `X-RateLimit-*` headers in the OpenAPI spec.
- **Alert/notification config is dashboard-only.** Slack, email, and webhook delivery are configured in the UI; the API has no endpoints for managing notification channels.
- **`GET /api/status` health endpoint is not in the spec.** It may still exist as a non-spec route; not verified against current docs.
