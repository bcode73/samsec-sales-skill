# Prospeo Platform Guide

## Person Enrichment

The core Prospeo feature — find verified emails, mobile numbers, and full B2B profiles.

**Input options** (any one of these):
- First name + last name + company identifier (name, website, or LinkedIn URL)
- Full name + company identifier
- LinkedIn URL (standalone)
- Email address (standalone — reverse lookup)
- Person ID (from a previous search)

**What you get back**:
- Verified email with status (VERIFIED, NOT_VERIFIED)
- Mobile number with verification status (costs 10 credits extra)
- Full profile: job title, job history, headline, skills, location, timezone
- Current company data: name, domain, industry, employee count, funding, tech stack, job postings

**Key settings**:
- `only_verified_email: true` — only return results with a verified email (saves credits on unmatched)
- `enrich_mobile: true` — include mobile number lookup (costs 10 credits instead of 1)
- `only_verified_mobile: true` — only return results with a verified mobile

**Credit costs**:
- Standard enrichment (person + company + email): 1 credit per email found
- With mobile: 10 credits per mobile found (email included free)
- No match found: free
- Same record enriched again within 90 days: free (re-enriching after 90 days uses credits again)

## Company Enrichment

Firmographic data on 30M+ companies — 50+ data fields.

**Input options** (any one of these):
- Company website/domain (most reliable)
- Company LinkedIn URL
- Company name (use with caution — less precise)
- Company ID (from previous enrichment)

**What you get back**:
- Basic info: name, website, domain, description
- Classification: industry, type, SIC/NAICS codes
- Size: employee count, employee range, revenue range
- Location: HQ address, country, state, city
- Social: LinkedIn, Twitter, Facebook, YouTube URLs
- Financial: funding history, total funding, last funding date
- Technology: tech stack detection
- Engagement: job postings, B2B/B2C attributes, free trial/pricing indicators

**Credit costs**: 1 credit per matched company. Free for no match, or for re-enriching the same record within 90 days (after 90 days it uses credits again).

## Person Search

Search through 200M+ contacts with 30+ filters. Returns up to 25 results per page, max 25,000 total (1,000 pages).

**Available filters**:

| Filter category | Filters |
|---|---|
| **Company** | industry, location, headcount range, funding (stage, date, amount, total), websites (up to 500), names (up to 500) |
| **Person** | seniority, department, location, job title, years of experience |

**Important**: Search returns profile data but NOT emails or phones. You must use Enrich Person on results to get contact info. Search costs 1 credit per request that returns results.

## Company Search

Search through 30M+ companies with filters. Same pagination as Person Search.

**Available filters**:
- Industry, location, headcount range
- Funding: stage, date, last amount, total amount
- Technology stack, email provider (MX)
- NAICS codes, SIC codes
- Websites (up to 500), names (up to 500)

**Credit cost**: 1 credit per request that returns results.

## Bulk Operations

Enrich up to 50 records per API call for both person and company enrichment.

**Bulk Enrich Person**: Same input options as single enrichment, but send an array of up to 50 records. Each record needs a unique `identifier` string for tracking. Response separates `matched`, `not_matched`, and `invalid_datapoints`.

**Bulk Enrich Company**: Same — up to 50 companies per call with identifiers.

**Credit costs**: Same as single enrichment (1 per matched person/company, 10 for mobile). `total_cost` field in response tracks total credits spent.

## Chrome Extension

Prospeo's Chrome extension extracts contact data from LinkedIn and LinkedIn Sales Navigator.

**What it does**:
- Find verified emails from LinkedIn profiles
- Extract contact data while browsing Sales Navigator
- One-click enrichment without switching to the Prospeo app

## 5-Step Email Verification

Prospeo uses a 5-step verification process (built into enrichment — not a separate endpoint):

1. **Syntax check** — valid email format
2. **Domain/MX check** — domain exists and accepts email
3. **SMTP verification** — mailbox exists
4. **Catch-all detection** — identifies domains that accept all addresses
5. **Result validation** — cross-references multiple signals

Verification statuses: `VERIFIED` (safe to send), `NOT_VERIFIED` (use with caution).

## Data Model

| Entity | What it represents | Key relationships |
|---|---|---|
| **Person** | A B2B professional with contact info | Has email, mobile, job history, skills; linked to Company |
| **Company** | An organization with firmographic data | Has employees, funding, tech stack, job postings |
| **Search** | A filtered query across the database | Returns Person or Company results (no contact info) |
| **Enrichment** | A lookup that returns full contact data | Consumes credits; 90-day dedup per account (re-enriching the same record within 90 days is free) |

## API Quick Reference

- **Base URL**: `https://api.prospeo.io`
- **Auth**: `X-KEY` header with API key
- **Method**: POST for all endpoints (GET for account-information only)
- **Content-Type**: `application/json`
- **Rate limits**: Per-plan, tracked via response headers (`x-daily-request-left`, `x-minute-request-left`, `x-second-rate-limit`)
- **Active endpoints**: `/enrich-person`, `/bulk-enrich-person`, `/enrich-company`, `/bulk-enrich-company`, `/search-person`, `/search-company`, `/search-suggestions`, `/account-information`
- **Deprecated** (removed March 1, 2026): `/email-finder`, `/mobile-finder`, `/email-verifier`, `/domain-search`, `/social-url-enrichment`

For the full endpoint catalog, request/response schemas, and rate limits, see `references/prospeo-api-reference.md`.

## Integrations

| Integration | Type | What it does |
|---|---|---|
| **HubSpot** | Native | Enrich CRM contacts with verified emails, phones, firmographic data |
| **Salesforce** | Native | Keep CRM data clean with enriched contacts and accounts |
| **Clay** | Native | Automate datan enrichment in Clay workflows, build dynamic lead lists |
| **Smartlead** | Native | Push enriched leads to Smartlead campaigns |
| **Instantly** | Native | Push enriched leads to Instantly campaigns |
| **Lemlist** | Native | Push enriched leads to Lemlist sequences |
| **Zapier** | Native | Connect to 8,000+ apps for automated workflows |
| **Make** | Native | Visual automation workflows with Prospeo actions |
| **n8n** | Native (community node) | Self-hosted automation with `@prospeo/n8n-nodes-prospeo` |
| **MCP Server** | Official (`@prospeo/mcp-server`) | Access enrichment and search from AI agents via Model Context Protocol |

## Pricing

*Plan names/credits re-verified 2026-06-13 against help.prospeo.io. Exact monthly dollar amounts are JS-rendered on prospeo.io/pricing and could not be machine-verified — confirm at prospeo.io/pricing before quoting prices.*

Prospeo has **four plans: Free, Starter, Growth, Pro**. All paid plans are **priced per user** (credit allotments below are **per user per month**) and offered in monthly or yearly billing (yearly is discounted).

| Plan | Credits/mo | Key features |
|---|---|---|
| Free | 100 (account, not per-user) | Core enrichment, Chrome extension, basic filters, limited API, no CSV enrichment |
| Starter | 2,000 / user | CSV enrichment, advanced filters (Technology, Job Posting, Revenue, Funding), API access |
| Growth | 5,000 / user | CRM integrations, Job Change filter, priority support |
| Pro | 15,000 / user | Higher API rate limits |

All paid plans include person + company enrichment, search, Chrome extension, and API access. Mobile enrichment costs 10 credits per mobile found on all plans.
