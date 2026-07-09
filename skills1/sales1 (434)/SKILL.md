---
name: sales-print-on-demand
description: "Print-on-demand (POD) provider selection and multi-provider strategy — compares Printful, Printify, CustomCat, Gelato, Gooten, and SPOD on fulfillment model (owns-factories vs broker network), base costs and per-order margins, shipping geography and speed for domestic vs international buyers, branding/white-label options, catalog breadth, and API/webhook surface. Use when choosing a POD provider for merch or a clothing brand, print quality is inconsistent and you're weighing a switch, international shipping is too slow or expensive, you need private-label branding (custom neck labels, branded packaging), you're deciding whether to route different products to different providers, comparing per-order economics at your sales volume, or setting up a sample-order vetting workflow before scaling. Do NOT use for platform-specific setup or API integration (use /sales-printful, /sales-printify, /sales-customcat) or for selling digital downloads (use /sales-digital-products)."
argument-hint: "[describe your print-on-demand decision or problem]"
license: MIT
version: 1.0.0
tags: [sales, digital-products, print-on-demand, strategy]
---

# Print-on-Demand Provider Selection

Help the user pick — and combine — print-on-demand providers. POD lets you sell custom merch (apparel, mugs, posters, accessories) with no inventory: the provider prints and ships each order. The decision is not "which is best" but "which trade-off profile fits this seller": every provider trades among cost, quality consistency, shipping geography, branding, and catalog breadth.

## Step 1 — Gather context

Ask the user (skip anything already answered):

1. **What are you selling, and where are your buyers?**
   - A) Mostly US buyers
   - B) Mostly EU/UK buyers
   - C) Global — significant international share (30%+)

2. **What matters most?** (pick 2)
   - A) Margin — lowest base cost per unit
   - B) Quality consistency — every order identical
   - C) Speed — fastest production + delivery
   - D) Branding — custom neck labels, branded packaging, white-label unboxing
   - E) Catalog breadth — unusual products beyond tees/mugs

3. **Volume and stage?**
   - A) Validating — first products, low volume
   - B) Selling steadily (50–500 orders/mo)
   - C) Scaling (500+ orders/mo — per-unit economics dominate)

4. **Sales channel?** Etsy / Shopify / TikTok Shop / Amazon / own headless store via API — connector coverage differs per provider.

## Step 2 — The decision framework

### Fulfillment model is the first fork

- **Owns its factories** (Printful, CustomCat, SPOD): consistent quality and branding control, higher base costs (Printful) or narrower reach (CustomCat US-only).
- **Broker network** (Printify, Gooten, Gelato*): routes orders to third-party printers — lowest costs and biggest catalogs, but quality/speed vary by the provider *you pick per product*, and you own vetting. (*Gelato is a hybrid: a curated partner network with strong QA, optimized for local international production.)

### Decision tree

1. **30%+ international buyers?** → Gelato first (local production in 30+ countries = 3–5 day delivery vs 10–14 shipping from the US), Printify with per-region providers second.
2. **Branding is the differentiator (own clothing brand)?** → Printful (inside/outside labels, branded inserts, embroidery) — accept the higher base cost as brand spend.
3. **Margin-first, US buyers?** → CustomCat (lowest base + 1–3 day Detroit production, no branding) or Printify (choose cheap US providers; slightly more vetting work).
4. **Widest catalog / unusual products?** → Printify (1,300+ blueprints).
5. **High volume (500+/mo) and operations-heavy?** → Gooten (order-management infrastructure, volume pricing) or negotiate Printify Enterprise / Printful volume rates.
6. **Speed guarantee matters more than unit cost?** → SPOD (48-hour production promise).

### Per-order economics (model this, don't guess)

Margin = retail − (base cost + fulfillment/print fee + shipping + branding add-ons + store fees). Compare at *your* product mix: a $1–2 base-cost gap (e.g. Printify tee ~$7 vs Printful ~$8.20) is ~$100–200/mo at 100 orders — real but smaller than a quality-driven refund/reprint rate. Factor provider subscriptions: Printify Premium (~$29/mo, up to 20% off base), Printful Growth ($24.99/mo, free above $12K/yr sales), CustomCat Pro ($30/mo, 20–40% off).

