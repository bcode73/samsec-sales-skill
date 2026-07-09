### Omnisend REST API — Comprehensive Reference

**Base URL**: `https://api.omnisend.com/api/`
**Docs**: https://api-docs.omnisend.com/
**Current API version**: 2026-03-15

---

## Authentication

Two authentication methods supported. **Both pass credentials in the `Authorization` header** (re-verified 2026-06-13 — the older `X-API-KEY` header is no longer the documented scheme):

| Method | Header | Use case |
|---|---|---|
| API Key | `Authorization: Omnisend-API-Key YOUR-API-KEY` | Direct integrations, server-to-server |
| OAuth 2.0 | `Authorization: Bearer {access-token}` | Third-party apps, marketplace integrations |

**API Key generation**: app.omnisend.com → Integrations → API keys → create key (`https://app.omnisend.com/integrations/api-keys`). OAuth supports per-scope authorization (e.g. `contacts.read`, `campaigns.write`, `automations.read`).

**OAuth 2.0 flow**: Authorization Code Grant. Submit an integration form to Omnisend to receive OAuth credentials. Redirect users to Omnisend's authorization endpoint, exchange code for token.

**Canonical example request** (current docs):

```shell
curl --request GET \
  --url 'https://api.omnisend.com/api/segments' \
  --header 'Authorization: Omnisend-API-Key YOUR-API-KEY' \
  --header 'Omnisend-Version: 2026-03-15'
```

---

## Versioning

Omnisend uses **header-based versioning**. Include the version header with every request:

```
Omnisend-Version: 2026-03-15
```

Current stable version is **`2026-03-15`** (the prior version was **`v5`**; docs provide a "Migrate from v5 to 2026-03-15" guide). A `2026-preview` version exists for beta features. The base host is `https://api.omnisend.com` and resource paths are prefixed with `/api/` (e.g. `/api/contacts`). If the version header is omitted, the API defaults to the latest stable version.

---

## Request & Response Format

### Requests

- **Content-Type**: `application/json`
- **Methods**: Standard REST — GET for reads, POST for creates, PATCH/PUT for updates, DELETE for deletes

### Response Format

List endpoints return:
```json
{
  "data": [...],
  "paging": {
    "cursors": {
      "after": "opaque_cursor_string",
      "before": "opaque_cursor_string"
    },
    "hasMore": true
  }
}
```

`paging.hasMore` indicates whether more results are available (re-verified 2026-06-13).

Single-record endpoints return:
```json
{
  "data": { ... }
}
```

### Error Responses

Errors follow **RFC 9457 Problem Details**. The `type` field is a `https://problems.omnisend.com/...` URI (re-verified 2026-06-13). Rate-limit (429) errors may include a `retryAfter` field (seconds to wait before retrying):

```json
{
  "type": "https://problems.omnisend.com/rate-limit-exceeded",
  "title": "Rate limit exceeded",
  "status": 429,
  "retryAfter": 30
}
```

Validation errors carry a structured `errors` array:

```json
{
  "type": "https://problems.omnisend.com/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Email address is required",
  "errors": [
    {
      "field": "email",
      "message": "Email address is required"
    }
  ]
}
```

API errors are also logged in the Omnisend app under the API Issues section for troubleshooting.

---

## Pagination

**Type**: Cursor-based (opaque tokens)

| Parameter | Type | Description |
|---|---|---|
| `after` | string | Cursor from `paging.cursors.after` — fetch next page |
| `before` | string | Cursor from `paging.cursors.before` — fetch previous page |
| `limit` | integer | Results per page (default varies by endpoint) |

**How to paginate**:
1. Make the initial request without cursor params
2. If `paging.cursors.after` exists, pass it as `?after={cursor}` for the next page
3. Continue until no `after` cursor is returned

---

## Rate Limits

Rate limits are applied **per endpoint type** (re-verified 2026-06-13 against the official rate-limit page):

| Endpoint type | Limit |
|---|---|
| List / GET collection | 100 requests / minute |
| Create / Update / Delete (POST, PATCH, PUT, DELETE) | 15 requests / minute |
| Analytics | 10 requests / minute, 55 requests / day |

When a limit is exceeded the API returns **HTTP 429** with an RFC 9457 body whose `type` is `https://problems.omnisend.com/rate-limit-exceeded`; some endpoints include a `retryAfter` field (seconds). Use the **`/batches`** endpoint (up to 100 operations per batch) for bulk contact/product work to stay under the 15/min write limit. Implement exponential backoff on 429 responses.

---

## All API Endpoints

All paths are relative to `https://api.omnisend.com/api/`.

---

### Contacts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/contacts` | List all contacts with optional filters |
| GET | `/contacts/{contactID}` | Get a single contact by ID |
| POST | `/contacts` | Create a contact — **upsert**: if a contact with the same email already exists it is updated instead (201 for new, 200 for update) |
| PATCH | `/contacts/{contactID}` | Update a contact by ID |
| PATCH | `/contacts` | Update a contact by email identifier (no ID needed) |
| POST | `/contacts/tags` | Batch add tags to contacts |
| DELETE | `/contacts/tags` | Batch remove tags from contacts |

