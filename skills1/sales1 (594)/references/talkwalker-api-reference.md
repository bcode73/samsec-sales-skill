<!-- Source: https://developer.talkwalker.com/api, https://developer.talkwalker.com/docs -->

# Talkwalker API Reference

## Authentication

- **Method**: Query parameter `access_token`
- **Token types**: `read_only` (search only), `read_write` (search + modify + stream)
- **How to get a token**: Contact Talkwalker sales (support@talkwalker.com) — not self-serve
- **Demo token**: `access_token=demo` — limited to queries `cats`, `dogs`, `cats AND dogs`; blogs/forums/news only; no social media

**Quick test:**
```bash
curl 'https://api.talkwalker.com/api/v1/search/results?access_token=demo&q=cats&hpp=5&pretty=true'
```

## Base URLs

| API | Base URL |
|---|---|
| Search, Summary, Histogram, Resources, Topic, Source panels, Modify docs | `https://api.talkwalker.com/api/v1/` |
| Image Detection | `https://api.talkwalker.com/api/v2/` |
| Streaming | `https://api.talkwalker.com/api/v3/` |

## API Modules & Endpoints

### Status API (1 endpoint)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/status` | Check API availability |

### Search API (3 endpoints)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/search/results` | Search outside a project (quicksearch — blogs, forums, news only; no social) |
| GET | `/api/v1/search/p/{project_id}/results` | Search within a project (includes social media) |
| GET | `/api/v1/search/p/{project_id}/results?topic={id}` | Search filtered by project topic |

**Parameters (Search):**

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `access_token` | string | Yes | — | Auth token |
| `q` | string | Yes | — | Boolean search query |
| `hpp` | int | No | 10 | Results per page (max 500) |
| `offset` | int | No | 0 | Results to skip |
| `sort_by` | string | No | engagement | `engagement`, `trending_score`, `published` |
| `sort_order` | string | No | desc | `asc` or `desc` |
| `time_range` | string | No | 30d | Duration: s, m, h, d, w, M units |
| `timezone` | string | No | UTC | Timezone for time_range |
| `hl` | bool | No | true | Enable snippet highlighting |
| `pretty` | bool | No | false | Pretty-print JSON |
| `summarize` | bool | No | false | AI summary (20 credits) |
| `custom_focus` | string | No | — | Restrict results to a custom-focus definition (verified 2026-06-13) |

**Project-specific params:** `topic`, `filter`, `channel`, `panel`, `dataset`

**Constraints:**
- Quicksearch: max offset 500, time range 30 days
- Project: max offset+hpp 10,000
- Datasets older than 7 days cannot be queried
- Credits: 1 per result, min 10 per call

### Summary API (2 endpoints)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/search/summary` | Aggregated metrics outside project |
| GET | `/api/v1/search/p/{project_id}/summary` | Aggregated metrics within project |

### Histogram API (3 endpoints)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/search/histogram` | Time-series data outside project |
| GET | `/api/v1/search/p/{project_id}/histogram` | Time-series data within project |
| GET | `/api/v1/search/p/{project_id}/histogram?topic={id}` | Histogram filtered by topic |

Rate limit: 60/min (quicksearch), 30/min (project). Credit cost: 10 credits/call (verified 2026-06-13).

### Streaming API v3 (8+ endpoints)

| Method | Path | Description |
|---|---|---|
| PUT | `/api/v3/stream/s/{stream_id}` | Create or replace a stream (5 calls/min) |
| GET | `/api/v3/stream/s/{stream_id}/results` | Connect to stream / pull results (persistent) |
| POST | `/api/v3/stream/s/{stream_id}/results` | Pull results with query in body or URL |
| DELETE | `/api/v3/stream/s/{stream_id}` | Delete a stream |
| GET/POST | `/api/v3/stream/p/{project_id}/results` | Project data access — pull project results (5 calls/min) |

**Rate limit:** Stream creation/replacement and project data-access endpoints are limited to **5 calls/min** (verified 2026-06-13). The api-restrictions page does not publish a separate limit for the results-streaming connection.

**Rule body:** rules are an array of objects with `rule_id` (string identifier) and `query` (the Boolean search string), e.g. `{"rules": [{"rule_id": "rule-1", "query": "\"Your Brand\""}]}`. If the stream ID already exists, the PUT overrides its rules.

**Streaming rules support:** Boolean queries, language, media type, title, content, author, URL, country, source include/exclude. Max 50 operands per rule (not re-verified 2026-06-13).

**Response chunk types:**
- `CT_CONTROL` — stream metadata and connection status
- `CT_RESULT` — search result documents

**Key behaviors:**
- Results delivered in crawler-found order (not chronological)
- Each result = 1 credit (regardless of matched rules)
- Manual updates and rule-applied tags do NOT transmit through streams
- Custom sorting not available (use Search API instead)

### Streaming > Collector API (6 endpoints)

Collector management for stream data collection.

