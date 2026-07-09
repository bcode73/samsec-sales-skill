# Square Online Platform Reference

## Overview

Square Online is the e-commerce storefront in the Square ecosystem — a free-to-start online store (Weebly-based site builder) that shares **one catalog, inventory, customer directory, and order book** with Square POS. It's aimed at retail/food sellers who already use (or want) in-person Square and need an online channel with unified inventory. The differentiator vs Shopify/Wix is the **POS↔online unification** and a genuine free tier; the tradeoff is limited design flexibility and a higher online processing fee on Free. You automate it at the **commerce-API layer** (Catalog/Orders/Inventory/Payments) — the storefront pages themselves are UI-only.

## Capabilities & automation surface

| Capability | What it does | Automation |
|---|---|---|
| **Catalog (items)** | Items, variations, categories, modifiers, images, taxes, discounts | **API-accessible** (Catalog API — batch upsert/retrieve); `catalog.version.updated` webhook |
| **Inventory** | Per-variation stock counts per location; auto-decrement on order completion | **API-accessible** (Inventory API); `inventory.count.updated` webhook |
| **Orders** | Online + in-person orders, line items, fulfillments (pickup/delivery/shipment) | **API-accessible** (Orders API — create/retrieve/search); `order.created`, `order.updated`, `order.fulfillment.updated` |
| **Payments** | Card, wallet (Apple/Google Pay), gift cards, ACH | **API-accessible** (Payments API); `payment.created`, `payment.updated`, `refund.created/updated` |
| **Hosted checkout / payment links** | Prebuilt hosted checkout pages and shareable payment links | **API-accessible** (Checkout / Payment Links API) |
| **Customers** | Customer directory shared across channels | **API-accessible** (Customers API); `customer.created/updated/deleted` |
| **Subscriptions** | Recurring billing plans | **API-accessible** (Subscriptions API); `subscription.*` webhooks |
| **Storefront site / pages / theme** | The Square Online website builder, themes, pages, SEO settings | **UI-only** — no site-builder API |
| **Fulfillment options** | Pickup, local delivery, shipping, QR-code ordering | Configured in UI; orders carry fulfillment objects via the API |
| **MCP server** | Natural-language access to the full Square API for AI agents | **Official MCP server** (Beta) — remote (OAuth) or local (token) |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — Square consolidated to unified plans; confirm current numbers and which surface (Square Online vs unified Square subscription) applies to you.*

| Plan | Price (best-effort) | Key gates |
|---|---|---|
| **Free** | $0/mo | `*.square.site` subdomain, Square ads shown, **higher online rate ~3.3% + 30¢**, basic inventory, unlimited items, pickup/delivery/shipping, SEO basics |
| **Plus** | ~$49/mo | Custom domain, no Square ads, abandoned-cart emails, gift cards, expanded customization, advanced item settings, QR ordering |
| **Premium** | ~$149/mo | Lower processing rate, real-time shipping rates, advanced reporting, 24/7 phone support |
| **Square Pro** | Custom | For businesses processing >$250k/yr — discounted processing, hardware discounts, account management |

- **Processing fees** (best-effort): online ~**3.3% + 30¢** (lower on paid tiers); in-person **2.6% + 15¢**; manually-keyed higher. Fees are separate from the subscription.
- **Free-plan break-even**: subscription ÷ (online-fee delta on your volume) = the monthly sales where upgrading pays for itself.
- **Tax**: automatic calculation **US & Canada only**.
- **API access is not plan-gated** — the Square APIs work regardless of your Square Online subscription tier (you need a Square account + Developer app).
- **Rate limits**: not publicly published; `429 RATE_LIMITED` under load → exponential backoff + jitter.
- **OAuth tokens**: access tokens expire after **30 days**; refresh tokens rotate access tokens.

## Integrations

- **Square POS** — bidirectional: the same catalog/inventory/customers/orders flow across in-person and online. This is the core value and the core pain (sync lag → overselling).
- **CRM / data warehouse** — outbound via webhooks (`order.created`, `customer.created`, `inventory.count.updated`) + follow-up API reads; or scheduled API pulls (`SearchOrders`, `BatchRetrieveInventoryCounts`).
- **Zapier / Make** — Square triggers (new order, new customer) and actions (create customer, create order/invoice).
- **Square App Marketplace** — third-party connectors (accounting, shipping, marketing). Smaller than Shopify's app ecosystem.
- **SDKs** — official server SDKs for Node.js, Python, Java, Ruby, PHP, .NET, Go; Web Payments SDK for client-side card entry.
- **MCP server** — `https://mcp.squareup.com/sse` (remote, OAuth) or `npx square-mcp-server` (local) for AI-agent access.

## Data model

Square objects are shared across POS and Online. Key objects:

**Catalog item (with variation)** — items contain one or more variations; prices live on the variation:
```json
{
  "object": {
    "type": "ITEM",
    "id": "#Coffee",
    "item_data": {
      "name": "Coffee",
      "description": "Fresh roasted",
      "category_id": "#Beverages",
      "variations": [
        {
          "type": "ITEM_VARIATION",
          "id": "#Coffee-Small",
          "item_variation_data": {
            "item_id": "#Coffee",
            "name": "Small",
            "pricing_type": "FIXED_PRICING",
            "price_money": { "amount": 300, "currency": "USD" },
            "track_inventory": true
          }
        }
      ]
    }
  }
}
```

**Order** — `location_id` + `line_items` (catalog-referenced or ad hoc) + optional `fulfillments`:
```json
{
  "order": {
    "location_id": "LOCATION_ID",
    "line_items": [
      { "quantity": "1", "catalog_object_id": "ITEM_VARIATION_ID" }
    ],
    "fulfillments": [
      {
        "type": "PICKUP",
        "state": "PROPOSED",
        "pickup_details": { "recipient": { "display_name": "Jordan" }, "pickup_at": "2026-07-01T17:00:00Z" }
      }
    ]
  }
}
```

