# TranscribeMe Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->
**2026-04-22**: Research baseline (from git history) — platform docs were captured on/around this date and the API surface, pricing, and webhooks have NOT been re-verified against live docs since. Re-verify specifics before relying on them.
**2026-06-13**: API re-verified against live official docs — no drift found. Base URL (rest-api.transcribeme.com/api/v1/), X-Api-Key + Bearer auth, all 4 grant types, expires_in:35999, chunked 5MB upload flow, orders/settings/place/status/transcription/download endpoints, BrainTree billing endpoints, no completion webhooks (poll-only), and the four pricing tiers ($0.07/$0.79/$1.25/$2.00 per min) all match current docs. SDKs (.NET, Node.js, Docs repos) still present on GitHub. Sources: https://api-docs.transcribeme.com/en/latest/index.html, https://api-docs.transcribeme.com/en/latest/quickstarts/2_request_token.html, https://api-docs.transcribeme.com/en/latest/quickstarts/0_overview.html, https://api-docs.transcribeme.com/en/latest/quickstarts/1_billing.html, https://www.transcribeme.com/transcription-services/, https://github.com/TranscribeMe.
