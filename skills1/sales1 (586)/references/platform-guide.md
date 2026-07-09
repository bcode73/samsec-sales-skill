# Syften Platform Reference

## Overview

Syften is an AI-filtered keyword monitoring tool for online communities. Built for founders, marketers, and support teams who need to find brand mentions, competitor mentions, and buying-intent conversations as they happen. Primary differentiator: sub-minute Reddit alert latency with AI noise suppression across 15+ community platforms.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| Keyword monitoring | Track mentions across 15+ platforms with Boolean operators | All plans |
| AI filtering | Suppresses spam, duplicates, auto-promos, weak matches | Standard+ (API-accessible) |
| Slack integration | Real-time alerts to Slack channels | Standard+ |
| Email alerts | Daily digest or instant email notifications | All plans |
| RSS feeds | Subscribe to mention streams via RSS reader | All plans |
| Archive search | Search past mentions before alert was created | PRO (unlimited), Standard (limited) |
| Tag routing | `$tag:` operator routes matches to different destinations | All plans |
| REST API | Pull matches programmatically (POST `/items/get`), read AI accept verdict | Standard+ (API-accessible) |
| Webhooks | Push-based delivery of new matches (JSON array of items) | PRO only (webhook-accessible) |
| MCP server | `https://syften.com/mcp` — config inspection, filter health, preview, match retrieval for Claude/Cursor | PRO only |
| Zapier | Token + Zapier setup under Setup → API and Zapier (many users wire via webhook) | Standard+ |
| Author filters | Filter by specific usernames or exclude authors | All plans |
| Site-specific filters | Narrow monitoring to specific platforms/subreddits | All plans |

## Pricing, limits & plan gates

| | Entry | Standard | PRO | Tailor Made |
|---|---|---|---|---|
| **Price** | $19.95/mo | $39.95/mo | $99.95/mo | Contact |
| **Filters** | 3 | 20 | 100 | Custom |
| **Daily results** | 100 | 200 | 500 | Custom |
| **AI filtering** | No | Yes | Yes | Yes |
| **Slack** | No | Yes | Yes | Yes |
| **API** | No | Yes | Yes | Yes |
| **Webhooks** | No | No | Yes | Yes |
| **MCP server** | No | No | Yes | Yes |
| **Archive search** | 7 days | 1 month | Unlimited | Custom |
| **Zapier setup** | No | Yes | Yes | Yes |

- Prices are in USD ($), billed monthly.
- Daily result limits are hard caps — no overage billing, but mentions are missed once exhausted.
- Filter slots are consumed per keyword/source combination.
- **Twitter/X and YouTube monitoring are paid add-ons** on Standard and PRO (not bundled). Exact add-on prices are not published on the pricing page (listed only as "Paid addon").

## Supported platforms

Reddit, Hacker News, Stack Exchange family, GitHub, Indie Hackers, Dev.to, Bluesky, Mastodon, Product Hunt, Steemit, Lobste.rs, Slack communities, Discourse forums, blogs/news (RSS), newsletters/mailing lists, podcasts.

**Pro-tier paid add-ons:** Twitter/X (~15 min delay) and YouTube are paid add-ons, available on Standard and PRO (not bundled into the base plan).

**NOT supported:** LinkedIn, Facebook, Instagram, TikTok.

## Integrations

| Integration | Direction | Details |
|---|---|---|
| Slack | Push (Syften → Slack) | Channel delivery, tag-based routing to different channels |
| Email | Push (Syften → email) | Daily digest, tag-based routing to different addresses |
| RSS | Pull | Tag-based separate feeds |
| REST API | Pull (client → Syften) | POST `/items/get` to query matches; `/filters/get`+`/filters/set` to read/replace filters |
| Webhooks | Push (Syften → endpoint) | PRO only, HTTP POST with a JSON array of item objects on new matches |
| MCP server | Pull (AI tool → Syften) | PRO only, `https://syften.com/mcp` for Claude/Cursor |
| Zapier | Setup → API and Zapier | Token-based; many users route via the webhook (Pro) rather than a native trigger |

No native CRM connectors. CRM sync requires Zapier or API/webhook integration.

## Data model

### Match item (from `POST /api/0.0/items/get`)

Verified against live docs 2026-06-13. Each match has a top-level `matched_on`/`filter` plus a nested `item` object; AI signal lives in `item.analysis`.

```json
{
  "id": "match-id",
  "matched_on": "2026-05-04T12:34:56Z",
  "filter": "example.com",
  "item": {
    "backend": "reddit",
    "backend_sub": "r/startups",
    "type": "comment",
    "icon_url": "https://example.com/icon.png",
    "timestamp": "2026-05-04T12:34:56Z",
    "item_url": "https://example.com/thread",
    "author": "someuser",
    "text": "The matched text",
    "title": "Thread title",
    "title_type": 1,
    "lang": "en",
    "analysis": {
      "lang": "en",
      "sentiment": "neutral",
      "nsfw": false,
      "accept": true,
      "suggested_reply": "A short suggested reply, if available.",
      "score": 8,
      "excerpt": "The part of the item that matched the filter.",
      "rejection_reason": ""
    }
  }
}
```

