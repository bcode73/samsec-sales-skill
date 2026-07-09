# KickoffLabs Platform Reference

<!-- Source: https://kickofflabs.com (homepage), https://app.kickofflabs.com/pricing (pricing redirect target), https://dev.kickofflabs.com/api/ (v2 docs index), https://api.kickofflabs.com/ (v1 docs), https://support.kickofflabs.com (support docs), Capterra/G2 review snippets, viral-loops.com / queueform.com / getlaunchlist.com / contentmation.com comparison articles. Research date 2026-06-01. Pricing pulled 2026-06-01; verify before quoting. -->

## Overview

KickoffLabs is a viral marketing platform for pre-launch waitlists, bonus-entry giveaways, milestone-reward referral programs, and leaderboard giveaways. Differentiator vs Viral Loops / UpViral / Prefinery: bonus-action scoring (60+ built-in actions), in-house fraud detection with structured webhook flags (`duplicate_ip` / `bounced` / `duplidate_email`), AnyForm script for posting existing site forms into KickoffLabs without rebuilding signup pages, both v1 + v2 REST API with server-side webhooks, and KOL.js for client-side embeds. Target audience: startups, small businesses, product launches, agencies, event/crowdfunding promoters.

## Capabilities & automation surface

- **Campaign types** (UI): bonus-entry giveaways, pre-launch waitlists, milestone reward programs, email opt-in bribes, newsletter referrals, leaderboard giveaways
- **Deployment** (UI + KOL.js): embedded widgets, popup boxes, existing-form connections (AnyForm), separate landing pages
- **Viral mechanics** (UI + API): automatic unique link generation (`?kid=` query param), personalized greeting bars, referral tracking, influencer identification
- **Custom scoring + actions** (UI, 60+ built-in): visit page, follow Twitter, like Facebook, etc. — each awards points toward milestones
- **Fraud detection** (UI + webhooks): duplicate IP, bounced email, duplicate email (typo: `duplidate_email`)
- **A/B testing** (Premium+)
- **Email autoresponders** (all tiers); **reward-level emails** (Premium+); **custom email templates + custom domains** (Business+)
- **SMS Contests + SMS verification** (Premium+ as $50/mo add-on; Enterprise includes)
- **Pick-a-winner** (UI)
- **Native ESP integrations** (UI): Klaviyo, Mailchimp, ActiveCampaign, Brevo
- **Website builder integrations** (UI): Webflow, Wix, Squarespace, Weebly
- **E-commerce**: Shopify
- **Other**: Facebook Audiences, Slack, Zapier
- **REST API**: v1 (`/subscribe`, `/info`) + v2 (`/v2/{CAMPAIGN_ID}/leads`, `/tags`, `/leaderboard`, `/approve`, `/block`, `/waitlist`, `/verify`, `/sms-verification`, bulk endpoints)
- **Webhooks** (in/out, all tiers): structured payload with `__event`, `__fraudulent`, `__referral`, `__reward_level`, `__score_change`, `__tagged` blocks
- **KOL.js**: client-side JavaScript library for embeds + AnyForm
- **AnyForm script** (recommended over direct API for browser-side flows)
- **iPaaS**: Zapier (deep), Integrately, Pipedream
- **No MCP server** (as of 2026-06-01)
- **No native CRM** — go via Zapier or your ESP's CRM connector

## Pricing, limits & plan gates

<!-- Pricing from https://app.kickofflabs.com/pricing on 2026-06-01. Annual billing shown; monthly pay-as-you-go is ~43% higher. Lead limits are per-month. -->

