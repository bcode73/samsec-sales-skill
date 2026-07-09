# Keap Platform Reference

## Overview

Keap (formerly Infusionsoft, rebranded 2019; now owned by Thryv) is an all-in-one CRM + marketing automation platform for small service businesses — contacts, the drag-and-drop Campaign Builder, email/SMS, sales pipeline, invoicing/payments, and appointments in one tool. Its differentiator is no-code automation ("if you can drag and drop, you can automate your business") aimed at solopreneurs and 1–25-person teams, not agencies. It positions explicitly as a HubSpot alternative.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Contacts / CRM** | Central contact + company records, custom fields, tags | API-accessible (v1/v2 REST), webhook-accessible (`contact.*`) |
| **Tags** | Categorize contacts; the primary trigger/segmentation primitive | API-accessible (apply/remove), webhook-accessible (`tag.applied/removed`) |
| **Campaign Builder / Automations** | Drag-and-drop "When-Then" sequences with goals, timers, emails, tasks | Partially API-accessible (list campaigns, add/remove contacts to a sequence); sequence *content* is UI-only |
| **Email marketing** | Broadcasts, automated sequence emails, 1:1 emails | API-accessible (send/queue email), templates UI-built |
| **SMS / text marketing** | Tiered text add-on (US business line) | UI-driven; some automation via campaigns |
| **Sales pipeline / Opportunities** | Deal stages, opportunity records | API-accessible, webhook-accessible (`opportunity.*`, including `stage_move`) |
| **Invoicing & payments** | Quotes, invoices, recurring subscriptions, payment processing | API-accessible (Orders, Invoices, Subscriptions, Payments), webhook-accessible (`order.add`, `payment.add`, `invoice.paid`) |
| **Appointments** | Native scheduling | UI-driven; appointment data via API |
| **Landing pages / Webforms** | Lead-capture forms and basic pages | Webforms API-accessible; full funnels are UI-only / third-party |
| **Lead scoring** | Engagement-based scoring | UI-configured |
| **Affiliate / referral** | Built-in referral partner commission tracking | API-accessible (Affiliates endpoints) |

**No native funnel/landing-page builder of note** — Keap users commonly bolt on Leadpages or ClickFunnels for multi-step funnels.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — Keap's plan lineup is in flux; verify on keap.com/pricing.*

