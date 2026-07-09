---
name: sales-printify
description: "Printify platform help — print-on-demand fulfillment via 140+ print providers (1,300+ products, lowest base costs) with a REST API (api.printify.com/v1, official OpenAPI spec), HMAC-signed webhooks, an API sales channel for headless stores, and connectors for Shopify/Etsy/TikTok Shop/Amazon/WooCommerce/Wix. Use when print quality varies between orders and you need to vet or switch print providers, store orders aren't reaching Printify or shipping is slower than promised, a product publish fails or hits the 200-per-30-minute publishing limit, a Printify webhook stopped firing (blocked after failed deliveries), building a headless store that creates products and submits orders via the API, verifying X-Pfy-Signature webhook payloads, hitting 429 rate limits, or deciding whether Printify Premium's ~20% base-cost discount pays off. Do NOT use for choosing between POD providers like Printful/Gelato/Gooten (use /sales-print-on-demand) or digital-product pricing and launch strategy (use /sales-digital-products)."
argument-hint: "[describe what you need help with in Printify]"
license: MIT
version: 1.0.0
tags: [sales, digital-products, platform]
github: "https://github.com/printify"
---

# Printify Platform Help

Printify is a print-on-demand (POD) fulfillment broker: you design products, and Printify routes production to a network of ~141 third-party print providers — the largest catalog (1,300+ products) and lowest base costs in the category, at the price of provider-to-provider variance in quality and speed. It plugs into your storefront (Shopify, Etsy, TikTok Shop, Amazon, WooCommerce, Wix, etc.) or runs headless via its REST API.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Connect Printify to a store (Shopify/Etsy/TikTok Shop/Amazon/WooCommerce/Wix/etc.)
   - B) Build a headless/custom integration via the API (create products, submit orders, webhooks)
   - C) Fix a broken order, sync, publish, or webhook
   - D) Pick a print provider for a product, or fix quality/shipping-speed problems
   - E) Decide on a plan (Free vs Premium) or understand fees/margins