| Plan | Annual $/mo (30% off) | Monthly $/mo | Leads/mo | Auto-upgrade rate | API access | A/B testing | Reward emails | Custom templates/domains | Team | Brands |
|---|---|---|---|---|---|---|---|---|---|---|
| **Hobby** | $13 | ~$19 | 500 | $8/1,000 | ✅ (10/min) | ❌ | ❌ | ❌ | 0 | 1 |
| **Premium** | $48 | ~$69 | 2,500 | $8/1,000 | ✅ (~20-50/min) | ✅ | ✅ | ❌ | 0 | 1 |
| **Business** | $99 | ~$141 | 10,000 | $8/1,000 | ✅ (~50-100/min) | ✅ | ✅ | ✅ | 3 | 3 |
| **Enterprise** | $202 | ~$289 | 25,000 | $8/1,000 | ✅ (~100/min) | ✅ | ✅ | ✅ | 5 | 5 |

- **SMS Contests/Verification**: Premium $50/mo add-on; Business optional; Enterprise included
- **Branding removal** begins at Premium
- **Unlimited landing pages** on all tiers
- **Unlimited total leads** (lifetime) — only the per-month count is metered
- **Webhooks (in + out)** on all tiers
- **Custom domains** count: Hobby 1 / Premium 1 / Business 3 / Enterprise 5
- **30% savings on annual** vs monthly

## Authentication & API basics

- **v1 base URL**: `https://api.kickofflabs.com/v1/{CAMPAIGN_ID}` — form-encoded `/subscribe` and `/info`
- **v2 base URL**: `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}` — JSON-first
- **Auth**: `api_key` parameter + `CAMPAIGN_ID` in path. Find both at Setup > Advanced Settings > API Access.
- **HTTPS required**
- **Response format**: JSON (always, even on form-encoded v1 requests)
- **Rate limit**: scales with plan (~10/min on Hobby → ~100/min on Enterprise). Headers + back-off response shape undocumented; verify with test traffic.
- **Critical security rule**: "Your API Key should never be used in client side JavaScript."

## Data model

```json
{
  "campaign": {
    "id": 123456,
    "name": "Holiday Giveaway",
    "campaign_type": "milestone_reward"
  },
  "lead": {
    "id": 56999,
    "email": "user@example.com",
    "given_name": "Jane",
    "family_name": "Doe",
    "avatar": "https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/...",
    "social_id": "1QN7",
    "social_url": "http://example.com?kid=1QN7",
    "redirect_url": "http://example.com/thanks?kolid=1QN7",
    "url": "http://example.com",
    "parent_id": null,
    "counter": 252,
    "contest_score": 300,
    "contest_score_rank": 19588,
    "lead_count": 1803,
    "rank": 1,
    "referrals": 5,
    "subscription_number": 1,
    "custom_fields": {"company": "Acme", "role": "Founder"}
  },
  "lead_tag": {
    "tag_id": "12324",
    "name": "Tag Name",
    "points": 20
  },
  "reward_level": {
    "reward_level_id": 1,
    "required_points": 5,
    "subject": "You did it!"
  },
  "webhook_envelope": {
    "__event": "the_webhook_event",
    "__fraudulent": ["duplicate_ip", "bounced", "duplidate_email"],
    "__referral": {"email": "...", "social_id": "ABC", "phone_number": "+1..."},
    "__reward_level": {"required_points": 5, "reward_level_id": 1, "subject": "..."},
    "__score_change": {"current_contest_score": 5, "previous_contest_score": 1},
    "__tagged": {"name": "Tag Name", "points": 20, "tag_id": "12324"}
  }
}
```

## Quick-start recipes

### Recipe 1: Add a lead via v1 with referrer attribution

```bash
curl -X POST "https://api.kickofflabs.com/v1/$CAMPAIGN_ID/subscribe" \
  --data-urlencode "email=newsignup@example.com" \
  --data-urlencode "api_key=$KICKOFFLABS_API_KEY" \
  --data-urlencode "social_id=1QN7" \
  --data-urlencode "ip=203.0.113.42" \
  --data-urlencode "__url=https://example.com/signup" \
  --data-urlencode "__ref=https://twitter.com/share?kid=1QN7"
```

The `social_id` here is the **referrer's** social_id (from the `?kid=` query param on the share URL). KickoffLabs uses this to credit the referrer. Run from your backend — never from client-side JS.

