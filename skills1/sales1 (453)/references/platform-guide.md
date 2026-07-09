# RafflePress Platform Guide

Full reference for the `sales-rafflepress` skill. Read the section you need; don't dump the whole file.

> *Pricing/plan gates are best-effort from research (2026-06) — the marketing site, docs, and reviews. Verify in-account.*

## What RafflePress is

A **WordPress giveaway & contest plugin** (by Awesome Motive, makers of WPForms/OptinMonster) for **viral list growth**. You build a giveaway with a drag-and-drop builder, add bonus-entry actions, publish a hosted giveaway landing page (or embed it), and collect entrants — mostly to grow an **email list + social following**. Self-hosted on WordPress. Target users: bloggers, marketers, ecommerce/WordPress site owners, agencies.

**Giveaway, not affiliate.** Refer-a-friend here is a *giveaway entry mechanic* (referrals earn extra entries), not a commission-based affiliate program. For partner/affiliate programs, use `/sales-affiliate-program`.

## Module map — webhook vs native vs UI-only

| Module | Surface | Notes |
|---|---|---|
| Giveaway builder / templates | **UI-only** | Drag-and-drop in WP admin; no API to create giveaways |
| Entry actions (30+) | **UI-config** | email signup, social follows, refer-a-friend, shares, video, polls, surveys, comments, image upload |
| Email-signup capture | **Webhook + native ESP + Zapier** | the entrant identity (name/email) flows out here |
| Social-action completion | **UI/reporting only** | explicitly **NOT** sent over webhook |
| Refer-a-friend (viral) | **UI + link** | +10 entries/referral; tracked via referral link |
| Native ESP/CRM sync | **Native integration** | 15+ ESPs via the Join-an-Email-Newsletter action |
| Zapier | **REST-hook trigger** | "New Contestant Created"; API key per newsletter action |
| Uncanny Automator | **WP automation** | trigger other plugins on entry |
| Fraud protection | **UI** | built-in; not an API surface |
| Winner selection | **UI** | random winner picker |
| Access permissions / prefill | **WP hooks / URL params** | developer customization |

## Pricing & plan gates (best-effort)

- **Lite** — free plugin on WordPress.org; basic giveaways, limited entry actions/integrations.
- **Pro (paid license)** — webhooks, refer-a-friend, the full 30+ entry actions, 15+ ESP integrations, Zapier, Automator. Sold as **one-time / lifetime** licensing:

| License | Price (one-time) | Scope |
|---|---|---|
| **Single Site** | ~$299 | 1 site, all features, lifetime updates, 1-yr support |
| **Unlimited Sites** | ~$349 | unlimited sites, all features, lifetime updates, 1-yr support |

> RafflePress has historically also sold annual Plus/Pro/Growth/Ultimate tiers; the site currently shows lifetime pricing. Treat exact tier names/prices as best-effort and confirm on the pricing page. You also need a **self-hosted WordPress site** (not WordPress.com low tiers).

## Data model (entrant — JSON shapes)

Webhook payload fields (the only entrant data that leaves RafflePress programmatically):

```json
{
  "fullname": "Jane Smith",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "giveaway_id": "123",
  "giveaway_name": "Summer Launch Giveaway",
  "sign_up_date": "2026-06-27"
}
```

- **Identity = `email`.** Dedupe and reward on `email` + `giveaway_id`.
- **Not included:** which social accounts were followed/shared (third-party action data stays in RafflePress).
- *(The docs publish no payload example — this is constructed from the documented field list. Verify the exact envelope against a live delivery.)*

## Quick-start recipes

### Recipe 1 — Receive entrants on your own endpoint (webhook)

In WP admin: **RafflePress → Settings → Webhooks** → enable → **Webhook 1** → set **Request URL**, **Format = JSON**, and add a secret **custom header** (there's no HMAC).

Python handler:

```python
@app.post("/rafflepress-webhook")
def rafflepress_webhook(payload: dict, x_auth: str = Header(default="")):
    # No HMAC — verify the secret header you configured in RafflePress.
    if x_auth != RAFFLEPRESS_SECRET:
        return Response(status_code=401)
    key = (payload["email"], payload["giveaway_id"])   # idempotency key
    if already_processed(key):
        return {"ok": True}
    upsert_contact(
        email=payload["email"],
        name=payload.get("fullname"),
        giveaway=payload.get("giveaway_name"),
        joined=payload.get("sign_up_date"),
    )
    mark_processed(key)
    return {"ok": True}
```

FORM format works the same way — read form fields instead of JSON.

### Recipe 2 — Auto-add entrants to an ESP (no code)

Add a **Join an Email Newsletter** entry action to the giveaway and select your ESP (Mailchimp, Kit, ActiveCampaign, MailerLite, Brevo, …). Entrants who complete that action sync directly — no endpoint to host. Turn on double opt-in in the ESP to filter junk.

If your ESP isn't native: select **Zapier** in that action's dropdown, copy the **API key**, and build a zap — trigger **New Contestant Created** → your app. (Only **one** newsletter action per giveaway when using Zapier.)

### Recipe 3 — Pre-fill the entry form / carry identity from a landing page

RafflePress supports **URL-parameter prefill**: pass values in the giveaway page URL to pre-populate entry fields (e.g. a known email for a logged-in user, or UTM/identity from your campaign). Combine with the access-permission filter (WordPress) to control who can manage giveaways. Exact parameter/hook names are in the live Developer docs.

## Fraud & quality watch

Viral giveaways attract fake/disposable emails, multi-entry, and **self-referral** abuse (refer-a-friend gives +10 entries). Use built-in fraud protection, but also: validate/verify emails before counting, require double opt-in, watch for same-person referrals, and review entrants before awarding prizes. For list quality/deliverability afterward, use `/sales-deliverability`.

## When to route out

- Which giveaway tool / viral mechanics across tools → `/sales-audience-growth`
- Generic CRM/ESP wiring (iPaaS) → `/sales-integration`
- Email sequences for the collected list → `/sales-email-marketing`
- Commission-based **affiliate/partner** program (not giveaway referrals) → `/sales-affiliate-program`
- Deliverability of the emails you collect → `/sales-deliverability`
