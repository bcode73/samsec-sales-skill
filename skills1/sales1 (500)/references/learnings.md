# Salesmate Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, v4 REST API surface (published Postman collection at apidocs.salesmate.io), pricing, and automation surface captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Auth is header-based API key — header `accessToken` carries your Access Key (My Account → Access Key) and `x-linkname` is your account host (e.g. `demo.salesmate.io`). The official Postman collection confusingly stores the `accessToken` value in a variable it labels `sessionToken`; Make's connector surfaces three fields (API Key, API Token, Session Token). A `401` is almost always a wrong/missing `accessToken` or `x-linkname`.

**2026-06-28**: Base URL is per-account: `https://{link_name}.salesmate.io/apis/{module}/v4/...`. Use v4 — v1/v3 were slated for deprecation May 1, 2023 (Products/Lookup Fields still expose v1/v3 paths).

**2026-06-28**: Rate limit is **1500 API calls/hour per link** (account-wide, not per-plan). No documented rate-limit response header — track call count client-side.

**2026-06-28**: Search/list pagination is **offset-based** (`?rows=` page size up to 250, `?from=` offset); `Data.totalRows`/`Data.totalPages` drive iteration. Search is a POST with a `displayingFields` + `filterQuery` (rule group) + `sort` body.

**2026-06-28**: No inbound API webhooks documented. Push events OUT via a Smart Flow "API Call/Webhook" automation action, or Zapier/Make/Pipedream "Watch …" triggers. To write INTO Salesmate from another tool, call the REST API.

**2026-06-28**: Plan gates worth flagging — Sequences, Sandy AI copilot, and products/quotes are **Pro ($39)+**; power dialer, custom modules, and SLAs are **Business ($63)+**; Basic ($23) is CRM-only. Smart Flow runs are credit-metered (5K/10K/15K by tier) and heavy automation can stall when credits run out. Calling/SMS numbers are a paid add-on (~$1.1/mo + usage). 24/7 support is Enterprise-only; support is otherwise live-chat-first.
