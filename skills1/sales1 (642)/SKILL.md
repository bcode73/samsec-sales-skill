---
name: sales-venturekit
description: "VentureKit (venturekit.ai) platform help — AI business-planning software for first-time founders and SMB owners that turns an idea into a full business plan, lender-ready financial forecasts (P&L, balance sheet, projections), a pitch deck, market research, an always-on AI business assistant, and a Radar monitor — plus a built-in LLC formation & compliance service (EIN, registered agent, state filings). Generous free tier; an Agency tier suits consultants writing many plans. Use when generating a business plan or financial forecast in VentureKit, interpreting or editing its AI-written plan, making a plan lender-ready or SBA-ready for a loan, deciding between the free, Pro, and Agency tiers, using its LLC formation service, or asking whether it has an API to export or automate plans. Do NOT use for the tool-agnostic validate-before-building method or comparing business-plan and validator tools across the market (use /sales-idea-validation), or building the smoke-test landing page (use /sales-funnel)."
argument-hint: "[describe what you need help with in VentureKit]"
license: MIT
version: 1.0.0
tags: [sales, validation, pre-launch, platform]
---

# VentureKit Platform Help

VentureKit (venturekit.ai) is **AI business-planning software** for first-time founders and small-business
owners. You describe an idea and it generates a **full business plan** (multi-section, ~28 pages), **editable
financial forecasts** (revenue, expenses, P&L, balance sheet), a **pitch deck** (designer themes), a **market
research** report, an always-on **AI business assistant**, and a **Radar** monitor — and it can also **form
your LLC** (articles of organization, EIN, registered agent, state filings) as a separate paid service. Its
angle vs the idea-validator cluster is **lender/SBA-ready plans to secure funding**, a **very generous free
tier**, and an **Agency tier for consultants** writing many plans. The catch: the plan and financials are
**AI-generated estimates** — reviewers note it can invent details and read cookie-cutter — and it's **UI-only
with no public API**. (Note: **venturekit.ai** is the tool; **venturekit.com** is an unrelated product.)

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer:

1. **What do you want from VentureKit?**
   - A) Generate/edit a plan, financials, pitch deck, or market research and interpret the output
   - B) Make the plan **lender-ready / SBA-ready** for a loan or investor
   - C) Understand the tiers — Free vs Pro vs Agency (plan limits), or the LLC Formation service
   - D) Export or automate plan generation (the API reality)
2. **What's the real question — "is this idea worth building?" or "how do I use this tool?"** If it's the
   go/no-go decision itself, that's `/sales-idea-validation` (a generated plan is a document, not demand) —
   route in Step 2.

Skip-ahead: if the user wants the validate-before-building *method* or to compare business-plan/validator
tools across the market to pick one, that's a `/sales-idea-validation` question — route immediately.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| The validate-before-building **method**, or the go/no-go decision itself | `/sales-idea-validation {question}` |
| A **cross-market ranking** of business-plan/validator tools (LivePlan, Upmetrics, VenturusAI… to pick one) — but answer a quick VentureKit-vs-X *how-they-differ* inline first (Step 4) | `/sales-idea-validation {question}` |
| Building the smoke-test / fake-door **landing page** to test real demand | `/sales-funnel {question}` |
| Growing a pre-launch **waitlist** / capturing real demand | `/sales-audience-growth {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-idea-validation {original question}`"

Otherwise, answer VentureKit-specific questions using Step 3.

## Step 3 — VentureKit platform reference

**Read `references/platform-guide.md`** for the full reference — the module set (business plan, financials,
pitch deck, market research, AI Assistant, Radar) and what each contains, what's editable vs generated, the
Free/Pro/Agency tiers with plan limits, the LLC Formation & registered-agent service and pricing, the
no-public-API reality and the manual PDF/print export, and how to feed it a rich input to avoid generic output.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the generated plan and financials as AI estimates, not facts — and swap in real numbers before a
  lender sees them.** VentureKit writes a polished, structured plan fast, but reviewers note it can **invent
  details out of thin air** and read cookie-cutter, and the **financial projections are the model's guesses**.
  Tell the user to keep the structure/outline and market-research framing, then **replace the forecasts,
  market size, and unit economics with their own real numbers** — a bank or SBA underwriter will scrutinize the
  financials, and AI-padded projections are the fastest way to lose credibility.
