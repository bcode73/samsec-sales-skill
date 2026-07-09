<!-- Source: https://developer.squareup.com/docs (Square API), https://developer.squareup.com/docs/orders-api, https://developer.squareup.com/docs/inventory-api, https://developer.squareup.com/docs/webhooks/overview, https://developer.squareup.com/docs/webhooks/step3validate, https://developer.squareup.com/docs/mcp -->
<!-- Captured 2026-06-29. Square Online has no separate site-builder API; you automate the commerce layer with the standard Square APIs documented here. Pricing/rate-limit specifics are best-effort — verify against live docs. -->

# Square API Reference (powers Square Online)

Square Online stores are built on the Square platform. There is **no dedicated "Square Online API"** for editing the storefront — you integrate at the commerce layer using the standard Square APIs (Catalog, Orders, Inventory, Payments, Checkout, Customers, Subscriptions), the same APIs that power Square POS. This file documents that surface.

## Authentication

- **Auth type:** Bearer token in the `Authorization` header.
  - **Personal access token** — for your own single Square account (from the Developer Dashboard). Long-lived.
  - **OAuth access token** — for multi-merchant apps. **Access tokens expire after 30 days**; use the refresh token to mint a new one (`POST /oauth2/token`, `grant_type=refresh_token`). Scopes are requested at authorization (e.g. `ORDERS_READ`, `ITEMS_WRITE`, `INVENTORY_READ`, `PAYMENTS_WRITE`, `CUSTOMERS_READ`).
- **Required headers:**
  - `Authorization: Bearer {ACCESS_TOKEN}`
  - `Square-Version: YYYY-MM-DD` — date-based API version; pin it. Square defaults to your app's version if omitted, but pinning is recommended.
  - `Content-Type: application/json` (for write requests).
- **Base URLs:**
  - Production: `https://connect.squareup.com/v2`
  - Sandbox: `https://connect.squareupsandbox.com/v2`
  - OAuth authorize (production): `https://connect.squareup.com/oauth2/authorize`

### Auth quick-start (simplest GET)
List your locations (needed for almost every other call):
```bash
curl https://connect.squareup.com/v2/locations \
  -H "Authorization: Bearer $SQUARE_ACCESS_TOKEN" \
  -H "Square-Version: 2026-06-18"
```

## Core commerce APIs

### Catalog API
Manages items, item variations, categories, modifiers, taxes, discounts, and images — the products that appear in Square Online and POS.

- `GET /v2/catalog/list?types=ITEM` — list catalog objects (cursor-paginated).
- `POST /v2/catalog/object` — upsert a single catalog object.
- `POST /v2/catalog/batch-upsert` — upsert many objects atomically (use `#`-prefixed temp IDs; response returns `id_mappings`).
- `POST /v2/catalog/batch-retrieve` — fetch objects by ID.
- `POST /v2/catalog/search` — query items by name/attribute.
- `DELETE /v2/catalog/object/{object_id}` — delete.

From the docs: *"The Catalog API includes detailed itemization and automatic taxes and discounts, with built-in Inventory API integration that automatically updates inventory levels for catalog item variations."*

Catalog item with a tracked variation (prices and `track_inventory` live on the **variation**):
```json
{
  "idempotency_key": "unique-key",
  "object": {
    "type": "ITEM",
    "id": "#Coffee",
    "item_data": {
      "name": "Coffee",
      "variations": [{
        "type": "ITEM_VARIATION",
        "id": "#Coffee-Small",
        "item_variation_data": {
          "item_id": "#Coffee",
          "name": "Small",
          "pricing_type": "FIXED_PRICING",
          "price_money": { "amount": 300, "currency": "USD" },
          "track_inventory": true
        }
      }]
    }
  }
}
```

### Orders API
> "The Orders API is your one-stop shop for adding rich functionality to payments. You can itemize payments using custom line items or catalog objects, send orders to physical Point of Sale devices to be fulfilled, attach a customer to a payment, and more."

> "The Orders API is the primary API for managing the order lifecycle."

**Create an order** — `POST /v2/orders`
Required: `location_id` and `line_items`.

Catalog-based line item (recommended):
```json
{
  "order": {
    "location_id": "your_location_id",
    "line_items": [
      { "quantity": "1", "catalog_object_id": "your_catalog_item_id" }
    ]
  }
}
```

Ad hoc line item (no catalog reference):
```json
{
  "order": {
    "location_id": "your_location_id",
    "line_items": [
      {
        "name": "Hamburger",
        "quantity": "1",
        "base_price_money": { "amount": 1000, "currency": "USD" }
      }
    ]
  }
}
```

