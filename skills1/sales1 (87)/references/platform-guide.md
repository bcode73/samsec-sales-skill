# CatchIntent Platform Reference

## Overview

> **2026-06-13 re-verification — major pivot.** As of v3.0.0 (2026-05-13) and v3.1.0 (2026-05-25), CatchIntent is now a **LinkedIn-exclusive B2B intent / outbound platform**. It has **sunset monitoring of Reddit, Hacker News, Bluesky, and X/Twitter for new customers** (changelog: Reddit/HN/Bluesky deprecated v3.0.0; X/Twitter "LinkedIn-only going forward" v3.1.0). Pricing also consolidated from seven tiers to three (Growth / Scale / Enterprise) priced by leads/month, with public dollar prices no longer shown on the page (trial/demo gated). Sections below have been updated; some older multi-platform / Basic-vs-Pro detail is retained only where still corroborated.

CatchIntent is an AI-powered intent platform that detects B2B buyer intent signals on **LinkedIn**, then enriches matching leads (Bedrock-powered enrichment) with profile, company, and scoring data. Differentiator: AI agents detect signals like job changes, funding, hiring, competitor engagement, and ICP-fit, score each lead (Warmth / ICP Fit / Intent / Recency), and draft personalized openers for same-day outreach. Earlier versions also monitored Reddit, X/Twitter, Hacker News, and Bluesky; those surfaces have been deprecated for new buyers.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **LinkedIn Intent Monitoring** | AI agents watch LinkedIn for buying signals — 8 signal types: job changes, funding, hiring spikes, exec moves/promotions, acquisitions, competitor engagement, keyword/category discussions, ICP-fit | MCP server (OAuth) |
| **Lead Scoring** | Scores each lead on Warmth, ICP Fit, Intent, and Recency | MCP server |
| **Drafted Openers** | AI drafts personalized outreach openers for high-intent leads | UI + MCP (all plans per current pricing) |
| **Lead Enrichment** | Bedrock-powered enrichment fills the profile (company, role, contact data, scores) | UI + MCP server |
| **Browser Extension** | Send LinkedIn DMs / outreach from the extension | UI-only |
| **CRM Push** | Push leads to CRM — **HubSpot live**; Pipedrive, Close, Zoho listed as coming soon | UI-only / all plans (current pricing lists "CRM push" on all tiers) |
| **Alerts** | Email, Slack, Discord, Telegram notifications with temperature + interactive "Reached Out / Ignore" buttons (Slack, Telegram) | UI config → push delivery |
| **MCP Server** | 27 typed tools (leads, agents, outreach, workspace) from Claude, Cursor, Codex, any MCP client | MCP (OAuth, all plans) at `https://engine.catchintent.com/mcp` |
| **CSV Export** | Bulk export lead data | UI-only |

<!-- HISTORICAL (deprecated 2026-05): earlier versions also offered multi-platform "listeners" across Reddit/X/HN/Bluesky, 0-100 relevance scoring, AI reply suggestions for forum threads, and CRM connectors to Lemlist/Instantly/Apollo. These are no longer the current product surface; retained only as context. Webhooks as a Pro+ delivery channel are NOT confirmed in current docs/changelog — treat as UNVERIFIED. -->

## Pricing, limits & plan gates

*Re-verified 2026-06-13 against catchintent.com/pricing. Pricing was overhauled: consolidated from seven tiers to **three** (changelog v3.0.0, 2026-05-13), now priced by **leads/month** rather than signals/month. Public dollar prices for Growth and Scale are **no longer shown** on the page — they are gated behind "Start trial" / "Book a demo." Verify exact $ at catchintent.com/pricing.*

| Feature | Growth | Scale (Popular) | Enterprise |
|---|---|---|---|
| Monthly price | Not publicly listed (trial/demo) | Not publicly listed (trial/demo) | Custom |
| Leads/month | 1,000 (~50/day) | 4,000 (~200/day) | 25,000+ |
| Products | 1 | 3 | 25 |
| Outreach accounts | 1 | 3 | 25 |
| Intent signals | All 8 | All 8 | All 8 (+ custom sources) |
| Drafted openers | Yes | Yes | Yes |
| Browser extension | Yes | Yes | Yes |
| CRM push | Yes | Yes | Yes |
| MCP server (27 tools) | Yes | Yes | Yes |
| Email/Slack/Discord/Telegram alerts | Yes | Yes | Yes |
| Support | Email | Email (priority) | Priority |

