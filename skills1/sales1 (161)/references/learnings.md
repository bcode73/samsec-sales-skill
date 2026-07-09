# EngageBay Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface (engagebay/restapi + engagebay/webhooks GitHub repos), pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-28**: API responses default to **XML**; you must send `Accept: application/json` to get JSON. Auth is the raw REST API Key in the `Authorization` header (no `Bearer` prefix), found at Account → Admin Settings → API → REST API Key. Base URL `https://app.engagebay.com/`.

**2026-06-28**: Webhooks are **outbound only** — EngageBay does NOT accept incoming webhooks. All writes into EngageBay go through the REST API. Outbound webhook payloads carry no documented HMAC signature.

**2026-06-28**: Listing contacts uses `POST dev/api/panel/subscribers` (not GET). Cursor pagination — the `cursor` is returned inside the LAST record of the page; absence of a cursor means end of list. `page_size` max is 100.

**2026-06-28**: Deals attach to a `track_id` (pipeline) + `milestoneLabelName` (stage); both are case-sensitive and must match the account exactly. A wrong milestone name still creates the deal but hides it from the milestone view — a silent failure.

**2026-06-28**: Monthly API-call quota is plan-gated (~750,000/month on Pro; much lower on free/Basic). `429` = quota/rate exceeded; back off and retry. Prefer webhooks for incremental sync over repeated full exports.
