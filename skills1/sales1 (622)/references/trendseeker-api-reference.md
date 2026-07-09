<!-- Source: https://trend-seeker.app/docs/api -->

# Trend Seeker Public API Reference

## Base URL

```
https://api.trend-seeker.app/v1
```

## Authentication

Two methods supported:

```
Authorization: Bearer tskr_your_api_key
```

or:

```
X-API-Key: tskr_your_api_key
```

Unauthenticated requests are permitted but receive reduced rate limits and basic field access only.

API keys are prefixed with `tskr_`.

## Rate Limits

| Tier | Requests/Minute | Max Results/Page | Max Offset | Data Access |
|------|-----------------|------------------|------------|-------------|
| Anonymous | 10 | 20 | N/A | Basic fields |
| Free (with API key) | 10 | 20 | 100 | Basic fields |
| Pro | 120 | 100 | Unlimited | Full data with scores/metrics |

Limits reset on a 60-second rolling window. HTTP 429 is returned when exceeded.

## Endpoints

### GET /v1/ideas

Retrieve a list of business ideas, sorted by opportunity score by default.

**Parameters:**
- `limit` (integer) — results per page. Default 20, max 20 (free), max 100 (Pro).
- `offset` (integer) — pagination offset. Max 100 (free), unlimited (Pro).
- `categories` (string) — comma-separated category filter (e.g. `saas,fintech`).
- `keywords` (string) — comma-separated keyword filter.
- `min_validation_score` (float) — minimum validation score, 0.0–1.0.
- `created_after` (string) — filter by date, `YYYY-MM-DD`.
- `created_before` (string) — filter by date, `YYYY-MM-DD`.
- `sort` (string) — `created_at`, `validation_score`, or default (opportunity score).

**Example:**
```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas?limit=10&categories=saas"
```

**Response:**
<!-- Verified against https://trend-seeker.app/docs/api 2026-06-13 -->
```json
{
  "ideas": [
    {
      "id": "abc123",
      "business_idea_id": "abc123",
      "title": "AI-powered invoice reconciliation for freelancers",
      "tagline": "Auto-match receipts to invoices for solo freelancers",
      "evidence_strength": {
        "volume": 0.85,
        "urgency": 0.72,
        "specificity": 0.91
      },
      "market_metrics": {
        "competition_level": "medium",
        "monetization_potential": "high",
        "opportunity_score": 0.88
      },
      "validation_score": 0.78,
      "confidence_tier": "premium",
      "categories": ["fintech", "saas"],
      "post_count": 47,
      "solution_approach": "SaaS tool that...",
      "why_now": "Growing freelance market...",
      "created_at": "2026-04-15T10:30:00Z",
      "updated_at": "2026-04-20T08:00:00Z"
    }
  ],
  "meta": {
    "total": 1250,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

**Field notes:**
- `evidence_strength` is an object: `{volume, urgency, specificity}` (each 0.0–1.0).
- `market_metrics` is an object: `{competition_level, monetization_potential, opportunity_score}`. `competition_level` and `monetization_potential` are string buckets (e.g. `low`/`medium`/`high`); `opportunity_score` is a float.
- `categories` is an array; `post_count` is a top-level integer.
- Pagination lives in a `meta` object: `{total, limit, offset, has_more}`.

**Access notes:**
- Free users: `solution_approach` and `why_now` are redacted for `confidence_tier: "premium"` ideas
- Pro users: all fields returned

### GET /v1/ideas/search

Full-text search across idea titles, taglines, and problem descriptions. Semantic (embedding-based) matching is Pro-only.

**Parameters:**
- `q` (string, required) — search query
- `mode` (string) — `text` (default) or `semantic` (Pro only, embedding-based)
- `limit` (integer) — results per page
- `offset` (integer) — pagination offset
- `categories` (string) — comma-separated category filter
- `min_validation_score` (float) — text mode only

**Response:** Same idea structure as `/v1/ideas`, plus a `relevance` score on each result.

**Example:**
```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/search?q=invoice+automation&mode=semantic&limit=10"
```

### GET /v1/ideas/:id

Fetch a specific idea by its ID.

**Example:**
```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/abc123"
```

### GET /v1/ideas/:id/posts

Retrieve the original source posts from Reddit/communities that support a specific idea.

**Parameters:**
- `limit` (integer) — max posts to return. Default 10, max 5 (free), max 100 (Pro).

**Example:**
```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/abc123/posts?limit=5"
```

<!-- Verified against https://trend-seeker.app/docs/api 2026-06-13 -->
```json
{
  "posts": [
    {
      "id": "xyz789",
      "title": "I wish there was a tool that auto-reconciles invoices",
      "content": "Spent 3 hours this weekend matching receipts to invoices...",
      "platform": "reddit",
      "url": "https://reddit.com/r/freelance/...",
      "created_at": "2026-03-20T15:00:00Z"
    }
  ]
}
```

**Field notes:** Post objects expose `id`, `title`, `content`, `platform`, `url`, `created_at`. (Earlier captures listed `post_id`/`source`/`subreddit`/`score`/`num_comments` — those field names are not in the current docs.)

### GET /v1/categories

List all available idea categories with idea counts.

**Example:**
```bash
curl "https://api.trend-seeker.app/v1/categories"
```

**Response:** Array of `{ "category": "saas", "count": 342 }` objects.

No authentication required.

## Pagination

Offset-based pagination:
```
?limit=20&offset=0   # Page 1
?limit=20&offset=20  # Page 2
?limit=20&offset=40  # Page 3
```

Free tier: offset capped at 100 (effectively 5 pages of 20 results). Pro: unlimited offset.

## Error Handling

Errors return a consistent JSON shape:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid API key"
  }
}
```

**Status codes:**
- `200` — Success
- `401` — `UNAUTHORIZED` (invalid or expired API key)
- `404` — `NOT_FOUND`
- `429` — Rate limit exceeded (60-second rolling window)
- `500` — `INTERNAL_ERROR`

### Rate Limit Retry Strategy

```python
import time
import requests

def fetch_with_retry(url, headers, params, max_retries=3):
    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 429:
            wait = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise Exception("Rate limit exceeded after retries")
```

## Gaps

- Webhook support: None documented
- Write endpoints (POST/PUT/DELETE): None documented — API is read-only
- Rate limit response headers: Not documented (no `X-RateLimit-*` headers specified in the current docs — do not rely on them)
- MCP server: None
- SDK: None (REST-only)
