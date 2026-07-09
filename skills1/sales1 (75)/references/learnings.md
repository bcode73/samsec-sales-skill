# sales-buska Learnings

Accumulated tips, gotchas, and corrections discovered during use.

<!-- Add entries: **YYYY-MM-DD**: description -->

**2026-05-10**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.

**2026-06-13**: API re-verified against live official docs — core tiers unchanged (Starter $49 / Growth $99 / Scale $249 / Agency custom; ICP 2/5/10; sources 16+/28+/33+; API 500/2,500 req/mo; webhooks + Reply Studio + CSV Growth+; analytics + full API Scale; 7-day trial). DRIFT: (1) pricing page now gates by "signals monitored" (5/15/30), replacing the old "keywords" (3/10/30) framing — Starter and Growth quotas relabeled and bumped; (2) per-week lead caps (50/150) no longer published on the pricing page; (3) NEW standalone à-la-carte "API Credit Plans" — Developer $50/1,000, Production $500/50,000, Business $3,000/500,000 calls, 1 credit = 1 successful call, credits never expire — so API/MCP access no longer strictly requires a Growth subscription (webhooks still Growth+); (4) team-member seats now published per tier (1/5/unlimited). MCP confirmed marketed under homepage "API, WEBHOOKS & MCP" as "plug Buska into Claude, GPT, or any AI agent," "Full REST API access (Scale plan)." Could not locate an official docs.buska.io developer reference (base URL/auth/endpoints) — left undocumented rather than invented. Third-party salesforge.ai directory listed a conflicting $9/$69 "Pro/Ultimate Yearly" structure; disregarded in favor of the first-party pricing page. Sources: https://www.buska.io/pricing, https://www.buska.io/.
