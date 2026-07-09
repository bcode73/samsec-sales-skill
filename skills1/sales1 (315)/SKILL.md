---
name: sales-litextension
description: "LitExtension platform help — automated ecommerce store-migration tool + done-for-you service moving products/variants, customers, orders, blogs, and SEO URLs between 140+ carts (Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, Wix, Ecwid, Squarespace…). Entity-count pricing, free limited demo migration, post-migration re-migration/smart-update window, All-in-One concierge tier. No public API — it consumes your source/target store APIs (per-cart API-key setup guides). Use when running a LitExtension demo or full migration, deciding DIY tool vs All-in-One service, orders keep arriving mid-migration and need a delta sync, preparing source/target API keys and bridge access, verifying migrated data and SEO redirects afterward, or estimating cost by entity counts. Do NOT use for choosing a migration approach or tool (use /sales-store-migration) or picking the destination platform (use /sales-checkout)."
argument-hint: "[describe what you need help with in LitExtension]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, migration, platform]
---

# LitExtension Platform Help

LitExtension is an ecommerce migration service: an automated tool (plus concierge tiers) that moves products, customers, orders, and SEO URLs between 140+ carts while the source store keeps selling. There's no public LitExtension API — automation means its connectors consuming your source/target store credentials.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Plan/run a migration (which source → which target cart?)
   - B) Decide DIY tool vs All-in-One (done-for-you) tier
   - C) Prepare access (API keys, bridge file) or fix a connection error
   - D) Handle mid-migration changes (new orders/customers → Smart Update)
   - E) Verify results (entity counts, variants, SEO redirects) or estimate cost

2. **Entity counts?** Products / customers / orders on the source — pricing and the order-history decision hinge on them.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which migration approach/tool (LitExtension vs Cart2Cart vs native importer vs CSV) | `/sales-store-migration {question}` |
| Migration strategy — redirect maps, cutover sequencing, integration re-wiring | `/sales-store-migration {question}` |
| Which destination platform to move TO | `/sales-checkout {question}` |
| SEO strategy beyond redirect mechanics | `/sales-seo {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-store-migration {original question}`"

Otherwise, answer LitExtension-specific questions directly using Step 3.

## Step 3 — LitExtension platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities, entity-count pricing levers, the safe migration sequence, per-cart access preparation, and when NOT to use LitExtension.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Always run the free demo migration first** (~20 products/customers/orders) and inspect the sample in the target — variants, images, prices, SEO URLs — before paying for the full run.
- **Cut cost with the order-history lever**: pricing scales with entity counts and order history usually dominates — migrate full catalog + customers but limit orders to the retention actually needed, archiving older orders as CSV.
- **Schedule cutover inside the post-migration window**: re-migration/Smart Update is free for a limited period (~3 months, ~10% data-growth cap) — run the full migration, verify, then Smart Update the delta of orders/customers that arrived during the window at cutover.
- **Tell the user customer passwords generally don't migrate** — carts hash differently; plan a password-reset campaign for migrated customers.
- **Any automation/API/scripting question gets the access-prep walkthrough as the practical answer**: after stating there's no public API, explain what LitExtension's connectors need — per-cart API keys following the guides at litextension.com/migration-guide (Shopify custom-app token, WooCommerce REST keys, etc.), or a bridge-file upload for API-less self-hosted carts (removed after migration).
- **Remove the bridge file after migration** on self-hosted carts — it's privileged code sitting in the webroot.
- **Verify before DNS cutover**: entity counts per type, spot-checked variants/orders, and a *tested* 301 redirect map — redirect testing is the single most underestimated step in replatforms.
- **Present pricing as estimator-driven and best-effort** — point the user to LitExtension's on-site estimator with their entity counts rather than quoting figures.
- **Calibrate review expectations**: LitExtension's near-uniform 5-star review profile is flagged by comparison sites as suspiciously clean — set expectations from the demo migration result, not the testimonials.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially the post-migration window terms and pricing model.*

