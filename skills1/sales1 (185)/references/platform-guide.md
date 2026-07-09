# Four/Four Platform Reference

## Overview

Four/Four (fourfour.ai) is an AI **customer-research / voice-of-customer copilot** that unifies customer conversations — calls, meetings, support tickets, emails, and chat — from 30+ sources into a single searchable layer of **Insights**, then lets product, sales, marketing, and CS teams query and act on them. Differentiator: a usage-based, **no-per-seat** model and an OData REST API + MCP server, so the whole conversation corpus is queryable programmatically (PowerBI/Tableau/Excel/Claude).

## Capabilities & automation surface

| Module | What it does | Automation surface |
|--------|--------------|--------------------|
| **Discovery** | Surfaces patterns/opportunities across conversations | Insights/Topics via OData API |
| **Validation** | Evidence-backed feature prioritization | Topics/TopicModels via OData API |
| **AI Analyst** | Natural-language Q&A grounded in your customer data | UI + MCP server (`/mcp` search tools) |
| **Workflows / Automation** | Routes insights to Slack, Jira, email via visual builder | UI-configured; webhook-accessible outputs |
| **Competitive Intelligence** | Tracks competitor mentions, links to deal outcomes | Insights/Topics via OData API |
| **Customer Success** | Account-health monitoring, churn prediction | CRM entities via OData API |
| **Meeting Notetaker** (AI Researcher plan) | Records/transcribes Teams, Zoom, Google Meet | UI; output flows into Conversations |
| **CRM sync** | Pull insights to CRM; push CRM records in | OData API (read) + CRM Importer API (write) + native connectors |

API-accessible: Insights, Topics, TopicModels, Conversations, Participants, CRM objects (Accounts/Contacts/Leads/Opportunities/Owners/Cases/Calls/CalendarEvents), Tracker* objects, Chats/ChatMessages/Fragments — all read via OData. Webhook-accessible: change events (`{timestamp, event, tenant, payload}`, HMAC-SHA256 signed). Write path: CRM Importer API (CSV upsert) for account/contact/lead/opportunity/user. UI-only: the visual workflow builder and notetaker configuration.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — confirm in-account.*

| Plan | Price | For | Includes | Usage limits |
|------|-------|-----|----------|--------------|
| **AI Analyst** | £199/mo (billed annually) | Companies up to 50 employees | AI Analyst, Workflows, Monitor, topic sets, 2 integrations | 50 hrs meeting recording/mo, 50 hrs conversation processing/mo, 100 support tickets/mo |
| **AI Researcher** | £250/mo (billed annually) | Companies up to 50 employees | Everything in AI Analyst + Meeting Notetaker (Teams/Zoom/Google Meet) | same as above |
| **Enterprise** | Custom | Larger orgs | Unlimited recording hours, embedded CRM apps, predictive analytics, custom reports, dedicated AI-prompting support | Unlimited |

- **Pricing is usage-based (content processed), not per-seat** — all plans include unlimited team access; you pay for hours/tickets processed, not seats.
- All plans include AI Analyst, Workflows, Monitor, and 40+ integrations available; paid plans get free trials (AI Analyst, AI Researcher); Enterprise is contact-sales.
- **Integration count is plan-gated** — entry plans cap at 2 active integrations even though 40+ exist.
- API/webhook access and BI connectivity are available across plans; some embedded-CRM-app and predictive-analytics features are Enterprise-only.

## Integrations

30+ platforms. Data-flow direction matters:

- **Reads conversations FROM:** Zoom, Microsoft Teams, Google Meet, Gong, Chorus, Fireflies, Aircall, Intercom, Zendesk, Pylon, Slack.
- **Reads/writes CRM (bidirectional):** Salesforce, HubSpot, Dynamics 365 (via native connectors + the OData read API and CRM Importer write API).
- **Pushes insights TO:** Slack, Jira, Productboard, email (via Workflows), plus webhooks to any endpoint.
- **BI / analytics:** PowerBI, Tableau, Excel, Databox, Clari, Planhat (OData feeds).
- **AI surfaces:** Claude, ChatGPT, Cursor (via the MCP server).
- **iPaaS:** Zapier; plus Outreach, Google Workspace, Microsoft 365.

