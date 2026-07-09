---
name: sales-customcat
description: "CustomCat platform help — budget US (Detroit) print-on-demand fulfillment for creators/sellers (apparel, drinkware, home décor) via DIGISOFT DTG/DTF, embroidery, and dye sublimation, with 1–3 day production, a REST API (catalog, orders, shipping, webhooks), and store connectors for Shopify/Etsy/WooCommerce/BigCommerce. Use when CustomCat orders aren't syncing from your store, an API write call returns 403 because you used the read-only key, an order fails with a duplicate-order/out-of-stock/AVS-address error, a CustomCat order-shipped webhook needs a polling backup, you're building a headless order pipeline against customcat-beta.mylocker.net, modeling whether the Pro plan beats Lite's free wholesale pricing, or you need branded/private-label merch (CustomCat can't do it). Do NOT use for choosing between POD providers like Printful/Printify/Gelato (use /sales-print-on-demand) or general digital-product pricing/launch strategy (use /sales-digital-products)."
argument-hint: "[describe what you need help with in CustomCat]"
license: MIT
version: 1.0.1
tags: [sales, digital-products, platform]
---

# CustomCat Platform Help

CustomCat is a budget, US-based (Detroit) print-on-demand (POD) fulfillment service: you upload designs, CustomCat prints products on demand and ships them, and you hold no inventory. It plugs into your storefront (Shopify, Etsy, WooCommerce, BigCommerce) or runs headless via its REST API. Its pitch is the lowest base prices + the fastest US production (1–3 business days) — at the cost of no private-label branding and US-only fulfillment.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Connect CustomCat to a store (Shopify/Etsy/WooCommerce/BigCommerce)
   - B) Build a headless/custom integration via the API (submit orders, read catalog, quote shipping, register webhooks)
   - C) Fix a broken order, sync, or webhook
   - D) Decide on a plan (Lite free vs Pro $30/mo vs Enterprise) or understand margins
   - E) Product, design-file, or shipping questions

