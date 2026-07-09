<!-- Source: https://woocommerce.github.io/woocommerce-rest-api-docs/ (REST API v3) and https://woocommerce.github.io/woocommerce-rest-api-docs/#webhooks — captured 2026-07-04. Content below is quoted/summarized from the official docs; representative JSON is marked as constructed. -->

# WooCommerce REST API v3 — Reference

The WooCommerce REST API lets you read and write store data (products, orders, customers, coupons,
etc.) with JSON over HTTP, from outside WordPress. It is a WordPress plugin, so it uses the WordPress
REST API infrastructure under `/wp-json/`.

## Requirements

- WooCommerce 3.5+ and WordPress 4.4+
- **Pretty permalinks** enabled (Settings → Permalinks; anything other than "plain") — otherwise
  `/wp-json/` returns 404
- **HTTPS recommended.** Over HTTPS you can use Basic Auth; over plain HTTP you must use OAuth 1.0a.

## Base URL

```
https://example.com/wp-json/wc/v3
```

The current namespace is `wc/v3`. (`wc/v1` and `wc/v2` remain for backward compatibility.)

## Authentication

Two methods:

### 1. HTTPS — Basic Auth (recommended)
Provide the **Consumer Key** as the username and the **Consumer Secret** as the password.

```bash
curl https://example.com/wp-json/wc/v3/orders \
    -u consumer_key:consumer_secret
```

If your server does not correctly parse the `Authorization` header, pass the credentials as query
string parameters instead (only over HTTPS):

```bash
curl "https://example.com/wp-json/wc/v3/orders?consumer_key=ck_xxx&consumer_secret=cs_xxx"
```

(In the official client libraries this is the `queryStringAuth: true` option.)

### 2. HTTP — OAuth 1.0a "one-legged"
For sites **not** served over HTTPS, use OAuth 1.0a one-legged authentication to prevent the consumer
secret from being intercepted. You build a signature base string from the HTTP method, the URL, and
the normalized parameters, then generate an **HMAC-SHA1** signature using the consumer secret.
Required OAuth params include `oauth_consumer_key`, `oauth_timestamp`, `oauth_nonce`,
`oauth_signature_method` (`HMAC-SHA1`), and `oauth_signature`.

### Generating keys
- **Manual:** WooCommerce → Settings → Advanced → REST API → "Add key". Choose a user and a
  **permission** of Read, Write, or Read/Write. You get a Consumer Key (`ck_...`) and Consumer
  Secret (`cs_...`) shown once.
- **Auth endpoint (for apps):** direct the user to `/wc-auth/v1/authorize` with `app_name`, `scope`
  (`read`/`write`/`read_write`), `user_id`, `return_url`, and `callback_url`. After the user approves,
  WooCommerce POSTs the generated key/secret to your `callback_url`.

## Request/response format

- Responses are JSON by default.
- Dates are returned in **ISO8601**: `YYYY-MM-DDTHH:MM:SS`.
- **Resource IDs are integers.**
- **Monetary amounts are strings** with two decimal places (e.g. `"29.99"`).
- Item counts are integers.
- Custom fields are exposed in a **`meta_data`** array of `{ "id", "key", "value" }` objects.

## Pagination

- Default: **10 items per page**. Control with `?per_page=` (**max 100**) and `?page=`.
- Total counts are returned in **headers**, not the body:
  - `X-WP-Total` — total number of resources
  - `X-WP-TotalPages` — total number of pages
- A `Link` header provides `next`, `prev`, `first`, and `last` page URLs.
- Common list filters: `?after=` / `?before=` (ISO8601), `?modified_after=`, `?order=`,
  `?orderby=`, `?status=`, `?search=`.

## Errors

Errors return an appropriate HTTP status and a JSON body:

```json
{
  "code": "woocommerce_rest_authentication_error",
  "message": "Consumer key is invalid.",
  "data": { "status": 401 }
}
```
<!-- Constructed from documented error shape — verify against live API -->

Common: `400` invalid params, `401` authentication error (no HTTPS / stripped `Authorization`
header / bad or under-permissioned key), `403` insufficient permission, `404` resource or route not
found (often plain permalinks), `500` server error.

## Rate limits

WooCommerce core imposes **no API rate limit** — throughput is bounded by your WordPress host and
database. (Some managed hosts add their own limits; WooCommerce's own hosting can enable a
configurable REST rate limiter.) Self-throttle bulk jobs.

## Endpoints (overview)

Base path `/wp-json/wc/v3`. Standard CRUD verbs apply: `GET` (list/retrieve), `POST` (create),
`PUT`/`PATCH` (update), `DELETE` (delete). Most collections also expose a `/batch` sub-route.

| Resource | Path | Notes |
|---|---|---|
| Products | `/products`, `/products/{id}` | create/list/get/update/delete/duplicate/batch |
| Product variations | `/products/{product_id}/variations` | for variable products |
| Product categories | `/products/categories` | taxonomy |
| Product attributes | `/products/attributes`, `/products/attributes/{id}/terms` | |
| Product reviews | `/products/reviews` | |
| Orders | `/orders`, `/orders/{id}` | full CRUD + actions |
| Order notes | `/orders/{order_id}/notes` | |
| Order refunds | `/orders/{order_id}/refunds` | |
| Customers | `/customers`, `/customers/{id}` | + `/customers/{id}/downloads` |
| Coupons | `/coupons`, `/coupons/{id}` | |
| Reports | `/reports/sales`, `/reports/top_sellers`, `/reports/totals/*` | read-only |
| Tax rates / classes | `/taxes`, `/taxes/classes` | |
| Shipping | `/shipping/zones`, `/shipping/zones/{id}/methods`, `/shipping_methods` | |
| Payment gateways | `/payment_gateways` | list/get/update |
| Settings | `/settings`, `/settings/{group}` | |
| System status | `/system_status`, `/system_status/tools` | diagnostics |
| Data | `/data/countries`, `/data/currencies` | reference data |
| Webhooks | `/webhooks`, `/webhooks/{id}` | + `/webhooks/{id}/deliveries` |

