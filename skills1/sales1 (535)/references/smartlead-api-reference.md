### Smartlead REST API — Comprehensive Reference

**Base URL**: `https://server.smartlead.ai/api/v1/`
**Docs**: https://api.smartlead.ai/
**API version**: v1

---

## Authentication

API Key authentication via the `api_key` query parameter. Every request must include your API key as a query string parameter.

| Detail | Value |
|---|---|
| Parameter | `api_key` (query string parameter) |
| Where to find | Settings > API Keys in Smartlead app |

**Example**:
```
GET https://server.smartlead.ai/api/v1/campaigns?api_key=YOUR_API_KEY
```

---

## Request & Response Format

### Requests

- **GET** for read operations, **POST** for create/update operations
- **Content-Type**: `application/json` for POST requests
- API key is always passed as a query parameter, even on POST requests

### Response Format

Successful responses return JSON. List endpoints return arrays directly or wrapped in a data object. Single-record endpoints return the object directly.

### Error Responses

Errors return a JSON object with an error message:

```json
{
  "error": "Invalid API key",
  "status": 401
}
```

**Common error codes**:

| HTTP Status | Description |
|---|---|
| `401` | Invalid or missing API key |
| `404` | Resource not found |
| `400` | Invalid request parameters |
| `429` | Rate limit exceeded |
| `500` | Server error — retry with backoff |

---

## Pagination

**Type**: Offset-based

| Parameter | Type | Description |
|---|---|---|
| `offset` | integer | Number of records to skip. Default: 0. |
| `limit` | integer | Number of records to return. Default: 100. Max: 100. |

**How to paginate**:
1. Make the initial request with `offset=0`
2. If the response contains `limit` results, increment `offset` by `limit` and request again
3. Continue until fewer than `limit` results are returned

**Example**:
```
GET /campaigns?api_key=YOUR_API_KEY&offset=0&limit=50
```

---

## Rate Limits

| Detail | Value |
|---|---|
| Model | Per-minute throttle, applied across all endpoints combined |
| Default limit | **60 requests per minute per API key** (this is the documented default; client-level API keys are also 60/min by default and adjustable). Higher-tier plans may have higher allowances — contact support for plan-specific limits. |
| Burst | A short-window burst limit also applies (~10 requests / 2 seconds). |
| Scope | Per API key (account-level or client-level) |
| When exceeded | HTTP `429 Too Many Requests`. Error body includes a `retry_after` value (commonly 30 seconds). |
| Retry strategy | On `429`, wait at least ~2 seconds before retrying; honor the `retry_after` value / `Retry-After` header when present, otherwise use **exponential backoff with jitter** (1s, 2s, 4s, 8s, 16s…). Set client-side throttle to ~80% of the limit (e.g. 50/min when the limit is 60) to avoid edge-case 429s. |

> Plan names referenced for rate tiers are now **Base, Pro, Unlimited Smart, Unlimited Prime** (the older "Basic/Custom" tier names are retired). The 60/min default applies broadly; do not assume a fixed 120/min "Pro" cap without confirming against support.

---

## All API Endpoints

All paths are relative to `https://server.smartlead.ai/api/v1/`.

---

### Campaigns (6 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/campaigns` | List all campaigns. Returns id, name, status, stats. |
| GET | `/campaigns/{id}` | Get a single campaign by ID with full details. |
| POST | `/campaigns` | Create a new campaign. |
| POST | `/campaigns/{id}` | Update an existing campaign. |
| GET | `/campaigns/{id}/statistics` | Get campaign statistics — sent, opens, clicks, replies, bounces. |
| DELETE | `/campaigns/{id}` | Delete a campaign. |

**`GET /campaigns` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `offset` | integer | No | Pagination offset (default 0) |
| `limit` | integer | No | Results per page (default 100, max 100) |

**Response**:
```json
[
  {
    "id": 12345,
    "name": "Q1 Cold Outreach",
    "status": "ACTIVE",
    "created_at": "2024-01-15T10:00:00Z",
    "stats": {
      "total_leads": 500,
      "sent": 450,
      "opened": 225,
      "clicked": 40,
      "replied": 35,
      "bounced": 10
    }
  }
]
```

**`POST /campaigns` — Body**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Campaign name |
| `client_id` | integer | No | Client/workspace ID (for agency accounts) |

**Campaign statuses**: `DRAFT`, `ACTIVE`, `PAUSED`, `COMPLETED`

---

### Leads

