# SweepWidget Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform docs, API surface (base `https://sweepwidgetapi.com/sw_api/`, Bearer/`api_key` auth, 50-rows/page `page_start` pagination, read + write endpoints), HMAC-SHA256 signed webhooks (`X-SweepWidget-Signature`, three events), pricing tiers (Free/Pro $29/Business $59/Premium $119/Enterprise $249, best-effort), and the 25%-recurring affiliate program captured from live sources on this date. Key gate: **REST API + server-side webhooks are Enterprise-only**. Re-verify specifics (especially pricing, rate limits, and the exact error/pagination semantics) against current docs before relying on them.