- **No public API, no webhooks** — you can't script LitExtension itself; automation is limited to what the tool offers. Custom pipelines belong in `/sales-store-migration` territory.
- **Order history drives the bill** — a 50k-order store pays mostly for orders it may never look at; decide retention first.
- **Passwords don't cross carts** — migrated customers need resets; unannounced, this looks like broken accounts.
- **The source store keeps selling — that's a feature AND a trap**: every sale after the migration snapshot exists only on the source until Smart Update runs. Cut over without it and orders are stranded.
- **Bridge files are webroot code** — required for API-less self-hosted carts; remove after use.
- **Field/plugin custom data needs explicit mapping** — WooCommerce plugin fields, BigCommerce price lists, OpenCart image paths are the recurring per-pair surprises; the demo migration is where you catch them.

## Related skills

- `/sales-store-migration` — Store-migration strategy: tool selection (LitExtension vs Cart2Cart vs Migratly vs native/CSV), redirect maps, cutover sequencing, integration re-wiring
- `/sales-checkout` — Choosing the destination platform
- `/sales-shopify` — Shopify platform help (the most common migration target)
- `/sales-ecwid` — Ecwid platform help (supported source/target)
- `/sales-prestashop` — PrestaShop platform help (supported source/target)
- `/sales-seo` — SEO strategy around a replatform
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: WooCommerce → Shopify with live sales (developer/automation)
**User says**: "We're moving from WooCommerce to Shopify with LitExtension but we get ~50 orders a day — how do we not lose any?"
**Skill does**: Lays out the zero-downtime sequence — demo first, full migration with SEO URLs while Woo keeps selling, verify + test redirects on the target, then at cutover run Smart Update to pull the delta of orders/customers that arrived since the snapshot (free within the post-migration window) — and flags the password-reset campaign for migrated customers.
**Result**: Cutover with zero stranded orders and no surprise "my account is broken" tickets.

### Example 2: Cost estimate sticker shock
**User says**: "The LitExtension estimator quoted way more than $59 for our store — why?"
**Skill does**: Explains entity-count pricing (products + customers + orders) and that order history usually dominates; recommends limiting migrated orders to the retention actually needed (e.g. 24 months) with a CSV archive for the rest, then re-running the estimator with real counts.
**Result**: A materially lower quote with no loss of operationally relevant data.

### Example 3: Post-migration verification
**User says**: "LitExtension says our migration finished — how do I know it actually worked before switching DNS?"
**Skill does**: Runs the verification checklist — entity counts per type against the source, spot-check variant structures/prices/images, confirm order↔customer linkage, and *test* the 301 redirect map (the most underestimated step) — before any DNS change; books Smart Update for the cutover delta.
**Result**: Cutover happens on evidence, not on the tool's completion banner.

## Troubleshooting

### Source or target won't connect
**Symptom**: The tool can't reach a store during setup.
**Cause**: Missing/under-scoped API credentials, or a self-hosted cart needing the bridge file.
**Solution**: Follow LitExtension's per-cart guide (litextension.com/migration-guide) — e.g. Shopify custom-app token with read scopes, WooCommerce REST consumer key/secret; for API-less self-hosted carts upload the bridge file to the store root (and remove it after migration).

### New orders missing on the new store after cutover
**Symptom**: Orders placed during the migration window aren't on the target.
**Cause**: The migration is a snapshot; the source kept selling afterward.
**Solution**: Run Smart Update/re-migration to sync the delta — free within the post-migration window (~3 months, ~10% growth cap). Schedule cutover so the delta sync is the last step.

### Migrated customers can't log in
**Symptom**: Customers report broken accounts on the new store.
**Cause**: Password hashes don't transfer between carts.
**Solution**: This is expected — send a proactive password-reset campaign at cutover and say why; some target carts support forced-reset-on-first-login flows.
