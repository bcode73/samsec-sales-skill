---
name: sales-plannit
description: "Plannit AI (now AIGenerator.com, by AIGenerator LLC) platform help — an AI business-plan generator that turns a short questionnaire into a 15–20 page plan with market analysis, financial projections, a pitch deck, and an executive summary, plus marketing assets (ad copy, email, social) and real-time team collaboration. Use when generating or editing a business plan in Plannit AI or AIGenerator, interpreting its AI-written financial projections, making a plan investor- or lender-ready, fixing a plan that reads generic or lacks depth for a niche industry, choosing between the free tier and the paid plan, confused by the plannit.ai → AIGenerator.com rebrand or an expired-domain redirect, or asking whether it has an API to export or automate plans. Do NOT use for the tool-agnostic validate-before-building method or comparing business-plan tools across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in Plannit AI]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# Plannit AI Platform Help

Plannit AI — now branded **AIGenerator.com** (both operated by **AIGenerator LLC**) — is an **AI
business-plan generator** for first-time founders, small-business owners, freelancers, and side-hustlers.
You answer a **short questionnaire** (~5–7 questions on product, target market, revenue model, competitive
edge, operations) and it generates a **15–20 page business plan** in about two minutes: executive summary,
market analysis, **financial projections**, and a **pitch deck**. The AIGenerator suite adds **marketing
assets** (ad copy, email campaigns, social strategy, content calendars), a domain-name generator, and an AI
business assistant. Unlike most siblings it offers **real-time team collaboration** (invite, comment, edit).
It's powered by GPT-4 under the hood and is **UI-only — no public API**. (Naming: **plannit.ai** now serves
**AIGenerator.com**; the unrelated **plannit.io** is a home/field-services app — don't conflate them.)

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from Plannit AI / AIGenerator?**
   - A) Generate/edit a plan, financials, pitch deck, or marketing assets and interpret the output
   - B) Make the plan **investor-ready / lender-ready** for funding
   - C) Understand access — the **free tier** vs the **paid plan**, one-time vs subscription pricing
   - D) Export or automate plan generation (the API reality), or you're confused by the **rebrand / dead site**
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a generated plan is a document, not demand) —
   route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare business-plan tools across
the market to pick one, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A **cross-market ranking** of business-plan/validator tools (Upmetrics, LivePlan, VentureKit… to pick one) — but answer a quick Plannit-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer Plannit-specific questions using Step 3.

## Step 3 — Plannit AI platform reference

**Read `references/platform-guide.md`** for the full reference — the module set (business plan, financials,
pitch deck, marketing assets, collaboration), what's editable vs generated, the free-tier vs paid-plan gates
and the one-time→subscription pricing shift, the no-public-API reality and manual export, the plannit.ai →
AIGenerator.com rebrand and plannit.io disambiguation, and how to feed rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

- **Treat the plan and financial projections as AI estimates, not facts — and swap in real numbers before an
  investor or lender sees them.** Plannit writes a polished plan fast, but its **forecasting is the weakest
  part** (reviewers rate it low) and its **revenue-stream suggestions read generic and sometimes unrelated**.
  Tell the user to keep the structure and market framing, then **replace the projections, market size, and
  unit economics with their own real numbers** — a funder will scrutinize the financials first.
- **De-genericize niche plans by feeding richer input and editing hard.** The top complaint is that plans
  **lack depth for specialized/niche industries** and could describe any business. The fix is input richness:
  feed a **detailed** description (exact customer, the specific problem, how it's solved today, business
  model, pricing) and **edit the draft heavily** — thin input in, cookie-cutter plan out. Expect to do manual
  adjustment; it drafts, you finish.
- **Separate "make it investor-ready" from "is this idea validated."** A fundable-looking plan is a
  *document*, not demand — Plannit will happily generate a confident plan for an idea nobody wants. If the
  real question is build-or-not, put the go/no-go on a **real demand test** (smoke test / pre-sale) and route
  it to `/sales-idea-validation`; use Plannit for the plan/pitch once demand is real.
- **Present all pricing as best-effort and flag the model shift.** The old Plannit AI charged **one-time per
  plan** (lifetime access, with 5/10-plan bundles); the rebranded AIGenerator.com moved to a **free tier + a
  monthly paid plan**. Sources disagree and the site's cert has lapsed — tell the user to **confirm current
  pricing on aigenerator.com** and note that if they need just one plan the free tier is usually enough.
- **There's no usable public API — don't plan an integration around it.** State plainly that Plannit /
  AIGenerator is **UI-only: no public API, no webhooks, no Zapier/Make, no MCP**. The only export is the plan
  itself (downloaded to a standard office format), done manually. For programmatic plan generation, **call an
  LLM API directly** instead.
- **Clear up the rebrand/dead-site confusion.** If the user hits a **redirect, an expired-certificate
  warning, or "Plannit is no longer available,"** explain that **plannit.ai now serves AIGenerator.com** (same
  company, AIGenerator LLC) — the product is still active, just rebranded — and that **plannit.io is a
  different, unrelated app** (home/field services), so reviews across the two don't transfer.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research (2026-07) — Plannit AI rebranded to AIGenerator.com; tiers, pricing model, and
reachability move. The live site's TLS cert was expired at research time; verify at aigenerator.com.*

- **AI-generated financials are guesses — and the weakest module.** Projections and revenue-stream ideas are
  the model's estimates (forecasting is its lowest-rated area); replace them with real numbers before funding.
- **Plans read generic for niche industries.** Reviewers flag shallow, cookie-cutter output that lacks depth
  for specialized niches; a thin input makes it worse. Feed a rich description and edit heavily.
