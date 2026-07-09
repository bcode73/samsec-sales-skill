<!-- Source: https://getwpfunnels.com/docs/wpfunnels-webhooks-support/ and https://getwpfunnels.com (fetched 2026-06) -->
<!-- WPFunnels is a self-hosted WordPress plugin. It has NO general hosted REST API. Its programmatic surface is: per-funnel outbound Webhooks, WordPress action/filter hooks, WooCommerce order hooks, the bundled Mail Mint email-automation engine, and page-builder integrations. The webhook UI fields below are reproduced verbatim from the official docs; the docs do NOT publish event names or a payload schema, so any JSON example is explicitly marked CONSTRUCTED and must be verified against a live delivery. -->

# WPFunnels Developer / Integration Reference

## Nature of the integration surface

WPFunnels runs **inside WordPress** (self-hosted plugin, free on WordPress.org + Pro). There is **no hosted REST API** to create funnels or read entries. Data flows **out** as visitors move through a funnel:

- **Per-funnel outbound Webhooks** (Pro) — POST funnel data to your endpoint / Zapier / an ESP
- **Mail Mint** — the bundled email-automation engine (same vendor) reacts to funnel **Event triggers**
- **WooCommerce** — funnels are built on WooCommerce orders/checkout (so WooCommerce REST API + order hooks apply to the underlying orders)
- **WordPress action/filter hooks** — PHP-side customization
- **Page builders** — Elementor, Gutenberg, Divi, Bricks, Oxygen (UI design, not data)

---

## Webhooks

**Requires:** WPFunnels **Pro** and an existing funnel.

**Set up (verbatim):**
1. Create a sales funnel in WPFunnels Pro.
2. On the **funnel canvas**, click the **three-dot menu** (top-right) → **"Webhook"** to open the webhooks drawer.
3. Click **"Add Webhook"**.
4. Configure these fields:
   - **Name** — identifier for the webhook
   - **Request URL** — destination endpoint
   - **Request Method** — HTTP method (e.g. POST)
   - **Request Format** — data format
   - **Webhook Event** — the trigger action
5. **Request Body** — choose **All Fields** (send complete funnel data) or **Select Fields** (send specific fields only).
6. **Save.**

**Management:** from the **Webhooks List** you can toggle status, edit, or delete. You can add **multiple webhooks per funnel**.

**Purpose:** send funnel data to automation tools like **Zapier** and most **email clients** based on user actions in the funnel.

> ⚠️ **Not documented:** the official docs do **not** publish the individual **Webhook Event** names, the **payload schema/fields**, custom-header support, signature/**HMAC** verification, or rate limits. Capture the actual payload with a test endpoint (e.g. webhook.site) before coding against it.

**CONSTRUCTED example** (illustrative only — built from the funnel/lead concept since the docs publish no payload; verify against a live delivery):

```json
{
  "funnel_id": "12",
  "funnel_name": "Spring Upsell Funnel",
  "step": "optin",
  "event": "lead_captured",
  "contact": {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com"
  },
  "order_id": null,
  "created_at": "2026-06-27T10:00:00Z"
}
```

Because the schema isn't published, prefer **Select Fields** to lock the payload to exactly the keys your endpoint expects, and treat the **Request URL** as a secret (no documented HMAC).

---

## Mail Mint (bundled email automation)

WPFunnels integrates with **Mail Mint** (same vendor) for email campaigns and automations. Funnel **Event triggers** start Mail Mint workflows (welcome, abandoned-cart recovery, post-purchase sequences). Mail Mint is a separate plugin with its own list/automation model — use it when you want the email side to live inside WordPress instead of routing to a third-party ESP via webhook/Zapier.

---

## WooCommerce + WordPress hooks

- **WooCommerce** is the commerce engine under WPFunnels funnels (checkout pages, order bumps, one-click upsells/downsells are WooCommerce orders). The **WooCommerce REST API** and WooCommerce **order webhooks/hooks** therefore apply to the resulting orders — often the most reliable programmatic read of funnel revenue.
- **WordPress action/filter hooks:** standard WP plugin hooks let server-side PHP react to funnel events; consult WPFunnels' developer docs for exact hook names (not enumerated in the public webhook doc).

---

## Integrations (UI / native)

- **Page builders:** Elementor, Gutenberg (block editor), Divi, Bricks, Oxygen.
- **eCommerce:** WooCommerce.
- **Email:** Mail Mint (bundled); other ESPs via webhook/Zapier.
- **Automation:** Zapier (via webhooks).
- CRM / form-builder / LMS integration categories are referenced by the vendor but specific partners aren't enumerated in fetched docs.

---

## Funnel mechanics (relevant to integration logic)

- **Funnel canvas:** visual builder for multi-step funnels (landing → checkout → upsell/downsell → thank-you).
- **Order bumps** at checkout; **one-click upsells/downsells** post-purchase (WooCommerce orders).
- **A/B split testing**, **abandoned-cart recovery**, **conditional funnel steps**, **lead-capture forms**, **funnel analytics**.
- **Identity:** email (lead/customer) is the contact key that flows to webhooks/Mail Mint/ESPs.
