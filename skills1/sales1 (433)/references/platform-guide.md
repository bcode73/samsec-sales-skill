# Printify Platform Reference

## Overview

Printify is a print-on-demand (POD) fulfillment **broker**: instead of owning factories (Printful's model), it routes your orders to a network of ~141 third-party print providers across 209 countries/territories. That buys the largest catalog in the category (1,300+ products) and the lowest base costs — and trades away consistency: quality, production speed, and shipping vary by which provider you pick per product. Free to use; Printify earns on the fulfillment margin.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Catalog (blueprints/providers/variants) | 1,300+ blank products ("blueprints"), each fulfillable by one or more print providers with their own variants, costs, and locations | **API-accessible** (`/v1/catalog/*`, 100 req/min) |
| Product designer / mockup generator | Position artwork on placeholders, auto-generate mockups | **API-accessible** (create product with `print_areas` → mockups generated) + UI editor |
| Products | Your designed products per shop | **API-accessible** (CRUD + publish flow) |
| Publishing to sales channel | Push product to Shopify/Etsy/etc. | **API-accessible** (`/publish.json`, 200 req/30 min) — for custom storefronts you implement the publish→`publishing_succeeded` handshake yourself |
| Orders | Submit, track, cancel, send to production; shipping cost calculation | **API-accessible** + **webhook-accessible** (`order:*` events) |
| Printify Express / economy shipping | Faster (2–3 day) delivery on eligible US products; cheaper economy tier | **API-accessible** (`is_printify_express`, `is_economy_shipping` flags, `/orders/express.json`) |
| Uploads | Artwork library (URL or base64 upload) | **API-accessible** (`/v1/uploads/*`) |
| Webhooks | 10 event types, HMAC-SHA256 signed (`X-Pfy-Signature`) | **API-accessible** (register/modify/delete/simulate per shop) |
| Profit calculator, analytics | Margin estimation, sales dashboards | **UI-only** |
| Printify Payments / billing | Card/balance charged per order | **UI-only** (fix billing in dashboard) |

**MCP server (community)**: `TSavo/printify-mcp` (github.com/TSavo/printify-mcp) — shop/product/catalog/upload tools plus AI image generation via Replicate, works with Claude Desktop over stdio. Useful as a conversational interface; for production pipelines use the REST API directly.

**iPaaS**: Zapier integration exists (order triggers); the REST API + webhooks are the primary automation surface.

## Pricing, limits & plan gates

*Best-effort (2026-07) — verify against printify.com/pricing.*

- **Free** — $0/mo, unlimited products, up to 5 stores. Full API access.
- **Premium** — ~$29/mo (~$24.99 annual): up to 20% discount on product base costs, up to 10 stores. Same API.
- **Enterprise** — custom: deeper discounts, dedicated support, unlimited stores.

Premium break-even: if 20% of your monthly base-cost spend exceeds ~$29, upgrade. (~$145/mo in base costs.)

API limits (per **account**, not per token): 600 req/min global, 100 req/min catalog, 200 publishes/30 min, error responses <5% of traffic. Personal Access Tokens expire after **1 year**; OAuth access tokens after **6 hours**.

## Integrations

Store connectors (bidirectional: products push out, orders flow in): **Shopify, Etsy, TikTok Shop, Amazon, eBay, Walmart, WooCommerce, Wix, Squarespace, BigCommerce, PrestaShop** — plus the **API channel** for custom/headless storefronts. Printful supports more connectors overall (~21 vs ~11), so check yours is on the list before committing.

Data flow: catalog/product data is read from Printify; orders are written to Printify (auto from connected stores, or `POST /orders.json` headless); fulfillment status flows back via webhooks or polling.

## Data model

Hierarchy: **Blueprint** (blank product, e.g. Unisex Heavy Cotton Tee) → **Print provider** (a factory that fulfills that blueprint; each has its own costs, locations, variants) → **Variant** (color/size combo with a specific cost) → **Product** (your design applied to variants in a shop) → **Order** (line items referencing product+variant, or blueprint+provider+variant for on-the-fly products).

```json
// Shop
{ "id": 5432, "title": "My new store", "sales_channel": "My Sales Channel" }

// Blueprint (catalog)
{ "id": 384, "title": "Unisex Heavy Cotton Tee", "brand": "Gildan", "model": "5000" }

// Product variant reference inside a product (price in cents)
{ "id": 45740, "price": 400, "is_enabled": true }

// Print area (design placement; x/y/scale are 0–1 relative coordinates)
{
  "variant_ids": [45740, 45742],
  "placeholders": [
    { "position": "front",
      "images": [{ "id": "5d15ca551163cde90d7b2203", "x": 0.5, "y": 0.5, "scale": 1, "angle": 0 }] }
  ]
}

// Webhook event envelope
{
  "id": "653b6be8-2ff7-4ab5-a7a6-6889a8b3bbf5",
  "type": "order:shipment:created",
  "created_at": "2017-04-18 13:24:28+00:00",
  "resource": { "id": "5cb87a8cd490a2ccb256cec4", "type": "order", "data": { "shop_id": 1234567 } }
}
```

Common query patterns: `GET /v1/catalog/blueprints/{id}/print_providers.json` to compare who can fulfill a blueprint; `GET .../print_providers/{id}/variants.json` for variant IDs + placeholder positions; `GET /v1/shops/{shop_id}/orders.json?status=...&page=N` for order sync.

## Quick-start recipes

### Recipe 1 — Upload artwork, create a product, publish it

```bash
# 1. Upload artwork by URL
curl -X POST https://api.printify.com/v1/uploads/images.json \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" -H "User-Agent: my-app" \
  -H "Content-Type: application/json" \
  -d '{"file_name": "design.png", "url": "https://example.com/design.png"}'
# → { "id": "5d15ca551163cde90d7b2203", ... }

# 2. Create the product (blueprint 384 = Gildan 5000 tee, provider 1; price in cents)
curl -X POST https://api.printify.com/v1/shops/$SHOP_ID/products.json \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" -H "User-Agent: my-app" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Tee","description":"…","blueprint_id":384,"print_provider_id":1,
       "variants":[{"id":45740,"price":2400,"is_enabled":true}],
       "print_areas":[{"variant_ids":[45740],"placeholders":[{"position":"front",
         "images":[{"id":"5d15ca551163cde90d7b2203","x":0.5,"y":0.5,"scale":1,"angle":0}]}]}]}'

# 3. Publish to the connected sales channel (200 req/30 min limit!)
curl -X POST https://api.printify.com/v1/shops/$SHOP_ID/products/$PRODUCT_ID/publish.json \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" -H "User-Agent: my-app" \
  -H "Content-Type: application/json" \
  -d '{"title":true,"description":true,"images":true,"variants":true,"tags":true}'
```

Gotchas: get real variant IDs from the catalog first — they differ **per print provider**. On a custom (API) sales channel, publish flips the product to a locked "publishing" state; you must call `publishing_succeeded.json` (or `publishing_failed.json`) to unlock it.

### Recipe 2 — Submit an order and poll it (Python)

```python
import os, time, requests

BASE = "https://api.printify.com/v1"
H = {"Authorization": f"Bearer {os.environ['PRINTIFY_API_TOKEN']}",
     "User-Agent": "my-app", "Content-Type": "application/json"}
shop = os.environ["SHOP_ID"]

order = {
    "external_id": "my-order-0001",          # your idempotent reference
    "line_items": [{"product_id": "5bfd0b66a342bcc9b5563216",
                    "variant_id": 17887, "quantity": 1}],
    "shipping_method": 1,
    "send_shipping_notification": False,
    "address_to": {"first_name": "John", "last_name": "Smith",
                   "email": "buyer@example.com", "phone": "",
                   "country": "US", "region": "CA", "address1": "1 Main St",
                   "address2": "", "city": "San Diego", "zip": "92093"},
}
r = requests.post(f"{BASE}/shops/{shop}/orders.json", json=order, headers=H)
r.raise_for_status()
order_id = r.json()["id"]

while True:                                   # polling backup to webhooks
    o = requests.get(f"{BASE}/shops/{shop}/orders/{order_id}.json", headers=H).json()
    if o["status"] in ("fulfilled", "canceled"):
        break
    time.sleep(300)
```

Gotchas: calculate shipping first with `POST /orders/shipping.json` if you charge buyers real rates. Orders auto-route to production per your shop's order-approval settings; use `send_to_production.json` when set to manual approval.

### Recipe 3 — Signed shipment webhook → notify CRM/customer

```bash
# Register the webhook with a secret (openssl rand -hex 20)
curl -X POST https://api.printify.com/v1/shops/$SHOP_ID/webhooks.json \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" -H "User-Agent: my-app" \
  -H "Content-Type: application/json" \
  -d '{"topic":"order:shipment:created","url":"https://example.com/hooks/printify","secret":"'$SECRET'"}'
```

```python
# Flask listener with constant-time HMAC verification
import hmac, os
from flask import Flask, request, abort

app = Flask(__name__)

@app.post("/hooks/printify")
def printify_hook():
    digest = hmac.new(os.environ["SECRET_TOKEN"].encode(),
                      request.get_data(), "sha256").hexdigest()
    if not hmac.compare_digest(request.headers.get("X-Pfy-Signature", ""),
                               f"sha256={digest}"):
        abort(401)
    event = request.get_json()
    if event["type"] == "order:shipment:created":
        order_id = event["resource"]["id"]
        # fetch full order for tracking number, then update CRM / email buyer
    return "", 200                     # ALWAYS 200 fast — 3 failures = 1h block
```

Gotchas: respond `200` before doing slow work (queue the processing) — after 3 failed deliveries the webhook is **blocked for one hour** and events in that window are lost. Keep a polling backup on `GET /orders.json` for anything business-critical. Use `POST /webhooks/{id}/simulate` to test your listener.

## Integration patterns

- **Provider selection per product**: for each blueprint, `GET .../print_providers.json`, then compare variant costs and provider locations against where your buyers are. US buyers → US provider; EU buyers → EU provider. Some sellers create duplicate products on different providers and route orders by destination.
- **Order sync into a warehouse/CRM**: webhooks (`order:created`, `order:updated`, `order:shipment:created`, `order:shipment:delivered`) as the trigger + a nightly `GET /orders.json` paginated sweep as reconciliation. Webhook payloads are thin (IDs) — always re-fetch the order for full detail.
- **Custom storefront (API sales channel)**: your app owns product display and checkout; on `product:publish:started` webhook, read `publish_details`, upsert into your storefront DB, then call `publishing_succeeded.json` with your external handle. Submit orders on your checkout events.
- **Rate-limit handling**: batch catalog reads (cache blueprints/variants locally — they change rarely), spread publishes to stay under 200/30 min, exponential backoff on 429 starting ~2s, keep error rate under 5%.