> "Order objects can be created with any combination of line items, fulfillments, taxes, and discounts. They can also be created empty and updated with elements over time." **Orders appear in the Square Dashboard only when they include fulfillment and payment has been processed.**

Other endpoints:
- `POST /v2/orders/search` — search orders (filter by location, date range, state, order IDs).
- `GET /v2/orders/{order_id}` — RetrieveOrder.
- `PUT /v2/orders/{order_id}` — UpdateOrder (sparse updates with `fields_to_clear`).
- `POST /v2/orders/{order_id}/pay` — PayOrder.

Include a `fulfillments` object (`PICKUP`, `SHIPMENT`, `DELIVERY`) to model how the order is fulfilled.

### Inventory API
> "When automatic inventory tracking is enabled, Square automatically updates seller inventory counts whenever an Order is completed through the Orders API."

- `POST /v2/inventory/counts/batch-retrieve` — BatchRetrieveInventoryCounts (current counts by `catalog_object_ids` × `location_ids`).
- `POST /v2/inventory/changes/batch-create` — BatchChangeInventory (apply `PHYSICAL_COUNT`, `ADJUSTMENT`, or `TRANSFER` changes).
- `POST /v2/inventory/changes/batch-retrieve` — history of changes.
- `GET /v2/inventory/{catalog_object_id}` — RetrieveInventoryCount.

Count shape:
```json
{
  "catalog_object_id": "ITEM_VARIATION_ID",
  "location_id": "LOCATION_ID",
  "state": "IN_STOCK",
  "quantity": "12",
  "calculated_at": "2026-06-29T12:00:00Z"
}
```

States include `IN_STOCK`, `SOLD`, `RETURNED_BY_CUSTOMER`, `RESERVED_FOR_SALE`, `WASTE`, etc. Counts are per **variation per location**.

### Payments & Checkout APIs
> "The Payments API lets developers take and manage payments." Payments have "built-in Orders API integration for order management."

- **Payments API** — `POST /v2/payments` (take a payment with a `source_id` nonce from the Web Payments SDK), `GET /v2/payments`, refunds via `POST /v2/refunds`.
- **Checkout / Payment Links API** — `POST /v2/online-checkout/payment-links` creates a hosted checkout page / shareable link (quick way to take an online payment without building a checkout UI).
- **Web Payments SDK** — client-side card/wallet entry that tokenizes payment details into a `source_id`.

### Customers & Subscriptions
- **Customers API** — `POST /v2/customers`, `GET /v2/customers`, `POST /v2/customers/search`. Shared customer directory across channels.
- **Subscriptions API** — `POST /v2/subscriptions`, plans defined as catalog `SUBSCRIPTION_PLAN` objects.

## Pagination
Cursor-based. List/search responses return a `cursor`; pass it back as `cursor` (query param on GETs, body field on POSTs) until absent.

## Errors & rate limits
- Errors return an `errors` array: `[{ "category": "...", "code": "...", "detail": "..." }]`.
- > "If your application sends a high number of requests to Square APIs in a short period of time, Square might temporarily stop processing your requests and return RATE_LIMITED errors with a 429 Too Many Requests status. However, Square does not publicly disclose specific rate limit numbers."
- Recommended: > "monitor responses for 429 errors and use a retry mechanism with an exponential backoff schedule ... use a randomized delay (jitter) ... to avoid a thundering herd effect."
- Write endpoints accept an `idempotency_key` — reuse it on retries to avoid double-creates.

## Webhooks

> "A webhook is a subscription that registers a notification URL and a list of event types to be notified about. When an event occurs, Square collects data about the event, creates an event notification, and sends it to the notification URL for all webhook subscriptions that are subscribed to that event."

### Requirements
The notification URL endpoint must:
- Use **HTTPS**
- Accept **JSON via POST**
- Return a **2xx** status code quickly to acknowledge receipt

### Delivery & retries
> "Square targets delivery within 60 seconds. If acknowledgment isn't received, the system retries for up to 24 hours using exponential backoff (starting at 1 minute, scaling to 8-hour intervals)."
Retried notifications include `square-retry-number` and `square-retry-reason` headers.

### Static source IPs (allowlist these)
- **Production:** `54.245.1.154`, `34.202.99.168`
- **Sandbox:** `54.212.177.79`, `107.20.218.8`

### Event types (commerce-relevant)
| Event | Meaning |
|---|---|
| `order.created` | Published when an Order is created |
| `order.updated` | Published when an Order is updated |
| `order.fulfillment.updated` | Published when an OrderFulfillment is created or updated |
| `inventory.count.updated` | Published when the quantity is updated for a CatalogItemVariation |
| `catalog.version.updated` | Published when the catalog is updated |
| `payment.created` | Published when a Payment is created |
| `payment.updated` | Triggered when payment status or card details change |
| `refund.created` | Published when a Refund is created |
| `refund.updated` | Occurs when refund status changes |
| `customer.created` / `customer.updated` / `customer.deleted` | Customer directory changes |
| `invoice.created` / `invoice.updated` / `invoice.published` / `invoice.payment_made` | Invoice lifecycle |
| `subscription.created` / `subscription.updated` | Subscription lifecycle |

