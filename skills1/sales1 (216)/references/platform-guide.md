# GroupApp Platform Guide

Detailed reference for GroupApp (group.app) — the module map (Zapier/webhook/API/UI-only), plan gates, the data model, and quick-start automation recipes.

## What GroupApp is

A **learning-focused community platform** (group.app) for creators, coaches, and learning businesses — communities *plus* a genuinely deep LMS in one place. Where Circle/Skool/Mighty Networks bolt shallow courses onto a community, GroupApp leads with a **drag-and-drop curriculum builder** (modules/lessons, enforced completion, native or embedded video), **auto-issued branded certificates**, progress tracking, events, and **B2B group subscriptions** (one manager buys access for a team) — all on **0% transaction fees**. Best fit: **group-coaching, cohort, and certification businesses** that want structured course delivery + peer community without stitching an LMS to a separate community tool. Weaker on white-label/branding depth than Circle and gamification depth than Skool.

## Module map — integration surface

| Module | What it does | Integration surface |
|---|---|---|
| **Communities / channels** | Spaces, posts, discussion | Zapier (add/remove channel member; New Post trigger); UI |
| **Members / segments** | Accounts + segment (tag) grouping | Zapier (create/invite, add/remove segment) + **webhooks** (New member, Profile updated) + **API token** |
| **Courses / LMS** | Curriculum builder, modules/lessons, enforced completion, certificates, progress | UI-built; Zapier (enroll, remove enrollment, lessons completed, Course completed) |
| **Events** | Scheduling + RSVP | Zapier (Event RSVP); UI |
| **Payments / subscriptions** | Stripe, **0% GroupApp fee** | Native Stripe; Zapier (New Payment, Payment Failed, Subscription canceled) |
| **Group subscriptions (B2B)** | One manager buys seats for a team | UI |
| **Membership questionnaire** | Application/approval questions | Zapier (Membership Questionnaire trigger) |
| **Auth / SSO** | Login + custom integrations | OAuth |

**Rule of thumb:** programmatic access is **API token + webhooks + Zapier/Pabbly/Integrately**; a full public REST endpoint reference wasn't found, so confirm direct-call endpoints in-account. No MCP server.

## Plans & gates (best-effort — verify; pricing changes often + sources conflict)

> *Pricing best-effort from 2026-06 research; sources disagree — confirm on group.app/pricing.*

- Entry pricing appears to start around **~$24–$49/mo** (one source quotes "from $24/mo," a third-party roundup lists **$49–$259/mo** across tiers) — treat the exact entry point as best-effort.
- **0% transaction fees on every plan** (you connect your own Stripe; Stripe's own fees still apply) — a consistent GroupApp selling point.
- Higher tiers raise member/admin limits and unlock advanced LMS/branding/B2B features.
- Differentiators vs peers: **deep LMS + certificates + group (B2B) subscriptions**; trade-off is lighter white-label/branding than Circle and lighter gamification than Skool.

## Data model

```json
// Member (identity = email)
{ "email": "jane@example.com", "name": "Jane Doe", "segments": ["vip"], "channels": ["general"] }

// Enrollment
{ "member_email": "jane@example.com", "course": "Signature Program", "status": "enrolled" }

// Payment
{ "member_email": "jane@example.com", "amount": 4900, "currency": "USD", "status": "succeeded" }
```

- **Email is the identity key** across members/enrollments/payments — dedupe on it.
- **Segments** are the tag/grouping primitive that drives automations.

## Quick-start recipes

### Recipe 1 — Enroll a buyer from an external cart (Zapier/webhook)

Sell on an external cart but deliver in GroupApp: trigger on the cart's purchase → Zapier **"Enroll a member in a course"** action (creates the member + enrolls). Or POST to a GroupApp webhook/automation that grants access. Key the enrollment on the buyer's **email**.

```text
Cart "purchase" (Stripe/SamCart/Gumroad)  →  Zapier  →  GroupApp "Enroll a member in a course"
   map: buyer email → member_email, product → course
```

### Recipe 2 — Route "Course completed" to issue/record a credential (Python webhook handler)

GroupApp auto-issues certificates, but you can also sync completions to your own system (CRM, credential registry, Slack):

```python
from flask import Flask, request
import requests
app = Flask(__name__)

@app.post("/groupapp/course-completed")
def course_completed():
    evt = request.get_json(force=True)           # confirm keys against a real delivery
    email  = evt.get("member_email") or evt.get("email")
    course = evt.get("course")
    requests.post("https://your-crm.example/api/events",
        json={"email": email, "event": "course_completed", "course": course}, timeout=20)
    return ("", 200)
```

Wire it via a GroupApp webhook (Settings → Integrations) or the **Course completed** Zapier trigger.

### Recipe 3 — Dunning on failed payments

Use the **Payment Failed** trigger (Zapier or webhook) to start a recovery sequence in your ESP, and **Subscription canceled** to trigger a win-back. Fulfill access only on **New Payment** (success), never on enrollment intent alone.

```text
GroupApp "Payment Failed"     → Zapier → ESP dunning sequence (retry reminders)
GroupApp "Subscription canceled" → Zapier → ESP win-back + access removal
```

## Known limitations to set expectations on

- **No published full REST reference** — for anything beyond Zapier/webhooks, generate an API token and confirm endpoints in-account; don't assume REST paths.
- **Lighter white-label/branding than Circle** and **lighter gamification than Skool** — pick GroupApp for *LMS depth + community*, not for the flashiest community design or game mechanics.
- **It doesn't send marketing email** — connect an ESP for sequences (use the payment/enrollment triggers to drive them).
- **Pricing entry point is fuzzy across sources** — verify the current tier that includes the features (advanced LMS, B2B group subscriptions, branding) you need.
- **Marketing/pricing pages are JS-rendered** — re-verify current features/pricing on the live site rather than trusting cached third-party numbers.