- **Separate "make it lender/SBA-ready" from "is this idea validated."** A fundable-looking plan is a
  *document*, not demand — VentureKit will happily generate a confident plan for an idea nobody wants. If the
  real question is build-or-not, put the go/no-go on a **real demand test** (smoke test / pre-sale) and route
  it to `/sales-idea-validation`; use VentureKit for the plan/pitch once demand is real.
- **Present all pricing/tiers as best-effort and point to venturekit.ai/pricing.** Frame the tiers around what
  breaks: **Free** gives unlimited "light" plans + a small number of **full plans per month** (commonly cited
  as 3) with forecasts, pitch deck, market research, AI Assistant, and Radar; **Pro** raises limits (its price
  is quoted inconsistently across sources — verify on site); **Agency** is the **many-plans-per-month** tier
  built for consultants. The **LLC Formation** service and **registered agent** are separate annual fees. **If the user only needs one or a few plans, tell them the free tier is enough — they don't need Pro or Agency** (those solve higher monthly volume, not more features).
- **There's no usable public API — don't plan an integration around it.** State plainly that VentureKit is
  **UI-only: no public API, no webhooks, no Zapier/Make, no MCP**. The only reliable export is the **plan
  itself (PDF/print/share)** done manually. If programmatic plan generation matters, call an **LLM API
  directly** or pick a tool built for it — don't build a pipeline on VentureKit.
- **The single biggest lever is input richness — coach it.** Generic output traces to a thin one-line idea.
  Tell the user to feed a **detailed** description (target customer, the specific problem, how it's solved
  today, the business model, pricing) and to edit the draft heavily; richer input in → specific plan out.
- **No team collaboration — flag it for team planners.** VentureKit is a solo, AI-first generator with no
  real-time co-editing; if the user needs a collaborative plan with teammates or an advisor, that's a
  cross-market comparison → route to `/sales-idea-validation` for LivePlan/Upmetrics-style alternatives.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — VentureKit's tiers, plan limits, and features move; verify at venturekit.ai/pricing.*

- **AI-generated financials are guesses.** Revenue/expense/P&L/balance-sheet projections are the model's
  estimates, not grounded numbers — replace them with your own before a lender or investor reviews them.
- **Plans can read cookie-cutter / invented.** Reviewers flag that it can fabricate details and lacks human
  nuance; a thin input makes it worse. Feed a rich description and edit heavily.
- **A generated plan is not validated demand.** It will produce a confident plan for an unwanted idea — settle
  the go/no-go with a real behavior test (smoke test / pre-sale), not the plan.
- **No public API / no automation.** UI-only: no API, webhooks, Zapier/Make, or MCP. Export is the manual
  PDF/print only; automate with an LLM API instead.
- **No team collaboration.** Solo generator, no real-time co-editing — unsuitable for team/advisor planning
  (LivePlan/Upmetrics do that).
- **Free tier caps *full* plans.** "Light" plans are unlimited but full plans are limited per month (commonly
  cited as 3); the **Agency** tier is the many-plans option. Verify current numbers on the pricing page.
- **LLC Formation is a separate paid service.** Business-entity formation, EIN, and registered agent are
  annual fees on top of the planning tiers — compare against dedicated formation services before buying.
- **Domain collision.** venturekit.**ai** is this tool; venturekit.**com** is an unrelated product — don't
  conflate reviews or docs across the two.

## Related skills

