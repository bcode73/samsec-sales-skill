---
name: sales-zoominfo
description: "ZoomInfo platform help — SalesOS, MarketingOS, OperationsOS, Copilot, API, integrations. Use when ZoomInfo searches aren't returning the right prospects, enrichment data is incomplete or stale, intent signals aren't surfacing target accounts, Engage sequences have low reply rates, advertising audiences aren't matching your ICP, FormComplete isn't auto-filling leads, data orchestration rules aren't firing, or Copilot recommendations seem off. Do NOT use for general enrichment strategy (use /sales-enrich), general intent strategy (use /sales-intent), general cadence design (use /sales-cadence), general data hygiene strategy (use /sales-data-hygiene), or general B2B advertising strategy (use /sales-b2b-advertising)."
argument-hint: "[describe what you need help with in ZoomInfo]"
license: MIT
version: 1.0.0
tags: [sales, enrichment, intent-data, prospecting, platform]
github: "https://github.com/Zoominfo"
---
# ZoomInfo Platform Help

Help the user with ZoomInfo platform questions — SalesOS (prospecting, enrichment, intent, org charts, Engage sequences, conversation intelligence), MarketingOS (B2B advertising, FormComplete, website chat), OperationsOS (data orchestration, CRM hygiene, deduplication), Copilot (AI pipeline management), and API integration.

## Step 1 — Gather context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user:

1. **Which ZoomInfo product are you working with?**
   - A) SalesOS — prospecting, enrichment, Engage sequences
   - B) MarketingOS — advertising, FormComplete, chat
   - C) OperationsOS — data orchestration, CRM hygiene
   - D) Copilot — AI-assisted pipeline management
   - E) API — building custom integrations
   - F) Not sure / multiple areas

2. **What's your role?**
   - A) Sales rep or SDR
   - B) Sales manager or director
   - C) Marketing / demand gen
   - D) Rev ops / sales ops
   - E) Developer / engineer
   - F) Admin configuring ZoomInfo

3. **What are you trying to accomplish?**
   - A) Find and export prospect lists
   - B) Enrich existing CRM records
   - C) Set up buyer intent alerts
   - D) Build outbound sequences (Engage)
   - E) Configure advertising audiences
   - F) Clean up / deduplicate CRM data
   - G) Integrate ZoomInfo with CRM or other tools
   - H) Use the API programmatically
   - I) Something else — describe it

## Step 2 — Route or answer directly

If the question is about **strategy** rather than ZoomInfo-specific configuration, hand off to the appropriate skill:

- General enrichment strategy → `/sales-enrich`
- Buying intent interpretation → `/sales-intent`
- Multi-channel cadence design → `/sales-cadence`
- Account mapping strategy → `/sales-account-map`
- CRM data quality strategy → `/sales-data-hygiene`
- B2B advertising strategy → `/sales-b2b-advertising`
- Call coaching methodology → `/sales-call-review`
- Lead routing rules → `/sales-lead-routing`
- Prospect list strategy → `/sales-prospect-list`
- Tool integrations → `/sales-integration`

If the question is ZoomInfo-specific, answer directly using the reference below.

## Step 3 — ZoomInfo platform reference

**Read `references/platform-guide.md`** for detailed module documentation, pricing, integrations, and data model.

*You no longer need the platform guide details — focus on the user's specific situation.*

## Step 4 — Actionable guidance

Based on the user's goal, provide step-by-step instructions:

### For prospecting (finding new leads)
1. Define your ICP using Advanced Search filters (industry, employee count, revenue, technology)
2. Layer intent signals — filter for companies showing intent on your topics
3. Use Org Charts to identify the buying committee (economic buyer, champion, technical evaluator)
4. Export to CRM or push directly to Engage/Salesloft/Outreach sequences
5. Set up Saved Searches with alerts for new matches

### For enrichment
1. Identify records to enrich (new leads, stale contacts, incomplete accounts)
2. Choose enrichment method: manual (in-platform), bulk (CSV upload), auto (rules-based), or API
3. Map enrichment fields to CRM fields before running bulk operations
4. Monitor credit usage — enrichment consumes credits per record
5. Set up auto-enrich rules for ongoing data freshness

