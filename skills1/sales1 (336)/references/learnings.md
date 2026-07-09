# Medusa Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, Admin/Store API surface, auth routes, events/subscribers model, and Medusa Cloud pricing captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Medusa has **no outbound-webhook UI** — the #1 point of confusion for people coming from Shopify/Stripe. "Events" are internal (pub/sub inside the app); you handle them in subscriber files (`src/subscribers/*.ts`) and make any external HTTP call yourself, or add a community webhook plugin. Outbound retries/signing/logging are not built in.

**2026-06-28**: v1 vs v2 is a real trap. v2 uses `@medusajs/js-sdk` + `@medusajs/framework`, the modular/workflow system, and `/auth/{actor_type}/{provider}` routes. Lots of tutorials and the old `medusa-react`/`@medusajs/medusa-js` client are v1 and won't match.

**2026-06-28**: Three auth methods — JWT Bearer (from auth routes), admin API key in `Authorization: Basic` (base64 optional in v2), and cookie session (`/auth/session`). Storefront Store API additionally requires the `x-publishable-api-key` header to scope the sales channel.

**2026-06-28**: Engine is MIT/free with 0% GMV fee; Medusa Cloud sells managed infra only. Develop ($29/mo) is dev/preview-grade (no custom domain/autoscaling); production starts at Launch ($99/mo). Self-host needs Postgres + Redis + Node.
