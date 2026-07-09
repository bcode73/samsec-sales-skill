# SnitchFeed Platform Reference

## Overview

SnitchFeed is an intent-based social listening platform for startups and SMBs that monitors Reddit, X/Twitter, LinkedIn, and Bluesky for high-intent buyer signals. Differentiator: keyword-level relevance context ("Define intent in natural language" — plain English intent descriptions per keyword, not just keyword matching) with AI scoring to filter noise. Target audience: GTM teams at startups, solo founders, and lean marketing teams who want to find and engage prospects before competitors.

**Live platforms (verified 2026-06-13):** Reddit and Bluesky refresh in real-time; LinkedIn and X (Twitter) refresh hourly. **Roadmap ("Soon" on homepage):** Hacker News, GitHub, dev.to, YouTube, and Newsletters. Verify current coverage in-dashboard before relying on a platform.

## Capabilities & automation surface

| Module | What it does | Access |
|---|---|---|
| Keyword monitoring | Tracks posts and comments across Reddit, X, LinkedIn, Bluesky | UI — all plans |
| AI relevance scoring | Scores each mention for relevance based on keyword context | UI — all plans |
| AI sentiment scoring + filtering | Classifies mentions as positive/negative | UI — Pro+ only |
| Automated intent tagging | Tags mentions as Buy Intent, Competitor Mention, Customer Testimonial, Promotional Post, Brand Mention, Industry Insights, Hiring, Event; "Filter by tags" control is Pro+ | UI — tagging all plans, tag filtering Pro+ |
| AI language detection | Detects the language of each mention | UI — all plans |
| One-line AI summaries | Generates brief summary per mention | UI — all plans |
| Keyword-level relevance context | Plain English description of what you're looking for, per keyword ("Define intent in natural language") | UI — all plans |
| Upvote/downvote feedback | Trains AI filter accuracy per keyword | UI — all plans |
| Saved views | Per-user dashboard views (Starter 3, Pro 10) | UI — all plans |
| Chat with mentions | Conversational AI over your mention feed | UI — Pro+ only |
| CSV export | Export mentions for offline analysis or enrichment (100 credits/export) | UI — Pro+ only |
| Slack alerts | Real-time, daily, or weekly delivery | Integration — all plans |
| Discord alerts | Real-time, daily, or weekly delivery | Integration — all plans |
| Email alerts | Real-time, daily, or weekly delivery | Integration — all plans |
| Webhook automations | Push mention payloads to external endpoints (Zapier, n8n, etc.) | Integration — Pro+ only |
| API | Listed as "API included" on every plan; API calls consume credits | All plans (see API note below) |
| HubSpot / Instantly / Clay | Homepage: "Plugs into Clay, Instantly, HubSpot, Slack, and more" | Integration — plan/detail unverified |
| Team collaboration | Invite users, shared views | UI — Starter (1 user), Pro (5 users) |

### API note (verified 2026-06-13)
The snitchfeed.com/pricing feature list now shows **"API included"** on all plans, and the credit explainer lists **"API calls"** as a credit-consuming action — so an API exists and is metered. However, **no public developer documentation** (endpoints, auth scheme, rate limits, SDKs) was found on snitchfeed.com as of 2026-06-13. Treat the API surface as undocumented: contact SnitchFeed for API access details; do not assume a queryable REST schema until docs are published. Outbound **webhook automations** (Pro+, "via Zapier, n8n, etc.") remain the documented automation path. No MCP server.

## Pricing, limits & plan gates

*Pricing re-verified against snitchfeed.com/pricing on 2026-06-13. Plans are now metered by a **credit** system rather than a hard "mentions/month" cap.*

| Feature | Starter ($59/mo, $47/mo annual) | Pro ($119/mo, $95/mo annual) | Enterprise ($399+/mo) |
|---|---|---|---|
| **Credits/mo** | 7,000 | 21,000 | Custom |
| **Keywords** | 10 | 30 | Custom |
| **Listeners** | 3 | 10 | Custom |
| **Users** | 1 | 5 | Unlimited |
| **Saved views** | 3 | 10 | Custom |
| **Data retention** | 3 months | 6 months | Unlimited |
| **Platforms** | Reddit, X, LinkedIn, Bluesky | Reddit, X, LinkedIn, Bluesky | All |
| **AI relevance scoring + filtering** | Yes | Yes | Yes |
| **AI sentiment scoring + filtering** | No | Yes | Yes |
| **Filter by tags (intent tag filtering)** | No | Yes | Yes |
| **Slack/Discord/email alerts** | Yes | Yes | Yes |
| **Webhook automations** | No | Yes | Yes |
| **API** | Yes (listed "API included") | Yes | Yes |
| **CSV exports** | No | Yes | Yes |
| **Chat with mentions** | No | Yes | Yes |

