<!-- Source: https://developers.referral-factory.com/ (ReadMe portal; pages fetched as Markdown via llms.txt index, 2026-06) -->
<!-- Verbatim from the official API reference. ReadMe's repeated "Documentation Index" boilerplate lines and HTML rendering wrappers have been stripped; all endpoint paths, methods, JSON schemas, field names, enums, and examples are reproduced exactly as documented. -->

# Referral Factory API Reference

## Introduction

The Referral Factory API lets you seamlessly integrate, automate, and extend your program with powerful actions and custom apps.

Using our API you will be able to:

- Add new users to your campaign, and issue them with referral links
- Send new referred users to any endpoint using webhooks
- Access all of your user records in real-time
- View, update, add or delete user records
- Qualify referred users
- View, update, issue rewards

The API is RESTful — clean URL structure, familiar HTTP methods (POST, GET, PUT, DELETE), and standardized JSON responses with clear error codes.

## Base URL

```
https://api.referral-factory.com/api/v2
```

(The OpenAPI `servers.url` is `https://api.referral-factory.com/api/v2`. Note: one help-doc example references `https://referral-factory.com/api/v2/users?per_page=250` — the `api.` host from the OpenAPI spec is authoritative; verify in-account.)

## Authentication

The Referral Factory API uses **Bearer Authentication**. Each account is issued a **single API Access Token**.

- **One token at a time:** Only one active access token is allowed per account. Generating a new token automatically deactivates any existing tokens for that account.
- **Authorization header:**

```
Authorization: Bearer your_access_key
```

Protect your account with 2FA, since the token grants full API access.

### Obtain API keys

Log in to your Referral Factory account (you must be on at least the **Basic plan**). Navigate to **Settings → 'Webhooks and API' tab**, scroll to the **API** section, and generate your API access token. Generating a new token deactivates any existing tokens.

## API Limits

- **Burst limit: 600 API calls per one minute.**
- Throttle accordingly. If you abuse your limits more than three times, your application IP will be temporarily blocked.

## Errors

| Error Code | Meaning |
| :--------- | :------ |
| 400 | Bad Request — Your request is invalid. |
| 401 | Unauthorized — Your API key is incorrect. |
| 403 | Forbidden — The resource requested is marked for administrators only. |
| 404 | Not Found — The specified resource could not be found. |
| 405 | Method Not Allowed — You tried to access a resource with an invalid method. |
| 406 | Not Acceptable — You requested a format that isn't in JSON format. |
| 410 | Gone — The resource requested has been removed from the data server. |
| 429 | Too Many Requests — You're requesting too many resources at one time. |
| 500 | Internal Server Error — We had a problem with our server. Please try again later. |
| 503 | Service Unavailable — We're temporarily offline for maintenance. Please try again later. |

Errors are returned as JSON structured like this:

```json
{
    "code": 422,
    "message": "Validation errors in your request",
    "errors": {
        "email": [
            {
                "field": "email",
                "message": "The email field is required."
            }
        ]
    }
}
```

---

## Users

### Create a user — `POST /users`

Creates a new user. This user will be a **Person Referring**, with a source of `API`. To add a **Person Invited** (a referral), attach the `referrer` field.

Request body schema:

```json
{
  "campaign_id": 1,            // integer, REQUIRED
  "first_name": "John",        // string, REQUIRED
  "email": "john@example.com", // string, REQUIRED
  "notify": true,              // boolean, optional — send the user a welcome notification
  "referrer": {                // object, optional — attach to credit a referrer (makes this a Person Invited)
    "field": "code",           // enum: "id" | "code" | "email"
    "value": "ueONFmUp"
  },
  "meta": [                    // array, optional — extra campaign field values
    { "field": "Last Name", "value": "Smith" }
  ],
  "promotion": true            // boolean, optional — also generate a promotion code (only works when Stripe is connected)
}
```

