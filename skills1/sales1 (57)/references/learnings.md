# Bizplanr Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-06**: Research baseline — platform capabilities, pricing, and the no-API reality captured from third-party sources on this date. The live site (bizplanr.ai) returned **HTTP 403 to automated fetches** (homepage, /pricing, /blog all blocked); research was assembled from GetApp, Upmetrics' review page (upmetrics.co/tools/bizplanr), TripleAReview, and comparison listicles (PrometAI). Re-verify pricing and free-export formats against the live site before relying on them.

**2026-07-06**: **Namesake collision is the biggest trap.** Three similarly named tools: **bizplanr.ai** (this — free generator + one-time ~$99 workspace), **bizplanner.ai** ("BizPlanner AI" — subscription + 30% affiliate program), and **bizplanaipro.com** ("BizPlan AI Pro"). A WebSearch for "Bizplanr affiliate program" returned bizplanner.ai's 30% program, not bizplanr.ai's — do not attribute it to this tool. Confirm the exact domain before quoting pricing/features/affiliate.

**2026-07-06**: **Pricing model is one-time, not subscription** — a genuine differentiator vs Plannit/Upmetrics/VentureKit. Free core generator + PDF (no credit card); ~$99 one-time workspace unlocks the guided editor, advanced forecasting, and Word/Excel export. Sources disagree on whether the free tier is PDF-only or supports multi-format export — most reviews say PDF-only free.

**2026-07-06**: **Standalone generators (SWOT / competitor / financial model / one-page) run independently** — their outputs don't cross-reference the main plan, so numbers must be reconciled by hand. Upmetrics' review flags this as "the free version's outputs don't talk to each other."

**2026-07-06**: **No public API / webhooks / Zapier / MCP** — UI + mobile app only. Export is a manual download. For programmatic plan generation, call an LLM API directly.
