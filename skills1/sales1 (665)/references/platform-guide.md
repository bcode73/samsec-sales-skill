# WooCommerce Platform Reference

## Overview

WooCommerce is the open-source (GPL) commerce plugin for WordPress — you install it on your own
WordPress host, so you own the code, the database, and the customer relationship, and pay **no
platform transaction fee**. It's the most-installed cart on the web. Its differentiator versus
hosted SaaS (Shopify/BigCommerce) is total ownership and an enormous extension ecosystem; the
tradeoff is that *you* run the server, so most integration friction is host/auth config rather than
a vendor limit. Two APIs matter: the **REST API v3** (`/wp-json/wc/v3`) for back-office data, and
the **Store API** (`/wp-json/wc/store/v1`) for headless buyer-facing cart/checkout.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Products | Physical, digital/downloadable, variable (variations), grouped, external | REST CRUD (`/products`, `/products/{id}/variations`), batch, webhook (`product.*`) |
| Product categories / attributes / tags | Catalog taxonomy | REST CRUD (`/products/categories`, `/products/attributes`) |
| Orders | Full order lifecycle, statuses, line items | REST CRUD (`/orders`), notes (`/orders/{id}/notes`), refunds (`/orders/{id}/refunds`), webhook (`order.*`) |
| Customers | Accounts, billing/shipping, order history | REST CRUD (`/customers`), downloads (`/customers/{id}/downloads`), webhook (`customer.*`) |
| Coupons | Fixed/percent discounts, usage restrictions | REST CRUD (`/coupons`), webhook (`coupon.*`) |
| Reports | Sales, top sellers, totals | REST read (`/reports/...`) |
| Tax rates & classes | Tax configuration | REST CRUD (`/taxes`, `/taxes/classes`) — you remit; not a MoR |
| Shipping zones / methods | Rates by region | REST CRUD (`/shipping/zones`, `/shipping/methods`) |
| Payment gateways | Enabled processors & settings | REST read/update (`/payment_gateways`) — UI to add gateways |
| Settings & System Status | Store config, diagnostics | REST (`/settings`, `/system_status`) |
| Webhooks | Event push to your endpoint | REST CRUD (`/webhooks`) or wp-admin UI |
| Headless cart & checkout | Buyer-facing cart, add-to-cart, checkout | **Store API** `/wc/store/v1` (Nonce + Cart-Token, no consumer key) |
| Extensions (subscriptions, bookings, memberships) | Woo Marketplace add-ons | Each extension may add its own REST routes; verify per-extension |

**wp-admin-only (no first-class REST):** theme/checkout-page layout, most extension configuration
screens, and email template editing. Automate data, not presentation.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — verify at woocommerce.com/pricing.*

- **Core plugin: free** (GPL, self-hosted). No license fee, no platform transaction fee.
- **Real cost is the total, not the plugin.** A production store typically pays for:
  - **Hosting** — from ~shared to managed WordPress; this is the biggest driver of API/checkout speed.
  - **Extensions** — roughly per-extension, per-year (subscriptions, advanced shipping, bookings, etc.).
  - **Theme** — free or a one-time/annual premium theme.
  - **Payment processing** — e.g. WooPayments/Stripe ~2.9% + 30¢ (US cards); varies by gateway/region.
- **Woo Express** is the hosted option (WordPress.com-managed) if the user doesn't want to self-host —
  presented as monthly tiers; still WooCommerce under the hood.
- **API rate limits:** none imposed by WooCommerce core — the ceiling is your host/DB. Batch endpoints
  cap at ~100 items per call; `per_page` caps at 100. Throttle bulk jobs yourself.
- **Not a Merchant of Record:** the store owner is the seller of record and owns VAT/GST/sales tax.

## Integrations

- **Direction:** REST API is **bidirectional** (read + write) for products/orders/customers/coupons;
  webhooks are **outbound** (WooCommerce → your endpoint) on create/update/delete events.
- **CRM/warehouse:** no native CRM; sync via REST + webhooks, or connectors (Zapier, Make, n8n all
  have WooCommerce triggers like "New Order" and actions like "Create Product/Coupon").
- **Payments:** 140+ gateways (WooPayments, Stripe, PayPal, Square, Amazon Pay, regional).
- **Marketing:** Google Shopping, Meta, Mailchimp, Klaviyo, Google Analytics via extensions.
- **Headless/JAMstack:** Store API for the cart/checkout; v3 API + WPGraphQL (WooGraphQL) for content.

## Data model

Resource IDs are integers. Monetary values are **strings with two decimals**. Dates are ISO8601.
Custom/plugin fields live in a `meta_data` array, not as top-level keys.

**Order (trimmed):**
```json
{
  "id": 727,
  "number": "727",
  "status": "processing",
  "currency": "USD",
  "date_created": "2026-07-04T14:22:07",
  "total": "29.99",
  "customer_id": 12,
  "billing": { "first_name": "Ada", "email": "ada@example.com", "country": "US" },
  "shipping": { "first_name": "Ada", "country": "US" },
  "payment_method": "woocommerce_payments",
  "line_items": [
    { "id": 315, "name": "Pro License", "product_id": 93, "quantity": 1, "total": "29.99" }
  ],
  "meta_data": [ { "id": 4021, "key": "_utm_source", "value": "newsletter" } ]
}
```
<!-- Constructed from documented field lists — verify against live API -->

