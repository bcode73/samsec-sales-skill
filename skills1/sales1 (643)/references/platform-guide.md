# VentureVault Platform Reference

<!-- Best-effort from research (2026-07). VentureVault is a young, solo-maker, free tool with a
JS-rendered SPA and little third-party review coverage — the homepage/pricing did not render for
automated fetches, so catalog size, exact scoring rubric, and idea-freshness cadence are inferred from
the platform's own copy, its GitHub repo, and the IdeaBrowser model it clones. Verify specifics at
venturevault.space before relying on them. -->

## Overview

VentureVault (**venturevault.space**) is a **free IdeaBrowser alternative** — a browsable **vault of
AI-scored, pre-researched startup ideas** for indie hackers, makers, vibe coders, and first-time
founders who want to *find* something worth building. You browse idea entries, each carrying AI-powered
market analysis and **opportunity scores**, then "discover → analyze → launch." Its differentiator is
price and access: **100% free forever, no credit card**, delivered as a web app plus **native iOS/
Android apps**, with the codebase **open-source on GitHub**. It is an idea-*discovery* tool, not a
demand test — a scored, researched idea is a hypothesis, not proof anyone will pay.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Idea vault (browse)** | A catalog of pre-researched startup ideas you browse/filter | UI-only |
| **Opportunity scores** | Per-idea AI scores — revenue potential, execution difficulty, go-to-market, community interest (mirrors IdeaBrowser's model) | UI-only |
| **AI market analysis** | Per-idea AI-generated market context (problem, audience, competitive/market signals) | UI-only |
| **Community/demand signals** | Interest signals (Reddit/Facebook/YouTube-style community demand, per IdeaBrowser's approach) | UI-only |
| **Save / shortlist ideas** | Keep ideas to revisit (account-based) | UI-only |
| **iOS / Android apps** | Same vault on mobile (built with Capacitor) | UI-only |

**Everything is UI-only.** There is **no public API, no webhooks, and no Zapier/Make/MCP** exposed to
consumers. The backend is Supabase (internal to the app). The GitHub repo
(`github.com/Stevekaplanai/venturevault`) is the **application's own source code** — React/TypeScript/
Vite frontend + Supabase migrations + Capacitor mobile builds — **not** a documented data API you can
call to export ideas.

## Pricing, limits & plan gates

*Best-effort — confirm on venturevault.space.*

- **100% free, forever. No credit card. No paid tier advertised.** The pitch is explicitly "free
  IdeaBrowser alternative / startup ideas FREE forever."
- Because it's a **solo-maker free project**, treat this as best-effort: pricing, catalog size, and
  update cadence can change without notice. There is no published SLA, rate limit, or plan matrix
  because there is no paid/API surface to gate.
- **Will my integration break on the free plan?** There is no integration surface at all — see
  Integrations below. Everything is free UI access.

## Integrations

- **CRM connectors:** none.
- **Zapier / Make / n8n:** none.
- **Webhooks:** none.
- **MCP server:** none.
- **Public REST/GraphQL API:** none documented.
- **Data flow:** effectively **read-only, human-in-the-loop** — you read ideas in the UI/app and copy
  what you need out by hand. Nothing writes into VentureVault, and nothing reads out of it programmatically.

If a user needs the *ideas* in another system, the only supported paths are manual copy (mind the site's
terms) or reconstructing the underlying signals from primary sources (Reddit API, Product Hunt, keyword/
trend tools, each niche's own pages).

## Data model

VentureVault exposes **no public data model** (no API, no documented schema). The consumer-visible shape
of an idea entry — reconstructed from the product's positioning and the IdeaBrowser model it clones — is
approximately:

```json
// <!-- Constructed from product positioning + the IdeaBrowser model VentureVault clones — NOT an API
//      response; there is no public API. Verify field names/values against the live venturevault.space UI. -->
{
  "idea": "One-line startup idea / opportunity",
  "summary": "AI market analysis: problem, target audience, why now",
  "opportunity_score": 0,            // overall AI score (higher = more promising, per the app)
  "signals": {
    "revenue_potential": "low | medium | high",
    "execution_difficulty": "low | medium | high",
    "go_to_market": "notes on channels / GTM difficulty",
    "community_interest": "Reddit / Facebook / YouTube-style demand signal"
  },
  "category": "e.g. AI, SaaS, marketplace, creator tools",
  "competitors": ["existing tools solving this today"]
}
```

Treat every field as an **AI estimate**, not audited data. There are no stable IDs, no query params, and
no pagination contract to build against — because there is no API.

## Quick-start recipes

VentureVault has **no API**, so there is no code-level integration. The realistic "recipes" are a manual
discovery workflow and the two export fallbacks — including code for the *fallback* signal sources, since
that's the only place code applies.

### Recipe 1 — Discovery workflow (manual, the intended use)
1. Open **venturevault.space** (or the iOS/Android app) and browse the vault by category.
2. Sort/scan by **opportunity score**; shortlist 5–10 ideas whose *problem* you actually understand.
3. For each shortlisted idea, read the AI market analysis and note the **competitors** and **community
   interest** — but treat the score as directional.
4. **Verify the market numbers** against a primary source before trusting them.
5. Take the shortlist into a real demand test (`/sales-funnel` smoke test → `/sales-audience-growth`
   waitlist → pre-sale). The vault ends where validation begins.

### Recipe 2 — "I want the ideas in my own database" (there is no API — pull signals from source)
There's no VentureVault API/export, so reconstruct the underlying signal yourself. Example: pull Reddit
demand for a niche (the same kind of community signal the vault summarizes):

```bash
# cURL — Reddit public search (no VentureVault API exists; this is a source fallback)
curl -s -H "User-Agent: idea-research/1.0" \
  "https://www.reddit.com/search.json?q=%22I%20wish%20there%20was%20an%20app%22&sort=new&limit=25"
```

```python
# Python — same idea, structured for shortlisting (fallback signal, NOT VentureVault data)
import requests

def reddit_demand(query, limit=25):
    r = requests.get(
        "https://www.reddit.com/search.json",
        params={"q": query, "sort": "new", "limit": limit},
        headers={"User-Agent": "idea-research/1.0"},
        timeout=20,
    )
    r.raise_for_status()
    for c in r.json()["data"]["children"]:
        d = c["data"]
        print(d["score"], d["num_comments"], d["title"])

# Use to sanity-check a VentureVault idea's "community interest" against real threads.
reddit_demand('"I would pay for" scheduling tool')
```

Gotcha: this is a **fallback**, not VentureVault integration — mind Reddit's API terms and rate limits,
and mind VentureVault's own terms if you copy its idea text.

### Recipe 3 — Compare a VentureVault idea to the paid IdeaBrowser before committing
1. Note the VentureVault idea's opportunity score and market claims.
2. Cross-check the *same* niche against a second lens (IdeaBrowser's daily idea, `/sales-buildornot`'s
   revenue datasets, or `/sales-trendseeker`'s Reddit scoring).
3. **Disagreement between two sources is the useful information** — a niche both flag is a stronger
   shortlist candidate; either way, the decision comes from a smoke test, not the higher score.

## Integration patterns

There is nothing to integrate. For teams that want a *pipeline* around idea discovery:

- **CRM/warehouse sync:** not possible from VentureVault (no API/webhooks). Store shortlisted ideas
  manually or in your own notes/DB.
- **Webhook listeners:** N/A — no events are emitted.
- **Batch/export:** N/A — copy visible ideas by hand (respecting terms), or build your own signal
  pipeline from primary sources (Reddit, Product Hunt, trend/keyword APIs) and use VentureVault only as
  a browsable inspiration layer.
- **The thing worth automating** is the *real demand signal* — landing-page conversions and pre-sale
  checkouts — not a directory of AI-scored ideas.

## Domain & namesake disambiguation

- **Canonical product:** `venturevault.space` (and its iOS/Android apps). GitHub homepage field confirms
  this domain.
- **`venturevault.co`** (listed in some directories) renders a **blank JS skeleton** — not the working app.
- Unrelated "Venture Vault" entities to not confuse it with: a **VC fund** (venturevault.vc /
  linkedin.com/company/venturevault), a **business-funding marketplace** (venturevaultnetwork.com), and
  a **think tank** (venturesvault.com). None are the startup-idea vault.
