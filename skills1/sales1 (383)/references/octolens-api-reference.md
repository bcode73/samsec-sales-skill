<!-- Source: https://octolens.com/docs/api/v2/overview -->
<!-- Re-verified against live docs 2026-06-13: API is now v2. -->

# Octolens API Reference

## Base URL

```
https://app.octolens.com/api/v2
```

The API is on **v2**. The older `/api/v1` paths are no longer current — migrate to `/api/v2`.

## Authentication

Bearer token in the Authorization header.

```bash
curl -X POST https://app.octolens.com/api/v2/mentions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit": 20}'
```

**Key management:** Create API keys at Settings > API tab. Specify name and expiration date. Revoke via three-dot menu.

**Scopes:** Keys carry one of three scopes — `read`, `write` (implies read), or `admin` (implies write).

API access included on all plans (Pro, Scale, Enterprise).

## Rate Limits

500 requests per hour, per organization (counted across all keys).

**Headers:**
- `X-RateLimit-Limit` — hourly cap (500)
- `X-RateLimit-Remaining` — requests left
- `X-RateLimit-Reset` — **Unix timestamp** when the window resets

**On 429:** Response includes a `Retry-After` header — back off until then.

## Endpoints

The v2 API exposes a broad surface. Full reference + "Try it" playgrounds at
`https://octolens.com/docs/api-reference/` (OpenAPI at
`https://octolens.com/docs/api-reference/openapi.json`).

| Group | Endpoints |
|---|---|
| Mentions | `POST /mentions` (list), `POST /mentions/export`, `GET /mentions/{id}`, list-by-author, `PATCH`/update-a-mention |
| Keywords | `GET /keywords`, create, update, delete, toggle-pause, list/accept/reject keyword suggestions |
| Feeds | list, get, create, update, delete (a "feed" = a saved filter view) |
| Filters | get/update global filters, list filterable tags |
| Analytics | mention-volume-over-time, per-keyword-breakdown, sentiment-distribution, source/platform-breakdown |
| AI | `POST /ai/filter-wizard` — convert natural language to a filter object |
| Organization | `GET /org`, `GET /org/usage`, get/update company profile, update organization |
| Members | list, invite, remove |
| Feedback | submit / remove relevance feedback |

> **Note:** v1 modeled saved filters as `GET /views`. In v2 these are **feeds** (`/feeds`),
> and a feed/view id is passed as the `view` parameter on the mentions endpoints.
> Keyword and feed **management** (create/update/delete) is now available via the API —
> it was UI-only in v1.

### POST /mentions

Retrieves mentions matching configured keywords with filtering.

**Request body:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer (1-100) | No | Page size. Default: 20 |
| `cursor` | string | No | Opaque cursor from a previous response's `pagination.nextCursor` |
| `view` | integer | No | Feed/view ID (>0) to reuse as a base filter |
| `includeAll` | boolean | No | When `true`, includes low-relevance mentions. Default: false |
| `filters` | object | No | Filter object — simple flat form, or advanced group form with AND/OR operators. (Generate one from natural language via `POST /ai/filter-wizard`.) |

**Response:**

```json
{
  "data": [
    {
      "id": 123,
      "sourceId": "111111111",
      "url": "https://reddit.com/r/SaaS/comments/abc123",
      "title": "...",
      "body": "Full text of the mention...",
      "source": "reddit",
      "timestamp": "2026-05-04T14:32:00.000Z",
      "author": "username",
      "authorName": "Display Name",
      "authorAvatar": "https://...",
      "authorUrl": "https://reddit.com/u/username",
      "authorFollowers": 1250,
      "relevance": "high",
      "relevanceComment": "...",
      "sentiment": "positive",
      "language": "en",
      "tags": ["Own Brand Mention"],
      "keywords": ["octolens"],
      "engaged": false,
      "relevanceScore": "high",
      "feedbackRelevant": null,
      "imageUrl": null,
      "keywordId": 42
    }
  ],
  "pagination": { "nextCursor": null }
}
```

> Field names are camelCase in v2 (e.g. `authorName`, `authorFollowers`, `relevanceScore`,
> `sourceId`). The legacy v1 snake_case shape (`keyword_id`, `published_at`,
> `relevance_tags`, `engagement{}`) and the top-level `mentions`/`cursor` keys no longer apply.

### POST /mentions/export

Export up to 50,000 mentions matching a view and filters. Same body as `POST /mentions`
plus `format` (`"json"` | `"csv"`, default `"json"`).

- `format=json` → `{ "data": Mention[], "total": <int> }`
- `format=csv` → `text/csv` body with an `X-Total-Count` header

### GET /keywords

Lists all configured keywords.

**Response:**

```json
{
  "data": [
    {
      "id": 42,
      "keyword": "octolens",
      "context": "social listening tool for developers",
      "additionalTerms": null,
      "additionalTermsAndOr": false,
      "caseSensitive": false,
      "symbolSensitive": false,
      "platforms": ["reddit", "twitter", "github", "hackernews", "linkedin"],
      "excludeWords": null,
      "wildcardExcludeWords": null,
      "excludeAuthors": null,
      "tag": "own_brand",
      "paused": false,
      "isSubReddit": null
    }
  ]
}
```