**Product (trimmed):**
```json
{
  "id": 93,
  "name": "Pro License",
  "slug": "pro-license",
  "type": "simple",
  "status": "publish",
  "price": "29.99",
  "regular_price": "29.99",
  "sale_price": "",
  "virtual": true,
  "downloadable": true,
  "categories": [ { "id": 9, "name": "Software" } ],
  "images": [ { "id": 200, "src": "https://.../pro.png" } ],
  "meta_data": []
}
```
<!-- Constructed from documented field lists — verify against live API -->

## Quick-start recipes

### Recipe 1 — Authenticated REST call (list recent orders)
Trigger: pull orders into a script/warehouse. Steps: generate a read key in
WooCommerce → Settings → Advanced → REST API; call over HTTPS with Basic auth.

```bash
# cURL — Basic auth over HTTPS (max 100 per page)
curl -s "https://store.example.com/wp-json/wc/v3/orders?per_page=100&page=1&status=processing" \
  -u "ck_live_xxx:cs_live_yyy"
# Total pages come back in response headers, not the body:
#   X-WP-Total, X-WP-TotalPages
```
```python
import requests
BASE = "https://store.example.com/wp-json/wc/v3"
AUTH = ("ck_live_xxx", "cs_live_yyy")

def all_orders(status="processing"):
    page, out = 1, []
    while True:
        r = requests.get(f"{BASE}/orders",
                         params={"per_page": 100, "page": page, "status": status},
                         auth=AUTH, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        out += batch
        if page >= int(r.headers.get("X-WP-TotalPages", 1)):
            break
        page += 1
    return out
```
Gotcha: if this 401s, the host is likely stripping the `Authorization` header — retry with
`params={"consumer_key": ..., "consumer_secret": ...}` (HTTPS only) or add the rewrite rule.

### Recipe 2 — Verify an order webhook (signature + re-fetch)
Trigger: react to new orders reliably. Steps: create a webhook (topic `order.created`,
delivery URL = your tokenized HTTPS endpoint, a secret you control), then verify every delivery.

```python
import base64, hashlib, hmac, requests
from flask import Flask, request, abort

app = Flask(__name__)
SECRET = b"your_webhook_secret"            # defaults to the API user's consumer secret if unset
BASE, AUTH = "https://store.example.com/wp-json/wc/v3", ("ck_live_xxx", "cs_live_yyy")

@app.post("/woo/orders")                    # keep this URL unguessable/tokenized
def orders():
    body = request.get_data()               # RAW bytes — hash before any parsing
    expected = base64.b64encode(hmac.new(SECRET, body, hashlib.sha256).digest()).decode()
    if not hmac.compare_digest(expected, request.headers.get("X-WC-Webhook-Signature", "")):
        abort(401)
    order_id = request.get_json().get("id")
    # Re-fetch the source of truth before provisioning/charging; dedupe on order_id.
    order = requests.get(f"{BASE}/orders/{order_id}", auth=AUTH, timeout=30).json()
    if order["status"] in ("processing", "completed"):
        provision(order)                    # your idempotent handler
    return "", 200                          # return fast 2xx or the webhook gets marked failed
```
Gotcha: WooCommerce **disables the webhook after 5 consecutive failed deliveries** — a slow or
non-2xx endpoint, or a security plugin blocking unauthenticated REST, will silently kill it.

### Recipe 3 — Bulk-create products with the batch endpoint
Trigger: import a catalog without one-request-per-row timeouts. Steps: chunk into ≤100 and POST to `/products/batch`.

```python
import requests
BASE, AUTH = "https://store.example.com/wp-json/wc/v3", ("ck_live_xxx", "cs_live_yyy")

def chunk(rows, n=100):
    for i in range(0, len(rows), n):
        yield rows[i:i+n]

def import_products(rows):                  # rows: list of product dicts
    for batch in chunk(rows, 100):          # batch endpoint caps ~100 items/call
        payload = {"create": [
            {"name": p["name"], "type": "simple", "regular_price": str(p["price"]),  # money as STRING
             "meta_data": [{"key": "_sku_source", "value": p.get("sku", "")}]}
            for p in batch
        ]}
        r = requests.post(f"{BASE}/products/batch", json=payload, auth=AUTH, timeout=60)
        r.raise_for_status()
        # throttle — the ceiling is the host/DB, not a vendor limit
```

## Integration patterns

- **CRM/warehouse sync:** webhooks for low-latency reaction + a nightly `per_page=100` paginated pull
  (`GET /orders?after=<iso8601>`) for reconciliation. Never trust a webhook alone — deliveries can be
  blocked by a security plugin or dropped when the webhook auto-disables. Dedupe on resource `id`.
- **Webhook listener:** register one webhook per topic (`order.created`, `order.updated`,
  `product.updated`, …) to a tokenized HTTPS URL; verify `X-WC-Webhook-Signature`
  (base64 HMAC-SHA256 of the raw body) with the stored secret; return a fast `2xx`; watch the
  per-webhook delivery log and re-enable if it flips to disabled.
- **Batch/ETL:** page with `page`/`per_page` (max 100), stop on empty page or when
  `page >= X-WP-TotalPages`; write with `/batch` (`create`/`update`/`delete`, ≤100 items). Add a
  `modified_after`/`after` filter to pull only deltas. Self-throttle — you're hitting your own DB.
- **Headless storefront:** buyer flow (cart, add item, apply coupon, checkout) → **Store API**
  `/wc/store/v1` with `Nonce` + `Cart-Token` headers (no consumer key). Admin/content → v3 API +
  optionally WPGraphQL/WooGraphQL. Don't put consumer keys in the browser.
