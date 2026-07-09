# SamCart Platform Reference

## Overview

SamCart is a hosted checkout/cart platform for digital-product creators — conversion-optimized checkout templates, order bumps, 1-click upsells, and subscription dunning, now wrapped in an AI layer that generates products, sales pages, and copy. Subscription-priced (vs ThriveCart's lifetime license); the trade is modern templates and ongoing feature development against recurring cost.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Checkout & sales pages | Templates, embedded checkout, A/B testing (Pro) | **UI-only** to build; orders flow out via API/webhooks |
| Order bumps & 1-click upsells | Pre- and post-purchase offers (Pro plan) | **UI-only** to configure; `upsell_id`/`funnel_id` visible on API orders; `POST /orders/{id}/add-to-order` can charge an extra product server-side |
| Orders / charges / customers | Sales records | **API-accessible** (read; refund via POST) |
| Subscriptions + Subscription Saver (dunning) | Recurring billing, failed-payment recovery | **API-accessible** (read, cancel, scheduleCancel, update; `/failed-charges` for dunning visibility) + **webhook-accessible** (charged/failed/delinquent/recovered/…) |
| Refunds | Full refund of a charge | **API-accessible** (`POST /refunds/charges/{id}/`) |
| Webhooks ("Notify URL") | ~15 event triggers via Integration Engine rules | **Webhook-accessible** (UI-configured; unsigned JSON POST) |
| Affiliate Center | Built-in affiliate program (Pro) | **UI-only**; `affiliate_id` appears on API orders/subscriptions |
| Courses / customer hub | Course delivery, student events | **Webhook-accessible** (student added/started/finished); otherwise UI |
| AI tools (product/page/copy generation) | "AI handles the hard parts" | **UI-only** |
| Email sequences, cart abandonment | Built-in recovery emails | **UI-only** |

**iPaaS**: Zapier (rich triggers/actions + a generic Zapier MCP server exposing SamCart actions to AI clients), Make app, Integrately. No dedicated MCP server.

## Pricing, limits & plan gates

*Best-effort (2026-07) — verify at samcart.com/pricing.*

- **Core — $79/mo** ($59/mo annual): unlimited products, checkout, courses, AI tools.
- **Pro — $199/mo** ($149/mo annual): **order bumps, 1-click upsells, A/B testing, Affiliate Center, custom checkout branding** — the conversion features that are SamCart's whole pitch are Pro-gated.
- **Enterprise — custom**: dedicated support, custom rates, unlimited seats.
- 7-day free trial; payment-processing fees (Stripe/PayPal) apply on top. Legacy Launch/Grow/Scale plans reportedly scaled price with revenue — grandfathered accounts should model that.
- **API access is not a plan toggle — it's a support-gated private beta** (email support@samcart.com for a key).

## Integrations

Payment: Stripe, PayPal, buy-now-pay-later options. Email/membership: most major ESPs and membership tools via the Integration Engine rules (the same rules system that powers Notify URL webhooks). Zapier/Make for everything else. Data flows: orders/subscriptions OUT via webhooks + API pulls; product/checkout config is UI-only IN.

## Data model

Marketplace (your account) → **Products** → **Orders** (with `cart_items[]`, each possibly linked to a `subscription_id` and `upsell_id`) → **Charges** (a subscription generates recurring charges; failures land in `/failed-charges`) → **Refunds**. **Customers** own orders/charges/subscriptions/addresses. `funnel_id`/`upsell_id` on orders attribute funnel and upsell revenue; `affiliate_id` attributes affiliate sales. All money in **cents**.

See `samcart-api-reference.md` for verbatim JSON shapes (Order, Subscription, Refund, Pagination).

## Quick-start recipes

### Recipe 1 — Nightly order sync into a warehouse/CRM (Python)

```python
import os, requests

BASE = "https://api.samcart.com/v1"
H = {"sc-api": os.environ["SAMCART_API_KEY"], "Accept": "application/json"}

url = f"{BASE}/orders?limit=100&created_at_min=2026-07-03T00:00:00Z"
while url:
    r = requests.get(url, headers=H)
    if r.status_code == 429:              # header states seconds remaining
        raise SystemExit("rate limited — back off and resume")
    r.raise_for_status()
    body = r.json()
    for order in body["data"]:
        # upsert into your DB: order["id"], order["total"], order["cart_items"], ...
        pass
    url = (body.get("pagination") or {}).get("next")
```

Gotchas: money is in cents; filter with `created_at_min`/`created_at_max` to keep pulls incremental; follow `pagination.next` until null.

### Recipe 2 — Notify URL webhook listener with API verification (Flask)

SamCart webhooks are **unsigned** — treat the payload as a hint and verify against the API before acting.

```python
import os, requests
from flask import Flask, request, abort

app = Flask(__name__)
H = {"sc-api": os.environ["SAMCART_API_KEY"], "Accept": "application/json"}

# Register this URL in SamCart: Apps → Webhooks → Install,
# then add a rule (e.g. trigger "Product Purchased").
# Put an unguessable token in the path since payloads aren't signed.
@app.post("/hooks/samcart/<token>")
def samcart_hook(token):
    if token != os.environ["HOOK_TOKEN"]:
        abort(404)
    event = request.get_json(force=True)
    order_id = (event.get("order") or {}).get("id")
    if order_id:                                # verify before trusting
        o = requests.get(f"https://api.samcart.com/v1/orders/{order_id}", headers=H)
        if o.status_code == 200:
            order = o.json()
            # grant access / update CRM using the VERIFIED order
    return "", 200
```

Gotchas: "Checkout failed" fires after a built-in 10-minute delay; "Prospect created" fires ~2 hours after creation; missing payload values arrive as NULL. The Integration Engine logs only the last 1,000 events — keep a polling reconciliation (Recipe 1).

### Recipe 3 — Cancel a subscription at period end (cURL)

```bash
# Immediate cancel
curl -X POST "https://api.samcart.com/v1/subscriptions/$SUB_ID/cancel" \
  -H "sc-api: $SAMCART_API_KEY" -H "Accept: application/json"

# Or schedule the cancellation instead (returns {"status":"scheduled","cancel_date":"..."})
curl -X POST "https://api.samcart.com/v1/subscriptions/$SUB_ID/scheduleCancel" \
  -H "sc-api: $SAMCART_API_KEY" -H "Accept: application/json"
```

Gotchas: build self-serve cancellation on `scheduleCancel` (access until period end) rather than immediate `cancel` — billing-after-cancellation complaints are SamCart's #1 public-review pattern, and giving buyers a reliable, logged path protects you. Pair with the `Subscription Canceled` webhook trigger to revoke access.

## Integration patterns

- **Revenue warehouse**: webhook triggers for freshness + incremental `GET /orders` / `GET /charges` / `GET /subscriptions` pulls (date-filtered) as source of truth. Attribute funnels/upsells/affiliates via `funnel_id`, `upsell_id`, `affiliate_id`.
- **Dunning watch**: poll `GET /failed-charges` daily + subscribe to `Subscription Delinquent`/`Recovered` triggers; alert on delinquency spikes before churn compounds.
- **Access provisioning**: `Product Purchased` webhook → verify via API → grant; `Subscription Canceled`/`Completed` → revoke. Never grant on the unsigned payload alone.
- **Migration off SamCart**: recurring payment methods don't port — the card tokens live with SamCart's processor arrangement. Export customers/subscriptions via API, then re-consent buyers on the new platform (see `/sales-subscription-billing` for don't-double-bill mechanics). Plan this before building large recurring revenue on the platform.
