# Teachery Platform Reference

## Overview

Teachery (teachery.co) is a **minimalist, design-first course builder** for solopreneurs, designers, and
coaches who want a clean, on-brand course without a heavy LMS. Its pitch is simplicity + **flat-rate
pricing with 0% transaction fees and unlimited everything** (courses, students, admins, domains, hubs).
The deliberate trade-off: it does **not host video/files** (you embed), and skips quizzes, multiple
instructors, and live sessions. Built and run by a tiny, very responsive team.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Course builder | Content blocks (text, **video-embed**, audio, embed), lessons/sublessons | Enroll/revoke via **Zapier**; authoring **UI-only** |
| Course Hubs ("Themes") | Membership grouping of courses | **Add/Revoke User to Theme** via Zapier; config UI-only |
| Drip scheduling | Time-released lessons | **UI-only** |
| Digital downloads | Deliver files/products | **UI-only** (host files externally) |
| Client portals | Private client access | **UI-only** |
| Landing & Payment Pages | Branded sales/checkout pages, custom CSS | **New Order** / **New Lead** Zapier triggers; design UI-only |
| Custom domains | Map your domain | **UI-only** |
| Email | 3 automated types only: welcome, completion, lesson-unlock | **UI-only** (connect an ESP via Zapier for real campaigns) |
| Course affiliates | Add affiliates → unique Payment Page links, recurring commissions | **UI-only** (no affiliate API/trigger) |
| Customer analytics | Basic customer/sales analytics | **UI-only** (CSV export) |
| **Video/file hosting** | **None — embed from YouTube/Vimeo/Drive** | n/a |

**Programmatic interfaces:** **No public REST API.** Integration = API key (Account → Integrations) for
**Zapier** (3 triggers / 4 actions), **Make**, **Pabbly**. No native webhooks beyond Zapier; no MCP. See
`references/teachery-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — verify on the live pricing page; the Lifetime deal is a
limited-time offer.*

| Plan | Price | What's included |
|---|---|---|
| Monthly | ~$49/mo | Everything |
| Annual | ~$470/yr | Everything (≈20% off) |
| Lifetime | ~$550 one-time | Everything (limited-time) |

- **Flat-rate, no feature gating** — every tier unlocks the full feature set with **unlimited** courses,
  customers, admins, custom domains, and Course Hubs.
- **0% transaction fees** on all plans. **14-day free trial.**
- The cost most people miss: because Teachery **doesn't host media**, you'll pay separately for video
  hosting (Vimeo/Bunny/YouTube) on top of the subscription.

## Integrations

- **Direction:** Zapier is built around **writing in** (Add User to Course/Theme on purchase) and
  **eventing out** (Completed Course, New Lead, New Order). No bulk read API — use CSV export.
- **Payments:** Stripe and PayPal via Teachery Payment Pages.
- **iPaaS:** Zapier, Make, Pabbly; bridge non-native systems with **Webhooks by Zapier**.
- **Media:** video/audio/PDF are **embedded** from external hosts — Teachery stores the embed, not the file.
- **Email:** built-in messages are limited to welcome/completion/lesson-unlock; route real nurture to an
  ESP (Kit/Mailchimp/ActiveCampaign) via the New Order / New Lead triggers.

## Data model

Identity is **email**. There is no API object model to query; the iPaaS surface exposes these shapes:

**Order (New Order trigger)** <!-- Constructed from Zapier fields — verify against a live Zap -->
```json
{ "email": "buyer@example.com", "first_name": "Sam", "course_name": "Launch Your Brand", "amount": 149.00, "currency": "USD" }
```

**Enrollment (Add User to Course action input)** <!-- Constructed — verify -->
```json
{ "course": "Launch Your Brand", "email": "buyer@example.com", "first_name": "Sam" }
```

**Theme / Course Hub enrollment (Add User to Theme)** <!-- Constructed — verify -->
```json
{ "theme": "Membership Hub", "email": "buyer@example.com", "first_name": "Sam" }
```

## Quick-start recipes

### Recipe 1 — Auto-enroll a buyer from an external cart (Zapier)

**Trigger:** purchase in ThriveCart/SamCart/Gumroad/Stripe → **steps:** map the buyer's email + first
name + target course into the **Add User to Course** action. For a membership, use **Add User to Theme**.

```text
Zap:
  Trigger: [Cart] New Sale
  Action:  Teachery → Add User to Course
           Course = "Launch Your Brand"
           Email = {{cart.buyer_email}}
           First Name = {{cart.buyer_first_name}}
```
```python
# No REST API — this is conceptual. Teachery is reached via Zapier/Make, not direct HTTP.
# If you must call from code, POST to a "Catch Hook" (Webhooks by Zapier) that runs the
# Teachery "Add User to Course" action:
import requests
requests.post("https://hooks.zapier.com/hooks/catch/123456/abcde/",
              json={"course": "Launch Your Brand", "email": "buyer@example.com", "first_name": "Sam"},
              timeout=30)
```
**Gotchas:** Teachery has **no REST API** — everything routes through Zapier/Make/Pabbly. The API key
(Account → Integrations) only links the account; watch for trailing spaces when pasting it.

### Recipe 2 — Send Teachery leads/orders to your ESP and CRM

**Trigger:** **New Lead** (Landing Page opt-in) or **New Order** → **steps:** create/update a subscriber in
Kit/Mailchimp and a contact in your CRM. Teachery's built-in email only does welcome/completion/lesson-
unlock, so the real sequence lives in the ESP. Use the New Order **Course/Theme Name** filter to branch by
product.

### Recipe 3 — Revoke access when a subscription cancels (dunning)

**Trigger:** your payment processor's "subscription canceled" (Teachery has no native cancel trigger) →
**steps:** **Revoke Course Access From User** (or **Revoke Theme Access**) by email, then add the student
to a win-back sequence in your ESP. Match on the exact email used at purchase.

## Integration patterns

- **CRM sync:** Teachery owns *enrollment*; your CRM/ESP owns *contact + revenue*. Map on email. Push in
  via Add User to Course/Theme; pull out via New Order / Completed Course / New Lead triggers.
- **No bulk read:** there's no list API — schedule a CSV export from customer analytics for warehousing.
- **Idempotency:** make enroll Zaps idempotent on (email, course) so retries don't double-send the welcome.
- **Media plan:** decide your video host up front (Vimeo/Bunny for privacy + clean player, YouTube unlisted
  for free). Teachery only stores the embed — broken/region-blocked source videos break the lesson.
- **Affiliates:** the built-in affiliate feature is UI-only (no API/trigger) — pull affiliate-attributed
  sales from the dashboard; for a programmatic affiliate engine, run it in a dedicated tool.
