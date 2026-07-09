---
name: sales-prometai
description: "PrometAI (prometai.app) platform help — an AI business-plan generator whose edge is a connected financial model: DCF valuation, stress testing, and scenario analysis that recalculate as inputs change, plus a 50+ tool \"Entrepreneur Journey\" and strategy frameworks (SWOT, VRIO). Subscription tiers (free Explore, Basic, investor-grade Pro), unlike the one-time/credit siblings. Use when generating or editing a plan in PrometAI, interpreting its DCF valuation or auto-updating financial projections, fixing exports that lose formatting or limited real-time collaboration, choosing between its Explore/Basic/Pro tiers, or asking whether it has an API to export or automate plans (it does not — UI-only; ERP integrations are Enterprise-only). Do NOT use for the tool-agnostic validate-before-building method or ranking business-plan tools across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in PrometAI]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# PrometAI Platform Help

PrometAI (**prometai.app**) is an **AI business-plan generator and planning suite** for founders and small
businesses. A questionnaire produces a **full investor-oriented plan** — executive summary, market analysis,
strategy frameworks (SWOT, VRIO) — in minutes. Its distinguishing edge over the rest of the AI-plan cluster is
a **connected financial model**: financial projections, a **DCF valuation**, **stress testing**, and
**scenario analysis** that **recalculate together when you change an input** (reviewers call it the tool whose
financials stay "grounded, consistent, and connected end-to-end"). Around the generator sits a **50+ tool
"Entrepreneur Journey"** (idea generation, branding, founder profiles, risk assessment, valuation). Unlike the
one-time/credit siblings it's a **subscription** (free **Explore** → **Application-Ready/Basic** →
investor-grade **Pro** → **Enterprise**). It's **UI-only — no public API**; the advertised **ERP integrations
and FP&A analytics are Enterprise-only, sales-gated** custom deployments, not a documented developer API.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from PrometAI?**
   - A) Generate/edit a plan or a section (market analysis, SWOT/VRIO) and interpret the output
   - B) Work with the **financial model** — projections, **DCF valuation**, **stress testing**, scenario
     analysis — and read it critically for a lender/investor
   - C) Pick a **subscription tier** (Explore vs Basic vs Pro) by what's gated (export format, DCF, plan count)
   - D) Fix a **broken export** (formatting lost) or work around **limited real-time collaboration**
   - E) Export or automate plan generation (the API reality) / use the Enterprise ERP + FP&A angle
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a generated plan, and PrometAI's own score, are
   not demand) — route in Step 2.

Skip-ahead: if the user already gave enough context, or wants to compare business-plan tools across the market
to pick one, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A **cross-market ranking** of business-plan/validator tools (Upmetrics, VentureKit, Bizplanr… to pick one) — but answer a quick PrometAI-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer PrometAI-specific questions using Step 3.

## Step 3 — PrometAI platform reference

**Read `references/platform-guide.md`** for the full reference — the module set (plan generator, connected
financial model with DCF valuation / stress testing / scenario analysis, SWOT/VRIO frameworks, the 50+ tool
"Entrepreneur Journey", NDA/term-sheet templates), the subscription tiers and what each gates (plan count, AI
requests, export format, DCF, translations), the no-public-API reality and manual export, the Enterprise
ERP/FP&A angle, and how to feed rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

- **Treat the financials — DCF valuation included — as AI estimates, and verify every market figure.** The
  connected model is PrometAI's best feature, but reviewers found it **invents market sizes and cites vague
  reports**; the DCF and projections are the model's guesses calibrated to an industry, not your business. Keep
  the structure and the fact that everything recalculates together, then **replace every projection, market-size
  figure, and valuation assumption with your own real numbers and cite sources** — a lender/investor probes the
  financials first, and PrometAI's own reviewers say most lenders still want a **separate financial review**.
- **The DCF valuation needs real inputs — it isn't a beginner "what's my company worth" button.** A DCF is only
  as good as its assumptions (discount rate, cash-flow forecast, terminal value); PrometAI will produce a
  confident number from thin input. Tell the user to sanity-check the inputs, not just accept the output, and to
  treat the valuation as a modelling exercise, not an appraisal.
