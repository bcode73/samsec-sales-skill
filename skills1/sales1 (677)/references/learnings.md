# New Zenler Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-27**: Research baseline — platform docs, public REST API (`https://api.newzenler.com/api/v1/`, headers `X-API-Key` + `X-Account-Name`, ~25 endpoints across Users/Courses/Funnels/Live Classes/Live Webinars/Reports, 15/page pagination, 1000/min → 403 "Rate Limited Exceeded"), Zapier surface (7 triggers / 7 actions), pricing, and partner/affiliate program captured from live sources on this date. Re-verify specifics against current docs before relying on them. Key facts: API + memberships + affiliate + white-label are all **Pro-gated** (not on Starter); no free plan (60-day trial); 0% transaction fees; **no native webhooks** (eventing via Zapier/Make); API user `id` is a string like `313.5c109f1b58473`; no GitHub org / MCP server found. Differentiator vs Kajabi = built-in live classes/interactive webinars + multi-instructor.
