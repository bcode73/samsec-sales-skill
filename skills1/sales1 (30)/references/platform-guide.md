# Anymail Finder Platform Guide

## Email Finder by Person
- **What it does**: Takes a person's name and company or domain, returns a verified email address with status (valid, risky, not_found, or blacklisted)
- **Endpoint**: `POST /v5.1/find-email/person` with `full_name` (or `first_name` + `last_name`) and `company_name` or `domain` in the request body. Also accepts `linkedin_url` as a fallback (name + company tried first, LinkedIn second)
- **Credit cost**: 1 credit per valid result — risky and not-found results are free
- **Key behavior**: Real-time searches can take up to 180 seconds — set your HTTP timeout accordingly. Duplicate searches within 30 days are free (not re-charged)
- **Use cases**: Finding a specific decision-maker's email when you know their name and company, building targeted outbound lists for account-based outreach

## Email Finder by Company/Domain
- **What it does**: Finds up to 20 email addresses at a given company or domain
- **Endpoint**: `POST /v5.1/find-email/company` with `company_name` or `domain`
- **Credit cost**: 1 credit per search (returns up to 20 emails)
- **Use cases**: Building prospect lists from target company domains, finding all reachable contacts at an account, enriching account records with contact emails

## Email Finder by Decision Maker
- **What it does**: Role-based email search — finds contacts by job function category at a company. Returns person name, title, LinkedIn URL, and email
- **Categories**: ceo, engineering, finance, hr, it, logistics, marketing, operations, buyer, sales
- **Endpoint**: `POST /v5.1/find-email/decision-maker` with `domain` (or `company_name`) and `decision_maker_category` (a string array, e.g. `["ceo"]` — multiple categories evaluated in order of importance)
- **Credit cost**: 2 credits per valid result (double the standard person search)
- **Use cases**: Finding the right department contact without knowing a name, account-based selling where you need to reach a specific function (e.g., "find me the head of engineering at acme.com")

## Email Finder by LinkedIn URL
- **What it does**: Extracts a verified email address from a LinkedIn profile URL
- **Endpoint**: `POST /v5.1/find-email/linkedin-url` with `linkedin_url` (note: superseded by Find Person Email, which now accepts `linkedin_url` directly, but still functional in v5.1)
- **Credit cost**: 1 credit per valid result
- **Use cases**: Converting LinkedIn prospects into contactable leads, enriching LinkedIn Sales Navigator exports with verified emails

## Email Verifier
- **What it does**: Validates an email address and returns a status of valid, risky, or invalid
- **Endpoint**: `POST /v5.1/verify-email` with `email`
- **Credit cost**: 0.2 credits per verification — repeated checks on the same email within 30 days are free
- **Use cases**: Cleaning email lists before outreach, reducing bounce rates, protecting sender reputation, validating leads before adding to CRM

## Bulk Email Search
- **What it does**: Process up to 100,000 rows per request asynchronously — supports JSON body or CSV/Excel file upload
- **Endpoint**: `POST /v5.1/bulk/json` (JSON rows) or `POST /v5.1/bulk/multipart` (CSV/Excel file upload). Check status via `GET /v5.1/bulk/{searchId}` and fetch results via `GET /v5.1/bulk/{searchId}/download`
- **Key behavior**: Async processing — approximately 1,000 rows in 5 minutes. Credits are charged only when you download results, not when you create the job. Webhook notifications via `x-webhook-url` header for completion alerts
- **Use cases**: Processing large prospect lists, batch-enriching CRM exports, high-volume email discovery campaigns

## GeoLead Finder
- **What it does**: Location-based lead discovery — find leads by geographic area
- **Endpoint**: `POST /v5.1/geo-lead` to create a search; body takes `query`, `latitude`, `longitude`, `radius_km`, `find_company_emails` (bool), `find_decision_maker_categories` (string[], `[]` to disable), optional `result_limit`/`file_name`. Free to create — credits charged on first download (same pattern as bulk jobs)
- **Use cases**: Territory-based prospecting, finding local businesses in a geographic area, location-targeted lead generation

## Chrome Extension
- **What it does**: Browser-based email finding from any website — find emails while browsing company websites or LinkedIn profiles
- **Requirement**: Requires login to anymailfinder.com in the same browser session
- **Use cases**: Prospecting while browsing target company websites, quick email lookup during research sessions, finding contact info without leaving the browser

## Domain Email Count / Order / Download
- **What it does**: Count the number of known emails at a domain, place an order for the full list, and download the results
- **Endpoints**: Count (`GET /v5.1/domain/{domain}/email` — free, returns `email_count`, `credits_required`, `status`), Order (`POST /v5.1/domain/{domain}/email/order`), Download (`GET /v5.1/domain/{domain}/email/download`). Note: ordered emails are NOT verified — validate before use
- **Use cases**: Assessing coverage at a target domain before committing credits, bulk domain email retrieval

