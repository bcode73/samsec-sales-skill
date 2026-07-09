# Plannit AI (AIGenerator.com) Platform Reference

<!-- Best-effort from research (2026-07). Plannit AI rebranded to AIGenerator.com (AIGenerator LLC); tiers,
the pricing model, module names, and the live site's reachability move. The live site's TLS certificate was
EXPIRED at research time and direct fetches failed — this reference is assembled from third-party sources
(Upmetrics, AIChief, Trustpilot, Capterra, comparison articles). Verify specifics at aigenerator.com before
relying on them. -->

## Overview

Plannit AI — now branded **AIGenerator.com** (both operated by **AIGenerator LLC**) — is an **AI business-plan
generator** for first-time founders, small-business owners, freelancers, side-hustlers, students, and
consultants. You answer a **short questionnaire** and it produces a **15–20 page business plan** in ~2 minutes.
It's powered by **GPT-4** under the hood and is **UI-only** (no public API). Its differentiators vs the
business-plan/validator cluster are **real-time team collaboration**, a broad **AIGenerator marketing-asset
suite** bolted onto the planner, and **150+ language** support.

**Naming / disambiguation:**
- **plannit.ai** now redirects to / serves **AIGenerator.com** — same company, rebranded.
- **plannit.io** is a **different, unrelated product** (a home/property/field-services management app). Reviews
  and help docs across the two domains do **not** transfer.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Business Plan generator** | Questionnaire (~5–7 questions: product, target market, revenue model, competitive edge, operations) → a **15–20 page** multi-section plan (executive summary, market analysis, product, operations, financial narrative), fully editable. | **UI-only** |
| **Financial Projections** | Auto-generates revenue/expense/financial projections. **Lowest-rated module** — forecasting reads generic and revenue-stream ideas can be unrelated; editable. | **UI-only** (edit in-app) |
| **Pitch Deck** | Generates an investor-facing pitch deck from the plan. | **UI-only** |
| **Executive Summary** | A free customized executive summary is offered even without buying a full plan. | **UI-only** |
| **Market Analysis** | Competition, target-audience, and industry-trend analysis for the plan. | **UI-only** |
| **Marketing Assets (AIGenerator suite)** | Ad copy, email campaigns, social-media strategy, content calendars, and a **domain-name generator**. | **UI-only** |
| **AI Business Assistant** | An in-app AI "business consultant" for iterative feedback and revisions. | **UI-only** |
| **Team Collaboration** | Invite team members to **comment, edit, and share** a plan in real time — a differentiator vs VentureKit (which has none). | **UI-only** |
| **Templates & Samples** | A limited gallery of sample plans across industries (food/beverage, tech, nonprofit, wellness) + educational content. | **UI-only** |

**Bottom line for developers:** every module is UI-only. There is **no public API, no webhooks, no
Zapier/Make connectors, and no MCP server**. The only export is the plan itself (download to a standard office
format / share), done manually. The GPT-4 that powers it is an internal dependency, not a developer surface.

## Pricing, limits & plan gates

*All figures best-effort — the product rebranded and sources disagree; the live site's cert was expired at
research time. Confirm at aigenerator.com.*

The pricing **model changed with the rebrand**:

| Era / Tier | Price (best-effort) | What you get |
|---|---|---|
| **Old — Plannit AI Free** | $0 | A free customized **executive summary** for your business (no full plan). |
| **Old — Plannit AI Pro** | **$39.99 one-time per plan** (lifetime access to that plan) | One full 15–20 page plan; **5-plan and 10-plan bundles** available; no subscription. |
| **Old — Plannit AI Enterprise** | Custom quote | For >10 plans. |
| **New — AIGenerator Free** | $0 | Basic business plan + financials, marketing-asset samples, the ~5-question guided setup. |
| **New — AIGenerator Pro** | **~$19 / month** (verify) | Full strategy docs, advanced financial projections, **unlimited exports**, priority support. |
| **New — AIGenerator Enterprise** | Custom quote | Higher volume / advanced needs. |

