# Xperiencify Platform Reference

## Overview

Xperiencify (xperiencify.com) is a **gamified online course platform** — its pitch is that game
mechanics (points, levels, badges, leaderboards, variable rewards, countdowns, celebrations) drive
course **completion**, where the industry average is ~3%. It bundles an all-in-one creator stack
(courses, community, email, CRM, funnels, checkout, basic affiliates, mobile apps) around that
"Experience Engine." Best for solo course creators and coaches who care about engagement/completion and
want one tool instead of stitching Kajabi + Skool + a CRM together.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Course builder | Drag-and-drop lessons, drip, quizzes/assessments, certificates | Enroll/remove via **API** + **Zapier**; authoring is **UI-only** |
| Gamification "Experience Engine" | XP points, XXP (variable/bonus), badge points (BP), badges, leaderboards, variable rewards, countdowns, celebrations | Award/claw back points via **API** (`redeem_points`/`unredeem_points`); design is **UI-only** |
| Students / access | Add, suspend, unsuspend, remove from one or all courses | **API + Zapier** |
| Tags & custom fields | Tag students, set custom fields (segmentation) | **API + Zapier** |
| Community / groups | Forums, groups, onsite chat | **UI-only** |
| Email | Broadcasts + autoresponders (built in) | **UI-only** for sends; route via Zapier to an external ESP if you need real automation |
| CRM + funnels + checkout | Sales pipeline, funnels, 1-click upsells, order bumps | Mostly **UI-only**; purchases can trigger enroll **Zaps** |
| Affiliate tracking | `?ref=affiliate_name` link tracking, CSV report | **UI-only** (no payout automation) |
| AI "Ask the Expert" bot | Course Q&A assistant | **UI-only** |
| SMS / voicemail / calls | 2-way SMS, ringless voicemail, phone | **UI-only** |
| Mobile apps | iOS & Android student apps | **UI-only** |
| Webhooks | Export student data to a webhook on events | **Webhook-accessible** (via Zapier triggers) |

**Programmatic interfaces:** REST API (`https://api.xperiencify.io`, `?api_key=`), Zapier (4 triggers /
8 actions — also Pabbly & Make), and webhook export. No MCP server. See
`references/xperiencify-api-reference.md` for full endpoint detail.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — pricing changes and sources conflict; verify on the live pricing
page before quoting.*

| Plan | Price | Published courses | Active **monthly** students |
|---|---|---|---|
| Sandbox (free) | $0 — full features until you publish | — | — |
| Growth | ~$99/mo | 10 | 1,000 |
| Pro | ~$199/mo | 20 | 5,000 |
| Lifetime | ~$1,499 one-time | 10 | 1,000 |
| Enterprise | custom | — | — |

- **All plans** include: unlimited sites/funnels/courses, gamification, quizzes, community, certificates,
  AI bot, email broadcasts + autoresponders, full CRM, affiliate management, funnels + appointment
  scheduling, landing pages + hosting, integrations (Zapier/Pabbly/Make), and iOS/Android apps. The
  tiers differ mainly by **published-course count** and **active-monthly-student** capacity.
- **The metering unit is _active monthly students_, not total enrolled.** A student who logs in counts
  that month; dormant students don't. Billing can surprise you during a launch spike — size the plan to
  peak monthly active, not lifetime enrollment.
- **API access is not separately gated** in current materials (the key lives in Account → Advanced).
  Some older roundups cite a $49/mo starter (3 courses, 50 students) — treat that as possibly retired.

## Integrations

- **Direction:** the API/Zapier surface is built around **writing into** Xperiencify (enroll students,
  tag, set custom fields, award points) and **reading out** progress (XP, completion %) + **eventing
  out** (added/completed/canceled/tagged).
- **Payments:** Stripe (native for installments + subscriptions) and PayPal (one-time course payments
  only). The **Removed (Canceled) Subscription** trigger fires specifically on a **Stripe** cancellation.
- **iPaaS:** Zapier, Pabbly Connect, Make. Third-party connectors also exist on Pipedream.
- **External ESP/CRM pattern:** because in-app email is basic, many creators trigger a Zap on enrollment
  to add the buyer to HubSpot/ActiveCampaign/Mailchimp and run nurture there.

