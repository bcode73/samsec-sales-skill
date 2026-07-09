# Wix eCommerce Platform Reference

## Overview

Wix eCommerce (a.k.a. Wix Stores) is the commerce layer inside the Wix website builder. It targets small stores, solopreneurs, and service-plus-store businesses who want a drag-and-drop site with a real store bolted on — an easy-setup alternative to Shopify/BigCommerce. Differentiator: design freedom + native bookings/ticketing/restaurant on the same platform. Weakness: JS-heavy performance and a walled-garden data/template model that bites at scale.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Stores / Products** | Catalog, variants, options, inventory, media, SEO per product | **API-accessible** — Stores **Products v3** (`/stores/v3/products/query`, etc.), Inventory, Variants APIs |
| **Orders** | Order lifecycle: view, update, cancel, fulfillment, payments | **API + webhook** — eCommerce **Orders API** (`/ecom/v1/orders/...`); Order Approved/Updated/Canceled events |
| **Checkout / Cart** | Custom checkout, current cart, draft orders, discounts/coupons | **API-accessible** — eCommerce Cart/Checkout/Draft Orders APIs |
| **Payments** | Wix Payments (native) or Stripe/PayPal and others | Mostly **UI-configured**; transactions surface on orders via API |
| **Subscriptions** | Recurring product/box subscriptions, frequency, free trials | **API-accessible** (subscription info on line items); plan-gated |
| **Dropshipping** | Modalyst, Spocket, Printful, Printify integrations | **UI-configured** app integrations; orders flow through Orders API |
| **Multichannel selling** | Sync catalog to Instagram/Facebook Shop, eBay, Amazon, Google | **UI/app-configured** (channel apps); `channelInfo.type` on orders |
| **Abandoned cart recovery** | Automated cart-recovery emails | **UI-configured**; plan-gated above entry tiers |
| **Bookings / POS / Tickets** | Native scheduling, in-person POS, event ticketing | Separate Wix APIs (Bookings, etc.) — out of scope here |
| **Wix MCP server** | AI-agent access to account/site APIs | **API-accessible** via API key — primary programmatic interface for AI agents |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against Wix's live pricing; eCommerce gating in particular changes.*

| Plan | ~Price/mo (annual) | eCommerce notes |
|---|---|---|
| **Light** | ~$17 | **No eCommerce** — basic site only |
| **Core** | ~$29 | **Unlocks eCommerce**: online store, dropshipping, loyalty |
| **Business** | ~$39 | Adds **advanced shipping** + **automated sales tax** |
| **Business Elite** | ~$159 | Higher dropshipping/product-review limits, loyalty program |

- **Fees:** Wix charges **no extra platform transaction fee** when you use **Wix Payments**; you still pay the processor's card rate. Using some third-party gateways may carry their own costs.
- **API/webhook gating:** the REST APIs and webhooks themselves aren't tier-gated the way some platforms are, but the *store* must be on **Core+** to transact. Abandoned-cart recovery and advanced merchandising are paywalled above entry.
- **Rate limits / retries:** webhooks retry up to **12 times** on failure (1 min → escalating up to 12 h) if you don't return 200 within **1250 ms**.

## Integrations

- **Direction:** the REST APIs are **bidirectional** (read + write products, orders, inventory, carts). Webhooks are **outbound** (Wix → your server) for near-real-time events.
- **Auth:** **API keys** (account owner generates; `Authorization` + `wix-site-id`/`wix-account-id`) for self-managed/headless, CLI, n8n, and the **Wix MCP server**. **OAuth** for published 3rd-party Wix apps.
- **SDKs:** official `@wix/sdk` core + domain packages (`@wix/stores`, `@wix/ecom`). `ApiKeyStrategy` or `OAuthStrategy`.
- **iPaaS:** native **n8n** integration documented; Zapier/Make via the App Market. **Wix Headless** for fully custom storefronts (React/Next.js etc.) talking to the same APIs.
- **CRM/warehouse:** no native "push to Snowflake" — you build it: webhook → verify JWT → GET full entity → write to your CRM/warehouse.

