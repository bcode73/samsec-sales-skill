# BizPlan AI Pro Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-06**: Research baseline — platform capabilities (questionnaire plan generator, Startup Idea Validator, AI Business Coach, AI Decision Analysis, 150+ industry templates, 5-year projections, real-time team collaboration), the credit-pack pricing (pay-per-use, no subscription, credits never expire), and the no-public-API reality captured from the live site (bizplanaipro.com, tools.bizplanaipro.com) and Capterra on this date. Maker listed as "S. Enterprise." Re-verify specifics against the live site before relying on them.

**2026-07-06**: Pricing is unsettled — the homepage lists Starter ~$2.99 / Professional ~$15 / Enterprise ~$39 (one-time credit packs), but Capterra lists a ~$30 Starter. Treat all pack prices, credit counts, and seat limits as best-effort and confirm live.

**2026-07-06**: Two separate credit meters — a **plan generation** consumes a **plan credit**; the **AI Business Coach** consumes separate **Coach credits** (Professional ~50, Enterprise ~150). Credits never expire, but a founder typically re-generates a plan 3–6× on pivots, so a 1-plan Starter pack rarely covers an iterating idea. Prefer hand-editing to re-generating to conserve plan credits.

**2026-07-06**: Marketing-claim caveat — the site advertises "97% financial accuracy," "$8M+ raised," and "15,000+ plans analyzed." These are unverifiable vendor claims, not a warranty on the user's numbers. Don't repeat the accuracy figure as fact; the generated financials are AI estimates like any tool in this class.

**2026-07-06**: Namesake collision (critical) — **bizplanaipro.com** ("BizPlan AI Pro", this skill: credit packs + AI Coach + Idea Validator + Decision Analysis) vs **bizplanr.ai** ("Bizplanr", `/sales-bizplanr`: free + one-time paid workspace + iOS/Android apps) vs **bizplanner.ai** ("BizPlanner AI", `/sales-bizplanner`: paid, no free tier, 30% affiliate, AI-word top-ups). Reliable tells: credit packs + AI Coach = this; free + mobile apps = Bizplanr; no free tier + 30% affiliate = BizPlanner AI. Don't cross-contaminate pricing/features/affiliate claims.

**2026-07-06**: Do not attribute bizplan.com (Startups.co "Bizplan") Trustpilot complaints ("charged without notice") to BizPlan AI Pro — that is a different, unrelated product.

**2026-07-06**: No developer surface — no public API, no webhooks, no Zapier/Make, no MCP. The `tools.bizplanaipro.com` free tools are UI widgets, not an API. The only export is a manual download. For programmatic plan generation, call an LLM API directly. There is also a regional `bizplanaipro.in` domain.
