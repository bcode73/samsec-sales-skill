# Kartra Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-20**: Research baseline — platform docs, API surface, pricing, and webhooks captured from live sources on this date. Re-verify specifics against current docs before relying on them.

**2026-06-20**: Kartra's live API article pages on `support.kartra.com` (and the `documentation.kartra.com` URLs that 301-redirect to them) are JS-rendered/bot-blocked — direct WebFetch returns 404 even though the pages exist in-browser. The action surface, endpoint, auth, and rate limit were captured from the official docs' descriptive text and the apitracker/help-center index; per-command request/response JSON was NOT fetchable and is constructed in the API reference. Future re-verification likely needs a browser/Firecrawl, not WebFetch.

**2026-06-20**: API access appears gated to the **Professional** tier on current Kartra plans (older plans historically had API on all paid tiers). This is the #1 integration gotcha — a key on Essentials/Starter/Growth may not authenticate. Verify against the live account/pricing before debugging code.

**2026-06-20**: The API is single-endpoint + `actions[]` array (form-POST to `https://app.kartra.com/api`), NOT resource-REST. A third-party "Rollout" Python guide that shows REST-style `/lead/list` endpoints with header auth and cursor pagination is AI-reconstructed and contradicts the official format — do not trust it.

**2026-06-20**: Platform-wide ~0.03% spam-complaint standard — Kartra throttles/suspends sending accounts that exceed it. This is account-protection (distinct from inbox-placement deliverability). Recurring user pain points from reviews: steep learning curve / clunky UI, custom-domain redirect slowing page load, and calendar dropping appointments.