> **Re-verified 2026-06-13**: There is **no documented `DELETE /contacts/{contactID}`** endpoint — individual contacts cannot be deleted via the public API (suppress/unsubscribe by PATCHing `status` instead, or remove in-app). Tag operations are **batch endpoints** (`/contacts/tags`), not the per-contact `/contacts/{id}/tags/{tag}` paths shown in older docs.

**Contact object fields**:

| Field | Type | Description |
|---|---|---|
| `contactID` | string | Unique contact identifier |
| `email` | string | Contact email address |
| `phone` | string | Contact phone number (E.164 format) |
| `firstName` | string | First name |
| `lastName` | string | Last name |
| `tags` | array | Array of tag strings |
| `status` | string | Subscription status: `subscribed`, `unsubscribed`, `nonSubscribed` |
| `smsStatus` | string | SMS subscription: `subscribed`, `unsubscribed`, `nonSubscribed` |
| `createdAt` | datetime | Creation timestamp (ISO 8601) |
| `customProperties` | object | Custom key-value pairs |

**Example — Create a contact**:
```bash
curl -X POST https://api.omnisend.com/api/contacts \
  -H "Authorization: Omnisend-API-Key YOUR-API-KEY" \
  -H "Omnisend-Version: 2026-03-15" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "tags": ["shopify", "vip"],
    "status": "subscribed"
  }'
```

---

### Products

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | List all products |
| GET | `/products/{productID}` | Get a single product |
| POST | `/products` | Create/sync a product |
| PUT | `/products/{productID}` | Update/replace a product (re-verified 2026-06-13 — update uses **PUT**, not PATCH) |
| DELETE | `/products/{productID}` | Delete a product |

> For bulk product create/update, submit a `/batches` operation (up to 100 actions, each with its own `method` of POST or PUT).

**Product object fields**:

| Field | Type | Description |
|---|---|---|
| `productID` | string | Unique product identifier (from your store) |
| `title` | string | Product name |
| `productUrl` | string | Product page URL |
| `imageUrl` | string | Product image URL |
| `price` | number | Product price |
| `currency` | string | ISO 4217 currency code |
| `status` | string | `inStock`, `outOfStock`, `discontinued` |
| `vendor` | string | Product vendor/brand |
| `variants` | array | Array of variant objects (size, color, etc.) |

---

### Product Categories

Re-verified 2026-06-13 — the resource path is **`/product-categories`** (not `/categories`).

| Method | Endpoint | Description |
|---|---|---|
| GET | `/product-categories` | List all product categories |
| GET | `/product-categories/{categoryID}` | Get a single category |
| POST | `/product-categories` | Create a category |
| PATCH | `/product-categories/{categoryID}` | Update a category |
| DELETE | `/product-categories/{categoryID}` | Delete a category |

---

### Campaigns

| Method | Endpoint | Description |
|---|---|---|
| GET | `/campaigns` | List all campaigns |
| GET | `/campaigns/{campaignID}` | Get a single campaign with stats |
| POST | `/campaigns` | Create a new campaign |
| PATCH | `/campaigns/{campaignID}` | Update a campaign |
| POST | `/campaigns/{campaignID}/actions/send` | Send a campaign |
| POST | `/campaigns/{campaignID}/actions/cancel` | Cancel a scheduled/sending campaign |

**Campaign statuses**: `draft`, `scheduled`, `sending`, `sent`, `cancelled`

---

### Events

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Send a custom event for a contact |

**Event tracking** is critical for custom ecommerce platforms without native integrations. Send events for:
- Page views (product viewed, category viewed)
- Cart events (added to cart, cart updated, cart abandoned)
- Order events (placed order, order fulfilled, order cancelled)
- Custom events (any action relevant to your automations)

**Payload shape (re-verified 2026-06-13)**: the contact is identified by a nested `contact` object and an **`origin`** field is required. Recommended (predefined ecommerce) events additionally require an `eventVersion`; custom events do not.

**Example — Track a custom cart event**:
```bash
curl -X POST https://api.omnisend.com/api/events \
  -H "Authorization: Omnisend-API-Key YOUR-API-KEY" \
  -H "Omnisend-Version: 2026-03-15" \
  -H "Content-Type: application/json" \
  -d '{
    "eventName": "added to cart",
    "origin": "api",
    "contact": {
      "email": "jane@example.com"
    },
    "properties": {
      "productID": "prod_123",
      "productTitle": "Blue T-Shirt",
      "price": 29.99,
      "currency": "USD"
    }
  }'
```

---

### Segments

| Method | Endpoint | Description |
|---|---|---|
| GET | `/segments` | List all segments |
| GET | `/segments/{segmentID}` | Get a segment with contact count |
| POST | `/segments` | Create a new segment |
| PATCH | `/segments/{segmentID}` | Update a segment |
| DELETE | `/segments/{segmentID}` | Delete a segment |

*Re-verified 2026-06-13: the Segments API now supports full CRUD (create/list/retrieve/update/delete) plus segment statistics — it is no longer read-only.*