## Data model

IDs are GUIDs. Money is represented as `{ "amount": "199.99", "formattedAmount": "$199.99" }` (string amounts). Key objects:

### Product (Stores v3 — abbreviated)

```json
{
  "id": "string (GUID)",
  "revision": "string (int64)",
  "name": "Premium Wireless Headphones",
  "slug": "premium-wireless-headphones",
  "visible": true,
  "visibleInPos": true,
  "productType": "PHYSICAL",
  "plainDescription": "string (HTML, max 16000 chars)",
  "url": { "relativePath": "/product-page/...", "url": "https://..." },
  "media": { "main": { "id": "string", "mediaType": "IMAGE" } },
  "options": [
    { "id": "string", "name": "Color", "choices": [ { "id": "string", "value": "Black" } ] }
  ],
  "physicalProperties": {
    "shippingWeightRange": { "minValue": 0, "maxValue": 0 },
    "deliveryProfileId": "string (GUID)"
  },
  "seoData": { "tags": [], "settings": { "keywords": [] } }
}
```
> Query Products does **not** return variant or price data — fetch those via Get Product or the Variants API.

### Order (eCommerce — abbreviated)

```json
{
  "id": "e0e2e0e2-...",
  "number": 1001,
  "createdDate": "2024-01-15T10:30:00.000Z",
  "lineItems": [
    {
      "id": "item-001",
      "productName": { "original": "Premium Wireless Headphones" },
      "catalogReference": { "catalogItemId": "prod-12345", "appId": "215238eb-..." },
      "quantity": 1,
      "price": { "amount": "199.99", "formattedAmount": "$199.99" },
      "itemType": { "preset": "PHYSICAL" }
    }
  ],
  "buyerInfo": { "email": "customer@example.com", "contactId": "c0c0..." },
  "paymentStatus": "PAID",
  "fulfillmentStatus": "FULFILLED",
  "currency": "USD",
  "priceSummary": {
    "subtotal": { "amount": "199.99", "formattedAmount": "$199.99" },
    "tax": { "amount": "20.00", "formattedAmount": "$20.00" },
    "total": { "amount": "219.99", "formattedAmount": "$219.99" }
  },
  "status": "APPROVED",
  "channelInfo": { "type": "WEB" }
}
```
- `status`: `INITIALIZED | APPROVED | CANCELED | PENDING | REJECTED` (Search Orders won't return `INITIALIZED`).
- `paymentStatus`: `NOT_PAID | PAID | PARTIALLY_REFUNDED | FULLY_REFUNDED | PENDING | ...`
- `channelInfo.type`: `WEB | POS | EBAY | AMAZON | FACEBOOK | TIKTOK | OTHER_PLATFORM | ...` — set this when creating orders from external systems.

## Quick-start recipes

### Recipe 1 — List visible products (API key)

**cURL**
```sh
curl -X POST \
  'https://www.wixapis.com/stores/v3/products/query' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <API_KEY>' \
  -H 'wix-site-id: <SITE_ID>' \
  -d '{
    "query": {
      "filter": { "visible": { "$eq": true } },
      "sort": [{ "fieldName": "createdDate", "order": "DESC" }],
      "cursorPaging": { "limit": 10 }
    }
  }'
```

**Python**
```python
import requests

BASE = "https://www.wixapis.com"
HEADERS = {
    "Authorization": API_KEY,          # from manage.wix.com/account/api-keys
    "wix-site-id": SITE_ID,            # site-level calls require this
    "Content-Type": "application/json",
}

def list_products(cursor=None, limit=100):
    query = {"filter": {"visible": {"$eq": True}},
             "sort": [{"fieldName": "createdDate", "order": "DESC"}],
             "cursorPaging": {"limit": limit}}
    if cursor:
        query["cursorPaging"]["cursor"] = cursor
    r = requests.post(f"{BASE}/stores/v3/products/query",
                      headers=HEADERS, json={"query": query})
    r.raise_for_status()
    data = r.json()
    return data["products"], data["pagingMetadata"]["cursors"].get("next")
```
Gotcha: a 403 means a missing `wix-site-id`, wrong scope, or a non-owner key. Variants aren't in this response.

### Recipe 2 — Pull paid+fulfilled orders for a CRM/warehouse (cursor pagination)

**cURL**
```sh
curl -X POST \
  'https://www.wixapis.com/ecom/v1/orders/search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <API_KEY>' \
  -H 'wix-site-id: <SITE_ID>' \
  -d '{
    "search": {
      "filter": { "paymentStatus": "PAID", "fulfillmentStatus": "FULFILLED" },
      "sort": [{ "fieldName": "createdDate", "order": "DESC" }],
      "cursorPaging": { "limit": 100 }
    }
  }'
```

**Python (paginate to a warehouse)**
```python
def export_orders():
    cursor, out = None, []
    while True:
        search = {"filter": {"paymentStatus": "PAID"},
                  "sort": [{"fieldName": "createdDate", "order": "DESC"}],
                  "cursorPaging": {"limit": 100}}
        if cursor:
            search["cursorPaging"]["cursor"] = cursor
        r = requests.post(f"{BASE}/ecom/v1/orders/search",
                          headers=HEADERS, json={"search": search})
        r.raise_for_status()
        body = r.json()
        out.extend(body["orders"])
        meta = body["metadata"]
        if not meta.get("hasNext"):
            break
        cursor = meta["cursors"]["next"]
    return out   # write rows to your warehouse here
```
Note: Search Orders excludes `INITIALIZED` orders and defaults to `createdDate DESC`, `limit` 100 (max 100).

### Recipe 3 — Verify an Order webhook (signed JWT) and react

Wix posts event data as a **signed JWT**. Verify with your app's **public key** (Webhooks page of the app dashboard), then act.

**Python (Flask listener)**
```python
import jwt  # PyJWT
from flask import Flask, request, abort

app = Flask(__name__)
WIX_PUBLIC_KEY = open("wix_public_key.pem").read()
_seen = set()  # persist this in prod (Redis/DB) for real dedupe

@app.post("/webhooks/wix")
def wix_webhook():
    token = request.get_data(as_text=True)  # raw body is the JWT
    try:
        payload = jwt.decode(token, WIX_PUBLIC_KEY, algorithms=["RS256"])
    except jwt.InvalidTokenError:
        abort(401)
    event_id = payload.get("eventId") or payload.get("id")
    if event_id in _seen:        # duplicates can arrive, possibly out of order
        return "", 200
    _seen.add(event_id)
    # payload may be partial — follow up with a GET for the full order
    # then write to your CRM / warehouse
    return "", 200              # MUST return 200 within 1250 ms or Wix retries
```
Gotchas: respond 200 within **1250 ms**; expect **duplicates and out-of-order** delivery; some events carry only changed fields so do a **follow-up GET**.

## Integration patterns

- **Webhook listener:** register in the Wix Developers Center → receive signed JWT → verify with public key → dedupe on event ID → GET full entity → write downstream → return 200 fast. Use the **Logs** tab in the app dashboard to inspect deliveries; store processed IDs to survive the up-to-12-attempt resend policy.
- **Batch pipeline:** cursor-paginate Search Orders / Query Products (`limit` ≤ 100), follow `metadata.hasNext` + `cursors.next`. Variants/prices need a per-product follow-up call, so budget extra requests.
- **CRM sync architecture:** key contacts on `buyerInfo.contactId` (or email); treat Wix as source of truth for orders; reconcile periodically by re-pulling Search Orders rather than trusting webhooks alone (they can be delayed/duplicated).
- **Auth choice:** self-managed/headless and the Wix MCP server use **API keys** (owner-generated, site-scoped). Published 3rd-party apps use **OAuth** with explicit user-granted permissions. Site-level calls always need `wix-site-id`.
- **External-order ingestion:** when recording orders from POS/marketplaces via Create Order, set `channelInfo.type` to the real source (or `OTHER_PLATFORM`); to edit pricing/line items on an existing order use the **Draft Orders API** (Update Order only changes contact/address/metadata).
