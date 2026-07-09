# Sellfy Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, webhook surface, pricing, and integrations captured from live sources on this date. Key facts to re-verify: (1) **no public REST CRUD API** — only outbound webhooks + a Zapier API token (`sellfy.com/user/integrations/apps/zapier`); (2) **7 webhook events** with **no HMAC signature**, JSON POST, money in **cents**; (3) **annual sales-volume caps** Starter ~$10k / Business ~$50k / Premium ~$200k force upgrades; (4) **0% Sellfy fee** but processor (Stripe/PayPal ~2.9%+30¢) still applies; (5) **not a Merchant of Record** — seller owns VAT/GST/sales tax; (6) conversion features (upselling, cart abandonment, affiliate marketing) are **Business+**; (7) digital protection = **PDF stamping + download limits**. Re-verify specifics (especially pricing/caps and whether a REST API has been introduced) against current docs before relying on them.
