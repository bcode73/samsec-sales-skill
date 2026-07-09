---
name: sales-multichannel-selling
description: "Multichannel & marketplace selling strategy — sell one product catalog across Amazon, eBay, Etsy, Walmart, TikTok Shop, Google Shopping, and Facebook/Instagram from a single store backend (Shopify, WooCommerce, Wix, BigCommerce). Covers which marketplaces to expand to, channel listing rules, inventory-sync conflicts and oversell prevention, order consolidation, product feeds, and when a builder's native multichannel feature is enough vs a dedicated channel manager (LitCommerce, Sellbrite, Codisto, CedCommerce, Channable). Use when deciding which channels to sell on, inventory or orders aren't syncing across marketplaces, items oversell across stores, picking a multichannel listing tool, listings get rejected on Amazon/eBay/Etsy, or planning marketplace expansion from your existing store. Do NOT use for single-store checkout-conversion optimization (use /sales-checkout), picking a Merchant of Record for tax (use /sales-merchant-of-record), or deep config of one tool like LitCommerce (use /sales-litcommerce)."
argument-hint: "[describe your multichannel situation — e.g., 'which tool to list my Shopify catalog on Amazon + eBay' or 'stop overselling across channels']"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, multichannel, marketplace, strategy]
---

# Multichannel & Marketplace Selling Strategy

Helps you **sell one catalog in many places** — Amazon, eBay, Etsy, Walmart, TikTok Shop, Google Shopping, Facebook/Instagram — from a single store backend, without the inventory, listing, and order chaos that breaks when you add channels manually. This is a tool-agnostic strategy skill: it frames the decisions (which channels, which tool, how to not oversell) across the whole category, then hands off to a specific platform skill for deep config.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user (lead with a best-effort answer if they've already told you most of this):

1. **What's the decision?**
   - A) **Which channels** to expand onto (Amazon vs eBay vs Etsy vs TikTok Shop vs Google/Meta)
   - B) **Which tool** — native builder feature vs a dedicated channel manager, and which one
   - C) **Fixing sync** — inventory/orders not matching across channels, overselling
   - D) **Listings rejected/not live** on a marketplace (identifiers, categories, policies)
2. **What's your store backend (source of truth)?** Shopify · WooCommerce · Wix · BigCommerce · Squarespace · Square · a spreadsheet/ERP. This decides which tools even connect.
3. **Catalog size & velocity?** Number of SKUs/variations, and how fast the fast-movers sell (drives the oversell-risk and tool tier).
4. **What do you sell?** New retail/DTC · handmade/vintage (Etsy/eBay) · resale/thrift (Poshmark/Mercari/Depop — different tool class) · branded products with GTINs.
5. **Stage/team?** Solo/maker · small team · scaling. Most makers want the lightest tool that won't oversell.

**Skip-ahead rule:** if the prompt already provides most of this, go straight to Step 4 with stated assumptions, then ask 1–2 critical clarifiers.

## Step 2 — Route or answer directly

| If the question is about… | Route to… |
|---|---|
| Deep config of **LitCommerce** specifically (sync rules, feeds, plan gates) | `/sales-litcommerce {question}` |
| The **store backend** itself (Shopify/BigCommerce/Wix/Square setup or API) | `/sales-shopify`, `/sales-bigcommerce`, `/sales-wix`, or `/sales-square-online {question}` |
| Single-store **checkout-conversion** (order bumps, AOV, cart abandonment) | `/sales-checkout {question}` |
| Picking a **Merchant of Record** for global tax | `/sales-merchant-of-record {question}` |
| Getting products to show up in **AI search** (LLMs.txt, ChatGPT shopping) | `/sales-ai-visibility {question}` |
| Generic iPaaS wiring into other tools | `/sales-integration {question}` |
| Not sure | `/sales-do {question}` |

Otherwise, answer from the framework below.

## Step 3 — Tool & channel comparison reference

**Read `references/platforms.md`** for the full comparison — the channel-manager landscape (LitCommerce, Sellbrite, Codisto/Shopify Marketplace Connect, CedCommerce, Channable, M2E Cloud, Linnworks, ChannelEngine, Vendoo), native-vs-dedicated tradeoffs, a channel-selection cheat sheet, and the oversell-prevention playbook.

