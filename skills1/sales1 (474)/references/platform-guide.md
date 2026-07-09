# Reletter Platform Reference

## Overview

Reletter is a newsletter search engine indexing 7M+ email newsletters across Substack, LinkedIn, Beehiiv, Kit, Ghost, and other platforms. It provides subscriber estimates, creator contact info, engagement metrics, and keyword monitoring. Primary use cases: sponsorship prospecting, PR outreach, cross-promotion, and newsletter research.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| **Newsletter Search** | Search 7M+ publications by topic, platform, subscriber count, engagement | API-accessible, UI |
| **AI Search** | Semantic search for newsletter discovery beyond keyword matching | UI (API support unclear) |
| **Contact Intelligence** | Creator email addresses and social media accounts | API-accessible (`contacts.get()`) |
| **List Building** | Create, manage, and export target newsletter lists | UI, API-accessible |
| **Keyword Monitoring** | Email alerts when brands/keywords appear in newsletter issues | UI-only (alerts) |
| **Issue Search** | Search full text of newsletter issues | API-accessible (`search.issues()`) |
| **Charts/Rankings** | Newsletter ranking data by category | API-accessible (`charts`) |
| **Publication Profiles** | Detailed pages with subscriber numbers, similar newsletters, traffic estimates | API-accessible (`publications.get()`) |

## Pricing, limits & plan gates

| Feature | Light ($49/mo) | Standard ($99/mo) | Business ($199/mo) |
|---|---|---|---|
| Searches/month | 100 | 500 | Unlimited |
| Lists | 3 | 50 | Unlimited |
| Alerts | Yes (count unclear) | 50 | 100 |
| Users | 1 | 5 | 10 |
| Exports | Yes | Yes | Yes |
| Priority Support | No | No | Yes |
| **API add-on** | +$59/mo (5K req) | +$59/mo (5K req) | +$59/mo (5K req) |

- 7-day free trial (credit card required, cancel anytime); full refund within 30 days if the service is unused
- Yearly billing: 2 months free
- API is a separate add-on on any plan: $59/mo for 5,000 requests, scaling up to 50,000 requests/month ($429/mo); 2,000 req/team/hour burst limit applies

## Integrations

- **API**: REST API at `https://api.reletter.com` (auth header `x-reletter-api-key`) with Python SDK and CLI
- **MCP Server**: `https://mcp.reletter.com` — works with Claude, ChatGPT, Cursor, or any MCP client
- **CRM export**: Export lists to CSV for CRM import
- **No Zapier/Make**: No iPaaS connectors available
- **No webhooks**: No event-driven integrations (no webhooks/callbacks anywhere in the docs)
- **Agent-native purchase**: API keys can be bought programmatically via `POST /api/payments/buy/` (HTTP 402 / IETF MPP) for autonomous agents

## Data model

### Publication object

```json
{
  "slug": "doomberg",
  "name": "Doomberg",
  "platform": "substack",
  "subscribers": 125000,
  "active": true,
  "topics": ["finance", "energy", "commodities"],
  "url": "https://doomberg.substack.com",
  "description": "...",
  "engagement_metrics": {
    "open_rate_estimate": 0.45,
    "frequency": "weekly"
  }
}
```
<!-- Constructed from docs — verify against live API -->

### Contact object

```json
{
  "publication_slug": "doomberg",
  "email": "hello@doomberg.com",
  "social": {
    "twitter": "@DoombergT",
    "linkedin": "..."
  }
}
```
<!-- Constructed from docs — verify against live API -->

### Search result

```json
{
  "results": [
    {
      "id": "doomberg",
      "name": "...",
      "subscribers": 50000,
      "topics": ["..."]
    }
  ],
  "page": 1,
  "per_page": 25,
  "count": 1247,
  "more": true
}
```
<!-- Pagination fields (page, per_page, count, more) verified 2026-06-13 against /llms-full.txt. Default per_page=25, max 100. Publications keyed by slug in the `id` field. -->

## Quick-start recipes

### Recipe 1: Find and contact newsletters in a niche

**Use case**: You want to sponsor AI newsletters with 10K+ subscribers.

