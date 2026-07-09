# UserJot Platform Reference

## Overview

UserJot (userjot.com) is an AI-first customer-feedback platform — feedback boards, a public roadmap, and an AI-generated changelog — built for SaaS founders and product teams who want an affordable, **no-per-seat** alternative to Canny and Productboard. Built in public by a solo founder (launched early 2025); stack is Node/TypeScript + PostgreSQL (pgvector for AI) + TanStack on Cloudflare Workers. Its differentiators are unlimited posts/users on every tier (including free), AI duplicate detection + auto-categorization, and a developer surface that includes a REST API, webhooks, and an **MCP server** so AI agents can run feedback triage.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Feedback boards** | Users submit posts ("requests"), upvote, and comment; AI dedupes and auto-categorizes | **API-accessible** (boards CRUD confirmed; posts via `/requests`), **webhook-accessible**, widget-embeddable |
| **Voting** | Upvotes on posts signal demand | API-accessible (read posts + counts); webhook events on votes |
| **Comments** | Threaded discussion on posts | API-accessible (referenced; confirm path in live docs) |
| **Public roadmap** | Posts grouped by status into roadmap columns | Driven by post status — set via API/UI; surfaced on the public board |
| **Changelog** | AI-assisted release notes; notifies relevant voters | **API-accessible** (`POST /changelogs`, idempotent), UI authoring |
| **In-app widget** | Embeds boards/roadmap/changelog; collects feedback in-product | **Widget SDK** (JS): init, `identify`, programmatic open/close + state |
| **Swift SDK** | Native iOS feedback capture + auth | SDK (`github.com/UserJot/userjot-ios`) |
| **AI layer** | Duplicate detection, auto-categorization, AI changelog drafting | Built-in (all plans); also drivable via the MCP server |
| **MCP server** | Lets AI agents triage feedback, update the roadmap, publish changelogs | **MCP** — setup guides for Claude Code / Cursor / Codex / ChatGPT / Windsurf |
| **SSO / automatic login** | Auto-authenticate users into the board | UI/SDK config — **plan-gated (Starter+)** |
| **Native integrations** | Slack, Linear, Discord | Per-integration config — **plan-gated** (1 on Starter, unlimited on Professional) |

## Pricing, limits & plan gates

*Best-effort (2026-06) — confirm at userjot.com/pricing.*

