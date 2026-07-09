<!-- Source: https://developers.swell.is/backend-api/introduction, /backend-api/authentication, /backend-api/products, /backend-api/webhooks, /frontend-api/introduction, /frontend-api/setup, /frontend-api/frontend-libraries/graphql (fetched 2026-06-29) -->

# Swell API Reference

Swell exposes two API surfaces that share one data model:

- **Backend API** — server-side, full access, authenticated with a **secret key**.
- **Frontend API** — client-side (browser-safe), authenticated with a **public key**, available via the **swell-js** library or **GraphQL**.

Get the **Store ID**, **secret key**, and **public key** from the Swell dashboard under **Developer → API keys** (a.k.a. **Settings → API**). The store ID is shown at the top of that page; click the eye icon to reveal/copy the secret key. Keys can be added or revoked if compromised.

---

## Backend API

> Verbatim from docs: "The Swell Backend API follows REST principles, utilizing predictable resource-oriented URLs, standard HTTP verbs, and response codes. It processes JSON-encoded requests and responses."

- **Base URL:** `https://api.swell.store`
- **Official libraries:** `swell-node` (Node.js), `swell-php` (PHP).
- **Connection requirement (verbatim):** "Official libraries use a custom wire protocol that improves performance and caching. When using these libraries, your server must be able to connect to the API on port **8443**."

### Authentication

```javascript
// Node.js (swell-node)
const swell = require('swell-node').init('store-id', 'secret-key');
```

Plain REST/HTTP fallback over port 443 (HTTP Basic — store ID as username, secret key as password):

```bash
curl https://api.swell.store/products \
  -u '<store-id>:<secret-key>' \
  -G --data-urlencode 'where[active]=true' --data-urlencode 'limit=25'
```

### Resource models

- **Products:** Products, Variants, Stock, Categories, Attributes, Purchase Links
- **Orders:** Carts, Orders, Payments, Refunds, Shipments, Returns
- **Subscriptions:** Subscriptions, Subscription Plans
- **Customers:** Accounts, Account Addresses, Account Cards, Account Credits, Invoices
- **Discounts:** Coupons, Coupon Codes, Coupon Generations, Promotions, Gift Cards
- **Content:** Pages
- **System:** Data Models, Events, Webhooks, Files

Additional doc sections: querying records, updating records, aggregation, localization, and formula functionality.

### CRUD operations (verbatim examples)

**List**
```javascript
await swell.get('/products', {
  where: { active: true },
  limit: 25,
  page: 1,
});
```

**Retrieve**
```javascript
await swell.get('/products/{id}', {});
```

**Create**
```javascript
await swell.post('/products', {
  name: 'T-Shirt',
  price: 99.00,
  active: true,
  options: [{ name: 'Size', values: [/* ... */] }]
});
```

**Update**
```javascript
await swell.put('/products/{id}', {
  id: '5c8fb5e1ed2faf8c79da492a',
  price: 19.98,
  $set: { options: [/* ... */] }
});
```

**Delete**
```javascript
await swell.delete('/products/{id}', {
  id: '5c8fb5e1ed2faf8c79da492a'
});
```

### Query parameters

`limit`, `page`, `where`, `expand`, `fields`, `include`, `search`, `sort`.

- **Pagination:** page-based — `limit` (page size) + `page` (1-indexed). Responses include `count` (total) and `results[]`. Walk `page` until `results.length < limit`.
- **Expansion:** `expand: ['variants']` inlines related records.

### The Product model (key fields, verbatim list)

- `id` (objectId) — unique identifier
- `name` (string, required) — product name
- `active` (boolean) — storefront visibility
- `price` (currency) — list price
- `sale` (boolean) / `sale_price` (currency) — sale state and price
- `sku` (string, required) — stock keeping unit
- `slug` (string, required) — URL-friendly identifier
- `purchase_options` — standard or subscription purchase config
- `variants`, `options` — product variations
- `stock_tracking`, `stock_level` — inventory
- `images`, `description` — product details
- `delivery` — fulfillment method: `shipment`, `subscription`, or `giftcard` (digital = none)

---

## Frontend API (swell-js)

Client-side library for storefronts; authenticated with the **public key**.

### Setup (verbatim)

```javascript
swell.init('<store-id>', '<public_key>', options)
```

`useCamelCase` option transforms responses snake_case → camelCase:

