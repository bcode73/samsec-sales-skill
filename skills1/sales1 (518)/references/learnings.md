# SendOwl Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-02**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

- Orders resource is on `/api/v1_3/orders` while most other resources are `/api/v1/`; a few order sub-actions (refund, resend_email, cancel_subscription, download_restrictions, override_country) stay on `/api/v1/`.
- Webhooks POST raw JSON ("order Liquid"), not form params — HMAC must be computed over the raw body; Rails exposes the header as `HTTP_X_SENDOWL_HMAC_SHA256`.
- Pricing shifted to a subscription model with volume caps (orders/yr + sales/yr) and **no free tier** and **no per-transaction fee** as of 2026-07; reviewers report abrupt, large price increases — keep this claim dated and re-verify.
- SendOwl stores download *links* (historically ~250 files), not unlimited raw file hosting — a recurring reviewer complaint; host large media externally.
- `check_valid` license endpoint must never be called from distributed client software (leaks credentials) — proxy server-side.
