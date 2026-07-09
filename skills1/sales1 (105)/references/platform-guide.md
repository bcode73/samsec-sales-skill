# Clearcue Platform Reference

## Overview

Clearcue is a GTM signal engine that detects real-time buying intent by monitoring person-level behavior across LinkedIn, X, Reddit, news, job postings, podcasts, and events. Unlike traditional social listening tools that track brand mentions, Clearcue tracks buying behaviors (competitor engagement, hiring signals, tech stack changes) and stacks them to identify genuine purchase intent. Target audience: B2B SaaS sales teams, revenue ops, and GTM engineers.

## Capabilities & automation surface

### Signals — API-accessible (MCP), webhook-accessible (all plans)
Real-time monitoring across 10+ data sources. Create signals using natural language descriptions of buying behaviors (e.g., "CFOs at Series B fintech companies who engage with content about payment automation"). AI qualification layer filters noise from keyword matches. Supports signal types:
- Competitor engagement (liking posts, following accounts)
- Job posting activity and hiring signals (role, seniority, location, remote/hybrid)
- Tech stack changes and tool switches
- Conference attendance and event RSVPs
- Funding announcements
- Customer complaints about competitors
- LinkedIn profile viewers and connections

### Signal Stacking — API-accessible (MCP), webhook-accessible (all plans)
Combine multiple signals with AND/OR logic. Two modes:
- **Person mode**: tracks individual-level behavior across signals
- **Company mode**: aggregates signals at the company level

Example: "Engaged with competitor content (Signal A) AND posted a job for my category (Signal B)" surfaces leads with two buying indicators vs one.

### Audiences — API-accessible (MCP)
AI-driven company intelligence using natural language ICP descriptions. Precision filtering by role, company size, industry, tech stack, behavior. Dynamic lists that auto-update as new matches are found (vs static CSVs).

### Researcher — API-accessible (MCP)
On-demand AI profile analysis for individual prospects. Generates:
- Behavioral pattern predictions
- Personalized talking points
- Outreach angles based on recent activity

