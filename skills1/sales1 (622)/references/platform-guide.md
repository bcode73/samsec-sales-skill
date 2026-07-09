# Trend Seeker Platform Reference

## Overview

Trend Seeker analyzes 50,000+ Reddit posts and online community discussions to discover and validate business ideas backed by real user demand. It extracts unmet needs ("I wish there was an app that...") and scores them by evidence strength, volume, and validation confidence.

**Primary audience**: Solopreneurs, micro-SaaS builders, and indie hackers looking for validated startup ideas.

**Key differentiator**: Pre-validated idea database with evidence scores from real community conversations, plus a free Idea Validator tool and a public REST API.

## Capabilities & automation surface

| Capability | Description | Surface |
|---|---|---|
| **Idea browsing** | Browse categorized business ideas with evidence scores | UI + API |
| **Idea Validator** | Test your own idea against 50K+ real user requests | UI (free) |
| **Idea search** | Full-text search by default; semantic (embedding) matching gated to Pro via `mode=semantic` | UI + API |
| **Source posts** | View the original Reddit/community posts that support each idea | UI + API |
| **Category filtering** | Filter by vertical: SaaS, mobile, e-commerce, AI/ML, fintech, EdTech, etc. | UI + API |
| **Weekly newsletter** | Curated market intelligence updates with emerging signals | Email |
| **Demand trends** | Interactive charts showing idea demand over time | UI-only |
| **Competition analysis** | Shows existing solutions and market gaps for each idea | UI-only |

## Pricing, limits & plan gates

Trend Seeker uses a freemium model. The Idea Validator tool is free with daily limits. Full idea data requires a Pro subscription.

| Feature | Free | Pro |
|---|---|---|
| Idea browsing | Basic fields only | Full data with scores/metrics |
| `solution_approach` field | Redacted for premium ideas | Full access |
| `why_now` field | Redacted for premium ideas | Full access |
| Idea Validator | Daily validation limits | Unlimited validations |
| AI insights | Basic score only | Detailed strengths, risks, next steps |
| API rate limit | 10 req/min | 120 req/min |
| API max results | 20/page, offset ≤ 100 | 100/page, unlimited offset |

**Pro pricing is not publicly listed** — check trend-seeker.app for current pricing.

**Important**: All pricing is best-effort from research and may change.

## API Reference

<!-- Source: https://trend-seeker.app/docs/api -->

### Base URL

```
https://api.trend-seeker.app/v1
```

### Authentication

Two methods supported:
```
Authorization: Bearer tskr_your_api_key
```
or:
```
X-API-Key: tskr_your_api_key
```

Unauthenticated requests are permitted but receive reduced rate limits and basic field access.

### Rate Limits

| Tier | Requests/Minute | Max Results/Page | Max Offset | Data Access |
|------|-----------------|------------------|------------|-------------|
| Anonymous | 10 | 20 | N/A | Basic fields |
| Free (with key) | 10 | 20 | 100 | Basic fields |
| Pro | 120 | 100 | Unlimited | Full data |

Limits reset on a 60-second rolling window. HTTP 429 returned when exceeded.

The current docs do not document `X-RateLimit-*` response headers, so rely on local rate-tracking and backoff rather than reading headers off the response.

### Endpoints

#### GET /v1/ideas

List business ideas with optional filters, sorted by opportunity score by default.

```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas?limit=10&categories=saas"
```

**Parameters:**
- `limit` — results per page (default 20; max 20 free, max 100 Pro)
- `offset` — pagination offset (max 100 free, unlimited Pro)
- `categories` — comma-separated category filter (e.g. `saas,fintech`)
- `keywords` — comma-separated keyword filter
- `min_validation_score` — minimum validation score, 0.0–1.0
- `created_after` / `created_before` — date filters, `YYYY-MM-DD`
- `sort` — `created_at`, `validation_score`, or default (opportunity score)

