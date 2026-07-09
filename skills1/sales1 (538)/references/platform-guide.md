# Snipcart Platform Reference

## Overview

Snipcart is a developer-first embeddable cart: drop a JS snippet on any site, mark up buy buttons with `data-item-*` HTML attributes, and Snipcart injects the cart and checkout overlay. Built for static/JAMstack/custom stacks (Hugo, Gatsby, Next.js, Astro, WordPress, Laravel) where a full store platform is overkill. Pricing is usage-based (2% of sales, or a flat monthly fee at low volume). Its distinctive mechanic — and #1 support topic — is **price validation by crawling your product URLs**.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Cart & checkout overlay | Injected UI on your site; theming/customization | **UI/HTML-defined**; JavaScript SDK for events + programmatic control |
| Products | Defined via `data-item-*` attributes (or JSON crawling endpoint); catalog mirrored in dashboard | **API-accessible** (read, stock updates) + crawler-validated |
| Orders | Status, tracking, notifications, digital-goods delivery | **API-accessible** + **webhook-accessible** (`order.completed`, …) |
| Customers | Accounts, dashboard, sessions | **API-accessible** |
| Discounts | Coupons with trigger types | **API-accessible** |
| Refunds | Full/partial | **API-accessible** |
| Abandoned carts | Recovery emails, list via API | **API-accessible** + dashboard |
| Subscriptions | Recurring products | HTML-defined + webhook events |
| Custom shipping/taxes | Your endpoint returns rates/taxes during checkout | **Webhook-accessible** (synchronous callbacks) |
| **MCP Server (official, hosted)** | 38 tools: orders, customers, products/stock, discounts, refunds, abandoned carts, shipping, domains | **MCP-accessible** — `snipcart-mcp.azurewebsites.net`, `X-Snipcart-Api-Key` header; Claude Code/Desktop, Cursor, Windsurf |

## Pricing, limits & plan gates

*Best-effort (2026-07) — verify at snipcart.com/pricing.*

- **2% per transaction** + payment-gateway fees (Stripe/PayPal/etc.), OR
- **$20/mo flat** when monthly sales are under $1,000 (i.e. the minimum you'll pay is $20 in months you sell < $1k).
- Free forever in Test mode (full integration development without charges); no setup fees; no product caps or plan tiers — every feature on the single plan.

Break-even intuition: 2% of $1,000 = $20, so the fee is effectively `max($20, 2% of sales)`. At $10k/mo you pay $200 — compare against flat-fee carts (ThriveCart/SamCart) at volume.

## Integrations

Framework-agnostic: official guides for Hugo, Gatsby, Next.js, Nuxt, React, Vue, Svelte, Angular, WordPress, Laravel. Payment gateways: Stripe, PayPal, and others per region. Affiliate tracking via third-party (Rewardful, iDevAffiliate). Data flows: products IN from your HTML/JSON (crawler), orders OUT via API + webhooks; shipping/tax callbacks are synchronous during checkout.

## Data model

Products live **in your markup**; Snipcart's backend records what was sold. Order tokens (GUIDs) key the API.

```html
<!-- A product IS this markup; all four data attributes are mandatory -->
<button class="snipcart-add-item"
  data-item-id="tee-001"
  data-item-price="25.00"
  data-item-name="Classic Tee"
  data-item-url="/products/tee-001"
  data-item-description="Heavy cotton tee">
  Add to cart
</button>
```

```json
// Webhook body shape
{ "eventName": "order.completed", "mode": "Live", "createdOn": "…", "content": { "token": "…", "email": "…", "items": [] } }

// Order (representative core fields)
{ "token": "22a1…-guid", "email": "buyer@example.com", "status": "Processed",
  "grandTotal": 27.5, "items": [{ "id": "tee-001", "price": 25.0, "quantity": 1 }] }
```
<!-- Webhook/order shapes constructed from docs descriptions — verify against live API -->

## Quick-start recipes

### Recipe 1 — Verify a webhook, then act on the order (Python/Flask)

Snipcart webhooks aren't HMAC-signed — you verify by **calling Snipcart back** with the request token:

```python
import os, requests
from flask import Flask, request, abort

app = Flask(__name__)
KEY = os.environ["SNIPCART_SECRET_KEY"]

@app.post("/hooks/snipcart")
def snipcart_hook():
    token = request.headers.get("X-Snipcart-RequestToken", "")
    ok = requests.get(f"https://app.snipcart.com/api/requestvalidation/{token}",
                      auth=(KEY, ""))            # key as username, empty password
    if ok.status_code != 200:
        abort(401)                                # not a genuine Snipcart request
    event = request.get_json(force=True)
    if event.get("eventName") == "order.completed":
        order_token = event["content"]["token"]
        # fulfill / sync to CRM using event content, or re-fetch:
        # requests.get(f"https://app.snipcart.com/api/orders/{order_token}", auth=(KEY, ""))
    return "", 200
```

Gotchas: the request token expires in ~1 hour; no automatic retries are documented — use the dashboard's request history ("Send this hook again") for redelivery and a `GET /api/orders` reconciliation poll.

### Recipe 2 — Pull recent orders (cURL + Python)

```bash
curl "https://app.snipcart.com/api/orders?limit=50&offset=0" \
  -H "Accept: application/json" \
  -u $SNIPCART_SECRET_KEY:
```

```python
import os, requests
auth = (os.environ["SNIPCART_SECRET_KEY"], "")
offset, total = 0, 1
while offset < total:
    r = requests.get("https://app.snipcart.com/api/orders",
                     params={"limit": 50, "offset": offset}, auth=auth)
    r.raise_for_status()
    body = r.json()
    for order in body.get("items", []):
        pass  # upsert into warehouse/CRM
    total = body.get("totalItems", 0)
    offset += 50
```

Gotchas: Basic auth = key as **username** with empty password (not a Bearer header); Test-mode keys only see Test data.

### Recipe 3 — Fix `product-crawling-failed` on a JS-rendered site

When products live on SPA/headless-CMS pages the crawler can't render, serve a **JSON crawling endpoint** and point `data-item-url` at it:

```json
// GET /products.json  (static file or serverless function)
[
  { "id": "tee-001", "price": 25.00, "url": "/products.json" },
  { "id": "mug-001", "price": 14.00, "url": "/products.json" }
]
```

```html
<button class="snipcart-add-item" data-item-id="tee-001"
        data-item-price="25.00" data-item-name="Classic Tee"
        data-item-url="/products.json">Add to cart</button>
```

Gotchas: the crawler must fetch the URL server-side — no client-rendered attributes; the domain must be in your allowed-domains list; price in the JSON must exactly match `data-item-price`; don't mutate `data-item-*` with JS after render.

## Integration patterns

- **Static-site commerce**: products in markdown/front-matter → build emits `data-item-*` buttons + a `products.json` crawling endpoint → webhooks drive fulfillment. No server needed except the webhook receiver (a serverless function works).
- **AI-operated store**: connect Claude Code/Cursor to the official MCP server (`snipcart-mcp.azurewebsites.net`, `X-Snipcart-Api-Key` header) for conversational order management, stock updates, discount creation — the REST API remains the programmatic path for pipelines.
- **Fulfillment/CRM sync**: `order.completed` webhook (token-validated) for freshness + paginated `GET /api/orders` reconciliation as source of truth.
- **Custom shipping/taxes**: synchronous webhook endpoints must respond fast during checkout — timeouts break the buyer's checkout, so precompute rates where possible.
