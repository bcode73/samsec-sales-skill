<!-- Source: https://replymer.com/api/docs -->

# Replymer API Reference

## Base URL

`https://replymer.com/api/v1`

## Authentication

API key via `X-API-Key` header (recommended) or `?api_key=` query parameter.

Key format: `rply_` prefix, 45 characters total. Max 3 active API keys per account.

```bash
curl https://replymer.com/api/v1/account \
  -H "X-API-Key: rply_your_api_key_here"
```

## Rate Limits

Per-user, hourly reset.

| Plan | Limit |
|---|---|
| Free Trial | 100/hr |
| Starter | 500/hr |
| Growth | 1,000/hr |
| Scale / Scale Plus / Scale Elite | Unlimited |

Every response includes `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers. 429 responses include retry guidance in the error message.

## Response Format

**Success:**
```json
{
  "success": true,
  "data": { ... },
  "meta": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human-readable description"
}
```

Error codes: `unauthorized` (401), `forbidden` (403), `not_found` (404), `bad_request` (400), `rate_limit_exceeded` (429), `plan_limit` (403), `internal_error` (500).

## Endpoints

### Account

| Method | Path | Description |
|---|---|---|
| GET | `/account` | Account info and current plan details |
| GET | `/account/stats` | Overall account statistics |

### Projects

| Method | Path | Description |
|---|---|---|
| GET | `/projects` | List all projects |
| GET | `/projects/:id` | Get a single project |
| POST | `/projects` | Create a new project (requires: title, domain) |
| PUT | `/projects/:id` | Update project settings (writable fields: `title`, `domain`, `description`, `notes`, `reddit`, `twitter`, `relevance`, `dailylimit`, `monthlylimit`, `repliesreport`, `twitter_handle`, `manual_approval`) |
| DELETE | `/projects/:id` | Delete a project permanently |
| POST | `/projects/:id/activate` | Reactivate a stopped project |
| POST | `/projects/:id/stop` | Pause monitoring and replies |

### Keywords

| Method | Path | Description |
|---|---|---|
| GET | `/projects/:projectId/keywords` | List project keywords |
| POST | `/projects/:projectId/keywords` | Add keywords (subject to plan limits) |
| DELETE | `/projects/:projectId/keywords/:id` | Remove a keyword by id |

### Negative Keywords

| Method | Path | Description |
|---|---|---|
| GET | `/projects/:projectId/negative-keywords` | List negative keywords |
| POST | `/projects/:projectId/negative-keywords` | Add negative keywords |
| DELETE | `/projects/:projectId/negative-keywords/:id` | Remove a negative keyword by id |

### Mentions

| Method | Path | Description |
|---|---|---|
| GET | `/projects/:projectId/mentions` | List mentions (paginated, filterable by status/source/keyword) |
| GET | `/projects/:projectId/mentions/:id` | Get a single mention |
| PUT | `/projects/:projectId/mentions/:id` | Update mention status (allowed values: `approved`, `declined`, `pending_client_approval`) |

### Replies

| Method | Path | Description |
|---|---|---|
| GET | `/projects/:projectId/replies` | List published replies (paginated) |
| GET | `/projects/:projectId/replies/:id` | Get a single reply |

### SEO

| Method | Path | Description |
|---|---|---|
| GET | `/projects/:projectId/seo-keywords` | List SEO keywords |
| POST | `/projects/:projectId/seo-keywords` | Add SEO keywords |
| DELETE | `/projects/:projectId/seo-keywords/:id` | Remove an SEO keyword by id |
| GET | `/projects/:projectId/seo-replies` | List SEO replies with Google ranking data (paginated) |
| GET | `/projects/:projectId/seo-replies/:id` | Get a single SEO reply |

### Analytics

| Method | Path | Description |
|---|---|---|
| GET | `/projects/:projectId/stats` | Project statistics for a given period |

Query parameters: `period` (1, 7, 30, or 90 days; default 7).

## Pagination

Mentions, replies, and SEO replies endpoints use offset pagination via `page` (default 1) and `limit` (default 20, max 100) query parameters. Responses include `meta: { page, limit, total, pages }`.

## Gaps

- Webhook support not documented — API appears pull-only
- Full request/response schemas not published (some field lists inferred from endpoint descriptions; PUT project writable fields and mention status enum confirmed from live docs)
- No published OpenAPI/Swagger spec
- No Postman collection found
- No official SDK / client library documented
