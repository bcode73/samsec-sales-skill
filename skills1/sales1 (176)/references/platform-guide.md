# FeedBear Platform Reference

## Overview

FeedBear (feedbear.com) is a budget customer-feedback platform — public feedback **boards** (upvoting + comments), a **roadmap**, and a **changelog** in one hub. Positioned as a cheaper, simpler **Canny / Nolt / Frill** alternative for SaaS, mobile-app, and product teams (nonprofit discounts available). Its defining technical trait: **there is no public pull/REST API** — automation happens through outbound webhooks, JWT SSO, Zapier, and a handful of native integrations.

## Capabilities & automation surface

| Module | What it does | Automation tag |
|---|---|---|
| **Feedback boards** | Multiple boards for feature requests / bug reports; users submit "ideas", upvote, and comment | **Webhook-accessible** (new idea, upvote, comment events) + Zapier triggers; **no pull API** |
| **Upvoting / prioritization** | Vote counts rank demand; sort by support | Webhook-accessible (upvote event); UI for sorting |
| **Duplicate detection / merge** | Suggests similar ideas to avoid redundancy; admins merge | UI-only |
| **Roadmap** | Public roadmap driven by idea **status**; auto-notifies voters on progress | UI-only (status changes may emit a webhook — confirm live) |
| **Changelog** | Announce shipped features / product updates | UI-only |
| **Private ideas / private projects** | Keep ideas or whole projects non-public | UI-only (private projects = Business tier) |
| **Website widget** | Embed boards inside your web app; webview/link for mobile | UI/embed (JS snippet); SSO to identify users |
| **AI-generated comments & replies** | AI drafts replies/comments to feedback | UI-only |
| **Custom branding (CSS/HTML/JS, accent, logo, custom domain)** | Brand the portal; custom domain on Startup+ | UI-only config |
| **SSO** | JWT-based single sign-on so board activity attaches to real users | **Developer (JWT)**; Business tier |

**Terminology:** a **Project** = a company/brand (its own branding + web address). Roles: **Owners** (full admin + billing), **Team Members / Admins** (manage ideas, statuses, changelog; no team/billing control), **Normal Users** (submit ideas, comment, upvote).

## Pricing, limits & plan gates

Best-effort, captured 2026-06 — **confirm in-account**. No free tier; 14-day trial, no card required.

| Plan | Monthly | Annual (2 mo free) | Adds vs previous tier |
|---|---|---|---|
| **Lite** | $19 | $15/mo | 1 team member, 1 board, unlimited ideas & users, roadmap + changelog + private ideas, custom branding/statuses/HTML-JS/CSS, website widget, AI comments & replies |
| **Startup** | $49 | $40/mo | 3 team members, **unlimited boards**, **custom domain**, **integrations: Intercom, Slack, Trello, Jira, Zapier** (and **webhooks**) |
| **Business** | $99 | $82/mo | 10 team members, **SSO**, **private projects**, **remove FeedBear branding** |
| **Enterprise** | $299 | $249/mo | Unlimited team members, priority support (Slack/phone/email), custom contracts/NDAs/SLAs/DPAs, **custom integrations**, bank transfer, security audit |

**Integration-relevant gates:** webhooks + native integrations + Zapier require **Startup**; **SSO** and **private projects** require **Business**; **custom integrations** are **Enterprise**. There is no rate-limit/credit model to budget for because there's no pull API.

## Integrations

Data flow is mostly **outbound** (FeedBear → your tools). There is **no REST pull API**.

| Integration | Direction | Notes |
|---|---|---|
| **Webhooks** | FeedBear → you | New idea / upvote / comment events POSTed as JSON over HTTPS; works with Make, Syncspider, Pabbly, KonnectzIT, or your own endpoint. **No documented HMAC.** Startup+. |
| **Zapier** | FeedBear → 5,000+ apps | Triggers for feedback / ideas / comments; store or fan out to other apps. Startup+. |
| **Intercom** | bi-directional (widget) | Collect feedback inside Intercom Messenger; (coming) add ideas to boards from Intercom. |
| **Slack** | FeedBear → Slack | Instant notifications on new feedback/comments. |
| **Trello** | FeedBear → Trello | One-click convert an idea into a Trello card. |
| **Jira** | FeedBear → Jira | Add a validated idea as a Jira issue after it gathers votes/comments. |
| **SSO (JWT)** | you → FeedBear | Authenticate your logged-in users into the board. Business+. |

## Data model

There's no published API schema, so these shapes are **constructed from the product's documented concepts** — capture a live webhook delivery to confirm exact field names.

```jsonc
// Project — a company/brand workspace (one board URL, own branding)
{ "id": "proj_...", "name": "Acme", "board_url": "https://acme.feedbear.com" }
```

