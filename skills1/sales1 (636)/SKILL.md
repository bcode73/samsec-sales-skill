---
name: sales-upmetrics
description: "Upmetrics (upmetrics.co) platform help — an AI business-planning suite for founders, consultants, and advisors: an AI Assistant that drafts plan sections, a large sample-plan library, deep multi-year financial forecasting (P&L, cash-flow, break-even, scenarios), plan-vs-actuals tracking, QuickBooks/Xero sync, a pitch-deck generator, strategic canvases (Lean Canvas, SWOT), collaborative workspaces, and a Professional/white-label tier for consultants managing client plans. Use when generating or editing a business plan or financial forecast in Upmetrics, making a plan lender- or investor-ready, fixing a plan that reads generic for a niche, tracking a forecast against actuals or connecting QuickBooks/Xero, recovering from a surprise renewal charge or lost work, or asking whether it has an API to export or automate plans. Do NOT use for the validate-before-building method or comparing business-plan tools to pick one (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Upmetrics]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
github: "https://github.com/upmetrics"
---

# Upmetrics Platform Help

Upmetrics (**upmetrics.co**) is an established **AI business-planning suite** for founders, consultants,
and advisors. You describe a business and its **AI Assistant** (Writing / Financial / Research Assist)
drafts and rewrites plan sections; it ships a large **sample-plan library**, deep **multi-year financial
forecasting** (automatic P&L, cash-flow, break-even, scenario testing over 3- and 7-year horizons),
**plan-vs-actuals tracking**, a **pitch-deck generator**, strategic-planning canvases (Lean Canvas,
Business Model Canvas, SWOT, OKR/KPI), **real-time collaborative workspaces**, and **QuickBooks/Xero**
connectors. Its angle vs the AI-first generators (VentureKit, Plannit) is a **mature, team-oriented
planning suite** with accounting sync, forecast-vs-actuals tracking, and a **Professional/white-label
tier** for consultants managing many client plans. The catches: the AI drafts read **generic** until you
feed rich input, the **financials are AI estimates**, and it's **UI-only with no public API**.

> **Namesake collision — always check the domain.** **upmetrics.co** is this business-planning tool.
> **upmetrics.com** is an *unrelated* impact/ESG-reporting platform for nonprofits and foundations — a
> different company. Don't merge their reviews, pricing, or "API" docs.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Upmetrics?**
   - A) Generate/edit a plan, financial forecast, or pitch deck and interpret the output
   - B) Make the plan **lender-ready / investor-ready** for a loan or raise
   - C) Track a **forecast against actuals** or connect **QuickBooks/Xero**
   - D) Understand the tiers (Starter vs Premium vs Professional / white-label) or a billing problem
   - E) Export or automate plans (the API reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a generated plan is a document, not demand).

Skip-ahead: if the user wants the validate-before-building *method* or to compare business-plan tools
across the market to pick one, route to `/sales-idea-validation` immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A **cross-market ranking** of business-plan/validator tools (VentureKit, Plannit, LivePlan… to pick one) — but answer a quick Upmetrics-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Upmetrics-specific questions using Step 3.

## Step 3 — Upmetrics platform reference

**Read `references/platform-guide.md`** for the full reference — the module set (AI Assistant, business-plan
builder, financial forecasting, plan-vs-actuals, pitch deck, strategic canvases, collaboration), what's
editable vs generated, the Starter/Premium/Professional tiers and white-label, the QuickBooks/Xero
integration reality (one-way import, not live sync), the no-public-API reality and the manual PDF/DOC
export, and how to feed rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the generated plan and financials as AI estimates, not facts — swap in real numbers before a
  lender or investor sees them.** Upmetrics drafts a polished, structured plan fast, but the forecasts are
  the model's guesses. Tell the user to keep the structure and framing, then **replace the projections,
  market size, and unit economics with their own real numbers** and cite sources — a bank or investor will
  scrutinize the financials, and AI-padded projections are the fastest way to lose credibility.
