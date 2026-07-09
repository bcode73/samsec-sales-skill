<!-- Source: https://syften.com/documentation + https://github.com/syften/syften-examples -->
<!-- Re-verified against live docs 2026-06-13. -->

# Syften API Reference

## Overview

Syften provides a REST API for programmatic access to keyword monitoring data. Available on Standard plan ($39.95/mo) and above. Webhooks and the MCP server are Pro-only.

## Base URL

```
https://syften.com/api/0.0
```

## Authentication

API token-based authentication via Bearer token in the `Authorization` header. Manage tokens in the dashboard under **Setup → API and Zapier**.

```bash
curl -X POST -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100}' \
  "https://syften.com/api/0.0/items/get"
```

## Endpoints

All endpoints use **POST** with `Content-Type: application/json`. There are no path parameters and no GET/PUT/DELETE verbs.

| Method | Path | Description | Request body | Plan |
|---|---|---|---|---|
| POST | `/api/0.0/items/get` | Return recent matches | `{"limit": 100}` (default 100, max 500) | Standard+ |
| POST | `/api/0.0/filters/get` | Return current filters as a JSON array of strings | none | Standard+ |
| POST | `/api/0.0/filters/set` | Replace ALL current filters | `{"filters": ["syften", "..."]}` | Standard+ |
| POST | `/api/0.0/settings/get` | Return account settings (API token redacted) | none | Standard+ |
| POST | `/api/0.0/info/get` | Return account info, plan details, stats, quota counters | none | Standard+ |

> `filters/set` REPLACES the entire filter set — it is not an append. To add a filter, first `filters/get`, modify the array, then `filters/set` with the full list. There is no per-filter create/update/delete endpoint.

## Response format

### POST /api/0.0/items/get

Returns a JSON array of match items. Each item:

```json
{
  "id": "match-id",
  "matched_on": "2026-05-04T12:34:56Z",
  "filter": "example.com",
  "item": {
    "backend": "reddit",
    "backend_sub": "r/startups",
    "type": "comment",
    "icon_url": "https://example.com/icon.png",
    "timestamp": "2026-05-04T12:34:56Z",
    "item_url": "https://example.com/thread",
    "author": "someuser",
    "text": "The matched text",
    "title": "Thread title",
    "title_type": 1,
    "lang": "en",
    "analysis": {
      "lang": "en",
      "sentiment": "neutral",
      "nsfw": false,
      "accept": true,
      "suggested_reply": "A short suggested reply, if available.",
      "score": 8,
      "excerpt": "The part of the item that matched the filter.",
      "rejection_reason": ""
    }
  }
}
```

**Analysis fields** (populated when AI filtering is enabled, Standard+):
- `accept`: bool — AI verdict on whether the match is relevant (true = accepted)
- `rejection_reason`: string — populated when `accept` is false
- `sentiment`: string (e.g. "neutral", "positive", "negative")
- `nsfw`: bool
- `score`: integer relevance score
- `excerpt`: string — the part of the item that matched the filter
- `suggested_reply`: string — a short suggested reply, if available
- `lang`: string — detected language

> Note: there is no `ai_verdict`/`ai_confidence` pair, no top-level `keyword`/`url`/`source` — those live under `item.*` (`item.backend`, `item.item_url`) and `filter`. The AI accept/reject signal is `item.analysis.accept`.

## Error handling

Errors return JSON: `{"code": 400, "error": "description"}`

## Pagination

`items/get` takes a `limit` (default 100, max 500). The daily result quota still applies. Poll no more than every 5 minutes.

## Rate limits

Not documented publicly with explicit headers. Daily result limits (Entry 100 / Standard 200 / PRO 500) act as the effective cap. Recommend polling no more than every 5 minutes.

## Webhooks (PRO only)

Webhooks push new matches to your HTTP endpoint as they arrive. Configure the webhook URL in **Setup → API and Zapier**.

### Webhook payload

The request is an HTTP POST with `Content-Type: application/json`. **The body is a JSON array of item objects, using the inner `item` shape from `items/get`** (not a single wrapped event object).

```json
[
  {
    "backend": "reddit",
    "backend_sub": "r/startups",
    "type": "comment",
    "timestamp": "2026-05-04T12:34:56Z",
    "item_url": "https://reddit.com/r/startups/comments/abc123/",
    "author": "someuser",
    "text": "The matched text",
    "title": "Thread title",
    "lang": "en",
    "analysis": {
      "sentiment": "neutral",
      "nsfw": false,
      "accept": true,
      "score": 8,
      "excerpt": "The part of the item that matched the filter."
    }
  }
]
```

Return any **2xx** status code to acknowledge delivery.

### Webhook retry behavior

Failed deliveries are retried for **up to 48 hours**. Retries start with a minimum backoff of **5 minutes** and can back off up to **12 hours** between attempts. If the webhook URL is no longer valid, delivery is skipped rather than retried.

> No documented HMAC signature header. The API and webhook payload formats are not version-locked; contact Syften if you need a strict field-stability guarantee.

## MCP server (PRO only)

Syften exposes an MCP endpoint at `https://syften.com/mcp` (Pro plan). It supports configuration inspection, filter health checking, preview, and match retrieval through MCP-compatible AI tools (Claude, Cursor, etc.).

## RSS / JSON feeds

Configured in **Setup → RSS**. Query parameters:
- `?tag=your-tag` — filter by tag
- `?accepted=true` — include accepted items
- `?accepted=false` — rejected items only

## Zapier integration

Token and Zapier setup live under **Setup → API and Zapier**. Official docs reference the API+Zapier setup section but do not document a named native Zapier trigger; many users wire Zapier via the webhook (Pro) instead. (Native trigger name unverified.)

## GitHub examples

Repository: https://github.com/syften/syften-examples

## Gaps

- Exact rate-limit headers and retry-after semantics for the API not documented
- No documented webhook HMAC signature header
- Exact Twitter/X and YouTube add-on prices not published on the pricing page (listed only as "Paid addon")
- Native Zapier trigger name not confirmed in official docs
