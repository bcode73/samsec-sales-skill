# Ruzuku Platform Reference

## Overview

Ruzuku (ruzuku.com) is a simple, teaching-first course + membership platform for coaches, consultants, educators, creatives, and wellness practitioners. Its differentiators are **ease of launching**, **direct Stripe/PayPal payments with 0% transaction fees**, and a focus on the student learning experience (discussions, activities, cohort/live courses). Its trade-offs are a tedious author workflow, a limited feature set vs all-in-one suites, and **no public REST API** — automation runs entirely through Zapier.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Course builder | Drag-and-drop lessons: video, audio, PDF, text, quizzes, assignments, discussions | UI-only (authoring); enrollments are Zapier-accessible |
| Drip scheduling | Release lessons by date or days-after-enrollment | UI-only |
| Quizzes & assignments | Graded quizzes (score captured) and assignment submissions (answers captured) | **Zapier trigger** (Quiz Submitted, Assignment Submitted) |
| Discussions / community | Per-lesson and activity-feed discussions, announcements | **Zapier trigger** (Comment Posted) |
| Progress & achievements | Lesson/course completion tracking, badges | **Zapier trigger** (Lesson Completed, Course Completed) |
| Certificates | Completion certificates | UI-only; **Pro plan** |
| Live webinars | Live group sessions via **Zoom** integration | Native Zoom (Pro); UI-only |
| Automated emails | Course/announcement/reminder emails | UI-only (basic; connect an ESP via Zapier for marketing) |
| Coaching | 1:1 / group coaching offerings | UI-only |
| Membership sites | Recurring-access content sites | UI-only; **Subscription Canceled** is a Zapier trigger |
| Payments | Stripe + PayPal, one-time/subscription/payment plans, coupons, price points | Native; **New Student Enrolled** trigger carries pricing/coupon |
| Storefront / digital products | Public storefront, sell standalone digital products | UI-only; **Pro plan** |
| White-label & custom domain | Remove Ruzuku branding, use your own domain, multiple instructors | UI-only; **Pro plan** |
| Transcription | AI transcription, closed captions, transcript search | UI-only; **Pro plan** |

**Rule of thumb:** anything about a *student moving through a course* (enrolled, completed a lesson/course, submitted a quiz/assignment, commented, canceled) is a Zapier trigger; *enroll/unenroll/find a student* are Zapier actions; everything else (building content, certificates, design) is UI-only.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify against current pricing.*

| Plan | Price | Students | Key limits & gates |
|---|---|---|---|
| **Free** | $0 | **≤5 enrolled** | Unlimited courses, 0% fees, video ≤2 GB/file, live meetings, community, sales pages, payments, tech support |
| **Core** | $99/mo or $997/yr | Unlimited | Everything in Free + unlimited invitations, 1080p HD, video ≤2 GB/file, student tech support |
| **Pro** | $199/mo or $1,997/yr | Unlimited | Everything in Core + **white-label, custom domain, multiple instructors, certificates, public storefront, digital-product sales, AI transcription, closed captions, transcript search, Zoom integration, analytics integration**; video ≤4 GB/file, up to 4K |

- **0% transaction fees on all plans** (Stripe/PayPal processing fees still apply).
- **Zapier integration is free on every plan**, including Free — no separate API/automation add-on.
- 30-day money-back guarantee on paid plans; annual billing saves ~2 months.
- **No API rate limits to design around** — there's no REST API; Zapier task limits are governed by your Zapier plan, not Ruzuku.

## Integrations

| Integration | Direction | Notes |
|---|---|---|
| **Stripe / PayPal** | into Ruzuku | Native payment processing; 0% Ruzuku fee |
| **Zoom** | bidirectional | Live webinars/classes (Pro) |
| **Zapier** | bidirectional | The primary automation surface — 7 triggers, 3 actions, bridges 5,000+ apps |
| **Webhooks by Zapier** | out of Ruzuku | Use when a target system has no native Zapier app — Zapier POSTs Ruzuku event data to your endpoint |
| ESPs (Mailchimp, Kit, ActiveCampaign, etc.) | out of Ruzuku | Via Zapier triggers; Ruzuku's own email is basic |
| CRMs (HubSpot, Salesforce, Pipedrive) | out of Ruzuku | Via Zapier triggers |
| External carts (ThriveCart, SamCart, etc.) | into Ruzuku | Cart purchase → Zapier → Enroll a Student action |

**Data-flow summary:** Ruzuku *reads in* enroll/unenroll requests (Zapier actions) and *emits out* student lifecycle events (Zapier triggers). There is no native inbound or outbound webhook product feature — use the Zapier action for inbound and Webhooks by Zapier for outbound to non-native systems.

## Data model

