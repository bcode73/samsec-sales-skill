# Kartra Platform Reference

## Overview

Kartra (kartra.com, by Genesis Digital — the same company behind WebinarJam/EverWebinar) is an all-in-one marketing platform that consolidates pages, email/SMS, checkout, memberships, video, webinars, affiliates, helpdesk, and calendars into one account. Primary audience: coaches, consultants, course creators, and "offline experts going digital" who want one integrated stack instead of stitching together a funnel builder + ESP + cart + LMS. Differentiator vs GoHighLevel: creator/course-first, without the agency white-label/sub-account layer.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| **Pages / Funnels** | Drag-and-drop page builder (100+ templates), visual funnel mapper & simulator with conditional branching | `get_pages` (read) via API; page-visit event via IPN; building/editing is **UI-only** |
| **Leads / Contacts** | Lead records with custom fields, tags, lead scoring | **API-accessible** (get/search/create/edit) + IPN on add/update |
| **Email + SMS** | Broadcasts and automation sequences, behavioral/adaptive sends | Sequences **API-accessible** for subscribe/unsubscribe; content & flow build **UI-only**; sequence-complete event via IPN |
| **Lists** | Mailing lists for segmentation | **API-accessible** (get lists; subscribe/unsubscribe lead) + IPN on list sub/unsub |
| **Tags** | Behavioral tagging that drives automations | **API-accessible** (get/assign/unassign) + IPN on tag applied/removed |
| **Checkout (Kartra Checkouts)** | Order forms, order bumps, 1-click upsells/downsells, payment plans | Transactions **API-accessible** (get/search/refund); purchase event via IPN; checkout build **UI-only** |
| **Recurring / Subscriptions** | Subscription billing | **API-accessible** (get/search/cancel/edit status) |
| **Memberships / Courses** | Gated content portals, drip lessons | Membership grant/revoke via IPN; access build **UI-only** |
| **Video hosting** | Kartra Video player with marketing tags/CTAs | **UI-only** |
| **Webinars** | Live + automated webinar hosting (Growth+) | **UI-only** |
| **Forms / Surveys / Quizzes** | Lead capture + segmentation (surveys/quizzes Growth+) | Form-fill event via IPN; build **UI-only** |
| **Affiliate management** | Built-in affiliate program for your products (Growth+) | **UI-only** |
| **Calendars** | Appointment scheduling | **API-accessible** (subscribe lead / cancel) |
| **Points** | Lead point scoring | **API-accessible** (give/remove) |
| **Helpdesk** | Support ticketing (Growth+, live chat Professional) | **UI-only** |

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against kartra.com/pricing; Kartra reprices and re-tiers frequently.*

| Plan | ~Price (annual) | Contacts | Notable gates |
|---|---|---|---|
| **Essentials** | ~$59/mo ($52 annual) | 500 | 5 pages, 1 product, 1 membership, 10k emails/mo, **5% transaction fee**, Kartra AI 30 uses |
| **Starter** | ~$99/mo | 2,500 | Unlimited pages/products/memberships, unlimited email/SMS, **0% transaction fee**, video hosting, 5 team members |
| **Growth** | ~$189/mo | 12,500 | Adds **webinars (300 guests), automations, affiliate management, surveys/quizzes, helpdesk** |
| **Professional** | ~$429/mo | 25,000 | Adds **API access, advanced automations, custom-code pages, real-time funnel analytics, helpdesk live chat, 5 custom domains** |

