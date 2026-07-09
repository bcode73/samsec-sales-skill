# EngageBay Platform Reference

## Overview

EngageBay is an all-in-one CRM + marketing + sales + service suite built for startups and small businesses — positioned as "HubSpot power at a fraction of the cost." It bundles three modules (Marketing Bay, Sales & CRM Bay, Service Bay) on one shared contact database, with a free tier and per-user/per-contact paid plans. Buy the modules separately or as the All-in-One Suite.

## Capabilities & automation surface

| Module / capability | What it does | Automation surface |
|---|---|---|
| **Sales & CRM Bay** — contacts, companies, deals, tasks, notes, products | Pipeline (deals on "tracks"/milestones), lead scoring, appointment scheduling, email tracking, call logs | **API-accessible** (contacts, companies, deals, tracks, tasks, notes, products, owners, custom fields) + **webhook-accessible** (outbound on contact/company/deal create/update/delete) |
| **Marketing Bay** — email campaigns, automations, landing pages, forms, broadcasts | Drag-and-drop email sequences, web forms, landing pages with A/B testing, SMS, push, drip campaigns | Mixed: lists, forms, sequences, broadcasts are **API-accessible** (add contact to form/list/sequence; create broadcast); the visual automation/landing-page builders are **UI-only**. Email open / link-click / reply fire **outbound webhooks** |
| **Service Bay** — helpdesk tickets, live chat, canned responses | Ticketing with status/priority/groups, automation workflows, AI chatbot trained on a knowledge base | **API-accessible** (list/create/delete tickets, filter tickets) |
| **Tags / lists / sequences** | Segmentation and enrollment | **API-accessible** (add/remove tags, add to list, add to sequence) |
| **Custom fields** | Extend contacts/deals/companies | **API-accessible** (list, create, delete) — every API write to a custom field must include `field_type` |

**Terminology:** contacts (a.k.a. "subscribers" in API paths), companies, deals, **tracks** = pipelines and **milestones** = stages, tasks, sequences (automation/drip), broadcasts (one-off email blasts), tickets, owners (users).

## Pricing, limits & plan gates

*Best-effort, captured 2026-06; All-in-One Suite, billed per user. Verify on the live pricing page.*

| Plan | ~Monthly (per user) | Contacts | Key gates |
|---|---|---|---|
| **Free** | $0 | 250 | 1 landing page, 2 email sequences, basic lead scoring, low API quota |
| **Basic** | ~$14.99 | 500 | up to 10 landing pages, 10 forms, 15 calling credits |
| **Growth** | ~$64.99 | 5,000 | up to 50 landing pages, 10 automations, 50 email lists |
| **Pro** | ~$119.99 | 50,000 | unlimited landing pages, 50 automation nodes, **~750,000 API calls/month** |

- **The API and webhooks are available across plans, but the monthly API-call quota is plan-gated** — a high-volume sync can exhaust the lower tiers and start returning `429`. Budget calls and cache.
- Pricing is per-user *and* contact-capped, so both seats and list growth raise the bill. Marketing Bay and CRM Bay can be bought standalone for less than the full suite.
- Yearly and biennial billing discount the monthly rate (~8% and ~15%).

## Integrations

- **Direction:** The REST API is bidirectional for core CRM objects (read + write contacts/companies/deals/tasks/tickets/products). **Webhooks are outbound only** — EngageBay pushes events out; it does **not** accept incoming webhooks, so all writes into EngageBay go through the REST API.
- **Native connectors:** SendGrid, Mailgun, Mandrill, Amazon SES (email sending), Shopify, Stripe, Xero, QuickBooks, Zapier (250+ apps), Make/Pipedream.
- **SDKs:** REST plus Java, .NET, JavaScript, and PHP wrappers (docs on the `engagebay/` GitHub org).
- **SSO + Tracking Code API** for website behavior capture.

## Data model

IDs are large integers (Google Datastore-style). Contacts are addressed as `subscribers` in API paths. Properties are an array of `{name, value, field_type, type}` objects where `type` is `SYSTEM` or `CUSTOM`.

**Contact (subscriber):**
```json
{
  "id": 4997280348241920,
  "owner_id": 6192449487634432,
  "name": "Test Contact",
  "email": "testcontact@gmail.com",
  "score": 5,
  "status": "CONFIRMED",
  "companyIds": [5278755324952576],
  "properties": [
    { "name": "name",  "value": "Test Contact", "field_type": "TEXT", "type": "SYSTEM" },
    { "name": "email", "value": "testcontact@gmail.com", "field_type": "TEXT", "type": "SYSTEM" },
    { "name": "phone", "value": "+91 9999999999", "field_type": "TEXT", "type": "SYSTEM" }
  ],
  "tags": [ { "tag": "United States", "assigned_time": 1535538585 } ]
}
```

**Deal** (`track_id` = pipeline, `milestoneLabelName` = stage — both **case-sensitive**, must match account exactly):
```json
{
  "id": 5088020441071616,
  "name": "sample deal",
  "amount": 100.0,
  "track_id": 5697266736168960,
  "milestoneLabelName": "New",
  "currency_type": "USD-$",
  "owner": { "id": 5676618345349120, "email": "rep@example.com", "name": "rep" }
}
```

