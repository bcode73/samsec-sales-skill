# GetResponse API v3 Reference

## Overview

| Property | Value |
|---|---|
| **Base URL (retail)** | `https://api.getresponse.com/v3` |
| **Base URL (MAX)** | `https://api3.getresponse360.com/v3` or `https://api3.getresponse360.pl/v3` |
| **Auth** | `X-Auth-Token: api-key {your-api-key}` header |
| **OAuth 2.0** | Supported — authorization code grant for third-party apps |
| **Content-Type** | `application/json` (all POST requests) |
| **Rate limits** | 30,000 calls / 10 min, 80 calls/sec, max 10 simultaneous requests |
| **Key expiry** | API keys expire after 90 days of inactivity |
| **MAX header** | MAX users must include `X-Domain: {client-domain}` header (domain only, no protocol) |
| **Multi-account header** | `X-Parent-Login` — for users in multiple parent accounts, restricts the request to a specific account |

## Authentication

### API Key (simplest)
```
GET /v3/contacts
X-Auth-Token: api-key abc123def456
```

### OAuth 2.0 (third-party apps)
1. Register app in GetResponse Developer Portal
2. Redirect user to `https://app.getresponse.com/oauth2_authorize.html?response_type=code&client_id={id}&state={state}`
3. Exchange code for token at `POST https://api.getresponse.com/v3/token`
4. Use `Authorization: Bearer {access_token}` header

## HTTP Methods

| Method | Usage |
|---|---|
| **GET** | Retrieve resources — idempotent, no body |
| **POST** | Create new resources or update existing |
| **DELETE** | Remove resources — no body or query string |

**Note**: GetResponse uses POST for both create and update (no PUT/PATCH).

## Pagination

Collections support pagination via query parameters:
- `page` — page number (1-based)
- `perPage` — items per page (max 1000, default 100)
- Response headers include total count: `TotalCount`, `TotalPages`, `CurrentPage`

## Error Handling

| Status | Meaning |
|---|---|
| 200 | Success |
| 202 | Accepted (async processing) |
| 400 | Validation error — response body details the issues |
| 401 | Unauthorized — invalid or expired API key |
| 404 | Resource not found |
| 409 | Conflict — duplicate resource |
| 429 | Rate limit exceeded |
| 500 | Server error |

Error response format:
```json
{
  "httpStatus": 400,
  "code": 1000,
  "codeDescription": "General error of validation process",
  "message": "Custom field invalid",
  "moreInfo": "https://apidocs.getresponse.com/v3/errors/1000",
  "context": { "fieldName": ["Invalid value"] }
}
```

---

## Endpoints by Resource

### Campaigns (Mailing Lists)

**Important**: In GetResponse, "campaign" = mailing list, NOT an email send.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/campaigns` | List all campaigns (lists) |
| GET | `/v3/campaigns/{campaignId}` | Get a campaign |
| POST | `/v3/campaigns` | Create a campaign (list) |
| POST | `/v3/campaigns/{campaignId}` | Update a campaign |
| DELETE | `/v3/campaigns/{campaignId}` | Delete a campaign |
| GET | `/v3/campaigns/{campaignId}/contacts` | Get contacts in a campaign |
| GET | `/v3/campaigns/{campaignId}/blacklists` | Get campaign blacklist |
| POST | `/v3/campaigns/{campaignId}/blacklists` | Add to campaign blacklist |

**Create campaign example:**
```json
POST /v3/campaigns
{
  "name": "my_list",
  "confirmation": {
    "fromField": { "fromFieldId": "abc123" },
    "replyTo": { "fromFieldId": "abc123" },
    "redirectType": "hosted"
  },
  "languageCode": "EN"
}
```

### Contacts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/contacts` | List contacts (supports query filters) |
| GET | `/v3/contacts/{contactId}` | Get a single contact |
| POST | `/v3/contacts` | Create a contact |
| POST | `/v3/contacts/{contactId}` | Update a contact |
| DELETE | `/v3/contacts/{contactId}` | Delete a contact |
| GET | `/v3/contacts/{contactId}/activities` | Get contact activities |
| GET | `/v3/contacts/{contactId}/tags` | Get contact tags |
| POST | `/v3/contacts/{contactId}/tags` | Add tag to contact |
| DELETE | `/v3/contacts/{contactId}/tags/{tagId}` | Remove tag from contact |

**Create contact example:**
```json
POST /v3/contacts
{
  "email": "user@example.com",
  "name": "John Doe",
  "campaign": { "campaignId": "abc123" },
  "dayOfCycle": 0,
  "tags": [
    { "tagId": "tag123" }
  ],
  "customFieldValues": [
    {
      "customFieldId": "field123",
      "value": ["Developer"]
    }
  ]
}
```

