---
name: sales-store-migration
description: "Ecommerce store-migration strategy — the tool-agnostic playbook for replatforming (Shopify ↔ WooCommerce ↔ Wix ↔ BigCommerce ↔ PrestaShop ↔ Magento and beyond): choosing between automated migration tools (LitExtension, Cart2Cart, Migratly), native importers, CSV, or custom API scripts; migration-order mechanics (products → customers → orders), SEO preservation with 301 redirect maps, delta migration for orders arriving mid-cutover, app/webhook/payment re-wiring, and post-migration verification. Use when switching ecommerce platforms without losing SEO or order history, planning redirect maps before a replatform, deciding migration tool vs doing it by hand, recent orders keep appearing on the old store during cutover, migrated data needs verification (counts, variants, customer passwords), or rebuilding integrations after the move. Do NOT use for choosing the destination platform itself (use /sales-checkout) or LitExtension specifics (use /sales-litextension)."
argument-hint: "[describe your store migration — source, target, and what worries you]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, migration, strategy]
---

# Ecommerce Store Migration

Help the user replatform an ecommerce store without losing SEO, order history, or sales in transit. Covers approach selection (tool vs native importer vs CSV vs custom scripts), the migration sequence, redirect/SEO preservation, delta handling, integration re-wiring, and verification. Tool-agnostic; platform specifics live in the platform skills.

## Step 1 — Gather context

Ask the user (skip anything already answered):

1. **Source → target?** (e.g. WooCommerce → Shopify) — the pair determines available native importers and known mapping quirks.
2. **Scale?** Products / customers / orders counts — drives tool pricing and the order-retention decision.
3. **Live sales volume?** Orders per day during the migration window — determines how much delta handling matters.
4. **What must survive?** (multi-select) SEO rankings/URLs · full order history · customer accounts · subscriptions/recurring billing · reviews · blog content.
5. **Who's doing the work?** Solo founder / dev on hand / agency — selects DIY tool vs done-for-you.

## Step 2 — Choose the migration approach

### Decision tree

