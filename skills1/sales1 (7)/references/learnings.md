# AdGlare Learnings

This file accumulates tips, gotchas, and workarounds discovered while helping users with AdGlare. When you discover something new, append it here.

## Format

Each entry should include:
- **Date**: When discovered
- **Context**: What the user was trying to do
- **Learning**: What was discovered
- **Source**: How it was confirmed (user report, docs, testing)
**2026-05-24**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — significant drift in the v2 API model. Docs moved /docs/api → /api-docs/v2. Campaign create now requires only name+folder_id+ad_format; pricing is {model: CPM|CPC, value} (CPA gone, rate→value); pacing is an object {event, period, speed(spread|asap), value} not a string; delivery is {start,end} unix timestamps not date strings. Creatives are nested under /campaigns/{id}/creatives (not top-level) with ad_type varying by format (image/code/video/zip/external, json, video/url/wrapper, url). Zones require name+folder_id+ad_format with format-specific data on PUT (vast_version 2.0–4.3, ad_sizes/auto_refresh/lazy_loading, log_impression/max_ads); API zone field enumerates 4 formats but catalog still exists in the product. The "PHP SDK" fluent-client example was fictional — real repo is github.com/adglare/ad-server-api, a small GPL-3.0 stats-pull class. API keys created in Settings => API Keys with per-endpoint/method/IP scoping. Plan gate: Management/Reporting/Decision APIs + native/video are Enterprise+Custom only (JS display API on all plans); pricing unchanged (Lite €99 1M / Pro €499 10M / Ent €649 10M); 14-day no-CC trial. Sources: https://www.adglare.com/api-docs/v2/introduction, https://www.adglare.com/api-docs/v2/campaigns, https://www.adglare.com/api-docs/v2/zones, https://www.adglare.com/api-docs/v2/creatives, https://www.adglare.com/pricing, https://www.adglare.com/user-guide/zones, https://github.com/adglare/ad-server-api.
