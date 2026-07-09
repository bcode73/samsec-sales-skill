# LitExtension Platform Reference

## Overview

LitExtension (litextension.com) is an ecommerce migration service: an automated tool plus concierge tiers that move store data between 140+ carts — the widest coverage in the category (Cart2Cart ~85). 15+ years, 300k+ migrations. The source store stays live during migration; a post-migration window covers re-runs and deltas. It is a *service you configure*, not a platform with a public API — automation means its connectors consuming your source/target store APIs.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Automated migration tool (DIY) | Web app: connect source + target, map entities, run | **UI-driven**; connectors consume store APIs / bridge files — no public LitExtension API |
| Entities migrated | Products + variants, customers, orders, coupons, pages/blogs, reviews (cart-dependent), custom fields | Selected per migration |
| SEO URL migration | Preserve/redirect old URLs (optional add-on) | Configured in the tool |
| Demo migration | Free limited run (~20 products / 20 customers / 20 orders) | **Always run first** |
| Re-migration & Smart Update | Re-run or delta-sync new orders/customers after the initial pass — free within ~3 months if data growth ≤ ~10% | Tool feature |
| Auto Test service | AI-assisted post-migration data verification | Service add-on |
| All-in-One / Done-for-You | Experts run the whole thing with a dedicated assistant | Concierge |
| Source connections | Per-cart API keys (Shopify tokens, Woo REST keys, etc.), "bridge" file uploads for self-hosted carts, CSV/SQL for custom sources | Documented per cart in their migration guides |

No public API, no webhooks, no MCP server. Integration = preparing credentials and letting their connectors work.

## Pricing, limits & plan gates

*Best-effort — verify with their on-site estimator.*

- **Entity-count pricing** starting around $59 — the estimator prices by number of products + customers + orders. Big order histories dominate cost; migrating "all orders" vs "last N months" is the main cost lever.
- **Demo migration free** (limited entities). **Re-migration/Smart Update free for ~3 months** post-migration when data hasn't grown more than ~10% — schedule the cutover inside that window.
- **All-in-One** (done-for-you) priced separately and substantially higher — the trade for not touching the tool.
- 30-day money-back guarantee on the automated tool (a differentiator vs Cart2Cart).

## Data model (what a migration actually maps)

```text
Source cart ──connector/bridge──▶ LitExtension mapping ──▶ Target cart
  products+variants  → target catalog (attribute/option mapping differs per cart pair)
  customers          → accounts (passwords rarely migrate — carts hash differently; expect reset emails)
  orders             → order history (linked to migrated customer + product IDs)
  SEO URLs           → redirect table / target URL structure
```

Key mapping gotchas by pair: WooCommerce plugin-created fields need custom-field mapping; OpenCart image paths are quirky; BigCommerce price lists/currencies need review; Wix content-heavy pages may not map 1:1.

## Quick-start recipes

### Recipe 1 — The safe migration sequence

1. **Run the free demo migration first** and inspect the 20-item sample in the target — variant structure, images, prices, SEO URLs.
2. Prepare credentials: source + target API keys per LitExtension's per-cart guides (or upload the bridge file for self-hosted carts).
3. Full migration with SEO URLs enabled; keep selling on the source store.
4. Verify (counts per entity, spot-check variants/orders), build and test the 301 redirect map, re-wire apps/payment/webhooks on the target.
5. **Cut over, then run Smart Update** to pull orders/customers that arrived during the window (free within the post-migration window).

### Recipe 2 — Estimate cost before committing

Count entities on the source (products, customers, orders — most carts show these in admin or via a quick API call), then use the on-site estimator. To cut cost: migrate full catalog + customers but limit orders to the retention you actually need (e.g. 2 years), archiving the rest as CSV.

### Recipe 3 — Prepare API access (the usual blocker)

Per-cart guides at litextension.com/migration-guide: e.g. Shopify custom-app Admin token with read scopes; WooCommerce REST consumer key/secret (read); self-hosted carts without APIs get a **bridge file** uploaded to the store root (remove it after migration — it's privileged code in your webroot).

## Integration patterns

- **Zero-downtime replatform**: source stays live → full migration → verification + redirect testing on the target behind a staging domain → DNS/theme cutover → Smart Update for the delta. Never point DNS before redirects are tested.
- **Cost-bounded history**: full catalog + customers, orders limited by date; old orders archived out-of-band.
- **Agency workflow**: the Agency Partner tier (discounts, account manager) for repeated migrations; pair with the Auto Test service instead of hand-verifying every entity.
- **When NOT LitExtension**: single-cart pairs with strong native importers (e.g. Shopify's WooCommerce importer) or tiny stores (CSV is free) — weigh via `/sales-store-migration`.
