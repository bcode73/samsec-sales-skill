<!-- Source: https://developer.systeme.io/reference/api + https://developer.systeme.io/llms.txt + https://help.systeme.io/article/2329-how-to-use-systeme-io-public-api + https://help.systeme.io/article/2323-how-to-create-a-public-api-key-on-systeme-io + https://dlthub.com/context/source/systeme-io -->
<!-- The developer portal (ReadMe.com-hosted) is JS-rendered; reference pages did not return full content via WebFetch. The base URL, auth, endpoint paths, pagination, rate-limit headers, and webhook events below are captured from the official llms.txt index, the help-center articles, and the dltHub loader docs (which document the live API). Request/response JSON is CONSTRUCTED from documented fields and marked — verify against the live API. -->

# Systeme.io Public API Reference

RESTful public API for programmatic access to a Systeme.io account — contacts, tags, funnels, products, orders, subscriptions, campaigns, and webhooks.

## Base URL

`https://api.systeme.io`

Endpoints are namespaced under `/api/<resource>`, e.g. `https://api.systeme.io/api/contacts`.

## Authentication

- **Header:** `X-API-Key: <your public API key>` on every request. (A `Authorization: Bearer <key>` header is also accepted.)
- **Getting a key:** Dashboard → profile **Settings → Public API keys → generate a new key**. Enter a name, choose an **expiration date/time**, and save.
- **Limits:** up to **3 API keys per account**. Keys expire on the date you set — a silently expired key reads as a 401.

## Creating an API key (verbatim from help docs)

> "To generate a new API key, navigate to the profile settings within your Systeme.io dashboard, and generate a new key under the 'Public API keys' section. You can create up to 3 API keys per account. When creating a public API key, enter a name, select an expiration date and time for your API key, and click Save."

## Auth quick-start (simplest call)

List contacts to confirm the key works:

```bash
curl -X GET "https://api.systeme.io/api/contacts?limit=1" \
  -H "X-API-Key: YOUR_API_KEY"
```

## Resources / endpoints

Documented resources (each under `/api/<resource>`), per the official docs index and the dltHub loader:

| Resource | Path | Operations (per docs) |
|---|---|---|
| **Contacts** | `/api/contacts` | list, retrieve, create, update, delete |
| **Tags** | `/api/tags` | list, retrieve, create, update, delete; assign/remove on a contact |
| **Funnels** | `/api/funnels` | list, retrieve (+ funnel steps) |
| **Products** | `/api/products` | list, retrieve |
| **Subscriptions** | `/api/subscriptions` | list, retrieve, handle unsubscription |
| **Campaigns** (newsletters) | `/api/campaigns` | list, retrieve, create, update |
| **Orders** | `/api/orders` | list, retrieve |
| **Webhooks** | `/api/webhooks` | list, register, delete |

> The help docs summarize the operation categories as: (1) Contact & tag management (create, update, delete, list, retrieve); (2) Subscription operations (retrieve resources, handle unsubscription); (3) Automation triggering (via actions like contact creation or tagging); (4) Newsletter management (create, update, list, retrieve).

## Example requests & responses

<!-- Constructed from documented fields — verify exact keys against the live API -->

**Create a contact** — `POST /api/contacts`:
```json
{ "email": "jane@example.com",
  "fields": [ { "slug": "first_name", "value": "Jane" } ] }
```
Response (shape):
```json
{ "id": 1234567, "email": "jane@example.com",
  "registeredAt": "2026-06-20T14:02:00+00:00" }
```

**Create a tag** — `POST /api/tags`:
```json
{ "name": "app-trial" }
```

**Assign a tag to a contact** — `POST /api/contacts/{contactId}/tags`:
```json
{ "tagId": 88 }
```

**List contacts (paginated)** — `GET /api/contacts?limit=100&startingAfter=1234567`:
```json
{ "items": [ { "id": 1234568, "email": "next@example.com" } ], "hasMore": true }
```

**Register a webhook** — `POST /api/webhooks`:
```json
{ "url": "https://yourapp.com/hooks/systeme", "event": "sale.new" }
```

**Error response** (shape):
```json
{ "status": 401, "detail": "Invalid or missing API key" }
```

## Pagination

**Cursor-based.** Use `startingAfter` = the **ID of the last item** you received, plus `limit` to control page size. There are no page numbers. Loop: request a page, take the last item's `id`, pass it as `startingAfter` on the next call, stop when a short/empty page returns.

```
GET /api/contacts?limit=100
GET /api/contacts?limit=100&startingAfter=1234567
GET /api/contacts?limit=100&startingAfter=1234667
...
```

## Rate limits

Communicated via response headers:

| Header | Meaning |
|---|---|
| `X-RateLimit-Limit` | Max requests in the window |
| `X-RateLimit-Remaining` | Requests left in the current window |
| `X-RateLimit-Refill` | When/how the budget refills |
| `Retry-After` | Seconds to wait, returned on `429` responses |

**Retry strategy:** read `X-RateLimit-Remaining` and throttle before it hits 0; on `429`, sleep for `Retry-After` seconds then retry with exponential backoff + jitter.

## Webhooks (events)

Register endpoints via `/api/webhooks` (or the dashboard). Documented events:

- **Contact created**
- **Contact tag added**
- **Contact tag removed**
- **New sale**
- **Sale canceled**

**Handling guidance:** respond `2xx` quickly and process asynchronously; treat delivery as at-least-once and dedupe on the resource id (e.g. order id); log a sample payload per event to confirm exact field names before coding against them.

## Gaps

- The **developer portal is ReadMe.com/JS-rendered** — full per-endpoint request/response schemas were not fetchable via WebFetch. Paths, auth, pagination, rate-limit headers, and webhook events above are sourced from the official `llms.txt` index, the help-center articles, and the dltHub loader docs; **example JSON bodies are constructed and marked**.
- **Exact list data key** (`items` vs another wrapper) is not confirmed in docs — dltHub explicitly advises inspecting a live GET to set the data selector. Verify before relying on it.
- **No OpenAPI/Swagger spec** and **no MCP server** found as of this research.
- Third-party "Rollout" SDK guides (Go/Python) appear partly auto-generated — prefer the official portal + a live test call over those.