- `/sales-idea-validation` — The tool-agnostic validate-before-building method + the full business-plan/validator landscape (use this to actually decide build-or-not; a generated plan is a document, not demand)
- `/sales-plannit` — Plannit AI platform help (the closest sibling — an AI business-plan generator, now rebranded AIGenerator.com, with a questionnaire → 15–20 page plan, financial projections, a pitch deck, and — unlike VentureKit — real-time team collaboration; UI-only/no public API)
- `/sales-upmetrics` — Upmetrics platform help (the mature-suite sibling — deeper multi-year forecasting, plan-vs-actuals tracking, QuickBooks/Xero import, real-time collaboration, and a Professional/white-label tier for consultants that VentureKit lacks; UI-only/no public API)
- `/sales-venturusai` — VenturusAI platform help (framework-driven validator — SWOT/PESTEL/Porter/VRIO + sizing/financials/pitch deck; the analysis-report sibling to VentureKit's full-plan generator)
- `/sales-informly` — Informly platform help (one freeform idea → a 75+ page PDF report bundle; per-report pricing, the document-generator sibling)
- `/sales-ideaproof` — IdeaProof platform help (120s viability score + pre-launch suite; the fast-score sibling)
- `/sales-validator-ai` — Validator AI platform help (a free score-and-report validator — the fast-gut-check sibling)
- `/sales-funnel` — Build the smoke-test / fake-door landing page the real demand test runs on
- `/sales-audience-growth` — Grow a pre-launch waitlist and capture real demand
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "VentureKit made me a great plan with financials — can I take it to my bank for a loan?"
**User says**: "VentureKit generated a full business plan with revenue projections and a P&L. Can I hand this to my bank/SBA for a loan?"
**Skill does**: Credits the structure and speed but warns the **financials are AI estimates** — VentureKit can
invent details, so a lender/underwriter will scrutinize numbers that read padded. Tells the user to keep the
outline and market-research framing but **replace every forecast, market-size, and unit-economics figure with
their own real numbers** before submitting, and to sanity-check assumptions against a primary source. Adds
that a fundable-looking plan is a document, not validated demand — if the go/no-go is still open, route it to
`/sales-idea-validation`.
**Result**: The founder submits a plan grounded in real numbers instead of AI-padded projections.

### Example 2: "Can I pull my VentureKit plans out via the API into my own app?" (developer/automation)
**User says**: "I want to script VentureKit to generate 15 plans and pull each one into my database via the API or a webhook."
**Skill does**: States plainly that VentureKit is **UI-only — there is no public API, no webhooks, no
Zapier/Make, and no MCP** — so there's no supported way to batch-generate or export programmatically. Notes
the only reliable export is the **plan PDF/print/share done manually**, and that if programmatic plan
generation is essential the user should **call an LLM API directly** or pick a tool built for automation.
Points out the thing actually worth automating is a real demand signal (landing-page analytics), not a
generated plan — routing that to `/sales-funnel`.
**Result**: The user avoids planning an integration around a nonexistent API and picks a workable path.

### Example 3: "Is VentureKit's free plan enough, or do I need Pro or the Agency plan?" (tiers)
**User says**: "I just need one solid business plan and a pitch deck. Is the free VentureKit plan enough, or should I pay for Pro/Agency?"
**Skill does**: Explains the **Free** tier already includes unlimited light plans plus a small number of full
plans per month (commonly cited as 3) with financial forecasts, a pitch deck, market research, the AI
Assistant, and Radar — so for a single plan it's usually enough. Notes **Pro** raises limits (price quoted
inconsistently — verify on site) and **Agency** is the **many-plans-per-month** tier for consultants, and that
**LLC Formation** is a separate annual fee. Presents all figures as best-effort and points to
venturekit.ai/pricing.
**Result**: The user picks the free tier for a one-off plan instead of over-buying.

## Troubleshooting

### "My VentureKit plan reads generic — it could describe any business"
**Symptom**: The plan is vague and not specific to the idea.
**Cause**: A thin, one-line input — VentureKit generates over whatever you give it, so a short description
yields a short, cookie-cutter plan, and it can invent filler to reach length.
**Solution**: Feed a **detailed** description — target customer, the exact problem, how people solve it today,
the business model and pricing — then **edit the draft heavily** and replace the AI's placeholder numbers.
Still settle the go/no-go with a real demand test via `/sales-idea-validation`.

### "The financial projections look too good — will a lender trust them?"
**Symptom**: Clean, optimistic revenue/P&L projections the founder didn't enter.
**Cause**: The forecasts are **AI-generated estimates**, not grounded in the founder's real costs, pricing, or
traction — a bank/SBA underwriter will probe them.
**Solution**: Treat the forecast as a **template to overwrite** — plug in real unit economics, costs, and a
defensible growth assumption, and cite sources for market size. Keep VentureKit's structure; own the numbers.

### "I want to export or automate my plans and there's no API"
**Symptom**: Can't find developer docs or an export API.
**Cause**: VentureKit is **UI-only** — no public API, webhooks, Zapier/Make, or MCP is documented.
**Solution**: Export the plan manually as **PDF/print/share**. If programmatic generation is core to your
workflow, call an **LLM API directly** or choose a business-plan tool built for automation — don't build a
pipeline on VentureKit.