**Python**:
```python
from reletter import Reletter

client = Reletter()  # Uses RELETTER_API_KEY env var

# Search for AI newsletters with 10K+ subscribers
results = client.search.publications(
    query="artificial intelligence",
    filters={"subscribers": {"gte": 10000}, "active": True}
)

for pub in results:
    print(f"{pub.name} — {pub.subscribers} subscribers")

    # Pull contact info
    contact = client.contacts.get(pub.slug)
    if contact.email:
        print(f"  Contact: {contact.email}")
```

**cURL**:
```bash
export RELETTER_API_KEY="your_key"

# Search publications (filters DSL: name:operator:value, comma-separated)
curl -H "x-reletter-api-key: $RELETTER_API_KEY" \
  "https://api.reletter.com/api/search/publications/?query=artificial+intelligence&filters=subscribers:gte:10000,active:is:true"

# Get contacts for a specific publication (by slug)
curl -H "x-reletter-api-key: $RELETTER_API_KEY" \
  "https://api.reletter.com/api/contacts/?publication_id=doomberg"
```
<!-- Base URL, x-reletter-api-key header, /api/... paths, and filters DSL verified 2026-06-13 against reletter.com/developers + /llms-full.txt -->

**Gotcha**: API is $59/mo add-on. Make sure it's enabled before running API calls.

### Recipe 2: Bulk export newsletter list for sponsorship outreach

**Use case**: Build a target list of 50+ fintech newsletters and export with contacts.

**Python**:
```python
from reletter import Reletter

client = Reletter()

# Use auto-pagination to get all results
newsletters = []
for pub in client.search.iter_publications(
    query="fintech",
    filters={"subscribers": {"gte": 5000}, "active": True}
):
    contact = client.contacts.get(pub.slug)
    newsletters.append({
        "name": pub.name,
        "subscribers": pub.subscribers,
        "url": pub.url,
        "email": contact.email if contact else None
    })
    if len(newsletters) >= 50:
        break

# Export to CSV
import csv
with open("fintech_newsletters.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "subscribers", "url", "email"])
    writer.writeheader()
    writer.writerows(newsletters)

print(f"Exported {len(newsletters)} newsletters")
```

**Gotcha**: `iter_publications()` handles pagination automatically. Watch your API quota — each page is one request.

### Recipe 3: Monitor brand mentions via CLI

**Use case**: Check which newsletters mentioned your brand this week.

**CLI**:
```bash
# Install CLI
pip install reletter

# Search newsletter issues for brand mentions
reletter search issues --query "YourBrandName" --filters '{"date": {"gte": "2026-05-04"}}'

# Look up a specific publication
reletter publications get doomberg

# Check your API quota
reletter account quota
```

**Gotcha**: CLI exit codes: 0 = success, 1 = API error, 2 = usage error, 4 = auth error, 5 = server error.

## Integration patterns

### Sponsorship prospecting pipeline

1. **Search** → Use `search.publications()` with topic + subscriber filters
2. **Qualify** → Check engagement metrics, frequency, and audience alignment
3. **Contact** → Pull creator email via `contacts.get()`
4. **Outreach** → Export to CSV → import into CRM or email tool
5. **Track** → Set up keyword alerts for your brand post-sponsorship

### MCP server setup

Connect Reletter to Claude, ChatGPT, or Cursor via MCP:

```
Server URL: https://mcp.reletter.com
Auth: RELETTER_API_KEY (REST API uses the x-reletter-api-key header, not Bearer)
```

Available through the MCP server: publication search, contact lookup, issue search, and chart data. Set up your API key in the MCP client configuration.

### Python SDK error handling

```python
from reletter import Reletter
from reletter.exceptions import AuthenticationError, RateLimitError, BadRequestError

client = Reletter()

try:
    results = client.search.publications(query="AI")
except AuthenticationError:
    print("Check your RELETTER_API_KEY")
except RateLimitError:
    print("API quota exceeded — wait or upgrade")
except BadRequestError as e:
    print(f"Invalid request: {e}")
```

The SDK retries automatically on 429/5xx responses (default 2 retries with exponential backoff).
