# EverShop Platform Reference

## Overview

EverShop is a modern, open-source (**GPL-3.0**) e-commerce platform built on **Node.js + TypeScript + React + GraphQL + PostgreSQL**. Unlike headless-only engines (Medusa, Vendure, Saleor), it ships the **storefront, admin panel, and API in one project** — making it the fastest OSS option to stand up a self-hosted store. It's for developers and makers who want a customizable, fee-free store they fully own, and are comfortable running Node + Postgres. Current line: **v2.x** (v2.1.2, April 2026). Self-host only — managed cloud is "coming soon."

## Capabilities & automation surface

EverShop ships **eight core modules**. Reads are GraphQL; writes are REST; there are **no outbound webhooks** (in-process events only).

| Module | What it does | Automation surface |
|--------|--------------|--------------------|
| **Catalog** | Products, variants, categories, collections, attributes, attribute groups | **REST write** (`/api/products`), **GraphQL read** |
| **Checkout** | Cart, shipping/payment-method selection, checkout → order | **REST** (`/api/carts/...`, `/api/cart/mine/...`) |
| **Customer** | Accounts, addresses, JWT auth | **REST** (`/api/customer/tokens`), **GraphQL read** |
| **OMS** | Orders, shipments, cancellation, delivery status | **REST** (`/api/orders`, `/api/deliveries`) |
| **Promotion** | Coupons / discounts | **REST** (Promotion resource), GraphQL read |
| **CMS** | Pages, dynamic widgets, storefront content | **REST** (CMS Page resource) |
| **Tax** | Tax classes & rates | **REST** (Tax resource) — **not** a Merchant of Record; you own remittance |
| **Setting** | Store config | UI / config |
| Payments (built-in) | Stripe, PayPal, Cash on Delivery | configured per provider; Stripe has its own integration guide |
| Events | `order_placed`, `product_created`, `inventory_updated`, … | **in-process subscribers only** (code in an extension), **NOT** UI-configurable webhooks |
| Extensions / themes | Add modules, GraphQL types, routes, subscribers; theme-based storefront | code (filesystem), marketplace |

**Key implication for integrators:** to *read* data (list products, fetch an order), use **GraphQL**. To *create/update/delete*, use **REST**. To *react to an event* (e.g. notify a CRM on a new order), write an **event subscriber** that makes the HTTP call itself — there is no webhook settings page.

## Pricing, limits & plan gates

- **Software is free** (GPL-3.0) — no per-sale/platform fee. You pay only for your own infra and payment-processor fees.
- **No managed cloud yet** — you run it. Minimum dev box: 2-core / 2 GB RAM / 10 GB. Recommended prod: 4+ core / 4+ GB / 20+ GB SSD. **Large catalogs (10,000+ products): 8 GB RAM minimum.**
- **Requirements:** Node.js **20.x+** (LTS), NPM **9.x+**, PostgreSQL **13+** (15+ recommended). Default app port **3000**, Postgres **5432**.
- **API token expiry is the main integration gate:** admin access tokens expire in **15 minutes** by default — long-running scripts must refresh (`/api/user/token/refresh`) or raise `JWT_ADMIN_TOKEN_EXPIRY`.
- No documented REST rate limits — self-throttle.

## Integrations

- **Built-in payments:** Stripe, PayPal, Cash on Delivery.
- **Commonly wired:** Algolia (search), Klarna, Mailchimp, Netlify (per the homepage). These are integrations you configure/build, not turnkey connectors.
- **Data flow direction:** EverShop is the source of truth. Push catalog *into* it via REST; pull catalog/orders *out* via GraphQL; react to changes via event subscribers that POST outward. No native iPaaS triggers — wire Zapier/Make through a thin custom endpoint or an event subscriber.
- **Extensibility:** drop a module into your project/extensions, extend GraphQL types with the SDL `extend` keyword, add Express routes (file-based middleware), and add subscribers. This is the primary "integration" mechanism.

## Data model

Key objects and their IDs. EverShop carries both an integer primary key (`product_id`, `order_id`) **and** a `uuid`; **REST mutations address resources by `uuid`** (e.g. `PATCH /api/products/{uuid}`).

**Product** (REST create/update response, abbreviated):

```json
{
  "data": {
    "product_id": 281,
    "uuid": "99a7b39ca63211edb46b60d819134f39",
    "sku": "blue-tee",
    "price": 43,
    "qty": 123,
    "status": 1,
    "manage_stock": 1,
    "stock_availability": 1,
    "url_key": "blue-tee",
    "name": "Blue Tee",
    "group_id": 4
  }
}
```

**Order** (from `POST /api/orders`, abbreviated):

