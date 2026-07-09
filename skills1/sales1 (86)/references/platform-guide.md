# CartFlows Platform Reference

## Overview

CartFlows (cartflows.com, by **Brainstorm Force** — makers of Astra/Spectra) is a **sales-funnel and checkout builder for WordPress + WooCommerce** — 200,000+ active installs, 4.8★. It replaces the default WooCommerce checkout with conversion-optimized layouts and adds funnel steps (landing → checkout → upsell/downsell → thank-you) you design in your own page builder. It is **checkout-first and lean** — no built-in email/CRM (its main contrast vs FunnelKit, which bundles automation).

## Capabilities & automation surface

| Capability | What it does | Automation tag |
|---|---|---|
| **Funnel + steps** (`cartflows_flow` / `cartflows_step` CPTs) | Multi-step funnels: landing, checkout, upsell, downsell, opt-in, thank-you | UI-built; CPTs queryable via WP-CLI / WP_Query |
| **Checkout layouts** | One/two-column, multi-step, instant checkout; custom checkout-field editor | UI-only |
| **Dynamic order bumps** | Rule-based bumps (by cart contents/total) with modern styles | UI-built; result = WooCommerce order line |
| **One-click upsells/downsells** | Post-purchase offers charged to the original WooCommerce order; **Offer Accepted/Rejected JS triggers** | UI-built; **JS triggers** + WooCommerce order |
| **A/B split testing** | Test funnel-page variants, traffic split | UI-only (no test-read API) |
| **Personalization shortcodes** | `[cartflows_order_fields]`, `[cartflows_url_fields]` on funnel steps | Shortcode (template) |
| **Funnel analytics** | Per-step conversions + revenue | UI-only |
| **Cart Abandonment Recovery** (companion plugin) | Abandoned-checkout capture + recovery emails | **Webhook-accessible** + PHP filters |
| **Social pixels** | Meta/Google/Pinterest/Snapchat/TikTok | UI-configured |
| **OttoKit / Zapier** | Automation across 1,000+ apps | iPaaS |
| **License/management** | Pro license activation | **WP-CLI** (`wp cartflows license activate`) |
| **Funnel revenue** | Bumps + upsells | **WooCommerce REST API** (no CartFlows read API) |

**Page builders supported:** Elementor, Divi, Beaver Builder, Bricks, Spectra, Gutenberg.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on cartflows.com; sources conflict on exact numbers.*

- **Free** (WordPress.org): simple funnels + basic checkout — good for getting one funnel live.
- **CartFlows Pro plugin** (annual): **Starter ~$99/yr** (1 site), **Plus ~$199/yr** (3 sites), **Pro ~$299/yr** (30 sites) — *first-year promo; renews higher (~$129/$249/$399)*. Pro tiers differ mainly by **site count**; features are largely identical across them.
- **Lifetime:** Plus ~$699 one-time, Pro ~$999 one-time (30 sites).
- **CartFlows Suite** (~$199/yr, ~69% off): bundles **CartFlows Pro + Modern Cart Pro + Cart Abandonment Recovery Pro + Power Coupons Pro + OttoKit Pro**.
- **14-day money-back guarantee.**

**Plan-gated for integrations:** dynamic order bumps, one-click upsells/downsells, A/B testing, advanced analytics, the **offer JS triggers (Pro)**, and **WP-CLI** all require **Pro**. The free plugin builds basic funnels only. There is **no API plan gate** because there is no hosted API.

## Integrations

- **WooCommerce** (required) — all checkout/order data flows through WooCommerce; read funnel revenue via the **WooCommerce REST API** (bidirectional with WooCommerce, read-only for "funnel" attribution).
- **OttoKit (SureTriggers)** — native CartFlows triggers/actions, 1,000+ apps (bundled in Suite).
- **Zapier / Make / Pabbly** — primarily via the Cart Abandonment Recovery **webhook** (data out) and the WooCommerce app (order data).
- **Payment gateways** — Stripe/PayPal etc. via WooCommerce; one-click upsells require a gateway that supports post-purchase charges.
- **Email/CRM** — none native; connect an ESP/CRM via WooCommerce, OttoKit, or Zapier.

## Data model

CartFlows objects are WordPress posts; money/orders are WooCommerce.

```jsonc
// cartflows_flow (a funnel) — WP post  <!-- Constructed from CPT behavior — verify against live install -->
{
  "ID": 412,
  "post_type": "cartflows_flow",
  "post_title": "Tripwire Funnel",
  "post_status": "publish"
}

// cartflows_step (a step) — WP post, parent = flow
{
  "ID": 418,
  "post_type": "cartflows_step",
  "post_parent": 412,            // the flow ID
  "post_title": "Checkout",
  "step_type": "checkout"        // checkout | upsell | downsell | optin | thankyou | landing
}
```

