<!-- Source: https://api.sender.net/ -->

# Sender API Reference

## Base URL

```
https://api.sender.net/v2/
```

HTTPS only — unencrypted HTTP is not supported.

## Authentication

Bearer token in the Authorization header:

```
Authorization: Bearer {API_ACCESS_TOKEN}
```

Generate tokens in Sender: Settings > API access tokens. Tokens are organization-wide (cover all groups/newsletters). Tokens are only shown once at creation — if lost, create a new one.

### Auth quick-start

```bash
curl -X GET https://api.sender.net/v2/subscribers \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Accept: application/json"
```

## Endpoints

### Subscribers (9 endpoints)

| Method | Path | Description |
|---|---|---|
| POST | `/subscribers` | Create new subscriber |
| GET | `/subscribers` | List all subscribers |
| GET | `/subscribers/{id}` | Get subscriber data |
| PUT | `/subscribers/{id}` | Update subscriber |
| DELETE | `/subscribers/{id}` | Delete subscriber |
| POST | `/subscribers/{id}/groups` | Add subscriber to a group (group ID in request body) |
| DELETE | `/subscribers/{id}/groups` | Remove subscriber from a group (group ID in request body) |
| DELETE | `/subscribers/{id}/phone` | Remove phone from subscriber |
| GET | `/subscribers/{id}/events` | Get subscriber's events |

<!-- 2026-06-13: Method corrected to PUT (not PATCH) and group add/remove paths corrected to /subscribers/{id}/groups with group ID in the body, per the live api.sender.net portal. -->

#### Add subscriber to a group — request

```json
POST /v2/subscribers/{id}/groups

{
  "groups": ["GROUP_ID"]
}
```

#### Create subscriber — request

```json
POST /v2/subscribers

{
  "email": "user@example.com",
  "firstname": "Jane",
  "lastname": "Doe",
  "phone": "+15551234567",
  "groups": ["GROUP_ID"],
  "trigger_automation": true
}
```
<!-- Constructed from docs — verify against live API -->

#### Create subscriber — response

```json
{
  "id": "z61Z7gy",
  "email": "user@example.com",
  "firstname": "Jane",
  "lastname": "Doe",
  "created": "2025-06-05T12:55:13.000000Z",
  "status": {
    "email": "active",
    "temail": "active"
  }
}
```
<!-- Constructed from docs — verify against live API -->

### Groups (6 endpoints)

| Method | Path | Description |
|---|---|---|
| POST | `/groups` | Create group |
| GET | `/groups` | List all groups |
| GET | `/groups/{id}` | Get group details |
| PUT | `/groups/{id}` | Update / rename group |
| DELETE | `/groups/{id}` | Delete group |
| GET | `/groups/{id}/subscribers` | List subscribers in group |

### Segments (4 endpoints)

| Method | Path | Description |
|---|---|---|
| GET | `/segments` | List all segments |
| GET | `/segments/{id}` | Get segment details |
| DELETE | `/segments/{id}` | Delete segment |
| GET | `/segments/{id}/subscribers` | Query subscribers in segment |

### Fields (4 endpoints)

| Method | Path | Description |
|---|---|---|
| POST | `/fields` | Create custom field |
| GET | `/fields` | List all custom fields |
| PATCH | `/fields/{id}` | Rename custom field |
| DELETE | `/fields/{id}` | Delete custom field |

### Campaigns (10 endpoints)

| Method | Path | Description |
|---|---|---|
| POST | `/campaigns` | Create campaign |
| GET | `/campaigns` | List all campaigns |
| GET | `/campaigns/{id}` | Get campaign details |
| PATCH | `/campaigns/{id}` | Update campaign |
| DELETE | `/campaigns/{id}` | Delete campaign |
| POST | `/campaigns/{id}/send` | Send campaign immediately |
| POST | `/campaigns/{id}/schedule` | Schedule campaign send |
| POST | `/campaigns/{id}/copy` | Copy/duplicate campaign |
| GET | `/campaigns/{id}/errors` | Get campaign errors |
| DELETE | `/campaigns/{id}/schedule` | Cancel scheduled send |

