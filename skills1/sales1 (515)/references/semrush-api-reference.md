# Semrush API Reference

## Overview

Semrush provides REST APIs for accessing SEO, advertising, and market data programmatically.

- **Developer portal**: https://developer.semrush.com/
- **API docs**: https://developer.semrush.com/api/
- **Auth**: API key passed as the `key` query parameter (found in Semrush dashboard → Subscription info → API units). OAuth 2.0 (Bearer token in header) is also supported for the Projects API and Map Rank Tracker API. The Listing Management API passes the key in a header: `Authorization: Apikey <YOUR_API_KEY>`.
- **Access (Standard SEO + Projects API)**: "available as an add-on to a Business subscription" ($499.95/mo) — you also purchase API units separately. (Verified on developer.semrush.com 2026-06-13.)
- **Other API products with different access**:
  - **Trends API** — separate Trends Basic / Trends Premium tiers; uses its own request limits (default 10,000 requests/mo) rather than Standard API units.
  - **Listing Management API** — available to all Semrush Local Pro and Business plan users.
  - **Map Rank Tracker API** — "available for all Semrush users. You don't need to purchase API units or have a special subscription to access it."
- **Pricing model**: Unit-based — each request/line consumes API units, cost varies by endpoint
- **MCP Server**: Official — available as an app in Claude, Claude Code, ChatGPT, Cursor, VS Code, Perplexity, Gemini. Available across Semrush One, SEO, and Trends API plans; every MCP query consumes API units based on your subscription.

## Authentication

Most requests pass the API key as the `key` query parameter:

```
https://api.semrush.com/?type=domain_ranks&key={API_KEY}&export_columns=Db,Dn,Rk,Or,Ot,Oc,Ad,At,Ac&domain=example.com
```

Exceptions (verified 2026-06-13):
- **Listing Management API** — key goes in a header: `Authorization: Apikey {API_KEY}`.
- **Projects API & Map Rank Tracker API** — also support **OAuth 2.0**, passing `Authorization: Bearer {TOKEN}` in the header (Device Authorization Grant recommended).

## Analytics API

### Domain Reports

**Domain Overview** (~10 units)
```
GET https://api.semrush.com/?type=domain_ranks&key={KEY}&domain={domain}&export_columns=Db,Dn,Rk,Or,Ot,Oc,Ad,At,Ac&database={db}
```
Returns: organic keywords, organic traffic, paid keywords, paid traffic, backlinks count.

**Organic Positions** (10 units per line; 50 units/line for historical data)
```
GET https://api.semrush.com/?type=domain_organic&key={KEY}&domain={domain}&database={db}&export_columns=Ph,Po,Pp,Pd,Nq,Cp,Ur,Tr,Tc,Co,Nr,Td&display_limit=10
```
Returns: keyword, position, previous position, position difference, volume, CPC, URL, traffic %, competition, trend. (Default `export_columns` verified 2026-06-13: `Ph,Po,Pp,Pd,Nq,Cp,Ur,Tr,Tc,Co,Nr,Td`.)

**Paid Search Positions** (20 units per line; 100 units/line for historical data)
```
GET https://api.semrush.com/?type=domain_adwords&key={KEY}&domain={domain}&database={db}&export_columns=Ph,Po,Pp,Pd,Nq,Cp,Vu,Tr,Tc,Co,Nr,Td
```
Returns: paid keywords, positions, ad copy, landing pages.

**Organic Competitors**
```
GET https://api.semrush.com/?type=domain_organic_organic&key={KEY}&domain={domain}&database={db}
```
Returns: competitor domains with overlap metrics.

### Keyword Reports

**Current endpoint — Get Keyword Metrics** (20 API units per request; verified 2026-06-13)
```
GET https://api.semrush.com/apis/v4/keywords/v1/metrics?keyword={keyword}&country={cc}&month={YYYY-MM}
Authorization: Bearer {TOKEN}   (or key= query param)
```
Returns metrics from the latest snapshot for the specified month: search volume, keyword difficulty, CPC, competitive density, SERP features, intents, and trend. Response available in JSON or CSV (semicolon-delimited).

**Deprecated legacy keyword endpoints** (still functional but moved to the "Deprecated" section of the official docs as of 2026-06-13 — prefer `keywords/v1/metrics` above):

- **Keyword Overview** (`type=phrase_all` / `phrase_this`) — `export_columns=Ph,Nq,Cp,Co,Nr,Td`; volume, CPC, competition, number of results, trend.
- **Related Keywords** (`type=phrase_related`) — semantically related keywords with metrics.
- **Keyword Difficulty** (`type=phrase_kdi`) — keyword difficulty percentage (0-100).
- Also deprecated: Batch Keyword Overview, Organic/Paid Results, Keyword Ads History, Broad Match Keyword, Phrase Questions.

```
# legacy example (deprecated)
GET https://api.semrush.com/?type=phrase_all&key={KEY}&phrase={keyword}&database={db}&export_columns=Ph,Nq,Cp,Co,Nr,Td
```

### Backlink Reports

