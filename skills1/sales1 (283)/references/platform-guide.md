# La Growth Machine Platform Guide

Full reference for the `sales-lagrowthmachine` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — the marketing site + integration listings. Verify in-account.*

## What La Growth Machine is

A **multichannel B2B outbound automation** platform (LinkedIn + email + X/Twitter, with phone steps) built for teams running **sequenced prospecting campaigns**. "Safely automating LinkedIn since 2017" — **cloud-based execution** with dedicated 5G mobile proxies and data-driven safety limits. Aimed squarely at **GTM Engineers, Sales Ops, Heads of Sales, and SDRs/AEs**.

**Execution tool, not strategy.** LGM runs the sequences; for channel-mix/timing/copy *strategy* across tools, use `/sales-cadence`.

## Core objects

| Object | What it is |
|---|---|
| **Identity** | A connected LinkedIn/email account that performs outreach; has per-day **safety limits**. Outreach volume = sum across identities. |
| **Audience** | A list/segment of **leads**. Campaigns run over an audience. |
| **Campaign** | A multichannel **sequence** (steps across LinkedIn/email/X with conditions, branches, A/B, custom variables, action limits). |
| **Lead** | A prospect + enrichment data; has an **Outcome** (Interested / Call Booked / Negotiating / Not Interested / Won / Lost). |

## Module / surface map

| Capability | Surface | Notes |
|---|---|---|
| Enroll lead → audience | **REST API** | `POST /flow/leads` (the main write) |
| Campaigns / audiences / identities | **REST API (read)** | Get Campaigns, List Audiences, List Identities |
| Sequence builder (steps, A/B, conditions) | **UI** | no create-campaign API; build in-app |
| Inbox webhooks (real-time events) | **Webhook API** | Create/List Inbox Webhooks; lead-reply events |
| Waterfall enrichment / lookalike / intent signals | **UI (+ feeds audiences)** | auto-import ICP-matching leads |
| Shared multichannel inbox | **UI** | LinkedIn + email conversations, role-based |
| AI Magic Messages / AI Voice | **UI** | AI copy + personalized voice at scale |
| Analytics | **UI + export** | per-campaign + channel stats |
| Native integrations | **HubSpot/Clay/Make/Slack** | + Zapier/n8n/Pipedream |
| MCP server | **MCP** | for AI agents (emerging/available) |

## Pricing & gating (best-effort)

Priced **per identity / month**:

| Plan | Price | Adds |
|---|---|---|
| **Basic** | ~€50/identity/mo | core multichannel sequences |
| **Pro** | ~€100/identity/mo | lookalike search, LinkedIn intent data, inbox rotation, advanced integrations |
| **Ultimate** | ~€150/identity/mo | custom sequences, **webhooks**, advanced CRM sync |

- **API + webhooks effectively need Ultimate** — confirm before building an integration.
- 14-day free trial, no card. Verify current pricing (it changes; per-identity model means cost scales with connected accounts).

## Data model (lead — JSON, constructed)

The API doc lives in the (JS-rendered) Postman collection; the lead shape is approximately:

```json
{
  "audience": "AUDIENCE_ID",
  "lead": {
    "firstname": "Jane",
    "lastname": "Smith",
    "email": "jane@example.com",
    "linkedinUrl": "https://www.linkedin.com/in/janesmith",
    "attributes": { "company": "Acme", "custom_var": "value" }
  }
}
```

Verify exact field names against the Postman collection (`documenter.getpostman.com/view/2071164/TVCmSkH2`).

## Quick-start recipes

### Recipe 1 — Enroll a lead into a campaign (API)

```bash
# 1. find the audience id (List Audiences)
curl "https://apiv2.lagrowthmachine.com/flow/audiences?apikey=$LGM_API_KEY"

# 2. enroll the lead into that audience (a launched campaign over it does the sending)
curl -X POST "https://apiv2.lagrowthmachine.com/flow/leads?apikey=$LGM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audience":"AUDIENCE_ID","lead":{"firstname":"Jane","email":"jane@example.com","linkedinUrl":"https://www.linkedin.com/in/janesmith"}}'
```

You **enroll into an audience**; there's no "send message" endpoint — the campaign sequence executes across channels. `apikey` is a query param — keep it server-side.

### Recipe 2 — Create a CRM contact when a lead replies (inbox webhook)

Use the **Create Inbox Webhook** operation (or in-app) pointing at your endpoint:

```python
@app.post("/lgm-inbox")
def lgm_inbox(payload: dict):
    # Treat this URL as a secret; confirm any signature in the Postman collection.
    lead = payload.get("lead", {})
    msg_id = payload.get("message", {}).get("id") or lead.get("id")
    if already_processed(msg_id):          # dedupe
        return {"ok": True}
    if payload.get("event") == "lead_replied":
        create_hubspot_contact(lead)
    mark_processed(msg_id)
    return {"ok": True}
```

No code? Use the native **HubSpot** integration or **Zapier/n8n** "new reply" trigger.

### Recipe 3 — Monitor identities & stay within safety limits

```bash
curl "https://apiv2.lagrowthmachine.com/flow/identities?apikey=$LGM_API_KEY"
```

Check each identity's state/limits; spread volume across identities and never push past the per-account caps (LGM sets them from years of LinkedIn-safety data). Warm up new identities slowly.

## When to route out

- Outbound **sequence/cadence strategy** (channels, timing, copy) across tools → `/sales-cadence`
- LinkedIn outreach / **social-selling strategy** → `/sales-linkedin`
- Email **warmup/deliverability** for the email channel → `/sales-deliverability`
- Generic CRM/iPaaS wiring → `/sales-integration`
