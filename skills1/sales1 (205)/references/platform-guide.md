# GetWaitlist Platform Reference

## Overview

GetWaitlist (getwaitlist.com) is a developer-friendly pre-launch **waitlist +
referral** tool: an embeddable/hosted signup widget that puts every signup in a
priority queue, gives each one a referral link that jumps them up the queue, and
shows a gamified leaderboard. Its differentiator is speed and a clean REST API —
signups can be created without authentication, and the whole thing embeds in
under 10 minutes. As of mid-2025 it **removed the free tier for new accounts**
(existing accounts grandfathered); new signups start at $15/mo.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Signup widget | Embeddable (HTML/iframe/React) + hosted page; collects email, optional name/phone, custom questions | **API-accessible** (`POST /signup`, unauthenticated) + UI embed |
| Priority queue | Each signup gets a `priority` position; referrals move you up `spots_to_move_upon_referral` spots | **API-accessible** (read via signup/waitlist objects; `PATCH /signup/<uuid>` to advance) |
| Referrals | Per-signup `referral_token` + `referral_link` (`?ref_id=`); pass `referral_link` on signup to credit the referrer | **API-accessible** |
| Leaderboard | Top referrers with censored email/name/phone for public display | **API-accessible** (`GET /waitlist/<id>/leaderboard`) |
| Custom questions | Extra fields on the form, stored in `answers` | API-accessible (create-time) / UI-configured |
| Metadata | Arbitrary JSON stored per signup | **API-accessible** (`metadata` on create) |
| Automatic emails | Welcome / verification / referral-congrats emails | UI-configured; **custom sending domain is Pro-gated** |
| Offboarding | Mark signups as launched/removed (keeps history) | **API-accessible** (`PATCH /signup` with `offboard_request`) |
| Webhooks | `new_signup`, `offboarded_signup` POST events | **Webhook-accessible** |
| No-code embeds | Webflow, Wix, Shopify, Squarespace, Framer, Carrd, Typedream, Weebly, WordPress, Notion | UI-only embed snippets |
| Connectors | Slack, Discord, Zapier, HubSpot, Airtable | Zapier + native |

There is **no MCP server**.

## Pricing, limits & plan gates

*Best-effort from research (2026-06); verify on the live pricing page — tiers
shift and the free-tier change is recent.*

| Tier | Price | Notable gates |
|---|---|---|
| (Free) | **Removed for new accounts** mid-2025 | Existing free accounts grandfathered; new accounts start paid |
| Basic | **$15/mo** | API access included; entry tier; 7-day trial |
| Advanced | **$50/mo** | Unlocks **custom domain** + **viral referrals**; email validation/fraud detection on higher tiers |
| Pro | **$250/mo** | Custom **email-sending domain** + full automatic-email customization ("send from your domain") |

- **API is available from Basic ($15)** — unlike some rivals that gate the API
  to a high tier.
- **Viral referrals + custom domain require Advanced ($50).**
- **Email-from-your-domain and full email automation require Pro ($250).**
- No published numeric rate limits or signup caps in the API docs — verify.

## Integrations

- **Ingress (data in)**: hosted page, embed widget, or `POST /signup`
  (unauthenticated). No-code embeds for 13+ site builders.
- **Egress (data out)**: `new_signup` / `offboarded_signup` webhooks, the
  authenticated list/get API, Zapier, and native **HubSpot** + **Airtable** +
  **Slack** + **Discord** connectors.
- **Direction**: GetWaitlist is the source of truth for signups; you typically
  read/push *out* to a CRM, ESP, or warehouse. There is no bulk-import API for
  signups (one POST at a time).
- **No Make/Pabbly modules and no MCP server documented** — for non-Zapier
  automation you write a small webhook handler or poll the list API.

## Data model

Core objects: **Waitlist** (the campaign) → many **Signups** (people in the
queue), each with referral attribution and an optional **Leaderboard** view.
See `references/getwaitlist-api-reference.md` for full verbatim schemas. Key
shapes:

```json
// Signup (authenticated)
{
  "uuid": "c60ff9f2-1a58-4551-87ea-414991184fba",
  "email": "maya@example.com",
  "first_name": "Maya",
  "priority": 4985,
  "amount_referred": 0,
  "referral_token": "4F0BTBMAB",
  "referral_link": "https://getwaitlist.com?ref_id=4F0BTBMAB",
  "referred_by_signup_token": null,
  "metadata": {},
  "answers": [],
  "removed_date": null,
  "verified": false
}
```

- `priority` = queue position (lower is closer to the front).
- `referral_token` credits this signup; pass a referrer's `referral_link` on a
  new signup to attribute it.