```json
{
  "data": {
    "order_id": 274,
    "uuid": "fd0b4f0fd6704ed0b53fa0c64ae7df3c",
    "order_number": "10274",
    "cart_id": 990,
    "currency": "USD",
    "customer_email": "buyer@example.com",
    "shipment_status": "unfullfilled",
    "payment_status": "pending",
    "grand_total": 12345
  }
}
```

**Product (GraphQL read) type fragment:**

```graphql
type Product { productId: ID! name: String sku: String weight: Decimal categories: [Category] }
```

See `references/evershop-api-reference.md` for the full cart/order/auth surface and the event list.

## Quick-start recipes

### Recipe 1 — Stand up a store (install + admin user)

```bash
# Fastest path (creates ./my-store and installs deps)
npx create-evershop-app my-store
#   add --playAround to seed demo data

cd my-store
# Manual/Node path instead of create-evershop-app:
#   npm install @evershop/evershop
#   add scripts: setup/build/start/dev/seed/user:create -> "evershop <cmd>"
npm run setup          # generates .env (DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD/DB_SSLMODE), runs migrations
npm run build
npm run start          # storefront :3000, admin :3000/admin

# Create an admin user
npm run user:create -- --email "admin@yourstore.com" --password "Str0ngP@ss!" --name "Admin"
```

Gotchas: needs Node **20+** (build fails on older); ensure `public/`, `.evershop`, `.log`, `media` are writable; in production run under a process manager (pm2/systemd) — see Gotchas about the server going unresponsive.

### Recipe 2 — Authenticate and create a product via REST

```bash
# 1) Get an admin token (expires in 15 min by default)
TOKEN=$(curl -s -H "Content-Type: application/json" -H "Accept: application/json" \
  --data-raw '{"email":"admin@yourstore.com","password":"Str0ngP@ss!"}' \
  https://yourstore.com/api/user/tokens | python3 -c 'import sys,json;print(json.load(sys.stdin)["data"]["accessToken"])')

# 2) Create a product (url_key/sku must be a clean slug — lowercase, no spaces)
curl -s -X POST https://yourstore.com/api/products \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  --data-raw '{"name":"Blue Tee","sku":"blue-tee","url_key":"blue-tee","price":29.99,"qty":100,"status":1,"group_id":1,"manage_stock":1,"stock_availability":1}'
```

```python
import requests

BASE = "https://yourstore.com"
auth = requests.post(f"{BASE}/api/user/tokens",
                     json={"email": "admin@yourstore.com", "password": "Str0ngP@ss!"},
                     headers={"Accept": "application/json"}).json()
token = auth["data"]["accessToken"]
h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

r = requests.post(f"{BASE}/api/products", headers=h, json={
    "name": "Blue Tee", "sku": "blue-tee", "url_key": "blue-tee",
    "price": 29.99, "qty": 100, "status": 1, "group_id": 1,
    "manage_stock": 1, "stock_availability": 1,
})
print(r.json()["data"]["uuid"])     # use this uuid for PATCH/DELETE
```

### Recipe 3 — Notify a CRM/warehouse when an order is placed (the "webhook" replacement)

There is **no webhook URL field**. Add an event subscriber to an extension:

```ts
// <project>/extensions/crm-sync/subscribers/order_placed/notifyCRM.ts
export default async function notifyCRM(order: any) {
  await fetch("https://your-crm.example.com/hooks/order", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      orderNumber: order.order_number,
      email: order.customer_email,
      total: order.grand_total,
    }),
  });
}
```

Enable the extension in the config, rebuild, restart. Because subscribers run **async in-process**, the outbound call won't block checkout — but you own retries/idempotency/logging. For higher reliability, have the subscriber enqueue to a real queue (BullMQ/Redis) and process there.

## Integration patterns

- **Catalog sync (push):** loop your source catalog → `POST /api/products` for new SKUs, `PATCH /api/products/{uuid}` for updates. Persist the returned `uuid` keyed by your SKU so updates/deletes can address the right record. Refresh the admin token before it expires.
- **Order/catalog export (pull):** query **GraphQL** for reads (there's no broad REST list endpoint). Request only the fields you need; page through results; cache where possible.
- **Event → external system:** prefer an event subscriber over polling. If you can't deploy code into the store, fall back to **polling** orders via GraphQL on a schedule and tracking the last-seen `order_id`. Subscribers are the right tool; polling is the fallback.
- **Auth lifecycle:** treat the 15-min admin access token as short-lived. Store the `refreshToken`, and on `401` call `POST /api/user/token/refresh` and retry once. Or set `JWT_ADMIN_TOKEN_EXPIRY` higher for server-to-server jobs (trade off security).
- **Self-host ops:** run under pm2/systemd with auto-restart, put PostgreSQL on SSD, give large catalogs 8 GB+ RAM, and reverse-proxy behind nginx with TLS (port 443) → app on 3000.