> The AI accept/reject verdict is `item.analysis.accept` (bool), not `ai_verdict`/`ai_confidence`. The platform/source is `item.backend` (e.g. `reddit`), subreddit/sub is `item.backend_sub`, and the link is `item.item_url`.

### Filters

Filters are stored as a plain JSON array of strings (the filter expressions). `POST /api/0.0/filters/get` returns them; `POST /api/0.0/filters/set` with `{"filters": ["...", "..."]}` REPLACES the whole set. There is no per-filter object with an `id`/CRUD endpoint.

```json
{ "filters": ["\"my-product\" OR \"myproduct\" -\"home automation\"", "$source:reddit \"email automation\""] }
```

## Quick-start recipes

### Recipe 1: Poll for new mentions (cURL + Python)

**Use case:** Pull recent mentions into your internal dashboard or CRM every hour.

**cURL:**
```bash
# Authenticate with API token (Standard+ plan required). All endpoints are POST.
curl -X POST -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 100}' \
  "https://syften.com/api/0.0/items/get"
```

**Python:**
```python
import requests

API_TOKEN = "YOUR_API_TOKEN"
BASE_URL = "https://syften.com/api/0.0"

# Get recent matches (limit default 100, max 500)
resp = requests.post(
    f"{BASE_URL}/items/get",
    headers={
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    },
    json={"limit": 100},
)
matches = resp.json()  # JSON array of match items

for match in matches:
    item = match["item"]
    analysis = item.get("analysis", {})
    if analysis.get("accept"):  # AI-accepted matches only
        print(f"[{item['backend']}] {item.get('title', '')}")
        print(f"  URL: {item['item_url']}")
        print(f"  score: {analysis.get('score')} sentiment: {analysis.get('sentiment')}")
```

**Gotchas:** API is only on Standard+ plans. All endpoints are POST against `https://syften.com/api/0.0`. The AI verdict is `item.analysis.accept` (bool), not `ai_verdict`. Daily result limits still apply. Poll no more frequently than every 5 minutes.

### Recipe 2: Webhook listener (PRO plan)

**Use case:** Get real-time push notifications when mentions arrive, without polling.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/syften-webhook", methods=["POST"])
def handle_matches():
    # The body is a JSON ARRAY of item objects (the inner item shape from items/get)
    items = request.json
    for item in items:
        analysis = item.get("analysis", {})
        if not analysis.get("accept"):
            continue  # skip AI-rejected matches
        if item.get("backend") == "reddit":
            notify_sales_team(item)
        else:
            create_ticket(item)
    return jsonify({"status": "ok"}), 200  # any 2xx acknowledges delivery
```

**Gotchas:** Webhooks are PRO-only ($99.95/mo). The payload is a JSON ARRAY of item objects, not a single `{"event":...,"mention":...}` wrapper. Return any 2xx to ack. Failed deliveries retry for up to 48h (5-minute min backoff, up to 12h between attempts); if the URL is invalid, delivery is skipped. No documented HMAC signature header. For Standard users, route via Zapier (token under Setup → API and Zapier) instead of a webhook.

### Recipe 3: Zapier workflow — mention to Google Sheet

**Use case:** Log all mentions to a spreadsheet for weekly review without code.

1. **Trigger:** Syften match (set up under Setup → API and Zapier; the token-based connection. If no native trigger is offered, point a Syften Pro webhook at a Zapier Catch Hook.)
2. **Filter (optional):** Only continue if the AI verdict (`item.analysis.accept`) is true
3. **Action:** Google Sheets → Create Spreadsheet Row
   - Column A: `{{matched_on}}`
   - Column B: `{{item.backend}}`
   - Column C: `{{item.title}}`
   - Column D: `{{item.item_url}}`
   - Column E: `{{item.analysis.score}}`

**Gotchas:** Zapier setup requires Standard+ plan (the API token). Official docs reference Setup → API and Zapier but do not document a named native trigger, so the most reliable route on Pro is a webhook → Zapier Catch Hook. High-volume keywords may consume Zapier task quota quickly.

## Integration patterns

### CRM sync (via Zapier or API)

- **Field mapping:** `item.item_url` → CRM activity/note, `item.backend` (source) → custom field, `item.analysis.score`/`sentiment` → CRM fields
- **Conflict resolution:** Syften matches are append-only — no bidirectional sync needed
- **Frequency:** Pro webhook fires per match (real-time); API polling (`POST /items/get`) recommended every 15-60 minutes

### Boolean query patterns

```
# Brand monitoring with exclusions
"acme" OR "acme.io" NOT "acme hardware" NOT "roadrunner"

# Competitor tracking
"competitor-name" AND ("review" OR "alternative" OR "vs" OR "comparison")

# Buying intent
("looking for" OR "recommend" OR "anyone tried" OR "best tool for") AND "your-category"

# Specific subreddit + keyword
$source:reddit $subreddit:SaaS "email automation"
```

### Tag-based routing

Use `$tag:` in filter definitions to route different match types:
- `$tag:leads` — buying intent mentions → sales Slack channel
- `$tag:support` — complaint mentions → support email
- `$tag:competitors` — competitor mentions → strategy Slack channel
- `$tag:brand` — direct brand mentions → general channel
