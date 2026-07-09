---
name: sales-wpfunnels
description: "WPFunnels (getwpfunnels.com) platform help — WordPress sales-funnel builder plugin for WooCommerce: visual funnel canvas, order bumps, one-click upsells/downsells, A/B testing, abandoned-cart recovery, conditional steps, lead capture, and analytics, plus bundled Mail Mint email automation. Self-hosted WordPress only — no hosted REST API; the developer surface is per-funnel outbound webhooks (All-Fields or Select-Fields body; no documented event names, payload schema, or HMAC), Mail Mint event triggers, WooCommerce order hooks/REST, and WordPress hooks; page builders Elementor/Gutenberg/Divi/Bricks/Oxygen. Use when sending funnel data to an endpoint or Zapier via webhook, wiring post-purchase upsells/order bumps, recovering abandoned carts, triggering Mail Mint flows, reading funnel orders via WooCommerce, or choosing Free vs Pro. Do NOT use for funnel/CRO strategy across tools (use /sales-funnel), generic iPaaS wiring (use /sales-integration), or checkout-conversion strategy (use /sales-checkout)."
argument-hint: "[describe what you need help with in WPFunnels]"
license: MIT
version: 1.0.0
tags: [sales, funnel, wordpress, platform]
---

# WPFunnels Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Send funnel data (leads/orders) to your own endpoint or Zapier via webhook
   - B) Build post-purchase one-click upsells/downsells and order bumps (WooCommerce)
   - C) Recover abandoned carts / trigger Mail Mint email flows on funnel events
   - D) Read funnel revenue/orders programmatically (via WooCommerce)
   - E) A/B test funnel steps, add conditional/personalized journeys
   - F) Decide Free vs Pro, or which page builder to design steps in

2. **Code or no-code?** Your own endpoint → per-funnel webhooks. No endpoint → Zapier (via webhook), Mail Mint (bundled email), or WooCommerce hooks for orders.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Funnel / CRO **strategy** across tools (which builder, funnel design) | `/sales-funnel {question}` |
| Checkout/cart **conversion** strategy across platforms | `/sales-checkout {question}` |
| Connecting WPFunnels to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |
| Email sequences / nurture beyond Mail Mint basics | `/sales-email-marketing {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-funnel design a post-purchase upsell flow`".

## Step 3 — WPFunnels platform reference