Ruzuku does not publish a REST schema; the shapes below are reconstructed from the documented Zapier trigger/action fields. Identity across everything is the student's **email**.

```json
// Student (as surfaced by Zapier triggers / Find a Student)
{
  "email": "jane@example.com",     // primary identity
  "first_name": "Jane",
  "last_name": "Doe",
  "student_id": "stu_abc123",       // representative; confirm field name in Zapier
  "enrolled_courses": ["Signature Course"]
}
```
<!-- Constructed from documented Zapier fields — verify exact keys against the live Zapier app -->

```json
// Enrollment event (New Student Enrolled trigger)
{
  "student": { "email": "jane@example.com", "first_name": "Jane", "last_name": "Doe" },
  "course": "Signature Course",
  "price": 197.00,
  "coupon": "LAUNCH50"              // present when a coupon/price-point was used (affiliate tracking)
}
```
<!-- Constructed from documented Zapier fields — verify exact keys against the live Zapier app -->

```json
// Quiz Submitted trigger
{
  "student": { "email": "jane@example.com" },
  "course": "Signature Course",
  "lesson": "Module 2 Quiz",
  "score": 8
}
```
<!-- Constructed from documented Zapier fields — verify exact keys against the live Zapier app -->

## Quick-start recipes

### Recipe 1 — Enroll a student from an external cart
**Trigger:** a purchase in ThriveCart / SamCart / Stripe / a custom checkout.
**Steps:** purchase event → Zapier → **Enroll a Student** action (maps email + name + target course). Ruzuku creates the account if the email is new.

```text
[ThriveCart: Product Purchased]  →  [Ruzuku: Enroll a Student]
   email, first_name, last_name  →   Email, First, Last, Course = "Signature Course"
```

Webhooks-by-Zapier variant for a custom cart that has no Zapier app:
```bash
# Your cart POSTs the sale to a Zapier "Catch Hook" URL; the Zap's second step is the
# Ruzuku "Enroll a Student" action. The cart's outbound call looks like:
curl -X POST "https://hooks.zapier.com/hooks/catch/XXXXX/yyyyy/" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","first_name":"Jane","last_name":"Doe","course":"Signature Course"}'
```
*Gotcha:* on the Free plan this silently stops working past 5 students.

### Recipe 2 — Route new enrollments into a CRM + ESP
**Trigger:** **New Student Enrolled**. **Steps:** fan out to a CRM create-contact action and an ESP add-subscriber action.

```python
# Conceptual handler if you catch the event via Webhooks by Zapier instead of native apps.
# Zapier delivers the Ruzuku enrollment payload to your endpoint; you forward it onward.
import requests

def on_ruzuku_enrollment(payload):
    student = payload["student"]
    # 1) Upsert into your CRM
    requests.post("https://api.yourcrm.example/contacts",
                  json={"email": student["email"],
                        "firstName": student.get("first_name"),
                        "source": "Ruzuku", "course": payload["course"]})
    # 2) Tag in your ESP
    requests.post("https://api.youresp.example/subscribers",
                  json={"email": student["email"], "tags": ["ruzuku-student"]})
```
*Gotcha:* dedupe on `email`; the same person across courses is one contact.

### Recipe 3 — Win-back on canceled subscription (dunning)
**Trigger:** **Subscription Canceled**. **Steps:** add the student to a win-back sequence in your ESP and/or create a CRM follow-up task.

```text
[Ruzuku: Subscription Canceled]  →  [ESP: Add to "Win-back" sequence]
                                  →  [CRM: Create task "Re-engage {email}"]
```
*Gotcha:* Ruzuku has no native dunning/retry — failed-payment recovery and retry logic must live in your payment processor and ESP, not Ruzuku.

## Integration patterns

- **CRM sync:** Ruzuku is a source of student lifecycle events, not a system of record you query. Sync is one-directional out (triggers) plus targeted writes in (Enroll/Unenroll actions). Map on `email`; store the course name and enrollment timestamp as CRM properties. There is no API to poll for drift — reconcile periodically with the in-app CSV export.
- **Affiliate tracking (no built-in engine):** issue each affiliate a unique **coupon** or a dedicated **price-point link**. The `coupon` field on the New Student Enrolled trigger tells you which affiliate referred the sale — pipe enrollments into a Google Sheet keyed by coupon, then calculate and pay commissions yourself. Scales to a few dozen affiliates; beyond that, add a dedicated tool (`/sales-affiliate-program`).
- **Webhook listener pattern:** Ruzuku has no native outbound webhook — use **Webhooks by Zapier** as the bridge. Zapier becomes your retry/queue layer; verify deliveries in the Zap history. There is no signing secret to verify, so don't expose the catch-hook URL and treat the payload as untrusted.
- **Bulk export:** for analytics or migration, use the in-app student/enrollment CSV export rather than scraping — there's no list API.
