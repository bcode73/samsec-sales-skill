# CustomCat Platform Reference

## Overview

CustomCat is a budget, US-based (Detroit, Michigan) print-on-demand (POD) fulfillment service: you upload designs, CustomCat prints products on demand and ships them, and you carry no inventory. It works two ways — as a backend that syncs to a hosted store (Shopify, Etsy, WooCommerce, BigCommerce), or headless via its REST API. Positioning vs Printful/Printify: **lowest base prices + fastest US production (1–3 business days)** because it owns its Detroit facility (ships 40,000+ units/day), at the cost of **no private-label branding** (products keep the manufacturer's tags) and **US-only fulfillment** (international shipping 1–4 weeks). Three decoration methods: **DIGISOFT™** (direct-to-garment / direct-to-film), **embroidery**, and **dye sublimation**.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| Catalog (200+ products, SKUs, images, weights, inventory) | Apparel, drinkware/housewares, accessories; branded blanks (Gildan, Bella+Canvas, Port Authority, Adidas) | **API-accessible** (`GET /catalog`, `/catalog/{id}`, `/catalog/sku/{sku}`) |
| Catalog categories | Filter catalog by decoration method / style | **API-accessible** (`GET /catalogcategory`) |
| Designs | List designs you've uploaded | **API-accessible** (`GET /design`) |
| Products (your created products) | Products you've built from blanks + designs | **API-accessible** (`GET /product`, `/product/{id}`) |
| Orders (submit, cancel, status, replacement) | Full order lifecycle; status `Pending → Verified → Shipped` | **API-accessible** (`POST/DELETE /order/{order_id}`, `GET /order/status/{order_id}`) + **webhook-accessible** |
| Shipping rates | List methods + calculate cost before submitting | **API-accessible** (`GET /shipping`, `POST /shipping/{shipping_id}`) |
| Webhooks (6 topics) | Order/product/design events via HTTP POST | **webhook-accessible** (`GET/POST/PUT/DELETE /webhook`, **NOT signed**) |
| Store connectors (Shopify/Etsy/WooCommerce/BigCommerce) | Auto-import products + push fulfillment | **UI-only** to configure (then events flow via API/webhook) |
| Mockup / design tool | Basic in-dashboard design + mockups | **UI-only** (no external image library) |
| CSV product upload | Bulk-add products without the API | **UI-only** |
| Custom branding / private labels | — **not offered** (products keep manufacturer tags) | **N/A** |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against the live pricing page.*

| Plan | Cost | Key contents |
|---|---|---|
| **Lite** | $0/mo | Full catalog at **standard wholesale** prices, unlimited products + order fulfillment, support, private forum |
| **Pro** | **$30/mo**, or **$300/yr (≈$25/mo)** — 60-day free trial | **20–40% off** standard wholesale across the entire catalog, exclusive promotions, early access |
| **Enterprise** | Custom (contact sales) | **30–50% off**, **custom API access**, dedicated account manager, all Pro features |

**Per-item / order add-ons:** **back print +$5 per line item**; design files should be **300 DPI** (or declare embedded DPI). Sample orders available. CustomCat charges *you* (base + fulfillment + shipping) when an order is submitted, then prints and ships — a declined card returns `400 Charge Failed`.

**API access:** the standard REST API is available to Lite/Pro accounts via read-only + read-write keys (Settings > Store > API). "Custom API access" is called out as an **Enterprise** benefit for higher-touch integrations. No published rate limits — be courteous and cache catalog reads.

## Integrations

- **Store connectors (bidirectional):** Shopify, Etsy, WooCommerce, BigCommerce. Products sync **out** to the store; orders flow **in** to CustomCat; tracking flows **back**. (Amazon/eBay listed as planned.) Fewer connectors than Printful (20+).
- **Headless (reads + writes):** the REST API lets you submit orders, read catalog/stock, quote shipping, and register webhooks — no hosted store required.
- **CSV:** bulk product upload in the dashboard for non-API workflows.
- **Affiliate program:** CustomCat runs an affiliate program (monthly commission on product cost, excluding shipping/refunds/returns) with a reporting dashboard — see `/sales-affiliate-program` for promoting it.

## Data model

**Catalog product vs SKU** — a *catalog product* is a blank style; a *SKU* (`catalog_sku`) is the specific color+size you fulfill. Order by `sku` (your CustomCat product) or by `catalog_sku` + `design_url` (external design printed on a blank).

Order submission body (`POST /order/{order_id}` — note required `shipping_*` fields, a `shipping_method` from `/shipping`, and the `items` array):

```json
{
  "api_key": "READ_WRITE_KEY",
  "shipping_first_name": "Joe",
  "shipping_last_name": "Testing",
  "shipping_email": "joe@example.com",
  "shipping_phone": "3135551234",
  "shipping_address1": "1300 Rosa Parks Blvd",
  "shipping_city": "Detroit",
  "shipping_state": "MI",
  "shipping_zip": "48216",
  "shipping_country": "US",
  "shipping_method": "Economy",
  "items": [
    { "sku": "YOUR_SKU", "quantity": 1 },
    { "catalog_sku": "CC_BLANK_SKU", "design_url": "https://example.com/art.png", "preset_id": 2, "quantity": 1 }
  ],
  "sandbox": 1
}
```

Order create response:

```json
{ "ORDER_ID": "Your_Order_ID", "MSG": "Order added successfully", "CUSTOMCAT_ORDER_ID": "UUID" }
```

Order status (`GET /order/status/{order_id}`): `ORDER_STATUS` is `Pending | Verified | Shipped`; each `LINE_ITEMS[].STATUS` walks `Processing → Picked/Received → Printed → Binned → Ready to Ship → Shipped` (or `Failed QA` / `Cancelled`); `SHIPMENTS[]` carries `TRACKING_ID`, `METHOD`, `VENDOR`.

**Design placement presets** (`preset_id`, Digisoft): `1` Left Chest (wide), `2` Full Front, `3` Full Back, `4` Center Chest (default), `9` Default Back, `10` Left Chest (tall). Omit `preset_id` for exact placement (transparent space preserved). Sublimation: omit for edge-to-edge, `4` centered. Leather-patch hats: `2` rectangle, `12` oval, `14` circle, `18` small circle.

## Quick-start recipes

### Recipe 1 — Submit an order (headless, idempotent)

Trigger: a sale happens in your own app; you want CustomCat to fulfill it. Use the **read-write** key and a **unique** `order_id` (the idempotency key).

```bash
curl -X POST https://customcat-beta.mylocker.net/api/v1/order/MYSTORE-1001 \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$CC_RW_KEY"'",
    "shipping_first_name":"Joe","shipping_last_name":"Testing",
    "shipping_email":"joe@example.com","shipping_phone":"3135551234",
    "shipping_address1":"1300 Rosa Parks Blvd","shipping_city":"Detroit",
    "shipping_state":"MI","shipping_zip":"48216","shipping_country":"US",
    "shipping_method":"Economy",
    "items":[{"catalog_sku":"CC_BLANK_SKU","design_url":"https://example.com/art.png","preset_id":2,"quantity":1}],
    "sandbox": 1
  }'
```

```python
import requests

BASE = "https://customcat-beta.mylocker.net/api/v1"
RW_KEY = "..."  # read-WRITE key — a read-only key here returns 403

def submit_order(order_id, recipient, items, sandbox=True):
    body = {"api_key": RW_KEY, "shipping_method": "Economy",
            "items": items, "sandbox": 1 if sandbox else 0, **recipient}
    r = requests.post(f"{BASE}/order/{order_id}", json=body)
    data = r.json()
    if r.status_code == 400:
        msg = data.get("error_description") or data.get("MSG", "")
        if "Duplicate Order" in msg:
            return {"status": "already_accepted", "order_id": order_id}   # idempotent: not a failure
        if data.get("suggestions"):                                       # AVS failure
            return {"status": "address_invalid", "suggestions": data["suggestions"]}
    r.raise_for_status()
    return {"status": "accepted", "customcat_order_id": data["CUSTOMCAT_ORDER_ID"]}
```

Gotchas: use the read-write key; keep `order_id` unique; test with `sandbox=1` before going live; on `Invalid Shipping Address` surface the `suggestions` to the buyer.

### Recipe 2 — Quote shipping before checkout

Trigger: show the buyer an accurate shipping cost / pick a method.

```bash
# 1. List available methods
curl "https://customcat-beta.mylocker.net/api/v1/shipping?api_key=$CC_RO_KEY"

# 2. Calculate cost for a method id + destination + items
curl -X POST "https://customcat-beta.mylocker.net/api/v1/shipping/{shipping_id}" \
  -H "Content-Type: application/json" \
  -d '{"api_key":"'"$CC_RO_KEY"'","country":"US","state":"MI","items":[{"sku":"YOUR_SKU","quantity":2}]}'
```

Gotchas: the `shipping_method` you later send in an order must match a method name returned here, or you'll get `400 Invalid Shipping Method`. Reads can use the read-only key.

### Recipe 3 — Register an order-shipped webhook, with a polling backup

Trigger: notify your buyer when their order ships. CustomCat webhooks are **not signed** — verify by the read-only `api_key` echoed in the body, and keep polling as a safety net.

```python
import requests
BASE = "https://customcat-beta.mylocker.net/api/v1"

# Register (read-WRITE key) — topic + your HTTPS endpoint
requests.post(f"{BASE}/webhook", json={
    "api_key": RW_KEY, "topic": "order-shipped",
    "url": "https://yourapp.com/hooks/customcat"
})

# Handler: payload = {api_key, order_id, customcat_order_id, tracker_number, tracking_url}
def handle(payload):
    if payload.get("api_key") != RO_KEY_EXPECTED:   # not HMAC — verify the echoed read-only key
        return 401
    notify_buyer(payload["order_id"], payload["tracking_url"])
    return 200

# BACKUP: webhooks are best-effort. Periodically poll
# GET /order/status/{order_id} for recently-Verified orders that haven't
# emitted a shipment, so a dropped order-shipped event never loses a notification.
```

Topics: `order-shipped`, `order-partial-shipment` (adds `items_remaining`), `product-created`, `product-deleted`, `product-updated`, `design-rejected`. Gotchas: registering a webhook is a **write** (read-write key); payloads are unsigned, so treat the echoed key as the only identity check and pair with polling.

## Integration patterns

- **Store-fronted (most users):** connect CustomCat to Shopify/Etsy/WooCommerce/BigCommerce in the UI, import + map products to CustomCat SKUs, enable auto-fulfillment, and let orders/tracking flow automatically. Failures are almost always a paused connection, unmapped products, or manual-approval left on.
- **Headless:** submit orders directly via `POST /order/{order_id}` with a unique id and the read-write key; quote shipping first; reconcile fulfillment via the `order-shipped` webhook **plus** a `GET /order/status/{order_id}` polling sweep.
- **Key hygiene:** read-only key for catalog/shipping reads and webhook-identity checks; read-write key for orders + webhook registration. A read-only key on a write call is the #1 cause of `403 Forbidden`.
- **Idempotency & errors:** `order_id` is the idempotency key (`400 Duplicate Order` on re-use); handle AVS `suggestions`, out-of-stock SKU (`There is an issue with the order. SKU: …`), and `Charge Failed` distinctly rather than blanket-retrying.
