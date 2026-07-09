# Skrapp.io Platform Guide

## Email Finder
- **What it does**: Finds a verified professional email address from a person's name and company or domain — 92% success rate, available as single lookup or bulk operation
- **Endpoint**: `GET /api/v2/find` with `firstName`+`lastName` (or `fullName`) and `company` or `domain`; add `includeCompanyData=true` to return firmographics inline. Bulk: `POST /api/v2/find_bulk` (max 100 entries per request).
- **Key behavior**: Returns the most likely email plus `pattern` and a `quality` object (`status`, `status_message`); uses pattern detection plus real-time mailbox validation to achieve 92% accuracy
- **Credit cost**: 1 credit per successful find (no charge for duplicates or invalid results)
- **Use cases**: Finding a specific decision-maker's email when you know their name and company, building targeted outbound lists for account-based outreach, enriching CRM records with missing emails

## Lead Finder
- **What it does**: Searches a database of 200M+ B2B contacts using 17+ filters — job title, location, industry, company size, revenue, seniority, and more — to build targeted prospect lists
- **Key filters**: Job title, seniority level, department/function, location (country/city), industry, company size (employees), company revenue, company name, domain
- **Credit cost**: 1 credit per contact revealed
- **Use cases**: Building ICPs-based prospect lists, finding decision-makers at target accounts by title and seniority, market research across industries and geographies, expanding TAM with filtered discovery

## Data Enrichment
- **What it does**: Bulk enrich CSV or Excel files with email addresses and firmographic data — upload your file, Skrapp auto-maps columns (name, company, domain), and enriches each row with emails, industry, revenue, employee count, and location
- **Key behavior**: Auto-column mapping detects common field names; supports CSV and Excel formats; enriches with both contact-level (email) and company-level (firmographics) data
- **Credit cost**: 1 credit per successfully enriched contact
- **Use cases**: Enriching event attendee lists with emails and company data, filling in missing fields in CRM exports, preparing outbound lists from raw prospect data

## AI Fields
- **What it does**: ML-powered attributes that are auto-populated during enrichment — buying role, seniority level, function/department, and gender — inferred from the contact's job title and company data
- **Availability**: Professional plan and above only
- **Key behavior**: AI Fields are automatically added to enrichment results without extra configuration; they help segment contacts by persona without manual research
- **Use cases**: Segmenting leads by buying role (decision-maker vs influencer vs user), filtering by seniority for executive outreach, routing leads to the right sales team by function/department

## Email Verifier
- **What it does**: Validates email addresses for deliverability — single lookup or bulk verification with 97% accuracy; performs syntax/format checks, domain/MX validation, and mailbox-level verification; detects webmail and disposable addresses
- **Endpoint**: `GET /v3/verify` with `email` (and optional `enrich`); bulk: `GET /v3/verify_bulk` (max 50 emails per request). Note the verifier is on the **v3** path with no `/api/` segment.
- **Verification levels**: Syntax/format check -> domain check -> MX record check -> mailbox-level check
- **Key behavior**: Returns `email_status` (e.g. `valid`, `catch-all`, `invalid`), `mailbox_status`, `mailbox_type` (`professional`/`webmail`/`temporary`), `format`, and `mailbox_exchange` (MX)
- **Credit cost**: 1 credit per verification (no charge for duplicates or previously verified emails)
- **Use cases**: Cleaning email lists before outreach campaigns, reducing bounce rates, protecting sender reputation, validating leads before CRM import

## Chrome Extension
- **What it does**: Extracts email addresses from LinkedIn profiles and Sales Navigator — processes up to 25 profiles per second; on Professional plan and above, supports multi-page enrichment (enrich entire search result pages, not just individual profiles)
- **Key features**: Single profile extraction, bulk extraction from LinkedIn search results (Pro+), auto-connect integration, list saver (save extracted contacts directly to Skrapp lists)
- **Rate**: Up to 25 profiles/sec for bulk extraction
- **Use cases**: Prospecting while browsing LinkedIn, enriching Sales Navigator saved leads, building lead lists from LinkedIn search results without leaving the browser

## Company Search
- **What it does**: Finds all professionals at a company by entering its domain — draws from a database of 40M+ company profiles to return contacts with name, title, and email
- **Key behavior**: Returns a list of known contacts at the company with available email addresses and job titles; useful for account-based selling where you need multiple contacts at a target company
- **Credit cost**: 1 credit per contact revealed
- **Use cases**: Account mapping for enterprise sales, finding multiple stakeholders at a target account, building multi-threaded outreach lists for a specific company

