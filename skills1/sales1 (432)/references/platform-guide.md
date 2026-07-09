# Printful Platform Reference

## Overview

Printful is a print-on-demand (POD) fulfillment and merch platform: you upload designs, Printful prints products on demand and ships them to your buyers, and you carry no inventory. It works two ways — as a backend that syncs to a hosted store (Shopify, WooCommerce, Etsy, Wix, Squarespace, Webflow, BigCommerce, Ecwid), or headless via its REST API. Differentiator vs Printify: Printful owns its fulfillment (more consistent quality, in-house branding/embroidery) rather than brokering a provider network.

## Capabilities & automation surface

| Capability | What it does | Surface |
|---|---|---|
| Catalog (products, variants, prices, sizes, availability) | 500+ blank products; variants are color/size SKUs | **API-accessible** (`/v2/catalog-products`, `/v2/catalog-variants`) |
| Orders (create, confirm, update, cancel, items, shipments, invoice) | Full order lifecycle, draft → confirm → ship | **API-accessible** (`/v2/orders`) + **webhook-accessible** |
| Mockup generator | Render product mockups from a design file | **API-accessible** (async `/v2/mockup-tasks`) + webhook (`mockup_task_finished`) |
| Files library | Upload design files for placements | **API-accessible** (`/v2/files`) |
| Shipping rates | Quote rates + delivery estimate before checkout | **API-accessible** (`/v2/shipping-rates`) |
| Order cost estimation | Async estimate of order cost | **API-accessible** (`/v2/order-estimation-tasks`) |
| Warehouse products | Inventory you stock with Printful | **API-accessible** (`/v2/warehouse-products`) |
| Stores & statistics | Connected store metadata + stats | **API-accessible** (`/v2/stores`) |
| Approval sheets | Design approval PDFs | **API-accessible** (`/v2/approval-sheets`) |
| Webhooks (19 events) | Order/shipment/catalog/mockup events | **webhook-accessible** (`/v2/webhooks`, signed, HTTPS-only) |
| Store connectors (Shopify/WooCommerce/Etsy/Wix/…) | Auto-import products + push fulfillment | **UI-only** to configure (then events flow via API/webhook) |
| Branding (inside/outside labels, packing slips, premium images) | White-label the unboxing | **UI-only** to configure; cost applies per item |
| Mockup/design editor (Quick Stores, Design Maker) | No-code product design | **UI-only** |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against the live pricing page.*

| Plan | Cost | Key contents |
|---|---|---|
| **Free** | $0/mo | 509 products, unlimited stores, 10 Quick Stores, 20% off 1 sample/mo |
| **Growth** | $24.99/mo (free above $12K/yr in sales) | up to 33% off product pricing, 9% off branding, 25% off samples, exclusive large front print, free sample embroidery digitization |
| **Enterprise** | Custom | Growth benefits + dedicated Success Manager, custom store management, facility access |

**Per-item / one-time add-ons:** embroidery digitization $2.95–$6.50 (one-time/design), inside label $0.99, outside label $2.49, premium image $1 per image/placement/item. Shipping + taxes calculated per destination.

**API limits:** v2 uses a **leaky-bucket** rate limiter — **120 requests / 60 seconds** by default; on `429`, honor the `retry-after` header. The API itself is **not plan-gated** (Free accounts can use it). The cost gate is on product discounts and sampling, not on API access.

## Integrations

- **Store connectors (bidirectional):** Shopify, WooCommerce, Etsy, Wix, Squarespace, Webflow, BigCommerce, Ecwid, Amazon, eBay. Products sync **out** to the store; orders flow **in** to Printful for fulfillment; shipment/tracking flows **back** to the store.
- **Headless (reads + writes):** the REST API lets you create orders, generate mockups, quote shipping, and read catalog/stock directly — no hosted store required.
- **iPaaS:** Zapier (triggers like new shipment + actions like create order), Pipedream, MESA, Make.
- **MCP:** community MCP server (`Purple-Horizons/printful-mcp`, 17 tools across catalog/orders/fulfillment/mockups) for driving Printful from Claude/Cursor.

## Data model

**Catalog product vs variant** — a *product* is a blank template (e.g., "Unisex Staple T-Shirt"); a *variant* is a specific color+size you actually fulfill. **Always order by `catalog_variant_id`.**

Order item (note `catalog_variant_id`, `source`, and the `placements` → `layers` design structure):

```json
{
  "quantity": 1,
  "catalog_variant_id": 4011,
  "source": "catalog",
  "placements": [
    {
      "placement": "front",
      "technique": "dtg",
      "layers": [
        { "type": "file", "url": "https://example.com/design.png" }
      ]
    }
  ]
}
```

Recipient:

```json
{
  "name": "John Smith",
  "address1": "19749 Dearborn St",
  "city": "Chatsworth",
  "country_code": "US",
  "state_code": "CA",
  "zip": "91311"
}
```

