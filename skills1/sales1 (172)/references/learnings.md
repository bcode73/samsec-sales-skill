# FastSpring Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-02**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them. Notes: FastSpring pricing is **quote-based/negotiable** (no public rate card; reported 8.9% or 5.9%+$0.95, sales-assigned by transaction type + volume). Much of developer.fastspring.com is **JS-rendered** — endpoint-level request/response JSON could not all be captured verbatim; base URL (`api.fastspring.com`), HTTP Basic auth, 250 calls/IP/min rate limit, and the full webhook event list + `X-FS-Signature` HMAC-SHA256 verification were captured cleanly. Classic Commerce API is deprecated (moved to github.com/fastspring/fastspring-api). Checkout-session path `/v2/checkouts/{checkoutPath}/sessions` came from the JS-rendered createsession page — verify against a live store (SBL is the more common embed path). Top user complaints: refunds keep the fee, high effective subscription rate (10–12%+), and support responsiveness.
