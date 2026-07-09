# BuildOrNot Platform Reference

<!-- Source: https://buildornot.io (live site Cloudflare/bot-blocked, 403); assembled from
https://readysetlaunch.ai/compare/buildornot/review/, WebSearch snippets, and
https://github.com/buildornot (public org). Re-verify against the live site. -->

## Overview

BuildOrNot (buildornot.io) is a **startup-idea discovery / market-research data platform** with a
bolted-on **free, no-signup AI idea evaluator**, aimed at indie hackers, makers, and first-time
founders looking for something to build (or a quick second opinion on an idea). Reviewers describe it
as "a scraped data directory that bolted on a free AI evaluator" — the **data is the core product**,
the evaluator is a low-friction gateway. It is **not** a structured validator and has **no public API**.

The two jobs it does — keep them separate:

- **Data platform (discovery/research):** browse curated datasets to find proven-demand niches and scan
  what's already making money. Useful as a *starting shortlist*, not proof of demand.
- **AI idea evaluator (gut check):** paste a freeform idea, get an instant AI take (USP, risk factors,
  suggestions). A single-prompt GPT wrapper — directional, reads optimistic, not demand.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **AI idea evaluator** | Freeform idea → instant AI feedback: unique selling point, risk factors, suggestions. No signup, no structured questionnaire. | **UI-only** (runs in-browser against an OpenAI backend; no exposed endpoint to build on) |
| **AI tools / startups dataset** | Tens of thousands of AI tools & startups ranked by **revenue and growth trends** (~55k tools cited). | **UI-only**; free tier = 100-item preview |
| **Reddit startup-ideas dataset** | Startup-idea threads mined from Reddit communities (~50k) — market discussion "heat" and pain-point signals. | **UI-only**; browsing is free/unlimited on the free tier |
| **Startup revenue records** | Revenue / payment-record data across products (~10k). | **UI-only**; free tier = 100-item preview |
| **Trending topics** | Trending topics/searches used to spot rising demand (~199k). | **UI-only**; free tier = 100-item preview |

All counts are marketing figures from the site/reviews — treat as approximate and dated.

## Pricing, limits & plan gates

*Best-effort — the live pricing page is bot-blocked (403); confirm current pricing on buildornot.io.*

| Tier | Price | What you get |
|---|---|---|
| **Free** | $0, no signup | Unlimited use of the AI idea evaluator; unlimited browsing of the Reddit startup-ideas dataset; a **100-item preview** of the other data pages (AI-tools/revenue/trending); community support. |
| **Paid** | **Unpublished / opaque** | Unlimited access to all datasets, advanced analytics, priority support. (Some reviewers report low per-analysis charges, e.g. a ~$3 paid analysis — unverified; pricing is not clearly published.) |

- **The gate that matters for research:** the free tier only *previews* the revenue/tools/trending
  datasets (100 items). If you need the full ranked lists, that's the paid unlock.
- **No published API pricing** — because there is no public API (see below).
- Present all pricing as best-effort and point the user to buildornot.io for the current numbers.

## Integrations

- **CRM / iPaaS connectors:** none documented. No native HubSpot/Salesforce, no Zapier, no Make, no n8n.
- **Data flow:** effectively **read-only, in-app**. BuildOrNot *ingests* public signals (AI-tool
  directories, Reddit, revenue sources) and presents them; it does not offer an outbound data feed.
