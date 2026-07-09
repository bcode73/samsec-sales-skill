# Swell Platform Reference

## Overview

Swell (swell.is) is an **API-first, headless SaaS commerce backend** for developers and makers — the same backend API powers the admin dashboard, hosted checkout, and any custom storefront you build. Its standout differentiator vs Shopify/BigCommerce is a **native subscription engine** (pause/resume, dunning, separate billing-vs-fulfillment schedules) and flexible **custom data models**, with **no per-transaction platform fee**. You can run it fully headless, on a Swell-hosted Liquid theme (Shopify-tag compatible), or on a visual block-based store builder.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Products** | Products, variants, options, attributes, categories, stock, purchase links, digital/subscription/giftcard delivery | **API** (Backend REST + Frontend swell-js/GraphQL) |
| **Carts & Orders** | Carts, orders, payments, refunds, shipments, returns | **API** + **webhooks** (`order.*`, `cart.*`) |
| **Checkout** | Hosted checkout or fully headless checkout via API | **API**; hosted UI is UI-configured |
| **Subscriptions** | Native recurring billing — intervals, pause/resume, dunning, separate billing/fulfillment schedules, subscription plans | **API** + **webhooks**; **Basic+ plan-gated** |
| **Discounts** | Coupons, coupon codes/generations, promotions (incl. BXGY/automatic), gift cards | **API** |
| **Customers** | Accounts, addresses, cards, account credits, invoices | **API** + **webhooks** (`account.*`) |
| **B2B / Wholesale** | Volume pricing, invoicing, customer groups, price lists | **API**; price lists **Standard+** |
| **Internationalization** | 230 currencies, 170 languages, region price lists | **API**; multi-currency **Standard+** |
| **Content** | Pages, menus, store settings (CMS in admin) | **API** (`/pages`) + UI |
| **Custom data models** | Extend core schema with your own models/fields | **API** + Swell Apps |
| **Swell Apps** | Serverless functions to customize logic / call external APIs, custom dashboard controls | Deployed via **Swell CLI** |
| **Storefronts** | Visual block builder, Liquid themes (Shopify-tag compatible), headless apps hosted on Cloudflare | UI + headless (swell-js/GraphQL) |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on swell.is/pricing. Monthly prices; ~25% off annual.*

| Plan | Price | Annual sales cap | Admin users | API requests/mo | Storage | Notable gates |
|---|---|---|---|---|---|---|
| **Starter** | $29/mo | $50K | 2 | 100K | 1GB | Basic reports; **no subscriptions** |
| **Basic** (popular) | $79/mo | $250K | 5 | 500K | 3GB | **Subscriptions**; no multi-currency |
| **Standard** | $299/mo | $1M | 15 | 2M | 10GB | **Multi-currency**, intl price lists, advanced reports, role-based permissions, priority support |
| **Unlimited** | $2,250/mo | $5M | Unlimited | Unlimited | Unlimited | 100% uptime SLA, developer support |
| **Custom** | Contact sales | >$10M | Custom | Custom | Custom | Dedicated support |

- **No transaction fees** on any plan; no setup fees; free trial available. (No permanent free plan / dev store documented.)
- **Revenue-ceiling overage** if you exceed the annual sales cap: **2% Starter / 1.5% Basic / 1% Standard / 0.4% Unlimited**.
- **API overage**: **$5 per 100K requests** over the monthly limit. **Storage overage**: **$5 per GB/mo**.
- **Integration-break check**: subscriptions need **Basic+**; multi-currency/price-lists need **Standard+**. A high-traffic headless storefront can burn the 100K/500K request caps fast — cache reads and budget for overage.

## Developer surface at a glance

