### Mailshake REST API — Comprehensive Reference

**Base URL**: `https://api.mailshake.com/2017-04-01`
**Docs**: https://api-docs.mailshake.com/
**API version**: 2017-04-01

---

## Authentication

Two authentication methods are supported:

1. **Simple (API key)** — pass the API key as `apiKey` in the query string OR as a field in the JSON request body, OR via an HTTP Basic auth header.
2. **OAuth 2.0** — for third-party apps acting on behalf of other Mailshake teams (see the OAuth2 section below).

| Detail | Value |
|---|---|
| Parameter | `apiKey` (query string or JSON body field) |
| Header (Basic) | `Authorization: Basic <base64 of the api key>` — with curl, use `-u "YOUR_API_KEY:"` (trailing colon, empty password) |
| Where to find | Integrations > API in the Mailshake app |

**Example (JSON body)**:
```json
{
  "apiKey": "YOUR_API_KEY",
  "campaignID": 123
}
```

**Example (query string)**:
```
POST https://api.mailshake.com/2017-04-01/campaigns/list?apiKey=YOUR_API_KEY
```

**Example (HTTP Basic header via curl)**:
```
curl "https://api.mailshake.com/2017-04-01/campaigns/list" -u "YOUR_API_KEY:"
```

---

## Request & Response Format

### Requests

- **All requests use POST** — even read operations use POST with a JSON body (not GET with query params)
- **Content-Type**: `application/json`
- Parameters are passed in the JSON body alongside the `apiKey`

### Response Format

All successful responses return:
```json
{
  "results": { ... },
  "nextToken": "opaque_cursor_string"
}
```

For list endpoints, `results` is an array. For single-record endpoints, `results` is an object. When there are no more pages, `nextToken` is `null`.

### Error Responses

Errors return a JSON object with an `error` field:

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "campaignID is required"
  }
}
```

**Common error codes**:

| Code | Description |
|---|---|
| `invalid_api_key` | API key is missing or invalid |
| `not_found` | The requested resource does not exist |
| `invalid_parameter` | A required parameter is missing or has an invalid value |
| `limit_reached` | Hourly quota-unit limit exceeded. The error message includes a retry timestamp (e.g. "Please wait and try again after: 2017-08-21T15:16:15.207Z") |
| `exceeds_monthly_recipients` | The API key's monthly recipient-add cap is reached (resets on the 1st of each calendar month) |
| `internal_error` | Server-side error — retry with backoff |

---

## Pagination

**Type**: Cursor-based (`nextToken`)

| Parameter | Type | Description |
|---|---|---|
| `nextToken` | string | Opaque cursor returned from the previous response. Pass this to fetch the next page. |
| `perPage` | integer | Number of results per page. Default: 100. Max: 100. |

**How to paginate**:
1. Make the initial request without `nextToken`
2. If `nextToken` in the response is not `null`, pass it in your next request
3. Continue until `nextToken` is `null`

**Example**:
```json
{
  "apiKey": "YOUR_API_KEY",
  "campaignID": 123,
  "perPage": 50,
  "nextToken": "abc123cursor"
}
```

---

## Rate Limits

Mailshake does NOT use a simple requests-per-minute cap. It uses a **quota-units-per-hour** model where each operation costs a different number of "units," plus a separate **monthly recipient-add cap**.

| Detail | Value |
|---|---|
| Model | Quota units consumed per hour (per-operation cost varies) |
| Scope | Per API key, scaled by your plan and number of user seats (adding seats multiplies your base limits) |
| When exceeded | `limit_reached` error whose message includes the timestamp after which you may retry |
| Monthly cap | Separate cumulative cap on recipients added via the API per calendar month; exceeding it returns `exceeds_monthly_recipients` (resets on the 1st) |
| Where to check yours | Integrations > API in the Mailshake app shows your plan's quota-unit-per-hour and monthly-recipient limits |

**Per-operation quota-unit costs** (any operation not listed costs **1 unit**):

| Operation | Units |
|---|---|
| `campaigns/list` | 10 |
| `campaigns/pause` | 5 |
| `campaigns/unpause` | 25 |
| `campaigns/export` | 20 + N (N = campaigns) |
| `recipients/add` | 20 + N (N = recipients) |
| `recipients/list` | 10 |
| `recipients/pause` | 5 |
| `recipients/unpause` | 10 |
| `recipients/unsubscribe` | 2 |
| `leads/create` | 25 |
| `leads/close` | 5 |
| `leads/ignore` | 5 |
| `leads/reopen` | 5 |
| `push/create` | 100 |
| `activity/sent` | 1 |
| `activity/opens` | 2 |
| `activity/clicks` | 3 |
| `activity/replies` | 10 |
| `activity/created-leads` | 5 |
| `activity/lead-status-changes` | 5 |
| All other operations | 1 |

To raise your limits, add user seats — base API limits are multiplied per seat.

---

## All API Endpoints

All paths are relative to `https://api.mailshake.com/2017-04-01`. **All endpoints use POST.**

