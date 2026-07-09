# MentionDrop Platform Reference

## Overview

MentionDrop monitors web mentions (via Ahrefs Firehose) and Reddit discussions for brands, delivering AI-powered summaries with sentiment analysis and suggested actions. Positioned as a budget Google Alerts replacement for indie founders, freelancers, and small teams at $29/mo (vs enterprise tools at $99-599+/mo). Built with Next.js, Supabase, and Gemini Flash-Lite.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| **Keyword monitoring** | Track brand, product, and competitor keywords across web and Reddit | UI **and API** (list/create/update via `/keywords`) |
| **AI summaries** | Gemini Flash-Lite summarizes each mention with context | Automatic on all mentions |
| **Sentiment analysis** | Positive/neutral/negative classification per mention | API-accessible (filter param) |
| **Relevance scoring** | AI scores each mention for relevance to your keyword context | API-accessible (in response) |
| **Suggested actions** | Respond, share, monitor, or ignore — AI-generated per mention | API-accessible (in response) |
| **Relevance feedback** | Mark a mention relevant / not-relevant to tune the model | API (`PATCH /mentions/{id}`) and UI |
| **Reply drafts** | AI-generated reply or outreach-email draft for a mention | API (`POST /reply-drafts`) and UI |
| **Digest** | Grouped view: owned-brand / competitor / demand / reply-worthy | API (`GET /digest`) and UI |
| **Real-time dashboard** | Live-streaming mention feed via Supabase real-time | UI-only |
| **Email alerts** | New mention notifications to inbox | UI — configure in settings |
| **Slack alerts** | New mention notifications to Slack channel | UI — configure in settings |
| **Webhook alerts** | HTTP POST to custom endpoint on new mentions | UI — configure in settings |
| **Mentions API** | List/get processed mentions, save feedback | API-accessible (read + feedback write) |

## Pricing, limits & plan gates

As of 2026-06-13 the public `/pricing` page brands the two paid tiers **Monitor** and **Radar** (previously "Starter" / "Pro"). Both list the same feature set; they differ on keyword count and history retention. The page shows only these two paid tiers (no Free plan listed on `/pricing`), though the API `/me` plan enum still includes a `free` code and some third-party listings still describe a free tier with 1 keyword / 7-day history — treat Free as unverified.

| Feature | Monitor ($29/mo) | Radar ($59/mo) — Most Popular |
|---|---|---|
| Keywords | 5 | 20 |
| Mention history | 30 days | 90 days |
| AI summaries + sentiment | Yes | Yes |
| Competitor share-of-voice | Yes | Yes |
| Reply drafts | Yes | Yes |
| Slack + email alerts | Yes | Yes |
| Webhook delivery | Yes | Yes |
| Noise filters | Yes | Yes |
| Money-back guarantee | 14 days (full refund, no questions) | 14 days |

Note: the OpenAPI `/me` plan codes (`free`/`starter`/`pro`) are internal and do not match the public tier names (`Monitor`/`Radar`).

**No annual contracts. Cancel anytime, no contracts.** Monthly billing only via Stripe. No sales calls required.

## Integrations

| Integration | Direction | Details |
|---|---|---|
| **Slack** | MentionDrop → Slack | Push notifications for new mentions |
| **Webhooks** | MentionDrop → Your endpoint | HTTP POST on new mentions |
| **Email** | MentionDrop → Inbox | Digest or real-time email alerts |
| **API** | Both directions | Read mentions/keywords/digest; write keyword create/update, mention feedback, reply drafts |

**No native Zapier/Make apps.** Use webhooks to trigger Zapier Webhooks or Make HTTP modules.

**No MCP server.** For AI agent integration, use the REST API directly.

## Data model

### Mention object

Per the OpenAPI spec. The keyword is embedded under `keywords` (not a flat `keyword_id`); timestamps are `matched_at`; `content_type` is a query filter, not a response field.

```json
{
  "id": "uuid",
  "url": "https://reddit.com/r/SaaS/comments/...",
  "title": "Looking for a project management tool",
  "summary": "User is asking for recommendations for lightweight PM tools for a 5-person remote team. Mentions frustration with Asana's complexity.",
  "sentiment": "negative",
  "relevance_score": 0.87,
  "suggested_action": "respond",
  "source": "reddit",
  "source_domain": "reddit.com",
  "matched_at": "2026-05-06T14:34:12Z",
  "keywords": {
    "id": "uuid",
    "keyword": "TaskFlow",
    "role": "own_brand",
    "context": "TaskFlow is a project management SaaS tool",
    "is_active": true,
    "min_relevance": 60,
    "mention_count_30d": 12
  }
}
```

### Sources

Mentions carry a `source` enum: `firehose`, `reddit`, `brave`, `google_news`, `serper`.

### Content types

Enum values (used as the `content_type` query filter): `article`, `comment`, `job_posting`, `cv`, `course`, `documentation`, `other`

### Keyword object (API-manageable)

Keywords can be listed, created, and updated via the API (`/api/v1/keywords`) as well as the dashboard. Fields:
- **keyword**: The phrase to monitor, 2–100 chars (e.g., "TaskFlow")
- **role**: `own_brand`, `competitor`, or `industry`
- **context**: Description (max 300 chars) to help the AI distinguish ambiguous terms (e.g., "TaskFlow is a project management SaaS tool")
- **is_active**: boolean; **min_relevance**: integer 0–100; plus update-only filters `excluded_content_types` and `exclusion_terms` (max 20)