### For intent-based selling
1. Configure your intent topics in ZoomInfo admin (align with your product's problem spaces)
2. Create a Saved Search filtered by intent spike + your ICP criteria
3. Set up Slack/email alerts for target account intent spikes
4. Use Recommended Contacts to find the right people at spiking accounts
5. Trigger Engage sequences or push to your sales engagement platform

### For advertising (MarketingOS)
1. Build audience segments using firmographic + intent + technographic filters
2. Create campaigns targeting those audiences across display, LinkedIn, Facebook
3. Set up WebSights to track which target accounts visit your site after seeing ads
4. Retarget engaged visitors with bottom-of-funnel creative
5. Measure with ZoomInfo attribution — which accounts progressed after ad exposure

### For data orchestration (OperationsOS)
1. Audit current CRM data quality — field completeness, duplicate rate, decay rate
2. Set up matching rules to prevent future duplicates
3. Configure normalization rules for job titles, industries, company names
4. Build enrichment workflows: new record → match → enrich → route
5. Schedule recurring data hygiene jobs (monthly dedup, quarterly refresh)

## Gotchas

*Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

1. **Intent topics are subscription-dependent** — you only receive intent signals for topics configured in your ZoomInfo account. If a user asks about intent data they're not seeing, check their topic configuration first — the API won't return topics that aren't in their subscription.

2. **Credit system is complex** — different actions consume different credit amounts (Search and Lookup are free; Enrich spends 1 bulk credit per new record; Research/Account-summary spend AI action credits). Bulk operations can burn through credits fast. **Rate-limit headers are NOT returned** by the current GTM API — check the Usage API (`GET /gtm/data/v1/users/current/usage`) before large operations rather than relying on response headers.

3. **OAuth access tokens are short-lived** — the CURRENT GTM API uses OAuth 2.0 (Client Credentials / Auth Code+PKCE / Refresh Token) with a short-lived bearer token (~1000 s in ZoomInfo's documented example), NOT the legacy PKI/JWT `/authenticate` 60-minute token. API integrations MUST handle token refresh; a common failure mode is hardcoding a token and having it silently expire. Implement auto-refresh. (The legacy Enterprise API's PKI/JWT 60-min token still exists at api-docs.zoominfo.com but is labeled "Legacy".)

4. **Copilot is Elite-only** — AI features (next-best-action, deal predictions, auto-research) require the Elite plan (~$39,995/yr). Don't recommend Copilot features to users who may be on Professional or Advanced plans.

5. **WebSights identifies companies, not individuals** — IP-to-company matching reveals the organization, not the specific person. Users sometimes expect individual visitor identification. Pair WebSights with Contact Search to find the right people at identified companies.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Step 5 — Related skills

- `/sales-enrich` — enrichment strategy across all providers, waterfall enrichment
- `/sales-intent` — interpreting buying signals and prioritizing accounts
- `/sales-account-map` — mapping buying committees and org charts
- `/sales-cadence` — designing multi-channel outbound sequences
- `/sales-call-review` — coaching from recorded sales calls
- `/sales-live-chat` — website chat strategy and implementation
- `/sales-data-hygiene` — CRM data quality, deduplication, and data decay management
- `/sales-b2b-advertising` — account-based advertising strategy across platforms
- `/sales-prospect-list` — building targeted prospect lists
- `/sales-integration` — connecting ZoomInfo to CRM and other tools
- `/sales-lead-routing` — lead assignment and territory rules
- `/sales-deliverability` — email deliverability for Engage sequences
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Setting up intent-based prospecting
**User says**: "I want to find companies showing buying intent for cybersecurity solutions and get the right contacts there"
**Skill does**: Walks through configuring intent topics (endpoint security, SIEM, zero trust, etc.), building a Saved Search with ICP filters + intent spike, using Recommended Contacts to find security decision-makers, and setting up Slack alerts for new spikes.
**Result**: User has an intent-triggered prospecting workflow that surfaces in-market accounts with the right contacts.

### Example 2: Bulk CRM enrichment
**User says**: "We have 15,000 contacts in Salesforce with missing phone numbers and stale job titles. How do I clean this up in ZoomInfo?"
**Skill does**: Recommends OperationsOS data orchestration approach — export stale records, run bulk enrichment via API or in-platform, map fields back to Salesforce, set up auto-enrich rules for ongoing freshness. Warns about credit consumption at scale.
**Result**: User has a plan to refresh 15K records and prevent future data decay.

### Example 3: API integration for custom enrichment
**User says**: "I'm building a lead scoring system and need to pull ZoomInfo data via API whenever a new lead comes in"
**Skill does**: Provides API authentication setup (OAuth 2.0 Client Credentials → bearer token from `/gtm/oauth/v1/token`), shows the Enrich Contacts endpoint (`POST /gtm/data/v1/contacts/enrich`) with request/response format, explains credit implications, recommends implementing token-refresh logic and 429 backoff handling.
**Result**: User has working API integration code for real-time lead enrichment.

## Troubleshooting

### Intent data not showing for target accounts
**Symptom**: User configured intent topics but isn't seeing signals for accounts they expect
**Cause**: Intent topics must match ZoomInfo's taxonomy exactly. Also, small companies may not generate enough web activity to trigger intent signals.
**Solution**: Review intent topic configuration in ZoomInfo admin. Check that topics align with ZoomInfo's available taxonomy (4,000+ topics). For small companies, use Scoops and News alerts as supplementary buying signals instead of relying solely on intent.

### API returns 401 after working initially
**Symptom**: API calls that were working suddenly return 401 Unauthorized
**Cause**: OAuth access token expired (short-lived — ~1000 s in ZoomInfo's documented example; the legacy PKI/JWT token lasted 60 min)
**Solution**: Implement token-refresh logic. On the current GTM API, re-request a token from `POST /gtm/oauth/v1/token` (Client Credentials) or use the Refresh Token flow before `expires_in` elapses. For server-to-server automation, use the Client Credentials flow with the `client_id`/`client_secret` from an app registered at developer.zoominfo.com. 401 is non-retryable — re-auth and retry once.

### Enrichment returning incomplete data
**Symptom**: Bulk enrichment returns records with missing fields (no phone, no email)
**Cause**: ZoomInfo's coverage varies by contact — not every person has a verified direct dial or email. Also, some fields are plan-gated.
**Solution**: Check your plan's data access level. For missing contacts, use waterfall enrichment (ZoomInfo → Apollo → Lusha) via `/sales-enrich`. For missing company data, try the Company Enrich endpoint with the company's domain as the identifier (higher match rate than company name).
