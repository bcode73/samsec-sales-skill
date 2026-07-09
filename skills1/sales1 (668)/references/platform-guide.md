# WorthBuild Platform Reference

*Best-effort from research (2026-07). WorthBuild (worthbuild.io) is a young, low-cost tool with thin
third-party review coverage — verify pricing, the free-tier allowance, report depth, and the scanned
data sources against the live site before relying on specifics.*

## Overview

WorthBuild is an AI startup-idea validator for first-time founders, indie hackers, makers, and vibe
coders. You describe an idea and, in ~2 minutes, it produces a **full validation report** plus its
signature feature — **"Your First Customers"**, a list of real people already voicing the problem in
public discussions, each with a ready-to-send outreach message. Its differentiator vs pure-score
validators (IdeaProof, VenturusAI, RebeccAi) is that it hands you an actual **customer-conversation
shortlist**, not just a number. Priced one-time per report with a free monthly validation; UI-only.

## Capabilities & automation surface

Every module below is **UI-only** — there is no public API, no webhooks, and no Zapier/Make/MCP.

- **Full Validation Report** — TAM/SAM/SOM market sizing, a competitor map (~12 competitors), risk
  assessment (market / technical / execution), unit economics, financial projections, and a
  week-by-week roadmap. *UI-only.*
- **Go/Pivot/Stop verdict** — a headline recommendation synthesizing the report's signals. *UI-only.*
- **Your First Customers** (signature) — scans **Reddit, Hacker News, X/Twitter, and forums** for people
  actively describing the problem the idea solves; each lead includes the pain point, an engagement
  signal, and a **personalized, ready-to-send outreach message**. *UI-only.*
- **Free landing page + waitlist** — auto-generates a hosted landing page with an email-capture waitlist
  so you can start collecting real signups. *UI-only.*
- **Investor Pitch Deck** — one-click **10-slide** deck auto-populated with the report's market data,
  competitor analysis, and financial projections; customizable theme/branding; **PDF export**. *UI-only.*
- **AI Pivot Suggestions** — if an idea scores low, recommends concrete alternative directions (different
  audience, adjacent problem, changed business model). *UI-only.*
- **Discovery Hub** — a browsable feed of problem discussions to explore/validate ideas against. *UI-only.*

