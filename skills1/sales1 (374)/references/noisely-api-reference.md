<!-- Source: https://noise.ly and https://noise.ly/compare/ (fetched 2026-06). No public REST API documentation was found (noise.ly/docs/webhooks → 404). This reference documents the integration/automation surface that IS documented (incoming sources, outbound channels incl. webhooks, CSV) and explicitly flags the gaps. Do NOT invent endpoints. -->

# Noisely Developer / Integration Reference

## Nature of the integration surface

Noisely is a hosted **AI feedback-tracking / product-intelligence** SaaS. It **ingests** feedback from many sources, runs AI analysis (categorize → sentiment → urgency/impact → cluster into "action items" → spike-detect), and **pushes** results to your tools.

> ⚠️ **No public REST API documented.** As of this research, Noisely does not publish a REST API reference (the docs/webhooks path 404s). The programmatic surface is **outbound webhooks**, **native tool integrations**, and **CSV import/export**. Treat any payload shape as unconfirmed — capture a live webhook delivery (e.g. webhook.site) before coding against it. If you need an API, confirm availability with Noisely (Custom plan mentions "custom integrations").

## Incoming sources (ingest — 22–23+)

Configured in-app (not via API). Noisely pulls mentions from:

- **Review platforms:** Trustpilot, G2, Google Reviews, Apple App Store, Google Play Store, BBB, ConsumerAffairs, Yelp
- **Community / social / developer:** Reddit, Hacker News, Quora, Bluesky, GitHub, DEV, Stack Overflow, YouTube, Google News
- **Support tools:** Zendesk, Freshdesk, Intercom, Canny
- **Manual:** CSV import

"**Brand ambiguity filters**" learn to exclude off-topic mentions (e.g. a brand name that's also a common word).

## AI analysis pipeline (what you get out)

- **12-category classification** (bugs, feature requests, UX issues, praise, etc.) with auto-duplicate detection
- **Sentiment** (positive / negative / neutral) at mention level
- **Urgency & impact scoring** (prioritize by severity × user volume)
- **Pattern detection** → clusters similar feedback across sources into **"action items"** ranked by frequency/impact
- **Spike detection** → real-time alerts when an issue trends
- Credit model: **"AI analyses"** are a monthly credit limit (e.g. **2,000/mo on Pro**)

## Outbound channels (push — 10)

Noisely pushes action items / alerts / digests to:

```
Slack, Microsoft Teams, Discord, Linear, Jira, Notion, Asana,
Google Sheets, Email, Webhooks
```

- **Linear / Jira / Asana / Notion** — turn an action item into a ticket/task/page.
- **Slack / Teams / Discord / Email** — alerts and digests (incl. spike alerts).
- **Google Sheets** — append rows for analysis/BI.
- **Webhooks** — the generic developer hook: Noisely POSTs to your endpoint (use for custom routing when a native channel doesn't fit).

### Webhook (best-effort — schema not published)

Configure a webhook as an outbound push channel in-app. The exact **event types** (likely: new action item, spike detected, new high-urgency mention) and **payload schema** are **not documented**. CONSTRUCTED illustration (verify against a live delivery; do not rely on these key names):

```json
{
  "event": "action_item.created",
  "action_item": {
    "id": "ai_123",
    "title": "Checkout fails on Safari",
    "category": "bug",
    "sentiment": "negative",
    "urgency": "high",
    "impact_score": 87,
    "mention_count": 14,
    "sources": ["reddit", "trustpilot", "zendesk"],
    "first_seen": "2026-06-20",
    "last_seen": "2026-06-27"
  }
}
```

No documented signature/HMAC, retry behavior, or rate limits — secure the endpoint as a secret URL and dedupe on the action-item id.

## CSV

- **Import:** bring your own feedback (e.g. support exports) as a source.
- **Export:** the analytics dashboard exports trends/mentions/action items to CSV — the most reliable way to get structured data out absent a REST API.

## Identity / dedupe

Feedback is mention-level; the durable unit for automation is the **action item** (a cluster). Key your downstream logic on the action-item id, not individual mentions (Noisely auto-dedupes/clusters).