**Integration-breaking gates to flag:**
- **API access appears gated to Professional** — an integration built on a lower tier can fail before any code runs. This is the single most important thing to verify.
- **Automations gated to Growth+** — tag-triggered flows the API relies on may not exist on Essentials/Starter.
- **Transaction fee:** 5% on Essentials, 0% on Starter+ (on top of the payment processor's own fees).
- **Rate limit:** 20 inbound API calls/second per App → `429` when exceeded.

## Integrations

- **Inbound API** (writes into Kartra): create/edit leads, manage tags/lists/sequences, read pages, manage transactions/subscriptions, calendars, points. Direction: external system → Kartra.
- **Outbound API / IPN webhooks** (reads out of Kartra): event-driven push on purchase, tag applied/removed, lead added/updated, sequence complete, form filled, membership granted/revoked, list/sequence sub/unsub, page visit. Direction: Kartra → your endpoint.
- **Native lead imports** from MailerLite, Mailchimp, ActiveCampaign, HubSpot, Brevo, ConvertKit/Kit, GetResponse, Omnisend, Salesforce, Shopify, WooCommerce, WordPress.
- **Zapier** — triggers/actions for connecting Kartra to tools without code (useful when the account lacks API-tier access).
- **Payment gateways** — Stripe, PayPal, Authorize.net, Braintree for Kartra Checkouts.

## Data model

Kartra's API is action-oriented (a single endpoint with an `actions[]` array), not resource-REST. Key objects:

**Lead** (the central object):
```json
<!-- Constructed from documented field lists — verify against live API -->
{
  "lead_id": "9f3c1a7e",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+15551234567",
  "lead_score": 12,
  "tags": ["app-trial", "webinar-2026"],
  "lists": ["Newsletter"],
  "custom_fields": { "plan": "pro", "signup_source": "blog" }
}
```

**Transaction** (from Kartra Checkouts):
```json
<!-- Constructed from documented field lists — verify against live API -->
{
  "transaction_id": "txn_8821",
  "lead_email": "jane@example.com",
  "product": "Signature Course",
  "amount": "297.00",
  "currency": "USD",
  "type": "one_time",
  "status": "completed",
  "date": "2026-06-18T14:02:00Z"
}
```

**Subscription** (recurring):
```json
<!-- Constructed from documented field lists — verify against live API -->
{
  "subscription_id": "sub_4410",
  "lead_email": "jane@example.com",
  "product": "Membership Monthly",
  "status": "active",
  "next_bill_date": "2026-07-18",
  "amount": "49.00"
}
```

## Quick-start recipes

> All calls go to one endpoint: `POST https://app.kartra.com/api` over HTTPS. Auth params (`app_id`, `api_key`, `api_password`) accompany every request. The body carries an `actions[]` array; each action has a `cmd`. See `references/kartra-api-reference.md` for the full command list.

### Recipe 1 — Create a lead and tag it in one call
Use when an app signup should land in Kartra already tagged. The **first action's `cmd` must be `create_lead`**, then chain an `assign_tag`.

**cURL** (form-encoded):
```bash
curl -X POST https://app.kartra.com/api \
  --data-urlencode "app_id=YOUR_APP_ID" \
  --data-urlencode "api_key=YOUR_API_KEY" \
  --data-urlencode "api_password=YOUR_API_PASSWORD" \
  --data-urlencode "lead[email]=jane@example.com" \
  --data-urlencode "lead[first_name]=Jane" \
  --data-urlencode "actions[0][cmd]=create_lead" \
  --data-urlencode "actions[1][cmd]=assign_tag" \
  --data-urlencode "actions[1][tag][tag_name]=app-trial"
```

**Python**:
```python
import requests

KARTRA_API = "https://app.kartra.com/api"

def create_and_tag(email, first_name, tag):
    payload = {
        "app_id": "YOUR_APP_ID",
        "api_key": "YOUR_API_KEY",
        "api_password": "YOUR_API_PASSWORD",
        "lead[email]": email,
        "lead[first_name]": first_name,
        "actions[0][cmd]": "create_lead",
        "actions[1][cmd]": "assign_tag",
        "actions[1][tag][tag_name]": tag,
    }
    r = requests.post(KARTRA_API, data=payload, timeout=30)
    r.raise_for_status()
    return r.json()   # { "status": "Success", ... }

create_and_tag("jane@example.com", "Jane", "app-trial")
```
**Gotchas:** upsert by email (creating a lead that already exists may error or no-op — search first if unsure); stay under 20 calls/sec; batch additional actions into the same `actions[]` array rather than firing separate requests.

### Recipe 2 — React to a purchase via IPN webhook (no polling)
Use when fulfillment should trigger the instant someone buys. Enable the **outbound API/IPN** under My Integrations » API, select the **purchase** event, and point it at your HTTPS endpoint.

**Python (Flask listener)**:
```python
from flask import Flask, request, abort
app = Flask(__name__)
seen = set()  # dedupe store — use Redis/db in production

@app.post("/kartra/ipn")
def kartra_ipn():
    data = request.form or request.json or {}
    txn_id = data.get("transaction_id") or data.get("lead", {}).get("email")
    if not txn_id:
        abort(400)
    if txn_id in seen:          # retries can repeat — make it idempotent
        return "", 200
    seen.add(txn_id)
    # ... grant access / write to CRM / notify Slack ...
    return "", 200             # respond 2xx fast; do slow work async
```
**Gotchas:** respond `2xx` immediately so Kartra doesn't retry; dedupe on the transaction id; validate the payload before acting; the exact field names depend on the event type — log a sample first.

### Recipe 3 — Bulk-export transactions for a revenue dashboard
Use `search transactions` (a payments `cmd`) to page through sales, then load into a warehouse.

**Gotchas:** the search/get actions are the read path — there's no per-resource REST list; pagination params aren't clearly documented (see API reference Gaps), so request narrow date windows and reconcile by `transaction_id`. Keep total request rate under 20/sec.

## Integration patterns

- **CRM sync (Kartra → CRM):** prefer IPN webhooks for real-time events (purchase, tag, lead update) over polling — polling `search` actions burns the 20/sec budget. Map Kartra `email` as the join key; carry `tags` and `custom_fields` into CRM properties. For backfill, do a one-time paced export via `search` actions.
- **CRM sync (CRM → Kartra):** use `create_lead`/`update_lead` with `assign_tag`/`subscribe_lead_to_sequence` to drive Kartra automations from external events. Batch actions per call.
- **Webhook reliability:** Kartra IPN is at-least-once — design idempotent handlers keyed on transaction/lead id, respond `2xx` within a couple seconds, and queue heavy work.
- **Rate-limit handling:** client-side token bucket at <20/sec, exponential backoff on `429`, and collapse multi-step lead operations into a single `actions[]` array.