**Will my integration break on the free plan?** There is no integration to break — the product is **UI-only on
every tier**, free or paid. Nothing exposes an API. **If the user needs just one plan, the free tier (or a
single one-time plan) is usually enough** — the paid plan buys volume/advanced financials/exports, not an API.

## Integrations

- **No native CRM connectors, no Zapier/Make modules, no public API, no webhooks, no MCP.**
- Data flow is **one-directional and manual**: fill the questionnaire in-app → generate → **download** the plan
  to a standard office format (or share it) → optionally collaborate with invited teammates in-app.
- If you need the plan content elsewhere, copy from the export. For **automated** plan generation, call an
  **LLM API directly** (you own the prompt and the data) — don't build a pipeline on Plannit/AIGenerator.

## Data model

Plannit / AIGenerator does not publish a data model or API, so there are no documented object shapes, IDs, or
query patterns. The user-facing objects are conceptually:

<!-- Constructed from the product's visible structure — Plannit/AIGenerator publishes no API/schema; illustrative only. -->
```json
{
  "plan": {
    "title": "Acme Coffee Roasters — Business Plan",
    "language": "en",                 // 150+ languages supported
    "questionnaire": {
      "product": "...",
      "target_market": "...",
      "revenue_model": "...",
      "competitive_edge": "...",
      "operations": "..."
    },
    "sections": ["executive_summary", "market_analysis", "product", "operations", "financials"],
    "financials": {
      "revenue_projection": [],       // AI-generated, editable — weakest module, replace with real numbers
      "expenses": [],
      "notes": "AI estimate — overwrite before showing an investor/lender"
    },
    "pitch_deck": { "slides": [] },
    "collaborators": []               // real-time comment/edit/share (differentiator)
  }
}
```

Treat the `financials` block as an **editable template to overwrite**, not as data to trust.

## Quick-start recipes

Plannit / AIGenerator has **no API**, so there is no code recipe against the product itself. The realistic
automation recipes are (a) getting non-generic output from the UI and (b) replacing its generation with a
direct LLM call when you need it programmatic.

### Recipe 1 — Get a non-generic, niche-ready plan out of the UI (manual)

1. Don't feed a one-liner. Write a **detailed** description: exact target customer, the specific problem, how
   it's solved today, the business model, and pricing.
2. Generate the plan; then **edit heavily** — the draft is a starting point, especially for niche industries.
3. **Replace the financial projections** with your real costs, pricing, and a defensible growth assumption
   (the forecasting module is the weakest part). Cite sources for market size.
4. Export by **downloading to a standard office format** (there is no export API) and keep your own copy.
5. Invite collaborators in-app if teammates/advisors need to comment or edit.

### Recipe 2 — Generate a business-plan draft programmatically (bypass the no-API limit)

Because Plannit/AIGenerator can't be scripted, do the generation yourself with an LLM API when you need it in a
pipeline. Illustrative — this is a direct LLM call, **not** Plannit's API:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 4096,
    "messages": [{"role":"user","content":"Write a 15-20 page business plan (executive summary, market analysis, product, operations, financial narrative) for: <detailed business description with target customer, problem, business model, pricing>. Use only figures I provide; flag any assumption you invent so I can replace it."}]
  }'
```

```python
import anthropic

client = anthropic.Anthropic()
prompt = (
    "Write a 15-20 page business plan (executive summary, market analysis, product, "
    "operations, financial narrative) for: <detailed business description>. "
    "Use only figures I provide; flag any assumption you invent so I can replace it."
)
msg = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}],
)
print(msg.content[0].text)
```

**Gotcha:** whether you use Plannit or a direct LLM call, the model will invent financials unless you constrain
it. Always instruct it to flag invented numbers, then replace them with real ones.

## Integration patterns

There is no supported integration pattern for Plannit/AIGenerator (no API/webhooks/iPaaS). If a workflow needs
business plans in a pipeline, the pattern is: **generate with a direct LLM API** (own the prompt and data),
template the sections, store the output yourself, and use Plannit only for its UI polish and in-app
collaboration if at all. The one thing worth automating for a real go/no-go is the **demand signal**
(landing-page analytics + waitlist), not the plan — see `/sales-funnel` and `/sales-audience-growth`.