---

### Brands

| Method | Endpoint | Description |
|---|---|---|
| GET | `/brands` | List connected brands/stores |
| GET | `/brands/{brandID}` | Get brand details |

---

### Batches

| Method | Endpoint | Description |
|---|---|---|
| POST | `/batches` | Submit a batch operation (bulk contact create/update) |
| GET | `/batches/{batchID}` | Check batch operation status |

Use batches for bulk operations (importing thousands of contacts). Submit an array of operations, receive a batch ID, poll for completion.

---

### Email Content

| Method | Endpoint | Description |
|---|---|---|
| GET | `/templates` | List email templates |
| GET | `/templates/{templateID}` | Get a template |

---

### Images

| Method | Endpoint | Description |
|---|---|---|
| POST | `/images` | Upload an image |
| GET | `/images` | List uploaded images |

---

### Analytics

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reports` | Generate analytics reports |

*Flag: Analytics API endpoints were not fully documented in public docs. The reports endpoint may require specific query parameters for date ranges, metrics, and grouping. Verify with Omnisend API documentation.*

---

## Webhooks

Re-verified 2026-06-13: Omnisend webhooks are **outbound action blocks inside automation workflows**, not a separate webhook-subscription API. You add a **"Webhook" block** at the point in an automation flow where you want to push data to an external endpoint, then configure the destination URL, HTTP method/headers, and a custom JSON payload built from automation variables (e.g. `{{contact.email}}`, order fields).

- **Plan gate**: Webhooks in Automations are available on **paid plans only** — free-plan accounts must upgrade.
- **Trigger model**: the webhook fires when a contact reaches that step of the automation (any automation trigger — signup, abandoned cart, order events, custom events, etc.), so the "events" are defined by where you place the block, not a fixed event catalog.
- **Payload**: fully user-defined in the block; insert merge variables for contact/order/event data.

*Signature verification: third-party integration guides report Omnisend signs webhook deliveries with SHA-256 HMAC in an `x-omnisend-signature` header. This was NOT confirmed on an official Omnisend page during the 2026-06-13 re-verification — treat HMAC signing as unverified and confirm in your account before relying on it.*

---

## JavaScript Snippet (Client-Side Tracking)

For tracking website behavior (page views, cart events) without a native ecommerce integration:

```html
<script>
  window.omnisend = window.omnisend || [];
  omnisend.push(["accountID", "YOUR_ACCOUNT_ID"]);
  omnisend.push(["track", "$pageViewed", {
    $productID: "prod_123",
    $title: "Blue T-Shirt"
  }]);
</script>
```

The JavaScript snippet enables browse abandonment and product recommendation features for custom platforms.

---

## MCP Server (NEW — added 2026-06-13)

Omnisend ships an **MCP (Model Context Protocol) Server v2** at `https://mcp.omnisend.com/v2/mcp`, letting MCP clients (Claude, Cursor, etc.) call the Omnisend API directly. The docs also publish a machine-readable index at `https://api-docs.omnisend.com/llms.txt` (all pages as Markdown + endpoints as OpenAPI) for AI agents.

---

## Key Differences from Other Marketing APIs

| Feature | Omnisend Behavior |
|---|---|
| Versioning | **Header-based** (`Omnisend-Version: 2026-03-15`), not URL-based |
| Pagination | **Cursor-based** (opaque tokens + `paging.hasMore`), not page-number-based |
| Authentication | API key in **`Authorization: Omnisend-API-Key …`** header, not a query param (and not the legacy `X-API-KEY`) |
| Error format | **RFC 9457 Problem Details** (`type` = `https://problems.omnisend.com/…`) with structured `errors` array |
| Contacts | Single entity for email + SMS + push — not separate lists |
| Events | Generic event tracking API — send any event name with properties |
| Batches | Async bulk operations with polling for completion |

---

## Common Integration Patterns

**Product catalog sync**: POST products and categories via API → enable product recommendations and browse abandonment automations.

**Order tracking**: POST events for order lifecycle (placed, fulfilled, cancelled) → trigger post-purchase automations.

**Custom cart tracking**: POST "added to cart" and "cart abandoned" events → trigger cart abandonment workflows without native ecommerce integration.

**Contact sync**: POST/PATCH contacts with tags and custom properties → maintain audience segments for targeted campaigns.

**Bulk import**: Use `/batches` for importing large contact lists → poll batch status for completion.

---

## Source URLs

- API Documentation: https://api-docs.omnisend.com/
- API Authentication: https://api-docs.omnisend.com/reference/authentication
- Rate limits / timeouts / errors: https://api-docs.omnisend.com/reference/rate-limit-timeouts-errors
- Machine-readable index (AI agents): https://api-docs.omnisend.com/llms.txt
- MCP Server: https://mcp.omnisend.com/v2/mcp
- Webhooks in Automations: https://support.omnisend.com/en/articles/9924457-webhooks-in-automations
- Help Center: https://support.omnisend.com/
- Pricing plans 2026: https://support.omnisend.com/en/articles/3533018-omnisend-pricing-plans-2026
