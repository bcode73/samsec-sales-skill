# Square Online Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, API surface (Catalog/Orders/Inventory/Payments/Checkout/Customers), pricing, webhooks (HMAC over notification-URL + raw body, `x-square-hmacsha256-signature`), OAuth (30-day access-token expiry), and the official Square MCP server captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: Square Online has **no site-builder API** — you automate the commerce layer (the standard Square APIs that also power Square POS), not the storefront pages/theme. Confirmed by the absence of a Sites/Online-Store API in the reference.

**2026-06-29**: The #1 user complaint (Square Community, Sept 2025) is **inventory sync lag → overselling** between POS and Square Online: online stock not decrementing on online orders, items stuck "sold out," the per-item sync toggle silently turning off, and 24h+ sync delays. Mitigation: treat the Inventory API as source of truth, enable `track_inventory` per variation, subscribe to `inventory.count.updated`, and reconcile on a schedule.

**2026-06-29**: Pricing is best-effort and ambiguous — Square consolidated à-la-carte subscriptions into unified plans (Free $0 / Plus ~$49 / Premium ~$149 / Square Pro custom for >$250k/yr). Older Square-Online-specific numbers (Plus $29 / Premium $79) may still surface in reviews. Online processing ~3.3% + 30¢ on Free, lower on paid tiers; in-person 2.6% + 15¢. Confirm current rates before quoting.
