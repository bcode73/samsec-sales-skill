<!-- Source: official OpenAPI spec (v1.6) at https://github.com/getaccept/openapi/blob/master/openapi.json — re-verified 2026-06-13. Base URL https://api.getaccept.com/v1 -->

# GetAccept API Reference

## Base URL

`https://api.getaccept.com/v1`

All requests over SSL. All request and response bodies encoded in JSON.

## Authentication

The API supports two auth schemes (per the official OpenAPI spec):

1. **Token (Bearer JWT)** — recommended for server-based access or where OAuth is not
   suitable. Request a token from `/auth` using an administrator's login credentials.
2. **OAuth2 (authorization code flow)** — for acting on behalf of a logged-in user.
   - Authorization URL: `https://app.getaccept.com/oauth2/authorize`
   - Token URL: `https://app.getaccept.com/oauth2/token`
   - Refresh URL: `https://app.getaccept.com/oauth2/token`
   - Scope: `basic`

### Token auth via `/auth`

```bash
curl -X POST https://api.getaccept.com/v1/auth \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password",
    "client_id": "optional-client-id",
    "entity_id": "optional-entity-id"
  }'
```

Only `email` and `password` are required. `client_id` is the id of your app if the API
team issued one; `entity_id` selects which entity to use when a user has multiple (omit
for the default entity).

Response:
```json
{
  "access_token": "eyJ...",
  "expires_in": 86400
}
```

`expires_in` is the number of seconds until the token expires. Use the token as:
`Authorization: Bearer {access_token}`. Refresh before expiry with `GET /refresh`
(or `GET /refresh/{entityId}`); revoke early with `GET /revoke`.

**Plan gate**: API read access is included with Enterprise; API write access is an
Enterprise add-on. Not available on eSign or Professional.

## Endpoints

### Authentication
| Method | Path | Description |
|---|---|---|
| POST | `/auth` | Token-based authentication |
| GET | `/refresh` | Refresh an access token before it expires |
| GET | `/refresh/{entityId}` | Refresh token scoped to a specific entity |
| GET | `/revoke` | Revoke an access token before it expires |

### Attachments
| Method | Path | Description |
|---|---|---|
| GET | `/attachments` | List available attachments |

### Communication Templates
| Method | Path | Description |
|---|---|---|
| GET | `/communication-templates` | List templates (pagination, status filtering) |
| POST | `/communication-templates` | Create template (language support) |
| GET | `/communication-templates/{id}` | Get specific template |
| PUT | `/communication-templates/{id}` | Update template |

### Contacts
| Method | Path | Description |
|---|---|---|
| GET | `/contacts` | List contacts (filtering, sorting, search) |
| POST | `/contacts` | Create contact |
| DELETE | `/contacts/{id}` | Delete contact (restricted if linked to active/signed docs) |

### Custom Data
| Method | Path | Description |
|---|---|---|
| GET | `/custom-data/entity` | Get entity custom data configuration |
| POST | `/custom-data/entity` | Add custom property (string, number, boolean) |
| DELETE | `/custom-data/entity/{key}` | Remove custom property |

### Documents
| Method | Path | Description |
|---|---|---|
| GET | `/documents` | List documents (filter by status: draft, sent, viewed, reviewed, signed, rejected, recalled) |
| POST | `/documents` | Create and send document with recipients, attachments, pricing tables |
| GET | `/documents/{id}` | Get document details (optional: attachments, pages, statistics) |
| PUT | `/documents/{id}` | Update document (tags, value, dates, external ID) |
| DELETE | `/documents/{id}` | Delete document |
| GET | `/documents/external/{externalId}` | Get document by external identifier |

### Document Sub-resources
| Method | Path | Description |
|---|---|---|
| GET | `/documents/{id}/attachments` | List document attachments |
| POST | `/documents/{id}/attachments/{attachId}/upload` | Upload file to attachment |
| GET | `/documents/{id}/comments` | Get chat comments |
| POST | `/documents/{id}/comments` | Add comment (optional position data) |
| GET | `/documents/{id}/custom-data` | List custom properties (pagination) |
| POST | `/documents/{id}/custom-data` | Add property to document |
| GET | `/documents/{id}/custom-data/{cdId}` | Get specific property |
| PUT | `/documents/{id}/custom-data/{cdId}` | Update property value |
| DELETE | `/documents/{id}/custom-data/{cdId}` | Delete property |
| GET | `/documents/{id}/download` | Download as PDF, base64, or URL (10-min access window) |
| GET | `/documents/{id}/events` | Get activity timeline |
| GET | `/documents/{id}/log` | Get document log |
| POST | `/documents/{id}/expiration` | Update expiration (optional recipient notification) |
| GET | `/documents/{id}/fields` | Extract form fields (optional resolution) |
| POST | `/documents/{id}/fields` | Add form fields |
| PUT | `/documents/{id}/fields` | Update form fields |
| POST | `/documents/{id}/forward` | Forward a document |
| GET | `/documents/{id}/pages` | List document pages |
| POST | `/documents/{id}/preview` | Generate a preview |
| GET | `/documents/{id}/pricing-tables` | Get pricing tables |
| PUT | `/documents/{id}/pricing-tables` | Update pricing tables |
| GET | `/documents/{id}/recipients` | List recipients |
| DELETE | `/documents/{id}/recipients/{recId}` | Remove a recipient |
| POST | `/documents/{id}/reminders` | Send a manual reminder |
| POST | `/documents/{id}/revisions` | Create a document revision |
| POST | `/documents/{id}/seal` | Apply company seal |
| POST | `/documents/{id}/send` | Send an existing draft document (only when `document_status = draft`) |
| GET | `/documents/{id}/status` | Get current document status |

