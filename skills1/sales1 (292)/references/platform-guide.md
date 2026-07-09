# LaunchList Platform Reference

## Overview

LaunchList (getlaunchlist.com) is viral pre-launch waitlist software with gamified referrals — signups get a unique referral link and jump the queue by inviting others. Its differentiator in the waitlist category is **one-time lifetime pricing** (pay once per submission tier, no subscription). Built for indie hackers, makers, and pre-revenue founders; claims 3,000+ startups launched and 6M+ early users collected.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Waitlist forms | Embed widget (iframe) or custom DIY form posting to `https://getlaunchlist.com/s/FORM_KEY` | **Form-POST-accessible** (ingress); AJAX submission Grow+ |
| Hosted landing pages | Branded, SEO-ready standalone page with signup form, leaderboard, social proof counters | UI-only |
| Gamified referrals | Unique referral links, queue-position jumping, leaderboard, reward/milestone settings, position inflation | UI-only config; events visible via webhooks |
| Direct link to signup | Shareable URL that signs people up without a website | UI-only |
| Analytics dashboard | 15+ data points per signup (location, device, browser, language, UTM, referral channel), filtering, sorting | UI-only; **CSV export** is the only bulk egress |
| Email notifications | Welcome emails (Launch+), email verification (Launch+), custom-domain sending (Grow+) | UI-only |
| Spam protection | Disposable-email blocklist (3,000+ domains), `_gotcha` honeypot, ReCaptcha v2, Cloudflare, domain/pattern blocks | Form-level config |
| Webhooks | `new_user` + `email_verify` JSON POSTs to your URL | **Webhook-accessible** (Grow+) |
| Zapier | New Submission + Email Verified triggers, access-token auth | **iPaaS-accessible** (Grow+); triggers only, no actions |
| Slack notifications | Per-signup alerts to a channel | UI config (Launch+) |
| Team management | Multi-user access with permissions | UI-only (Grow+) |
| Public REST API | — | **Does not exist** — "planned" on the roadmap |

## Pricing, limits & plan gates

> Best-effort from getlaunchlist.com/pricing as of 2026-06-06 — verify before committing. One-time charge for lifetime access, per project; "no monthly subscription."

| Plan | Price | Submissions | Key unlocks |
|---|---|---|---|
| Free | $0 | 100 | Form builder, custom forms, referral management, CSV export, basic analytics, email notifications, fraud detection, email validation, chat support |
| Launch | $29 one-time | 500 | Email verification, welcome emails, Slack notifications, position inflation, reward/milestone settings, thank-you page customization, language translation, ReCaptcha |
| Grow | $79 one-time | 10,000 | **Webhooks, Zapier**, unlimited team members, custom-domain email sending, AJAX form submission, conversion tracking, brand removal, priority support |
| Scale | Custom | 100,000+ | 10K email-validation credits, dedicated account manager, onboarding, beta access, custom integrations |

**Gates that bite:**
- **Webhooks and Zapier start at Grow ($79)** — any signup→ESP/CRM/warehouse automation forces Grow minimum. Free and Launch are UI + CSV export only.
- **Email verification and welcome emails start at Launch ($29)** — Free-tier signups can't be double-opt-in verified.
- **Position inflation** (display inflated queue positions for FOMO) is Launch+.
- Refund policy: 100% within 7 days **only if you received zero signups**.
- ⚠️ Pricing discrepancy: third-party comparisons and LaunchList's own blog have cited $19 (500), $39 (2,000), $149 (25K), and $299 (100K) volume steps, and a $19 custom-domain add-on for hosted pages. The live pricing page shows only the four tiers above. Treat intermediate steps as unverified.

## Integrations

**No-code platform guides (13 native)**: Webflow, WordPress, React, HTML/CSS/JS, Framer, Squarespace, Bubble, Wix, Typedream, Weebly, Instapage, Carrd — all are embed-widget or DIY-form installs, not data connectors.

**Data egress** (one-directional, LaunchList → elsewhere):
- **Webhooks** (Grow+): `new_user`, `email_verify` → your endpoint
- **Zapier** (Grow+): New Submission / Email Verified triggers → 3,000+ apps (Sheets, Airtable, Mailchimp, HubSpot, Kit)
- **Slack** (Launch+): human-readable signup alerts
- **CSV export** (all plans): manual bulk export from dashboard

