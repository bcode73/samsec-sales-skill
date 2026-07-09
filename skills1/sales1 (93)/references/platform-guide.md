# Chargebee Platform Reference

## Overview

Chargebee is a **subscription-billing and revenue-management platform** that sits on top of *your own* payment gateway (40+ supported, incl. Stripe/Braintree/Adyen). It automates recurring billing, dunning, proration, revenue recognition (ASC 606 / IFRS 15), retention, and tax — for B2B SaaS and AI companies. **It is NOT a Merchant of Record:** you remain the seller of record and own your tax liability (contrast with Paddle/Lemon Squeezy). Its praised surface is the **API/webhooks**; its UI and docs are commonly called complex.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|--------|--------------|--------------------|
| **Subscription management** | Plans/items, multi-model pricing (flat, tiered, volume, usage-based, hybrid), trials, pauses, term changes | **API-accessible** + webhook events |
| **Billing & invoicing** | Invoice generation, proration, credits, taxes, offline/auto collection | **API-accessible** + webhook (`invoice_generated`) |
| **Payments** | 40+ gateways, 100+ currencies, payment-source vaulting, 3DS/SCA | **API-accessible** (gateway config is UI) |
| **Receivables / dunning** | Smart Retry (decline-type-aware) + custom retry, dunning emails, recovery | API for triggers; **retry schedule config is UI/plan-gated** |
| **Revenue Recognition (RevRec)** | ASC 606 / IFRS 15 deferred-revenue automation, reports | **Add-on, often priced separately**; reports via API/export |
| **Retention** | Cancel-flow offers, pause/downgrade deflection, churn analytics | **Add-on (Chargebee Retention, ex-Brightback)**; mostly UI-config |
| **Entitlements** | No-code feature provisioning / access mapping to items | **API-accessible** |
| **CPQ** | Quote-to-cash for sales-assisted deals | Largely UI; quotes API exists |
| **Tax** | US sales tax, EU-VAT, AU-GST calculation (you remit — not a MoR) | API surfaces tax on invoices; config UI |

## Pricing, limits & plan gates

> Best-effort from research (2026-06) — pricing changes; verify on chargebee.com/pricing.

