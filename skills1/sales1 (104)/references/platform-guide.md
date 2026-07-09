# Clearbit Platform Guide

## Data Model

| Entity | Key | Attributes | Source |
|--------|-----|------------|--------|
| Person | email | name, title, role, seniority, company, employment history, social profiles (LinkedIn, Twitter, GitHub), location, bio, avatar, time zone | Person API |
| Company | domain | name, legal name, industry (SIC/NAICS/GICS), sector, sub-industry, employee count, revenue range, funding (raised, stage), tech stack, type (private/public/nonprofit), location (HQ + geo), logo, social profiles, phone, description, founded year, parent company | Company API |
| Reveal | IP address | company match (domain, name, industry, employee count, revenue, location, tech stack), confidence score | Reveal API |
| Prospect | domain + filters | name, email, title, role, seniority, verified status | Prospector API |

## Person Enrichment

Look up a person by email to get 80+ attributes:

```
GET https://person.clearbit.com/v2/people/find?email={email}
```

**Streaming** (holds connection up to 60s instead of 202 queue):
```
GET https://person-stream.clearbit.com/v2/people/find?email={email}
```

**Key attributes returned**: `name.fullName`, `name.givenName`, `name.familyName`, `employment.title`, `employment.role`, `employment.seniority`, `employment.company`, `employment.domain`, `geo.city`, `geo.state`, `geo.country`, `linkedin.handle`, `twitter.handle`, `github.handle`, `avatar`, `bio`, `timeZone`

## Company Enrichment

Look up a company by domain to get 100+ firmographic attributes:

```
GET https://company.clearbit.com/v2/companies/find?domain={domain}
```

**Streaming**:
```
GET https://company-stream.clearbit.com/v2/companies/find?domain={domain}
```

**Key attributes returned**: `name`, `legalName`, `industry`, `sector`, `subIndustry`, `category.industryGroup`, `tags`, `metrics.employees`, `metrics.estimatedAnnualRevenue`, `metrics.raised`, `metrics.alexaUsRank`, `tech` (array of technologies), `type` (private/public/nonprofit/education/government), `geo`, `logo`, `url`, `phone`, `foundedYear`, `parent.domain`

## Combined Enrichment

Look up both person and company in one call:

```
GET https://person.clearbit.com/v2/combined/find?email={email}
```

Returns `{ person: {...}, company: {...} }`.

## Reveal (IP Intelligence)

Identify the company behind a website visitor's IP:

```
GET https://reveal.clearbit.com/v1/companies/find?ip={ip}
```

Returns company firmographics + a confidence score. Use for:
- De-anonymizing website traffic
- Personalizing website content by company
- Triggering sales alerts when target accounts visit
- Feeding intent models with visit data

## Prospector

Search for contacts at a company by role, seniority, title, or location:

```
GET https://prospector.clearbit.com/v1/people/search?domain={domain}
```

**Filter parameters**: `role`, `roles[]`, `seniority`, `seniorities[]`, `title`, `titles[]`, `city`, `cities[]`, `state`, `states[]`, `country`, `countries[]`, `name`, `page`, `page_size`, `suppression` (domain to exclude)

## Name to Domain

Resolve a company name to its website domain:

```
GET https://company.clearbit.com/v1/domains/find?name={company_name}
```

Returns `{ name, domain, logo }`. Useful for building prospect lists from company names without domains.

> **Access note (2026-06)**: As of the April 30, 2025 free-tools sunset, the Name to Domain API is a **customer-only API requiring a valid API key** — it is no longer available for free without an account. The `logo` field references `logo.clearbit.com`, which was **sunset Dec 8, 2025**, so logo URLs returned here no longer resolve.

## Form Shortening

Auto-populate form fields when a visitor enters their email:
1. User enters email in form field
2. JavaScript calls Person Enrichment API
3. Pre-fill company, name, title, phone fields
4. User confirms and submits shorter form

Reduces form fields from 8-10 to 1-2, improving conversion rates by 20-50%.

## Risk API

Score signups for fraud risk:

```
GET https://risk.clearbit.com/v1/calculate?email={email}&ip={ip}&name={name}
```

Returns risk score and signals (disposable email, IP proxy, new domain, etc.).

> **Access note (2026-06)**: After the April 30, 2025 free-tools sunset, the Risk API is a **customer-only API requiring a valid API key** — the previously free implementation was discontinued.

