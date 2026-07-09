# Foxy Platform Reference

## Overview

Foxy (foxy.io, formerly FoxyCart — ~20 years in service, $3B+ processed) is a hosted cart/checkout layer: your site keeps the product pages, Foxy hosts the cart, checkout, and receipt. Products are defined in add-to-cart **links and forms**, secured against tampering by **HMAC signing**. Strongest niche: Webflow (and other builder) sites that outgrow native ecommerce — more gateways (100+), subscriptions at any frequency, donations, configurable products. Trade-offs: a dated (beta-refreshing) admin, a second dashboard to run, and cart/checkout styled separately from the host site.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Cart & hosted checkout | Foxy-hosted pages; customizable via template sets (Twig-based) | **UI/template-defined**; hAPI for template sets |
| Products (links/forms) | Defined in your markup: name/price/options as URL/form params, **HMAC-signed** | **Build-time signing** via SDK utilities or serverless signers |
| Transactions | Full order records with embedded items/payments/shipments | **API-accessible** (hAPI) + **webhook-accessible** (`transaction/*`) |
| Subscriptions | Any frequency, self-service management, dunning | **API-accessible** + **webhook-accessible** (`subscription/*`) |
| Customers | Accounts, saved payment, SSO options | **API-accessible** + webhooks |
| Digital goods (downloadables) | Auto-delivery, download tracking/expiry | **API-accessible** |
| Coupons/discounts | Codes, categories | **API-accessible** |
| Webhooks | JSON webhooks, HMAC-signed, 11 retries/hour + auto-deactivate at 12 fails, manual refeed | **API-accessible** (configure via hAPI or admin) |
| Payment gateways | 100+ incl. Stripe, PayPal, Apple Pay, Square, Adyen, iDEAL | **UI-only** config |
| Admin dashboard | Order management (legacy UI + new beta) | UI; everything scriptable via hAPI |

No MCP server found. iPaaS: Zapier (legacy webhook), Webflow-specific webhook, official Node/universal SDKs.

## Pricing, limits & plan gates

*Best-effort (2026-07) — sources conflict on current tiers; verify at foxy.io/pricing.*

- Entry plans reportedly from ~$20–25/mo; **Advanced ~$300/mo** (priority support, first 1,000 transactions included); **Enterprise from ~$2,000/mo**.
- **Per-transaction fee: 1% of sale, minimum 5¢, capped 35¢/25¢/7.5¢ depending on plan** — effectively a flat cap per order at real basket sizes (a $100 sale = 25–35¢, not $1), which at volume undercuts Snipcart's uncapped 2%.
- Unlimited free trial (no card). Payment-gateway fees are separate and additional.

## Integrations

Site builders: Webflow (flagship), WordPress, Squarespace, Wix, Framer, Webstudio, any HTML site — via links/embeds. Data flows: products IN from your signed markup; transactions/subscriptions OUT via hAPI + webhooks; merchant-side affiliate/referral tools (ReferralCandy, Post Affiliate Pro, OSI Affiliate, Monto) connect via integrations.

## Data model

Store → Transactions (embedded items, payments, shipments, addresses) → Customers (accounts, subscriptions) → Subscriptions (recurring transactions). Products have no server-side catalog by default — they're parameters in your signed links/forms; `downloadables` and coupon/category resources live server-side.

```json
// Webhook payload core (hAPI-shaped, embedded resources trimmed)
{
  "id": 123456789, "store_version_uid": "…",
  "customer_first_name": "Jane", "customer_email": "jane@example.com",
  "total_order": 54.99, "currency_code": "USD", "status": "completed",
  "_embedded": { "fx:items": [{ "name": "Classic Tee", "price": 25.0, "quantity": 1 }] }
}
```
<!-- Constructed from docs descriptions of the hAPI payload structure — verify against a live webhook -->

## Quick-start recipes

### Recipe 1 — Verify a Foxy webhook and sync the transaction (Python/Flask)

```python
import hmac, hashlib, os
from flask import Flask, request, abort

app = Flask(__name__)

@app.post("/hooks/foxy")
def foxy_hook():
    raw = request.get_data()                       # RAW body — sign before parsing
    digest = hmac.new(os.environ["FOXY_WEBHOOK_KEY"].encode(),
                      raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(request.headers.get("Foxy-Webhook-Signature", ""), digest):
        abort(401)
    event = request.headers.get("Foxy-Webhook-Event", "")
    payload = request.get_json(force=True)
    if event == "transaction/created":
        pass  # upsert payload into CRM/warehouse; _embedded['fx:items'] has line items
    return "", 200                                  # respond within 1 minute
```

Gotchas: sign the **raw body** with the webhook's **encryption key** (hex digest, constant-time compare); reply 200 within a minute or Foxy retries (11 more times over an hour) and **deactivates the webhook after 12 straight failures** — monitor for deactivation and use admin **refeed** to replay missed events (`Foxy-Webhook-Refeed: true`).

### Recipe 2 — Sign an add-to-cart link at build time (Node)

```javascript
// npm i @foxy.io/sdk  — signing utility prevents price tampering
import { Signer } from "@foxy.io/sdk/backend";

const signer = new Signer(process.env.FOXY_STORE_SECRET);
// Sign a whole HTML fragment (links + forms) during your static build:
const signedHtml = signer.htmlString(rawProductHtml);
// Or sign one URL:
const signedUrl = signer.url("https://yourstore.foxycart.com/cart?name=Classic%20Tee&price=25&code=tee-001");
```

Gotchas: unsigned links let buyers edit `price=` — treat signing as mandatory for anything beyond a prototype. For static sites without a build step, deploy a pre-built serverless signer (Foxy publishes Netlify functions). Keep the store secret out of the browser.

### Recipe 3 — Pull transactions via the hAPI (cURL)

```bash
# 1. Get a token with your OAuth client (client_credentials / refresh_token flow)
# 2. Discover and follow links:
curl "https://api.foxycart.com" -H "Authorization: Bearer $TOKEN" -H "FOXY-API-VERSION: 1"
# follow fx:store → fx:transactions with paging params:
curl "$TRANSACTIONS_URL?limit=100&offset=0&zoom=items" \
  -H "Authorization: Bearer $TOKEN" -H "FOXY-API-VERSION: 1"
```

Gotchas: code against **link relations**, not hardcoded URLs (HATEOAS); use `zoom` to embed related resources in one call; let the official SDK manage token refresh.

## Integration patterns

- **Webflow + Foxy**: Webflow owns pages/CMS; Foxy owns cart/checkout/receipt — style Foxy's templates to match the site or the checkout will look like a different product (top review complaint). Budget for running two dashboards.
- **Fulfillment/CRM sync**: `transaction/created` webhook (HMAC-verified) as trigger — payloads embed full order data so a re-fetch is usually unnecessary; hAPI paging as reconciliation; watch for webhook auto-deactivation.
- **Static/CDN sites**: HMAC link-signing works with no crawlable endpoint — the alternative model to Snipcart's crawler; pick by whether your build can sign (Foxy) or your products are fetchable server-side (Snipcart).
- **Subscriptions**: `subscription/*` webhooks drive provisioning; customers self-serve frequency/payment changes on Foxy-hosted pages.
