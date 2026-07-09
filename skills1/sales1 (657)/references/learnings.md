# Waitlistly Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-19**: Research baseline — platform positioning, sitemap, custom-domain + webhook help guides, and the absence of a public API/pricing/docs page captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-19**: ⚠️ Live site unreachable for detail — `waitlistly.live` homepage and `/growth` are JS-rendered SPAs that return only the page title; there is no public `/pricing`, `/api`, or `/docs` page, and no third-party reviews exist. Research was assembled from the sitemap, the two Help guides (Custom Domains; Webhooks/Integrations), the OG/meta description, and comparison roundups. Future runs: expect the live fetch to be unreliable; the Help pages (`/help`) are the most extractable source.

**2026-06-19**: Verified surface = on-signup webhooks ("real-time lead data to Zapier, Make, Slack, or your own API") + custom domains. No public REST API. Webhook payload schema is undocumented — inspect a real delivery before mapping fields.
