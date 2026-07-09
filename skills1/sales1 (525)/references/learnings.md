# Shopware Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of
each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform docs, Admin API + Store API surface (OAuth
client_credentials via Integration, `POST /api/search/{entity}` Criteria model, Sync API, 300 req/min
cap), App-system webhooks (`shopware-shop-signature` HMAC-SHA256, event list), editions/pricing, and
the GMV fair-usage policy captured from live sources on this date (shopware.com,
developer.shopware.com, github.com/shopware/docs). Re-verify specifics against current docs before relying on them.

**2026-07-04**: The #1 API footgun is OAuth 401 — access key/secret returned by a plugin/extension
install frequently cannot mint tokens; create a dedicated Integration under Settings → System →
Integrations and use client_credentials. Store API uses `sw-access-key` (sales-channel key), not OAuth
— mixing the two is another 401 cause.

**2026-07-04**: Reads use the search-Criteria model (`POST /api/search/{entity}` with a JSON body:
filter/sort/limit/page/associations/aggregations), not URL query filters. Pagination is page-based
(`limit`+`page`), not offset. IDs are 32-char hex UUIDs; many fields are translatable by language context.

**2026-07-04**: Admin API rate limit is 300 req/min — batch writes via `POST /api/_action/sync`
rather than per-row calls. Random Administration logouts are a long-standing refresh-token race
condition (worse with multiple tabs), not a config error.

**2026-07-04**: Fair Usage Policy (from March 2026): Community Edition (MIT) is free only under ~€1M
GMV; above that a paid plan (Rise/Evolve/Beyond) is required. Flag for scaling merchants.
