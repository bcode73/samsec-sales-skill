# ReferralHero Platform Reference

<!-- Source: https://referralhero.com (homepage), https://referralhero.com/pricing, https://support.referralhero.com/integrate/rest-api, https://support.referralhero.com/integrate/rest-api/endpoints-reference, Capterra (38 reviews, 4.5/5), SaaSHub comparison vs Viral Loops. Research date 2026-06-01. Pricing and ESP integration list may shift; verify before quoting. -->

## Overview

ReferralHero is a full-stack referral marketing platform supporting referral programs, affiliate programs, waitlists, contests, NPS surveys, and gamified engagement campaigns. It targets junior marketers through growth experts and serves verticals from FinTech and SaaS to dentists, home services, med spas, and mobile app developers. Differentiator vs SparkLoop, ReferralKit, and Viral Loops: a documented REST API with 40+ endpoints, native webhooks, 500+ integrations via Zapier, six native ESP connectors (Mailchimp, Kit, AWeber, Klaviyo, ActiveCampaign, SendLane), multi-level referral tracking (Level 1/2/3), and built-in coupon group management.

## Capabilities & automation surface

- **Referral programs** (UI + API + webhooks, PRO+): Subscribers refer friends via unique links; tracked via `POST /lists/:uuid/subscribers/track_referral_conversion_event`.
- **Affiliate programs** (UI + API): Multi-tier commission structures supported via the same subscriber/referral primitives.
- **Waitlists & contests** (UI + API): Position-based mechanics, broadcasts on the PREMIUM Waitlist/Contest tier.
- **NPS surveys** (UI-only): Survey module bundled into the campaign builder.
- **Multi-level tracking** (API): Separate endpoints for Level 1, Level 2, and Level 3 referrals (qualified-only and "all" variants).
- **Coupon codes** (UI + API, PRO+): Coupons grouped under coupon groups; bulk-importable.
- **Anti-fraud + ReCaptcha + SMS Verification** (UI, ReCaptcha+SMS PREMIUM-only).
- **Automation emails + custom sender domain** (UI, PRO+).
- **Native ESP connectors** (UI): Mailchimp, ConvertKit/Kit, AWeber, Klaviyo, ActiveCampaign, SendLane.
- **Zapier + 500+ apps** (UI + Zapier): Triggers and actions; full subscriber/referral lifecycle covered.
- **Webhooks** (PRO+): Confirmation events, reward unlocks.
- **REST API** (PRO+): 40+ endpoints under `https://app.referralhero.com/api/v2`. See `referralhero-api-reference.md` for the verbatim reference.
- **No MCP server** (as of 2026-06-01).
- **No native CRM connector** — go via Zapier or build with the API.

## Pricing, limits & plan gates

<!-- Pricing pulled from https://referralhero.com/pricing on 2026-06-01. Older sources may quote different numbers. -->

| Plan | Price | Members | API + webhooks | ReCaptcha + SMS Verify | Branding-free | Notes |
|---|---|---|---|---|---|---|
| **Free Forever** | $0 | 25 | ❌ | ❌ | ✅ (excludes RH branding from end-user view) | All PRO features included for the 25-member ceiling — proof-of-concept only |
| **PRO** | $199/mo | 10,000 | ✅ | ❌ | ✅ | Branding, analytics, integrations, FB Pixel, anti-fraud, coupon codes, unlimited campaigns, referral links, automation emails, custom sender domain |
| **PREMIUM** | $399/mo | 50,000 | ✅ | ✅ | ✅ | All PRO features plus ReCaptcha and SMS Verification |
| **PREMIUM (Waitlist/Contest)** | $199/mo | 50,000 subscribers | ✅ | (n/a — waitlist-focused) | ✅ | All above features plus broadcasts and priority support; 10-day risk-free trial; annual prepay saves $597 (3 months free) |
| **Enterprise** | Custom | Custom | ✅ | ✅ | ✅ | Customized packages on request |

- **SMS/MMS usage** is billed pay-as-you-go weekly, on top of subscription.
- **Cash and gift card payouts** incur processing fees.
- **No subscriber-overage scaled pricing** — "no scaled pricing, grow as much as you want for the same flat rate" (within plan cap).

## Authentication & API basics

- **Base URL**: `https://app.referralhero.com/api/v2`
- **Auth**: `Authorization: Bearer YOUR_API_TOKEN` (preferred). Fallback: `X-API-Key: YOUR_API_TOKEN`.
- **HTTPS required**. Unauthenticated → `no_token` error.
- **Response format**: JSON; any non-200 indicates error.
- **Rate limit**: 5,000 req/hour soft per token; overage returns HTTP 429 + `too_many_calls`. Contact support to raise.
- **Token location**: ReferralHero dashboard > Account > API.
- **Breaking changes**: ReferralHero commits to 2 weeks' advance notice.

