# VentureKit Platform Reference

<!-- Best-effort from research (2026-07). VentureKit's tiers, plan limits, module names, and the LLC
Formation service move; verify at venturekit.ai and venturekit.ai/pricing before relying on specifics. -->

## Overview

VentureKit (venturekit.ai) is **AI business-planning software** aimed at first-time founders and
small-business owners who need a **lender-/SBA-ready business plan fast**. You describe a business and it
generates a full plan, editable financial forecasts, a pitch deck, market research, an always-on AI business
assistant, and a Radar monitor — and it can separately handle **LLC formation & compliance**. Its
differentiator vs the idea-validator cluster is the **funding-document angle** plus a **generous free tier**
and an **Agency tier for consultants**. Founded by Dawson Whitfield (also Looka). It is **UI-only** — there is
no public API. Naming note: **venturekit.ai** is this tool; **venturekit.com** is an unrelated product.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Business Plan generator** | Turns a description into a full, multi-section plan (~28 pages): summary, market, product, operations, team, financial narrative. "Light" (preview) plans are unlimited; "full" plans are metered per tier. | **UI-only** |
| **Financial Forecasting** | Auto-generates revenue, expenses, P&L, and balance-sheet projections with **editable** tables ("lender-ready statements"). | **UI-only** (edit in-app) |
| **Pitch Deck creator** | Generates an investor pitch deck with "dozens of designer themes." | **UI-only** |
| **Market Research** | Generates a market/industry research report for the plan. | **UI-only** |
| **AI Business Assistant** | Always-on chat "business consultant" for questions and revisions. | **UI-only** |
| **Radar** | Monitoring/analytics tool surfaced in-app. | **UI-only** |
| **Guides / Perks** | Educational content and a partner-perks program. | **UI-only** |
| **LLC Formation & Compliance** | Separate paid service: articles of organization, EIN acquisition, operating agreement, registered-agent service, and state filings. | **UI-only / done-for-you service** |

**Bottom line for developers:** every module is UI-only. There is **no public API, no webhooks, no
Zapier/Make connectors, and no MCP server**. The only export is the plan itself (PDF / print / share link),
done manually.

## Pricing, limits & plan gates

*All figures best-effort — sources disagree (notably on the Pro price); confirm at venturekit.ai/pricing.*

| Tier | Price (best-effort) | Key limits / what you get |
|---|---|---|
| **Free** | $0 (free forever) | Unlimited **light** business plans; a small number of **full** plans per month (commonly cited as **3**); lender-ready statements, financial forecasts, pitch decks; market research; AI Assistant; Radar; guides + support. |
| **Pro** | ~$8/mo billed annually (**some sources quote ~$16/mo** — verify) | Everything in Free with higher limits; cancel anytime. |
| **Agency** | ~$38/mo | For consultants: **~20 full business plans per month**. |
| **Formation** (LLC service) | **$169/year** + state filing fees | Operating agreement, EIN, compliance tools; ~1 business day processing (excl. state processing); 100% accuracy guarantee. |
| **Registered Agent** (add-on) | **+$199/year** | Optional registered-agent service. |

**Will my integration break on the free plan?** There is no integration to break — the product is UI-only on
every tier, including paid. Nothing exposes an API even on Agency.

## Integrations

- **No native CRM connectors, no Zapier/Make modules, no public API, no webhooks, no MCP.**
- Data flow is **one-directional and manual**: input a description in-app → generate → export the plan as
  **PDF / print / share link**. There is no documented programmatic read or write.
- If you need the plan content elsewhere, copy from the export. If you need automated plan generation, use an
  **LLM API directly** (you own the prompt and the data) or a business-plan tool built for automation.

## Data model

VentureKit does not publish a data model or API, so there are no documented object shapes, IDs, or query
patterns. The user-facing objects are conceptually:

<!-- Constructed from the product's visible structure — VentureKit publishes no API/schema; illustrative only. -->
```json
{
  "plan": {
    "title": "Acme Coffee Roasters — Business Plan",
    "type": "full",                 // "light" (unlimited) | "full" (metered per tier)
    "sections": ["executive_summary", "market_analysis", "product", "operations", "team", "financials"],
    "financials": {
      "revenue_projection": [],     // AI-generated, editable — replace with your real numbers
      "expenses": [],
      "profit_and_loss": {},
      "balance_sheet": {}
    },
    "pitch_deck": { "theme": "designer-theme-name", "slides": [] },
    "market_research": {}
  }
}
```

Treat the `financials` block as an **editable template to overwrite**, not as data to trust.

## Quick-start recipes

VentureKit has **no API**, so there is no code recipe against VentureKit itself. The realistic automation
recipes are (a) exporting manually and (b) replacing VentureKit's generation with a direct LLM call when you
need it programmatic.

### Recipe 1 — Export a VentureKit plan for use elsewhere (manual)

1. Generate the full plan in-app (feed a rich description — see "Getting non-generic output" below).
2. Edit the financials: replace AI projections with your real costs, pricing, and growth assumptions.
3. Export via **PDF / print / share link** (there is no export API).
4. If you need the text in a repo/CRM, copy from the PDF — there is no programmatic pull.

### Recipe 2 — Generate a business-plan draft programmatically (bypass VentureKit's no-API limit)

Because VentureKit can't be scripted, do the generation yourself with an LLM API when you need it in a
pipeline. Illustrative, not VentureKit's API:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 4096,
    "messages": [{"role":"user","content":"Write a lender-ready business plan (exec summary, market, product, operations, team, financial narrative) for: <detailed business description with target customer, problem, business model, pricing>. Use only figures I provide; flag any assumption you invent."}]
  }'
```

```python
import anthropic

client = anthropic.Anthropic()
prompt = (
    "Write a lender-ready business plan (exec summary, market, product, operations, "
    "team, financial narrative) for: <detailed business description>. "
    "Use only figures I provide; flag any assumption you invent so I can replace it."
)
msg = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}],
)
print(msg.content[0].text)
```

**Gotcha:** whether you use VentureKit or a direct LLM call, the model will invent financials unless you
constrain it. Always instruct it to flag invented numbers, then replace them with real ones.

### Getting non-generic output

The #1 quality complaint is generic, cookie-cutter plans — almost always caused by a thin one-line input.
Feed VentureKit a **detailed** description: the specific target customer, the exact problem, how people solve
it today, the business model, and pricing. Then edit the draft heavily and overwrite the placeholder numbers.

## Integration patterns

There is no supported integration pattern for VentureKit (no API/webhooks/iPaaS). If a workflow genuinely
needs business plans in a pipeline, the pattern is: **generate with a direct LLM API** (own the prompt and the
data), template the sections, and store the output yourself — then use VentureKit only for its UI polish
(pitch-deck themes, formatting) if at all. The one thing worth automating for a real go/no-go is the **demand
signal** (landing-page analytics + waitlist), not the plan — see `/sales-funnel` and `/sales-audience-growth`.
