# Shopware Platform Reference

## Overview

Shopware 6 is an open-source **PHP/Symfony** commerce platform (Vue.js Administration, Twig or headless
storefront) aimed at mid-market and B2B merchants, with a strong European footprint. The **Community
Edition is free (MIT) and self-hosted**; paid **Rise / Evolve / Beyond** tiers and a managed
**Shopware Cloud** add automation (Flow Builder), B2B Components, subscriptions, and support. Its
differentiator versus SaaS (Shopify/BigCommerce) is deep customizability and API-first/composable
architecture; versus lighter OSS (EverShop/Medusa) it is heavier — you run PHP/Symfony + MySQL +
OpenSearch + a message queue. Two APIs matter: the **Admin API** (`/api/*`) for back-office data and
the **Store API** (`/store-api/*`) for the headless buyer flow.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Products | Products, variants, properties, prices, categories | Admin API CRUD + `POST /api/search/product`; webhook `product.written`/`product.deleted` |
| Orders | Order lifecycle, transactions, deliveries, documents | Admin API; webhook `checkout.order.placed`, `order.written`, `state_enter.order_transaction.state.*` |
| Customers | Accounts, addresses, customer groups (incl. B2B) | Admin API; webhook `customer.written`, `checkout.customer.register`/`login` |
| Sales channels | Storefronts/channels, domains, currencies, languages | Admin API; **Store API access key per channel** |
| Cart & checkout | Buyer-facing cart, line items, promotions, checkout | **Store API** `/store-api/*` (`sw-access-key` + `sw-context-token`) |
| Promotions / discounts | Rule-based promotions, discounts | Admin API CRUD |
| Flow Builder | Event → action automation (email, tag, **HTTP/webhook call**) | Rise+ tier; can POST to an endpoint as an action |
| Apps & plugins | Extend admin/storefront; register webhooks | App system (manifest) + plugin system (self-host) |
| Sync API | Bulk upsert/delete across entities in one call | `POST /api/_action/sync` |
| Media / documents | Assets, invoices/delivery notes | Admin API; webhook `media.written`, `document.written` |

**Administration-only (no first-class API):** theme/storefront layout, most plugin configuration
screens, and Flow Builder rule authoring. Automate data and events, not presentation.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — verify at shopware.com/pricing.*

- **Community Edition: free (MIT), self-hosted.** You cover hosting, dev, PCI scope, and updates.
- **Fair Usage Policy (from March 2026):** CE is free only for merchants **under ~€1M GMV**; **above
  ~€1M GMV you must move to a paid plan.** This is the key gate for scaling stores.
- **Paid tiers (self-hosted or cloud), best-effort:**
  - **Rise** — from ~**€600/mo**: Flow Builder, AI Copilot, Social Shopping, business support.
  - **Evolve** — from ~**€2,400/mo**: B2B Components, Advanced Search, Flow Builder Professional.
  - **Beyond** — from ~**€6,500/mo** (custom): Digital Sales Rooms, Multi-Inventory, Subscriptions, 24/7.
  - Evolve/Beyond are negotiated by GMV and requirements.
- **Rate limits:** **Admin API = 300 requests/minute.** Store API limits vary by server config.
- **Not a Merchant of Record:** the merchant owns VAT/GST/sales tax.

## Integrations

- **Direction:** Admin API is **bidirectional** (read + write) over all back-office entities; webhooks
  are **outbound** (Shopware → your endpoint) via the App system; Store API is buyer-facing read/write
  for cart/checkout.
- **CRM/warehouse:** no native CRM; sync via Admin API + app webhooks, or Flow Builder HTTP actions.
- **Extension surface:** the Shopware Store (apps/plugins), the App system (cloud-safe, manifest-based),
  and the plugin system (self-host, deeper). Zapier/Make integrate via community apps, not first-party.
- **Headless:** Store API + **Composable Frontends** (Vue/Nuxt) or any framework; the Admin API feeds
  PIM/OMS-style back-office integrations.

## Data model

IDs are **32-character hex UUIDs** (no dashes). Reads use a **Criteria** query model. Many fields are
**translatable** and resolve by the request's language/sales-channel context. Prices are objects
(net/gross per currency), not bare strings.

**Order (trimmed, from `POST /api/search/order`):**
```json
{
  "data": [
    {
      "id": "b7f2c9e1a4d8460fbc3e5a1029d7e6f4",
      "orderNumber": "10001",
      "amountTotal": 29.99,
      "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
      "orderCustomer": { "email": "ada@example.com", "firstName": "Ada" },
      "stateMachineState": { "technicalName": "open" },
      "lineItems": [ { "label": "Pro License", "quantity": 1, "totalPrice": 29.99 } ],
      "createdAt": "2026-07-04T14:22:07.000+00:00"
    }
  ],
  "total": 1
}
```
<!-- Constructed from documented field lists — verify against live API -->

