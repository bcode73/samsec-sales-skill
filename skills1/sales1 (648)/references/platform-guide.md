# Viral Loops Platform Reference

## Overview

Viral Loops (viral-loops.com) is a **referral & viral-marketing campaign builder** for startups, SaaS, and
ecommerce — pick a template (referral, pre-launch waitlist, giveaway, milestone, ambassador, leaderboard),
embed a widget, and run a viral loop without building referral mechanics yourself. Best for founders/
marketers who want a turnkey waitlist or refer-a-friend program fast. Trade-offs: notifications are basic
(email only; SMS/automation thinner than ReferralHero), and pricing scales by participants.

## Capabilities & automation surface

| Module | What it does | Automation surface |
|---|---|---|
| Campaign templates | Referral, **pre-launch waitlist**, giveaway, milestone, ambassador, leaderboard, refer-a-friend | Built in dashboard (**UI**) |
| Widget / form | Embeddable signup + referral widget (JS) | Front-end JS with the `publicToken` |
| Participants | Add/read people, attribute referrers, track referral count + rank | **API** (`/campaign/participant`) + **webhooks** |
| Leaderboard | Top-referrer ranking for gamified pages | **API** (`/campaign/leaderboard`) |
| Rewards / milestones | Reward at N referrals; redeem | **API** + Reward-Redeemed webhook/Zap |
| Conversions | Mark a participant converted (paid/qualified) | **API** + Participant-Converted webhook/Zap |
| Integrations | Email/ESP, CRM, Zapier/Make | **Two-way Zapier** + webhooks |

**Programmatic interfaces:** REST API (`app.viral-loops.com/api/v3`, `publicToken`), **webhooks** (join /
referral-count / converted / reward-redeemed), **two-way Zapier**, Make, Pipedream. No MCP. See
`references/viral-loops-api-reference.md`.

## Pricing, limits & plan gates

*Best-effort from research (2026-06) — the live pricing page blocked automated fetches; verify on the site.*

| Plan | ~Price/mo | Notes |
|---|---|---|
| Build | ~$49 | entry; core templates, capped participants |
| Accelerate | ~$229 | higher participant limits, more features |
| Enterprise | custom | white-label, concierge/managed service |

- Pricing scales by **participants/contacts** — model the cap against your expected signup volume.
- White-label / unbranded and the fully-managed **Concierge** service are upper-tier/add-on.
- Free trial typically available; confirm current terms.

## Integrations

- **Direction:** push participants **in** (API/Zapier action), and react to referral/convert/reward events
  **out** (webhooks / Zapier triggers). The widget collects signups client-side.
- **Auth:** the campaign **`publicToken`** (per campaign) drives both widget and most API calls.
- **iPaaS / native:** two-way Zapier, Make, Pipedream; ESP/CRM connectors for syncing referred leads.

## Data model

Campaign-scoped; identity is **email**.

**Participant** <!-- Constructed — verify against live API -->
```json
{ "user": { "firstname": "Sam", "email": "sam@example.com" }, "referralCode": "abc123",
  "referralCountTotal": 6, "rank": 12, "referrer": { "email": "friend@example.com" } }
```

**Referral-count webhook** <!-- Constructed — verify -->
```json
{ "event": "participant.referral_count", "campaignId": "cmp_123",
  "participant": { "email": "sam@example.com", "referralCountTotal": 6 } }
```

## Quick-start recipes

### Recipe 1 — Add a participant from your app (API)

**Trigger:** new signup in your product → register them in the Viral Loops campaign, attributing the
referrer so the referral counts.
```bash
curl -s -X POST "https://app.viral-loops.com/api/v3/campaign/participant" \
  -H "Content-Type: application/json" \
  -d '{ "apiToken":"$PUBLIC_TOKEN", "user":{"firstname":"Sam","email":"sam@example.com"},
        "referrer":{"referralCode":"abc123"} }'
```
```python
import requests
def add_participant(email, first, referrer_code, token):
    r = requests.post("https://app.viral-loops.com/api/v3/campaign/participant",
        json={"apiToken": token, "user": {"firstname": first, "email": email},
              "referrer": {"referralCode": referrer_code}}, timeout=30)
    r.raise_for_status(); return r.json()
```
**Gotchas:** the `publicToken` is **per-campaign** (grab it from that campaign's install settings). Email is
the identity — pass the `referrer`'s code so the referral is credited.

### Recipe 2 — React to referral milestones (webhook, not polling)

**Trigger:** set up a webhook (Campaign Wizard) → on **New Referral Count** check if the threshold is hit,
then fulfill the reward (grant credit, send a code) and/or notify Slack. On **Participant Converted**, sync
the paid customer to your CRM. No documented HMAC, so restrict to a secret URL and **dedupe on
(email, referralCountTotal)** since count events can repeat. No-code alternative: the Zapier triggers.

### Recipe 3 — Push leads from another tool into a campaign (Zapier)

**Trigger:** a new lead in your CRM/form → Zapier **Create Participant** action adds them to the Viral Loops
campaign (with their referrer if known). Use this when you don't want to host an endpoint.

## Integration patterns

- **Campaign = the unit.** Each campaign has its own `publicToken`, widget, participants, and leaderboard;
  multi-program setups mean multiple tokens.
- **Attribute referrers on create.** A participant only earns a referral if you pass the referrer's code (or
  they came through the referral link) — missing it breaks attribution.
- **Webhook reliability.** No signature documented — secret URL + re-verify via `GET /campaign/participant`
  before paying out a reward; idempotent handlers (count events repeat).
- **Sync, don't silo.** Pipe New Participant → ESP/CRM so your referral list lives where you nurture it;
  Viral Loops' built-in email is basic.
- **Fraud watch.** Viral referral/giveaway campaigns attract fake signups — validate emails and watch for
  same-IP/disposable-email abuse before fulfilling rewards.
