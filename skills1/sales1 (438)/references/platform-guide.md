# PrometAI Platform Reference

<!-- Best-effort from the live site (prometai.app, prometai.app/pricing) + third-party reviews
(Product Hunt, Trustpilot, Upmetrics/Venngage comparisons) on 2026-07-08. Pricing pages and reviews
disagree on exact tier prices and inclusions; verify plan counts, AI-request caps, export gates, and
DCF availability against the live site before relying on them. No public API exists to verify a data model
against. -->

## Overview

PrometAI (**prometai.app**) is an **AI business-plan generator and planning suite** aimed at founders,
first-time entrepreneurs, and small businesses (marketed as "100,000+ founders, 100+ industries"). A
questionnaire produces a **full plan** (executive summary, market analysis, strategy frameworks) in minutes
(the site claims an average ~1.6-minute first draft). Its differentiator vs the rest of the AI-plan cluster is
a **connected financial model**: projections, a **DCF valuation**, **stress testing**, and **scenario
analysis** that **recalculate together** when an input changes — reviewers single this out as the thing
PrometAI does better than most ("grounded, consistent, connected end-to-end"). Around the generator sits a
**50+ tool "Entrepreneur Journey"** (idea generation, branding, founder profiles, risk assessment, valuation,
scenario analysis). It's a **subscription** product (unlike the one-time/credit siblings), and it's **UI-only —
no public API**.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Questionnaire plan generator | Idea/industry/market input → executive summary, market analysis, plan sections | UI-only |
| Connected financial model | Financial projections + **DCF valuation** + **stress testing** + **scenario analysis** that recalculate together on input change | UI-only |
| Strategy frameworks | SWOT, VRIO (consultant-style analysis) baked into the plan | UI-only |
| "Entrepreneur Journey" (50+ tools) | Idea generation, branding, founder profiles, risk assessment, valuation, scenarios | UI-only |
| Financial dashboards | Visual financial summaries (paid tiers) | UI-only |
| NDA & term-sheet templates | Fundraising document templates (Pro) | UI-only |
| Translations | Translate a plan into other languages (Pro, ~10) | UI-only |
| Export | PDF (Basic+), PowerPoint (Pro); free Explore is **view-only, no export** | UI-only (manual download) |
| Enterprise: FP&A analytics + ERP integrations | Custom deployments, finance analytics, ERP connectors | **Enterprise-only, sales-gated** (not a self-serve API) |

**Note:** the financial model, DCF valuation, and any built-in "score" are **AI estimates** — directional, not
evidence of demand or a real appraisal. Keep the structured output (competitor framing, SWOT/VRIO, the
recalculating model) and replace the numbers with real ones.

## Pricing, limits & plan gates

Best-effort at research (2026-07) — **verify at prometai.app/pricing**; reviews and the live page disagree, so
treat all figures as unsettled. Billing offers monthly / quarterly / annual, with steep annual discounts.

| Tier | Price (best-effort) | Includes | Key gates |
|---|---|---|---|
| **Explore (Free)** | $0 | 1 business plan, 25 AI requests/mo, 2 AI images/mo, core sections, **view-only link sharing** | **No export**; no financial dashboards; no DCF |
| **Application-Ready (Basic)** | ~$55/mo · ~$45 quarterly · ~$25 annual | 3 plans, 200 AI requests/mo, 20 AI images, **PDF export**, financial dashboards, currency selection | No PowerPoint; **no DCF/stress testing** |
| **Investor-Grade (Pro)** | ~$145/mo · ~$119 quarterly · ~$65 annual | 8 plans, 500 AI requests/mo, 50 HQ images, **PowerPoint export**, **DCF valuation & stress testing**, NDA & term-sheet templates, 10 translations | — |
| **Enterprise** | Custom ("contact sales") | AI planning, **FP&A analytics**, **ERP integrations**, tailored deployment, team support | Sales-gated; not a self-serve API |

- **Subscription, not one-time.** This is the key economic contrast with Bizplanr (free + one-time workspace),
  BizPlanner AI, and BizPlan AI Pro (credit packs) — PrometAI bills recurring, and Pro is on the pricey end.
- **The two gates that usually decide the tier:** (1) **can you export at all** — no on free, PDF on Basic,
  PowerPoint on Pro; (2) **do you need the DCF valuation / stress testing** — **Pro only**.
- **AI requests are metered per month** (25 / 200 / 500) — heavy iteration on a plan can exhaust the lower caps.
- No documented rate limits (no API to rate-limit).

## Integrations

- **No public API, no webhooks, no Zapier/Make, no MCP.** PrometAI is a web app; there is no documented
  self-serve programmatic interface.
- **The only data-out path is a manual export** — PDF (Basic+) or PowerPoint (Pro). No live CRM/accounting sync.
- **Enterprise "ERP integrations" + "FP&A analytics"** are **sales-gated custom deployments**, not a documented
  developer API. Don't plan a self-serve integration around them.
- To automate plan generation, **call an LLM API directly** rather than building on PrometAI.

## Data model

PrometAI exposes no API, so there is no queryable data model. Conceptually a **plan** is a document composed of
sections plus a connected financial model; the shape below is illustrative for anyone modeling exported content
— it is **not** an API response.

