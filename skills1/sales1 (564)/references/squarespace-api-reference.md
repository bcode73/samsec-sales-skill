<!-- Source: https://developers.squarespace.com/commerce-apis/overview + /making-requests + /orders-overview + /commerce-apis/orders + /inventory-overview + /products-overview + /webhooks/overview + /webhooks/verifying-notifications (fetched 2026-06-29) -->

# Squarespace Commerce API Reference

Verbatim capture of the Squarespace Commerce APIs, enriched with auth quick-start, request/response JSON, pagination, and webhook signature verification. Pricing/plan gates are best-effort — re-verify against the live docs.

> **Plan gate (read first):** The Commerce APIs are **not available on the free trial or the cheapest tier.** Squarespace's developer docs list Orders/Inventory as available on **Core, Plus, Advanced, and Commerce Advanced** plans; some third-party reviews state Commerce API access requires the **Advanced (~$99/mo)** plan. Confirm against your own plan before building. There is **no API on a non-commerce (personal) plan.**

---

## Making requests

### Base URL

```
https://api.squarespace.com/{api-version}/{resource-path}
```

`{api-version}` is **per-endpoint** (Orders is `1.0`, Inventory is `1.0`, Products is `2`, etc.) — it is not a single global version. Example concrete paths:

- `https://api.squarespace.com/1.0/commerce/orders`
- `https://api.squarespace.com/1.0/commerce/inventory`
- `https://api.squarespace.com/2/commerce/products`
- `https://api.squarespace.com/1.0/commerce/transactions`
- `https://api.squarespace.com/1.0/webhook_subscriptions`

**All requests sent over HTTP instead of HTTPS are rejected.**

### Authentication

Two methods, both **Bearer** tokens in the `Authorization` header:

