# Ideagrape Platform Reference

<!-- Best-effort from research (2026-07). Ideagrape (ideagrape.com) is a small, solo-maker tool with a
JS-rendered site and thin third-party review coverage; the FAQ/blog live on richdackam.com. Pricing,
free-tier limits, catalog size, and scoring methodology are best-effort — verify on the live site. -->

## Overview

Ideagrape is a **startup-idea discovery + AI-validation hybrid** aimed at indie hackers, makers, and
first-time founders hunting for a SaaS to build. It blends two products in one: (1) a **browsable
database of 700+ pre-researched, market-scored SaaS ideas** (the discovery/IdeaBrowser-style side) and
(2) an **AI validation suite** that generates a custom idea and analyzes it (opportunity score,
willingness-to-pay, assumptions, a build blueprint, a growth matrix). Its differentiator vs the paid
IdeaBrowser is **price + speed** ("conviction in minutes" at a fraction of the cost). It is a **UI web
app with no public API**, and every score/number it shows is a **directional AI/data estimate, not
validated demand**.

## Capabilities & automation surface

Every module below is **UI-only** — there is no API, webhook, Zapier/Make, or MCP surface to automate
any of it. The tags note whether output can be *scripted* (none can) vs *copied manually*.

**Discovery side**
- **Idea Database / Browser** — 700+ AI-validated SaaS ideas, each with market data (search volume,
  year-over-year growth, market-size estimate, competitor notes). *UI-only.*
- **Idea of the Day** — a daily surfaced idea with its analysis. *UI-only.*
- **Trending Keywords** — keyword/topic trends to spot demand before saturation. *UI-only.*
- **Market Analytics** — a dashboard of growth trends and market signals across the catalog. *UI-only.*

**Validation side**
- **Idea Generator** — generates custom SaaS ideas from your skills/interests/target market (metered per
  plan; the free tier has a daily generation cap). *UI-only.*
- **Idea Analyzer / opportunity score** — competitor analysis, market sizing, and an **opportunity score**
  for a chosen idea. *UI-only.*
- **WTP (Willingness-to-Pay) Analyzer** — estimates what buyers would pay / a price point. *UI-only.*
- **Assumption Validator** — surfaces the key assumptions your idea rests on to test them. *UI-only.*
- **Build Blueprint** — an interactive plan for how to build/ship the idea. *UI-only.*
- **Startup Growth Matrix** — a growth/positioning matrix for the idea. *UI-only.*
- **AI Chat & Strategize** — a chat helper to refine strategy (**Pro-gated**). *UI-only.*

## Pricing, limits & plan gates

*Best-effort — confirm at ideagrape.com/pricing. Plans are billed **annually**.*

| Plan | Price (best-effort) | Key inclusions / gates |
|---|---|---|
| **Free** | $0, no card | Limited window of recent ideas (commonly cited **~10 recent ideas**) + a **daily generation cap** (commonly cited **~1 generation/day**); browse the database. |
| **Starter** | **~$199/year** | ~**90 AI generations**; full idea database + analyzers. |
| **Pro** | **~$697/year** | ~**1,500 AI generations** + **AI Chat & Strategize** + 50+ tools. |

Notes:
- **The free tier is a trial-grade cap**, not a working free product — a daily generation limit and a
  limited recent-ideas window. Anyone iterating on ideas will hit it fast.
- **AI Chat & Strategize is Pro-only.**
- Generation counts are the main lever between Starter and Pro. Because founders **re-validate the same
  idea 3–6× across pivots**, budget generations for re-runs, not a single pass.
- **Positioning vs IdeaBrowser:** Ideagrape's annual Starter/Pro (~$199 / ~$697) undercut IdeaBrowser's
  pricier tiers (commonly cited ~$499 / ~$1,499). Treat any price comparison as best-effort.

## Integrations

**None.** Ideagrape reads from and writes to nothing outside its own UI — no native CRM connectors, no
Zapier triggers/actions, no Make modules, no MCP server, no webhooks, no public REST/GraphQL API. Data
flow is **inbound only** (you type an idea in; you read the analysis on screen). The only way "out" is a
manual copy of what's on the page.