Current backlinks endpoints use a REST-style base path `https://api.semrush.com/apis/v4/backlinks/v1/` with a required `scope` parameter (`ROOT_DOMAIN`, `SUBDOMAIN`, `SUBFOLDER`, or `PAGE`). Responses in JSON or CSV. (Base path and costs verified 2026-06-13.)

**Backlinks Overview** (45 API units per request)
```
GET https://api.semrush.com/apis/v4/backlinks/v1/overview?url={domain}&scope=ROOT_DOMAIN&key={KEY}
```
Returns: total backlinks, referring domains, referring IPs, authority score.

**Historical Summary** (40 API units per line)
```
GET https://api.semrush.com/apis/v4/backlinks/v1/summary?url={domain}&scope=ROOT_DOMAIN&key={KEY}
```

**Backlinks List** (45 API units per line)
```
GET https://api.semrush.com/apis/v4/backlinks/v1/links?url={domain}&scope=ROOT_DOMAIN&key={KEY}
```
Returns: individual backlinks with source URL, anchor text, type (dofollow/nofollow), first/last seen.

**Referring Domains** (40 API units per line)
```
GET https://api.semrush.com/apis/v4/backlinks/v1/ref-domains?url={domain}&scope=ROOT_DOMAIN&key={KEY}
```

**Referring IPs** (20 API units per line)
```
GET https://api.semrush.com/apis/v4/backlinks/v1/ref-ips?url={domain}&scope=ROOT_DOMAIN&key={KEY}
```

> Note: older docs referenced backlinks under `api.semrush.com/analytics/v1/?type=backlinks_overview`. The current documented surface is the `apis/v4/backlinks/v1/` REST paths above.

### URL Reports

**URL Organic Positions**
```
GET https://api.semrush.com/?type=url_organic&key={KEY}&url={url}&database={db}
```
Returns: keywords a specific URL ranks for.

## Projects API

For managing Semrush projects (Position Tracking, Site Audit, etc.):

- **Base URL**: https://api.semrush.com/management/v1/ (path not re-confirmed against current docs 2026-06-13 — see developer.semrush.com/api/projects/)
- **Auth**: API key or **OAuth 2.0** (Bearer token in header)
- **Position Tracking**: Create/manage tracking campaigns, retrieve ranking data
- **Site Audit**: Trigger crawls, retrieve audit results and issue lists

## Local API (Listing Management + Map Rank Tracker)

For local SEO directory management:

- **Manage business listings** across 150+ directories
- **Sync business information** (name, address, phone, hours)
- **Monitor listing accuracy** and resolve inconsistencies
- **Access (verified 2026-06-13)**: Listing Management API is available to all **Local Pro and Business** plan users; auth via `Authorization: Apikey {KEY}` header (a deprecated OAuth version also exists).
- **Map Rank Tracker API**: "available for all Semrush users. You don't need to purchase API units or have a special subscription to access it." Auth via OAuth 2.0.

## Trends API (separate product)

- Website traffic and market insights; sold as **Trends Basic / Trends Premium** tiers.
- Uses its own request limits (default cap **10,000 requests/month**), not Standard API units.

## Databases

Semrush maintains 142 geo databases. Common ones:

| Code | Country |
|------|---------|
| us | United States |
| uk | United Kingdom |
| ca | Canada |
| au | Australia |
| de | Germany |
| fr | France |

Full list at: https://developer.semrush.com/api/v3/analytics/databases/

## Response Format

The official docs describe Analytics/SEO API responses as **CSV**, but the field separator is a **semicolon** (`;`), not a comma. Headers are in the first row. (Verified 2026-06-13.)

```
Ph;Po;Nq;Cp;Ur;Tr;Tc;Co;Nr
seo tools;3;22200;4.46;https://example.com/seo;5234;3.12;0.89;342000000
```

The newer v4 REST endpoints (`apis/v4/keywords/v1/metrics`, `apis/v4/backlinks/v1/*`) support both **JSON and CSV** output.

## Unit Costs

Unit costs vary significantly by endpoint:

| Endpoint | Cost (verified 2026-06-13) |
|---|---|
| Domain Ranks (Domain Overview) | 10 units/line (50/line historical) |
| Domain Organic Positions | 10 units/line (50/line historical) |
| Domain Paid (AdWords) Positions | 20 units/line (100/line historical) |
| Keyword Metrics (`keywords/v1/metrics`) | 20 units per request |
| Backlinks Overview | 45 units per request |
| Backlinks Historical Summary | 40 units/line |
| Backlinks List | 45 units/line |
| Referring Domains | 40 units/line |
| Referring IPs | 20 units/line |

**Budget carefully.** Costs are per **line returned**, not per request — pulling 1,000 organic keywords for one domain costs ~10,000 units on live data (~50,000 units historical).

## Rate Limits

- No traditional requests-per-second rate limit documented
- Consumption is unit-based — once units are exhausted, requests fail
- Monitor usage in Semrush dashboard → Subscription info → API units
- Set up consumption alerts to avoid unexpected overages

## Zapier Integration (No API Key Required)

The **Site Audit** connector works on all Semrush plans via Zapier:
- Trigger: Site Audit completes, health score changes, new issues found
- Actions: Retrieve audit results, issue lists
- No API key or Business plan needed — uses OAuth through Zapier