**8 intent signal types** (shared across all plans): job changes, funding, hiring spikes, exec moves/promotions, acquisitions, competitor engagement, keyword/category discussions, ICP-fit. Enterprise adds custom signal sources.

**Done-for-you service**: starting at **$1,999/mo**, 3-month minimum — includes product audit, audience setup, weekly signal tuning, drafted openers, weekly reporting.

**Trial**: 7 days, 50 trial leads, **card on file required**, cancel before day 7 to avoid charges (full refund policy in terms).

<!-- HISTORICAL (deprecated 2026-05): older tier model was Basic $49 / Pro $69 / Enterprise, gated by signals/month (150/500) and listeners, with multi-platform monitoring, webhooks Pro+, AI reply suggestions Pro+, and a separate "LinkedIn Intelligence" add-on (~$69/mo, up to 18,000 leads/mo). The interim v2.0 model used a credits system (Basic 25/mo, Pro 50/mo + packs of 500–2,500). None of these reflect the current three-tier lead-volume pricing. -->

No annual discount confirmed on the current page.

## Integrations

*Re-verified 2026-06-13. HubSpot is the only CRM connector confirmed live (changelog v1.7.0, 2026-02-04). Pipedrive, Close, and Zoho are listed as "coming soon" and remained pending as of v3.1.0 (2026-05-25). Lemlist / Instantly / Apollo are no longer listed as connectors in current materials.*

| Integration | Direction | Plan required / status |
|---|---|---|
| HubSpot | CatchIntent → HubSpot (push leads) | Live (current pricing lists CRM push on all tiers) |
| Pipedrive | CatchIntent → Pipedrive (push leads) | Coming soon (pending) |
| Close | CatchIntent → Close (push leads) | Coming soon (pending) |
| Zoho | CatchIntent → Zoho (push leads) | Coming soon (pending) |
| Slack | CatchIntent → Slack (alerts, interactive buttons) | All plans |
| Discord | CatchIntent → Discord (alerts, one-click setup) | All plans |
| Telegram | CatchIntent → Telegram (alerts, interactive buttons) | All plans |
| Email | CatchIntent → email (alerts with temperature) | All plans |
| MCP Server | Bidirectional — 27 typed tools, OAuth | All plans (`https://engine.catchintent.com/mcp`) |
| CSV Export | CatchIntent → file (bulk export) | All plans |

<!-- UNVERIFIED: "Webhooks → any endpoint (Pro+)" appeared in the earlier capture but is NOT confirmed in current changelog/docs/pricing (which list only Email/Slack/Discord/Telegram alert channels). Treat webhook delivery as unverified; do not rely on it without testing. Lemlist/Instantly/Apollo connectors also unverified in current materials. -->

<!-- HISTORICAL: earlier captures listed Lemlist (push to sequences), Instantly (push to campaigns), and Apollo (push leads) as Pro+ connectors. Not corroborated in current materials. -->

The author/attribution-free data model below predates the LinkedIn-only pivot; field names (e.g. relevance_score 0-100, intent_type, listener_id) reflect the older social-listening schema and may differ from the current LinkedIn lead schema. Retained as historical reference — verify against the 27 MCP tool schemas.

## Data model

### Signal object
<!-- Constructed from docs — verify against live API -->
```json
{
  "signal_id": "sig_abc123",
  "platform": "reddit",
  "source_url": "https://reddit.com/r/SaaS/comments/...",
  "content": "Looking for a project management tool that integrates with Slack...",
  "relevance_score": 87,
  "intent_type": "buying",
  "surfacing_rationale": "User is actively comparing tools and requesting specific integration",
  "author": {
    "username": "techfounder42",
    "platform_profile_url": "https://reddit.com/u/techfounder42"
  },
  "enrichment": {
    "email": "verified@example.com",
    "linkedin_url": "https://linkedin.com/in/...",
    "company": "Acme Corp",
    "icp_score": 82,
    "warmth_score": "high"
  },
  "created_at": "2026-05-06T14:30:00Z",
  "listener_id": "lst_xyz789"
}
```