Answer using only the relevant section. Don't dump the whole reference.

## Step 4 — Actionable guidance

### Pick channels where your product + buyers already are
- **Amazon** — largest reach, fiercest competition + fees; needs GTINs (or GTIN-exemption) and a Professional plan to list at volume. Best for branded/commodity products.
- **eBay** — strong for used, refurbished, parts, collectibles, and auction-style; flexible identifiers.
- **Etsy** — handmade, vintage, craft supplies, digital downloads, and personalization. Off-brand for mass-produced goods.
- **TikTok Shop** — social/impulse + live shopping; fast-growing but heavy on content and region rules.
- **Walmart** — curated approval, big reach for established retail brands.
- **Google Shopping / Meta (Facebook/Instagram) Shops** — these are **feeds/ads**, not marketplaces — you fulfill on your own store. Lowest-friction first expansion for a maker.
- **Resale (Poshmark/Mercari/Depop/Vinted)** — a different tool class (cross-listers like Vendoo), not the store-backend channel managers.

Sequence: start with the 1–2 channels closest to your existing buyers; don't light up 8 at once.

### Native builder feature vs a dedicated channel manager
- **Native is enough when:** few channels (Shopify/Wix/BigCommerce ship Amazon/eBay/Google/Meta connectors), modest SKU count, and the native sync interval is acceptable. Cheapest, fewest moving parts.
- **Use a dedicated channel manager when:** 3+ marketplaces, channel-native listing depth (eBay business policies, Amazon GTIN-exemption, Etsy personalization), bulk listing/templates, or you've already hit overselling. See `references/platforms.md` for which one fits.

### Overselling is the #1 failure — design for it
Every channel manager syncs in **batches** (intervals from ~minutes to, on weaker tools, a day). Real-time is rare. So:
- Treat your **store backend as the single source of truth**; never hand-edit stock on a marketplace.
- Set an **out-of-stock buffer** (channel goes out of stock at qty 1–2) so the sync lag can't sell the last unit twice.
- For fast-movers, lower max display qty or hold safety stock off-channel.
- Prefer tools with **faster sync** (15-min class) over once-a-day sync if you sell volume.

### Listings rejected/not live — it's almost always identifiers or policies
GTIN/UPC/EAN mismatches, missing Amazon GTIN-exemption, wrong category, or unset marketplace policies (eBay business policies, shipping templates) cause most rejections. Fix the data on the **source catalog**, not per-channel, so it stays fixed on re-sync.

If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Gotchas

> *Best-effort from research (2026-06) — tool features, sync intervals, and fees change frequently; verify on each vendor.*

1. **"Real-time sync" is marketing — it's batched.** Intervals range from ~15 min (LitCommerce, M2E) to **1–2 days** (older Codisto behavior). Slower sync = higher oversell risk. Always add a buffer rule regardless of the tool's claims.
2. **Inventory sync is usually one-directional** (store → channels). Editing stock on a marketplace gets overwritten on the next sync. Don't.
3. **Listing count, not product count, drives pricing.** Variations multiply listings — a few thousand products can blow past a tool's listing tier.
4. **Order consolidation ≠ fulfillment.** Most listing tools pull orders into your store but don't ship; if shipping/label printing is your pain, that's a different feature class (Sellbrite, Linnworks, Multiorders) — see `references/platforms.md`.
5. **Most of these tools have no public API/webhooks for *you*** (LitCommerce, many connectors). They talk to the marketplaces, not to your code. Integrate at the **store backend** layer for CRM/warehouse sync.
6. **Resale cross-listers are a separate category.** Vendoo/List Perfectly (Poshmark/Mercari/Depop) solve a different problem than store-backend channel managers — don't conflate them.
7. **Marketplace fees + ad costs stack on top of the tool fee.** Model total take-rate per channel (referral fee + closing fee + tool + ads), not just the SaaS price.

## Related skills

