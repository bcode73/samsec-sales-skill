# FreshLearn Platform Reference

## Overview

FreshLearn (freshlearn.com) is an **all-in-one LMS / creator-economy platform** — courses, cohorts,
digital products, memberships, communities, email marketing, checkout, and a deep **AI Studio** (AI course
creation, chat-with-content, AI coaching, quiz generation). Pitch: Kajabi's all-in-one convenience at a
fraction of the price, with **no caps on learners/enrollments/storage** and **0% transaction fees**. Best
for budget-conscious creators and coaches who want unlimited students and built-in AI authoring. Weak
spots: a limited page builder and automations/API locked to the upper tiers.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Course builder | Drip, quizzes, PDFs/video, cohorts, learning paths | Enroll/unenroll via **API** + **Zapier**; authoring **UI-only** |
| AI Studio | AI course outline/content, "Course AI" chat-with-content, AI Coach scoring, AI quiz, captions | **UI-only** (Course AI is No Brainer+) |
| Members / learners | Create, update, read; bulk enrollment | **API + Zapier** |
| Product enrollments | Course / digital download / masterclass / bundle | **API + Zapier** (enroll creates member if new) |
| Communities | Built-in social/community (No Brainer+) | **UI-only** |
| Email marketing | Campaigns, drip, workflows/automations | Campaigns **UI-only**; workflows are **No Brainer+** |
| Landing pages / checkout | Sales pages, checkout funnels, coupons | **UI-only** (limited builder) |
| Live sessions | Zoom-based live classes (No Brainer+) | **UI-only** |
| Certificates / assessments | Certificates, assignments, question bank, gamification | Assessment reads via **API**; config **UI-only** |
| Referral + affiliate | Built-in referral + member affiliate programs (No Brainer+) | **UI-only** |
| Payments | Stripe / PayPal / Razorpay, 0% FreshLearn fee | Read via **API** (Payments section) |
| Branded mobile apps | iOS/Android (No Brainer+ included; add-on for lower tiers) | **UI-only** |

**Programmatic interfaces:** REST API (`https://api.freshlearn.com/v1`, `api-key` header, **No Brainer+**),
**native webhooks**, Zapier (6 triggers / 9 actions), Make, Pabbly, Integrately. No MCP server. See
`references/freshlearn-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on the live pricing page; FreshLearn shows monthly,
"annual-equivalent," and bi-annual prices, so quoted numbers vary by billing term.*

| | Free | Pro | No Brainer | No Brainer+ | Enterprise |
|---|---|---|---|---|---|
| ~Price/mo | $0 | ~$35 | ~$46 | ~$89 | custom |
| Products | 1 | Unlimited | Unlimited | Unlimited | Unlimited |
| Learners | 25 manual | Unlimited | Unlimited | Unlimited | Unlimited |
| Email campaigns / custom domain | ❌ | ✅ | ✅ | ✅ | ✅ |
| Community, certificates, assessments, **Zapier**, mobile apps, branding removal | ❌ | ❌ | ✅ | ✅ | ✅ |
| **API access**, unlimited workflows, Course AI, native Zoom/HubSpot/Mailchimp, user roles, auto tax | ❌ | ❌ | ❌ | ✅ | ✅ |
| SCORM/xAPI, SSO/MFA | ❌ | ❌ | ❌ | ❌ | ✅ |

- **0% transaction fees** and **unlimited learners** on all paid tiers — the headline differentiator vs Kajabi.
- **The gates that bite integrators:** **Zapier is No Brainer ($46)+**, but the **REST API and unlimited
  automations/workflows are No Brainer+ ($89)+**. A maker who buys Pro to script enrollments will find no
  API and no Zapier.
- **Communities, certificates, assessments, and branding removal are No Brainer+** — Pro is courses + email + checkout only.
- Branded mobile apps are included on No Brainer+; lower tiers can buy a branded app add-on (~$199/yr).

## Integrations

- **Direction:** API/Zapier is built around **writing in** (create/update member, enroll into
  course/download/masterclass/bundle) and **reading out** (members, courses, payments, assessments,
  course-completed). Native webhooks + Zapier triggers push events out.
- **Payments:** Stripe, PayPal, Razorpay. 0% FreshLearn fee (processor fees still apply).
- **Native integrations** (No Brainer+): Zoom, HubSpot, Mailchimp; plus Slack/WhatsApp/SSO surfaced on the site.
- **iPaaS:** Zapier, Make, Pabbly, Integrately, Pipedream. Auth everywhere = the `api-key`.

## Data model

Identity is **email**; objects are member, course, and product-enrollment. Cursor-paginated lists return
`{data[], pageInfo}`.

**Member** <!-- Constructed from docs/connectors — verify against live API -->
```json
{ "id": "mem_8f3", "email": "buyer@example.com", "first_name": "Sam", "last_name": "Rivera", "created": 1718900000 }
```

**Product enrollment** (course / digital-download / masterclass / bundle) <!-- Constructed — verify -->
```json
{ "member_id": "mem_8f3", "course_id": "crs_123", "product_type": "course", "status": "enrolled" }
```

**List envelope** (verbatim from docs):
```json
{ "data": [], "pageInfo": { "limit": 50, "hasMore": true, "nextCursor": "eyJ0...", "sort": "created_desc" } }
```

## Quick-start recipes

### Recipe 1 — Auto-enroll a buyer from an external cart (API)

**Trigger:** purchase in ThriveCart/SamCart/Stripe → **steps:** call enroll-in-course-product with the
buyer's email + course id; it creates the member if new.

```bash
curl -s -X POST "https://api.freshlearn.com/v1/product-enrollments" \
  -H "api-key: $KEY" -H "Content-Type: application/json" \
  -d '{ "email": "buyer@example.com", "first_name": "Sam", "course_id": "crs_123", "product_type": "course" }'
