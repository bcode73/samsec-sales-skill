<!-- Source: https://docs.sparkloop.app/ (re-verified 2026-06-13) -->

# SparkLoop API v2 Reference

> An API v1 is also still documented at `https://api.sparkloop.app/v1` (same `X-Api-Key` auth). v1 is "in active development" and not deprecated, but v2 is the recommended surface for new integrations and covers far more resources.

## Base URL

`https://api.sparkloop.app/v2`

## Authentication

Every request must include the `X-Api-Key` header with your API key (found in Account Settings → Integrations).

Missing or incorrect key returns HTTP 401:
```json
{ "error": "API key is missing!" }
```
or
```json
{ "error": "User not found!" }
```

## Request format

- POST and PUT requests must include: `Content-Type: application/json; charset=utf-8`
- Successful responses return HTTP 200/201 with JSON body
- Errors return 400/500 range with descriptive JSON messages

## Pagination

Endpoints returning multiple objects support:
- `page` — page number (default: 1)
- `per_page` — objects per request (default: 50, max: 200)

## Rate limiting

120 requests over a rolling 60-second period per API key. Exceeding returns HTTP 429. Implement exponential backoff.

---

## Subscribers

### Create a Subscriber
**POST** `/v2/subscribers`

| Parameter | Type | Required | Description |
|---|---|---|---|
| email | string | Yes | Subscriber email |
| name | string | No | Subscriber name |
| referrer_code | string | No | Referral code of the referring subscriber |
| ip_address | string | No | Subscriber IP |
| user_agent | string | No | Subscriber user agent |
| utm_source | string | No | UTM source |
| utm_campaign | string | No | UTM campaign |
| created_at | string | No | Creation timestamp |
| country_code | string | No | ISO 3166-1 Alpha2 country code |

**Response** (201):
```json
{ "subscriber": <Subscriber Object> }
```

**Errors** (400): Invalid/duplicate email, missing email field.

### List Subscribers
**GET** `/v2/subscribers`

| Parameter | Type | Description |
|---|---|---|
| type | string | Filter: `all`, `referrals`, `advocates` |
| expand | string | Include related data: `campaigns` |
| page | integer | Page number |
| per_page | integer | Results per page (max 200) |

**Response** (200):
```json
{
  "subscribers": [...],
  "per_page": 50,
  "page": 1,
  "total_pages": 10,
  "total_subscribers": 500
}
```

### Get Subscriber
**GET** `/v2/subscribers/:identifier`

Path parameter: `identifier` — subscriber UUID or email address.

Query parameter: `expand=campaigns` to include campaign memberships.

**Response** (200): `{ "subscriber": <Subscriber Object> }`
**Error** (404): Subscriber not found.

### Update Subscriber
**PUT** `/v2/subscribers/:identifier`

| Parameter | Type | Description |
|---|---|---|
| status | string | `unsubscribed` or `confirmed` |
| name | string | Updated name |
| email | string | Updated email |

**Response** (200): Updated subscriber object.
**Errors** (400): Invalid status, empty request body.

### Unsubscribe Subscriber
**PUT** `/v2/subscribers/:identifier/unsubscribe`

**Response** (200): Subscriber object with updated status.
**Error** (409): Already unsubscribed.

### Reject Subscriber
**PUT** `/v2/subscribers/:identifier/reject`

**Response** (200): Subscriber object with rejected status.
**Error** (409): Not in pending status.

---

## Campaigns

### List Campaigns
**GET** `/v2/campaigns`

Returns all campaigns. Currently limited to 1 campaign per account.

**Response** (200):
```json
{ "campaigns": [<Campaign Object>, ...] }
```

### Get Campaign
**GET** `/v2/campaigns/:identifier`

Path parameter: `identifier` — campaign UUID.

**Response** (200): `{ "campaign": <Campaign Object> }`
**Error** (404): Campaign not found.

### Update Campaign
**PUT** `/v2/campaigns/:identifier`

| Parameter | Type | Description |
|---|---|---|
| name | string | Campaign name |

**Response** (200): Updated campaign object.

---

## Partner Programs

Your own partner programs (where other newsletters recommend yours). Distinct from the read-only Partner Network directory below.

### List Partner Programs
**GET** `/v2/partner_programs`

Query: `page`, `per_page`. Ordered by `created_at` descending.

**Response** (200): `{ "partner_programs": [...], "meta": { "per_page", "page", "total_pages", "total_partner_programs" } }`