#### Create campaign — request

```json
POST /v2/campaigns

{
  "title": "Weekly Newsletter #42",
  "subject": "This week in tech",
  "from": "Tech Digest",
  "reply_to": "hello@example.com",
  "preheader": "5 stories you missed",
  "content_type": "html",
  "content": "<html><body><h1>Hello</h1></body></html>",
  "groups": ["GROUP_ID"],
  "segments": [],
  "google_analytics": 1,
  "auto_followup_active": false,
  "auto_followup_subject": "Did you miss this?",
  "auto_followup_delay": 24
}
```

#### Create campaign — response

```json
{
  "success": true,
  "data": {
    "id": "campaign-id",
    "title": "Weekly Newsletter #42",
    "subject": "This week in tech",
    "status": "DRAFT"
  }
}
```
<!-- Constructed from docs — verify against live API -->

**Campaign parameters:**
- `content_type`: "editor", "html", or "text"
- `auto_followup_delay`: 12, 24, 48, 72, 96, 120, 144, or 168 hours
- `reply_to`: must belong to a verified domain in your account

### Transactional Campaigns (7 endpoints)

| Method | Path | Description |
|---|---|---|
| POST | `/transactional-campaigns` | Create transactional campaign template |
| GET | `/transactional-campaigns` | List all transactional campaigns |
| GET | `/transactional-campaigns/{id}` | Get transactional campaign details |
| PATCH | `/transactional-campaigns/{id}` | Update transactional campaign |
| DELETE | `/transactional-campaigns/{id}` | Delete transactional campaign |
| POST | `/transactional-campaigns/{id}/send` | Send using template |
| POST | `/transactional-campaigns/send-raw` | Send raw HTML transactional email |
| POST | `/message/send` | Send a single transactional email directly (from/to/subject/html) |

#### Send transactional email — request

```json
POST /v2/message/send

{
  "from": { "email": "you@yourdomain.com", "name": "Your Name" },
  "to": { "email": "recipient@example.com", "name": "Recipient Name" },
  "subject": "Your Subject Line",
  "html": "<p>Your email content</p>"
}
```

Headers: `Authorization: Bearer YOUR_TOKEN`, `Content-Type: application/json`, `Accept: application/json`. The `from` address must use a verified transactional sender identity / domain.
<!-- 2026-06-13: Added — POST /v2/message/send is the documented REST endpoint for one-off transactional sends. -->

### Statistics (8 endpoints)

| Method | Path | Description |
|---|---|---|
| GET | `/statistics/sents` | Get campaign sends |
| GET | `/statistics/opens` | Get campaign opens |
| GET | `/statistics/clicks` | Get campaign clicks |
| GET | `/statistics/hard-bounces` | Get hard bounces |
| GET | `/statistics/soft-bounces` | Get soft bounces |
| GET | `/statistics/complaints` | Get spam reports |
| GET | `/statistics/unsubscribes` | Get unsubscribes |
| GET | `/statistics/group-percentages` | Get group performance (Pro plan) |

### Workflows (6 endpoints)

| Method | Path | Description |
|---|---|---|
| POST | `/workflows` | Create workflow |
| GET | `/workflows` | List all workflows |
| GET | `/workflows/{id}` | Get workflow details |
| PATCH | `/workflows/{id}` | Update workflow |
| DELETE | `/workflows/{id}` | Delete workflow |
| GET | `/workflows/{id}/performance` | Get workflow performance metrics |

### Custom Events (1 endpoint)

| Method | Path | Description |
|---|---|---|
| POST | `/custom-events` | Create custom event (triggers automations) |

### Account Webhooks (6 endpoints) — paid plans only

