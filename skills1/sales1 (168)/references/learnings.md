# F5Bot Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-05-06**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — no API/webhook drift (base URL, Bearer auth, 4 CRUD endpoints, webhook payload fields, retry policy immediate→5min→1hr→15hr, "no hard rate limits" all unchanged). Pricing updated to show monthly rates alongside annual (Power $16.99/mo vs $14.17/mo annual; Ultra $69.99/mo vs $58.33/mo annual). Added confirmed details: Free flag length is 150 chars (1,024 on paid), AI semantic alerts are 2-included/token-metered with separate LLM billing, 50–1,000 char descriptions, up to 5 subreddits each, routable via the `semantic=` flag, and Ultra includes 2 Slack/Discord integrations. Sources: https://f5bot.com/docs-api, https://f5bot.com/tiers, https://f5bot.com/docs-semantic, https://f5bot.com/faq, https://f5bot.com/.
