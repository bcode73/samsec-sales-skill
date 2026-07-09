# ZoomInfo Platform Guide

## SalesOS

The core prospecting and intelligence product.

### Search & Prospecting
- **Advanced Search** — filter by 300+ attributes: company size, revenue, industry, technology, location, job title, seniority, department, funding, news triggers
- **Boolean Search** — combine filters with AND/OR/NOT for precision targeting
- **Saved Searches** — save filter combinations, receive alerts when new matches appear
- **Org Charts** — visualize reporting hierarchies, identify decision-makers and buying committee members
- **News & Alerts** — track company events (funding, leadership changes, expansion) as prospecting triggers
- **Scoops** — pre-built buying signals: projects, initiatives, pain points reported by ZoomInfo's research team

### Enrichment
- **Contact Enrich** — pass partial records (name + company), get back verified email, direct dial, title, department, seniority
- **Company Enrich** — firmographic data: revenue, employee count, industry, sub-industry, SIC/NAICS codes, tech stack, location
- **Bulk Enrich** — enrich up to 25 records per API call, or use in-platform bulk operations
- **Auto-Enrich** — configure rules to enrich new CRM records automatically on creation
- **Credit system** — enrichment consumes credits; monitor via Usage API or in-platform dashboard

### Buyer Intent
- **Intent signals** — tracks 4,000+ topics across the web; surfaces companies actively researching topics relevant to your product
- **Topic configuration** — select intent topics in ZoomInfo admin; these determine which signals you receive
- **Intent scoring** — companies scored by signal strength; "Spike" indicates surge vs baseline
- **Recommended Contacts** — intent enrichment returns suggested contacts at companies showing intent
- **Alerts** — configure email/Slack alerts when target accounts show intent spikes

### Engage (Sales Engagement)
- **Sequences** — multi-step email + call + LinkedIn sequences with automated follow-up
- **Email templates** — personalization variables, A/B testing, template library
- **Dialer** — built-in power dialer with local presence, call recording, voicemail drop
- **Task management** — automated task creation for manual steps (LinkedIn, research)
- **Analytics** — open/click/reply rates, sequence performance, rep activity metrics

### Conversation Intelligence
- **Chorus** (acquired) — call recording, transcription, and AI analysis
- **Deal insights** — tracks mentions of competitors, pricing, next steps, objections
- **Coaching** — highlights talk-to-listen ratio, longest monologue, question frequency
- **CRM sync** — auto-logs call summaries and key moments to CRM records

## MarketingOS

B2B marketing-specific features.

### Advertising
- **Display ads** — target accounts across programmatic ad networks based on ZoomInfo data
- **Audience Builder** — create audiences from ZoomInfo segments: intent, firmographic, technographic
- **Cross-channel** — display, social (LinkedIn, Facebook), connected TV
- **ABM campaigns** — target specific account lists with tailored creative
- **Retargeting** — re-engage website visitors identified by WebSights

### FormComplete
- **Form shortening** — auto-fill form fields using ZoomInfo data when a visitor's email is recognized
- **Progressive profiling** — reduce form fields to 2-3; ZoomInfo enriches the rest
- **Lead capture** — even partial submissions get enriched with full contact/company data
- **Integration** — works with Marketo, HubSpot, Pardot, and custom forms

### Chat (Website Visitor Engagement)
- **Chatbot** — trigger conversations based on visitor firmographic data (identified via WebSights)
- **Routing** — route high-value visitors to the right sales rep based on territory/account ownership
- **Meeting booking** — let visitors book meetings directly from chat

### WebSights
- **Anonymous visitor ID** — identify companies visiting your website using IP-to-company matching
- **Visitor analytics** — see which pages target accounts are viewing, session frequency, time on site
- **Alerts** — get notified when target accounts visit key pages (pricing, demo, case studies)
- **Integration** — feed visitor data into CRM, marketing automation, or advertising audiences

## OperationsOS

Data management and orchestration.

### Data Orchestration
- **Workflows** — build automated data flows: when X happens → enrich → route → update CRM
- **Matching** — fuzzy match incoming records to existing CRM records before creating duplicates
- **Normalization** — standardize job titles, industries, company names across your database
- **Routing** — assign leads to reps based on territory, account ownership, round-robin, or custom rules

### CRM Hygiene
- **Deduplication** — identify and merge duplicate contacts, leads, and accounts
- **Data decay management** — flag stale records (job changes, company changes) and auto-refresh
- **Field completeness** — identify records missing critical fields and trigger enrichment
- **Compliance** — manage opt-outs and do-not-contact lists across your database

## Copilot

AI-powered sales assistant (Elite plan).

- **Next-best-action** — AI recommends which accounts to prioritize and what action to take
- **Deal predictions** — forecasts deal outcomes based on engagement signals, intent, and activity
- **Pipeline management** — surfaces at-risk deals, stalled opportunities, and buying committee gaps
- **Auto-research** — generates account briefs and talking points before meetings
- **Integration** — surfaces recommendations in CRM, email, and Engage

## Data model