> Attribution: a new user only counts as a referral of someone else when you pass the `referrer` object (or the signup arrives through that referrer's referral link). Omitting `referrer` creates a standalone Person Referring.

### Retrieve a user — `GET /users/{identifier}`

Retrieves a specific user and all their data. `identifier` = the user's `code` **or** `id`.

### List all users — `GET /users`

Retrieves users in chunks. Default 25 per chunk; add `per_page` (max **250**) to get more, e.g. `GET /users?per_page=250`. Get the next chunk via the `links → next` property in the response (cursor-style pagination).

### Update a user — `PUT /users/{id}`

Updates a specific user (e.g. when a referral is qualified, or user info changes). `id` is the integer user id. Body:

```json
{
  "first_name": "John",
  "email": "john@example.com",
  "meta": [ { "field": "Country", "value": "Netherlands" } ]
}
```

### Delete a user — `DELETE /users/{id}`

Deletes a specific user. **Irreversible on live data** — test on a staging/test campaign.

### Qualification of user — `PUT /users/qualification`

Updates a user's qualification (qualifying triggers reward eligibility). Three ways to identify the user:

1. By user `id`
2. By user `code`
3. By `email` **and** `campaign_id`

Body:

```json
{
  "id": 123,             // OR "code": "ueONFmUp", OR ("email" + "campaign_id")
  "email": "john@example.com",
  "campaign_id": 1,      // required when using email
  "qualified": true      // boolean, REQUIRED (set false to unqualify)
}
```

### User object (Example)

```json
{
    "id": 123,
    "campaign_id": 1,
    "referrer_id": null,
    "first_name": "John",
    "email": "john@example.com",
    "code": "ueONFmUp",
    "reach": 3,
    "source": "Direct",
    "type": "person_referring",
    "ip": "62.90.15.90",
    "url": "https://example.referral-factory.com/ueONFmUp",
    "promotion": { "code": "SAVE50" },
    "qr": {
        "src": "https://example.referral-factory.com/ueONFmUp/qr-code",
        "download": "https://example.referral-factory.com/ueONFmUp/download-qr-code"
    },
    "signed_up_at": "2024-12-27",
    "qualified_at": null,
    "unsubscribed_at": null,
    "meta": [
        { "field": "Last Name", "value": "Smith" },
        { "field": "Country", "value": "Netherlands" }
    ],
    "sharing": {
        "socials": [
            { "social": "email", "url": "https://referral-factory.com/ueONFmUp/socials/email" },
            { "social": "twitter", "url": "https://referral-factory.com/ueONFmUp/socials/twitter" },
            { "social": "whatsapp", "url": "https://referral-factory.com/ueONFmUp/socials/whatsapp" }
        ],
        "subject": null,
        "text": null
    },
    // analytics property is only present when you pass `with=user.analytics`
    "analytics": { "reach": 12, "referrals": 8, "qualified_referrals": 3 }
}
```

**User field reference:** `id` (int), `campaign_id` (int), `referrer_id` (int), `code` (string, unique), `url` (unique join link), `promotion.code` (string, only if Stripe connected), `qr.src` / `qr.download`, `first_name`, `email`, `reach` (string), `source` (enum: `Direct`, `Referred`, `Api`, `Added`, `Zapier`, `Widget`, `Popup`, `Embed`, `Test`), `type` (enum: `person_referring`, `person_invited`), `ip`, `signed_up_at` (date), `qualified_at` (nullable date — `null` if not qualified), `unsubscribed_at` (nullable date), `meta[]` (`field` + `value`), `sharing.socials[]` (`social` enum: sms/lineme/email/wechat/twitter/facebook/linkedin/telegram/whatsapp/messenger + `url`), `sharing.subject`, `sharing.text`, `analytics.reach` / `analytics.referrals` / `analytics.qualified_referrals` (only with `with=user.analytics`).

---

## Campaigns

### List all campaigns — `GET /campaigns`

Retrieves a list of all campaigns.

### Retrieve a campaign — `GET /campaigns/{identifier}`

Retrieves a specific campaign. `identifier` = the campaign's `code` **or** `id`.

**Campaign field reference:** `id` (int), `name`, `code` (unique), `lang`, `url` (unique join link), `reach`, `status` (enum: `launched`, `draft`, `paused`), `starts_at` (nullable date — `null` = already live), `ends_at` (nullable date — `null` = live forever until paused/deleted), `created_at`, `fields.person_referring[]` / `fields.person_invited[]` (each: `id`, `type` enum input/select, `label`, `value`, `required`), `assets.logo` (`type` enum circle/rectangle/square, `path` nullable), `analytics.reach` / `analytics.users` / `analytics.referrals` / `analytics.qualified_referrals` (only with `with=campaign.analytics`).

---

## Rewards

Reward endpoints are scoped by a `{metric}` path param: enum `amount`, `commission`, `coupon`, `custom`.

### List all rewards — `GET /rewards/dashboard/{metric}`

Retrieves a list of all the rewards in your dashboard.

### List all due rewards — `GET /rewards/due/{metric}`

Lists rewards that are owed (due) but not yet issued.

### List all issued rewards — `GET /rewards/issued/{metric}`

Lists rewards that have already been issued.

### List all remaining coupons — `GET /rewards/...` (coupon metric)

Lists remaining (unallocated) coupons.

### Issue a due reward — `POST /rewards/issue/{identifier}`

Issues a due reward. `identifier` = the due reward's integer id (from the due rewards list).

### Cancel a due reward — `POST /rewards/cancel/{identifier}`

Cancels a due reward. `identifier` = the due reward's integer id.

### Update total spend of a due reward — `PUT /rewards/...`

Updates the total spend of a `commission`/`amount`/`custom` due reward.

**Due reward field reference:** `id` (int), `reward_id` (int), `recipient_id` (int — the user), `can_be_issued` (boolean), `coupon` (string — only for `coupon` rewards), `count` (int — only for `amount`/`commission`/`custom`), `total` (float — only for `amount`/`commission`/`custom`).

---

## Webhooks

Webhooks send data in and out of Referral Factory in real time. With them you can:

- Send users out of Referral Factory to any endpoint
- Qualify users by email, code or coupon (inbound)
- Issue rewards in real time

**Setup:** in your Referral Factory account go to **Settings → 'Webhook and API'** to find your webhook endpoints and set up triggers.

**Outbound triggers (documented):**
- When a new user (Person Referring **or** Person Invited) joins your campaign
- When a referred user (Person Invited) becomes **qualified**

**Inbound webhook:** send a referred user's unique `code` (or coupon code) to the endpoint shown in your account to qualify them once they convert. Inbound webhooks can also issue rewards.

**Signature / HMAC:** none documented. No webhook signing or HMAC verification is described in the docs — treat the endpoint as a secret URL, dedupe, and re-verify via `GET /users/{identifier}` before issuing rewards.

**Retry behaviour:** not specified in the docs.

> ⚠️ Payload schema: the docs do not publish an explicit outbound webhook JSON schema (they suggest inspecting deliveries via webhook.site). Expect a User-shaped object (see the User example above). Confirm the exact fields against a live test delivery before coding against them.

---

## Query modifiers (collections)

Most list/retrieve endpoints support: **Filtering** (e.g. search by a string), **Relations** via `with=` (e.g. `with=user.analytics`, `with=campaign.analytics`), **Select Fields** (reduced payloads), and **Ordering** (directional sort). See the live reference for exact param syntax per resource.
