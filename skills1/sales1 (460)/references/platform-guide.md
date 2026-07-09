# RebeccAi Platform Reference

<!-- Best-effort from research (2026-07). RebeccAi is a small solo-maker tool with no verified
third-party reviews; verify all pricing, caps, and plan contents at rebecc.ai. -->

## Overview

RebeccAi (**rebecc.ai**) is a low-cost AI **business-idea evaluator + one-off business-plan generator**
for solo founders, indie hackers, and first-time entrepreneurs. You paste an idea into a single text box
(with team size, budget, and a chosen "feedback personality"), and it returns a quick evaluation,
strengths/weaknesses, improvement suggestions, and — as a separate one-time purchase — a ready-to-use
~15–25 page business plan. Its edge is **price**; its weaknesses are that the evaluation is an AI opinion
you can tune to flatter you, and the plan's financials are AI estimates with no real market input.

> **Domain note:** the product lives at **rebecc.ai**. `rebeccai.com` is a parked/for-sale GoDaddy
> domain, not the product. Don't confuse the two.

## Capabilities & automation surface

| Module | What it does | Automation |
|---|---|---|
| **Quick Evaluation** | Reads a freeform idea description + context (personality, team size, budget) → a fast AI assessment of the idea's potential | **UI-only** |
| **Assessment (evaluation points)** | Structured breakdown of the idea's perceived strengths and weaknesses across its evaluation points | **UI-only** (all points require Premium; free tier is limited) |
| **Improve Your Idea** | Concrete AI suggestions to strengthen the concept — moves it from validator to ideation partner | **UI-only** |
| **Feedback Personality** | Input toggle that sets the tone/lens of the feedback (e.g. "conservative & traditional"); **biases the verdict** | **UI-only** |
| **Business Plan** | A separate one-time product — a ready-to-use ~15–25 page plan (editable, savable, generated "within seconds") | **UI-only**; exports as an editable/savable document only |

**There is no API, no webhooks, no Zapier/Make, and no MCP server.** Every module above is UI-only. The
only "export" is the business-plan document (edit / save / download).

## Pricing, limits & plan gates

*Best-effort — confirm at rebecc.ai/pricing. A small tool's tiers and intro pricing change often.*

| Plan | Price (best-effort) | What you get | Key limits |
|---|---|---|---|
| **Free** | Free | Evaluation points (limited), daily idea evaluations | ~**5 ideas/day**, **short per-point output** (~160 characters), **no customization** |
| **Premium** | Intro **~$5/mo for the first two months, then ~$19/mo** | **Unlimited** idea evaluations, **all evaluation points**, **500+ characters per point**, **customizable answers**, example report | Subscription; intro price steps up |
| **Business Plan** | **~$14.99 one-time** | A ready-to-use **~15–25 page** business plan, **edit + save**, generated "within seconds" | One-off per plan; separate from the subscription |

**Will my integration break on the free plan?** There is no integration surface at all (no API/webhooks),
so this question is moot — the free vs Premium difference is purely about idea volume, output length, and
customization inside the UI. The business plan is a separate one-time purchase regardless of tier.

## Integrations

**None documented.** No native CRM connectors, no Zapier/Make modules, no public API, no webhooks, no MCP
server. Data flow is one-directional and manual: you type an idea in, you read/copy the evaluation out,
and you can download the business-plan document. If you need RebeccAi's outputs elsewhere, copy them
manually (mind their terms).

## Data model

RebeccAi exposes **no API**, so there are no documented object schemas, IDs, or query patterns. The
conceptual objects a user works with:

<!-- Constructed from the product UI/positioning — RebeccAi has no public API; these are illustrative
shapes, not a real schema. Do not build against them. -->

```json
{
  "idea": {
    "description": "freeform text — the single-text-box input",
    "context": {
      "feedbackPersonality": "conservative & traditional",
      "teamSize": 1,
      "budget": "low"
    }
  },
  "evaluation": {
    "score": "AI-generated potential score (directional, not audited)",
    "evaluationPoints": [
      { "point": "market", "assessment": "strength/weakness text", "chars": "160 free / 500+ Premium" }
    ],
    "improvements": ["AI suggestion to strengthen the idea"]
  },
  "businessPlan": {
    "pages": "15-25",
    "sections": ["summary", "market", "financial projections (AI estimates)", "..."],
    "export": "editable/savable document"
  }
}
```

None of these are retrievable via an API — they exist only inside the web app.

## Quick-start recipes

RebeccAi has **no API**, so there are no code recipes. The realistic "automation" is to script the
*inputs and downstream signals* around it, not RebeccAi itself:

### Recipe 1 — Use RebeccAi as a fast first-pass, then test real demand (the intended workflow)
1. In the UI, run the idea with the **most skeptical** feedback personality; keep the weaknesses +
   improvement suggestions, discard the verdict.
2. Turn the sharpest version into a one-line value prop.
3. Build a smoke-test landing page + waitlist (see `/sales-funnel`, `/sales-audience-growth`) and set a
   go/no-go threshold *before* driving traffic.
4. Only trust the RebeccAi business plan after a real demand signal — then replace its numbers.

### Recipe 2 — If you need the "market signal" scripted, pull it from source (not RebeccAi)
Since there's no API, get demand signals from real sources instead:

```bash
# Example: pull Reddit discussion volume for a problem keyword (real behavior signal),
# which is closer to demand than an AI evaluation. Replace {keyword}.
curl -s "https://www.reddit.com/search.json?q=%22{keyword}%22&sort=new&limit=100" \
  -H "User-Agent: idea-research/1.0" | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d['data']['children']),'recent posts')"
```

```python
# Same idea in Python — count recent mentions as a rough demand proxy.
import requests
kw = "your problem keyword"
r = requests.get(
    "https://www.reddit.com/search.json",
    params={"q": f'"{kw}"', "sort": "new", "limit": 100},
    headers={"User-Agent": "idea-research/1.0"},
    timeout=30,
)
posts = r.json()["data"]["children"]
print(len(posts), "recent posts mentioning the problem")
# Gotcha: mentions = interest, not willingness to pay. Confirm with a pre-sale.
```

**Gotcha for both recipes:** neither RebeccAi's evaluation nor a Reddit count is validated demand — only
a stranger taking a costly action (waitlist email, "buy" click, pre-order) is.

## Integration patterns

There is nothing to integrate — no API, webhooks, CRM sync, or iPaaS surface. If a user asks for a
CRM-sync or pipeline architecture around RebeccAi, the honest answer is that it isn't possible with
RebeccAi as the source; the pattern to build is around a **real demand signal** (landing-page conversion
events → your CRM/warehouse), which the validators and funnel skills cover. Route data-pipeline questions
to `/sales-idea-validation` (for the method) and `/sales-funnel` (for the page that emits real events).
