# Memberstack Platform Guide

Detailed reference for Memberstack — the module map (API/webhook/UI-only), plan gates, the data model, and quick-start automation recipes.

## What Memberstack is

A **no-code membership, authentication, and payments layer for sites you build yourself** (memberstack.com). You paste one script tag and add **data attributes** to mark login/signup forms and gated elements; Memberstack handles auth (login, passwordless, social, 2FA), **Stripe** payments (subscriptions, one-time, trials, tiered plans), and content gating — while you keep full control of your design. Primary home is **Webflow**, but it works on WordPress and any site that can run a script (custom HTML, React, AI-built). Best fit: **makers/solopreneurs who want paid memberships + gated content on their own site** in ~30 minutes, not a hosted course platform. It is *not* a course/LMS host and does *not* send marketing email — it's the auth + paywall plumbing.

## Module map — integration surface

| Module | What it does | Integration surface |
|---|---|---|
| **Authentication** | Email/password, passwordless (OTP), social login, 2FA, email verification, password reset | **DOM package** (front-end) for flows; **Admin REST** `POST /members/verify-token` to validate JWTs server-side |
| **Members / member data** | Accounts + custom fields, metaData, json | **Admin REST** full CRUD (`/members`) + **webhooks** (member.created/updated/deleted) |
| **Payments** | Stripe subscriptions, one-time, trials, tiered plans | UI config; **paid** checkout via DOM package (front-end); **free** plans via Admin REST add/remove-plan; **webhooks** (member.plan.*) |
| **Gating** | Lock pages/sections/elements behind login or plan | **Front-end DOM** via data attributes; UI-only config |
| **Teams** | Group members into teams/seats | Admin REST (`include=teams`) + **webhooks** (team.member.added/removed) |
| **Webhooks** | Notify your backend on events | Configured in **Devtools**; 8 events |

**Rule of thumb:** front-end auth/gating/checkout = **DOM package** (public key, browser). Server-side member management, reads, and token verification = **Admin REST/Node** (secret key). No MCP server.

## Plans & gates (best-effort — verify; pricing changes often)

> *Pricing best-effort from 2026-06 research — confirm on memberstack.com/pricing.*

- **Free until launch** — build/test free; the **test secret key (`sk_sb_`) is capped at 50 test members**. No permanently free *live* tier.
- **Basic** — ~$25/mo (billed yearly), **4% transaction fee**, up to 1,000 members.
- **Professional** — ~$39/mo, **2% fee**, up to 5,000 members.
- **Business** — ~$79/mo, **0.9% fee**, 10,000+ members.
- **Established** — ~$399/mo, **0% Memberstack fee**, 10,000+ members.
- **All transaction fees stack on top of standard Stripe fees.** Only the $399 tier removes Memberstack's cut — factor this into membership pricing, especially at higher volume.

## Data model

```json
// Member
{
  "id": "mem_abc123",
  "auth": { "email": "jane@example.com" },
  "verified": true,
  "customFields": { "company": "Acme" },   // shallow-merged on PATCH
  "metaData": { "source": "webflow" },       // shallow-merged on PATCH
  "json": { "prefs": { "theme": "dark" } },  // FULLY REPLACED on PATCH — read-modify-write
  "plans": [ { "id": "pln_xyz789", "status": "ACTIVE" } ]
}
```

- IDs: members `mem_*`, plans `pln_*`. Identity is email or `mem_*`.
- **`json` is fully replaced on PATCH** while `customFields`/`metaData` shallow-merge — the #1 data-loss footgun.
- Non-existent member = `200` + `"data": null`, not `404`.

## Quick-start recipes

### Recipe 1 — Create a member server-side after an external signup (Admin REST)

```bash
curl -X POST https://admin.memberstack.com/members \
  -H "X-API-KEY: sk_sb_your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"TempPass!23","customFields":{"company":"Acme"}}'
```

```python
import requests
r = requests.post("https://admin.memberstack.com/members",
    headers={"X-API-KEY": "sk_sb_your_secret_key"},
    json={"email": "jane@example.com", "password": "TempPass!23",
          "customFields": {"company": "Acme"}}, timeout=30)
print(r.json())   # {"data": {"id": "mem_...", ...}}
```

> Secret key is **server-side only**. Respect the **25 req/s** limit; on `429`, back off.

### Recipe 2 — Gate your own backend API with a Memberstack JWT

When a logged-in member calls your API, verify their token before serving data:

```python
import requests

def member_from_token(jwt):
    r = requests.post("https://admin.memberstack.com/members/verify-token",
        headers={"X-API-KEY": "sk_live_your_secret_key"},
        json={"token": jwt}, timeout=30)
    data = r.json().get("data")
    return data and data.get("id")   # member id if valid, else None
```

This lets a custom/no-code front-end (Webflow + Memberstack DOM) authenticate against your own backend.

### Recipe 3 — Sync new members to a CRM via webhook

Enable the `member.created` webhook in **Devtools** → point it at your endpoint:

```python
from flask import Flask, request
import requests
app = Flask(__name__)

@app.post("/memberstack/member-created")
def member_created():
    evt = request.get_json(force=True)
    m = evt.get("payload", evt)          # confirm envelope against a real delivery
    email = (m.get("auth") or {}).get("email") or m.get("email")
    requests.post("https://your-crm.example/api/contacts",
                  json={"email": email, "source": "memberstack"}, timeout=20)
    return ("", 200)
```

> ⚠️ **Webhook signature verification is NOT available via REST** — only via the Node Admin package. If you're on REST only, verify out-of-band: re-fetch the member with `GET /members/:id` before trusting the event, or move verification to the Node package.

## Known limitations to set expectations on

- **Webhook signatures need the Node package** — REST can't verify them. Plan your stack accordingly.
- **Transaction fees stack on Stripe** (0.9–4%); only the $399 tier is 0%.
- **No permanently free live tier** — free only until launch; test key caps at 50 members.
- **It's a layer, not a host** — great for auth/paywall on your own site; not a course/LMS or email tool. Pair with an ESP for email and an LMS if you need structured courses.
- **Webflow-centric** — works elsewhere, but the smoothest path (and most tutorials) assume Webflow + data attributes.
- **1.0 vs 2.0** — Memberstack 2.0 is the current rebuild; 1.0 is legacy with a different API. Confirm you're on 2.0 docs.
