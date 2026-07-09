# Medusa Platform Reference

## Overview

Medusa is an MIT-licensed, open-source **headless commerce engine** written in TypeScript/Node.js — you own the storefront, checkout, admin, orders, and data, with no per-sale platform fee and no lock-in. It's a **framework you build on** (like a self-hostable Shopify backend), aimed at developers, GTM/commerce engineers, and AI agents (it ships an "Agent Harness": CLI, dev agent, and an MCP server). Differentiator vs Shopify/commercetools: full code-level customization via a modular architecture, self-host or use managed Medusa Cloud.

## Capabilities & automation surface

Each capability tagged by how you automate it: **API** (REST Admin/Store), **event** (internal event + subscriber), or **UI-only** (Admin dashboard).

- **Products / variants / collections / categories** — full CRUD. *(API: `/admin/products`, `/store/products`)*
- **Orders, draft orders, returns, exchanges, fulfillments** — manage the order lifecycle. *(API: `/admin/orders`; emits events like `order.placed`)*
- **Carts & checkout** — build the buyer flow on the Store API. *(API: `/store/carts`, completion → order)*
- **Customers & customer groups** — accounts, auth, B2B groups. *(API: `/admin/customers`, `/store/customers`)*
- **Promotions / discounts / price lists** — promotion engine, tiered/region pricing. *(API: `/admin/promotions`, `/admin/price-lists`)*
- **Regions, currencies, tax rates, shipping options** — multi-region/currency/tax config. *(API)*
- **Inventory & stock locations** — multi-warehouse inventory. *(API: `/admin/inventory-items`, `/admin/stock-locations`)*
- **Sales channels** — multi-channel; storefronts scoped by **publishable API key**. *(API + UI)*
- **API keys** — create publishable (storefront) and secret (admin) keys. *(API: `/admin/api-keys` + UI)*
- **Events / subscribers** — react to commerce events in code; **the substitute for outbound webhooks**. *(event — code in `src/subscribers/`)*
- **Notification Module** — send emails/SMS/etc. via providers from subscribers. *(API/config in code)*
- **Workflows & workflow hooks** — durable, multi-step commerce logic; hooks run on the critical path (unlike async subscribers). *(code: `@medusajs/framework/workflows-sdk`)*
- **Admin dashboard** — customizable React admin; unlimited admin users on all Cloud plans. *(UI; extendable via custom routes/widgets)*
- **MCP server** — Model Context Protocol server so LLMs/agents can drive the store. *(programmatic, agentic)*

## Pricing, limits & plan gates

The **engine is free (MIT), 0% GMV/platform fee on every tier**, self-host at no license cost. **Medusa Cloud** sells managed infra (Postgres, Redis, deploys, autoscaling). Best-effort 2026-06:

| Plan | Price | Position | Key gates |
|---|---|---|---|
| **Develop** | $29/mo | dev/preview, "zero-config" | 1 shared server, 150 compute hrs/mo, **no custom domain**, **no autoscaling**, no zero-downtime deploy, no backups; email 100/day (1,000/mo) |
| **Launch** | $99/mo | production-ready | 2 shared servers, 800 compute hrs/mo, **custom domains**, **autoscaling**, zero-downtime deploy, 7-day backups, 1,500 emails/day |
| **Scale** | $299/mo | growing stores/teams | autoscaling 2 servers + 1 worker, 2,800 compute hrs/mo, **background workers**, 14-day backups, 3 seats |
| **Enterprise** | custom | SLAs | **SSO/RBAC/audit logs**, dedicated support, custom config |

- **Always included (all Cloud tiers):** unlimited orders, products, sales channels, regions/currencies; unlimited Admin dashboard users.
- **Overages:** object storage $0.025/GB-mo, DB storage $0.5/GB-mo, edge requests $0.3/1M, email $0.7/1,000.
- **Seats:** Develop/Launch include 1 Cloud seat (then $30/seat); Scale includes 3.
- **No published self-host pricing** — you pay only your own infra; export data anytime (no lock-in).
- **Rate limits:** no documented public API rate limit — throttle your own bulk jobs.

## Integrations

- **Direction:** the Admin/Store REST APIs are fully bidirectional (read + write). External systems integrate by (a) calling the APIs, or (b) receiving pushes from **your** subscriber code.
- **No native iPaaS/Zapier app and no outbound-webhook UI** — push to Zapier/n8n/CRM by calling their webhook URL from a Medusa subscriber, or add a community webhook plugin.
- **JS SDK** (`@medusajs/js-sdk`) wraps Admin + Store APIs with auth handling.
- **Payment/shipping/notification providers** plug in as modules (e.g. Stripe payment provider, SendGrid/Resend notification provider). **Medusa is NOT a Merchant of Record** — you own tax/VAT (pair with a tax module/provider or a MoR upstream).
- **MCP server** for agentic tools (Claude/Cursor) to read and act on store data.

