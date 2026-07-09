# BizPlan AI Pro Platform Reference

<!-- Best-effort from the live site (bizplanaipro.com, tools.bizplanaipro.com) + Capterra (2026-07). The tool
has near-zero third-party reviews at research time and its pricing pages disagree with Capterra on the Starter
price; verify pack prices, credit counts, and seat limits against the live site. -->

## Overview

BizPlan AI Pro (**bizplanaipro.com**, by **S. Enterprise**) is a **credit-based, pay-per-use AI
business-plan generator**: a questionnaire → a full "investor-ready / lender-ready" plan (executive summary,
market analysis, competitive landscape, 5-year financial projections) across **150+ industry templates**. It
targets entrepreneurs, startups, and small-business owners who want a fast first draft without a subscription.
Its differentiators vs the free/one-time cluster are (1) a **credit-pack model where credits never expire**
and (2) a **bundle of AI tools around the generator** — a Startup Idea Validator, an AI Business Coach, and an
AI Decision Analysis tool. A separate `tools.bizplanaipro.com` subdomain hosts free UI widgets (e.g. a free
business-plan generator). There is a regional `bizplanaipro.in` domain as well.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Questionnaire plan generator | Idea/industry/market input → executive summary, market analysis, competitive landscape, 5-year financial projections | UI-only |
| 150+ industry templates | Industry-specific plan scaffolds | UI-only |
| Startup Idea Validator | Tests idea "viability" against market data; returns a directional score/assessment | UI-only |
| AI Business Coach | Strategy chat (marketing/operations advice); metered by **Coach credits** | UI-only |
| AI Decision Analysis | Structured pros/cons/decision breakdown for a business choice | UI-only |
| 5-year financial projections | Revenue, cash-flow, break-even estimates calibrated to industry | UI-only |
| Real-time team collaboration | Multiple seats edit a plan together (seat count gated by pack) | UI-only |
| Free tools (`tools.bizplanaipro.com`) | Free standalone widgets (e.g. business-plan generator) | UI-only |

**Note:** the bundled Idea Validator, Coach, and Decision Analysis are **AI opinions** — directional, not
evidence of demand. Keep their structured output (competitors, risks) and discard the verdict.

## Pricing, limits & plan gates

Best-effort at research (2026-07) — **verify at bizplanaipro.com**; the homepage and Capterra disagree on the
Starter price, so treat all figures as unsettled.

| Tier | Price (best-effort) | Includes | Key limits |
|---|---|---|---|
| **Starter** | ~$2.99 one-time (Capterra lists ~$30) | ~1 plan generation | Single plan; no/low AI Coach credits; no team seats |
| **Professional** | ~$15 one-time | ~5 plan generations, ~50 AI Coach credits, 3 team members | Coach credits separate from plan credits |
| **Enterprise** | ~$39 one-time | ~15 plan generations, ~150 AI Coach credits, 10 team members | Still credit-metered — heavy iteration can exhaust it |

- **Credit-based, pay-per-use, no subscription — credits never expire.** This is the distinguishing trait vs
  Bizplanr (free + a one-time $99 workspace) and BizPlanner AI (one-time $9.99 + AI-word top-ups).
- **Two separate meters:** a **plan generation** consumes a **plan credit**; the **AI Business Coach**
  consumes **Coach credits**. Budget both.
- A founder typically **re-generates the same plan 3–6× as the idea pivots**, so a 1-plan Starter pack rarely
  covers an iterating idea — size the pack to your expected re-run count.
- No documented rate limits (no API to rate-limit).

## Integrations

- **No public API, no webhooks, no Zapier/Make, no MCP.** BizPlan AI Pro is a web app; there is no documented
  programmatic interface. The `tools.bizplanaipro.com` free tools are UI widgets, not an API.
- **Export is the only data-out path:** manual download of the generated plan. No live CRM/accounting sync.
- To automate plan generation, **call an LLM API directly** rather than building on BizPlan AI Pro.

## Data model

BizPlan AI Pro exposes no API, so there is no queryable data model. Conceptually a **plan** is a document
composed of sections; the shape below is illustrative for anyone modeling exported content — it is **not** an
API response.