### Streaming > Task API (6 endpoints)

Task management for stream processing jobs.

### Modify Documents API (Documents API v2)

Document modification now lives under the v2 `docs` namespace (not the old `/api/v1/search/p/{project_id}/results/...` paths). Verified 2026-06-13.

| Method | Path | Description |
|---|---|---|
| POST | `/api/v2/docs/p/<project_id>/create` | Import/create a single document |
| POST | `/api/v2/docs/p/<project_id>/update` | Update a single document's fields |
| POST | `/api/v2/docs/p/<project_id>/upsert` | Create or update a single document |
| POST | `/api/v2/docs/p/<project_id>/delete` | Delete a single document |
| POST | `/api/v2/docs/p/<project_id>/undelete` | Restore a previously deleted document |
| POST | `/api/v2/docs/p/<project_id>` | Batch create/update/delete multiple documents |

**Dataset variants** (Customer Intelligence projects) use `/api/v2/docs/p/<project_id>/d/<dataset_id>/<operation>` and `/api/v2/docs/p/<project_id>/d/<dataset_id>` for batch.

**Notes:**
- Rate limit: 120 calls/min.
- **No credits** are consumed for document create/update/delete calls.
- Only documents that match at least one topic in the project can be imported.
- Batch operations return HTTP `200` even if some documents fail — check each item's status individually.
- Any modification via the API **overwrites** changes made in the Talkwalker UI; all earlier changes (manual or via export/import) in the same project are lost.

### Resources API (8 endpoints)

Managing project resources (filters, channels, etc.).

### Topic API (4 endpoints)

CRUD operations for monitoring topics within a project.

### Source Panels API (3 endpoints)

Managing source panel configurations.

### Image API v2 (2 endpoints)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v2/detect/images/{type}?image_url={url}` | Detect features in image by URL |
| POST | `/api/v2/detect/images/{type}` | Detect features in uploaded image (multipart) |

**Detection types:** `logo`, `object`, `scene`

**Parameters:**
- `access_token` (required)
- `image_url` (for GET — must be from whitelisted URL prefix)
- `image_file` (for POST — multipart/form-data)
- `detect` (optional — restrict to specific image IDs)

**Response fields:** `confidence` (0-1), `position` (top/left/right/bottom for logos), `id` (Talkwalker image ID), image dimensions

**Rate limit:** 300 calls/min

## Rate Limits Summary

| API | Limit |
|---|---|
| Search (quicksearch) | 240 calls/min |
| Search (project) | 60 calls/min |
| Histogram (quicksearch) | 60 calls/min |
| Histogram (project) | 30 calls/min |
| Document Import | 120 calls/min |
| Image Detection | 300 calls/min |
| Streaming (create/replace stream, project data access) | 5 calls/min |

Credit reset: monthly, on the day of the subscription at 03:00 UTC (verified 2026-06-13).

## Pagination

- **Pattern:** offset + hpp (hits per page)
- Quicksearch: max offset = 500, max hpp = 500
- Project: max offset + hpp = 10,000
- Response includes `next` link for pagination and `total` count

```bash
# Page 1
curl '...&hpp=100&offset=0'
# Page 2
curl '...&hpp=100&offset=100'
```

## Data Export Restrictions

The following data CANNOT be fully exported via API:
- **Facebook/Instagram**: not exportable via the APIs (aggregated metrics only via Histogram API)
- **X (Twitter)**: limited to ~1.5M docs per month per account (tweet ID, author ID, sentiment score)
- **Online news / TV Eyes**: content is truncated
- **LinkedIn, raw Reddit, raw TikTok, Chinese sources, Disqus, monitored sites, certain review sites**: not exportable
- **WEB_NLA restricted articles**: blocked from export

<!-- Export restrictions re-verified 2026-06-13 against developer.talkwalker.com/docs/getting-started/api-restrictions: FB/IG not exportable; X (Twitter) 1.5M docs/mo/account; online news + TV Eyes truncated; LinkedIn, raw Reddit, raw TikTok not exportable. -->


## Error Handling

API returns standard HTTP status codes. Check for:
- `401` — invalid or expired access token
- `429` — rate limit exceeded (implement exponential backoff)
- `400` — malformed query or invalid parameters

## Gaps

- Full OpenAPI/Swagger spec is JS-rendered and not directly fetchable
- Collector API and Task API endpoint details not documented in public pages
- Resources API endpoint details not fully documented
- Webhook support not documented — no push/webhook mechanism found in the official developer portal as of 2026-06-13 (egress is poll-based Search API or persistent Streaming API)
- Credit quota/allocation per plan not publicly documented
- MCP server availability is not confirmed on Talkwalker's official developer portal; some third-party reviews mention MCP for Claude/ChatGPT/Gemini/Copilot but this may refer to the Hootsuite platform — treat as unverified
- Whether the Streaming API has a published rate limit on the results-streaming connection itself (separate from the 5/min on stream creation) is not stated