### The sample-order vetting workflow (non-negotiable for broker networks)

1. Shortlist 2–3 providers/products; order a sample of each (most platforms discount samples).
2. Check: print color accuracy after wash, placement, fabric feel, packaging state, actual production + transit days vs promised.
3. Scale on one provider; keep the runner-up mapped so you can migrate a product when quality degrades — on broker networks quality is per-provider and *does* drift.
4. Re-sample your bestsellers quarterly and after any provider change.

## Step 3 — Provider notes

### In Printify (broker network — biggest catalog, lowest costs)
1,300+ blueprints via ~141 third-party print providers; you pick the provider per product (each has its own costs, locations, speed). Free plan; Premium ~$29/mo for up to 20% off base costs. Connectors: Shopify, Etsy, TikTok Shop, Amazon, eBay, Walmart, WooCommerce, Wix, Squarespace + API sales channel; REST API + HMAC-signed webhooks + official OpenAPI spec. Trade-off: quality/speed vary by provider — the vetting workflow above is mandatory. For setup/integration, use `/sales-printify`.

### In Printful (owns factories — consistency + branding)
In-house fulfillment: the most consistent quality and the branding leader (inside/outside labels, packing inserts, embroidery) at higher base costs (~$1–2/unit more than Printify-cheap). ~450 products, 20+ store connectors, REST API v2 with signed webhooks + mockup generator. Growth plan $24.99/mo (free above $12K/yr sales) for up to 33% off. Best for brand builders who value unboxing over unit margin. For setup/integration, use `/sales-printful`.

### In CustomCat (owns factory — budget US)
Detroit in-house production: lowest base prices of the big three and 1–3 business-day turnaround, but **no private-label branding** (manufacturer tags stay) and **US-only fulfillment** (international 1–4 weeks). 200+ products via DTG/DTF, embroidery, dye sublimation. Lite free / Pro $30/mo (20–40% off). Connectors: Shopify, Etsy, WooCommerce, BigCommerce + REST API. Best for cheap domestic merch where unboxing doesn't matter. For setup/integration, use `/sales-customcat`.

### In Gelato (local-production network — international)
Curated partner network across 30+ countries producing *near the buyer*: 3–5 day international delivery without cross-border shipping, customs, or carbon-heavy freight. Strong for posters/wall art, apparel, mugs, photo books. REST API + store integrations; subscription tiers add discounts. Best when a large share of buyers are outside your home country.

### In Gooten (broker network — high-volume operations)
Order-management-first POD for scaling sellers: reliable routing infrastructure, often 25–35% cheaper than Printful at 500+ orders/mo, VIM (volume) pricing tiers, API available. Catalog and connector list are smaller than Printify's. Best when operations reliability at volume matters more than catalog breadth.

### In SPOD (owns factories — speed guarantee)
By Spreadshirt: 48-hour production promise on 95%+ of orders, US + EU facilities, simple flat shipping. Smaller catalog and fewer connectors. Best when predictable speed is the selling point.

