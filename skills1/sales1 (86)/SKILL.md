---
name: sales-cartflows
description: "CartFlows (cartflows.com) platform help — WordPress/WooCommerce sales-funnel & checkout builder: checkout layouts, custom fields, order bumps, one-click upsells/downsells, and A/B split testing. Self-hosted WordPress only — no hosted REST API and no MCP; automation runs on WP-CLI, personalization + offer-JS shortcodes, WordPress hooks, OttoKit/Zapier, and Cart Abandonment Recovery webhooks, with funnel revenue read from WooCommerce orders. Use when your CartFlows checkout 404s or falls back to the default WooCommerce checkout, a checkout-field or theme plugin conflicts, building one-click upsells/order bumps, sending abandoned-cart events to Zapier via webhook, reading funnel revenue via the WooCommerce API, wiring offer-accepted JS triggers, or choosing CartFlows vs FunnelKit/WPFunnels or Free vs Pro. Do NOT use for funnel/CRO strategy across tools (use /sales-funnel), checkout-conversion strategy across platforms (use /sales-checkout), or generic iPaaS wiring (use /sales-integration)."
argument-hint: "[describe what you need help with in CartFlows]"
license: MIT
version: 1.0.0
tags: [sales, funnel, wordpress, platform]
---

# CartFlows Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Fix a broken funnel — checkout 404 / "Page Not Found", default WooCommerce checkout showing instead of CartFlows, a plugin/theme conflict
   - B) Build/optimize the funnel — checkout layout, custom fields, order bumps, one-click upsells/downsells, A/B test
   - C) Wire automation — offer-accepted/rejected JS triggers, personalization shortcodes, Cart Abandonment Recovery webhook, OttoKit/Zapier
   - D) Read funnel revenue/orders programmatically (via WooCommerce)
   - E) Choose a plan/tool — Free vs Pro vs Suite vs lifetime, or CartFlows vs FunnelKit/WPFunnels

2. **Free or Pro?** Order bumps, one-click upsells/downsells, A/B testing, offer JS triggers (Pro vars), and WP-CLI are **Pro**. The free plugin builds basic funnels only.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Funnel / CRO **strategy** across tools (which builder, funnel design) | `/sales-funnel {question}` |
| Checkout/cart **conversion** strategy across platforms (AOV, order bumps as strategy) | `/sales-checkout {question}` |
| Connecting CartFlows to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |
| Abandoned-cart **email sequence** strategy beyond the recovery plugin | `/sales-email-marketing {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-funnel design a tripwire funnel with a post-purchase upsell`".

## Step 3 — CartFlows platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities + what's WP-CLI/shortcode/hook/webhook vs UI-only, best-effort pricing (plugin tiers vs the Suite vs lifetime), the funnel/step/WooCommerce-order data model, and quick-start recipes (offer-accepted pixel; abandoned-cart webhook to Zapier; read funnel revenue via WooCommerce).