- **Pick the tier by what's gated, not the headline price.** Best-effort: **Explore (free)** = 1 plan, 25 AI
  requests/mo, **view-only sharing, no export**; **Application-Ready/Basic** (~$55/mo, ~$25 annual) = 3 plans,
  **PDF export**, financial dashboards; **Investor-Grade/Pro** (~$145/mo, ~$65 annual) = 8 plans, **PowerPoint
  export**, **DCF valuation + stress testing**, NDA/term-sheet templates, 10 translations. The two gates that
  usually decide it: **can you export at all** (not on free) and **do you need DCF/stress-testing** (Pro only).
  Confirm live — annual discounts are steep and pricing moves.
- **Plan around limited collaboration and lossy exports.** Reviewers flag **very limited collaboration (no
  real-time co-editing)** and **exports that sometimes lose formatting**. For a team plan, have one owner drive
  and share a view-only link; after export, **re-check formatting in the target app** (PDF/PowerPoint) and fix
  layout there rather than expecting a clean round-trip.
- **There's no usable public API — don't plan an integration around it.** State plainly that PrometAI is
  **UI-only: no public API, no webhooks, no Zapier/Make, no MCP**. The only export is the plan itself
  (PDF/PowerPoint on paid tiers), downloaded manually. The advertised **"ERP integrations" and "FP&A analytics"
  are Enterprise-only, sales-gated** custom deployments — not a self-serve developer API. For programmatic plan
  generation, **call an LLM API directly** instead.
- **Present all pricing/tier limits as best-effort and point to prometai.app.** Plan counts, AI-request caps,
  and export gates move; tell the user to confirm on the live pricing page rather than trusting a review's
  numbers.
- **A polished, investor-grade plan is still not validated demand.** PrometAI's strength is making output *look*
  fundable (DCF, term sheets, consultant-style SWOT/VRIO); that is a document, not evidence anyone will pay.
  Settle the go/no-go with a **real behavior test — a smoke test or a pre-sale** — routed to
  `/sales-idea-validation`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research (2026-07) — PrometAI is a fast-moving tool; tiers, prices, AI-request caps, and
export gates move. Verify at prometai.app.*

- **The financials are AI estimates — DCF and all.** The connected model recalculates consistently, but the
  underlying projections, market sizes, and valuation are the model's guesses; reviewers caught it inventing
  market figures. Replace the numbers with real ones and cite sources before funding — most lenders still want a
  separate financial review.
- **The DCF valuation isn't beginner-friendly.** It needs real assumptions (discount rate, forecast, terminal
  value) to mean anything; a confident number from thin input is not an appraisal. Sanity-check the inputs.
- **No export on the free tier.** Explore is **view-only** (link sharing only). PDF export starts on Basic;
  PowerPoint + DCF + stress testing are **Pro-only**. Pick the tier by the export/DCF gate, not the price.
- **Collaboration is very limited.** No real-time co-editing — reviewers call this a weak spot. Have one owner
  drive and share a view-only link for a team plan.
- **Exports can lose formatting.** Re-check the exported PDF/PowerPoint in the target app and fix layout there;
  don't expect a clean round-trip.
- **No public API / no automation.** UI-only: no API, webhooks, Zapier/Make, or MCP. The advertised ERP
  integrations + FP&A analytics are **Enterprise-only, sales-gated**, not a developer API. Export is a manual
  download. Automate with an LLM API instead.
- **Subscription, and on the pricey end.** Unlike the one-time/credit siblings (Bizplanr, BizPlanner AI, BizPlan
  AI Pro), PrometAI is a **monthly/quarterly/annual subscription** — Pro is ~$145/mo (~$65 annual). Factor the
  recurring cost against one-time alternatives if you only need one plan.
- **A generated plan is not validated demand.** It will produce a confident, investor-grade plan (and a
  valuation) for an unwanted idea — settle the go/no-go with a real behavior test, not the plan.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full business-plan/validator landscape (use this to actually decide build-or-not; a generated plan and an AI score are not demand)
