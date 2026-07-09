<!-- Source: https://docs.ahrefs.com/docs/ahrefs-connect/developers/api-guide -->
<!-- Source: https://docs.ahrefs.com/docs/api/reference/api-keys-creation-and-management -->
<!-- Source: https://docs.ahrefs.com/docs/mcp/reference/introduction  |  https://github.com/ahrefs/ahrefs-mcp-server -->
<!-- Captured 2026-06-27. Base URL, auth, endpoint groups, the API-units cost model, and the MCP facts
     are from the official docs. Endpoint paths and JSON are CONSTRUCTED from the documented groups and
     marked — verify against the live reference / OpenAPI before relying. -->

# Ahrefs API Reference (v3) + MCP

Ahrefs exposes a **REST API v3** plus an **official hosted MCP server**. **API v2 was fully discontinued
2025-11-01** — build only on v3. Most data calls consume **API units** (a metered budget), so the whole
game is fetching exactly what you need. For AI-agent use, the **MCP server** is usually the faster path.

## Official MCP server (primary interface for AI agents)

- **What:** `ahrefs/ahrefs-mcp-server` (official, hosted) connects Claude / ChatGPT / Cursor directly to
  your Ahrefs account so an agent can pull backlinks, keywords, Domain Rating, and competitive data by
  prompt instead of clicking dashboards.
- **Plan:** available to **Lite plan and above**.
- **Claude Code setup (HTTP transport):**
  ```bash
  claude mcp add --transport http ahrefs "https://mcp.ahrefs.com" --header "Authorization: Bearer YOUR_API_KEY"
  ```
  (Confirm the exact hosted URL/headers in the MCP docs; some setups proxy via Composio.)
- **Docs:** `docs.ahrefs.com/docs/mcp`. MCP calls draw on the same account **API units** as the REST API.

## Base URL & authentication

- **Base URL:** `https://api.ahrefs.com/v3/`
- **Auth:** `Authorization: Bearer YOUR_API_KEY`.
- **Keys:** create/manage in **Account settings → API keys** (workspace **owners/admins only**). Up to
  **1,000 keys**; each key **expires after 1 year**.
- **OAuth 2.0:** for public Ahrefs Connect apps (multi-account).

### Auth quick-start (cheap call — your unit balance)

```bash
curl -s "https://api.ahrefs.com/v3/subscription-info/limits-and-usage" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## API units (the cost model — read this first)

- Every data request (except free test queries and a few endpoints — **Rank Tracker, Management, Public**,
  etc.) **consumes API units** from your account's monthly allocation.
- **Minimum 50 units per request**; cost **scales with rows returned × fields requested**.
- **Conserve units:** use **`select`** to request only needed fields, cap **`limit`** on rows, prefer
  **`batch-analysis`** for many targets, and expose the **`limits-and-usage`** endpoint so you can monitor
  spend. During app development (Inactive status) you get **free test requests** that don't consume units.
- Plans: **Lite / Standard / Advanced include a monthly API-unit allocation** for light use; heavy or
  production usage needs a **paid API subscription (≈$500–$10,000/mo) or Enterprise**.

## Endpoint groups

| Group | Example paths | Notes |
|---|---|---|
| Site Explorer | `/site-explorer/backlinks`, `/site-explorer/organic-keywords`, `/site-explorer/domain-rating`, `/site-explorer/metrics` | the core backlink/keyword/DR data; unit-metered |
| Keywords Explorer | `/keywords-explorer/overview`, `/keywords-explorer/volume-history` | keyword metrics, difficulty, volume |
| Rank Tracker | `/rank-tracker/...` | read your tracked-keyword projects (**often free** of units) |
| Site Audit | `/site-audit/...` | your audit projects/issues |
| Batch Analysis | `/batch-analysis` | bulk metrics for many URLs/domains in one call (unit-efficient) |
| Subscription | `/subscription-info/limits-and-usage` | remaining units/credits (free) |

> Exact paths/params vary — confirm against the live reference / OpenAPI. The constructed examples below are
> best-effort.

## Top endpoint examples

<!-- JSON CONSTRUCTED from documented groups — verify against the live reference -->

### 1. Domain Rating (GET `/site-explorer/domain-rating`)
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/domain-rating?target=example.com&date=2026-06-27" \
  -H "Authorization: Bearer $KEY"
```
```json
{ "domain_rating": { "domain_rating": 76, "ahrefs_rank": 12453 } }
```

### 2. Backlinks (GET `/site-explorer/backlinks`) — note `select` to save units
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/backlinks?target=example.com&limit=50&select=url_from,anchor,domain_rating_source,first_seen" \
  -H "Authorization: Bearer $KEY"
```
```json
{ "backlinks": [
  { "url_from": "https://blog.acme.com/post", "anchor": "great tool", "domain_rating_source": 64, "first_seen": "2026-05-01" }
] }
```

### 3. Organic keywords (GET `/site-explorer/organic-keywords`)
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/organic-keywords?target=example.com&country=us&limit=100&select=keyword,volume,position,traffic" \
  -H "Authorization: Bearer $KEY"
```
```json
{ "keywords": [ { "keyword": "best crm", "volume": 24000, "position": 7, "traffic": 320 } ] }
```

### 4. Keyword overview (GET `/keywords-explorer/overview`)
```bash
curl -s "https://api.ahrefs.com/v3/keywords-explorer/overview?keywords=best%20crm&country=us&select=keyword,volume,difficulty,cpc" \
  -H "Authorization: Bearer $KEY"
```
```json
{ "keywords": [ { "keyword": "best crm", "volume": 24000, "difficulty": 78, "cpc": 9.40 } ] }
```

### 5. Batch analysis (POST `/batch-analysis`) — many targets, fewer units
```bash
curl -s -X POST "https://api.ahrefs.com/v3/batch-analysis" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{ "targets": ["example.com","competitor.com"], "select": ["domain_rating","org_traffic","backlinks"] }'
```
```json
{ "results": [ { "target": "example.com", "domain_rating": 76, "org_traffic": 120000, "backlinks": 480000 } ] }
```

## Pagination & rate limits

- Most list endpoints support a `limit` (rows) and offset/cursor paging — keep `limit` small to save units.
- The docs reference a **limits-consumption** model rather than a fixed per-second rate; the practical
  constraint is your **unit budget**, and an **anti-abuse "suspicious activity"** system that can throttle
  bursty automated access even within plan limits. Spread calls, cache results, and back off on 429.

```python
import requests, time
def ahrefs(path, key, params=None):
    url = f"https://api.ahrefs.com/v3/{path.lstrip('/')}"
    h = {"Authorization": f"Bearer {key}"}
    for attempt in range(5):
        r = requests.get(url, headers=h, params=params, timeout=30)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** attempt); continue
        r.raise_for_status(); return r.json()
    r.raise_for_status()
```

## Gaps / not documented here

- Exact per-endpoint paths, params, and response schemas: use the **official reference / OpenAPI** — the
  paths above are constructed from the documented groups.
- No published fixed numeric rate limit; the binding constraint is **API units** + anti-abuse throttling.
- Webhooks: Ahrefs is a read/research API — no general event webhooks (it's pull, not push).