## Data model

Key objects (v2). JSON shapes constructed from documented fields — verify against live API.

**Product** <!-- Constructed from docs — verify against live API -->
```json
{
  "id": "prod_01H...",
  "title": "Medusa Sweatpants",
  "handle": "sweatpants",
  "status": "published",
  "variants": [
    { "id": "variant_01H...", "title": "M", "sku": "SWT-M", "inventory_quantity": 42 }
  ],
  "options": [ { "id": "opt_01H...", "title": "Size", "values": ["S","M","L"] } ],
  "collection_id": "pcol_01H...",
  "created_at": "2026-06-28T10:00:00.000Z"
}
```

**Order** <!-- Constructed from docs — verify against live API -->
```json
{
  "id": "order_01H...",
  "display_id": 1042,
  "status": "pending",
  "email": "buyer@example.com",
  "currency_code": "usd",
  "region_id": "reg_01H...",
  "sales_channel_id": "sc_01H...",
  "items": [ { "id": "item_01H...", "variant_id": "variant_01H...", "quantity": 1, "unit_price": 4500 } ],
  "total": 4500,
  "created_at": "2026-06-28T10:05:00.000Z"
}
```
> Money is stored in the smallest currency unit (e.g. `4500` = $45.00 USD).

**Event payload delivered to a subscriber** (thin — id only):
```json
{ "id": "order_01H...", "metadata": {} }
```
You receive `event.data` (typically just `{ id }`) and must load the full object via the service/API.

## Quick-start recipes

### Recipe 1 — React to a new order and notify an external system (the "webhook" pattern)
Medusa has no outbound-webhook UI; you write a subscriber.

`src/subscribers/order-placed.ts`:
```ts
import { SubscriberArgs, type SubscriberConfig } from "@medusajs/framework"

export default async function orderPlacedHandler({
  event: { data },
  container,
}: SubscriberArgs<{ id: string }>) {
  const orderService = container.resolve("order")
  const order = await orderService.retrieveOrder(data.id, {
    relations: ["items", "summary"],
  })

  await fetch("https://hooks.example-crm.com/medusa", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id: order.id, email: order.email, total: order.total }),
  })
}

export const config: SubscriberConfig = { event: "order.placed" }
```
Gotchas: runs async (won't block/roll back the order); add your own retry/logging; use the **Redis Event Module** in production so events survive restarts.

### Recipe 2 — Authenticate and list orders from a script (Admin API)
```bash
# Option A: admin API key in Basic auth (base64 optional in v2)
curl -s "https://your-app.medusajs.app/admin/orders?limit=100&offset=0&order=-created_at" \
  -H "Authorization: Basic sk_test_xxxx..."

# Option B: get a JWT, then Bearer it
TOKEN=$(curl -s -X POST https://your-app.medusajs.app/auth/user/emailpass \
  -H 'Content-Type: application/json' \
  --data '{"email":"admin@example.com","password":"REDACTED"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])')

curl -s "https://your-app.medusajs.app/admin/orders?limit=100&offset=0" \
  -H "Authorization: Bearer $TOKEN"
```
```python
import requests
base = "https://your-app.medusajs.app"
tok = requests.post(f"{base}/auth/user/emailpass",
                    json={"email": "admin@example.com", "password": "REDACTED"}).json()["token"]
h = {"Authorization": f"Bearer {tok}"}
offset, out = 0, []
while True:
    r = requests.get(f"{base}/admin/orders", params={"limit": 100, "offset": offset}, headers=h).json()
    out += r["orders"]
    offset += r["limit"]
    if offset >= r["count"]:
        break
```

### Recipe 3 — Fetch products from a storefront (Store API + publishable key)
```bash
curl -s "https://your-app.medusajs.app/store/products?limit=20" \
  -H "x-publishable-api-key: pk_xxxx..."
```
Gotcha: without the `x-publishable-api-key` header the Store API returns errors/empty — the key scopes which sales channel's products you see.

## Integration patterns

- **CRM/warehouse sync:** prefer event-driven (`order.placed`, `order.updated`, `customer.created` → subscriber → upsert into CRM by `display_id`/`email`) for freshness; back it with a nightly Admin-API reconciliation crawl (`limit`/`offset`, `order=-created_at`) to catch anything a dropped event missed.
- **Outbound delivery reliability:** because Medusa gives you no retries/signing/logging, treat the subscriber as a producer into your own durable queue (or a gateway like Hookdeck/Svix) rather than calling the partner inline; sign your own payloads.
- **Auth choice by caller:** server scripts → admin **API key (Basic)**; user/session flows → **JWT** from `/auth/{actor}/{provider}` then Bearer (or `/auth/session` for a cookie); storefront → **publishable key** header.
- **Production infra:** swap the default Local Event Module + in-memory cache for **Redis** modules; run a separate **worker** process (Scale tier / self-host) so long subscribers/workflows don't block web requests.
