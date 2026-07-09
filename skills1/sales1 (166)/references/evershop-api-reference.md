<!-- Source: https://evershop.io/docs/api/overview, /docs/api/authentication, /docs/api/cart, /docs/api/product, /docs/api/order, /docs/development/knowledge-base/events-and-subscribers, /docs/development/knowledge-base/graphql (fetched 2026-06-29) -->

# EverShop API Reference

EverShop exposes **two complementary interfaces**:

- **REST API** — for **creating, updating, and deleting** resources (mutations).
- **GraphQL API** — for **efficient querying** of resources with precise field control (reads). EverShop uses GraphQL both for server-side data fetching and as the storefront/admin read API. There is no broad REST "list/get" surface — read data via GraphQL.

All communication is JSON. Requests require `Content-Type: application/json`; send `Accept: application/json`.

## Authentication

EverShop uses **JWT** for both admin and customer endpoints. **Endpoints without an explicitly defined `access` property are private by default** — they require a valid token.

### Get an admin access token

```
POST /api/user/tokens
Content-Type: application/json

{ "email": "string", "password": "string" }
```

Response contains `accessToken` and `refreshToken`.

```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" \
  --data-raw '{"email":"admin@admin.com","password":"password"}' \
  https://yourdomain.com/api/user/tokens
```

### Get a customer access token

```
POST /api/customer/tokens
{ "email": "string", "password": "string" }   # → { accessToken, refreshToken }
```

### Use the token

Include it on every protected request:

```
Authorization: Bearer <accessToken>
```

### Token expiry (env-configurable, seconds)

| Token | Env var | Default |
|-------|---------|---------|
| Admin access | `JWT_ADMIN_TOKEN_EXPIRY` | `900` (15 min) |
| Admin refresh | `JWT_ADMIN_REFRESH_TOKEN_EXPIRY` | `1296000` (15 days) |
| Customer access | `JWT_CUSTOMER_TOKEN_EXPIRY` | `1800` (30 min) |
| Customer refresh | `JWT_CUSTOMER_REFRESH_TOKEN_EXPIRY` | `2592000` (30 days) |

### Refresh a token

```
POST /api/user/token/refresh        { "refreshToken": "string" }   # admin
POST /api/customer/token/refresh    { "refreshToken": "string" }   # customer
```

## Response & error shapes

Paginated/standard responses:

```json
{ "data": [ ], "links": { }, "meta": { } }
```

Errors:

```json
{ "error": { "status": 400, "message": "..." } }
```

HTTP status codes: 2xx success through 5xx server error.

## Documented REST resource categories

`Attribute`, `Attribute Group`, `Product`, `Variant`, `Category`, `Cart`, `Promotion`, `Order`, `Customer`, `CMS Page`, `Tax`.

---

## Product REST API

> EverShop uses **GraphQL for querying product data** — these REST endpoints are for writes.

### Create a product — `POST /api/products`

Request body (key fields):

```json
{
  "name": "string",
  "description": [ { "id": "string", "size": 0, "columns": [ { "id": "string", "size": 0, "data": {} } ] } ],
  "short_description": "string",
  "url_key": "string",
  "meta_title": "string",
  "meta_description": "string",
  "meta_keywords": "string",
  "status": 1,
  "sku": "string",
  "price": 0,
  "weight": 0,
  "qty": 0,
  "tax_class": null,
  "manage_stock": 1,
  "stock_availability": 1,
  "group_id": 1,
  "visibility": 1,
  "images": ["string"],
  "attributes": [ { "attribute_code": "string", "value": "string|array" } ],
  "category_id": null,
  "options": [
    { "option_name": "string", "option_type": "select|multiselect", "is_required": 1,
      "values": [ { "value": "string", "extra_price": 0 } ] }
  ]
}
```

Response (abbreviated):

```json
{
  "data": {
    "product_id": 281,
    "uuid": "99a7b39ca63211edb46b60d819134f39",
    "sku": "Q7Oq0kxZIMQ5isUyJRbg",
    "price": 43,
    "qty": 123,
    "status": 0,
    "url_key": "Q7Oq0kxZIMQ5isUyJRbg",
    "name": "Q7Oq0kxZIMQ5isUyJRbg",
    "links": [
      { "rel": "view", "href": "/product/Q7Oq0kxZIMQ5isUyJRbg", "action": "GET", "types": ["text/xml"] },
      { "rel": "edit", "href": "/admin/products/edit/99a7b39ca63211edb46b60d819134f39", "action": "GET", "types": ["text/xml"] }
    ]
  }
}
```

### Update a product — `PATCH /api/products/{id}`
`{id}` = product **UUID**. Same schema as create (all fields optional). Returns the updated product `data`.

### Delete a product — `DELETE /api/products/{id}`
`{id}` = product **UUID**. No body. Returns the deleted product `data`.

---

## Cart REST API

