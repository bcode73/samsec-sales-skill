# Sybill Platform Reference

## Platform overview

Sybill is an AI sales assistant that combines conversation intelligence with deal execution automation. Positioning: "context infrastructure" that learns how teams win deals — connects conversation data, maintains deal memory, and improves recommendations based on actual outcomes (won, lost, stalled). Used by 850+ revenue teams. Target audience: mid-market to enterprise sales teams ($30-90/user/mo for self-serve, custom for enterprise). Key differentiator vs Gong: Sybill centers on rep productivity (CRM autofill, follow-ups, deal workspace) while Gong centers on leadership analytics (forecasting, coaching at scale). Key differentiator vs Fathom: Sybill adds CRM Autofill, Deal Workspace, and pipeline intelligence that Fathom doesn't have.

## Key modules

### Magic Summaries
Automatic AI summaries generated after every call. Includes meeting recap, key topics, action items, and talking points. Pushed to CRM, Slack, and email automatically.
- Free plan: 20 AI summaries/month (team-wide limit)
- Pro+: Unlimited summaries

### CRM Autofill
After every call and email, Sybill extracts deal-relevant data and auto-populates CRM fields. Supports MEDDPICC, BANT, SPICED, and custom frameworks. Fields include: budget, authority, need, timeline, competitor mentions, next steps, stakeholder roles.
- **Business plan required** ($79/user/mo annual, $108 monthly)
- Business: 10 CRM fields
- Enterprise: Unlimited fields

### Ask Sybill
Natural-language queries about deals, pipeline, and rep performance. Accessible in browser, Slack, and mobile.
- Free: 10 queries/week
- Pro: Unlimited, queries across calls + email + Slack
- Business+: Adds CRM data to query context

### Deal Workspace
Pipeline views with deal health, risk signals, and activity timeline. Includes deal inspection, stakeholder mapping, and next-step tracking.
- **Business plan required**

### Pre-Meeting Briefs
AI-generated prep documents before meetings. Includes previous call history, deal status, stakeholder context, and suggested talking points.
- Available on all plans (with meeting limits on Free)

### Follow-Up Emails
AI drafts personalized follow-up emails based on call content, matching the user's communication style.
- Available on all plans

### AI Tasks
Automated task management — identifies to-dos from conversations, manages deadlines, and tracks completion.
- Credit-dependent (500/week Free, 2,500/week Pro, unlimited Business+)

### Personal Coach
Individual coaching insights and performance diagnostics.
- Business+ plans

## Pricing and limits

*Re-verified 2026-06-13 against sybill.ai/pricing. Prices below are the discounted annual-billing rate; monthly billing is higher (Pro $36/mo, Business $108/mo). Annual billing = ~34% savings.*

| Feature | Free | Pro ($30/user/mo annual, $36 monthly) | Business ($79/user/mo annual, $108 monthly) | Enterprise (custom) |
|---|---|---|---|---|
| Credits/week | 500 | 2,500 | Unlimited | Unlimited |
| AI summaries | 20/mo (team-wide) | Unlimited | Unlimited | Unlimited |
| Ask Sybill | 10/week | Unlimited | Unlimited | Unlimited |
| Ask Sybill context | Calls only | Calls + email + Slack | Calls + email + Slack + CRM | Full |
| CRM Autofill | No | No | 10 fields | Unlimited |
| Deal Workspace | No | No | Yes | Yes |
| Pipeline views | No | No | Yes | Yes |
| Admin controls | No | No | Yes | Yes |
| Custom Slack channels | No | No | Yes | Yes |
| Webhooks (automations) | No | Yes | Yes | Yes |
| API access | No | No | No | Yes |
| MCP access | No | No | No | Yes |
| Custom integrations | No | No | No | Yes |
| Data storage | 3 months | Unlimited | Unlimited | Unlimited |
| Meeting platforms | Zoom, Teams, Meet | + Webex | + Webex | + Webex |
| Custom email templates | No | Yes | Yes | Yes |

Note on gating: **Webhook automations are available on Pro and up** (pricing page shows checkmarks for Pro/Business/Enterprise). **REST API + MCP access remain Enterprise-only** per the pricing comparison, even though the developer docs (see API reference below) are now publicly published.

14-day free trial available for all paid plans.

Minimum seats: Enterprise has historically required 20+ seats (not re-confirmed on the 2026-06 pricing page — verify with sales).

## Integrations

### CRM (Business+ required for autofill)
- **Salesforce** — native, auto-updates opportunity fields, contact/company matching
- **HubSpot** — native, auto-updates deal properties, contact/company matching
- **Zoho** — CRM + Calendar + Mail + Meetings
- **Dynamics 365** — native, auto-updates
- **Netsuite** — coming soon
- **Pipedrive** — coming soon (webhook-based)

### Meeting platforms
- **Zoom** — full support including behavioral insights (Buyer EQ)
- **Microsoft Teams** — transcription + summaries (no behavioral insights)
- **Google Meet** — transcription + summaries (no behavioral insights)
- **Webex** — transcription + summaries

### Communication
- **Gmail** — drafts follow-ups, updates CRM, shares summaries
- **Outlook** — email follow-ups and CRM integration
- **Zoho Mail** — follow-up drafting and summary sharing
- **Slack** — captures internal conversations, enables Ask Sybill via Slack, custom deal channels (Business+)

### Dialers (call capture)
- **Outreach** — analyzes cold and prospect calls
- **Salesloft** — native (per integrations page, 2026-06)
- **Zoom Phone** — native (per integrations page, 2026-06)
- **Dialpad** — native (per integrations page, 2026-06)
- **Nooks** — coming soon
- **Aircall** — coming soon
- **RingCentral** — coming soon
- **HubSpot Dialer** — coming soon
- **Salesforce Dialer** — coming soon

