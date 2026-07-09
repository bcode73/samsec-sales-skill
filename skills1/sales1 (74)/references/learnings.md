# BuildOrNot Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform overview, two-product structure (data platform + free AI evaluator), datasets and counts, free-tier 100-item preview limit, and the no-public-API reality captured from third-party sources on this date (the live buildornot.io site is Cloudflare/bot-blocked — homepage and /pricing return 403). Re-verify specifics against current docs before relying on them.

**2026-07-05**: ⚠️ The backlog listed the URL as `buildornot.co`, which does NOT resolve (ENOTFOUND). The real domain is `buildornot.io`. Do not use the `.co`.

**2026-07-05**: Live site unreachable for direct fetch — research assembled from the ReadySetLaunch review (readysetlaunch.ai/compare/buildornot/review/), WebSearch snippets, and the public GitHub org (github.com/buildornot, 2 repos: a marketing README `buildornot-idea-evaluator` and `awesome-ai-startup-tools`). The GitHub org is marketing, NOT an API.

**2026-07-05**: No public API, no webhooks, no Zapier/Make, no MCP found. Tech stack per the GitHub README: React + Tailwind, OpenAI GPT backend, Vercel hosting. Paid pricing is unpublished/opaque; a reviewer/user mentions a ~$3 paid analysis (unverified).

**2026-07-05**: Credibility flags from reviews — anonymous founder (no LinkedIn / company registration), contradictory social proof (site claims 30,000 users on one page, 1,000 on another), unverifiable "90% success rate" claim, GitHub org created the same day the site launched, and a user report of paying then waiting ~3 days for an incomplete analysis. Lean on the raw data (sanity-checkable), distrust the marketing claims and the evaluator verdict.