```javascript
const options = {
  useCamelCase: true, // default false
};
swell.init('<store-id>', '<public_key>', options)
```

### Listing products (verbatim)

```javascript
import swell from 'swell-js';
swell.init('my-store', 'pk_...');

await swell.products.list({
  category: 't-shirts',
  limit: 25,
  page: 1,
});

// expand active variants
await swell.products.list({
  limit: 25,
  page: 1,
  expand: ['variants'],
});
```

### Frontend API sections

Getting Started (intro, frontend libraries, setup); Products (products, attributes, categories); Accounts (user management, sessions, recovery, addresses, credit cards, order history); Orders (carts, orders, payments); Discounts (coupons, promotions, gift cards); Subscriptions; Store (settings, currencies, localization, menus, payment settings).

---

## Frontend API (GraphQL)

- **Endpoint:** `https://<store-id>.swell.store/graphql/v2`
- **Auth:** add your **public key** to the HTTP `Authorization` header.
- **Playground:** `https://<store-id>.swell.store/playground` (log in to the dashboard first).

```bash
curl https://<store-id>.swell.store/graphql/v2 \
  -H "Authorization: <public_key>" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ products(limit: 5){ results { id name price } } }"}'
```

---

## Webhooks

Configured in the dashboard under **Developer → Webhooks**, or by a Swell App. Event-based: subscribe to events that occur on any data model.

### The webhook model (fields)

| Field | Meaning |
|---|---|
| `id` | Unique identifier (auto-generated) |
| `alias` | Reference name |
| `url` | Endpoint URL (**required**) |
| `events` | Array of trigger events (**required**) |
| `enabled` | Boolean status (defaults to `false`) |
| `auto_disabled` | Auto-disabled after 7 days of failures |
| `retry_disabled_events` | Whether to retry failed events |
| `attempts_failed` | Count of failed attempts |
| `date_first_failed`, `date_last_warned`, `date_final_attempt` | Failure tracking |
| `schedule` | Optional object: `hour`, `month_day`, `month`, `week_day` |

### Receiving webhooks — payload shape

Payloads arrive as JSON **POST** requests:

```json
{
  "id": "<event-id>",
  "date_created": "2026-06-29T12:00:00.000Z",
  "model": "order",
  "type": "order.created",
  "data": { "id": "<record-id>" }
}
```

`data` contains the associated record's `id` (and a subset of fields) — use it to GET the full record from the Backend API. Event `type` is `{model}.{action}` (e.g. `order.created`, `order.updated`, `subscription.created`, `account.created`).

### Origin verification (no HMAC)

There is **no HMAC signature**. Verify origin with the **allowed Swell IP addresses**:

```
52.52.111.237
54.219.85.17
54.241.235.166
216.218.185.0/27
216.218.244.192/27
74.80.234.0/24
```
<!-- Verify the current IP allowlist against live docs before relying on it for production firewalling. -->

Also secure the endpoint with a **secret URL path or custom header** of your own.

### Responding & retry behavior

- Handler **must return a 2xx** HTTP status. Timeout is **10 seconds**.
- Non-2xx → retries **hourly for ~2 days**, then continued hourly delivery **with email alerts**.
- After **~3 days** without success the webhook **disables automatically**; `auto_disabled` trips after **7 days** of failures.

---

## Rate limits & plan caps

Swell meters by **monthly API request count per plan** (not a per-second header limit documented publicly):

- Starter 100K, Basic 500K, Standard 2M, Unlimited unlimited.
- **Overage: $5 per 100,000 requests** over the plan limit.
- Throttle politely and cache reads; a busy headless storefront can exhaust the lower caps quickly.

## Error responses

Standard HTTP status codes with JSON bodies. A typical error looks like:

```json
{ "errors": { "name": { "code": "REQUIRED", "message": "Name is required" } } }
```
<!-- Constructed from documented error conventions — verify the exact error envelope against the live API. -->

## Gaps / to verify against live docs

- Exact, complete **event-type catalog** for webhooks (only representative `{model}.{action}` events confirmed).
- Whether any **per-second/burst** rate limit exists beyond the monthly request cap.
- Precise **error envelope** shape and codes.
- Current **IP allowlist** (IPs can change — re-check before firewalling).
- **Zapier/Make** trigger/action inventory (integrations exist; confirm specifics in-account).
