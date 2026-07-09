# BigCommerce Platform Reference

## Overview

BigCommerce is an open-SaaS commerce platform (hosted backend + APIs) for makers, growing DTC brands, and B2B sellers. Like Shopify it owns the storefront, catalog, orders, customers, and checkout — but it differentiates on **zero platform transaction fees** on embedded payment providers, strong **B2B** features, and an **API-first / headless ("composable")** posture. It is **not** a Merchant of Record — you remain seller of record and own tax compliance.

## Capabilities & automation surface

| Capability | What it does | Automation |
|---|---|---|
| Catalog (products, variants, SKUs, categories, brands) | Product data, options/modifiers, inventory | **API-accessible** (`/v3/catalog/*`); inventory + product webhooks |
| Orders | Order records, transactions, refunds, shipments | **API-accessible** — classic **Orders API is v2** (`/v2/orders`); v3 Orders also exists for newer use; order webhooks |
| Customers | Customer accounts, addresses, customer groups | **API-accessible** (`/v3/customers`, v2 also exists); customer webhooks |
| Carts & Checkouts | Server-side cart + checkout objects for headless | **API-accessible** (`/v3/carts`, `/v3/checkouts`); cart + abandoned-cart webhooks |
| Storefront (themes, pages) | Stencil themes, control-panel pages | Mostly **UI-only**; headless via Storefront APIs |
| Checkout page | Hosted/optimized one-page checkout, wallets, BNPL | **UI-only** to configure; customizable via Checkout SDK / headless |
| Price Lists | Customer-group / channel-specific pricing (B2B) | **API-accessible** (`/v3/pricelists`); price-list webhooks |
| Multi-Storefront / Channels | Sell across multiple storefronts + marketplaces (Google, Meta, Amazon, eBay) | **API-accessible** (Channels API) + UI |
| Webhooks | Event notifications (thin payloads) | **Webhook-accessible** (`/v3/hooks`) |
| Metafields | Custom key/value data on objects | **API-accessible** (per-object `/metafields`); metafield webhooks |

**API interfaces:**
- **REST Management API** — store admin operations. Resources split across **v2** (Orders, some Customers) and **v3** (Catalog, Customers, Carts, Checkouts, Webhooks, Price Lists). Base: `https://api.bigcommerce.com/stores/{store_hash}/v3/` (or `/v2/`).
- **GraphQL Storefront API** — client-side, public token, for headless front-ends (catalog/cart/checkout).
- **GraphQL Admin API** — newer typed admin surface (overlaps REST; growing).
- **GraphQL Account API** — account-level, across all stores in a parent account.
- **Webhooks** — event notifications; **thin payloads** (id only), **no HMAC**.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against the live pricing page; BigCommerce shows GMV-threshold plans that auto-upgrade.*

Two naming schemes appear depending on where you look:

- **Legacy / API-tier names:** Standard, Plus, Pro, Enterprise.
- **Current pricing page names:** Core (~$39/mo, up to ~$30K TTM GMV), Growth (~$105/mo, up to ~$100K GMV), Scale (~$399/mo, "Most Popular", 0.9% overage above cap), Performance/Enterprise (custom, from ~$1,499/mo).

Plan gates worth knowing:
- **Customer segmentation / customer groups** and **abandoned-cart recovery** are gated above the entry tier.
- **Price Lists**, advanced product filtering, and **API support / advanced promotions** land on higher tiers.
- **Rate limits scale by plan** — see the API reference: ~**150 requests / 30s** on Standard & Plus, ~**450 / 30s** on Pro, custom on Enterprise.
- **Transaction fees:** **$0** on orders through embedded payment providers on every plan. Using an **open/third-party** gateway adds a per-GMV fee (~2.0% Core, ~1.0% Growth, ~0.6% Scale, 0% on contracted Enterprise).
- **No published platform cap on products/staff** at most tiers, but GMV thresholds trigger auto-upgrade.

## Integrations

- **Direction:** the Management API is bidirectional (read + write store data); webhooks are read-only notifications (outbound from BigCommerce).
- **Native:** 600+ app marketplace integrations (ERP, CRM, PIM, WMS), multi-channel selling (Google, Meta, TikTok, Amazon, Walmart, eBay), Feedonomics product feeds.
- **iPaaS:** Zapier, Make, and similar can trigger on store events and act via the Management API; many middleware tools (api2cart, Celigo) wrap it.
- **Payments:** 20+ embedded providers (fee-free) plus 130+ additional payment solutions.

## Data model

Common objects (v3 unless noted). Shapes below are representative — verify against the live API.

**Product** (`GET /v3/catalog/products/{id}`):
<!-- Constructed from docs — verify against live API -->
```json
{
  "data": {
    "id": 111,
    "name": "Sample Product",
    "type": "physical",
    "sku": "SKU-111",
    "price": 49.0,
    "weight": 1.0,
    "categories": [23, 24],
    "is_visible": true,
    "inventory_level": 100,
    "variants": [{ "id": 201, "sku": "SKU-111-S", "price": 49.0, "inventory_level": 40 }]
  },
  "meta": {}
}
```