**Response fields:**
<!-- Verified against https://trend-seeker.app/docs/api 2026-06-13 -->
```json
{
  "ideas": [
    {
      "id": "abc123",
      "business_idea_id": "abc123",
      "title": "AI-powered invoice reconciliation for freelancers",
      "tagline": "Auto-match receipts to invoices for solo freelancers",
      "evidence_strength": {
        "volume": 0.85,
        "urgency": 0.72,
        "specificity": 0.91
      },
      "market_metrics": {
        "competition_level": "medium",
        "monetization_potential": "high",
        "opportunity_score": 0.88
      },
      "validation_score": 0.78,
      "confidence_tier": "premium",
      "categories": ["fintech", "saas"],
      "post_count": 47,
      "solution_approach": "SaaS tool that...",
      "why_now": "Growing freelance market...",
      "created_at": "2026-04-15T10:30:00Z",
      "updated_at": "2026-04-20T08:00:00Z"
    }
  ],
  "meta": {
    "total": 1250,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

**Notes:**
- `evidence_strength` is an object (`volume`/`urgency`/`specificity`), and `market_metrics` is an object (`competition_level`/`monetization_potential`/`opportunity_score`). `post_count` is a top-level integer. Pagination is in a `meta` object.
- `solution_approach` and `why_now` are redacted for `confidence_tier: "premium"` ideas on the free plan.

#### GET /v1/ideas/search

Full-text search across titles, taglines, and problem descriptions. Semantic (embedding-based) matching is gated to Pro via `mode=semantic`.

```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/search?q=invoice+freelancer&mode=semantic&limit=10"
```

**Parameters:**
- `q` — search query (required)
- `mode` — `text` (default) or `semantic` (Pro only, embedding-based)
- `limit` — results per page
- `offset` — pagination offset
- `categories` — comma-separated category filter
- `min_validation_score` — text mode only

Each result includes a `relevance` score.

#### GET /v1/ideas/:id

Fetch a specific idea by ID.

```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/abc123"
```

#### GET /v1/ideas/:id/posts

Retrieve the original community posts supporting an idea.

**Parameters:**
- `limit` — max posts to return (default 10; max 5 free, max 100 Pro)

```bash
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/abc123/posts?limit=5"
```

<!-- Verified against https://trend-seeker.app/docs/api 2026-06-13 -->
```json
{
  "posts": [
    {
      "id": "xyz789",
      "title": "I wish there was a tool that auto-reconciles invoices",
      "content": "Spent 3 hours this weekend matching receipts to invoices...",
      "platform": "reddit",
      "url": "https://reddit.com/r/freelance/...",
      "created_at": "2026-03-20T15:00:00Z"
    }
  ]
}
```

Post objects expose `id`, `title`, `content`, `platform`, `url`, `created_at`.

#### GET /v1/categories

List all available idea categories with idea counts. Returns an array of `{ "category": "saas", "count": 342 }`.

```bash
curl "https://api.trend-seeker.app/v1/categories"
```

### Pagination

Offset-based pagination:
```
?limit=20&offset=0   # Page 1
?limit=20&offset=20  # Page 2
?limit=20&offset=40  # Page 3
```

Free tier: offset capped at 100 (5 pages of 20). Pro: unlimited.

### Error Handling

HTTP 429 — rate limit exceeded. Implement exponential backoff:

```python
import time
import requests

def fetch_ideas(api_key, params, max_retries=3):
    headers = {"Authorization": f"Bearer {api_key}"}
    for attempt in range(max_retries):
        resp = requests.get(
            "https://api.trend-seeker.app/v1/ideas",
            headers=headers, params=params
        )
        if resp.status_code == 429:
            wait = 2 ** attempt
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise Exception("Rate limit exceeded after retries")
```

## Idea Validator

The free Idea Validator at `trend-seeker.app/idea-validator` tests your concept against the database.

### How it works
1. Enter a business idea description in natural language
2. The system converts it to a semantic embedding
3. Matches against thousands of real user requests from Reddit/communities
4. Returns a validation score (0-100) combining two metrics

### Scoring methodology

| Metric | Range | Measures |
|---|---|---|
| Post Volume | 0-50 | How many users requested something similar |
| Idea Similarity | 0-50 | How closely existing solutions match your concept |

**Interpretation:**
- **High volume + low similarity** = underserved market opportunity (best signal)
- **High volume + high similarity** = competitive market (demand exists but crowded)
- **Low volume + low similarity** = unproven market (risky)
- **Low volume + high similarity** = niche already served (avoid)

### Tips for better scores
- Describe the problem in user language, not product jargon
- Try multiple phrasings — "invoice tool for freelancers" vs "freelancer billing automation"
- Scores above 0.7 with 10+ supporting posts indicate strong demand

## Quick-start recipes

### Recipe 1: Find underserved SaaS ideas via API

**Goal:** Query the API for high-evidence SaaS ideas, filter for underserved markets.

```bash
# Fetch top SaaS ideas sorted by evidence
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas?categories=saas&limit=50"
```

```python
import requests

