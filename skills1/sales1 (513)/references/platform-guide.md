# Sellfy Platform Reference

## Overview

Sellfy (sellfy.com) is an all-in-one **online store builder made for creators** — sell digital products, print-on-demand merch, physical goods, and subscriptions from a hosted storefront or via embeddable buy buttons. Its pitch is simplicity plus **0% Sellfy transaction fees** on every plan. Best fit: solo creators and small brands who want a fast, no-code store; weak fit: developers needing a programmable commerce backend (no public REST CRUD API) or sellers needing global tax handled (not a Merchant of Record).

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Digital products** | Sell ebooks, music, video, design files, code; auto-delivered via unique download links; **PDF stamping** + **download limits** | UI-only to manage; purchase fires **New Order webhook** |
| **Print-on-demand (POD)** | T-shirts, mugs, hoodies etc.; 11 fulfillment centers; design uploads | UI-only; sale fires New Order webhook |
| **Physical products** | Ship your own inventory (no native multi-warehouse) | UI-only; New Order webhook |
| **Subscriptions** | Recurring digital products (weekly/monthly/yearly) | **Subscription Product Bought / Canceled** webhooks |
| **Store builder** | Drag-and-drop, ~10 themes, custom domain (all tiers) | UI-only |
| **Embed / buy buttons** | Embed products, cart, or buy buttons on any site; "Sell Downloads" app on Wix | UI-generated embed code |
| **Cart & checkout** | Express checkout, Stripe/PayPal/Apple Pay/Google Pay | **Cart Abandoned webhook** (when buyer consents to email but doesn't finish) |
| **Email marketing** | Built-in campaigns + automation; credits per tier | UI; **Email Subscribe / Unsubscribe webhooks** |
| **Upselling** | Product upsell offers (Business+) | UI-only |
| **Cart abandonment** | Recovery emails (Business+) | Cart Abandoned webhook |
| **Affiliate marketing** | Run your own product affiliate program (Business+) | UI-only |
| **Coupons / discounts** | Discount codes (all tiers) | reflected in New Order `discount` fields |
| **Contact form** | Store contact form | **Contact Form Submitted webhook** |
| **Analytics & pixels** | Google Analytics, Facebook/Twitter Ads pixels, Google Merchant Center | UI tag insertion |

**Developer reality:** there is **no public REST API** for creating/reading products, orders, or customers. The only programmatic surfaces are **outbound webhooks** and the **Zapier API token**. Treat Sellfy as a source of *events*, not a queryable backend.

## Pricing, limits & plan gates

*(Best-effort from 2026-06 research — verify against the live pricing page.)*

| | Starter | Business | Premium |
|---|---|---|---|
| Price (annual) | **$22/mo** | **$59/mo** | **$119/mo** |
| Price (monthly) | $29/mo | $79/mo | $159/mo |
| **Annual sales cap** | **up to ~$10k** | **up to ~$50k** | **up to ~$200k** |
| Sellfy transaction fee | 0% | 0% | 0% |
| Max file size / product | 10 GB | 15 GB | 20 GB |
| Products | Unlimited | Unlimited | Unlimited |
| Email credits / mo | 2,000 | 10,000 | 50,000 |
| Custom domain | ✓ | ✓ | ✓ |
| Coupons, reviews, email marketing | ✓ | ✓ | ✓ |
| **Upselling, cart abandonment, affiliate marketing, custom fields, remove branding, store-design migration** | — | ✓ | ✓ |
| **Product migration, priority support** | — | — | ✓ |

- **The cap, not the fee, drives upgrades.** Cross a tier's rolling-12-month revenue cap and Sellfy prompts an upgrade. Model expected annual revenue first, gated features second.
- **0% is the Sellfy fee only.** Payment processors (Stripe/PayPal) still charge ~2.9% + 30¢.
- **Webhooks/Zapier are not plan-gated** in the docs (confirm in-account), but the *features that emit some events* (cart abandonment, affiliates) are Business+.

## Integrations

- **Payments (inbound):** Stripe, PayPal, Apple Pay, Google Pay. No proprietary gateway.
- **Webhooks (outbound, real-time):** 7 event types POST JSON to your URL. See `sellfy-api-reference.md`.
- **Zapier (bidirectional via no-code):** authenticate with a Sellfy **API token**; triggers are payment-based (Completed payment, Refunds, Reversed payments, or all). Actions are whatever the 5,000+ Zapier apps expose (Sellfy itself is mostly a *trigger* source). Zapier filtering supported.
- **Analytics/ads (outbound tags):** Google Analytics, Facebook Pixel, Twitter Ads, Google Merchant Center.
- **Site embed:** buy buttons / product / cart embed codes; "Sell Downloads" app for Wix.
- **Data-flow summary:** Sellfy *emits* purchase/subscription/email/cart/contact events; it does not expose a read API, so a CRM/warehouse sync is **event-driven (push)**, reconciled by capturing every webhook (there's no backfill endpoint — store events as they arrive).

## Data model

Money is in **cents** (`449` = $4.49). Timestamps are **ISO 8601**. Country is **ISO** code. Objects below are the shapes seen in webhook payloads (the canonical data surface).

**Order** (New Order webhook):
```json
{
  "id": "dmnVQFUm",
  "status": "COMPLETED",
  "currency": "USD",
  "amount": 449,
  "discount": { "amount": 499 },
  "tax": { "amount": 0, "percents": 0 },
  "customer": {
    "country": "US",
    "payment_type": "card",
    "email": "buyer@example.com",
    "ip": "127.0.0.1",
    "consent_to_newsletters": true,
    "name": "John Doe",
    "address": { "line1": "Wall street", "line2": "12-b7", "state": "NY",
      "country": "US", "city": "New York", "postal_code": "10105", "phone": "212-487-2939" }
  },
  "products": [
    { "id": "61d2ef5352ca3cdc80662cb1", "key": "uQsm", "name": "Icon set",
      "amount": 299,
      "discount": { "type": "coupon", "code": "25OFF", "amount": 25,
        "amount_type": "percentage", "amount_applied": 25, "currency": "USD" },
      "quantity": 1,
      "variant": { "id": "65782c83586fbb97ce6a8715", "name": "Outline set" } }
  ],
  "date": "2022-01-12T11:57:59+00:00"
}
```

**Subscription** (Subscription Product Bought/Canceled webhook):
```json
{
  "id": "61542a2a67cfd83cd57ae4bb",
  "payer_email": "buyer@example.com",
  "plan_name": "Subscription plan name",
  "plan_amount": 2000,
  "interval": "month",
  "product": { "id": "60e5b823221c469a8daede88", "key": "QFUm", "name": "Subscription product name" },
  "activated_at": "2022-05-28T23:17:05+00:00",
  "current_period_started_at": "2022-05-28T23:17:05+00:00",
  "current_period_ends_at": "2022-06-27T23:17:05+00:00"
}
```

- **Product identity:** products have both an internal `id` (Mongo-style ObjectId) and a short `key` (e.g. `uQsm`). Variants have their own `id` + `name`.
- **Customer identity:** email is the practical key; there's no customer object API to query.

## Quick-start recipes

### Recipe 1 — Sync every new sale into a CRM (webhook listener)

Sellfy has no REST API, so capture the **New Order** event.

Setup: Sellfy → Integrations → Webhooks → add title + your HTTPS URL → select "New Order".

Python (Flask):
```python
from flask import Flask, request, abort
app = Flask(__name__)
SECRET = "long-random-string-in-your-url"   # no HMAC — use a secret path/token

@app.post(f"/sellfy/{SECRET}")
def sellfy_order():
    o = request.get_json(force=True)
    if o.get("status") != "COMPLETED":
        return "", 200
    upsert_crm_contact(
        email=o["customer"]["email"],
        name=o["customer"].get("name"),
        country=o["customer"]["country"],
        order_id=o["id"],
        total_usd=o["amount"] / 100,                       # cents -> dollars
        products=[p["name"] for p in o["products"]],
    )
    return "", 200   # respond 2xx fast so Sellfy doesn't treat it as failed
```

Test the endpoint shape with cURL (simulating Sellfy's POST):
```bash
curl -X POST "https://yourapp.com/sellfy/$SECRET" \
  -H "Content-Type: application/json" \
  -d '{"id":"dmnVQFUm","status":"COMPLETED","currency":"USD","amount":449,
       "customer":{"email":"buyer@example.com","name":"John Doe","country":"US"},
       "products":[{"id":"61d2...","key":"uQsm","name":"Icon set","quantity":1}],
       "date":"2022-01-12T11:57:59+00:00"}'
```
Gotchas: idempotency — dedupe on `id` (Sellfy may retry; no signature to verify). Amounts are cents. Only act on `status == "COMPLETED"`.

### Recipe 2 — Provision/revoke subscription access

Listen for **Subscription Product Bought** (grant access / extend `current_period_ends_at`) and **Subscription Product Canceled** (schedule revoke at period end).
```python
@app.post(f"/sellfy/subs/{SECRET}")
def sellfy_subs():
    s = request.get_json(force=True)
    grant_access(
        email=s["payer_email"],
        product_key=s["product"]["key"],
        until=s["current_period_ends_at"],   # ISO 8601
    )
    return "", 200
```
Gotcha: "Bought" fires on the **initial purchase AND each renewal** — make `grant_access` idempotent and just push the expiry forward.

### Recipe 3 — No-code routing with Zapier (no server)

1. In Sellfy, open `https://sellfy.com/user/integrations/apps/zapier` and create your **API token**.
2. In Zapier, add a **Sellfy** trigger; authenticate with the token; pick the event (Completed payment / Refunds / Reversed / all).
3. Add an action (Google Sheets row, email, Slack message, CRM contact, etc.).
Gotcha: leaving the event selection blank fires on *all* events — filter explicitly or add a Zapier filter step.

## Integration patterns

- **Event capture as source of truth:** with no read/backfill API, your integration must persist every webhook on arrival (write to a durable queue/DB before processing). A missed delivery can't be re-fetched.
- **Endpoint security without HMAC:** put a long random secret in the URL path or a query param, restrict by source IP/User-Agent if Sellfy publishes them, and reject anything else. Never grant access purely on payload trust.
- **Idempotency / ordering:** dedupe on order/subscription `id`; treat renewals as expiry extensions; webhook ordering isn't guaranteed, so make handlers commutative where possible.
- **Reconciliation:** since you can't poll, periodically export the orders CSV from the Sellfy dashboard to reconcile against events you stored, and alert on gaps.
- **When Sellfy isn't enough:** if you need programmatic product/order management, a real REST/GraphQL backend, or global tax as MoR, evaluate Payhip, Gumroad (MoR), Lemon Squeezy (MoR), or a full backend (Shopify/BigCommerce/Saleor/Medusa).