**Query filters for GET /v3/contacts:**
- `query[email]` — filter by email
- `query[name]` — filter by name
- `query[campaignId]` — filter by campaign (list)
- `query[origin]` — filter by source (import, api, webform, etc.)
- `query[createdOn][from]` / `query[createdOn][to]` — date range
- `sort[fieldName]` — sort by field (email, name, createdOn)
- `fields` — select specific fields to return

### Batch Contacts

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v3/contacts/batch` | Batch create/update contacts (async) |

Batch endpoint accepts up to 100 contacts per request and processes asynchronously.

### Search Contacts (Segments)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/search-contacts` | List saved segments |
| GET | `/v3/search-contacts/{searchContactId}` | Get segment details |
| POST | `/v3/search-contacts` | Create a segment |
| POST | `/v3/search-contacts/{searchContactId}` | Update a segment |
| DELETE | `/v3/search-contacts/{searchContactId}` | Delete a segment |
| GET | `/v3/search-contacts/{searchContactId}/contacts` | Get contacts in a segment |

**Note**: "search-contacts" in the API = "segments" in the GetResponse UI.

### Tags

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/tags` | List all tags |
| GET | `/v3/tags/{tagId}` | Get a tag |
| POST | `/v3/tags` | Create a tag |
| POST | `/v3/tags/{tagId}` | Update a tag |
| DELETE | `/v3/tags/{tagId}` | Delete a tag |

### Custom Fields

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/custom-fields` | List custom fields |
| GET | `/v3/custom-fields/{customFieldId}` | Get a custom field |
| POST | `/v3/custom-fields` | Create a custom field |
| POST | `/v3/custom-fields/{customFieldId}` | Update a custom field |
| DELETE | `/v3/custom-fields/{customFieldId}` | Delete a custom field |

### Newsletters (Email Sends)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/newsletters` | List newsletters |
| GET | `/v3/newsletters/{newsletterId}` | Get a newsletter |
| POST | `/v3/newsletters` | Create and schedule a newsletter |
| DELETE | `/v3/newsletters/{newsletterId}` | Cancel a scheduled newsletter |
| GET | `/v3/newsletters/{newsletterId}/statistics` | Get newsletter statistics |

**Create newsletter example:**
```json
POST /v3/newsletters
{
  "subject": "Welcome to our newsletter",
  "name": "March Newsletter",
  "campaign": { "campaignId": "abc123" },
  "sendOn": "2026-04-15T10:00:00+0000",
  "content": {
    "html": "<html><body>Hello {{CONTACT \"subscriber_first_name\"}}!</body></html>",
    "plain": "Hello!"
  },
  "flags": ["openrate", "clicktrack"]
}
```

### Autoresponders

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/autoresponders` | List autoresponders |
| GET | `/v3/autoresponders/{autoresponderId}` | Get an autoresponder |
| POST | `/v3/autoresponders` | Create an autoresponder |
| POST | `/v3/autoresponders/{autoresponderId}` | Update an autoresponder |
| DELETE | `/v3/autoresponders/{autoresponderId}` | Delete an autoresponder |
| GET | `/v3/autoresponders/{autoresponderId}/statistics` | Get autoresponder statistics |

**Create autoresponder example:**
```json
POST /v3/autoresponders
{
  "name": "Day 1 Welcome",
  "subject": "Welcome aboard!",
  "campaign": { "campaignId": "abc123" },
  "triggerSettings": {
    "dayOfCycle": 0,
    "frequency": "once",
    "selectedDays": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "selectedCampaigns": []
  },
  "content": {
    "html": "<html><body>Welcome!</body></html>"
  },
  "flags": ["openrate", "clicktrack"]
}
```

### From Fields (Sender Addresses)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/from-fields` | List sender addresses |
| GET | `/v3/from-fields/{fromFieldId}` | Get a sender address |
| POST | `/v3/from-fields` | Create a sender address |
| DELETE | `/v3/from-fields/{fromFieldId}` | Delete a sender address |

### Landing Pages

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/landing-pages` | List landing pages |
| GET | `/v3/landing-pages/{landingPageId}` | Get a landing page |

### Webinars

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/webinars` | List webinars |
| GET | `/v3/webinars/{webinarId}` | Get a webinar |

### Forms

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/forms` | List signup forms |
| GET | `/v3/forms/{formId}` | Get a form |

### Statistics

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/statistics/sms` | SMS sending statistics |
| POST | `/v3/statistics/emails` | Email statistics (with date range filters) |

### Accounts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/accounts` | Get account info (plan, limits, features) |
| POST | `/v3/accounts` | Update account info |
| GET | `/v3/accounts/billing` | Get billing info |