### Credit model (verified 2026-06-13, snitchfeed.com/pricing)

"Credits are consumed for certain actions in SnitchFeed like scanning LinkedIn or Twitter, AI scoring mentions, API calls, etc."

| Action | Credit cost |
|---|---|
| X (Twitter) scan | 2 per keyword per scan |
| LinkedIn scan | 4 per keyword per scan |
| AI scoring a mention | 0.2 per mention |
| CSV export | 100 (flat) |
| API calls | Consume credits (rate not quantified on pricing page) |

- **~20% annual discount** (annual prices ~$47/$95 vs monthly $59/$119)
- **7-day free trial with 800 free credits** — no credit card required
- Credits are the limiting factor — broad keywords on metered platforms (X/LinkedIn) burn credits fastest; Reddit/Bluesky are real-time and cheaper to monitor.
- "Filter by tags" / sentiment scoring / webhooks / CSV exports / chat-with-mentions all gate to **Pro+**.

## Integrations

| Integration | Direction | Notes |
|---|---|---|
| Slack | SnitchFeed → Slack | Real-time, daily, or weekly alerts. All plans. |
| Discord | SnitchFeed → Discord | Same alert options as Slack. All plans. |
| Email | SnitchFeed → Email | Same alert options. All plans. |
| Webhook automations | SnitchFeed → endpoint | JSON payload per mention; SnitchFeed positions these as "via Zapier, n8n, etc." Pro+ only. |
| API | bidirectional (undocumented) | "API included" on all plans per pricing page; API calls consume credits. No public endpoint/auth docs found 2026-06-13. |
| HubSpot | SnitchFeed → HubSpot | Homepage lists it ("Plugs into Clay, Instantly, HubSpot, Slack"). Plan gate/detail unverified. |
| Instantly | SnitchFeed → Instantly | Homepage lists it. Plan gate/detail unverified. |
| Clay | SnitchFeed → Clay | Homepage lists it. Plan gate/detail unverified. |
| Google Sheets / Zendesk / Linear / Apollo | SnitchFeed → tool | Not found on current official pages (2026-06-13) — unverified; may have been removed or never shipped. |
| CSV export | Manual | Download mention data. **Pro+ only** (100 credits/export). |

**Automation path:** outbound **webhook automations** (Pro+) are the documented bridge — trigger Zapier/n8n/Make scenarios via webhook URL. An **API** is advertised on all plans but undocumented (see API note above). No native MCP server.

## Data model

<!-- Constructed from UI research — no API docs, verify against live product -->

```json
{
  "listener": {
    "name": "Competitor Tracking",
    "keywords": ["alternative to Jira", "looking for PM tool"],
    "relevance_context": "People actively looking to switch project management tools for small teams",
    "platforms": ["reddit", "twitter", "bluesky"],
    "alert_channels": ["slack", "email"],
    "alert_frequency": "real-time"
  },
  "mention": {
    "platform": "reddit",
    "url": "https://reddit.com/r/SaaS/comments/...",
    "content": "We need something simpler than Jira for our small team...",
    "ai_relevance_score": 0.92,
    "ai_sentiment": "negative",
    "ai_tags": ["Buy Intent", "Competitor Mention"],
    "ai_summary": "User frustrated with Jira complexity, actively seeking simpler PM tool for 5-person team",
    "detected_at": "2026-05-08T14:23:00Z",
    "keyword_matched": "alternative to Jira"
  }
}
```

*Note: This is a representative shape constructed from feature descriptions. SnitchFeed advertises an API (all plans) but publishes no public schema/field reference as of 2026-06-13, so field names are inferred. Webhook payloads may differ — test with webhook.site to confirm the real structure.*

## Quick-start recipes

### Recipe 1: Monitor Reddit for buying signals and alert Slack

**Trigger**: New high-intent Reddit mention detected
**Steps**:
1. Create a listener in SnitchFeed with keywords like "best tool for [category]", "alternative to [competitor]", "recommend [category]"
2. For each keyword, add relevance context: "People who are actively evaluating tools and ready to buy, not just casually browsing"
3. Connect Slack workspace and select the channel for alerts
4. Set alert frequency to "real-time" for immediate notifications
5. Review first 20-30 mentions, upvote relevant ones, downvote noise to train the AI

