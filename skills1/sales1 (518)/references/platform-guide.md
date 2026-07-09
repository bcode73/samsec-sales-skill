# SendOwl Platform Reference

## Overview

SendOwl is a digital-commerce platform for solopreneurs and small businesses to sell and **securely deliver** digital goods directly to buyers — "no marketplace, no middleman." Its differentiator is delivery security (expiring/limited download links, PDF stamping, license keys) rather than storefront design. Sellers have processed over $2B in sales. It is **not** a merchant of record — you own VAT/GST/sales tax.

## Capabilities & automation surface

| Capability | What it does | Automation |
|-----------|--------------|-----------|
| Products (digital, service, physical) | Sell downloads, streamed audio/video, software, courses, coaching | **API-accessible** (`/products` CRUD + `issue`) |
| Secure delivery | Download-limit + link-expiry per product; automated delivery emails | Configured per product (UI); reset via `PUT /orders/{id}/download_restrictions` |
| PDF stamping | Embeds buyer name into delivered PDFs to deter sharing | `pdf_stamping` flag on product (**API-visible**) |
| License keys | Upload a key pool; issue one per sale; validate keys | **API-accessible** (`/products/{id}/licenses`, `check_valid`) |
| Subscriptions | Recurring billing (trial + recurring price/frequency), access control | **API-accessible** (`/subscriptions` CRUD + `issue`); order-level cancel |
| Drip content | Release course modules on a schedule | **API-accessible** (drip items resource) |
| Bundles | Group products into a discounted package | **API-accessible** (bundles resource) |
| Discounts / promo codes | Percentage/fixed codes, affiliate-scoped | **API-accessible** (`/discounts`) |
| Upsells | Post-purchase / cart upsell offers | UI-configured |
| Affiliate program | Referral tracking, per-affiliate commissions | Order `referred_by` filter (**API-visible**) |
| Orders | Buyer, cart, transactions, refunds, access control | **API + webhook-accessible** |
| Analytics | Sales reports | UI (export orders via API for custom reporting) |

**Payments**: processed through Stripe, PayPal, or Square — SendOwl is the cart/delivery layer, not the processor.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — verify against the live pricing page; SendOwl has changed pricing models and reviewers report abrupt increases.*

| Plan | Price (annual) | Orders/yr | Sales/yr | Bandwidth/mo |
|------|----------------|-----------|----------|--------------|
| Launch | $39/mo ($32.50 annual) | 5,000 | $10,000 | 10 GB |
| Grow | $87/mo ($72.50 annual) | 25,000 | $36,000 | 20 GB |
| Scale | $159/mo ($132.50 annual) | 50,000 | $100,000 | 50 GB |
| Business | from $299/mo | higher | up to $200k+ | higher |

- **No free tier** (free trial only, with some limits lifted on support request).
- **No per-transaction fees** — SendOwl charges only the monthly subscription; the payment processor (Stripe/PayPal/Square) still takes its cut.
- **All features on every plan** — API access, subscriptions, PDF stamping, license keys, upsells, affiliates, analytics are **not** plan-gated. Your integration won't break on the cheapest plan.
- **Bandwidth overage**: ~$1 per GB over the monthly allotment.
- **Caps are on volume, not features** — crossing an orders/year or sales/year cap forces an upgrade. Model expected annual volume.
- **File hosting is limited** — SendOwl stores download *links* (historically ~250 files), not an unlimited file host. Host large media externally and deliver the link.

## Integrations

- **Payment processors**: Stripe, PayPal, Square (reads authorized payments, issues refunds).
- **Shopify**: SendOwl app delivers digital goods for Shopify orders; look up by variant via `GET /products/shopify_lookup?variant_id=`.
- **Webhooks (outbound)**: SendOwl → your endpoint on order/subscription state changes (see below). Bidirectional in effect: webhook notifies, then you read/write via the API.
- **iPaaS**: Zapier (new-order triggers, actions) and Zapier-managed webhooks. Zapier-created webhooks are removed by deleting the Zap.
- **Custom**: REST API (Basic Auth) for full catalog/order/license/subscription management. Code samples on `github.com/SendOwl`.

## Data model

Money is returned as a **string with currency symbol** in some payloads (e.g. `"£15.00"`) and as a numeric in others (e.g. product `price: 17`) — normalize per endpoint. IDs are integers.

**Product** (`GET /api/v1/products/{id}`):
```json
{
  "product": {
    "id": 1,
    "name": "Curing RSI:Beta (first version)",
    "product_type": "digital",
    "price": 17,
    "currency_code": "USD",
    "created_at": "2010-08-30T16:53:10Z",
    "updated_at": "2011-05-28T14:08:20Z",
    "instant_buy_url": "https://www.sendowl.com/products/1/X4J5B018/purchase",
    "add_to_cart_url": "https://www.sendowl.com/products/1/X4J5B018/add_to_cart",
    "pdf_stamping": true,
    "price_is_minimum": false,
    "attachment": { "filename": "cure-rsi.pdf", "size": 1087311 },
    "drip_items": []
  }
}
```