## Breeze Intelligence (HubSpot)

For HubSpot users, Clearbit is integrated as **Breeze Intelligence**:
- **Auto-enrichment** — new contacts/companies automatically enriched in HubSpot
- **Bulk enrichment** — enrich existing records in batches
- **Form shortening** — built into HubSpot forms
- **Buyer intent** — Reveal data powers HubSpot's intent features
- **40+ attributes** — firmographic, demographic, technographic data on every record

**Credit system (updated)**: Between **June 2–15, 2025**, legacy Breeze Intelligence credit packs migrated into the unified **HubSpot Credits** system. Conversion at migration: 100 Breeze Credits → 3,000 HubSpot Credits, 1,000 → 15,000, 10,000 → 125,000. Credits are now consumed from your account's monthly HubSpot Credit pool (used for data enrichment, smart properties, buyer intent, and other Breeze features), not bought as standalone Breeze "100/1,000/10,000" packs. Overage is **$0.010 per credit, invoiced in increments of 10 credits**. Included credits vary by HubSpot subscription edition (consult HubSpot's Products & Services catalog for the current per-edition amount). Credits **do not roll over** — unused credits expire at the end of each usage period. Only paid seats (Core/Sales/Service/Commerce/Partner) can use HubSpot Credits; free/view-only seats cannot. Source verified 2026-06-13.

> Historical note: the older standalone Breeze pricing of "100 credits = $45/mo, 1,000 = $150/mo, 10,000 = $700/mo" no longer reflects how Breeze Intelligence is billed after the June 2025 HubSpot Credits migration.

## API Quick Reference

| API | Base URL | Method | Key param | Status (2026-06) |
|-----|----------|--------|-----------|------------------|
| Person | `person.clearbit.com/v2/people/find` | GET | `email` | Active (legacy accounts) |
| Person (stream) | `person-stream.clearbit.com/v2/people/find` | GET | `email` | Active (legacy accounts) |
| Company | `company.clearbit.com/v2/companies/find` | GET | `domain` | Active (legacy accounts) |
| Company (stream) | `company-stream.clearbit.com/v2/companies/find` | GET | `domain` | Active (legacy accounts) |
| Combined | `person.clearbit.com/v2/combined/find` | GET | `email` | Active (legacy accounts) |
| Reveal | `reveal.clearbit.com/v1/companies/find` | GET | `ip` | Active (legacy accounts) |
| Prospector | `prospector.clearbit.com/v1/people/search` | GET | `domain` | Active (legacy accounts) |
| Name to Domain | `company.clearbit.com/v1/domains/find` | GET | `name` | Active, customer-only (API key) |
| Risk | `risk.clearbit.com/v1/calculate` | GET | `email`, `ip` | Active, customer-only (API key) |
| Autocomplete | `autocomplete.clearbit.com/v1/companies/suggest` | GET | `query` | Active, no key — but `logo` field returns null since 2025-09-09 |
| ~~Logo~~ | ~~`logo.clearbit.com/{domain}`~~ | GET | domain | **SUNSET 2025-12-08 — requests now fail; migrate to logo.dev** |

**Account access note**: Per Clearbit, free Clearbit accounts are no longer being created, and the standalone API is in maintenance/wind-down after the HubSpot acquisition. New accounts (2024+) are steered to **Breeze Intelligence inside HubSpot** rather than standalone API keys; only legacy accounts retain standalone API access.

**Auth**: HTTP Basic Auth — API key as username, empty password. Or `Authorization: Bearer {api_key}`.

**Rate limit**: 600 requests/minute per API (streaming and Reveal may differ).

## Integrations

| Integration | Type | What it does |
|-------------|------|-------------|
| HubSpot | Native (Breeze Intelligence) | Auto-enrich contacts/companies, form shortening, intent |
| Salesforce | Native | Enrich leads/contacts/accounts, create enrichment workflows |
| Segment | Native | Enrichment pushed to all connected destinations |
| Zapier | Triggers + actions | Enrich person/company on trigger, push data to 8,000+ apps |
| Make (Integromat) | Module | Clearbit enrichment in automation scenarios |
| Marketo | Native | Lead enrichment in marketing automation |
| Slack | Native (clearbit-slack) | Notify channels when target accounts visit site |
| Webhooks | API | Async enrichment delivery for queued lookups |
