---
name: sales-bizplanner
description: "BizPlanner AI (bizplanner.ai) platform help — an AI business-plan generator that turns a short questionnaire into a full multi-section plan (executive summary, market and competitor analysis, SWOT, financial projections, industry trends, regulations, next steps) in about fifteen minutes, with in-browser editing, document regeneration, and PDF/Word export. Use when generating or editing a plan in BizPlanner AI, interpreting its AI-written financials, fixing a plan that reads generic or lacks depth for a niche, deciding whether the one-time payment plus AI-word top-ups is worth it, getting Word export, joining its 30% affiliate program, telling bizplanner.ai apart from the similarly named bizplanr.ai, or asking whether it has an API to export or automate plans. Do NOT use for the tool-agnostic validate-before-building method or comparing business-plan tools across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in BizPlanner AI]"
license: MIT
version: 1.0.1
tags: [sales, validation, pre-launch, platform]
---

# BizPlanner AI Platform Help

BizPlanner AI (**bizplanner.ai**) is a **paid AI business-plan generator** for entrepreneurs and small-business
owners. You answer a **short questionnaire** and it generates a **full multi-section plan in ~15 minutes** —
executive summary, business description, market research & analysis, competitor analysis, SWOT, organizational
structure, products/services, marketing & sales strategy, operations plan, **financial projections**, industry
trends & stats, relevant regulations, risk analysis, and suggested next steps — powered by **GPT-4**. It has an
**in-browser editor**, a **regenerate-document** feature, and **PDF/Word export**. Unlike its free namesake, there
is **no free plan**: a **one-time payment (~$9.99, no subscription)** unlocks a plan plus **2 free full
regenerations**, and further AI generation/rewriting is bought as **AI-word top-ups**. It's **UI-only — no public
API**. It runs a **30% affiliate program**. (Naming: **bizplanner.ai** is this tool; **bizplanr.ai** — "Bizplanr"
— is a *different*, free generator; **bizplanaipro.com** — "BizPlan AI Pro" (`/sales-bizplanaipro`), a
credit-based generator — is another; don't conflate them.)

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from BizPlanner AI?**
   - A) Generate/edit a plan, financials, competitor analysis, or SWOT and interpret the output
   - B) Make the plan **investor-ready / lender-ready** for funding
   - C) Understand access — the **one-time payment**, the **2 free regenerations**, **AI-word top-ups**, and export formats
   - D) Export or automate plan generation (the API reality), join the **30% affiliate program**, or you hit the **bizplanner.ai vs bizplanr.ai** mix-up
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a generated plan is a document, not demand) —
   route in Step 2.

Skip-ahead: if the user already gave enough context, or wants to compare business-plan tools across the
market to pick one, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A **cross-market ranking** of business-plan/validator tools (Bizplanr, Upmetrics, VentureKit… to pick one) — but answer a quick BizPlanner-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer BizPlanner AI-specific questions using Step 3.

## Step 3 — BizPlanner AI platform reference

**Read `references/platform-guide.md`** for the full reference — the section set the generator produces, what the
one-time payment includes vs the AI-word top-ups, the 2-free-regenerations limit, export formats, the no-public-API
reality and manual export, the 30% affiliate program terms, the bizplanner.ai vs bizplanr.ai disambiguation, and
how to feed rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

- **Treat the plan and financial projections as AI estimates, not facts — and swap in real numbers before an
  investor or lender sees them.** BizPlanner AI drafts a clean plan fast, but its **financials are GPT-generated
  estimates**; reviewers warn that if you give thin input (pricing, capacity, target-customer volume), it **fills
  in assumptions that may not match reality**. Tell the user to keep the structure and market framing, then
  **replace the projections, market size, and unit economics with their own real numbers and cite sources** — a
  funder scrutinizes the financials first. And a fundable-looking plan is **not demand**: settle the go/no-go with
  a **real behavior test — a smoke test or a pre-sale** — not the plan, and route that to `/sales-idea-validation`.
