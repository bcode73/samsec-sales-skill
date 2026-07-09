<!-- Source: https://pypi.org/project/reletter/, https://reletter.com/developers, https://reletter.com/llms-full.txt — re-verified 2026-06-13 -->

# Reletter API Reference

## Overview

Reletter provides a REST API for searching 7M+ email newsletters, pulling contact data, and accessing publication metadata. The API is available as a $59/mo add-on to any base plan (5,000 requests/month); higher request tiers run up to 50,000 requests/month ($429/mo).

## REST API base URL & auth

- **Base URL**: `https://api.reletter.com`
- **Auth header**: `x-reletter-api-key: YOUR_API_KEY` (NOT `Authorization: Bearer`)

```bash
curl -H "x-reletter-api-key: $RELETTER_API_KEY" \
  "https://api.reletter.com/api/search/publications/?query=fintech"
```

### REST endpoints (verbatim from /developers + /llms-full.txt)

| Method | Path | Key params |
|---|---|---|
| GET | `/api/search/publications/` | `query` (required), `mode`, `page`, `per_page`, `filters` |
| GET | `/api/search/issues/` | `query` (required), `highlight`, `threshold`, `page`, `per_page`, `filters` |
| GET | `/api/search/autocomplete/` | `query` (required), `mode` (required) |
| GET | `/api/publications/<publication_id>/` | — (single publication; `publication_id` is the slug, e.g. `doomberg`) |
| GET | `/api/publications/` | `publication_ids` (required), `include`, `ignore_missing`, `suggest` |
| GET | `/api/issues/` | `publication_id` (required) |
| GET | `/api/issues/<issue_id>/` | — |
| GET | `/api/contacts/` | `publication_id` (required) |
| GET | `/api/charts/` | — |
| GET | `/api/charts/<platform>/<category>/` | `variant` (optional) |
| GET | `/api/misc/languages/` | — |
| GET | `/api/misc/stats/` | — |
| GET | `/api/accounts/quota/` | — (does NOT count against quota) |
| GET | `/api/payments/bundles/` | — (unauthenticated; pricing source of truth) |
| POST | `/api/payments/buy/` | `{"quota": <int>}` (unauthenticated MPP bootstrap) |

**Publication identity**: publications are keyed by **slug** (string, e.g. `doomberg`, `noahpinion`), returned in the `id` field. The contacts endpoint takes `publication_id=<slug>`.

**Pagination**: response includes `page`, `per_page`, `count`, and `more` (boolean). Default `per_page` is 25, max 100.

### Filters DSL (REST)

Format: `name:operator:value`, comma-separated, max 20 filters per request. Example: `filters=subscribers:gte:5000,active:is:true`.

| Filter type | Fields | Example |
|---|---|---|
| Range | `subscribers`, `engagement`, `monthlyvisits`, `issues`, `founded` | `subscribers:gte:5000`, `engagement:lte:100` |
| Boolean | `active`, `sponsored` | `active:is:true`, `sponsored:is:false` |
| Choice | `languages`, `platforms`, `pubmodels`, `frequencies` | `languages:any:en-es-fr`, `platforms:any:substack-beehiiv` |
| Sort | `sort` | `sort:eq:subscribers` |

**Issues search** adds `highlight` (boolean, highlighted snippets) and `threshold` (integer seconds, max 14 days = 1209600).
**Autocomplete** `mode` values: `topics`, `titles`, `authors`, `issues`.

## Authentication (SDK)

API key via environment variable or direct parameter:

```bash
export RELETTER_API_KEY="your_api_key"
```

```python
from reletter import Reletter

# Option 1: Uses RELETTER_API_KEY env var automatically
client = Reletter()

# Option 2: Pass key directly
client = Reletter(api_key="your_api_key")
```

Two ways to get an API key:
1. Sign up at reletter.com with monthly billing
2. Programmatic payment via HTTP 402/MPP for autonomous AI agents

## Python SDK

**Install**: `pip install reletter` (or `pipx install reletter` for isolated CLI)

**Requirements**: Python 3.8+

**Version**: 1.0.2 (released 2026-05-09, Production/Stable)

**License**: MIT

**Source**: `https://github.com/getreletter/reletter-python`

### Key methods

