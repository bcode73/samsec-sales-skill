# BigCommerce Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface (REST v2/v3 + GraphQL Storefront/Admin/Account), webhooks, rate limits, and pricing captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Developer-portal URLs are inconsistent — `developer.bigcommerce.com/docs/...` 301-redirects to `docs.bigcommerce.com/developer/docs/...`, and several deep links return "Page Not Found" via WebFetch (JS-rendered). Use the `docs.bigcommerce.com/developer/...` form and lean on WebSearch snippets for canonical detail.

**2026-06-28**: Two pricing-naming schemes coexist — legacy API-tier names (Standard/Plus/Pro/Enterprise, which the rate-limit docs use) and the current pricing-page names (Core/Growth/Scale/Performance with GMV thresholds that auto-upgrade). Always state which set you mean.

**2026-06-28**: The single biggest integration footgun is the **thin webhook payload** (id only, no HMAC, no delivery logs). Every event becomes a follow-up REST read; budget that against the 30s rate quota and reconcile via polling because delivery isn't guaranteed and subscriptions silently deactivate on repeated 4XX/5XX or long inactivity.
