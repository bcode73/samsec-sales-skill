# Ontraport Platform Reference

## Overview

Ontraport (ontraport.com) is an all-in-one business platform — CRM, marketing automation, payments, and a dynamic CMS on a single unified database. Built for established small and mid-market businesses (info-marketers, coaches, membership sites, service businesses) that want enterprise-grade automation without Salesforce/HubSpot cost or complexity. Closest peer is Keap; competes with GoHighLevel and ActiveCampaign. Differentiator: deep automation + native payments + membership/CMS in one tool. Trade-offs: a steep learning curve and per-contact pricing that escalates as the list grows.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **CRM** | Contacts, visual pipelines, lead scoring/routing, tasks, self-scheduling calendars, mobile app | **API-accessible** (objects: Contact = objectID 0) + webhook on object created |
| **Campaign Builder (automation)** | Visual automation maps — triggers, conditions, actions; embedded AI assistant | Triggered via API/tags/forms; rule build **UI-only** |
| **Email + SMS** | Broadcasts + automated sequences, segmentation, attribution | Sends triggered by automation/tags; content build **UI-only**; tag add/remove via API + webhook |
| **Tags** | Behavioral tags that drive automations | **API-accessible** (add/remove on a contact) + webhook on tag added/removed |
| **Payments** | Order forms, subscriptions, upsells/order bumps, decline recovery, offline transactions, customer portal | Transactions **API-accessible** (read); webhook on product purchased / transaction added; order-form build **UI-only** |
| **Dynamic CMS** | Drag-and-drop pages: landing pages, courses, portals, membership sites | Page build **UI-only**; membership access driven by tags/automation |
| **Forms** | Lead-capture forms (smart forms, order forms) | Webhook on form submitted; build **UI-only** |
| **Shared inbox** | Unified customer communications | **UI-only** |
| **Webhooks** | Outbound event notifications, subscribed via the API | **API-accessible** (subscribe/list/delete) |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against ontraport.com/pricing; per-contact pricing means your real cost depends on list size.*

| Plan | Price | Contacts | Notes |
|---|---|---|---|
| **Basic** | ~$79/mo | 1,000 | Core CRM + automation + email, unlimited emails |
| **Plus** | ~$147/mo | 2,500 (scales) | Advanced automation + CRM features |
| **Pro** | ~$297/mo | 10,000 (scales) | Deeper reporting + partner/affiliate programs |
| **Enterprise** | ~$497/mo | higher tiers | Highest limits |

**Notes for integrators:**
- **Per-contact pricing** — the bill scales with contact count, and **overages stack unpredictably** (users report ~$600/mo at ~43k contacts). This is the dominant cost complaint.
- **Additional users** ~$46/mo each on all plans.
- **API + webhooks** are core platform features (not a separate add-on) — verify availability for the specific plan, but they're generally available.
- **Rate limit:** 180 requests/minute (rolling) — see API reference.
- 14-day free trial; no permanent free plan.

## Integrations

- **Object REST API** (`https://api.ontraport.com/1`, `Api-Key` + `Api-Appid`) — the primary programmatic surface for contacts, objects, transactions, tags, and webhook management.
- **Webhooks** — outbound push on object created, form submitted, tag added/removed, product purchased, transaction added.
- **Zapier** — connects Ontraport to thousands of apps without code.
- **Native** — payment gateways and popular business tools; interactive Swagger doc at `api.ontraport.com/doc`, live tester at `api.ontraport.com/live`.
- **Direction of flow:** external → Ontraport via `/1/objects` (create/update contacts, add tags → trigger automations); Ontraport → external via webhooks (sales/contact/form events).

## Data model

Everything is an **object** with a numeric `objectID`. `GET /1/objects/meta` returns every object type and its ID. Contact = objectID `0`.

**Contact (objectID 0)**:
```json
<!-- Constructed from documented fields — verify against live API -->
{
  "id": "1234",
  "objectID": 0,
  "firstname": "Jane",
  "lastname": "Doe",
  "email": "jane@example.com",
  "contact_cat": "*/*88/*",
  "date": 1718890920
}
```
> Tag membership is stored in delimited fields like `contact_cat` (`*/*<tagId>/*`), a classic Ontraport quirk — use the dedicated tag endpoints rather than editing the string by hand.

**Transaction**:
```json
<!-- Constructed from documented fields — verify against live API -->
{
  "id": "9901",
  "contact_id": "1234",
  "total": "297.00",
  "status": "paid",
  "product_id": "12",
  "date": 1718891000
}
```

