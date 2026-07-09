<!-- Source: https://api.landingi.com (REST API) — compiled from Landingi help center (landingi.com/help/webhook-integration/, /help/landingi-platform-overview/), the Landingi WordPress plugin, apitracker.io/a/landingi, and community integration guides (rollout.com). Official endpoint-level docs are partly behind the in-account developer area; paths/versions below are community-documented and MUST be verified against your account's API docs. -->

# Landingi API Reference

> Landingi's complete, authoritative endpoint reference lives in the in-app developer area (API tokens + API Reference, with Postman/Insomnia collections and an OpenAPI spec, per apitracker.io). This file captures what is publicly documented. Where a shape or path is reconstructed, it is marked `<!-- Constructed -->` — verify before relying on it.

## Base URL

- `https://api.landingi.com/v1` — used with **API key** auth (`X-Api-Key` header)
- `https://api.landingi.com/v2/` — used with **OAuth 2.0** Bearer auth

Community sources show both versions and both `/landing_pages` and `/landing-pages` path styles. Confirm the active version + path for your account.

## Authentication

### Option A — API key (server-to-server)

Generate an API token in the Landingi dashboard (Integrations → API tokens). Send it on every request:

```
X-Api-Key: <YOUR_API_KEY>
```

```bash
curl -s "https://api.landingi.com/v1/landing_pages" \
  -H "X-Api-Key: $LANDINGI_API_KEY" \
  -H "Accept: application/json"
```

### Option B — OAuth 2.0 (authorization code grant, for apps acting on other accounts)

1. **Authorize** — redirect the user to:

```
GET https://api.landingi.com/oauth/authorize
    ?response_type=code
    &client_id=<CLIENT_ID>
    &redirect_uri=<REDIRECT_URI>
    &scope=read_landing_pages
    &state=<CSRF_TOKEN>
```

2. **Exchange the code for tokens** — POST to the token endpoint:

```
POST https://api.landingi.com/oauth/token
grant_type=authorization_code
code=<AUTH_CODE>
client_id=<CLIENT_ID>
client_secret=<CLIENT_SECRET>
redirect_uri=<REDIRECT_URI>
```

3. **Refresh** an expired access token:

```
POST https://api.landingi.com/oauth/token
grant_type=refresh_token
refresh_token=<REFRESH_TOKEN>
client_id=<CLIENT_ID>
client_secret=<CLIENT_SECRET>
```

4. **Call the API** with the Bearer token:

```
Authorization: Bearer <ACCESS_TOKEN>
```

Security: always use HTTPS, send a `state` parameter to prevent CSRF, and store tokens securely.

## Core endpoints

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | `/landing_pages` | List landing pages | key / OAuth |
| GET | `/landing_pages/{id}` | Get one landing page | key / OAuth |
| POST | `/landing_pages` | Create a landing page | key / OAuth |
| PUT | `/landing_pages/{id}` | Update a landing page | key / OAuth |
| DELETE | `/landing_pages/{id}` | Delete a landing page | key / OAuth |
| GET | `/forms/{formId}/submissions` | List submissions (leads) for a form | key / OAuth |
| POST | `/leads` | Create a lead | key / OAuth |

### List landing pages

```bash
curl -s "https://api.landingi.com/v1/landing_pages" \
  -H "X-Api-Key: $LANDINGI_API_KEY"
```

<!-- Constructed — verify against live API -->
```json
{
  "data": [
    {
      "id": "lp_8421",
      "name": "Spring Webinar Registration",
      "url": "https://go.example.com/spring-webinar",
      "status": "published",
      "created_at": "2026-06-01T10:22:00Z",
      "updated_at": "2026-06-20T14:03:00Z"
    }
  ]
}
```

### Get form submissions (leads)

```bash
curl -s "https://api.landingi.com/v1/forms/frm_902/submissions" \
  -H "X-Api-Key: $LANDINGI_API_KEY"
```

<!-- Constructed — verify against live API -->
```json
{
  "data": [
    {
      "id": "sub_55123",
      "form_id": "frm_902",
      "landing_page_id": "lp_8421",
      "submitted_at": "2026-06-21T09:15:42Z",
      "fields": { "email": "jane@example.com", "name": "Jane Doe", "company": "Acme Co" }
    }
  ]
}
```