### Recipe 2: Webhook handler with fraud routing (Python)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

FRAUD_AUTO_BLOCK = {"bounced"}
FRAUD_REVIEW = {"duplicate_ip", "duplidate_email", "duplicate_email"}  # support both typo and corrected forms

@app.post("/kickofflabs-webhook")
def webhook():
    payload = request.get_json()
    fraud_flags = set(payload.get("__fraudulent", []))

    if fraud_flags & FRAUD_AUTO_BLOCK:
        block_lead(payload["email"])
        return jsonify({"action": "blocked"}), 200

    if fraud_flags & FRAUD_REVIEW:
        queue_for_human_review(payload)
        return jsonify({"action": "queued_for_review"}), 200

    if "__reward_level" in payload:
        fulfill_reward(payload["email"], payload["__reward_level"])

    return jsonify({"action": "ok"}), 200
```

Match `duplidate_email` *and* `duplicate_email` — KickoffLabs's published docs use the typo, and you don't want to silently miss flagged leads if they ever fix it.

### Recipe 3: Bulk-approve 200 leads after manual review (v2)

```bash
curl -X POST "https://api.kickofflabs.com/v2/$CAMPAIGN_ID/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$KICKOFFLABS_API_KEY'",
    "email": ["a@example.com", "b@example.com", "c@example.com"]
  }'
