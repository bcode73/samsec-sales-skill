# Surfe Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface (v2 enrich/search, v1 credits), webhooks (`x-surfe-signature` HMAC-SHA256), pricing, and credit model captured from live sources (developers.surfe.com + Surfe Help Center) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: Credits are billed **per year**, not per month — the single biggest cost surprise. Three separate pools (email / mobile / search). API spends a credit only on a successful find.

**2026-06-28**: The Chrome extension enriches in-session only (must be on a LinkedIn profile/list); true background bulk enrichment lives in the REST API (`POST /v2/people/enrich`, up to 10,000 people/job; companies ≤500/job). Don't tell users "Surfe can't bulk-enrich" — the extension can't, the API can.

**2026-06-28**: The public REST API does NOT write to the CRM. It returns enriched data; CRM writes happen via the native extension/connector (HubSpot/Salesforce/Pipedrive/Copper). Niche CRMs are unsupported.

**2026-06-28**: Surfe was previously named **Leadjet** — older comparison articles use that name.
