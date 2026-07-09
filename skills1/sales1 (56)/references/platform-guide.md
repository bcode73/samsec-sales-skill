# BizPlanner AI Platform Reference

<!-- Best-effort from research (2026-07). BizPlanner AI (bizplanner.ai) publishes no developer docs; pricing,
AI-word top-up sizes, and export formats change. Verify at bizplanner.ai. -->

## Overview

BizPlanner AI (**bizplanner.ai**) is a **paid, GPT-4-powered AI business-plan generator** for entrepreneurs and
small-business owners who want a professional first draft fast (~15 minutes) rather than writing one manually or
paying a freelancer. Its differentiator vs the free-first cluster (Bizplanr) is that it is **pay-once to generate**
(no free tier, no subscription), with a **word-metered top-up** model for additional AI generation. ~27,300+ users
cited on the site.

## Capabilities & automation surface

Every module below is **UI-only** — there is no public API, no webhooks, and no Zapier/Make/MCP surface.

| Capability | What it does | Automation |
|---|---|---|
| AI plan section generator | Generates every plan section from a short questionnaire | UI-only |
| Target-audience analysis | Describes the customer and their motivations | UI-only |
| Competitor analysis | Highlights competitor strengths/weaknesses | UI-only |
| SWOT analysis | Strengths, weaknesses, opportunities, threats | UI-only |
| Financial projections | Startup costs, revenue, profitability estimates | UI-only |
| Industry trends & statistics | Curated trend and stat context for the sector | UI-only |
| Relevant regulations | Overview of regulations that may apply | UI-only |
| Suggested next steps | Recommended actions after the plan | UI-only |
| In-browser editor | Edit any section in the browser | UI-only |
| Regenerate document | Re-run a section/plan (2 free, then AI-word top-ups) | UI-only |
| Export | Download the finished plan | UI-only (PDF / Word) |

## The plan structure

A generated plan typically includes these sections:

- Executive Summary
- Business Description
- Market Research & Analysis
- Competitor Analysis
- Organizational Structure
- Products / Services
- Marketing & Sales Strategy
- Operations Plan
- Financial Plan (projections: startup costs, revenue, profitability)
- Risk Analysis
- (plus target-audience analysis, SWOT, industry trends/stats, relevant regulations, suggested next steps)

## Pricing, limits & plan gates

Best-effort at research — **confirm at bizplanner.ai**. There is **no free tier** and **no subscription**.

- **One-time payment: ~$9.99** — generates a complete plan and includes **2 free full regenerations after edits**.
- **AI Words top-ups** — additional generation/rewriting is metered in "AI words" bought separately, commonly cited
  as **~$7.99 for 50,000 words** and **~$9.99 for 100,000 words**. Regenerating beyond the 2 free full
  regenerations draws on this balance.
- **30-day money-back guarantee** advertised.
- **Export**: PDF and Word (both included with the one-time payment).
- **Model**: uses GPT-4 for content generation.

**"Will my integration break on the free plan?"** — N/A; there is no API and no free plan. There is nothing to
integrate: the plan is produced and exported entirely in the UI.

## Affiliate program

BizPlanner AI runs a **30% commission** affiliate program (bizplanner.ai/affiliate):

- Affiliates get a **unique referral link** to share with their network.
- **30% commission** on each successful referred purchase.
- **Self-referrals are not permitted** (you can't buy through your own link).
- **Manipulation** — e.g. posting invalid discounts on coupon sites — leads to a **permanent ban**.

(This 30% affiliate is a reliable way to tell BizPlanner **AI** apart from the free **Bizplanr** — see below.)

## Integrations

None. No native CRM connectors, no Zapier triggers/actions, no Make modules, no webhooks, no MCP server. Data flow
is one-way and manual: you enter input in the UI and download a PDF/Word file. To move a plan anywhere else, copy
the exported document.

## Data model

Not applicable in an API sense — there are no exposed objects, IDs, or query endpoints. The only "object" a user
handles is the exported **plan document** (PDF or Word). For a programmatic equivalent, model your own plan schema
and generate sections against an LLM API. Illustrative shape you might build yourself:

<!-- Constructed illustration — BizPlanner AI exposes no API or data model; this is a suggested local schema. -->

```json
{
  "plan": {
    "executive_summary": "string",
    "business_description": "string",
    "market_analysis": "string",
    "competitor_analysis": [{ "name": "string", "strengths": "string", "weaknesses": "string" }],
    "swot": { "strengths": [], "weaknesses": [], "opportunities": [], "threats": [] },
    "financials": { "startup_costs": 0, "revenue_projection": [], "profitability": [] },
    "risk_analysis": "string"
  }
}
```

## Quick-start recipes

Because BizPlanner AI has no API, "automation" means replacing it with your own LLM call. These recipes show the
workable path.

### Recipe 1 — Generate a plan section programmatically (the API-less alternative)

BizPlanner AI can't be scripted, so call an LLM directly for the same output you'd regenerate in its UI.

cURL (Anthropic Messages API):

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 2000,
    "messages": [{
      "role": "user",
      "content": "Write the Market Research & Analysis section of a business plan for: <rich idea description with exact customer, problem, pricing, business model>. Be specific to the niche; do not invent market-size numbers — flag any figure that needs a real source."
    }]
  }'
```

Python:

```python
import anthropic

client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=2000,
    messages=[{
        "role": "user",
        "content": (
            "Write the Financial Plan section for: <rich idea description>. "
            "Return startup costs, a 12-month revenue projection, and a profitability estimate. "
            "Do NOT fabricate numbers — leave placeholders where I must supply real figures."
        ),
    }],
)
print(resp.content[0].text)
```

**Gotcha**: whether you use BizPlanner AI or your own LLM call, the financials are estimates — force placeholders
for anything that needs a real source rather than letting the model invent them.

### Recipe 2 — Get the most out of the 2 free regenerations

1. Draft a **rich input** first (exact customer, the specific problem, how it's solved today, business model,
   pricing, capacity) — thin input is the #1 cause of generic output and wasted regenerations.
2. Generate the plan once.
3. Read every section; identify the **1–2 weakest** (usually competitive, operations, or revenue).
4. Spend the **2 free full regenerations** only on those, or edit them by hand in the in-browser editor.
5. If you need more generation, buy an **AI-word top-up** — but prefer hand-editing numbers to burning words.

### Recipe 3 — Take the exported plan to a funder safely

1. Export to **Word** (editable) rather than PDF.
2. Replace every **projection, market-size, and unit-economics** figure with your own real numbers and **cite
   sources**.
3. Reconcile the **SWOT / competitor** sections against your real market knowledge — the model may list irrelevant
   competitors for a niche.
4. Remember a polished plan is a **document, not validated demand** — run a smoke test / pre-sale
   (`/sales-idea-validation`) before betting on it.

## Integration patterns

There is no supported integration surface. If you need plans inside a CRM, data warehouse, or product:

- **Generate with your own LLM API** (see Recipe 1) so you control schema, storage, and versioning.
- **Manual bridge**: export the Word file from BizPlanner AI and parse it downstream (e.g. `python-docx`) — brittle
  and unofficial; prefer generating your own structured JSON.
- **Do not** build against any "BizPlanner AI API" — none exists; a review claiming one has conflated the internal
  GPT integration with a developer API.
