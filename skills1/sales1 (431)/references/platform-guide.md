# Preuve AI Platform Reference

<!-- Source: https://preuve.ai/ , https://preuve.ai/pricing , https://preuve.ai/idea-validation , https://preuve.ai/blog/preuve-ai-review (fetched 2026-07) -->

## Overview

Preuve AI (preuve.ai) is an **AI startup-idea validator built around cited, live evidence** — its name is
French for "proof." Rather than one model's opinion, it runs a **10-agent pipeline** searching **50+ live
sources** and **links every key claim back to its origin**, so a founder can audit the evidence behind the
score. Target user: first-time and serial founders, vibe coders, and solo builders who can now ship anything
and need a reality check on *what* to build. Built on **Claude (Opus 4.8)**; independently bootstrapped by a
solo founder. Primary differentiator vs the field: **source-linked claims + a deliberately conservative
score** (median ~55, vs inflated ~78 elsewhere) + **Radar**, an ongoing re-scan/monitoring tier.

## The 10-agent architecture

Preuve runs specialized agents in parallel, then reconciles them:

- **Market analyst** — TAM/SAM/SOM sizing, trend reads
- **Competitor scout** — up to 15 competitors with funding and pricing
- **Community researcher** — Reddit / X / Product Hunt / Quora / Indie Hackers signal
- **Financial analyst** — unit-economics and monetisation read
- **Real-time news scanner** — recent funding, launches, market moves
- **Cross-validator** — fact-checks the other agents' claims and filters junk before it reaches the report

**50+ live sources** include: Crunchbase, Google Trends, G2, Capterra, Product Hunt, Reddit, Quora, Hacker
News, X/Twitter, SEC filings, LinkedIn, Trustpilot, Indie Hackers, Statista, TechCrunch, app stores, and
public pricing pages. Every material finding in the report carries a link to the source it came from.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Reality Check** (free) | 60-second scan: viability score, top risks, ~2 competitor previews, go/no-go verdict | **UI-only** |
| **Founder Report** (paid, one-time) | Full 50+-source analysis (~8–12 min): score, up to 15 competitors, TAM/SAM/SOM, founder-market fit, blind spots, 3 pivots, business plan, source links | **UI-only** |
| **Source-linked claims** | Every key finding cited to its origin (thread, review, filing) | **UI-only** (links viewable/shareable) |
| **Investor-Ready Package** (paid, one-time) | Pitch deck, investment memo, 18-month financial model, competitive teardown | **UI-only** |
| **Audio pitch** | Generated spoken pitch of the idea | **UI-only** |
| **Radar** (subscription) | Scheduled re-scans, competitor threat flagging, viability-score tracking over time | **UI-only** |
| **Competitor Cockpit** (Builder tier) | Enriched, ongoing competitor tracking | **UI-only** |
| **Shareable dashboard** | Interactive report shared via a public link (`preuve.ai/share/{slug}`) | **Link-shareable** (no API) |

**No public API, no webhooks, no MCP server, no Zapier/Make modules.** Everything runs in the browser; the
only programmatic-ish surface is the shareable dashboard link.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — confirm at preuve.ai/pricing. Report-pack prices in particular vary
between pages; treat every figure as approximate.*

Preuve mixes **three pricing axes** — this is the #1 source of confusion:

**1. One-time reports (no subscription):**
- **Reality Check** — **free** (score + risks + ~2 competitors + verdict, 60s)
- **Founder Report** — **~$29 one-time**, with a 14-day report guarantee (full 50+-source analysis)
- **Report packs** — discounted per-report: **5-pack ~$89–95**, **10-pack ~$149–159** (per-report price
  drops to roughly $15–19) — prices differ between pages, so confirm live
- **Investor-Ready Package** — **~$499 one-time** (deck, memo, 18-month model, teardown)

**2. Radar monitoring (monthly subscription):**
- **Radar** — **~$9/month** (monthly re-scans, threat flagging, score tracking)
- **Radar Pro** — **~$24/month** (Radar + enriched competitor data + 1 deep-analysis token/month)
- **Builder** — **~$59/month** (3 deep-analysis tokens/month + Competitor Cockpit)

**3. Lifetime (one-time):**
- **Lifetime Pro** — **~$499 one-time** (≈10 scans/month forever)
- **Lifetime Business** — **~$999 one-time** (≈25 scans/month forever + Investor Package)