Order states: `draft` (not charged/fulfilled) → `confirmed` → (processing → shipment → delivered); `failed`; `canceled`.

Pagination envelope (uniform across endpoints):

```json
{
  "paging": { "total": 100, "offset": 10, "limit": 20 },
  "_links": { "self": {"href":"..."}, "next": {"href":"..."}, "previous": {"href":"..."} }
}
```

## Quick-start recipes

### Recipe 1 — Create and confirm an order (headless)

Trigger: a sale happens in your own app; you want Printful to fulfill it.
Steps: create draft order with recipient + items → wait for async cost calc → confirm.

```bash
# 1. Create a draft order
curl -X POST https://api.printful.com/v2/orders \
  -H "Authorization: Bearer $PRINTFUL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {"name":"John Smith","address1":"19749 Dearborn St","city":"Chatsworth","country_code":"US","state_code":"CA","zip":"91311"},
    "order_items": [
      {"quantity":1,"catalog_variant_id":4011,"source":"catalog",
       "placements":[{"placement":"front","technique":"dtg","layers":[{"type":"file","url":"https://example.com/design.png"}]}]}
    ]
  }'

# 2. Confirm it for fulfillment (only after cost calculation completes)
curl -X POST https://api.printful.com/v2/orders/{id}/confirm \
  -H "Authorization: Bearer $PRINTFUL_TOKEN"
```

```python
import time, requests

H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
BASE = "https://api.printful.com/v2"

def post(path, body=None):
    while True:
        r = requests.post(f"{BASE}{path}", headers=H, json=body)
        if r.status_code == 429:                 # leaky-bucket limiter
            time.sleep(int(r.headers.get("retry-after", 2)))
            continue
        r.raise_for_status()
        return r.json()

order = post("/orders", {
    "recipient": {"name":"John Smith","address1":"19749 Dearborn St","city":"Chatsworth",
                  "country_code":"US","state_code":"CA","zip":"91311"},
    "order_items": [{
        "quantity":1, "catalog_variant_id":4011, "source":"catalog",
        "placements":[{"placement":"front","technique":"dtg",
                       "layers":[{"type":"file","url":"https://example.com/design.png"}]}]
    }],
})
oid = order["data"]["id"]
# Cost is async — confirm once it's no longer "calculating", else you'll get an error.
post(f"/orders/{oid}/confirm")
```

Gotchas: use `catalog_variant_id` (not product id); don't confirm while cost is `calculating`; a bad file URL/placement pushes the order to `failed`.

### Recipe 2 — Generate a product mockup (async)

Trigger: you want a preview image of a design on a product before listing it.

```bash
curl -X POST https://api.printful.com/v2/mockup-tasks \
  -H "Authorization: Bearer $PRINTFUL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "format":"jpg",
    "products":[{
      "source":"catalog","catalog_product_id":294,
      "mockup_style_ids":[16652],"catalog_variant_ids":[9231],
      "placements":[{"placement":"front","technique":"dtg",
        "layers":[{"type":"file","url":"https://example.com/design.png"}]}]
    }]
  }'
# Then poll GET /v2/mockup-tasks (or listen for the mockup_task_finished webhook).
```

Gotchas: mockup generation is a **task** (status `pending` → `completed`/`failed`); poll the task or subscribe to `mockup_task_finished`. Don't block a request thread waiting.

### Recipe 3 — Listen for shipment, with a polling backup

Trigger: notify your buyer when their order ships.

```python
import hmac, hashlib, requests

def verify(raw_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)   # v2 webhooks are signed — verify it

# Webhook handler: on `shipment_sent`, read tracking and email the buyer.
# BACKUP: webhooks are best-effort. Run a periodic sweep that polls
# GET /v2/orders/{id}/shipments for recently-confirmed orders that
# haven't yet emitted a shipment, so a dropped webhook never loses a notification.
```

Set up the subscription with `POST /v2/webhooks` + `POST /v2/webhooks/events` for `shipment_sent` (HTTPS endpoint required). Gotchas: subscriptions can expire/auto-disable — re-check `GET /v2/webhooks`; always pair with polling.

## Integration patterns

- **Store-fronted (most users):** connect Printful to Shopify/WooCommerce/Etsy in the UI, map SKUs to `sync_variant_id`, and let orders/shipments flow automatically. Failures are almost always SKU mismatches or paused connections.
- **Headless:** create orders directly via `/v2/orders`; handle the async cost-calc → confirm step; reconcile fulfillment via webhooks **plus** a polling sweep.
- **Rate-limit handling:** leaky bucket = the bucket refills gradually, so spread bulk operations rather than bursting; read `X-Ratelimit-Remaining`/`X-Ratelimit-Reset` and back off on `429` using `retry-after`.
- **Versioning:** prefer v2 for new builds (signed webhooks, RFC 9457 `application/problem+json` errors, HATEOAS `_links`). Don't mix v1 and v2 object shapes in one code path.
