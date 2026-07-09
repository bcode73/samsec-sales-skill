<!-- Source: https://waitlistly.live/ , https://waitlistly.live/help , https://waitlistly.live/sitemap.xml (homepage + /growth are JS-rendered SPAs; fetched 2026-06) -->

# Waitlistly Platform Reference

## Overview

Waitlistly (waitlistly.live) is a hosted **pre-launch waitlist landing-page builder** positioned around idea validation — "The Fastest Way to Validate Your Idea." You stand up a waitlist page in minutes, collect emails before you build, and decide whether demand justifies building. It targets founders, makers, indie hackers, and solopreneurs. Differentiator: speed-to-launch and a validation framing rather than a deep ESP/CRM feature set.

> **Research caveat.** Waitlistly's homepage and `/growth` page are JavaScript-rendered single-page apps that returned no extractable copy, there is no public `/pricing`, `/api`, or `/docs` page, and no third-party reviews exist. The **verified** facts come from the OG/meta description, the sitemap, and the two published help guides (Custom Domains, Webhooks/Integrations). Everything tagged *(unconfirmed)* below needs checking against the live app before you rely on it.

## Capabilities & automation surface

| Capability | What it does | Automation surface | Confidence |
|---|---|---|---|
| Hosted waitlist landing page | Launch a waitlist/validation landing page that collects emails | UI-only (built in-app) | Verified (core pitch) |
| Custom domains | Point your own domain/subdomain at the Waitlistly page | UI + DNS | **Verified** (Help → Custom Domains) |
| On-signup webhooks | "Send real-time lead data to Zapier, Make, Slack, or your own API when someone joins your waitlist" | **Webhook-accessible** (egress) | **Verified** (Help → Webhooks/Integrations) |
| Zapier / Make connection | No-code routing of the webhook to 1000s of apps | Webhook → iPaaS | **Verified** (named in Help) |
| Slack notification | Real-time signup ping to a channel | Webhook → Slack | **Verified** (named in Help) |
| Referral / viral growth | A `/growth` page exists in the sitemap, implying viral/referral mechanics | Unknown | *(unconfirmed — page wouldn't render)* |
| Analytics on signups/traffic | Signup and traffic stats are typical of the category | UI-only (assumed) | *(unconfirmed)* |
| Email broadcasts | Sending launch/nurture emails from inside Waitlistly | — | *(unconfirmed — no evidence; treat as not present and use your ESP)* |
| Public REST API | Programmatic read/write of signups | — | **Verified absent** (no `/api`, `/docs`; Help documents only webhooks + domains) |
| MCP server | — | — | None found |

**Rule of thumb:** the only confirmed programmatic hook is the **on-signup webhook**. Build integrations around that (plus Zapier/Make), not around an API that doesn't exist.

## Pricing, limits & plan gates

- **No public pricing page** — the sitemap contains no `/pricing`. The only confirmed public claim is **"free to start."**
- Tiers, subscriber caps, custom-domain gating, and any webhook/automation gating live **behind sign-in** — confirm in-app.
- Treat any pricing figure from third-party listicles as best-effort; Waitlistly's own pages don't publish numbers as of this research.
- **Integration impact:** because the API doesn't exist on any tier, the free-vs-paid question that actually matters is whether **webhooks and custom domains** are free or gated — verify both in-app before committing a launch to them.

## Integrations

Data flow is **one-directional egress** (Waitlistly → elsewhere) on signup:

- **Webhook (your own endpoint):** real-time POST when someone joins → write to your CRM/warehouse/Slack.
- **Zapier / Make:** no-code routing of the same signup event to 1000s of destinations (HubSpot, Airtable, Google Sheets, ESPs, etc.).
- **Slack:** direct signup notifications to a channel.
- **No native CRM connectors documented**, **no inbound API**, **no MCP**. Anything richer than "on join, push the lead out" is not supported as of this research.

## Data model

> ⚠️ **The webhook payload schema is NOT published.** Do not build against the shape below as if it were authoritative. The fields shown are a *representative* guess at what a "lead joined the waitlist" payload typically carries — **log a real delivery first and replace these with the actual field names.**

```json
<!-- Constructed/representative — NOT from Waitlistly docs. Verify against a live webhook delivery before mapping. -->
{
  "event": "signup.created",
  "email": "founder@example.com",
  "waitlist": "my-idea",
  "referrer": null,
  "created_at": "2026-06-19T12:00:00Z"
}
```

Practical handling, regardless of exact shape:
- **Dedupe** on whatever stable identifier the payload carries (an `id`/`uuid` if present, else `email` + `created_at`).
- **Guard** optional fields (referrer/UTM/custom questions may be absent for direct signups).
- **Don't trust it as authenticated** — no signature scheme is documented (see Integration patterns).

## Quick-start recipes

### Recipe 1 — Test the webhook end-to-end before wiring a CRM
Stand up a throwaway receiver, point Waitlistly's webhook at it, submit a test signup, and read the real payload.

```bash
# Simplest possible inspector: pipe deliveries to your terminal via a tunnel
# (e.g. run a local server on :5000, expose it, paste the public URL into
#  Waitlistly → Help → Webhooks/Integrations as your endpoint)
curl -X POST http://localhost:5000/waitlistly \
  -H "Content-Type: application/json" \
  -d '{"event":"signup.created","email":"test@example.com","created_at":"2026-06-19T12:00:00Z"}'
# ^ this is just a local sanity check of YOUR handler. The real schema comes
#   from an actual Waitlistly delivery — log it (Recipe 2) and adapt.
```

### Recipe 2 — Webhook → CRM/Slack handler (log first, then map)
```python
# Flask receiver. First deploy logs the raw body so you learn the real schema,
# THEN you map fields. No documented signature — use an unguessable path.
from flask import Flask, request, abort
import json, logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
SEEN = set()  # swap for Redis/DB in production

@app.post("/hooks/waitlistly-9f3c2a")  # secret-ish path stands in for a signature
def waitlistly():
    if not request.is_json:
        abort(400)
    payload = request.get_json()
    logging.info("WAITLISTLY RAW: %s", json.dumps(payload))  # <-- inspect this on first runs

    email = payload.get("email")
    if not email:
        return ("ignored: no email", 200)

    # Dedupe on the most stable id available
    key = payload.get("id") or payload.get("uuid") or f'{email}:{payload.get("created_at")}'
    if key in SEEN:
        return ("duplicate", 200)
    SEEN.add(key)

    # upsert_contact_to_crm(email=email, source="waitlistly", joined=payload.get("created_at"))
    # post_to_slack(f":tada: New waitlist signup: {email}")
    return ("ok", 200)
```
**Gotchas:** respond `2xx` fast (do CRM writes async if they're slow); the first few runs are for *reading* the payload, not trusting it; once you know the real id field, dedupe on it.

### Recipe 3 — No-code route to your ESP/CRM (Zapier or Make)
1. In Waitlistly: **Help → Webhooks/Integrations**, connect Zapier (or Make).
2. Trigger: *New waitlist signup*. 3. Action: *Create/Update contact* in your ESP/CRM (or *Add row* in Google Sheets) and/or *Send Slack message*.
3. Add a filter step if you want to drop obvious junk (no `@`, disposable domains) before it hits your ESP.
4. On launch day, broadcast from the ESP — Waitlistly is the capture layer, not the sender.

## Integration patterns

- **Webhook listener:** no documented HMAC/signature and no documented retry policy. Mitigate with (a) an unguessable endpoint path or a shared-secret query param, (b) payload-shape validation, (c) idempotency keyed on a stable id, (d) a periodic reconciliation/export since you can't re-pull via an API.
- **CRM sync architecture:** treat Waitlistly as a **source-only** node. Map `email` (+ created-at, referrer/UTM if present) into your CRM; resolve conflicts in the CRM, not Waitlistly (you can't write back). Sync is event-driven (on join), not scheduled.
- **No batch/backfill API:** if the webhook wasn't configured from day one, earlier signups can't be pulled programmatically — export from the dashboard manually. Configure the webhook **before** you start driving traffic.

## Fit vs. other indie waitlist tools

| Need | Better fit |
|---|---|
| Fastest possible idea-validation page, custom domain, free to start | **Waitlistly** |
| Documented REST API + signed (HMAC) webhooks + built-in email broadcasts | `/sales-waitlister` |
| Developer widget, unauthenticated signup API, censored public leaderboard | `/sales-getwaitlist` |
| One-time lifetime pricing instead of subscription | `/sales-launchlist` |
| Waitlists **plus** giveaways/contests with fraud webhooks and a REST API | `/sales-kickofflabs` |
| Multi-level (L1/2/3) referral/affiliate tracking with coupon groups | `/sales-referralhero` |
| The growth *strategy* (lead magnets, referral design, cross-promotion) — tool-agnostic | `/sales-audience-growth` |
