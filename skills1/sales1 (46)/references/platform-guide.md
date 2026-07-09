# Bagisto Platform Guide

<!-- Source: https://bagisto.com, https://github.com/bagisto/bagisto, https://devdocs.bagisto.com, https://api-docs.bagisto.com (research 2026-06) -->

*Best-effort from research (2026-06). Bagisto ships frequently (v2.4.x in mid-2026) — re-verify pricing, plan gates, and API headers/endpoints against live docs.*

## What Bagisto is

Bagisto is a **free, open-source (MIT) eCommerce framework built on Laravel (PHP) and Vue.js**. It's a developer/maker platform you build on and self-host — not a turnkey hosted SaaS store and not a drop-in checkout cart. You own the code and data, run your own infra (or pay for Bagisto Cloud), and pay **no per-sale/GMV platform fee**.

It targets developers, GTM/commerce engineers, agencies, and SMBs who want full code-level control on a PHP/Laravel stack. Bagisto is maintained by **Webkul** and is part of an ecosystem (Krayin CRM, UnoPim PIM, Aureus ERP, QloApps).

**Pick Bagisto when:** you want a fee-free, fully customizable store backend on the Laravel/PHP stack and are comfortable running the infra. **Pick a hosted SaaS** (Shopify/BigCommerce) **or a drop-in cart** (ThriveCart/SamCart) if you don't want to run servers. **Compare** with Medusa (Node/TypeScript), Saleor (Python/Django, GraphQL-first), Vendure (Node/TypeScript), and Sylius (Symfony/PHP).

## Modules & capabilities — what's API vs event vs UI

| Module | What it does | Programmatic access |
|---|---|---|
| Catalog (products, variants, attributes, categories) | Configurable/simple/grouped/bundle/virtual/downloadable products, attribute families, category tree | **REST + GraphQL** (Shop read, Admin write) |
| Orders, invoices, shipments | Order lifecycle, fulfillment, refunds | **REST + GraphQL** (Admin); read in Shop API for the customer |
| Carts & checkout | Guest + customer carts, multi-step checkout (address → shipping → payment → place order) | **REST + GraphQL** (Shop) with **cart tokens** for guests |
| Customers & addresses | Registration, login, profile, address book | **REST + GraphQL** (Shop) |
| Reviews, wishlist, compare | Customer-generated content | **REST + GraphQL** (Shop) |
| Inventory (multi-source) | Stock per source/warehouse | **REST + GraphQL** (Admin) |
| Promotions (catalog & cart rules) | Discounts, coupons | **REST + GraphQL** (Admin); UI rule builder |
| Channels / locales / currencies | Multi-store, multi-language, multi-currency | Header scoping (`X-Channel`/`X-Locale`/`X-Currency`) + Admin config |
| CMS pages, theme | Storefront content & design | Admin UI (theme is code/Blade) |
| Multi-Vendor Marketplace | Multiple sellers, seller dashboards, commissions | **Paid/add-on extension** (Webkul) — UI + some API |
| POS (Point of Sale) | In-store selling synced to catalog | **Paid/add-on extension** |
| B2B Commerce | Bulk ordering, quotes, customer groups | Extension / config |
| Magic AI | AI content/image generation in admin | Admin UI feature |
| Headless / mobile | Drive any front-end (Next.js, Flutter app) off the API | **REST + GraphQL** |

**Rule of thumb:** core catalog/cart/checkout/customer/order data is API-accessible (REST and GraphQL). The site **theme/CMS and promotion rule-builders are UI-configured**. Marketplace, POS, and many advanced features are **paid Webkul extensions**.

## API surface (summary — full detail in `bagisto-api-reference.md`)

Bagisto exposes **two API flavors over the same engine**, each split into a public **Shop API** and a protected **Admin API**:

- **REST API** — install `composer require bagisto/rest-api`; base `https://{domain}/api/shop/...` and `/api/admin/...`. Auth: **`X-STOREFRONT-KEY`** (`pk_storefront_...`) on Shop calls + **Laravel Sanctum bearer token** on customer/admin routes; **guest cart token** via `POST /api/shop/cart-tokens`. Interactive Swagger/OpenAPI docs at `/api/shop/documentation` and `/api/admin/documentation`. Pagination via `?page=&per_page=` (max 50) with `X-Total-Count`/`X-Page`/`X-Per-Page`/`X-Total-Pages` headers.
- **GraphQL API** — endpoint `https://{domain}/api/graphql`, playground at `/api/graphiql`. Same Shop/Admin split. Headers: `X-STOREFRONT-KEY`, `Authorization: Bearer {token}`, optional `X-LOCALE`/`X-CURRENCY`/`X-CHANNEL`. Auth mutations: `createCartToken` (guest), `createCustomerLogin` (returns JWT-style token), `createVerifyToken`. Cursor pagination (`first`/`after` + `pageInfo`).
- **Legacy headless package** — the older standalone `bagisto/graphql-api` (Mobikul) uses a `/graphql` endpoint + `/graphiql` playground with **JWT** and an `x-app-secret-key` header (configured via `JWT_TTL`, `MOBIKUL_API_KEY`). Don't mix its headers with the unified API.

**Webhooks:** core has **no native outbound webhooks**. Use Laravel **events/listeners** (e.g. `checkout.order.save.after`), a polling job, or a community webhook package.

## Pricing & plan posture

