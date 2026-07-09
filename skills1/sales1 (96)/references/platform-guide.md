# Checkout Page Platform Reference

## Overview

Checkout Page (checkoutpage.com) is a no-code, **Stripe-based** hosted checkout builder for
founders, creators, and small teams selling digital products, subscriptions, payment plans,
pay-what-you-want offers, and **event tickets** — plus standalone lead/form capture. It bolts a
branded, conversion-optimized checkout (order bumps, 1-click upsells, cart-abandonment recovery)
onto whatever you already run, and charges **0% platform transaction fees** on every plan. It is
**not a Merchant of Record** — because it runs on your own Stripe account, you are the seller of
record and own tax compliance (Stripe Tax is available). Its standout differentiator is that
forms, checkout, upsells, events, and customer records all live behind **one REST API + native
MCP server**, so an AI agent can build a paid checkout end-to-end from a prompt.

## Capabilities & automation surface

| Capability | What it does | Automation |
|---|---|---|
| Checkout page builder | Point-and-click branded payment pages | **API-accessible** (create/read/update/archive) + **MCP** (`create_checkout_page`, `get_checkout_page`) |
| Order bumps + 1-click upsells | Post-add and post-purchase offers to lift AOV ("Funnel Builder") | UI-configured; conversions reported via webhook |
| Subscriptions & payment plans | Recurring billing, trials, setup fees, `endsAfterPayments` | **API + webhook** (`object: subscription`) + **MCP** (`list_subscriptions`) |
| Pay-what-you-want / one-time | Flexible one-time pricing | **API + webhook** (`object: payment`) |
| Events & ticketing | Ticket types, registration, attendee fields, **mobile check-in** | **API** (`/v1/events`, `/v1/tickets/validate`, `/v1/bookings`) + **MCP** (`list_bookings`) |
| Form builder | Surveys, applications, RSVPs, lead capture (with or without payment) | **API** (`/v1/forms`) + **webhook** (`object: submission`) + **MCP** (`create_form`, `get_form`, `list_submissions`, `get_submission`) |
| Cart-abandonment recovery | Automated recovery emails for started-but-unfinished checkouts | UI-configured |
| Coupons | Percentage/amount discount codes, duration rules | **API** (`/v1/coupons`) + **MCP** (`create_coupon`) |
| Customers | Buyer records with Stripe id cross-reference | **API** (`/v1/customers`) + **MCP** (`list_customers`, `get_customer`) |
| Invoices | Auto-generated invoice PDFs, regeneration | **API** (`/v1/invoices`) |
| Tax rates | Manual tax-rate objects (or Stripe Tax) | **API** (`/v1/tax-rates`) |
| Files | Digital-good file upload/download/delete | **API** (`/v1/files/*`) + **MCP** (`upload_file`) |

Full endpoint list, auth, pagination, rate limits, and verbatim webhook payloads are in
[`checkoutpage-api-reference.md`](./checkoutpage-api-reference.md).

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — verify live at checkoutpage.com/pricing before advising.*

| Plan | Price (best-effort) | Sales cap | Notes |
|---|---|---|---|
| Launch | ~$24/mo billed annually (~$29 monthly) | up to ~$3K/mo online sales | Standard support |
| Grow ("Recommended") | ~$83/mo annual (~$990/yr) | volume tiers ~$10K→$100K+/mo | + custom domain, custom email domain, premium support |
| Enterprise | Custom | Custom | Dedicated support, custom billing, onboarding, free migration |

