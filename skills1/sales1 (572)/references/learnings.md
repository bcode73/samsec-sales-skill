# Substack Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-05-11**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — official Developer API endpoint now documented (`GET substack.com/profile/search/linkedin/{handle}`, token auth via Settings > Developer API, returns public-profile fields identityHandle/profileUrl/leaderboardStatus/bestsellerTier/roughNumFreeSubscribers/followerCount); Stripe Billing recurring fee corrected 0.5% → 0.7% (raised July 2024, legacy 0.5% ended June 30, 2025); 10% Substack cut, no-tier/no-publisher-API/no-webhooks model, and reverse-engineered endpoints unchanged. Sources: https://substack.com/api-tos, https://support.substack.com/hc/en-us/articles/45099095296916-Substack-Developer-API, https://support.substack.com/hc/en-us/articles/360037607131-How-much-does-Substack-cost, https://github.com/NHagar/substack_api