```jsonc
// Idea (a.k.a. feedback post) — lives on a Board, gathers votes + comments
// <!-- Constructed from docs — verify against a live webhook payload -->
{
  "id": "idea_...",
  "title": "Dark mode",
  "description": "Please add a dark theme",
  "board": "Feature Requests",
  "status": "planned",            // drives roadmap column
  "votes": 42,
  "author": { "name": "Jane", "email": "jane@example.com" },
  "created_at": "2026-06-29T10:00:00Z"
}
```

```jsonc
// Comment — attached to an Idea
// <!-- Constructed from docs — verify against a live webhook payload -->
{ "id": "cmt_...", "idea_id": "idea_...", "body": "+1", "author": { "name": "Sam" }, "created_at": "2026-06-29T11:00:00Z" }
```

**Relationships:** Project → Boards → Ideas → (Votes, Comments). An idea's **status** is its roadmap column; shipping it can feed the changelog.

## Quick-start recipes

### Recipe 1 — Catch a new-idea webhook and post to Slack (no pull API needed)

**Trigger:** a user submits an idea → FeedBear POSTs JSON to your endpoint.
**Steps:** Project Settings → Webhooks → set a **secret HTTPS URL** → enable → process the payload.

```python
# Flask receiver — FeedBear webhooks are NOT documented as HMAC-signed,
# so protect by secret URL + payload validation + dedupe.
import os, requests
from flask import Flask, request, abort

app = Flask(__name__)
SECRET_PATH = os.environ["FEEDBEAR_WEBHOOK_PATH"]   # unguessable path segment
SLACK = os.environ["SLACK_WEBHOOK_URL"]
seen = set()

@app.post(f"/feedbear/{SECRET_PATH}")
def feedbear():
    e = request.get_json(silent=True) or {}
    idea = e.get("idea") or e.get("data") or e          # field name varies — confirm live
    iid = idea.get("id")
    if not iid or iid in seen:                           # dedupe on idea id
        return ("", 200)
    seen.add(iid)
    requests.post(SLACK, json={"text": f"💡 New FeedBear idea: {idea.get('title','(untitled)')}"})
    return ("", 200)
```

```bash
# Simulate a delivery while you confirm the real schema from a live event
curl -X POST "https://your-app.example.com/feedbear/$FEEDBEAR_WEBHOOK_PATH" \
  -H "Content-Type: application/json" \
  -d '{"event":"idea.created","idea":{"id":"idea_123","title":"Dark mode","votes":1}}'
```

**Gotchas:** no signature to verify → rely on the secret URL + shape validation; the exact payload keys are unpublished, so log the first real delivery and adjust.

### Recipe 2 — Generate a JWT SSO token so votes attach to real users

**Trigger:** a logged-in user clicks "Login" on your FeedBear board.
**Steps:** Project Settings → SSO → copy the **private key** → after you authenticate the user, mint a JWT from their name + email → redirect to `{{BOARD_URL}}/sso/auth?payload={{JWT}}`.

```python
import jwt   # PyJWT

def feedbear_sso_redirect(board_url, private_key, user):
    token = jwt.encode(
        {"name": user["name"], "email": user["email"]},   # required identity claims
        private_key,
        algorithm="HS256",                                  # confirm algorithm in-account
    )
    return f"{board_url}/sso/auth?payload={token}"
```

**Gotchas:** keep the private key **server-side only**; SSO requires the **Business** plan; without SSO, widget feedback is anonymous.

### Recipe 3 — Mirror feedback to a spreadsheet via Zapier (no-code)

**Trigger:** new idea / comment in FeedBear.
**Steps:** Zapier → FeedBear trigger (New Feedback / Idea / Comment) → Action: append a row to Google Sheets (or create a card in Trello, a row in Airtable, etc.). Useful as a poor-man's export when there's no pull API.
**Gotchas:** requires the **Startup** plan; Zapier polling intervals add latency vs a direct webhook.

## Integration patterns

- **Push, not pull.** Architect every FeedBear integration around *receiving* events. There is no endpoint to query, so your system must persist webhook events as the source of truth (or re-export via Zapier on demand).
- **Webhook listener.** Secret URL + payload validation + idempotency (dedupe on idea id). No documented retry/auto-disable behavior — make your endpoint return 200 fast and process async; capture a live payload to finalize field mapping.
- **SSO bridge.** Authenticate on your side → JWT (private key) → `/sso/auth?payload=` redirect. Treat the private key like any signing secret.
- **One-off export.** Use Zapier or the in-app export to snapshot ideas/votes; there is no programmatic bulk-read API.