---

### Campaigns (7 endpoints)

| Endpoint | Description |
|---|---|
| `/campaigns/list` | List all campaigns with optional filters. Returns id, title, status, created, stats. |
| `/campaigns/get` | Get a single campaign by ID. Returns full campaign details including messages and stats. |
| `/campaigns/create` | Create a new campaign. The campaign must be finished in the web UI before it can send. Returns the new campaign object. |
| `/campaigns/pause` | Pause an active campaign by ID. |
| `/campaigns/unpause` | Resume a paused campaign by ID. The calendar reschedules, so sending may resume up to ~5 minutes later. |
| `/campaigns/export` | Start an asynchronous CSV export of campaign data (max 20 campaigns; types: `simple`, `show-each-message`, `unsubscribes`). Returns a `statusID`. |
| `/campaigns/exportStatus` | Check the progress of an export started by `/campaigns/export` (also accepts `/campaigns/export-status`). Pass the `statusID`. |

**`POST /campaigns/list` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `search` | string | No | Search campaigns by title |
| `teamFilter` | string | No | Filter scope: `my`, `team`, `everyone` |
| `nextToken` | string | No | Pagination cursor |
| `perPage` | integer | No | Results per page (default 100, max 100) |

**Response**:
```json
{
  "results": [
    {
      "id": 123,
      "title": "Q1 Outreach",
      "status": "active",
      "created": "2024-01-15T10:00:00Z",
      "sender": {
        "id": 1,
        "emailAddress": "sales@company.com",
        "fromName": "Jane Doe"
      },
      "stats": {
        "sent": 500,
        "opens": 250,
        "clicks": 45,
        "replies": 30,
        "bounces": 12
      }
    }
  ],
  "nextToken": null
}
```

**`POST /campaigns/get` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `campaignID` | integer | Yes | The campaign ID to retrieve |

**`POST /campaigns/create` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `title` | string | Yes | Campaign name |
| `senderID` | integer | No | ID of the sending account (from `/senders/list`). Uses default sender if omitted. |

**Campaign statuses**: `draft`, `active`, `paused`, `ended`

**`POST /campaigns/pause` and `/campaigns/unpause` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `campaignID` | integer | Yes | The campaign ID to pause or unpause |

---

### Recipients (7 endpoints)

| Endpoint | Description |
|---|---|
| `/recipients/list` | List recipients in a campaign. Filter by status and action. |
| `/recipients/get` | Get a single recipient. Look up by `recipientID`, or by `emailAddress` + `campaignID`. Returns full activity history. |
| `/recipients/add` | Add recipients to a campaign (asynchronous). Accepts `listOfEmails`, an `addresses` array, OR `csvData` (one is required). Max 5,000 recipients per campaign. |
| `/recipients/addStatus` | Check the status of a bulk add operation (also accepts `/recipients/add-status`). |
| `/recipients/pause` | Pause a specific recipient in a campaign. |
| `/recipients/unpause` | Resume a paused recipient. |
| `/recipients/unsubscribe` | Unsubscribe a recipient by email address. |

