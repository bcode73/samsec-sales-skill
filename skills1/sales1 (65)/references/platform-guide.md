# BrandMentions Platform Reference

## Overview

BrandMentions is a social listening and brand monitoring platform that tracks online mentions across web and social media in real time. Differentiator: emotion AI sentiment analysis that breaks reactions into categories (admiration, frustration, sarcasm, joy) beyond basic positive/negative/neutral. Targets SMBs and agencies that need affordable monitoring with competitor intelligence.

## Capabilities & automation surface

| Capability | Description | Automation |
|---|---|---|
| **Brand monitoring** | Track mentions across web, social, news, blogs, forums, reviews. 9.4B+ mentions analyzed. Sources: Facebook, X, Instagram, LinkedIn, Reddit, YouTube, TikTok, Bluesky | API-accessible (Expert+ plans) |
| **Sentiment analysis** | Emotion AI with categories (admiration, frustration, sarcasm, joy). Basic AI on Starter, advanced multilingual on Pro+ | API-accessible (Expert+ plans) |
| **Competitor intelligence** | Side-by-side competitor tracking, Share of Voice analysis | API-accessible (Expert+ plans) |
| **Real-time alerts** | Email notifications for new mentions and links. Volume spike detection | UI-only (email delivery) |
| **White-label reports** | Customizable branded reports without BrandMentions branding | UI-only (Expert+ plans) |
| **Influencer identification** | GetProjectInfluencers endpoint returns top authors/influencers by reach | API-accessible (Expert+ plans) |
| **Historical data** | Backfill searches by month. Starter = 3mo, Pro = 6mo, Expert = 12mo, Enterprise = unlimited | API-accessible (Expert+ plans) |
| **Review monitoring** | AddReviewSourceToProject integrates review platforms | API-accessible (Expert+ plans) |
| **Data export** | CSV export. Starter = 1K rows, Pro = 10K, Expert = 100K, Enterprise = unlimited | UI-only (manual download) |
| **Boolean search** | AND, OR, NOT, exact phrases — Expert+ plans only | API-accessible (Expert+ plans) |

## Pricing, limits & plan gates

| Feature | Starter $99/mo | Pro $299/mo | Expert $499/mo | Enterprise $1,299+/mo |
|---|---|---|---|---|
| **Annual price** | $89/mo | $249/mo | $399/mo | $1,099+/mo |
| **Keywords** | 5 | 20 | 50 | Custom |
| **Mentions/month** | 5,000 | 30,000 | 75,000 | Custom |
| **Users** | 1 | 2 | 10 | Custom |
| **Update frequency** | Daily | Hourly | Real-time | Real-time |
| **Sentiment** | Basic AI | Advanced AI, multilingual | Advanced AI, multilingual | Advanced AI, multilingual |
| **Historical data** | 3 months | 6 months | 12 months | Unlimited |
| **Projects** | 3 | 10 | 50 | Unlimited |
| **Boolean search** | No | No | Yes | Yes |
| **White-label reports** | No | No | Yes | Yes |
| **Data export rows** | 1,000 | 10,000 | 100,000 | Unlimited |
| **API access** | No | No | Yes | Yes |
| **App white-label** | No | No | No | Yes |

**API access starts at Expert ($499/mo)** — confirmed on the live pricing page (the "API & Boolean Search" row is Yes for Expert and Enterprise) and the help center ("API access on the Expert and custom subscription packages"). Contact support to activate the key once your plan includes it. (Re-verified 2026-06-13; was previously documented here as Enterprise-only.)

**7-day free trial** on all plans — no credit card required. Watch for auto-upgrade billing behavior.

**Mention limit is a hard stop** — monitoring pauses when you hit your monthly cap. No degraded mode.

## Integrations

BrandMentions has a limited integration surface:

- **Email alerts**: Real-time mention notifications via email (all plans)
- **CSV export**: Manual data export with row limits per plan
- **REST API**: Expert ($499/mo) and Enterprise — full programmatic access
- **Callbacks (webhooks)**: PostSearch and AddProject accept a `callback` URL that BrandMentions POSTs to on completion (`search_hash` / `project_id` in body). No HMAC signing documented. Available wherever the API is (Expert+).
- **No Zapier/Make**: No iPaaS connectors
- **No MCP server**: No AI assistant integration

For Starter/Pro users (no API), the only data egress path is manual CSV export.

## Data model

### Mention object (from GetProjectMentions / GetMentions)

```json
<!-- Constructed from docs — verify against live API -->
{
  "title": "Blog post mentioning Acme Corp",
  "url": "https://example.com/article",
  "source": "web",
  "date": "2026-05-01T14:30:00Z",
  "sentiment": "positive",
  "emotion": "admiration",
  "reach": 15000,
  "engagement": 42,
  "language": "en",
  "country": "US",
  "author": "john_doe",
  "snippet": "Acme Corp just launched their new product and it looks impressive..."
}
```

### Project object (from ListProjects)

```json
<!-- Constructed from docs — verify against live API -->
{
  "project_id": "abc123",
  "name": "Acme Brand Monitor",
  "keywords": ["Acme Corp", "AcmeCorp", "Acme software"],
  "sources": ["web", "facebook", "twitter", "instagram", "reddit"],
  "language": "en",
  "country": "US",
  "created_at": "2026-01-15T10:00:00Z"
}
```

### Search result (from PostSearch → GetMentions flow)

```json
<!-- search_hash and status are from live docs; mention sub-fields partly reconstructed -->
{
  "search_hash": 3186302626,
  "status": "completed",
  "total_results": 247,
  "mentions": [
    {
      "title": "...",
      "url": "...",
      "source": "twitter",
      "sentiment": "negative",
      "emotion": "frustration",
      "date": "2026-05-01T09:15:00Z"
    }
  ]
}
```

## Quick-start recipes

### Recipe 1: Check remaining API credits

**Trigger**: Before running searches, verify you have credits available.

**cURL:**
```bash
curl "https://api.brandmentions.com/command.php?api_key=YOUR_API_KEY&command=GetRemainingCredits"
```

**Python:**
```python
import requests

API_KEY = "YOUR_API_KEY"
BASE = "https://api.brandmentions.com/command.php"

resp = requests.get(BASE, params={"api_key": API_KEY, "command": "GetRemainingCredits"})
credits = resp.json()
# Response shape: {"PostSearch": 99, "AddProject": 2, "Mentions": 3459}
print(f"Search credits: {credits.get('PostSearch')}")
print(f"Project credits: {credits.get('AddProject')}")
print(f"Mention quota remaining: {credits.get('Mentions')}")
```

**Gotcha**: Each PostSearch costs 1 credit. GetMentions and GetProcessedMentions are free.

### Recipe 2: Run an on-demand search and retrieve results

**Trigger**: Need to search for mentions outside your saved projects.

**cURL (create search):**
```bash
curl -X POST "https://api.brandmentions.com/command.php" \
  -d "api_key=YOUR_API_KEY" \
  -d "command=PostSearch" \
  -d "keyword1=Acme Corp" \
  -d "keyword2=AcmeCorp" \
  -d "match_type1=exact" \
  -d "active_sources[]=web" \
  -d "active_sources[]=twitter"
  # optional: -d "callback=https://your-app.example.com/bm-webhook" to be POSTed the search_hash on completion
```

**Note**: keywords use numbered params (`keyword1`..`keyword5`), match type is per-keyword (`match_type1`, values `exact`/`broad`/`case_sensitive`), and sources use `active_sources[]` array notation — NOT `keywords[0]`/`sources`. Per-keyword `required_keywordsN[]` and `excluded_keywordsN[]` add include/exclude terms for noise reduction.

**cURL (retrieve results — use the search_hash from PostSearch response):**
```bash
curl "https://api.brandmentions.com/command.php?api_key=YOUR_API_KEY&command=GetMentions&search_hash=HASH_FROM_ABOVE"
```