| Method | Use when | How |
|---|---|---|
| **API Key** | Automating your *own* single site | Generate in **Settings → Advanced → Developer API Keys** (commerce plan required). Each key is scoped to chosen permissions (e.g. Orders, Inventory, Products read/write). |
| **OAuth 2.0** | A third-party app acting on *other* sites | Register an OAuth client at developers.squarespace.com; user authorizes; you receive access + refresh tokens. **Webhook Subscriptions API requires OAuth** (API keys can't subscribe to webhooks). |

### Required headers

Every request must include:

- `Authorization: Bearer YOUR_API_KEY_OR_OAUTH_TOKEN`
- `User-Agent: YOUR_CUSTOM_APP_DESCRIPTION` — **send a custom User-Agent.** Requests with a default/generic UA "may be subject to stricter rate limiting."
- `Content-Type: application/json` (only when sending a request body)

### Auth quick-start (simplest GET)

```bash
curl "https://api.squarespace.com/1.0/commerce/orders" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "User-Agent: my-crm-sync/1.0" \
  -H "Content-Type: application/json"
```

### Versioning

Version numbers are endpoint-specific and documented on each API's overview page. See the docs' Versioning guide.

### Rate limits

Rate limiting applies to all requests; **specific thresholds are not published.** A default/generic `User-Agent` draws stricter limiting. Treat `429` as expected under load and back off with exponential delay + jitter; check for `Retry-After` if present.

### Responses & errors

All responses are JSON and use standard HTTP status codes. A failed request returns a JSON body with a machine-readable `type` and a human `message`, e.g.:

<!-- Constructed from docs — verify against live API -->
```json
{ "type": "INVALID_ARGUMENT", "message": "modifiedAfter and modifiedBefore must be supplied together." }
```

---

## Commerce API catalog (overview)

| API | Version | What it does |
|---|---|---|
| **Orders** | 1.0 | Access order history for one-time + subscription orders; import orders from third-party sales channels; mark orders fulfilled (triggers shipment notification). |
| **Inventory** | 1.0 | Read and adjust stock for product variants. |
| **Products** | 2 (legacy 1.1, 1.0) | Manage physical, service, gift-card, and download products — variants and images. |
| **Transactions** | 1.0 | Access financial transactions for **orders and donations**. (Donations are NOT in the Orders API — use Transactions.) |
| **Contacts** | — | Manage people associated with a site — customers, subscribers, donors — address books and marketing preferences. |
| **Analytics** | — | Retrieve aggregated commerce data (order counts, totals, donations) for contacts in bulk. |
| **Profiles** | — | Read customers, mailing-list subscribers, donors. **Maintenance mode — new integrations should use Contacts.** |
| **Webhook Subscriptions** | 1.0 | Subscribe to site notifications (e.g. order created) by configuring a webhook endpoint. **OAuth only.** |

---

## Orders API (v1.0)

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/1.0/commerce/orders` | List orders (up to 50 per page, ordered by `modifiedOn`) |
| POST | `/1.0/commerce/orders` | Create order (import from a third-party sales channel) |
| GET | `/1.0/commerce/orders/{orderId}` | Get a single order |
| POST | `/1.0/commerce/orders/{orderId}/fulfillments` | Mark order fulfilled (optionally notify customer) |

> **Donations are not accessible via the Orders API; use the Transactions API instead.**
> **Payment Plan orders** (deposit + installments) are represented as a single Order.

### List Orders — query parameters

| Param | Notes |
|---|---|
| `cursor` | Pagination pointer. **Cannot be combined with the date params.** |
| `modifiedAfter` | ISO 8601 UTC timestamp. **Must be supplied together with `modifiedBefore`.** |
| `modifiedBefore` | ISO 8601 UTC timestamp. Must be paired with `modifiedAfter`. |
| `fulfillmentStatus` | Filter by `PENDING`, `FULFILLED`, or `CANCELED`. |
| `customerId` | Filter orders by Customer ID. |
| `paymentStates` | Comma-separated. **Default (when omitted):** `NOT_CHARGED,AUTHORIZED,PAID,REFUNDED`. Full set: `NOT_CHARGED`, `AUTHORIZED`, `PAID`, `PARTIALLY_PAID`, `PENDING`, `FAILED`, `REFUND_PENDING`, `REFUNDED`, `REFUND_FAILED`. |

### Pagination response shape

```json
{
  "result": [],
  "pagination": {
    "hasNextPage": true,
    "nextPageCursor": "ewogICJhIiA6ICI2OWNhOWExZjgxNGMwYTY0MmIwMTIzYzkiLAogICJiIiA6ICJJRCIKfQ",
    "nextPageUrl": "/1.0/commerce/orders?cursor=ewogICJhIiA6ICI2OWNhOWExZjgxNGMwYTY0MmIwMTIzYzkiLAogICJiIiA6ICJJRCIKfQ"
  }
}
```

Loop: follow `nextPageCursor` until `hasNextPage` is `false`. To page through a date window, make the **first** call with `modifiedAfter`/`modifiedBefore`, then subsequent calls with only `cursor` (the cursor encodes the original filter).

### Order object (full schema)

```json
{
  "id": "585d498fdee9f31a60284a37",
  "orderNumber": "3",
  "createdOn": "2016-12-23T15:58:07.187Z",
  "modifiedOn": "2016-12-23T15:58:07.187Z",
  "channel": "web",
  "channelName": "Faire Wholesale",
  "testmode": true,
  "customerEmail": "customer@example.com",
  "customerId": "585d498fdee9f31a60284a38",
  "billingAddress": {
    "firstName": "Bob", "lastName": "Loblaw",
    "address1": "459 Broadway", "address2": "address2",
    "city": "New York", "state": "NY", "postalCode": "10003",
    "countryCode": "US", "phone": "5553334444"
  },
  "shippingAddress": {
    "firstName": "Bob", "lastName": "Loblaw",
    "address1": "459 Broadway", "address2": "address2",
    "city": "New York", "state": "NY", "postalCode": "10003",
    "countryCode": "US", "phone": "5553334444"
  },
  "fulfillmentStatus": "PENDING",
  "fulfilledOn": "2024-08-25T15:00:00Z",
  "paymentState": "NOT_CHARGED",
  "priceTaxInterpretation": "EXCLUSIVE",
  "lineItems": [
    {
      "id": "585d4975dee9f31a60284a16",
      "lineItemType": "PHYSICAL_PRODUCT",
      "productId": "565c8f3da7c8a3cf71d5fd0a",
      "productName": "Product",
      "variantId": "88c16ee4-547b-445e-a392-bded9991ae30",
      "sku": "SQ3381024",
      "quantity": 1,
      "unitPricePaid": { "currency": "USD", "value": 49.99 },
      "imageUrl": "https://static.squarespace.com/universal/commerce/images/brine-32oz-spring-mix-v2.jpg?format=300w",
      "variantOptions": [ { "optionName": "Size", "value": "Large" } ],
      "customizations": [ { "label": "How did you hear about us?", "value": "Facebook" } ],
      "weight": 1, "length": 3, "width": 2, "height": 4
    }
  ],
  "subtotal":      { "currency": "USD", "value": 49.99 },
  "shippingTotal": { "currency": "USD", "value": 49.99 },
  "discountTotal": { "currency": "USD", "value": 49.99 },
  "taxTotal":      { "currency": "USD", "value": 49.99 },
  "grandTotal":    { "currency": "USD", "value": 49.99 },
  "refundedTotal": { "currency": "USD", "value": 49.99 },
  "discountLines": [
    {
      "name": "Summer Sale - 20% Off",
      "description": "20% off all orders over $50",
      "promoCode": "SUMMER20",
      "amount": { "currency": "USD", "value": 49.99 }
    }
  ],
  "shippingLines": [ { "method": "UPS Ground", "amount": { "currency": "USD", "value": 49.99 } } ],
  "shippingOptionName": "shippingOptionName",
  "shippingOptionServiceType": "FEDEX_GROUND",
  "fulfillments": [
    {
      "carrierName": "FedEx",
      "service": "Same-Day Delivery",
      "shipDate": "2017-01-29T22:19:26.98Z",
      "trackingNumber": "103932814692659",
      "trackingUrl": "https://www.fedex.com/apps/fedextrack/?tracknumbers=103932814692659"
    }
  ],
  "internalNotes": [ { "content": "First note" } ],
  "formSubmission": [ { "label": "How did you hear about us?", "value": "Facebook" } ],
  "externalOrderReference": "EXT-98765"
}
```

**Money fields are objects** (`{ "currency": "USD", "value": 49.99 }`) — `value` is a decimal string/number, NOT integer cents (contrast with Square/Sellfy which use cents). `priceTaxInterpretation` is `EXCLUSIVE` or `INCLUSIVE`.

### Fulfill an order

```bash
curl -X POST "https://api.squarespace.com/1.0/commerce/orders/585d498fdee9f31a60284a37/fulfillments" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "User-Agent: my-fulfillment-app/1.0" \
  -H "Content-Type: application/json" \
  -d '{
    "shouldSendNotification": true,
    "shipments": [
      {
        "shipDate": "2026-06-29T15:00:00Z",
        "carrierName": "FedEx",
        "service": "Ground",
        "trackingNumber": "103932814692659",
        "trackingUrl": "https://www.fedex.com/apps/fedextrack/?tracknumbers=103932814692659"
      }
    ]
  }'
