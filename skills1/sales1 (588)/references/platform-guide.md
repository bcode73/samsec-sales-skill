# Systeme.io Platform Reference

## Overview

Systeme.io (systeme.io, HQ Ireland) is a budget all-in-one for bootstrappers, solopreneurs, and first-time creators — funnels, email, courses, community, automation, affiliates, and webinars in one account. Its differentiator is a genuinely usable **free plan** (2,000 contacts, 0% transaction fees, unlimited emails) and aggressive pricing. Trade-off vs Kartra/GoHighLevel/ActiveCampaign: simpler page/email builders, a smaller native-integration ecosystem, and a less flexible workflow editor — the public API and iPaaS connectors are how power users fill those gaps.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Contacts / CRM** | Contact records, tags, CRM pipelines | **API-accessible** (`/api/contacts`, `/api/tags`) + webhooks on contact created / tag added/removed |
| **Tags** | Behavioral tags that trigger automations | **API-accessible** (`/api/tags`; assign/remove on a contact) + webhooks |
| **Funnels + website** | Drag-and-drop funnel/page/website builder, blog | `/api/funnels` (read) via API; building is **UI-only** |
| **Email marketing** | Broadcasts + automation sequences (`campaigns`) | `/api/campaigns` (read) via API; content/flow build **UI-only** |
| **Automation / workflows** | Rule-based automations (triggers → actions) | Triggered via API actions (create contact, assign tag) + webhooks; rule build **UI-only** |
| **Courses** | Course builder, unlimited students | Enrollment can be driven by tags/automation; build **UI-only** |
| **Community + booking** | Community spaces and a booking calendar | **UI-only** |
| **Checkout / sales** | Order forms, order bumps, upsells, 0% fees | `/api/orders`, `/api/subscriptions`, `/api/products` (read) via API; webhooks on new sale / sale canceled; checkout build **UI-only** |
| **Affiliate management** | Built-in affiliate program for your products (all plans) | **UI-only** |
| **Webinars** | Automated/evergreen webinars (Webinar plan+) | **UI-only** |
| **Webhooks** | Outbound event notifications | **API-accessible** (`/api/webhooks` — register/list/delete) |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against systeme.io/pricing; Systeme.io adjusts limits over time.*

| Plan | Price | Contacts | Notable limits/gates |
|---|---|---|---|
| **Free** | $0 | 2,000 | 3 funnels, 1 course, 1 blog, 1 affiliate program, 1 custom domain, unlimited emails, **0% transaction fees** |
| **Startup** | $17/mo | 5,000 | Unlimited funnels, 5 courses, 3 custom domains |
| **Webinar** | $47/mo | 10,000 | Adds **automated webinars**, more courses/domains |
| **Unlimited** | $97/mo | Unlimited | Everything, **sub-accounts**, free migration service |

