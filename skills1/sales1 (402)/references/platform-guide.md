# Paddle Platform Reference

## Overview

Paddle (paddle.com) is a **Merchant of Record (MoR)** for SaaS, digital products, apps, and games — Paddle
becomes the **legal seller**, so it handles payments, **global sales-tax/VAT compliance (300+ markets)**,
subscriptions, checkout, invoicing, fraud, dunning (**Retain**), and analytics (**ProfitWell Metrics**).
Best for software businesses that want to *not* operate their own tax/compliance stack. The trade-offs:
~5% + $0.50/transaction (higher than a bare Stripe rate), and a hard split between the legacy **Paddle
Classic** and the current **Paddle Billing** products.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Checkout | Localized overlay/inline checkout, client-side token | **API** (transactions) + JS checkout |
| Subscriptions | Plans, trials, proration, pauses, upgrades | **API** (`/subscriptions`) + webhooks |
| Catalog | Products + prices + discounts | **API** (`/products`, `/prices`, `/discounts`) |
| Transactions | One-off + recurring charges, invoices | **API** (`/transactions`) + webhooks |
| Tax & compliance | Auto sales tax/VAT calc + remittance (MoR) | **Handled by Paddle** (not your code) |
| Adjustments | Refunds, credits, chargebacks | **API** (`/adjustments`) + `adjustment.created` webhook |
| Retain | Failed-payment recovery, churn reduction | **UI/config** (dunning); events via webhooks |
| ProfitWell Metrics | MRR, churn, LTV analytics (free tier) | **API** (reports) + UI |
| Notifications | Webhook destinations, logs, simulator | **API** (`/notification-settings`) + webhooks |

**Programmatic interfaces:** **Paddle Billing REST API** (`api.paddle.com`, Bearer key, sandbox at
`sandbox-api.paddle.com`), **HMAC-SHA256 signed webhooks**, **Docs MCP**, Postman collection. Legacy
**Paddle Classic** API is separate and being phased out. See `references/paddle-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on the live pricing page; Paddle quotes are often custom.*

- **~5% + $0.50 per transaction**, all-inclusive — **global tax compliance + remittance included** (no
  extra fee for selling internationally). Same headline as Lemon Squeezy; Polar is ~10% + $0.50; Stripe is
  ~2.9% + $0.30 but **not** a MoR (you'd add Stripe Tax + handle remittance yourself).
- **ProfitWell Metrics** has a free tier; **Retain** and higher-touch support are negotiated.
- No "plan gates" on the API per se — it's transaction-fee based; sandbox is free for development.
- As MoR, **Paddle controls payouts** (it pays you out on a schedule after collecting), and enforces
  acceptable-use/risk review — high-risk or disallowed categories can be declined.

## Integrations

- **Direction:** the API **writes** catalog/customers/subscriptions and **reads** transactions/reports;
  **webhooks push** lifecycle events. Checkout runs client-side with a client token.
- **Auth:** secret Bearer API key (server) + client-side token (browser checkout). Separate sandbox keys.
- **Native/iPaaS:** Zapier, RevenueCat (mobile), and many billing tools; ProfitWell for metrics.

## Data model

IDs are prefixed ULIDs (`pro_`, `pri_`, `ctm_`, `txn_`, `sub_`, `adj_`). Money is a **string in the
smallest unit** (cents). Identity for buyers is the **customer** (`ctm_`).

**Subscription** <!-- Constructed — verify against live API -->
```json
{ "id": "sub_01h...", "status": "active", "customer_id": "ctm_01h...",
  "items": [ { "price_id": "pri_01h...", "quantity": 1 } ],
  "current_billing_period": { "starts_at": "2026-06-01T00:00:00Z", "ends_at": "2026-07-01T00:00:00Z" } }
```

**Transaction** <!-- Constructed — verify -->
```json
{ "id": "txn_01h...", "status": "completed", "customer_id": "ctm_01h...",
  "details": { "totals": { "grand_total": "2000", "tax": "350", "currency_code": "USD" } } }
```

**Webhook event** <!-- Constructed — verify -->
```json
{ "event_id": "evt_01h...", "event_type": "subscription.activated", "occurred_at": "2026-06-27T10:00:00Z",
  "data": { "id": "sub_01h...", "status": "active", "customer_id": "ctm_01h..." } }
```

## Quick-start recipes

### Recipe 1 — Provision access when a subscription activates (webhook)

**Trigger:** `subscription.activated` / `transaction.completed` webhook → grant the customer access; on
`subscription.canceled` / `past_due`, revoke or start dunning.
```python
# Flask-style handler
from flask import request, abort
def paddle_webhook(secret):
    if not verify(request.get_data(), request.headers["Paddle-Signature"], secret):  # see api-reference
        abort(401)
    e = request.get_json()
    if e["event_type"] in ("subscription.activated","transaction.completed"):
        grant_access(e["data"]["customer_id"])
    elif e["event_type"] in ("subscription.canceled","subscription.past_due"):
        start_dunning_or_revoke(e["data"]["customer_id"])
    return "", 200
```
**Gotchas:** **verify the HMAC signature** first; order by **`occurred_at`** (delivery order isn't
guaranteed); dedupe on **`event_id`** (Paddle redelivers). Build against **sandbox** first.

### Recipe 2 — Create a product + price via the API

```bash
PRO=$(curl -s -X POST "https://api.paddle.com/products" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d '{"name":"Pro","tax_category":"saas","type":"standard"}' | jq -r .data.id)
curl -s -X POST "https://api.paddle.com/prices" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"product_id\":\"$PRO\",\"unit_price\":{\"amount\":\"2000\",\"currency_code\":\"USD\"},\"billing_cycle\":{\"interval\":\"month\",\"frequency\":1}}"
```
**Gotchas:** `amount` is **cents as a string** (`"2000"` = $20.00). Set the right `tax_category` so Paddle
taxes correctly.

### Recipe 3 — Sync subscriptions/MRR into your warehouse

**Trigger:** cron → page `GET /subscriptions` and `GET /transactions` (follow `meta.pagination.next`), or
pull the **reports** endpoints (MRR/churn). Use `include` to avoid N+1 calls.

## Integration patterns

- **Build on Billing, not Classic.** They're incompatible; new integrations use `api.paddle.com` + Bearer.
- **Webhooks are the source of truth for state.** Verify signatures, order by `occurred_at`, idempotency on
  `event_id`, and reconcile periodically via the API (webhooks can be missed).
- **You don't touch tax.** As MoR, Paddle calculates + remits sales tax/VAT; don't build your own tax logic
  — set `tax_category` correctly and let Paddle handle it. (For the MoR-vs-DIY decision, see
  `/sales-merchant-of-record`.)
- **Payouts are Paddle's, on a schedule.** Model cash flow around Paddle's payout timing and its fee, not
  instant Stripe-style settlement.
- **Sandbox everything.** A separate sandbox account + keys; never test against production billing.
