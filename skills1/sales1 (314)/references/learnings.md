# LitCommerce Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, pricing, and integration surface captured from live sources on this date (litcommerce.com, /pricing, help.litcommerce.com). Re-verify specifics against current docs before relying on them.

**2026-06-29**: Confirmed via LitCommerce's own LLM docs interface — **no public REST API, no webhooks, no MCP server**. LitCommerce consumes the marketplaces' APIs on the user's behalf. The only programmatic surfaces are inbound CSV/XML/Google-Sheet import (auth: none / Basic / Digest / auth-header token / Amazon S3) and outbound Product Feed export. Integrate at the **Main Store** layer (Shopify/WooCommerce/BigCommerce API + webhooks), not "through" LitCommerce.

**2026-06-29**: Sync is **every 15 minutes** and **one-directional (Main Store → channels)** for inventory — this near-time (not real-time) cadence is the documented cause of overselling during bursts. Standard mitigation is an inventory rule that sets a channel out of stock at qty = 1–2 (a buffer). Editing stock directly on a marketplace does not flow back.

**2026-06-29**: Two separate products with separate pricing — the **Multichannel Listing Tool** (channels × listings, from ~$29/mo, 7-day free trial) and the **Product Feed Tool** (free for 2 feeds; hourly sync + AI Smart Setup on paid). "Feed" is for ad/shopping/AI-search engines, not marketplace order sync. Listing counts are inflated by variations — recount before assuming a tier fits.

**2026-06-29**: No relevant GitHub org for LitCommerce (the `LitGroup` GitHub org is an unrelated Russian entity at litgroup.ru; LitCommerce's parent is LitGroup/LitExtension at litgroup.io). `github:` field intentionally omitted from frontmatter.

**2026-06-29**: Help center exposes machine-readable docs — `help.litcommerce.com/{section}/overview.md?ask=<question>`, `sitemap.md`, and `llms-full.txt`. Useful for grounding answers; the live help article HTML URLs change slugs (several 404'd during research), so prefer the `.md`/ask interface.
