<!-- Source: https://developer.shopware.com/docs/guides/integrations-api/ , https://developer.shopware.com/docs/guides/integrations-api/admin-api/ , and https://github.com/shopware/docs/blob/main/resources/references/app-reference/webhook-events-reference.md — captured 2026-07-04. Content is quoted/summarized from the official docs; representative JSON is marked as constructed. -->

# Shopware 6 API — Reference

Shopware exposes two HTTP APIs:

- **Admin API** — "for backend operations such as products, orders, customers, plugins, and (via the
  Sync API) bulk processing." Base path **`/api/*`**.
- **Store API** — "for storefront-facing interactions such as headless frontends, mobile apps, carts,
  checkout, and sales channel access." Base path **`/store-api/*`**.

## Admin API — Authentication (OAuth 2.0)

The Admin API uses OAuth 2.0. First create an **Integration** in Administration under
**Settings → System → Integrations**, which yields two credentials:

- **Access key ID** (maps to `client_id`)
- **Secret access key** (maps to `client_secret`)

**Token endpoint:** `POST /api/oauth/token`

```json
{
  "grant_type": "client_credentials",
  "client_id": "YOUR_ACCESS_KEY_ID",
  "client_secret": "YOUR_SECRET_ACCESS_KEY"
}
```

Response includes `access_token` (Bearer token), `token_type`, and `expires_in` (3600 seconds).
A `password` grant also exists (for admin-user login with `username`/`password`, returning a
`refresh_token`), but integrations should use `client_credentials`.

```bash
curl "http://127.0.0.1:8000/api/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "YOUR_ACCESS_KEY_ID",
    "client_secret": "YOUR_SECRET_ACCESS_KEY"
  }'
```

Use the Bearer token on subsequent calls:

```bash
curl -X POST "http://127.0.0.1:8000/api/search/product" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Store API — Authentication

The Store API uses a **sales channel access key** (Administration → **Sales Channels → [channel] →
API access**), passed as a header:

```
sw-access-key: YOUR_ACCESS_KEY
```

```bash
curl "http://127.0.0.1:8000/store-api/product" \
  -H "sw-access-key: YOUR_ACCESS_KEY"
```

Cart/checkout calls also use an `sw-context-token` header to carry the shopper's session/cart context.

## The search Criteria model (Admin API)

Most reads go through `POST /api/search/{entity}` with a JSON **Criteria** body. Both APIs "support
search criteria including filtering, sorting, and pagination; responses are context-aware based on
permissions or sales channel state."

Criteria fields:
- `filter` — array of filters (`equals`, `equalsAny`, `contains`, `range`, `multi`, …)
- `sort` — array of `{ "field": "...", "order": "ASC|DESC" }`
- `limit`, `page` — pagination (page-based, not offset)
- `total-count-mode` — `0` none, `1` exact, `2` next-page-exists
- `associations` — eager-load related entities
- `aggregations` — server-side aggregations (counts, stats, buckets)

Example:
```json
{
  "limit": 50,
  "page": 1,
  "total-count-mode": 1,
  "filter": [{ "type": "equals", "field": "active", "value": true }],
  "sort": [{ "field": "createdAt", "order": "DESC" }],
  "associations": { "categories": {} }
}
```
<!-- Constructed from documented Criteria fields — verify against live API -->

Response shape: `{ "data": [ ... ], "total": N, "aggregations": { ... } }`.

## CRUD endpoints (Admin API)

Standard verbs on `/api/{entity}`:

| Operation | Method + path |
|---|---|
| List | `GET /api/{entity}` |
| Search | `POST /api/search/{entity}` (Criteria body) |
| Get one | `GET /api/{entity}/{id}` |
| Create | `POST /api/{entity}` |
| Update | `PATCH /api/{entity}/{id}` |
| Delete | `DELETE /api/{entity}/{id}` |

IDs are **32-character hex UUIDs** (no dashes), typically generated client-side for creates.

## Sync API (bulk)

For bulk create/update/delete across entities in a single request:

`POST /api/_action/sync`

```json
[
  {
    "action": "upsert",
    "entity": "product",
    "payload": [
      { "id": "…", "name": "Pro License", "stock": 100 }
    ]
  },
  {
    "action": "delete",
    "entity": "product",
    "payload": [ { "id": "…" } ]
  }
]
```
<!-- Constructed from documented sync structure — verify against live API -->

Use this instead of per-row requests to stay within the rate limit.

## Rate limits

- **Admin API: 300 requests per minute.**
- **Store API: varies by server configuration.**

On `429`, back off (exponential) and resume. Batch writes via the Sync API and enable HTTP
cache/Redis/OpenSearch to reduce request volume.

## Errors

Errors return a JSON `errors` array with a status and detail, e.g.:

```json
{ "errors": [ { "status": "401", "code": "…", "title": "Unauthorized", "detail": "…" } ] }
```
<!-- Constructed from documented error shape — verify against live API -->

Common: `400` invalid Criteria/body, `401` bad/expired token or wrong key source (plugin-returned
keys frequently can't mint tokens; use an Integration), `403` missing integration permission,
`404` unknown entity/id, `429` rate limit.

## Webhooks (App system)

Webhooks are registered by **apps** via a `<webhooks>` block in the app **manifest**, each with a
`name`, `url`, and `event`. Add `onlyLiveVersion="true"` to fire only for live-version writes (e.g.
placed orders, not drafts).

```xml
<webhooks>
    <webhook name="order-placed"
             url="https://my-app.example.com/webhook/order-placed"
             event="checkout.order.placed"
             onlyLiveVersion="true"/>
