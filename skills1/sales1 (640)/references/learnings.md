# Validator AI Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of
each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-04**: Research baseline — platform positioning (free AI startup-idea validator, 300K+
founders), outputs (score, market size, competitor scan, customer-reaction simulation, AI mentor,
accelerator roadmap), and best-effort pricing (free core; Accelerator ~$15/mo; Pro ~$99/mo — sources
disagree) captured from live sources on this date (validatorai.com, coldiq.com, third-party review
listings). Re-verify specifics against current site before relying on them.

**2026-07-04**: No documented public API. Multiple review sites parrot a marketing line ("provides API
access"), but no developer docs exist. The site uses an internal `/api/free-tool.php` endpoint — it is
unsupported and must not be built on. Treat the platform as UI-only.

**2026-07-04**: The score is an LLM opinion, not demand evidence — it can invent market sizes and
encourage almost any idea. The reusable value is the competitor list and customer-objection simulation
(pitch-sharpening); the go/no-go must come from a real demand test (smoke test + pre-sale). Pair with
[[sales-idea-validation]] for the method.

**2026-07-04**: Pricing is inconsistent across third-party listings (e.g. coldiq quotes a "$12
Professional with API access" that contradicts the site) — always present pricing as best-effort and
tell the user to confirm live at validatorai.com.