```jsonc
// WooCommerce order produced by a CartFlows funnel (read via /wp-json/wc/v3/orders/{id})
{
  "id": 9001,
  "status": "completed",
  "total": "67.00",
  "line_items": [
    { "name": "Core Offer", "total": "47.00" },
    { "name": "Order Bump — Toolkit", "total": "20.00" }  // bump = a line item
  ],
  "meta_data": [
    { "key": "_wcf_flow_id", "value": "412" },        // <-- CartFlows attribution
    { "key": "_wcf_checkout_id", "value": "418" }      // <!-- meta keys constructed — verify on a live order -->
  ]
}
```

## Quick-start recipes

### Recipe 1 — Fire a conversion pixel only when a one-click upsell is accepted

**Trigger:** customer clicks "Yes, add this" on an Upsell step.
**Steps:** CartFlows → Funnels → edit funnel → Upsell step → **Custom Script → Offer Accepted** → paste JS using the `{{...}}` substitution variables.

```html
<script>
  gtag('event', 'purchase', {
    transaction_id: '{{order_id}}',
    value: '{{order_total}}',
    items: [{ item_name: '{{offer_product_name}}' }]   // Pro-only var
  });
</script>
```

**Gotcha:** `{{offer_product_name/qty/price}}` are **Pro-only**; free funnels only expose `{{order_id}}`, `{{txn_id}}`, `{{order_total}}`. The matching **Offer Rejected** field fires on decline.

### Recipe 2 — Send abandoned-checkout events to Zapier via webhook

**Trigger:** shopper abandons the CartFlows checkout.
**Steps:**
1. In Zapier, create a Zap with **Webhooks by Zapier → Catch Raw Hook**; copy its URL.
2. **WooCommerce → Cart Abandonment → Settings → Webhook**, enable, paste the URL.
3. Click **Trigger a Sample**, then map fields from the live payload in Zapier (schema isn't published).

```bash
# Inspect the delivered shape (point your own catcher at it first):
curl -X POST https://hooks.zapier.com/hooks/catch/XXX/YYY/ \
  -H "Content-Type: application/json" -d '{}'   # then read what Cart Abandonment actually sent
```

**Gotcha:** there's no documented payload schema or HMAC — always capture a live sample and treat the URL as a secret.

### Recipe 3 — Read funnel revenue from WooCommerce (no CartFlows API)

**Trigger:** nightly revenue sync.
**Steps:** generate WooCommerce REST keys (WooCommerce → Settings → Advanced → REST API), then page through orders and filter by the CartFlows flow meta.

```python
import requests
BASE, AUTH = "https://example.com/wp-json/wc/v3", ("ck_xxx", "cs_xxx")

def funnel_revenue(flow_id):
    page, total = 1, 0.0
    while True:
        r = requests.get(f"{BASE}/orders", auth=AUTH,
                         params={"per_page": 100, "page": page, "status": "completed"})
        r.raise_for_status()
        rows = r.json()
        if not rows: break
        for o in rows:
            meta = {m["key"]: m["value"] for m in o.get("meta_data", [])}
            if str(meta.get("_wcf_flow_id")) == str(flow_id):
                total += float(o["total"])
        if page >= int(r.headers.get("X-WP-TotalPages", 1)): break
        page += 1
    return total
```

**Gotcha:** there is **no CartFlows read API** — funnel revenue *is* WooCommerce order data. Confirm the `_wcf_flow_id` meta key on a real order in your install.

## Integration patterns

- **Read path = WooCommerce.** Treat CartFlows as the funnel UI and WooCommerce as the system of record. Sync orders to a CRM/warehouse via the WooCommerce REST API or WooCommerce order webhooks (`X-WC-Webhook-Signature`, HMAC-SHA256).
- **Event-out = Cart Abandonment webhook.** The only first-party "push" is abandoned-checkout. Everything else is polled from WooCommerce or pushed by OttoKit/Zapier.
- **Offer logic = JS triggers.** Bind pixels/analytics/external calls to Offer Accepted/Rejected with the documented `{{...}}` variables; don't expect a server-side webhook for accept/reject.
- **No hosted API means no rate limits of CartFlows' own** — your limits are WooCommerce/WordPress host limits. Use `per_page=100`, cache, and back off on host 429/503.
