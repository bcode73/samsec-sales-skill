---
name: sales-bizplanr
description: "Bizplanr (bizplanr.ai) platform help — a free AI business-plan generator that turns a short questionnaire into a full structured plan (executive summary, market analysis, marketing strategy, operations, basic financials) in about five minutes, plus standalone SWOT/competitor/financial-model/one-page generators, an AI business advisor, and iOS/Android apps. Use when generating or editing a plan in Bizplanr, interpreting its AI-written financial projections, fixing a plan that reads generic or lacks depth for a niche, deciding whether the free tier is enough or the one-time paid workspace is worth it, getting Word/Excel export instead of PDF-only, telling bizplanr.ai apart from the similarly named BizPlanner.ai, or asking whether it has an API to export or automate plans. Do NOT use for the tool-agnostic validate-before-building method or comparing business-plan tools across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Bizplanr]"
license: MIT
version: 1.0.2
tags: [sales, validation, pre-launch, platform]
---

# Bizplanr Platform Help

Bizplanr (**bizplanr.ai**) is a **free AI business-plan generator** for first-time founders, solopreneurs,
freelancers, and small-business owners. You answer a **short questionnaire** (business idea, market,
competitors, USP, funding needs) and it generates a **full structured plan in about five minutes** —
executive summary, market analysis, marketing strategy, operations, and **basic financials**. Around it sit
**standalone generators** (SWOT, competitor analysis, financial model, one-page plan), an **AI business
advisor** you can chat with to refine sections, a **sample-plans** library, and **iOS/Android apps**. The
core generator and PDF download are **free (no credit card)**; a **one-time paid workspace** unlocks the
guided section-by-section editor, advanced forecasting, and Word/Excel export. It's **UI-only — no public
API**. (Naming: **bizplanr.ai** is this tool; **bizplanner.ai** — "BizPlanner AI" — is a *different* paid
product [one-time payment + AI-word top-ups, no free tier, a 30% affiliate], and **bizplanaipro.com** — "BizPlan AI Pro"
(`/sales-bizplanaipro`), a credit-based generator — is another; don't conflate them.)

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Bizplanr?**
   - A) Generate/edit a plan, financials, SWOT, competitor analysis, or one-page plan and interpret the output
   - B) Make the plan **investor-ready / lender-ready** for funding
   - C) Understand access — the **free tier** vs the **one-time paid workspace**, and export formats
   - D) Export or automate plan generation (the API reality), or you hit the **bizplanr.ai vs bizplanner.ai** mix-up
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a generated plan is a document, not demand) —
   route in Step 2.

Skip-ahead: if the user already gave enough context, or wants to compare business-plan tools across the
market to pick one, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A **cross-market ranking** of business-plan/validator tools (Upmetrics, VentureKit, LivePlan… to pick one) — but answer a quick Bizplanr-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Bizplanr-specific questions using Step 3.

## Step 3 — Bizplanr platform reference

**Read `references/platform-guide.md`** for the full reference — the module set (plan generator, standalone
SWOT/competitor/financial/one-page tools, AI advisor, mobile apps), what's free vs the one-time paid
workspace, export formats by tier, the no-public-API reality and manual export, the bizplanr.ai vs
bizplanner.ai disambiguation, and how to feed rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

- **Treat the plan and financial projections as AI estimates, not facts — and swap in real numbers before an
  investor or lender sees them.** Bizplanr drafts a clean plan fast, but its **financials are AI-generated
  estimates** and the free tier is deliberately **basic** (no deep/scenario forecasting). Tell the user to
  keep the structure and market framing, then **replace the projections, market size, and unit economics with
  their own real numbers and cite sources** — a funder scrutinizes the financials first. And a fundable-looking
  plan is **not demand**: settle the go/no-go with a **real behavior test — a smoke test or a pre-sale** — not
  the plan, and route that to `/sales-idea-validation`.
