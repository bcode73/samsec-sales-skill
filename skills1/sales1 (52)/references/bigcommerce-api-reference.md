<!-- Source: https://docs.bigcommerce.com/developer/docs/overview/api-fundamentals/api-accounts -->
<!-- Source: https://developer.bigcommerce.com/docs/start/authentication -->
<!-- Source: https://docs.bigcommerce.com/developer/docs/overview/api-fundamentals/rate-limits -->
<!-- Source: https://developer.bigcommerce.com/docs/integrations/webhooks -->
<!-- Source: https://docs.bigcommerce.com/developer/docs/integrations/webhooks/event-reference/events -->
<!-- Source: https://developer.bigcommerce.com/docs/store-operations/orders (v2/v3 split) -->
<!-- Captured 2026-06-28. Verbatim excerpts from BigCommerce developer docs, enriched with developer context where marked. -->

# BigCommerce API Reference

## Authentication (verbatim)

> Authenticate requests by passing an access token to the `X-Auth-Token` header.

> Requests are made to `https://api.bigcommerce.com/stores/{{STORE_HASH}}/v3/` endpoints with `X-Auth-Token: {{access_token}}` in the headers. The store hash is the value between `/stores/` and `/v3/` in the API Path.

> BigCommerce's V3 APIs are accessible exclusively with OAuth.

> If you accidentally include a terminal forward slash to your endpoint, you will get a 403.

### API account types (verbatim)

> BigCommerce offers three OAuth-based API account types:
>
> 1. **Store-level API accounts** – Created by merchants in their store control panel (Settings > Store-level API accounts). Best for single-store frontend applications and manual third-party integrations.
> 2. **App-level API accounts** – Created in the Developer Portal. Ideal for multi-store apps and applications hosted in the control panel.
> 3. **Account-level API accounts** – Provide access to all stores within a parent account. Used with the GraphQL Account API for platform-wide resource management.

> Merchants generate single-store API credentials when they create API accounts in their store control panel, in the **Settings > Store-level API accounts** menu.

Each store-level API account includes:
- `client_id` – uniquely identifies the client making requests
- `client_secret` – cryptographically secure value (keep confidential)
- `access_token` – static token accompanying most REST API requests
- Client name – a label
- API path – the URL for requests (`/v3/` or `/v2/` is appended depending on the endpoint version)

> Do not send your `client_secret` or `access_token` in plain text or an unencrypted payload.

Example authenticated request (verbatim shape):
```http
GET https://api.bigcommerce.com/stores/{{STORE_HASH}}/v3/endpoint
X-Auth-Token: {{access_token}}
Accept: application/json
```

### OAuth scopes (verbatim)

> Configure your API account with the minimum set of OAuth scopes that your implementation needs. To find the specific OAuth scopes your requests require, consult the root API reference pages for the families of endpoints you plan to use.

Example scope names (non-exhaustive):
- `store_v2_products` – Modify products
- `store_v2_products_read_only` – View products only
- `store_v2_orders` – Modify orders
- `store_v2_customers` – Manage customer data

> All non-default scopes provide read-only variants for GET/HEAD requests only.

### Auth quick-start (cURL)

```bash
# Simplest GET — list products
curl -X GET "https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=1" \
  -H "X-Auth-Token: {access_token}" \
  -H "Accept: application/json"
# NOTE: no trailing slash on the path, or you get 403.
```

## API versions & base paths

> The API path won't change, but it will have `/v3/` or `/v2/` appended to it, depending on the current version for the endpoint you're querying.

- Base: `https://api.bigcommerce.com/stores/{store_hash}/`
- **v3** resources (preferred where they exist): Catalog (`/v3/catalog/products`, `/v3/catalog/categories`, `/v3/catalog/brands`), Customers (`/v3/customers`), Carts (`/v3/carts`), Checkouts (`/v3/checkouts`), Webhooks (`/v3/hooks`), Price Lists (`/v3/pricelists`), Channels (`/v3/channels`), Metafields (per-object `/metafields`).
- **v2** resources (legacy but current for some): **Orders (`/v2/orders`)**, Customers v2 (`/v2/customers`), some store info.

> V2 Order API … Released in 2016 … straightforward endpoints for basic order operations.
> V3 Order API … Launched in 2020 … better support for multiple shipments per order, improved filtering, and more granular control over order items.

GraphQL surfaces:
- **GraphQL Storefront API** — client-side, public token, for headless front-ends.
- **GraphQL Admin API** — typed admin surface (overlaps REST; growing).
- **GraphQL Account API** — account-level, across all stores in a parent account.

