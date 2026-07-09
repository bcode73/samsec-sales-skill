# CommunityTracker Platform Reference

## Overview

CommunityTracker is a community intelligence platform built for GTM teams — sales, marketing, founders, and product. It monitors public communities (Reddit, Slack, Discord, LinkedIn, X, GitHub, Product Hunt, Stack Overflow, Indie Hackers, Dev.to, Hacker News, and niche forums) for high-intent buyer signals, scores them by commercial relevance, and delivers them through a unified inbox with AI summaries and recommended next steps. Differentiator vs general social listening tools: focuses specifically on community discussions where product research and buying decisions happen, not news/media monitoring.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| **Keyword monitoring** | Track keywords across community platforms with intent filtering | All plans (3-20 keywords by tier) |
| **Signal detection** | AI surfaces buyer research, solution comparisons, pain-point discussions | All plans |
| **Intent scoring** | Filters commercially relevant conversations (high/medium priority) | All plans |
| **Competitor tracking** | Monitor competitor mentions and share of voice across communities | All plans |
| **Unified inbox** | Aggregate signals from multiple platforms in one dashboard | All plans |
| **AI summaries** | Context on why signals matter + recommended next steps | All plans |
| **Team workflows** | Signal assignment, notes, collaboration | Pro+ |
| **Content generation** | AI-crafted social posts from trending discussions (`/generate` endpoint) | Pro+ (API-accessible) |
| **Slack integration** | Real-time signal alerts to Slack channels | Pro+ |
| **Email alerts** | Daily digest or real-time notifications | All plans (daily on Starter, real-time on Pro+) |
| **Webhooks** | JSON POST to custom URL on each signal (marketing page; not in technical API docs) | Pro+ (webhook-accessible) |
| **REST API** | `X-API-Key` auth; GET `/api-posts` (AI-scored posts) + GET `/api-intelligence` (Share of Voice); 5,000 req/day | Pro+ |
| **Task management** | Route signals as tasks to ClickUp, Notion, Trello, Linear | Pro+ |
| **Warm outreach** | LinkedIn and email integration for personalized follow-up | Pro+ |
| **CSV export** | Export signal lists | Pro+ |

## Pricing, limits & plan gates

*Verified 2026-06-13 against https://www.communitytracker.ai/pricing — four tiers (Free / Starter / Pro / Advanced).*

| Feature | Free $0/mo | Starter $39/mo | Pro $99/mo | Advanced $199/mo |
|---|---|---|---|---|
| Keywords | 1 | 4 | 10 | 20 |
| Community platforms | Reddit only | Reddit, LinkedIn, HN, GitHub | All communities | All communities |
| Alert frequency | Daily | Daily | Daily Slack alerts | Daily Slack alerts |
| Mentions | Basic analytics | 5,000 mentions | Unlimited | Unlimited |
| Warm emails | — | Up to 100/mo | Unlimited | Unlimited |
| Response/AI generator | — | Response Generator | AI Response Generator | AI Response Generator |
| AI scoring | — | Signal detection | Yes | Yes |
| Share of Voice | No | No | Yes | Yes + SoV Exporter |
| Advanced AI filtering | No | No | Yes | Yes |
| Community AI / intelligence | No | No | Community AI | Community Intelligence + AI Visibility |
| REST API | No | No | Yes | Yes |
| Webhooks | No | No | Yes | Yes |

**Plan gate warning:** API access requires **Pro ($99/mo) or higher** — trial/no-API plans get a `403 PLAN_NO_API_ACCESS` error. Free and Starter are monitoring + daily alerts only.

**Pricing changes (2026-06-13):** A **Free tier ($0, 1 keyword, Reddit only)** now exists. **Starter rose from $29 to $39** and now includes **4 keywords** (was 3) plus 5,000 mentions and up to 100 warm emails/month. Pro and Advanced prices unchanged at $99 and $199. Note the official pricing page lists alert frequency as "Daily Slack alerts" on Pro/Advanced (not explicitly "real-time"); older copy described Pro+ as real-time — verify in-dashboard.