- **De-genericize niche plans by feeding rich input — this is the #1 complaint.** Reviewers report the AI
  draft reads generic and needs ~60% rewriting. Coach the user to feed a **detailed** description (exact
  customer, the specific problem, how it's solved today, business model, pricing) and to **rewrite the
  competitive, operations, and revenue sections by hand** — the model has thin depth for specialized
  verticals. Richer input in → specific plan out.
- **Separate "make it lender/investor-ready" from "is this idea validated."** A fundable-looking plan is a
  *document*, not demand — Upmetrics will happily generate a confident plan for an idea nobody wants. If the
  real question is build-or-not, put the go/no-go on a **real demand test** (smoke test / pre-sale) and
  route it to `/sales-idea-validation`; use Upmetrics for the plan/forecast once demand is real.
- **Tell users to save often and export frequently — data loss is a reported risk.** Some users report
  whole sections of inputs disappearing without warning. Advise **exporting a PDF/DOC snapshot before big
  edits** and not treating the app as the sole copy near a grant or investor deadline.
- **Set QuickBooks/Xero expectations: it's a one-way import, not live two-way sync.** Despite "sync"
  marketing, reviewers find the accounting connectors pull data one-directionally and not in real time —
  tell the user to plan manual refreshes and not rely on it as a live actuals feed.
- **Whenever you name a tier or price, add that it's best-effort and subject to change and point to
  upmetrics.co/pricing to confirm** — the numbers move and sources disagree. Frame tiers around what breaks:
  **Starter** (single workspace, sample plans, AI writing, forecasting, QuickBooks/Xero); **Premium** (more
  capacity/features); **Professional** (client management, custom templates, workspace transfer, and an
  **optional white-label** for consultants/advisors). If the user just needs one plan, the entry tier is
  usually enough — the higher tiers solve consultant/client volume, not core planning.
- **There's no usable public API — don't plan an integration around it.** State plainly that Upmetrics is
  **UI-only: no public API, no webhooks, no Zapier/Make, no MCP**. Any "API" is a **custom, sales-gated
  white-label arrangement** for advisors/accelerators, undocumented. To automate plan generation, call an
  **LLM API directly**; the only reliable export is the **plan PDF/DOC** done manually.
- **Warn about auto-renewal — cancel early and keep the confirmation.** Reviewers report being charged again
  at full price after cancelling, with no cancellation email. Tell the user to cancel **well before** the
  renewal date, screenshot the confirmation, and check the annual-renewal terms.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — Upmetrics's tiers, plan limits, and integrations move; verify at upmetrics.co/pricing.*

- **Namesake collision.** upmetrics.**co** = this business-planning tool; upmetrics.**com** = an unrelated
  nonprofit impact-reporting platform. Don't conflate their features, pricing, or API claims.
- **AI drafts read generic.** The plan needs a rich input and heavy hand-editing (reviewers cite ~60%
  rewrite), especially the competitive, operations, and revenue sections for niche verticals.
- **Financials are AI estimates.** P&L/cash-flow/forecast numbers are the model's guesses — replace them
  with real unit economics before a lender or investor reviews them.
- **A generated plan is not validated demand.** It will produce a confident plan for an unwanted idea —
  settle the go/no-go with a real behavior test (smoke test / pre-sale), not the plan.
- **Data-loss risk — save/export often.** Users report sections of input vanishing without warning; keep a
  PDF/DOC snapshot before big edits and don't rely on the app as the only copy near a deadline.
- **QuickBooks/Xero is a one-way import, not live sync.** The accounting connectors pull data
  one-directionally and not in real time despite "sync" marketing — plan manual refreshes.
- **Auto-renewal surprise charges.** Reviewers report being re-billed at full price after cancelling with no
  confirmation email — cancel early and keep proof.
- **No public API / no automation.** UI-only: no API, webhooks, Zapier/Make, or MCP. "API" access is a
  custom white-label arrangement (advisors/accelerators), undocumented. Export is manual PDF/DOC.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full business-plan/validator landscape (use this to actually decide build-or-not; a generated plan is a document, not demand)
- `/sales-venturekit` — VentureKit platform help (the AI-first business-plan generator sibling — full plan + lender-ready forecasts, pitch deck, and LLC formation; generous free tier, but **no team collaboration** and no accounting sync — Upmetrics does both)
- `/sales-plannit` — Plannit AI platform help (AI business-plan generator, now AIGenerator.com — questionnaire → 15–20 page plan with real-time collaboration; forecasting is its weakest module, where Upmetrics is deeper)
- `/sales-venturusai` — VenturusAI platform help (framework-driven validator — SWOT/PESTEL/Porter/VRIO + sizing/financials/pitch deck; the analysis-report cousin, not a full planning suite)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Upmetrics wrote me a plan with financials — can I take it to my bank for a loan?"
**User says**: "Upmetrics generated a business plan with revenue projections and a P&L. Can I hand this to my bank for a loan?"
**Skill does**: Credits the structure and speed but warns the **financials are AI estimates** — a lender will
scrutinize numbers that read padded. Tells the user to keep the outline and market framing but **replace
every forecast, market-size, and unit-economics figure with their own real numbers** before submitting, and
to cite sources. Adds that a fundable-looking plan is a document, not validated demand — if the go/no-go is
still open, route it to `/sales-idea-validation`.
**Result**: The founder submits a plan grounded in real numbers instead of AI-padded projections.

### Example 2: "Can I pull my Upmetrics plans out via the API into my own app?" (developer/automation)
**User says**: "I want to script Upmetrics to generate plans and pull each one into my database via the API or a webhook."
**Skill does**: States plainly that Upmetrics is **UI-only — no public API, no webhooks, no Zapier/Make, no
MCP** — so there's no supported way to batch-generate or export programmatically; any "API" is a
**custom, sales-gated white-label arrangement** for advisors/accelerators, undocumented. Notes the only
reliable export is the **plan PDF/DOC done manually**, and that if programmatic generation is essential the
user should **call an LLM API directly** or pick a tool built for automation. Points out the thing worth
automating is a real demand signal (landing-page analytics), not a generated plan — routing that to
`/sales-funnel`.
**Result**: The user avoids planning an integration around a nonexistent API and picks a workable path.

### Example 3: "My Upmetrics plan reads generic and I lost a section — what's going on?" (quality + data loss)
**User says**: "The plan Upmetrics made could describe any business, and a whole section of my inputs disappeared. How do I fix this?"
**Skill does**: Explains the generic output traces to a **thin input** — coach the user to feed a detailed
description and **rewrite the competitive/operations/revenue sections by hand** for their niche. On the data
loss, tells them to **export a PDF/DOC snapshot before big edits** and not treat the app as the sole copy,
since sections vanishing without warning is a reported issue. Notes the connectors and forecasts are
best-effort and to verify current behavior in-app.
**Result**: The user gets a specific plan and protects their work against loss.

## Troubleshooting

### "My Upmetrics plan reads generic — it could describe any business"
**Symptom**: The plan is vague and not specific to the idea; the user is rewriting most of it.
**Cause**: A thin input — Upmetrics's AI generates over whatever you give it, and it has thin depth for
specialized verticals, so a short description yields a cookie-cutter plan.
**Solution**: Feed a **detailed** description — exact customer, the specific problem, how people solve it
today, the business model and pricing — then **rewrite the competitive overview, operations, and revenue
sections by hand**. Replace the AI's placeholder numbers. Still settle the go/no-go with a real demand test
via `/sales-idea-validation`.

### "I cancelled but Upmetrics charged me again at full price"
**Symptom**: A renewal charge appeared after the user thought they cancelled, with no confirmation email.
**Cause**: Reviewers report auto-renewal at full price with weak cancellation confirmation — the plan renews
on the annual/period date unless cancelled well ahead.
**Solution**: Cancel **well before** the renewal date, **screenshot/keep the confirmation**, and review the
renewal terms in account settings. If wrongly charged, use the **15-day money-back guarantee** and contact
support (consistently praised in reviews) with your cancellation proof.

### "QuickBooks/Xero isn't syncing my actuals in real time"
**Symptom**: Accounting data isn't flowing live into the forecast; actuals look stale.
**Cause**: The connectors are a **one-way import, not two-way live sync**, despite "sync" marketing.
**Solution**: Treat it as a periodic **manual import** — refresh on a cadence rather than expecting a live
actuals feed, and reconcile plan-vs-actuals against your accounting source of truth. Don't build a workflow
that assumes real-time bidirectional sync.