**Data sources the scan draws on (per WorthBuild's own description):** search-trend data, community
discussions (Reddit, Hacker News, forums), X/Twitter, startup-launch platforms, developer ecosystems,
traffic analytics, and funding databases. Treat the resulting numbers as AI estimates synthesized from
these signals, not audited figures.

## Pricing, limits & plan gates

Best-effort — confirm at worthbuild.io. WorthBuild is **one-time per report with a free monthly
validation — NOT a subscription and NOT credits.**

| Plan | Price (best-effort) | What you get |
|---|---|---|
| **Free** | $0, no credit card | **One validation per month** — the *full* report, not a teaser |
| **Single Report** | ~$5 one-time | One additional full validation report |
| **5-Report Bundle** | ~$20 one-time | Five reports (marketed as saving ~$5 vs buying singly) |

- **Speed:** ~2 minutes per validation.
- **Free tier is genuinely full** — you experience the complete report on the monthly free run; the paid
  packs are for validating *more* ideas (or the same idea's pivots) within a month.
- **Re-runs cost again:** re-validating a pivoted idea is a separate report once the monthly free run is used.
- **No API/webhook features to gate** — there is no developer surface on any tier.
- The framing WorthBuild uses ("a freelance market researcher charges $500–$2,000; WorthBuild is ~$5") is
  a marketing comparison, not a like-for-like — a $5 AI report is a directional gut check, not consultancy.

## Integrations

- **CRM connectors:** none documented.
- **iPaaS (Zapier/Make/n8n):** none documented.
- **API/webhooks:** none — data flow is **out only, manual** (you read the report, copy the leads,
  download the pitch deck PDF from the browser).
- **Waitlist capture:** the auto-generated landing page collects emails inside WorthBuild; export/handoff
  to an ESP is manual (verify what the UI allows).

## Data model

WorthBuild does not publish a data model or API schema. The report is a rendered web document, not a
queryable object. The shapes below are **constructed from the product description to illustrate the
fields a user sees** — they are NOT an API contract.

<!-- Constructed from product description — NOT an API; verify against the live report UI -->

```json
{
  "idea": "AI tool that auto-chases late invoices for freelancers",
  "verdict": "Go",                          // one of: Go | Pivot | Stop
  "market": { "tam": "…", "sam": "…", "som": "…" },
  "competitors": [ { "name": "…", "positioning": "…", "pricing": "…" } ],   // ~12
  "risks": { "market": "…", "technical": "…", "execution": "…" },
  "unit_economics": { "notes": "…" },
  "financials": { "projection": "…" },
  "roadmap": [ { "week": 1, "focus": "…" } ]
}
```

```json
// "Your First Customers" — one entry per surfaced lead
{
  "source": "reddit",                       // reddit | hackernews | x | forum
  "handle_or_thread": "…",                  // link/handle to the public post
  "pain_point": "quote or paraphrase of the problem they voiced",
  "engagement_signal": "e.g. upvotes / recency / thread activity",
  "outreach_message": "personalized, ready-to-send draft"
}
```

## Quick-start recipes

WorthBuild has **no API**, so there is no code path to call it. The realistic "automations" are (a) using
its outputs well and (b) scripting the *underlying* demand signals yourself when you need them in a
pipeline. Both are shown below.

### Recipe 1 — Run a validation and act on the leads (UI flow, no code)
1. Enter a **specific** problem statement (audience + concrete pain), not a vague one-liner — precision of
   the "First Customers" scan tracks how specific the description is.
2. Read the report for **structure** (competitor map, risks, positioning); treat the **Go/Pivot/Stop**
   verdict and all numbers as AI estimates to verify.
3. Open **Your First Customers** → hand-filter the list (drop bots, off-topic threads, stale posts).
4. For each vetted lead, **rewrite** the canned outreach into a genuinely personal message and send it via
   the platform it came from (respect Reddit/HN norms). Sequence with `/sales-cadence`; land it with
   `/sales-deliverability`.
5. Publish the **free landing page + waitlist** and drive a little traffic; the **waitlist signups**, not
   the lead list, are the real signal. For a purpose-built fake-door page, use `/sales-funnel`.

### Recipe 2 — Reconstruct the demand signal in code (since there's no WorthBuild API)
When you need the signal in a pipeline, pull it from source instead of WorthBuild. Example: surface recent
Reddit posts voicing a problem (the same job "First Customers" does), so you can score/store them yourself.

```bash
# Reddit public search (respect Reddit's API terms + rate limits; use OAuth for anything sustained)
curl -s -H "User-Agent: demand-scan/0.1 by yourname" \
  "https://www.reddit.com/search.json?q=%22chasing%20late%20invoices%22&sort=new&limit=25"
```

```python
import requests

HEADERS = {"User-Agent": "demand-scan/0.1 by yourname"}  # Reddit requires a descriptive UA

def find_problem_threads(phrase: str, limit: int = 25):
    r = requests.get(
        "https://www.reddit.com/search.json",
        params={"q": f'"{phrase}"', "sort": "new", "limit": limit},
        headers=HEADERS, timeout=20,
    )
    r.raise_for_status()
    for child in r.json()["data"]["children"]:
        p = child["data"]
        yield {
            "title": p["title"],
            "url": "https://reddit.com" + p["permalink"],
            "score": p["score"],          # engagement signal
            "subreddit": p["subreddit"],
        }

for t in find_problem_threads("chasing late invoices"):
    print(t["score"], t["subreddit"], t["url"])
```

Gotcha: this reconstructs the *discovery*, not the WorthBuild report — and a thread is still interest, not
demand. Automate the **real** signal (landing-page conversions, replies), not a verdict.

## Integration patterns

There is no sync/webhook/batch surface. Practical patterns:
- **Report handoff:** manual — copy the competitor/risk sections into your notes or pitch; download the
  pitch deck as PDF.
- **Waitlist → ESP:** manual export from the landing page (verify what the UI supports) into your email
  tool; there's no automated pipe.
- **Demand-signal pipeline:** don't depend on WorthBuild — pull from the Reddit API, a keyword-volume
  API, or Google Trends (Recipe 2) and store/score those yourself.

## How WorthBuild compares in the validator cluster

- **vs pure-score validators (IdeaProof, VenturusAI, RebeccAi):** WorthBuild's edge is the **"First
  Customers" shortlist** — an actual conversation list, not just a score. Those rivals go deeper on
  frameworks/assets but don't hand you leads.
- **vs source-cited validators (Preuve AI, DimeADozen):** those emphasize verifiable citations and long
  reports; WorthBuild emphasizes **speed + leads + a landing page** at a far lower price, with lighter
  sourcing — verify its numbers yourself.
- **vs Reddit demand-signal tools (Trend Seeker):** overlap on "find people with the problem," but Trend
  Seeker is a dedicated Reddit-signal engine; WorthBuild bundles a lighter version of that into a
  full-report-plus-assets package. Cross-check demand with `/sales-trendseeker`.
- **The constant:** every one of these gives an AI opinion. The go/no-go is a real behavior test (reply →
  call, waitlist signup, pre-sale), routed to `/sales-idea-validation` and `/sales-funnel`.