**Order** (`GET /v2/orders/{id}` — note v2):
<!-- Constructed from docs — verify against live API -->
```json
{
  "id": 250,
  "status_id": 11,
  "status": "Awaiting Fulfillment",
  "total_inc_tax": "53.00",
  "currency_code": "USD",
  "customer_id": 12,
  "date_created": "Tue, 25 Jun 2026 18:00:00 +0000",
  "products": { "url": "https://api.bigcommerce.com/stores/{store_hash}/v2/orders/250/products", "resource": "/orders/250/products" }
}
```
(In v2, sub-resources like products/shipping addresses are returned as `{url, resource}` links you must follow with separate calls.)

**Webhook callback payload** (what your endpoint receives — thin, no HMAC):
```json
{
  "scope": "store/order/created",
  "store_id": "1025646",
  "data": { "type": "order", "id": 250 },
  "hash": "dd70c0976e06b67aaf671e73f49dcb79230ebf9d",
  "created_at": 1561479335,
  "producer": "stores/{store_hash}"
}
```

## Quick-start recipes

### Recipe 1 — Listen for a new order and pull the full record into a CRM
BigCommerce sends only the order id, so subscribe, then fetch.

Create the webhook (cURL):
```bash
curl -X POST "https://api.bigcommerce.com/stores/{store_hash}/v3/hooks" \
  -H "X-Auth-Token: {access_token}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "scope": "store/order/created",
    "destination": "https://example.com/bc-webhooks",
    "is_active": true,
    "headers": { "X-Custom-Secret": "super-secret-password" }
  }'
```

Handler (Python / Flask):
```python
import os, requests
from flask import Flask, request, abort

app = Flask(__name__)
STORE = os.environ["STORE_HASH"]
TOKEN = os.environ["BC_TOKEN"]
SECRET = os.environ["BC_WEBHOOK_SECRET"]
BASE = f"https://api.bigcommerce.com/stores/{STORE}"
HEADERS = {"X-Auth-Token": TOKEN, "Accept": "application/json"}

@app.post("/bc-webhooks")
def hook():
    if request.headers.get("X-Custom-Secret") != SECRET:   # BigCommerce has NO HMAC — use your own header
        abort(401)
    body = request.get_json(force=True)
    order_id = body["data"]["id"]                            # thin payload: id only
    # Orders live on v2:
    order = requests.get(f"{BASE}/v2/orders/{order_id}", headers=HEADERS).json()
    upsert_into_crm(order)                                   # de-dupe on order_id
    return ("", 200)                                         # respond 2XX fast or the hook deactivates
```

### Recipe 2 — Backfill the full catalog without tripping the rate limit
```python
import time, requests
BASE = f"https://api.bigcommerce.com/stores/{STORE}/v3/catalog/products"
page, out = 1, []
while True:
    r = requests.get(BASE, headers=HEADERS, params={"limit": 250, "page": page})
    if r.status_code == 429:
        time.sleep(int(r.headers.get("X-Rate-Limit-Time-Reset-Ms", "30000")) / 1000)
        continue
    j = r.json()
    out.extend(j["data"])
    pag = j["meta"]["pagination"]
    if page >= pag["total_pages"]:
        break
    page += 1
    if int(r.headers.get("X-Rate-Limit-Requests-Left", "999")) < 5:  # proactive throttle
        time.sleep(int(r.headers.get("X-Rate-Limit-Time-Reset-Ms", "30000")) / 1000)
```

### Recipe 3 — Create a product (write path)
```bash
curl -X POST "https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products" \
  -H "X-Auth-Token: {access_token}" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{ "name": "New Product", "type": "physical", "weight": 1, "price": 29.0 }'
```
(No trailing slash on the path — a stray `/` returns 403.)

## Integration patterns

- **Webhook → fetch → upsert.** Because payloads are thin, every event becomes (at least) one extra API read. Account for that doubling in your rate budget; de-dupe on `data.id` + `created_at` because redelivery can occur and ordering isn't guaranteed.
- **Reconcile, don't trust delivery.** There are no delivery logs on BigCommerce's side. Persist a local log of received events and run a periodic reconcile (poll `/v2/orders?min_date_modified=...`) to catch anything the webhook dropped.
- **Keep subscriptions alive.** A subscription deactivates after repeated 4XX/5XX (and inactivity). Return 2XX within a couple of seconds (queue the heavy work), and periodically `GET /v3/hooks` to confirm `is_active`.
- **Secure callbacks yourself.** No HMAC: set a secret custom header at creation and verify it; require HTTPS on port 443; optionally IP-allowlist.
- **Mind the version split.** Prefer v3 for catalog/customers/carts; Orders classic is v2 and uses link-style sub-resources. Newer GraphQL Admin API can replace some REST calls but coverage is still growing.
