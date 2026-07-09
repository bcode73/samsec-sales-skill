---
name: sales-foxy
description: "Foxy (foxy.io) platform help — hosted cart/checkout layer that bolts commerce onto any site or CMS (Webflow, WordPress, Squarespace, Wix, Framer): add-to-cart links/forms on your pages, Foxy hosts the cart, customizable checkout, and receipt; physical/digital/subscription/donation products via 100+ gateways. Automation through the hAPI (hypermedia REST API at api.foxy.io, OAuth 2.0, HATEOAS link relations, official SDKs), HMAC-signed JSON webhooks with documented retries, and HMAC cart-link signing to stop price tampering. Use when securing add-to-cart links/forms so buyers can't edit prices, verifying Foxy-Webhook-Signature payloads, a webhook auto-deactivated after repeated failures, syncing transactions/subscriptions into a CRM via the hAPI, or the cart/checkout looks mismatched with your Webflow site. Do NOT use for cart-platform selection or checkout strategy (use /sales-checkout) or JAMstack markup-defined carts (use /sales-snipcart)."
argument-hint: "[describe what you need help with in Foxy]"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/Foxy"
---

# Foxy Platform Help

Foxy (foxy.io, formerly FoxyCart) is a hosted cart/checkout layer: your site keeps the product pages, Foxy hosts the cart, checkout, and receipt. Products live in add-to-cart links/forms secured by **HMAC signing**; automation runs through a hypermedia REST API (hAPI, OAuth 2.0) and HMAC-signed webhooks with real retry semantics. The go-to when a Webflow/builder site outgrows native ecommerce.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Add Foxy to a site (Webflow/WordPress/Squarespace/Wix/Framer/custom)
   - B) Secure products — HMAC-sign add-to-cart links/forms
   - C) Integrate transactions/subscriptions with a CRM/fulfillment (hAPI, webhooks)
   - D) Style the cart/checkout to match the site (template sets)
   - E) Understand pricing (plan + 1% capped per-transaction fee)

2. **Do you have a build step or serverless functions?** Link signing needs one (SDK signer at build time, or a deployed signer function).

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/checkout platform to pick (Foxy vs Snipcart/Ecwid/Shopify Buy Button) | `/sales-checkout {question}` |
| JAMstack carts with crawler validation (Snipcart) | `/sales-snipcart {question}` |
| Widget-store platforms (Ecwid) | `/sales-ecwid {question}` |
| Checkout-conversion strategy across tools | `/sales-checkout {question}` |
| Subscription billing strategy / migrating subscribers | `/sales-subscription-billing {question}` |
| Tax / Merchant-of-Record obligations | `/sales-merchant-of-record {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer Foxy-specific questions directly using Step 3.

## Step 3 — Foxy platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing, data model, and quick-start recipes (HMAC webhook verification, build-time link signing, hAPI transaction pulls).

For raw hAPI detail, webhook events/headers/retry semantics, and the signing model, read `references/foxy-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat HMAC link/form signing as mandatory, not optional** — unsigned add-to-cart links let buyers edit `price=` in the URL. Sign at build time with the official SDK (`@foxy.io/sdk` Signer) or deploy a pre-built serverless signer; never put the store secret in the browser. When explaining the model, note it works on fully static/CDN pages with nothing to crawl — the alternative to Snipcart's crawler validation, which needs server-fetchable product URLs.
- **Verify webhooks by HMAC-SHA256 of the RAW body** (hex digest, webhook encryption key, constant-time compare against `Foxy-Webhook-Signature`) — and reply 200 within a minute.
- **Watch for webhook auto-deactivation**: Foxy retries 11 more times over an hour, then **deactivates the webhook after 12 consecutive failures** — monitor deactivation and replay missed events with admin refeed (`Foxy-Webhook-Refeed: true`).
- **Code against hAPI link relations, not hardcoded URLs** — it's a HATEOAS API; follow `fx:transactions`/`fx:subscriptions` links and use `zoom` to embed related data; let the SDK handle OAuth token refresh.
- **Style Foxy's templates to match the host site** — cart/checkout/receipt are Foxy-hosted and will look mismatched out of the box (the top Webflow-user complaint); budget template work and expect to run two dashboards.
- **Quote pricing as plan fee + 1% per transaction (min 5¢, capped ~7.5–35¢ by plan) plus gateway fees, flagged best-effort** — point the user to foxy.io/pricing; the caps make Foxy cheaper than uncapped 2% carts at higher basket sizes.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially pricing tiers (sources conflict) and the beta admin UI status.*

