# Ecwid Platform Reference

## Overview

Ecwid (by Lightspeed) is embeddable ecommerce: a JS widget that adds a full store — catalog, cart, checkout — to any site you already run (WordPress, Wix, Squarespace, custom HTML), plus a hosted "Instant Site" if you have no site at all. 0% Ecwid transaction fees on all plans (processor fees still apply). The trade: convenience and multichannel reach over deep design control and page speed.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Storefront widget / Instant Site | Embeddable store + hosted one-pager | **UI-only** to configure; Storefront JS API for front-end customization |
| Products & categories | Catalog, variations (paid plans), digital goods (Venture+) | **API-accessible** (full CRUD) + **webhook-accessible** (`product.*`, `category.*`) |
| Orders & abandoned carts | Order management, unfinished sales, recovery emails | **API-accessible** + **webhook-accessible** (`order.*`, `unfinished_order.*`) |
| Customers & groups | Customer records, groups/pricing tiers | **API-accessible** + **webhook-accessible** (`customer.*`) |
| Coupons & promotions | Discounts, scheduled promos | **API-accessible** |
| Multichannel (Instagram/Facebook/TikTok/Google/Amazon) | Sync catalog to social/marketplaces | **UI-only** (channel connections) |
| POS (Lightspeed ecosystem) | In-person sales, shared inventory | **UI-only** |
| Payments (PayPal/Stripe/Square + 100+) | Checkout processing | **UI-only** config; Custom Payment API for building new methods |
| Shipping | Rates, labels, tracking | **UI-only** config; Custom Shipping API for new methods |
| Email marketing / abandoned-cart automations | Built-in campaigns | **UI-only** |
| App storage | Key-value store for app data | **API-accessible** |
| Batch API | Bundle many API calls into one | **API-accessible** |

No MCP server found. Zapier + Make apps cover no-code triggers/actions.

## Pricing, limits & plan gates

*Best-effort (2026-07) — pricing changed 2026-03-02; verify at ecwid.com/pricing.*

- **Free** — 10 products, basic widget. **No API access, no digital goods, no variations.**
- **Starter — ~$5/mo** (annual) — 10 products, lighter feature set.
- **Venture — ~$29/mo** — 100 products, digital products, app market access.
- **Business — ~$49/mo** — 2,500 products, product variations, staff accounts.
- **Unlimited — ~$119/mo** — unlimited products, POS, priority support.

Watch-outs: **API requires a paid plan**; product variations are effectively a paid upgrade; post-Lightspeed-acquisition price increases are a recurring complaint and the old "Free Forever" positioning has narrowed. Rate limit 600 req/min per token.

## Integrations

Embeds into WordPress, Wix, Squarespace, Weebly, Joomla, Drupal, any HTML site. Payments: PayPal, Stripe, Square + local gateways. Apps: 1,500+ in the App Market (QuickBooks, ShipStation, Printful, Omnisend…). Data flow: catalog/orders/customers read+write via REST v3; store events out via signed webhooks; QuickBooks sync is **one-way** (sales out; inventory does NOT sync back into Ecwid).

## Data model

Store (`storeId`) → Products (with variations/combinations, categories, product classes/attributes) → Orders (line items, payment + fulfillment status; unfinished/abandoned sales are separate) → Customers (with groups). Coupons/promotions attach to the store.

```json
// Webhook event (thin — always re-fetch the entity)
{ "eventId": "80aece08-…", "eventCreated": 1234567, "storeId": 1003,
  "entityId": 100, "eventType": "order.created" }

// Product (representative core fields)
{ "id": 37208339, "sku": "TEE-001", "name": "Classic Tee", "price": 25.00,
  "enabled": true, "quantity": 10, "categoryIds": [9691094] }

// Order (representative core fields)
{ "orderNumber": 100, "email": "buyer@example.com", "total": 27.50,
  "paymentStatus": "PAID", "fulfillmentStatus": "AWAITING_PROCESSING",
  "items": [{ "productId": 37208339, "sku": "TEE-001", "quantity": 1, "price": 25.00 }] }
```
<!-- Product/Order shapes constructed from docs field lists — verify against live API -->

## Quick-start recipes

### Recipe 1 — Pull new orders into a CRM/warehouse (Python, paginated)

```python
import os, time, requests

BASE = f"https://app.ecwid.com/api/v3/{os.environ['STORE_ID']}"
H = {"Authorization": f"Bearer {os.environ['ECWID_SECRET_TOKEN']}"}

offset, total = 0, 1
while offset < total:
    r = requests.get(f"{BASE}/orders", headers=H,
                     params={"offset": offset, "limit": 100,
                             "createdFrom": "2026-07-01 00:00:00"})
    if r.status_code == 429:
        time.sleep(int(r.headers.get("Retry-After", 5))); continue
    r.raise_for_status()
    body = r.json()
    for order in body["items"]:
        pass  # upsert order into your DB / CRM
    total = body["total"]
    offset += body["count"]
```

Gotchas: 600 req/min per token — honor `Retry-After` on 429; API needs a paid plan.

### Recipe 2 — Signed webhook listener (Flask) → verified order sync

```python
import base64, hmac, hashlib, os, requests
from flask import Flask, request, abort

app = Flask(__name__)
H = {"Authorization": f"Bearer {os.environ['ECWID_SECRET_TOKEN']}"}

@app.post("/hooks/ecwid")
def ecwid_hook():
    body = request.get_json(force=True)
    msg = f"{body['eventCreated']}.{body['eventId']}".encode()
    digest = hmac.new(os.environ["ECWID_CLIENT_SECRET"].encode(),  # client_secret, NOT secret_* token!
                      msg, hashlib.sha256).digest()
    if not hmac.compare_digest(request.headers.get("X-Ecwid-Webhook-Signature", ""),
                               base64.b64encode(digest).decode()):
        abort(401)
    if body["eventType"] == "order.created":
        store, oid = body["storeId"], body["entityId"]
        o = requests.get(f"https://app.ecwid.com/api/v3/{store}/orders/{oid}", headers=H)
        # payload is thin by design — this re-fetch is the actual data
    return "", 200
```

Gotchas: the signing key is the app's **`client_secret`** issued at app registration — using the `secret_*` access token makes every verification fail. Payloads carry only IDs; always re-fetch.

### Recipe 3 — Bulk price update via cURL

```bash
# Update a product's price (PUT with partial body)
curl -X PUT "https://app.ecwid.com/api/v3/$STORE_ID/products/$PRODUCT_ID" \
  -H "Authorization: Bearer $ECWID_SECRET_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price": 29.00}'
```

Gotchas: PUT accepts partial updates (only send changed fields). For many updates, use the Batch API to bundle calls and stay under the 600/min limit.

## Integration patterns

- **Store→CRM sync**: `order.*` / `customer.*` webhooks for freshness (verify signature, re-fetch entity) + a nightly paginated `GET /orders?createdFrom=…` reconciliation sweep.
- **Catalog sync**: `product.updated` webhook → re-fetch just that product ("make your app in sync in one HTTP request instead of downloading the whole catalog" — the docs' own advice).
- **Existing-site commerce**: Ecwid's core fit — embed the widget on the site you already rank with, rather than migrating to a hosted store builder. Compare against Snipcart (JS cart, dev-first) and Shopify Buy Button for the same job.
- **Rate-limit discipline**: batch writes via the Batch API; honor `Retry-After`; one token per integration so limits don't collide.