- **De-genericize niche plans by feeding richer input and editing hard.** A thin one-line idea yields a
  cookie-cutter plan that "could describe any business." The fix is input richness: feed a **detailed**
  description (exact customer, the specific problem, how it's solved today, business model, pricing) and
  **edit heavily** — especially the competitive, operations, and revenue sections, where the model lacks
  depth for specialized verticals.
- **Reconcile the standalone tools by hand — their outputs don't cross-reference.** The SWOT, competitor,
  financial-model, and one-page generators run independently, so numbers and claims won't automatically agree
  across them. Warn the user to **manually align** figures (e.g. the financial model vs the plan's financials)
  before presenting.
- **Present all pricing as best-effort and point to bizplanr.ai/pricing.** Best-effort at research: the core
  generator + PDF download is **free (no credit card)**; a **one-time ~$99 workspace** (not a subscription)
  adds the guided editor, advanced forecasting, and **Word/Excel** export. Free-tier export is commonly
  **PDF-only** — if the user needs Word/Excel or the section-by-section editor, that's the paid unlock. Tell
  them to **confirm current pricing and free-export limits on the live site**; for one basic plan, free is
  usually enough.
- **There's no usable public API — don't plan an integration around it.** State plainly that Bizplanr is
  **UI-only: no public API, no webhooks, no Zapier/Make, no MCP**. The only export is the plan itself,
  downloaded manually (PDF free; Word/Excel on the paid workspace). For programmatic plan generation, **call
  an LLM API directly** instead.
- **Clear up the bizplanr.ai vs bizplanner.ai mix-up.** If the user cites a paid-to-generate tool with **no
  free tier**, a **30% affiliate program**, or features you don't recognize, they're likely on
  **bizplanner.ai ("BizPlanner AI")** or **bizplanaipro.com** — separate products with confusingly similar
  names. Confirm which domain they're on so
  reviews, pricing, and tips don't cross-contaminate — and because all pricing here is **best-effort**, tell
  them to **confirm the current tiers and export formats on bizplanr.ai** rather than trusting a review's numbers.
- **Separate "make it investor-ready" from "is this idea validated."** A polished plan is a *document*, not
  demand — Bizplanr will happily generate one for an idea nobody wants. If the real question is build-or-not,
  put the go/no-go on a **real demand test** (smoke test / pre-sale) and route it to `/sales-idea-validation`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research (2026-07) — Bizplanr is an actively evolving free tool; tiers, the one-time price,
and free-export formats move. Verify at bizplanr.ai/pricing.*

- **AI-generated financials are guesses — and thin on the free tier.** Projections are the model's estimates
  and the free forecasting is basic (no scenario/multi-year depth); replace them with real numbers before
  funding.
- **Plans read generic for niche/complex businesses.** Reviewers flag shallow, cookie-cutter output that
  lacks depth for specialized or complex planning; a thin input makes it worse. Feed a rich description and
  edit heavily.
- **The standalone tools' outputs don't talk to each other.** SWOT, competitor, financial-model, and
  one-page generators run independently — reconcile their numbers/claims by hand before presenting.
- **Free export is typically PDF-only; Word/Excel is the paid unlock.** Sources vary on the exact free-tier
  formats — verify on the live site if the user needs editable exports.
- **No public API / no automation.** UI-only: no API, webhooks, Zapier/Make, or MCP. Export is a manual
  download. Automate with an LLM API instead.
- **Namesake collision.** **bizplanr.ai** (this — free + one-time paid) vs **bizplanner.ai** ("BizPlanner AI",
  a separate paid product — one-time payment + AI-word top-ups, no free tier, a 30% affiliate — see
  `/sales-bizplanner`) vs **bizplanaipro.com** ("BizPlan AI Pro" — a credit-based generator with an AI Coach,
  see `/sales-bizplanaipro`) — don't merge their pricing, features, or affiliate claims.
- **A generated plan is not validated demand.** It will produce a confident plan for an unwanted idea — settle
  the go/no-go with a real behavior test (smoke test / pre-sale), not the plan.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full business-plan/validator landscape (use this to actually decide build-or-not; a generated plan is a document, not demand)
- `/sales-bizplanner` — BizPlanner AI (bizplanner.ai) — the near-namesake *paid* generator (one-time payment + AI-word top-ups, no free tier, 30% affiliate); don't confuse the two domains
- `/sales-bizplanaipro` — BizPlan AI Pro (bizplanaipro.com) — the third near-namesake, a *credit-based* generator (credit packs that never expire) bundling a Startup Idea Validator, an AI Business Coach, and AI Decision Analysis; don't confuse the domains
- `/sales-plannit` — Plannit AI (now AIGenerator.com) platform help (the closest sibling — questionnaire → a 15–20 page plan with marketing assets and real-time team collaboration; UI-only/no API)
- `/sales-venturekit` — VentureKit platform help (AI business-planning software angled at lender/SBA-ready funding docs, with a built-in LLC-formation service; UI-only/no API)
- `/sales-upmetrics` — Upmetrics platform help (mature, team-oriented suite — deeper multi-year forecasting, plan-vs-actuals, QuickBooks/Xero import, white-label consultant tier; UI-only/no API)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Bizplanr made me a plan with financial projections — can I take it to investors?"
**User says**: "Bizplanr generated a full plan with revenue projections in five minutes. Is it investor-ready as-is?"
**Skill does**: Credits the structure and speed but warns the **financials are AI estimates** (and the free
tier's forecasting is basic), so an investor/lender will probe them. Tells the user to keep the outline and
market framing but **replace every projection, market-size, and unit-economics figure with their own real
numbers and cite sources**, and to **reconcile the standalone financial-model output with the plan's
financials by hand**. Adds that a fundable-looking plan is a document, not validated demand — if the go/no-go
is still open, route it to `/sales-idea-validation`.
**Result**: The founder submits a plan grounded in real numbers instead of AI-padded projections.

### Example 2: "Can I call Bizplanr's API to generate plans and pull them into my app?" (developer/automation)
**User says**: "I want to script Bizplanr to batch-generate plans and export each via the API or a webhook."
**Skill does**: States plainly that Bizplanr is **UI-only — no public API, no webhooks, no Zapier/Make, no
MCP** — so there's no supported way to batch-generate or export programmatically. Notes the only export is a
**manual download** (PDF free; Word/Excel on the one-time paid workspace), and that for programmatic plan
generation the user should **call an LLM API directly**. Points out the thing actually worth automating for a
go/no-go is a real demand signal (landing-page analytics), not a generated plan — routing that to
`/sales-funnel`.
**Result**: The user avoids planning an integration around a nonexistent API and picks a workable path.

### Example 3: "Bizplanr wants a subscription and my plan reads generic"
**User says**: "A Bizplanr review mentions a monthly subscription and a 30% affiliate, but my plan is really generic. What gives?"
**Skill does**: Flags the **namesake collision** — a paid-to-generate tool with a 30% affiliate points to
**bizplanner.ai ("BizPlanner AI")**, a *different* product, not **bizplanr.ai** (free + a one-time paid
workspace); a monthly-subscription mention is likely a separate similarly named tool entirely — and asks
which domain they're on so reviews/pricing don't cross-contaminate. Then fixes the
generic output: the cause is thin input, so feed a **detailed** description (exact customer, the specific
problem, how it's solved today, business model, pricing) and **edit the draft heavily**, especially the
competitive and operations sections.
**Result**: The user sorts out which tool they're using and gets a more specific plan by enriching the input.

## Troubleshooting

### "Is this the same as BizPlanner.ai / bizplanaipro.com? The pricing I see doesn't match"
**Symptom**: A review or checkout shows a monthly subscription, a 30% affiliate program, or features that
don't match a free tool.
**Cause**: **Namesake collision** — **bizplanr.ai** (this tool) is easily confused with **bizplanner.ai**
("BizPlanner AI") and **bizplanaipro.com**, which are separate products with their own pricing models.
**Solution**: Confirm the exact domain in the address bar. Bizplanr.ai's core generator + PDF is **free** with
a **one-time** paid workspace; if you're seeing a subscription/affiliate, you're on a different site. Don't
transfer pricing, features, or tips across the three.

### "My Bizplanr plan reads generic — it could describe any business"
**Symptom**: The plan is vague and not specific to the niche or idea.
**Cause**: A thin, one-line input — Bizplanr generates over whatever you give it, so a short description
yields a short, cookie-cutter plan, and it's known to lack depth for specialized/complex businesses.
**Solution**: Feed a **detailed** description — target customer, the exact problem, how people solve it today,
the business model and pricing — then **edit the draft heavily** and replace placeholder numbers. Settle the
go/no-go with a real demand test via `/sales-idea-validation`.

### "The financial projections look off, and the SWOT/financial tools don't agree with the plan"
**Symptom**: Revenue and projections the founder didn't enter, and numbers that differ across the standalone
generators.
**Cause**: The forecasts are **AI-generated estimates** (basic on the free tier), and the **standalone tools
run independently** so their outputs don't cross-reference the main plan.
**Solution**: Treat the forecast as a **template to overwrite** — plug in real unit economics, costs, and a
defensible growth assumption, cite sources for market size, and **manually reconcile** the financial-model /
SWOT / competitor outputs with the plan before sharing. Advanced forecasting is a paid-workspace unlock.
