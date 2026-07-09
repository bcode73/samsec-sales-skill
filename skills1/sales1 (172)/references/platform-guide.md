# FastSpring Platform Reference

## Overview

FastSpring is an **all-in-one Merchant of Record (MoR)** for selling **SaaS, downloadable software, games, AI
products, eLearning, and other digital goods** globally. As the MoR, FastSpring is the **legal seller** of your
product — it processes payments in **35+ currencies across 200+ regions**, and **collects and remits sales
tax / VAT / GST** so you never register or file in each jurisdiction. It's an established, enterprise-heritage
platform (3,200+ customers incl. Adobe, Intel, Rovio), which shows up as deeper B2B features and a
**quote-based, sales-assisted pricing** model rather than a public rate card.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Global payments** | Card + local payment methods, 35+ currencies, 200+ regions, higher cross-border approval | Checkout via SBL / checkout session (API) |
| **Subscription management + billing** | Recurring billing, trials, upgrades/downgrades, proration, dunning, co-term/grouped subscriptions | **API-accessible** (query/update/cancel/pause/resume) + **webhook-accessible** |
| **Branded checkout** | Localized popup / embedded / hosted / web checkout | **Store Builder Library (JS)** + checkout-session API |
| **Tax compliance (MoR)** | FastSpring is seller of record; collects + **remits** VAT/GST/sales tax | Automatic (no config); reflected in pricing endpoint |
| **Fraud prevention** | Risk scoring, chargeback reduction | UI + `chargeback.created` webhook |
| **Affiliate marketing** | Built-in partner/affiliate network | UI-managed (some data via API/reports) |
| **B2B: digital invoicing** | Invoices for B2B software sales | UI + API |
| **B2B: interactive quotes** | Custom SaaS deals with e-signatures | **Quotes API** + quote webhooks |
| **Reporting & analytics** | Revenue, subscription, and payout insights | Reports via UI + API; `payout` webhooks |
| **Products & pricing** | Catalog, offers, region/currency-adjusted prices | **API-accessible** (CRUD products/offers/prices) |

## Pricing, limits & plan gates

> Best-effort from research (2026-07) — **FastSpring pricing is quote-based and negotiable; verify with their sales team.**

- **Model:** revenue-share, **"all-in-one pricing, no additional fees"** — one rate covers every feature
  (subscriptions, tax, etc.), no per-feature charges, **no monthly subscription fee**, no minimum volume.
- **Rates (reported, best-effort):** **8.9%** or **5.9% + $0.95** per transaction — **FastSpring's sales team
  assigns your rate** by transaction type and volume; custom rates are negotiated. Specific percentages are
  **not published** on the pricing page.
- **Effective rate runs higher for subscriptions:** for low-to-mid-ticket recurring plans, reviewers report
  effective rates regularly exceeding **10–12%** once the per-transaction component is spread across small charges.
- **Refunds keep the fee:** a frequent complaint — FastSpring **retains its transaction fee even when you refund**
  a customer. Model this into your refund policy.
- **API is not plan-gated** — the REST API, SBL, and webhooks are part of the platform, not an upsell tier.
- **Rate limit:** 250 API calls / IP / minute (`429` on exceed).

## Integrations

- **Data flow:** checkout **writes** orders/subscriptions into FastSpring; **webhooks push** events out to your
  app (order/subscription/account/payout/quote/return/fulfillment); the **REST API reads** orders/subscriptions/
  accounts and **reads/writes** products, prices, coupons, and subscriptions.
- **Native connectors:** Salesforce, HubSpot, and other out-of-the-box extensions (Developer Tools > Extensions).
- **iPaaS:** Zapier (triggers/actions) and similar, driven off webhooks.
- **Mobile/game:** FastSpring **Steer Safe** integration paths for React Native and Unity/UGS (iOS & Android).
- **Community:** Laravel Cashier driver (`bgultekin/cashier-fastspring`); license platforms (e.g. Cryptlex).

## Data model

Key objects (see `references/fastspring-api-reference.md` for endpoints):

- **Account** — a customer. `account.created` / `account.updated`.
- **Order** — a completed purchase (created by checkout, read via API).
- **Subscription** — a recurring instance with statuses `active` / `trial` / `overdue` / `canceled` /
  `deactivated`, plus **grouped (co-term)** subscriptions.
- **Product / Offer / Price** — catalog; prices are returned **adjusted by country + currency** (VAT/GST inclusive).