**`POST /recipients/list` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `campaignID` | integer | Yes | Campaign to list recipients from |
| `filter` | string | No | Filter by status: `active`, `paused`, `bounced`, `unsubscribed`, `completed` |
| `action` | string | No | Filter by action taken: `opened`, `clicked`, `replied`, `wasSent`, `bounced`, `paused`, `hasProblems` |
| `nextToken` | string | No | Pagination cursor |
| `perPage` | integer | No | Results per page (default 100, max 100) |

**Response**:
```json
{
  "results": [
    {
      "id": 456,
      "emailAddress": "prospect@example.com",
      "fullName": "John Smith",
      "fields": {
        "first": "John",
        "last": "Smith",
        "company": "Acme Corp"
      },
      "status": "active",
      "campaignID": 123
    }
  ],
  "nextToken": "next_page_cursor"
}
```

**`POST /recipients/get` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `recipientID` | integer | One required | The recipient ID to retrieve |
| `emailAddress` | string | One required | Look up by email instead — must be paired with `campaignID` |
| `campaignID` | integer | Conditional | Required when looking up by `emailAddress` |

> Either `recipientID`, or `emailAddress` + `campaignID`, is required.

**`POST /recipients/add` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `campaignID` | integer | Yes | Campaign to add recipients to |
| `addAsNewList` | boolean | No | If `true`, creates a new list for these recipients |
| `addresses` | array | One required | Array of recipient objects (see below) |
| `listOfEmails` | string | One required | Comma- or newline-separated list of email addresses (no merge fields) |
| `csvData` | object | One required | CSV payload — `csvRawData` (or `link`) plus column-name mappings |

> **One of `addresses`, `listOfEmails`, or `csvData` is required.** Adding is asynchronous — poll `/recipients/addStatus` with the returned status ID. A campaign holds a maximum of 5,000 recipients.

**Recipient object in `addresses` array**:

| Field | Type | Required | Description |
|---|---|---|---|
| `emailAddress` | string | Yes | Recipient's email address |
| `fullName` | string | No | Recipient's full name |
| `fields` | object | No | Merge field key-value pairs |

**Merge fields** map to template variables in your campaign messages. Common fields:

| Field Key | Description |
|---|---|
| `first` | First name |
| `last` | Last name |
| `company` | Company name |
| `title` | Job title |
| `phone` | Phone number |
| `city` | City |

**Example request**:
```json
{
  "apiKey": "YOUR_API_KEY",
  "campaignID": 123,
  "addAsNewList": false,
  "addresses": [
    {
      "emailAddress": "jane@acme.com",
      "fullName": "Jane Doe",
      "fields": {
        "first": "Jane",
        "last": "Doe",
        "company": "Acme Corp",
        "title": "VP of Sales"
      }
    },
    {
      "emailAddress": "bob@globex.com",
      "fullName": "Bob Johnson",
      "fields": {
        "first": "Bob",
        "last": "Johnson",
        "company": "Globex Inc"
      }
    }
  ]
}
```

**`POST /recipients/addStatus` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `statusID` | string | Yes | The status ID returned from a `/recipients/add` call |

**`POST /recipients/pause` and `/recipients/unpause` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `recipientID` | integer | Yes | The recipient ID to pause or unpause |

**`POST /recipients/unsubscribe` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `emailAddress` | string | Yes | Email address to unsubscribe (globally across all campaigns) |

**Recipient statuses**: `active`, `paused`, `bounced`, `unsubscribed`, `completed`

---

### Activity (7 endpoints)

