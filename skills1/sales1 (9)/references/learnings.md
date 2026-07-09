# Admailr Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-05-13**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — no API drift (base URL https://api.admailr.com, 3 auth methods ADMAILR-ADS-API-KEY/Bearer/query param, same 5 endpoint groups Campaigns/Campaign lifecycle/Banners/Categories/Devices, page+per_page pagination, still no webhooks/reporting/rate-limit docs all confirmed verbatim from api.admailr.com/docs). Pricing drift corrected: publisher commission is now confirmed at 70% of confirmed-ad-click revenue (was "% not disclosed"); added private-marketplace CPM fee with 500K impressions/month minimum; confirmed $100 payout on the 20th, PayPal/ACH/check (PIN only for check), global support = Native Ads only. Sources: https://api.admailr.com/docs/, https://www.admailr.com/faq/, http://help.admailr.com/faq/faq, https://www.activecampaign.com/apps/admailr
