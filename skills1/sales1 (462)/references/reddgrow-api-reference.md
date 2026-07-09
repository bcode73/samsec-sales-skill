<!-- Source: https://docs.reddgrow.ai/docs and https://docs.reddgrow.ai/docs/reddit-intelligence/api — re-verified 2026-06-13 -->

# ReddGrow API Reference

There are TWO distinct REST APIs on the same host (`https://api.reddgrow.ai`), both authenticated with the same `x-api-key` key:

1. **Agent API** (`/agent/*`) — Reddit Intelligence: 19 GET endpoints returning clean Reddit JSON. All plans (credit-based).
2. **AEO API** (`/v1/aeo/*`) — AI Observability / answer-engine-optimization data (visibility, citations, sources, brands, topics, scores). **Pro plan required.**

## Authentication

All requests require an API key passed in the `x-api-key` header. Keys are prefixed with `rg_` and created at **Settings → API Keys** in the ReddGrow dashboard (`https://app.reddgrow.ai/settings/api-keys`).

```bash
curl -H "x-api-key: rg_your_key_here" https://api.reddgrow.ai/agent/me
```

## Base URL

```
https://api.reddgrow.ai
```

All Agent API endpoints use **GET** requests and return clean JSON.

## Rate limits

- **60 requests per minute**
- **1,000 requests per hour**
- Both windows are enforced independently per API key.
- Exceeding either returns **HTTP 429** with body `{"statusCode": 429, "message": "Too many requests"}`. Wait for the window to reset (per-minute resets every 60s, per-hour every 3,600s).

**Credit usage headers** are returned on responses: `X-Credits-Used`, `X-Credits-Remaining`, `X-Credits-Limit`.

**Retry strategy:** On a 429, wait for the current window to reset before retrying; exponential backoff starting at 1 second is a safe default.

## Credit costs (Agent API)

Per the docs, credits are tiered by endpoint type:

| Tier | Cost | Endpoints |
|---|---|---|
| Simple lookup | 1 credit | `about`, `rules`, `traffic`, `widgets`, user `profile` |
| List/feed | 2 credits | `posts`, `comments`, user `posts`/`comments` |
| Search | 3 credits | subreddit `search`, post `search`, `check-url` |
| Heavy/batch | 5 credits | `wiki`, `duplicates`, batch `posts`, `domain mentions` |

## Agent API endpoints (19 total)

### Meta (1)

| Method | Path | Description | Credits |
|---|---|---|---|
| GET | `/agent/me` | Account identity and current credit balance | 1 |

### Subreddits (10)

| Method | Path | Description | Credits |
|---|---|---|---|
| GET | `/agent/subreddits/search` | Search subreddits by keyword (`?q=`) | 3 |
| GET | `/agent/subreddits/{name}/about` | Subreddit info — subscribers, description, settings | 1 |
| GET | `/agent/subreddits/{name}/rules` | Get posting rules for a subreddit | 1 |
| GET | `/agent/subreddits/{name}/posts` | Read post feed from a subreddit | 2 |
| GET | `/agent/subreddits/{name}/comments` | Read comment feed from a subreddit | 2 |
| GET | `/agent/subreddits/{name}/wiki` | Subreddit wiki index | 5 |
| GET | `/agent/subreddits/{name}/wiki/{page}` | A specific wiki page | 5 |
| GET | `/agent/subreddits/{name}/widgets` | Subreddit widgets | 1 |
| GET | `/agent/subreddits/{name}/traffic` | Subreddit traffic stats | 1 |
| GET | `/agent/subreddits/{name}/check-url` | Check if a URL was posted to a subreddit | 3 |

### Posts (4)

| Method | Path | Description | Credits |
|---|---|---|---|
| GET | `/agent/posts/search` | Search all posts by keyword (`?q=`, `?limit=` max 100, default 25) | 3 |
| GET | `/agent/posts/batch` | Batch fetch posts by ID | 5 |
| GET | `/agent/posts/{subreddit}/{id}/comments` | Comments on a post | 2 |
| GET | `/agent/posts/{subreddit}/{id}/duplicates` | Duplicate/cross-posts of a post | 5 |

### Domains (1)

| Method | Path | Description | Credits |
|---|---|---|---|
| GET | `/agent/domains/{domain}/mentions` | Reddit posts linking to a domain (`?limit=` max 100, default 25) | 5 |

### Users (3)

| Method | Path | Description | Credits |
|---|---|---|---|
| GET | `/agent/users/{username}` | User profile — karma, account age | 1 |
| GET | `/agent/users/{username}/posts` | User's recent posts (`?limit=` max 100) | 2 |
| GET | `/agent/users/{username}/comments` | User's recent comments (`?limit=` max 100) | 2 |

## AEO API endpoints (`/v1/aeo/*`, Pro plan required)

AI-visibility / answer-engine-optimization data. Auth is the same `x-api-key` header; rate limits are the shared 60/min · 1,000/hr pool. Returns 402 if the plan does not include AEO access.

