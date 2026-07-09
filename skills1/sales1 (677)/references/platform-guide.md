# New Zenler Platform Reference

## Overview

New Zenler (newzenler.com) is an **all-in-one course + membership platform** for creators and coaches —
courses, memberships, communities, funnels, email marketing, and (its differentiator) **built-in live
classes and interactive webinars**. Positioned as a "human-centered," live-session-first, multi-instructor
alternative to Kajabi at a lower price with **0% transaction fees**. Best for coaches who teach live and
want one tool instead of stitching a course host + webinar tool + email + funnels.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Course builder | Drip, quizzes/assignments, certificates, video hosting, mobile player | Enroll/unenroll via **API** + **Zapier/Make**; authoring **UI-only** |
| Memberships / bundles | Tiered recurring access (**Pro+**) | Access follows enrollment — **API/Zapier** to grant; config **UI-only** |
| Communities | Forums, member directory, DMs, private group spaces | **UI-only** |
| Funnels + landing pages | Drag-and-drop pages, funnel templates, lead capture | List + subscribe/unsubscribe via **API**; **New Funnel Subscription** Zapier trigger |
| Email marketing | Broadcasts + automation sequences | **UI-only** (trigger external ESP via Zapier if needed) |
| Live classes / interactive webinars | Built-in Zoom-like sessions, whiteboards, Q&A, auto-record to courses, live-stream to social | List + register/unregister via **API**; registration **Zapier triggers** |
| 1-on-1 coaching | Bookings + calendar | **UI-only** |
| Digital downloads | Sell files/products | **UI-only** |
| Website builder | Multi-site, custom domains (**Pro+**) | **UI-only** |
| Affiliate program | Built-in partner/affiliate management (**Pro+**) | Read via **Reports API** (`/reports/affiliates/*`); config **UI-only** |
| Branded mobile apps | iOS/Android (add-on **+$197/mo**, Pro+) | **UI-only** |
| Reports | Enrollment, sales, course-progress, affiliate | **API-accessible** (brief + detailed) |

**Programmatic interfaces:** REST API (`https://api.newzenler.com/api/v1/`, `X-API-Key` + `X-Account-Name`
headers, **Pro-gated**), Zapier (7 triggers / 7 actions), Make, Integrately. **No native webhooks; no MCP
server.** See `references/zenler-api-reference.md` for the full endpoint inventory.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on the live pricing page before quoting.*

| | Starter | Pro | Premium |
|---|---|---|---|
| Price (monthly) | ~$47/mo | ~$97/mo | ~$277/mo |
| Websites | 1 | 3 | 10 |
| Courses | 5 | Unlimited | Unlimited |
| People/students | 500 | Unlimited | Unlimited |
| Communities | 1 | 20 | Unlimited |
| Custom domains | 0 | 3 | 10 |
| Monthly emails | 5,000 | 100,000 | 500,000 |
| Marketing funnels | 2 | 100 | Unlimited |
| Live sessions | 10 | 100 | 300 |
| **Memberships/bundles, affiliate, API, white-label** | ❌ | ✅ | ✅ |
| SSO | ❌ | ❌ | ✅ |

- **No free plan** — a **60-day free trial** instead. **0% transaction fees** on all tiers.
- **The big Starter gaps that bite integrators:** **API access, memberships, affiliate marketing, and
  white-label are all Pro+.** A maker who buys Starter expecting to script enrollments will find no
  Developers area.
- **Custom domains are 0 on Starter** — pages stay on `*.newzenler.com`, a common "looks unprofessional"
  complaint. White-label (removing Zenler branding) is also Pro+.
- Branded mobile app is a **$197/mo add-on** on Pro+.

## Integrations

- **Direction:** API/Zapier is built around **writing in** (create user, enroll, subscribe to funnel,
  register for a live class/webinar) and **reading out** (users, courses, funnels, and the four report
  families). Eventing **out** is Zapier-only (no native webhooks).