## Data model

Identity is **email** everywhere. Key objects:

**Student** <!-- Constructed from docs — verify against live API -->
```json
{
  "email": "buyer@example.com",
  "first_name": "Sam",
  "last_name": "Rivera",
  "phone": "+15551234567",
  "tags": ["vip", "early-bird"],
  "custom_fields": { "source": "thrivecart" }
}
```

**Course** <!-- Constructed from docs — verify against live API -->
```json
{ "course_id": 12345, "name": "The Gamified Launch Course", "published": true }
```

**Enrollment / progress** (from `POST /student/info/`) <!-- Constructed from docs — verify against live API -->
```json
{
  "course_id": 12345,
  "xp_earned": 480,
  "xp_total": 1200,
  "xxp_earned": 60,
  "completion_percent": 40
}
```

**Points types:** `xp` (experience), `xxp` (variable/bonus), `bp` (badge points) — the currencies the
`redeem_points`/`unredeem_points` endpoints move.

## Quick-start recipes

### Recipe 1 — Auto-enroll a buyer from an external cart (API)

**Trigger:** purchase in ThriveCart/SamCart/Stripe → **steps:** call create-student with the buyer's
email + `course_id`; the call creates the account if new and returns a magic link you can email.

```bash
curl -s -X POST "https://api.xperiencify.io/api/public/student/create/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "student_email": "buyer@example.com", "first_name": "Sam", "course_id": 12345 }'
```
```python
import requests
def enroll(email, course_id, api_key, first_name=""):
    r = requests.post(
        f"https://api.xperiencify.io/api/public/student/create/?api_key={api_key}",
        json={"student_email": email, "first_name": first_name, "course_id": course_id},
        timeout=30)
    r.raise_for_status()
    return r.json().get("magic_link")
```
**Gotchas:** the API key is in the URL — call only from a server. Email is the identity key and can't be
changed later. If you'd rather not write code, the **Add Student to a Course** Zapier action does the same.

### Recipe 2 — Sync completions into your CRM (Zapier trigger)

**Trigger:** **Student Completed Course** → **steps:** map `student_email` + `course_id` into a
create/update-contact action in HubSpot/Mailchimp, set a "course_complete" property, optionally fire a
certificate-delivery or upsell email. Use **Tag Added to a Student** the same way to mirror Xperiencify
segments into your ESP. (No HMAC signature on the webhook — verify the student via
`POST /student/info/` before granting anything sensitive downstream.)

### Recipe 3 — Award bonus XP from another tool (points API)

**Trigger:** buyer completes an action elsewhere (books a call, refers a friend) → **steps:** grant
gamification currency so the leaderboard/celebration reflects it.

```bash
curl -s -X POST "https://api.xperiencify.io/api/public/student/redeem_points/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "course_ids": [12345], "student_ids": [98765],
        "points_type": "xp", "operation_type": "REDEEM_POINTS", "value": 100 }'
```
**Gotchas:** this endpoint takes `student_ids`/`course_ids` arrays (not email) — resolve IDs first via
`GET /coach/students/`. Use `unredeem_points` to reverse an erroneous award.

## Integration patterns

- **CRM sync:** Xperiencify is the system of record for *progress/XP*; your CRM is the system of record
  for *contact + revenue*. Map on email. Push enrollments out on **Student Added to Course**, push
  completions on **Student Completed Course**, and run dunning/win-back off **Removed (Canceled)
  Subscription** (Stripe only).
- **Webhook listener:** no published signature — restrict to a secret URL and re-verify via
  `POST /student/info/` before acting. Expect retries to be your responsibility; make handlers idempotent
  on (`student_email`, `course_id`, `event`).
- **Batch/export:** for a full roster, prefer the in-app **CSV export** (Students page, filterable by
  affiliate/course) over paging `/coach/students/`, since pagination params aren't documented.
- **Affiliate tracking:** built-in tracking is a `?ref=` URL param recorded against the purchase +
  CSV export; there is **no automatic payout**. For a real affiliate engine, run payouts manually from
  the export or bolt on a dedicated tool.