- `removed_date` / `removed_priority` are set on offboarding (the signup is kept,
  not deleted).

## Quick-start recipes

### Recipe 1 — Create a signup with referral attribution (server-side)

Trigger: your own custom form posts to your backend; you forward to GetWaitlist.

```bash
curl -X POST "https://api.getwaitlist.com/api/v1/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maya@example.com",
    "waitlist_id": 12345,
    "first_name": "Maya",
    "referral_link": "https://getwaitlist.com?ref_id=4F0BTBMAB",
    "metadata": { "source": "landing_v2" }
  }'
```

```python
import requests

resp = requests.post(
    "https://api.getwaitlist.com/api/v1/signup",
    json={
        "email": "maya@example.com",
        "waitlist_id": 12345,
        "first_name": "Maya",
        # the ?ref_id=<token> value captured from the visitor's URL:
        "referral_link": "https://getwaitlist.com?ref_id=4F0BTBMAB",
        "metadata": {"source": "landing_v2"},
    },
    timeout=10,
)
signup = resp.json()
print(signup["priority"], signup["referral_token"])
```

Gotcha: this endpoint is **unauthenticated** — anyone can call it with your
public `waitlist_id`. Capture `ref_id` from the visitor's URL yourself; if you
drop it, the referrer gets no credit and won't move up the queue.

### Recipe 2 — Webhook handler: sync new signups to a CRM

Trigger: GetWaitlist `new_signup` webhook (Features tab → Webhook URL).

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
SEEN = set()  # replace with a real store

@app.post("/getwaitlist-webhook")
def webhook():
    body = request.get_json(force=True)
    event = body.get("event")
    signup = body.get("signup", {})
    uuid = signup.get("uuid")

    # Webhooks are UNSIGNED — make handlers idempotent and re-verify if needed.
    if uuid in SEEN:
        return jsonify(ok=True), 200
    SEEN.add(uuid)

    if event == "new_signup":
        push_to_crm(signup["email"], signup.get("first_name"), signup["priority"])
    elif event == "offboarded_signup":
        mark_launched_in_crm(uuid, signup.get("removed_date"))

    return jsonify(ok=True), 200  # respond fast: 30s connect / 90s response cap
```

Gotchas: respond **2xx quickly** — POSTs time out at 30s to connect / 90s for a
response. Payloads are **unsigned** (no documented HMAC), so don't trust them
for anything sensitive without re-fetching via the authenticated API. Dedupe on
`signup.uuid`.

### Recipe 3 — Offboard the first 500 signups at launch

Trigger: you're ready to let the front of the queue in.

```python
import requests

API = "https://api.getwaitlist.com/api/v1"
HEADERS = {"api-key": "YOUR_API_KEY", "Content-Type": "application/json"}
WAITLIST_ID = 12345

# 1) pull the front of the queue (lowest priority first)
rows = requests.get(
    f"{API}/signup/waitlist/{WAITLIST_ID}?offset=0&limit=500",
    headers=HEADERS, timeout=15,
).json()

# 2) offboard them in one PATCH (keeps history; fires offboarded_signup webhook)
requests.patch(
    f"{API}/signup",
    headers=HEADERS,
    json={
        "waitlist_id": WAITLIST_ID,
        "offboard_request": True,
        "signups": [{"uuid": r["uuid"]} for r in rows],
    },
    timeout=30,
)
```

Gotcha: **offboard ≠ delete.** Offboarded signups keep `removed_date` /
`removed_priority` and stay queryable (`offboarded_request=true`). Use
`DELETE /signup` only for true erasure (GDPR) — it returns 204 and is permanent.

## Integration patterns

- **CRM sync**: prefer the `new_signup` webhook (push) over polling. Map
  `email` → contact, `priority` → custom field, `referral_token` /
  `referred_by_signup_token` → referral attribution, `metadata` → whatever you
  stuffed in at create time. Re-fetch via the authenticated API when you need
  fields the webhook omits.
- **Webhook reliability**: unsigned, no documented retries → make handlers
  idempotent on `uuid`, respond fast, and run a periodic reconciliation job that
  pages the authenticated list API to backfill anything missed.
- **Referral fraud**: GetWaitlist's signup-create endpoint is unauthenticated
  and the docs don't describe IP/fingerprint fraud params — so a public
  `waitlist_id` can be scripted. Enable `uses_signup_verification` (email
  verification) so unverified referrals don't count, gate rewards on `verified`
  signups, and watch for same-domain / rapid-fire patterns. Email validation and
  fraud detection are gated to higher tiers.
- **Pagination**: authenticated list uses `offset` / `limit`; page with
  `limit=100` and increment `offset`.
