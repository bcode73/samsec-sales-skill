# IdeaTwister Platform Reference

<!-- Best-effort from research (2026-07). IdeaTwister is a young pay-per-run tool with thin third-party
review coverage; verify pricing, per-tier alternative/validation counts, and refund policy at
ideatwister.com. -->

## Overview

IdeaTwister (ideatwister.com) is a **pay-per-run AI idea validator whose distinctive job is ranking the
best *angle* of an idea you already have.** You submit one rough idea; a fleet of specialised AI agents
runs in parallel, pulls live web research, "twists" the idea into **10–25 angle-variations (pivots)**,
scores every pivot across **five commercial dimensions**, and returns an **interactive HTML dashboard**
(the "workspace"). It's for founders, indie hackers, vibe coders, and solopreneurs who have *an* idea and
need to decide **which version to build** — not to discover an idea from scratch, and not as proof of
demand. It also has a **Business Growth Run** for existing businesses (growth opportunities + a 90-day
execution plan). It is **UI-only — no public API.**

## The twist engine & the five scoring dimensions

The core loop: **one seed idea → many pivots → a ranked shortlist.** The engine "twists" your idea across
angles (different customers, monetisation, wedges, positioning) and scores each pivot so you can compare
them side by side. The five dimensions (confidence scoring, roughly 0–100):

- **Buyer urgency** — how badly the target buyer needs this now (pain intensity / "hair on fire").
- **Market proof** — evidence the market exists and is moving (competitors, demand signals, live research).
- **Solo executability** — can one founder / a small team actually ship and run this.
- **Revenue speed** — how fast it can plausibly reach money (time-to-first-dollar).
- **Defensibility** — moat / how hard it is to copy once it works.

Top picks are developed further: a **GTM sketch**, **"$100K math"** (a path-to-revenue model), and a
**30-day validation plan**. *All of this is UI-only* — the deliverable is the dashboard, not a file or API.

**What each capability is, and how you can (can't) automate it:**

| Capability | What it does | Automation surface |
|---|---|---|
| Idea "twist" (pivot generation) | Generates 10–25 angle-variations of one seed idea | UI-only |
| Five-dimension pivot scoring | Ranks pivots by buyer urgency / market proof / solo executability / revenue speed / defensibility | UI-only |
| Deep validation | Full stress-test of the strongest pivot(s) — top tier fully validates 2 | UI-only |
| GTM sketch + "$100K math" + 30-day plan | Go-to-market + revenue model + validation plan for top picks | UI-only |
| Interactive dashboard ("workspace") | The deliverable — a shareable HTML workspace (yours commercially) | UI-only (view/copy) |
| Business Growth Run | Growth-opportunity identification + 90-day execution plan for an existing business | UI-only |
| Free tools | Idea viability calculator, validation checklist, niche-ideas list | UI-only |

## Pricing, limits & plan gates

**Model: one-time pay-per-run — NO subscription, no token budgeting, no API key.** Best-effort (verify at
ideatwister.com/pricing):

| Tier | Price (best-effort) | Alternatives generated | Validation depth |
|---|---|---|---|
| **Quick Idea Check** | ~$9/run | Original idea only | Light analysis (~27 insights): market reality check, founder scorecard, main failure risk, first proof needed |
| **Validate This Idea** | ~$29/run | ~10 alternatives | Deep-dive validation (~43 insights): full stress-test, 90-day recommendation, yes/no/fix memo, side-by-side comparisons |
| **Find My Best Direction** | ~$59/run | ~25 alternatives (2 fully validated) | 3 deep-dive validations: original + 2 strongest alternatives, final recommendation |
| **Business Growth Run** | ~$349 | Growth opportunities for an existing business | Business analysis + 90-day execution plan |

- **Add-on:** additional deep validations (Launch Kit) ~$19 each beyond those included.
- **Turnaround:** results in ~5–25 min depending on complexity.
- **Refunds:** a run that **fails before delivering the workspace is refunded automatically**; completed
  runs are ineligible. Frame spend as "cost per attempt" — iterating an idea means paying per re-run.
- **Ownership:** "the angles, opportunities, and dashboards belong to you" (commercial use OK).
- **No plan gates on an API** — because there is no API on any tier.

## Integrations

**None documented.** No native CRM connectors, no Zapier triggers/actions, no Make modules, no MCP server,
no webhooks. Data flow is one-way and manual: you type an idea in the browser → you read/copy the
resulting dashboard. There is no read-from / write-to surface for another system.

## Data model

There is **no public API and no structured export**, so there is no documented object schema. The
conceptual shape of a run's output (constructed from the product UI for orientation only — not an API
contract):

```jsonc
<!-- Constructed from the product UI for orientation — NOT an API response; there is no public API. -->
{
  "seed_idea": "A scheduling tool for freelance designers",
  "tier": "find_my_best_direction",
  "pivots": [
    {
      "angle": "Invoicing-first scheduler for solo designers",
      "scores": {
        "buyer_urgency": 78,
        "market_proof": 64,
        "solo_executability": 82,
        "revenue_speed": 71,
        "defensibility": 40
      },
      "validated": true,
      "gtm_sketch": "…",
      "revenue_math": "path to $100K …",
      "validation_plan_30d": "…"
    }
    // …up to ~25 pivots; top 2 fully validated on the top tier
  ],
  "final_recommendation": "…"
}
```

Treat every number here as an **AI estimate**, not a measured fact.

## Quick-start recipes

IdeaTwister has **no API**, so there are no cURL/Python integration recipes. The useful "recipes" are
workflow patterns for getting value out of a UI-only, pay-per-run tool:

### Recipe 1 — Pick the best angle, then prove it for real
1. Frame the seed idea concretely (specific customer + exact problem + wedge) before you run — output
   quality tracks input depth.
2. Run **Find My Best Direction** to twist into ~25 pivots and rank them; read the five-dimension scores
   to shortlist 2–3 angles (the top tier already fully validates 2).
3. **Discard the verdict, keep the structure**: pull the winning pivot's GTM sketch, competitor/market
   read, and 30-day plan.
4. Build a smoke-test / fake-door landing page for the winning angle (`/sales-funnel`), drive a little
   traffic, and set a pre-committed conversion bar; then attempt a pre-sale (`/sales-idea-validation`).
5. The go/no-go comes from stranger behavior on the chosen angle, not the pivot score.

### Recipe 2 — Automate the *signal*, not IdeaTwister
Because there's no API, don't try to script IdeaTwister. If you want programmatic idea/market signals,
pull them from source instead:
```python
# Pseudocode — reconstruct the demand signals IdeaTwister estimates, from real sources you CAN script.
# (IdeaTwister itself has no API/webhooks/Zapier/MCP.)
import requests

# e.g. search-volume / trend APIs, Reddit API for pain-point threads, Product Hunt for competitors.
# Then run your own smoke test and read landing-page analytics — that's the signal worth automating.
```

## Integration patterns

**Not applicable — there is no integration surface.** No CRM sync, no webhook listener, no batch pipeline.
The only "integration" is manual: copy the dashboard's contents (which are yours to use commercially) into
your own docs/CRM by hand. If a workflow needs the underlying data programmatically, reconstruct it from
scriptable sources (keyword-volume API, Google Trends, Reddit, Product Hunt) and put the go/no-go on a
real demand test whose analytics you *can* automate.