<!-- Constructed from docs — verify against live API -->
```json
// order.completed webhook event data (representative)
{
  "id": "evt_abc123",          // dedupe on this — events can be redelivered
  "type": "order.completed",
  "live": true,
  "created": 1719000000000,     // milliseconds
  "data": {
    "order": "AB1-CD2-EF3",
    "account": { "id": "acct_123", "contact": { "email": "buyer@example.com" } },
    "items": [{ "product": "my-saas-pro", "quantity": 1 }],
    "total": 49.00,
    "currency": "USD"
  }
}
```

## Quick-start recipes

### Recipe 1 — Provision access when an order completes (webhook)

Trigger: buyer checks out → FastSpring sends `order.completed` (and `subscription.activated` for subscriptions).

Steps: (1) configure a webhook with an HMAC secret; (2) verify `X-FS-Signature` over the raw body; (3) dedupe on
`event.id`; (4) grant access.

```python
# Flask handler — verify signature, then provision. Full snippet in fastspring-api-reference.md
import base64, hashlib, hmac
from flask import request, abort

FS_SECRET = b"your-webhook-hmac-secret"

def verify(raw, header_sig):
    expected = base64.b64encode(hmac.new(FS_SECRET, raw, hashlib.sha256).digest()).decode()
    return hmac.compare_digest(header_sig, expected)

# in the route:
raw = request.get_data()
if not verify(raw, request.headers.get("X-FS-Signature", "")):
    abort(401)
for e in request.get_json()["events"]:
    if e["type"] in ("order.completed", "subscription.activated"):
        grant_access(e["data"])          # idempotent on e["id"]
```

### Recipe 2 — Pull subscriptions into a warehouse/CRM (API)

Trigger: nightly sync of active subscriptions to your CRM or BigQuery/Snowflake.

```bash
# All active live subscriptions changed in a date range
curl "https://api.fastspring.com/subscriptions?status=active&begin=2026-06-01&end=2026-06-30&live=true" \
  -u "$FS_API_USER:$FS_API_PASSWORD" \
  -H "User-Agent: warehouse-sync/1.0" -H "Content-Type: application/json"
```

```python
# Python: page/batch, back off on 429 (see fs_get helper in the API reference)
subs = fs_get("/subscriptions", (FS_API_USER, FS_API_PASSWORD),
              params={"status": "active", "live": "true",
                      "begin": "2026-06-01", "end": "2026-06-30"})
for s in subs:
    upsert_to_crm(s)   # map FastSpring subscription -> your CRM object
```

Gotcha: no documented rate-limit reset header — back off exponentially on `429`; batch by comma-separating IDs
where an endpoint supports it.

### Recipe 3 — Launch a branded checkout from your site (Store Builder Library)

Trigger: a "Buy" button on your marketing site should open FastSpring checkout without a full server round-trip.

```html
<script id="fsc-api" src="https://sbl.onfastspring.com/sbl/1.0.1/fastspring-builder.min.js"
        type="text/javascript" data-storefront="yourstore.onfastspring.com"></script>
<button onclick="fastspring.builder.push({ products: [{ path: 'my-saas-pro', quantity: 1 }] });
                 fastspring.builder.checkout();">Buy Pro</button>
```

To prevent price tampering, sign the cart server-side using the **SBL Access Key** (Developer Tools > Store
Builder Library) and pass the secured payload. Confirm the final SBL version/URL against the live docs.

## Integration patterns

- **Webhook listener:** always set an HMAC secret and verify `X-FS-Signature` over the **raw** body; **dedupe on
  `event.id`** (redelivery happens); switch on `event.type`; return `2xx` fast and process async. Enable **webhook
  expansion** if you want full JSON rather than references. Use the **Events API** to replay/reconcile if your
  endpoint was down.
- **Subscription lifecycle → dunning:** react to `subscription.charge.failed`, `subscription.payment.overdue`,
  and `subscription.payment.reminder` to drive retries/emails; `subscription.deactivated` = access should end.
- **CRM/warehouse sync:** treat webhooks as the real-time signal and a **daily API pull as reconciliation**
  (FastSpring refreshes FX every 6 hours; re-pull pricing daily). Map `account` → contact/company,
  `order`/`subscription` → deal/subscription objects.
- **Refund accounting:** FastSpring keeps its fee on refunds — reconcile net revenue from `return` events, don't
  assume the fee is reversed.