- **Starter — free, but the cap is CUMULATIVE not monthly.** Free for the **first $250K in total billing since signup**; past that, **0.75% on all billing** with no grace wall.
- **Performance — ~$599/mo ($7,188/yr, annual commitment, billed monthly).** Caps monthly billing at **$100K** before the same **0.75% overage** applies.
- **Enterprise — custom.**
- **Add-ons priced separately:** Revenue Recognition, Retention/analytics, advanced reporting, premium integrations — commonly **$200–$2,000+/mo**, which is why real TCO often lands **$3K–$8K/mo**.
- **Payment processing is separate** (your gateway's ~2.9% + 30¢) — Chargebee orchestrates billing, it doesn't replace your processor.
- **API/webhook access is available across tiers** (it's a billing engine, not a gated API product), but specific modules (RevRec, Retention) gate behind add-ons.

## Integrations

Data-flow oriented:

- **Payment gateways (writes to):** Stripe, Braintree, Adyen, Authorize.Net, PayPal, GoCardless, + 40 total. Chargebee orchestrates; the gateway moves money.
- **CRM (bidirectional):** Salesforce (deep), HubSpot — sync customers/subscriptions/MRR, push quotes.
- **Accounting (writes to):** QuickBooks, Xero, NetSuite, Sage Intacct — invoices + RevRec journals.
- **Data warehouse (reads from):** export/Sync to Snowflake/BigQuery/Redshift (RevenueStory analytics; or pull via API).
- **iPaaS:** Zapier, Make — triggers on subscription/payment events, actions to create customers/subscriptions.
- **AI / dev:** AgentKit + **MCP server** (`@chargebee/mcp`) for Claude/Cursor/Windsurf.

## Data model

Core objects and how they relate:

```
Customer ──< Subscription ──< SubscriptionItem (item_price_id)
   │             │
   │             └──< Invoice ──< InvoiceLineItem
   │                    └──< Transaction (payment/refund)
   └──< PaymentSource
Event (immutable log of every change; drives webhooks)
```

- **Customer** owns billing identity, payment sources, and ≤900 subscriptions.
- **Subscription** (PC 2.0) holds `subscription_items[]`, each referencing an **`item_price_id`** (a price point of an **Item** in a **Product Family**). PC 1.0 uses `plan_id` + `addons[]` instead.
- **Invoice** is generated per term; **proration** produces credit-notes/adjustments on change.
- **Event** is the immutable change record that webhooks deliver — dedupe on `event.id`, order by `resource_version`.

Subscription JSON (PC 2.0):

```json
{
  "subscription": {
    "id": "8avVGOkx8U1MX",
    "customer_id": "cust_8a1",
    "status": "active",
    "currency_code": "USD",
    "billing_period": 1, "billing_period_unit": "month",
    "current_term_start": 1620000000, "current_term_end": 1622592000,
    "next_billing_at": 1622592000, "mrr": 4900, "auto_collection": "on",
    "subscription_items": [
      { "item_price_id": "pro-USD-monthly", "item_type": "plan", "quantity": 1, "amount": 4900 }
    ]
  }
}
```
<!-- Constructed from docs — verify against live API. -->

## Quick-start recipes

### Recipe 1 — Create a customer + subscription (PC 2.0)

**Trigger:** a new signup picks the Pro monthly plan. **Steps:** create customer → create subscription for an item price.

```bash
# 1) Create the customer
curl https://{site}.chargebee.com/api/v2/customers \
  -u {api_key}: \
  --data-urlencode "first_name=Ada" \
  --data-urlencode "last_name=Lovelace" \
  --data-urlencode "email=ada@example.com"

# 2) Create the subscription for that customer (idempotent)
curl https://{site}.chargebee.com/api/v2/customers/cust_8a1/subscription_for_items \
  -u {api_key}: \
  -H "chargebee-idempotency-key: $(uuidgen)" \
  --data-urlencode "subscription_items[item_price_id][0]=pro-USD-monthly" \
  --data-urlencode "subscription_items[quantity][0]=1"
```

```python
import os, uuid, requests

SITE = os.environ["CB_SITE"]; KEY = os.environ["CB_API_KEY"]
base = f"https://{SITE}.chargebee.com/api/v2"
auth = (KEY, "")  # key as username, empty password

cust = requests.post(f"{base}/customers", auth=auth, data={
    "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com",
}).json()["customer"]

sub = requests.post(
    f"{base}/customers/{cust['id']}/subscription_for_items", auth=auth,
    headers={"chargebee-idempotency-key": str(uuid.uuid4())},
    data={"subscription_items[item_price_id][0]": "pro-USD-monthly",
          "subscription_items[quantity][0]": 1},
).json()["subscription"]
print(sub["id"], sub["status"])
```

**Gotchas:** money is in cents; PC 1.0 sites use `plan_id` not `subscription_items`; always send the idempotency key so a network retry doesn't double-create.

### Recipe 2 — Provision / revoke access on a webhook (no HMAC)

**Trigger:** subscription activates → grant your app's Pro; payment fails / cancels → start dunning / revoke. **Verification:** basic-auth + IP allowlist (no HMAC), dedupe on `event.id`, order by `resource_version`.

```python
from flask import Flask, request, abort

app = Flask(__name__)
seen = set()          # back this with Redis/DB, keep ids 3+ days
versions = {}         # subscription_id -> last resource_version

ALLOWED_IPS = {...}   # Chargebee published ranges
BASIC = ("cb_hook_user", "cb_hook_pass")

@app.post("/webhooks/chargebee")
def hook():
    if request.remote_addr not in ALLOWED_IPS: abort(403)
    if request.authorization != None and (request.authorization.username,
            request.authorization.password) != BASIC: abort(401)

    ev = request.get_json()["event"]
    if ev["id"] in seen: return "", 200      # dedupe redelivery
    seen.add(ev["id"])

    sub = ev["content"]["subscription"]
    rv = sub.get("resource_version", 0)
    if rv <= versions.get(sub["id"], 0): return "", 200   # out-of-order/stale
    versions[sub["id"]] = rv

    t = ev["event_type"]
    if t in ("subscription_activated", "subscription_created"):
        grant_access(sub["customer_id"])
    elif t in ("payment_failed",):
        start_dunning(sub["customer_id"])
    elif t in ("subscription_cancelled",):
        revoke_access(sub["customer_id"])
    return "", 200   # respond 2xx fast; do heavy work async
```

**Gotchas:** there is **no signature header** — your auth IS the basic-auth creds + IP allowlist; reconcile missed events with a nightly `GET /subscriptions?updated_at[after]=...` pull.

### Recipe 3 — Sync subscriptions / MRR to a warehouse

**Trigger:** nightly job pages all subscriptions into Snowflake/BigQuery.

```python
import requests, os
base = f"https://{os.environ['CB_SITE']}.chargebee.com/api/v2"
auth = (os.environ["CB_API_KEY"], "")

rows, offset = [], None
while True:
    params = {"limit": 100, "sort_by[asc]": "updated_at"}
    if offset: params["offset"] = offset
    r = requests.get(f"{base}/subscriptions", auth=auth, params=params).json()
    rows += [x["subscription"] for x in r["list"]]
    offset = r.get("next_offset")
    if not offset: break
# upsert rows into the warehouse; mrr is async-updated so re-pull on a schedule
```

**Gotchas:** `mrr` updates asynchronously (don't treat a single pull as final); use `updated_at[after]` for incremental syncs; 429 → exponential backoff.

## Integration patterns

- **CRM sync:** key on `customer_id` ↔ your CRM record; push `status`, `mrr`, `next_billing_at`. Resolve conflicts by `resource_version` (Chargebee is source of truth for billing state).
- **Webhook listener:** basic-auth + secret-URL + IP allowlist; **idempotent on `event.id`**; **order by `resource_version`**; 2xx fast + async processing; **reconcile** via API for missed events.
- **Batch pipeline:** offset pagination (`next_offset`), `limit=100`, incremental via `updated_at[after]`; idempotency keys on any writes; backoff on 429.
- **Catalog migration (PC 1.0 → 2.0):** one-way, not automatic — plans/addons become items + item_prices + price points under product families; the API calls change, so dual-write/test on a test site (Time Machine) first.