## Data model

API surface implies the following data model:

```json
{
  "list": {
    "uuid": "abc-123-def-456",
    "name": "Holiday giveaway",
    "website": "https://example.com"
  },
  "subscriber": {
    "id": "sub_789",
    "uuid": "abc-123-def-456",
    "email": "user@example.com",
    "phone_number": "+15551234567",
    "name": "Jane Doe",
    "referral_code": "JANE7X",
    "referral_url": "https://example.com/r/JANE7X",
    "status": "confirmed",
    "points": 12,
    "referrer": "BOB5Y",
    "stripe_customer_id": "cus_xyz",
    "transaction_id": "txn_001",
    "conversion_value": 49.99,
    "tags": ["vip", "early-bird"],
    "extra_field": "newsletter_2026",
    "extra_field_2": "",
    "level_1_count": 5,
    "level_2_count": 12,
    "level_3_count": 3
  },
  "transaction": {
    "amount": 49.99,
    "transaction_id": "txn_001",
    "product_id": "prod_x",
    "lifetime_spend": 199.96,
    "reward_value": 5.00
  },
  "coupon_group": {
    "id": "cg_456",
    "name": "Welcome 10% off",
    "active": true,
    "coupons": ["WELCOME10-A", "WELCOME10-B"]
  },
  "reward": {
    "reward_id": "rwd_111",
    "milestone": 10,
    "status": "sent",
    "subscriber_id": "sub_789"
  }
}
```

## Quick-start recipes

### Recipe 1: Add a subscriber via API with attribution

```bash
curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newsignup@example.com",
    "name": "Alex",
    "referrer": "JANE7X",
    "source": "landing_page",
    "double_optin": true,
    "tags": ["holiday_2026"]
  }'
```

If `double_optin: true` and the campaign requires confirmation, the new subscriber is created in `unconfirmed` state until they click the confirmation email; the referrer's count increments only on confirmation. If your stack already verifies the email server-side, set `double_optin: false`.

### Recipe 2: Bulk-import 5,000 transactions in batches of 500

```python
import os, requests, time

API = "https://app.referralhero.com/api/v2"
LIST = os.environ["LIST_UUID"]
HEADERS = {"Authorization": f"Bearer {os.environ['REFERRALHERO_API_TOKEN']}",
           "Content-Type": "application/json"}

def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

transactions = load_transactions()  # list of {email, amount, transaction_id, ...}

for batch in chunked(transactions, 500):
    r = requests.post(
        f"{API}/lists/{LIST}/subscribers/add_bulk_transactions",
        headers=HEADERS,
        json={"transactions": batch},
    )
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", "60"))
        time.sleep(wait)
        continue
    r.raise_for_status()
```

Stays under the 5,000 req/hour soft limit by using one bulk call per 500 transactions. For sustained high-volume use, request a rate-limit increase via support.

### Recipe 3: Reward fulfillment — promote + unlock_promoted_reward

```bash
# Step 1: promote the subscriber to the next reward tier
curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers/$SUB_ID/promote" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN"

# Step 2: unlock the specific reward (you need the reward_id from /rewards or /bonuses)
curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers/$SUB_ID/unlock_promoted_reward" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reward_id": "rwd_111"}'
```

Skipping the `promote` step causes `unlock_promoted_reward` to silently fail. For automatic milestone rewards configured in the UI, this two-step flow runs server-side — only call it manually if you're driving rewards from external logic.

## Integration patterns

- **ESP-native (no code)**: Connect Mailchimp / Kit / AWeber / Klaviyo / ActiveCampaign / SendLane via dashboard > Integrations. Subscribers added to your ESP audience are mirrored into ReferralHero. WARNING: if you also POST to the API, you'll get duplicates — pick one ingestion path per campaign.
- **Zapier**: 500+ apps; common use is to push referral-confirmed events into HubSpot, Salesforce, Pipedrive, Notion, Slack.
- **Webhooks (PRO+)**: Configure in dashboard. Common events: subscriber confirmed, referral attributed, milestone reached, reward unlocked.
- **Server-to-server API**: For custom flows — typically signup form → your backend → POST `/subscribers` with `referrer` attribution, then poll `/subscribers/:id` or react to webhooks.
- **Make.com**: Documented at `make.com/en/help/app/referralhero` and `apps.make.com/referralhero`; covers add-subscriber, retrieve-subscriber, and trigger-on-new-referral scenarios.
- **Pipedream**: Listed at `pipedream.com/apps/referralhero` with common workflows like "Add Subscriber on New Contact from Missive."