### Signal Templates — UI + MCP
Pre-configured signal templates by use case:
- Competitors (who's engaging with rival content)
- Brand (your own brand mentions)
- Company Activity (funding, hiring, events)
- Sales Opportunities (buying signals)
- Conferences (event attendees matching ICP)

## Pricing, limits & plan gates

| Feature | Starter €79/mo | Pro €199/mo | Scale €439/mo | Enterprise |
|---|---|---|---|---|
| Active signals | 7 | 25 | 75 | Unlimited |
| Users | Unlimited | Unlimited | Unlimited | Unlimited |
| AI signal qualification | Yes | Yes | Yes | Yes |
| Company AI qualification | No | Yes | Yes | Yes |
| Signal stacking | Yes | Yes | Yes | Yes |
| MCP access | Yes | Yes | Yes | Yes |
| Webhooks | Yes | Yes | Yes | Yes |
| CRM integrations | No | No | Yes (HubSpot, Salesforce, Pipedrive) | Yes |
| Slack notifications | Yes | Yes | Yes | Yes |
| CSV export | Yes | Yes | Yes | Yes |
| Custom tags | Yes | Yes | Yes | Yes |
| Unlimited lists | Yes | Yes | Yes | Yes |
| Support | Email + Chat | Slack channel | Slack channel | Dedicated CSM + Priority SLA |

Monthly pricing: Starter €99, Pro €249, Scale €549.

7-day free trial with unlimited leads, no credit card required.

**Key cost considerations:**
- Flat-rate pricing with unlimited users on all plans — no per-seat cost
- "Active signals" = number of monitoring queries running, not number of results
- Webhooks and Clearcue MCP are included on ALL plans (Starter included) — no upgrade needed for programmatic push or AI-assistant access
- CRM sync locked to Scale (€439/mo) — use webhooks (any plan) or MCP as workaround on Starter/Pro
- Company AI qualification is the only Starter→Pro upgrade trigger (Starter does keyword-only matching)
- No rate limit documentation for MCP or webhooks

## Integrations

### Native connectors (data flow direction)
- **HubSpot** (Scale+): bidirectional — push leads to HubSpot, pull CRM data for qualification
- **Salesforce** (Scale+): bidirectional — same as HubSpot
- **Pipedrive** (Scale+): bidirectional — same as HubSpot
- **Salesloft** (native): push leads to sequences
- **Outreach** (native): push leads to sequences
- **HeyReach** (native): bidirectional — push lists, receive engagement data back as signals
- **Slack** (all plans): push — signal notifications to channels
- **Clay** (native): push leads for enrichment
- **Lemlist** (native): push leads to campaigns
- **Instantly** (native): push leads to campaigns

### iPaaS
No Zapier or Make support. All automation through webhooks, MCP, or native connectors.

### MCP (Model Context Protocol)
Publicly available and included on all plans (self-serve since Feb 12, 2026 — no longer "on request"). Find your MCP URL in **Settings > Integrations > Clearcue MCP** and paste it into the client's Custom Connectors; connection takes ~5 minutes. Two auth paths: paste the remote MCP URL into Custom Connectors (OAuth), or use a personal access token ("MCP token authentication," added Apr 30, 2026, as an alternative to OAuth). Works with Claude Code, Claude Desktop, ChatGPT, Perplexity, Cursor.

Capabilities via MCP:
- Create and manage signals
- Query signal results with filters
- Build and query audiences
- Run Researcher on individual profiles
- Tag and organize leads
- Access signal templates

## Data model

### Signal object
<!-- Constructed from docs — verify against live API -->
```json
{
  "id": "sig_abc123",
  "name": "Competitor engagers - LinkedIn",
  "type": "competitor_engagement",
  "status": "active",
  "qualification": "ai",
  "sensitivity": "medium",
  "created_at": "2026-05-01T10:00:00Z",
  "results_count": 142
}
```

### Lead/Result object
<!-- Constructed from docs — verify against live API -->
```json
{
  "person_id": "per_xyz789",
  "company_id": "com_def456",
  "name": "Jane Smith",
  "title": "VP Engineering",
  "company": "Acme Corp",
  "signal_type": "competitor_engagement",
  "signal_context": "Liked 3 posts from CompetitorX about payment automation",
  "signal_stack_score": 2,
  "detected_at": "2026-05-06T14:30:00Z",
  "tags": ["high-priority", "series-b"]
}
```

### Audience object
<!-- Constructed from docs — verify against live API -->
```json
{
  "id": "aud_ghi012",
  "description": "Series B+ fintech companies, 50-500 employees, using Stripe",
  "filters": {
    "funding_stage": "series_b+",
    "employee_range": "50-500",
    "industry": "fintech",
    "tech_stack": ["Stripe"]
  },
  "matched_companies": 847,
  "auto_updating": true
}
```

## Quick-start recipes

### Recipe 1: Set up competitor engagement monitoring

**Trigger:** You want to find prospects actively engaging with competitor content on LinkedIn.

**Steps:**
1. Create a signal using natural language: "People who like, comment on, or share posts from [Competitor LinkedIn Page]"
2. Enable AI qualification to filter noise
3. Set up Slack notification for new results
4. (Pro+) Configure webhook to push leads to your CRM or outreach tool

**Via MCP (Claude Code):**
```
"Show me recent signals from my competitor engagement monitoring"
"Create a signal tracking people who engage with [Competitor] posts on LinkedIn"
"Tag all leads from the competitor signal as 'warm-competitor'"
```

**Gotchas:**
- First results take 24-48 hours after signal creation
- LinkedIn engagement signals depend on public post visibility — private posts won't be tracked

### Recipe 2: Build a signal stack for high-intent leads

**Trigger:** You want to find prospects showing multiple buying indicators.

**Steps:**
1. Create Signal A: "Companies hiring [your category] roles" (e.g., "hiring payment engineers")
2. Create Signal B: "People engaging with [your topic] content on LinkedIn"
3. Create a signal stack: Signal A AND Signal B (Person mode)
4. Set Company AI qualification to filter by company size/industry

**Via MCP (Claude Code):**
```
"Show me leads that match both my hiring signal AND my competitor engagement signal"
"Which companies have the most stacked signals this week?"
```

**Gotchas:**
- Signal stacking requires at least 2 active signals — counts against your signal limit
- Person mode tracks individuals, Company mode aggregates — pick based on your sales motion (1:1 outreach vs account-based)

### Recipe 3: MCP-powered lead qualification pipeline

**Trigger:** You want Claude Code to automatically analyze and qualify Clearcue leads.

**Steps:**
1. Open Clearcue **Settings > Integrations > Clearcue MCP** to get your MCP URL (MCP is on all plans, self-serve — no support request needed)
2. Add it as a Custom Connector in Claude (paste the MCP URL), or authenticate with a personal access token
3. Query: "Show me leads who engaged with competitor content this week"
4. Ask Claude to analyze: "For each lead, write a personalized opening line based on their signal context"
5. Push qualified leads to HeyReach/Lemlist/Instantly via Clearcue's native connectors

**Example MCP queries:**
```
"Show leads who engaged with competitor content this week"
"Cross-reference: people interacting with both my and competitor content"
"Latest post engagers matching my Series B fintech audience"
"What industries and roles are most common in the last 3 weeks of engagement?"
"SaaStr Annual attendees matching my ICP"
```

**Gotchas:**
- MCP is self-serve and included on all plans (publicly available since Feb 12, 2026) — get the MCP URL from Settings > Integrations > Clearcue MCP
- Two auth paths: paste the remote MCP URL into Custom Connectors (OAuth), or use personal access token auth (added Apr 30, 2026 as an OAuth alternative) — token rotation not documented
- MCP returns data in markdown or CSV format, configurable per query

## Integration patterns

### Webhook listener (all plans)
Webhooks launched Oct 14, 2025 and are available on every plan (including Starter). The "About me" profile field is included in webhook payloads (added Feb 25, 2026). Clearcue sends POST requests when new signals match. Set up an endpoint to receive:
1. New lead detected
2. Signal stack threshold reached
3. Engagement data from HeyReach flowing back

**Retry behavior:** Not documented. Recommend building idempotent endpoints.

### CRM sync (Scale+)
Native bidirectional sync with HubSpot, Salesforce, Pipedrive:
- Push: new leads auto-create contacts/deals in CRM
- Pull: CRM data enriches Clearcue audience filtering
- Sync includes "About me" field from profiles

**Workaround for Starter/Pro:** Use webhooks (available on every plan, including Starter) to push to CRM via middleware (Clay, n8n, Make). Or use CSV export for batch updates.

### Outreach pipeline
Native connectors to Salesloft, Outreach, HeyReach, Lemlist, Instantly:
- Push Clearcue lists directly to campaigns
- HeyReach: bidirectional — engagement data flows back as new signals
- No documented API for managing these connections programmatically