2. **Auth type?** Personal Access Token (single merchant, 1-year expiry) or OAuth 2.0 (platform apps, 6-hour access tokens).

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which POD provider to pick (Printify vs Printful/CustomCat/Gelato/Gooten/SPOD) | `/sales-print-on-demand {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Checkout-page conversion (order bumps, upsells, cart abandonment) | `/sales-checkout {question}` |
| Tax / Merchant-of-Record obligations on merch sales | `/sales-merchant-of-record {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-print-on-demand {original question}`"

Otherwise, answer Printify-specific questions directly using Step 3.

## Step 3 — Printify platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model (blueprint → print provider → variant → product → order), and quick-start recipes (upload + create + publish a product, submit and poll an order, signed shipment webhook listener).

For raw endpoint detail, auth, rate limits, scopes, and webhook payloads, read `references/printify-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **The print provider choice is the product decision.** Same blueprint, different provider = different cost, quality, location, and speed. Compare providers per blueprint via the catalog API and order samples before scaling a bestseller.
- **Variant IDs are per-provider.** A blueprint's variant IDs differ across print providers — always pull them from `GET .../print_providers/{id}/variants.json`, never reuse across providers.
- **Respond 200 to webhooks fast, and keep a polling backup.** 3 failed deliveries block the webhook for an hour and those events are gone. Queue slow work; reconcile with `GET /orders.json`.
- **Model margin before Premium.** Premium (~$29/mo) pays off once ~20% of monthly base-cost spend exceeds the fee (~$145/mo in base costs).

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan-gated features and pricing that may have changed.*

- **Quality varies by provider, not by Printify** — the #1 complaint pattern. A tee from provider A and the "same" tee from provider B can print differently. Vet with sample orders per provider; when a provider degrades, migrate the product to another provider for the same blueprint.
- **Shipping speed ranges 3–12 days domestic** depending on provider location and season — set buyer expectations from the chosen provider's production + shipping estimate, not from a generic promise.
- **You own end-customer support.** Buyers complain to your store, not Printify; reprints/refunds for defects go through Printify support per order, which can be slow — budget response time into your CX.
- **Publishing is rate-limited to 200 per 30 minutes** — bulk catalog pushes must be throttled or they 429. Product creation via order submission is exempt.
- **Personal Access Tokens silently expire after 1 year** — a working integration dies on its anniversary. Calendar the rotation.
- **Catalog endpoints have their own 100 req/min limit** (separate from the 600/min global) and limits are per account, not per token — cache blueprints/variants locally.
- **Custom API-channel products lock during publish** until you call `publishing_succeeded`/`publishing_failed`.

## Related skills

- `/sales-print-on-demand` — Choosing between POD providers (Printful vs Printify vs CustomCat vs Gelato vs Gooten vs SPOD) and multi-provider routing strategy
- `/sales-printful` — Printful platform help (the owns-its-factories alternative: consistent quality, in-house branding, higher base costs)
- `/sales-customcat` — CustomCat platform help (budget US POD: lowest base prices, 1–3 day Detroit production, no private-label branding)
- `/sales-digital-products` — Digital product & merch strategy: pricing, validation, launch
- `/sales-checkout` — Checkout-page optimization for the store that fronts Printify
- `/sales-merchant-of-record` — Tax/VAT handling on merch sales (Printify is not a Merchant of Record)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Print quality suddenly dropped
**User says**: "My Printify mugs were great for months, now customers say the print fades after one wash."
**Skill does**: Explains the provider-network model (quality is per print provider, not per Printify), pulls up how to identify the fulfilling provider on the affected orders, files reprint claims through Printify support, and walks through comparing alternative providers for the same blueprint via `GET /catalog/blueprints/{id}/print_providers.json` + sample orders before migrating the product.
**Result**: User gets defective orders reprinted and moves the product to a better provider with samples verified.

### Example 2: Headless product creation + order flow (developer/automation)
**User says**: "How do I create Printify products from my own app and submit orders when customers buy?"
**Skill does**: Walks through upload (`POST /uploads/images.json`) → product create with per-provider variant IDs and `print_areas` → publish handshake for the API sales channel (`publish` → `publishing_succeeded`), then order submission with `external_id`, shipping calculation, and the signed `order:shipment:created` webhook listener with `X-Pfy-Signature` verification — with the cURL + Python recipes from the platform guide and rate-limit handling (600/min global, 200 publishes/30 min).
**Result**: User has a working headless pipeline with verified webhooks and a polling backup.

### Example 3: Is Premium worth it?
**User says**: "I'm doing about 300 shirt orders a month — should I pay for Printify Premium?"
**Skill does**: Models the decision: Premium ~$29/mo buys up to 20% off base costs, so at ~$8 base per shirt × 300 = $2,400/mo base spend, ~20% saves ~$480/mo — far above the fee. Flags that the discount percentage varies by product and to verify current pricing.
**Result**: User upgrades with a concrete break-even calculation instead of guessing.

## Troubleshooting

### Webhook stopped delivering events
**Symptom**: `order:created` or `order:shipment:created` events stop arriving.
**Cause**: The endpoint returned 4xx/5xx three times in a row — Printify blocks the webhook for 1 hour, and events during the block are not replayed.
**Solution**: Make the listener return `200` immediately (queue processing), verify the `X-Pfy-Signature` HMAC without erroring on edge cases, test with `POST /webhooks/{id}/simulate`, and run a reconciliation poll of `GET /orders.json` to backfill missed events.

### 429 Too Many Requests
**Symptom**: API calls fail with 429, especially catalog reads or bulk publishing.
**Cause**: Global 600 req/min, catalog 100 req/min, or publishing 200 req/30 min limit — counted per account, not per token.
**Solution**: Cache catalog data locally (blueprints/variants change rarely), throttle publish jobs below 200/30 min, add exponential backoff starting ~2s, and keep error responses under 5% of traffic to avoid account-level throttling.

### Product stuck in "publishing" state
**Symptom**: A product on a custom/API sales channel is locked and can't be edited.
**Cause**: `publish.json` was called (or publishing started from the UI) but the integration never confirmed the result.
**Solution**: Complete the handshake — after your app pushes the product to your storefront, call `POST .../publishing_succeeded.json` (with your external handle) or `.../publishing_failed.json` to unlock it. Handle the `product:publish:started` webhook to automate this.