```
<!-- Fulfillment body shape constructed from docs — verify field names against live API -->

---

## Inventory API (v1.0)

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/1.0/commerce/inventory` | List inventory (cursor-paginated) |
| GET | `/1.0/commerce/inventory/{variantId}` | Get inventory for one or more variants (comma-separated IDs) |
| POST | `/1.0/commerce/inventory/adjustments` | Adjust stock quantities |

### InventoryItem object

<!-- Constructed from documented fields — verify against live API -->
```json
{
  "variantId": "88c16ee4-547b-445e-a392-bded9991ae30",
  "sku": "SQ3381024",
  "descriptor": "Spring Mix - Large",
  "isUnlimited": false,
  "quantity": 42
}
```

`isUnlimited: true` means the variant is **not tracked** (sells without decrementing). When `false`, `quantity` is the available stock.

### Adjust stock

```bash
curl -X POST "https://api.squarespace.com/1.0/commerce/inventory/adjustments" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "User-Agent: my-inventory-sync/1.0" \
  -H "Content-Type: application/json" \
  -d '{
    "incrementOperations": [],
    "decrementOperations": [ { "variantId": "88c16ee4-547b-445e-a392-bded9991ae30", "quantity": 1 } ],
    "setFiniteOperations": [ { "variantId": "abc...", "quantity": 100 } ]
  }'
```
<!-- Adjustment body constructed from docs — verify operation names against live API -->