### Batch operations
Each major collection accepts a batch request that mixes create/update/delete in one call:

```bash
curl -X POST https://example.com/wp-json/wc/v3/products/batch \
  -u ck_xxx:cs_xxx \
  -H "Content-Type: application/json" \
  -d '{
    "create": [ { "name": "Pro License", "type": "simple", "regular_price": "29.99" } ],
    "update": [ { "id": 93, "sale_price": "19.99" } ],
    "delete": [ 42 ]
  }'
```
The batch endpoint processes up to **100 objects per call** (across create+update+delete).

## Top endpoint examples (representative request/response)

### List / retrieve an order
`GET /orders/727`
```json
{
  "id": 727,
  "number": "727",
  "status": "processing",
  "currency": "USD",
  "date_created": "2026-07-04T14:22:07",
  "total": "29.99",
  "customer_id": 12,
  "billing": { "first_name": "Ada", "email": "ada@example.com", "country": "US" },
  "line_items": [ { "id": 315, "product_id": 93, "quantity": 1, "total": "29.99" } ],
  "meta_data": [ { "id": 4021, "key": "_utm_source", "value": "newsletter" } ]
}
```
<!-- Constructed from documented field lists — verify against live API -->

### Create a product
`POST /products`
```json
{
  "name": "Pro License",
  "type": "simple",
  "regular_price": "29.99",
  "virtual": true,
  "downloadable": true,
  "categories": [ { "id": 9 } ],
  "meta_data": [ { "key": "_sku_source", "value": "csv" } ]
}
```
<!-- Constructed from documented field lists — verify against live API -->

### Create a coupon
`POST /coupons`
```json
{ "code": "LAUNCH20", "discount_type": "percent", "amount": "20", "individual_use": true }
```
<!-- Constructed from documented field lists — verify against live API -->

## Webhooks

Create via wp-admin (WooCommerce → Settings → Advanced → Webhooks) or `POST /webhooks`.

### Webhook properties
- `id` — unique identifier
- `name` — label
- `status` — `active` / `paused` / `disabled`
- `topic` — a `resource.event` pair (see below)
- `resource` — entity (`order`, `product`, `customer`, `coupon`, …)
- `event` — `created` / `updated` / `deleted` (or `restored`)
- `delivery_url` — HTTPS endpoint the payload is POSTed to
- `secret` — key used to generate the signature (**defaults to the API user's consumer secret** if
  not set)
- `date_created` / `date_modified`

### Topics
Pattern `resource.event`. Built-in:
- `coupon.created`, `coupon.updated`, `coupon.deleted`
- `customer.created`, `customer.updated`, `customer.deleted`
- `order.created`, `order.updated`, `order.deleted`
- `product.created`, `product.updated`, `product.deleted`
- `product_variation.created`, `product_variation.updated`, `product_variation.deleted`
- Custom `action.{hook_name}` topics can fire on any WordPress action hook.

### Delivery headers
Each POST includes:
- `X-WC-Webhook-Source`
- `X-WC-Webhook-Topic`
- `X-WC-Webhook-Resource`
- `X-WC-Webhook-Event`
- `X-WC-Webhook-Signature` — **base64-encoded HMAC-SHA256** hash of the payload body, keyed by the
  webhook `secret`
- `X-WC-Webhook-ID`
- `X-WC-Webhook-Delivery-ID`

### Signature verification
Compute `base64( HMAC_SHA256( raw_request_body, secret ) )` and compare (constant-time) to the
`X-WC-Webhook-Signature` header. Hash the **raw** body bytes before any JSON parsing.

### Delivery behavior
- Your endpoint should return an HTTP **2xx** quickly.
- WooCommerce logs each delivery (viewable per webhook) and **automatically disables a webhook after
  5 consecutive failed deliveries** (non-2xx or unreachable). A common cause of failure is a security
  plugin (or the "restrict REST API to authenticated users" setting) rejecting the unauthenticated
  delivery request with a 401.

## Store API (headless cart & checkout) — separate namespace

`/wp-json/wc/store/v1` is a **separate, buyer-facing** API for building custom/headless storefronts.
It does **not** use consumer keys — cart and checkout endpoints are session-based via a `Nonce`
header and a `Cart-Token` (JWT) header returned on the first cart request. Key routes include
`/products`, `/cart`, `/cart/add-item`, `/cart/apply-coupon`, and `/checkout`. Use the Store API for
the shopper flow and the v3 REST API for back-office/admin data. Never expose v3 consumer keys in the browser.

## Gaps / verify against live docs

- Full per-field schemas (every product/order/customer property) live in the official docs; only the
  most-used fields are reproduced here. Confirm exact field names against `/system_status` or the
  live docs before a migration.
- Exact Store API route list and token/nonce mechanics evolve — verify against the current Store API docs.
- Some extensions (Subscriptions, Bookings, Memberships) add their own REST routes not covered here.
