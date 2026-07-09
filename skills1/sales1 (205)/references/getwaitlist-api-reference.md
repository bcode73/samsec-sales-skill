<!-- Source: https://getwaitlist.com/docs/api-docs/api-quickstart, /waitlist, /waiter, /authenticated, /schemas, and /docs/integrations/webhooks (fetched 2026-06-15) -->

# GetWaitlist API Reference

GetWaitlist exposes a small REST API split into an **unauthenticated** surface
(create/get a signup, read a waitlist or its leaderboard) and an
**authenticated** surface (list signups, advance/offboard/delete signups) that
requires an `api-key` header or a JWT access token.

- **Base URL**: `https://api.getwaitlist.com/api/v1/`
- **Content type**: `application/json`
- **No MCP server.** Automation = REST API + webhooks (`new_signup`,
  `offboarded_signup`) + Zapier/native connectors.

> The signup-create and signup-get endpoints require **no authentication** —
> anyone with your numeric `waitlist_id` can add or look up a signup. Treat
> `waitlist_id` as public (it is exposed in the embed widget) and never rely on
> these endpoints for trusted data. Sensitive reads (full email lists, names,
> phone, metadata) live behind the authenticated endpoints.

---

## Authentication

There are two authenticated mechanisms:

### 1. API key (`api-key` header)
Generate in the dashboard under **My Account → API Keys**. Keys **do not
expire** and are revoked only by manual deletion. Send on every authenticated
request:

```
api-key: YOUR_API_KEY
```

### 2. JWT access tokens (for dashboard-style auth)
Exchange email + password for a short-lived access token and a longer refresh
token.

**Create tokens** — `POST /api/v1/auth/create_tokens`
```json
// request
{ "email": "you@example.com", "password": "••••••••" }

// response
{
  "access_token": "string (3-day validity)",
  "refresh_token": "string (30-day validity)"
}
```

**Refresh access token** — `GET /api/v1/auth/refresh_access_token`
Header: `Authorization: Bearer {refresh_token}` → returns a new
`access_token` + `refresh_token` pair.

---

## Auth quick-start (simplest GET)

Read a public waitlist object (no auth needed):

```bash
curl "https://api.getwaitlist.com/api/v1/waitlist?waitlist_id=12345"
```

---

## Endpoints

### Unauthenticated

#### Create a signup — `POST /api/v1/signup`
Required: `email` (string), `waitlist_id` (integer).
Optional: `first_name`, `last_name`, `phone`, `referral_link` (the referrer's
share URL — credits the referrer), `metadata` (object), `answers` (object).

```bash
curl -X POST "https://api.getwaitlist.com/api/v1/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maya@example.com",
    "waitlist_id": 12345,
    "first_name": "Maya",
    "referral_link": "https://getwaitlist.com?ref_id=4F0BTBMAB",
    "metadata": { "plan_interest": "pro" }
  }'
```

Returns the **unauthenticated Signup object** (see Schemas) — includes
`priority`, `referral_token`, `referral_link`, `uuid`, `created_at`, `verified`.

#### Get a signup — `GET /api/v1/signup`
Required: `email`, `waitlist_id`. Optional: `phone`.
Returns the unauthenticated Signup object (same shape as the POST response).

#### Get a waitlist — `GET /api/v1/waitlist?waitlist_id=<id>`
Returns the Waitlist object: configuration, `statistics`
(`total_signups`, `current_signups`), styling, questions, and feature flags.