- **Backend API** — REST, base `https://api.swell.store`, **secret key** auth (server-side only). Official libs: **swell-node** (Node), **swell-php** (PHP), which use a custom wire protocol on **port 8443**. Generic REST/HTTP works over 443.
- **Frontend API** — **swell-js** (npm `swell-js`) initialized with the **store ID + public key**; client-side, browser-safe. Also **GraphQL** at `https://<store-id>.swell.store/graphql/v2` (public key in the `Authorization` header; playground at `/playground`).
- **Webhooks** — event-based, configured in **Developer → Webhooks** or by a Swell App. Thin JSON payload, **no HMAC** (secure via IP allowlist + secret URL). See the api-reference for the model and retry/disable behavior.
- **Swell Apps** — serverless functions + custom models + dashboard controls, deployed with the **Swell CLI**.
- **MCP server** — none found as of 2026-06 (you'd wrap the Backend API yourself).
- **iPaaS** — 40+ native integrations; Zapier/Make typically via Swell Apps or community connectors (confirm in-account).

## Data model

Money is stored in the store's currency as decimals (e.g. `19.99`), not cents. IDs are Mongo-style objectIds. Common query params: `limit`, `page`, `where`, `expand`, `fields`, `include`, `search`, `sort`.

**Product** (`/products`):
```json
{
  "id": "5c8fb5e1ed2faf8c79da492a",
  "name": "Classic Tee",
  "slug": "classic-tee",
  "sku": "TEE-001",
  "active": true,
  "price": 29.00,
  "sale": false,
  "sale_price": null,
  "delivery": "shipment",            // shipment | subscription | giftcard | null (digital)
  "stock_tracking": true,
  "stock_level": 120,
  "purchase_options": {
    "standard": { "active": true, "price": 29.00 },
    "subscription": { "active": false, "plans": [] }
  },
  "options": [{ "name": "Size", "values": [{ "name": "M" }, { "name": "L" }] }],
  "images": [{ "file": { "url": "https://cdn.swell.store/..." } }]
}
```

**Order** (`/orders`) — note `account_id`, `items[]`, and `status`:
```json
{
  "id": "5fd3...",
  "number": "100023",
  "account_id": "5fab...",
  "status": "complete",            // pending | complete | canceled | ...
  "paid": true,
  "currency": "USD",
  "sub_total": 58.00,
  "grand_total": 64.50,
  "items": [{ "product_id": "5c8f...", "quantity": 2, "price": 29.00 }],
  "shipping": { "name": "Ada L", "address1": "1 Main St", "country": "US" }
}
```

**Subscription** (`/subscriptions`):
```json
{
  "id": "61aa...",
  "account_id": "5fab...",
  "product_id": "5c8f...",
  "status": "active",              // active | paused | canceled | trial | pastdue | ...
  "interval": "monthly",
  "interval_count": 1,
  "date_period_start": "2026-06-01T00:00:00.000Z",
  "date_period_end": "2026-07-01T00:00:00.000Z",
  "billing_schedule": { "interval": "monthly", "interval_count": 1 }
}
```
<!-- Constructed from Swell docs field lists — verify exact field names against the live Backend API. -->

## Quick-start recipes

### Recipe 1 — List products from a server script (Backend API, secret key)

cURL is awkward with the custom wire protocol, so use the official lib server-side:

```js
// npm i swell-node
const swell = require('swell-node').init('<store-id>', '<secret-key>');

const products = await swell.get('/products', {
  where: { active: true },
  limit: 25,
  page: 1,
  expand: ['variants'],
});
console.log(products.count, products.results.length);
```

```python
# Swell ships Node/PHP libs; from Python use plain REST/HTTP over 443:
import requests
r = requests.get(
    "https://api.swell.store/products",
    params={"where[active]": "true", "limit": 25, "page": 1},
    auth=("<store-id>", "<secret-key>"),   # store id as user, secret key as password
)
r.raise_for_status()
print(r.json().get("count"))
```
*Gotcha:* server-only — never expose the secret key. If `swell-node` hangs, your host is likely blocking **port 8443**; use the REST/HTTP form above over 443.

### Recipe 2 — Storefront product list + add to cart (Frontend API, public key)

```js
// npm i swell-js  — runs in the browser
import swell from 'swell-js';
swell.init('<store-id>', '<public_key>', { useCamelCase: true });

const products = await swell.products.list({ category: 't-shirts', limit: 25, page: 1 });
const cart = await swell.cart.addItem({ product_id: products.results[0].id, quantity: 1 });
```

GraphQL equivalent (public key in the header):
```bash
curl https://<store-id>.swell.store/graphql/v2 \
  -H "Authorization: <public_key>" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ products(limit: 5){ results { id name price } } }"}'
```

### Recipe 3 — React to a new order and push it to a CRM (webhook + Backend API)

1. **Developer → Webhooks → Add**: URL = your endpoint, events = `order.created` (or `subscription.created`, etc.).
2. Handle the thin payload, then fetch the full record by id:

```js
// Express handler — secure by IP allowlist + secret path, ack fast, process async
app.post('/hooks/swell/:secret', async (req, res) => {
  if (req.params.secret !== process.env.SWELL_HOOK_SECRET) return res.sendStatus(403);
  res.sendStatus(200);                                  // 2xx within 10s
  const { type, data } = req.body;                      // {id,date_created,model,type,data:{id,...}}
  if (type === 'order.created') {
    const order = await swell.get('/orders/{id}', { id: data.id });
    await pushToCrm(order);                              // your CRM write
  }
});
```
*Gotcha:* **no HMAC** — verify with Swell's published IP allowlist + the secret path. Non-2xx responses trigger hourly retries (~2 days) then the hook **auto-disables**.

## Integration patterns

- **CRM / warehouse sync.** Webhooks are notifications, not the source of truth — always re-read the full record via the Backend API by `data.id`. For backfills/reconciliation, paginate `GET /orders?limit=100&page=N` (or `/customers`, `/subscriptions`) and sort by `date_created`; dedupe on the Swell `id`. Budget against the plan's monthly API-request cap.
- **Webhook listener.** Acknowledge in <10s and process asynchronously (queue the job). Secure with **IP allowlist + secret URL/header** (no signature to verify). Track delivery yourself — Swell has limited webhook logging and **auto-disables** failing hooks, so monitor the enabled flag and alert on gaps.
- **Headless storefront.** Public key + swell-js/GraphQL in the browser for catalog/cart/account/session; secret key + swell-node in server routes for admin operations. Cache catalog reads (CDN/edge) to stay under the API-request cap on traffic spikes.
- **Subscription migration.** Import existing subscriptions as normal records and **never set `$migrate: true`** (it skips billing-schedule events). Recreate interval, current period, anchor, and payment method; verify the computed **next charge date** in a sandbox before going live; watch the first live cycle.