**No native ESP/CRM connectors.** LaunchList has **no email broadcast system** — you cannot email your waitlist from LaunchList beyond welcome/verification messages. Wire signups into your ESP via Zapier or a webhook handler, and send launch announcements from there.

**No Make/Pabbly/Pipedream modules, no MCP server, no WordPress plugin** (WordPress is supported via embed only).

## Data model

One object matters: the **submission** (a person on a waitlist). Its full shape is the `new_user` webhook payload — see `launchlist-api-reference.md` for the verbatim JSON. Key fields:

```json
{
  "id": "02a146c3-7b36-490c-a97f-bba76ba1c900",
  "waitlist_key": "aa53Pf",
  "position": 49,
  "email": "richard@piedpiper.com",
  "referral_code": "9ZK8QR",
  "users_referred": 0,
  "is_email_verified": null,
  "is_spam": 0,
  "info": { "ip": "…", "location": { "...": "…" }, "analytics": { "utm_source": "…", "http_referrer": "…" } },
  "referred_by": { "id": "…", "referral_code": "ae4s4C", "positon": 3, "...": "…" }
}
```

- `referral_code` is the person's own share code; `referred_by` is the full submission object of their referrer (`null` for direct signups)
- `is_email_verified`: `null` = unverified, timestamp string = verified (not a boolean)
- `is_spam`: `1` = flagged by fraud heuristics
- `referred_by.positon` — verbatim typo in their docs; parse both spellings

## Quick-start recipes

### Recipe 1 — Custom signup form with referral tracking

Use when the embed widget doesn't match your design. The DIY form posts directly to LaunchList; `widget-diy.js` handles referral attribution from the visitor's URL.

```html
<head>
  <script src="https://getlaunchlist.com/js/widget-diy.js" defer></script>
</head>
<body>
  <form class="launchlist-form" action="https://getlaunchlist.com/s/YOUR_FORM_KEY" method="POST">
    <input name="email" type="email" required placeholder="you@example.com">
    <input name="name" type="text" placeholder="Name">
    <input name="role" type="text" placeholder="What's your role?"> <!-- custom field -->
    <input type="hidden" name="_gotcha"> <!-- honeypot: bots fill it, get rejected -->
    <button type="submit">Join the waitlist</button>
  </form>
</body>
```

Smoke-test the endpoint (server-side; note this loses browser referral context, so use it only for testing):

```bash
curl -X POST "https://getlaunchlist.com/s/YOUR_FORM_KEY" \
  -d "email=test@example.com" \
  -d "name=Test User"
```

**Gotchas**: the email input must be named exactly `email`; the form must keep class `launchlist-form`; leave `_gotcha` empty (and hidden) or the signup is rejected as a bot.

### Recipe 2 — Webhook handler: route signups into your ESP/CRM (Grow+)

LaunchList has no email broadcast system, so push every verified, non-spam signup into your ESP. Create the webhook under Plugins → "Create a webhook".

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
WAITLIST_KEY = "aa53Pf"  # reject payloads for other waitlists
seen_ids = set()         # use a durable store in production

@app.route("/hooks/launchlist", methods=["POST"])
def launchlist_hook():
    payload = request.get_json(force=True)

    # No HMAC signing documented — validate shape + waitlist_key instead
    if payload.get("waitlist_key") != WAITLIST_KEY:
        return jsonify(ok=False), 403

    # Idempotency: no documented retry policy, but dedupe anyway
    if payload.get("id") in seen_ids:
        return jsonify(ok=True)
    seen_ids.add(payload.get("id"))

    if payload.get("event") == "new_user":
        if payload.get("is_spam") == 1:
            return jsonify(ok=True)  # skip fraud-flagged signups
        referred_by = payload.get("referred_by") or {}
        add_to_esp(
            email=payload["email"],
            name=payload.get("name"),
            tags=["waitlist"],
            fields={
                "waitlist_position": payload.get("position"),
                "referral_code": payload.get("referral_code"),
                "referred_by_code": referred_by.get("referral_code"),
                # 'positon' is a verbatim typo in LaunchList's payload docs
                "referrer_position": referred_by.get("positon") or referred_by.get("position"),
                "utm_source": (payload.get("info", {}).get("analytics") or {}).get("utm_source"),
            },
        )
    elif payload.get("event") == "email_verify":
        mark_verified_in_esp(payload["email"])  # gate launch emails on this

    return jsonify(ok=True)