| | **Free** ($0) | **Starter** ($29/mo) | **Professional** ($59/mo) |
|---|---|---|---|
| Posts / users | Unlimited | Unlimited | Unlimited |
| Feedback boards | 2 | 5 | Unlimited |
| Admin roles | 3 | — | Unlimited |
| Public roadmap + AI changelog + widget | ✅ | ✅ | ✅ |
| AI duplicate detection + auto-categorization | ✅ | ✅ | ✅ |
| Custom domain | ❌ (subdomain only) | ✅ | ✅ |
| Guest posting | ❌ | ✅ | ✅ |
| Private boards | ❌ | ✅ | ✅ |
| Custom branding | basic | ✅ | ✅ |
| SSO (automatic login) | ❌ | ✅ | ✅ |
| Integrations (Slack/Linear/Discord/**API/webhooks/MCP**) | ❌ none | **1** | Unlimited |
| Advanced / semantic search | ❌ | ❌ | ✅ |
| Public identity masking | ❌ | ❌ | ✅ |

**Integration gate is the one that bites developers.** Free has *no* integrations; the API, webhooks, and MCP server appear to fall under the integration cap (1 on Starter, unlimited on Professional). Verify in-account exactly which surfaces count before building against a free workspace.

**Rate limits:** `429` responses carry a **`Retry-After`** header — honor it. Exact per-minute limits aren't published; back off and retry on `429`/`5xx`.

## Integrations

- **Reads from / writes to UserJot:** the REST API (boards, posts/`requests`, changelogs) is bidirectional; webhooks push events out (new post / vote / status change → your endpoint).
- **Native connectors:** Slack, Linear, Discord (e.g. mirror feedback into Linear issues or Slack channels).
- **MCP server:** the AI-agent interface — an agent (Claude Code, Cursor, Codex, ChatGPT, Windsurf) can list/triage feedback, update the roadmap, and publish changelogs.
- **iPaaS:** no first-party Zapier/Make module is documented in research — bridge via webhooks + the REST API, or check the live integrations page.

## Data model

> The Boards object below is from the verbatim API docs. Other shapes are **constructed from documented field lists / product behavior** and must be confirmed against the live API.

**Board** (confirmed shape from `POST /boards`):
```json
<!-- Constructed from docs — verify against live API -->
{
  "board": {
    "id": "brd_...",
    "name": "Feature Requests",
    "slug": "feature-requests",
    "color": "gold",
    "type": "public"
  }
}
```
- `name`: string, 1–255 chars, **unique per organization**
- `color`: `BoardColor` enum (e.g. `gray`, `gold`, `bronze`, `brown`, `yellow`, …)
- `slug`: auto-generated from name
- `type`: defaults to `public` (private boards require Starter+)

**Post / "request"** (the feedback item — create via `POST /requests`):
```json
<!-- Constructed from docs/product behavior — confirm fields/path in live docs -->
{
  "id": "req_...",
  "board_id": "brd_...",
  "title": "Add dark mode",
  "details": "Would love a dark theme for the dashboard",
  "status": "open",
  "vote_count": 42,
  "author": { "id": "usr_...", "name": "Jane", "email": "jane@acme.com" }
}
```
- Status values drive the public **roadmap** columns (e.g. open / planned / in-progress / complete — confirm exact set).

**Changelog entry** (create via `POST /changelogs`):
```json
<!-- Constructed from docs/product behavior — confirm fields/path in live docs -->
{
  "id": "chg_...",
  "title": "Dark mode is here",
  "body": "We shipped dark mode based on your feedback.",
  "published": true,
  "linked_post_ids": ["req_..."]
}
```

## Quick-start recipes

### Recipe 1 — List boards and their posts
**Trigger:** you want to export feedback into your own DB/warehouse.
```bash
# 1. List boards
curl -s https://api.userjot.com/v1/boards \
  -H "Authorization: Bearer $USERJOT_TOKEN"

# 2. List feedback posts (the /requests resource — confirm exact list path/params in live docs)
curl -s "https://api.userjot.com/v1/requests?board_id=brd_123" \
  -H "Authorization: Bearer $USERJOT_TOKEN"
```
```python
import os, requests
H = {"Authorization": f"Bearer {os.environ['USERJOT_TOKEN']}"}
BASE = "https://api.userjot.com/v1"

boards = requests.get(f"{BASE}/boards", headers=H).json()["boards"]
for b in boards:
    posts = requests.get(f"{BASE}/requests", headers=H,
                         params={"board_id": b["id"]}).json()
    print(b["name"], "→", posts)
```
**Gotchas:** the list-posts path/params are JS-rendered in the docs — confirm them in-app. Keep the token server-side.

### Recipe 2 — Create a feedback post idempotently
**Trigger:** you forward feedback from another channel (support, email) into UserJot and must not double-post on retry.
```bash
curl -s -X POST https://api.userjot.com/v1/requests \
  -H "Authorization: Bearer $USERJOT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"board_id":"brd_123","title":"Add dark mode","details":"From support ticket #842"}'
```
```python
import os, uuid, requests
H = {"Authorization": f"Bearer {os.environ['USERJOT_TOKEN']}",
     "Idempotency-Key": str(uuid.uuid4())}
r = requests.post("https://api.userjot.com/v1/requests", headers=H, json={
    "board_id": "brd_123", "title": "Add dark mode",
    "details": "From support ticket #842"})
# 409 => duplicate name OR quota exceeded; 422 => validation; 429 => check Retry-After
print(r.status_code, r.json())
```
**Gotchas:** `Idempotency-Key` is honored **only** on `POST /requests` and `POST /changelogs`. Persist the key with the source record so retries reuse it.

### Recipe 3 — Verify and handle an inbound webhook
**Trigger:** UserJot POSTs new-post / vote / status-change events to your endpoint and you sync them into Slack/CRM.
```python
from flask import Flask, request, abort
app = Flask(__name__)

@app.post("/userjot-webhook")
def hook():
    # UserJot's webhook signing scheme is not captured in research — confirm in live docs.
    # Until confirmed, secure by: a hard-to-guess endpoint URL, IP allowlisting,
    # and/or a shared secret you configure. Verify server-side before trusting.
    event = request.get_json()
    # dedupe on the entity id + a timestamp/event id
    ...
    return "", 200  # return 2xx promptly
```
**Gotchas:** webhook payload schema and signature/verification method are JS-rendered — **capture a live delivery** and confirm the signing scheme in-app before writing verification code. Don't assume HMAC.

## Integration patterns

- **CRM/PM sync:** poll `GET /boards` + posts on a schedule for backfill, then switch to webhooks for deltas. Map UserJot post `status` → your roadmap/issue states; store `req_*` ids to avoid re-creating. For Linear specifically, the native integration may be simpler than building it yourself.
- **Webhook listener:** return `2xx` fast, process async (queue the payload). Dedupe on the entity id (+ event id/timestamp). Verify authenticity with whatever scheme the live docs confirm (URL secrecy + IP allowlist as a baseline).
- **Rate-limit handling:** on `429`, read `Retry-After` and sleep that many seconds; exponential backoff on `5xx`. Batch reads where the API supports filtering by `board_id`.
- **AI triage via MCP:** instead of building categorization yourself, let the MCP server + UserJot's AI layer dedupe/categorize, and have your agent draft changelog entries (`POST /changelogs`) from completed posts.