**Pricing note:** Some blog/comparison copy still shows the older $29 Starter / 3-keyword figures; the live pricing page is authoritative.

## Integrations

- **Notifications**: Email (all plans), Slack (Pro+)
- **Webhooks**: JSON POST to any endpoint on each signal (Pro+)
- **Task management**: ClickUp, Notion, Trello, Linear (Pro+)
- **Outreach**: LinkedIn and email integration (Pro+)
- **Automation**: n8n, Make.com, Zapier (via webhooks, Pro+)
- **REST API**: `X-API-Key` auth; GET `/api-posts` (AI-scored community posts) and GET `/api-intelligence` (Share of Voice). Pro+ only (`403 PLAN_NO_API_ACCESS` otherwise). 5,000 req/day.
- **No native Zapier app.** The `/api-integration` page positions n8n / Make.com / Zapier as the workflow targets (via API/webhooks).

Data flow: CommunityTracker monitors communities → scores signals by intent → pushes qualified signals out via email/Slack/webhooks/API.

## Data model

### Post object (from GET /api-posts) — verified 2026-06-13

```json
{
  "url": "https://reddit.com/r/devops/comments/abc123",
  "title": "Looking for a better CI/CD pipeline tool",
  "body": "We've been using Jenkins but it's too complex for our small team...",
  "author": "some_user",
  "source": "reddit",
  "kind": "post",
  "posted_at": "2026-06-01T14:30:00Z",
  "ai_score": 9,
  "ai_reason": "Explicitly evaluating CI/CD tools and naming pain points",
  "intent": "buying",
  "urgency": "high",
  "buying_stage": "evaluation",
  "action_type": "engage",
  "suggested_play": "Share a concise comparison and offer a trial",
  "competitor_named": true,
  "buying_signals": ["evaluating alternatives", "named pain point"],
  "engagement_status": "new",
  "subreddit": "r/devops"
}
```

**Key fields:**
- `ai_score` (1–10): AI relevance/intent score. Filter with `min_score`.
- `intent`: one of `buying`, `pain_point`, `question`, `comparison`. Filter with `intent`.
- `source`: which community the signal came from. Filter with `source`.
- `subreddit`: Reddit-only community identifier.
- `ai_reason`, `suggested_play`, `buying_signals`: AI-generated context and recommended next move.

> Older `/v1/mentions`-style fields (`id`, `platform`, `intent_score` 0–100, `sentiment`, `created_at`) are deprecated. The current technical API uses the field names above. Webhook payloads (Pro+, marketing page) are not officially documented — verify the live shape with webhook.site.

### Pagination

`/api-posts` uses `limit` (default 50, max 100) and `offset`. `/api-intelligence` uses `limit` (default 30) plus optional `date` or `from`/`to`.

## Quick-start recipes

### Recipe 1: Monitor competitor mentions and push to Slack (cURL)

```bash
# Fetch high-intent competitor posts (X-API-Key auth, /api-posts endpoint)
curl -H "X-API-Key: ct_live_your_key_here" \
  "https://api.communitytracker.ai/api-posts?keyword=competitor-name&min_score=7&intent=buying&limit=20"
```

```python
# Poll CommunityTracker API and post high-intent signals to Slack
import requests

CT_API_KEY = "ct_live_your_key_here"
SLACK_WEBHOOK = "https://hooks.slack.com/services/T.../B.../xxx"

response = requests.get(
    "https://api.communitytracker.ai/api-posts",
    params={"keyword": "competitor-name", "min_score": 7, "limit": 50},
    headers={"X-API-Key": CT_API_KEY}
)

for post in response.json().get("data", []):
    if post.get("ai_score", 0) >= 7:
        requests.post(SLACK_WEBHOOK, json={
            "text": f"*High-intent signal* (score {post['ai_score']}/10, intent: {post.get('intent')})\n"
                    f"Source: {post['source']}\n"
                    f"Title: {post['title']}\n"
                    f"<{post['url']}|View conversation>"
        })
```