### Automation
- **Webhooks** — push meeting insights to external apps (Pro+). Single event today: `meeting.new_recording.v1` ("New Meeting Recording"). Delivered via **Svix**, which provides **HMAC signature verification** (verify the signature + timestamp before trusting a payload) and exponential-backoff retries (immediately, then 5s, 5m, 30m, 2h, 5h, then 10h intervals). Configure under Settings → Integrations → Automations with filters by participants, topic trackers, meeting type, and deal parameters.
- **Zapier** — via webhook URL
- **Make** — via webhook URL

### AI/Developer
- **REST API** (Enterprise access; docs public at api.sybill.ai/docs) — programmatic access to conversations, deals, accounts, messages, and custom data ingestion. Currently in **alpha** (schemas/limits may change). See the API reference below.
- **Claude/MCP** — MCP server at `https://mcp.sybill.ai/mcp` (Streamable HTTP transport, OAuth sign-in). Brings Sybill deal data and reasoning into Claude, ChatGPT, Gemini, Cursor, or other agents. Tools: `ask_sybill`, `get_ask_sybill_result`, `list_conversations`, `get_conversation`, `list_deals`, `get_deal`, `list_accounts`, `get_account`. Shares REST API rate limits.
- **Mobile app** — native app for field recording and task execution

## Data model (REST API)

The REST API (docs at api.sybill.ai/docs, alpha) exposes these objects:
- **Conversation** — `conversationId`, `sourceId`, `title`, `startTime`, `endTime`, `type`, `participants`, `crm`, `category`, `summary`, `transcript`, `recordings`
- **Deal** — `dealId`, `name`, `accountName`, `stage`, `pipeline`, `amount`, `closeDate`, `closed`, `createdDate`, `lastActivityDate`, `owner`, `summary`, `crmAutofill`, `contacts`
- **Account** — `accountId`, `name`, `website`, `owner`, `createdDate`, `lastActivityDate`, `latestDeal`, `contacts`, `syncedCrmFields`
- **Message** — `messageId`, `sourceId`, `remoteId`, `threadId`, `subject`, `sender`, `recipients`, `bodyPreview`, `createdAt`, `body`, `attachments`
- **Row** / **ObjectType** — flexible structured records (custom object schemas) with `fieldDefinitions`
- **Document** — uploaded files with normalized text representations
- **Source** — logical origin grouping for ingested data

**Auth**: `Authorization: Bearer sk_live_<KEY>`. Keys created in dashboard at Settings → Integrations → API Keys; scopes are `read` (GET), `ingest` (POST/PATCH/DELETE), `ask_sybill`. See `references/sybill-api-reference.md` for full endpoint, rate-limit, and pagination detail.

## Workflow setup

### Initial setup (all plans)
1. Sign up at sybill.ai, connect calendar (Google or Microsoft)
2. Connect meeting platform (Zoom/Teams/Meet/Webex)
3. Sybill's bot will auto-join scheduled meetings
4. Configure meeting inclusion/exclusion rules to avoid joining unwanted meetings
5. (Optional) Connect email (Gmail/Outlook) for follow-up drafting
6. (Optional) Connect Slack for deal alerts and Ask Sybill

### CRM Autofill setup (Business+)
1. Connect CRM (Salesforce/HubSpot/Zoho/Dynamics) from Settings → Integrations
2. Map CRM fields to Sybill extraction categories (MEDDPICC, BANT, SPICED, or custom)
3. Configure matching rules — Sybill matches meetings to CRM records by participant email
4. Run a test: have a call, wait 5-10 min, verify fields populated in CRM
5. Iterate on field mappings based on extraction quality

### Webhook automation setup (Pro+)
1. Go to Settings → Integrations → Automations
2. Add webhook URL (must be publicly accessible HTTPS endpoint)
3. The available event is `meeting.new_recording.v1` ("New Meeting Recording"); add filters by participants, topic trackers, meeting type, or deal parameters to control which meetings fire
4. Grab the signing secret from the dashboard and **verify the Svix HMAC signature + timestamp** on every payload before trusting it (use the Svix client libraries)
5. Test with webhook.site or similar tool
6. Note: webhooks fire after processing (5-30 min after call ends, not immediately). Svix retries on failure with exponential backoff (5s → 5m → 30m → 2h → 5h → 10h)

## Deep dives

### Behavioral insights (Buyer EQ) — Zoom only
Sybill analyzes non-verbal cues (facial expressions, body language, engagement patterns) during Zoom calls. Provides buyer sentiment scores and engagement heatmaps. This feature adds ~30 minutes to processing time and is only available on Zoom — Teams and Meet don't expose the necessary video data.

**Limitations**: May miss cultural nuances and sarcasm. Potential issues with neurodivergent users. Legal considerations with EU AI Act regarding emotion/sentiment analysis in workplace settings.

### Security and compliance
- SOC 2 Type II certified
- GDPR compliant
- ISO 27001 certified
- PCI compliant
- Data encrypted in transit and at rest

### Credit system
Credits are consumed by AI operations: generating summaries, drafting follow-ups, executing tasks, running Ask Sybill queries. Free plan gets 500/week, Pro gets 2,500/week, Business+ gets unlimited. Credits reset weekly — no rollover.

### Meeting matching
Sybill matches meetings to CRM records by looking up participant email addresses against contacts in your CRM. If a participant isn't in the CRM, Sybill may not match the meeting to the right deal. Ensure key contacts are in your CRM before important calls.
