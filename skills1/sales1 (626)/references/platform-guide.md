<!-- Source: https://tuemilio.com/ , https://tuemilio.com/pricing , https://docs.tuemilio.com/api/ , https://docs.tuemilio.com/javascript-api/ , https://docs.tuemilio.com/webhooks/ — fetched 2026-06 -->

# Tuemilio Platform Reference

## Overview

Tuemilio (tuemilio.com) is an **early-access waitlist and pre-launch validation platform** with a built-in **viral referral loop**: subscribers join, see their position, get a referral link, and climb the queue by inviting friends (points/leaderboard). It adds white-labeled subscriber dashboards, email marketing, fraud protection, and "Tuemilio Analytics™." For startup founders and indie makers finding product-market fit before launch. Differentiator vs the lighter indie tools: a genuinely developer-friendly trio of **REST API + JavaScript SDK + webhooks** plus native Zapier/Mailchimp.

## Capabilities & automation surface

| Capability | What it does | Automation surface | Confidence |
|---|---|---|---|
| Waitlist + referral loop | Position, referral link, points, leaderboard (`waiters`) | JS SDK + REST + UI | Verified |
| Signup form / widget | Customizable, branded, custom fields, GDPR | JS SDK (`init`, `t-signup`) | Verified |
| White-labeled dashboard | Subscriber sees position, referrals, rewards | JS SDK (`getDashboard`/`showDashboard`/`onDashboardData`) | Verified |
| Email marketing | Custom domain, templates, activity-triggered emails | UI | Verified |
| Subscriber CRUD | Create/list/get/update/delete emails, add points | **REST API** | Verified (verbatim) |
| Waitlist read | List/get waitlists with counts + conversion | **REST API** | Verified (verbatim) |
| Webhooks | `new-subscriber`, `grant-access`, `confirmed-subscriber` | **Webhook (egress)** | Verified |
| Fraud protection | `anti_points`, `blocked`, `fraud_id` flags | REST fields + UI | Verified |
| Analytics | Channels, referrer URLs, geolocation; GA events | UI + GA | Verified |
| Zapier / Mailchimp / Typeform | 3,000+ apps; auto Mailchimp sync; surveys | iPaaS / native | Verified |
| MCP server | — | — | None found |

**Rule of thumb:** browser → **JS SDK**; server → **REST API**; push out → **webhooks**. The docs explicitly forbid the REST API on the frontend.

## Pricing, limits & plan gates

> Best-effort (2026-06) — verify on the live pricing page. Tuemilio previously had a free tier; current public tiers are paid + a 30-day free trial (no credit card).

| Plan | Price | Subscribers / Lists | Notable |
|---|---|---|---|
| Founder | $29/mo | Unlimited / Unlimited | Custom email domain, email marketing, campaign analytics, fraud protection, **REST API & JS SDK**, support |
| Startup | $49/mo | Unlimited / Unlimited | Everything in Founder **+ teams + priority support** |
| Enterprise | Custom | Unlimited | Everything in Startup + account management, custom integrations, design tweaks |

**Integration impact:** unusually, **API, webhooks, custom domains, email sending, and unbranded forms are on every paid tier** — so the developer surface isn't a high-tier upsell. The only real gate is **teams** (Startup+). The 30-day trial needs no card.

## Integrations

- **Egress (webhooks):** `new-subscriber`, `grant-access`, `confirmed-subscriber` → your endpoint / Zapier / Telegram / etc.
- **REST API (server-side):** bidirectional subscriber management + waitlist reads.
- **JS SDK (browser):** signup, dashboard, referral widget, event hooks.
- **Native:** Mailchimp (auto subscriber sync), Typeform (surveys), Google Analytics (auto events), Zapier (3,000+ apps; New Subscriber trigger).
- **No MCP server.**

## Data model

**Email (subscriber)** — the core object:
```json
{
  "id": 1112,
  "address": "hello@mail.com",
  "points": 1,
  "anti_points": 0,
  "source": "email-form",
  "referrer_id": 109,
  "referral_id": "AvzMb",
  "referral_link": "https://yourapp.com?r=AvzMb",
  "position": 186,
  "position_ordinal": "186th",
  "people_ahead": 185,
  "subscribed": 1,
  "blocked": 0,
  "custom_fields": { "name": "rob" },
  "dashboard_link": "https://yourapp.com?email=hello@mail.com",
  "waiters": [ { "address": "h××××@×××.com", "points": 0, "position": 184 } ]
}
```

**Wait List**:
```json
{
  "id": 724,
  "name": "Watape",
  "host": "https://example.com/launch",
  "emails_count": 194,
  "visits_count": 2124,
  "unique_visits": 1599,
  "conversion": 0.12,
  "referrals_count": 20,
  "uuid": "98f5535f-32bc-425c-a3d1-af950f8ac4e6"
}
```

Notes: `points` ranks the queue (higher = closer to front); `waiters` is the leaderboard with **censored** emails (safe to display publicly); the **`uuid`** is the Widget List UUID used by the JS SDK, while the numeric `id` is used by REST paths.

## Quick-start recipes