2. **API keys?** Read-only vs read-write — most "403 Forbidden" issues are a read-only key on a write (order/webhook) call. Keys live in **Settings > Store > API**.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which POD provider to pick (CustomCat vs Printful/Printify/Gelato/SPOD) | `/sales-print-on-demand {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Checkout-page conversion (order bumps, upsells, cart abandonment) | `/sales-checkout {question}` |
| Tax / Merchant-of-Record obligations on merch sales | `/sales-merchant-of-record {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-digital-products {original question}`"

Otherwise, answer CustomCat-specific questions directly using Step 3.

## Step 3 — CustomCat platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model (catalog product, SKU, design placement presets, orders), and quick-start recipes (submit an order, quote shipping, register an order-shipped webhook).

For raw endpoint detail, auth, webhook payloads, and error messages, read `references/customcat-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Read-only vs read-write key is the #1 API trap.** A read-only key on any write call (submit/cancel order, register webhook) returns `403 Forbidden`. Use the read-write key for orders/webhooks; reserve the read-only key for the value CustomCat echoes back in webhook payloads.
- **Your `order_id` is the idempotency key.** Resubmitting the same `order_id` returns `400 Duplicate Order`. Generate a unique id per order and treat a duplicate response as "already accepted," not a failure.
- **Webhooks are NOT signed — verify by the echoed read-only key and keep a polling backup.** Unlike Printful, CustomCat doesn't HMAC-sign payloads; it embeds your read-only `api_key` in the body. Confirm that value and still poll `GET /order/status/{order_id}` so a dropped `order-shipped` event never loses a notification.
- **CustomCat charges you per order, then ships.** A `400 Charge Failed` means the payment method on file was declined — fix billing before resubmitting. Model margin = retail − (base + fulfillment + shipping + any back-print/$5 fee).
- **No private-label branding.** Products keep the manufacturer's tags (Gildan, Bella+Canvas, etc.). If white-label unboxing matters, CustomCat can't do it — Printful can (compare via `/sales-print-on-demand`).

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and pricing that may have changed.*

- **No custom branding / private labeling** — products ship with the original manufacturer's brand tags and no custom packing slips or neck labels. This is the single biggest difference from Printful; for branded merch, choose Printful/Printify instead.
- **US-only fulfillment; international is slow** — all production is in Detroit. Domestic ships in 3–5 days, but international can take 1–4 weeks. If 30%+ of buyers are international, weigh **Gelato**'s local print network (compare via `/sales-print-on-demand`).
- **403 Forbidden = read-only key on a write op** — the most common API failure. Switch to the read-write key for order/webhook calls.
- **`400 Duplicate Order`** — the `order_id` was already processed. Use a unique id per order and make submission idempotent.
- **AVS rejects bad US addresses** — `Invalid Shipping Address` / `Conflicting ZIP Code/city/state` come back with a `suggestions` array; surface the suggestion to the buyer rather than blindly resubmitting.
- **Out-of-stock SKU fails the order** — `There is an issue with the order. SKU: {sku}` means that variant is unavailable; check `/catalog` inventory before submitting.
- **Pro only pays off above volume** — Lite (free) gives the full catalog at standard wholesale; Pro ($30/mo, or $300/yr ≈ $25/mo) only wins once its 20–40% catalog discount on your monthly volume exceeds the subscription.
- **Basic design tool** — no built-in external image library; design files should be **300 DPI** (or declare embedded DPI). Back print adds a **$5 fee per line item**.

## Related skills

- `/sales-print-on-demand` — POD provider selection: **choosing between CustomCat/Printful/Printify/Gelato/Gooten/SPOD** and multi-provider routing
- `/sales-digital-products` — Digital-product & merch strategy: pricing, validation, launch
- `/sales-printify` — Printify platform help (the broker-network alternative — 1,300+ products, lowest base costs, per-provider quality vetting)
- `/sales-printful` — Printful platform help (the branded, multi-region POD alternative — owns fulfillment, private labels, signed v2 webhooks)
- `/sales-sellfy` — Sellfy platform help (creator storefront with built-in POD if you want store + merch in one tool)
- `/sales-checkout` — Checkout-page optimization (order bumps, upsells, cart abandonment) for the store that fronts CustomCat
- `/sales-merchant-of-record` — Tax/VAT handling on merch sales
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Orders not reaching CustomCat
**User says**: "My Shopify orders aren't showing up in CustomCat."
**Skill does**: Checks that the store connection is active and the products were imported/mapped to CustomCat SKUs, verifies auto-fulfillment is enabled (vs orders waiting for manual approval), and — for API submitters — confirms a unique `order_id` was sent and the call used the read-write key, not the read-only one.
**Result**: User finds the disconnected store / wrong key, re-syncs, and orders flow through.

### Example 2: Headless order submission via the API (developer/automation)
**User says**: "How do I submit an order to CustomCat from my own backend?"
**Skill does**: Walks through `POST /order/{order_id}` with the `shipping_*` recipient fields, a `shipping_method` from `GET /shipping`, and an `items` array (using `sku`+`quantity` for catalog products, or `catalog_sku`+`design_url`+`preset_id` for external designs), explains the read-write key requirement and `sandbox=1` for testing, and shows the cURL + Python example plus the `400` error handling (Duplicate Order, Invalid Shipping Address with `suggestions`).
**Result**: User has a working, idempotent order-submission flow with address-validation handling.

### Example 3: Plan decision and margins
**User says**: "Is CustomCat Pro worth $30/mo for me?"
**Skill does**: Explains Lite is free at standard wholesale and Pro unlocks 20–40% off the catalog, then models the break-even — Pro pays off once (discount % × monthly product spend) exceeds $30 — and compares the annual $300 (~$25/mo) option, factoring base + fulfillment + shipping + any $5 back-print fee against retail.
**Result**: User decides based on projected order volume, not feature FOMO.

## Troubleshooting

### Orders aren't appearing in CustomCat
**Symptom**: Store orders don't create CustomCat orders.
**Cause**: Store connection paused/disconnected, products not mapped to CustomCat SKUs, manual order approval enabled, or (API) a non-unique `order_id` / read-only key.
**Solution**: Re-connect the store and re-map products, enable auto-fulfillment, and for API submitters send a unique `order_id` with the read-write key. Register the `order-shipped` webhook and poll `GET /order/status/{order_id}` as a backup.

### API write call returns 403 Forbidden
**Symptom**: Submitting an order or registering a webhook returns `403`.
**Cause**: You used the read-only API key on a write operation.
**Solution**: Switch to the read-write key (Settings > Store > API) for all order and webhook calls. Keep the read-only key only for reads and for verifying the value CustomCat echoes in webhook payloads.

### Order rejected on submission
**Symptom**: `POST /order` returns a `400` (Duplicate Order, Invalid Shipping Address, out-of-stock SKU, or Charge Failed).
**Cause**: Re-used `order_id`, a US address that fails AVS, an unavailable variant, or a declined payment method on file.
**Solution**: Use a unique `order_id`; on `Invalid Shipping Address`/`Conflicting ZIP` apply the returned `suggestions`; check `/catalog` stock before ordering; and fix the billing method for `Charge Failed`. Test against `sandbox=1` first.
