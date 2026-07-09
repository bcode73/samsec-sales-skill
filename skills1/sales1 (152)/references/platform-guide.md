# Dodo Payments Platform Guide

Full reference for the `sales-dodo-payments` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — docs.dodopayments.com + the marketing site. Verify in-account.*

## What Dodo Payments is

A **developer-first Merchant of Record (MoR)** billing + payments platform aimed at **SaaS, AI-first companies, and indie developers/founders**. As MoR, Dodo is the **legal seller of record**: it collects and **remits global sales tax / VAT / GST** across **220+ countries** and **40+ payment methods**, so you don't register/file taxes per jurisdiction. ~50,000+ users; PCI DSS Level 1; 99.99% uptime.

**MoR, not a raw processor.** Stripe/PayPal process payments but leave tax compliance to you; an MoR (Dodo, Paddle, Lemon Squeezy, Polar, Creem) takes that liability — at a higher fee. For the cross-vendor *choice*, use `/sales-merchant-of-record`.

## Billing models

- **One-time payments** · **Subscriptions** (with add-ons, plan change/upgrade/downgrade, proration preview) · **Usage-based** · **Credit-based / wallets** · **On-demand charges**.
- **Digital products:** license keys (create/activate/deactivate), entitlements + grants, digital file delivery.
- **Discounts**, **localized prices** (per-country pricing), **short links**, hosted **customer portal**.

## Object / surface map

| Capability | Surface | Notes |
|---|---|---|
| Payments / subscriptions | **REST API + SDK** | create/list/get/update; on-demand charge |
| Checkout | **Hosted Checkout Session + embeddable + adapters** | `POST /checkouts`; Next.js/Express/… adapters |
| Products / prices / files | **REST API** | CRUD, localized prices, file delivery |
| Customers | **REST API + hosted portal** | portal session, payment methods, wallets |
| License keys / entitlements | **REST API** | software activation + delivery |
| Refunds / disputes / payouts | **REST API** | create refund; list disputes; payout breakups + CSV |
| Webhooks | **Standard Webhooks (signed)** | management API + `standardwebhooks` verify |
| Tax / VAT / GST | **MoR (automatic)** | Dodo remits; not your liability |
| AI agents | **MCP server + Agent Skills** | first-class programmatic surface |

## Pricing (best-effort)

- **Standard: ~4% + $0.40 per transaction**, **no monthly or setup fee**.
- **Enterprise:** custom.
- The fee covers MoR tax handling + remittance — that's the tradeoff vs a raw processor's ~2.9% + 30¢ (where you own tax compliance).

## Data model (payment / subscription — JSON shapes)

No fixed schema reproduced here (see each endpoint's `.md`), but conceptually:

```json
// One-time payment (POST /payments) request, illustrative
{
  "customer": { "email": "jane@example.com", "name": "Jane" },
  "product_cart": [ { "product_id": "prod_123", "quantity": 1 } ],
  "billing": { "country": "US" },
  "payment_link": true
}
```

```json
// Webhook envelope (Standard Webhooks) — headers carry the signature
// webhook-id, webhook-signature, webhook-timestamp
{ "type": "payment.succeeded", "data": { "payment_id": "pay_123", "...": "..." } }
```

Confirm exact field names + event-type strings in the live API reference / Webhooks doc before coding.

## Quick-start recipes

### Recipe 1 — Create a one-time payment (cURL)

```bash
curl -X POST https://test.dodopayments.com/payments \
  -H "Authorization: Bearer $DODO_TEST_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {"email": "jane@example.com", "name": "Jane"},
    "product_cart": [{"product_id": "prod_123", "quantity": 1}],
    "billing": {"country": "US"},
    "payment_link": true
  }'
```

Switch to `https://live.dodopayments.com` + a live key for production. Prefer an official **SDK** (TS/Python/Go/PHP/Java/Kotlin/C#/Ruby/React Native) or a **framework adapter** to avoid hand-building requests + webhook verification.

### Recipe 2 — Verify a webhook (Standard Webhooks)

```python
from standardwebhooks import Webhook   # use the official library, don't hand-roll

wh = Webhook(SIGNING_KEY)  # from dashboard or GET /webhooks/{id}/signing-key

@app.post("/dodo-webhook")
async def dodo_webhook(request):
    raw = await request.body()                 # RAW bytes
    headers = {                                  # Standard Webhooks headers
        "webhook-id": request.headers["webhook-id"],
        "webhook-signature": request.headers["webhook-signature"],
        "webhook-timestamp": request.headers["webhook-timestamp"],
    }
    event = wh.verify(raw, headers)            # validates signature + timestamp (replay-safe)
    if event["type"] == "subscription.active" and not seen(headers["webhook-id"]):
        provision(event["data"])
    return {"ok": True}
```

Local testing: `dodo wh trigger` (Dodo CLI) forwards events to your endpoint over a WebSocket — **test-mode keys only**. CLI mock payloads are **unsigned**, so use the library's `unsafe_unwrap()` in tests (never prod). Dedupe on `webhook-id`.

### Recipe 3 — Spin up a hosted Checkout Session (low-code)

`POST /checkouts` returns a hosted checkout URL you redirect to (or embed); or use a **framework adapter** (Next.js/Express/SvelteKit/…) that scaffolds the checkout route + webhook handler. Use **short links** for a no-backend payment link, and the **customer portal session** so customers self-manage subscriptions.

## When to route out

- **Choosing** MoR vs MoR (Dodo vs Paddle/Lemon Squeezy/Polar/Creem) or MoR vs Stripe → `/sales-merchant-of-record`
- Checkout/AOV conversion strategy across platforms → `/sales-checkout`
- General digital-product selling strategy → `/sales-digital-products`
- Wiring Dodo events into a CRM/ESP (iPaaS) → `/sales-integration`