### Recipe 1 — Next.js embed with referral attribution (frontend, JS SDK)
```jsx
import { useEffect } from "react";

export default function Waitlist() {
  useEffect(() => {
    if (typeof window === "undefined") return;
    (function (t,u,e,m,i,l,io){
      t["TuemilioObject"]=m;t[m]=t[m]||function(){(t[m].q=t[m].q||[]).push(arguments);};
      t[m].id="YOUR_WIDGET_LIST_UUID";l=u.createElement(e),io=u.getElementsByTagName(e)[0];
      l.id=m;l.src=i;l.async=1;io.parentNode.insertBefore(l,io);
    }(window,document,"script","Tuemilio","https://tuemilio.com/assets/js/modal/4.0/tuemilio-modal.js"));

    Tuemilio("init", {});
    Tuemilio("sendVisit");

    // Forward the inbound ?r= referral code so the referrer gets credited
    const ref = new URLSearchParams(window.location.search).get("r");
    Tuemilio("onSubscriberCreated", (sub) => console.log("joined at position", sub));
    // When you collect the email yourself:
    // Tuemilio("createSubscriber", { address, referralId: ref || undefined });
  }, []);

  return <div className="t-signup"></div>;
}
```
**Gotchas:** guard on `window` (SSR); use the **UUID**, not the numeric list id; never put the REST `api_token` in this file.

### Recipe 2 — `new-subscriber` webhook → CRM/Slack (server)
```python
from flask import Flask, request, abort

app = Flask(__name__)
SEEN = set()  # use Redis/DB in production

@app.post("/hooks/tuemilio-7c1f9a")  # secret path stands in for a signature
def tuemilio():
    if request.headers.get("User-Agent", "").startswith("Tuemilio-Hookshot") is False:
        abort(403)
    event = request.headers.get("X-Tuemilio-Event")     # new-subscriber | grant-access | confirmed-subscriber
    sub = request.get_json()
    sid = sub.get("id")
    if sid in SEEN:
        return ("duplicate", 200)
    SEEN.add(sid)

    if event == "new-subscriber":
        # upsert_hubspot(email=sub["address"], position=sub.get("position"), ref=sub.get("referral_id"))
        # post_slack(f"New waitlister: {sub['address']} (#{sub.get('position')})")
        pass
    elif event == "grant-access":
        # provision_account(sub["address"]); send_youre_in_email(sub["address"])
        pass
    return ("ok", 200)
```
**Gotchas:** no HMAC — rely on the secret URL + user-agent; dedupe on `id`; respond 2xx fast.

### Recipe 3 — Server-side REST sync + batch launch (cURL + Python)
```bash
# Pull the whole list (server-side only — token is secret)
curl "https://tuemilio.com/api/v1/lists/$LIST_ID/emails?api_token=$TUEMILIO_TOKEN"

# Add a subscriber with referral attribution
curl -X POST "https://tuemilio.com/api/v1/lists/$LIST_ID/emails?api_token=$TUEMILIO_TOKEN" \
  -d "address=new@user.com" -d "referral_id=AvzMb"

# Award 2 bonus points (additive)
curl -X PUT "https://tuemilio.com/api/v1/lists/$LIST_ID/emails/$EMAIL_ID/add-points?api_token=$TUEMILIO_TOKEN" \
  -d "points=2"
```
```python
import os, requests
BASE = "https://tuemilio.com/api/v1"
tok = os.environ["TUEMILIO_TOKEN"]; LIST = os.environ["LIST_ID"]

emails = requests.get(f"{BASE}/lists/{LIST}/emails", params={"api_token": tok}).json()
# Top of the queue first → grant access in batches; the grant-access webhook fires per grant.
for e in sorted(emails, key=lambda x: x.get("points", 0), reverse=True)[:50]:
    print("invite", e["address"], "pos", e.get("position"))
```
**Gotchas:** pagination isn't documented — verify behavior on large lists; `add-points` is additive while `PUT /emails` sets `points` absolutely.

## Integration patterns

- **Three-surface split:** keep the `api_token` server-side; do all browser work through the SDK; treat webhooks as the real-time spine and REST as the reconciliation/backfill path (no documented webhook retries).
- **Referral integrity:** always forward `?r=`; gate reward fulfillment on clean records (`anti_points == 0`, `blocked == 0`, `fraud_id` empty).
- **Launch flow:** grant access in batches → `grant-access` webhook → provision + "you're in" email; reconcile via `GET /emails`.
- **ESP handoff:** Tuemilio sends waitlist/activity emails, but for a full launch/nurture program sync to Mailchimp (native) or your ESP and send there.

## Fit vs. other indie waitlist tools

| Need | Better fit |
|---|---|
| Waitlist + viral referral with a full REST API + JS SDK + webhooks at a low flat price | **Tuemilio** |
| Built-in broadcasts + HMAC-**signed** webhooks + documented retries | `/sales-waitlister` |
| Unauthenticated signup API + censored public leaderboard, developer widget | `/sales-getwaitlist` |
| Cheapest no-code referral waitlist with an npm component | `/sales-referlist` |
| One-time lifetime pricing | `/sales-launchlist` |
| Waitlists **plus** giveaways/contests with structured fraud webhooks | `/sales-kickofflabs` |
| The growth *strategy* (referral design, lead magnets, cross-promotion) — tool-agnostic | `/sales-audience-growth` |