| Endpoint | Description |
|---|---|
| `/activity/sent` | List sent emails with timestamps, subjects, and recipients. (Pagination max is 25 per page here, not 100.) |
| `/activity/opens` | List email opens with timestamp and recipient. Optional duplicate-exclusion. |
| `/activity/clicks` | List link clicks with timestamp, recipient, and clicked URL. Optional duplicate-exclusion and URL matching. |
| `/activity/replies` | List replies with timestamp, recipient, and body preview. Includes bounces, out-of-office, and unsubscribe replies; filter by `type`. |
| `/activity/created-leads` | List leads created by Lead Catcher (auto-generated or manual). |
| `/activity/lead-assignments` | List recently assigned leads. |
| `/activity/lead-status-changes` | List lead status changes (open, won/closed, lost, ignored). |

**Common parameters for all activity endpoints**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `campaignID` | integer | No | Filter activity to a specific campaign |
| `recipientID` | integer | No | Filter activity to a specific recipient |
| `nextToken` | string | No | Pagination cursor |
| `perPage` | integer | No | Results per page (default 100, max 100 — except `/activity/sent`, where the max is 25) |

**`POST /activity/sent` — Response**:
```json
{
  "results": [
    {
      "id": 789,
      "recipientID": 456,
      "campaignID": 123,
      "emailAddress": "prospect@example.com",
      "subject": "Quick question about Acme's growth plans",
      "sentAt": "2024-01-15T10:30:00Z",
      "messageType": "initial"
    }
  ],
  "nextToken": null
}
```

**`POST /activity/opens` — Response**:
```json
{
  "results": [
    {
      "recipientID": 456,
      "campaignID": 123,
      "emailAddress": "prospect@example.com",
      "openedAt": "2024-01-15T11:05:00Z",
      "device": "desktop"
    }
  ],
  "nextToken": null
}
```

**`POST /activity/clicks` — Response**:
```json
{
  "results": [
    {
      "recipientID": 456,
      "campaignID": 123,
      "emailAddress": "prospect@example.com",
      "clickedAt": "2024-01-15T11:10:00Z",
      "url": "https://company.com/pricing"
    }
  ],
  "nextToken": null
}
```

**`POST /activity/replies` — Response**:
```json
{
  "results": [
    {
      "recipientID": 456,
      "campaignID": 123,
      "emailAddress": "prospect@example.com",
      "repliedAt": "2024-01-15T14:00:00Z",
      "bodyPreview": "Thanks for reaching out, I'd love to learn more...",
      "sentiment": "positive"
    }
  ],
  "nextToken": null
}
```

Reply sentiment values: `positive`, `neutral`, `negative`, `unsubscribe`

**Bounces** are not a separate endpoint. They surface through `/activity/replies`, which returns bounces, out-of-office, and unsubscribe replies alongside normal replies — filter with the `type` parameter to isolate bounces. Bounce types are typically `hard` / `soft`.

---

### Leads — Lead Catcher (6 endpoints)

Lead Catcher automatically captures replies and creates leads for follow-up. Leads have their own lifecycle separate from the campaign.

| Endpoint | Description |
|---|---|
| `/leads/list` | List all leads captured by Lead Catcher. Filter by status, assignee, campaign. |
| `/leads/get` | Get a single lead. Look up by `leadID`, `recipientID`, or `emailAddress`. Returns full conversation thread, status, and assignment. |
| `/leads/create` | Create a lead from one or more `recipientIDs` or `emailAddresses`. |
| `/leads/close` | Close a lead. Accepts an optional `status` of `closed` (the default — equivalent to "Won") or `lost`. |
| `/leads/ignore` | Ignore a lead (mark as unpromising / remove from active queue). |
| `/leads/reopen` | Reopen a previously closed or ignored lead. |

> **There is no `markAsLost` endpoint.** To mark a lead lost, call `/leads/close` with `status: "lost"`.

