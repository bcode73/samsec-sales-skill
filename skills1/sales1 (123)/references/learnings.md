# Convertri Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, automation surface (no public REST API; Zapier API key + custom webhooks with `cverify` SHA-1 signing), pricing (Convert $99 / Scale ~$199 / Maximize $299; impression caps 250k/500k/unlimited; $30 per extra 250k impressions; video bandwidth 100GB/mo, $10 per extra 100GB), and webhook payload fields captured from live sources (help.convertri.com, zapier.com) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Convertri has **no public REST API** — the most important integration fact. You cannot create/read pages, funnels, or products programmatically. Data-out automation is custom webhooks (5 types: Sale, Rebill, Rebill Cancellation, Refund, Lead Capture) + Zapier (8 triggers). The single account-level "API key" only authenticates the Convertri app inside Zapier.

**2026-06-28**: `cverify` is an HMAC-style signature but uses SHA-1 and only the first 8 chars uppercased — easy to implement wrong. Order matters: drop `cverify`, sort remaining keys alphabetically, pipe-join the values, append `|<secret>` last, UTF-8 encode, SHA-1, uppercase first 8.

**2026-06-28**: Money fields (`ctransamount`, `ctaxamount`, `cshippingamount`) are integers in pennies/smallest unit ($10.00 = 1000). `ctranstime` is a Unix timestamp in seconds. Payment method is Stripe or PayPal only.

**2026-06-28**: Affiliate program exists — ~30% lifetime recurring commission, instant approval, must be an active Convertri user (free trial counts). Logged to _internal/affiliates.md.
