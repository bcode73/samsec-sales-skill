# Ontraport Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-20**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-20**: The official API reference is an interactive Swagger UI at `api.ontraport.com/doc` (+ live tester `api.ontraport.com/live`) that requires credentials and is JS-rendered — WebFetch can't reproduce per-endpoint schemas. Base URL (`https://api.ontraport.com/1`), header auth (`Api-Key` + `Api-Appid`), the object model, pagination params, and the 180-req/min limit were corroborated by the official support docs, the API announcement blog, and the tray.ai connector docs. Example JSON in the API reference is constructed and marked.

**2026-06-20**: Object-oriented API — there is NO `/contacts` endpoint. Everything is an object addressed by a numeric `objectID` (Contact = 0). Discover IDs with `GET /1/objects/meta`. Operate via `/1/objects` (+ objectID); upsert with `/1/objects/saveorupdate` (match on email). Tags live in delimited fields like `contact_cat` (`*/*<tagId>/*`) — use the tag endpoints, never edit the string manually.

**2026-06-20**: Rate limit is 180 requests/minute (rolling). Pagination is offset-based: `range` (max 50) + `start`, plus `listFields`/`sort`/`condition`/`search`. Send `Api-Key`/`Api-Appid` in headers only (Ontraport explicitly warns against putting them in GET/POST data).

**2026-06-20**: Webhook events (subscribe via API): object created, form submitted, tag added, tag removed, product purchased, transaction added. Debug via Administration → Integrations → Webhook Logs (max 10,000 entries).

**2026-06-20**: Top user pain points from reviews — brutal/steep learning curve ("not intuitive", weeks to ramp) is the #1 complaint; per-contact pricing escalates with unpredictable overages (~$600/mo reported at ~43k contacts); the email editor is a clunky "fake drag-and-drop" with a smaller template library; mixed deliverability; and overcharge/support complaints. Pricing ~Basic $79 (1k contacts) / Plus $147 / Pro $297 / Enterprise $497, +$46/user.

**2026-06-20**: Affiliate/partner — Customer Referral pays 25% of monthly fees for the lifetime of the referred subscription (free to join for customers, 30-day qualification), plus Expert / VAR-Agency / Influencer partner tracks. Logged in `_internal/affiliates.md`.