API_KEY = "tskr_your_key"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Fetch SaaS ideas
resp = requests.get(
    "https://api.trend-seeker.app/v1/ideas",
    headers=headers,
    params={"categories": "saas", "limit": 50}
)
ideas = resp.json()["ideas"]

# Filter for high validation + strong evidence volume (underserved markets)
# evidence_strength is an object {volume, urgency, specificity}; post_count is top-level
strong_ideas = [
    i for i in ideas
    if i["validation_score"] > 0.7 and i["evidence_strength"]["volume"] > 0.6
]

for idea in strong_ideas:
    print(f"{idea['title']} — score: {idea['validation_score']}, "
          f"evidence volume: {idea['evidence_strength']['volume']}, "
          f"opportunity: {idea['market_metrics']['opportunity_score']}, "
          f"posts: {idea['post_count']}")
```

**Gotcha:** Free tier returns basic fields only. `solution_approach` and `why_now` require Pro.

### Recipe 2: Validate your own idea and fetch supporting evidence

**Goal:** Use the Idea Validator, then pull source posts for the closest matching ideas.

1. Go to `trend-seeker.app/idea-validator` and enter your idea
2. Note the top matching ideas and their IDs
3. Fetch source posts via API:

```bash
# Get the original Reddit posts supporting idea abc123
curl -H "Authorization: Bearer tskr_your_key" \
  "https://api.trend-seeker.app/v1/ideas/abc123/posts"
```

```python
# Fetch source posts for an idea
idea_id = "abc123"
resp = requests.get(
    f"https://api.trend-seeker.app/v1/ideas/{idea_id}/posts",
    headers=headers
)
posts = resp.json()["posts"]

# Post objects expose: id, title, content, platform, url, created_at
for post in posts:
    print(f"[{post['platform']}] {post['title']}")
    print(f"  {post['url']}")
    print(f"  {post['content'][:120]}...")
```

**Gotcha:** Source posts link to real Reddit threads — read them to understand context beyond the score.

### Recipe 3: Build a weekly idea digest pipeline

**Goal:** Automatically query new ideas weekly and send to Slack/email.

```python
import requests
from datetime import datetime, timedelta

API_KEY = "tskr_your_key"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Paginate through all ideas, filter by recency
all_ideas = []
offset = 0
while True:
    resp = requests.get(
        "https://api.trend-seeker.app/v1/ideas",
        headers=headers,
        params={"limit": 100, "offset": offset}
    )
    data = resp.json()
    ideas = data["ideas"]
    if not ideas:
        break
    all_ideas.extend(ideas)
    offset += len(ideas)
    # Pagination metadata lives in the meta object
    if not data["meta"].get("has_more") or offset >= data["meta"]["total"]:
        break

# Filter for ideas created in the last 7 days with strong signals
cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
new_ideas = [
    i for i in all_ideas
    if i.get("created_at", "") >= cutoff
    and i["validation_score"] > 0.6
]

# Format for Slack/email
for idea in new_ideas:
    print(f"*{idea['title']}* — score {idea['validation_score']}")
```

**Gotcha:** Requires Pro plan for unlimited offset. Free tier caps at offset 100 (max ~120 ideas visible).

## Comparison with similar tools

| Feature | Trend Seeker | PainOnSocial | Reddinbox | Reddily |
|---|---|---|---|---|
| **Focus** | Pre-validated idea database | Pain point scoring | Audience intelligence | Thread analysis |
| **Input** | Browse/search/validate | Choose subreddits | Natural language queries | Individual threads |
| **Output** | Ideas with evidence scores | Pain points ranked by frequency/severity | Market briefs, intent scoring | Sentiment, pain points, demographics |
| **API** | Yes (REST, 5 endpoints) | No | No | No |
| **Pricing** | Freemium (Pro price unlisted) | $19-49/mo | $39/mo | Pay-per-analysis ($0.24-0.30) |
| **Monitoring** | No (database, not real-time) | No (on-demand scans) | Yes (always-on feed) | No (on-demand analysis) |
| **Best for** | Finding ideas you haven't thought of yet | Quantifying pain in a niche you've chosen | Ongoing demand research | Deep single-thread insight extraction |
