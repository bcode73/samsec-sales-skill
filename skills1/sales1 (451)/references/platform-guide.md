# Quickhunt Platform Reference

## Overview

Quickhunt (quickhunt.app) is an affordable, all-in-one customer-feedback and product-communication suite for SaaS teams — feedback boards, a public roadmap, a changelog, in-app messages, a knowledge base, an AI assistant, and live chat in one dashboard. It positions itself as a polished, cheaper Canny / Frill / Featurebase / Productboard / Upvoty alternative, and its standout is a **genuinely free lifetime tier**. Its weak spot is the developer surface: the REST API is gated to the top Premium plan and undocumented publicly, and integrations don't appear until the Growth plan.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Feedback boards** | Collect ideas / feature requests / bug reports with upvoting, comments, reactions, categories/tags, anonymous submission | UI-first; **webhooks** for new feedback/comment/vote (schema unpublished); read via **API on Premium only**; no-code via **Zapier/viaSocket** (Growth+) |
| **Roadmap** | Visual roadmap with customizable stages (planned / in-progress / shipped); prioritize by demand/value/feasibility; link feedback ↔ roadmap ↔ announcements | UI-first; a feedback item's **status** drives its roadmap column; surfaced via integrations on Growth+ |
| **Changelog** | Public changelog / release notes; in-app notification widget; **scheduled publishing** (Starter+); engagement analytics | UI-first; new-changelog can fan out via Zapier/native connectors (Growth+) |
| **In-app messages** | Surveys, checklists, posts, banners with triggers/timing; modal / sidebar / popover / embed widget formats | UI-first; configured in-app; targeting/triggers are UI-only |
| **Docs / knowledge base** | FAQ + help articles with search, rich media (images/video/code), embeddable widget | UI-first; article counts are plan-capped (50 Free / 150 Starter / 300 Growth / unlimited Premium) |
| **AI assistant** | Context-aware Q&A grounded in your connected docs; embeddable widget | UI-first; available from the Free tier |
| **Live chat** | Real-time conversations, page-visit history, auto ticket creation, AI response suggestions (newer add) | UI-first |
| **Integrations** | Slack, Zapier, ClickUp, GitHub, HubSpot, Jira, viaSocket (Intercom coming soon) | **Growth-tier ($49/mo) and up** — Free and Starter have **no integrations** |
| **REST API** | Programmatic access (endpoints/auth undocumented publicly) | **Premium-tier ($99/mo) only**; request docs from the dedicated account manager |

**Rule of thumb:** below Premium there is no API; below Growth there are no integrations at all. Plan automation around **Zapier / viaSocket / native connectors + webhooks** (Growth+), not an API, unless the account is on Premium.

## Pricing, limits & plan gates

*Best-effort, captured 2026-06 from quickhunt.app/pricing — confirm in-account.*

| Plan | Price (monthly / annual) | Key inclusions | Notable gates |
|---|---|---|---|
| **Free** (lifetime) | $0 | 1 feedback board, 1 roadmap, 50 articles, 2 in-app messages, **unlimited feedback posts + changelog**, AI assistant | Limited embed widget; **no custom domain, no remove-branding, no integrations** |
| **Starter** | $29 / $23 | 5 boards, multiple roadmaps, 150 articles, 10 in-app messages, **custom domain**, scheduled changelog, analytics, conditional logic, **remove branding**, email + live-chat support | **No integrations** |
| **Growth** ("Most Popular") | $49 / $40 | 10 boards, 300 articles, 20 in-app messages, **5 team members**, **unlimited integrations** (Slack/Zapier/ClickUp/GitHub/HubSpot/Jira/viaSocket) | **No API** |
| **Premium** | $99 / $79 | Unlimited boards / articles / in-app messages / changelog, **dedicated account manager**, **API support** | — |

- **Extra team members: +$10/mo each** on every plan (Growth includes 5).
- **Annual billing ≈ 20% off.**
- **Two hard cliffs to remember:** integrations appear at **Growth ($49)**, and the **API appears only at Premium ($99)**.

## Integrations

Data flow by connector (all **Growth-tier and up**):

- **Slack** — push: Quickhunt feedback → Slack channels with insights (notification/intake).
- **Zapier** — bidirectional bridge to 5,000+ apps; the primary no-code stand-in for the missing low-tier API. Confirm exact trigger/action names in the live Zap editor.
- **viaSocket** — second iPaaS bridge to "thousands of apps"; same role as Zapier.
- **ClickUp** — push: feedback → ClickUp tasks.
- **GitHub** — push: feedback → actionable GitHub issues for engineering.
- **HubSpot** — connect feedback with HubSpot to enrich contacts / uncover insights.
- **Jira** — push: feedback → Jira issues.
- **Intercom** — *coming soon*: convert Intercom messages into Quickhunt feedback (verify before relying on it).

There is no documented native Salesforce/Zendesk connector — route those through Zapier/viaSocket.

## Data model

> <!-- Constructed from product docs/UI terminology — Quickhunt publishes no API spec; verify field names against the live API (Premium) or a captured webhook payload before relying on them. -->

Quickhunt's public terminology maps to these objects:

