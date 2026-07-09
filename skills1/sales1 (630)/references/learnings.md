# Unbounce Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-04-14**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — API surface UNCHANGED (base URL https://api.unbounce.com, v0.4, Accept: application/vnd.unbounce.api.v0.4+json, API-key HTTP Basic + OAuth 2.0 JWT, 500 req/min + 429, full endpoint set, no public REST webhooks). PRICING DRIFT FIXED: new entry-level Starter plan ($29/mo, $22 annual, 5 pages, 500 visitors); Build annual $64→$74 (now 20K visitors, was "Varies"); Experiment annual $99→$112; Optimize annual $161→$187; added per-plan user/root-domain counts; Smart Copy AI copywriting starts on Build, NOT on the new Starter plan. 30% overage penalty left as-is (official overage doc returned 403, third-party-only). Sources: https://developer.unbounce.com/getting_started/, https://developer.unbounce.com/api_reference/, https://unbounce.com/pricing/