### Multi-provider routing (advanced)
Nothing forces one provider. Common splits: Printful for the branded flagship line + Printify/CustomCat for volume basics; Gelato for international orders + a US provider domestically (duplicate the product, route orders by destination — native on broker platforms by picking per-region providers, or in your own middleware via each provider's API). Cost: more sample vetting, more SKU mapping, more integration surface.

## Step 4 — Actionable guidance

- Match the provider to your top-2 priorities from Step 1 — every "best POD" listicle ignores that the ranking flips with buyer geography and branding needs.
- Order samples before scaling anything; on broker networks, re-sample after any provider switch.
- Model per-order margin at your real volume including subscriptions and branding add-ons before committing to a paid tier.
- Plan the migration path: keep design source files off-platform and note each product's blueprint/provider mapping so you can rebuild elsewhere.

## Gotchas

*Best-effort from research (2026-07) — pricing, discounts, and catalog counts drift; verify before deciding.*

1. **"Cheapest base cost" lists compare different garments.** A $7 tee on one provider may be a lighter blank than the $8.20 tee elsewhere. Compare the same brand/model (e.g. Gildan 5000 vs Bella+Canvas 3001), not headline prices.
2. **Quality complaints on broker networks are provider problems, not platform problems** — and the fix (switch providers) is available without replatforming. Don't churn off Printify for what one print provider did.
3. **Branding add-ons erode margin quietly** — Printful inside labels $0.99, outside $2.49, premium images $1/item. Price them into retail or skip them.
4. **International shipping kills conversion silently.** 10–14 day delivery from a US-only provider suppresses repeat purchases from EU buyers — check your buyer geography before blaming the product.
5. **None of these providers is a Merchant of Record** — you own VAT/GST/sales-tax obligations on merch sales (see `/sales-merchant-of-record`).
6. **Subscription discounts have break-evens**: Printify Premium ~$145/mo base spend; Printful Growth free above $12K/yr sales; CustomCat Pro when the 20–40% discount beats $30/mo. Below break-even the free tier wins.

## Related skills

- `/sales-printify` — Printify platform help (broker network; REST API, HMAC-signed webhooks, provider selection per blueprint)
- `/sales-printful` — Printful platform help (owns factories; branding, mockup generator, REST API v2)
- `/sales-customcat` — CustomCat platform help (budget US POD; read/write API keys, unsigned webhooks)
- `/sales-digital-products` — Digital product & merch strategy: pricing, validation, launch, platform selection
- `/sales-checkout` — Checkout-page optimization for the store that fronts your POD provider
- `/sales-merchant-of-record` — Tax/VAT handling on merch sales
- `/sales-multichannel-selling` — Selling the same catalog across Etsy/Shopify/TikTok Shop/Amazon
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: First merch line
**User says**: "I have an audience of 20K followers and want to launch a small clothing brand — which print-on-demand service should I use?"
**Skill does**: Asks about buyer geography and branding priority; for a *brand* (custom labels, consistent quality) recommends Printful despite higher base costs, models a $25 tee's margin with branding add-ons, and sets up the sample-order vetting checklist before launch.
**Result**: User picks a provider aligned with brand-building, not the cheapest headline price.

### Example 2: International shipping complaints
**User says**: "Half my Etsy buyers are in Europe and they keep complaining orders take two weeks."
**Skill does**: Diagnoses US-only fulfillment as the cause; compares Gelato (local EU production, 3–5 days) vs Printify with EU-based print providers; outlines duplicating bestsellers onto an EU provider and routing by destination, with sample orders to verify EU print quality first.
**Result**: EU delivery drops to under a week without abandoning the existing US setup.

### Example 3: Margin squeeze at volume
**User says**: "I'm doing 800 POD orders a month on Printful and my margins are thin — is switching worth it?"
**Skill does**: Models per-order economics across CustomCat (lowest US base), Gooten (25–35% cheaper at volume), and Printify Premium (~20% off base); quantifies the monthly delta at 800 orders against switching costs (re-vetting samples, SKU remapping, connector rework) and suggests a phased migration of the top 5 SKUs first.
**Result**: User migrates high-volume basics to a cheaper provider and keeps branded items on Printful, raising blended margin.

## Troubleshooting

### Print quality became inconsistent after months of good orders
**Symptom**: Same product, same design — defect complaints spike.
**Cause**: On broker networks (Printify/Gooten) the fulfilling print provider drifted, changed equipment, or your product silently rerouted to a different provider.
**Solution**: Identify the fulfilling provider on the bad orders, file reprint claims, sample 1–2 alternative providers for the blueprint, and migrate the product. Re-sample quarterly.

### Margins looked good on paper but the payout is thin
**Symptom**: Retail minus base cost promised a healthy margin; the bank account disagrees.
**Cause**: Un-modeled costs — shipping charged to you, branding add-ons, marketplace fees (Etsy ~6.5% + payment), refunds/reprints, and provider subscription fees.
**Solution**: Rebuild the margin model per SKU: retail − (base + print fee + shipping + add-ons + channel fees + subscription amortized). Kill or reprice SKUs under ~30% net margin.

### Can't decide between two providers
**Symptom**: Comparison paralysis — both look fine.
**Cause**: Priorities not ranked; listicle rankings don't weight your geography/branding/volume.
**Solution**: Rank your top-2 priorities (Step 1), run the decision tree, then order the same product from both providers and let the samples decide. The physical sample resolves what spreadsheets can't.