**Gotcha:** API requires Pro ($99/mo) or higher — trial/Free/Starter keys get `403 PLAN_NO_API_ACCESS`. Auth is the `X-API-Key` header (NOT `Authorization: Bearer`). Inspect the actual response envelope (`data` vs top-level array) against the live API.

### Recipe 2: Pull Share of Voice snapshots (cURL)

```bash
# 1. Discover your active query IDs (call with no query_id → 400 lists them)
curl -H "X-API-Key: ct_live_your_key_here" \
  "https://api.communitytracker.ai/api-intelligence"

# 2. Fetch the latest Share of Voice snapshot for a query
curl -H "X-API-Key: ct_live_your_key_here" \
  "https://api.communitytracker.ai/api-intelligence?query_id=YOUR_QUERY_UUID"

# 3. Fetch a date range of snapshots
curl -H "X-API-Key: ct_live_your_key_here" \
  "https://api.communitytracker.ai/api-intelligence?query_id=YOUR_QUERY_UUID&from=2026-05-01&to=2026-06-01&limit=30"
```

**Use case:** Track brand-vs-competitor mention share over time and export trend data into a dashboard or warehouse.

### Recipe 2b: AI content generation (marketing-page feature)

The `/api-integration` marketing page references a `/generate` endpoint for AI-crafted LinkedIn posts, newsletters, and Twitter threads fed into n8n/Make/Zapier. This endpoint is **not** listed on the technical `/api-documentation` page (which documents only `/api-posts` and `/api-intelligence`). Confirm the exact path, method, and auth against the live API before building on it.

### Recipe 3: Webhook → n8n → CRM pipeline

1. Set up a webhook URL in CommunityTracker pointing to your n8n webhook trigger
2. n8n receives the signal JSON payload on each qualified mention
3. Filter node: `ai_score >= 7` AND `intent == "buying"` (or `source` in reddit/linkedin)
4. Map fields to CRM contact: `author`, `source`, `url`, `ai_score`, `intent`, `suggested_play`
5. Create/update contact in HubSpot/Salesforce with signal context in notes
6. Optional: send Slack notification to sales team for immediate engagement

**Gotcha:** Webhook payload schema is not publicly documented. Test with webhook.site first to inspect the actual payload format.

## Integration patterns

### Webhook listener

CommunityTracker pushes JSON POST to your endpoint on each qualified signal. Set up the webhook URL in your dashboard settings.

**Expected payload structure** (NOT officially documented — the technical API docs do not describe webhook payloads or signing; verify against the actual webhook with webhook.site). It likely mirrors the `/api-posts` post object:

```json
{
  "url": "https://...",
  "title": "Looking for a tool...",
  "body": "...",
  "source": "reddit",
  "ai_score": 9,
  "intent": "buying",
  "posted_at": "2026-06-01T14:30:00Z"
}
```
<!-- Webhook payload undocumented — verify against live webhook -->

**Retry behavior / signing:** Not documented. Implement idempotency on your endpoint (dedupe on `url`).

### Rate limit handling

- Single daily allowance: **5,000 requests/day** with an hourly reset (per the technical API docs).
- Every response carries `X-RateLimit-Limit` (5000), `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.
- When the limit is reached, the API returns HTTP 429 with error code `RATE_LIMIT_EXCEEDED`.

> The marketing `/api-integration` page describes a per-plan model (Pro 1,000/day, Advanced 5,000/day). At runtime trust the `X-RateLimit-*` response headers over either static figure.

**Backoff strategy:**
1. Read `X-RateLimit-Remaining`; throttle as it approaches 0.
2. On `429` (`RATE_LIMIT_EXCEEDED`), wait until `X-RateLimit-Reset`, then retry.
3. Prefer larger `limit` (max 100 on `/api-posts`) to cut call count, and cache results locally.
