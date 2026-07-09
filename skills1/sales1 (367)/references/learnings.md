# Multichannel Selling Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — channel-manager landscape, sync behaviors, and channel-selection guidance captured from comparison research (LitCommerce alternatives/competitor articles, G2, vendor sites) on this date. Re-verify tool features, sync intervals, and fees against current sources before relying on them.

**2026-06-29**: Created from the backlog "Multichannel / omnichannel selling from one catalog" problem row. Warranted by 9+ tools in the category (LitCommerce, Sellbrite, Codisto/Shopify Marketplace Connect, CedCommerce, Channable, M2E Cloud, Linnworks, ChannelEngine, Vendoo) and the recurring "inventory/orders aren't syncing across channels" complaint. Distinct from /sales-checkout (single-store conversion).

**2026-06-29**: Two distinct tool classes — **store-backend channel managers** (assume a Shopify/Woo backend + GTIN'd, stocked catalog) vs **resale cross-listers** (Vendoo/List Perfectly — one-of-a-kind items, no central store, delist-on-sale). Don't recommend a channel manager for resale or vice versa.

**2026-06-29**: Overselling is the #1 failure mode and is structural — all these tools sync in batches (~15 min for LitCommerce/M2E down to ~1–2 days for older Codisto behavior), not real-time. The universal mitigation is an out-of-stock buffer rule (channel out of stock at qty 1–2) + treating the store backend as the single source of truth. This applies regardless of vendor "real-time" marketing claims.

**2026-06-29**: Most channel managers expose no public API/webhooks for the seller (confirmed for LitCommerce) — they consume marketplace APIs. For CRM/warehouse pipelines, integrate at the store-backend layer (Shopify/Woo/BigCommerce order webhooks or API), not "through" the channel manager.
