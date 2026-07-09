<!-- Source: https://developer.infusionsoft.com/docs/restv2/ , https://developer.infusionsoft.com/getting-started-oauth-keys/ , https://developer.infusionsoft.com/rest-hook-documentation/ , https://rollout.com/integration-guides/keap/api-essentials , https://aeroleads.com/blog/keap-api-getting-started-with-rest-api-integrations/ -->
<!-- The official interactive REST docs (Stoplight) are JS-rendered and could not be fetched verbatim; endpoint specifics below are assembled from official OAuth/REST-Hook pages plus reputable third-party guides and marked where constructed. Re-verify against the live interactive docs. -->

# Keap REST API Reference

## API versions & base URLs

- **REST v2 (current/default)**: `https://api.infusionsoft.com/crm/rest/v2/`
- **REST v1 (still current)**: `https://api.infusionsoft.com/crm/rest/v1/`
- **Legacy XML-RPC**: still available but deprecated for new work. REST cuts the number of calls roughly in half vs XML-RPC.
- The developer portal lives at `developer.infusionsoft.com` (a.k.a. `developer.keap.com`).

## Authentication

Three auth methods:

### 1. OAuth 2.0 (recommended for apps / multi-account)

- **Authorize**: redirect the user to
  `https://accounts.infusionsoft.com/app/oauth/authorize` (older docs show `https://signin.infusionsoft.com/app/oauth/authorize`)
  with query params: `client_id`, `redirect_uri` (HTTPS, required), `response_type=code` (default), `scope=full` (default; granular scopes like `contacts.read contacts.write` are available).
- **Token exchange**: `POST https://api.infusionsoft.com/token` (`application/x-www-form-urlencoded`) with `client_id`, `client_secret`, `code`, `grant_type=authorization_code`, `redirect_uri`. Response: `access_token`, `refresh_token`, `expires_in` (seconds).
- **Refresh**: `POST https://api.infusionsoft.com/token` with `grant_type=refresh_token`, `refresh_token`, and header `Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)`. Returns a new access/refresh pair.
- **Token lifetimes** (best-effort): access token ~24h; refresh token ~90 days.
- **Use**: header `Authorization: Bearer <ACCESS_TOKEN>` on every request.

### 2. Personal Access Token (PAT) — single account

Generated from the Keap account. Simpler for internal scripts; lower rate ceiling than OAuth apps.

### 3. Service Account Key — single account, server-to-server

Used alongside PATs for backend automation against one account.

## Auth quick-start (simplest GET)

```bash
curl "https://api.infusionsoft.com/crm/rest/v2/contacts?page_size=1" \
  -H "Authorization: Bearer $KEAP_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

## Rate limits

*Best-effort from research — confirm against current docs/headers.*

| Auth type | Per second | Per minute | Per day (resets 00:00 UTC) |
|---|---|---|---|
| **Personal Access Token** | 10 q/s | 240 q/min | 30,000 |
| **OAuth 2.0 bearer** | (25 q/s spike cap) | 1,500 q/min | 150,000 |

- Global **spike policy: 25 calls/second**.
- OAuth apps are throttled at the **application level** and independently of one another; Keap can adjust an app's throttle on request.
- Some third-party guides cite a simpler "120 requests/minute per application" figure for older app tiers — treat the table above as the upper-bound model and the per-app limit as account/tier-dependent.
- On `429`, back off exponentially and retry.

## Endpoint groups

Representative resources (v1 and/or v2). Exact paths and field availability differ by version and by Max Classic vs new Keap — verify in the interactive docs.

| Group | Typical operations | Notes |
|---|---|---|
| **Contacts** | `GET/POST /contacts`, `GET/PATCH/DELETE /contacts/{id}` | Core object. v2 supports richer field control. |
| **Contact Tags** | `GET /contacts/{id}/tags`, `POST /contacts/{id}/tags`, `DELETE /contacts/{id}/tags/{tagId}` | Applying a tag is the most common automation trigger. |
| **Tags** | `GET/POST /tags`, `GET /tags/{id}` | Categories + tags. |
| **Companies** | `GET/POST /companies`, `GET/PATCH /companies/{id}` | |
| **Opportunities** | `GET/POST /opportunities`, `GET/PATCH /opportunities/{id}` | Sales pipeline / stages. |
| **Campaigns** | `GET /campaigns`, `GET /campaigns/{id}`, add/remove contacts to a sequence | **Read/membership only** — sequence content is UI-built. |
| **Orders** | `GET/POST /orders`, `GET /orders/{id}` | E-commerce orders. |
| **Invoices / Transactions** | `GET /invoices`, `GET /transactions` | Billing. |
| **Subscriptions** | `GET/POST /subscriptions` | Recurring billing. |
| **Products** | `GET/POST /products` | Catalog. |
| **Payments** | `GET /payments` | |
| **Emails** | `POST /emails` (send/queue), `GET /emails` | Send transactional/1:1 email, list sent. |
| **Affiliates** | `GET /affiliates`, commissions/clawbacks | Referral partner program. |
| **Webforms** | `GET /hooks`, webform submissions | Lead capture. |
| **Files / Notes / Tasks / Appointments / Users** | CRUD | Supporting objects. |
| **REST Hooks** | `GET/POST/DELETE /hooks` | Webhook subscriptions (see below). |

## Top-5 endpoint request/response examples

<!-- Constructed from docs + third-party guides — verify against live API -->

### List contacts (GET)
```
GET /crm/rest/v2/contacts?page_size=50&order=date_created
Authorization: Bearer <token>
```
```json
{
  "contacts": [
    { "id": 12345, "given_name": "Dana", "family_name": "Lee",
      "email_addresses": [{ "email": "dana@example.com", "field": "EMAIL1" }],
      "date_created": "2026-06-01T14:22:03.000Z" }
  ],
  "next": "https://api.infusionsoft.com/crm/rest/v2/contacts?page_token=abc123",
  "count": 50
}
```

### Get one contact (GET)
```
GET /crm/rest/v2/contacts/12345
```
Returns the single Contact object (shape as above).

### Create contact (POST)
```
POST /crm/rest/v2/contacts
{ "given_name": "Dana", "family_name": "Lee",
  "email_addresses": [{ "email": "dana@example.com", "field": "EMAIL1" }] }