```jsonc
// Feedback item (a.k.a. "idea" / feature request / bug report)
{
  "id": "fb_123",
  "board_id": "board_abc",
  "title": "Add a Kanban view for form entries",
  "description": "Let me view entries as Kanban/Card/Table by status/category/tags",
  "type": "feature_request",          // feature_request | bug | suggestion (UI categories)
  "status": "planned",                // drives the roadmap column: planned | in_progress | shipped (+ custom)
  "upvotes": 42,
  "tags": ["forms", "ui"],
  "author": { "name": "Jane D.", "email": "jane@acme.com" },  // anonymous if not identified
  "created_at": "2026-06-29T10:00:00Z"
}
```

```jsonc
// Roadmap is a view over feedback items grouped by status (no separate object).
// Changelog post (release note)
{
  "id": "cl_789",
  "title": "Kanban view is live",
  "body_html": "<p>You can now view entries as Kanban/Card/Table.</p>",
  "category": "new",                  // new | improvement | fix
  "published_at": "2026-06-29T12:00:00Z",
  "scheduled_for": null               // scheduled changelog is Starter+
}
```

```jsonc
// In-app message
{
  "id": "msg_456",
  "format": "survey",                 // survey | checklist | post | banner
  "display": "modal",                 // modal | sidebar | popover | embed
  "trigger": "on_page_load",          // UI-configured targeting/timing
  "status": "active"
}
```

## Quick-start recipes

Quickhunt has **no documented public API** below Premium, so these recipes are no-code (Growth+) except where Premium is called out.

### Recipe 1 — Push every new feature request into your own system (no-code, Growth+)

**Trigger:** New feedback created in Quickhunt.
**Steps:** In Quickhunt **Integrations**, connect **Zapier** (or **viaSocket**). Create a Zap with the Quickhunt "new feedback" trigger → an action that POSTs to your app (or creates a row/record in your CRM/DB). Confirm the exact trigger name in the live Zap editor — Quickhunt doesn't publish them.

```bash
# Receiving side: a webhook endpoint that Zapier (or a Quickhunt webhook) POSTs to.
# Payload shape is unpublished — log the first delivery, then map fields.
curl -X POST https://your-app.example.com/hooks/quickhunt \
  -H "Content-Type: application/json" \
  -d '{ "event": "feedback.created", "data": { "id": "fb_123", "title": "...", "status": "planned" } }'
```

```python
# Flask receiver — capture-first, then map once you know the shape.
from flask import Flask, request
import logging

app = Flask(__name__)

@app.post("/hooks/quickhunt")
def quickhunt_hook():
    payload = request.get_json(force=True, silent=True) or {}
    logging.info("Quickhunt delivery: %s", payload)   # learn the real schema from this line
    data = payload.get("data", {})
    # idempotency: dedupe on the feedback id since you can't re-read from Quickhunt below Premium
    upsert_feedback(id=data.get("id"), title=data.get("title"), status=data.get("status"))
    return "", 200
```

**Gotchas:** No integrations on Free/Starter — this requires **Growth**. Webhooks have no documented HMAC; secure the endpoint by secret URL / IP allowlist and dedupe on the feedback id.

### Recipe 2 — Turn high-demand feedback into a GitHub issue (no-code, Growth+)

**Trigger:** Feedback reaches a chosen status (e.g. `planned`).
**Steps:** Connect the native **GitHub** integration in Integrations, map the board/status to a target repo so qualifying feedback creates an actionable issue. For more control (templated title/body, labels), use **Zapier**: Quickhunt status-change trigger → GitHub "Create Issue" action.

```text
Zap: Quickhunt (feedback status = planned) ──▶ GitHub: Create Issue
  Title:  [Feedback] {{title}}
  Body:   {{description}}\n\nUpvotes: {{upvotes}} · Source: Quickhunt {{id}}
  Labels: feedback, {{type}}
```

**Gotchas:** Two-way status sync (issue closed → feedback shipped) isn't documented — verify in-account. Confirm the status-change trigger exists in the live Zap editor.

### Recipe 3 — Embed the feedback / changelog / docs widget (any plan)

**Steps:** Add Quickhunt's embed snippet to your app to surface the feedback board, changelog ("what's new"), or knowledge base. Choose a format — **embed, modal, sidebar, popover, or banner**.

```html
<!-- Representative embed — copy the exact snippet from Quickhunt → Widget settings. -->
<script>
  window.QuickhuntSettings = { board: "YOUR_BOARD_ID", widget: "sidebar" };
</script>
<script async src="https://quickhunt.app/widget.js"></script>
```

**Gotchas:** The embed widget is **limited on Free**; custom domain for a hosted portal is **Starter+**. To attach feedback to known users (vs anonymous), check the in-account widget/identify settings — Quickhunt's identify mechanism isn't publicly documented.

## Integration patterns

- **No-API intake (below Premium):** Treat Quickhunt as **push-only**. Use Zapier/viaSocket triggers + native connectors + webhooks to move feedback *out*; you cannot reliably poll it back *in*, so make your receiver **idempotent** (dedupe on the feedback id) and **capture-first** (log the first webhook delivery to learn the unpublished schema before mapping fields).
- **API intake (Premium):** If on Premium, request the API docs from your dedicated account manager and confirm base URL, auth scheme, pagination, and rate limits in-account before building — none are published.
- **Plan-gate guardrails:** Before designing any automation, confirm the customer's plan. Free/Starter → **no integrations** (recommend upgrade to Growth first). Growth → integrations yes, API no. Premium → API yes.
- **Status → roadmap → changelog flow:** A feedback item's status is the single lever — it drives the roadmap column and is the natural trigger for "create issue" / "notify voters" / "publish changelog" automations. Standardize your status set first, then wire automations to status transitions.
