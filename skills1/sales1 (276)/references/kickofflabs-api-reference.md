# KickoffLabs REST API Reference

<!-- Source: https://api.kickofflabs.com/ (v1 docs) + https://dev.kickofflabs.com/api/ (v2 docs index) + per-endpoint pages at https://dev.kickofflabs.com/{endpoint}/ + https://gist.github.com/scottwater/1224e7c727fcd3d96e29c7db3890e4a3 (webhooks). Research date 2026-06-01. v1 and v2 coexist — see Versioning note below. -->

## Overview

The KickoffLabs API enables integration with external services for lead management, campaign operations, and referral/contest automation. Two versions coexist: **v1** (older `/subscribe` and `/info` endpoints) and **v2** (newer endpoints under `/v2/CAMPAIGN_ID/...` for tags, leads, actions, leaderboard, fraud approval). With v2 you can send all data as JSON; responses are always JSON regardless of request type.

## Versioning

- **v1 base URL**: `https://api.kickofflabs.com/v1/{CAMPAIGN_ID}` — `/subscribe` and `/info`. Still active for simple lead adds.
- **v2 base URL**: `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}` — newer endpoints. JSON-first.

## Authentication

All endpoints require:
- **CampaignId** (path parameter in v1/v2)
- **API Key** — passed as `api_key` parameter (v1) or in the request body / header per v2 endpoint conventions

**Location**: KickoffLabs dashboard > Setup > Advanced Settings > API Access

**Security note**: "Your API Key should never be used in client side JavaScript." Use server-to-server only.

## Lead identification

Endpoints accepting existing leads support identification via:
1. **Email**
2. **Social_Id** (shorthand: `kid`, used in share URLs like `?kid=1QN7`)

---

# v1 Endpoints

## POST /subscribe — Add Lead

**URL**: `https://api.kickofflabs.com/v1/{CAMPAIGN_ID}/subscribe`

**Required parameters:**
- `email` — Lead's email address
- `api_key` — Campaign API key

**Recommended parameters:**
- `ip` — User's IP address
- `__url` — URL where lead signed up
- `__ref` — Referrer URL
- `__user_agent` — Lead's user agent

**Optional parameters:**
- `social_id` — Parent record social ID (for attribution)
- `points` — Points to assign (overwrites previous)
- `your_custom_parameters` — Custom data fields (avoid names starting with `_`)

## GET /info — Retrieve Lead Data

**URL**: `https://api.kickofflabs.com/v1/{CAMPAIGN_ID}/info`

**Required parameters (choose one):**
- `email` — Lead's email address
- `social_id` — Social ID from signup

**Optional parameters:**
- `api_key` — Returns custom fields when included
- `jsonp` — Wraps response in callback (HttpGet only)

**Response JSON fields:** `avatar`, `contest_score`, `contest_score_rank`, `counter`, `custom_fields`, `email`, `family_name`, `given_name`, `lead_count`, `parent_id`, `rank`, `redirect_url`, `referrals`, `social_id`, `social_url`, `url`

JSONP callback parameter wraps the JSON response (HttpGet only).

---

# v2 Endpoints

The v2 API is JSON-first. Most endpoints require `CampaignId` and `API_Key`.

## Campaigns

### Campaign Actions
**GET** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/actions`

Returns the bonus actions defined on the campaign (e.g. "follow on Twitter", "visit page", etc.).

### Campaign Lead Tags
**GET** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/tags`

Returns all lead tags configured on the campaign.

### Campaign Leaderboard
**GET** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leaderboard`

**Required parameters:**
- `limit` — Number of top leads to return (max 50)
- `lead_description` — How leads appear in results. Accepts `first_name`, `full_name`, `social_id`, or custom data field names
- `avatar_default` — Avatar style: `identicon`, `icon`, or `ui`

**Optional parameters:**
- `social_id` — A specific lead's identifier for flagging in the response

### Campaign Stats
**GET** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/stats`

Returns campaign-level statistics.

## Leads

### Approve (override fraud flag)
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/approve`

Manually override a lead that has been flagged as fraudulent.

**Required parameters:**
- `api_key` — Your account's API Key
- `email` — Single email or an array of up to 200 emails (bulk mode)

### Block
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/block`

Block a lead (prevent further participation / mark as fraudulent).

### Create / Update Lead
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads`

Create or update a lead; JSON body with email or social_id and custom fields.

### Get Lead
**GET** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/{email-or-social_id}`

### Delete Lead
**DELETE** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/{email-or-social_id}`

### Action Completed
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/actions/completed`

Mark a bonus action as completed for a lead. Awards configured points.

### Parent Action Completed
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/actions/parent-completed`

Mark a parent action as completed (for nested referral scoring).

### Add Points
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/add-points`

Add (not overwrite) points to a lead's score.

### Email Opt Out
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/opt-out`

### Waitlist (move to waitlist)
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/waitlist`

### Remove from Waitlist
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/remove-from-waitlist`

### Verify
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/verify`

Verify a lead via email confirmation flow.

### SMS Verification
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/leads/sms-verification`

Trigger an SMS verification flow for the lead. Requires SMS Contests add-on or Enterprise plan.

## Lead Tags

### Tag (and Create) Lead
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/tags/{TAG_ID}/lead`

Tags and creates a lead with the given lead tag. The `TAG_ID` is found at Set up > Advanced Settings > Lead Tags > "Add to your site".

**Required parameters:**
- `email` OR `social_id`

### Tag Lead Parent (if Exists)
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/tags/{TAG_ID}/lead-parent`

Tag the parent of a lead (the referrer who brought them in).

### Bulk Tags
**POST** `https://api.kickofflabs.com/v2/{CAMPAIGN_ID}/tags/bulk`