```

The `approve` endpoint accepts up to 200 emails per call — chunk larger batches. Use after triaging fraud-flagged leads from your webhook review queue.

## Integration patterns

- **AnyForm + KOL.js (recommended for custom pages)**: Drop `kol.js` on your site; AnyForm script intercepts existing form submits and posts to KickoffLabs with cookie-based attribution. No API key in browser.
- **Server-to-server v1/v2 API**: Your backend signup handler calls `POST /v1/{CAMPAIGN_ID}/subscribe` (form) or `POST /v2/{CAMPAIGN_ID}/leads` (JSON). Pass `social_id` for referrer attribution.
- **Native ESP** (Klaviyo / Mailchimp / ActiveCampaign / Brevo): Configure in dashboard > Integrations. New KickoffLabs leads sync to ESP audience automatically. Pair with your ESP's automations for confirmation emails / reward delivery.
- **Webhooks**: Configure per-campaign in dashboard. Subscribe to confirmation + score-change + reward-level events. Handler-side, route by `__fraudulent` and `__event` keys.
- **Zapier**: Triggers (new lead, score change, reward unlocked) + actions (create lead, tag lead, approve, block). Use for HubSpot/Salesforce/Notion sync without code.
- **Pipedream / Integrately**: Listed working integrations for ad-hoc workflows.
- **Shopify**: Native connector — post-purchase referral triggers for ecommerce.
- **Facebook Audiences**: Sync KickoffLabs leads as a custom audience for retargeting.

## Campaign type selection

| Campaign type | Best for | Key feature | Plan minimum |
|---|---|---|---|
| **Pre-launch waitlist** | New product launches, app betas | Queue jumping via referrals; Dropbox/Robinhood style | Hobby |
| **Bonus-entry giveaway** | Lead gen via prize incentive | Multiple actions for entries (follow, share, refer); Gleam-style | Hobby (but Premium for A/B + reward emails) |
| **Milestone reward** | Newsletter / community growth | Tiered rewards at 3/10/25 referrals; Morning Brew style | **Premium** (reward emails are Premium+) |
| **Leaderboard giveaway** | High-engagement contests | Top-N referrers win; leaderboard endpoint capped at 50 | Hobby |
| **Email opt-in bribe** | Lead magnet downloads | Simple email-for-content swap | Hobby |
| **Newsletter referrals** | Subscriber-recruits-subscriber | Combines milestone + leaderboard | **Premium** |

## Fraud detection signals

Webhook `__fraudulent` array can contain:
- `duplicate_ip` — multiple signups from the same IP within KickoffLabs's window
- `bounced` — verification email bounced (requires email-verify enabled)
- `duplidate_email` — exact duplicate email (verbatim typo from docs)

Recommended response: auto-block on `bounced`, queue for human review on `duplicate_ip`/`duplidate_email`, then bulk-approve cleared leads via `POST /v2/{CAMPAIGN_ID}/approve` (up to 200 per call).

For weaker signals not caught by KickoffLabs (disposable domains, lookalike emails), filter server-side before forwarding to the API.

## Comparison with alternatives

| Tool | Primary use | Free tier | API + webhooks | Best for |
|---|---|---|---|---|
| **KickoffLabs** | Viral waitlists, giveaways, milestone, leaderboard | None (Hobby $13/mo annual) | ✅ v1 + v2, webhooks, Zapier | Founders + marketers running pre-launch waitlists + giveaways with built-in fraud detection |
| **Viral Loops** | Templated viral campaigns (Dropbox / Robinhood / Airbnb templates) | 14-day trial | ✅ API, webhooks, Zapier | Marketers wanting templated quick-launch campaigns; Webflow/Shopify/WP native integrations |
| **UpViral** | Viral contests + lead-gen funnels + referral leaderboards | None (~$59/mo entry) | ✅ API, webhooks, Zapier | Info-product entrepreneurs running viral contests + leaderboards |
| **Prefinery** | Developer-friendly private beta / gated access / waitlist + referrals | None (~$39/mo entry) | ✅ Unlimited API calls, webhooks, Zapier | SaaS / B2B running private betas and staged rollouts with unlimited API + forms |
| **ReferralCandy** | E-commerce referral marketing (Shopify-heavy) | None ($49/mo entry) | ✅ | Shopify stores wanting plug-and-play referrals |
| **ReferralHero** | Full-stack referral / affiliate / waitlist / contest with multi-level | 25 subs | ✅ (PRO+) | Teams wanting multi-level Level 1/2/3 + coupon groups + API |
| **ReferralKit** | Newsletter-only merge-tag referrals (no API) | First 10K leads free | ❌ | No-code newsletter operators under 10K leads |
| **SparkLoop** | Newsletter referrals + paid recommendations + partner network | Free Recs tier | ❌ public API | Newsletters at scale wanting referral + paid-rec monetization |
| **Voucherify** | Coupon + referral API for engineering teams | Build tier | ✅ API-first | Engineering teams building custom promo + referral logic |
| **LaunchList** | Viral Loops alternative for waitlists | Free tier | ✅ | Indie launches wanting Viral Loops-equivalent at lower cost |
| **QueueForm** | Word-of-mouth marketing SaaS | TBD | TBD | TBD (see backlog) |
| **Vyper** | Viral giveaways + contests | None | ✅ | Lifecycle: appears acquired/dormant — verify before recommending |

## When to use KickoffLabs

- Running pre-launch waitlist or giveaway and want built-in viral mechanics + fraud detection
- Need 60+ built-in bonus actions (visit page, follow Twitter, etc.) without custom code
- Want server-side webhooks with structured fraud flags
- Already using Klaviyo / Mailchimp / ActiveCampaign / Brevo (native ESP integration)
- Comfortable with $13–$202/mo annual based on lead volume

## When NOT to use KickoffLabs

- Need fully bespoke landing-page design — Capterra reviews flag design flexibility limits. Pair with Unbounce/Leadpages/Framer + AnyForm instead.
- Need multi-level Level 1/2/3 referral tracking — use ReferralHero.
- Newsletter-only with merge-tag insertion as the primary mechanic — use ReferralKit (free up to 10K).
- Need paid recommendations or a partner network — use SparkLoop.
- Need an API-first developer experience with unlimited API calls + forms — Prefinery is positioned more for that.
- Shopify-only e-commerce referral — ReferralCandy is Shopify-first.
- Need signed webhooks with documented HMAC — KickoffLabs doesn't publish a signing scheme; if regulated, verify with support first.