```json
// Illustrative only — BizPlan AI Pro has no API. Represents a generated plan's structure.
{
  "plan": {
    "title": "Acme Cold-Brew Subscription",
    "template": "food-and-beverage",
    "sections": {
      "executive_summary": "…",
      "market_analysis": "…",
      "competitive_landscape": "…",
      "financials": {
        "profit_and_loss": [ { "year": 1, "revenue": 0, "expenses": 0, "net": 0 } ],
        "cash_flow": [ { "year": 1, "inflow": 0, "outflow": 0 } ],
        "break_even": { "months": 0 }
      }
    },
    "idea_validator": { "score": 0, "note": "AI opinion, not demand" }
  },
  "credits": { "plan_credits": 5, "coach_credits": 50 }   // two separate meters
}
```
<!-- Constructed for illustration — BizPlan AI Pro has no public API to verify against. -->

## Quick-start recipes

BizPlan AI Pro has no API, so there are no request/response recipes. The practical "recipes" are workflow
patterns.

### Recipe 1 — Get a specific (not generic) first draft, without burning credits
1. Write a **rich** idea statement before starting: exact customer, the specific problem, how it's solved
   today, business model, pricing, and any traction.
2. Pick the closest of the **150+ industry templates**; paste the rich statement into the free-text fields
   rather than a one-liner.
3. **Hand-edit** the competitive and operations sections (thinnest by default) instead of **re-generating**
   (a re-generation burns another **plan credit**).
4. Use the **AI Business Coach** sparingly — it draws on separate **Coach credits**.
5. Replace every AI projection with real unit economics; cite sources for market size.

### Recipe 2 — Programmatic plan generation (the API workaround)
Since there's no BizPlan AI Pro API, generate structured plans with an LLM directly:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 4000,
    "messages": [{
      "role": "user",
      "content": "Write a structured business plan (executive summary, market analysis, competitive landscape, 5-year P&L) for: <rich idea statement>. Return JSON with a section per key."
    }]
  }'
```

```python
import anthropic
client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4000,
    messages=[{"role": "user", "content":
        "Write a structured business plan (executive summary, market analysis, competitive landscape, "
        "5-year P&L) for: <rich idea statement>. Return JSON with a section per key."}],
)
print(resp.content[0].text)
```
Gotcha: an LLM-generated plan has the **same "financials are estimates" caveat** as BizPlan AI Pro — overwrite
the numbers with real ones.

### Recipe 3 — Which credit pack to buy
- Testing **one idea, one plan** → **Starter** is enough (but confirm it's really 1 plan credit at the live price).
- Expect to **iterate a plan across pivots** or need **AI Coach chat + team seats** → **Professional** (~5 plans
  + ~50 Coach credits + 3 seats).
- Running **many ideas or a heavy iteration cycle** → **Enterprise** (~15 plans + ~150 Coach credits + 10 seats).
- Need **multi-year scenario forecasting, plan-vs-actuals, or accounting sync** → BizPlan AI Pro won't do it;
  look at Upmetrics/LivePlan (see `/sales-idea-validation`).

## Integration patterns

There is no integration surface (no API/webhooks/iPaaS). The only supported data flow is a **manual export**.
For any pipeline that needs generated plans as structured data, replace BizPlan AI Pro with a direct LLM call
(Recipe 2) and treat the output as a draft to edit, not a source of truth.

## Namesake disambiguation

- **bizplanaipro.com** ("BizPlan AI Pro") — *this* tool: **credit packs** (never expire) + a bundled **AI
  Business Coach**, **Startup Idea Validator**, and **AI Decision Analysis**.
- **bizplanr.ai** ("Bizplanr", `/sales-bizplanr`) — a **free** AI business-plan generator with standalone
  SWOT/competitor tools, iOS/Android apps, and a **one-time paid workspace**.
- **bizplanner.ai** ("BizPlanner AI", `/sales-bizplanner`) — a **paid** generator with **no free tier**, a
  one-time payment + **AI-word top-ups**, and a **30% affiliate** program.

Reliable tells: **credit packs + AI Coach + Idea Validator** = BizPlan AI Pro; **free + mobile apps** =
Bizplanr; **no free tier + 30% affiliate + AI-word top-ups** = BizPlanner AI. Always confirm the exact domain
before quoting pricing or features.

## Marketing-claim caveats

The site advertises "**97% financial accuracy**," "**$8M+ raised** with plans," and "**15,000+ plans
analyzed**." These are **unverifiable vendor claims**, not a warranty on the user's numbers — the generated
financials are AI estimates like any other tool in this class. Do not repeat the accuracy figure as fact;
replace projections with real numbers before a lender or investor sees them.