- **Bagisto engine: free, open-source, MIT.** No license cost, no per-sale fee. You pay only for your own hosting + any paid extensions.
- **Paid extensions (Webkul Bagisto store):** Multi-Vendor Marketplace, POS, B2B, mobile apps, and many connectors are **separately priced one-time/recurring add-ons**.
- **Bagisto Cloud (managed hosting):** tiers **Starter Pack** and **Pro Pack** — both include core commerce; Pro adds a higher uptime SLA (≈99.9% vs 99.5%) and advanced support; migration/technical assistance are paid add-ons. **Public per-month prices aren't listed — contact sales / verify live.**

⚠️ Treat all pricing as best-effort and re-verify — Webkul changes extension and Cloud pricing periodically.

## Data model — JSON shapes

**Product (Shop API, simplified):**
```json
{
  "id": 1,
  "sku": "tshirt-blue-l",
  "type": "configurable",
  "name": "Blue T-Shirt",
  "url_key": "blue-t-shirt",
  "price": "29.9900",
  "formatted_price": "$29.99",
  "in_stock": true,
  "images": [{ "id": 10, "url": "https://store.test/storage/product/1/img.png" }],
  "variants": [{ "id": 2, "sku": "tshirt-blue-l", "price": "29.9900" }]
}
```

**Cart token (guest checkout):**
```json
{ "data": { "cart_token": "cT_5b3a1c9f0e..." } }
```

**Customer login response (GraphQL `createCustomerLogin`):**
```json
{
  "data": {
    "createCustomerLogin": {
      "token": "eyJ0eXAiOiJKV1Qi...",
      "success": true,
      "message": "Logged in successfully.",
      "customer": { "id": 5, "email": "buyer@example.com", "firstName": "Ada", "lastName": "Lovelace" }
    }
  }
}
```

**Order (Admin API, simplified):**
```json
{
  "id": 1001,
  "increment_id": "1000001",
  "status": "processing",
  "grand_total": "59.9800",
  "customer_email": "buyer@example.com",
  "items": [{ "id": 1, "sku": "tshirt-blue-l", "qty_ordered": 2, "total": "59.9800" }],
  "created_at": "2026-06-24T10:00:00.000000Z"
}
```

Money is stored as a **decimal string in the store currency** (e.g. `"29.9900"`), not integer cents — format with the `formatted_*` fields or your own locale logic.

## Quick-start recipes

### Recipe 1 — List products (Shop REST, guest, cURL)
```bash
curl "https://your-domain/api/shop/products?page=1&per_page=10" \
  -H "X-STOREFRONT-KEY: pk_storefront_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Accept: application/json"
```
Paginate by incrementing `page` until `X-Page` == `X-Total-Pages`.

### Recipe 2 — Pull all orders into a warehouse (Admin REST, Python)
```python
import requests

BASE = "https://your-domain/api/admin"
TOKEN = "1|your-sanctum-admin-token"  # from the admin login endpoint
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

page, rows = 1, []
while True:
    r = requests.get(f"{BASE}/orders", headers=headers,
                     params={"page": page, "per_page": 50})
    r.raise_for_status()
    body = r.json()
    rows.extend(body.get("data", []))
    total_pages = int(r.headers.get("X-Total-Pages", 1))
    if page >= total_pages:
        break
    page += 1

print(f"pulled {len(rows)} orders")
# upsert rows into BigQuery/Snowflake here
```

### Recipe 3 — Notify a CRM on every new order (Laravel event listener)
Bagisto has no webhook UI — react to the order event in code:
```php
// app/Providers/EventServiceProvider.php  (or a custom package)
protected $listen = [
    'checkout.order.save.after' => [
        \App\Listeners\NotifyCrmOnOrder::class,
    ],
];
```
```php
// app/Listeners/NotifyCrmOnOrder.php
namespace App\Listeners;

use Illuminate\Support\Facades\Http;

class NotifyCrmOnOrder
{
    public function handle($order): void
    {
        Http::post('https://your-crm.example.com/hooks/order', [
            'increment_id' => $order->increment_id,
            'email'        => $order->customer_email,
            'grand_total'  => $order->grand_total,
        ]);
    }
}
```
Queue the listener (`implements ShouldQueue`) and run a worker so the outbound call never blocks checkout.

### Recipe 4 — Customer login + product query (GraphQL Shop)
```graphql
mutation {
  createCustomerLogin(input: { email: "buyer@example.com", password: "secret" }) {
    token
    success
    customer { id email firstName lastName }
  }
}
```
Then send the returned token as `Authorization: Bearer {token}` and query:
```graphql
query {
  products(first: 10) {
    edges { node { id name price } }
    pageInfo { hasNextPage endCursor }
  }
}
```

## Where Bagisto fits vs alternatives

- **vs Shopify/BigCommerce (hosted SaaS):** Bagisto is free + self-hosted with full code control, but you run the stack and there's no app-store ecosystem at the same scale.
- **vs Medusa / Vendure (Node/TypeScript):** same self-host/open-source idea on a different stack — choose by team language (PHP/Laravel ↔ Node/TS).
- **vs Saleor (Python/Django, GraphQL-first with native webhooks):** Saleor ships outbound webhooks; Bagisto relies on Laravel events. Pick by stack + webhook needs.
- **vs Sylius (Symfony/PHP):** both PHP — Sylius is Symfony + API Platform, Bagisto is Laravel + Vue; choose by framework preference.
- **vs WooCommerce (WordPress plugin):** Woo lives inside WordPress; Bagisto is a standalone Laravel app — pick Bagisto for a cleaner app architecture, Woo for the WordPress ecosystem.