### Shops (E-commerce)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/shops` | List shops |
| POST | `/v3/shops` | Create a shop |
| GET | `/v3/shops/{shopId}/products` | List products |
| POST | `/v3/shops/{shopId}/products` | Create a product |
| GET | `/v3/shops/{shopId}/orders` | List orders |
| POST | `/v3/shops/{shopId}/orders` | Create an order |
| GET | `/v3/shops/{shopId}/carts` | List carts |
| POST | `/v3/shops/{shopId}/carts` | Create a cart |

E-commerce endpoints enable abandoned cart tracking, product recommendations, and revenue attribution.

### Transactional Email (MAX only)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v3/transactional-emails` | Send a transactional email |
| GET | `/v3/transactional-emails` | List transactional emails |

**Note**: Transactional email API is only available on MAX/Enterprise plans.

---

## Real-time notifications: Callbacks vs Webhooks

GetResponse has **two distinct** real-time notification mechanisms. They are not the same surface — use the one that matches your needs.

### Callbacks (legacy URL action callbacks)

Per-action callback URLs managed at the account level. Managed via API **GET / POST / DELETE `/v3/accounts/callbacks`** (NOT `/v3/callbacks`) or in the UI.

| Action | Trigger |
|---|---|
| `subscribe` | Contact subscribes to a list |
| `open` | Contact opens an email |
| `click` | Contact clicks a link |
| `goal` | Contact reaches a conversion goal |
| `survey` | Contact responds to a survey |
| `unsubscribe` | Contact unsubscribes |

Callbacks deliver the event as a query string (e.g. `action=open&ACCOUNT_ID=A1&account_login=myaccount&CAMPAIGN_ID=C1&campaign_name=mycampaign&MESSAGE_ID=M1`), not a JSON body.

### Webhooks (current event-payload feature)

Configured in the GetResponse UI by selecting an event type and providing an HTTPS webhook URL (valid SSL required). The endpoint must respond within the timeout and return a 2xx status. Multiple events can be batched into one request as an array of objects.

Webhook event types (verbatim from the official payloads docs):

| Event type | Meaning |
|---|---|
| `contact_added` | Contact subscribed |
| `contact_opened_message` | Message opened |
| `contact_clicked_message_link` | Email link clicked |
| `contact_clicked_sms_link` | SMS link clicked |
| `contact_copied` | Contact copied to another list |
| `contact_moved` | Contact moved between lists |
| `contact_removed_link` | Contact unsubscribed |
| `contact_removed_bounce` | Bounced contact removed |
| `contact_custom_field_changed` | Custom field value changed |
| `contact_email_changed` | Contact email address changed |
| `contacts_import_finished` | Contact import finished |
| `contact_rejected` | Contact rejected |
| `custom_reports_file_status_changed` | Custom report file status changed |

**Payload shape** — JSON with top-level fields `type`, `account` (containing `accountId`), and `event` (containing `occurredAt`, an ISO8601/RFC3339 timestamp); event-specific fields vary by type.

**Webhook authenticity**: GetResponse does **not** sign webhooks with HMAC or any cryptographic signature. The documented verification method is to append your own secret query-string parameter to the webhook URL and check it on receipt. Do not assume HMAC verification exists.

---

## SDKs and Libraries

GetResponse provides API client libraries:
- **PHP**: Official PHP SDK
- **Python**: Community libraries available
- **Node.js**: Community libraries available
- **Ruby**: Community libraries available

For all other languages, use the REST API directly with any HTTP client.

---

## Key Gotchas

1. **"Campaign" = mailing list** — `POST /v3/campaigns` creates a list, not an email send. Use `POST /v3/newsletters` to send email.
2. **POST for updates** — GetResponse uses POST (not PUT/PATCH) to update existing resources.
3. **API keys expire** — Unused keys are deactivated after 90 days of no API calls.
4. **MAX requires X-Domain header** — All MAX/Enterprise API calls must include the `X-Domain` header.
5. **Rate limits are per-account** — 30K calls/10 min is shared across all API keys on the account.
6. **Batch contacts are async** — `POST /v3/contacts/batch` returns 202 and processes in the background.
7. **Search-contacts = segments** — The API uses "search-contacts" where the UI shows "segments."
8. **Callbacks live at `/v3/accounts/callbacks`** — not `/v3/callbacks`. Legacy callbacks send query-string payloads; the newer Webhooks feature sends JSON event payloads but is UI-configured.
9. **No webhook signing** — GetResponse does not HMAC-sign webhooks/callbacks. Verify authenticity with a secret query-string parameter you add to the URL, and validate the payload against the API.

---

*API reference is best-effort from research — some endpoints may have additional parameters not documented here. Refer to the official documentation at https://apidocs.getresponse.com/v3 for complete details.*