- **A generated plan is not validated demand.** It will produce a confident plan for an unwanted idea — settle
  the go/no-go with a real behavior test (smoke test / pre-sale), not the plan.
- **No public API / no automation.** UI-only: no API, webhooks, Zapier/Make, or MCP. Export is manual (to a
  standard office format); automate with an LLM API instead. (An earlier "API available" claim conflated the
  internal GPT API — there is no developer-facing API.)
- **Rebrand + reachability.** plannit.ai now serves **AIGenerator.com** (AIGenerator LLC); the live site had an
  **expired certificate** and a competitor claimed it was "no longer available," but it's active under the new
  brand. Don't confuse it with **plannit.io** (an unrelated home/field-services app).
- **Pricing model changed.** Old Plannit = one-time per plan (lifetime) + 5/10-plan bundles; new AIGenerator =
  free tier + monthly paid plan. Verify current pricing on the live site — don't quote the old $ figure.
- **Support & reliability caveats.** Reviews (Trustpilot ~4.1) note slow support responsiveness and occasional
  reliability issues — set expectations and keep your own copy of any plan you generate.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full business-plan/validator landscape (use this to actually decide build-or-not; a generated plan is a document, not demand)
- `/sales-venturekit` — VentureKit platform help (the closest sibling — AI business-planning software with lender-ready financial forecasts and an LLC-formation service; no team collaboration, unlike Plannit)
- `/sales-upmetrics` — Upmetrics platform help (mature business-planning suite — deeper multi-year forecasting and plan-vs-actuals tracking than Plannit, plus QuickBooks/Xero import and a Professional/white-label consultant tier; also has real-time collaboration; UI-only/no public API)
- `/sales-venturusai` — VenturusAI platform help (framework-driven validator — SWOT/PESTEL/Porter/VRIO + sizing/financials/pitch deck; the analysis-report sibling)
- `/sales-informly` — Informly platform help (one idea → a 75+ page PDF report bundle; the per-report document-generator sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Plannit made me a plan with financial projections — can I take it to investors?"
**User says**: "Plannit AI generated a full business plan with revenue projections. Is it investor-ready as-is?"
**Skill does**: Credits the structure and speed but warns the **financials are AI estimates** — forecasting is
Plannit's weakest module and revenue ideas can read generic — so an investor/lender will probe them. Tells the
user to keep the outline and market framing but **replace every projection, market-size, and unit-economics
figure with their own real numbers**, then adds that a fundable-looking plan is a document, not validated
demand — if the go/no-go is still open, route it to `/sales-idea-validation`.
**Result**: The founder submits a plan grounded in real numbers instead of AI-padded projections.

### Example 2: "Can I call Plannit's API to generate 20 plans and pull them into my app?" (developer/automation)
**User says**: "I want to script Plannit AI / AIGenerator to batch-generate plans and export each via the API or a webhook."
**Skill does**: States plainly that Plannit / AIGenerator is **UI-only — no public API, no webhooks, no
Zapier/Make, no MCP** — so there's no supported way to batch-generate or export programmatically (an earlier
"API available" mention conflated the internal GPT API). Notes the only export is a **manual download to a
standard office format**, and that for programmatic plan generation the user should **call an LLM API
directly**. Points out the thing actually worth automating for a go/no-go is a real demand signal
(landing-page analytics), not a generated plan — routing that to `/sales-funnel`.
**Result**: The user avoids planning an integration around a nonexistent API and picks a workable path.

### Example 3: "The Plannit site redirects to something else and my plan reads generic"
**User says**: "plannit.ai sends me to AIGenerator.com now and threw a certificate error — is it dead? Also my plan is really generic."
**Skill does**: Explains that **plannit.ai now serves AIGenerator.com** (same company, AIGenerator LLC) — the
product is **active, just rebranded**, and the expired-cert warning is a maintenance lapse, not a shutdown
(and **plannit.io is a different, unrelated app**). Then fixes the generic output: the cause is a thin input,
so feed a **detailed** description (exact customer, the specific problem, how it's solved today, business
model, pricing) and **edit the draft heavily** — expect manual adjustment on niche industries.
**Result**: The user understands the rebrand and gets a more specific plan by enriching the input.

## Troubleshooting

### "plannit.ai redirects / shows a certificate error / says it's no longer available"
**Symptom**: The old Plannit AI domain redirects, throws an expired-cert warning, or a review says it's gone.
**Cause**: Plannit AI **rebranded to AIGenerator.com** (both AIGenerator LLC); the live site's TLS certificate
lapsed and a competitor review labeled it defunct.
**Solution**: Go to **aigenerator.com** — the business-plan generator is active under the new brand. Verify
current pricing/features there. Don't confuse it with **plannit.io**, an unrelated home/field-services app.

### "My Plannit plan reads generic — it could describe any business"
**Symptom**: The plan is vague and not specific to the niche or idea.
**Cause**: A thin, one-line input — Plannit generates over whatever you give it, so a short description yields a
short, cookie-cutter plan, and it's known to lack depth for specialized industries.
**Solution**: Feed a **detailed** description — target customer, the exact problem, how people solve it today,
the business model and pricing — then **edit the draft heavily** and replace placeholder numbers. Settle the
go/no-go with a real demand test via `/sales-idea-validation`.

### "The financial projections look off / too optimistic"
**Symptom**: Revenue and financial projections the founder didn't enter, or revenue ideas that feel unrelated.
**Cause**: The forecasts are **AI-generated estimates** (Plannit's lowest-rated area), not grounded in the
founder's real costs, pricing, or traction.
**Solution**: Treat the forecast as a **template to overwrite** — plug in real unit economics, costs, and a
defensible growth assumption, and cite sources for market size. Keep Plannit's structure; own the numbers.
