# Medallia Platform Reference

## Platform overview

Medallia Experience Cloud is an enterprise-grade experience management platform that captures customer and employee signals across channels (surveys, digital, social, contact center, IoT) and uses AI-powered analytics to drive action. Acquired by Thoma Bravo in 2021. Primary target: large enterprises (12+ industries including financial services, healthcare, retail, telecom, hospitality, automotive, and public sector). Competes directly with Qualtrics XM.

## Key modules

### Customer Experience (CX)

The core module. Captures feedback via email, SMS, web, mobile, and in-app surveys. Supports NPS, CSAT, CES, and custom metrics. Key capabilities:
- **Multi-channel feedback capture** — email surveys, SMS, web intercepts, in-app, IVR, kiosk
- **Action management** — alerts, case management, closed-loop follow-up workflows
- **Role-based reporting** — executive dashboards, frontline dashboards, location-level views
- **Text analytics** — AI-powered theme extraction from open-ended responses
- **Hierarchy-based organization** — data organized by region → business unit → location → team

### Digital Experience Analytics (DXA)

Session replay, heatmaps, and digital journey scoring. Captures user behavior across web and mobile without surveys. Key capabilities:
- **Session replay** — watch individual user sessions with interaction tracking
- **Heatmaps** — click maps, scroll maps, attention maps across pages
- **Digital Experience Score (DXS)** — AI-generated score for digital journey quality
- **Error detection** — automatic identification of JavaScript errors, rage clicks, dead clicks
- **Form analytics** — field-level drop-off tracking for web forms

### Contact Center Intelligence

Analyze 100% of customer interactions (calls, chats, emails) without manual QA sampling. Key capabilities:
- **Conversational intelligence** — automated transcription and analysis of calls/chats
- **Agent coaching** — AI-identified coaching moments, best practice sharing
- **Quality management** — automated QA scoring replacing manual call monitoring
- **Intelligent Callback** (Mindful by Medallia) — virtual hold, scheduled callback, estimated wait times

### Employee Experience (EX)

Employee listening platform for engagement, pulse surveys, and lifecycle surveys. Captures employee sentiment and connects it to CX outcomes.
- **Pulse surveys** — short, frequent employee check-ins
- **Lifecycle surveys** — onboarding, exit, milestone surveys
- **Always-on listening** — continuous feedback channels beyond formal surveys
- **Employee activation** — connecting frontline employees to customer feedback for action

### Experience Orchestration

Personalized customer journeys triggered by experience signals. Combines feedback data with behavioral data to deliver individualized interactions.
- **Personalized messaging** — AI-driven two-way communication based on experience signals
- **Journey orchestration** — trigger actions based on feedback events (detractor → escalation)
- **Signal-based triggers** — combine survey responses, digital behavior, and operational data

### Market Research (Agile Research)

Pre-built survey templates for quick-turn research studies. Separate from the core CX survey engine.
- **Agile surveys** — pre-built methodologies for concept testing, brand tracking, competitive analysis
- **Video research** — online focus groups and video surveys
- **Research strategy services** — Medallia's research consultants for custom studies

### Frontline-Ready AI

AI capabilities embedded across the platform:
- **Smart Response** — AI-generated reply suggestions for customer feedback
- **Themes with GenAI** — automated theme surfacing from unstructured text
- **Root Cause Assist** — AI-identified root causes behind negative experiences
- **Intelligent Summaries** — AI-generated summaries of feedback trends

## Pricing and limits

**Pricing model**: Experience Data Records (EDRs) — priced in annual tiers. Each EDR represents a discrete customer or employee interaction (one survey response = one EDR, one contact center call = one EDR, one digital session = one EDR).

**Key characteristics**:
- Custom enterprise pricing only — no published rates, requires demo and quote
- Usage-based on EDR volume, not seats or survey count
- High total cost of ownership — license + significant professional services fees
- Professional services are a major expense — even basic configuration changes (adding touchpoints, modifying dashboards) often require Medallia consultants
- Contract typically includes implementation, ongoing managed services, and platform access