Bulk-tag multiple leads in one request.

## KOL.js

KickoffLabs offers a client-side JavaScript library (`KOL.js`) for embedding signup widgets, popups, and AnyForm integration. The platform's own guidance: "In most cases, we recommend using the AnyForm for custom pages instead of adding leads directly via the API."

---

# Webhooks

Webhook configuration is per-campaign. When events occur, KickoffLabs makes an HTTP POST to your configured URL with the event payload.

## Base webhook payload

```json
{
  "__event": "the_webhook_event",
  "avatar": "https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/310c4ac2-7026-4700-afde-496b1d217b03",
  "counter": 252,
  "contest_score": 300,
  "contest_score_rank": 19588,
  "custom_fields": {},
  "email": "scott@kickofflabs.com",
  "family_name": "Watermasysk",
  "given_name": "Scott",
  "id": 56999,
  "lead_count": 1803,
  "parent_id": null,
  "rank": 1,
  "redirect_url": "http://simple-leaderboard.kickoffpages.com?kolid=1QN7",
  "social_id": "1QN7",
  "social_url": "http://koapi.heroku.com?kid=1QN7",
  "subscription_number": 1,
  "referrals": 5,
  "url": "http://koapi.heroku.com"
}
```

## Conditional event extensions

The base payload is extended with these blocks depending on event:

### Fraud detection (`__fraudulent`)
```json
{
  "__fraudulent": [
    "duplicate_ip",
    "bounced",
    "duplidate_email"
  ]
}
```
(Note: `duplidate_email` typo is verbatim from KickoffLabs's own docs — keep it as-is when matching.)

### Referral data (`__referral`)
```json
{
  "__referral": {
    "email": "scott@kickofflabs.com",
    "social_id": "ABC",
    "phone_number": "+18779211031"
  }
}
```

### Reward level reached (`__reward_level`)
```json
{
  "__reward_level": {
    "required_points": 5,
    "reward_level_id": 1,
    "subject": "You did it!"
  }
}
```

### Score change (`__score_change`)
```json
{
  "__score_change": {
    "current_contest_score": 5,
    "previous_contest_score": 1
  }
}
```

### Tagged event (`__tagged`)
```json
{
  "__tagged": {
    "name": "Tag Name",
    "points": 20,
    "tag_id": "12324"
  }
}
```

## Webhook signing & retry behavior

The published gist and support docs do not document a signing mechanism (no HMAC header) or retry semantics. **If you need signed webhooks or guaranteed delivery, validate against the live dashboard configuration screen or contact KickoffLabs support** — don't assume.

---

# Rate limits

API rate limits scale with plan tier (per support docs):

| Plan | Rate limit |
|---|---|
| Hobby | ~10 calls/minute |
| Premium | ~20-50 calls/minute |
| Business | ~50-100 calls/minute |
| Enterprise | ~100 calls/minute (highest documented) |

Specific headers and back-off response shape are not documented in the public pages — confirm via test calls. Use bulk endpoints (Bulk Tags, bulk Approve) for high-volume scenarios.

---

# Working cURL examples

## v1: subscribe a lead with referrer attribution
```bash
curl -X POST "https://api.kickofflabs.com/v1/$CAMPAIGN_ID/subscribe" \
  --data-urlencode "email=newsignup@example.com" \
  --data-urlencode "api_key=$KICKOFFLABS_API_KEY" \
  --data-urlencode "social_id=1QN7" \
  --data-urlencode "ip=203.0.113.42" \
  --data-urlencode "__url=https://example.com/signup" \
  --data-urlencode "__ref=https://twitter.com/share?kid=1QN7"
```

## v1: get lead info by email
```bash
curl -G "https://api.kickofflabs.com/v1/$CAMPAIGN_ID/info" \
  --data-urlencode "email=newsignup@example.com" \
  --data-urlencode "api_key=$KICKOFFLABS_API_KEY"
```

## v2: tag and create a lead
```bash
curl -X POST "https://api.kickofflabs.com/v2/$CAMPAIGN_ID/tags/$TAG_ID/lead" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newsignup@example.com",
    "api_key": "'$KICKOFFLABS_API_KEY'"
  }'
```

## v2: leaderboard (top 10)
```bash
curl -G "https://api.kickofflabs.com/v2/$CAMPAIGN_ID/leaderboard" \
  --data-urlencode "api_key=$KICKOFFLABS_API_KEY" \
  --data-urlencode "limit=10" \
  --data-urlencode "lead_description=full_name" \
  --data-urlencode "avatar_default=identicon"
```

## v2: bulk-approve fraud-flagged leads (up to 200)
```bash
curl -X POST "https://api.kickofflabs.com/v2/$CAMPAIGN_ID/approve" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$KICKOFFLABS_API_KEY'",
    "email": ["a@example.com", "b@example.com", "c@example.com"]
  }'
```

---

# Gaps & notes

- The v2 endpoint index at `dev.kickofflabs.com/api/` lists endpoints but per-endpoint pages mostly do NOT include full request/response JSON examples. The shapes here are inferred from the lead response, webhook payload, and parameter lists — verify against a live test call before production use.
- Webhook signing is undocumented in public material.
- Rate-limit headers are undocumented; verify with test traffic.
- KOL.js library is referenced; complete JS API not documented in public pages.
- Pipedream + Integrately listings show working triggers/actions if you'd rather use iPaaS than raw HTTP.
- A community .NET SDK exists: `KickLib` (NuGet, not official).

**Note from KickoffLabs**: "In most cases, we recommend using the AnyForm for custom pages instead of adding leads directly via the API."