- **Unsigned links = editable prices.** HMAC product verification is the security model; a prototype without it ships a price-tampering hole.
- **12 consecutive webhook failures silently deactivate the webhook** — a flaky endpoint doesn't just miss events, it turns the firehose off. Alert on deactivation; refeed to recover.
- **The admin UI is dated** ("circa 2008" per reviews) with a new dashboard in beta — and Foxy is a **second dashboard** next to your site builder's; factor the ops overhead.
- **Cart/checkout/receipt are Foxy-hosted pages** styled via template sets — they don't inherit your site's design; unstyled they read as a different product mid-purchase.
- **Deep customization, thin guidance** — reviewers report feeling "lost in the woods" among options; start from the Webflow/builder getting-started guides and change one template at a time.
- **Not a Merchant of Record** — you own tax obligations; gateway fees are additional to Foxy's fee.

## Related skills

- `/sales-checkout` — Cart/checkout platform selection (Foxy vs Snipcart vs Ecwid vs Shopify Buy Button) and conversion strategy
- `/sales-snipcart` — Snipcart platform help (the crawler-validation alternative for JAMstack markup-defined products)
- `/sales-ecwid` — Ecwid platform help (the widget-store alternative with a hosted storefront UI)
- `/sales-subscription-billing` — Recurring billing strategy and subscriber migration across platforms
- `/sales-merchant-of-record` — Tax/VAT handling (Foxy is not a Merchant of Record)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Lock down add-to-cart links (developer/automation)
**User says**: "I realized customers can change the price in my Foxy add-to-cart URL before checkout. How do I stop that?"
**Skill does**: Explains HMAC product verification — every product parameter gets signed with the store secret so the cart rejects tampered values — and applies Recipe 2: sign links/forms at build time with `@foxy.io/sdk`'s Signer (or deploy Foxy's pre-built serverless signer for no-build sites), keeping the secret server-side.
**Result**: Tampered links are rejected at the cart; prices are enforceable again.

### Example 2: Webhook-driven fulfillment that survives failures
**User says**: "Sync every completed Foxy order into our warehouse — and last month our webhook just stopped firing."
**Skill does**: Sets up the `transaction/created` JSON webhook, verifies `Foxy-Webhook-Signature` (HMAC-SHA256 hex of the raw body, constant-time compare), returns 200 fast — then explains the stoppage: 12 consecutive failures auto-deactivate the webhook. Adds deactivation monitoring, admin refeed for the gap, and an hAPI reconciliation pull.
**Result**: Verified, monitored order sync with a documented recovery path.

### Example 3: Webflow store outgrowing native ecommerce
**User says**: "Webflow Ecommerce only gives me Stripe and PayPal and no real subscriptions — is Foxy the answer?"
**Skill does**: Maps the fit — Foxy adds 100+ gateways, any-frequency subscriptions, donations, and configurable products on top of the existing Webflow site — while flagging the trade-offs from reviews (separately-styled checkout needing template work, a dated second dashboard, learning curve) and the pricing shape (plan + 1% capped per transaction, best-effort — verify at foxy.io/pricing). Routes a broader platform comparison to `/sales-checkout`.
**Result**: User decides with the real trade-offs, not just the feature list.

## Troubleshooting

### Webhook stopped delivering entirely
**Symptom**: Events flowed for months, then nothing.
**Cause**: The endpoint failed 12 consecutive deliveries (non-200 or >1-minute responses) and Foxy auto-deactivated the webhook.
**Solution**: Fix the endpoint (fast 200, verify against the raw body), re-enable the webhook, and replay the gap via admin refeed — refeeds arrive with `Foxy-Webhook-Refeed: true`. Add monitoring so deactivation pages you.

### Signature verification fails on every webhook
**Symptom**: Computed HMAC never matches `Foxy-Webhook-Signature`.
**Cause**: Hashing a re-serialized/parsed body instead of the raw bytes, using the wrong key (it's the webhook's **encryption key**, not an API token), or comparing against a base64 digest when Foxy sends **hex**.
**Solution**: HMAC-SHA256 the raw request body with the webhook encryption key, hex-encode, `hmac.compare_digest` — Recipe 1 in the platform guide.

### Checkout looks nothing like my site
**Symptom**: Buyers hit a cart/checkout that visually breaks from the Webflow design.
**Cause**: Cart, checkout, and receipt are Foxy-hosted pages with their own template sets — they don't inherit the host site's styles.
**Solution**: Customize the template sets (colors, fonts, layout) to match the site; start from Foxy's builder-specific guides and iterate one template at a time. Budget this styling work into any Foxy adoption estimate.