**Gotcha**: Starter plan caps at 10 keywords and 7,000 credits/mo (credits are spent per scan + per AI-scored mention, not per raw mention). X scans cost 2 credits/keyword and LinkedIn 4/keyword, so broad keywords on those platforms burn credits fastest. Start narrow and expand if you have capacity.

### Recipe 2: Push mentions to HubSpot via webhook (Pro plan)

**Trigger**: SnitchFeed webhook fires on new mention
**Steps**:
1. In SnitchFeed dashboard, navigate to webhook settings
2. Add your endpoint URL (e.g., a Zapier/Make webhook URL or your own server)
3. Configure a Zapier/Make scenario: receive webhook → create/update HubSpot contact
4. Map fields: mention URL → contact note, platform → custom property, intent tag → lead status
5. Alternatively, use the native HubSpot integration if available on your plan

```python
# Example: Simple webhook receiver (Flask)
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HUBSPOT_API_KEY = "your-hubspot-api-key"

@app.route("/snitchfeed-webhook", methods=["POST"])
def handle_mention():
    mention = request.json
    # Create a note in HubSpot with mention details
    # Adapt field names based on actual webhook payload
    note = {
        "properties": {
            "hs_note_body": f"SnitchFeed mention: {mention.get('url', 'N/A')}\n"
                           f"Platform: {mention.get('platform', 'N/A')}\n"
                           f"Summary: {mention.get('ai_summary', 'N/A')}\n"
                           f"Tags: {mention.get('ai_tags', [])}"
        }
    }
    # Post to HubSpot API
    resp = requests.post(
        "https://api.hubapi.com/crm/v3/objects/notes",
        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}",
                 "Content-Type": "application/json"},
        json=note
    )
    return jsonify({"status": "ok"}), 200
```

**Gotcha**: Webhook payload schema is not publicly documented. Test with webhook.site first to inspect the actual JSON structure before building your integration.

### Recipe 3: Competitive intelligence tracking

**Trigger**: Ongoing monitoring of competitor mentions
**Steps**:
1. Create separate listeners for each competitor (e.g., "Competitor A complaints", "switching from Competitor A")
2. Set relevance context: "People complaining about [Competitor A] or expressing desire to switch to a different tool"
3. Enable AI intent tagging (Pro plan) to auto-categorize as "Competitor Mention"
4. Set up a weekly digest alert to track sentiment trends around competitors
5. Export CSV monthly for share-of-voice analysis

**Gotcha**: Keywords are quota-limited (Starter: 10, Pro: 30) and listeners too (Starter: 3, Pro: 10). Group related competitor keywords in a single listener, and remember CSV export is Pro-only and costs 100 credits per export.

## Integration patterns

### Webhook-based automation (Pro+)
SnitchFeed pushes mention data to your configured webhook endpoint whenever a new mention matches your keywords and passes the relevance filter.

**Setup**:
1. Create a publicly accessible endpoint (your server, Zapier webhook URL, or Make webhook URL)
2. Configure the webhook URL in SnitchFeed dashboard settings
3. SnitchFeed sends a POST request with JSON payload per mention

**Retry behavior**: Unknown — not documented. Assume no automatic retry. Build idempotent receivers.

**Payload schema**: Not publicly documented. Test with a webhook debugging service first:
1. Go to webhook.site and copy the unique URL
2. Add this URL as your webhook endpoint in SnitchFeed
3. Wait for a matching mention to trigger a payload
4. Inspect the JSON structure and map fields to your downstream system

### Enrichment pipeline
SnitchFeed → webhook → Clay/Apollo enrichment → CRM/outreach:
1. SnitchFeed detects high-intent mention with poster's profile URL
2. Webhook pushes mention data to middleware (Zapier/Make/custom)
3. Middleware sends profile URL to Clay or Apollo for enrichment (email, company, title)
4. Enriched contact is created in HubSpot or added to Instantly sequence

### CSV batch workflow (all plans)
For teams on Starter without webhook access:
1. Export mentions as CSV from SnitchFeed dashboard
2. Upload CSV to Clay for bulk enrichment
3. Push enriched contacts to CRM or outreach tool
4. Repeat weekly or as needed
