# Saleor — Learnings

Accumulated, dated knowledge about the Saleor platform. Append new findings with the date you learned them.

**2026-06-29**: Research baseline established from saleor.io, docs.saleor.io (authentication, quickstart/api, webhooks overview + payload-signature), saleor.io/pricing, and comparison articles (Swell/Vendure roundups). Key facts captured:
- GraphQL-only (single `/graphql/` endpoint), no REST. Built on Python/Django, BSD-3 license, open-source.
- Auth: JWT (RS256). Users via `tokenCreate` (access + refresh), Apps get long-lived tokens. OIDC (SSO + legacy proxy). JWKS at `/.well-known/jwks.json`. `tokenRefresh`/`tokenVerify`/`tokensDeactivateAll`.
- **Webhook signature: JWS RS256 (detached payload) is the DEFAULT; HMAC SHA-256 is DEPRECATED** and only used when a `secretKey` was set. Verify against the RAW body. This is the #1 integration gotcha.
- Saleor HAS native outbound webhooks (sync + async, 160+ events, GraphQL `subscription`-shaped payloads) — unlike Medusa. Headers: `Saleor-Event`, `Saleor-Domain`, `Saleor-Signature`, `Saleor-Api-Url`. ~20s round-trip cap (2s connect + 18s response). `webhookDryRun` tests async only.
- Checkout flow: `checkoutCreate` (variant IDs + channel) → email/address updates → `checkoutDeliveryMethodUpdate` → payment → `orderCreateFromCheckout` (**needs app token**) → `orderMarkAsPaid`.
- Pagination: Relay cursor (`first`/`after`, `pageInfo`), channel-scoped lists.
- Pricing (best-effort): self-host OSS free (no per-sale fee); Cloud Sandbox free but **non-commercial**; Select ~$1,599/mo (≤$200k GMV, 0.8% over), Volume ~$3,999/mo (≤$1M GMV, 0.4% over), Enterprise custom (0.2%). Add-ons: Accelerator ~$6k, Forward Deployed Eng ~$12k. OSS↔Cloud migration if compatible version.
- Self-host: needs Postgres + Redis (Celery worker+beat) + Django. **`saleor-platform` repo is dev-only, not production**; Core Dockerfile is production-ready. `ALLOWED_HOSTS` misconfig → "Invalid host header"/blank page is a common self-host bug.
- Not a Merchant of Record — tax via tax Apps / sync webhooks (Avalara etc.).
- Audience caveat: Cloud commercial pricing leans mid-market/enterprise; the **self-hosted OSS path is the maker/GTM-engineer fit**.

**2026-06-29**: WebFetch on Saleor docs returned condensed (summarized) content rather than verbatim, because docs.saleor.io is client-rendered. The api-reference.md is assembled from authoritative doc content but exact GraphQL field shapes should be re-verified against the live schema.