- `/sales-litcommerce` — LitCommerce platform help (multichannel listing & 15-min sync; Main Store → 20+ channels; no public API; Product Feed + AI-search feeds).
- `/sales-checkout` — Checkout-conversion optimization on your own storefront (order bumps, AOV, cart recovery).
- `/sales-shopify` — Shopify backend as the source of truth (Admin API, native channel apps).
- `/sales-bigcommerce` — BigCommerce backend (REST v3/v2, channels, webhooks).
- `/sales-wix` — Wix eCommerce backend.
- `/sales-square-online` — Square Online store unified with Square POS.
- `/sales-merchant-of-record` — Choosing a MoR (Paddle/Lemon Squeezy) for global tax vs owning tax.
- `/sales-ai-visibility` — Getting product/brand content to surface in ChatGPT/Perplexity (product AI feeds feed this).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "I'm on Shopify and want to add Amazon + eBay — native apps or a tool like LitCommerce?"
**Skill does**: Asks SKU count and how fast top items sell. For 2 channels and a modest catalog, Shopify's native Amazon/eBay/Google channels may be enough and cheapest. For channel-native depth (eBay business policies, Amazon GTIN-exemption), bulk listing templates, or if overselling has already bitten, recommends a dedicated channel manager and frames LitCommerce (15-min sync, maker pricing) vs Sellbrite (adds shipping) vs Codisto/Shopify Marketplace Connect (native, fewer channels). Hands deep config to `/sales-litcommerce`. Stresses starting with 1–2 channels + a buffer rule.
**Result**: A native-vs-tool decision matched to catalog size and a shortlist.

### Example 2: "My inventory is wrong across channels and I sold the same item twice"
**Skill does**: Explains the root cause — batched sync (not real-time) plus, often, hand-edits made directly on a marketplace. Fixes: make the store backend the single source of truth, enable an **out-of-stock-at-1-or-2 buffer** on every channel, stop editing stock on marketplaces (it's overwritten), and for fast-movers hold safety stock off-channel or lower max display qty. If their tool only syncs daily, recommend moving to a 15-min-class tool. Routes tool-specific buffer setup to that tool's skill.
**Result**: An oversell-prevention playbook plus a possible tool upgrade.

### Example 3: "Which tool to cross-list my thrift inventory on Poshmark, Mercari, and Depop?"
**Skill does**: Flags that this is the **resale cross-lister** category, not store-backend channel managers — recommends Vendoo/List Perfectly-class tools (per-listing cross-posting, delisting on sale, relisting), and notes the different workflow (one-of-a-kind items, no central store backend). Distinguishes it from LitCommerce/Sellbrite (which assume a Shopify/Woo backend + GTIN'd catalog). Adds the same anti-oversell discipline: delist everywhere the moment one platform sells the unique item.
**Result**: Correct tool class for resale, with the unique-item delisting caveat.

## Troubleshooting

### "Items oversell across my channels"
Batched sync means a window exists where two channels sell the last unit. Set an **out-of-stock buffer** (channel out of stock at qty 1–2) on every channel; make the store backend the source of truth; never edit stock on a marketplace (one-directional sync overwrites it); for high-velocity SKUs reduce max display qty or keep safety stock off-channel. If your tool only syncs once a day, that cadence is the problem — move to a faster-sync tool.

### "My listings keep getting rejected or won't go live on Amazon/eBay/Etsy"
Almost always identifiers or policies: missing/invalid GTIN/UPC/EAN, no Amazon **GTIN-exemption** where required, wrong category, or unset marketplace policies (eBay business/shipping policies, return policy). Fix the data on the **source catalog** so it persists across re-syncs, confirm the marketplace account has selling permissions (Amazon Professional plan, Walmart/TikTok approval), and read the tool's per-channel **error report** for the exact rejection reason instead of guessing.

### "Orders from marketplaces aren't all in one place / my CRM"
Most channel managers consolidate orders into your **store backend** but expose no API/webhook of their own. So integrate at the store: use Shopify/WooCommerce/BigCommerce order webhooks or scheduled API pulls (deduped on the marketplace order id) to feed a CRM/warehouse. If you also need shipping/label printing from one screen, that's a fulfillment feature — consider Sellbrite/Linnworks/Multiorders rather than a pure listing tool.