**`POST /leads/list` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `status` | string | No | Filter by lead status: `open`, `closed` (= "Won"), `ignored`, `lost` |
| `assignedToEmailAddress` | string | No | Filter by assignee's email address |
| `campaignID` | integer | No | Filter by source campaign |
| `nextToken` | string | No | Pagination cursor |
| `perPage` | integer | No | Results per page (default 100, max 100) |

**Response**:
```json
{
  "results": [
    {
      "id": 321,
      "emailAddress": "prospect@example.com",
      "fullName": "John Smith",
      "status": "open",
      "assignedTo": {
        "emailAddress": "rep@company.com",
        "fullName": "Sales Rep"
      },
      "campaignID": 123,
      "createdAt": "2024-01-15T14:00:00Z",
      "conversation": [
        {
          "from": "sales@company.com",
          "to": "prospect@example.com",
          "subject": "Quick question",
          "body": "Hi John, I noticed...",
          "sentAt": "2024-01-15T10:30:00Z"
        },
        {
          "from": "prospect@example.com",
          "to": "sales@company.com",
          "subject": "Re: Quick question",
          "body": "Thanks for reaching out...",
          "sentAt": "2024-01-15T14:00:00Z"
        }
      ]
    }
  ],
  "nextToken": null
}
```

**`POST /leads/get` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `leadID` | integer | One required | The lead ID to retrieve |
| `recipientID` | integer | One required | Look up the lead by recipient instead |
| `emailAddress` | string | One required | Look up the lead by email instead |

**`POST /leads/close` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `leadID` | integer | Yes | The lead ID to update |
| `status` | string | No | `closed` (default, = "Won") or `lost` |

**`POST /leads/ignore` and `/leads/reopen` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `leadID` | integer | Yes | The lead ID to update |

**Lead statuses**: `open`, `closed` (= "Won"), `ignored`, `lost`

---

### Team (1 endpoint)

| Endpoint | Description |
|---|---|
| `/team/list-members` | List all team members with roles and permissions. |

**`POST /team/list-members` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |

**Response**:
```json
{
  "results": [
    {
      "id": 1,
      "emailAddress": "admin@company.com",
      "fullName": "Jane Admin",
      "role": "admin",
      "isActive": true
    }
  ]
}
```

---

### Senders (1 endpoint)

| Endpoint | Description |
|---|---|
| `/senders/list` | List all connected sending accounts with daily limits and usage. |

**`POST /senders/list` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |

**Response**:
```json
{
  "results": [
    {
      "id": 1,
      "emailAddress": "sales@company.com",
      "fromName": "Jane Doe",
      "isDefault": true,
      "dailyLimit": 500,
      "isPaused": false
    }
  ]
}
```

---

### Push / Webhooks (2 endpoints)

| Endpoint | Description |
|---|---|
| `/push/create` | Create a webhook subscription for a specific event. |
| `/push/delete` | Delete a webhook subscription by ID. |

**`POST /push/create` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `targetUrl` | string | Yes | The URL to receive webhook notifications |
| `event` | string | Yes | The event to subscribe to (see supported events below) |

> Optional filters (e.g. by campaign, or a URL match for `Clicked`, or duplicate-exclusion for `Opened`) can be attached on subscription. `/push/create` costs **100 quota units**.

**`POST /push/delete` — Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | Your API key |
| `targetUrl` | string | Yes | The `targetUrl` of the subscription to delete |

**Supported webhook events** (exact names):

| Event | Description |
|---|---|
| `Clicked` | Recipient clicked a tracked link |
| `Opened` | Recipient opened an email |
| `Replied` | Recipient replied to an email |
| `MessageSent` | A campaign email was sent to a recipient |
| `LeadCreated` | A new lead was created (Lead Catcher) |
| `LeadStatusChanged` | A lead's status changed (open → closed/lost/ignored, etc.) |

> There is no separate `Bounce` or `Unsubscribe` push event. Bounces and unsubscribe replies surface through `/activity/replies` (filter by `type`).