- `/sales-upmetrics` — Upmetrics platform help (the closest peer on financial depth — deep multi-year forecasting, plan-vs-actuals, QuickBooks/Xero import, real-time collaboration, white-label consultant tier; UI-only/no API)
- `/sales-venturekit` — VentureKit platform help (AI business-planning software angled at lender/SBA-ready funding docs + a built-in LLC-formation service; generous free tier; UI-only/no API)
- `/sales-bizplanr` — Bizplanr platform help (a *free* AI business-plan generator with standalone SWOT/competitor tools and mobile apps, monetized by a one-time paid workspace — the low-cost contrast to PrometAI's subscription)
- `/sales-venturusai` — VenturusAI platform help (framework-driven validator — SWOT/PESTEL/Porter's/VRIO + TAM/SAM/SOM, personas, financials, pitch deck; pure-LLM, scores skew encouraging; API Enterprise-only)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "PrometAI gave me a DCF valuation and a full plan — can I take it to an investor as-is?"
**User says**: "It generated an investor-grade plan with a DCF valuation and 5-year projections. Is it fundable straight away?"
**Skill does**: Credits the **connected financial model** (its real edge — everything recalculates together) but
flags that the **projections, market sizes, and the DCF valuation are AI estimates**, that reviewers caught it
**inventing market figures**, and that a DCF is only as good as its assumptions (so it's a modelling exercise,
not an appraisal). Tells the user to keep the structure but **replace every number with real figures and cite
sources**, and notes most lenders still want a **separate financial review**. Adds that a fundable-looking plan
is a document, not demand — if the go/no-go is open, route it to `/sales-idea-validation`.
**Result**: The founder presents a plan grounded in defensible numbers instead of an AI-padded valuation.

### Example 2: "Can I call PrometAI's API to export plans into my app?" (developer/automation)
**User says**: "I want to script PrometAI to generate plans for a list of ideas and pull each out via the API or a webhook."
**Skill does**: States plainly that PrometAI is **UI-only — no public API, no webhooks, no Zapier/Make, no
MCP** — so there's no supported way to batch-generate or export programmatically; the only export is a **manual
PDF/PowerPoint download** on paid tiers. Notes the advertised **ERP integrations + FP&A analytics are
Enterprise-only, sales-gated** custom deployments, not a self-serve developer API, and that for programmatic
plan generation the user should **call an LLM API directly**. Points out the thing worth automating for a
go/no-go is a real demand signal (landing-page analytics), not a generated plan — routing that to `/sales-funnel`.
**Result**: The user avoids building an integration around a nonexistent API and picks a workable path.

### Example 3: "Which PrometAI tier do I need, and is the free plan enough?"
**User says**: "I'm on the free Explore plan but can't export. Do I need Basic or Pro?"
**Skill does**: Explains the **tier gates**: **Explore (free)** is **view-only, no export**; **Basic** adds
**PDF export** + financial dashboards; **Pro** adds **PowerPoint export, the DCF valuation, and stress testing**
plus NDA/term-sheet templates and translations. Frames the choice on the two gates that actually decide it —
**can you export at all** (needs Basic) and **do you need DCF/stress-testing** (needs Pro) — and flags that
PrometAI is a **subscription** (Pro ~$145/mo, ~$65 annual), pricier than one-time siblings, so confirm current
prices on prometai.app and weigh the recurring cost if you only need one plan.
**Result**: The user picks the tier by the export/DCF gate rather than overpaying or hitting the free-tier wall.

## Troubleshooting

### "My PrometAI plan reads generic — it could describe any business"
**Symptom**: The plan is vague and not specific to the niche or idea.
**Cause**: A thin, one-line input — the generator writes over whatever you give it, so a short description yields
a short, cookie-cutter plan, and AI plan tools lack depth for specialized verticals.
**Solution**: Feed a **detailed** description — target customer, the exact problem, how people solve it today,
business model and pricing — then **edit the draft heavily**, especially the competitive and operations
sections. Replace the AI projections and the DCF inputs with real numbers. Settle the go/no-go with a real
demand test via `/sales-idea-validation`.

### "My export lost its formatting / I can't co-edit with my team"
**Symptom**: The exported PDF/PowerPoint looks broken, or teammates can't edit the plan live.
**Cause**: Two known PrometAI limits — **exports sometimes lose formatting** and **collaboration is very limited
(no real-time co-editing)**.
**Solution**: For exports, re-check the file in the target app (PDF viewer / PowerPoint) and fix layout there
rather than expecting a clean round-trip. For teams, have **one owner drive** the plan and share a **view-only
link**; merge feedback manually instead of relying on live co-editing.

### "Is PrometAI's DCF valuation my real company valuation?"
**Symptom**: The founder wants to quote PrometAI's valuation number to an investor.
**Cause**: A DCF is a **model** whose output depends entirely on its assumptions (discount rate, cash-flow
forecast, terminal value); PrometAI produces a confident figure from whatever inputs it's given.
**Solution**: Treat it as a **modelling exercise, not an appraisal**. Sanity-check the inputs, replace
AI-guessed cash flows with real projections, and — for anything high-stakes — get an independent valuation.
Present the number as "an illustrative DCF at these assumptions," not a market valuation.
