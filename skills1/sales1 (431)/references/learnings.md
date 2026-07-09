# Preuve AI Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-05**: Research baseline — platform positioning, 10-agent/50+-source architecture, tiers (free Reality Check, one-time Founder Report, Investor-Ready Package, Radar/Radar Pro/Builder subscriptions, Lifetime Pro/Business), and the no-public-API reality captured from live sources on this date. Re-verify specifics against current docs before relying on them.
**2026-07-05**: Report-pack prices differed between the homepage (5-pack $95 / 10-pack $159) and search snippets (5-pack $89 / 10-pack $149) — treat report-pack figures as best-effort and confirm at preuve.ai/pricing. The one-time Founder Report (~$29) and the free Reality Check were consistent across sources.
**2026-07-05**: No public API, webhooks, MCP server, or Zapier/Make found (confirmed via homepage, idea-validation page, and API-doc search — nothing surfaced). Only programmatic-ish surface is the shareable dashboard link `preuve.ai/share/{slug}`. If Preuve later ships an API, update the SKILL's Step 4 + Gotchas + platform-guide.
**2026-07-05**: Built on Claude Opus 4.8 (single-model, vs IdeaProof's multi-model ensemble) with a dedicated cross-validator agent for fact-checking. Viability score is deliberately conservative (median ~55) — do NOT compare it on the same scale as IdeaProof's ~78 median.