**Webhook payload format** — Mailshake POSTs a **minimal notification containing only a `resource_url`**. The payload does NOT contain the full event data; your handler must make an authenticated GET/POST to the `resource_url` to fetch the actual record.

```json
{
  "resource_url": "https://api.mailshake.com/2017-04-01/..."
}
```

**Handler requirements**:
- Respond **HTTP 200** to acknowledge successful handling. Mailshake retries if it does not receive a 200.
- Respond **HTTP 410** to unsubscribe (tells Mailshake to stop sending to this `targetUrl`).
- **No HMAC signing.** Webhooks are not signed — security relies on the `targetUrl` being secret/unguessable (embed a secret token in the URL path or query and validate it on receipt).
- After receiving the notification, fetch `resource_url` with your API credentials to get the full record.

---

### OAuth2

OAuth 2.0 (authorization-code flow) is for third-party apps acting on behalf of other Mailshake teams.

| URL | Purpose |
|---|---|
| `https://app.mailshake.com/oauth/` | Authorization URL — redirect users here to grant access. |
| `https://api.mailshake.com/2017-04-01/token` | Token endpoint — exchange the auth code for tokens, and refresh tokens (same URL). |

**Scopes** (comma-delimited): `campaign-read` (read access to all operations), `campaign-write` (write access to all operations).

**OAuth2 Authorization Code Flow**:

1. **Redirect** the user to the authorization URL:
```
https://app.mailshake.com/oauth/?client_id=YOUR_ID&response_type=code&redirect_uri=YOUR_URI&scope=campaign-read,campaign-write
```

2. **User approves** and is redirected back to your `redirect_uri` with a `code` parameter.

3. **Exchange** the code for tokens:
```json
POST https://api.mailshake.com/2017-04-01/token
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "code": "AUTHORIZATION_CODE",
  "grant_type": "authorization_code",
  "redirect_uri": "YOUR_URI"
}
```

4. **Token response** includes `access_token` and `refresh_token`.

5. **Refresh** when the access token expires — POST to the **same** `/token` URL with `grant_type=refresh_token`:
```json
POST https://api.mailshake.com/2017-04-01/token
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "grant_type": "refresh_token",
  "redirect_uri": "YOUR_URI"
}
```

---

## Data Models

### Campaign

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique campaign ID |
| `title` | string | Campaign name/title |
| `status` | string | Current status: `draft`, `active`, `paused`, `ended` |
| `created` | datetime | Creation timestamp (ISO 8601) |
| `sender` | object | Sending account — contains `id`, `emailAddress`, `fromName` |
| `messages` | array | Campaign messages (initial email + follow-ups). Each is a Message object. |
| `stats` | object | Aggregate stats — `sent`, `opens`, `clicks`, `replies`, `bounces` |

### Recipient

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique recipient ID |
| `emailAddress` | string | Recipient's email address |
| `fullName` | string | Recipient's full name |
| `fields` | object | Merge field key-value pairs (e.g., `first`, `last`, `company`, `title`) |
| `status` | string | Current status: `active`, `paused`, `bounced`, `unsubscribed`, `completed` |
| `campaignID` | integer | ID of the parent campaign |

### Lead

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique lead ID |
| `emailAddress` | string | Lead's email address |
| `fullName` | string | Lead's full name |
| `status` | string | Current status: `open`, `closed` (= "Won"), `ignored`, `lost` |
| `assignedTo` | object | Assigned team member — contains `emailAddress`, `fullName` |
| `campaignID` | integer | ID of the source campaign |
| `conversation` | array | Full email thread (array of message objects with `from`, `to`, `subject`, `body`, `sentAt`) |
| `createdAt` | datetime | When the lead was captured (ISO 8601) |

### Message (campaign step)

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique message ID |
| `type` | string | Message type: `initial`, `follow-up`, `drip`, `on-click` |
| `subject` | string | Email subject line (only on initial; follow-ups use the same thread) |
| `body` | string | Email body content (HTML) |
| `delayDays` | integer | Number of days after the previous message before this one sends |
| `isPaused` | boolean | Whether this message step is currently paused |

