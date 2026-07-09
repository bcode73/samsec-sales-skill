# Noisely Platform Guide

Full reference for the `sales-noisely` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — the marketing + comparison pages. No public API docs exist. Verify in-account.*

## What Noisely is

An **AI feedback-tracking / product-intelligence** SaaS: it continuously **ingests** customer feedback from 23+ external sources, runs an **AI pipeline** (categorize → sentiment → urgency/impact → cluster into "action items" → spike-detect), and **pushes** the results into your tools (tickets, chat, sheets). Positioned as the **affordable** option ($49/mo) vs enterprise VoC platforms (Enterpret/unitQ/Chattermill/Medallia/Qualtrics). Target users: PMs, founders, CS teams at customer-facing companies.

**Aggregation, not surveys.** Noisely mines *unsolicited* feedback at scale. It does not run NPS/CSAT surveys — for solicited-feedback program strategy use `/sales-customer-feedback`.

## Module map — UI vs webhook vs CSV

| Module | Surface | Notes |
|---|---|---|
| Source connections (23+) | **UI-config** | reviews/social/dev/support; not API-configured |
| AI categorization / sentiment / urgency | **AI (automatic)** | 12 categories, mention-level sentiment, impact score |
| Action items (clusters) | **AI + outbound** | the durable unit; ranked by frequency × impact |
| Spike detection | **Alert (outbound)** | real-time trending-issue alerts |
| Native channels (Linear/Jira/Asana/Notion) | **Integration** | action item → ticket/task/page |
| Chat alerts (Slack/Teams/Discord/Email) | **Integration** | alerts + digests |
| Google Sheets | **Integration** | append rows for BI |
| Webhooks | **Webhook (outbound)** | custom routing; payload schema unpublished |
| CSV | **Import + export** | bring data in / get structured data out |
| REST API | **Not available** | none documented (404) |

## Pricing & plan gates (best-effort)

| Tier | Cost | Key limits |
|---|---|---|
| **Try Noisely** | **$29 one-time** | up to 500 mentions, 1-hour report, $29 Pro credit |
| **Pro** | **$49/mo** | 23+ sources, 10 push channels, **2,000 AI analyses/mo**, 12-category classification, real-time alerts, **unlimited seats** |
| **Custom** | contact sales | higher analysis limits, **custom integrations**, dedicated support, SLA |

No per-seat fees; cancel anytime. The binding constraint is usually **AI analyses/mo** (credits), not seats — high-volume sources consume them quickly.

## Data model (action item — JSON shape)

No published schema. The durable automation unit is the **action item** (a cross-source cluster). CONSTRUCTED illustration (verify against a live webhook delivery; key on the `id`):

```json
{
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
```

Individual mentions roll up into action items; build downstream logic on the action-item id, not raw mentions (Noisely auto-dedupes/clusters).

## Quick-start recipes

### Recipe 1 — Route urgent action items into Linear/Jira (no code, preferred)

In Noisely, connect **Linear** (or Jira/Asana) as an outbound channel and configure which action items create issues (e.g. `urgency = high`). Each qualifying cluster opens a ticket with its sources/score. No endpoint to host.

### Recipe 2 — Custom routing via webhook

When native channels aren't enough (custom filtering/enrichment), add a **Webhook** outbound channel pointing at your endpoint:

```python
@app.post("/noisely-webhook")
def noisely_webhook(payload: dict):
    # Schema is undocumented — capture a real delivery (webhook.site) and map from it.
    # No documented HMAC — keep this URL secret.
    item = payload.get("action_item", payload)
    aid = item.get("id")
    if not aid or already_processed(aid):     # dedupe on the action-item id
        return {"ok": True}
    if item.get("urgency") == "high":
        open_ticket(title=item.get("title"), sources=item.get("sources"))
    mark_processed(aid)
    return {"ok": True}
```

### Recipe 3 — Export to Sheets / CSV for BI (no API)

Use the **Google Sheets** outbound channel to append action items, or **export CSV** from the analytics dashboard for batch analysis. This is the reliable structured-data path since there's no REST API. You can also **import CSV** (e.g. a Zendesk export) as an additional source.

## Tuning signal & credits

- **Brand-ambiguity filters:** train them early if your brand name is a common word — off-topic mentions both pollute action items and waste analysis credits.
- **Scope sources to your buyers:** disable noisy/low-signal sources (broad Google News, unrelated subreddits). Credits are consumed per analyzed mention.
- **Start on Try ($29):** validate mention volume and source fit before committing to Pro.

## When to route out

- Survey/VoC **program** design (NPS/CSAT/CES) across tools → `/sales-customer-feedback`
- Getting more **public reviews** (Trustpilot/G2 generation) → `/sales-customer-reviews`
- Broad **brand/social listening** / PR monitoring → `/sales-social-listening`
- Generic CRM/ticketer wiring (iPaaS) → `/sales-integration`