**Order** (`GET /api/v1_3/orders/{id}`):
```json
{
  "order": {
    "id": 3101,
    "state": "complete",
    "gateway": "PayPal",
    "buyer_email": "testuser@gmail.com",
    "buyer_name": "Test User",
    "settled_currency": "GBP",
    "settled_gross": "64.90",
    "settled_tax": "5.90",
    "refunded": false,
    "created_at": "2011-05-17T06:05:56Z",
    "updated_at": "2011-05-17T06:15:13Z"
  }
}
```

**License** (`GET /api/v1/products/{product_id}/licenses`):
```json
{
  "license": {
    "id": 42,
    "key": "AY3C-7C9E-BC3E-J2MA",
    "order_id": 3101,
    "order_refunded": false,
    "product_id": 1
  }
}
```

**Webhook order payload** (raw JSON POST body — see api-reference for the full shape):
```json
{
  "order": {
    "id": "0000123456",
    "state": "complete",
    "buyer_name": "Mr Buyer",
    "buyer_email": "mrbuyer@gmail.com",
    "buyer_country": "GB",
    "price_at_checkout": "£15.00",
    "cart": { "cart_items": [ { "product": { "id": 2811, "name": "My Product", "product_type": "digital" }, "quantity": 1, "tax_rate": 20.0 } ] },
    "transactions": [ { "gateway_transaction_id": "ch_fake001", "payment_gross": "£18.00", "payment_tax": "£3.00" } ]
  }
}
```

## Quick-start recipes

### Recipe 1 — List your products (auth smoke test)

Trigger: confirm credentials and see catalog. Auth = API key:secret via Basic Auth (Settings → SendOwl API).

```bash
curl -H "Accept: application/json" \
  "https://KEY:SECRET@api.sendowl.com/api/v1/products?per_page=50&page=1"
```

```python
import requests
from requests.auth import HTTPBasicAuth

r = requests.get(
    "https://api.sendowl.com/api/v1/products",
    auth=HTTPBasicAuth(API_KEY, API_SECRET),
    headers={"Accept": "application/json"},
    params={"per_page": 50, "page": 1},
)
r.raise_for_status()
products = r.json()
```

Gotchas: default page size is 10, max 50. Stay ≤1 request/second. Orders use `/api/v1_3/`, not `/api/v1/`.

### Recipe 2 — Verify & handle the `order_completed` webhook (order → CRM)

Trigger: a sale completes; push the buyer to your CRM. Verify HMAC over the **raw** body, then act idempotently.

```python
import hmac, hashlib, base64
from flask import Flask, request, abort

app = Flask(__name__)
SIGNING_KEY = b"YOUR_SIGNING_KEY_SECRET"  # from the SendOwl API settings page

@app.post("/sendowl/webhook")
def sendowl_webhook():
    raw = request.get_data()  # RAW body — do not use request.json here
    sig = request.headers.get("X-SENDOWL-HMAC-SHA256", "")
    expected = base64.b64encode(hmac.new(SIGNING_KEY, raw, hashlib.sha256).digest()).decode().strip()
    if not hmac.compare_digest(expected, sig):
        abort(401)

    event = request.headers.get("X-SENDOWL-EVENT")   # e.g. "order_completed"
    order = request.get_json()["order"]              # state is in the body
    if event == "order_completed":
        upsert_crm_contact(order["buyer_email"], order["buyer_name"], order_id=order["id"])
    return "", 200
```

Gotchas: retries send duplicates → dedupe on `order.id`. The event is in the header; the order's state at trigger time is in the body. In Rails the header is `HTTP_X_SENDOWL_HMAC_SHA256` and the raw body is `request.raw_post`.

### Recipe 3 — Issue a software license on a sale (server-side validation)

Trigger: sell software with keys. Upload a key pool, let SendOwl assign one per order, and validate server-side.

```bash
# Upload a batch of keys to a product's pool
curl -X POST "https://KEY:SECRET@api.sendowl.com/api/v1/products/1/licenses" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"licenses":["AY3C-7C9E-BC3E-J2MA","AY3C-7C9E-BC3E-J2MB"]}'

# Validate a key server-side (never from shipped client code)
curl "https://KEY:SECRET@api.sendowl.com/api/v1/products/1/licenses/check_valid?key=AY3C-7C9E-BC3E-J2MA"
```

Gotchas: the create response lists `invalid-keys` (duplicates that were rejected). **Never embed `check_valid` in distributed software** — it would expose your credentials; proxy it through your own server.

## Integration patterns

- **CRM sync architecture**: use webhooks as the primary trigger (`order_completed`, `refund_issued`, `subscription_active`/`_cancelled`), map `buyer_email` as the identity key, and reconcile nightly with `GET /api/v1_3/orders?updated_after={ISO8601}`. On refund, revoke access with `DELETE /api/v1_3/orders/{id}/access`.
- **Webhook listener**: HTTPS endpoint returning 2XX/3XX fast; verify HMAC over raw body; enqueue work (SendOwl retries 10× with exponential backoff, so slow handlers get duplicate deliveries). Idempotency key = `order.id` + event.
- **Batch/export pipeline**: page with `per_page=50`, filter with `from`/`to`/`updated_after`/`state`/`orderable`/`referred_by`, throttle ≤1 req/sec, and store a high-water `updated_at` cursor for incremental pulls.
- **Access control off purchase**: for true gating (vs shareable links), don't rely on the download URL — grant entitlement in your app on `order_completed` and revoke on `refund_issued`/`subscription_cancelled`.
