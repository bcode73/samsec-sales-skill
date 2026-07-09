# Tuemilio Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-19**: Research baseline — REST API (verbatim), JavaScript SDK, webhook events, pricing tiers, and integrations captured from live docs (docs.tuemilio.com) on this date. Re-verify specifics against current docs before relying on them.

**2026-06-19**: Three programmatic surfaces — REST API (`tuemilio.com/api/v1`, `?api_token=` query auth, server-side only per docs warning), JavaScript SDK (`Tuemilio('init'|'createSubscriber'|'getDashboard'|…)` + event listeners, browser-side), and webhooks (`new-subscriber`/`grant-access`/`confirmed-subscriber`, `X-Tuemilio-Event` header, `User-Agent: Tuemilio-Hookshot/1.0`, no documented signing/retries).

**2026-06-19**: Pricing best-effort — Founder $29/mo, Startup $49/mo (+teams), Enterprise custom; API/webhooks/custom domains/email/unbranded forms on ALL tiers; 30-day free trial no CC. Tuemilio previously had a free tier — verify the live pricing page.

**2026-06-19**: Gaps not in docs — REST pagination, rate limits, error shapes; webhook signing/retry/timeout; field-level JSON for JS SDK returned objects. `add-points` is additive; `PUT /emails` sets points absolutely. Widget List UUID (list `uuid`) is used by the JS SDK; numeric `id` is used by REST paths.