**Python (full flow):**
```python
import requests
import time

API_KEY = "YOUR_API_KEY"
BASE = "https://api.brandmentions.com/command.php"

# Step 1: Create search
search_resp = requests.post(BASE, data={
    "api_key": API_KEY,
    "command": "PostSearch",
    "keyword1": "Acme Corp",
    "keyword2": "AcmeCorp",
    "match_type1": "exact",
    "active_sources[]": ["web", "twitter"]
})
search_hash = search_resp.json().get("search_hash")  # returned as a number

# Step 2: Poll for results (13-second intervals)
while True:
    poll_resp = requests.get(BASE, params={
        "api_key": API_KEY,
        "command": "GetProcessedMentions",
        "search_hash": search_hash
    })
    data = poll_resp.json()
    if data.get("processing_ended"):
        break
    time.sleep(13)

# Step 3: Get complete results
results = requests.get(BASE, params={
    "api_key": API_KEY,
    "command": "GetMentions",
    "search_hash": search_hash
})
mentions = results.json().get("mentions", [])
print(f"Found {len(mentions)} mentions")
```

**Gotchas**:
- Search hash expires after 1 hour (returned as a number, e.g. `3186302626`)
- Up to 5 keywords per search (3-50 chars each), passed as `keyword1`..`keyword5`
- Use GetProcessedMentions with 13-second polling intervals for partial results — or pass a `callback` URL on PostSearch and skip polling (BrandMentions POSTs the `search_hash` when done)

### Recipe 3: List project mentions with pagination

**Trigger**: Export mentions from a saved project for reporting or CRM sync.

**cURL:**
```bash
curl "https://api.brandmentions.com/command.php?api_key=YOUR_API_KEY&command=GetProjectMentions&project_id=PROJECT_ID&page=1&per_page=100"
```

**Python:**
```python
import requests

API_KEY = "YOUR_API_KEY"
BASE = "https://api.brandmentions.com/command.php"

all_mentions = []
page = 1

while True:
    resp = requests.get(BASE, params={
        "api_key": API_KEY,
        "command": "GetProjectMentions",
        "project_id": "PROJECT_ID",
        "page": page,
        "per_page": 100
    })
    data = resp.json()
    mentions = data.get("mentions", [])
    if not mentions:
        break
    all_mentions.extend(mentions)
    page += 1

print(f"Total mentions exported: {len(all_mentions)}")
```

**Gotcha**: Max 100 mentions per page. Use date range filters to reduce result sets.

## Integration patterns

### CRM sync (Expert+ plans)

CRM sync runs over the API (Expert $499/mo and up). Two patterns:

- **Poll**: Run GetProjectMentions on a cron (hourly or daily).
- **Callback-driven**: Pass a `callback` URL on AddProject/PostSearch; BrandMentions POSTs the `project_id`/`search_hash` on completion, then you fetch the mentions. No HMAC signing — re-fetch via the API using the supplied id rather than trusting the POST body.

1. **Fetch**: GetProjectMentions on a cron, or react to the callback POST
2. **Dedup**: Track last-seen mention date/URL to avoid duplicates
3. **Map fields**: mention.url → CRM note URL, mention.sentiment → custom field, mention.author → contact lookup
4. **Error handling**: Check `status` field in every response. Error code 3 = missing API key (auth failure) — retry with a fresh key

### Batch export pattern

1. Use GetProjectMentions with date range filters
2. Paginate through all results (100 per page max)
3. Rate limit: No documented rate limit, but space requests by 1-2 seconds
4. Export to CSV/JSON for BI tools

### No-API workaround (Starter / Pro plans)

For plans without API access (Starter, Pro):
1. Use manual CSV export (limited to plan's row cap)
2. Schedule weekly exports and import into Google Sheets or BI tool
3. Use email alerts as a lightweight trigger (forward to Zapier Email Parser for basic automation)