- **Payments:** Stripe, PayPal, Razorpay. 0% Zenler transaction fee (processor fees still apply).
- **iPaaS:** Zapier, Make, Integrately. Auth everywhere = **API key + subdomain (`X-Account-Name`)**.
- **External ESP/CRM:** trigger a Zap on **New Sale**/**New User** to push the contact into HubSpot/
  Mailchimp and nurture there if you outgrow Zenler's built-in email.

## Data model

Identity is **email**; the API user `id` is a **string** like `313.5c109f1b58473` (store as text, not int).

**User** (note `roles` is an array of role codes — Student 4, Affiliate 7, Lead 8, Instructor 3) — request shape is verbatim from the docs:
```json
{
  "first_name": "Test",
  "last_name": "Test",
  "email": "test@example.com",
  "password": "123456",
  "commission": 10,
  "roles": [3, 7]
}
```

**Response envelope** (every call):
```json
{ "response_code": 201, "message": "People added successfully",
  "data": { "id": "313.5c109f1b58473", "first_name": "test", "last_name": "test", "email": "test@example.com" } }
```

**List pagination block:**
```json
{ "pagination": { "total_items": 142, "items_per_page": 15, "page_index": 1, "total_pages": 10 } }
```

## Quick-start recipes

### Recipe 1 — Auto-enroll a buyer from an external cart (API)

**Trigger:** purchase in ThriveCart/SamCart/Stripe → **steps:** create the user (if new), then enroll them.

```bash
# 1) create the user
curl -s -X POST "https://api.newzenler.com/api/v1/users" \
  -H "X-API-Key: $KEY" -H "X-Account-Name: $SUB" -H "Content-Type: application/json" \
  -d '{ "first_name": "Sam", "email": "buyer@example.com", "roles": [4] }'
# 2) enroll into the course (use the returned id)
curl -s -X POST "https://api.newzenler.com/api/v1/users/313.5c109f1b58473/enroll" \
  -H "X-API-Key: $KEY" -H "X-Account-Name: $SUB" -H "Content-Type: application/json" \
  -d '{ "course_id": 12345 }'
```
```python
import requests
H = {"X-API-Key": KEY, "X-Account-Name": SUB, "Content-Type": "application/json"}
def enroll_buyer(email, course_id, first_name=""):
    u = requests.post("https://api.newzenler.com/api/v1/users", headers=H,
                      json={"first_name": first_name, "email": email, "roles": [4]}, timeout=30).json()
    uid = u["data"]["id"]
    requests.post(f"https://api.newzenler.com/api/v1/users/{uid}/enroll", headers=H,
                  json={"course_id": course_id}, timeout=30).raise_for_status()
    return uid
```
**Gotchas:** API needs **Pro+**. The `id` is a string. No-code alternative: the **Create User** → **Enroll
User** Zapier actions do the same. To bulk-enroll, use `POST /courses/{course_id}/enroll`.

### Recipe 2 — Push new sales/completions into a CRM (Zapier, no webhooks)

**Trigger:** **New Sale** (or **Course Complete**) Zapier trigger → **steps:** map email + course into a
HubSpot/Mailchimp create-or-update action; tag "customer" / "completed". Since there are **no native
webhooks**, Zapier (or Make) is the eventing path — connect with your API key + subdomain. For a pure-API
shop, **poll `/reports/sales/detailed`** on a schedule with `from`/`to` date filters instead.

### Recipe 3 — Nightly revenue/enrollment export (Reports API)

**Trigger:** cron → **steps:** page `GET /reports/sales/detailed` (and `/reports/enrollments/detailed`)
with `limit=15` + `page`, accumulate to your warehouse.
```python
def detailed_sales(frm, to):
    page, rows = 1, []
    while True:
        b = requests.get("https://api.newzenler.com/api/v1/reports/sales/detailed",
                         headers=H, params={"from": frm, "to": to, "limit": 15, "page": page},
                         timeout=30).json()
        rows += b["data"]
        if page >= b["pagination"]["total_pages"]: break
        page += 1
    return rows
```
**Gotchas:** 1000 req/min cap returns **403 "Rate Limited Exceeded"** (a 403 is *rate-limit*, not auth —
branch on the message). Reports come in `brief` and `detailed` variants.

## Integration patterns

- **CRM sync:** Zenler is system-of-record for *enrollment/progress*; your CRM owns *contact + revenue*.
  Map on email. Push in via Create User + Enroll; pull out via the Reports API or Zapier New Sale.
- **No-webhook eventing:** there are no native webhooks — either use Zapier/Make triggers, or **poll** the
  detailed reports with date windows and dedupe on `order_id`/email.
- **Make handlers idempotent** on (email, course_id) — re-running an enroll for an existing user should be
  a no-op in your logic.
- **Backup/export discipline:** reviewers have reported catastrophic content loss; export students
  (Reports API / CSV) and keep your source videos/lesson content off-platform. Don't treat Zenler as your
  only copy.