## Data model

Conversations are the raw input; **Insights** are the atomic extracted findings, grouped into **Topics**, which roll up into **TopicModels**. Insights link to **Participants** and to CRM objects (Accounts/Contacts/Opportunities), which is how voice-of-customer ties back to revenue.

```json
<!-- Constructed from docs — verify against live API -->
{
  "Conversation": { "id": "cnv_9c0", "source": "zoom", "participants": ["par_1","par_2"], "accountId": "acc_771" },
  "Insight":      { "id": "ins_8f31", "text": "Wants SSO before expanding", "topicId": "top_22a", "conversationId": "cnv_9c0", "accountId": "acc_771" },
  "Topic":        { "id": "top_22a", "name": "Security & SSO", "insightCount": 47 },
  "TopicModel":   { "id": "tm_5", "name": "Q2 churn drivers", "topics": ["top_22a","top_19b"] }
}
```

OData response envelope: `{ "@odata.nextLink": "...", "@count": n, "value": [ ... ] }`.

## Quick-start recipes

### Recipe 1 — Pull this quarter's insights into a warehouse (developer)

Trigger: nightly sync. Steps: OAuth2 client-credentials/refresh → page `Insights` with `$top`/`$skip` and `$filter` → land in your warehouse.

```bash
# token (authorization-code already exchanged; refresh as needed)
curl 'https://fourfour.ai/odata/Insights?$top=100&$filter=created ge 2026-04-01T00:00:00Z&$orderby=created desc' \
  -H 'Authorization: Bearer {access_token}'
```

```python
import requests
def fetch_insights(token, since):
    url = "https://fourfour.ai/odata/Insights"
    params = {"$top": 100, "$filter": f"created ge {since}", "$orderby": "created desc"}
    out, headers = [], {"Authorization": f"Bearer {token}"}
    while url:
        r = requests.get(url, params=params, headers=headers).json()
        out += r.get("value", [])
        url, params = r.get("@odata.nextLink"), None  # nextLink carries paging
    return out
```

Gotcha: follow `@odata.nextLink` until absent; don't assume you got everything from page one.

### Recipe 2 — Push CRM accounts so insights link to deals (developer)

Trigger: CRM account created. Upsert via the Importer API (CSV, async), then poll the job.

```bash
curl -X PUT https://fourfour.ai/import/crm/account \
  -H 'Authorization: Bearer {pat}' -H 'Content-Type: text/csv' \
  --data-binary $'id,name,website,industry\nacc_771,Acme Inc,acme.example,Software'
# -> {"jobId":"job_5a2c","status":"queued"}; poll /import/job/job_5a2c until completed
```

Gotcha: CSV needs a required `id` column; dates are ISO 8601 UTC; writes are asynchronous — confirm via the job, don't assume immediate.

### Recipe 3 — React to new insights via signed webhook

Trigger: `insight.created`. Verify HMAC, then route into your tooling.

```python
import hmac, hashlib
def verify(raw, sig, secret):
    return hmac.compare_digest(hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest(), sig)
# payload: {"timestamp","event","tenant","payload":{...}}
```

Gotcha: signature is HMAC-SHA256 over the **raw** body in the `Signature` header; return 2xx fast or Four/Four retries 3x with backoff.

## Integration patterns

- **CRM sync:** read insights/accounts via OData; write CRM records via the Importer API (CSV upsert keyed on `id`). For ongoing freshness, prefer webhooks over polling the OData feed; reconcile with a nightly full pull.
- **Webhook listener:** verify HMAC-SHA256 (`Signature` header) over raw bytes, dedupe on `payload.id` + `timestamp`, ack 2xx immediately, process async. Expect up to 3 retries on failure.
- **MCP-first:** for Claude/Cursor workflows, add `https://fourfour.ai/mcp` as a remote MCP server and let the AI Analyst tools search conversations/insights/accounts/contacts — no token plumbing beyond the OAuth prompt.
- **BI feeds:** point PowerBI/Tableau/Excel at `/odata` with Basic or OAuth; the OData metadata document drives the schema.
