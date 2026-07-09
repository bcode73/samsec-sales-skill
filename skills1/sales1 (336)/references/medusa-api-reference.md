<!-- Source: https://docs.medusajs.com/api/admin -->
<!-- Source: https://docs.medusajs.com/api/store -->
<!-- Source: https://docs.medusajs.com/resources/commerce-modules/auth/authentication-route -->
<!-- Source: https://docs.medusajs.com/learn/fundamentals/events-and-subscribers -->
<!-- Captured 2026-06-28. Verbatim excerpts from Medusa v2 docs, enriched with developer context. -->

# Medusa v2 API Reference

Medusa exposes two REST API surfaces plus an auth route set:

- **Admin API** — Admin functionality / building an admin dashboard. All routes prefixed with `/admin`. In dev: `http://localhost:9000/admin`. In production replace the host with your Medusa application URL.
- **Store API** — Storefront functionality (webshop, mobile app). Routes prefixed with `/store`.
- **Auth routes** — Obtain tokens. Prefixed with `/auth`.

## Authentication

There are three ways to send authenticated requests to the Medusa server.

### 1. Bearer Authorization (JWT token)

Obtain a token by sending credentials to an authentication route (see Auth Routes below). The response includes a `token` property. Send it as:

```
Authorization: Bearer {jwt_token}
```

The JS SDK's `login` method manages tokens automatically, or use `client.setToken` manually. Set the SDK's `auth.type` to `jwt` to use JWT tokens.

### 2. API Token (Basic auth)

Create an API key from the Medusa Admin or via the Create API Key endpoint. Pass it in the **Authorization Basic** header:

```
Authorization: Basic {api_token}
```

> Previous versions required base64-encoding the token; in v2 this remains supported but is **optional** — you may pass the raw secret key.

### 3. Cookie Session ID

Requires obtaining a JWT token first. Set the SDK's `auth.type` to `session`.

- **Obtain:** send `POST /auth/session` with JWT bearer authorization. The response includes a `Set-Cookie: connect.sid=...` header.
- **Use (cURL):** `Cookie: connect.sid={sid}`
- **Use (Fetch):** include the `credentials: "include"` option.

### Storefront publishable API key

Store API requests are scoped to a sales channel by a **publishable API key**, sent in the header:

```
x-publishable-api-key: {pk_...}
```

Without it, Store API requests error or return empty results.

## Auth Routes (obtaining tokens)

Verbatim from the authentication-route docs:

### Register route

**Path:** `/auth/{actor_type}/{provider}/register` — creates an auth identity and returns a token.

```bash
curl -X POST http://localhost:9000/auth/customer/emailpass/register \
-H 'Content-Type: application/json' \
--data-raw '{
  "email": "user@example.com",
  "password": "REDACTED"
}'
```

**Response:**
```json
{
  "token": "eyJhbGc..."
}
```

### Login route

**Path:** `/auth/{actor_type}/{provider}` — authenticates existing users.

```bash
curl -X POST http://localhost:9000/auth/customer/emailpass \
-H 'Content-Type: application/json' \
--data-raw '{
  "email": "user@example.com",
  "password": "REDACTED"
}'
```

For third-party providers the response may include a `location` property for redirect authentication.

### Validate callback route

**Path:** `/auth/{actor_type}/{provider}/callback` — handles third-party service redirects with query parameters like `code` and `state`.

### Token refresh

**Path:** `/auth/token/refresh` — refreshes and repopulates user information in the token after third-party authentication.

### Using the token

```bash
curl -X POST http://localhost:9000/store/customers \
-H 'Authorization: Bearer {token}' \
-H 'Content-Type: application/json'
```

> `actor_type` is `user` for admin users and `customer` for storefront customers; `provider` is e.g. `emailpass` (email/password), or an OAuth provider id (`google`, etc.).

## Pagination

**Query parameters:**
- `limit` — maximum items returned
- `offset` — items to skip before the result set

**Response fields:**
- `limit`, `offset`, and `count` (total number of available items)

**Sorting:**
- `order` — sort by a field (e.g. `created_at`). Default ascending; prefix with `-` for descending (e.g. `order=-created_at`).

Walk pages by incrementing `offset` by `limit` until `offset >= count`.

## Main resource endpoints

Admin API resources (each supports the standard list / retrieve / create / update / delete where applicable):

Products, Orders, Customers, Cart / Draft Orders, Collections, Categories, Variants, Inventory Items, Fulfillments, Payments, Returns, Exchanges, Gift Cards, Promotions, Price Lists, Regions, Sales Channels, Shipping Options, Stock Locations, Tax Rates, Users, API Keys, and Workflows Executions.

