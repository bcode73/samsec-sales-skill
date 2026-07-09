# Brandwatch API Reference

## Authentication

**Method**: OAuth 2.0 (grant type: `api-password`)

**Get an access token:**
```bash
curl -X POST --data-urlencode 'password=[yourpassword]' \
  'https://api.brandwatch.com/oauth/token?username=[your@username.com]&grant_type=api-password&client_id=brandwatch-api-client'
```

**Response:**
```json
{
  "access_token": "aa000000-0aaa-0000-0a00-aa00a000a00a",
  "token_type": "bearer",
  "expires_in": 31535999,
  "scope": "read trust write"
}
```

**Token expiration**: ~1 year (31,535,999 seconds) for API users.

**Using the token** — either method works:
- Header: `Authorization: Bearer [ACCESS_TOKEN]`
- URL parameter: `&access_token=[ACCESS_TOKEN]`

**Multi-organization**: If your account accesses multiple organizations, add `platform_client_id` to the token request. Contact Brandwatch support for available platform client IDs.

**Requirements**: Only "Regular" or "Admin" user accounts can access the API.

## Base URL

```
https://api.brandwatch.com
```

## API Products

Brandwatch offers 6 API products:

| API | Purpose | Key endpoints |
|---|---|---|
| **Analysis API** | Query content library, return aggregated statistics | Mentions, topics, charts, sentiment breakdowns, top sites/authors |
| **Consumer Research API** | Real-time data export and streaming | Mention retrieval, filtered mentions, data streaming |
| **Data Upload API** | Import custom data for analysis alongside social data | Document upload, custom data source creation |
| **Measure API** | Owned social media metrics export | Social channel analytics, performance data |
| **Publish API** | Social publishing data export | Scheduled posts, publishing history |
| **Engage API** | Social inbox and conversation data | Messages, conversations, assignments |

## Key Endpoints (Consumer Research API)

### User and client management
- `GET /me` — combined User + Client info in one call
- `GET /user` — current user (id, username, name, role, permissions)
- `GET /client` — current client (singular; the entity that is billed, includes rate-limit config)

### Projects and queries
- `GET /projects/summary` — list your Projects (recommended first call; returns id + name)
- `GET /projects` — list Projects with full detail
- `GET /projects/{id}` — get a specific Project
- `GET /projects/{projectId}/queries` — list queries in a project
- `POST /projects/{projectId}/queries` — create a new query
- `PUT /projects/{projectId}/queries/{queryId}` — update a query (PATCH also accepted)
- `DELETE /projects/{projectId}/queries/{queryId}` — delete a query

### Data retrieval
- `GET /projects/{projectId}/data/mentions` — retrieve mentions (snippets)
- `GET /projects/{projectId}/data/mentions/fulltext` — retrieve mentions with full text instead of snippets
- `GET /projects/{projectId}/data/mentions/count` — total number of mentions in a time period
- `GET /projects/{projectId}/data/volume` — volume over time
- `GET /projects/{projectId}/data/topics` — trending topics
- `GET /projects/{projectId}/data/sentiment` — sentiment breakdown

### Filtering and paging
Mention retrieval requires `queryId` (or `queryGroupId`, repeatable) plus `startDate` / `endDate`
in ISO format `YYYY-MM-DDThh:mm:ss.SSS+ZZZZ` (UTC offset). Optional filters/paging:
- `pageSize` — 1–5000 mentions per page
- `page` — page number, zero-indexed
- `orderBy` / `orderDirection` — sort field and `asc`/`desc`
- `language` — language codes
- `sentiment` — positive, neutral, negative
- `locationId` — geographic filter
- `pageType` — source type (twitter, reddit, blog, forum, news, etc.)

### Organization
- Tags, categories, rules, and lists (author, location, site)
- Custom alerts and workflow management

## Python SDK

**Current SDK** (for Consumer Research):
```bash
pip install bcr-api
```

```python
from bcr_api import BWProject

# Authenticate
project = BWProject(username='you@company.com', password='yourpassword')

# Or with API key
project = BWProject(token='your-access-token')

# Query mentions
mentions = project.get_mentions(
    queryId=12345,
    startDate='2025-01-01',
    endDate='2025-01-31'
)
```

**GitHub repos**:
- `BrandwatchLtd/bcr-api` — Python client for Consumer Research API
- `BrandwatchLtd/api_sdk` — General API SDK with examples and Jupyter notebook demo

## Rate Limits

**Default limit (Consumer Research API):** 30 API requests per rolling 10-minute window.
- Applied **per-Client** (not per-User) — all users on the same billed Client share the budget.
- Exceeding the limit returns **HTTP 429 Too Many Requests**.
- Two response headers report your usage:
  - `x-rate-limit` — the limit in `<limit>/<period>m` form, e.g. `30/10m`
  - `x-rate-limit-used` — calls made in the current window, e.g. `5`
- If your use case needs more, Brandwatch can grant alternative arrangements on request.

Docs: https://developers.brandwatch.com/docs/rate-limiting

*Re-verified 2026-06-13. Other API products (Measure, Publish, Engage, Data Upload) may differ — check their docs.*

## Developer Resources

- **Developer portal**: https://developers.brandwatch.com/
- **Getting started**: https://developers.brandwatch.com/docs/getting-started
- **Authentication**: https://developers.brandwatch.com/docs/authenticate
- **Data retrieval**: https://developers.brandwatch.com/docs/data-retrieval
- **Best practices**: https://developers.brandwatch.com/docs/best-practices
- **GitHub**: https://github.com/BrandwatchLtd
