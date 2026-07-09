# ReferralHero REST API Reference

<!-- Source: https://support.referralhero.com/integrate/rest-api and https://support.referralhero.com/integrate/rest-api/endpoints-reference (fetched 2026-06-01). Captured verbatim — do not summarize. -->

## Overview

ReferralHero offers a REST-based API that returns JSON responses. The service is actively developed, so changes are expected, with breaking changes requiring 2 weeks' advance notice.

## Base URL

All API calls target: `https://app.referralhero.com/api/v2`

## Authentication Methods

**Primary approach (recommended):**
- Header: `Authorization: Bearer YOUR_API_TOKEN`

**Fallback option:**
- Header: `X-API-Key: YOUR_API_TOKEN`

All requests require HTTPS. Unauthenticated calls fail with error `no_token`.

Token location: ReferralHero dashboard > Account > API.

## API Token Security

Your token grants significant access privileges and should remain confidential. Avoid exposing it in public repositories, client-side implementations, or any publicly visible locations, as this creates security vulnerabilities.

## Response Format

Responses use JSON. Any HTTP status code other than 200 indicates an error condition.

## Rate Limits

The API enforces a soft threshold of 5,000 requests per hour. Exceeding this limit returns HTTP 429 with error code `too_many_calls`. Contact ReferralHero support to request higher limits.

---

# Endpoints Reference

## Lists Endpoints

### Create a new list
**POST** `https://app.referralhero.com/api/v2/lists`

Parameters: `website` (string), `name` (string)

### Retrieve all lists
**GET** `https://app.referralhero.com/api/v2/lists`

Parameters: `page` (string, default 1)
Returns: Paginated results (10 per page)

### Get List Leaderboard
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/leaderboard`

Parameters: `uuid` (string), `count` (string, 10-100)

### Get list rewards
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/bonuses`

Parameters: `uuid` (string)

---

## Subscribers Endpoints

### Add a subscriber
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers`

Key parameters: `uuid`, `email` / `phone_number` / `crypto_wallet_address` / `other_identifier_value`, `name`, `status`, `transaction_id`, `conversion_category`, `conversion_value`, `device`, `source`, `double_optin`, `points`, `referrer`, `extra_field`, `extra_field_2`, `domain`, `stripe_customer_id`, `advocate_name`, `tags`

### Track referral conversion event
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/track_referral_conversion_event`

Parameters: `uuid`, identifier fields, `referrer`, `conversion_value`, `stripe_customer_id`, `transaction_id`, `product_id`, `tags`

### Confirm referral by Subscriber ID
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/confirm`

Parameters: `uuid`, `subscriber_id`

### Confirm referral by Unique Identifier
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/confirm`

Parameters: `uuid`, identifier fields (`email`, `crypto_wallet_address`, `phone_number`, `other_identifier_value`)

### Update a subscriber
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id`

Parameters: `uuid`, `subscriber_id`, `name`, `email`, identifier fields, `extra_field`, `extra_field_2`, `points`, `stripe_customer_id`, `tags`, `address`, `city`, `country`, `referral_status`

### Add points to a subscriber
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/add_points`

Parameters: `uuid`, identifier field, `points`

### Track Transactions (Single)
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/add_transactions`

Parameters: `uuid`, identifier field, `amount` (required), `transaction_id`, `product_id`, `lifetime_spend`, `reward_value`

### Track Bulk Transactions
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/add_bulk_transactions`

Request body: JSON with `transactions` array (max 500 per request)

### Promote a subscriber
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/promote`

Parameters: `uuid`, `subscriber_id`

### Trigger manual rewards
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/unlock_promoted_reward`

Parameters: `uuid`, `subscriber_id`, `reward_id`

### Retrieve all subscribers by name
**GET** `https://app.referralhero.com/api/v2/subscribers/search_by_name`

Parameters: `name` (required), `page` (default 1)

### Retrieve all subscribers from a list
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers`

Parameters: `uuid`, `sort_by`, `page`, `extra_field`, `extra_field_2`, `option_field`, `stripe_customer_id`

### Retrieve subscriber by ID
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id`

Parameters: `uuid`, `subscriber_id`

### Retrieve subscriber by email
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/retrieve_by_email`

Parameters: `uuid`, `email`

### Retrieve subscriber by MWR
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/retrieve_by_mwr`