**Notes for integrators:**
- **API access is not plan-gated** — the public REST API works across plans, including Free (verify against the live account). This is unusual and a real advantage for makers prototyping on the free tier.
- **0% transaction fees on all plans** (you still pay Stripe/PayPal's own fees).
- **Automated webinars** require the Webinar plan or higher.
- **Rate limits** are communicated via `X-RateLimit-*` response headers (see API reference).

## Integrations

- **Public REST API** (`https://api.systeme.io`, `X-API-Key`) — the primary programmatic surface; read contacts/tags/funnels/products/orders/subscriptions/campaigns, write contacts/tags, manage webhooks.
- **Webhooks** — outbound push on contact created, tag added/removed, new sale, sale canceled.
- **iPaaS** — Zapier, Make, Pabbly Connect, n8n (preconfigured nodes exist). These are the practical bridge for the many tools Systeme.io doesn't integrate natively.
- **Payment gateways** — Stripe and PayPal (0% Systeme.io fee).
- **Direction of flow:** external → Systeme.io via `/api/contacts` + `/api/tags` (drive automations); Systeme.io → external via webhooks (sales/contact events).

## Data model

REST resources under `/api/<resource>`. Core objects:

**Contact**:
```json
<!-- Constructed from documented fields — verify against live API -->
{
  "id": 1234567,
  "email": "jane@example.com",
  "fields": [
    { "slug": "first_name", "value": "Jane" },
    { "slug": "surname", "value": "Doe" }
  ],
  "tags": [ { "id": 88, "name": "app-trial" } ],
  "registeredAt": "2026-06-20T14:02:00+00:00"
}
```

**Tag**:
```json
<!-- Constructed from documented fields — verify against live API -->
{ "id": 88, "name": "app-trial" }
```

**Order** (sale):
```json
<!-- Constructed from documented fields — verify against live API -->
{
  "id": 99001,
  "contact": { "id": 1234567, "email": "jane@example.com" },
  "total": "47.00",
  "currency": "USD",
  "status": "paid",
  "items": [ { "product": "Webinar Plan", "price": "47.00" } ],
  "createdAt": "2026-06-20T14:05:00+00:00"
}
```

**Cursor-paginated list response** (shape):
```json
<!-- Constructed from documented pagination behavior — verify the data key against a live GET -->
{
  "items": [ { "id": 1234567, "email": "jane@example.com" } ],
  "hasMore": true
}
```

## Quick-start recipes

> Base URL `https://api.systeme.io`. Every request carries `X-API-Key: <your key>` (created in profile settings → Public API keys). See `references/systemeio-api-reference.md` for the endpoint list.

### Recipe 1 — Create a contact and assign a tag
Use when an app signup should land in Systeme.io already tagged. Create (or upsert) the contact, then assign an existing tag.

**cURL**:
```bash
# 1) Create the contact
curl -X POST https://api.systeme.io/api/contacts \
  -H "X-API-Key: $SYSTEME_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","fields":[{"slug":"first_name","value":"Jane"}]}'

# 2) Assign tag 88 to the contact (id from step 1)
curl -X POST https://api.systeme.io/api/contacts/1234567/tags \
  -H "X-API-Key: $SYSTEME_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tagId":88}'
```

**Python**:
```python
import requests

BASE = "https://api.systeme.io"
H = {"X-API-Key": SYSTEME_KEY, "Content-Type": "application/json"}

def upsert_and_tag(email, first_name, tag_id):
    c = requests.post(f"{BASE}/api/contacts", headers=H,
                      json={"email": email,
                            "fields": [{"slug": "first_name", "value": first_name}]},
                      timeout=30)
    # If the contact already exists, look it up instead of failing hard
    contact_id = c.json().get("id") if c.ok else _find_contact_id(email)
    requests.post(f"{BASE}/api/contacts/{contact_id}/tags", headers=H,
                  json={"tagId": tag_id}, timeout=30).raise_for_status()
    return contact_id
```
**Gotchas:** the tag must already exist — create it once with `POST /api/tags`. Creating a contact that already exists may 4xx, so handle the conflict (search by email). Watch `X-RateLimit-Remaining`. Exact field/body keys may differ — confirm against a live call (see API reference Gaps).

### Recipe 2 — React to a new sale via webhook (no polling)
Use when fulfillment should fire the instant someone buys. Register a webhook on the **new sale** event, then handle it idempotently.

**Register** (or use the dashboard):
```bash
curl -X POST https://api.systeme.io/api/webhooks \
  -H "X-API-Key: $SYSTEME_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://yourapp.com/hooks/systeme","event":"sale.new"}'
```

**Flask listener**:
```python
from flask import Flask, request
app = Flask(__name__)
seen = set()  # use Redis/db in production

@app.post("/hooks/systeme")
def systeme_hook():
    data = request.json or {}
    eid = str(data.get("order", {}).get("id") or data.get("id"))
    if eid in seen:        # deliveries can repeat — be idempotent
        return "", 200
    seen.add(eid)
    # ... grant access / write to CRM / notify ...
    return "", 200         # respond 2xx fast; do slow work async
```
**Gotchas:** respond `2xx` quickly so retries don't pile up; dedupe on the order id; the exact event name/payload keys depend on the account — log a sample first. Webhook events available: contact created, tag added/removed, new sale, sale canceled.

### Recipe 3 — Export all contacts into a warehouse (cursor pagination)
Loop `GET /api/contacts?limit=100&startingAfter=<lastId>` until a short page returns.

```python
def all_contacts():
    params = {"limit": 100}
    while True:
        r = requests.get(f"{BASE}/api/contacts", headers=H, params=params, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", "2"))); continue
        page = r.json().get("items", [])
        if not page:
            break
        yield from page
        params["startingAfter"] = page[-1]["id"]
```
**Gotchas:** it's cursor pagination (`startingAfter` = last id you saw), not page numbers. Confirm the list data key (`items` vs another) against a live response before relying on it.

## Integration patterns

- **CRM sync (Systeme.io → CRM):** prefer webhooks (new sale, contact created, tag added) for real-time events; reserve `GET /api/contacts` (cursor-paged) for backfills. Join on `email`.
- **CRM sync (CRM → Systeme.io):** `POST /api/contacts` + assign tags to trigger Systeme.io automations from external events. Pre-create the tags you'll reference.
- **Filling the integration gap:** when no native connector exists, the decision order is: public API → Zapier/Make/Pabbly/n8n → webhook to your own endpoint. Document which you chose so future maintainers know.
- **Rate-limit handling:** read `X-RateLimit-Remaining`/`X-RateLimit-Refill`, back off on `429` honoring `Retry-After`, and paginate instead of re-pulling whole lists.