There is **no API at all**, so no plan gates an API. A one-time report never renews; only the Radar/Builder
tiers recur.

## Integrations

**None documented.** No native CRM connectors, no Zapier/Make triggers or actions, no webhooks, no public
API, no MCP server. Data flow is **into** the tool (you type the idea) and **out** only via the on-screen
report you can **share by link** (`preuve.ai/share/{slug}`) or save manually (print-to-PDF, copy). If you
need validation output in another system, re-key it by hand or drive a programmatic validator instead.

## Data model

There is **no public API**, so there are no documented object schemas. The user-facing artifact is the
**shareable report/dashboard**. A representative shape of what a Founder Report contains (constructed from
the product description — **not** an API response):

```json
{
  "idea": "One-line description of the idea being validated",
  "viability_score": 61,
  "verdict": "build | pivot | pass",
  "market": { "tam": "…", "sam": "…", "som": "…" },
  "founder_market_fit": "strong | moderate | weak",
  "competitors": [
    { "name": "Acme", "funding": "$4M seed", "pricing": "$29/mo", "source_url": "https://…" }
  ],
  "risks": [ { "risk": "Crowded space", "source_url": "https://…" } ],
  "blind_spots": [ "Regulatory exposure not addressed", "…" ],
  "pivots": [ "Narrow to vertical X", "Sell to segment Y", "Reposition as Z" ],
  "sources": [ { "claim": "…", "url": "https://…" } ]
}
```
<!-- Constructed from docs — verify against live product; Preuve exposes no API. -->

Every material field is expected to carry a `source_url` — the source-linking is the core selling point.

## Quick-start recipes

Preuve has no API, so "recipes" are workflow patterns, not code.

### Recipe 1 — Get an honest read out of a Founder Report (workflow)
1. Write a **sharp one-line idea** first: specific customer + exact problem + why-you-vs-today. Vague input
   → vague evidence.
2. Run the **free Reality Check** to see the score, top risks, and competitor previews before paying.
3. If the verdict is promising, buy the **Founder Report** and **read the citations, not just the number** —
   open the linked Reddit/G2/Crunchbase sources and judge whether the "demand" is real discussion or noise.
4. **Keep the cited structured outputs** (competitor list + pricing, risks, blind spots, pivots) as pitch
   ammunition; **discard the verdict** as your decision — that belongs to a real demand test.

### Recipe 2 — Share or archive a report without an API (workaround)
```bash
# There is NO Preuve API. To share a report, use the built-in shareable dashboard link:
#   https://preuve.ai/share/{your-slug}
# To archive it, use the browser:
#   - Print to PDF (Cmd/Ctrl-P → Save as PDF), or
#   - Select-all → copy into a doc/markdown file.
# To structure competitors for a spreadsheet, paste them into a CSV by hand:
printf 'competitor,funding,pricing,source_url\n' > preuve_competitors.csv
printf 'Acme,"$4M seed","$29/mo",https://example.com\n' >> preuve_competitors.csv
```

### Recipe 3 — Pair the score with the demand test that actually decides (the part worth automating)
The cited report is a strong gut check; the go/no-go is stranger behavior. Automate *that* instead:
```python
# Pseudocode: the demand signal, not the Preuve report, is what you script.
# 1. Build a fake-door landing page (see /sales-funnel).
# 2. Drive a little traffic (a community post or small ad budget).
# 3. Measure the action rate; a commonly cited bar is ~5%+ of targeted visitors.
conversions = signups / targeted_visitors
go = conversions >= 0.05           # decide this threshold BEFORE the test
```

## Integration patterns

**Not applicable — no API, webhooks, or connectors.** If a user asks for a CRM-sync, webhook-listener, or
batch-pipeline pattern, the honest answer is that Preuve supports none of them. The realistic architecture
is: (1) run ideas manually (Reality Check → Founder Report), (2) **share** the report by its dashboard link
or copy it out by hand, and (3) build any automation around the **real demand test** (landing-page
analytics, waitlist signups, pre-sale checkout) — see `/sales-funnel` and `/sales-audience-growth`. For
programmatic idea validation at volume, choose a tool that actually exposes an API.

## Privacy & data handling

Preuve states that **no humans review submissions**, processing is **encrypted**, and idea data is **never
sold or used for model training** — a relevant point for founders wary of typing a novel idea into a
third-party tool. (Vendor claims — verify current terms at preuve.ai before relying on them for anything
sensitive.)