| Object | Key fields | Notes |
|--------|-----------|-------|
| Contact | personId, firstName, lastName, email, phone, directPhoneDoNotCall, jobTitle, managementLevel, department, companyId | personId is the unique identifier; email may have multiple (work, personal) |
| Company | companyId, companyName, website, revenue, employeeCount, industry, subIndustry, sicCode, naicsCode, techStack | revenue and employeeCount are ranges in search, exact in enrich |
| Intent | companyId, topicId, topicName, signalScore, signalStartDate, audienceStrength | signalScore is relative to baseline; "Spike" = above normal |
| Scoops | scoopId, topicName, companyId, publishedDate, description | Pre-researched buying signals from ZoomInfo research team |
| News | newsId, companyId, headline, category, publishedDate | Categories: funding, acquisition, expansion, leadership, product launch |

## API quick reference

> **Verified 2026-06-13**: ZoomInfo's CURRENT developer API is the **GTM API** (`https://api.zoominfo.com/gtm`, OAuth 2.0). The older PKI/JWT Enterprise API is now labeled **"Legacy"** at [api-docs.zoominfo.com](https://api-docs.zoominfo.com/). Paths below are the GTM (current) paths.

| Action | Method | Endpoint (GTM, current) | Notes |
|--------|--------|----------|-------|
| Get OAuth token | POST | `/gtm/oauth/v1/token` | Client Credentials; bearer token, ~1000 s lifetime |
| Lookup search fields | GET | `/gtm/data/v1/lookup/search` | Resolve valid filter values |
| Search Contacts | POST | `/gtm/data/v1/contacts/search` | Returns IDs/hints — no emails/phones |
| Search Companies | POST | `/gtm/data/v1/companies/search` | Basic firmographics; enrich for the rest |
| Enrich Contacts | POST | `/gtm/data/v1/contacts/enrich` | Up to 25 records per call |
| Enrich Companies | POST | `/gtm/data/v1/companies/enrich` | Up to 25 records per call |
| Enrich Intent | POST | `/gtm/data/v1/intent/enrich` | Intent signals for a company |
| Search Intent/News/Scoops | POST | `/gtm/data/v1/{intent\|news\|scoops}/search` | New GTM search surfaces |
| Contact Recommendations | GET | `/gtm/data/v1/contact-recommendations` | Recommended contacts |
| Company Lookalikes | GET | `/gtm/data/v1/company-lookalikes` | Similar companies |
| Usage | GET | `/gtm/data/v1/users/current/usage` | Credit consumption tracking |
| Trigger automation/webhook run | POST | `/gtm/agent/v1/agent-teams/{id}/runs` | Agent Teams = webhook/event mechanism |

**Base URL**: `https://api.zoominfo.com/gtm` (data under `/gtm/data/v1/`, OAuth under `/gtm/oauth/v1/`, agents under `/gtm/agent/v1/`)
**Auth**: OAuth 2.0 — Client Credentials, Authorization Code w/ PKCE, or Refresh Token. Bearer access token, short-lived (~1000 s in the documented example). Register an app at [developer.zoominfo.com](https://developer.zoominfo.com).
**Rate limits**: 25 req/s default · 30 req/s Premium add-on · 35 req/s Premium+ add-on (per tenant). **Rate-limit headers are NOT returned** — on `429`, back off (exponential backoff with jitter) and honor `Retry-After` if present.
**Pagination**: `page[number]` + `page[size]` (max page size 100).
**MCP server**: `https://mcp.zoominfo.com/mcp` (OAuth Authorization Code; works with Claude Code, Cursor, Windsurf, Claude Desktop).
**Webhooks**: now documented via Agent Teams (job-complete / record-change / credit-threshold / new-signal events).

**Legacy Enterprise API** (existing integrations only): `https://api.zoominfo.com` root, PKI/username-password `POST /authenticate` → JWT (60-min lifetime), singular paths (`/search/contact`, `/enrich/contact`, `/bulk/enrich`, `/usage`), `page`/`rpp` pagination.

See `/sales-zoominfo/references/zoominfo-api-reference.md` for the full API reference.

## Integrations

| Integration | Type | What it does |
|-------------|------|-------------|
| Salesforce | Native app | Bi-directional sync: contacts, accounts, leads, opportunities. Enrich on create. View ZoomInfo data in SF. |
| HubSpot | Native | Contact/company sync, enrich on create, intent data in HubSpot, FormComplete for HubSpot forms |
| Microsoft Dynamics | Native | Contact/account sync, enrichment, intent alerts |
| Marketo | Native | Lead enrichment, audience sync for nurture, FormComplete integration |
| Pardot | Native | Lead enrichment, scoring integration |
| Salesloft | Native | Push contacts to Salesloft cadences directly from ZoomInfo |
| Outreach | Native | Push contacts to Outreach sequences from ZoomInfo |
| Slack | Native | Intent alerts, Scoops notifications, daily digests |
| Zapier | Connector | Trigger on new contacts/companies, enrich records in other tools |
| Pipedrive | Native | Contact/deal sync, enrichment |
