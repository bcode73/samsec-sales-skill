# LaunchList Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-06**: Initial research. No public REST API — roadmap lists "API Access" as planned with no ETA. Programmatic surface = form POST endpoint (`/s/FORM_KEY`, all plans) + webhooks (`new_user`, `email_verify`, Grow $79+) + Zapier triggers (Grow+). Webhook payload contains the verbatim typo `positon` inside `referred_by` (top level is `position`); `users_referred` is int at top level but string inside `referred_by`. No HMAC signing or retry policy documented for webhooks.

**2026-06-06**: Pricing conflict between sources — live /pricing page shows Free $0/100, Launch $29/500, Grow $79/10K, Scale custom/100K+ (one-time lifetime, per project). LaunchList's own blog and third-party comparisons (Waitlister guide) cite $19/$39/$149/$299 volume steps and a $19 custom-domain add-on. Schema markup on /pricing carried both $29 and $19 for Launch. Always re-verify pricing before recommending.

**2026-06-06**: No affiliate/partner program found. No GitHub org. No MCP server (nothing to wrap — no API). No Make/Pabbly modules; Zapier only, triggers only (no actions).
