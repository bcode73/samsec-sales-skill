# Checkout Page Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform docs, REST API surface (base `https://api.checkoutpage.com/v1`, Bearer auth, cursor pagination, 500/min store + 100/min key rate limits), verbatim `conversion` webhook payloads (payment/subscription/submission), native MCP server (`https://mcp.checkoutpage.com`, OAuth, 13 tools), and pricing captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-07-04**: Webhook payloads carry **no documented HMAC signature or retry policy** — treat as unsigned (tokenize the endpoint URL + re-fetch via API to verify). Re-check live docs for a signing scheme.

**2026-07-04**: Money in webhook payloads is a **decimal string in the display currency** (`"23.99"`), NOT cents — differs from SamCart/Sellfy. Parse as decimal.

**2026-07-04**: Live subscription payload spells the trial-start field **`trailStart`** (vendor typo); `trialEnd` is spelled correctly. Read both exactly as sent.

**2026-07-04**: The docs render endpoints in both REST (`GET /v1/checkout-pages`) and action (`/v1/checkout-pages/list`) styles in different views — confirm the exact path style against live docs before coding. Docs site is partly JS-rendered.

**2026-07-04**: NOT a Merchant of Record — runs on the seller's own Stripe account, so the seller owns tax (Stripe Tax available). Contrast Lemon Squeezy/Paddle (true MoR).
