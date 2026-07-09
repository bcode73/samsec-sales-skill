# Bizplanr Platform Reference

<!-- Best-effort from third-party sources + review sites (2026-07). The live site (bizplanr.ai) returned
403 to automated fetches at research time; details below are assembled from GetApp, Upmetrics' review page,
TripleAReview, and comparison listicles. Verify pricing and free-export formats against the live site. -->

## Overview

Bizplanr (**bizplanr.ai**) is a **free AI business-plan generator**: a short questionnaire → a full,
structured plan in about five minutes. It targets first-time founders, solopreneurs, freelancers, and
small-business owners who want a fast, good-enough first draft without a subscription. Its differentiator vs
the paid-first cluster (VentureKit, Upmetrics, LivePlan) is that **the core generator and PDF download are
free with no credit card**, monetized by a **one-time** paid workspace rather than a recurring plan.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Questionnaire plan generator | Guided, context-aware questions → executive summary, market analysis, marketing strategy, operations, basic financials (~5 min) | UI-only |
| AI business advisor | Chat to refine, rewrite, or expand any section | UI-only |
| Guided section-by-section builder | Structured editor with in-context AI assistants for deeper control over organization | UI-only (paid workspace) |
| SWOT generator | Standalone SWOT analysis | UI-only |
| Competitor analysis generator | Standalone competitor breakdown | UI-only |
| Financial model generator | Standalone basic financial model | UI-only |
| One-page plan generator | Condensed single-page plan | UI-only |
| Sample plans library | Browsable example plans by industry | UI-only |
| Mobile apps (iOS + Android) | Draft, edit, or review plans from a phone | UI-only |

**Note:** the standalone generators run **independently** — their outputs do not cross-reference the main
plan, so numbers/claims must be reconciled by hand.

## Pricing, limits & plan gates

Best-effort at research (2026-07) — **verify at bizplanr.ai/pricing**; sources disagree on free-export scope.

| Tier | Price | Includes | Key limits |
|---|---|---|---|
| **Free** | $0, no credit card | Full AI-generated plan, sample plans, basic financials (simplified P&L / cash flow), basic pitch deck, **PDF export** | Basic forecasting only; limited formatting control; **PDF-only export** (per most reviews); collaboration not included |
| **Paid workspace** | **~$99 one-time (lifetime)** | Full guided editor + AI assistant, **advanced financial forecasting** (granular line-item drivers, scenario adjustments), **Word/Excel export**, greater pitch-deck customization, collaboration | No scenario planning beyond the paid drivers; no forecasts past ~5 years |

- **One-time, not a subscription** — a distinguishing trait vs Plannit/Upmetrics/VentureKit's recurring
  models. Reviewers describe it as "completely free to use" with a single optional $99 unlock.
- The free tier is designed to let a user **finish a full draft without being pushed to upgrade**.
- No documented rate limits (no API to rate-limit).

## Integrations

- **No public API, no webhooks, no Zapier/Make, no MCP.** Bizplanr is a web + mobile app; there is no
  documented programmatic interface.
- **Export is the only data-out path:** manual download — **PDF** on the free tier; **Word and Excel** on the
  paid workspace (some sources also cite PowerPoint). No live CRM/accounting sync.
- To automate plan generation, **call an LLM API directly** rather than building on Bizplanr.

## Data model

Bizplanr exposes no API, so there is no queryable data model. Conceptually a **plan** is a document composed
of sections; the shape below is illustrative for anyone modeling exported content — it is **not** an API
response.

```json
// Illustrative only — Bizplanr has no API. Represents a generated plan's structure.
{
  "plan": {
    "title": "Acme Cold-Brew Subscription",
    "sections": {
      "executive_summary": "…",
      "market_analysis": "…",
      "marketing_strategy": "…",
      "operations": "…",
      "financials": {
        "profit_and_loss": [ { "year": 1, "revenue": 0, "expenses": 0, "net": 0 } ],
        "cash_flow": [ { "month": 1, "inflow": 0, "outflow": 0 } ]
      }
    },
    "export_formats": ["pdf"]        // "docx","xlsx" unlock on the paid workspace
  }
}
```
<!-- Constructed for illustration — Bizplanr has no public API to verify against. -->

## Quick-start recipes

Bizplanr has no API, so there are no request/response recipes. The practical "recipes" are workflow patterns.

### Recipe 1 — Get a specific (not generic) first draft
1. Write a **rich** idea statement before starting: exact customer, the specific problem, how it's solved
   today, business model, pricing, and any traction.
2. Run the questionnaire; paste the rich statement into the free-text fields rather than a one-liner.
3. Use the **AI business advisor** to expand the competitive and operations sections (thinnest by default).
4. **Manually reconcile** the standalone financial-model/SWOT outputs with the plan's financials.
5. Replace every AI projection with real unit economics; cite sources for market size.

### Recipe 2 — Programmatic plan generation (the API workaround)
Since there's no Bizplanr API, generate structured plans with an LLM directly:

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
      "content": "Write a structured business plan (executive summary, market analysis, marketing strategy, operations, basic P&L) for: <rich idea statement>. Return JSON with a section per key."
    }]
  }'
```

```python
import anthropic, json
client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4000,
    messages=[{"role": "user", "content":
        "Write a structured business plan (executive summary, market analysis, marketing strategy, "
        "operations, basic P&L) for: <rich idea statement>. Return JSON with a section per key."}],
)
plan = resp.content[0].text
print(plan)
```
Gotcha: an LLM-generated plan has the **same "financials are estimates" caveat** as Bizplanr — overwrite the
numbers with real ones.

### Recipe 3 — Free vs paid decision
- Need **one basic plan + a PDF** to think through an idea → **free tier** is enough.
- Need **editable Word/Excel export**, the **guided section editor**, **advanced forecasting**, or
  **collaboration** → the **one-time paid workspace**.
- Need **multi-year scenario forecasting, plan-vs-actuals, or accounting sync** → Bizplanr won't do it; look
  at Upmetrics/LivePlan (see `/sales-idea-validation`).

## Integration patterns

There is no integration surface (no API/webhooks/iPaaS). The only supported data flow is a **manual export**
(PDF free; Word/Excel paid). For any pipeline that needs generated plans as structured data, replace Bizplanr
with a direct LLM call (Recipe 2) and treat the output as a draft to edit, not a source of truth.

## Namesake disambiguation

- **bizplanr.ai** — *this* tool: free AI business-plan generator + a **one-time** paid workspace.
- **bizplanner.ai** ("BizPlanner AI") — a **separate** product with a **subscription** model and a **30%
  affiliate** program. Reviews and pricing do **not** transfer.
- **bizplanaipro.com** ("BizPlan AI Pro", `/sales-bizplanaipro`) — another separate tool: a **credit-based,
  pay-per-use** generator (credit packs that never expire) bundling a Startup Idea Validator, an AI Business
  Coach, and AI Decision Analysis. Reviews and pricing do **not** transfer.

Always confirm the exact domain before quoting pricing or features.