**Read `references/cartflows-api-reference.md`** for the developer surface — **no hosted REST API/MCP**: WP-CLI (`wp cartflows license activate`), personalization shortcodes (`[cartflows_order_fields]`, `[cartflows_url_fields]`), Offer JS triggers/variables (`{{order_id}}`, `{{offer_product_name}}` on Accept/Reject), WordPress filter hooks, Cart Abandonment Recovery webhooks, and reading funnel revenue via the **WooCommerce REST API**.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Checkout-first, no email/CRM.** CartFlows builds funnels + checkout; it does **not** send email or run a CRM (that's the FunnelKit contrast). Wire follow-up via WooCommerce, OttoKit, or Zapier.
- **WooCommerce is the system of record.** Order bumps + one-click upsells are **WooCommerce orders** — read revenue via the **WooCommerce REST API** (`/wp-json/wc/v3/orders`), not a CartFlows endpoint. There is no CartFlows read API.
- **The only first-party push is abandoned-checkout.** Use the **Cart Abandonment Recovery** plugin's webhook (capture a live sample — no published schema/HMAC). For order events, use WooCommerce webhooks.
- **Offer logic lives in JS triggers.** Bind pixels/analytics to **Offer Accepted/Rejected** with the documented `{{...}}` vars; Pro unlocks `{{offer_product_name/qty/price}}`.
- **Most "broken funnel" tickets are config/conflicts.** Confirm the WooCommerce checkout page exists/is assigned and the flow isn't trashed; resolve conflicts by deactivating all but CartFlows + WooCommerce, then re-enabling one by one.
- **It's WordPress-only.** Self-hosted WP + WooCommerce required; no hosted SaaS/MCP. Free plugin exists; advanced funnel features are Pro/Suite-gated (best-effort pricing — verify).

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — pricing/feature specifics verified against the marketing site, developer docs, and comparison articles; confirm in-account.*

1. **No hosted API/MCP.** Programmatic surface = WP-CLI (Pro), shortcodes, WP hooks, OttoKit/Zapier, and the Cart Abandonment Recovery webhook. **Funnel revenue is read from WooCommerce orders.**
2. **Checkout 404 / "Page Not Found"** is the #1 issue — usually the WooCommerce checkout page isn't created/assigned, or the flow was deleted/trashed.
3. **Falls back to default WooCommerce checkout** when the CartFlows checkout isn't active/assigned for the flow — check the flow's checkout step and global checkout setting.
4. **Checkout-field-editor conflicts** — CartFlows has its own field editor; third-party field-editor plugins override or fight it. Pick one.
5. **Pro gates** order bumps, one-click upsells/downsells, A/B testing, the Pro offer-JS vars, and WP-CLI. Free builds basic funnels only.
6. **One-click upsells need a compatible gateway** that supports post-purchase charges (Stripe/PayPal via WooCommerce).
7. **Suite ≠ plugin.** The CartFlows Suite (~$199/yr) bundles 5 products; the standalone Pro plugin is tiered by site count; lifetime deals exist. Sources conflict — verify.

## Related skills

- `/sales-funnel` — Sales-funnel / CRO strategy across tools (CartFlows is one of the WordPress/WooCommerce funnel builders covered) — funnel design, tool selection vs FunnelKit/WPFunnels
- `/sales-checkout` — Checkout/cart conversion strategy (order bumps, one-click upsells, AOV) across platforms
- `/sales-funnelkit` — FunnelKit platform help (the CartFlows rival that bundles a CRM + email/SMS automation; has an Automations REST API)
- `/sales-wpfunnels` — WPFunnels platform help (another WordPress/WooCommerce funnel builder; bundled Mail Mint email)
- `/sales-email-marketing` — Abandoned-cart + post-purchase email sequence strategy beyond the recovery plugin
- `/sales-integration` — Connecting CartFlows/WooCommerce to a CRM/ESP via OttoKit/Zapier/WooCommerce REST/webhooks
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Read funnel revenue via the API (developer/automation)
**User says**: "How do I pull total revenue for one CartFlows funnel into my dashboard via the API?"
**Skill does**: Explains there's **no CartFlows API** — order bumps + upsells are **WooCommerce orders**, so read them via the **WooCommerce REST API** (`GET /wp-json/wc/v3/orders`, Consumer key/secret over HTTPS, `page`/`per_page` pagination, `X-WP-TotalPages` header). Shows the Python loop from Recipe 3 that filters orders by the `_wcf_flow_id` order-meta key, and flags that the meta key should be confirmed on a live order.
**Result**: Funnel revenue flows into the dashboard from WooCommerce.

### Example 2: My checkout shows a 404 / "Page Not Found"
**User says**: "Customers hit a 'Page Not Found' on my CartFlows checkout when they go to pay."
**Skill does**: Walks the top causes — the **WooCommerce Checkout page isn't created/assigned** under WooCommerce settings, a **flow was deleted/trashed**, or a permalink/cache issue. Has them confirm the checkout page, re-save permalinks, verify the flow is published and its checkout step active, then run the deactivate-all-but-CartFlows-&-WooCommerce conflict test if it persists.
**Result**: Checkout resolves to the CartFlows checkout step and completes payment.

### Example 3: Fire a pixel only when an upsell is accepted
**User says**: "I want to track conversions only when someone accepts my one-click upsell, not on the main order."
**Skill does**: Points to the **Offer Accepted** custom-script field on the Upsell step and the `{{...}}` substitution variables (`{{order_id}}`, `{{order_total}}`, and the Pro-only `{{offer_product_name}}`), with a `gtag('event','purchase',...)` snippet, and notes the matching **Offer Rejected** field. Flags that `{{offer_product_*}}` requires Pro.
**Result**: The pixel fires only on accepted upsells.

## Troubleshooting

### My funnel sends buyers to the default WooCommerce checkout
**Symptom**: Clicking buy lands on the standard WooCommerce checkout, not the CartFlows step.
**Cause**: The CartFlows checkout step isn't active/assigned for the flow, or the global checkout override is off.
**Solution**: Open the flow, confirm a **Checkout** step exists and is published, set it as the funnel's checkout, and check CartFlows global settings. Re-save permalinks and clear cache. If it still falls back, run the plugin-conflict test.

### My abandoned-cart webhook isn't sending the fields I expect
**Symptom**: The Zapier/Make webhook fires but fields are missing or unmapped.
**Cause**: The Cart Abandonment Recovery webhook has **no published payload schema or HMAC** — you must map from a live sample.
**Solution**: In WooCommerce → Cart Abandonment → Settings → Webhook, enable it, paste the catch-hook URL, click **Trigger a Sample**, then map fields from the delivered payload. Treat the URL as a secret; use it server-side.

### I can't find a CartFlows API to read my funnel's orders/upsells
**Symptom**: Looking for a CartFlows endpoint for funnel revenue.
**Cause**: There is **no hosted CartFlows API**; the funnel runs on **WooCommerce orders**.
**Solution**: Read order bumps + one-click upsells as **WooCommerce orders** via the **WooCommerce REST API** (`/wp-json/wc/v3/orders`) or WooCommerce order webhooks, filtering by the CartFlows flow order-meta. For AOV strategy across tools, use `/sales-checkout`.
