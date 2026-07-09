<!-- Source: https://developers.memberstack.com/admin-rest-api/quick-start -->
<!-- Source: https://developers.memberstack.com/admin-rest-api/member-actions -->
<!-- Source: https://developers.memberstack.com/admin-rest-api/verification -->
<!-- Source: https://docs.memberstack.com/hc/en-us/articles/7329156946587-Webhooks -->

# Memberstack Admin REST API Reference

> Captured verbatim from the Memberstack 2.0 developer docs (research baseline 2026-06-22). Memberstack has two developer surfaces: the **DOM package** (front-end JS, public key, runs in the browser for login/signup/gating) and the **Admin package** (server-side — a **REST API** and a **Node.js** library). This file covers the **Admin REST API**. There is **no MCP server**.

## Base URL

```
https://admin.memberstack.com
```

## Authentication

Secret keys passed in the **`X-API-KEY`** header. Two key types:

- **Test mode** — prefix `sk_sb_` — development; limited to **50 test members**.
- **Live mode** — prefix `sk_live_` (also seen as `sk_`) — production; processes real charges.

> "Your secret keys carry administrative privileges, so keep them secure and use them in **server-side environments only**." Store in env vars — never in client-side code, public repos, or a CMS. (The browser-side DOM package uses a separate **public** key.)

```javascript
fetch('https://admin.memberstack.com/members', {
  headers: { 'X-API-KEY': 'sk_sb_your_secret_key' }
})
```

## Rate limiting

**25 requests/second.** Exceeding it returns **`429`**. Back off and retry.

## Error handling

Errors return JSON with `code` + `message`:

```json
{ "code": "generic-message", "message": "Human-readable description" }
```

Status codes: `400` bad request/invalid input · `401` secret key doesn't match any app · `429` rate limit. **A non-existent member returns `200` with `"data": null`** (not `404`) — handle this in code.

## Pagination (list endpoints)

Cursor-based: `after` (number), `first`/`limit` (max **100**), `order` (ASC/DESC). Response includes `totalCount`, `endCursor`, `hasNextPage`, and a `data` array. Loop while `hasNextPage`, passing `endCursor` as the next `after`.

## Member endpoints

### List members
`GET /members` — params: `after`, `order` (ASC/DESC), `first`/`limit` (max 100), `includeJSON`.

### Get member
`GET /members/:id_or_email` — by ID (`mem_*`) or URL-encoded email. Param: `include` (comma-separated relations, e.g. `teams`). Returns `200` + `"data": null` if not found.

```bash
curl https://admin.memberstack.com/members/mem_abc123 \
  -H "X-API-KEY: sk_sb_your_secret_key"
```

### Create member
`POST /members` — body:
- `email` (required)
- `password` (required unless passwordless auth enabled)
- `plans` (array of plan objects)
- `customFields`, `metaData`, `json` (objects)
- `loginRedirect` (string)

### Update member
`PATCH /members/:id` — body: `email`, `customFields`, `metaData`, `json`, `loginRedirect`, `verified` (boolean), `profileImage`.

> **Merge semantics (footgun):** `customFields` and `metaData` are **shallow-merged**, but **`json` is fully replaced**. To avoid wiping `json`, read it first, merge in app code, then write the full object back.

### Delete member
`DELETE /members/:id` — optional body: `deleteStripeCustomer` (boolean), `cancelStripeSubscriptions` (boolean). Returns `"data": { "id": "mem_*" }`.

## Plan endpoints (free plans)

### Add free plan
`POST /members/:id/add-plan` — body `planId` (required, `pln_*`). Returns `200`, no body.

### Remove free plan
`POST /members/:id/remove-plan` — body `planId` (required, `pln_*`). Returns `200`, no body.

> These manage **free** plan connections. **Paid** plans run through Stripe checkout (initiated via the front-end DOM package), not a direct Admin REST "add paid plan" call.

## Token & webhook verification

- **JWT verification:** `POST /members/verify-token` — send a member's JWT, get back decoded payload (member ID, issued-at, expiry, audience). Use this to gate **your own backend API** by validating the logged-in member's token.
- **Webhook signature verification:** ⚠️ **NOT supported through the REST API.** You must use the **Node.js Admin Package** to verify webhook signatures. If you only have the REST API, you can receive webhook POSTs but cannot cryptographically verify them via REST — verify out-of-band (e.g. re-fetch the member by ID via `GET /members/:id`) or use the Node package.

## Webhooks

Enabled in the dashboard **Devtools** section. Each event sends a **POST** (JSON) to your endpoint.

**Events:**
- `member.created` — fires after a new member is created (payload: member `id`, auth email, metaData, customFields)
- `member.updated` — member data changed
- `member.deleted` — member removed
- `member.plan.added` — a plan connection was created for a member (V2 supports multiple plans; fires per plan added — via the DOM package a single signup with multiple plans can fire once with a `plans` array)
- `member.plan.updated` — a plan status changed
- `member.plan.canceled` — a plan was canceled
- `team.member.added` — a member added to a team
- `team.member.removed` — a member removed from a team

## Data model

```json
// Member
{
  "id": "mem_abc123",
  "auth": { "email": "jane@example.com" },
  "verified": true,
  "customFields": { "company": "Acme" },   // shallow-merged on PATCH
  "metaData": { "source": "webflow" },       // shallow-merged on PATCH
  "json": { "prefs": { "theme": "dark" } },  // FULLY REPLACED on PATCH
  "plans": [ { "id": "pln_xyz789", "status": "ACTIVE" } ]
}
```

```json
// List response envelope
{ "data": [ /* members */ ], "totalCount": 1234, "endCursor": 50, "hasNextPage": true }
```

## Native / iPaaS integrations

Webflow (script + data attributes), WordPress, Stripe (payments), Zapier, Pipedream, plus the REST + Node admin packages and the front-end DOM package.
