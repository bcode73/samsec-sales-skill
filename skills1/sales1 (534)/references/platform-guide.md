# Sleekplan Platform Reference

## Overview

Sleekplan (sleekplan.com) is an AI-powered customer-feedback suite for product teams: feedback boards (voting + comments), a public/internal roadmap, a changelog, and built-in NPS/CSAT + in-app surveys — a Canny/Frill/Featurebase alternative whose differentiators are an AI layer ("Sleek Intelligence" / the "Sleekmate" PM agent: auto-categorization, duplicate merging) and a first-class **MCP server** for Claude/Cursor. German company (github.com/Sleekplan).

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Feedback boards** | Public/private boards; posts (feedback items) with voting, comments, status, AI auto-categorization + duplicate merging | **API** (posts/comments/votes), **webhook** (item/comment/vote events), **MCP**, widget, UI |
| **Roadmap** | Drag-and-drop prioritization, public or internal; links feedback → roadmap items (driven by a post's status) | **API** (read/set status), **MCP**, UI |
| **Changelog** | Formatted release notes with reactions, embeds, in-app widget | **API** (create/update/list), **webhook** (`changelog.*`), **MCP**, widget |
| **NPS / CSAT** | Targeted satisfaction surveys with sentiment scoring, integrated into boards | **API** (responses), **webhook** (`satisfaction.create`), **MCP** |
| **Surveys** | In-app questionnaires triggered at strategic moments | **API**, `$sleek` widget SDK (popup triggers), UI |
| **Sleek Intelligence / Sleekmate** | AI layer: auto-categorize, merge duplicates, themes/trends/signal, multi-step PM agent | UI + **MCP** (`find-similar`, `merge`, stats); consumes monthly AI credits |
| **Widget** | Embeddable launcher (boards/changelog/surveys) | **`$sleek` JS SDK** (front-end), HTML triggers, iframe/standalone embed |
| **Canvas** | Interactive custom admin integrations | Secret-token auth (same family as webhooks); UI-config |

## Pricing, limits & plan gates

*Best-effort from sleekplan.com/pricing (2026-06) — confirm in-account.*

| Tier | Price | Includes | Gated (not included) |
|---|---|---|---|
| **Indie** | **Free forever** | Unlimited feedback + subscribers, single-admin workspace, Feedback Board + Changelog + Roadmap, email & in-app announcements | **No team seats, no CSAT/NPS, no Surveys, no API access, no SSO, no integrations, no white-label** |
| **Starter** | **$13/mo** (billed yearly) | Everything in Indie + 3 team seats, CSAT/NPS, **1,000 AI credits/mo**, standard integrations | Surveys, topic analytics, custom domain, remove branding |
| **Business** (most popular) | **$38/mo** (billed yearly) | Everything in Starter + 10 team seats, **5,000 AI credits/mo**, Surveys, topic analytics, custom domain, remove branding | Advanced CSS/JS customization, user segmentation, premium integrations, SAML SSO |
| **Enterprise** | Custom | Unlimited seats, SAML SSO (Okta/Azure AD/Auth0), multi-workspace org, custom contracts | — |

- **30-day free trial** of the Business plan, no card.
- **API/SSO/integrations are plan-gated** — they do **not** exist on the free Indie tier. An integration built against a free workspace will fail auth.
- **AI credits** are the binding constraint on the AI features (auto-categorization, duplicate merging, Sleekmate), not seats.
- Multi-product/multi-workspace was historically capped below Enterprise (recurring user complaint) — verify current limits before consolidating products.

## Integrations

- Native: **Intercom, Help Scout, Zendesk, G2, App Store, Slack** (data flows feedback/tickets → Sleekplan; announcements → Slack/in-app).
- **MCP server** (`https://mcp.sleekplan.com/mcp`) — bidirectional via AI clients (Claude/Cursor/Windsurf): read + create + merge + tag feedback, manage changelog/surveys/votes/users/topics/tags, read workspace config.
- **No Zapier integration is documented** (as of this research) — use the REST API, webhooks, or MCP for automation.
- Custom domains / standalone portal / iframe embedding supported.

## Data model

Sleekplan does **not** publish a separate public REST spec; resources are listed in the docs, full paths/bodies live in-app (Settings → Developer). Key objects (shapes constructed from docs — verify against the live API):

**Feedback post** (the core board item; webhook `action: item.*`):
```json
<!-- Constructed from docs — verify against live API -->
{
  "id": 1234567890,
  "title": "Add dark mode",
  "description": "Please add a dark theme",
  "status": { "id": 3, "name": "Planned" },
  "votes": 42,
  "topics": [{ "id": 9, "name": "UI" }],
  "tags": ["mobile"],
  "author": { "id": 555, "mail": "user@example.com", "name": "user" },
  "created": "1506985999999"
}
```
*(Listing posts: "Returns a list of feedback posts. Sorted by trend by default.")*

**Webhook payload** (verbatim shape from docs — same `data` shape as the REST response for that object):
```json
{
  "product_id": 5456534244,
  "action": "item.create",
  "data": {},
  "timestamp": "1506985999999"
}
```

**JWT SSO payload** (HS256-signed with the SSO secret — verbatim fields):
```json
{ "mail": "user@example.com", "id": "555", "name": "user", "img": "https://…/a.png", "weight": 4, "meta": { "companyName": "Acme" } }
```
Only `mail` is required; sign server-side with `algorithm: 'HS256'`.

## Quick-start recipes

### Recipe 1 — Pull feedback posts via the REST API (cURL + Python)
Auth is `Authorization: Bearer <API_KEY>` (key from `app.sleekplan.com/settings/developer`). The exact path is shown in the in-app reference; the posts list resource returns feedback "sorted by trend by default."

```bash
# List feedback posts (confirm the exact path in Settings → Developer)
curl -s https://api.sleekplan.com/v1/post \
  -H "Authorization: Bearer $SLEEKPLAN_API_KEY"   # base/path: verify in-app reference
```

```python
import os, requests
H = {"Authorization": f"Bearer {os.environ['SLEEKPLAN_API_KEY']}"}
# Confirm the exact base + path + pagination params in Settings → Developer
r = requests.get("https://api.sleekplan.com/v1/post", headers=H, timeout=30)
r.raise_for_status()
for post in r.json().get("data", []):
    print(post["id"], post.get("title"), post.get("votes"))
```
Gotcha: don't invent endpoints — Sleekplan publishes no public spec, so confirm the base URL, path, and pagination params in the in-app reference. Keep the key server-side.

### Recipe 2 — Receive + verify a webhook (no HMAC — secret GET param)
Register the endpoint in **Settings → Developer → Webhooks** with a secret query param. Sleekplan does **not** HMAC-sign; you verify by checking that secret.

```python
from flask import Flask, request, abort
import os
app = Flask(__name__)
SECRET = os.environ["SLEEKPLAN_WEBHOOK_SECRET"]

@app.post("/webhooks/sleekplan")
def hook():
    if request.args.get("key") != SECRET:   # the ?key= you registered
        abort(401)
    e = request.get_json(force=True)         # {product_id, action, data, timestamp}
    action, data = e["action"], e["data"]    # e.g. "item.create", "vote.create"
    # idempotency: dedupe on data["id"] + e["timestamp"]
    return ("", 200)                          # MUST return 2xx
```
Register URL as `https://you.app/webhooks/sleekplan?key=MY_SECRET_KEY`. Events: `item.create|update|delete`, `comment.create|update|delete`, `vote.create`, `subscription.create|delete`, `user.create|update|delete`, `changelog.create|update|subscribe`, `satisfaction.create`. No documented retry — return `2xx` quickly and process async.

### Recipe 3 — Connect the Sleekplan MCP server to Claude Code
```bash
claude mcp add sleekplan --transport streamable-http https://mcp.sleekplan.com/mcp
# then launch Claude Code and run:  /mcp   (opens a browser to authorize via OAuth 2.1)
```
`claude_desktop_config.json`:
```json
{ "mcpServers": { "sleekplan": { "url": "https://mcp.sleekplan.com/mcp" } } }
```
Auth is **OAuth 2.1 with PKCE + dynamic client registration**; on first connect a browser opens to sign in and pick a workspace; only access tokens reach the client. Exposed tools: feedback (list/create/get/update/delete/stats/find-similar/merge/tag), comments, changelog, surveys, votes, users, topics, tags, workspace config.

### Recipe 4 — Identify a logged-in user (JWT SSO) so feedback isn't anonymous
```javascript
const jwt = require('jsonwebtoken');
const key = process.env.SLEEKPLAN_SSO_KEY;     // server-side ONLY (Settings → Developer)
function createSSOToken(u) {
  return jwt.sign(
    { mail: u.mail, id: u.id, name: u.name, img: u.imgStr, weight: 4, meta: { companyName: u.cName } },
    key, { algorithm: 'HS256' }
  );
}
```
Front-end: set `window.SLEEK_USER` before the snippet loads, call `$sleek.setUser()` after the `sleek:init` event, assign a function to `$sleek.sso`, or (standalone/iframe) pass `?sso=YOURTOKEN`. Without SSO, board votes/ideas are anonymous.

## Integration patterns

- **Sync architecture:** Prefer **webhooks** (real-time `item.*`/`vote.*`/`comment.*`/`changelog.*`/`satisfaction.create`) over polling; reconcile with a periodic full read of posts. Because `data` mirrors the REST shape, one mapper handles both webhook + API payloads. Dedupe on entity `id` + `timestamp`.
- **Auth selection (four mechanisms):** **JWT SSO (HS256)** to identify widget users, **API key (Bearer)** for the REST API, **OAuth 2.1 (PKCE)** for the MCP server, and **secret GET-param tokens** for webhooks + Canvas. Use the right one per surface — an SSO token won't authenticate REST calls.
- **Webhook hardening:** the secret is in the URL — keep it private, rotate by re-registering, and IP-allowlist where possible since there's no signature to verify.
- **AI-client workflow:** the MCP server lets Claude list, find-similar, merge, and tag feedback directly — good for triage/dedup without writing API glue, subject to your AI-credit budget.
