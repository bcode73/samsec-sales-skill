# FeatureOS Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface (v3 base `api.featureos.app/api/v3`, `API-KEY` header, `hn_` key prefix, page/per_page pagination, 100 req/min), OAuth 2.0 apps (`foapp_`/`fosec_`/`fooc_`/`foot_`/`foor_` tokens, scopes, app/self actor modes, role-capping), webhooks (post/changelog events, 3x retry at 5m/30m/2h then auto-disable, `postCompleted` payload), errors table, and widget (`HellonextWidget` class, `ssoToken`) captured from live sources (developers.featureos.app) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Hellonext rebranded to **FeatureOS**; `hellonext.co` 308-redirects to `featureos.com`. Legacy names persist: API keys still prefixed `hn_`, the embed class is still `window.HellonextWidget`, and feedback posts are the `feature_requests` resource. Skill named `sales-featureos`; "Hellonext" kept as a routing keyword.

**2026-06-28**: The full endpoint catalog at `/docs/api` is client-side-rendered (SvelteKit) and could not be captured by WebFetch/curl. Auth, errors, OAuth, webhooks, and widgets pages ARE static and were captured verbatim. Resource paths beyond the confirmed `feature_requests`/`buckets`/`session_info`/`votes_on_behalf` were constructed from the OAuth scopes inventory and marked as such in the api-reference — verify against the live reference.

**2026-06-28**: API access is plan-gated and the docs/pricing disagree on which tier — the live pricing page says "complete API access" from **Growth (~$120/mo)**; the Help Center says API-key usage is on the top ("Fly High") plan. Treat full API as a higher-paid-tier feature and confirm in-account. Pricing tier names have changed across versions (Runway/Takeoff/Fly vs Starter/Growth/Business) — flag all pricing as best-effort.