| Method | Description |
|---|---|
| `publications.get(slug)` | Look up a publication by slug |
| `search.publications(query, filters)` | Search publications with filters |
| `search.iter_publications(query, filters)` | Auto-paginating search iterator |
| `search.issues(query, filters)` | Search newsletter issue content |
| `contacts.get(slug)` | Pull contact info for a publication |
| `charts` | Access chart/ranking data |
| `account.quota()` | Check API usage quota |

### Search with filters

Filters support three formats:

```python
# Dict format
results = client.search.publications(
    query="artificial intelligence",
    filters={"subscribers": {"gte": 5000}, "active": True}
)

# DSL string format (REST filter syntax: name:operator:value, comma-separated)
results = client.search.publications(
    query="artificial intelligence",
    filters="subscribers:gte:5000,active:is:true"
)

# Clause list format
results = client.search.publications(
    query="artificial intelligence",
    filters=[
        {"field": "subscribers", "op": "gte", "value": 5000},
        {"field": "active", "op": "eq", "value": True}
    ]
)
```

### Auto-pagination

```python
# Iterates through all pages automatically
for pub in client.search.iter_publications(query="fintech"):
    print(pub.name, pub.subscribers)
```

### Async support

```python
from reletter import AsyncReletter

async def main():
    client = AsyncReletter()
    results = await client.search.publications(query="AI")
    for pub in results:
        print(pub.name)
```

### Error handling

```python
from reletter.exceptions import (
    AuthenticationError,   # Invalid or missing API key
    RateLimitError,        # 429 — quota exceeded
    BadRequestError,       # 400 — invalid parameters
)
```

Automatic retries: Default 2 retries with exponential backoff on 429 and 5xx responses.

## CLI

**Install**: `pip install reletter` or `pipx install reletter`

```bash
# Look up a publication
reletter publications get doomberg

# Search publications
reletter search publications --query "artificial intelligence" --filters '{"subscribers": {"gte": 5000}}'

# Search issues
reletter search issues --query "YourBrand"

# Check quota
reletter account quota
```

**Exit codes**: 0 = success, 1 = API error, 2 = usage error, 4 = auth error, 5 = server error

## MCP Server

**URL**: `https://mcp.reletter.com`

Works with Claude, ChatGPT, Cursor, or any MCP client. Requires `RELETTER_API_KEY` for authentication.

**Source**: `https://github.com/getreletter/reletter-mcp`

Available operations: publication search, contact lookup, issue search, chart data.

## LLM reference files

- `https://reletter.com/llms.txt` — short index
- `https://reletter.com/llms-full.txt` — full reference with every endpoint

## Rate limits & quotas

- **API add-on**: 5,000 requests/month ($59/mo); higher tiers run up to 50,000 requests/month ($429/mo).
- **Monthly subscription quota**: counted per calendar month; the `/api/accounts/quota/` endpoint returns `usage` and `quota` and does NOT count against the quota.
- **Hourly burst limit**: 2,000 requests per team per hour (sliding window).
- Quota errors return HTTP `400` with `code: api_quota_exceeded`; pay-per-bundle exhaustion returns `400` with `code: bundle_exhausted`.
- SDK handles rate limits automatically with retries + exponential backoff (default 2 retries, configurable via `Reletter(max_retries=N)`).
- Monitor usage: `client.account.quota()` or `reletter account quota`.

## Agent-native API purchase (HTTP 402 / MPP)

For autonomous agents, an API key can be bought without a dashboard signup:

- `GET /api/payments/bundles/` — list available bundles (unauthenticated; source of truth for pricing).
- `POST /api/payments/buy/` with body `{"quota": <int>}` — initiates purchase. Returns `402` with a `WWW-Authenticate: Payment ...` challenge header (`method="stripe|tempo"`). On success returns `200` with `api_key`, `quota`, `used`, `remaining`, `expires_at`, `bundle_id`, `payment_intent_id`.
- Payment methods: `stripe` (SPT, synchronous), `tempo` (USDC, asynchronous with deposit address). Implements the IETF MPP standard.

## Gaps

- MCP server tool list not fetchable without auth.
- Webhook support: none (no webhooks, callbacks, or push notifications mentioned anywhere in the docs).
- Zapier/Make integrations: none.
- Exact monthly quota tier breakpoints between $59 (5K) and $429 (50K) not enumerated on the developers page — fetch `/api/payments/bundles/` for the live price/quota list.
- AI Search availability via API: unclear (may be UI-only).