## Data model

| Object | Description | Key fields |
|--------|-------------|------------|
| **Contact/Lead** | Individual person record | name, email, job_title, company, domain, seniority, function |
| **Company** | Organization profile | name, domain, industry, revenue, employee_count, location |
| **List** | Collection of contacts | id, name, contact_count, created_at |
| **Email (verified)** | Validated email record | email, email_status (valid/catch-all/invalid/unknown), mailbox_status, mailbox_type (professional/webmail/temporary), mailbox_exchange |
| **Search** | Lead Finder search query | filters, result_count, created_at |
| **Enrichment Job** | Bulk enrichment operation | id, status, file_name, total_rows, enriched_rows, failed_rows |
| **AI Field** | ML-inferred attribute | buying_role, seniority, function, gender |
| **Credit** | Usage unit | type (find/verify/enrich), consumed_at, contact_id |

## API quick reference

- **Base URL**: `https://api.skrapp.io` (HTTPS only; finder/account/list under `/api/v2/...`, verifier under `/v3/...`)
- **Authentication**: HTTP Basic Auth — API key passed via `X-Access-Key` header on all requests
- **Format**: JSON responses
- **Key endpoints**:
  - `GET /api/v2/find?firstName=<>&lastName=<>&domain=<>` — find professional email from name + company/domain
  - `POST /api/v2/find_bulk` — bulk email finder (JSON array, max 100 entries)
  - `GET /v3/verify?email=<email>` — verify email deliverability (`email_status`: valid/catch-all/invalid/...)
  - `GET /v3/verify_bulk` — bulk email verification (`email` array, max 50)
  - `GET /api/v2/account` — account info and credit quota/used
  - `GET /api/v2/list/:listId` — list metadata; `GET /api/v2/list/:listId/leads` — leads (start/size pagination, max size 500)
- **Rate limits**: Not published in the official API docs — monitor via dashboard
- **API access**: Per the pricing page, "API Integration" is an Enterprise-plan feature (Professional does not include API access). The API docs phrase the gate generically as "paid accounts."
- **Docs**: API reference at `https://skrapp.io/api`

## Integrations

| Category | Tools |
|----------|-------|
| **CRM** | HubSpot, Salesforce, Zoho, Pipedrive, Outreach (native list-level sync) |
| **Automation** | Zapier (1,000+ app connections) |
| **Browser** | Chrome Extension (LinkedIn & Sales Navigator extraction) |
| **API** | REST API with HTTP Basic `X-Access-Key` header auth (Enterprise plan required) |

## Pricing (USD, verified 2026-06-13 at skrapp.io/pricing — verify current pricing before relying on it)

| Plan | Price (monthly bill / annual bill) | Credits/mo | Users | Key features |
|------|-------|-----------|-------|-------------|
| **Free** | $0 | 50 | 1 | Basic LinkedIn extraction, restricted searches, no API |
| **Professional** (Most Popular) | $39/mo billed monthly / $29/mo billed annually | 2,000 | 2 | Multi-page LinkedIn enrichment, auto-connect, list saver, unlimited searches, list CRM sync, AI enrichment, Fair Credit Policy, credits roll over — **no API** |
| **Enterprise** | $349/mo billed monthly / $262/mo billed annually | 50,000 | 15 | API Integration, SSO, dedicated account manager |

> Note: the pricing page also exposes credit-tier selectors (2K / 5K / 10K / 25K, etc.) that scale price and seats within the Professional/Enterprise tiers; third-party trackers list intermediate steps (e.g. Pro 5K, Pro 10K, Pro 20K). Prices above are the headline tiles shown on the official page.

**Key pricing notes**:
- **1 credit = 1 email found (Valid or Catch-all) or 1 email verified.** Per Skrapp's Fair Credit Policy, accounts are **not** charged for emails labeled `Invalid` or `Unknown`, and duplicates do not consume credits.
- Credits roll over month-to-month on paid plans, and the balance is kept even if you cancel.
- AI Fields are included on Professional plan and above at no extra credit cost — they are auto-populated during enrichment.
- API access ("API Integration") is restricted to the Enterprise plan — Professional plan users must use the web UI, Chrome extension, or CRM integrations.
- SSO (Single Sign-On) is Enterprise-only.