### Get Partner Program
**GET** `/v2/partner_programs/:identifier`

Path parameter: `identifier` — partner program UUID. Response fields include `uuid`, `publication` (nested), `status`, `cpa`, `referral_pending_duration`, `geo_restrictions`, `created_at`.

### Update Partner Program
**PUT** `/v2/partner_programs/:identifier`

| Parameter | Type | Description |
|---|---|---|
| total_budget | number | Total program budget |
| cpa | number | Cost per acquisition you pay per confirmed referral |
| redirect_url | string | Post-signup redirect |
| slug | string | Program slug |
| thankyou_page_url | string | Thank-you page |
| resources_url | string | Resources link for recommenders |
| terms | string | Program terms |
| show_in_directory | boolean | List in Partner Network directory |
| referral_pending_duration_enabled | boolean | Enable a screening/pending window |
| referral_pending_duration | integer | Pending window length |

### List Partner Program Referrals
**GET** `/v2/partner_programs/:identifier/referrals`

Query: `page`, `per_page`. Ordered by `referred_at` descending. Each referral includes email, status, CPA, confirmation data, and recommending publication details.

---

## Partner Network (directory)

Read-only directory of partner programs and publications you can recommend or join.

### List Partner Network Programs
**GET** `/v2/partner_network/partner_programs`

| Parameter | Type | Description |
|---|---|---|
| cpa | number | Filter by minimum CPA |
| max_payout | number | Filter by minimum max payout |
| accepted_countries | string | Comma-separated ISO 3166 country codes |
| can_be_recommended_via | string | Comma-separated channels: `upscribe`, `partner_link`, `magic_link` |
| sort | string | `max_payout` or `cpa` |

### Get Partner Network Program
**GET** `/v2/partner_network/partner_programs/:identifier`

### Join a Partner Network Program
**POST** `/v2/partner_network/partner_programs/:identifier/join`

| Parameter | Type | Required | Description |
|---|---|---|---|
| reason_for_recommending | string | Yes | Why you want to recommend this program |

---

## Publications

Your newsletter publications registered with SparkLoop.

### Create Publication
**POST** `/v2/publications`

Required: `name`, `categories`, `logo`, `audience_gender`, `income_levels`, `age_ranges`. Optional: `description`, `list_id`, `status`.

### List / Get / Delete Publications
- **GET** `/v2/publications`
- **GET** `/v2/publications/:identifier`
- **DELETE** `/v2/publications/:identifier`

### Update Publication
**PUT** `/v2/publications/:identifier`

Optional body fields: `name`, `description`, `categories`, `logo`, `status`, `auto_pilot`, `audience_gender`, `income_levels`, `age_ranges`.

### Partner Network Publications (directory)
- **GET** `/v2/partner_network/publications`
- **GET** `/v2/partner_network/publications/:identifier`
- **POST** `/v2/partner_network/publications/:identifier/recommend` — recommend a publication (no body parameters required).

---

## Partner Profile

### Get Partner Profile
**GET** `/v2/partner_profile`

**Response** (200): `{ "partner_profile": <Partner Profile Object> }`
**Error** (404): Partner profile not found.

---

## Upscribe

### List Upscribes
**GET** `/v2/upscribes`

**Response** (200): Array of Upscribe objects.

### Get Upscribe
**GET** `/v2/upscribes/:identifier`

Path parameter: `identifier` — Upscribe UUID.

**Response** (200): Upscribe object.
**Error** (404): Upscribe not found.

### Update Upscribe
**PUT** `/v2/upscribes/:identifier`

| Parameter | Type | Description |
|---|---|---|
| auto_pilot | boolean | Enable/disable auto-pilot recommendation matching |

**Response** (200): Updated Upscribe object.

### Subscribe to Recommendations
**POST** `/v2/upscribes/:identifier/subscribe`

| Parameter | Type | Required | Description |
|---|---|---|---|
| subscriber_email | string | Yes | Subscriber's email |
| country_code | string | Yes | ISO 3166-1 Alpha2 country code |
| recommendations | string | Yes | Comma-separated recommendation ref_codes |
| utm_source | string | No | For advanced reports |
| utm_campaign | string | No | For advanced reports |

**Response** (200): `{ "response": "ok" }`
**Errors** (400): Missing required parameters.

**Critical**: Always pass `country_code` — earnings depend on subscriber geography.