**Outbound webhook payload** (deal created — no HMAC signature):
```json
{
  "event": "deal.created",
  "entity": {
    "id": 5802786220408832,
    "unique_id": 1594305685795,
    "name": "Test Deal",
    "amount": 200,
    "track_id": 5634472569470976,
    "milestoneLabelName": "New",
    "owner_id": 5358693205934080
  }
}
```

## Quick-start recipes

### Recipe 1 — Create a contact (write into EngageBay via REST)

Webhooks can't write into EngageBay, so contact creation goes through the API. Note: `Authorization` is the raw key (no `Bearer`), and custom fields need `field_type`.

cURL:
```sh
curl -i -X POST \
  -H "Authorization: YOUR_REST_API_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "score": 10,
    "properties": [
      { "name": "name",  "value": "Sample",                "field_type": "TEXT", "type": "SYSTEM" },
      { "name": "email", "value": "sample@engagebay.com",  "field_type": "TEXT", "type": "SYSTEM" },
      { "name": "phone", "value": "+91 9999999999",        "field_type": "TEXT", "type": "SYSTEM" }
    ],
    "tags": [ { "tag": "sample" } ]
  }' \
  "https://app.engagebay.com/dev/api/panel/subscribers/subscriber"
```

Python:
```python
import requests

H = {"Authorization": "YOUR_REST_API_KEY",
     "Accept": "application/json",
     "Content-Type": "application/json"}
payload = {
    "score": 10,
    "properties": [
        {"name": "name",  "value": "Sample",               "field_type": "TEXT", "type": "SYSTEM"},
        {"name": "email", "value": "sample@engagebay.com", "field_type": "TEXT", "type": "SYSTEM"},
    ],
    "tags": [{"tag": "sample"}],
}
r = requests.post("https://app.engagebay.com/dev/api/panel/subscribers/subscriber",
                  headers=H, json=payload)
print(r.status_code, r.json())
```
**Gotcha:** Omit the `Accept: application/json` header and you get XML back — the #1 "why won't my parser work" surprise.

### Recipe 2 — Export all contacts to a warehouse (cursor pagination)

List contacts is a **POST**, and the cursor lives in the last record of each page.

```python
import requests

H = {"Authorization": "YOUR_REST_API_KEY", "Accept": "application/json"}
url = "https://app.engagebay.com/dev/api/panel/subscribers"
cursor, rows = None, []
while True:
    data = "page_size=100&sort_key=-created_time" + (f"&cursor={cursor}" if cursor else "")
    page = requests.post(url, headers=H, data=data).json()  # form-encoded body
    if not page:
        break
    rows.extend(page)
    cursor = page[-1].get("cursor")   # cursor is on the LAST record
    if not cursor:
        break
print(f"pulled {len(rows)} contacts")
```
**Gotcha:** Lower plans have a small monthly API-call quota; a full re-pull can trip `429`. Prefer incremental sync via the `contact.updated` webhook (Recipe 3) over repeated full exports.

### Recipe 3 — Listen for a deal-closed webhook and sync to your CRM

Create the webhook in **Account Settings → Webhooks** (pick "Deal updated"), point it at your endpoint. EngageBay supports mustache personalization in the URL (e.g. `https://you.com/hook?id={{entity.id}}`).

```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/engagebay/webhook")
def hook():
    body = request.get_json(force=True)
    if body.get("event") == "deal.updated":
        e = body["entity"]
        # No HMAC: validate via a secret path/IP allowlist, then act on e["id"], e["milestoneLabelName"]...
        sync_to_crm(deal_id=e["id"], stage=e.get("milestoneLabelName"), amount=e.get("amount"))
    return "", 200
```
**Gotcha:** There is no documented signature header. Don't trust the payload blindly — put a hard-to-guess secret in the URL path or restrict by source IP, and treat the body's `id` as the source of truth (re-fetch via `GET /dev/api/panel/subscribers/{id}` or the deal endpoint for full data).

## Integration patterns

- **Writes into EngageBay = REST only.** There is no inbound webhook; any "when X happens elsewhere, update EngageBay" flow polls/pushes via the API (use `saveorupdate`-style create-or-update by email where available, e.g. create-deal-to-contact-by-email).
- **CRM sync / field mapping:** map your stage names to EngageBay **`track_id` + `milestoneLabelName`** exactly (case-sensitive). A mismatched milestone name creates the deal but hides it from the milestone/pipeline view — a silent failure.
- **Webhook listener:** outbound events cover contact/company/deal CRUD + email open/click/reply. No HMAC; secure the endpoint yourself. Payloads carry the entity `id` and changed properties — re-fetch for the complete record when you need fields not in the payload.
- **Rate-limit handling:** treat the monthly quota as the real constraint on free/Basic/Growth. Cache reads, batch contact creation (`POST .../subscribers/batch`), and prefer webhooks for incremental updates. On `429`, exponential-backoff and retry.
- **Format:** always send `Accept: application/json`; all field values are case-sensitive (emails, names, tag names, milestone names).
