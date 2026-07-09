<!-- Source: https://dev.mention.com/current/src/index.html -->

# Mention API Reference

## Overview

JSON-based RESTful API. The live docs at dev.mention.com label **1.8 as "current"**; later versioned doc trees (1.9–1.19) also exist. Pin a version with the `Accept-Version` header (e.g. `Accept-Version: 1.8`). Omitting it uses the account default.

**Base URL:** `https://api.mention.net/api` (the real-time stream uses a separate host — see Streaming below).

**Authentication:** Bearer token via `Authorization: Bearer {token}` header or `?access_token={token}` query parameter. Create an app in the developer dashboard to get a token, or use OAuth2 for third-party accounts.

**Important:** API access is a **paid add-on with an "extra cost" on every plan, including the Company plan** (Mention's API Access help article states "This service has an extra cost"; pricing is unpublished — contact your account manager). Re-verified 2026-06-13.

## Auth quick-start

```bash
curl -s 'https://api.mention.net/api/accounts/{account_id}/alerts' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Accept-Version: 1.19'
```

## Request/response format

- POST/PUT: JSON body with `Content-Type: application/json`
- Responses: JSON, status 200 for success
- Dates: W3C level 6 format (e.g., `1997-07-16T19:20:30.12345+01:00`)

## Error responses

| Status | Meaning |
|---|---|
| 400 | Invalid input — returns structured validation errors |
| 401/403 | Access denied |
| 404 | Resource not found |
| 429 | Rate limited — check `X-Rate-Limit-Reset` header (unix timestamp) |

Error shape:
```json
{
  "error": {
    "status": 400,
    "message": "Validation failed",
    "fields": {
      "name": ["Name is required"]
    }
  }
}
```
<!-- Constructed from docs — verify against live API -->

## Rate limits

The live rate-limits appendix (re-checked 2026-06-13) only states "Limits vary based on resource types and methods" and returns `429` + `X-Rate-Limit-Reset` (unix timestamp) when exceeded — it does **not** publish per-endpoint numbers. The values below were captured from earlier docs and are **indicative, not currently re-confirmed**; always honor `X-Rate-Limit-Reset` rather than hard-coding these.

| Resource | Limit (indicative) |
|---|---|
| Create alert | max(20, alertsQuota * 2) per 24 hours |
| List mentions | 3,600 per alert per 24 hours |
| Other endpoints | Varies — check `X-Rate-Limit-Reset` on 429 |

## Pagination

Cursor-based. Responses include `_links` object:

```json
{
  "_links": {
    "more": {
      "href": "/api/accounts/.../alerts?limit=20&cursor=abc",
      "params": {"limit": 20, "cursor": "abc"}
    }
  }
}
```

Follow `_links.more.href` for next page. Attribute only present if more results exist. For mentions, `_links.pull` provides a URL for fetching only newer mentions (incremental polling).

## Endpoints

### Alerts

#### List alerts
```
GET /accounts/{account_id}/alerts
```

**Query params:**
| Param | Type | Description |
|---|---|---|
| `limit` | integer | Number of alerts to return (default: all) |
| `cursor` | string | Pagination cursor |
| `ids` | array | Specific alert IDs (max 50) |

**Response:**
```json
{
  "alerts": [
    {
      "id": 12345,
      "name": "My Brand",
      "query": {"type": "basic", "included_keywords": ["acme"]},
      "languages": ["en"],
      "sources": ["web", "twitter"],
      "stats": {"mentions": 1542},
      "created_at": "2026-01-15T10:30:00+00:00"
    }
  ],
  "_links": {"more": {"href": "..."}}
}
```
<!-- Constructed from docs — verify against live API -->

#### Create alert
```
POST /accounts/{account_id}/alerts
```

**Required body fields:**
| Field | Type | Description |
|---|---|---|
| `name` | string | Human-readable identifier |
| `query` | object | `{type: "basic"|"advanced", included_keywords, excluded_keywords, required_keywords}` |
| `languages` | array | Language codes (max 5) |

**Optional body fields:**
| Field | Type | Description |
|---|---|---|
| `countries` | array | Country codes (max 5) |
| `sources` | array | Source types: web, twitter, facebook, instagram, reddit, etc. |
| `blocked_sites` | array | URLs to exclude |
| `noise_detection` | boolean | Enable noise filtering |
| `sentiment_analysis` | boolean | Enable sentiment (Pro+ only) |
| `reviews_pages` | array | Review site URLs to monitor |
| `color` | string | Alert color in UI |
| `connection_type` | string | "main", "related", or "independent" |
| `connection_id` | string | Related alert ID |
| `description` | string | Alert description |

#### Update alert
```
PUT /accounts/{account_id}/alerts/{alert_id}
```

Same body fields as create. Omitted fields remain unchanged.

#### Delete alert
```
DELETE /accounts/{account_id}/alerts/{alert_id}
```

#### Pause / unpause alert
```
POST /accounts/{account_id}/alerts/{alert_id}/pause
POST /accounts/{account_id}/alerts/{alert_id}/unpause
```
Pause stops a running alert from consuming your mention quota; unpause resumes it. Verified in the live docs 2026-06-13.

### Mentions

#### List mentions
```
GET /accounts/{account_id}/alerts/{alert_id}/mentions
```

**Query params:**
| Param | Type | Description |
|---|---|---|
| `limit` | integer | Results per page (default 20, max 1000) |
| `cursor` | string | Pagination cursor |
| `since_id` | string | Return mentions newer than this ID |
| `before_date` | date | Mentions published before this date |
| `not_before_date` | date | Ignore mentions older than this date |
| `source` | string | Filter by source type |
| `unread` | boolean | Only unread mentions |
| `favorite` | boolean | Only favorited mentions |
| `folder` | string | inbox, archive, spam, trash |
| `tone` | integer | Sentiment: -1, 0, 1 |
| `countries` | array | Filter by country |
| `languages` | array | Filter by language |
| `sort` | string | Order by: published_at, author_influence.score, direct_reach, cumulative_reach, or domain_reach |
| `q` | string | Keyword search within results |
| `include_children` | boolean | Include child mentions |
| `timezone` | string | Timezone for date parsing |

**Response:**
```json
{
  "mentions": [
    {
      "id": "67890",
      "alert_id": 12345,
      "title": "Great review of Acme",
      "description": "Acme Corp just launched their...",
      "original_url": "https://example.com/post",
      "tone": 1,
      "source_type": "web",
      "source_name": "Example Blog",
      "published_at": "2026-03-10T14:22:00+00:00",
      "author_influence": {"score": 72},
      "tags": [],
      "folder": "inbox",
      "read": false
    }
  ],
  "_links": {
    "more": {"href": "...older mentions..."},
    "pull": {"href": "...newer mentions..."}
  }
}
```
<!-- Constructed from docs — verify against live API -->

**Note:** `description` is truncated to ~250 characters. Follow `original_url` for full content.

#### Get single mention
```
GET /accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}
```

Returns full mention object (see data model in platform-guide.md).

#### Curate mention
```
PUT /accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}
```

**Body fields (all optional):**
| Field | Type | Description |
|---|---|---|
| `favorite` | boolean | Mark as favorite (admin only) |
| `trashed` | boolean | Move to trash (admin only) |
| `read` | boolean | Mark as read |
| `tags` | array | Array of `{id: tag_id}` objects |
| `folder` | string | Move to folder (archive, inbox, etc.) |
| `tone` | integer | Override sentiment: -1, 0, 1 |

No minimum required fields — send only what you want to update.

### Streaming mentions (real-time)

Separate host: **`https://stream.mention.net/api`** (not `api.mention.net`).

```
GET https://stream.mention.net/api/accounts/{account_id}/mentions?alerts[]={alert_id}
```

Opens a long-lived HTTP connection and pushes each mention as soon as it's fetched. Verified in the live docs 2026-06-13.

- **`alerts[]`** (array, required) — alert IDs to stream.
- **`since_id`** (optional) — object keyed by alert ID → mention ID, to backfill recent history per alert.
- Only **one open stream per `account_id`** at a time.
- Sends a maximum of **1000 mentions per alert**, then emits a warning message.
- The stream also emits `"mark"` keep-alive signals interleaved with mention objects — your client must tolerate them.

Use streaming for real-time use cases; use the `_links.pull` polling pattern (below) for simpler incremental sync.

### Statistics

```
GET /accounts/{account_id}/alerts/{alert_id}/stats
```
Returns aggregated alert statistics (mention volume, etc). Documented in the live docs (section "Fetch Statistics") 2026-06-13; full response schema not captured here — inspect a live response.

## Gaps

- **No webhooks/callbacks** — confirmed against live docs 2026-06-13. Egress is GET polling (`_links.pull`) or the real-time streaming endpoint only. There is no push/HMAC-signed callback surface.
- Streaming endpoint host/path/limits now captured above, but the full streamed-object schema and reconnection/backoff semantics are not fully specified in public docs.
- Statistics endpoint exists (`/alerts/{id}/stats`) but its response schema is not captured here — inspect a live response.
- Per-endpoint rate-limit numbers are **not published** in the live docs (the appendix only says "Limits vary based on resource types and methods" and to read `X-Rate-Limit-Reset` on 429). The specific numbers in the Rate-limits table below were captured earlier from the docs and are NOT re-confirmed by the current appendix — treat as indicative.
- Tag CRUD endpoints and full account-management endpoints not fully documented.
- Full response schemas may have additional fields not captured here.