`GET /v1/aeo/me`, `/engines`, `/countries`, `/score-methodology`, `/prompts`, `/prompts/{id}`, `/prompts/{id}/runs`, `/runs/{scan_result_id}`, `/runs/{scan_result_id}/explain`, `/brands`, `/brands/ranking`, `/topics`, `/citations`, `/sentiment/explain`, `/sources/detail`, `/sources/domains`, `/sources/top-domains`, `/sources/domain-types`, `/sources/urls`, `/visibility/by-brand`, `/visibility/by-engine`, `/visibility/by-country`, `/visibility/by-topic`, `/visibility/timeline`, `/visibility/explain`.

## Request/response examples

### GET /agent/me

```bash
curl -H "x-api-key: rg_abc123" https://api.reddgrow.ai/agent/me
```

Response (verbatim from docs):

```json
{
  "ok": true,
  "credits": {
    "used": 42,
    "remaining": 958,
    "limit": 1000
  }
}
```

### GET /agent/subreddits/search?q=typescript+programming

```bash
curl -H "x-api-key: rg_abc123" \
  "https://api.reddgrow.ai/agent/subreddits/search?q=typescript+programming"
```

Returns a JSON array of subreddit objects (note: `display_name`, NOT `name`; there is no `relevance_score` field):

```json
[
  {
    "display_name": "typescript",
    "subscribers": 312000,
    "created_utc": 1356998400,
    "public_description": "TypeScript is a language for application-scale JavaScript.",
    "over18": false,
    "subreddit_type": "public",
    "active_user_count": 847,
    "submission_type": "any",
    "allow_images": true,
    "allow_videos": true,
    "restrict_posting": true,
    "link_flair_enabled": true
  }
]
```

### GET /agent/domains/{domain}/mentions

```bash
curl -H "x-api-key: rg_abc123" \
  "https://api.reddgrow.ai/agent/domains/example.com/mentions"
```

Returns a flat JSON **array of post objects** (NOT an object with a `mentions` key), sorted by recency:

```json
[
  {
    "id": "abc123",
    "title": "TypeScript 5.4 released — what's new?",
    "selftext": "string",
    "author": "typescript_fan",
    "created_utc": 1704067200,
    "url": "https://devblogs.microsoft.com/typescript/announcing-typescript-5-4/",
    "permalink": "/r/typescript/comments/abc123/typescript_54_released/",
    "subreddit": "typescript",
    "score": 1247,
    "num_comments": 89,
    "domain": "devblogs.microsoft.com",
    "post_hint": "image",
    "is_self": true
  }
]
```

### GET /agent/users/{username}

```bash
curl -H "x-api-key: rg_abc123" \
  "https://api.reddgrow.ai/agent/users/spez"
```

Response (verbatim from docs — separate `link_karma`/`comment_karma`, no `post_history` on this endpoint; use `/users/{username}/posts` for history):

```json
{
  "id": "string",
  "name": "string",
  "created_utc": 0,
  "link_karma": 0,
  "comment_karma": 0,
  "is_gold": true,
  "icon_img": "string",
  "subreddit": {
    "public_description": "string"
  }
}
```

## CLI Reference

The official CLI is `@reddgrow/cli`. Install with any package manager:

```bash
npm install -g @reddgrow/cli      # or: yarn global add / pnpm add -g / bun add -g
reddgrow --version
```

Quick start:

```bash
reddgrow auth login rg_your_key_here   # save your API key
reddgrow auth whoami                    # verify the connection
reddgrow subreddits about MachineLearning
```

### Command groups (alias)

| Group | Alias | Description |
|---|---|---|
| `auth` | — | Manage API key/connection — `login`, `whoami`, `status`, `logout` |
| `subreddits` | `r` | 10 commands: `search`, `about`, `rules`, `posts`, `comments`, `wiki`, `wiki-page`, `widgets`, `traffic`, `check-url` |
| `posts` | — | `search`, `comments`, `duplicates`, `batch` |
| `users` | `u` | `profile`, `posts`, `comments` |
| `domains` | `d` | `mentions` |

### Global options

| Flag | Description |
|---|---|
| `--mode agent` | Force raw JSON output (for scripting / AI agent pipelines) |
| `--mode human` | Force rich colored output |
| `--help` | Show help for any command |
| `--version` | Print installed version |

Output mode is auto-detected (human terminal / agent JSON) when not forced.

## Gaps

- Full request/response schemas for the wiki/widgets/traffic/duplicates/batch endpoints not captured here — query the interactive playground at `docs.reddgrow.ai`.
- Pagination beyond the `limit` query param (max 100, default 25) is not documented — unclear if cursor or offset paging exists for large result sets.
- Detailed error-response schemas (beyond the 429 body) not documented.
- No webhook / push support found — both APIs are read-only GET-only.
- AEO API (`/v1/aeo/*`) response payloads not captured here — Pro-plan-gated; see the AEO API Reference in the docs.
