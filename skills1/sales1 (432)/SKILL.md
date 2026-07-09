---
name: sales-printful
description: "Printful platform help — print-on-demand merch fulfillment for creators/brands (apparel, accessories, all-over print) with a REST API (v2 beta + v1), signed webhooks, mockup generator, and store connectors for Shopify/WooCommerce/Etsy/Wix. Use when orders aren't appearing in Printful or SKUs aren't matching sync variants, an order is stuck in the failed state, a Printful webhook never fired and you need a polling backup, shipping takes too long and customers complain, building a headless store that creates orders via the API, generating product mockups programmatically, or choosing between the Free and Growth plans. Do NOT use for choosing between POD providers like Printify/Gelato/Gooten (use /sales-print-on-demand) or general digital-product pricing/launch strategy (use /sales-digital-products)."
argument-hint: "[describe what you need help with in Printful]"
license: MIT
version: 1.0.0
tags: [sales, digital-products, platform]
github: "https://github.com/printful"
---

# Printful Platform Help

Printful is a print-on-demand (POD) fulfillment service: you design custom products, Printful prints and ships them on demand, and you hold no inventory. It plugs into your storefront (Shopify, WooCommerce, Etsy, Wix, etc.) or runs headless via its REST API.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Connect Printful to a store (Shopify/WooCommerce/Etsy/Wix/etc.)
   - B) Build a headless/custom integration via the API (create orders, mockups, sync catalog)
   - C) Fix a broken order, webhook, or sync
   - D) Decide on a plan (Free vs Growth) or understand fees/margins
   - E) Product, branding, or shipping questions

2. **API version?** v2 (beta, recommended for new builds — `/v2/` paths, leaky-bucket rate limit, signed webhooks) or legacy v1.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which POD provider to pick (Printful vs Printify/Gelato/Gooten/SPOD) | `/sales-print-on-demand {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Checkout-page conversion (order bumps, upsells, cart abandonment) | `/sales-checkout {question}` |
| Tax / Merchant-of-Record obligations on merch sales | `/sales-merchant-of-record {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-digital-products {original question}`"

Otherwise, answer Printful-specific questions directly using Step 3.

## Step 3 — Printful platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model (catalog product vs variant, orders, mockups), and quick-start recipes (create an order, generate a mockup, listen for a shipment webhook).

For raw endpoint detail, auth, rate limits, and webhook payloads, read `references/printful-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Always use variant IDs, not product IDs, when creating orders.** A catalog product is a blank template; a variant is the actual color/size you fulfill. Most "order won't create" bugs are a missing/wrong `catalog_variant_id`.
- **Order cost is calculated asynchronously.** A freshly created order may show cost `calculating`; you can't `confirm` it until calculation finishes. Poll the order or wait for the estimation task.
- **Treat webhooks as best-effort, not guaranteed.** Always keep a GET-endpoint polling backup for critical events (shipment, mockup task). v2 webhooks are signed — verify the signature.
- **Model fees before committing.** Base cost + fulfillment + shipping is what you pay; your retail margin is the gap. Growth's per-product discount only pays off above steady volume.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may have changed.*

- **Fulfillment + shipping is slow on default routing** — US/EU orders commonly land in ~5 days but worldwide can be 10–14. If 30%+ of buyers are international, that's a real CX problem; Gelato's local network is the usual answer (compare via `/sales-print-on-demand`).
- **SKU / sync-variant mismatch silently drops orders** — if store orders aren't appearing in Printful, the product SKU must match Printful's `sync_variant_id`. This is the #1 store-integration failure.
- **`draft` orders are never charged or fulfilled** — you must `POST /orders/{id}/confirm`. Many "Printful didn't ship my order" cases are unconfirmed drafts.
- **Growth plan billing flips at $12K/yr sales** — the $24.99/mo becomes free above that threshold; below it, the per-product discount may not cover the subscription.
- **Branding and premium placements cost extra per item** — inside label $0.99, outside label $2.49, premium image $1/item, embroidery digitization $2.95–$6.50 one-time. These erode margin if unpriced.
- **v1 vs v2** — v2 is beta but recommended for new builds (signed webhooks, leaky-bucket rate limiting, RFC 9457 errors). v1 still works; don't mix object shapes across versions.

## Related skills

- `/sales-print-on-demand` — POD provider selection: **choosing between Printful/Printify/CustomCat/Gelato/Gooten/SPOD** and multi-provider routing
- `/sales-digital-products` — Digital-product & merch strategy: pricing, validation, launch
- `/sales-printify` — Printify platform help (the broker-network alternative — 1,300+ products, lowest base costs, per-provider quality vetting)
- `/sales-customcat` — CustomCat platform help (the budget POD alternative — lowest base prices + fastest US production, but no private-label branding and US-only fulfillment)
- `/sales-checkout` — Checkout-page optimization (order bumps, upsells, cart abandonment) for the store that fronts Printful
- `/sales-merchant-of-record` — Tax/VAT handling on merch sales
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Orders not reaching Printful
**User says**: "My Shopify orders aren't showing up in Printful."
**Skill does**: Checks that each product's SKU matches Printful's `sync_variant_id`, confirms the store connection is active and not paused, verifies orders aren't sitting as unconfirmed `draft`, and explains the auto vs manual order-confirmation setting.
**Result**: User finds the SKU mismatch, re-syncs, and orders flow through.

### Example 2: Headless order creation via the API (developer/automation)
**User says**: "How do I create and confirm a Printful order from my own backend?"
**Skill does**: Walks through `POST /v2/orders` with a recipient + `order-items` using `catalog_variant_id` and a `placements`/`layers` design payload, explains the async cost `calculating` state, then `POST /v2/orders/{id}/confirm`, with a cURL + Python example from the platform guide and the leaky-bucket 429 retry pattern.
**Result**: User has a working order-creation flow with retry handling.

### Example 3: Plan decision and margins
**User says**: "Is Printful Growth worth $24.99/mo for me?"
**Skill does**: Explains Growth becomes free above $12K/yr in sales, quantifies the up-to-33% product discount + 9% branding discount against the user's volume, and models base cost + fulfillment + shipping vs retail price to show the break-even order count.
**Result**: User decides based on actual projected volume, not feature FOMO.

## Troubleshooting

### Orders aren't appearing in Printful
**Symptom**: Store orders don't create Printful orders.
**Cause**: SKU doesn't match `sync_variant_id`, store connection paused, or orders left as `draft`.
**Solution**: Re-map product SKUs to Printful sync variants, re-enable the connection, and either enable auto-confirm or call `POST /orders/{id}/confirm`. For API orders, double-check you used `catalog_variant_id` (not product id).

### Order stuck in `failed` state
**Symptom**: An order moved to `failed` after submission.
**Cause**: A problem surfaced during processing (bad design file/placement, out-of-stock variant, address issue).
**Solution**: Read the order's error detail, fix the offending item (file URL, placement/technique, or variant), then resubmit. Listen for the `order_failed` webhook to catch this automatically.

### Webhook never fired
**Symptom**: A `shipment_sent` or `mockup_task_finished` event didn't arrive.
**Cause**: Webhooks are best-effort; delivery can be missed, and v2 subscriptions can expire or auto-disable.
**Solution**: Keep a GET-endpoint polling backup (poll the order/shipment or mockup task), re-register the webhook, ensure your endpoint is HTTPS and verifies the v2 signature, and check the configured event is still enabled.