## Data model

There is **no public API**, so there are no documented object schemas, IDs, or query patterns. The
conceptual objects a user works with (for orientation only — **not** an API contract):

<!-- Constructed from the product UI described in research — NOT from any API. No programmatic access exists. -->

```json
{
  "idea": {
    "title": "AI-powered X for Y",
    "category": "SaaS niche",
    "opportunity_score": 0,
    "market": {
      "search_volume": "estimate",
      "yoy_growth": "estimate",
      "market_size": "estimate"
    },
    "competitors": ["..."],
    "wtp_estimate": "price point (hypothesis)",
    "assumptions": ["key assumption to test", "..."],
    "build_blueprint": ["step", "..."]
  }
}
```

Every value here is an **AI/data estimate rendered in the UI**; none of it is retrievable or writable
programmatically.

## Quick-start recipes

Because there is **no API**, the "recipes" are the realistic *manual* and *fallback* workflows — there is
no cURL/SDK path to Ideagrape itself.

### Recipe 1 — Shortlist a niche from the database (manual)
1. Open the **Idea Database** and filter/browse by growth trend or category.
2. For 5–10 candidates, copy the title, opportunity score, market-size/search-volume estimate, and
   competitor notes into your own sheet.
3. **Verify each market/search number against a primary source** (a keyword-volume tool, Google Trends,
   real competitor pricing) — treat the built-in numbers as directional only.
4. Take the top 1–2 to a real demand test (smoke test / pre-sale), not straight to build.

### Recipe 2 — Validate one idea, keep the structure, discard the verdict (manual)
1. **Generate** or paste your idea; run the **opportunity score**, **WTP Analyzer**, and **Assumption
   Validator**.
2. Keep the **structured** outputs — competitor list, the assumptions to test, the market angle, the
   build blueprint. Discard the score-as-verdict.
3. Turn the top assumptions + the WTP price into a **pre-sale hypothesis**, then test it. The price is a
   guess until a stranger pays it.

### Recipe 3 — "Export the ideas via API" → the fallback that actually works (developer)
There is no endpoint to call. If you need Ideagrape-style data in your own pipeline:

```bash
# There is NO Ideagrape API. Build the signal from primary sources instead, e.g.:
# 1) keyword/search-volume via a keyword API (illustrative)
curl "https://api.example-keyword-tool.com/v1/volume?q=your+niche" -H "Authorization: Bearer $KEY"
# 2) demand chatter via Reddit's public API, Product Hunt, Hacker News
curl "https://www.reddit.com/search.json?q=your+niche&sort=new" -H "User-Agent: your-app/1.0"
```

```python
# Pattern: assemble your own "opportunity" record from real sources, since Ideagrape can't be queried.
import requests

def niche_signal(term, kw_key):
    volume = requests.get(
        "https://api.example-keyword-tool.com/v1/volume",
        params={"q": term},
        headers={"Authorization": f"Bearer {kw_key}"},
        timeout=30,
    ).json()
    reddit = requests.get(
        "https://www.reddit.com/search.json",
        params={"q": term, "sort": "new", "limit": 50},
        headers={"User-Agent": "niche-research/1.0"},
        timeout=30,
    ).json()
    return {
        "term": term,
        "search_volume": volume,            # verify — your own primary source
        "recent_threads": len(reddit.get("data", {}).get("children", [])),
    }
```

**Gotcha:** this reconstructs the *inputs* Ideagrape summarizes; it does not reproduce its scores. The
point of automating is a **real demand signal** (landing-page conversions), not a directory of ideas.

## Integration patterns

Not applicable — there is nothing to integrate against. If a user insists on a pipeline:
- **CRM/warehouse sync:** none possible; copy manually or build from primary sources (above).
- **Webhook listeners:** none — Ideagrape emits no events.
- **Batch export:** none — no pagination/rate-limit surface because there is no API. Manual copy only.

The durable takeaway for any integration question: **automate the smoke-test's conversion data, not
Ideagrape.** That's where a go/no-go actually lives (`/sales-idea-validation`, `/sales-funnel`).
