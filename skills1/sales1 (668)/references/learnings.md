# WorthBuild Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each
invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-07-08**: Research baseline — platform positioning, modules, pricing, and the (absence of) API
surface captured from live sources (worthbuild.io homepage + the platform's own "best idea-validation
tools 2026" comparison blog) on this date. Re-verify specifics against current docs before relying on them.

**2026-07-08**: No public API, webhooks, Zapier/Make, or MCP found — WorthBuild is a UI web app; report,
leads, landing page, and pitch deck are used/downloaded from the browser. If a user wants automation,
route them to reconstructing the demand signal from source (Reddit API / keyword-volume API / Google
Trends), not to a WorthBuild API.

**2026-07-08**: Pricing observed as one-time-per-report with a free monthly validation (Free = 1 full
validation/mo, no card; Single Report ~$5 one-time; 5-Report Bundle ~$20 one-time) — NOT a subscription
and NOT credits. Re-runs (e.g. pivoted ideas) are separate reports. Flag all figures as best-effort.

**2026-07-08**: Differentiator vs the rest of the validator cluster is the **"Your First Customers"**
feature — it surfaces real people from Reddit/HN/X/forums with ready-to-send outreach. Distinct caveat to
always raise: surfaced leads are AI-scraped from public posts (interest, not willingness-to-pay), and the
canned outreach should be personalized + vetted, not blasted. Route real outreach to /sales-cadence +
/sales-deliverability; the go/no-go stays with real behavior (/sales-idea-validation, /sales-funnel).

**2026-07-08**: Niche indie tool (<100 reviews) — community problem-sweep capped per add-platform adaptive
depth. Comparison competitors named on the site: IdeaProof, Validator AI, ProductGapHunt, ValidateMySaaS.
