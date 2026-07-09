# Squarespace Platform Reference

## Overview

Squarespace is a design-first, all-in-one website builder with a built-in **commerce** layer — online store, memberships, digital downloads, gift cards, donations, subscriptions, and (via the bundled **Acuity Scheduling**) appointment booking. It's aimed at creative professionals and service businesses who want a polished site + store in one place, not a scale-out DTC engine (that's Shopify/BigCommerce). You **don't** automate the site builder (pages/themes are UI-only); you automate the **commerce layer** with the Squarespace **Commerce APIs** (Orders, Inventory, Products, Transactions, Contacts) plus OAuth-gated webhooks. **Not a Merchant of Record** — you own tax (automated US sales tax via TaxJar). For raw endpoints, JSON, and signature code, read `squarespace-api-reference.md`.

## Capabilities & automation surface

| Capability | What it does | Automation |
|---|---|---|
| **Online store / products** | Physical, service, gift-card, download products; variants, images, SKUs | **API-accessible** — Products API v2 (DOWNLOAD readable but not creatable; categories not exposed) |
| **Orders** | One-time + subscription order history; fulfillment | **API + webhook** — Orders API v1.0; `order.create`/`order.update` webhooks |
| **Inventory** | Per-variant stock, tracked vs unlimited | **API-accessible** — Inventory API v1.0 (list/get/adjust) |
| **Transactions** | Payments, refunds, fees, **donations** | **API-accessible** — Transactions API v1.0 (only surface for donation data) |
| **Contacts / customers** | Customers, subscribers, donors, marketing prefs | **API + webhook** — Contacts API; `contact.*`/`address.*` webhooks |
| **Checkout** | Hosted checkout, express/wallet pay, coupons | **UI-configured** — no headless checkout API; conversion levers are plan-gated |
| **Abandoned cart recovery** | Recovery emails | **UI-only**, gated to the top (Advanced) tier |
| **Subscriptions** | Recurring product sales (monthly/biweekly) | Orders flow through the API; setup is UI, gated to higher tier |
| **Memberships / member areas** | Gated paid content | **UI-managed**; member content not a primary API object |
| **Acuity Scheduling** | Appointment booking for service sellers | **Separate Acuity API** (own product, bundled) — not part of Commerce APIs |
| **Site builder (pages/themes/blog)** | Design + content | **UI-only** — no site-builder API |

## Pricing, limits & plan gates

*Best-effort, 2026 — Squarespace has reshuffled plan names/fees recently (legacy "Business / Commerce Basic / Commerce Advanced" vs current "Basic / Core / Plus / Advanced"). Confirm live before quoting.*

| Plan (annual) | ~Price/mo | Commerce transaction fee | Digital-product fee | Notable gates |
|---|---|---|---|---|
| **Basic** | ~$16 | **2%** | 7% | No store-grade commerce; no Commerce API |
| **Core** | ~$23 | **0%** | 5% | Entry commerce plan; Commerce APIs per docs |
| **Plus** | ~$39 | 0% | 1% | Lower processing rate, more selling features |
| **Advanced** | ~$99 | 0% | 0% | **Abandoned-cart recovery, subscriptions, advanced shipping/discounts, Commerce APIs** (some reviews say API is Advanced-only) |

- **Plan gate is the #1 integration trap.** The Commerce APIs require a paid commerce plan — Squarespace's developer docs list **Core/Plus/Advanced/Commerce Advanced**; some third-party reviews say API access is **Advanced ($99/mo) only**. Verify against the target site's plan before building.
- **Rate limits unpublished.** A default `User-Agent` draws stricter limiting — always send a custom UA. Treat `429` as expected; back off with jitter.
- **No multi-currency.** A site sells in a single fixed display currency; the API reflects that one currency. International sellers who need localized pricing must switch platforms or front a converter.
- **Payment gateways are limited:** Squarespace Payments, Stripe, PayPal, plus wallets (Apple Pay, Afterpay/Klarna). Fewer than Shopify/BigCommerce.

## Integrations

- **Reads/writes:** Products, Orders (read + fulfill + import), Inventory (read + adjust), Transactions (read), Contacts (read/write) — all REST/JSON.
- **Push:** OAuth-registered webhooks for `order.*`, `contact.*`, `address.*`, `extension.uninstall`.
- **Native:** Printful (print-on-demand), TaxJar (tax), Xero (accounting), FedEx/USPS/UPS (real-time rates, Advanced), Acuity (scheduling), Tock (reservations), Google, Mailchimp-style marketing via Squarespace Email Campaigns.
- **iPaaS:** Zapier and Make have Squarespace apps (new-order/new-form-submission triggers) — useful when you don't want to host a webhook listener or you're below the API-eligible plan.

## Data model

Money is a `{currency, value}` object (decimal, **not** integer cents — unlike Square/Sellfy).

**Order** (abridged — full schema in the API reference):
```json
{
  "id": "585d498fdee9f31a60284a37",
  "orderNumber": "3",
  "modifiedOn": "2016-12-23T15:58:07.187Z",
  "channel": "web",
  "testmode": true,
  "customerEmail": "customer@example.com",
  "fulfillmentStatus": "PENDING",
  "paymentState": "PAID",
  "priceTaxInterpretation": "EXCLUSIVE",
  "lineItems": [
    { "productId": "565c...", "variantId": "88c1...", "sku": "SQ3381024",
      "quantity": 1, "unitPricePaid": { "currency": "USD", "value": 49.99 } }
  ],
  "grandTotal": { "currency": "USD", "value": 49.99 }
}
```