- **De-genericize niche plans by feeding richer input and editing hard.** A thin one-line idea yields a
  cookie-cutter plan that "could describe any business." The fix is input richness: feed a **detailed**
  description (exact customer, the specific problem, how it's solved today, business model, pricing) and
  **edit heavily** — especially the competitive, operations, and revenue sections, where the model lacks
  depth for specialized verticals.
- **Budget the regenerations — you get 2 free, then pay for AI words.** The one-time payment includes **2 free
  full regenerations**; beyond that, regenerating or rewriting sections consumes **AI-word top-ups** (bought
  separately). Tell the user to **spend the free regenerations on the sections that matter most** and get the
  input right up front rather than burning regenerations fixing a thin first draft.
- **Present all pricing as best-effort and point to bizplanner.ai.** Best-effort at research: a **one-time
  ~$9.99 payment (no subscription)** generates a plan with 2 free regenerations and **PDF/Word export**, with
  **AI-word top-ups** (e.g. ~$7.99/50k, ~$9.99/100k words) for more generation; a **30-day money-back guarantee**
  is advertised. Tell them to **confirm current pricing and top-up sizes on the live site** — there's no free
  tier here (unlike bizplanr.ai), so budget the one-time fee.
- **There's no usable public API — don't plan an integration around it.** State plainly that BizPlanner AI is
  **UI-only: no public API, no webhooks, no Zapier/Make, no MCP**. The only export is the plan itself, downloaded
  manually as **PDF or Word**. For programmatic plan generation, **call an LLM API directly** instead.
- **Clear up the bizplanner.ai vs bizplanr.ai mix-up.** If the user cites a **free** plan generator or a
  **one-time paid workspace with mobile apps**, they're likely on **bizplanr.ai ("Bizplanr")** — a *separate*
  product. **bizplanner.ai** (this tool) has **no free tier**: you pay once (~$9.99) to generate. Confirm which
  domain they're on so reviews, pricing, and tips don't cross-contaminate.
- **On the affiliate program, quote the terms carefully.** BizPlanner AI pays a **30% commission** per referred
  sale via a unique referral link; **self-referrals are banned** and coupon/discount manipulation triggers a
  permanent ban. Present the rate as best-effort and point to bizplanner.ai/affiliate for current terms.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Best-effort from research (2026-07) — BizPlanner AI is an actively evolving tool; the one-time price, AI-word
top-up sizes, and export formats move. Verify at bizplanner.ai.*

- **AI-generated financials are guesses.** Projections are the model's estimates; with thin input it invents
  assumptions (pricing, capacity, customer volume) that may not match reality. Replace them with real numbers
  before funding, and sanity-check every figure.
- **Plans read generic for niche/complex businesses.** A thin input yields cookie-cutter output that lacks depth
  for specialized verticals. Feed a rich, detailed description and edit heavily.
- **No free tier — you pay to generate.** Unlike bizplanr.ai, there's no free plan; a one-time payment generates
  the plan with **2 free regenerations**, after which you buy **AI-word top-ups**. Get the input right before
  spending regenerations.
- **No public API / no automation.** UI-only: no API, webhooks, Zapier/Make, or MCP. Export is a manual PDF/Word
  download. Automate with an LLM API instead.
- **Namesake collision.** **bizplanner.ai** (this — paid one-time + AI-word top-ups, 30% affiliate) vs
  **bizplanr.ai** ("Bizplanr", a *free* generator with a one-time paid workspace and mobile apps) vs
  **bizplanaipro.com** ("BizPlan AI Pro", a *credit-based* generator with an AI Coach, see
  `/sales-bizplanaipro`) — don't merge their pricing, features, or affiliate claims.
- **A generated plan is not validated demand.** It will produce a confident plan for an unwanted idea — settle
  the go/no-go with a real behavior test (smoke test / pre-sale), not the plan.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full business-plan/validator landscape (use this to actually decide build-or-not; a generated plan is a document, not demand)
- `/sales-bizplanr` — Bizplanr (bizplanr.ai) — the near-namesake *free* AI business-plan generator (questionnaire → a full plan with basic financials in ~5 min, plus standalone SWOT/competitor/financial/one-page tools and mobile apps; one-time paid workspace, not a subscription; UI-only/no API) — don't confuse the two domains
- `/sales-bizplanaipro` — BizPlan AI Pro (bizplanaipro.com) — the third near-namesake, a *credit-based* generator (credit packs that never expire) bundling a Startup Idea Validator, an AI Business Coach, and AI Decision Analysis; UI-only/no API — don't confuse the domains
- `/sales-plannit` — Plannit AI (now AIGenerator.com) platform help (questionnaire → a 15–20 page plan with marketing assets and real-time team collaboration; UI-only/no API)
- `/sales-venturekit` — VentureKit platform help (AI business-planning software angled at lender/SBA-ready funding docs, with a built-in LLC-formation service; UI-only/no API)
- `/sales-upmetrics` — Upmetrics platform help (mature, team-oriented suite — deeper multi-year forecasting, plan-vs-actuals, QuickBooks/Xero import, white-label consultant tier; UI-only/no API)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "BizPlanner AI made me a plan with financial projections — can I take it to investors?"
**User says**: "BizPlanner AI generated a full plan with revenue projections in fifteen minutes. Is it investor-ready as-is?"
**Skill does**: Credits the structure and speed but warns the **financials are AI estimates** (and with thin
input it invents assumptions that may not match reality), so an investor/lender will probe them. Tells the user
to keep the outline and market framing but **replace every projection, market-size, and unit-economics figure
with their own real numbers and cite sources**. Adds that a fundable-looking plan is a document, not validated
demand — if the go/no-go is still open, route it to `/sales-idea-validation`.
**Result**: The founder submits a plan grounded in real numbers instead of AI-padded projections.

### Example 2: "Can I call BizPlanner AI's API to generate plans and pull them into my app?" (developer/automation)
**User says**: "I want to script BizPlanner AI to batch-generate plans and export each via the API or a webhook."
**Skill does**: States plainly that BizPlanner AI is **UI-only — no public API, no webhooks, no Zapier/Make, no
MCP** — so there's no supported way to batch-generate or export programmatically. Notes the only export is a
**manual PDF/Word download**, and that for programmatic plan generation the user should **call an LLM API
directly**. Points out the thing actually worth automating for a go/no-go is a real demand signal (landing-page
analytics), not a generated plan — routing that to `/sales-funnel`.
**Result**: The user avoids planning an integration around a nonexistent API and picks a workable path.

### Example 3: "Is BizPlanner AI the same as Bizplanr? My plan reads generic and I'm out of regenerations"
**User says**: "I thought BizPlanner AI was the free one, but I paid — and now my plan is really generic and I've used my regenerations. What gives?"
**Skill does**: Flags the **namesake collision** — the *free* generator is **bizplanr.ai ("Bizplanr")**, a
*different* product; **bizplanner.ai** (this tool) has **no free tier** and you pay once, getting **2 free
regenerations** before AI-word top-ups. Then fixes the generic output: the cause is thin input, so feed a
**detailed** description (exact customer, the specific problem, how it's solved today, business model, pricing)
and **edit the draft heavily**, especially the competitive and operations sections — and get the input right
before spending the remaining regenerations.
**Result**: The user sorts out which tool they're using and gets a more specific plan without wasting top-ups.

## Troubleshooting

### "Is this the same as Bizplanr / bizplanaipro.com? The pricing I see doesn't match"
**Symptom**: A review or checkout shows a **free** generator, a one-time **workspace** with mobile apps, or
features that don't match what you paid for.
**Cause**: **Namesake collision** — **bizplanner.ai** (this tool, paid one-time + AI-word top-ups) is easily
confused with **bizplanr.ai** ("Bizplanr", a *free* generator) and **bizplanaipro.com**, which are separate
products with their own pricing models.
**Solution**: Confirm the exact domain in the address bar. BizPlanner.ai has **no free tier** — a one-time
~$9.99 payment generates a plan with 2 free regenerations; if you're seeing a free generator or mobile apps,
you're on a different site. Don't transfer pricing, features, or affiliate terms across the three.

### "My BizPlanner AI plan reads generic — it could describe any business"
**Symptom**: The plan is vague and not specific to the niche or idea.
**Cause**: A thin, one-line input — BizPlanner AI generates over whatever you give it, so a short description
yields a short, cookie-cutter plan, and it's known to lack depth for specialized/complex businesses.
**Solution**: Feed a **detailed** description — target customer, the exact problem, how people solve it today,
the business model and pricing — then **edit the draft heavily** and replace placeholder numbers. Spend your
**2 free regenerations** on the sections that matter, and settle the go/no-go with a real demand test via
`/sales-idea-validation`.

### "The financial projections look off and I'm running out of regenerations"
**Symptom**: Revenue and projections the founder didn't enter, and no free regenerations left to fix them.
**Cause**: The forecasts are **AI-generated estimates** (it invents assumptions from thin input), and the
one-time payment only includes **2 free full regenerations** — beyond that you buy **AI-word top-ups**.
**Solution**: Treat the forecast as a **template to overwrite** — plug in real unit economics, costs, and a
defensible growth assumption, and cite sources for market size. Get the input rich before regenerating so you
don't burn top-ups; edit the numbers by hand in the in-browser editor rather than regenerating repeatedly.