| Method | Path | Description |
|---|---|---|
| POST | `/account/webhooks` | Create webhook |
| GET | `/account/webhooks` | List all webhooks |
| GET | `/account/webhooks/{id}` | Get webhook details |
| PATCH | `/account/webhooks/{id}` | Update webhook |
| DELETE | `/account/webhooks/{id}` | Delete webhook |

#### Create webhook — request

```json
POST /v2/account/webhooks

{
  "url": "https://your-app.com/webhooks/sender",
  "topic": "groups/new-subscriber",
  "relation_id": "GROUP_ID"
}
```

#### Create webhook — response

```json
{
  "id": "QbY0Wa",
  "account_id": "Eqqve",
  "url": "https://your-app.com/webhooks/sender",
  "topic": "groups/new-subscriber",
  "group": "GROUP_ID",
  "total_deliveries": 0,
  "total_failures": 0,
  "response_time": 0,
  "status": "ACTIVE"
}
```

**Webhook topics (8 total):**
- `subscribers/new` — a new subscriber is added to the account
- `subscribers/updated` — subscriber data is updated
- `subscribers/unsubscribed` — a subscriber unsubscribes (account-wide)
- `groups/new` — a new group is created
- `groups/new-subscriber` — a subscriber is added to a specific group
- `groups/unsubscribed` — a subscriber unsubscribes from a specific group
- `campaigns/new` — a new campaign is created
- `bounces/new` — new bounces are recorded after a campaign send

Group-scoped topics (`groups/new-subscriber`, `groups/unsubscribed`) require `relation_id` (the group ID to track).
<!-- 2026-06-13: Expanded from 2 to the full 8 documented topics per the live webhooks help docs. -->

**Payload signing.** Each webhook configuration provides a **Signing Secret** (shown/rotatable in the Webhooks section of Account settings). Use it to compute an HMAC of the raw request body and compare it against the signature sent in the request headers to verify authenticity. The exact signature header name and HMAC algorithm are not stated verbatim in the public help docs — inspect the delivered request headers to confirm before deploying verification. Rotating the secret immediately invalidates the previous one.
<!-- 2026-06-13: Added — webhook payload signing via a per-webhook Signing Secret + HMAC is now documented; header name/algorithm not published. -->

Webhooks require a paid plan (Standard or Professional).

## Pagination

Page-based pagination is used on list endpoints. Specific pagination parameters are not documented publicly — check response headers for page/total metadata.

<!-- Pagination details not fully documented — verify against live API -->

## Rate limits

Rate limits are enforced **per account** (shared across all API tokens on the account) on a per-minute window. Every API response includes rate-limit headers:

- `X-RateLimit-Limit` — the maximum requests allowed per minute for your account
- `X-RateLimit-Remaining` — requests left in the current window
- `X-RateLimit-Reset` — when the current window resets

Exceeding the limit returns `429 Too Many Requests` with a `Retry-After` header giving the number of seconds to wait before retrying. Read `Retry-After` and back off accordingly; the exact numeric per-minute limit is account-specific and returned in `X-RateLimit-Limit` rather than published as a fixed number.
<!-- 2026-06-13: Updated — Sender now documents per-account rate limits with X-RateLimit-* headers and a Retry-After header on 429. -->

## Error handling

The API returns standard HTTP status codes:
- `200` — Success
- `401` — Invalid or missing Bearer token
- `403` — Insufficient permissions (e.g., webhook on free plan)
- `404` — Resource not found
- `422` — Validation error (e.g., invalid email format)
- `429` — Rate limited

## Gaps

- Pagination parameters not fully documented
- Webhook signature header name and HMAC algorithm not stated verbatim in public docs (signing secret + HMAC verification confirmed; inspect delivered headers)
- Custom event payload schema not documented
- Workflow creation parameters not documented
- No official SDKs (use any HTTP library)

<!-- 2026-06-13: Resolved prior gaps — rate limits ARE now documented (per-account, X-RateLimit-* headers, 429 + Retry-After), and all 8 webhook topics are now confirmed. -->
