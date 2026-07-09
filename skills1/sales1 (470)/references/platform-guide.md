# Referral Factory Platform Guide

Full reference for the `sales-referral-factory` skill. Read the section you need; don't dump the whole file.

> *Pricing and plan gates are best-effort from research (2026-06) — the live pricing page + G2/Capterra reviews. Verify in-account.*

## What Referral Factory is

A **no-code referral program builder**. You design an on-brand referral campaign (landing pages, links, codes, rewards) without engineering, then optionally drive it via API/webhooks. Positioned for SaaS, ecommerce, and service businesses (insurance, banking, solar, telecom, real estate, education). G2/Capterra ~4.8★. Built and run as self-serve (Basic/Pro) or managed (Enterprise).

**Referral, not affiliate.** It runs *customer* referral programs (your customers/fans/ambassadors refer friends for rewards/discounts). It *can* pay commissions, but it is not a full affiliate-partner platform (no partner portal/recruiting funnel like a dedicated affiliate tool). For commission-based partner programs, compare via `/sales-affiliate-program`.

## Campaign types (templates)

100+ industry templates built on a few mechanics:

- **Single-sided** — only the referrer is rewarded.
- **Double-sided** — referrer *and* the friend both get a reward (give-get).
- **Invite-only** — closed/ambassador programs.
- **Refer-to-win** — sweepstakes/competition entries instead of guaranteed rewards.

Each campaign has a `status` (`launched` / `draft` / `paused`), its own join `url`, `code`, language, optional `starts_at` / `ends_at`, and configurable `fields` for both `person_referring` and `person_invited`.

## Module map — API vs widget vs UI-only

| Module | Surface | Notes |
|---|---|---|
| Campaigns (create/design) | **UI-only** | Build in the dashboard; API can `GET` campaigns but not create them |
| Users (referrers + referred) | **API** | `POST/GET/PUT/DELETE /users`, `GET /users` list |
| Referrer attribution | **API + link** | `referrer` field on `POST /users`, or signups via the referral link |
| Qualification | **API + inbound webhook** | `PUT /users/qualification`, or qualify-in webhook by code/coupon |
| Rewards (due/issue/cancel/list) | **API** | `/rewards/due|issue|cancel|dashboard|issued/{metric}` |
| Promotion codes | **API (Stripe-gated)** | `promotion: true` on create only works when Stripe is connected |
| Promotion widgets (popups, sticky bars, embeds) | **UI / embed** | Configure in dashboard; embed on your site |
| Outbound webhooks | **Webhook** | New user / qualified referral → your endpoint |
| Fraud detection | **UI** | Alerts in dashboard; not a documented API surface |
| Reporting / analytics | **API (opt-in) + UI** | `with=user.analytics` / `with=campaign.analytics` for counts |
| White-label / custom domain | **UI (Pro+)** | Plan-gated |

## Pricing & plan gates (best-effort)

| Plan | Price (monthly) | Users | Notable gates |
|---|---|---|---|
| **Basic** | ~$200/mo ($160 annual) | 20,000 | API + webhooks + integrations + fraud alerts; **no** white-label/custom domain/SSO |
| **Pro** | ~$400/mo ($320 annual) | 40,000 | Adds white-label (remove branding), custom domain, SSO (SAML) |
| **Enterprise** | ~$1,000/mo (annual avail.) | 100,000+ ($100 per +100k) | Adds custom HTML upload, on-prem data, invoice billing, dedicated AM |

- **API/webhooks/Zapier are available on every paid plan** (you must be on at least Basic to get a token).
- 15-day free trial on Basic/Pro (card required, auto-charges). No trial on Enterprise. No refunds on annual.
- Pricing scales by **users** (people in your campaigns) — size to expected program volume.

## Data model (JSON shapes)

**User** (referrer or referred):

```json
{
  "id": 123,
  "campaign_id": 1,
  "referrer_id": null,
  "first_name": "John",
  "email": "john@example.com",
  "code": "ueONFmUp",
  "url": "https://example.referral-factory.com/ueONFmUp",
  "source": "Api",
  "type": "person_referring",
  "signed_up_at": "2024-12-27",
  "qualified_at": null,
  "promotion": { "code": "SAVE50" },
  "analytics": { "reach": 12, "referrals": 8, "qualified_referrals": 3 }
}
```

- `type`: `person_referring` (the referrer) vs `person_invited` (the friend they referred).
- `source`: `Direct` / `Referred` / `Api` / `Added` / `Zapier` / `Widget` / `Popup` / `Embed` / `Test`.
- `qualified_at`: `null` until you qualify the user.
- `analytics`: only present when you pass `with=user.analytics`.