#### Get the leaderboard — `GET /api/v1/waitlist/<ID>/leaderboard`
Optional: `total_signups` (number of leaderboard rows; defaults to the
dashboard's `leaderboard_length`, typically 5).
Returns the Leaderboard object — top referrers with **censored** email/last
name/phone (privacy-safe for public display).

### Authenticated (`api-key` header or Bearer access token)

#### List signups — `GET /api/v1/signup/waitlist/<waitlist_id>`
Params: `offset`, `limit` (pagination — **offset/limit**), `referral_token`
(filter to signups referred by one token), `referral_tokens`,
`questions_request` (include `answers`), `include_referrer`,
`offboarded_request` (include removed signups).
Returns an array of authenticated Signup objects (or a grouped referral
structure when filtered).

#### Advance a signup — `PATCH /api/v1/signup/<uuid>`
Body: `spots_to_advance` (integer), optional `metadata`.
Moves a signup up the queue. Returns the updated Signup object.

#### Offboard signups — `PATCH /api/v1/signup`
Body: `waitlist_id`, `offboard_request: true`, `signups` (array of `{ "uuid": ... }`).
Marks signups as removed/launched — they get `removed_date` and
`removed_priority` but are retained (not deleted). Fires the
`offboarded_signup` webhook. Returns the array of offboarded Signup objects.

```bash
curl -X PATCH "https://api.getwaitlist.com/api/v1/signup" \
  -H "api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "waitlist_id": 12345,
    "offboard_request": true,
    "signups": [{ "uuid": "c60ff9f2-1a58-4551-87ea-414991184fba" }]
  }'
```

#### Delete signups — `DELETE /api/v1/signup`
Body: `waitlist_id`, `signups` (array of `{ "uuid": ... }`).
Permanently deletes (use for GDPR erasure). Returns **HTTP 204**.

---

## Pagination

Authenticated list uses **offset / limit**:

```bash
curl "https://api.getwaitlist.com/api/v1/signup/waitlist/12345?offset=0&limit=100" \
  -H "api-key: YOUR_API_KEY"
# next page: offset=100&limit=100 ...
```

<!-- Constructed pattern from documented offset/limit params — verify exact max page size against the live API. -->

---

## Schemas (verbatim from docs)

### Signup (unauthenticated)
```json
{
  "amount_referred": 0,
  "created_at": "2022-04-10_18-34-28",
  "email": "maya@example.com",
  "priority": 4985,
  "referral_link": "https://getwaitlist.com?ref_id=4F0BTBMAB",
  "referral_token": "4F0BTBMAB",
  "referred_by_signup_token": "REFTOKEN1",
  "removed_date": null,
  "removed_priority": null,
  "uuid": "c60ff9f2-1a58-4551-87ea-414991184fba",
  "verified": false,
  "waitlist_id": 12345
}
```
- `amount_referred` (int): number of other signups this one referred
- `priority` (int): position in the waitlist queue (lower = closer to front)
- `referral_token` (string): unique token to credit this signup when they refer
- `referral_link` (string): the share URL containing `ref_id=<token>`
- `referred_by_signup_token` (string): token of the referring signup (nullable)
- `removed_date` / `removed_priority`: set when offboarded (else null)
- `verified` (bool): email verification status

### Signup (authenticated) — adds PII + custom fields
```json
{
  "amount_referred": 0,
  "created_at": "2022-04-10_18-34-28",
  "email": "maya@example.com",
  "priority": 4985,
  "referral_link": "https://getwaitlist.com?ref_id=4F0BTBMAB",
  "referral_token": "4F0BTBMAB",
  "referred_by_signup_token": null,
  "removed_date": null,
  "removed_priority": null,
  "uuid": "c60ff9f2-1a58-4551-87ea-414991184fba",
  "verified": false,
  "answers": [{ "question_value": "What is your favorite animal?", "optional": false, "answer_value": "Cat" }],
  "phone": null,
  "first_name": "Maya",
  "last_name": "Kyler",
  "metadata": {},
  "waitlist_id": 1234
}
```
- `first_name`, `last_name`, `phone`: optional PII
- `metadata` (object): any custom JSON key-value pairs you store with the signup
- `answers` (array): responses to custom waitlist `questions`

### Waitlist
```json
{
  "id": 213,
  "configuration_style_json": {
    "widget_background_color": "#4937E7",
    "widget_button_color": "#000000",
    "widget_font_color": "#000000"
  },
  "logo": null,
  "spots_to_move_upon_referral": 3,
  "uses_firstname_lastname": false,
  "uses_leaderboard": true,
  "uses_signup_verification": false,
  "waitlist_name": "Title",
  "waitlist_url_location": "https://getwaitlist.com",
  "statistics": { "total_signups": 2200, "current_signups": 2200 },
  "title": null,
  "required_contact_detail": "EMAIL",
  "widget_shows_social_links": false,
  "signup_button_title": "Sign Up",
  "hide_counts": false,
  "leaderboard_length": 5,
  "remove_widget_headers": false,
  "questions": [{ "question_value": "What is your favorite animal?", "optional": false, "answer_value": ["Cat", "Dog", "Duck", "Other"] }],
  "twitter_message": "",
  "organization_uuid_fk": "30120c24-0ddc-4f35-9bc6-f5e3c7b09257"
}
```
Key fields: `spots_to_move_upon_referral` (queue boost per referral),
`uses_leaderboard`, `uses_signup_verification` (double opt-in / email verify),
`required_contact_detail` (`EMAIL` / phone / both), `questions` (custom signup
questions), `uses_zapier`, `uses_waitlist_widget_branding` (branding toggle),
`email_configuration_json`, `send_email_congratulations_on_referral`,
`hide_counts`, `leaderboard_length`.

### Leaderboard (censored for public display)
```json
{
  "leaderboard": [
    { "amount_referred": 5, "email": "b***@g**************", "first_name": "Brittany", "last_name": "S.", "phone": "415 *** ****" },
    { "amount_referred": 4, "email": "b*****@g**************", "first_name": "Bianca", "last_name": "G.", "phone": "234 *** ****" },
    { "amount_referred": 1, "email": "b*****@g**************", "first_name": "Bonnie", "last_name": "L.", "phone": "123 *** ****" }
  ]
}
```
Emails are masked, only the first letter of `last_name` is shown, and only the
first three phone digits — safe to render on a public landing page.

---

## Webhooks

Configure in the dashboard under the **Features** tab → **Webhook URL**.
GetWaitlist sends a `POST` to that URL on:

| Event | `event` value | Fires when |
|---|---|---|
| New Signup | `new_signup` | a user joins the waitlist |
| Signup Offboarded | `offboarded_signup` | a signup is removed/launched |

**Timeouts**: a webhook POST times out if it cannot **connect within 30
seconds**, or if the server **does not respond within 90 seconds**.

Payload — both events share `{ event, signup }` where `signup` is an
Authenticated Signup object:

```json
// new_signup
{
  "event": "new_signup",
  "signup": {
    "uuid": "c60ff9f2-1a58-4551-87ea-414991184fba",
    "email": "maya@example.com",
    "first_name": "Maya",
    "last_name": "Kyler",
    "priority": 4985,
    "created_at": "2022-04-10_18-34-28",
    "referral_token": "4F0BTBMAB",
    "amount_referred": 0
  }
}
```

```json
// offboarded_signup
{
  "event": "offboarded_signup",
  "signup": {
    "uuid": "c60ff9f2-1a58-4551-87ea-414991184fba",
    "removed_date": "2022-05-10_18-34-28",
    "removed_priority": 1000,
    "priority": null
  }
}
```

> The docs do not document an HMAC signing secret or a retry policy for
> webhooks. Treat deliveries as unsigned: validate by re-fetching the signup
> via the authenticated API (`GET /signup/waitlist/<id>` filtered by email)
> before trusting webhook contents for anything sensitive, and make handlers
> idempotent on `signup.uuid`.

---

## Error handling & gaps

- **Error shape**: not documented verbatim. Expect standard HTTP status codes
  (4xx for bad/missing `waitlist_id` or auth, 204 on successful delete).
  <!-- Constructed expectation — verify against live API. -->
- **Rate limits**: no published rate-limit headers or numeric limits in the
  docs. Be conservative (batch with `limit=100`, back off on 429) and re-verify.
- **No documented bulk-create endpoint** — signups are created one POST at a
  time.
- **No MCP server** as of this writing.
