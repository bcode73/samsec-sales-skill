<!-- Source: La Growth Machine API (apiv2.lagrowthmachine.com) — auth/base-URL from the official API settings docs; operation list from the public Postman collection (documenter.getpostman.com/view/2071164/TVCmSkH2) as surfaced via Composio/MindCloud/Make/n8n integration listings (fetched 2026-06). The Postman doc is JS-rendered (not directly fetchable); confirm exact request/response JSON in the live Postman collection. -->

# La Growth Machine API Reference

## Overview

La Growth Machine (LGM) exposes an **external REST API** (plus webhooks and an emerging MCP server) so you can build custom outbound workflows — enroll leads, read campaigns/audiences/identities, and get real-time inbox events. **API + webhooks are gated to the Ultimate plan** (best-effort — verify).

## Base URL

```
https://apiv2.lagrowthmachine.com/flow
```

## Authentication

API key passed as a **query parameter** named `apikey`:

```
https://apiv2.lagrowthmachine.com/flow/leads?apikey=YOUR_API_KEY
```

Get the key from **app.lagrowthmachine.com/settings/api** (Settings → Integrations / API). Keep it server-side (it's in the query string — avoid logs/referrers).

## Core concepts

- **Identity** — a connected LinkedIn/email account that *does* the outreach, each with its own per-day **safety limits** (LGM runs cloud-based with dedicated proxies). You enroll leads to be worked by identities.
- **Audience** — a list/segment of **leads**. Campaigns run over an audience.
- **Campaign** — an automated multichannel **sequence** (LinkedIn + email + X/Twitter, with conditions/branches/A-B).
- **Lead** — a prospect (with enrichment data); has **Outcomes** (Interested / Call Booked / Negotiating / Not Interested / Won / Lost).

## Endpoints (operations)

> The API is "flow"-oriented; the operations below are confirmed via the public Postman collection + integration listings. Verify exact paths/params/JSON in the live Postman doc.

- **Leads**
  - **Add lead(s) to an audience** — `POST /flow/leads?apikey=…` — the primary write: create/enroll a lead into an audience (which a campaign then works). Body carries the lead's fields (name, email, LinkedIn URL, custom attributes) + the target audience.
  - **Search Lead** — look up a lead by criteria (e.g. email / LinkedIn URL).
- **Campaigns**
  - **Get Campaigns** — list all campaigns (paginated).
- **Audiences**
  - **List Audiences** — list all audiences in the workspace.
- **Identities**
  - **List Identities** — list connected LinkedIn/email identities (and their state/limits).
- **Webhooks (inbox)**
  - **Create Inbox Webhook** — register a URL for **real-time inbox notifications** (e.g. a lead replies).
  - **List Inbox Webhooks** — list configured inbox webhooks.

**CONSTRUCTED example — enroll a lead** (assembled from the documented `POST /flow/leads` + lead model; verify field names in the Postman collection):

```bash
curl -X POST "https://apiv2.lagrowthmachine.com/flow/leads?apikey=$LGM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audience": "AUDIENCE_ID",
    "lead": {
      "firstname": "Jane",
      "lastname": "Smith",
      "email": "jane@example.com",
      "linkedinUrl": "https://www.linkedin.com/in/janesmith",
      "attributes": { "company": "Acme" }
    }
  }'
```

## Webhooks (real-time events)

Use **inbox webhooks** to react to conversation events in real time — the canonical use case is **"create a contact in your CRM when a lead replies."** Create one via the **Create Inbox Webhook** operation (or in-app), pointing at your endpoint; LGM POSTs the event (lead + message/outcome) when it fires.

- Signature/secret: not clearly documented in public sources — treat the endpoint as a secret URL and dedupe on the lead/message id; confirm any signing in the Postman collection.
- Webhooks are an **Ultimate-plan** feature (best-effort).

## Native integrations & automation (non-API)

- **Native:** HubSpot, Clay, Make, Slack.
- **iPaaS:** Zapier, n8n, Pipedream (export/pull campaign + lead data; trigger on events).
- **MCP server** for AI agents — available/emerging (Composio toolkit exists; LGM lists it as a first-class surface alongside API + webhooks).
- **Postman collection** (authoritative endpoint reference): `https://documenter.getpostman.com/view/2071164/TVCmSkH2`.

## Notes / gaps

- The full per-endpoint request/response JSON, pagination params, rate limits, and webhook event-type catalog aren't published outside the Postman collection (JS-rendered) — pull them from Postman or `help.lagrowthmachine.com` when implementing.
- **API/webhooks require the Ultimate tier** (€150/mo, best-effort) — Basic/Pro may not expose them.