```
Returns the created Contact with its new `id`.

### Update contact (PATCH)
```
PATCH /crm/rest/v2/contacts/12345
{ "family_name": "Lee-Smith" }
```
Returns the updated Contact.

### Delete contact (DELETE)
```
DELETE /crm/rest/v2/contacts/12345
```
Returns `204 No Content`.

## Pagination

- **v2**: cursor-based — responses include a `next` URL containing a `page_token`; follow it until absent. `page_size` controls page length (up to ~1,000).
- **v1**: offset-based — `?limit=50&offset=100`; responses include `count` and `next`/`previous`.

## Error responses

<!-- Constructed from docs — verify against live API -->
```json
{ "message": "Invalid token", "code": "401" }
```
Standard HTTP status codes: `400` validation, `401` auth, `403` scope, `404` not found, `429` rate-limited, `5xx` server.

## Rate-limit retry snippet

```python
import time, requests

def call(url, headers, attempts=5):
    for i in range(attempts):
        r = requests.get(url, headers=headers)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        time.sleep(2 ** i)        # exponential backoff; respect the 25 req/s spike cap
    raise RuntimeError("rate limited")
```

## REST Hooks (webhooks)

REST Hooks treat webhooks as subscriptions managed via the REST API.

- **Subscribe**: `POST /crm/rest/v1/hooks` with `eventKey` and `hookUrl`. Keap calls your URL with a verification challenge; echo it back to activate (verification handshake required — events only fire once verified).
- **List / delete**: `GET /crm/rest/v1/hooks`, `DELETE /crm/rest/v1/hooks/{key}`.
- **Available event types** (fetch the live list via the API; representative set):
  `contact.add`, `contact.edit`, `contact.delete`,
  `opportunity.add`, `opportunity.edit`, `opportunity.stage_move`,
  `task.add`, `task.edit`,
  `order.add`, `payment.add`, `invoice.paid`,
  `tag.applied`, `tag.removed`,
  `campaign.completed`, `contactGroup.*` (tag category events).
- **Signature**: payloads are signed (HMAC-SHA256 with the application secret); verify before trusting.
- **Payload** (verbatim shape):
  ```json
  {
    "event_key": "<HOOK EVENT KEY>",
    "object_type": "<RESOURCE NAME>",
    "object_keys": [
      { "id": "<RESOURCE ID>", "apiUrl": "<REST API URL>", "timestamp": "<EVENT TIMESTAMP>" }
    ]
  }
  ```
  Up to **1,000** changed objects per payload (same event type only). Payload is ID-only — GET the `apiUrl` for the full record.
- **Delivery / retries**: events are batched. Up to **4 attempts**: (1) ~30–60s after the event (5–10 min for `contactGroup` events), (2) 30–60s after a failure, (3) 5 min after, (4) 30 min after. A retry triggers if the receiver doesn't respond within **30s** or returns status `<200` or `>=400` — **except `410`, which immediately and permanently deactivates the subscription.** After the 4th failed attempt the subscription is marked inactive.

## Gaps

- Verbatim interactive endpoint specs (full field lists, every path) are behind a JS-rendered Stoplight app; the table above is assembled from official OAuth/REST-Hook pages and reputable guides. Verify exact paths/fields in the live interactive docs at `developer.infusionsoft.com/docs/restv2/`.
- Campaign/sequence write coverage is limited and version-dependent — confirm current capability in the Keap Integration Q&A community (`integration.keap.com`).
- Token lifetimes and the precise per-app rate tier are account/tier-dependent — read the `X-RateLimit-*` response headers at runtime.