## Multi-level referral mechanics

ReferralHero supports Level 1, Level 2, and Level 3 referrals (referrer-of-referrer-of-referrer). Endpoints come in pairs:

| Endpoint | Includes |
|---|---|
| `/subscribers/:id/level_1_referrals` | Confirmed Level 1 only |
| `/subscribers/:id/level_2_all_referrals` | All Level 2 (qualified + unqualified) |
| `/subscribers/:id/level_2_referrals` | Confirmed Level 2 only |
| `/subscribers/:id/level_3_all_referrals` | All Level 3 |
| `/subscribers/:id/level_3_referrals` | Confirmed Level 3 only |

Most "count is wrong" complaints come from calling the `_all_` endpoint when expecting confirmed counts. Use `qualify` / `unqualify` to manually adjust suspicious referrals before crediting commissions.

## Anti-fraud controls

- **Anti-fraud (PRO+)**: Built-in heuristics flag suspicious referrals.
- **ReCaptcha (PREMIUM-only)**: Adds Google ReCaptcha to signup forms; blocks bot signups.
- **SMS Verification (PREMIUM-only)**: Requires referees to verify a phone number before counting as a confirmed referral. The strongest fraud control on the platform.
- **Manual qualify/unqualify** (API + UI): Review top referrers before paying out cash/gift card rewards.
- **`double_optin`** (campaign setting): Don't count referrals until referee confirms email.

If your program offers cash, gift cards, or high-value rewards, budget PREMIUM ($399/mo) from day one — PRO's anti-fraud alone has been called out as insufficient for high-value programs in Capterra reviews.

## Comparison with alternatives

| Tool | Primary use | Free tier | API + webhooks | ESP support | Best for |
|---|---|---|---|---|---|
| **ReferralHero** | Full-stack referral/affiliate/waitlist/contest | 25 subs | ✅ (PRO+) | 6 native + Zapier 500+ | Teams wanting documented API + webhooks + multi-level + coupons across many verticals |
| **SparkLoop** | Newsletter referrals + paid recommendations + partner network | Free Recs tier | ❌ public API; Zapier via ESP | 25+ ESPs | Newsletters at scale wanting referral + paid-rec monetization in one stack |
| **ReferralKit** | Newsletter referrals (merge-tag, no-code) | First 10K leads free | ❌ | 4 native (Mailchimp, Kit, MailerLite, AWeber) | No-code newsletter operators under 10K leads who want Morning Brew-style milestones |
| **Viral Loops** | Templated viral campaigns (waitlist, milestone, prelaunch) | 14-day trial | ✅ API, webhooks, Zapier | Generic via API | Marketers running templated multi-format viral campaigns |
| **GrowSurf** | Scalable referral with strong analytics + fraud | 14-day trial | ✅ API, webhooks, Zapier | Generic via API | SaaS / e-commerce teams needing analytics + fraud detection |
| **KickoffLabs** | Viral giveaways, waitlists, milestone rewards | 7-day trial | ✅ API, webhooks, Zapier | Generic via API | Pre-launch and giveaway-driven growth campaigns |
| **ReferralCandy** | E-commerce referral marketing (Shopify-heavy) | None (Premium $49/mo + Enterprise $3,999/mo) | ✅ | Shopify-first | Shopify stores wanting plug-and-play referrals |
| **Prefinery** | Pre-launch waitlists + referrals | 14-day trial | ✅ | Generic via API | Pre-launch waitlist programs specifically |
| **Voucherify** | Coupon + referral marketing API | Build tier | ✅ API-first | Generic via API | Engineering teams building custom promo + referral logic |

## When to use ReferralHero

- Need a documented REST API + webhooks + Zapier without going to enterprise pricing
- Running a multi-vertical program (FinTech, SaaS, home services, dentists, med spas) — not just newsletters
- Need multi-level referral tracking (Level 2/3 downline counts)
- Need coupon code groups bundled into the referral program
- Already on Mailchimp / Kit / AWeber / Klaviyo / ActiveCampaign / SendLane (native ESP integration)
- Sub-50K subscribers and OK with $199–$399/mo

## When NOT to use ReferralHero

- Need a free tier for a real campaign — Free is capped at 25 subscribers. Use ReferralKit (10K leads free) instead.
- Newsletter-only with merge-tag insertion as the primary mechanic — ReferralKit is purpose-built for that.
- Need paid recommendations or a partner network — use SparkLoop.
- Need an API-first developer experience — Voucherify is more developer-centric; GrowSurf has stronger analytics.
- Shopify-only e-commerce referral — ReferralCandy is Shopify-first.
- Need MCP server — none exists for ReferralHero (as of 2026-06-01).
