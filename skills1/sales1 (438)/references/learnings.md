# PrometAI Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-08**: Research baseline — platform capabilities (questionnaire plan generator; a **connected financial model** with financial projections + **DCF valuation** + **stress testing** + **scenario analysis** that recalculate together; SWOT/VRIO strategy frameworks; a 50+ tool "Entrepreneur Journey" covering idea generation, branding, founder profiles, risk assessment, valuation; NDA/term-sheet templates; translations), the **subscription** pricing model (Explore free → Application-Ready/Basic → Investor-Grade/Pro → Enterprise), and the **no-public-API** reality captured from the live site (prometai.app, prometai.app/pricing) + third-party reviews (Product Hunt, Trustpilot, Upmetrics/Venngage comparisons) on this date. Re-verify specifics against the live site before relying on them.

**2026-07-08**: Differentiator vs the AI-plan cluster — the **connected financial model**. Reviewers single it out as the tool whose financials stay "grounded, consistent, and connected end-to-end" (DCF valuation + stress testing + scenario analysis update automatically when inputs change). This is its strongest selling point; treat it as the reason a user picks PrometAI over cheaper siblings.

**2026-07-08**: Pricing is best-effort and moves — Explore Free ($0, 1 plan, 25 AI requests/mo, view-only, NO export); Application-Ready/Basic (~$55/mo, ~$25 annual, 3 plans, PDF export, financial dashboards); Investor-Grade/Pro (~$145/mo, ~$65 annual, 8 plans, PowerPoint export, DCF valuation + stress testing, NDA/term-sheet templates, 10 translations); Enterprise (custom, FP&A analytics + ERP integrations). Billing is monthly/quarterly/annual with steep annual discounts. Confirm live.

**2026-07-08**: The two tier gates that usually decide it — (1) **can you export at all** (no on free Explore, PDF on Basic, PowerPoint on Pro), and (2) **do you need the DCF valuation / stress testing** (Pro only). AI requests are also metered per month (25/200/500) — heavy iteration can exhaust the lower caps.

**2026-07-08**: Reviewer-noted limits — (a) it **invents unverified market figures and cites vague reports** (verify every stat); (b) **financial integrity is only "moderate" for lenders** — most lenders still want a separate financial review; (c) the **DCF valuation isn't beginner-friendly** (needs real inputs; it's a model, not an appraisal); (d) **exports sometimes lose formatting**; (e) **collaboration is very limited — no real-time co-editing**.

**2026-07-08**: No developer surface — no public API, no webhooks, no Zapier/Make, no MCP. The advertised **"ERP integrations" and "FP&A analytics" are Enterprise-only, sales-gated** custom deployments, NOT a self-serve developer API. The only export is a manual PDF/PowerPoint download (paid tiers). For programmatic plan generation, call an LLM API directly.

**2026-07-08**: Economic contrast — PrometAI is a **subscription** (recurring, and Pro is on the pricey end at ~$145/mo), unlike its one-time/credit siblings: Bizplanr (free + one-time workspace), BizPlanner AI (one-time + AI-word top-ups), BizPlan AI Pro (credit packs). If a user only needs one plan, weigh the recurring cost against a one-time alternative.

**2026-07-08**: Affiliate/partner program exists (referral commissions) — noted for _internal/affiliates.md. Also written "Promet AI" (two words) in some comparison articles; canonical domain is prometai.app.
