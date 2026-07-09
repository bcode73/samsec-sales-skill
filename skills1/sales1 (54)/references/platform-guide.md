# Bitrix24 Platform Guide

Full reference for the `sales-bitrix24` skill. Read the section you need; don't dump the whole file.

> *Pricing/features are best-effort from research (2026-06) — the marketing site + API docs. Verify in-account.*

## What Bitrix24 is

A **free-forever all-in-one business suite** (CRM + tasks/projects + contact center + sites/store + marketing + collaboration + HR/automation), cloud or **self-hosted on-prem**. Its hook is **unlimited users on the free plan**, which makes it a popular free **Keap / Ontraport / Zoho / HubSpot-free alternative** for solo founders and SMBs (it also scales to enterprise). The CRM (leads, deals, pipelines, Smart Process Automation) is the sales-relevant core.

**It's a suite, not a focused CRM.** Breadth = power + a learning curve. For a *which-CRM* decision, use `/sales-crm-selection`.

## Module map (CRM-relevant first)

| Module | Surface | Notes |
|---|---|---|
| CRM — leads/deals/contacts/companies | **REST `crm.*` methods** | add/update/get/list/delete/fields per entity |
| Pipelines & stages | **REST** | `crm.dealcategory.*` (funnels) + `crm.status.*` (stages) |
| Smart Process Automation (custom objects) | **REST `crm.item.*`** | `entityTypeId`-scoped custom CRM entities |
| CRM automation / triggers / robots | **UI + REST** | workflow automation in CRM |
| Activities / products / invoices | **REST** | `crm.activity.*`, `crm.product.*` |
| Contact center (omnichannel) | **UI + partial REST** | web forms, live chat, WhatsApp/IG, telephony, email |
| Tasks & projects | **REST `tasks.*`** | Gantt, Scrum |
| Sites & store builder | **UI** | landing pages, online store |
| Marketing (email/SMS/ads) | **UI** | campaigns |
| Events (changes) | **Outbound webhooks** | `ONCRM*` events |
| 740+ integrations | **Market** | prebuilt apps |
| AI tools | **MCP server** | external AI integration |

## Pricing & hosting (best-effort)

- **Free** — forever, **unlimited users**, core CRM + tasks + contact center + collaboration (with feature/usage caps).
- **Paid (cloud)** — typically **Basic / Standard / Professional / Enterprise**, priced per-plan with a **fixed user cap per tier** (not strictly per-seat), unlocking more automation, SPA, storage, and throughput.
- **On-Premise (Self-Hosted)** — one-time/owned license, you host it; more control + source access; **outbound webhooks need an active license**.

Confirm current tier names/limits on the pricing page — Bitrix24 changes them.

## CRM data model (JSON shapes)

**Deal** (`crm.deal.add` FIELDS):

```json
{
  "TITLE": "Acme — annual plan",
  "CATEGORY_ID": 0,            // pipeline/funnel id
  "STAGE_ID": "PREPARATION",   // crm_status within that funnel
  "CURRENCY_ID": "USD",
  "OPPORTUNITY": 12000,         // amount
  "CONTACT_IDS": [84, 83],
  "COMPANY_ID": 17,
  "ASSIGNED_BY_ID": 1,
  "CLOSEDATE": "2026-07-31",
  "SOURCE_ID": "WEB"
}
```

Add response: `{ "result": 394, "time": {…} }` — `result` is the new deal id.

**Lead** (`crm.lead.add`): `TITLE`, `NAME`, `STATUS_ID`, `OPPORTUNITY`, `ASSIGNED_BY_ID`, `SOURCE_ID`, and multi-fields `PHONE`/`EMAIL` as `[{ "VALUE": "...", "VALUE_TYPE": "WORK" }]`.

**Outbound event** payload: `{ "event": "ONCRMDEALUPDATE", "data": { "FIELDS": { "ID": 662 } } }` — ID only; re-fetch with `crm.deal.get`.

## Quick-start recipes

### Recipe 1 — Create a deal in a specific pipeline (inbound webhook)

```bash
# webhook URL from: Applications -> Developer resources -> Incoming webhook (scope: CRM)
curl -X POST -H "Content-Type: application/json" \
  -d '{"FIELDS":{"TITLE":"Website lead","CATEGORY_ID":0,"STAGE_ID":"NEW","OPPORTUNITY":5000,"CURRENCY_ID":"USD","CONTACT_IDS":[84],"ASSIGNED_BY_ID":1}}' \
  "https://yourportal.bitrix24.com/rest/1/$WEBHOOK_CODE/crm.deal.add"
```

Python (look up the funnel/stage first):

```python
import requests
BASE = f"https://yourportal.bitrix24.com/rest/1/{WEBHOOK_CODE}"
funnels = requests.get(f"{BASE}/crm.dealcategory.list").json()["result"]   # valid CATEGORY_IDs
deal = requests.post(f"{BASE}/crm.deal.add", json={
    "FIELDS": {"TITLE": "Website lead", "CATEGORY_ID": 0, "STAGE_ID": "NEW",
               "OPPORTUNITY": 5000, "CONTACT_IDS": [84], "ASSIGNED_BY_ID": 1}}).json()
deal_id = deal["result"]
```

### Recipe 2 — Get notified when a deal changes (outbound webhook)

Developer resources → **Outgoing webhook** → handler URL + event `ONCRMDEALUPDATE`. Handler:

```python
@app.post("/bx24-event")
def bx24_event(form):
    if form["auth[application_token]"] != BX24_OUT_TOKEN:   # verify the token
        return Response(status_code=401)
    deal_id = form["data[FIELDS][ID]"]
    if already_processed(deal_id):                          # dedupe
        return {"ok": True}
    deal = requests.get(f"{BASE}/crm.deal.get", params={"ID": deal_id}).json()["result"]
    sync(deal)
    return {"ok": True}
```

### Recipe 3 — Batch to avoid rate limits

```bash
# one request, up to 50 commands; chain with $result[...]
curl -X POST "https://yourportal.bitrix24.com/rest/1/$WEBHOOK_CODE/batch" \
  -d 'halt=0' \
  --data-urlencode 'cmd[add_contact]=crm.contact.add?fields[NAME]=Jane' \
  --data-urlencode 'cmd[add_deal]=crm.deal.add?fields[TITLE]=Jane deal&fields[CONTACT_IDS][]=$result[add_contact]'
```

Bitrix24 throttles (~2 req/sec + per-method operating-time limits) — `batch`, page `*.list` via `start`, and back off on errors.

## When to route out

- **Choosing** a CRM across vendors (Bitrix24 vs HubSpot/Pipedrive/Zoho/Keap) → `/sales-crm-selection`
- CRM/RevOps **strategy** (pipeline design, forecasting, hygiene) → `/sales-crm`
- Generic iPaaS wiring → `/sales-integration`