- **0% transaction fees** on all plans (you still pay Stripe's processor rate ~2.9% + 30¢).
- **7-day free trial**, no credit card required; 7-day money-back guarantee.
- **99% of features are on every plan** — plans differ mainly on **sales volume**, support level,
  and custom domains, not feature access. This is a **volume-cap** pricing model (like
  Sellfy/SendOwl), not a feature-gate model (like SamCart/ThriveCart) — forecast monthly sales,
  not just features.
- **API rate limits**: 500 req/min per store, 100 req/min per API key → `429` on exceed. These
  apply on all plans (no separate API tier gate found — verify).
- 50% discount for nonprofits/charities/education.

## Integrations

Data flows out of Checkout Page mainly via **webhooks** and the **REST API** (bidirectional:
read customers/payments/subscriptions; create checkouts/forms/coupons; upload files).

- **Stripe** (core — the payment rail; "Built on Stripe, Verified by Stripe"). Stripe object ids
  are echoed in webhooks so you can reconcile in Stripe directly.
- **Stripe Tax** — tax calculation on your Stripe account.
- **Zapier** — triggers/actions + a **Zapier MCP** endpoint (`zapier.com/mcp/checkout-page`).
- **Webhooks** — store-level (all pages) and page-level (single page, `conversion` only).
- **Google Sheets** — append conversions.
- **Rewardful** / **Tolt** — affiliate/referral attribution.
- **Meta Pixel** / **Google Analytics** — client-side conversion tracking.
- **Native MCP server** (`https://mcp.checkoutpage.com`, OAuth) — 13 tools for AI assistants.

## Data model

Money is a **decimal string in the display currency** (`"23.99"`), not cents. Key objects
(shapes echoed by the `conversion` webhook — see api-reference for full verbatim payloads):

**Payment** (`object: "payment"`):
```json
<!-- Constructed from docs — verify against live API -->
{
  "id": "6464cc07822f15f2aca067dd",
  "orderId": "02009743",
  "amount": "23.99",
  "currency": "usd",
  "status": "paid",
  "customerId": "611e6383cf7d2c0020380e53",
  "customerEmail": "buyer@example.com",
  "stripeCustomerId": "cus_...",
  "stripePaymentId": "pi_...",
  "fields": { "customer_email": "buyer@example.com", "quantity": "1" },
  "variants": { "size": { "name": "Size", "selectedOption": "Medium", "price": "10.00", "sku": "100" } },
  "couponCode": "COUPON",
  "queryParameters": { "utm_source": "google" },
  "livemode": false,
  "checkoutSlug": "t-shirt"
}
```

**Subscription** (`object: "subscription"`): adds `interval`, `intervalCount`, `endsAfterPayments`,
`setupFee`, `trailStart` (sic), `trialEnd`, `cancelAt`, `currentSubscriptionPeriodStart/End`,
`stripeSubscriptionId`, `paymentGateway`, `paymentMethod`, `status` (`active`/…).

**Submission** (`object: "submission"`): form fields + `variants`, no `amount`/payment fields;
`productTitle` is the form name.

**Relationships**: a checkout page (`checkoutId`/`checkoutSlug`) produces payments/subscriptions/
submissions, each tied to a customer (`customerId` + `stripeCustomerId`) and optionally a coupon.
Events own tickets → bookings (attendees).

## Quick-start recipes

### Recipe 1 — Sync paid conversions into a CRM/warehouse (webhook listener)

Trigger: a buyer completes checkout → `conversion` webhook fires.

Steps: register a **store-level** webhook at a tokenized URL → on POST, branch on
`object` → re-verify via the REST API → upsert the customer + order into your CRM.

```python
# Flask listener — treats the webhook as a hint, the API as truth (payloads are unsigned)
import os, requests
from flask import Flask, request, abort

app = Flask(__name__)
API = "https://api.checkoutpage.com/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['CHECKOUTPAGE_API_KEY']}"}
WEBHOOK_TOKEN = os.environ["CHECKOUTPAGE_WEBHOOK_TOKEN"]  # secret in the URL path

@app.post(f"/hooks/checkoutpage/{WEBHOOK_TOKEN}")
def hook():
    body = request.get_json(force=True)
    if body.get("event") != "conversion":
        return "", 200
    data = body["data"]
    if data.get("livemode") is not True:
        return "", 200                      # ignore test payments in prod
    # Re-verify by re-fetching the customer (unsigned payload → don't trust blindly)
    cust = requests.get(f"{API}/customers/{data['customerId']}", headers=HEADERS, timeout=10)
    if cust.status_code != 200:
        abort(400)
    upsert_crm(
        object_type=body["object"],         # payment | subscription | submission
        order_id=data.get("orderId"),
        email=data.get("customerEmail"),
        amount=data.get("amount"),           # decimal STRING, not cents
        utm=data.get("queryParameters", {}),
    )
    return "", 200                           # ack fast; dedupe on orderId upstream
```

```bash
# Manually replay/verify a payment referenced by a webhook
curl "https://api.checkoutpage.com/v1/payments?limit=5" \
  -H "Authorization: Bearer $CHECKOUTPAGE_API_KEY"
```

Gotchas: payloads are **unsigned** (no documented HMAC) → tokenize the URL + re-fetch;
`amount` is a decimal string; dedupe on `orderId`; keep a nightly polling backup (no
delivery log documented).

### Recipe 2 — Nightly incremental pull of payments (pagination + rate limits)

Trigger: scheduled job → reconcile against webhook-driven data.

```python
import os, time, requests

API = "https://api.checkoutpage.com/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['CHECKOUTPAGE_API_KEY']}"}

def pull_all(resource="payments"):
    after, rows = None, []
    while True:
        params = {"limit": 100}
        if after:
            params["starting_after"] = after
        r = requests.get(f"{API}/{resource}", headers=HEADERS, params=params, timeout=15)
        if r.status_code == 429:
            time.sleep(2)                    # back off; 100 req/min per key
            continue
        r.raise_for_status()
        page = r.json().get("data", [])
        if not page:
            break
        rows.extend(page)
        after = page[-1]["id"]               # cursor = last id (newest-first)
        if len(page) < 100:
            break
    return rows
```

### Recipe 3 — Build a paid event-registration checkout from a prompt (MCP)

Trigger: you want a ticketed event page with custom attendee fields — no clicking.

```bash
claude mcp add --transport http checkoutpage https://mcp.checkoutpage.com
# then in Claude: /mcp  → authenticate (OAuth), then prompt:
# "Create a checkout page for a paid workshop: one 'General Admission' ticket at $49,
#  collect attendee name and a 'dietary requirements' question, and make a LAUNCH20 coupon."
```

The agent calls `create_checkout_page` (+ `create_form` for the attendee fields, `create_coupon`
for the code). Because forms + Stripe checkout sit in the same MCP, the whole flow runs in chat —
Checkout Page's key edge over form-only MCP builders.

## Integration patterns

- **Webhook + API reconciliation** (recommended): react in near-real-time to `conversion`, but
  treat the payload as a hint — re-fetch the object by id before provisioning access or moving
  money, since payloads are unsigned. Dedupe on `orderId`.
- **CRM field mapping**: `customerEmail`/`customerName` → contact; `orderId` → deal/order;
  `amount` (decimal string → parse) → value; `queryParameters` (UTM) → attribution;
  `stripeCustomerId` → link to Stripe.
- **Batch pipeline**: cursor pagination (`starting_after` = last `id`), 100/page, 100 req/min per
  key — sleep on `429` and resume from the last cursor; keep pulls incremental.
- **Agentic**: the native MCP is the fastest path for a maker to spin up/query checkouts; the REST
  API is the path for a durable production integration.
