# RB2B Platform Guide

## Data model

| Entity | Key | Attributes | Source |
|--------|-----|------------|--------|
| Person (US only) | pixel visit | full name, email, LinkedIn profile URL, job title, city/state, company name | Person-Level ID |
| Company (global) | pixel visit | company name, domain, industry, employee count, revenue range, location | Company-Level ID (Demandbase) |
| Page visit | URL + timestamp | page URL, visit time, visitor identity (person or company), referral source | Hot Pages |
| Hot Lead | filter match | visitors matching firmographic/demographic criteria (title, company size, industry) | Hot Leads |

## Person-Level Visitor ID

RB2B's core differentiator — identifies the **individual person** visiting your website (US traffic only):

1. **Install the RB2B pixel** — JavaScript snippet added to your website (similar to a Facebook pixel)
2. **Pixel fires on page load** — captures the visitor's IP and browser fingerprint
3. **RB2B matches to identity** — resolves to a real person with name, work email, LinkedIn URL, job title, company
4. **Data pushed to integrations** — visitor data sent to Slack, CRM, webhook, etc. in real-time

**Coverage** (US person-level, per RB2B pricing page 2026):
- Pro+ plan: 35-45% of US website visitors identified at person level (premium resolution)
- Starter / Pro plans: 15-20% US person-level coverage
- Starter: LinkedIn URLs only (no email addresses); Pro/Pro+: includes business email addresses
- Free plan: company-level only (no person-level contact data as of Jan 2026)

**US-only limitation**: Person-level ID only works for US-based visitors. This is a compliance decision (GDPR prohibits this in EU). Non-US traffic gets company-level ID only.

## Company-Level Visitor ID

Powered by **Demandbase** — identifies the company behind a website visit:

- Works **globally** (not limited to US)
- Available on all plans including Free
- Returns company name, domain, industry, employee count, revenue range, location
- Similar to Clearbit Reveal but included in RB2B at no extra cost

## Hot Pages

Flag specific pages as high-intent signals:

1. **Configure Hot Pages** in RB2B dashboard — select URLs that indicate buying intent (pricing, demo request, case studies, comparison pages)
2. **Visitors to Hot Pages get flagged** — these visitors are highlighted in your feed and alerts
3. **Use for prioritization** — sales team focuses on visitors who viewed high-intent pages

## Hot Leads

Filter identified visitors by firmographic and demographic criteria:

1. **Set filters** — job title, company size, industry, location, seniority
2. **Matching visitors surfaced** — only visitors matching your ICP appear in Hot Leads feed
3. **Reduce noise** — ignore visitors who don't match your target profile

## Traffic Insights

Dashboard analytics on your website visitors:
- Total visitors identified (person + company level)
- Traffic trends over time
- Top pages visited
- Top companies visiting
- Geographic breakdown

## Identity Resolution API (APIs V2)

RB2B offers a **separate API product** ("APIs V2" / API Partner Program). Base URL `https://api.rb2b.com/api/v1`; manage the account and keys at `https://ui.api.rb2b.com`. All calls are **POST with a JSON body** and an `Api-Key` header. Credit cost is **per endpoint** (1–4), not a flat 1. See `rb2b-api-reference.md` for full paths and input fields.

| Endpoint | Input | Output | Credits |
|----------|-------|--------|---------|
| IP → Company | IP address | Company domain / firmographics | 1 |
| IP → HEM | IP address | Hashed emails (MD5 + SHA256) | 1 |
| IP → MAID | IP address | Mobile Advertising IDs | 1 |
| Email → LinkedIn (slug / best) | Email | LinkedIn slug or best URL | 1 |
| Email → Business Profile | Email | Employer, title | 2 |
| Email → MAID | Email | Mobile Advertising IDs | 1 |
| HEM → LinkedIn (slug / best) | MD5 hashed email | LinkedIn slug or best URL | 1 |
| HEM → Business Profile | MD5 hashed email | Employer, title | 2 |
| HEM → MAID | MD5 hashed email | Mobile Advertising IDs | 1 |
| LinkedIn → Hashed Emails | LinkedIn slug | All HEMs | 1 |
| LinkedIn → Personal Email (best / all) | LinkedIn slug | Personal email(s) | 1 |
| LinkedIn → Mobile Phone | LinkedIn slug | Mobile phone | 3 |
| LinkedIn → Business Profile | LinkedIn slug | Employer, role | 4 |
| MAID → HEM (reverse) | Mobile ad ID | Hashed email | Coming soon |

**API auth**: API key in the `Api-Key` header. **Rate limit**: 50 requests/second per endpoint. **Official MCP server**: `@rb2b/rb2b-apis-mcp` (`npx -y @rb2b/rb2b-apis-mcp init`).

**API pricing** (separate from pixel product; prepaid credits never expire, unified balance, per-endpoint cost 1–4):
| Credits | Price |
|---------|-------|
| 100 | $9 |
| 3,000 | $149 |
| 50,000 | $999 |
| 500,000 | $4,999 |
| 5,250,000 | $49,999 |

## Pricing (Pixel Product)

| Plan | Price/mo | Resolutions | Person-Level | Key features |
|------|----------|-------------|--------------|--------------|
| Free | $0 | 150 | No (company only) | Company-level ID (global), Slack/Teams alerts. **As of Jan 2026 the Free plan no longer includes any person-level contact data (no names/emails/LinkedIn).** |
| Starter | $79 | 300 | LinkedIn URLs only (15-20% US) | Person-level LinkedIn URLs to Slack, no email addresses, Slack/Teams only. Overage ~$0.45/resolution |
| Pro | $149 | 600 (expandable to 1,250 / 2,500) | Yes — 15-20% US, business emails | Hot Pages, Hot Leads, all integrations, business email addresses. Overage ~$0.25/resolution. Extra domains ~$99/mo (up to 5) |
| Pro+ | $199 | 600–250,000 (tiered) | Yes — 35-45% US, premium resolution | Highest match rate, premium resolution, business emails, all integrations. Overage ~$0.25/resolution |

**Credit-per-visitor model**: As of the Jan 14, 2026 billing restructure, each **unique visitor identified within a 30-day period consumes one credit**, regardless of how many times they return in that cycle. Credits refresh each billing cycle and do not roll over. The restructure doubled monthly limits on paid plans at no extra cost and defaulted subscriptions to month-to-month.

## Integrations

| Integration | Type | What it does |
|-------------|------|-------------|
| Slack | Native | Real-time alerts when visitors identified — includes name, company, title, LinkedIn |
| HubSpot | Native | Push identified visitors as contacts, create/update records |
| Salesforce | Native | Push to leads/contacts, match to existing accounts |
| Zapier | Triggers | New visitor identified → trigger any Zapier workflow |
| Make (Integromat) | Module | RB2B visitor data in automation scenarios |
| Webhooks | API | Push visitor data to any endpoint in real-time |
| Apollo.io | Native | Sync identified visitors to Apollo for sequencing |
| Outreach | Native | Push visitors to Outreach sequences |
| Salesloft | Native | Push visitors to Salesloft cadences |
| Clay | Native | Enrich RB2B visitors with Clay's waterfall enrichment |
| Smartlead | Native | Add identified visitors to Smartlead campaigns |

## Compliance

- **SOC2 Type II certified** — enterprise security standards
- **CCPA compliant** — California privacy law compliance
- **Person-level US-only** — GDPR compliance by not offering person-level ID in EU/UK
- **No cookie-based tracking** — uses deterministic identity resolution, not cookies
