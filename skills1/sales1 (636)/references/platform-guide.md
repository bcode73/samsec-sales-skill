# Upmetrics Platform Reference

<!-- Best-effort from research (2026-07). Pricing, tiers, and integration behavior move — verify at upmetrics.co/pricing. -->

## Overview

Upmetrics (**upmetrics.co**) is an established AI business-planning suite for founders, consultants, and
advisors — an AI Assistant that drafts and rewrites plan sections, deep multi-year financial forecasting,
plan-vs-actuals tracking, a pitch-deck generator, strategic canvases, and real-time collaborative
workspaces. Its differentiator vs the AI-first generators (VentureKit, Plannit) is a **mature,
team-oriented suite** with accounting sync, forecast-vs-actuals tracking, and a **Professional/white-label**
tier for consultants managing many client plans.

> **Namesake collision:** upmetrics.**co** = this business-planning tool. upmetrics.**com** = an unrelated
> nonprofit impact/ESG-reporting platform (different company). Do not merge their features or docs.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **AI Assistant** (Writing / Financial / Research Assist) | Drafts and rewrites plan sections, suggests financial assumptions, pulls industry/market context; multilingual (90+ languages) | UI-only |
| **Business-plan builder** | Guided sections — executive summary, company/market analysis, operations, strategy; 400+ sample plans and industry templates | UI-only |
| **Financial forecasting** | Automatic P&L, cash-flow, break-even, and scenario testing over **3- and 7-year** horizons; startup-cost and funding-requirement modeling | UI-only |
| **Plan-vs-actuals tracking** | Live comparison of forecasts against actual results (fed by accounting imports/manual entry) | UI-only; data in via QuickBooks/Xero import |
| **Pitch-deck generator** | One-click deck from the approved plan | UI-only |
| **Strategic canvases** | Lean Canvas, Business Model Canvas, SWOT, OKR/KPI tracking | UI-only |
| **Collaborative workspaces** | Real-time multi-user editing, comments, feedback | UI-only |
| **Client management / white-label** (Professional) | Manage many client plans, custom templates, workspace transfer, optional white-label | UI-only |

**No module is API-accessible or webhook-accessible.** The entire product is UI-only.

## Pricing, limits & plan gates

*Best-effort — sources disagree on exact figures (starting quotes range from ~$7 to ~$19/mo); confirm at upmetrics.co/pricing. 15-day money-back guarantee.*

| Tier | Roughly includes | Notes |
|---|---|---|
| **Starter** | Single workspace, 400+ sample plans, up to 7-year forecasting, unlimited AI writing (incl. 90+-language translation, refinement, industry research), QuickBooks Online + Xero | Entry tier — enough for one founder writing one plan |
| **Premium** | More capacity/features on top of Starter | Mid tier |
| **Professional** | Client management, custom template creation, workspace transfer, **optional white-label** (quoted ~$185/mo annual) | Built for consultants/advisors managing many client plans |

**Will my integration break on the entry plan?** There's no API to break — the product is UI-only on every
tier. The only "API/white-label" path is a **custom, sales-gated arrangement** for advisors/accelerators,
undocumented and not self-serve.

## Integrations

Focus is data flow *in*, not out:

- **QuickBooks Online** and **Xero** — **one-way import** of accounting data into forecasts/actuals. Despite
  "live sync" marketing, reviewers report it is **not real-time and not bidirectional** — plan periodic
  manual refreshes.
- Marketing/help pages also reference **Stripe**, **Chargebee**, and **Looker Studio** connectors (verify
  scope and direction in-app).
- **No Zapier / Make / n8n triggers or actions, no webhooks, no MCP server** were found.

## Data model

Upmetrics does not expose a public data model or API. There is **no documented object schema, no
endpoints, and no example payloads** to copy. Practically, the user's data lives in three shapes inside the
app, all edited and exported through the UI only:

- **Plan** — sectioned document (executive summary, market analysis, operations, strategy).
- **Forecast** — multi-year financial model (P&L, cash-flow, break-even, scenarios); actuals compared
  against it via **plan-vs-actuals**.
- **Pitch deck** — generated from the approved plan.

<!-- No public API — no JSON object shapes exist to document. Any programmatic representation would have to be constructed and could not be verified against a live API, so none is provided. -->

## Quick-start recipes

Upmetrics is **UI-only**, so the "recipes" are UI/export workflows plus the correct automation alternative.

### Recipe 1 — Generate a first-draft plan and de-genericize it
1. In the app, start a plan, pick the closest **sample plan / industry template**.
2. Feed the **AI Assistant a rich prompt** — exact customer, the specific problem, how it's solved today,
   business model, pricing. (Thin input is the #1 cause of generic output.)
3. Generate, then **rewrite the competitive overview, operations, and revenue sections by hand** for your
   niche — the model has thin depth there.
4. **Export a PDF/DOC snapshot before major edits** (data-loss safeguard).

### Recipe 2 — Build a forecast and track plan-vs-actuals
1. Build the **financial forecast** (P&L, cash-flow, break-even) over a 3- or 7-year horizon.
2. Connect **QuickBooks Online or Xero** to import actuals — treat this as a **periodic manual import**, not
   a live feed.
3. Use **plan-vs-actuals** to compare, and reconcile against your accounting system as the source of truth.
4. **Replace AI-suggested assumptions with your real unit economics** before sharing with a lender/investor.

### Recipe 3 — Automate plan generation (there is no Upmetrics API — do this instead)
There is **no public API** to script Upmetrics. If you need programmatic plan generation:

```bash
# Call an LLM API directly instead of building on a nonexistent Upmetrics API.
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 4000,
    "messages": [{
      "role": "user",
      "content": "Write a business plan section (market analysis) for: <rich idea description here>."
    }]
  }'
```

```python
# Python equivalent
import anthropic
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
msg = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4000,
    messages=[{"role": "user",
               "content": "Write a business plan section (market analysis) for: <rich idea description>."}],
)
print(msg.content[0].text)
```

The only Upmetrics export is the **plan PDF/DOC** downloaded manually from the UI.

## Integration patterns

- **Getting data OUT:** manual **PDF/DOC export** of the plan is the only path. There is no API, feed, or
  webhook — a pipeline that needs structured plan data cannot read it programmatically.
- **Getting actuals IN:** QuickBooks/Xero **one-way import** on a refresh cadence; do not architect around
  real-time two-way sync.
- **Automating generation:** call an **LLM API directly** (see Recipe 3); Upmetrics offers no programmatic
  generation surface.
- **Consultant/agency use:** the **Professional/white-label** tier is the "many client plans" path — it's a
  UI/account feature, not an API. Evaluate it against the volume you handle, not against automation needs.