**Due reward**:

```json
{
  "id": 55,
  "reward_id": 9,
  "recipient_id": 123,
  "can_be_issued": true,
  "coupon": "WELCOME10",   // coupon rewards only
  "count": 1,               // amount/commission/custom only
  "total": 25.00            // amount/commission/custom only
}
```

Reward `{metric}` enum: `amount`, `commission`, `coupon`, `custom`.

## Reward / qualification lifecycle

```
POST /users (with referrer)        → referral created, attributed to referrer
        │
        ▼
PUT /users/qualification {qualified:true}   → referral becomes "qualified", reward becomes DUE
   (or inbound qualify webhook by code/coupon)
        │
        ▼
GET /rewards/due/{metric}          → see what's owed
        │
        ▼
POST /rewards/issue/{id}           → reward issued   (or POST /rewards/cancel/{id})
```

Rewards pay out as PayPal cash, gift cards (200+ countries), Stripe credits/coupons, commissions, points, vouchers, swag, or custom — **not** direct bank transfer.

## Quick-start recipes

### Recipe 1 — Create a referred user and attribute the referrer

cURL:

```bash
curl -X POST https://api.referral-factory.com/api/v2/users \
  -H "Authorization: Bearer $RF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": 1,
    "first_name": "Jane",
    "email": "jane@example.com",
    "referrer": { "field": "code", "value": "ueONFmUp" }
  }'
```

Python:

```python
import requests

resp = requests.post(
    "https://api.referral-factory.com/api/v2/users",
    headers={"Authorization": f"Bearer {RF_TOKEN}"},
    json={
        "campaign_id": 1,
        "first_name": "Jane",
        "email": "jane@example.com",
        # omit `referrer` for a standalone referrer; include it to credit one:
        "referrer": {"field": "code", "value": "ueONFmUp"},
    },
)
user = resp.json()  # contains the new user's own code + url to share
```

Pass `referrer` by `code`, `id`, or `email`. Omit it and you create a Person Referring with no attribution.

### Recipe 2 — Qualify a converted referral, then issue the reward

```python
# 1. Mark the referred user qualified (by email + campaign, or id/code)
requests.put(
    "https://api.referral-factory.com/api/v2/users/qualification",
    headers={"Authorization": f"Bearer {RF_TOKEN}"},
    json={"email": "jane@example.com", "campaign_id": 1, "qualified": True},
)

# 2. Find the now-due reward (metric: amount|commission|coupon|custom)
due = requests.get(
    "https://api.referral-factory.com/api/v2/rewards/due/amount",
    headers={"Authorization": f"Bearer {RF_TOKEN}"},
).json()

# 3. Issue it (idempotent: re-check before issuing)
for r in due["data"]:
    if r["can_be_issued"]:
        requests.post(
            f"https://api.referral-factory.com/api/v2/rewards/issue/{r['id']}",
            headers={"Authorization": f"Bearer {RF_TOKEN}"},
        )
```

### Recipe 3 — Receive an outbound webhook and sync to your CRM (no-code-friendly)

Configure the outbound webhook in **Settings → Webhook and API** to fire on *new user* and *qualified referral*. Your handler:

```python
@app.post("/rf-webhook")
def rf_webhook(payload: dict):
    # No HMAC is documented — restrict this URL to a secret path and re-verify.
    code = payload.get("code")
    user = requests.get(
        f"https://api.referral-factory.com/api/v2/users/{code}",
        headers={"Authorization": f"Bearer {RF_TOKEN}"},
    ).json()
    if already_processed(user["id"]):   # idempotency guard
        return {"ok": True}
    upsert_into_crm(user)               # push to HubSpot/Salesforce/your ESP
    mark_processed(user["id"])
    return {"ok": True}
```

No code to host? Use the native HubSpot/Salesforce/Stripe/Pipedrive/Zoho/Intercom connectors or Zapier/Make/n8n instead.

## Fraud & quality watch

Referral incentives attract fake/disposable signups and self-referral abuse. Referral Factory has built-in fraud alerts, but still: qualify on a *real conversion event* (not signup), review before issuing high-value rewards, and watch for same-IP clusters. For list quality/deliverability of the resulting emails, use `/sales-deliverability`.

## When to route out

- Which referral tool / viral mechanics / **is my program incremental** → `/sales-audience-growth`
- Commission-based **affiliate/partner** program design → `/sales-affiliate-program`
- Generic CRM/ESP/Stripe wiring (iPaaS) → `/sales-integration`
- Deliverability of referral/notification emails → `/sales-deliverability`