**Inventory item:**
```json
{ "variantId": "88c1...", "sku": "SQ3381024", "descriptor": "Spring Mix - Large", "isUnlimited": false, "quantity": 42 }
```

**Webhook notification** (thin — carries a pointer, not the object):
```json
{ "id": "5c2b...", "websiteId": "5f3c...", "subscriptionId": "5f3c...",
  "topic": "order.create", "createdOn": "2020-04-22T22:18+00:00",
  "data": { "orderId": "585d498fdee9f31a60284a37", "update": "CREATED" } }
```

**IDs & query patterns:** orders are listed by `modifiedOn` (≤50/page); page with `cursor`. To pull a date window, first call uses paired `modifiedAfter`+`modifiedBefore`, later calls use only `cursor`. Line items reference `productId` + `variantId`; inventory is keyed by `variantId`.

## Quick-start recipes

### Recipe 1 — Sync every new order into a CRM/warehouse (webhook + follow-up GET)

Trigger: a sale happens → `order.create`. Steps: register an OAuth webhook, verify the HMAC, GET the full order, upsert to your system.

```bash
# 1) Subscribe (OAuth token required — API keys can't subscribe)
curl -X POST "https://api.squarespace.com/1.0/webhook_subscriptions" \
  -H "Authorization: Bearer $OAUTH_TOKEN" \
  -H "User-Agent: crm-sync/1.0" -H "Content-Type: application/json" \
  -d '{"endpointUrl":"https://example.com/sqsp/webhook","topics":["order.create","order.update"]}'
# response includes a one-time hex `secret` — store it
```

```python
# 2) Listener (Flask): verify signature on the RAW body, then GET the order
import hashlib, hmac, os, requests
from flask import Flask, request, abort
app = Flask(__name__)
SECRET_HEX = os.environ["SQSP_WEBHOOK_SECRET"]
API_KEY    = os.environ["SQSP_API_KEY"]  # or an OAuth token

@app.post("/sqsp/webhook")
def hook():
    raw = request.get_data()  # raw bytes — do NOT use request.json here
    sig = request.headers.get("Squarespace-Signature", "")
    expected = hmac.new(bytes.fromhex(SECRET_HEX), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        abort(401)
    event = request.get_json()
    if event["topic"] == "order.create":
        order_id = event["data"]["orderId"]
        order = requests.get(
            f"https://api.squarespace.com/1.0/commerce/orders/{order_id}",
            headers={"Authorization": f"Bearer {API_KEY}", "User-Agent": "crm-sync/1.0"},
        ).json()
        upsert_to_crm(order)        # your code; dedupe on order["id"]
    return "", 204
```

Gotchas: hash the **raw** body; decode the hex secret to bytes; return 2xx fast; dedupe on `order.id` (retries/duplicates happen); `data` is a pointer, not the order.

### Recipe 2 — Nightly order export by date window (polling, works with just an API key)

Trigger: scheduled job. Use when you're below the webhook-eligible setup or want a backfill.

```python
import requests
H = {"Authorization": "Bearer YOUR_API_KEY", "User-Agent": "order-export/1.0"}
params = {"modifiedAfter": "2026-06-28T00:00:00Z",
          "modifiedBefore": "2026-06-29T00:00:00Z"}  # paired; required together
url = "https://api.squarespace.com/1.0/commerce/orders"
orders = []
while True:
    r = requests.get(url, headers=H, params=params).json()
    orders += r["result"]
    if not r["pagination"]["hasNextPage"]:
        break
    params = {"cursor": r["pagination"]["nextPageCursor"]}  # cursor replaces the date filter
print(len(orders), "orders")
```

Gotcha: `modifiedAfter`/`modifiedBefore` must be sent together and **cannot** be combined with `cursor` — switch to cursor-only after the first page.

### Recipe 3 — Adjust stock from an external system (prevent overselling)

Trigger: stock changes in your warehouse/ERP. Keep Squarespace counts in sync.

```bash
curl -X POST "https://api.squarespace.com/1.0/commerce/inventory/adjustments" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "User-Agent: inv-sync/1.0" -H "Content-Type: application/json" \
  -d '{"setFiniteOperations":[{"variantId":"88c16ee4-547b-445e-a392-bded9991ae30","quantity":100}]}'
```

Gotcha: drive stock from the Inventory API as source of truth; an `isUnlimited` variant won't decrement.

## Integration patterns

- **CRM sync:** key on `order.id`; map `customerEmail`/`customerId` to your contact, `lineItems[].sku`/`productId` to products. Convert the `{currency,value}` money objects to your schema. Use webhooks for real-time + a nightly date-window poll for reconciliation (belt and suspenders, since payloads are thin and retries duplicate).
- **Webhook listener:** OAuth subscription; verify `Squarespace-Signature` (HMAC-SHA256 over raw body, hex→bytes secret, constant-time compare); 2xx fast; idempotent upsert; rotate the secret if leaked.
- **Batch pipeline:** cursor pagination, ≤50 orders/page ordered by `modifiedOn`; honor `429` with backoff + jitter (limits unpublished); always send a custom `User-Agent`.
- **Tax/MoR:** Squarespace is not a Merchant of Record — automate US tax via TaxJar/native auto-calc; for global VAT/GST remittance handled-for-you, front the sale with a MoR (see `/sales-merchant-of-record`).