| Method | Endpoint | Description |
|---|---|---|
| POST | `/campaigns/{campaign_id}/leads` | Add leads to a campaign. Accepts an array of lead objects in `lead_list`. **Max 400 leads per request.** Validates against block lists and duplicates. |
| GET | `/campaigns/{campaign_id}/leads` | List leads in a campaign (paginated). |
| GET | `/leads/{id}` | Get a single lead by ID with full activity history. |
| POST | `/campaigns/{campaign_id}/leads/{lead_id}/category` | Update a lead's **category** (Interested, Not Interested, etc.) for the campaign they belong to. Body: `category_id` (number; `null` to remove), `pause_lead` (boolean, default `false`). |
| GET | `/campaigns/{campaign_id}/leads-export` | Export campaign leads as CSV. |
| DELETE | `/campaigns/{campaign_id}/leads/{lead_id}` | Remove a lead from a campaign. |

> **Lead "statuses" are actually categories.** Smartlead organizes leads with **lead categories** (e.g. Interested, Not Interested, Meeting Booked), not a fixed status enum. Categories are customizable and referenced by numeric `category_id`. Fetch the campaign's categories via `GET /campaigns/{campaign_id}/leads/fetch-categories` (a.k.a. fetch lead categories) to map names → IDs before updating. The category-update endpoint takes `category_id`, **not** a string like `INTERESTED`.

**`POST /campaigns/{campaign_id}/leads/{lead_id}/category` — Body**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category_id` | number | Yes | Category ID to assign. Use `null` to remove the category. |
| `pause_lead` | boolean | No | Pause the lead after categorizing (default `false`). |

**`POST /campaigns/{campaign_id}/leads` — Body**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lead_list` | array | Yes | Array of lead objects (see below). **Max 400 per request.** |

**Lead object in `lead_list` array**:

| Field | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Lead's email address |
| `first_name` | string | No | Lead's first name |
| `last_name` | string | No | Lead's last name |
| `company` | string | No | Company name |
| `custom_fields` | object | No | Key-value pairs for custom merge fields |

**Example request**:
```json
POST /campaigns/12345/leads?api_key=YOUR_API_KEY

{
  "lead_list": [
    {
      "email": "jane@acme.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "company": "Acme Corp",
      "custom_fields": {
        "title": "VP of Sales",
        "pain_point": "low reply rates"
      }
    },
    {
      "email": "bob@globex.com",
      "first_name": "Bob",
      "last_name": "Johnson",
      "company": "Globex Inc"
    }
  ]
}
```

**`GET /campaigns/{campaign_id}/leads` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `offset` | integer | No | Pagination offset |
| `limit` | integer | No | Results per page (max 100) |

To filter by category, fetch the campaign's lead categories first (each has a numeric `category_id` and a display name) and filter/segment client-side or via the category-specific endpoints. The default category names are **Interested**, **Not Interested**, **Meeting Booked** (plus any user-created categories); these are customizable, so do not hardcode a fixed enum.

**Response**:
```json
[
  {
    "id": 67890,
    "email": "jane@acme.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "company": "Acme Corp",
    "lead_category_id": 1,
    "campaign_id": 12345,
    "custom_fields": {
      "title": "VP of Sales"
    },
    "activity": {
      "sent": 3,
      "opened": 2,
      "clicked": 1,
      "replied": 1
    }
  }
]
```

**Lead categories**: Leads are organized by **category** (referenced by `category_id`), not a fixed status enum. Default categories include **Interested**, **Not Interested**, and **Meeting Booked**; additional categories can be created in the app. Map names → IDs via the fetch-categories endpoint before filtering or updating.

---

### Sender Accounts (4 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/sender-accounts` | List all connected sender accounts with warmup status and limits. |
| POST | `/sender-accounts` | Connect a new sender account (SMTP, Gmail OAuth, Outlook OAuth). |
| GET | `/sender-accounts/{id}` | Get a single sender account with details. |
| DELETE | `/sender-accounts/{id}` | Remove a sender account. |

**`GET /sender-accounts` — Response**:
```json
[
  {
    "id": 101,
    "email": "jane@outbound.company.com",
    "type": "GMAIL_OAUTH",
    "daily_limit": 50,
    "warmup_enabled": true,
    "warmup_status": "ACTIVE",
    "warmup_reputation": 85,
    "is_active": true
  }
]
```

**`POST /sender-accounts` — Body**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Account type: `SMTP`, `GMAIL_OAUTH`, `OUTLOOK_OAUTH` |
| `email` | string | Yes | Sender email address |
| `smtp_host` | string | Conditional | SMTP host (required for SMTP type) |
| `smtp_port` | integer | Conditional | SMTP port (required for SMTP type) |
| `smtp_username` | string | Conditional | SMTP username (required for SMTP type) |
| `smtp_password` | string | Conditional | SMTP password (required for SMTP type) |
| `daily_limit` | integer | No | Max emails per day (default: 50) |
| `warmup_enabled` | boolean | No | Enable Ultra Premium Warmup (default: true) |

---

