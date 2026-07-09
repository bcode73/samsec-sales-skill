# BizPlanner AI Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-06**: Research baseline — platform capabilities, plan section set, pricing (one-time ~$9.99 + AI-word top-ups, no free tier, no subscription, 30-day money-back), 30% affiliate program, and the no-public-API reality captured from live sources (bizplanner.ai, bizplanner.ai/pricing, bizplanner.ai/affiliate) and third-party reviews on this date. Re-verify specifics against current docs before relying on them.

**2026-07-06**: Pricing model correction — earlier internal notes described bizplanner.ai as a *subscription* product. The live site now shows a **one-time $9.99 payment (no subscription)** plus **AI-word top-ups** (~$7.99/50k, ~$9.99/100k words) and 2 free full regenerations. The 30% affiliate program is confirmed at bizplanner.ai/affiliate.

**2026-07-06**: Namesake collision (critical) — **bizplanner.ai** ("BizPlanner AI", this skill: paid one-time + AI-word top-ups, 30% affiliate, no free tier) vs **bizplanr.ai** ("Bizplanr", `/sales-bizplanr`: a *free* generator with a one-time paid workspace and iOS/Android apps) vs **bizplanaipro.com** ("BizPlan AI Pro", separate). The reliable tells: a **free** generator or **mobile apps** = Bizplanr; **no free tier + 30% affiliate** = BizPlanner AI. Don't cross-contaminate pricing/features/affiliate claims.

**2026-07-06**: No developer surface — no public API, no webhooks, no Zapier/Make, no MCP. The only export is a manual PDF/Word download. For programmatic plan generation, call an LLM API directly.