- **Base Keap plan**: ~**$249–299/mo** (billed annually), includes **2 user licenses** and a starting contact tier (~1,500 contacts).
- **Pricing scales with contact count** — more contacts = higher monthly bill (the #1 cost complaint; GoHighLevel undercuts with flat unlimited-contact pricing).
- **Extra users**: ~$39/mo each.
- **Text/SMS marketing**: 6-tier add-on — Tier 1 included (500 msgs/100 min) up to Tier 6 $279/mo (25,000 msgs/2,000 min).
- **All core features (CRM, automation, email, sales tools) are in the base plan** — not gated by contact tier.
- **Interfaces**: Max Classic (legacy Infusionsoft engine) and the newer Keap (Pro / Max / Ultimate UI). Pick affects Campaign Builder, reporting, and some API fields.
- **API access** is available on paid plans; **rate limits depend on auth type** (see API reference). Integration won't "break on a free plan" because there is no free plan — there's a free trial only.

## Integrations

- **Direction**: bidirectional via REST API (read + write contacts, orders, opportunities, tags).
- **Native**: 5,000+ app integrations advertised; common ones include QuickBooks, Shopify/WooCommerce/BigCommerce, Calendly, RingCentral, Zapier.
- **iPaaS**: **Zapier** (triggers + actions), **Make**, **n8n**, **Pipedream** all have Keap/Infusionsoft modules — good for no-code sync without touching OAuth.
- **CRM sync pattern**: use REST Hooks for change events + REST v2 for backfill/pulls. Webhook payloads are thin, so every event triggers a follow-up GET.

## Data model

Key objects: **Contact**, **Tag**, **Company**, **Opportunity**, **Order**, **Invoice**, **Subscription**, **Product**, **Campaign**, **Affiliate**. IDs are integers.

### Contact (REST v2 — representative shape)

<!-- Constructed from docs + AeroLeads/Rollout guides — verify against live API -->
```json
{
  "id": 12345,
  "given_name": "Dana",
  "family_name": "Lee",
  "email_addresses": [
    { "email": "dana@example.com", "field": "EMAIL1", "opt_in_status": "single_opt_in" }
  ],
  "phone_numbers": [
    { "number": "+15551234567", "field": "PHONE1", "type": "Mobile" }
  ],
  "tag_ids": [101, 205],
  "date_created": "2026-06-01T14:22:03.000Z",
  "last_updated": "2026-06-12T09:10:55.000Z"
}
```

### Order (representative shape)

<!-- Constructed from docs — verify against live API -->
```json
{
  "id": 88,
  "contact_id": 12345,
  "order_date": "2026-06-10T00:00:00.000Z",
  "order_items": [
    { "product_id": 7, "quantity": 1, "price": "49.00", "name": "Starter Plan" }
  ],
  "status": "PAID",
  "total": "49.00"
}
```

### REST Hook event payload (verbatim shape from docs)

```json
{
  "event_key": "contact.add",
  "object_type": "contact",
  "object_keys": [
    {
      "id": "12345",
      "apiUrl": "https://api.infusionsoft.com/crm/rest/v1/contacts/12345",
      "timestamp": "2026-06-12T09:10:55.000Z"
    }
  ]
}
```
Up to 1,000 changed objects per payload (same event type). Payload carries IDs only — call `apiUrl` for the full record.

## Quick-start recipes

### Recipe 1 — Create a contact and apply a tag

**Trigger**: a new lead from your own form/app → push into Keap and tag for a campaign.

cURL:
```bash
# 1. Create the contact (REST v2)
curl -X POST "https://api.infusionsoft.com/crm/rest/v2/contacts" \
  -H "Authorization: Bearer $KEAP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "given_name": "Dana",
        "family_name": "Lee",
        "email_addresses": [{ "email": "dana@example.com", "field": "EMAIL1" }]
      }'

# 2. Apply a tag (this is what a campaign goal usually watches for)
curl -X POST "https://api.infusionsoft.com/crm/rest/v1/contacts/12345/tags" \
  -H "Authorization: Bearer $KEAP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "tagIds": [101] }'
```

Python:
```python
import os, requests

BASE = "https://api.infusionsoft.com/crm"
H = {"Authorization": f"Bearer {os.environ['KEAP_ACCESS_TOKEN']}",
     "Content-Type": "application/json"}

contact = requests.post(f"{BASE}/rest/v2/contacts", headers=H, json={
    "given_name": "Dana", "family_name": "Lee",
    "email_addresses": [{"email": "dana@example.com", "field": "EMAIL1"}],
}).json()

# Apply the tag the campaign goal listens for
requests.post(f"{BASE}/rest/v1/contacts/{contact['id']}/tags",
              headers=H, json={"tagIds": [101]})
```
**Gotcha**: the campaign only starts when its *goal* (e.g., "tag applied: 101") is met. Creating the contact alone does nothing — the tag is the trigger.

### Recipe 2 — Listen for a paid order and sync to your CRM/warehouse

**Trigger**: `payment.add` / `invoice.paid` → enrich and write to your system.

```python
import hashlib, hmac, base64, requests, os
from flask import Flask, request, abort

app = Flask(__name__)
SECRET = os.environ["KEAP_HOOK_SECRET"].encode()

@app.post("/keap-hook")
def hook():
    # 1. Verify HMAC-SHA256 signature
    sig = request.headers.get("X-Hook-Signature", "")
    digest = base64.b64encode(hmac.new(SECRET, request.data, hashlib.sha256).digest()).decode()
    if not hmac.compare_digest(sig, digest):
        abort(401)

    body = request.get_json()
    for obj in body["object_keys"]:
        # 2. Payload is thin — fetch the full record
        rec = requests.get(obj["apiUrl"], headers={
            "Authorization": f"Bearer {os.environ['KEAP_ACCESS_TOKEN']}"}).json()
        upsert_to_warehouse(rec)        # your code
    return "", 200                       # MUST 200 within 30s or it retries
```
**Gotcha**: respond `200` within 30s. A `410` permanently deactivates the subscription; other non-2xx triggers up to 4 retries (30–60s, 30–60s, 5min, 30min).

### Recipe 3 — Paginated full export of contacts

```python
import requests, os

H = {"Authorization": f"Bearer {os.environ['KEAP_ACCESS_TOKEN']}"}
url = "https://api.infusionsoft.com/crm/rest/v2/contacts?page_size=1000"
all_contacts = []
while url:
    page = requests.get(url, headers=H).json()
    all_contacts += page.get("contacts", [])
    url = page.get("next")    # v2 returns a cursor/next URL; v1 uses offset+limit
print(len(all_contacts))
```
**Gotcha**: v2 uses a `next` cursor (`page_token`); v1 uses `offset`/`limit`. Stay under the rate ceiling (OAuth ~1,500/min, 25 req/sec spike) and back off on `429`.

## Integration patterns

- **CRM sync architecture**: REST Hooks for deltas + a nightly v2 paginated reconcile to catch missed events. Map Keap `tag_ids` → your segment fields; treat tags as the source of truth for lifecycle stage. Resolve conflicts by `last_updated` timestamp (Keap wins on Keap-owned fields).
- **Webhook listener**: subscribe via the REST Hooks API, complete the verification handshake, verify HMAC on every delivery, dedupe on `id`+`timestamp` (events are batched and retried — you *will* get duplicates), and always GET the `apiUrl` because payloads are ID-only.
- **Batch pipelines**: prefer OAuth app tokens (higher throttle) over Personal Access Tokens for bulk jobs. Page with the v2 cursor, cap concurrency under the 25 req/sec spike policy, and retry `429`/`5xx` with exponential backoff.
- **Auth choice**: OAuth 2.0 for multi-account/marketplace apps (independent per-app throttling); a Personal Access Token or Service Account Key for a single-account internal script (lower limits, simpler setup).
