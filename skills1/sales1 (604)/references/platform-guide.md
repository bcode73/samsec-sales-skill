# ThriveCart Platform Reference

## Overview

ThriveCart (thrivecart.com) is a **checkout/cart platform for creators** selling digital products, courses,
and subscriptions — known for **lifetime (one-time) pricing** and strong conversion tooling (order bumps,
1-click upsells/downsells, A/B testing). Best for creators who want to *own* a high-converting cart instead
of paying a monthly cart fee. Watch-outs: the "lifetime" deal now has a **$295/yr Pro+ renewal** for key
features, **ThriveCart Learn is being deprecated**, and there's **no download protection**.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Checkout / cart | Hosted/embedded pages, 100+ countries, 1 click | UI build; purchases fire **webhooks** |
| Order bumps | Add-on offer at checkout (1 on Standard, multiple Pro+) | UI; bump events via webhook |
| 1-click upsells/downsells | Post-purchase funnel offers | UI; upsell/downsell webhook events |
| A/B testing | Split-test carts | **UI-only** |
| Subscriptions + dunning | Recurring billing; failed-payment recovery (**Pro+**) | `order.subscription_*` webhooks |
| Affiliate Center | Built-in affiliates + automated payouts (**Pro+**) | `affiliate.*` webhooks; REST read |
| ThriveCart Learn (LMS) | Course hosting — **being deprecated → ThriveAcademy** | UI; grant access via webhook→your LMS |
| Abandon-cart recovery | Email failed/abandoned checkouts | UI; abandoned-cart webhook |
| REST API | Read products/orders/customers/affiliates | **API** (token/OAuth, 60/min) |

**Programmatic interfaces:** **webhooks** (standard = all events; **Event Subscription API** = targeted),
**REST API** (token auth, OAuth for apps, 60 req/min), **PHP SDK**, Zapier + 100+ integrations. **No MCP**;
no native HMAC (webhook auth is a shared **secret**). See `references/thrivecart-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on the live pricing page; the "lifetime" model changed in 2025.*

| Plan | Cost | Notable |
|---|---|---|
| Standard | **$495 one-time** | unlimited products/funnels, upsells/downsells, A/B, abandon-cart, subscriptions |
| Pro+ | **$790 one-time + $295/yr (from year 2)** | **affiliate center, sales tax, custom checkout domain, dunning, advanced reporting** |
| Ultimate | **$985 one-time + $295/yr** | everything + extras (Learn+/ThriveAcademy bundle) |

- **"Lifetime" has an asterisk:** the big creator features (affiliates, tax, dunning, custom domain) live on
  **Pro+**, which **renews at $295/yr** — model that, not just the headline one-time price.
- **Standard is genuinely one-time** but minimal for a serious creator (no affiliates/tax/dunning).
- **ThriveCart Learn / Learn+ are deprecated** (no new features) — **ThriveAcademy** is the replacement;
  don't build new course delivery on Learn.

## Integrations

- **Direction:** ThriveCart is the system of record for the *sale*; it **pushes** purchase/subscription/
  affiliate events out via webhooks, and you **read** history via the REST API. Grant access in your app
  off `order.success`.
- **Auth:** API token (your account) or OAuth (apps); webhook authenticity = the shared `thrivecart_secret`.
- **iPaaS/native:** Zapier + 100+ direct integrations (ActiveCampaign, Kit/ConvertKit, Mailchimp, HubSpot,
  Kajabi, WordPress). Payments via Stripe/PayPal/ThrivePay.

## Data model

Identity is **email**. Key objects: order, customer, product, subscription, affiliate.

**Order webhook (order.success)** <!-- Constructed — verify against a live delivery -->
```json
{ "event": "order.success", "thrivecart_account": "yourname", "thrivecart_secret": "•••",
  "order_id": 123456, "customer": { "email": "buyer@example.com", "name": "Sam" },
  "base_product": 7, "base_product_name": "Pro Course", "order": { "total": "49.00", "currency": "USD" } }
```

**Subscription event** <!-- Constructed — verify -->
```json
{ "event": "order.subscription_cancelled", "order_id": 123456,
  "customer": { "email": "buyer@example.com" }, "subscription": { "id": "sub_abc", "status": "cancelled" } }
```

## Quick-start recipes

### Recipe 1 — Grant course/product access on purchase (webhook)

**Trigger:** `order.success` webhook → verify the secret, then grant access in your app/LMS by email +
`base_product`; on `order.subscription_cancelled` / `order.refund`, revoke.
```python
from flask import request, abort
def hook():
    d = request.form or request.get_json(silent=True) or {}
    if d.get("thrivecart_secret") != SECRET: abort(401)
    if d["event"] == "order.success":
        grant_access(d["customer"]["email"], d.get("base_product"))
    elif d["event"] in ("order.subscription_cancelled", "order.refund"):
        revoke(d["customer"]["email"])
    return "", 200
```
**Gotchas:** there's **no HMAC** — validate the shared `thrivecart_secret` on every call; dedupe on
`order_id` (events can repeat); match offers by **product id**, not name. Prefer the **Event Subscription
API** if you only want `order.success`.

### Recipe 2 — Send purchases to a CRM/ESP (no code, Zapier)

**Trigger:** ThriveCart "Product purchased" Zap (or webhook) → create/update a contact + tag in
HubSpot/Kit/Mailchimp. Use this when you don't want to host an endpoint; ThriveCart has 100+ native
integrations too.

### Recipe 3 — Reconcile orders via the REST API

**Trigger:** scheduled job → pull orders/transactions with a token (`Authorization: Bearer`), reconcile
against your DB to catch any missed webhooks. Respect the **60 req/min** limit; generate exact calls from
`apidocs.thrivecart.com` or the PHP SDK.

## Integration patterns

- **Webhooks are the spine.** Grant/revoke off `order.success` / `order.refund` / `order.subscription_*`;
  validate the secret, dedupe on `order_id`, and **reconcile via the REST API** for missed events.
- **Gate access in YOUR app** if you need real protection — ThriveCart has **no download/link protection**,
  so delivering a raw file link lets customers share it freely.
- **Don't build on Learn.** It's deprecated; deliver courses via ThriveAcademy or grant access to an external
  LMS (Kajabi/Teachable/etc.) off the purchase webhook.
- **Budget the renewal.** If you need affiliates/tax/dunning/custom-domain, you're on **Pro+** at $295/yr —
  factor it into "lifetime."
- **Match on product id.** Product names change; the numeric `base_product` (and bump/upsell ids) are stable.