### Analytics (3 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/campaigns/{id}/statistics` | Campaign-level stats — sent, opens, clicks, replies, bounces. |
| GET | `/campaigns/{id}/analytics` | Detailed analytics with daily breakdowns. |
| GET | `/sender-accounts/{id}/warmup-stats` | Warmup progress and reputation score for a sender. |

**`GET /campaigns/{id}/statistics` — Response**:
```json
{
  "campaign_id": 12345,
  "total_leads": 500,
  "sent": 450,
  "unique_opened": 225,
  "unique_clicked": 40,
  "replied": 35,
  "bounced": 10,
  "unsubscribed": 5,
  "open_rate": 50.0,
  "click_rate": 8.9,
  "reply_rate": 7.8,
  "bounce_rate": 2.2
}
```

---

### Webhooks (campaign-scoped)

**Webhooks are configured per campaign**, not globally. Use the campaign webhook endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/campaigns/{campaign_id}/webhooks` | List all webhooks configured for a campaign. |
| POST | `/campaigns/{campaign_id}/webhooks` | Create or upsert a webhook for a campaign (save webhooks). |
| DELETE | `/campaigns/{campaign_id}/webhooks` | Delete a campaign webhook (by webhook id in the body/path). |

**`POST /campaigns/{campaign_id}/webhooks` — Body** (typical fields):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | A label for the webhook |
| `webhook_url` | string | Yes | The URL to receive webhook payloads |
| `event_types` | array | Yes | One or more event types to subscribe to (see below) |
| `categories` | array | No | For category-update events, the lead categories that should trigger it |

**Supported webhook event types** (exact identifiers, from the official API reference):

| Event | Description |
|---|---|
| `EMAIL_SENT` | An email was successfully sent to a lead |
| `FIRST_EMAIL_SENT` | Fires only when the initial sequence email is sent |
| `EMAIL_OPEN` | A lead opened your email (tracking pixel loaded) |
| `EMAIL_LINK_CLICK` | A lead clicked a tracked link |
| `EMAIL_REPLY` | A lead replied to your email |
| `EMAIL_BOUNCE` | An email bounced (delivery failed; payload includes bounce type/reason) |
| `LEAD_UNSUBSCRIBED` | A lead clicked the unsubscribe link |
| `LEAD_CATEGORY_UPDATED` | A lead's category changed |
| `CAMPAIGN_STATUS_CHANGED` | A campaign's status changed |
| `UNTRACKED_REPLIES` | An untracked reply was received |
| `MANUAL_STEP_REACHED` | A lead reached a manual step in the sequence |
| `EMAIL_ACCOUNT_DISCONNECTED` | A sending email account was disconnected |
| `LINKEDIN_DISCONNECTED` | A LinkedIn cookie became invalid |

> The older event names `LEAD_REPLIED`, `LEAD_INTERESTED`, `EMAIL_OPENED`, `EMAIL_CLICKED`, `EMAIL_BOUNCED` are **not** valid identifiers — use `EMAIL_REPLY`, `EMAIL_OPEN`, `EMAIL_LINK_CLICK`, `EMAIL_BOUNCE`. There is no dedicated "interested" event; interest is surfaced via `LEAD_CATEGORY_UPDATED` (filter on the Interested category).

**Webhook payload format** (illustrative; fields vary by event):
```json
{
  "event_type": "EMAIL_REPLY",
  "campaign_id": 12345,
  "lead_id": 67890,
  "to_email": "prospect@example.com",
  "sequence_number": 2,
  "time_replied": "2024-01-15T14:00:00Z",
  "reply": {
    "subject": "Re: quick question",
    "body": "Thanks for reaching out, I'd love to learn more..."
  }
}
```

**Webhook signature / verification**: Smartlead's help center references signing webhooks (an `X-Smartlead-Signature` HMAC-SHA256 header over the raw body, plus an `X-Request-Id` for idempotency), but this is **not confirmed in the current API reference** — treat the exact header name and algorithm as UNVERIFIED. As a baseline, serve your endpoint over HTTPS and validate a shared secret/token before acting on payloads. Confirm signature specifics in-app or with support before relying on them.

---

### Clients / Workspaces (Agency accounts) (4 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/clients` | List all client workspaces (agency/white-label accounts only). |
| POST | `/clients` | Create a new client workspace. |
| GET | `/clients/{id}` | Get client workspace details. |
| DELETE | `/clients/{id}` | Remove a client workspace. |

**`POST /clients` — Body**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Client/workspace name |
| `email` | string | No | Client contact email |

---

## Data Models

### Campaign

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique campaign ID |
| `name` | string | Campaign name |
| `status` | string | Current status: `DRAFT`, `ACTIVE`, `PAUSED`, `COMPLETED` |
| `created_at` | datetime | Creation timestamp (ISO 8601) |
| `client_id` | integer | Client/workspace ID (agency accounts) |
| `stats` | object | Aggregate stats — `sent`, `opened`, `clicked`, `replied`, `bounced` |

