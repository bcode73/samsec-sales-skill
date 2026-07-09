# Adserver.Online Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-05-25**: Initial research — API v2.4.0 at api.adsrv.net/v2, Bearer token auth, 100 req/min rate limit. Email ads require Premium plan ($199/mo). Free plan was discontinued. Reporting latency has been noted by G2 reviewers. Homepage and pricing page are JS-rendered (Framer).

**2026-06-13**: API re-verified against live official docs — API version is now 2.4.1 (added GET|POST /group for campaign group management, requires "Campaign grouping" enabled in Settings/Common); base URL, Bearer auth, 100 req/min rate limit, and X-Rate-Limit-*/X-Pagination-* headers all unchanged; no webhooks/signing (confirmed). Pricing unchanged on official /plans page (Starter $49/1M, Premium $199/10M, Ultimate $599/50M — third-party aggregators listing $20/$50 are stale). Corrected plan-gate drift: programmatic OpenRTB, Prebid adapters, Google RTB, XML/JSON feeds, and multicurrency bidding are Ultimate-only, NOT Premium+ (skill previously listed OpenRTB as Premium). REST API stays Premium+; Decisioning/programmatic API is Ultimate. OpenRTB protocol is v2.5 (Banner/Native/VAST/Direct Link/Push). Sources: https://adserver.online/site/openapi, https://adserver.online/plans, https://adserver.online/article/buy-traffic-using-openrtb, https://adserver.online/article/multicurrency-bidding.
