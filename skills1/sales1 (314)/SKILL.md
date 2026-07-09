---
name: sales-litcommerce
description: "LitCommerce platform help — multichannel listing & inventory-sync tool that connects one Main Store (Shopify, WooCommerce, Wix, BigCommerce, Squarespace) to 20+ marketplaces (Amazon, eBay, Etsy, Walmart, TikTok Shop, Google, Facebook, Temu, Reverb, Faire, Shopee) with a 15-minute price/inventory/order sync, plus a Product Feed tool that exports a catalog to 300+ ad/shopping/AI-search channels. Use when LitCommerce listings won't sync or won't connect to eBay/Amazon, items oversell despite inventory sync being on, product-ID/GTIN mapping fails across channels, the TikTok Shop or Facebook connection keeps breaking, picking a LitCommerce plan by channels × listings, or building a product feed for Google Shopping/Meta/LLM search. Do NOT use for choosing between multichannel tools like Sellbrite/Codisto/CedCommerce (use /sales-multichannel-selling) or cross-tool checkout-conversion strategy (use /sales-checkout). Note: LitCommerce has no public REST API or webhooks."
argument-hint: "[describe what you need help with in LitCommerce]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, multichannel, platform]
---

# LitCommerce Platform Help

LitCommerce connects one **Main Store** (Shopify, WooCommerce, Wix, BigCommerce, Squarespace, or a CSV/XML file) to 20+ marketplaces and sales channels, keeping **listings, price, inventory, and orders** in sync from a single dashboard. It runs an automatic sync **every 15 minutes** and ships a separate **Product Feed tool** for exporting a catalog to ad/shopping engines. Critically, **LitCommerce has no public REST API or webhooks** — you automate *into* it via CSV/feed imports and it talks to the marketplaces' own APIs for you. This skill covers that integration surface and the sync/connection pain points that trip people up.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you need (skip if the prompt already says):

1. **What's the goal?** (a) fix a sync/connection/overselling problem, (b) set up listings on a new channel, (c) build/export a product feed, (d) automate around LitCommerce (no API — feeds/CSV), (e) pick a plan or weigh fees.
2. **Which Main Store + channels?** Shopify/WooCommerce/Wix/BigCommerce/Squarespace/file as the source, and which marketplaces (Amazon, eBay, Etsy, Walmart, TikTok Shop, Facebook, Temu, …).
3. **Which tool?** The **Multichannel Listing Tool** (list + sync) or the **Product Feed Tool** (export to ad/shopping/AI channels) — they price and behave differently.

Skip-ahead rule: if the user's prompt already contains enough context, go straight to Step 2.

## Step 2 — Route or answer directly

Map the request to the right home. When routing, give the exact command.

| The user's real problem | Route to |
|---|---|
| Choosing *between* multichannel tools (LitCommerce vs Sellbrite/Codisto/CedCommerce/Channable), channel-expansion strategy | `/sales-multichannel-selling {question}` |
| Cross-tool checkout-conversion strategy (order bumps, AOV, cart abandonment) | `/sales-checkout {question}` |
| The Main Store platform itself (Shopify/WooCommerce/BigCommerce/Wix/Square setup or API) | `/sales-shopify`, `/sales-bigcommerce`, `/sales-wix`, or `/sales-square-online {question}` |
| Getting a product catalog to rank in AI search / building llms.txt strategy | `/sales-ai-visibility {question}` |
| Not sure which skill | `/sales-do {question}` |

Anything LitCommerce-specific (sync, channel connections, feeds, plan gates, overselling) — answer here using Step 3.

## Step 3 — LitCommerce platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities & automation surface, pricing/plan gates, the data model with JSON shapes, feed/CSV recipes, and integration patterns.

For the integration surface in detail (no public API; CSV/feed import auth, Product Feed export, the help-docs query interface, channel auth), read `references/litcommerce-api-reference.md`.

Answer using only the relevant section — don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide loaded — focus on the user's situation:

- **Automation reality:** There is **no public REST API and no webhooks**. You can't subscribe to "order created" or pull orders out of LitCommerce programmatically. Pull orders from the **Main Store's** API instead (Shopify/WooCommerce/BigCommerce) — LitCommerce writes channel orders back into the Main Store, so the store is your integration point. Feed *into* LitCommerce via **CSV/XML/Google-Sheets import** (a file Main Store) on a schedule.
- **Overselling:** the 15-minute sync is **near-time, not real-time** — during a flash sale two channels can both sell the last unit inside one window. Set an **out-of-stock buffer rule** (mark a channel out of stock at qty ≥ 1–2) so the safety margin absorbs the lag.
- **Connections:** eBay/Amazon/TikTok/Facebook auth is the #1 setup friction. It's per-channel OAuth into the marketplace; re-auth when tokens lapse. If a channel "won't connect," it's usually a marketplace-side account/permission issue, not LitCommerce.
- **Plan math:** priced by **channels × listings** (from ~$29/mo). Count distinct *channels* and total *listings* (variations can multiply listing count) before picking a tier; 20% off annual.
- **Feeds:** the Product Feed tool is a separate product with its own free tier — use it for Google Shopping/Meta/Pinterest and **AI-search feeds (LLMs.txt, ChatGPT/OpenAI)**, not for marketplace order sync.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