### List Recommendations for an Upscribe
**GET** `/v2/upscribes/:identifier/recommendations`

Query: `page`, `per_page`.

### Generate Recommendations
**POST** `/v2/upscribes/:identifier/recommendations`

| Parameter | Type | Description |
|---|---|---|
| country_code | string | ISO 3166-1 Alpha2 — critical for paid recommendations |
| region_code | string | ISO 3166-2 state/region (helpful for US-targeted advertisers) |
| limit | integer | Number of recommendations to return (default: 1) |

### Manage a Recommendation
- **PUT** `/v2/upscribes/:identifier/recommendations/:recommendation_identifier` — update a recommendation
- **PUT** `/v2/upscribes/:identifier/recommendations/:recommendation_identifier/pin`
- **PUT** `/v2/upscribes/:identifier/recommendations/:recommendation_identifier/unpin`
- **PUT** `/v2/upscribes/:identifier/recommendations/:recommendation_identifier/pause`
- **PUT** `/v2/upscribes/:identifier/recommendations/:recommendation_identifier/unpause`

Use pin to force a recommendation to the top and pause to temporarily stop showing one without removing it.

---

## Offers

### List Offers
**GET** `/v2/offers`

Query parameters: `page`, `per_page`. Ordered by `created_at` descending.

**Response** (200): Paginated offers array with metadata (`per_page`, `page`, `total_pages`, `total_offers`).

### Get Offer
**GET** `/v2/offers/:identifier`

Path parameter: `identifier` — offer UUID.

**Response** (200): `{ "offer": <Offer Object> }`
**Error** (404): Offer not found.

### Confirm an Offer Conversion
**POST** `/v2/offers/:offer_uuid/submissions/:submission_uuid/conversion`

Path parameters: `offer_uuid` (offer UUID), `submission_uuid` (submission UUID). Marks an action-type offer submission as converted.

**Response** (200): `{ "message": "Conversion tracked successfully" }`
**Errors**: 422 if the submission isn't an action type or the conversion is already confirmed; 404 if the offer or submission isn't found.

> Brand Offers pay $2–$200+ per confirmed conversion depending on the brand and conversion type (click, lead, or action).

---

## Webhooks

### Configuration
Set up in Account Settings → Integrations dashboard. SparkLoop sends POST requests with JSON payloads.

Optional: Verify webhook authenticity via the `SparkLoop-Token` request header.

**Important**: Respond with HTTP 200 and an empty body. All non-200 responses are treated as errors.

### Event types

#### `new_referral`
Triggered when a subscriber makes a tracked referral. Payload includes referrer and referred subscriber objects (ID, email, referral code, link, referral count).

#### `new_partner_pending_referral`
Sent when a partner-generated referral enters the screening period. Contains campaign data, subscriber info with "pending" status, and partner details including logo URL.

#### `new_partner_referral`
Dispatched when a partner referral passes verification. Same structure as pending but with "verified" `referral_status`.

#### `new_offer_lead`
Sent on lead confirmation. Includes `offer_id`, lead object (email, source, partner_id, referral_status), and partner information.

#### `reward_unlocked`
Triggered when a subscriber hits a referral milestone. Contains subscriber details, reward metadata (name, referrals required, recurring status), coupon code, and referral count.

#### `reward_redeemed`
Sent when a subscriber submits their address for a physical reward. Includes all unlock data plus `reward_variant` details (name, SKU) and complete shipping information.

#### `sync_subscriber`
Dispatched on referral creation/updates. Carries subscriber object with `referral_status` field (supports "rejected" and other states).

---

## Using Upscribe via API

### Generating recommendations

Call the recommendations endpoint with your Upscribe ID:

**Required parameters:**
- `country_code` — ISO 3166-1 Alpha2 (e.g., US, UK, DE). Critical for paid recommendations and earnings.
- `region_code` — ISO 3166-2 state/region code (optional, helpful for US-targeted advertisers)
- `limit` — number of recommendations to display (default: 1)

**Response includes:**
- `publication_name` and `description` — newsletter details
- `publication_logo` — asset URL
- `signup_url` — subscription destination
- `ref_code` — required for tracking subscriptions

### Submitting subscriptions

Use the subscribe endpoint with:
- `subscriber_email`
- `ref_codes` — comma-separated codes from selected recommendations
- `country_code` — required for accurate tracking and earnings

**Compliance note**: Ensure subscribers give explicit consent before being subscribed to recommended newsletters.