**No free tier or self-serve option.** Medallia targets mid-to-large enterprises exclusively.

**Rate limits**: 60,000 API calls per 24-hour window (all instances get at least this allocation).

## Integrations

### Native integrations
- **Salesforce** — bi-directional via AppExchange app (Medallia for Salesforce). Pushes feedback to Salesforce accounts/cases, triggers surveys from Salesforce events. Closed-loop alerting creates cases for detractor follow-up.
- **ServiceNow** — feedback integration for IT service management
- **Workday** — employee experience data integration
- **Adobe Experience Platform** — digital experience data sharing
- **Slack** — feedback alerts and notifications

### XChange marketplace
Medallia's marketplace (XChange) offers partner-built integrations and apps for additional connectors.

### API integration
REST and GraphQL APIs for custom integrations (see API reference).

### Webhooks
Supports webhooks for real-time event notifications. On creation Medallia fires a `Webhook.Created` event carrying an `X-Hook-Key` header; you must activate the webhook (`POST .../hooks/{WebhookId}/activate`) before any data flows. Validate the auth header on every delivery (HTTPS + TLS 1.2 required). Outbound calls can authenticate via OAuth 2.0, HTTP Basic, or shared-token. (Agile Research has a fuller Webhooks REST API at `api-us`/`api-eu.agileresearch.medallia.com`.)

## Data model

### Core concepts
- **Unit** — the organizational entity (a location, department, or team) that data rolls up to. Units form a hierarchy.
- **Record** — a single feedback instance (survey response, contact center interaction, digital session). Each record is an EDR.
- **Field** — a data point within a record (NPS score, comment text, channel, date).
- **Role** — defines what data and dashboards a user can access. Roles are tied to the organizational hierarchy.

### Key identifiers
- Records have unique record IDs
- Units have unit IDs organized in a tree hierarchy
- Customers are identified by email, phone, or custom ID fields
- API requests reference fields by their programmatic names (not display names)

## API overview

### REST APIs
- **Gateway base URL**: `https://{instance}-{company}.apis.medallia.com/{path}` (suffix `apis.medallia.com` is constant). Admin APIs live under `/admin/v1/<rest-api>` (e.g. `/admin/v1/users`); Import APIs live under `/inbound/...`.
- **Auth**: OAuth 2.0 (`client_credentials` grant — client ID + client secret via HTTP Basic header). Token endpoint is on the reporting-instance host: `POST https://{instance}.medallia.com/oauth/{company}/token`, returns a `Bearer` token with `expires_in: 3600`.
- **Purpose**: Object manipulation, bulk data import, user/role administration, program management
- **Import API**: Submit data under `/inbound/{version}/{importer-name}` (sync) or `/inbound/v2/async/{importer-name}` (async — returns a **feed file ID** to query status/results; opt-in feature from the 2023 Summer Release). Detailed results return up to the first 5,000 records per result status.

### GraphQL Query API
- **Endpoint**: `POST https://{instance}-{company}.apis.medallia.com/data/v0/query`
- **Auth**: OAuth 2.0 (same credentials as REST)
- **Purpose**: Real-time analytics and data extraction. Single endpoint — specify exactly what data you need.
- **Use cases**: Extract survey responses, pull analytics for reporting/data warehouse, build custom dashboards

### Rate limits
- Minimum 60,000 API calls per 24-hour window across all API types
- 10 API calls/second per API (burst/simultaneous cap, e.g. Users API, Roles API)
- Query API additionally throttles at 3,000,000 cost-units per query
- Rate-limit HTTP headers returned per IETF `draft-polli-ratelimit-headers`
- Higher limits available by contract

### SDKs and tools
- **MEC CLI** — command-line interface for interacting with Experience Cloud services (Homebrew: `brew tap medallia/mec-cli && brew install mec`; repo `medallia/mec-cli`)
- **Mobile SDKs** — iOS (Swift), Android (Kotlin) for in-app feedback and DXA
- **React Native SDK** — cross-platform mobile support for DXA
- **Query API Explorer** — built-in GraphQL explorer in the developer portal for testing queries

