# Salesmate Platform Reference

## Overview

Salesmate is an AI-powered sales CRM and "customer platform" for SMB and mid-market teams (Rapidops,
salesmate.io). It bundles CRM (contacts/companies/deals), built-in calling + SMS, email sequences,
marketing automation, Smart Flow workflow automation, a ticketing/team inbox, and the **Sandy AI**
copilot — an affordable Pipedrive/Close/Freshsales alternative whose differentiator is native
voice/SMS plus AI baked across the funnel.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Contacts & Companies | Core records; companies own contacts | **API-accessible** (`/apis/contact/v4`, `/apis/company/v4`) + Zapier/Make |
| Deals & Pipelines | Multi-pipeline deal stages, products, followers | **API-accessible** (`/apis/deal/v4`) |
| Activities / Tasks | Calls, meetings, tasks | **API-accessible** (`/apis/activity/v4`) |
| Notes | Per-record notes, pin/unpin | **API-accessible** (`/apis/{module}/v4/.../notes`) |
| Custom modules | User-defined objects (incl. tickets/quotes) | **API-accessible** (`/apis/module/v4/{moduleId}/records`) |
| Sequences | Automated multi-step email/text outreach | UI-built; **Pro+ only**; not in public API |
| Built-in calling & SMS | Native dialer, power dialer, voicemail drop, texts | UI/app; numbers are a paid add-on (from ~$1.1/mo) |
| Marketing automation | Campaigns, lead scoring, A/B tests, segmentation | UI-built; **Pro+** |
| Smart Flow | Workflow automation (incl. "API Call/Webhook" action) | UI-built; **credits-metered** |
| Ticketing / Team Inbox | Support tickets, SLAs, shared inbox | UI; **Pro+** (SLAs Business+) |
| Sandy AI copilot / Auto-pilot | Drafting, call transcription/summary, suggestions | UI; **Pro+** |
| Meeting scheduler, web forms, quotes/products | Scheduling links, lead capture, quoting | UI; quotes/products **Pro+** |

**Webhooks:** No documented inbound API webhooks. Push events OUT via a Smart Flow "API Call/Webhook"
action, or via Zapier/Make/Pipedream "Watch …" triggers. Make a generic call with Make's "Make an API
Call" module.

## Pricing, limits & plan gates

Best-effort, per user/month, captured 2026-06 (15-day free trial on all plans):

| Plan | Price | Key gates |
|---|---|---|
| Basic | $23 | CRM, deals, email sync/tracking, meeting scheduler, web forms, **5K** smart-flow credits/mo. **No sequences, no automation, no Sandy AI.** |
| Pro (most popular) | $39 | + **Sequences**, products & quotes, ticket management, team inbox, custom dashboards, SSO, **Sandy AI included**, **10K** credits/mo. |
| Business | $63 | + deal credit split, **custom modules**, duplicate-management rules, surveys, **SLAs**, **power dialer**, voicemail drop, **15K** credits/mo. |
| Enterprise | Custom | + audit logs, IP restriction, dedicated IP, 24/7 support, dedicated account manager. Onboarding packages from $1,999. |

- **API access** ("publicly available RESTful APIs") is included across plans.
- **Rate limit: 1500 API calls/hour per link** (account), regardless of plan.
- **Calling/SMS** is a usage add-on — local numbers from ~$1.1/month, plus per-minute/per-message usage.
- **Smart Flow credits** meter automation runs; heavy automation can exhaust the monthly pool and stall flows until reset/top-up.
- Commonly cited Pro caps: ~5 active sequences and ~500 emails/day.

## Integrations

- **700+ apps**; native Google, Microsoft, Slack; Chrome extension.
- **Telephony:** built-in Salesmate calling/SMS; integrations with RingCentral and other providers
  (RingCentral call/recording logging is known to need periodic re-authorization).
- **iPaaS:** Zapier, **Make** (Watch Contacts/Companies/Deals/Activities triggers; Create/Update/Get/
  Delete modules; "Make an API Call"), Pipedream.
- **Data flow:** REST API is bidirectional (read + write contacts/companies/deals/activities/notes/
  custom records). No inbound webhooks — to update Salesmate from another app, call the REST API.

## Data model