> Two flavors: explicit `{cart_id}` (server/agent-driven) and `mine` (the current authenticated customer's cart). All accept `Accept: application/json`.

| # | Action | Method | Path | Body |
|---|--------|--------|------|------|
| 1 | Create a new cart | POST | `/api/carts` | `{ customer_full_name?, customer_email?, items:[{ sku, qty }] }` |
| 2 | Add item to cart | POST | `/api/cart/{cart_id}/items` | `{ sku, qty }` |
| 3 | Remove item | DELETE | `/api/cart/{cart_id}/items/{item_id}` | — |
| 4 | Add customer (contact) | POST | `/api/carts/{id}/contacts` | `{ email }` |
| 5 | Add address | POST | `/api/carts/{id}/addresses` | `{ address: { full_name, telephone, address_1, address_2?, city, province, country, postcode, type:"shipping|billing" } }` |
| 6 | Add shipping method | POST | `/api/carts/{cart_id}/shippingMethods` | `{ method_code }` |
| 7 | Add payment method | POST | `/api/carts/{cart_id}/paymentMethods` | `{ method_code }` |
| 8 | Add shipping note | POST | `/api/carts/{cart_id}/shippingNotes` | `{ note }` |
| 9 | Update item quantity | PATCH | `/api/cart/{cart_id}/items/{item_id}` | `{ qty, action:"increase|decrease" }` |
| 10 | Add item to my cart | POST | `/api/cart/mine/items` | `{ sku, qty }` |
| 11 | Remove item from my cart | DELETE | `/api/cart/mine/items/{item_id}` | — |
| 12 | Update item in my cart | PATCH | `/api/cart/mine/items/{item_id}` | `{ qty, action:"increase|decrease" }` |
| 13 | Checkout cart | POST | `/api/carts/{cart_id}/checkout` | `{ cart_id }` |

Checkout (#13) response confirms the order with `order_id`, `uuid`, and `order_number`.

---

## Order REST API

> All order endpoints require `Authorization: Bearer <admin JWT token>`.

### Create an order — `POST /api/orders`
Body: `{ "cart_id": "string" }`. Response (abbreviated):

```json
{
  "data": {
    "order_id": 274,
    "uuid": "fd0b4f0fd6704ed0b53fa0c64ae7df3c",
    "order_number": "10274",
    "cart_id": 990,
    "currency": "USD",
    "customer_id": 20,
    "customer_email": "buyer@example.com",
    "shipment_status": "unfullfilled",
    "payment_status": "pending",
    "grand_total": 12345,
    "items": [ {} ],
    "shipping_address": {},
    "billing_address": {}
  }
}
```

### Create a shipment — `POST /api/orders/{order_uuid}/shipments`
Body: `{ carrier?, tracking_number? }`. Returns `{ data: { shipment_id, uuid, carrier_name, tracking_number, created_at } }`.

### Update a shipment — `PATCH /api/orders/{order_uuid}/shipments/{shipment_uuid}`
Body: `{ carrier?, tracking_number? }`. Same response shape as create.

### Cancel an order — `POST /api/orders/{id}/cancel`
Body: `{ "reason": "string" }`. Returns `{ "data": {} }`.

### Mark as delivered — `POST /api/deliveries`
Body: `{ "order_id"?: "string" }`. Returns `{ "data": {} }`.

---

## GraphQL (reads)

Each module ships a `graphql/` folder with `.graphql` type definitions (SDL) and `.resolvers.ts` resolvers. The catalog module defines `Product`, `Category`, `Attribute`, etc. with fields like `productId`, `name`, `sku`, `weight`, `categories`.

- **Extend** existing types without editing core files using the SDL `extend` keyword (e.g. add a field to `Product` or `Query`). This is the extension pattern.
- **Admin vs storefront split by filename convention:** `TypeName.admin.graphql` and `TypeName.admin.resolvers.ts` compile **only** into the admin schema and are not exposed to the storefront GraphQL layer.
- The frontend fetches via **URQL** (a full-featured GraphQL client).

Example type fragment:

```graphql
type Product {
  productId: ID!
  name: String
  sku: String
  weight: Decimal
  categories: [Category]
}
```

---

## Events & subscribers (there are NO outbound webhooks)

EverShop has an **event-driven architecture**, but events are **in-process only** — there is **no external webhook delivery** and no UI to register a webhook URL. To notify an external system (CRM, warehouse, Slack), write a subscriber that makes the outbound HTTP call itself.

- **Emit** with `emit` from `@evershop/evershop/lib/event`. An event has a `name` + `data` object. Events are **stored in the database** and subscribers run **asynchronously**; an event is removed from the pool once all subscribers have executed (regardless of result).
- **Subscribe** by creating a `subscribers/` folder in your extension, with one sub-folder per event name; each handler file uses a **default-exported async function** receiving the event data:

```
your-extension/
  subscribers/
    order_placed/
      notifyCRM.ts        # export default async (data) => { ... }
```

```ts
// subscribers/order_placed/notifyCRM.ts
export default async function notifyCRM(data: any) {
  await fetch('https://your-crm.example.com/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ orderId: data.order_id, total: data.grand_total }),
  });
}
```

Type-safe helpers: the `EventSubscriber` type and `createSubscriber` helper; register custom event payload types by extending the `EventDataRegistry` interface.

### Available events

| Domain | Events |
|--------|--------|
| Product | `product_created`, `product_updated`, `product_deleted`, `product_image_added` |
| Category | `category_created`, `category_updated`, `category_deleted` |
| Order | `order_created`, `order_placed` (payment succeeded / offline method), `order_status_updated` |
| Customer | `customer_registered` (account active), `customer_created`, `customer_updated`, `customer_deleted` |
| Inventory | `inventory_updated` (stock changed) |

---

## Gaps / notes

- No published hard rate-limit numbers in the REST docs. Throttle politely and back off on 429/5xx.
- No documented bulk/batch write endpoints — loop with concurrency limits.
- No managed cloud or hosted webhook relay as of the research date — you run Node + PostgreSQL yourself and you own the outbound-integration code.
- Money fields in sample responses appear as plain numbers in the store currency — verify decimal handling against your live instance before relying on it.