### Templates
| Method | Path | Description |
|---|---|---|
| GET | `/templates` | List templates |
| GET | `/templates/{id}/custom-images` | List custom images |
| GET | `/templates/{id}/fields` | List template fields |
| GET | `/templates/{id}/fields_roles` | List field roles |
| GET | `/templates/{id}/pricing-tables` | List template pricing tables |
| GET | `/templates/{id}/roles` | List template roles |

### Email Templates
| Method | Path | Description |
|---|---|---|
| GET | `/email/templates` | List email templates |
| POST | `/email/templates` | Create email template |
| GET | `/email/templates/{id}` | Get email template |
| PUT | `/email/templates/{id}` | Update email template |

### Users, Teams, Folders & Notifications
| Method | Path | Description |
|---|---|---|
| GET | `/users` | List users |
| POST | `/users` | Create user |
| GET | `/users/{id}` | Get user |
| DELETE | `/users/{id}` | Delete user |
| GET | `/users/{id}/statistics` | Get user statistics |
| GET | `/teams` | List teams |
| GET | `/folders` | List folders |
| GET | `/folders/{id}` | Get folder |
| GET | `/notifications` | List notifications |

### Uploads & Video
| Method | Path | Description |
|---|---|---|
| POST | `/upload` | Upload a file |
| POST | `/upload/archive` | Upload an archive |
| POST | `/upload/attachment` | Upload an attachment |
| POST | `/upload/video` | Upload a video |
| GET | `/videos` | List videos |
| GET | `/videos/{id}` | Get video |
| GET | `/video/job/{id}` | Get video processing job status |

## Pagination

List endpoints use `offset` + `limit` query parameters (per the official OpenAPI spec).
- `offset` — start the list from record X
- `limit` — number of records to return

The documents list also supports `filter` (status), `sort_by`, `sort_order`,
`showteam`, `showall`, and `external_id` query parameters.

## Rate Limits

A numeric limit is not published, but rate-limit state is exposed via response headers
(per the official OpenAPI spec):
- `X-Rate-Limit-Limit` — allowed requests in the current period
- `X-Rate-Limit-Remaining` — remaining requests in the current period
- `X-Rate-Limit-Reset` — seconds left in the current period

Read these headers and back off when `X-Rate-Limit-Remaining` approaches 0.

## Error Responses

Standard HTTP status codes. Error body format (per the official `Error` schema):
```json
{
  "error": "error_type",
  "description": "Human-readable description",
  "status": 400
}
```

## Webhooks (native subscriptions)

GetAccept has a **native webhook API** (REST hooks) via the `/subscriptions` resource —
you do NOT need Zapier or Make for event-driven workflows.

| Method | Path | Description |
|---|---|---|
| GET | `/subscriptions` | List subscriptions for the current entity |
| POST | `/subscriptions` | Create a subscription (subscribe to a document event) |
| GET | `/subscriptions/{id}` | Get subscription details |
| DELETE | `/subscriptions/{id}` | Delete a subscription |
| GET | `/subscriptions/events` | List available subscription events |
| GET | `/subscriptions/errors` | Get the last errors for active subscriptions |
| POST | `/subscriptions/test` | Simulate/test a subscription (webhook) event |
| POST | `/subscriptions/events/signed` | Inbound event endpoint (signed) |
| POST | `/subscriptions/events/reviewed` | Inbound event endpoint (reviewed) |
| POST | `/subscriptions/events/rejected` | Inbound event endpoint (rejected) |

### Create subscription request body
Required: `event`, `target_url`. Optional: `host`, `global` (catch events for all entity
users, default `true`), `notification_email` (notified if delivery fails), `payload`
(extra data posted with the event). The create response is wrapped in an array even for a
single object, per REST hook conventions.

### Available document events
`document.created`, `document.sent`, `document.viewed`, `document.reviewed`,
`document.signed`, `document.approved`, `document.expired`, `document.rejected`,
`document.downloaded`, `document.printed`, `document.forwarded`,
`document.partially_signed`, `document.commented`, `document.hardbounced`,
`document.imported`.

### Verification / security
GetAccept does **not** sign webhook payloads with an HMAC signature. Per the official
help center, verification is via (a) **IP whitelisting** — webhooks are sent from a fixed
set of IP addresses, and (b) **custom HTTP headers** you configure (e.g. an
`Authorization: Bearer …` header) so your endpoint can authenticate the caller.

> Note: Subscription/webhook management is also available through GetAccept Tech Support —
> contact your representative with your endpoint URL, the events to subscribe to, and any
> auth headers your endpoint requires. Deal Room and recipient activity events may also be
> available depending on entity configuration.

### Zapier / Make alternative
Zapier and Make remain available (Professional+) for no-code event handling: Zapier
triggers include Document Created / Sent / Viewed / Reviewed / Signed.

## Gaps

- Webhook delivery payload field schema is confirmed by Tech Support during setup; not
  fully published in the OpenAPI spec.
- No published numeric rate limit (headers expose live state — see Rate Limits).
- Full request/response examples for all endpoints require an Enterprise API entitlement
  to test against live data.
