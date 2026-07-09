# FeatureOS Platform Reference

## Overview

FeatureOS (formerly **Hellonext**) is an all-in-one customer-feedback platform for product teams: collect feature requests on voting **boards**, prioritize on a **roadmap**, ship updates via a branded **changelog**, and deflect with an AI **knowledge base** — a closed loop from feedback to release. It targets product/SaaS teams from solo operators to enterprise, and competes with Canny, Frill, Featurebase, Nolt, and UserVoice. Built by Skcript (github.com/skcript).

> The Hellonext → FeatureOS rebrand left **legacy identifiers** in place: API keys are prefixed `hn_`, the embed JS class is `HellonextWidget`, and feedback posts are called `feature_requests` in the v3 API.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Feedback boards (buckets)** | Posts/feature requests with upvotes, comments, statuses, AI duplicate detection | API-accessible (`feature_requests`, `buckets`, `votes`, `comments`); webhook-accessible (post events) |
| **Roadmap** | Drag-and-drop List/Kanban/Timeline views driven by post **status** | API: `roadmap:read`; status drives roadmap column |
| **Changelog** | Branded release notes, custom domain, in-app announcements | API: `changelog:read|write`; webhook-accessible (`changelog_published`/`_updated`) |
| **Knowledge base** | AI-powered searchable help articles + collections | API: `articles:read|write`, `collections:read` |
| **Forms & Surveys** | Conditional logic, custom fields, in-product capture | UI + widget; survey responses captured in-app |
| **Customers** | CRM-style customer records attached to feedback (segments) | API: `customers:read|write` (incl. import) |
| **Widget** | Embeddable feedback/roadmap/changelog widget with SSO | Front-end JS (`HellonextWidget`); `ssoToken` to attribute activity |
| **AI Copilot** | Duplicate detection, sentiment, `ai_summary`, trend analysis | Surfaced in post payloads (`sentiment_type`, `ai_summary`, `resource_keywords`) |
| **Integrations** | Slack, Jira, Linear, Intercom, Salesforce (2-way sync) | Native connectors; OAuth apps for third-party installs |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — confirm in-account; FeatureOS has re-priced/renamed tiers more than once.*

| Tier | Price (monthly) | Highlights |
|---|---|---|
| **Free trial** | 30-day, no card | Evaluate all 5 modules |
| **Starter** | ~$60/mo | 5 seats, 5 boards, 3 integrations, all modules + AI; SSO add-on |
| **Growth** ("Most Popular") | ~$120/mo | 10 seats, 10 boards, 5 integrations, 5 user segments, **complete API access**, SSO included |
| **Business** | ~$250/mo | 15 seats, **unlimited** boards + integrations, 10 segments, dedicated CSM, priority dev hours, native Salesforce |
| **Enterprise** | Custom | — |

- **Annual discount:** ~17% off. **Add-ons:** extra seats/boards ~$15/mo each.
- **API access is plan-gated.** The live pricing page lists "complete API access" starting at **Growth (~$120)**; the Help Center separately says API-key usage is on the top plan ("Fly High"). Treat full API access as a **paid/higher-tier** feature and verify what your tier includes before building.
- **Rate limit:** 100 requests/min per API key (`429` on overage).
- **Seat-limit errors** (`ERROR_CODE_*_LIMIT_REACHED`) surface in API responses when you exceed admin/CSM/manager seats — handle them in import scripts.

## Integrations

- **Reads/writes:** REST API v3 (`api.featureos.app/api/v3`) for posts/votes/comments/changelog/customers/etc.; **webhooks** push post + changelog events to you (one-directional, FeatureOS → you).
- **Native two-way sync:** Jira, Linear (engineering); Slack, Intercom (notifications/capture); Salesforce (Business+).
- **OAuth apps:** build an integration that **other workspaces install** (Slack bot, internal tool) via OAuth 2.0 — no shared API key.
- **iPaaS:** available through Zapier/Pabbly-style connectors (legacy "Hellonext" connectors still listed on some iPaaS catalogs).

## Data model

A **post** (feature request) — the central object (verbatim shape from a webhook payload):