**Product create body (`POST /api/product`):**
```json
{
  "name": "Pro License",
  "productNumber": "SW-PRO-1",
  "stock": 100,
  "taxId": "5f2e9a1b8c7d4e3f9a0b1c2d3e4f5a6b",
  "price": [
    { "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca", "gross": 29.99, "net": 25.20, "linked": true }
  ]
}
```
<!-- Constructed from documented field lists — verify against live API -->

## Quick-start recipes

### Recipe 1 — OAuth token + entity search (Admin API)
Trigger: read back-office data from a script. Steps: create an Integration
(Settings → System → Integrations), get a token, then search.

```bash
# 1) Get an OAuth token (client_credentials)
curl -s "https://shop.example.com/api/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"ACCESS_KEY_ID","client_secret":"SECRET_ACCESS_KEY"}'
# -> { "token_type":"Bearer", "expires_in":3600, "access_token":"eyJ0..." }

# 2) Search orders (Criteria in the body; pagination via limit/page)
curl -s -X POST "https://shop.example.com/api/search/order" \
  -H "Authorization: Bearer eyJ0..." -H "Content-Type: application/json" \
  -d '{"limit":50,"page":1,"total-count-mode":1,
       "filter":[{"type":"equals","field":"stateMachineState.technicalName","value":"open"}],
       "sort":[{"field":"createdAt","order":"DESC"}],
       "associations":{"lineItems":{}}}'
```
```python
import requests
BASE = "https://shop.example.com"

def token():
    r = requests.post(f"{BASE}/api/oauth/token", json={
        "grant_type": "client_credentials",
        "client_id": "ACCESS_KEY_ID", "client_secret": "SECRET_ACCESS_KEY"}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def search_orders(tok, page=1):
    r = requests.post(f"{BASE}/api/search/order",
        headers={"Authorization": f"Bearer {tok}"},
        json={"limit": 50, "page": page, "total-count-mode": 1,
              "sort": [{"field": "createdAt", "order": "DESC"}]}, timeout=30)
    r.raise_for_status()
    return r.json()  # {"data": [...], "total": N}
```
Gotcha: if the token call 401s, you're likely using keys from a plugin install — create a dedicated
Integration instead. Refresh the Bearer before `expires_in` (~3600s).

### Recipe 2 — Bulk upsert with the Sync API
Trigger: import/update many entities without hitting 300 req/min. Steps: one `sync` call with batched operations.

```python
import requests
BASE, TOK = "https://shop.example.com", "eyJ0..."

def sync_upsert_products(rows):                 # rows: list of product dicts (with id or productNumber)
    payload = [{
        "action": "upsert",
        "entity": "product",
        "payload": rows                          # many entities in ONE request
    }]
    r = requests.post(f"{BASE}/api/_action/sync",
        headers={"Authorization": f"Bearer {TOK}", "Content-Type": "application/json"},
        json=payload, timeout=120)
    r.raise_for_status()
    return r.json()
# Batch a few hundred per call; back off on 429 (300 req/min Admin API cap).
```

### Recipe 3 — App webhook with signature verification
Trigger: react to placed orders. Steps: declare the webhook in the app manifest, verify the signature.

```xml
<!-- manifest.xml (excerpt) -->
<webhooks>
    <webhook name="order-placed"
             url="https://my-app.example.com/webhook/order-placed"
             event="checkout.order.placed"
             onlyLiveVersion="true"/>   <!-- skip order drafts -->
</webhooks>
```
```python
import base64, hashlib, hmac, requests
from flask import Flask, request, abort

app = Flask(__name__)
APP_SECRET = b"the_secret_assigned_at_registration"

@app.post("/webhook/order-placed")
def order_placed():
    body = request.get_data()                    # RAW bytes — hash before parsing
    sig = request.headers.get("shopware-shop-signature", "")
    expected = hmac.new(APP_SECRET, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        abort(401)
    data = request.get_json()
    order_id = data["data"]["payload"][0]["id"]  # entity id from the event payload
    # re-fetch via Admin API before provisioning; dedupe on order_id
    return "", 200
```
Gotcha: the signature is **HMAC-SHA256 of the raw body** keyed by the per-shop app secret; compare
constant-time. Cloud stores can only run App-system webhooks, not self-host plugins.

## Integration patterns

- **CRM/warehouse sync:** app webhook (`checkout.order.placed`, `order.written`) for low latency + a
  batched **Sync API** or paginated `/api/search/{entity}` reconciliation pull as a backstop. Verify
  `shopware-shop-signature`, re-fetch the entity, dedupe on UUID id. Stay under 300 req/min.
- **Webhook listener:** declare `<webhooks>` in the manifest (or use Flow Builder's HTTP action on
  Rise+); return fast `2xx`; use `onlyLiveVersion` to skip drafts; verify HMAC before trusting.
- **Batch/ETL:** query with Criteria (`filter`/`sort`/`associations`/`aggregations`), page with
  `limit`+`page`, and write with the Sync API rather than per-row calls. Enable OpenSearch for large catalogs.
- **Headless storefront:** buyer flow via **Store API** (`sw-access-key` + `sw-context-token` per
  shopper) — cart, line items, checkout; keep the Admin API server-side only (never expose OAuth
  secrets or public admin tokens in the browser — proxy instead).
