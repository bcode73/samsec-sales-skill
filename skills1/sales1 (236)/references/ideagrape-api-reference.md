<!-- Source: https://ideagrape.com and https://ideagrape.com/alternatives-ideabrowser (researched 2026-07) -->

# Ideagrape API Reference

## No public API

As of the 2026-07 research, **Ideagrape does not expose any public API.** No REST or GraphQL endpoints,
no authentication scheme for third-party access, no webhooks, no Zapier or Make connectors, and no MCP
server were found on the site, in its docs, or in third-party listings. Ideagrape is a **UI web app**;
all functionality (idea database, Idea Generator, opportunity score, WTP Analyzer, Assumption Validator,
Build Blueprint, Growth Matrix, AI Chat) runs in the browser and is not programmatically accessible.

There is also **no GitHub org** for Ideagrape (checked — 404) and no OpenAPI/Swagger/Postman collection.

## Automation surface inventory

| Surface | Available? | Notes |
|---|---|---|
| Public REST/GraphQL API | ❌ No | None documented or found. |
| Authentication for API access | ❌ No | N/A — no API. |
| Webhooks | ❌ No | Ideagrape emits no events. |
| Zapier triggers/actions | ❌ No | Not listed on Zapier. |
| Make (Integromat) modules | ❌ No | Not listed on Make. |
| MCP server | ❌ No | None. |
| Data export | ❌ UI-only | Manual copy of on-screen ideas/analysis only. |

## Getting data out (fallbacks)

Since there is no endpoint to call, reconstruct the *inputs* Ideagrape summarizes from primary sources:

- **Search volume / keyword trends** — a keyword-volume API (e.g. a keyword-research provider) or Google
  Trends.
- **Demand chatter** — Reddit's public JSON API, Product Hunt, Hacker News.
- **Competitor/market data** — the niche's own sites, G2/Capterra, Crunchbase.

See `platform-guide.md` → "Quick-start recipes" → Recipe 3 for working cURL/Python patterns that build
your own opportunity record from these sources.

## Gaps / to re-verify

- Exact **free-tier limits** (recent-ideas window and daily generation cap) are cited from third-party
  summaries (commonly ~10 recent ideas + ~1 generation/day) — the FAQ subpage (saasideas.richdackam.com)
  returned 404 at research; confirm on ideagrape.com/pricing.
- Exact **generation counts** per plan (~90 Starter / ~1,500 Pro) and **prices** (~$199 / ~$697 annual)
  are best-effort — verify on the live pricing page.
- **Scoring methodology** (how the opportunity score and market estimates are derived) is not documented;
  treat all figures as AI/data estimates to verify against a primary source.
- If a public API, webhooks, or an MCP server appears later, add them here and update `platform-guide.md`
  and the SKILL.md automation claims.