### Sender

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique sender ID |
| `emailAddress` | string | Sender's email address |
| `fromName` | string | Display name used in outgoing emails |
| `isDefault` | boolean | Whether this is the default sending account |
| `dailyLimit` | integer | Maximum emails per day for this sender |
| `isPaused` | boolean | Whether sending is paused for this account |

### Team Member

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique team member ID |
| `emailAddress` | string | Team member's email address |
| `fullName` | string | Team member's full name |
| `role` | string | Role in the team (e.g., `admin`, `member`) |
| `isActive` | boolean | Whether the team member account is active |

---

## Common Automation Patterns

**Campaign lifecycle**: Create a campaign via `/campaigns/create` -> add recipients via `/recipients/add` -> check add status via `/recipients/addStatus` -> unpause with `/campaigns/unpause` -> monitor via `/activity/*` endpoints -> manage leads in Lead Catcher via `/leads/*`.

**Recipient import**: Build an array of recipient objects with `emailAddress` (required) and merge fields -> POST to `/recipients/add` with the campaign ID -> poll `/recipients/addStatus` with the returned status ID to confirm completion.

**Lead management**: Poll `/leads/list` filtered by `status=open` -> review each lead -> take action with `/leads/close` (default `status=closed` for won, or `status=lost`), or `/leads/ignore` (not relevant) -> sync lead data to your CRM.

**Webhook pipeline**: Create push subscriptions for `Replied` and `LeadCreated` events via `/push/create` -> Mailshake POSTs a `{ "resource_url": ... }` notification to your endpoint -> fetch the full record from `resource_url` with your API credentials -> respond HTTP 200 -> route to CRM, Slack, or other systems in real time.

**Analytics and reporting**: Poll `/activity/sent`, `/activity/opens`, `/activity/clicks`, and `/activity/replies` on a schedule -> aggregate metrics per campaign -> build dashboards or sync to your BI tool.

**Multi-campaign coordination**: Use `/campaigns/list` with `teamFilter=everyone` to audit all active campaigns -> pause overlapping campaigns with `/campaigns/pause` -> manage send volume across the team.

**Recipient hygiene**: Monitor `/activity/replies` (filter by `type` to find bounces) for hard bounces -> unsubscribe bad addresses via `/recipients/unsubscribe` -> maintain sender reputation.

---

## Key Differences from Other Sales APIs

| Feature | Mailshake Behavior |
|---|---|
| All requests | **POST only** — even reads/lists use POST, not GET |
| Pagination | **Cursor-based** (`nextToken`), not page-number-based |
| Authentication | API key as a **parameter** (query string or JSON body) OR via `Authorization: Basic <base64 apiKey>` header; OAuth 2.0 for third-party apps |
| Campaigns | "Campaign" is what other tools call a "sequence" or "cadence" |
| Lead Catcher | Built-in lead management — replies automatically create leads with status tracking |
| Rate limits | **Quota-units-per-hour** model (per-operation cost), scaled per plan/seat — NOT a flat requests/minute cap. Separate monthly recipient-add cap. |
| Webhooks | Send a minimal `{ "resource_url": ... }` notification (fetch full record yourself); no HMAC signing; respond 200 to ack, 410 to unsubscribe |
| Recipient fields | Only `emailAddress` is required for import; all other fields are optional merge fields |
| Response envelope | Consistent `{ "results": ..., "nextToken": ... }` wrapper on all endpoints |
| Bulk add | Recipients are added asynchronously — use `/recipients/addStatus` to check completion |

---

## Source URLs

- API Documentation: https://api-docs.mailshake.com/
- API limits (help): https://docs.mailshake.com/article/260-api-limits
- Pricing: https://mailshake.com/pricing/
- Webhook/Push events: https://api-docs.mailshake.com/#Push