- **Export:** no documented export. To reuse the data you'd copy what's visible (mind their terms) or
  re-derive the signals from source (Reddit API, Product Hunt, each tool's own page/similarweb).

## Data model

BuildOrNot exposes **no public API and no documented schema**. There are no object IDs, endpoints, or
webhook payloads to integrate against. The tables below are a *conceptual* shape of what the UI shows —
useful for planning your own store if you re-derive the data from source, **not** a real API contract.

<!-- Constructed from the visible UI/reviews — BuildOrNot has NO public API; do not treat as a schema. -->

```json
// Conceptual shape of an "AI tool / startup" row (as displayed in the UI)
{
  "name": "ExampleAI",
  "category": "AI writing",
  "estimated_monthly_revenue_usd": 42000,   // scraped/estimated — verify against a primary source
  "growth_trend": "up",
  "source_url": "https://exampleai.com"
}
```

```json
// Conceptual shape of a "Reddit startup idea" row
{
  "title": "Someone should build X for Y",
  "subreddit": "r/SaaS",
  "engagement": { "upvotes": 312, "comments": 89 },  // interest, NOT willingness to pay
  "permalink": "https://reddit.com/r/SaaS/comments/..."
}
```

```json
// Conceptual shape of the free AI-evaluator response (rendered in-browser, no API)
{
  "idea": "A tool that ...",
  "usp": "…",
  "risk_factors": ["…", "…"],
  "suggestions": ["…", "…"]
  // NOTE: a single-prompt GPT wrapper — no score rubric, no per-gap follow-up, no citations
}
```

## Quick-start recipes

BuildOrNot has **no public API**, so there is no supported programmatic recipe against BuildOrNot
itself. The recipes below are the **workable fallbacks** — get the *signal* BuildOrNot surfaces from
its actual sources, which you *can* automate.

### Recipe 1 — Re-derive "trending Reddit startup ideas" from the source (Python)

Trigger: you want a scriptable feed of startup-idea threads instead of BuildOrNot's preview-capped UI.

```python
import requests

# Reddit's public JSON endpoint — the same kind of signal BuildOrNot's "Reddit ideas" dataset mines.
# For volume/production use, register an app and use OAuth (https://www.reddit.com/dev/api).
url = "https://www.reddit.com/r/SaaS/search.json"
params = {"q": "someone should build", "sort": "new", "limit": 50, "restrict_sr": 1}
headers = {"User-Agent": "idea-discovery/1.0 (by u/yourname)"}

resp = requests.get(url, params=params, headers=headers, timeout=30)
resp.raise_for_status()
for child in resp.json()["data"]["children"]:
    p = child["data"]
    print(p["ups"], p["num_comments"], p["title"], "https://reddit.com" + p["permalink"])
# Treat upvotes/comments as INTEREST, not validated demand.
```

```bash
# cURL equivalent
curl -s -A "idea-discovery/1.0 (by u/yourname)" \
  "https://www.reddit.com/r/SaaS/search.json?q=someone%20should%20build&sort=new&limit=50&restrict_sr=1" \
  | jq '.data.children[].data | {title, ups, num_comments, permalink}'
```

Gotcha: unauthenticated Reddit JSON is rate-limited and best-effort; move to OAuth for anything beyond
ad-hoc research. BuildOrNot itself gives you no endpoint to hit.

### Recipe 2 — Turn a BuildOrNot shortlist into a real demand test (concept)

Trigger: BuildOrNot surfaced a promising niche; now get evidence a stranger wants it.

1. Pick a candidate from the data and write a one-line value prop (specific customer + problem + differentiation).
2. Stand up a fake-door / smoke-test landing page with a single "Get started / Join waitlist / Pre-order" CTA — build via `/sales-funnel`.
3. Drive a little targeted traffic (a relevant community post, a small ad budget) — capture signups via `/sales-audience-growth`.
4. Read the conversion against a **pre-committed threshold** (a commonly cited bar is ~5%+ of targeted visitors), then attempt a small pre-sale for willingness-to-pay.
5. Take the go/no-go from that behavior — not from BuildOrNot's data hit or evaluator verdict. Decision belongs to `/sales-idea-validation`.

Gotcha: this is where truth lives — a directory ranking and an AI take are inputs, the conversion is the evidence.

## Integration patterns

- **No API / webhook patterns apply** — there is nothing to authenticate against, no events to
  subscribe to, no pagination or rate-limit headers of BuildOrNot's own to handle.
- **If you scrape the UI:** respect robots.txt / terms, the site is Cloudflare-fronted (expect bot
  challenges), and the free tier only renders 100 items per dataset — so a scrape is preview-capped too.
- **Preferred pattern:** treat BuildOrNot as a *discovery lens* a human uses in-browser, then feed the
  shortlist into a real, automatable pipeline — Reddit/Product Hunt APIs for demand signal on the source
  side, and landing-page analytics (the real demand test) on the validation side.