All events follow a `resource.action` or `resource.subresource.action` naming pattern.

### Signature verification (HMAC-SHA256)
> Square webhook notifications include an `x-square-hmacsha256-signature` header. "The value of this header is an HMAC-SHA-256 signature generated using" three components: the **signature key** for your webhook subscription, the **notification URL** for your webhook subscription, and the **raw body** of the request.

To validate: generate the HMAC-SHA-256 signature in your own code (over `notification_url + raw_body`, keyed by the signature key) and compare it to the `x-square-hmacsha256-signature` header. **Use a constant-time comparison** to prevent timing attacks.

SDK helpers (recommended — they handle the concatenation and constant-time compare):

**Node.js (square v40.0.0+):**
```javascript
import { WebhooksHelper } from "square";

async function isFromSquare(signature, body) {
  return await WebhooksHelper.verifySignature({
    requestBody: body,
    signatureHeader: signature,
    signatureKey: SIGNATURE_KEY,
    notificationUrl: NOTIFICATION_URL
  });
}
```

**Python:**
```python
from square.utilities.webhooks_helper import is_valid_webhook_event_signature

is_from_square = is_valid_webhook_event_signature(
    body, square_signature, SIGNATURE_KEY, NOTIFICATION_URL)
```

**PHP (square v41.0.0.20250220+):**
```php
use Square\Utils\WebhooksHelper;

if (WebhooksHelper::verifySignature($body, $signature, SIGNATURE_KEY, NOTIFICATION_URL)) {
    // Valid signature
}
```

**Ruby:**
```ruby
require 'square'

Square::WebhooksHelper.is_valid_webhook_event_signature(
    body, signature, SIGNATURE_KEY, NOTIFICATION_URL)
```

Manual verification (when not using an SDK) — Python:
```python
import hmac, hashlib, base64
payload = NOTIFICATION_URL.encode() + raw_body_bytes
digest = hmac.new(SIGNATURE_KEY.encode(), payload, hashlib.sha256).digest()
expected = base64.b64encode(digest).decode()
valid = hmac.compare_digest(expected, request_signature_header)
```

## SDKs
Official server SDKs: **PHP, Java, Python, Node.js, Ruby, .NET, Go**. Plus the client-side **Web Payments SDK** for card/wallet tokenization.

## MCP Server (Beta)

The **Square MCP Server** implements the Model Context Protocol, connecting AI assistants to the Square REST API. Hosted at `https://mcp.squareup.com/sse`. Repo: `github.com/square/square-mcp-server` (auto-generated from Square's OpenAPI spec).

**Remote (recommended)** — OAuth, no manual token management, production only.
**Local** — Node.js, configured with env vars, can hit Sandbox or Production.

### Claude.ai
In Settings → Integrations, add the URL `https://mcp.squareup.com/sse`, then authenticate with your Square account.

### Claude Desktop (Remote)
```json
{
  "mcpServers": {
    "mcp_square_api": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.squareup.com/sse"]
    }
  }
}
```

### Claude Desktop (Local)
```json
{
  "mcpServers": {
    "mcp_square_api": {
      "command": "npx",
      "args": ["square-mcp-server", "start"],
      "env": {
        "ACCESS_TOKEN": "YOUR_SQUARE_ACCESS_TOKEN",
        "SANDBOX": "true"
      }
    }
  }
}
```

### Local server quickstart
```bash
npx square-mcp-server start
# or with inline env vars:
ACCESS_TOKEN=YOUR_SQUARE_ACCESS_TOKEN SANDBOX=true npx square-mcp-server start
```

### Key environment variables
- `ACCESS_TOKEN` — your Square API access token
- `SANDBOX` — `true` for testing
- `DISALLOW_WRITES` — restrict to read-only operations
- `SQUARE_VERSION` — specify API version

> Note: "Square maintains an allowlist of MCP clients" to prevent malicious registrations; request additions via the developer forum if needed.

## Gaps
- Square does not publish exact rate-limit numbers — treat `429` reactively with backoff.
- The eCommerce API overview page and parts of the webhook events reference are JS-rendered; endpoint paths/JSON above are from the per-API docs and SDK helpers and should be verified against the live reference at `developer.squareup.com/reference/square`.
- Square Online storefront/theme/page management has no public API (UI-only) — confirmed by the absence of a Sites/Online-Store builder API in the reference.