```
```python
import requests
def enroll(email, course_id, first_name=""):
    r = requests.post("https://api.freshlearn.com/v1/product-enrollments",
        headers={"api-key": KEY, "Content-Type": "application/json"},
        json={"email": email, "first_name": first_name, "course_id": course_id, "product_type": "course"},
        timeout=30)
    r.raise_for_status(); return r.json()
```
**Gotchas:** API is **No Brainer+**. The `enroll` operation creates the member if the email is new — no
separate create call needed. No-code alternative: the **Enroll Member in Course Product** Zapier action
(needs **No Brainer**+ for Zapier). Exact path is best-effort — confirm in the live reference.

### Recipe 2 — Push new sales/completions into a CRM (webhook or Zapier)

**Trigger:** **Get Course Completed Members** / **Get Member Data** Zapier trigger (or a native webhook) →
**steps:** map email + course into a HubSpot/Mailchimp create-or-update action; tag "customer"/"completed".
No published webhook signature — re-read the member via `GET /v1/members` before granting sensitive access.

### Recipe 3 — Nightly member/payment export (Reports via API)

**Trigger:** cron → **steps:** cursor-page `GET /v1/members` and `GET /v1/payments` with `limit=200`,
following `pageInfo.nextCursor` until `hasMore` is false; filter with Unix-timestamp date params.
```python
members = paginate("/members", KEY, {"limit": 200, "order": "desc"})   # paginate() from the API reference
```
**Gotchas:** date filters are **Unix seconds**, not ISO strings; `limit` max is 200.

## Integration patterns

- **CRM sync:** FreshLearn owns *enrollment/progress*; your CRM owns *contact + revenue*. Map on email.
  Push in via enroll endpoints; pull out via members/payments reads or Zapier/webhook events.
- **Webhook listener:** no published signature — restrict to a secret URL and re-verify the member via the
  API before acting. Make handlers idempotent on (email, course_id).
- **Plan-gate awareness in code:** if calls 401/403 unexpectedly, confirm the account is **No Brainer+**
  (API) — not just any paid tier. Zapier needs No Brainer.
- **Backup discipline:** export members + payments via the API on a schedule and keep source content
  off-platform; reviewers cite a no-refund policy and occasional glitches, so don't treat it as your only copy.