```json
{
  "id": 80874,
  "title": "Time specification for Changelogs",
  "object": "post",
  "status": { "label": "Completed", "value": "completed" },
  "upvotes_count": 1, "downvotes_count": 0,
  "approval_status": "approved", "hidden": false, "pinned": false,
  "created_at": 1648026486, "updated_at": 1651686939,
  "submitter": { "name": "Swathy R", "email": "..." },
  "sentiment_type": "positive",
  "ai_summary": "Request for specifying precise time for publishing changelog",
  "resource_keywords": [ { "name": "changelogs", "slug": "changelogs" } ],
  "bucket": { "id": 1, "slug": "feature-requests", "display_name": "Feature Requests" }
}
```

- **bucket** = board. **status.value** (`planned`/`in_progress`/`completed`…) = the roadmap column. Timestamps are **unix seconds**. A **customer** record can be attached to posts for segmentation. On status-change webhooks you also get `before`/`after` diff blocks.

## Quick-start recipes

### 1. Export all feedback posts (paginate)

```bash
curl -s 'https://api.featureos.app/api/v3/feature_requests?per_page=100&page=1' \
  -H 'API-KEY: hn_your_api_key'
```

```python
import requests
def all_posts(key):
    out, page = [], 1
    while True:
        r = requests.get("https://api.featureos.app/api/v3/feature_requests",
                          headers={"API-KEY": key},
                          params={"per_page": 100, "page": page})
        r.raise_for_status()
        batch = r.json().get("data", r.json())   # confirm envelope vs bare array
        if not batch: break
        out += batch
        if len(batch) < 100: break               # last page (default 30, max 100)
        page += 1
    return out
```

Gotcha: pagination is **`page`/`per_page`** (not cursors). 100 req/min — sleep on 429.

### 2. Receive a `post_completed` webhook and update your tracker

```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/webhooks/featureos")
def hook():
    e = request.get_json()
    etype = e.get("type") or e.get("event")          # dashboard: type; OAuth-app: event
    if etype in ("postCompleted", "post_completed"):
        p = e["data"]
        # p["after"]["completed_at"], p["url"], p["bucket"], p["upvotes_count"]
        notify_team(p["title"], p["url"])
    return "", 200                                    # MUST 200 or it retries (5m/30m/2h) then disables
```

Gotcha: respond **200 fast**. After 3 failed retries the webhook is **auto-disabled** (email sent). Dashboard webhooks aren't HMAC-signed — keep the URL secret / verify by IP.

### 3. Embed the widget and identify the logged-in user (SSO)

```html
<button id="featureosWidget">Feedback ✨</button>
<script>
  new window.HellonextWidget({
    token: 'YOUR_ORG_WIDGET_TOKEN',
    ssoToken: '<JWT signed with your org SSO key: {"email":"...","name":"..."}>',
    modules: ['feature_requests', 'changelog'],
    selector: '#featureosWidget'
  }).init();
</script>
```

Gotcha: without `ssoToken`, votes/posts are **anonymous**. Class is `HellonextWidget` (legacy), not `FeatureOSWidget`.

## Integration patterns

- **CRM/roadmap sync:** treat `status.value` as the source of truth for roadmap state; map FeatureOS statuses → your columns. Use `customers` (with import) to attach accounts/segments to feedback for revenue-weighted prioritization.
- **Webhook listener:** subscribe to `post_created`/`post_updated`/`post_completed` + `changelog_published`; dedupe on `data.id` + `created`/`updated_at` (unix seconds); always 200; rebuild missed events by polling `feature_requests` (webhooks aren't replayable once disabled).
- **OAuth app (multi-tenant):** for a product other orgs install, register an app (`POST /oauth/apps`), request **minimum scopes**, handle the 24h access-token expiry by refreshing (rotation — store the newest `foot_`/`foor_` pair), and provision webhooks via `webhooks:manage` + `subscribed_webhook_events`.
- **Rate-limit handling:** 100/min/key — batch reads with `per_page=100`, cache, and back off on `429`/`ERROR_CODE_RATE_LIMITED`.