## Pagination

v3 list endpoints return a `meta.pagination` object:
<!-- Constructed from docs — verify against live API -->
```json
{
  "data": [ /* ... */ ],
  "meta": {
    "pagination": {
      "total": 246,
      "count": 250,
      "per_page": 250,
      "current_page": 1,
      "total_pages": 1,
      "links": { "current": "?page=1&limit=250" }
    }
  }
}
```
Query params: `?limit={n}&page={n}` (max `limit` is typically 250). Walk pages until `current_page == total_pages`.

## Rate limits (verbatim)

BigCommerce returns these headers with each response:

- `X-Rate-Limit-Time-Window-Ms` — size of your current rate-limiting window
- `X-Rate-Limit-Time-Reset-Ms` — time in milliseconds until your quota resets
- `X-Rate-Limit-Requests-Quota` — how many API requests are allowed in the current window
- `X-Rate-Limit-Requests-Left` — how many remaining requests your client can make

> The quota resets every 30 seconds:
>
> | Plan | Rate |
> |------|------|
> | Pro | 450 requests per 30 seconds |
> | Plus & Standard | 150 requests per 30 seconds |
> | Enterprise | Custom per plan and resource |

Handling `429: Too Many Requests` (verbatim guidance):
> 1. Use the `X-Rate-Limit-Time-Reset-Ms` header to determine how long to wait before retrying.
> 2. Implement a delay: the header provides the time in milliseconds until your quota resets.
> 3. If retries continue failing, gradually increase the wait time to avoid overwhelming the server.

PHP backoff example (verbatim):
```php
$milliseconds = $response->getHeader("X-Rate-Limit-Time-Reset-Ms");
usleep($milliseconds * 1000);
```

## Webhooks

### Create a webhook (verbatim)

> To create a webhook, send a POST request to `/stores/{{STORE_HASH}}/v3/hooks`.

Request body:
```json
{
  "scope": "store/product/updated",
  "destination": "https://6a35e97b.ngrok.io/webhooks",
  "is_active": true
}
```

Optional `headers` property for security (verbatim):
```json
{
  "headers": {
    "Authorization": "Basic SGVsbG86R29vZGJ5ZQ=="
  }
}
```

> The `headers` property accepts any key-value pair as a string, and BigCommerce will include the headers in callback requests made to your application.

> BigCommerce does not support destination URLs served over custom HTTPS ports — use the default HTTPS port 443.

### Callback payload shape (verbatim)

BigCommerce sends the **bare minimum** — store, data type, and id — which prevents assumptions from being made without checking with the BigCommerce API.

Cart event:
```json
{
  "scope": "store/cart/created",
  "store_id": "1025646",
  "data": {
    "type": "cart",
    "id": "09346904-4175-44fd-be53-f7e598531b6c"
  },
  "hash": "352e4afc6dd3fc85ea26bfdf3f91852604d57528",
  "created_at": 1561482670,
  "producer": "stores/{store_hash}"
}
```

Order event:
```json
{
  "scope": "store/order/created",
  "store_id": "1025646",
  "data": {
    "type": "order",
    "id": 250
  },
  "hash": "dd70c0976e06b67aaf671e73f49dcb79230ebf9d",
  "created_at": 1561479335,
  "producer": "stores/{store_hash}"
}
```

### Verification / security (verbatim)

> BigCommerce does **not** use HMAC signing.

The recommended security method is to set a **custom header** (e.g. a shared secret) when creating the webhook; BigCommerce echoes it back on each callback so you can validate the sender. This relies on HTTPS transport security rather than cryptographic verification. The `hash` field cannot be verified — BigCommerce does not provide a way of verifying it.

### Deactivation behavior (verbatim)

> Webhooks deactivate when [BigCommerce is] repeatedly unable to deliver webhook notifications because your service was unavailable or was unable to handle the requests (e.g. responded with 4XX or 5XX response).

Practitioner guidance widely reports a subscription also deactivates after ~90 days of inactivity, and that there are **no delivery logs, no webhook activity dashboard, and no API endpoint to query delivery history** — respond 2XX quickly and reconcile against the API.

### Event scopes (verbatim list)

**Orders**
- `store/order/*`
- `store/order/created`
- `store/order/updated`
- `store/order/archived`
- `store/order/statusUpdated`
- `store/order/message/created`
- `store/order/refund/created`
- `store/order/transaction/created`
- `store/order/transaction/updated`
- `store/order/metafield/created`
- `store/order/metafield/updated`
- `store/order/metafield/deleted`

