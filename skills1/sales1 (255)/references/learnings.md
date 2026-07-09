# Instapage Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-28**: Research baseline — platform docs, API surface (api.instapage.com/v1, Bearer personal token), pricing (Create $99 / Optimize $199 / Convert custom), plan gates (A/B testing + AI Experiments + Personalization/DTR = Optimize+; heatmaps + ad-to-page personalization + root-domain publishing + Global Elements + SSO + Direct Lead Bypass = Convert only), rate limits (200 req/min per token+IP + per-plan daily quota resetting 00:00 UTC, both → 429 + Retry-After), and the per-form Form Submit webhook (POST, internal field_N IDs not labels, 20s endpoint timeout, no documented HMAC) captured from live sources on this date. Owned by airSlate. GitHub org github.com/Instapage exists (13 public repos). Homepage help center (help.instapage.com) returns 403 to WebFetch; webhook details cross-checked via third-party integration docs. Re-verify pricing/quotas against current docs before relying on them.