Parameters: `uuid`, `mwr` (referrer's referral code)

### Retrieve all referrals of a subscriber
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/referred`

Parameters: `uuid`, `subscriber_id`, `page`, `sort_by`

### Retrieve Level 2 referrals
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/level_2_all_referrals`

Parameters: `uuid`, `subscriber_id`

### Retrieve Level 3 referrals
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/level_3_all_referrals`

Parameters: `uuid`, `subscriber_id`

### Retrieve Level 1 confirmed referrals
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/level_1_referrals`

Parameters: `uuid`, `subscriber_id`, `page`, `sort_by`

### Retrieve Level 2 confirmed referrals
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/level_2_referrals`

Parameters: `uuid`, `subscriber_id`, `page`, `sort_by`

### Retrieve Level 3 confirmed referrals
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/level_3_referrals`

Parameters: `uuid`, `subscriber_id`, `page`, `sort_by`

### Retrieve all rewards for all subscribers
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/rewards`

Parameters: `uuid`, `status` (optional), `page`, `per_page`

### Retrieve all rewards unlocked by a subscriber
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/rewards`

Parameters: `uuid`, `subscriber_id`, `status` (optional)

### Delete a subscriber
**DELETE** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id`

Parameters: `uuid`, `subscriber_id`

### Update reward status by reward_id
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/update_reward_status`

Parameters: `uuid`, `reward_id`, `status` (sent / resent / canceled)

### Mark Referral as Unqualified
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/unqualify`

Parameters: `uuid`, `subscriber_id`

### Mark Referral as Qualified
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/subscribers/:subscriber_id/qualify`

Parameters: `uuid`, `subscriber_id`

---

## Coupon Endpoints

### Create coupon group
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/coupon_groups`

Parameters: `uuid`, `name`, `coupons` (array), `active` (boolean)

### Create coupons
**POST** `https://app.referralhero.com/api/v2/lists/:uuid/coupons`

Parameters: `uuid`, `coupon_group_id`, `coupons` (array)

### Retrieve all coupon groups
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/coupon_groups`

Parameters: `uuid`

### Retrieve coupons
**GET** `https://app.referralhero.com/api/v2/lists/:uuid/coupon_groups/:id`

Parameters: `uuid`, `id` (coupon group ID)

---

## Working cURL examples

### Add a subscriber with attribution
```bash
curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newsignup@example.com",
    "name": "Alex",
    "referrer": "JANE7X",
    "source": "landing_page",
    "double_optin": true
  }'
```

### Retrieve subscriber by email
```bash
curl -G "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers/retrieve_by_email" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN" \
  --data-urlencode "email=newsignup@example.com"
```

### Bulk-track transactions (500 per request)
```bash
curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers/add_bulk_transactions" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {"email":"a@example.com","amount":49.99,"transaction_id":"t1"},
      {"email":"b@example.com","amount":29.99,"transaction_id":"t2"}
    ]
  }'
```

### Promote + unlock reward
```bash
curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers/$SUB_ID/promote" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN"

curl -X POST "https://app.referralhero.com/api/v2/lists/$LIST_UUID/subscribers/$SUB_ID/unlock_promoted_reward" \
  -H "Authorization: Bearer $REFERRALHERO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reward_id":"rwd_111"}'
```

## Error handling

| Status | Error code | Meaning |
|---|---|---|
| 200 | — | Success |
| 4xx/5xx | (various) | Any non-200 indicates error |
| 401 | `no_token` | Missing or invalid auth header |
| 429 | `too_many_calls` | 5,000 req/hour soft limit hit; back off and retry |

## Pagination

Endpoints returning lists use `page` (1-based). Default page size is 10 for `/lists`, varies for other endpoints. Use `per_page` where supported (e.g., `/rewards`).

## Webhooks

Webhooks are configured in the dashboard (PRO+ plans). Supported events include subscriber confirmation, referral attribution, milestone reached, and reward unlocked. The endpoint reference docs above do not enumerate the webhook payload schema verbatim — confirm payload shape against a live webhook capture or the dashboard configuration screen.

---

**Note from source:** For questions beyond this documentation's scope, query the full knowledge base using: `GET https://support.referralhero.com/integrate/rest-api.md?ask=<your_question>`.