## Quick-start recipes

### Recipe 1: Fetch negative mentions for triage

**Trigger:** Daily cron job or manual check
**Use case:** Surface negative sentiment mentions for immediate response

```bash
# cURL — fetch negative mentions from the last 24 hours
curl -s "https://www.mentiondrop.com/api/v1/mentions?sentiment=negative&from=$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ)&limit=50" \
  -H "X-API-Key: your_api_key_here" | jq '.mentions[] | {url, title, summary, relevance_score}'
```

```python
import requests
from datetime import datetime, timedelta, timezone

API_KEY = "your_api_key_here"
BASE_URL = "https://www.mentiondrop.com/api/v1/mentions"

yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
resp = requests.get(BASE_URL, headers={"X-API-Key": API_KEY}, params={
    "sentiment": "negative",
    "from": yesterday,
    "limit": 50,
})
resp.raise_for_status()

for mention in resp.json().get("mentions", []):
    print(f"[{mention['sentiment']}] {mention['title']}")
    print(f"  URL: {mention['url']}")
    print(f"  Summary: {mention['summary'][:120]}...")
    print()
```

**Gotchas:** The mention list returns a `pagination` object (`page`/`limit`/`hasNext`/`hasPrev`), not a flat `total`. There's no "handled" flag, but you can record relevance feedback via `PATCH /api/v1/mentions/{id}` (`verdict`: `relevant`/`not_relevant`) to tune the model; track full triage state in your own system.

### Recipe 2: Webhook to Slack via n8n

**Trigger:** MentionDrop webhook fires on new mention
**Use case:** Get rich mention alerts in a Slack channel with sentiment color-coding

1. Create an n8n webhook node — copy the webhook URL
2. In MentionDrop dashboard → Settings → Webhooks → paste the URL
3. Add an n8n Slack node that formats the payload:

```json
{
  "channel": "#brand-mentions",
  "text": "New mention detected",
  "attachments": [{
    "color": "{{ $json.sentiment === 'positive' ? '#36a64f' : $json.sentiment === 'negative' ? '#ff0000' : '#cccccc' }}",
    "title": "{{ $json.title }}",
    "title_link": "{{ $json.url }}",
    "text": "{{ $json.summary }}",
    "fields": [
      {"title": "Sentiment", "value": "{{ $json.sentiment }}", "short": true},
      {"title": "Relevance", "value": "{{ $json.relevance_score }}", "short": true}
    ]
  }]
}
```

**Gotchas:** Webhook payload schema not fully documented — test with webhook.site first to capture the actual structure. The JSON above is based on the data model; field names may differ in the webhook payload.

### Recipe 3: Build a weekly mention report

**Trigger:** Weekly cron (Monday 9 AM)
**Use case:** Generate a summary of the past week's mentions for stakeholders

```python
import requests
from datetime import datetime, timedelta, timezone
from collections import Counter

API_KEY = "your_api_key_here"
BASE_URL = "https://www.mentiondrop.com/api/v1/mentions"

week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
all_mentions = []
page = 1

while True:
    resp = requests.get(BASE_URL, headers={"X-API-Key": API_KEY}, params={
        "from": week_ago, "limit": 100, "page": page,
    })
    resp.raise_for_status()
    data = resp.json()
    mentions = data.get("mentions", [])
    if not mentions:
        break
    all_mentions.extend(mentions)
    page += 1

sentiments = Counter(m["sentiment"] for m in all_mentions)
print(f"Weekly Mention Report ({len(all_mentions)} total)")
print(f"  Positive: {sentiments['positive']}")
print(f"  Neutral: {sentiments['neutral']}")
print(f"  Negative: {sentiments['negative']}")
print(f"\nTop negative mentions:")
for m in sorted(
    [m for m in all_mentions if m["sentiment"] == "negative"],
    key=lambda x: x.get("relevance_score", 0), reverse=True
)[:5]:
    print(f"  - {m['title']} ({m['url']})")
```

**Gotchas:** Pagination returns max 100 per page. If you monitor high-volume keywords, you may need many pages. There's no `total` count in the response — loop while `pagination.hasNext` is true (or until `mentions` is empty / shorter than `limit`).

## Integration patterns

### CRM sync (via webhook + middleware)

MentionDrop has no native CRM connectors. Use webhooks to push to middleware:

1. **MentionDrop → webhook → n8n/Make → CRM**
2. Map mention fields to CRM contact/activity fields
3. Use sentiment as a triage signal — auto-create tasks for negative mentions
4. Use relevance score as a filter — only push mentions above a threshold

### Dashboard pipeline (via API polling)

1. Poll `GET /api/v1/mentions` on a schedule (hourly or daily)
2. Store in your own database (Supabase, PostgreSQL, Google Sheets)
3. Build dashboards in your BI tool of choice
4. Track trends: mention volume, sentiment ratio, top sources

### Webhook listener pattern

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/mentiondrop-webhook", methods=["POST"])
def handle_mention():
    payload = request.json
    # Process the mention — log, notify, create CRM record, etc.
    print(f"New mention: {payload.get('title', 'Unknown')}")
    print(f"Sentiment: {payload.get('sentiment', 'Unknown')}")
    return jsonify({"status": "ok"}), 200
```

**Note:** Webhook payload schema is not fully documented. Log raw payloads initially to understand the structure before building production integrations.