All v4 responses use the envelope `{ "Status": "success", "Data": {…} }`. Records reference each
other by integer `id`; companies and owners embed as nested objects on a contact.

Contact (abridged Get response):
```json
{
  "id": 40, "name": "Chaitali Chouhan", "email": "", "mobile": "",
  "company": { "id": 38, "name": "test company" },
  "owner": { "id": 1, "name": "Sweta Kumari", "email": "sweta@example.com" },
  "currency": { "code": "USD", "rate": "1.00", "symbol": "$" },
  "billingCity": "", "billingState": ""
}
```

Deal (create body):
```json
{
  "title": "Bags Deal with VIP", "primaryContact": 1540, "primaryCompany": 1, "owner": 1,
  "dealValue": "7410000", "estimatedCloseDate": "2024-11-29T09:34:00Z",
  "pipeline": "Sellers", "stage": "Property Listed", "status": "Open", "currency": "USD",
  "followers": [ { "userId": 1 }, { "contactId": 3 } ]
}
```

Module IDs (used in nested note paths): Contact `1`, Task `2`, Email `3`, Deal `4`, Company `5`,
Product `6`, Team Inbox `7`.

## Quick-start recipes

### 1. Create a contact, then attach a deal (cURL)
```bash
LINK=demo.salesmate.io
H=(-H "accessToken: YOUR_ACCESS_KEY" -H "x-linkname: $LINK" -H "Content-Type: application/json")

# Create the contact
CID=$(curl -s "https://$LINK/apis/contact/v4" "${H[@]}" \
  -d '{"firstName":"Ada","lastName":"Lovelace","email":"ada@example.com","owner":1}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["Data"]["id"])')

# Create a deal linked to that contact
curl -s "https://$LINK/apis/deal/v4" "${H[@]}" \
  -d "{\"title\":\"New opp\",\"primaryContact\":$CID,\"owner\":1,\"dealValue\":\"5000\",\"pipeline\":\"Sales\",\"stage\":\"New\",\"status\":\"Open\",\"currency\":\"USD\"}"
```

### 2. Search + paginate contacts into a warehouse (Python)
```python
import requests
BASE="https://demo.salesmate.io/apis"
H={"accessToken":"YOUR_ACCESS_KEY","x-linkname":"demo.salesmate.io","Content-Type":"application/json"}

def search_page(frm, rows=250):
    body={"displayingFields":["contact.name","contact.email","contact.mobile","contact.id"],
          "filterQuery":{"group":{"operator":"AND","rules":[]}},
          "sort":{"fieldName":"contact.id","orderType":"asc"}}
    r=requests.post(f"{BASE}/contact/v4/search?rows={rows}&from={frm}",headers=H,json=body)
    r.raise_for_status()
    return r.json()["Data"]

frm, rows = 0, 250
while True:
    d=search_page(frm, rows)
    for c in d["data"]:
        ...  # upsert into your warehouse
    frm += rows
    if frm >= d["totalRows"]:
        break
```
Gotcha: pagination is **offset-based** (`from` + `rows`), not cursor; `totalRows`/`totalPages` come
back inside `Data`. Stay under **1500 calls/hour per link** — add `time.sleep` between pages.

### 3. Push a deal-won event OUT to Slack/your app
There is no inbound webhook to subscribe to programmatically. Build a **Smart Flow** on "Deal stage =
Won" with an **API Call / Webhook** action posting to your endpoint, or use the Make/Zapier "Watch
Deals" trigger. Treat the payload `id` as source of truth and re-fetch via `GET /apis/deal/v4/{id}`
for full fields.

## Integration patterns

- **Auth:** header-based API key — `accessToken` (your Access Key) + `x-linkname` (account host).
  A `401` almost always means one of those two headers is missing/wrong; a `403` means the user
  lacks access or the feature isn't enabled.
- **Versioning:** use `v4`. v1/v3 were slated for deprecation (May 2023); Products/Lookup still expose
  v1/v3 paths.
- **CRM sync:** map by integer `id`; resolve `owner`/`company` to existing IDs before writes.
  Currency must already exist on the portal (`"No such currency exists"` is a common 400).
- **Rate limits:** budget against 1500/hour per link; batch reads via search with large `rows`; cache.