```

**Gotchas**: `referred_by` is absent for direct signups — guard with `or {}`. If you enabled email verification (Launch+), wait for `email_verify` before sending anything beyond a welcome — unverified addresses include typos and bots that beat the heuristics.

### Recipe 3 — Zapier: New Submission → Mailchimp/Sheets (Grow+, no code)

1. LaunchList: Plugins → Zapier → **Generate Access Token**
2. Zapier: Create Zap → app **LaunchList** → event **New Submission** → authenticate with the token → test (pulls a sample submission)
3. Add a Filter step: `is_spam` equals `0` (skip fraud-flagged signups)
4. Action: Mailchimp "Add/Update Subscriber" (map email, name, mark with a `waitlist` tag) — or Google Sheets "Create Spreadsheet Row" for a zero-ESP setup
5. Optional second Zap on **Email Verified** to flip a "verified" merge field, and only send launch campaigns to verified segments

**Gotchas**: triggers only — Zapier cannot add signups to LaunchList (use the form POST endpoint). The token is per-project; regenerating it breaks existing Zaps.

## Integration patterns

- **ESP sync**: webhook (or Zapier) → ESP with a `waitlist` tag. Gate broadcast sends on `email_verify` if verification is enabled. There is no back-sync — unsubscribes in your ESP don't remove people from the LaunchList queue.
- **Webhook trust model**: no signing → use an unguessable URL path, check `waitlist_key`, and dedupe on `id`. Treat webhooks as at-most-once: reconcile against a periodic CSV export if completeness matters (no read API to reconcile against).
- **Launch-day export**: final source of truth is the CSV export (all plans). Export, dedupe against your ESP, then import the remainder before sending the launch email.
- **Reward fulfillment**: there's no API to query referral counts — use the `new_user` webhook to maintain your own per-`referral_code` counter keyed on `referred_by.referral_code`, or read counts manually from the dashboard/leaderboard.

## Comparison grid

| Platform | Pricing model | API | Webhooks | Best for |
|---|---|---|---|---|
| **LaunchList** | One-time $0–$79+ | ❌ (planned) | ✅ Grow+ | Indie hackers wanting a no-subscription waitlist |
| KickoffLabs | $13–$202/mo annual | ✅ v1+v2 | ✅ structured fraud flags | Waitlists + giveaways needing API + fraud webhooks (`/sales-kickofflabs`) |
| UpViral | $79–$319/mo annual | ✅ Business+ | ✅ Callback URL | B2C sweepstakes/points campaigns with A/B testing (`/sales-upviral`) |
| ReferralHero | $199–$399/mo | ✅ 40+ endpoints | ✅ | Multi-level (L1/2/3) referral/affiliate stacks (`/sales-referralhero`) |
| Viral Loops | $35–$299/mo | ✅ | ✅ | Template-driven referral campaigns (backlog) |
| Prefinery | $39–$399/mo | ✅ | ✅ | Beta-launch management at scale (backlog) |
| GetWaitlist | $15–$250/mo | ✅ | — | Developer-quick widget waitlists (backlog) |
| Waitlister | Free–$129/mo | ✅ $39/mo+ | ✅ $39/mo+ | Multi-project founders; email broadcasts built in (backlog) |
| Referlist | Free–paid | — | — | Plug-n-play minimal waitlist (backlog) |
| Tuemilio | Free–paid | ✅ REST + JS | ✅ | API-first indie waitlists (backlog) |

**Use LaunchList when**: you hate subscriptions, your list is under ~10K, you want referrals + spam protection on a free tier, and webhook/Zapier egress (at Grow) covers your automation needs.

**Don't use LaunchList when**: you need a read/write API today (KickoffLabs, ReferralHero, Tuemilio), email broadcasts from the same tool (Waitlister, or any ESP), milestone giveaways beyond a waitlist (KickoffLabs, UpViral), or multi-level referral tracking (ReferralHero).