1. **Active subscriptions on the store?** → That's the hard part; route billing continuity to `/sales-subscription-billing` (don't double-bill on import) and handle catalog/SEO here.
2. **Tiny store (≲100 products, no order history worth keeping)?** → CSV export/import or the target's native importer. Free; redirects still matter.
3. **Common pair with a strong native importer** (e.g. WooCommerce → Shopify's official importer)? → Try native first; fall back to a tool if variants/orders map badly.
4. **Real store, real history, uncommon pair, or no dev time?** → **Automated migration tool**: LitExtension (widest cart coverage ~140+, done-for-you tiers, money-back guarantee — `/sales-litextension`), Cart2Cart (long-standing, ~85 carts, self-directed automation with detailed logging), Migratly (newer, modern UX, flexible attribute mapping — early-stage, thinner delta support).
5. **Custom source (homegrown cart, weird schema) or heavy data transformation?** → Custom scripts against both platforms' APIs, or a tool's custom/API migration service.

### Tool-selection criteria

Cart-pair support and per-pair mapping quality (test with a demo) · delta/re-migration support for live stores · SEO URL handling · entity pricing at YOUR counts · DIY vs concierge · refund terms. Discount review scores: migration-tool review profiles skew implausibly clean — judge by a demo migration on your own data, never testimonials.

## Step 3 — The migration playbook

### Sequence (order matters)

1. **Freeze scope**: decide order-history retention (order count usually dominates tool pricing — archive older orders as CSV), which entities migrate, and what gets cleaned up rather than carried over (~40% of merchants hit unexpected data-cleanup needs).
2. **Demo/sample migration first** — always. Inspect variant structure, images, prices, categories, SEO URLs in the target before paying or committing.
3. **Full migration while the source keeps selling.** Never take the store down to migrate.
4. **Build the 301 redirect map** old-URL → new-URL for every product/category/content page, and **test it** — redirect testing is the single most underestimated step (~60% of merchants per agency data). Preserve URL paths where target allows; redirect where it doesn't.
5. **Re-wire integrations on the target**: payment processor, webhooks, ESP/CRM syncs, analytics, feeds, apps — inventory each source integration before cutover; they do not migrate.
6. **Verify**: entity counts per type vs source, spot-check variants/prices/images, order↔customer linkage, and a crawl of the redirect map.
7. **Cut over DNS/theme, then run the delta** (re-migration/smart update) for orders and customers that arrived since the snapshot.
8. **Post-cutover**: password-reset campaign (hashes don't cross carts), monitor 404s and Search Console for a few weeks, keep the source exportable until the window closes.

### What silently breaks (plan for these)

- **Customer passwords** — never migrate; announce resets proactively.
- **Subscriptions/recurring billing** — payment tokens don't port; see `/sales-subscription-billing`.
- **Plugin/app-created custom fields** — need explicit mapping (Woo plugin fields, BigCommerce price lists, OpenCart image paths are the classics).
- **SEO equity** — lost by unredirected URLs, not by the move itself.
- **Integrations/webhooks** — everything connected to the old store needs re-connecting.

## Step 4 — Actionable guidance

- Always run a demo/sample migration before committing money or the calendar — it's where per-pair mapping surprises surface, and for SEO plans it reveals how the target restructures URLs BEFORE you build the redirect map.
- Treat the redirect map as a deliverable with its own testing pass, not a checkbox in the tool.
- Decide order-history retention before pricing tools — it's the main cost lever.
- Schedule the delta sync as the LAST step before announcing cutover; every sale between snapshot and delta exists only on the source.
- Inventory integrations (payments, webhooks, ESP, analytics, apps) on day one — re-wiring them is usually more work than the data move.

## Gotchas

*Best-effort from research (2026-07) — tool coverage, pricing models, and importer quality shift; verify per pair.*

1. **The migration is the easy 60%** — redirects, integration re-wiring, and verification are where replatforms actually fail, and where merchants under-budget time.
2. **"Zero downtime" ≠ "zero delta"** — the source selling through the migration is standard, but only if a delta sync closes the gap at cutover.
3. **Native importers are free but pair-specific** — great for the blessed pairs, silently lossy on variants/metafields elsewhere; verify with a sample either way.
4. **Tool review profiles are unreliable in this category** — uniform 5-star walls are a documented pattern; the demo migration is your only trustworthy signal.
5. **Don't migrate garbage** — a replatform is the moment to drop dead SKUs, stale customers, and spam accounts; cleaning after the move costs double.
6. **Keep the source alive (read-only) after cutover** until the redirect map has soaked and the delta is confirmed — it's your rollback and audit trail.

## Related skills

- `/sales-litextension` — LitExtension platform help (the widest-coverage migration tool; demo, Smart Update, entity pricing)
- `/sales-checkout` — Choosing the destination platform (the decision upstream of migration)
- `/sales-subscription-billing` — Migrating active subscriptions without double-billing (payment tokens don't port)
- `/sales-seo` — SEO strategy around a replatform (beyond redirect mechanics)
- `/sales-shopify` — Shopify platform help (most common target; native importers, webhooks to re-wire)
- `/sales-membership` — Course/membership platform migration is a different playbook (see its migration gotchas)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: WooCommerce → Shopify, SEO is the fear
**User says**: "We rank well on our WooCommerce store and want to move to Shopify without tanking our traffic."
**Skill does**: Builds the plan around the redirect map — inventory every indexed URL, map to Shopify's URL structure, 301 everything unmappable, test the map before DNS — plus a demo migration to check variant/category mapping, and Search Console monitoring for weeks after.
**Result**: The replatform ships with rankings protected by tested redirects, not hope.

### Example 2: Tool or by hand?
**User says**: "600 products, 9k customers, 40k orders — Wix to BigCommerce. Should we pay for a migration tool or script it ourselves?"
**Skill does**: Applies the decision tree — uncommon pair, real history → automated tool; compares LitExtension (coverage + concierge) vs Cart2Cart (self-directed) at their entity counts, flags order-retention as the cost lever (40k orders dominate the quote), and prescribes the demo-first rule.
**Result**: A tool choice priced on real counts, validated by a sample before commitment.

### Example 3: Orders straddling the cutover
**User says**: "We migrated last weekend but orders from Friday and Saturday are missing on the new store."
**Skill does**: Diagnoses the snapshot gap — sales continued on the source after the migration ran — and closes it with the tool's delta/re-migration (Smart Update in LitExtension), then re-sequences the rollout so the delta sync is the final pre-announcement step.
**Result**: The stranded orders sync over and the cutover process gets fixed for next time.

## Troubleshooting

### Traffic dropped after the move
**Symptom**: Organic sessions fall off a cliff post-cutover.
**Cause**: Unredirected URLs — the old paths 404 and equity evaporates.
**Solution**: Crawl the old sitemap against the new store, 301 every miss, resubmit sitemaps in Search Console, and watch the 404 report daily until it flatlines.

### Variants/options came over wrong
**Symptom**: Products migrated but sizes/colors are flattened or scrambled.
**Cause**: Source and target model options differently; the per-pair mapping needed configuration the default run didn't apply.
**Solution**: This is exactly what the demo migration exists to catch — configure attribute/option mapping (or use a tool's custom mapping), re-run affected products, and re-verify a sample before cutover.

### Old store's integrations keep firing
**Symptom**: The ESP/CRM/analytics still receive events from the source store after cutover.
**Cause**: Integrations were never inventoried and re-pointed.
**Solution**: List every webhook, app, and API connection on the source; disable them there and re-create them on the target. Keep the source read-only until the list is empty.
