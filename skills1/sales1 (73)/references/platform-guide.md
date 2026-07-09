# Builderall Platform Guide

Detailed reference for Builderall — the module map (what's API-accessible vs UI-only), plan gates, the MailingBoss data model, and quick-start automation recipes.

## What Builderall is

A **budget all-in-one digital marketing suite** (founded 2011, Erick Salgado). One subscription bundles ~50 tools: website/funnel builders, email (MailingBoss), CRM, courses/membership, e-commerce checkout (SuperCheckout), webinars, booking, chatbot, heatmaps, and A/B testing. Positioned as a low-cost alternative to ClickFunnels / Kartra / Kajabi. Best fit: **non-technical solopreneurs and small creators who want everything in one bill and dread wiring tools together with Zapier.** Weakness: it's broad, not deep — no single module beats the best-of-breed specialist, and the breadth creates a real learning curve.

## Module map — integration surface

| Module | What it does | Integration surface |
|---|---|---|
| **Website / Funnel builders** (3: responsive, pixel-perfect, mobile-first) | Multi-page sites, blogs, conversion funnels | **UI-only**; capture leads into MailingBoss lists |
| **MailingBoss** | Email autoresponder, lists, campaigns, automations, tags | **API-accessible** (subscribers) + **inbound webhooks** (per-list URL) |
| **SuperCheckout** | Carts, order bumps, upsells, payment | **UI-only**; trigger MailingBoss tags on purchase |
| **CRM** | Pipelines, contact management | **UI-only** (sync via MailingBoss contacts + iPaaS) |
| **Courses / Membership** | Hosted courses, drip, locked lessons | **UI-only** |
| **Webinars** | Live + (plan-gated) automated/evergreen webinars | **UI-only** |
| **Chatbot / Booking / Heatmaps / A·B testing** | Engagement + analytics tools | **UI-only** |

**Rule of thumb:** if you need data in/out programmatically, the path is **MailingBoss API + webhooks + Zapier/Make/Pabbly/Integrately**. There is no broad REST API across funnels/checkout/courses and **no MCP server**.

## Plans & gates (best-effort — verify; pricing changes often)

> *Pricing and plan gates are the fastest-moving facts here. Treat every number below as best-effort from 2026-06 research and confirm on builderall.com/pricing.*

- **Free plan** — exists; limited tools/usage. Good for kicking the tires.
- **Entry tier** — ~$14.90–17/mo; core builder + MailingBoss with caps.
- **Funnel/Marketer tier** — historically the **funnel builder (and heavier features) sit on a higher tier (~$79.90/mo)**. Don't assume funnel building is on the cheapest plan — confirm before recommending Builderall as a "cheap funnel builder."
- Higher tiers raise contact/list limits, unlock automated webinars, and add agency/white-label options.

When a user asks "is it cheap?": yes at the entry tier, **but the funnel builder and the marquee features are usually gated higher** — set that expectation.

## MailingBoss data model

The programmatic objects are **lists** and **subscribers** (built on a MailWizz-style codebase).

```json
// Subscriber (representative — confirm envelope in your account)
{
  "subscriber_uid": "ab12cd34ef",   // contact id WITHIN a list
  "list_uid": "ls9f8e7d6c",         // the list it belongs to
  "email": "jane@example.com",
  "FNAME": "Jane",                   // custom fields are uppercase MailWizz field tags
  "LNAME": "Doe",
  "taginternals": "app-trial,lead",  // tags
  "status": "confirmed"              // confirmed | unconfirmed | unsubscribed
}
```

```json
// List (representative)
{
  "list_uid": "ls9f8e7d6c",
  "name": "Main Newsletter"
}
```

Key facts:
- A subscriber is **scoped to a list** — the same person on two lists has two `subscriber_uid`s. Dedupe on `email`, not `subscriber_uid`.
- **Tags** ride on `taginternals`. Tags drive MailingBoss automations and segmentation.
- Custom fields use **field tags** (e.g. `FNAME`, `LNAME`) — create them in the list settings first, then pass them as body params.

## Quick-start recipes

### Recipe 1 — Create a contact and tag it (upsert by email)

Search first so you don't create duplicates, then create-or-update.

```python
import requests

BASE = "https://member.mailingboss.com/integration/index.php"
TOKEN = "YOUR_TOKEN"
LIST_UID = "ls9f8e7d6c"

def upsert(email, fname=None, tags=None):
    # 1) search by email within the list
    s = requests.post(
        f"{BASE}/lists/subscribers/search-by-email/{TOKEN}",
        data={"email": email, "list_uid": LIST_UID},
        timeout=30,
    ).json()
    sub_uid = s.get("subscriber_uid") if isinstance(s, dict) else None

    body = {"list_uid": LIST_UID, "email": email}
    if fname: body["FNAME"] = fname
    if tags:  body["taginternals"] = ",".join(tags)

    if sub_uid:  # 2a) update existing
        body["subscriber_uid"] = sub_uid
        return requests.post(f"{BASE}/lists/subscribers/update/{TOKEN}", data=body, timeout=30).json()
    # 2b) create new
    return requests.post(f"{BASE}/lists/subscribers/create/{TOKEN}", data=body, timeout=30).json()

upsert("jane@example.com", fname="Jane", tags=["app-trial"])
```

> The search response envelope/field names are best-effort — log the raw response once and adjust the `.get("subscriber_uid")` extraction to match what your account returns.

### Recipe 2 — Add a lead from your app to a MailingBoss list

```bash
curl -X POST \
  "https://member.mailingboss.com/integration/index.php/lists/subscribers/create/<TOKEN>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "list_uid=<LIST_UID>" \
  --data-urlencode "email=lead@example.com" \
  --data-urlencode "FNAME=Lead" \
  --data-urlencode "taginternals=from-app"
```

### Recipe 3 — Form/webhook → list (no code)

1. In MailingBoss, open the target **list → get its webhook URL**.
2. Point your external form's webhook (or a Zapier/Make/Pabbly/Integrately "Create MailingBoss contact" action) at it.
3. Map the form's email + name fields to `email` / `FNAME`. This is the supported pattern when a native connector doesn't exist.

### Recipe 4 — Tag on purchase to drive follow-up

SuperCheckout is UI-only, so wire purchase → email follow-up with **tags**: configure the checkout/automation to apply a MailingBoss tag (e.g. `bought-course`) on purchase, then trigger the post-sale MailingBoss automation off that tag. For external stores, send the purchase event through iPaaS to the create/update endpoint with `taginternals=bought-course`.

## Deliverability note

MailingBoss is frequently flagged in reviews as weaker than dedicated ESPs. Inbox placement depends on **your** domain authentication (SPF/DKIM/DMARC), list hygiene, and warm-up — not the platform alone. For inbox-placement strategy, route to `/sales-deliverability`. If deliverability is mission-critical, consider sending through a specialist ESP and using Builderall for pages/funnels.

## Reliability note

Reviews report periodic outages (site, SuperCheckout, or email sends) and slow support (multi-day, no phone). For anything time-sensitive (a launch), **build and test ahead**, keep a fallback for checkout/email, and don't cut over mid-launch.