Example top-5 CRUD against `/admin/products`:

```bash
# List (paginated)
curl -s "$BASE/admin/products?limit=50&offset=0&order=-created_at" -H "Authorization: Bearer $TOKEN"

# Retrieve one
curl -s "$BASE/admin/products/prod_01H..." -H "Authorization: Bearer $TOKEN"

# Create
curl -s -X POST "$BASE/admin/products" -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"title":"New Product","status":"draft"}'

# Update
curl -s -X POST "$BASE/admin/products/prod_01H..." -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' --data '{"status":"published"}'

# Delete
curl -s -X DELETE "$BASE/admin/products/prod_01H..." -H "Authorization: Bearer $TOKEN"
```

List responses wrap the collection under the resource name plus pagination meta, e.g.:

```json
{ "products": [ { "id": "prod_01H...", "title": "..." } ], "count": 230, "offset": 0, "limit": 50 }
```

<!-- Constructed from documented pagination fields — verify exact wrapper key per endpoint. -->

## Rate limits

No public API rate limit is documented in the Medusa docs. Self-hosted limits are whatever your infrastructure imposes; on Medusa Cloud, compute hours / edge requests are metered per plan (see platform-guide.md). Throttle bulk jobs defensively regardless.

## Events and Subscribers (Medusa's "webhook" substitute)

Verbatim from the events-and-subscribers docs:

> Medusa's event system enables you to "perform an action after a commerce operation is performed." Unlike webhooks in other platforms, you don't need separate applications — you write the logic directly in your codebase.

When core commerce features execute, Medusa **emits events**. You listen to these events through **subscribers**, which are asynchronous functions executed when the associated event is emitted.

**Key distinction:** Subscribers handle actions *not integral to the original flow* (e.g. sending confirmation emails). For critical operations that affect the main flow, use **workflow hooks** instead — a failing subscriber will not roll back the original operation.

**File location:** `src/subscribers` directory.

**Example** (`src/subscribers/order-placed.ts`):

```ts
import { SubscriberArgs, type SubscriberConfig } from "@medusajs/framework"

export default async function orderPlacedHandler({
  event: { data },
  container,
}: SubscriberArgs<{ id: string }>) {
  const logger = container.resolve("logger")
  logger.info("Sending confirmation email...")
}

export const config: SubscriberConfig = {
  event: `order.placed`,
}
```

**SubscriberArgs shape** — the subscriber function receives:
- `event` — object containing event details; `event.data` holds the payload (typically `{ id }`).
- `container` — the Medusa container for resolving registered resources (services, logger, etc.).

The `config` object accepts either a single event string or an array of event strings for multiple events.

A complete list of emitted events (e.g. `order.placed`, `order.updated`, `customer.created`, `product.created`) is in the events reference: `https://docs.medusajs.com/resources/references/events`.

### Event Module options (pub/sub backend)

The subscription and emitting of events is handled by an **Event Module** (an Infrastructure Module implementing pub/sub):

- **Local Event Module** — default; for development. No additional setup, but in-memory (events are lost on restart, doesn't scale across processes).
- **Redis Event Module** — for production; uses Redis to implement the pub/sub system.
- **Custom Event Module** — implement pub/sub with a different service/logic.

### Sending to external systems (outbound "webhooks")

Webhooks to external URLs are **not natively built-in**. Implement them via:
- a **subscriber** that makes the outbound HTTP call yourself (add your own retries, signing, logging), or
- the **Notification Module** (for emails/SMS/etc. via providers), or
- a community plugin such as `@lambdacurry/medusa-webhooks` or `medusa-events-webhooks`, which register webhook URLs and send events for order, order-edit, payment, customer, and cart events.

## Error response shape

<!-- Constructed from documented Medusa error conventions — verify against live API. -->

Errors return a non-2xx status with a JSON body, e.g.:

```json
{ "type": "not_found", "message": "Order with id order_01H... was not found" }
```

Common `type` values include `not_found` (404), `invalid_data` (400), and `unauthorized` (401). Authenticate (or add the publishable key) and check the `message` for the failing field.

## JS SDK quick note

`@medusajs/js-sdk` (v2) wraps both APIs and handles auth. Configure `auth.type` to `jwt` or `session`; `sdk.auth.login(...)` performs the auth-route call and stores the token; `sdk.admin.*` / `sdk.store.*` call the respective surfaces. The legacy `@medusajs/medusa-js` client and `medusa-react` hooks target **v1** and are not compatible with v2 routes.
