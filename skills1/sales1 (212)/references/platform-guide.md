# Graphy Platform Guide

Detailed reference for Graphy — the module map (API/webhook/UI-only), plan gates, the data model, and quick-start automation recipes.

## What Graphy is

An **all-in-one course/membership platform for creators, coaches, and educators** (graphy.com; formerly **Spayee**, backed by Unacademy). Run courses (self-paced or cohort), memberships, communities, coaching, webinars, and digital products from one place, with no-code branded **mobile apps**, an AI layer (AI website builder, AI agent for sales/support), and 0%-platform-fee payments. Positioned squarely as a **Kajabi/Teachable alternative** that bundles community + learning at a lower price. Center of gravity is **India** (support runs India timezone; most marquee customers are India-based). Best fit: a community-focused creator who wants courses + membership + a branded app affordably and values simplicity over deep marketing/customization.

## Module map — integration surface

| Module | What it does | Integration surface |
|---|---|---|
| **Courses** (self-paced / cohort) | Video/audio/docs, quizzes, assignments, drip, certificates | UI-built; **webhooks** (New Course Published, Course/Item Completion) |
| **Learners** | Student records, profiles, progress | **REST API** (Create Learner — Advanced plan) + **webhooks** (New Learner Created, Learner Profile Updated) |
| **Enrollments** | Learner ↔ course access | **REST API** (Enroll Learner to Course) + **webhook** (New Enrollment) |
| **Memberships / subscriptions** | Recurring access tiers | UI; **webhook** (New Subscriber) |
| **Transactions / payments** | Checkout, 0% platform fee (verify), Stripe etc. | UI; **webhooks** (Init Transaction, Success Transaction) |
| **Communities** | Discussion, chat, engagement spaces | UI-only |
| **Coaching / Webinars / live classes** | 1:1, group, live teaching, Q&A | UI-only |
| **Digital products** | One-off downloads/offers | UI; transaction webhooks |
| **Branded mobile apps** | No-code iOS/Android app builder | UI; **Rise plan+**; DIY publish to App Store / Play Console |
| **AI layer** (website builder, operator, agent, brain) | Generate sites, automate setup, AI sales/support | UI; AI Agent webhook surfaces escalations |

**Rule of thumb:** the **REST API is gated to the Advanced/Scale (top) plan**. On lower tiers, integrate via **webhooks + Zapier/Pabbly**. No MCP server.

## Plans & gates (best-effort — verify; pricing changes often + sources conflict)

> *Pricing here is best-effort from 2026-06 research and sources disagree — confirm on graphy.com/pricing.*

Current public tiers appear to be:
- **Launch** — ~$49/mo. **No native mobile apps.** ⚠️ At least one third-party review reports a **transaction fee on this tier (~10%)** despite Graphy's "0% platform fee" marketing — verify before committing.
- **Rise** — ~$149/mo (~$112 annual). **Adds branded iOS/Android apps** (DIY build/publish). Third-party reports a lower (~5%) fee on this tier.
- **Scale** — ~$399/mo. Highest limits.
- **API access + SSO** are gated to the **top (Advanced/Scale) plan**.
- Annual billing ~25% off; learner-count caps rise by tier.

An older tier naming (Basic $54 / Pro $109 / Business $182 / Advanced $320, with API on Advanced) also appears in listings — treat the whole pricing picture as **best-effort and verify live**, and especially **confirm the real transaction-fee story**, since "0% platform fee" and "10%/5% on lower tiers" both appear in sources.

## Data model

```json
// Learner (identity = email)
{ "email": "learner@example.com", "name": "New Learner" }

// Enrollment
{ "learner_email": "learner@example.com", "course_url": "https://you.graphy.com/courses/..." }

// Transaction (Init / Success Transaction webhooks)
{ "learner_email": "learner@example.com", "status": "success", "amount": 4900, "currency": "USD" }
```

- **Email is the learner identity** — Create Learner + Enroll both key on email; dedupe on it.
- Webhook field keys aren't published — capture one delivery on webhook.site to confirm before parsing.

## Quick-start recipes

### Recipe 1 — Enroll a buyer from an external cart (API, top plan)

If you sell elsewhere and host on Graphy, create + enroll the learner via the API (gated to Advanced/Scale). Confirm the exact base URL/paths in the Postman collection; auth is `mid` + `key` from Integration API.

```python
import requests

API = "https://<graphy-api-base>"     # confirm in Postman
HEADERS = {"mid": "<MID>", "key": "<API_KEY>", "Content-Type": "application/json"}

def enroll(email, name, course_url):
    requests.post(f"{API}/<create-learner-path>",
                  headers=HEADERS, json={"email": email, "name": name}, timeout=30)
    return requests.post(f"{API}/<enroll-path>",
                  headers=HEADERS, json={"learner_email": email, "course_url": course_url}, timeout=30)

enroll("buyer@example.com", "Buyer", "https://you.graphy.com/courses/signature")
```

### Recipe 2 — Grant access on payment via webhook (any plan)

No top plan? Use webhooks. Register a **Success Transaction** webhook (Dashboard → Integrations → Webhooks) pointed at your endpoint, and fulfill there.

```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/graphy/paid")
def paid():
    data = request.get_json(force=True)         # confirm keys against a real delivery
    if data.get("status") == "success":         # use Success Transaction, NOT Init Transaction
        grant_access(data.get("learner_email"))
    return ("", 200)
```

> **Critical:** fulfill on **Success Transaction**, not **Init Transaction** (Init fires when checkout merely starts). And remember: **5 failed deliveries auto-disable the webhook** — keep the endpoint reliable and alert on disables.

### Recipe 3 — Sync new learners to your CRM/ESP (Zapier/Pabbly)

Trigger on **New Learner Created** (or New Enrollment) → Zapier/Pabbly → upsert into HubSpot/Mailchimp/your CRM by email. This is the no-code path when you're below the API plan tier.

## Known limitations to set expectations on

- **Post-sale support is the top complaint** — responsive pre-sale, slow afterward, on **India timezone**. Set expectations; don't promise fast turnaround.
- **Branded mobile apps are DIY and gated to Rise+** — you build them in the no-code App Builder and publish under your own Apple/Google developer accounts. The "$49 with an app" expectation is wrong; real entry for an app is Rise.
- **Transaction fees are murky on lower tiers** — verify the actual cut before pricing your offers.
- **Smaller ecosystem** — fewer third-party integrations, tutorials, and advanced marketing tools than Kajabi; plan to bridge marketing via Zapier/Pabbly + your ESP.
- **API gated to the top plan** — budget for it if programmatic learner/enrollment sync is a hard requirement.