**Read `references/platform-guide.md`** for the full reference — the funnel/step model (what's webhook vs WooCommerce vs UI-only), Free-vs-Pro gating and best-effort pricing, the lead/order data model, and quick-start recipes (receive a funnel webhook; read orders via WooCommerce; trigger a Mail Mint flow).

**Read `references/wpfunnels-api-reference.md`** for the integration surface — WPFunnels is **WordPress-only (no REST API)**: per-funnel **webhooks** (funnel canvas → three-dot → Webhook → Add Webhook; fields Name/Request URL/Method/Format/Event; body **All Fields** or **Select Fields**; **no documented event names, payload schema, or HMAC**), **Mail Mint** event triggers, **WooCommerce** order hooks/REST for the underlying orders, and **WordPress hooks**.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Webhooks are per-funnel and undocumented in payload.** Set them up from the **funnel canvas → three-dot → Webhook**. Since the docs don't publish event names or the payload schema, use **Select Fields** to pin the exact keys your endpoint needs, and capture a test delivery (webhook.site) before coding.
- **No documented HMAC.** Treat the Request URL as a secret; if your endpoint supports it, add verification on a value you send in Select Fields, and dedupe on email + funnel/order id.
- **Read money through WooCommerce, not WPFunnels.** Order bumps and one-click upsells/downsells are **WooCommerce orders** — the most reliable programmatic read of funnel revenue is the **WooCommerce REST API / order webhooks**, not a WPFunnels API (there isn't one).
- **Email can stay in WordPress via Mail Mint.** Funnel **Event triggers** start Mail Mint automations (welcome, abandoned-cart, post-purchase). Use it instead of routing to a third-party ESP if you want email inside WP; otherwise webhook/Zapier to your ESP.
- **It's a WordPress plugin.** No SaaS API or MCP — you need a self-hosted WordPress + WooCommerce site. Design steps in your page builder (Elementor/Gutenberg/Divi/Bricks/Oxygen).
- **Pro gates the good parts.** Webhooks, one-click upsells, A/B testing, conditional steps and order bumps are **Pro**; the free plugin builds basic funnels. Confirm current Pro pricing on the site (best-effort).

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — pricing/feature specifics verified against the marketing site, docs, and comparison articles; confirm in-account.*

1. **Webhook payload/events aren't documented.** The setup UI (Name/Request URL/Method/Format/Event, All/Select Fields) is documented, but **not** the event names or payload fields — capture a live delivery before relying on the shape.
2. **No documented webhook HMAC.** Secure the Request URL as a secret and dedupe; there's no published signature to verify.
3. **WordPress + WooCommerce required.** No hosted API/MCP; everything runs on your self-hosted site, and commerce features need WooCommerce.
4. **Revenue lives in WooCommerce.** For reliable order/upsell data, use the WooCommerce REST API / order webhooks, not WPFunnels (which has no read API).
5. **Pro-gated features.** Webhooks, one-click upsells/downsells, A/B testing, conditional steps need **Pro** — the free version is basic. Pricing is best-effort; verify.
6. **Mail Mint is a separate (bundled) tool.** Email automation is Mail Mint, not WPFunnels itself — its list/automation model is its own; for advanced sequences compare via `/sales-email-marketing`.
7. **Page builder matters for design.** Steps render through your builder (Elementor/Gutenberg/Divi/Bricks/Oxygen); template availability and styling depend on it.

## Related skills

- `/sales-funnel` — Sales-funnel / CRO strategy across tools (WPFunnels is one of the WordPress funnel builders covered) — funnel design, tool selection vs CartFlows/FunnelKit
- `/sales-checkout` — Checkout/cart conversion (order bumps, one-click upsells) across platforms
- `/sales-integration` — Connecting WPFunnels to a CRM/ESP via webhooks/Zapier/WooCommerce
- `/sales-email-marketing` — Email sequences beyond Mail Mint basics for the leads you capture
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Send funnel leads to my own endpoint via webhook (developer/automation)
**User says**: "When someone opts into my WPFunnels funnel, how do I POST their email to my own API?"
**Skill does**: Walks Recipe 1 — on the **funnel canvas**, three-dot → **Webhook** → **Add Webhook**, set **Request URL** + **Method=POST** + **Format**, pick the opt-in **Webhook Event**, and choose **Select Fields** to send exactly `email`/name/`funnel_id`. Warns the **payload schema isn't documented** (capture via webhook.site) and there's **no HMAC** (secret URL + dedupe). Notes Zapier as the no-code alternative and Mail Mint if email should stay in WordPress.
**Result**: Leads POST to the user's endpoint with a known, pinned payload.

### Example 2: Build a post-purchase one-click upsell
**User says**: "I want to offer a one-click upsell after checkout in WooCommerce."
**Skill does**: Explains WPFunnels **Pro** one-click upsells/downsells add a post-purchase offer charged to the original WooCommerce order (no re-entering card). Points to the funnel canvas to add the upsell step, A/B test the offer, and read results via the **WooCommerce REST API/order webhooks** (since WPFunnels has no read API). Routes broader AOV strategy: "run: `/sales-checkout maximize average order value with order bumps and upsells`."
**Result**: A working post-purchase upsell with a reliable way to read the orders.

### Example 3: Free vs Pro — what do I actually need?
**User says**: "Is the free WPFunnels enough, or do I need Pro?"
**Skill does**: Maps features to tiers — free builds basic funnels; **Pro** unlocks webhooks, one-click upsells/downsells, order bumps, A/B testing, and conditional steps. Frames pricing as best-effort (verify on site) and notes it needs WooCommerce + a page builder. Compares positioning vs CartFlows/FunnelKit and routes the tool-selection decision: "run: `/sales-funnel choose a WordPress funnel builder`."
**Result**: User picks the right tier and knows the prerequisites.

## Troubleshooting

### My webhook fires but the data isn't what I expected
**Symptom**: The receiving endpoint gets a payload with unexpected or missing fields.
**Cause**: WPFunnels doesn't publish the webhook payload schema or event names, and **All Fields** sends the complete (variable) funnel dataset.
**Solution**: Switch the webhook **Request Body** to **Select Fields** and pick exactly the keys your endpoint needs, then capture one real delivery (e.g. webhook.site) to confirm names/format. Recreate the endpoint mapping from that sample. Verify you attached the webhook to the correct **Webhook Event** on that funnel.

### My one-click upsell / order bump isn't working
**Symptom**: Post-purchase upsell doesn't appear or doesn't charge.
**Cause**: One-click upsells/downsells and order bumps are **Pro** features and require **WooCommerce** with a compatible payment gateway that supports post-purchase charges.
**Solution**: Confirm you're on WPFunnels **Pro**, WooCommerce is active, and your gateway supports one-click/post-purchase charges. Rebuild the upsell step on the funnel canvas and test a full checkout. For AOV strategy across tools, use `/sales-checkout`.

### I can't find a WPFunnels API to read my funnel orders
**Symptom**: Looking for a REST endpoint to pull funnel revenue/contacts.
**Cause**: WPFunnels is a WordPress plugin with **no hosted REST API** — there's no `api.wpfunnels.com`.
**Solution**: Read the underlying orders via the **WooCommerce REST API / order webhooks** (order bumps and upsells are WooCommerce orders), capture leads via the funnel **webhook** or **Mail Mint**, and use **WordPress hooks** for server-side PHP. For generic iPaaS wiring, use `/sales-integration`.
