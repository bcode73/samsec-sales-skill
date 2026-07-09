# WPFunnels Platform Guide

Full reference for the `sales-wpfunnels` skill. Read the section you need; don't dump the whole file.

> *Pricing/plan gates are best-effort from research (2026-06) — the marketing site, docs, and comparison articles. Verify in-account.*

## What WPFunnels is

A **WordPress sales-funnel builder plugin** for **WooCommerce** — a CartFlows / FunnelKit competitor. You design multi-step funnels on a **visual canvas** (landing → checkout → upsell/downsell → thank-you), add order bumps and one-click post-purchase offers, A/B test, recover abandoned carts, and (via the bundled **Mail Mint**) run email automation. Self-hosted on WordPress. Target users: WooCommerce store owners, digital creators/marketers, agencies, non-technical builders.

**Funnel builder, not a SaaS.** No hosted API; commerce runs on WooCommerce, email on Mail Mint. For funnel *strategy/tool selection* across tools, use `/sales-funnel`.

## Module map — webhook vs WooCommerce vs UI-only

| Module | Surface | Notes |
|---|---|---|
| Funnel canvas / steps | **UI-only** | visual builder; no API to create funnels |
| Landing/checkout/thank-you pages | **UI (page builder)** | Elementor/Gutenberg/Divi/Bricks/Oxygen |
| Order bumps | **WooCommerce (Pro)** | checkout add-on offers → WooCommerce orders |
| One-click upsell/downsell | **WooCommerce (Pro)** | post-purchase, charged to original order |
| A/B split testing | **UI (Pro)** | test steps/offers |
| Lead capture / opt-in | **Webhook + Mail Mint** | contact identity flows out here |
| Abandoned-cart recovery | **Mail Mint / WooCommerce** | event-triggered email |
| Outbound webhooks | **Webhook (Pro)** | per-funnel; Zapier/email/your endpoint |
| Email automation | **Mail Mint** | bundled engine; funnel Event triggers |
| Funnel analytics | **UI** | reporting in dashboard |
| Order/revenue read | **WooCommerce REST/hooks** | most reliable programmatic read |
| Server-side customization | **WordPress hooks** | PHP actions/filters |

## Pricing & plan gates (best-effort)

- **Free** — WPFunnels on WordPress.org; build basic funnels.
- **Pro (paid)** — webhooks, **one-click upsells/downsells**, order bumps, A/B testing, conditional steps, advanced analytics. WPFunnels' exact Pro tiers/prices weren't captured in research (the pricing page references a "Large Bundle" for agencies, 15-day money-back). For reference, peers price around: **FunnelKit** ~$99.50–$399/yr, **CartFlows** ~$79–$449/yr (+ lifetime). Confirm WPFunnels' current Pro pricing on the site.
- Requires **WooCommerce** + a supported **page builder**; a self-hosted WordPress site (not low-tier WordPress.com).

## Data model (lead/order — JSON shapes)

WPFunnels publishes **no** webhook payload schema. Conceptually a funnel webhook carries a **lead/contact** (and, on purchase steps, a reference to the WooCommerce order). CONSTRUCTED illustration (verify against a live delivery; prefer **Select Fields** to pin keys):

```json
{
  "funnel_id": "12",
  "funnel_name": "Spring Upsell Funnel",
  "step": "optin",
  "event": "lead_captured",
  "contact": { "first_name": "Jane", "last_name": "Smith", "email": "jane@example.com" },
  "order_id": null
}
```

The authoritative **order/revenue** shape is the **WooCommerce order** object (read via the WooCommerce REST API / order webhooks) — order bumps and upsells are WooCommerce line items on the order.

## Quick-start recipes

### Recipe 1 — Send funnel leads to your endpoint (webhook)

On the **funnel canvas → three-dot menu → Webhook → Add Webhook**: set **Name**, **Request URL**, **Request Method = POST**, **Request Format**, the opt-in **Webhook Event**, and **Request Body = Select Fields** (pin `email`, name, `funnel_id`).

```python
@app.post("/wpfunnels-webhook")
def wpfunnels_webhook(payload: dict):
    # No documented HMAC — keep this URL secret; verify a token you put in Select Fields if possible.
    email = payload.get("email") or payload.get("contact", {}).get("email")
    if not email:
        return Response(status_code=400)
    key = (email, payload.get("funnel_id"))      # idempotency
    if not already_processed(key):
        upsert_lead(email=email, funnel=payload.get("funnel_name"))
        mark_processed(key)
    return {"ok": True}
```

Because the schema is undocumented, capture one real delivery (webhook.site) and map from that. No endpoint? Point the webhook at **Zapier**, or use **Mail Mint** to keep email in WordPress.

### Recipe 2 — Read funnel revenue via WooCommerce (not WPFunnels)

WPFunnels has no read API; the orders (incl. order bumps + one-click upsells) are **WooCommerce orders**:

```bash
curl https://yourstore.com/wp-json/wc/v3/orders \
  -u ck_xxx:cs_xxx \
  -G --data-urlencode "after=2026-06-01T00:00:00"
```

Or subscribe to WooCommerce **order.created/updated** webhooks for real-time revenue. This is the reliable way to attribute funnel AOV.

### Recipe 3 — Trigger a Mail Mint email flow on a funnel event (no code)

Install **Mail Mint** (bundled), build an automation whose entry is a funnel **Event trigger** (opt-in, purchase, abandoned cart), and add the email steps (welcome, recovery, post-purchase). Keeps the email side inside WordPress instead of routing to a third-party ESP. For advanced sequences/deliverability, compare via `/sales-email-marketing` and `/sales-deliverability`.

## When to route out

- Which funnel builder / funnel design across tools → `/sales-funnel`
- AOV / order-bump / upsell **strategy** across platforms → `/sales-checkout`
- Generic CRM/ESP wiring (iPaaS) → `/sales-integration`
- Email sequences beyond Mail Mint basics → `/sales-email-marketing`