### Create a lead

<!-- Constructed — verify against live API -->
```bash
curl -s -X POST "https://api.landingi.com/v1/leads" \
  -H "X-Api-Key: $LANDINGI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "email": "jane@example.com", "name": "Jane Doe", "source": "api" }'
```

## JavaScript client (axios)

```javascript
require('dotenv').config();
const axios = require('axios');

const landingiApi = axios.create({
  baseURL: 'https://api.landingi.com/v1',
  headers: { 'X-Api-Key': process.env.LANDINGI_API_KEY }
});

// Example: fetch submissions for a form
const { data } = await landingiApi.get('/forms/frm_902/submissions');
```

(Keep keys in environment variables, wrap calls in try/catch, and retry on HTTP 429.)

## Pagination

Not authoritatively documented publicly. List endpoints return a `data` array (envelope shape per community guides). Check response headers and any `page`/`limit`/`cursor` query params against your account's API docs before assuming a pattern.

## Rate limits

- The API enforces rate limiting and returns **HTTP 429** when exceeded.
- Honor a `Retry-After` header if present; otherwise use exponential backoff (e.g. `2 ** attempt` seconds) and cap concurrency.
- No published per-minute quota — measure and stay conservative.

```python
if r.status_code == 429:
    wait = int(r.headers.get("Retry-After", 2 ** attempt))
    time.sleep(wait)
```

## Error responses

Standard HTTP status codes: `401` (bad/missing key or expired token), `403` (insufficient scope/plan), `404` (unknown id), `422` (validation), `429` (rate limited), `5xx` (server). Error bodies are JSON; capture a live example to confirm the exact shape.

## Webhooks (form-submission)

Landingi webhooks are configured **per form**, not at the account level, and fire on **form submission**.

Setup (in the page editor): open the form **Settings → Integrations**, search **Webhook**, then:

1. **Request URL** — your endpoint (click the plus icon to add multiple URLs).
2. **Method** — **GET** (fields appended to the URL as query params) or **POST** (fields in the request body).
3. **Field mapping** — connect each Landingi form field to your server-side field name.
4. **Request headers** — optional key/value pairs, e.g. `API_KEY: 1234-abcd-5678` (use as a shared-secret check).
5. **Request parameters** — optional static key/value pairs sent with every submission, e.g. `source:landingi` (behave like invisible hidden fields).
6. **Save and publish** the page for the webhook to go live.

Notes:
- **No published HMAC signature** — there is no documented signing scheme. Authenticate inbound calls with the custom-header shared secret you set above, and/or allowlist source IPs.
- **Delivery is not guaranteed** — pair webhooks with a periodic `GET /forms/{formId}/submissions` reconciliation.
- A `Webhooks management API` is referenced by third-party listings (apitracker) — confirm availability in-account.

<!-- Constructed — verify against live payload -->
```json
// POST body delivered to your Request URL on submit (mapped fields + static params)
{ "email": "jane@example.com", "name": "Jane Doe", "source": "landingi" }
```

## Orbit MCP server (AI/programmatic interface)

- **Orbit** is Landingi's Model Context Protocol (MCP) server: it connects **Lunar** (AI page generator) and **Solis** (AI insights) to an LLM client (Claude, Cursor, etc.), so an agent can generate pages, pull performance insights, and manage campaigns without leaving the AI workspace.
- Plan-gated to **Scale+**; **in development** at time of research — verify current availability and the connection string in-account before building against it.

## WordPress plugin

The `landingi-landing-pages` WordPress plugin publishes Landingi pages on your WordPress domain. Connect it by generating an **API token** in Landingi and pasting it into the plugin settings.

## Gaps

- Exact, version-locked endpoint catalog, request/response schemas, pagination params, and error-body shapes live in the in-account developer area (API Reference + Postman/Insomnia collections + OpenAPI spec) and were not publicly fetchable — the shapes above marked `<!-- Constructed -->` must be verified against a live call.
- API version (`v1` vs `v2`) and path style (`/landing_pages` vs `/landing-pages`) differ across community sources — confirm the active surface for your account.
- Webhook payload schema and any signing mechanism are undocumented publicly — capture a live sample.
