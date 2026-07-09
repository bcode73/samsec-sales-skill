# Swell Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — platform docs, API surface (Backend REST + Frontend swell-js/GraphQL), pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-29**: Pricing sources disagree. The help-doc page (`/help/pricing/pricing-plans`) showed older/higher numbers ($299–$2,000); the live pricing page (`swell.is/pricing`) shows Starter **$29** / Basic $79 / Standard $299 / Unlimited $2,250 / Custom with **annual sales caps** ($50K/$250K/$1M/$5M) and revenue-ceiling overages (2%/1.5%/1%/0.4%). Trust the live pricing page; flag both as best-effort.

**2026-06-29**: Two key types — **secret** (Backend API, server-only) and **public** (Frontend swell-js/GraphQL, browser-safe), both from Developer → API keys; store ID shown there too.

**2026-06-29**: Official libs (`swell-node`, `swell-php`) use a custom wire protocol on **port 8443**. If calls hang, the host is likely blocking 8443 — fall back to plain REST/HTTP Basic over 443.

**2026-06-29**: Webhooks are **thin** (`{id,date_created,model,type,data:{id}}`) and have **no HMAC** — verify via the published Swell IP allowlist + a secret URL/header, return 2xx within 10s, then GET the full record by `data.id`. Hooks **auto-disable** after repeated failures (~3 days) / `auto_disabled` after 7 days.

**2026-06-29**: Subscription migration footgun — **do NOT pass `$migrate: true`** when importing existing subscriptions; it skips the events that schedule billing and corrupts next-charge dates. Import as normal records and verify the computed next charge in a sandbox.

**2026-06-29**: GraphQL endpoint is `https://<store-id>.swell.store/graphql/v2` (public key in `Authorization` header); playground at `/playground`.

**2026-06-29**: No MCP server found for Swell as of this date — wrap the Backend API yourself if an AI agent needs tool access.