- **No public API, no webhooks, no MCP.** LitCommerce uses the *marketplaces'* APIs on your behalf; it exposes nothing you can build on. Integrate at the **Main Store** layer instead. Don't promise an "order webhook from LitCommerce."
- **15-minute sync is near-time → overselling happens anyway.** Inventory updates batch every 15 min; high-velocity SKUs can oversell within a window. Use the **out-of-stock-at-N buffer rule**; don't rely on the UI claim of "real-time."
- **Inventory sync is one-directional.** Main Store → channels for stock. Editing stock *directly on a marketplace* won't flow back to your Main Store/LitCommerce and will be overwritten on the next sync.
- **Channel connection is the hard part.** eBay/Amazon/TikTok Shop/Facebook OAuth + policy mapping is fiddly; setup is **not** one-click. Connection failures are usually marketplace account/permission issues.
- **Product-ID/GTIN mapping breaks listings.** Amazon GTIN-exemption, EAN/UPC mismatches, and SKU mapping across channels are common error sources — fix the identifier on the Main Store, not per-channel.
- **Two products, two bills.** The Multichannel Listing Tool and the Product Feed Tool are separate (separate free tiers/pricing). "Feed" ≠ marketplace order sync.
- **Pricing is per channels × listings.** Variations inflate listing counts; recount before assuming you fit a tier.

## Related skills

- `/sales-multichannel-selling` — Cross-tool strategy: which marketplaces to sell on, oversell prevention, and choosing a channel manager (LitCommerce vs Sellbrite/Codisto/CedCommerce/Channable/Linnworks).
- `/sales-checkout` — Checkout-conversion strategy on your storefront (order bumps, AOV, cart recovery).
- `/sales-shopify` — Shopify commerce backend (pull orders/products via the GraphQL Admin API — your real integration point behind LitCommerce).
- `/sales-bigcommerce` — BigCommerce backend (REST v3/v2, webhooks) as the Main Store.
- `/sales-wix` — Wix eCommerce as the Main Store.
- `/sales-ai-visibility` — Getting product/brand content to surface in ChatGPT/Perplexity (the Product Feed AI/LLMs.txt feeds feed this).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "How do I pull my marketplace orders into my CRM/warehouse from LitCommerce?"
A developer/automation question — and the answer reframes it. **LitCommerce has no public API or webhooks**, so you cannot pull orders from LitCommerce directly. But LitCommerce *writes* channel orders (Amazon/eBay/Etsy/…) back into your **Main Store** as orders. So integrate at the store: use the **Shopify Admin API** (`/admin/api/.../orders.json` or GraphQL) or **WooCommerce REST** (`/wp-json/wc/v3/orders`, HMAC webhooks) to read consolidated orders, filtered by the channel/source tag LitCommerce stamps. To push data *into* LitCommerce, point it at a **file Main Store** (CSV/XML/Google Sheet) it re-imports on a schedule. Point them to `references/litcommerce-api-reference.md` for the import auth options.

### Example 2: "My store keeps overselling even though inventory sync is on"
The #1 LitCommerce pain point. Explain the cause: sync runs **every 15 minutes** (near-time), so within one window two channels can each sell the last unit. Fix: set an **inventory rule** to "set the product to out of stock on [channel] at quantity = 1 (or 2)" so the buffer absorbs the sync lag; confirm sync direction is Main Store → channels (edits on a marketplace don't flow back); for fast-movers, lower the buffer threshold or reduce reliance on the last unit. Note that no tool with batch sync is truly real-time — buffers are the standard mitigation.

### Example 3: "Free vs paid, and which plan for 6 channels and 8,000 products?"
Pricing/plan-gate question (answer from the guide). There's a **7-day free trial** with full access; paid is **pay-as-you-go by channels × listings** from ~$29/mo (3 channels/1,000 listings) up to ~$369/mo (15 channels/100k), custom above; **20% off annual**. For 6 channels and 8,000 *products*, count listings carefully — variations multiply listing count, so 8,000 products with variants can exceed 10,000 listings and bump you a tier. The **Product Feed Tool** is billed separately (free for 2 feeds). Flag all pricing as best-effort and tell them to confirm current rates.

## Troubleshooting

### "My listings won't sync / I can't connect eBay or Amazon"
Setup is not one-click — each channel is a separate OAuth + policy mapping. Confirm the marketplace account itself is in good standing and has selling permissions (Amazon Professional selling plan, eBay business policies enabled). Re-authorize the channel if the token lapsed. Check that the product has the required identifiers for that channel (GTIN/UPC/EAN, or an Amazon GTIN-exemption). If eBay/Amazon support says "it's a LitCommerce issue," it's usually a missing marketplace permission or a category/identifier requirement surfaced through LitCommerce — fix it on the listing/Main Store. Use LitCommerce's per-channel **error reports** to see the exact rejection reason.

### "Inventory isn't matching across channels / items oversell"
Sync is **Main Store → channels every 15 minutes** and one-directional. Causes: (1) the 15-min window let two channels sell concurrently — add an **out-of-stock-at-N buffer rule**; (2) someone edited stock directly on a marketplace — that won't flow back and gets overwritten; (3) "No Manage Stock" products need a **fixed quantity rule**; (4) Shopify multi-location — confirm LitCommerce is syncing from the right location(s). Treat the Main Store as the single source of truth and never adjust channel stock by hand.

### "My product feed isn't updating on Google/Meta"
That's the **Product Feed Tool**, not the listing sync. On the **free plan there's no hourly sync** — feeds refresh on a slower cadence; upgrade for hourly. Confirm the feed format matches the destination (Google Shopping vs Meta catalog vs a generic CSV), that required attributes (id, title, price, availability, gtin) are mapped, and that multi-currency/multi-language variants are set if you sell across regions. For AI-search destinations, use the dedicated **LLMs.txt / ChatGPT-OpenAI** feed templates.
