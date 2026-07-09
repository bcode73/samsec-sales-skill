# Ahrefs Platform Reference

## Overview

Ahrefs (ahrefs.com) is the **industry-leading SEO toolset** — best known for the largest live backlink
index and high-quality keyword/rank data. Best for SEOs, content marketers, and agencies doing backlink
analysis, keyword research, rank tracking, and competitive intel. The watch-out is **cost**: a credit
system on lower tiers, expensive add-ons, a metered **API-units** model, and no free trial make it the
most-praised-but-most-complained-about-on-price tool in SEO.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Site Explorer | Backlinks, organic keywords, **Domain Rating (DR)/URL Rating (UR)**, traffic | **API** (`/site-explorer/*`) + **MCP**; unit-metered |
| Keywords Explorer | Volume, difficulty, CPC, SERP | **API** (`/keywords-explorer/*`) + MCP |
| Rank Tracker | Track keyword positions over time | **API** (often **free of units**) + UI |
| Site Audit | Technical crawl, issues | **API** (`/site-audit/*`); crawl runs **UI/scheduled** |
| Content Explorer | Find top content by topic | **UI-only** (no documented API group) |
| Brand Radar | AI-search-visibility tracking (ChatGPT/Perplexity mentions) — **$199 add-on** | **UI-only** (see `/sales-ai-visibility`) |
| Batch Analysis | Bulk DR/traffic/backlinks for many targets | **API** (`/batch-analysis`) — unit-efficient |
| Webmaster Tools (AWT) | Free Site Audit + limited Site Explorer for your own verified sites | **UI-only** |
| AI Content Helper / Report Builder | Content briefs / custom reports — **$99 add-ons each** | **UI-only** |

**Programmatic interfaces:** REST **API v3** (`api.ahrefs.com/v3`, Bearer, API-units), **official MCP
server** (Claude/ChatGPT/Cursor, Lite+), OAuth (Ahrefs Connect), Looker Studio connectors. **v2
discontinued 2025-11-01.** No event webhooks (read/research API). See `references/ahrefs-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on the live pricing page; Ahrefs changes pricing/credits often.*

| Plan | ~Price/mo | Notable limits |
|---|---|---|
| Starter | ~$29 | credit-metered, very limited |
| Lite | ~$129 ($108 annual) | **500 credits/mo**, monthly-only rank updates, API units (light), **MCP** |
| Standard | ~$249 ($208 annual) | more credits, daily rank updates, API units |
| Advanced | ~$449 ($374 annual) | higher limits, API units |
| Enterprise | from ~$1,499 (annual) | SSO, audit, full API |

- **No free trial.** Lower tiers run a **credit system** — every report opened in Site Explorer / Keywords
  Explorer / Content Explorer costs **1 credit** (e.g. 500/mo on Lite). Heavy use incurs overage.
- **API access:** Lite/Standard/Advanced include a **monthly API-unit allocation** for light use; heavy or
  production API needs a **paid API subscription (~$500–$10,000/mo) or Enterprise**.
- **Add-ons** stack: Brand Radar **$199**, AI Content Helper **$99**, Report Builder **$99**.
- **No affiliate program** — Ahrefs deliberately doesn't run one.

## Integrations

- **Direction:** pull/read only — the API and MCP **read** SEO data into your tools/agents; there is no
  write surface and no event webhooks.
- **Auth:** Bearer API key (owners/admins, 1-yr expiry) or OAuth for public apps. **MCP** uses your key.
- **Native:** Looker Studio (Data Studio) connectors, GSC Insights (Search Console), AI-chatbot connect.

## Data model

Read-oriented; identity is a **target** (domain, subdomain, or URL) + market (`country`).

**Domain metrics** <!-- Constructed from docs — verify -->
```json
{ "target": "example.com", "domain_rating": 76, "ahrefs_rank": 12453, "org_traffic": 120000, "backlinks": 480000, "refdomains": 9200 }
```

**Organic keyword row** <!-- Constructed — verify -->
```json
{ "keyword": "best crm", "country": "us", "volume": 24000, "difficulty": 78, "position": 7, "traffic": 320 }
```

**Limits/usage** <!-- Constructed — verify -->
```json
{ "units_limit": 500000, "units_used": 137250, "units_remaining": 362750, "reset_date": "2026-07-01" }
```

## Quick-start recipes

### Recipe 1 — Pull a competitor's top organic keywords (API, unit-aware)

**Trigger:** report request → call organic-keywords with a tight `select` + `limit` to minimize units.
```bash
curl -s "https://api.ahrefs.com/v3/site-explorer/organic-keywords?target=competitor.com&country=us&limit=100&select=keyword,volume,position,traffic" \
  -H "Authorization: Bearer $KEY"
```
```python
import requests
def top_keywords(target, key, n=100):
    r = requests.get("https://api.ahrefs.com/v3/site-explorer/organic-keywords",
        headers={"Authorization": f"Bearer {key}"},
        params={"target": target, "country": "us", "limit": n,
                "select": "keyword,volume,position,traffic"}, timeout=30)
    r.raise_for_status(); return r.json()
```
**Gotchas:** min **50 units/request**, scaling with rows × fields — always pass **`select`** and a small
`limit`. Check remaining units via `/subscription-info/limits-and-usage` first.

### Recipe 2 — Let Claude pull SEO data directly (MCP)

**Setup:** add the official Ahrefs MCP (Lite+) so an agent can answer "what are competitor.com's top
backlinks?" without code:
```bash
claude mcp add --transport http ahrefs "https://mcp.ahrefs.com" --header "Authorization: Bearer $KEY"
```
**Gotchas:** MCP draws on the same **API units** as REST — a chatty agent burns the budget; keep queries
specific. Confirm the exact hosted URL in the MCP docs.

### Recipe 3 — Bulk-score a list of prospect domains (batch, unit-efficient)

**Trigger:** you have 500 domains → one `batch-analysis` call beats 500 single calls.
```bash
curl -s -X POST "https://api.ahrefs.com/v3/batch-analysis" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{ "targets": ["a.com","b.com"], "select": ["domain_rating","org_traffic","backlinks"] }'
```
**Gotchas:** batch endpoints are the cheapest way to score many targets; still unit-metered, so request
only the fields you'll use.

## Integration patterns

- **Budget units like money.** The #1 integration failure is blowing the monthly unit/credit allocation.
  Always `select` minimal fields, cap rows, prefer `batch-analysis`, cache aggressively, and poll
  `limits-and-usage`. For sustained/production volume, you need the paid API subscription or Enterprise.
- **Avoid the anti-abuse trap.** Ahrefs throttles bursty automated access (the "suspicious activity"
  system) even within plan limits — pace requests, add jitter/backoff, and don't parallelize hard.
- **MCP for exploration, REST for pipelines.** Use the MCP server for ad-hoc agent questions; use the REST
  API with tight `select` for scheduled exports.
- **Read-only mindset.** There's no write API and no webhooks — Ahrefs is a data source you pull from, then
  push into your own CRM/warehouse/report.
- **v3 only.** v2 is dead (since 2025-11-01); any tutorial referencing v2 endpoints is obsolete.
