# GetWaitlist Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-15**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Key facts to re-verify: free tier was removed for new accounts mid-2025 (existing grandfathered); pricing $15 Basic / $50 Advanced / $250 Pro with 7-day trial; API available from Basic; custom domain + viral referrals gated to Advanced; custom email-sending domain gated to Pro; base URL `https://api.getwaitlist.com/api/v1/`; signup create/get are unauthenticated; authenticated reads use an `api-key` header (or JWT via `create_tokens`); webhooks are `new_signup` + `offboarded_signup` with 30s connect / 90s response timeouts and no documented HMAC signing or retry policy; no MCP server. Re-verify specifics against current docs before relying on them.