### Listener object
<!-- Constructed from docs — verify against live API -->
```json
{
  "listener_id": "lst_xyz789",
  "name": "PM tool buyers",
  "keywords": ["project management", "task management", "Asana alternative"],
  "platforms": ["reddit", "hackernews", "bluesky"],
  "relevance_threshold": 75,
  "status": "active",
  "notification_channels": ["slack", "email"],
  "signals_this_month": 42,
  "created_at": "2026-04-01T10:00:00Z"
}
```

## Quick-start recipes

### Recipe 1: Set up a buyer intent listener

**Goal**: Monitor Reddit and HN for people actively looking for your type of product.

**Steps**:
1. Go to Listeners → Create New
2. Add 3-5 keywords using buyer language: "looking for [category]", "need a [category] tool", "alternative to [competitor]"
3. Select platforms: Reddit + Hacker News
4. Set relevance threshold to 75%
5. Connect Slack for real-time alerts
6. Review first 20 signals after 48 hours, adjust threshold up/down

**Gotchas**: Don't use your product name as a keyword — that captures mentions of you, not buyers looking for your category. Use competitor names and problem-language keywords instead.

### Recipe 2: Push qualified leads to HubSpot via webhook

**Goal**: Automatically create HubSpot contacts when CatchIntent surfaces a high-intent signal.

**Trigger**: CatchIntent webhook fires on new signal (Pro+ plan required)

**Webhook endpoint setup** (your server):
```python
from flask import Flask, request
import requests

app = Flask(__name__)

HUBSPOT_TOKEN = "pat-na1-xxx"

@app.route("/catchintent-webhook", methods=["POST"])
def handle_signal():
    signal = request.json
    if signal.get("relevance_score", 0) >= 80:
        # Create HubSpot contact
        requests.post(
            "https://api.hubapi.com/crm/v3/objects/contacts",
            headers={"Authorization": f"Bearer {HUBSPOT_TOKEN}",
                     "Content-Type": "application/json"},
            json={
                "properties": {
                    "email": signal["enrichment"]["email"],
                    "firstname": signal["author"]["username"],
                    "company": signal["enrichment"].get("company", ""),
                    "hs_lead_status": "NEW",
                    "notes_last_activity": f"CatchIntent signal: {signal['source_url']}"
                }
            }
        )
    return "", 200
```

**Gotchas**: Webhook payload schema is not formally documented — test with a real signal and log the full payload before building your handler. Filter by `relevance_score >= 80` to avoid creating contacts from noise.

### Recipe 3: Query signals via MCP server

**Goal**: Access CatchIntent data from Claude or Cursor via natural language.

**Setup**:
1. In your MCP client (Claude, Cursor, Codex, any MCP client), add the CatchIntent MCP server at `https://engine.catchintent.com/mcp` (Streamable HTTP transport)
2. Authentication uses OAuth — no API key needed; the server initiates an OAuth flow on first connect ("one command, one authorization, done")
3. Once connected, you have **27 typed tools** spanning leads, agents, outreach, and workspace. Query naturally: "Show me today's high-intent LinkedIn leads" or "Draft an opener for this lead and push it to HubSpot."

**Gotchas**: MCP server is on all plans with no add-on. Tools operate over LinkedIn leads/signals (the multi-platform Reddit/X/HN/Bluesky surfaces were sunset in 2026-05). Workspaces are multi-brand with OAuth-scoped access isolated per brand.

## Integration patterns

### Alert routing architecture

CatchIntent supports parallel alert delivery — a single listener can push to Slack AND email AND Discord simultaneously. Design your routing by urgency:

- **Immediate action** (relevance 85+): Slack DM or Discord with @mention
- **Daily review** (relevance 70-84): Email digest
- **Weekly audit** (relevance below 70): CSV export review

### CRM sync pattern

CatchIntent's CRM integrations are one-click push, not continuous sync. The workflow:
1. Signal appears in dashboard with enrichment data
2. User reviews and clicks "Push to CRM"
3. Contact/lead created in CRM with signal context

For automated push, use webhooks (Pro+) to build your own pipeline.

### MCP server interaction pattern

The MCP server at `https://engine.catchintent.com/mcp` exposes **27 typed tools** (leads, agents, outreach, workspace) over Streamable HTTP, authorized via an OAuth flow on first connect (no API key). It is the primary programmatic surface and is included on every plan with no separate pricing. Use it to query LinkedIn intent signals/leads, draft and send outreach, manage pipeline, and operate multi-brand workspaces (OAuth-scoped, isolated per brand) — all in natural language from Claude, Cursor, Codex, or any MCP client.