**Carts**
- `store/cart/*`
- `store/cart/created`
- `store/cart/updated`
- `store/cart/deleted`
- `store/cart/couponApplied`
- `store/cart/abandoned`
- `store/cart/converted`
- `store/cart/metafield/created`
- `store/cart/metafield/deleted`
- `store/cart/metafield/updated`

**Cart Line Items**
- `store/cart/lineItem/*`
- `store/cart/lineItem/created`
- `store/cart/lineItem/updated`
- `store/cart/lineItem/deleted`

**Products**
- `store/product/*`
- `store/product/created`
- `store/product/updated`
- `store/product/deleted`
- `store/product/inventory/updated`
- `store/product/inventory/order/updated`
- `store/product/metafield/*` (created/updated/deleted)
- `store/product/variant/metafield/*` (created/updated/deleted)

**SKUs**
- `store/sku/*`
- `store/sku/created`
- `store/sku/updated`
- `store/sku/deleted`
- `store/sku/inventory/updated`
- `store/sku/inventory/order/updated`

**Customers**
- `store/customer/*`
- `store/customer/created`
- `store/customer/updated`
- `store/customer/deleted`
- `store/customer/address/*` (created/updated/deleted)
- `store/customer/payment/instrument/default/updated`

**Categories**
- `store/category/*` (created/updated/deleted)
- `store/category/metafield/*` (created/updated/deleted)

**Brands**
- `store/brand/metafield/*` (created/updated/deleted)

**Shipments**
- `store/shipment/*` (created/updated/deleted)

**Price Lists**
- `store/priceList/created`, `store/priceList/updated`, `store/priceList/activated`, `store/priceList/deactivated`, `store/priceList/deleted`, `store/priceLists/deleted`
- `store/priceList/record/*` (created/updated/deleted), `store/priceList/records/*` (created/updated/deleted)
- `store/priceList/assignment/updated`, `store/priceList/assignment/deleted`

**Subscribers**
- `store/subscriber/*` (created/updated/deleted)

**Inventory / Metafields / Modifiers / Options**
- `store/inventory/location/metafield/*` (created/updated/deleted)
- `store/metafield/*` (created/updated/deleted)
- `store/modifier/updated`
- `store/option/updated`

**Stores / Delivery Exceptions**
- `store/app/uninstalled`
- `store/information/updated`
- `store/hook/deliveryException`

## Top 5 endpoints (request/response shapes)

<!-- Constructed from docs — verify against live API -->

**List products** — `GET /v3/catalog/products?limit=250&page=1`
```json
{ "data": [ { "id": 111, "name": "Sample", "sku": "SKU-111", "price": 49.0 } ],
  "meta": { "pagination": { "total": 1, "current_page": 1, "total_pages": 1 } } }
```

**Get a product** — `GET /v3/catalog/products/111`
```json
{ "data": { "id": 111, "name": "Sample", "type": "physical", "price": 49.0, "inventory_level": 100 }, "meta": {} }
```

**Create a product** — `POST /v3/catalog/products`
```json
{ "name": "New Product", "type": "physical", "weight": 1, "price": 29.0 }
```

**Update a product** — `PUT /v3/catalog/products/111`
```json
{ "price": 24.0, "is_visible": true }
```

**Get an order (v2)** — `GET /v2/orders/250`
```json
{ "id": 250, "status": "Awaiting Fulfillment", "total_inc_tax": "53.00", "customer_id": 12,
  "products": { "url": "https://api.bigcommerce.com/stores/{store_hash}/v2/orders/250/products", "resource": "/orders/250/products" } }
```

## Error response shape

<!-- Constructed from docs — verify against live API -->
```json
{
  "status": 403,
  "title": "Forbidden",
  "type": "https://developer.bigcommerce.com/api-docs/getting-started/api-status-codes",
  "errors": {}
}
```
Common cases: **403** for a missing OAuth scope OR a trailing slash on the path; **422** for a malformed body; **429** when over the 30-second quota (read `X-Rate-Limit-Time-Reset-Ms`).

## Gaps

- Live developer-portal pages are JS-rendered and some canonical URLs 301-redirect (developer.bigcommerce.com ↔ docs.bigcommerce.com); endpoint-level field lists above the verbatim sections are constructed from documented shapes and marked accordingly — verify against the live API reference before relying on them.
- Exact GraphQL Admin API coverage vs REST is evolving; confirm specific mutations exist before designing around them.
