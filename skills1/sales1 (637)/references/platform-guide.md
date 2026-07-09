# UpViral Platform Guide

> Best-effort reference assembled from upviral.com, support.upviral.com, the public API listing at upviral.com/api, and third-party review/comparison sources (June 2026). Treat all pricing and plan-gating as best-effort — verify in-app before committing.

UpViral (by **Emarky**, live since 2015) is a **viral referral marketing and list-building platform**. You run incentivized-sharing campaigns — sweepstakes, giveaways, waiting lists, and milestone referral programs — where participants earn points for inviting friends, and points unlock rewards or leaderboard rank. Stated scale: 32,600+ businesses, 72.7M+ leads generated.

For day-to-day routing and quick answers, start in `SKILL.md`. This file is the deep reference.

## Table of contents

- [Pricing and plan gating](#pricing-and-plan-gating)
- [Campaign types — which to pick](#campaign-types--which-to-pick)
- [Presentation formats](#presentation-formats)
- [Campaign tools](#campaign-tools)
- [Fraud detection model](#fraud-detection-model)
- [Integrations](#integrations)
- [Capabilities matrix (API / webhook / UI-only)](#capabilities-matrix)
- [Data model](#data-model)
- [Quick-start recipes](#quick-start-recipes)
- [Comparison grid](#comparison-grid)
- [When to use / when not](#when-to-use--when-not)

## Pricing and plan gating

Annual billing (monthly is ~33–60% higher; "normally" struck-through anchors are marketing). 14-day trial for $1, 30-day money-back guarantee.

| Plan | Annual | Monthly | Lead limit | Brands | AI Credits | API + Webhooks | Notable |
|------|--------|---------|-----------|--------|-----------|----------------|---------|
| **Starter** | $79/mo | $99/mo | 10,000 | 1 | 1/mo | ❌ **No** | Unlimited campaigns, builder, sweepstakes, leaderboards, 30+ integrations |
| **Business** | $119/mo | $149/mo | 25,000 | 2 | 3/mo | ✅ **Yes** | "BEST DEAL" — adds API/Webhooks, universal capture, location restrictions, advanced Zapier |
| **Premium** | $319/mo | $399/mo | 100,000 | 5 | 10/mo | ✅ Yes | Dedicated account manager, priority support |

**Critical gate: API access and webhooks (Callback URL) start at Business.** Starter is UI + native integrations + basic Zapier only. Any server-side automation, CRM-sync-via-API, data-warehouse pipeline, or webhook handler forces Business minimum. This is the #1 pricing surprise in research.

Other gated items:
- **Universal capture, location restrictions, advanced Zapier**: Business+.
- **Dedicated account manager, priority support**: Premium only.
- **All plans**: unlimited campaigns, drag-and-drop builder, viral sweepstakes, smart leaderboards, 30+ direct integrations, A/B testing, fraud detection, chat/email support.

## Campaign types — which to pick

| Campaign type | What it is | Pick it when | Plan minimum |
|---|---|---|---|
| **Viral Sweepstakes** | Point-based competition; top point-earners (or a draw) win a grand prize | You have a prize budget and want maximum sharing velocity | Any |
| **Viral Rewards** (giveaway) | Everyone who hits a points threshold unlocks a reward (digital download, discount, bonus) | Lead gen where every referrer should get something, not just winners | Any |
| **Viral Waiting List** | Pre-launch list; referring jumps you up the queue / unlocks early access (Dropbox-style) | Product/launch waitlist where queue position is the incentive | Any |
| **Milestone Campaign** | Evergreen referral program; rewards unlock at referral milestones (refer 3 → reward A, 10 → reward B) | Always-on referral program, not a one-off contest | Any |
| **Custom Campaign** | Mix-and-match builder combining the above mechanics | None of the presets fit; you want bespoke point/reward logic | Any |

The campaign type is not what gates you — the **lead cap, brand count, and API access** are. A single Starter account can run any campaign type, just capped at 10K leads / 1 brand / no API.

## Presentation formats

How the campaign appears to visitors (all available on all plans):

- **Full-page landing page** — UpViral-hosted page (custom domain on paid plans).
- **Embedded form** — drop the form into your own page/site.
- **Pop-up window** — modal overlay triggered on your site.
- **Pop-over widget** — slide-in/corner widget.

Because the in-app drag-and-drop builder is the most-complained-about surface (broken widgets, limited customization), the **embedded form** on an externally built page is often the most reliable choice for polished designs.

## Campaign tools

- **Smart leaderboards** — live ranking of top referrers; drives competition in sweepstakes.
- **Unlockable incentives** — gate rewards behind points/referral milestones.
- **Social sharing buttons** — Facebook, X/Twitter, LinkedIn, WhatsApp, Pinterest, Instagram.
- **A/B testing** — split-test landing pages, thank-you pages, and email copy (a differentiator vs simpler tools like RafflePress).
- **Automated winner selection** — random/point-based draw for sweepstakes.
- **Retargeting & tracking** — pixels and tracking for paid retargeting.
- **Custom domains** — host campaigns on your domain (paid plans).
- **Scheduled campaigns** — set start/end times.
- **AI Credits** — metered AI copy/asset generation (1/3/10 per month by tier).

## Fraud detection model

UpViral's anti-fraud is **IP-based and semi-manual**:

- **Signal**: when a referred signup comes from the **same IP address** as the referrer's unique invite link, the system marks it **"suspicious."** This is the primary documented signal.
- **What the platform claims more broadly**: detection of fake entries, duplicate emails, and bot traffic (per marketing/review copy) — but the documented mechanic is IP-matching.
- **Disposition is manual**: flagged leads appear in the **Fraud Detection** section where you choose to **Activate** (legitimate — count them), **Delete**, or **Blacklist**.
- **Fraud Prevention** settings can auto-deactivate leads UpViral considers fraudulent, but review is expected for borderline cases.

**Watch for false positives**: legitimate signups behind shared office NAT, household routers, or mobile carrier CGNAT share IPs and get flagged. Review before bulk-deleting. For prevention, combine email verification with points/IP caps.

## Integrations

**Native ESP / CRM (30+):** Mailchimp, ActiveCampaign, ConvertKit, AWeber, HubSpot, Klaviyo, Intercom (and more).

**Site builders / forms:** WordPress (no native plugin — embed manually), ClickFunnels, Wufoo, Jotform, Webflow.

**Automation / iPaaS:** Zapier (triggers: **New Lead**, **New Reward Unlocked**), Make/Integromat, Pipedream, Integrately, Pabbly Connect, plus HTML forms and the REST API.

**No MCP server.** Programmatic surface is REST API + Callback URL webhook + iPaaS.

**Integration caveats (from reviews):** ClickFunnels, Shopify, and funnel-builder integrations are reported flaky; there's no native WordPress plugin. Prefer Zapier or the REST API over deep native funnel integrations when reliability matters.

## Capabilities matrix

| Capability | Surface |
|---|---|
| Add a lead/contact | API (`add_contact`), UI, native integration |
| Read a lead | API (`get_lead_details`, `get_lead_details_by_email`) |
| List all leads (paginated) | API (`get_leads` with `start`/`size`) |
| Filter leads by points | API (`get_leads_points` with operator + value) |
| Award points to a lead | API (`add_points`) |
| Read campaign custom fields | API (`get_custom_fields`) |
| List campaigns | API (`lists`) |
| Reward-unlock notification | Webhook (Callback URL), Zapier (New Reward Unlocked) |
| New-lead notification | Webhook (Callback URL), Zapier (New Lead) |
| Build campaign / design pages | UI-only (drag-and-drop builder) |
| Fraud review (activate/delete/blacklist) | UI-only |
| Winner selection | UI-only (automated draw) |
| A/B test setup | UI-only |

**API + webhooks require Business tier or above.**

## Data model

Shapes are best-effort (the public API page is JS-rendered; per-field bodies aren't fully published). Treat as indicative.

**Campaign** (from `lists`):
```json
{
  "campaign_id": "123456",
  "name": "Summer Launch Giveaway",
  "status": "active"
}
```

**Lead / contact** (from `get_lead_details`):
```json
{
  "lead_id": "987654",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "points": 120,
  "referral_code": "abc123",
  "referred_by": "xyz789",
  "ip": "203.0.113.4",
  "status": "active",
  "fraud_status": "ok",
  "custom_fields": { "company": "Acme" }
}
```

**Custom fields** (from `get_custom_fields`):
```json
{
  "campaign_id": "123456",
  "custom_fields": [
    { "key": "company", "label": "Company", "type": "text" }
  ]
}
```

**Callback URL (webhook) payload** — lean; fires on events such as reward-unlock. Enrich by calling `get_lead_details` with the returned `lead_id`:
```json
{
  "event": "reward_unlocked",
  "campaign_id": "123456",
  "lead_id": "987654",
  "email": "jane@example.com",
  "points": 120
}
```

## Quick-start recipes

> Requires **Business tier or above** (API access). Base URL `https://app.upviral.com/api/v1/`. Auth = form-encoded `uvapikey` + `uvmethod`. Responses are JSON.

### Recipe 1 — Add a contact with referral attribution (cURL)

```bash
curl -X POST https://app.upviral.com/api/v1/ \
  --data-urlencode "uvapikey=YOUR_API_KEY" \
  --data-urlencode "uvmethod=add_contact" \
  --data-urlencode "campaign_id=123456" \
  --data-urlencode "email=jane@example.com" \
  --data-urlencode "name=Jane Doe" \
  --data-urlencode "ip=203.0.113.4" \
  --data-urlencode "referral_code=xyz789"
```

`referral_code` is the inviting lead's code (captured from the `?ref=` param on your signup page) — pass it so UpViral attributes the referral and awards points. Omit it for a direct (non-referred) signup.

### Recipe 2 — Pull reward-eligible leads by points threshold (Python)

```python
import requests

BASE = "https://app.upviral.com/api/v1/"
API_KEY = "YOUR_API_KEY"
CAMPAIGN_ID = "123456"

def reward_eligible(threshold=100, page_size=100):
    eligible, start = [], 0
    while True:
        r = requests.post(BASE, data={
            "uvapikey": API_KEY,
            "uvmethod": "get_leads_points",
            "campaign_id": CAMPAIGN_ID,
            "operator": ">",        # one of <, >, =
            "points": threshold - 1,
            "start": start,
            "size": page_size,
        })
        r.raise_for_status()
        batch = r.json().get("leads", [])
        if not batch:
            break
        eligible.extend(batch)
        start += page_size
    return eligible

for lead in reward_eligible(100):
    print(lead["email"], lead.get("points"))
```

Use `get_leads_points` rather than pulling every lead and filtering in code — it pages only the matching set.

### Recipe 3 — Handle the Callback URL webhook and enrich (Python/Flask)

```python
from flask import Flask, request
import requests

app = Flask(__name__)
BASE = "https://app.upviral.com/api/v1/"
API_KEY = "YOUR_API_KEY"

@app.post("/upviral/callback")
def upviral_callback():
    evt = request.get_json(force=True, silent=True) or request.form.to_dict()
    lead_id = evt.get("lead_id")
    campaign_id = evt.get("campaign_id")

    # Callback payload is lean — enrich with full lead details
    detail = requests.post(BASE, data={
        "uvapikey": API_KEY,
        "uvmethod": "get_lead_details",
        "campaign_id": campaign_id,
        "lead_id": lead_id,
    }).json()

    # e.g. on reward_unlocked, push to your CRM / fulfillment queue
    if evt.get("event") == "reward_unlocked":
        fulfill_reward(detail)   # your code
    return "", 200

def fulfill_reward(lead):
    ...
```

Set the Callback URL per campaign in UpViral's settings. There's no documented HMAC signature scheme — restrict by source IP, use a hard-to-guess path/secret query param, and treat the callback as advisory (re-fetch authoritative state via `get_lead_details`).

## Comparison grid

| Platform | Niche | API/Webhooks | Pricing floor (annual) | Notes |
|---|---|---|---|---|
| **UpViral** | Viral sweepstakes/giveaways/waitlists/milestones | ✅ Business+ ($119/mo) | $79/mo (no API) | A/B testing, IP fraud detection; B2C-focused; builder fragile |
| **KickoffLabs** | Waitlists + giveaways + milestone rewards | ✅ (v1+v2 REST, webhooks) | ~$13/mo | Cheaper floor, structured webhook fraud flags, AnyForm/KOL.js — use `/sales-kickofflabs` |
| **Viral Loops** | Template-driven referral campaigns | ✅ | ~$49/mo | Pre-built Dropbox/Airbnb-style templates; subscription-only |
| **Vyper** | Giveaways + contests + rewards | ✅ | AppSumo/LTD history | Strong referral mechanics; needs an existing audience to seed |
| **Prefinery** | API-first pre-launch waitlists | ✅ (API-first) | — | Best for technical teams running staged betas |
| **Gleam** | Contests with 100+ entry actions | ✅ | — | Most flexible entry actions; multi-channel |
| **KingSumo** | Budget giveaways | Limited | low/LTD | AppSumo-made; creators/bloggers; minimal API |
| **ShortStack** | Contests + landing/form builder | ✅ | — | Drag-and-drop pages + contests |
| **ReferralHero** | Full-stack referral/affiliate multi-level | ✅ | ~$199/mo | Level 1/2/3 tracking, coupon groups — use `/sales-referralhero` |
| **ReferralKit** | No-code newsletter merge-tag referrals | ❌ (no API) | free→ | Newsletter-only — use `/sales-referralkit` |

## When to use / when not

**Use UpViral when:**
- You're running a **B2C viral campaign** (sweepstakes, giveaway, waitlist, milestone) and want point-for-share mechanics with leaderboards.
- You need **A/B testing** of landing/thank-you/email variants out of the box.
- You're on **Business+** and want REST API + Callback URL webhooks to wire campaigns into a CRM or warehouse.

**Don't use UpViral when:**
- Your audience is **B2B** — point-for-share doesn't motivate business buyers (consider a different demand-gen motion).
- You need **API/webhooks but only have a Starter budget** — those are gated to Business ($119/mo).
- You want a **cheap one-off campaign** — the $79/mo floor and $1/14-day trial make occasional use expensive; KickoffLabs (~$13/mo) or KingSumo (LTD) fit better.
- You need **multi-level Level 1/2/3 referral/affiliate tracking** — use ReferralHero (`/sales-referralhero`).
- You need **newsletter-only merge-tag referrals with no API** — use ReferralKit (`/sales-referralkit`).