**Inventory count** — quantity is per `catalog_object_id` (variation) × `location_id`:
```json
{
  "catalog_object_id": "ITEM_VARIATION_ID",
  "location_id": "LOCATION_ID",
  "state": "IN_STOCK",
  "quantity": "12",
  "calculated_at": "2026-06-29T12:00:00Z"
}
```

- **Money** is always an integer in the smallest currency unit (cents) + a currency code: `{ "amount": 300, "currency": "USD" }`.
- IDs: when creating catalog objects you may use temporary `#`-prefixed IDs that map to real `idempotency`-safe IDs in the response (`id_mappings`).
- Pagination: cursor-based — responses return a `cursor`; pass it as `cursor` on the next call.

## Quick-start recipes

### Recipe 1 — List catalog items
**Trigger:** export your products into another system.
```bash
curl https://connect.squareup.com/v2/catalog/list?types=ITEM \
  -H "Authorization: Bearer $SQUARE_ACCESS_TOKEN" \
  -H "Square-Version: 2026-06-18"
```
```python
import os, requests
BASE = "https://connect.squareup.com/v2"
H = {"Authorization": f"Bearer {os.environ['SQUARE_ACCESS_TOKEN']}",
     "Square-Version": "2026-06-18", "Content-Type": "application/json"}

items, cursor = [], None
while True:
    params = {"types": "ITEM"}
    if cursor: params["cursor"] = cursor
    r = requests.get(f"{BASE}/catalog/list", headers=H, params=params).json()
    items += r.get("objects", [])
    cursor = r.get("cursor")
    if not cursor: break
print(len(items), "items")
```
**Gotcha:** prices and `track_inventory` live on the **variation**, not the item — drill into `item_data.variations`.

### Recipe 2 — Read live inventory so you don't oversell
**Trigger:** keep an external system's stock in sync with Square.
```python
r = requests.post(f"{BASE}/inventory/counts/batch-retrieve", headers=H, json={
    "catalog_object_ids": ["ITEM_VARIATION_ID_1", "ITEM_VARIATION_ID_2"],
    "location_ids": ["LOCATION_ID"]
}).json()
for c in r.get("counts", []):
    print(c["catalog_object_id"], c["state"], c["quantity"])
```
To correct a wrong count, post a physical-count adjustment:
```python
requests.post(f"{BASE}/inventory/changes/batch-create", headers=H, json={
    "idempotency_key": "unique-key-123",
    "changes": [{
        "type": "PHYSICAL_COUNT",
        "physical_count": {
            "catalog_object_id": "ITEM_VARIATION_ID_1",
            "location_id": "LOCATION_ID",
            "state": "IN_STOCK",
            "quantity": "12",
            "occurred_at": "2026-06-29T12:00:00Z"
        }
    }]
}).json()
```
**Gotcha:** the Inventory API is the source of truth — don't trust the dashboard sync toggle. Subscribe to `inventory.count.updated` for real-time deltas.

### Recipe 3 — Listen for new online orders (webhook)
**Trigger:** push every Square Online sale into a CRM/Slack.
```python
import hmac, hashlib, base64
from flask import Flask, request, abort
app = Flask(__name__)
SIGNATURE_KEY = os.environ["SQUARE_WEBHOOK_SIGNATURE_KEY"]
NOTIFICATION_URL = "https://example.com/square/webhook"  # must match exactly

def verify(body_bytes, signature):
    payload = NOTIFICATION_URL.encode() + body_bytes
    digest = hmac.new(SIGNATURE_KEY.encode(), payload, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, signature)

@app.post("/square/webhook")
def hook():
    sig = request.headers.get("x-square-hmacsha256-signature", "")
    if not verify(request.get_data(), sig):
        abort(401)
    event = request.get_json()
    if event.get("type") in ("order.created", "order.updated"):
        order_id = event["data"]["id"]
        full = requests.post(f"{BASE}/orders/search", headers=H, json={
            "location_ids": ["LOCATION_ID"],
            "query": {"filter": {"order_id_filter": {"order_ids": [order_id]}}}
        }).json()  # or RetrieveOrder
        # ... push to CRM ...
    return "", 200
```
**Gotcha:** the signature is over **notification URL + raw body**, not the body alone. Hash the raw bytes (not a re-serialized dict) and match the configured URL exactly (no trailing slash). Prefer the official SDK `WebhooksHelper`.

## Integration patterns

- **CRM/warehouse sync** — webhook-first (`order.created`, `customer.created`, `inventory.count.updated`) with a follow-up GET for the full object, since the notification carries an id + minimal data. Dedupe on `event_id`; reconcile nightly with `SearchOrders` (filter by `updated_at`) to catch missed events.
- **Inventory reconciliation** — never let two systems both decrement stock. Make Square the master (or your ERP the master and push via `BatchChangeInventory`), enable `track_inventory` per variation, and treat the Inventory API as truth — the UI sync toggle is unreliable.
- **Webhook reliability** — Square retries for up to 24h with exponential backoff; respond 2xx fast and process async. Source IPs are static (allowlist them). Always HMAC-verify; reject on mismatch.
- **Auth lifecycle** — for multi-merchant apps, store the OAuth refresh token securely and refresh access tokens before the 30-day expiry; handle `401` by refreshing then retrying. For your own account, use a personal access token.
- **Idempotency** — order/payment/inventory writes take an `idempotency_key`; reuse it on retries so a network blip doesn't double-create.
- **Versioning** — pin `Square-Version` (date string); upgrade deliberately and read the changelog before bumping.