</webhooks>
```

### Signature verification
"Every webhook request should have a SHA256 HMAC of the request body that is signed with the secret
your app assigned the shop during the registration. You can verify the authenticity of the incoming
request by checking the **`shopware-shop-signature`**." Recompute `HMAC-SHA256(raw_body, app_secret)`
and compare constant-time.

### Payload structure
Payloads include a `source` object (`url`, `appVersion`, `shopId`), a `data` object (the `event` name
and a `payload` describing the affected `entity` and `operation` — `insert`/`update`/`delete`), and a
`timestamp`.

```json
{
  "source": { "url": "https://shop.example.com", "appVersion": "1.0.0", "shopId": "…" },
  "data": {
    "event": "checkout.order.placed",
    "payload": [ { "entity": "order", "operation": "insert", "id": "…" } ]
  },
  "timestamp": 1750000000
}
```
<!-- Constructed from documented payload description — verify against live API -->

### Available webhook events (verbatim list)

**Checkout & customer:**
`checkout.customer.before.login`, `checkout.customer.changed-payment-method`,
`checkout.customer.deleted`, `checkout.customer.double_opt_in_guest_order`,
`checkout.customer.double_opt_in_registration`, `checkout.customer.guest_register`,
`checkout.customer.login`, `checkout.customer.logout`, `checkout.customer.register`

**Order & payment:**
`checkout.order.payment_method.changed`, `checkout.order.placed`, `order.written`, `order.deleted`

**State transitions:**
`state_enter.order.state.*` (cancelled, completed, in_progress, open),
`state_enter.order_delivery.state.*` (shipping states),
`state_enter.order_transaction.state.*` (paid, authorized, failed, …),
`state_leave.order.*` (exit equivalents)

**Entity write/delete:**
`product.written`/`product.deleted`, `product_price.written`/`product_price.deleted`,
`category.written`/`category.deleted`, `customer.written`/`customer.deleted`,
`customer_address.written`/`customer_address.deleted`, `media.written`/`media.deleted`,
`document.written`/`document.deleted`, `sales_channel.written`/`sales_channel.deleted`,
`order_address.written`/`order_address.deleted`

**Communication:**
`contact_form.send`, `review_form.send`, `mail.after.create.message`, `mail.before.send`,
`mail.sent`, `newsletter.confirm`, `newsletter.register`, `newsletter.unsubscribe`

**App lifecycle:**
`app.activated`, `app.deactivated`, `app.deleted`, `app.installed`, `app.updated`, `shopware.updated`

**Other:**
`customer.group.registration.accepted`/`declined`, `customer.recovery.request`,
`user.recovery.request`, `product_export.log`

## Flow Builder

Flow Builder (Rise tier and up) reacts to business events with actions — send mail, set order/tag
state, and **call a webhook / HTTP endpoint** — configured in the Administration rather than in code.
It's the no-code sibling of app webhooks for merchants who can't deploy an app.

## Gaps / verify against live docs

- Full per-entity field schemas live in the official docs and the generated OpenAPI (`/api/_info/openapi3.json`).
  Only the most-used fields are reproduced here.
- Exact Store API route list and context/cart token mechanics evolve — verify against the current Store API docs.
- The webhook event list reflects the reference at capture time; new events are added across versions.