## Workflow setup

### Setting up a post-interaction NPS survey
1. Define the touchpoint (post-purchase, post-support, post-onboarding)
2. Configure the survey in Medallia's survey builder — NPS question + 1 open-end + optional driver questions
3. Set up the invitation rule — channel (email/SMS), timing (delay after interaction), throttling (max 1 survey per customer per 90 days)
4. Configure the data feed — connect your CRM/ticketing system to provide customer contact info and interaction data via Import API or native integration
5. Set up role-based dashboards — executive summary, location-level detail, frontline alerts
6. Configure closed-loop alerts — detractor score triggers alert to appropriate team, creates follow-up task
7. Test with internal team before launching to customers

### Connecting to Salesforce
1. Install "Medallia for Salesforce" from Salesforce AppExchange
2. Configure authentication between Medallia and Salesforce instances
3. Map Medallia fields to Salesforce object fields (Account, Contact, Case)
4. Set up feedback-to-Salesforce sync — NPS/CSAT scores pushed to account records
5. Set up Salesforce-to-Medallia triggers — case closure events trigger feedback surveys
6. Configure closed-loop alerts — detractor responses create Salesforce cases
7. Build Salesforce reports/dashboards using Medallia data fields

### Extracting data via Query API
1. Register an API application in Medallia admin → get client ID and client secret (per instance)
2. Obtain OAuth token: `POST https://{instance}.medallia.com/oauth/{company}/token` with `grant_type=client_credentials`, passing client ID/secret in the HTTP Basic header (token endpoint is on the reporting-instance host, not the API gateway)
3. Construct GraphQL query specifying fields, filters, date ranges
4. Send query to `POST https://{instance}-{company}.apis.medallia.com/data/v0/query` with the bearer token
5. Handle pagination for large result sets (cursor-based)
6. Schedule recurring exports for data warehouse loading

## Deep dives

### Medallia vs Qualtrics
| Dimension | Medallia | Qualtrics |
|---|---|---|
| **Strongest for** | Real-time action management, enterprise CX programs | Advanced survey methodology, research depth |
| **AI capabilities** | Frontline-Ready AI (Smart Response, Themes, Root Cause) | XM/discover (conversational analytics, text iQ) |
| **Digital experience** | DXA built-in (session replay, heatmaps, DXS) | Requires separate Qualtrics Digital (formerly Clarabridge) |
| **Contact center** | Strong conversational intelligence, Mindful callback | Qualtrics XM Discover for call analytics |
| **Ease of use** | Steep learning curve, consultant-heavy | Steep learning curve, more self-serve training available |
| **Pricing** | EDR-based, high TCO with consulting | Seat-based + response-based, also expensive |
| **Market position** | Gartner Leader, Forrester Leader | Gartner Leader, Forrester Leader |

### Survey design best practices in Medallia
- Keep surveys to 2-3 questions max for transactional touchpoints (NPS + open-end + driver)
- Use conditional logic to skip irrelevant questions — Medallia supports branching
- Send within 1 hour of the interaction for transactional surveys
- Relationship surveys (quarterly/annual) can be longer (8-12 questions) but test completion rates
- Use Medallia's text analytics instead of adding multiple choice questions — let customers tell you in their own words
- Survey fatigue throttling: minimum 90 days between surveys for the same customer

### DXA implementation
- Install DXA tracking script on all pages — similar to Google Analytics
- Configure session replay sampling rate (1-5% for high-traffic sites, 100% for low-traffic)
- Set up page groups for organized analysis (checkout flow, product pages, account management)
- Define custom events for key interactions (add to cart, form submission, error states)
- Use DXS (Digital Experience Score) as an aggregate metric for digital health — combines rage clicks, dead clicks, error rates, and navigation patterns