**List response (paginated)**:
```json
<!-- Constructed from documented behavior — verify against live API -->
{
  "code": 0,
  "data": [ { "id": "1234", "email": "jane@example.com" } ],
  "account_id": 55555,
  "misc": { "listFields": ["id","email"] }
}
```

## Quick-start recipes

> Base URL `https://api.ontraport.com/1`. Every request carries `Api-Key: <key>` and `Api-Appid: <app id>` headers (from Administration → Integrations). See `references/ontraport-api-reference.md` for the full endpoint list.

### Recipe 1 — Create a contact via the objects API
Use when an app signup should become an Ontraport contact. Contacts are objectID 0.

**cURL**:
```bash
curl -X POST https://api.ontraport.com/1/objects \
  -H "Api-Key: $ONTRA_KEY" \
  -H "Api-Appid: $ONTRA_APPID" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "objectID=0" \
  --data-urlencode "email=jane@example.com" \
  --data-urlencode "firstname=Jane"
```

**Python** (upsert by email so re-runs don't duplicate):
```python
import requests

BASE = "https://api.ontraport.com/1"
H = {"Api-Key": ONTRA_KEY, "Api-Appid": ONTRA_APPID}

def upsert_contact(email, firstname):
    # saveorupdate matches on a unique field (email) and creates or updates
    r = requests.post(f"{BASE}/objects/saveorupdate", headers=H,
                      data={"objectID": 0, "email": email, "firstname": firstname},
                      timeout=30)
    r.raise_for_status()
    return r.json()["data"]
```
**Gotchas:** discover objectIDs with `GET /1/objects/meta` first; use `saveorupdate` (match on email) to avoid duplicate contacts; assign tags via the tag endpoint, not by editing `contact_cat`. Stay under 180 req/min.

### Recipe 2 — Subscribe to a new-sale webhook (no polling)
Use when fulfillment should fire the instant someone buys. Subscribe a webhook **via the API**, then handle it idempotently.

**Subscribe**:
```bash
curl -X POST https://api.ontraport.com/1/objects \
  -H "Api-Key: $ONTRA_KEY" -H "Api-Appid: $ONTRA_APPID" \
  --data-urlencode "objectID=<webhook objectID from /objects/meta>" \
  --data-urlencode "url=https://yourapp.com/hooks/ontraport" \
  --data-urlencode "event=transaction_added"
```

**Flask listener**:
```python
from flask import Flask, request
app = Flask(__name__)
seen = set()  # use Redis/db in production

@app.post("/hooks/ontraport")
def ontra_hook():
    data = request.form.to_dict() or request.json or {}
    tid = str(data.get("transaction_id") or data.get("id"))
    if tid in seen:           # deliveries can repeat — be idempotent
        return "", 200
    seen.add(tid)
    # ... grant access / write to CRM / notify ...
    return "", 200            # respond 2xx fast; do slow work async
```
**Gotchas:** webhook events available — object created, form submitted, tag added/removed, product purchased, transaction added; respond `2xx` fast; dedupe on the transaction id; debug via Administration → Integrations → Webhook Logs (max 10,000 entries). Exact payload keys vary — log a sample first.

### Recipe 3 — Page through all contacts (range + start)
List calls cap at 50 records. Loop with `start` and request only the fields you need.

```python
def all_contacts():
    start = 0
    while True:
        r = requests.get(f"{BASE}/objects", headers=H, params={
            "objectID": 0, "range": 50, "start": start,
            "listFields": "id,email,firstname"
        }, timeout=30)
        if r.status_code == 429:
            time.sleep(2); continue
        rows = r.json().get("data", [])
        if not rows:
            break
        yield from rows
        start += 50
```
**Gotchas:** `range` max is 50; advance with `start` (offset), not page numbers; complex filters use a JSON `condition` param; throttle to 180/min.

## Integration patterns

- **CRM sync (Ontraport → CRM/warehouse):** prefer webhooks (transaction added, object created, tag added) for real-time; reserve `GET /1/objects` (range/start paging) for backfills. Join on `email`.
- **CRM sync (external → Ontraport):** `POST /1/objects/saveorupdate` (objectID 0) to upsert contacts, then add tags to trigger Campaign Builder automations.
- **Discovering the schema:** always start with `GET /1/objects/meta` to map object names → objectIDs (custom objects get their own IDs) and `GET /1/objects/getInfo` / field metadata before hardcoding field names.
- **Rate-limit handling:** stay under 180 req/min, read the rate-limit headers, back off on 429, batch with `range`, and request only needed `listFields`.