## Report Bad Email
- **What it does**: Report an incorrect/bounced email result back to Anymail Finder for correction
- **Endpoint**: `POST /v5.1/report/bad-email` with `email` (required), `additional_info` (required), and optional `bounce_message`
- **Use cases**: Improving data quality by flagging bounced or incorrect emails, contributing to the platform's accuracy

## Data model

| Object | Description | Key fields |
|--------|-------------|------------|
| **Email** | Found or verified email | email, status (valid/risky/not_found/blacklisted), domain |
| **Person** | Contact found via decision maker or person search | name, title, linkedin_url, email |
| **Company/Domain** | Target company for email search | domain, company_name, email_count |
| **Bulk Search** | Async bulk job | id, status, total_rows, processed_rows, webhook_url |
| **GeoLead Search** | Location-based lead search | id, status, results |
| **Account** | User account details | credits_remaining, plan, api_key |

## API quick reference

- **Base URL**: `https://api.anymailfinder.com/v5.1`
- **Authentication**: `Authorization: <your-api-key>` header on all requests
- **Format**: JSON responses; all search endpoints use POST
- **Rate limits**: None — requests are queued and the system auto-scales. At high volume, requests are queued rather than rejected, so response times may increase
- **Webhook support**: Pass `x-webhook-url` header to receive async completion notifications (especially useful for bulk operations)
- **Key endpoints**:
  - `POST /v5.1/find-email/person` — find email by person name + company/domain, or by `linkedin_url` (1 credit)
  - `POST /v5.1/find-email/company` — find up to 20 emails at a company/domain (1 credit)
  - `POST /v5.1/find-email/decision-maker` — find email by `decision_maker_category` array at a domain (2 credits)
  - `POST /v5.1/find-email/linkedin-url` — find email from LinkedIn URL (1 credit; superseded by person endpoint)
  - `POST /v5.1/verify-email` — verify an email address with `email` param (0.2 credits)
  - `POST /v5.1/bulk/json` — bulk email search via JSON rows (up to 100K rows)
  - `POST /v5.1/bulk/multipart` — bulk email search via CSV/Excel file upload
  - `GET /v5.1/bulk/{searchId}` — bulk job status; `GET /v5.1/bulk/{searchId}/download` — download results
  - `POST /v5.1/geo-lead` — create a location-based GeoLead search
  - `GET /v5.1/account` — account details (`credits_left`, `email`)
  - `GET /v5.1/domain/{domain}/email` — count known emails at a domain
  - `POST /v5.1/domain/{domain}/email/order` — order full email list for a domain
  - `GET /v5.1/domain/{domain}/email/download` — download ordered domain email list
  - `POST /v5.1/report/bad-email` — report a bad email result
- **Docs**: API documentation at https://anymailfinder.com/email-finder-api/docs

## Integrations

| Category | Tools |
|----------|-------|
| **Automation** | Make.com, Zapier, n8n (7,000+ app connections via these platforms) |
| **Browser** | Chrome Extension (in-browser email lookup — requires anymailfinder.com login) |
| **API** | REST API v5.1 with API key auth — integrate with any system that can make HTTP requests |

## Pricing (EUR monthly, re-verified 2026-06-13 at https://anymailfinder.com/pricing)

Plans are now labeled by monthly credit volume — there are **no longer** named tiers ("Starter/Standard/Scale/Ultimate") and **no €14/50-credit plan**. A slider sets the credit count; representative monthly steps:

| Credits/mo | Price | ~Per credit |
|-----------|-------|-------------|
| 400 | EUR 26 | EUR 0.065 |
| 1,000 | EUR 39 | EUR 0.039 |
| 2,000 | EUR 69 | EUR 0.035 |
| 5,000 | EUR 129 | EUR 0.026 |
| 10,000 | EUR 179 | EUR 0.018 |
| 25,000 | EUR 259 | EUR 0.010 |
| 50,000 | EUR 449 | EUR 0.009 |
| 100,000 | EUR 719 | EUR 0.007 |

**Key pricing notes**:
- **Yearly billing saves ~33%** vs monthly (e.g., the 1,000-credit tier is EUR 312/yr for 12,000 credits).
- **Free trial**: 100 free credits, valid 14 days.
- **Credit costs by operation**: Person search = 1 credit, Decision Maker search = 2 credits, Email Verifier = 0.2 credits, Company/Domain search = 1 credit (up to 20 emails).
- **Free for risky/blacklisted/not-found results** — you only pay for valid emails.
- **Duplicate searches within 30 days are free** — re-searching the same person or email does not consume additional credits.
- **Credit rollover**: unused credits roll over with **no cap** while your subscription stays active; the balance keeps accumulating. If you cancel, unused credits expire at the end of the current billing cycle. (The previous "capped at 2x plan size" rule is no longer stated on the pricing page as of 2026-06-13.)