---

## Products API (v2)

**Current version: v2.** Legacy: v1.1, v1.0.

### Endpoints

| Method | Path / anchor | Description |
|---|---|---|
| GET | `/2/commerce/products` | List products |
| POST | `/2/commerce/products` | Create product |
| GET | `/2/commerce/products/{id}` | Get product(s) |
| POST | `/2/commerce/products/{id}` | Update product |
| DELETE | `/2/commerce/products/{id}` | Delete product |
| POST | `/2/commerce/products/{id}/images` | Upload image |
| POST | `/2/commerce/products/{id}/images/{imageId}` | Update image |
| DELETE | `/2/commerce/products/{id}/images/{imageId}` | Delete image |
| POST | `/2/commerce/products/{id}/images/order` | Reorder images |
| GET | `/2/commerce/products/{id}/images/{imageId}/status` | Image processing status |
| POST | `/2/commerce/products/{id}/variants` | Create variant |
| POST | `/2/commerce/products/{id}/variants/{variantId}` | Update variant |
| DELETE | `/2/commerce/products/{id}/variants/{variantId}` | Delete variant |
| POST | `/2/commerce/products/{id}/variants/{variantId}/image` | Assign variant image |

### Product types

- **PHYSICAL** — tangible goods requiring shipping/pickup
- **SERVICE** — services and experiences (v2 only)
- **GIFT_CARD** — digital gift cards (v2 only)
- **DOWNLOAD** — digital files (**readable but NOT creatable in v2**)

> **Limitation:** Categories that a Store Page uses to group products are **not available via the API.**

### Product object

<!-- Constructed from documented fields — verify against live API -->
```json
{
  "id": "5cda060f70df8b00012345ab",
  "type": "PHYSICAL",
  "storePageId": "5c5a...",
  "name": "Spring Mix",
  "description": "<p>Fresh greens.</p>",
  "url": "spring-mix",
  "tags": ["greens", "salad"],
  "isVisible": true,
  "variants": [
    {
      "id": "88c16ee4-547b-445e-a392-bded9991ae30",
      "sku": "SQ3381024",
      "pricing": {
        "basePrice": { "currency": "USD", "value": 49.99 },
        "salePrice": { "currency": "USD", "value": 39.99 },
        "onSale": false
      },
      "stock": { "quantity": 42, "unlimited": false },
      "attributes": { "Size": "Large" },
      "shippingMeasurements": { "weight": 1.0, "dimensions": "3x2x4" }
    }
  ],
  "images": [
    { "id": "5cda...img", "altText": "Spring mix bag", "url": "https://images.squarespace-cdn.com/..." }
  ],
  "variantAttributes": ["Size"],
  "createdOn": "2019-05-13T20:00:00Z",
  "modifiedOn": "2019-05-13T20:00:00Z"
}
```

---

## Transactions API (v1.0)

`GET /1.0/commerce/transactions` — financial transactions for **orders and donations** (payments, refunds, fees, payouts). This is the only API surface for **donation** data; the Orders API excludes donations. Cursor-paginated, supports `modifiedAfter`/`modifiedBefore` like Orders.

---

## Webhook Subscriptions API (v1.0)

**Authentication:** Requests to the Webhook Subscriptions API **must use an OAuth token** with permissions matching the event types you subscribe to. (API keys cannot create webhook subscriptions.)

### Endpoints

| Method | Operation |
|---|---|
| GET | List webhook subscriptions |
| POST | Create webhook subscription |
| GET | Get webhook subscription |
| POST | Update webhook subscription |
| DELETE | Delete webhook subscription |
| POST | Rotate webhook subscription secret |
| POST | Send test notification |

### Supported event topics

- **Commerce orders:** `order.create`, `order.update`
- **Contacts:** `contact.create`, `contact.update`, `contact.delete`
- **Addresses:** `address.create`, `address.update`, `address.delete`
- **Extension:** `extension.uninstall`

> Inventory-change notifications are surfaced through order events / the Inventory API rather than a standalone `inventory.update` topic in the current docs — verify the topic list for your API version before relying on a specific event.

