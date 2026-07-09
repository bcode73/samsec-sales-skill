# Octolens Platform Reference

## Overview

Developer-first social listening platform that monitors brand mentions across 13+ platforms (Reddit, GitHub, Hacker News, X, LinkedIn, Bluesky, Stack Overflow, DEV.to, podcasts, newsletters, YouTube, TikTok, news). Primary differentiator: MCP server for AI tools + focus on developer/SaaS-relevant platforms that general listening tools ignore (GitHub, HN, Stack Overflow, DEV.to).

## Capabilities & automation surface

| Module | What it does | Access |
|---|---|---|
| Keyword monitoring | Tracks mentions across all platforms with configurable refresh | UI + API (GET /keywords; full CRUD in v2) |
| AI relevance scoring | Auto-tags mentions (own_brand / competitor / industry_term tags + relevance) | API-accessible (in mention response) |
| Sentiment analysis | Classifies positive/negative/neutral | API-accessible (in mention response) |
| Feeds (filtered views) | Saved filter combinations for segmented monitoring | API-accessible (GET /feeds; CRUD in v2). Pass feed id as `view` on /mentions |
| Alerts | Email, Slack, webhook push on new mentions (per-feed) | Webhook-accessible |
| Weekly AI summaries | AI-generated intelligence digest | UI-only (Scale+ plans) |
| Conversation Rank | Reddit-specific thread ranking | UI-only |
| Analytics & trends | Volume, sentiment, source breakdown over time | API (GET /analytics/*) or CSV export |
| MCP server | Natural language queries from AI tools | MCP v2 (HTTP transport, OAuth); v1 legacy (SSE, token) |

## Pricing, limits & plan gates

| Feature | Pro ($119/mo) | Scale ($319/mo) | Enterprise (custom) |
|---|---|---|---|
| Mentions/mo | 15,000 | 50,000 | Unlimited |
| Keywords | 10 | 15 | Unlimited |
| Refresh rate | Hourly | Real-time | Real-time |
| Data history | 2 years | Unlimited | Unlimited |
| Sources | Social + communities | + podcasts, media, newsletters | + custom |
| AI summaries | No | Weekly | Custom |
| API/webhooks/MCP | Yes | Yes | Yes |
| Workspaces | 1 | 1 | Multiple |

**Add-ons:** Extra mentions from $0.007/mention. Additional keywords $5-10/mo each.

**Free trial:** 7 days, Pro features, 1K mention cap. No credit card required.

**Annual discount:** 20% off (Pro ~$95/mo, Scale ~$255/mo).

**Overage behavior:** Mentions stop being tracked when quota hits limit — no automatic overage charges. You can purchase add-on mention packs.

## Integrations

| Integration | Direction | Notes |
|---|---|---|
| Slack | Octolens → Slack | Alert delivery, channel routing |
| Email | Octolens → Email | Digest and alert delivery |
| Webhooks | Octolens → Your endpoint | Real-time mention push (HTTPS required) |
| MCP (Claude, Cursor, Windsurf) | Bidirectional | Query mentions via natural language |
| Zapier | Octolens → Any | Trigger on new mentions |
| Make | Octolens → Any | Trigger on new mentions |
| n8n | Octolens → Any | Trigger on new mentions |
| Clay | Octolens → Clay | Webhook integration for lead enrichment |
| CSV export | Octolens → File | Manual bulk export |

No native CRM connectors — use webhooks or Zapier/Make to push to HubSpot, Salesforce, Attio, etc.

## Data model

### Mention object (v2)

camelCase fields; `id` and `keywordId` are integers.

```json
{
  "id": 123,
  "sourceId": "111111111",
  "url": "https://reddit.com/r/SaaS/comments/abc123",
  "title": "...",
  "body": "Has anyone tried Octolens for tracking GitHub mentions? Way better than...",
  "source": "reddit",
  "timestamp": "2026-05-04T14:32:00.000Z",
  "author": "username",
  "authorName": "Display Name",
  "authorAvatar": "https://...",
  "authorUrl": "https://reddit.com/u/username",
  "authorFollowers": 1250,
  "relevance": "high",
  "relevanceComment": "...",
  "sentiment": "positive",
  "language": "en",
  "tags": ["Own Brand Mention"],
  "keywords": ["octolens"],
  "engaged": false,
  "relevanceScore": "high",
  "imageUrl": null,
  "keywordId": 42
}
```

### Keyword object (v2)

```json
{
  "id": 42,
  "keyword": "octolens",
  "context": "social listening tool for developers",
  "additionalTerms": null,
  "additionalTermsAndOr": false,
  "caseSensitive": false,
  "symbolSensitive": false,
  "platforms": ["reddit", "twitter", "github", "hackernews", "linkedin"],
  "excludeWords": null,
  "excludeAuthors": null,
  "tag": "own_brand",
  "paused": false
}
```

`tag` enum: `own_brand`, `competitor`, `industry_term`, or null.

### Feed (saved view) object

Feeds are the v2 replacement for "views". Manage via `GET/POST/PUT/DELETE /feeds`; reference a
feed in mention queries by passing its integer id as the `view` parameter.

## Quick-start recipes

### Recipe 1: List all mentions via API (Python)

**Use case:** Pull recent mentions into a custom dashboard or spreadsheet.

```bash
curl -X POST https://app.octolens.com/api/v2/mentions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50}'
```

```python
import requests

API_KEY = "your_api_key"
BASE_URL = "https://app.octolens.com/api/v2"

def get_mentions(limit=50, cursor=None, view_id=None):
    payload = {"limit": limit}
    if cursor:
        payload["cursor"] = cursor
    if view_id:
        payload["view"] = view_id  # integer feed/view id

    resp = requests.post(
        f"{BASE_URL}/mentions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=payload
    )
    resp.raise_for_status()
    return resp.json()

# Get first page
data = get_mentions(limit=100)
mentions = data["data"]
next_cursor = data["pagination"]["nextCursor"]

# Paginate
while next_cursor:
    data = get_mentions(limit=100, cursor=next_cursor)
    mentions.extend(data["data"])
    next_cursor = data["pagination"]["nextCursor"]
```

**Gotchas:** POST not GET for mentions endpoint. Response is `{data, pagination.nextCursor}` (not
`{mentions, cursor}`). Max 100 per page. Cursor is opaque — don't construct it manually. To dump
a large date range in one call, use `POST /mentions/export` (up to 50K, JSON or CSV) instead of
paginating.

### Recipe 2: Set up MCP for Claude Code

**Use case:** Query Octolens mentions directly from your terminal via Claude Code.

**MCP v2 (current — OAuth, HTTP transport):**

```bash
# No token to paste — v2 signs in via OAuth in the browser on first use.
claude mcp add --transport http octolens \
  "https://app.octolens.com/api/mcp/v2"

# Restart Claude Code, then test:
# @octolens list my keywords
# @octolens show mentions from Reddit in the last 24 hours
# @octolens find buy-intent mentions this week
```

**For team sharing via `.mcp.json` (v2):**

```json
{
  "mcpServers": {
    "octolens": {
      "type": "http",
      "url": "https://app.octolens.com/api/mcp/v2"
    }
  }
}
```

**MCP v1 (legacy — token in URL, SSE):** still works for existing connections but receives no new
features. `claude mcp add octolens --transport sse "https://app.octolens.com/api/mcp?token=YOUR_API_KEY"`.

**Gotchas:** Prefer v2 (OAuth + feeds/analytics/management tools). v2 needs no pasted key — each
user authenticates via OAuth, so there's no shared token to commit. Generate setup snippets under
Settings → MCP. Restart the tool completely after a config change.

### Recipe 3: Webhook to Slack (high-intent mentions only)

**Use case:** Push only buy-intent or product-question mentions to a Slack channel.

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

@app.route("/octolens-webhook", methods=["POST"])
def handle_mention():
    payload = request.json
    # Webhook wraps the mention in {action, data}; one mention per request.
    if payload.get("action") != "mention_created":
        return jsonify({"status": "ignored"}), 200
    mention = payload["data"]

    # Filter: only forward high-relevance, brand/competitor tagged mentions
    tags = mention.get("tags", [])
    if mention.get("relevanceScore") != "high":
        return jsonify({"status": "skipped"}), 200

    src = (mention.get("source") or "").title()
    # Format Slack message
    slack_msg = {
        "text": f"*{src}* mention ({', '.join(tags)}):\n"
                f">{mention.get('body', '')[:200]}\n"
                f"<{mention['url']}|View on {src}>"
    }

    requests.post(SLACK_WEBHOOK, json=slack_msg)
    return jsonify({"status": "forwarded"}), 200

if __name__ == "__main__":
    app.run(port=5000)
```

**Gotchas:** Webhooks are configured **per feed** with a frequency (Instantly / Hourly / Daily /
Weekly), not globally. Payload is `{ "action": "mention_created", "data": {...} }` — read fields
off `data` (camelCase: `body`, `relevanceScore`, `authorName`). No signing — protect with a secret
URL. Endpoint must be HTTPS and publicly reachable. Test with ngrok during development.

## Integration patterns

### Webhook listener pattern

1. Deploy HTTPS endpoint (Cloudflare Worker, Railway, or similar)
2. Set up the webhook on a **feed** (Set up alert → Webhook → URL → frequency)
3. Mentions arrive as POST with JSON body `{ "action": "mention_created", "data": {...} }` — one mention per request
4. Return any 2xx quickly — process asynchronously if doing heavy work
5. No signature verification — validate via a secret/unguessable URL path or query param

### CRM sync via Zapier/Make

1. Trigger: "New Mention" in Octolens
2. Filter: `tags` contains "Own Brand Mention"/"Competitor"/etc., or `relevanceScore` == "high"
3. Action: Create contact/note in HubSpot/Attio/Pipedrive (native Attio integration also exists)
4. Map: `data.authorName` → contact name, `data.body` → note body, `data.url` → source link

### Batch export pattern

For one-shot date-range dumps, prefer `POST /mentions/export` (up to 50K, JSON or CSV) over
paginating `POST /mentions`. To paginate manually:

```python
# Paginate all mentions (date filters go inside the v2 `filters` object)
import time

all_mentions = []
cursor = None

while True:
    payload = {
        "limit": 100,
        # Date/source/sentiment filters live under `filters` in v2.
        # Generate a filter object from natural language via POST /ai/filter-wizard.
    }
    if cursor:
        payload["cursor"] = cursor

    resp = requests.post(f"{BASE_URL}/mentions",   # BASE_URL ends in /api/v2
                         headers={"Authorization": f"Bearer {API_KEY}"},
                         json=payload)

    if resp.status_code == 429:
        # Rate limited — honor Retry-After (seconds)
        time.sleep(int(resp.headers.get("Retry-After", 60)))
        continue

    data = resp.json()
    all_mentions.extend(data["data"])
    cursor = data["pagination"]["nextCursor"]

    if not cursor:
        break

print(f"Exported {len(all_mentions)} mentions")
```

### Rate limit handling

- 500 requests/hour per organization (counted across all keys)
- Check `X-RateLimit-Remaining`; `X-RateLimit-Reset` is a Unix timestamp for the window reset
- On 429: a `Retry-After` header tells you how long to back off
- For batch operations: add a small delay between requests to stay well under the limit
