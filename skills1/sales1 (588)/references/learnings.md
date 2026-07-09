# Systeme.io Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-20**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-20**: The developer portal (`developer.systeme.io`, ReadMe.com-hosted) is JS-rendered — WebFetch returns only nav/index, not full endpoint schemas. The portal exposes an AI-friendly index at `developer.systeme.io/llms.txt` (and points agents there). Base URL, auth, endpoint paths, cursor pagination, and rate-limit headers were corroborated by the help-center articles and the dltHub data-loader docs (`dlthub.com/context/source/systeme-io`); per-endpoint JSON examples are constructed and marked in the API reference.

**2026-06-20**: API is NOT plan-gated — the public REST API works across plans including the Free plan (unusual vs competitors like Kartra, which gates API to its top tier). Auth via `X-API-Key` header; up to 3 keys per account, each with an expiry date — an expired key reads as a 401.

**2026-06-20**: Pagination is cursor-based (`startingAfter` = last item id, plus `limit`), not page numbers. Rate limits surface via `X-RateLimit-Limit/Remaining/Refill` headers + `Retry-After` on 429.

**2026-06-20**: Top user pain points from reviews — small native-integration ecosystem (the API/Zapier is the workaround), restrictive/occasionally-buggy drag-and-drop page builder (less polished than Leadpages/Unbounce), basic email templates, inconsistent deliverability (authenticate domain + warm up), workflow editor less flexible than GoHighLevel/ActiveCampaign, and longer-than-expected migration timelines (free migration offered on Unlimited).

**2026-06-20**: Affiliate program is a standout — 60% lifetime recurring, no application, permanent (non-cookie) attribution, $30 min payout, monthly on the 10th. Logged in `_internal/affiliates.md`.