### Lead

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique lead ID |
| `email` | string | Lead's email address |
| `first_name` | string | Lead's first name |
| `last_name` | string | Lead's last name |
| `company` | string | Company name |
| `lead_category_id` | integer | The lead's category ID (customizable categories such as Interested / Not Interested / Meeting Booked — not a fixed status enum). |
| `campaign_id` | integer | Parent campaign ID |
| `custom_fields` | object | Custom merge field key-value pairs |
| `activity` | object | Activity stats — `sent`, `opened`, `clicked`, `replied` |

### Sender Account

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique sender account ID |
| `email` | string | Sender's email address |
| `type` | string | Account type: `SMTP`, `GMAIL_OAUTH`, `OUTLOOK_OAUTH` |
| `daily_limit` | integer | Maximum emails per day |
| `warmup_enabled` | boolean | Whether Ultra Premium Warmup is active |
| `warmup_status` | string | Warmup status: `ACTIVE`, `PAUSED`, `COMPLETED` |
| `warmup_reputation` | integer | Reputation score (0-100) |
| `is_active` | boolean | Whether the sender is active |

### Client / Workspace

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique client/workspace ID |
| `name` | string | Client name |
| `email` | string | Client contact email |
| `created_at` | datetime | Creation timestamp (ISO 8601) |

---

## Common Automation Patterns

**Campaign lifecycle**: Create a campaign via `POST /campaigns` → add leads via `POST /campaigns/{campaign_id}/leads` → connect sender accounts → enable warmup → activate campaign → monitor via `/campaigns/{id}/statistics` → manage leads via `POST /campaigns/{campaign_id}/leads/{lead_id}/category`.

**Lead import from CRM**: Query your CRM for new leads → build `lead_list` array with email, name, company, and custom fields → POST to `/campaigns/{id}/leads` → leads are automatically enrolled in the campaign sequence.

**Lead management**: Poll `/campaigns/{campaign_id}/leads` → review leads → set a lead's category via `POST /campaigns/{campaign_id}/leads/{lead_id}/category` (`category_id`) → sync Interested-category leads to your CRM for pipeline management.

**Webhook pipeline**: Create campaign webhooks (`POST /campaigns/{campaign_id}/webhooks`) for `EMAIL_REPLY` and `LEAD_CATEGORY_UPDATED` events → receive payloads at your endpoint → route to CRM, Slack, or other systems in real time. (Use `LEAD_CATEGORY_UPDATED` filtered on the Interested category instead of a non-existent "interested" event.)

**Multi-client management (agency)**: Create client workspaces via `POST /clients` → create campaigns scoped to client_id → connect client-specific sender accounts → run campaigns per workspace → aggregate reporting via per-campaign statistics.

**Sender warmup monitoring**: List sender accounts via `GET /sender-accounts` → check `warmup_reputation` scores → pause senders with reputation below 70 → resume campaigns only when warmup is healthy.

---

## Key Differences from Other Sales APIs

| Feature | Smartlead Behavior |
|---|---|
| HTTP methods | Standard REST — **GET** for reads, **POST** for creates/updates |
| Pagination | **Offset-based** (`offset` + `limit`), not cursor-based |
| Authentication | API key as **query parameter** (`api_key=`), not a header |
| Campaigns | "Campaign" includes email steps/sequences — not a separate concept |
| Lead statuses | Customizable **categories** (Interested, Not Interested, Meeting Booked…) referenced by `category_id` — not a fixed status enum and not pipeline stages |
| Rate limits | **60 requests/min per API key** by default (account- and client-level keys), adjustable on higher plans; short burst cap ~10 req/2s |
| Sender warmup | Built-in Ultra Premium Warmup with reputation scoring — no third-party needed |
| Agency/multi-client | Native client workspaces with `client_id` scoping on campaigns |
| Lead import | Accepts `custom_fields` object for arbitrary merge variables |

---

## Source URLs

- API Reference (developer docs): https://api.smartlead.ai/reference/authentication
- Webhook events reference: https://api.smartlead.ai/api-reference/webhooks/events
- Add leads to a campaign: https://api.smartlead.ai/reference/add-leads-to-a-campaign-by-id
- Update lead category: https://api.smartlead.ai/reference/update-a-leads-category-based-on-their-campaign
- Fetch campaign webhooks: https://api.smartlead.ai/reference/fetch-webhooks-by-campaign-id
- Full API documentation (help center): https://helpcenter.smartlead.ai/en/articles/125-full-api-documentation
- Client-level API keys & rate limit: https://helpcenter.smartlead.ai/en/articles/430-how-client-level-api-keys-work-in-smartlead
- Pricing: https://www.smartlead.ai/pricing
