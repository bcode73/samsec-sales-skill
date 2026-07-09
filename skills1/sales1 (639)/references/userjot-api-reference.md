<!-- Source: https://userjot.com/docs/api (captured 2026-06-29) + userjot.com/docs, userjot.com/pricing -->

# UserJot API Reference

UserJot exposes a REST API, webhooks, and an MCP server. This file captures what is **confirmed verbatim** from the live API docs plus the developer context needed to build against it. The docs page is JS-rendered and lazy-loads sections beyond Boards, so endpoint bodies past the Boards module are listed as **confirmed-to-exist but unconfirmed-shape** — see the **Gaps** section and confirm in the live docs / in-account before relying on them. Do not invent endpoint paths or fields.

## Authentication

- **Scheme:** Bearer token — `Authorization: Bearer <token>`
- **Base URL:** `https://api.userjot.com/v1`
- Generate the token in your UserJot workspace settings; keep it server-side.
- **Plan-gating:** API access appears to fall under the "integrations" cap — Free has none, Starter allows 1, Professional unlimited. Verify in-account.

### Auth quick-start (simplest GET)
```bash
curl -s https://api.userjot.com/v1/boards \
  -H "Authorization: Bearer $USERJOT_TOKEN"
```

## Boards (confirmed verbatim)

| Method | Path | Description |
|---|---|---|
| `GET` | `/boards` | List all boards for the organization. Response: `{ "boards": [...] }` |
| `POST` | `/boards` | Create a board. Body: `{ "name": "string (1-255 chars)", "color": "BoardColor enum" }`. Response: `{ "board": {...} }` |
| `GET` | `/boards/{board_id}` | Get a board |
| `PATCH` | `/boards/{board_id}` | Update a board |
| `DELETE` | `/boards/{board_id}` | Delete a board |

**Notes (from docs):**
- Board **slugs auto-generate**.
- Board **names must be unique per organization** (duplicate → `409`).
- **Default board type:** `public` (private boards require Starter+).
- **`BoardColor` enum** includes: `gray`, `gold`, `bronze`, `brown`, `yellow` (and others — confirm full set in docs).

### Example — create a board
```bash
curl -s -X POST https://api.userjot.com/v1/boards \
  -H "Authorization: Bearer $USERJOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Feature Requests","color":"gold"}'
```
```json
<!-- Constructed from documented field list — verify against live API -->
{ "board": { "id": "brd_...", "name": "Feature Requests", "slug": "feature-requests", "color": "gold", "type": "public" } }
```

## Posts / "requests" and Changelogs (confirmed to exist)

The docs explicitly state that **only `POST /requests` and `POST /changelogs` support the optional `Idempotency-Key` header** — which confirms these two write endpoints exist:

| Method | Path | Description | Idempotency-Key |
|---|---|---|---|
| `POST` | `/requests` | Create a feedback post (the product calls these "posts"; the API resource is **requests**) | ✅ optional |
| `POST` | `/changelogs` | Create a changelog entry | ✅ optional |

- Send a stable UUID in `Idempotency-Key` so retries don't double-create.
- **List/get/update/delete paths and full request/response bodies for these resources are JS-rendered and were not captured** — confirm in the live docs.

## Idempotency

```bash
curl -s -X POST https://api.userjot.com/v1/requests \
  -H "Authorization: Bearer $USERJOT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 6f9619ff-8b86-d011-b42d-00cf4fc964ff" \
  -d '{"board_id":"brd_123","title":"Add dark mode"}'
```
Honored **only** on `POST /requests` and `POST /changelogs`.

## Status codes (confirmed verbatim)

| Code | Meaning |
|---|---|
| `200` / `201` | Success |
| `401` | Missing/invalid API token |
| `409` | Duplicate name **or quota exceeded** |
| `422` | Request validation failed |
| `429` | Rate limit exceeded — **check the `Retry-After` header** |
| `500` | Server error |

### Rate-limit retry snippet
```python
import time, requests

def call(method, url, **kw):
    while True:
        r = requests.request(method, url, **kw)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", "1")))
            continue
        return r
```

## Pagination

Not captured verbatim (JS-rendered). Boards return a `{ "boards": [...] }` array. Confirm whether list endpoints use cursor/offset/page params in the live docs before paging large result sets.

## Webhooks

Confirmed to exist (UserJot markets "webhooks" as part of its developer surface and as a supported integration). **Event list, payload schema, and signature/verification method were not captured** (JS-rendered). Before building a receiver:
1. Register the endpoint in-app and **capture a live delivery** to learn the payload shape.
2. **Don't assume HMAC** — confirm the signing scheme in the live docs; until then secure by endpoint-URL secrecy + IP allowlist + a shared secret.
3. Return `2xx` promptly and process async; dedupe on the entity id + event id/timestamp.

## MCP server

UserJot ships an **MCP server** so AI agents can triage feedback, update the roadmap, and publish changelogs. Setup guides exist for **Claude Code, Cursor, Codex, ChatGPT, and Windsurf** (`userjot.com/docs` → MCP). The exact endpoint URL / `claude mcp add` command was not captured — grab it from the live MCP docs rather than hard-coding an unverified URL.

## SDKs

- **Widget SDK (JavaScript):** embed the in-app widget; methods include initialization, **`identify`** (attach feedback to a logged-in user), programmatic open/close, and state management. Reference: `userjot.com/docs/widget-sdk-reference` (JS-rendered — confirm method signatures live).
- **Swift SDK (iOS):** `github.com/UserJot/userjot-ios` — overview, installation, authentication, common flows.

## Integrations (confirmed)

Slack, Linear, Discord, webhooks, REST API, and an MCP server. Native connectors are plan-gated (1 on Starter, unlimited on Professional).

## Gaps

- **List/get/update/delete bodies for `/requests`, comments, votes, users, and `/changelogs`** — referenced/confirmed-to-exist but shapes are JS-rendered; confirm in live docs.
- **Webhook event names + payload schema + signature scheme** — not captured.
- **MCP server endpoint URL / setup command** — not captured (guides exist per client).
- **Pagination parameters** for list endpoints — not captured.
- **Full `BoardColor` enum** — only a partial list captured.
- The docs are being migrated ("This route has not been migrated into the new marketing app yet" on some sub-paths); `userjot.com/docs/api` is the single live API reference page. Re-verify before relying on any uncaptured detail.