- `tag` enum: `own_brand`, `competitor`, `industry_term` (or null).
- `platforms` enum: `dev`, `github`, `hackernews`, `linkedin`, `producthunt`, `reddit`,
  `stackoverflow`, `twitter`, `youtube`, `tiktok`, `medium`, `reddit_comment`, `bluesky`,
  `newsletter`, `podcasts`, `news`.

### GET /org/usage

Returns plan consumption. Response (`OrgUsage`): `plan`, `mentions {count, limit, resetAt}`,
`keywords {count, limit}`, and `flex {enabled, budgetCents, used, resetAt}` when flex
billing is enabled. Useful for checking remaining mention quota programmatically.

## Error Responses

| Status | Code | Description |
|---|---|---|
| 400 | `invalid_request` | Malformed request body or invalid parameters |
| 401 | `unauthorized` | Missing or invalid API key |
| 403 | `forbidden` | Key lacks permission for this resource |
| 404 | `not_found` | Resource does not exist |
| 429 | `rate_limit_exceeded` | Over 500 req/hr — check X-RateLimit-Reset |
| 500 | `internal_error` | Server error — retry with backoff |

**Error response shape:**

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 42 seconds."
  }
}
```
<!-- Constructed from docs — verify against live API -->

## Pagination

Cursor-based. The response includes `pagination.nextCursor` when more results exist. Pass it in the next request's `cursor` parameter.

- Cursors are opaque strings — do not parse or construct them
- When `pagination.nextCursor` is null, you've reached the end
- Maximum 100 results per page

## Webhooks

Webhooks push new mentions to your configured HTTPS endpoint as they're detected.

**Setup:** Webhooks are configured **per feed**, not globally. Open a feed → "Set up alert"
→ toggle on Webhook → enter URL → test → pick a **frequency** (Instantly, Hourly, Daily, or
Weekly) → save. Octolens webhook URLs are **Discord-compatible** (point straight at a Discord
channel webhook with no middleware).

**Delivery:** HTTPS `POST` with a JSON body, `Content-Type: application/json`. One mention per
request. Reply with any `2xx` to acknowledge, promptly (under a few seconds) — if processing is
slow, acknowledge first and queue the work.

**Payload shape:** a top-level `action` field plus a `data` object. `action` is currently always
`mention_created` ("a new mention matched the feed"); docs note more action types may be added.

```json
{
  "action": "mention_created",
  "data": {
    "title": "...",
    "body": "...",
    "url": "https://...",
    "timestamp": "2024-12-04T13:55:32.000Z",
    "imageUrl": "...",
    "author": "...",
    "authorName": "...",
    "authorAvatarUrl": "...",
    "authorProfileLink": "https://...",
    "authorFollowerCount": 1234,
    "source": "reddit",
    "sourceId": "111111111",
    "relevanceScore": "high",
    "relevanceComment": "...",
    "keyword": "Octolens",
    "keywords": ["Octolens", "social listening"],
    "sentimentLabel": "Neutral",
    "tags": ["Own Brand Mention"],
    "language": "en",
    "subreddit": "r/subreddit",
    "viewId": 111,
    "viewName": "Feed name",
    "viewKeywords": ["Octolens"]
  }
}
```

> Note the webhook `data` field names differ slightly from the REST mention object
> (e.g. `authorAvatarUrl`/`authorProfileLink`/`authorFollowerCount`/`sentimentLabel` and the
> `viewId`/`viewName`/`viewKeywords` feed context), and the payload is wrapped in `action`/`data`.

**No signature verification.** Docs state webhook signing is not currently available; use a
unique, unguessable endpoint URL or a secret query parameter and validate it server-side.

## MCP Server

The MCP server enables AI tools (Claude Code, Cursor, Windsurf, VS Code, Zed) to query Octolens data via natural language.

### MCP v2 (current — OAuth, HTTP transport)

v2 uses **OAuth** — there's no API key or token to paste. The transport is **HTTP** (not SSE)
and the endpoint is `https://app.octolens.com/api/mcp/v2`. Beyond mentions, v2 adds feeds,
analytics, and keyword/feed management tools.

```bash
claude mcp add --transport http octolens \
  "https://app.octolens.com/api/mcp/v2"
```

On first use you'll complete a browser-based OAuth sign-in. Generate setup snippets from
**Settings → MCP** in the app.

### MCP v1 (legacy — token in URL, SSE)

The older v1 server still works for existing connections but is **no longer the default and
receives no new features**. It uses SSE with a token in the URL:

```bash
claude mcp add octolens --transport sse \
  "https://app.octolens.com/api/mcp?token=YOUR_API_KEY"
```

New setups should use v2 (OAuth + feeds/analytics/management). Either way, the MCP credential
flow is separate from the REST API key.

**Available queries (natural language):**
- List keywords / manage feeds (v2)
- Show recent mentions
- Filter by platform, sentiment, tags
- Summarize mention trends / pull analytics (v2)

## Gaps

- Webhook retry/failure behavior not documented (timeout expectation only — reply 2xx promptly)
- Webhook signing not available — authenticate via secret/unguessable URL
- No official Python/Node SDKs published — call the REST API directly (OpenAPI spec available
  at `https://octolens.com/docs/api-reference/openapi.json` for codegen)
- Per-endpoint request/response detail beyond mentions/keywords/usage above is summarized — see
  the live `api-reference/` pages for exact schemas of feeds, filters, analytics, members, feedback