### Create a subscription

```bash
curl -X POST "https://api.squarespace.com/1.0/webhook_subscriptions" \
  -H "Authorization: Bearer YOUR_OAUTH_TOKEN" \
  -H "User-Agent: my-webhook-app/1.0" \
  -H "Content-Type: application/json" \
  -d '{
    "endpointUrl": "https://example.com/squarespace/webhook",
    "topics": ["order.create", "order.update"]
  }'
```

The create (and rotate-secret) response returns a **`secret`** — a **hex string** — shown **only once**. Store it; you need it to verify signatures.

### Notification payload

```json
{
  "id": "5c2ba184b63ed3cb411ce2b1",
  "websiteId": "5f3c3d55ac435e1a051f77b3",
  "subscriptionId": "5f3c2155d947844beedda991",
  "topic": "order.create",
  "createdOn": "2020-04-22T22:18+00:00",
  "data": {
    "orderId": "585d498fdee9f31a60284a37",
    "update": "CREATED"
  }
}
```

**Payloads are thin** — `data` typically carries an `orderId` (or contact id), not the full object. Make a follow-up `GET /1.0/commerce/orders/{orderId}` to retrieve the full order.

### Signature verification (critical)

- **Header:** `Squarespace-Signature` carries the signature.
- **Algorithm:** **HMAC-SHA256.**
- **What is signed:** the **raw HTTP request body** as a UTF-8 string (the exact bytes received — do NOT re-serialize a parsed JSON object).
- **Key:** the subscription **`secret`**, which is **hex-encoded** and **must be decoded to raw bytes** before constructing the HMAC. *"The hex-encoded secret should be decoded to raw bytes when constructing the HMAC otherwise the expected signature won't match."*
- **Formula:** `Expected signature = HMAC-SHA256(hexToBytes(secret), request payload)`, hex-encoded.
- Compare with the header value using a **constant-time** comparison.

**Node.js:**
```javascript
const crypto = require('crypto');

function isFromSquarespace(rawBody, headerSignature, secret) {
  const expected = crypto
    .createHmac('sha256', Buffer.from(secret, 'hex'))  // hex secret -> raw bytes
    .update(rawBody)                                    // RAW body, not parsed JSON
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(headerSignature)
  );
}
```

**Python:**
```python
import hashlib, hmac

def is_from_squarespace(raw_body: bytes, header_signature: str, secret_hex: str) -> bool:
    key = bytes.fromhex(secret_hex)                 # hex secret -> raw bytes
    expected = hmac.new(key, raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header_signature)
```

### Test notification

`POST` the "Send test notification" endpoint to have Squarespace deliver a sample event to your `endpointUrl` so you can validate signature handling before going live. Rotate the secret with the "Rotate secret" endpoint if it leaks (returns a new `secret` once).

---

## Integration gotchas

- **No API on a non-commerce plan / free trial.** The whole Commerce API surface requires a paid commerce plan (Core+; some sources say Advanced). Don't promise an integration to someone on a personal plan.
- **Webhooks need OAuth, not an API key.** A single-site automation using an API key can still *poll* `GET /commerce/orders?modifiedAfter=...`, but to receive `order.create` push events you must register an OAuth app.
- **Thin payloads → double the calls.** Every webhook is a pointer; budget a follow-up GET per event.
- **`modifiedAfter` + `modifiedBefore` are paired and mutually exclusive with `cursor`.** First page uses the date window; later pages use only the returned cursor.
- **Money is a `{currency, value}` object**, decimal — not integer cents.
- **Donations bypass Orders.** Use the Transactions API for donation financials.
- **Send a custom `User-Agent`** or eat stricter rate limiting.
- **No multi-currency.** A site sells in one display currency; the API reflects that single currency.

## Gaps

- Exact rate-limit thresholds are unpublished.
- Full request/response bodies for Inventory adjustments and Product create/update were not provided verbatim in the fetched overview pages; the JSON above the `<!-- Constructed -->` markers is assembled from documented field lists — verify against the live endpoint docs at developers.squarespace.com before relying on exact field names.
- No official Squarespace MCP server was found at research time.
