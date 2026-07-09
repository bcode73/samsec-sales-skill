# AdvertServe Learnings

Accumulated knowledge from real usage and research. Append new discoveries with today's date.

## 2026-05-24 — Initial research

- AdvertServe Code Wizard supports "E-mail" code type specifically for Banner zones — generates static IMG tags
- Image format restriction: code-based images are rejected, must be JPEG/GIF/PNG files
- G2/Capterra reviews praise support responsiveness but note documentation is technical
- 45-day free trial is generous compared to competitors (AdButler has shorter trial)
- Referral program: 5% monthly credit (not cash) for referred customers
- GitHub org exists at github.com/AdvertServe but no public SDKs found
- AMP integration documented in amphtml project on GitHub

## 2026-06-13 — API re-verified

**2026-06-13**: API re-verified against live official docs — no contradicting drift found; all core claims (v5.0, secret-param auth 32 chars, `/servlet/control/api/{module}/{action}` base, JSON via output=json, 17 modules incl. Pixels/Segments/Stacks/Videos/Prefetch, zone types 1-8, targeting codes 1-11, zones/campaigns/advertisers create params, Reports structure + export formats, no webhooks, no SDK, no documented rate limit, $299/mo base / 2M impressions, 45-day trial, 99.995% SLA, Prebid.js header bidding, weather targeting, Forensiq IVT) confirmed UNCHANGED. Added missing detail: JSON error format `{ "error": "..." }` (docs document both XML and JSON error bodies); overage pricing of **$0.05 CPM** for impressions beyond plan (live pricing calculator now shows base + overage CPM rather than fixed volume tiers); named targeting codes 1-11 (CUSTOM/DATETIME/GEOGRAPHY/KEYWORDS/NETWORK/REFERRERS/SOFTWARE/THEMES/RETARGETING/LANGUAGES/WEATHER); zone bidding flags `bidding_consent_api` (empty|iab), `bidding_coppa`/`bidding_privacy`/`bidding_ssl`. Sources: https://www.advertserve.com/docs/latest/html/manual/api.html, https://www.advertserve.com/docs/latest/html/manual/api_zones_create.html, https://www.advertserve.com/docs/latest/html/manual/api_campaigns_create.html, https://www.advertserve.com/docs/latest/html/manual/api_advertisers_create.html, https://www.advertserve.com/docs/latest/html/manual/api_reports.html, https://www.advertserve.com/docs/latest/html/manual/api_code_banner.html, https://www.advertserve.com/pricing.html, https://www.advertserve.com/features.html, https://www.advertserve.com/developers.html