```json
// Illustrative only — PrometAI has no API. Represents a generated plan's structure.
{
  "plan": {
    "title": "Acme Cold-Brew Subscription",
    "industry": "food-and-beverage",
    "sections": {
      "executive_summary": "…",
      "market_analysis": "…",
      "swot": { "strengths": [], "weaknesses": [], "opportunities": [], "threats": [] },
      "vrio": { "value": "", "rarity": "", "imitability": "", "organization": "" }
    },
    "financials": {
      "projections": [ { "year": 1, "revenue": 0, "expenses": 0, "net": 0 } ],
      "dcf_valuation": { "discount_rate": 0.0, "terminal_value": 0, "enterprise_value": 0 },
      "stress_test": { "scenario": "downside", "revenue_delta": -0.3 },
      "note": "AI estimates — recalculate together, but replace with real numbers"
    }
  },
  "usage": { "ai_requests_remaining": 200, "plans_remaining": 3 }   // metered per tier
}
```
<!-- Constructed for illustration — PrometAI has no public API to verify against. -->

## Quick-start recipes

PrometAI has no API, so there are no request/response recipes. The practical "recipes" are workflow patterns.

### Recipe 1 — Get a specific (not generic) investor-grade draft
1. Write a **rich** idea statement first: exact customer, the specific problem, how it's solved today, business
   model, pricing, and any traction — a one-liner yields a cookie-cutter plan.
2. Generate the plan, then **hand-edit** the competitive and operations sections (thinnest by default).
3. In the **financial model**, replace the AI-guessed drivers with real numbers — projections, and especially
   the **DCF inputs** (discount rate, cash-flow forecast, terminal value). Because the model recalculates
   together, fixing the drivers propagates to the valuation and stress tests.
4. Watch the **monthly AI-request cap** (25 / 200 / 500) — prefer editing over re-generating whole sections.
5. Export on a paid tier (PDF on Basic, PowerPoint on Pro) and **re-check formatting** in the target app.

### Recipe 2 — Programmatic plan generation (the API workaround)
Since there's no PrometAI API, generate structured plans with an LLM directly:

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
      "content": "Write a structured business plan (executive summary, market analysis, SWOT, VRIO, 5-year P&L, and a DCF valuation with stated assumptions) for: <rich idea statement>. Return JSON with a section per key."
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
        "Write a structured business plan (executive summary, market analysis, SWOT, VRIO, 5-year P&L, "
        "and a DCF valuation with stated assumptions) for: <rich idea statement>. Return JSON with a "
        "section per key."}],
)
print(resp.content[0].text)
```
Gotcha: an LLM-generated plan (and DCF) has the **same "financials are estimates" caveat** as PrometAI —
overwrite the numbers with real ones, and treat the DCF as a modelling exercise, not an appraisal.

### Recipe 3 — Which tier to buy
- **Just trying it / one plan, no export needed** → **Explore (free)**, but note you **can't export** (view-only).
- **Need to export a plan (PDF) + financial dashboards** → **Application-Ready/Basic**.
- **Need the DCF valuation, stress testing, PowerPoint, or term-sheet templates for fundraising** → **Pro**.
- **Need FP&A analytics, ERP integration, or a tailored deployment** → **Enterprise** (sales-gated).
- **Only need one plan and hate recurring cost** → weigh a **one-time** sibling (Bizplanr / BizPlanner AI /
  BizPlan AI Pro, see `/sales-idea-validation`) against PrometAI's subscription.

## Integration patterns

There is no self-serve integration surface (no API/webhooks/iPaaS). The only supported data flow is a **manual
export** (PDF/PowerPoint). For any pipeline that needs generated plans as structured data, replace PrometAI with
a direct LLM call (Recipe 2) and treat the output as a draft to edit, not a source of truth. The Enterprise ERP
integrations are a **custom, sales-led** engagement, not something you can self-provision.

## Reviewer-noted strengths & limits

- **Strength — connected, end-to-end financials.** Reviewers consistently name PrometAI's financial model as its
  edge: DCF valuation + stress testing + scenario analysis that update automatically when inputs change, plus
  consultant-style SWOT/VRIO framing. Serious about investor-grade output.
- **Limit — invents market figures.** Testing surfaced **unverified market figures and vague report
  references**; verify every statistic and market claim independently.
- **Limit — moderate financial integrity for lenders.** Useful for early modelling, but limited exports and
  lighter reporting mean **most lenders still want a separate financial review**.
- **Limit — DCF isn't beginner-friendly.** Valuations require real understanding of the business inputs; the
  output is a model, not an appraisal.
- **Limit — exports lose formatting; collaboration is very limited (no real-time editing).** Re-check exported
  files and drive team plans from a single owner.

## Namesake / disambiguation

- **prometai.app** ("PrometAI", also written "Promet AI") is *this* tool. Confirm the domain before quoting
  pricing — the AI-business-plan cluster has many confusingly similar names (Bizplanr / BizPlanner AI / BizPlan
  AI Pro / Plannit, etc.). Don't cross-contaminate PrometAI's **subscription** pricing with the siblings'
  one-time/credit models.
