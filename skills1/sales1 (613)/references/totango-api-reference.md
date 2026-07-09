<!-- Source: https://support.totango.com/hc/en-us/sections/360005893212-Totango-API (403 to direct fetch — Zendesk JS-rendered) -->
<!-- Re-verified 2026-06-13 via search-engine reads of the official support.totango.com articles (Search API, Touchpoints API, Tasks API, SuccessPlay API, Objectives API, Accounts Plan API, Audit Log API, API rate limit). -->
<!-- Supplemented from: https://www.stitchflow.com/user-management/totango/api, https://docs.tray.ai/connectors/service/totango, https://github.com/r0hitacharya/Totango -->
<!-- Note: Official API docs are behind Zendesk and 403 on direct fetch; content below is corroborated against the official article text returned by search. Review against official docs when directly accessible. -->

# Totango API Reference

## Base URLs

- **US**: `https://api.totango.com`
- **EU**: `https://api-eu1.totango.com`

## Authentication

### App Token (recommended)
Header: `app-token: YOUR-TOKEN-HERE`

Generate in: Settings → Integrations → API Token

**Warning**: Clicking "Generate Token" creates a new token and invalidates the previous one. This breaks other integrations using the old token.

### Session Token (legacy)
Either a v1 token or a session token generated upon login. Used in some older endpoints.

### OAuth 2.0
Create and manage OAuth applications for third-party integrations.
Docs: https://support.totango.com/hc/en-us/articles/14475645271956-Create-and-manage-OAuth-applications

### SCIM 2.0 (Enterprise only)
- **Endpoint**: `https://api.totango.com/scim/v2` (as previously documented). NOTE: official Okta-provisioning material also references a service-scoped path of the form `https://app.totango.com/t01/on/api/v2/scim/services/{service-id}/Users` — host/path is ambiguous across sources; confirm the exact base for your tenant.
- **Enable**: Settings → User Management → Totango Users → General Settings → "Enable SCIM APIs for User Management."
- **SSO prerequisite — UNVERIFIED**: Some sources say SSO must be enabled first; the official remote-user-management article states SSO enforcement "has no effect on this [server-to-server] API." Treat the SSO prerequisite as unconfirmed.
- **Operations**: GET/POST/PUT/PATCH/DELETE on `/Users` and `/Users/{id}`; `userName` (the user's email) is the unique identifier. Note: the SCIM API does not support custom group attributes from Okta.

## Rate Limits

- **Global**: 100 calls/minute per token
- **Search**: Max 1,000 results per call (use `offset` for pagination)
- **Exemptions**: The HTTP API (collection gateway / activity ingest) and its JavaScript wrapper (collector) are **not** rate-limited.
- **429 response**: Exceeding the limit returns `HTTP/1.1 429 Too Many Requests` with headers `RateLimit-Limit` (e.g. `100`), `RateLimit-Remaining` (e.g. `0`), `RateLimit-Reset` (seconds until the counter resets), and `Retry-After` (seconds to wait before retrying, e.g. `60`). Honor `Retry-After` for backoff.

## Endpoints

### Search Accounts

```
POST {base_url}/api/v1/search/accounts
Content-Type: application/x-www-form-urlencoded
app-token: YOUR-TOKEN

query={"terms":[],"count":100,"offset":0,"fields":[{"type":"string_attribute","attribute":"Name","field_display_name":"Name"}]}
```

- `terms` array is **mandatory** — omitting returns 401
- `count`: number of results (max 1,000)
- `offset`: pagination offset
- `fields`: array of field definitions to return
- Response data is in `hits` property

### Search Users

```
POST {base_url}/api/v1/search/users
Content-Type: application/x-www-form-urlencoded
app-token: YOUR-TOKEN

query={"terms":[],"count":100,"offset":0}
```

Same structure as account search. Search criteria in `terms` array.

### Search Events (Touchpoints)

```
POST {base_url}/api/v2/events/search
app-token: YOUR-TOKEN

query={"terms":[],"count":100,"offset":0}
```

Searches any event type that matches criteria (e.g. "all touchpoints created in the last 90 days"). Returns up to **1,000 events per call**; use the `offset` property for pagination. Subject to the global 100 calls/min limit.

Documented `event_type` values:
- `note` — touchpoint
- `campaign_touch` — campaign event
- `alert` — health change
- `task` — task event (created, updated, completed)

### Touchpoints API (v3)

#### Create Touchpoint
```
POST {base_url}/api/v3/touchpoints/
Content-Type: application/json
app-token: YOUR-TOKEN

{
  "account_id": "ACC-123",
  "content": "Quarterly business review completed",
  "activity_type_id": "escalation",
  "subject": "QBR Q1 2026"
}
```

Documented fields:
- `account_id` — **required**, the account identifier.
- `content` — the body/content of the touchpoint.
- `activity_type_id` — the **Flow ID** for the touchpoint. Get available IDs from the `/api/v3/activity-types` endpoint. (The older `touchpointType` field is the touchpoint type ID.)
- `created_by` — email of the creator; Totango shows the name if it matches a Totango user, otherwise the raw email (external user).
- `create_date` — Unix EPOCH time in **milliseconds**; defaults to the current timestamp if omitted.
- `disable_sync` — set `true` to prevent Totango syncing this touchpoint to Salesforce or other 3rd-party systems.
- `touchpoint_tags` — array of tag IDs.
- `subject` — free-text subject line.

#### Read, Update, Delete
- **GET** `{base_url}/api/v3/touchpoints/{touchpoint_id}`
- **PUT** `{base_url}/api/v3/touchpoints/{touchpoint_id}`
- **DELETE** `{base_url}/api/v3/touchpoints/{touchpoint_id}`

#### Activity Types (Flows)
```
GET {base_url}/api/v3/activity-types
app-token: YOUR-TOKEN
```
Returns the available Flow IDs used as `activity_type_id` on touchpoints and tasks.

### Team Members API (v2)

#### List All
```
GET {base_url}/api/v2/team_members
app-token: YOUR-TOKEN
```
Returns all team members. Pagination via offset for large result sets.

#### Get Single Member
```
GET {base_url}/api/v2/team_members/{user_id}
```
Note: `user_id` must be URL-encoded when it contains `@`.

#### Create/Update (Upsert)
```
POST {base_url}/api/v2/team_members
Content-Type: application/json
app-token: YOUR-TOKEN

{
  "id": "csm@company.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "csm"
}
```
Upsert behavior: if user exists, updates the record.

#### Deactivate
```
DELETE {base_url}/api/v2/team_members/{user_id}
```
Deactivates the user — does **not** permanently remove from Totango.

### Ingest Account/User Data (HTTP API)

```
POST {base_url}/api/v1/accounts
Content-Type: application/x-www-form-urlencoded
app-token: YOUR-TOKEN

data={"service_id":"YOUR-SERVICE-ID","account_id":"ACC-123","account_attributes":{"Name":"Acme Corp"}}
```

Uses form-encoded body with a JSON string in the `data` parameter — **not** a raw JSON body.

### Tasks API (v3)

Full CRUD on tasks (not just CSV export).

#### Create Task
```
POST {base_url}/api/v3/tasks
Content-Type: application/json
app-token: YOUR-TOKEN

{
  "title": "task title",
  "description": "task description",
  "due_date": "2024-02-28",
  "priority": 2,
  "status": "open",
  "status_label_id": "status-label-id",
  "account_id": "account-id",
  "assignee": "username",
  "activity_type_id": "activity-type-id"
}
```

#### Update Task
```
PUT {base_url}/api/v3/tasks/{task_id}
Content-Type: application/json
app-token: YOUR-TOKEN

{"priority":"3","due_date":"2024-02-25","assignee":"username","account_id":"account-id","status_label_id":"45de43fe-1b17-47d2-9dbf-996aa891b00e"}
```

Field notes:
- `priority`: `1` (high), `2` (normal), `3` (low).
- `assignee`: assignee email or UUID.
- `activity_type_id`: the Flow ID (required) — fetch from `/api/v3/activity-types`.
- `status_label_id`: the task status label UUID.

Delete is also documented (DELETE on a task by ID); confirm the exact path against official docs before relying on it.

#### Task / SuccessPlay CSV Export
```
GET {base_url}/api/v3/tasks/export/csv
app-token: YOUR-TOKEN
```
Exports task/SuccessPlay statistics as CSV.

### SuccessPlay API (v2) — run a manual SuccessPlay

```
POST {base_url}/api/v2/automations/run-manual-successplay
Content-Type: application/json
app-token: YOUR-TOKEN

{ "successplayId": "{SuccessPlay-id}", "accountId": "{account-id}" }
```
Triggers a manual SuccessPlay against a single account. The SuccessPlay ID appears in the URL of any SuccessPlay.

### Objectives API (v3)

Create and manage success-plan objectives.

#### Create Objective
```
POST {base_url}/api/v3/objectives-collection
Content-Type: application/json
app-token: YOUR-TOKEN

{ "accountId": "account-id", "ObjectiveTemplateId": "objective-template-id" }
```

#### Create Objective from Template
```
POST {base_url}/api/v3/objectives-collection/create-by-template
app-token: YOUR-TOKEN
```
Supply the objective template ID and the account ID.

### Accounts Plan API (v3)

Read an account's plan summary:
```
GET {base_url}/api/v3/accounts/{account_id}/plan_summary
app-token: YOUR-TOKEN
```
- US: `https://api.totango.com/api/v3/accounts/{account_id}/plan_summary`
- EU: `https://api-eu1.totango.com/api/v3/accounts/{account_id}/plan_summary`

### Audit Log API (v2)

```
GET {base_url}/api/v2/audit?startDate=2018-04-29&endDate=2018-05-12
app-token: YOUR-TOKEN
```
- `startDate` / `endDate`: filter by action date, format `YYYY-MM-DD`.
- Constraint: start and end **years must be equal**; a single query can span at most a one-year period.
- Optional filtering by user action (e.g. `USER_PROFILE_VIEW`).

### User Management API

Manage Totango system users remotely. Docs: https://support.totango.com/hc/en-us/articles/360031891612

## Data Model

### Team Member fields
| Field | Type | Required |
|---|---|---|
| id | string | Yes |
| email | string | Yes (create) |
| first_name | string | No |
| last_name | string | No |
| role | string | No |
| status | string | No |
| teams | array | No |

### Pagination
- Offset-based: use `offset` parameter in search queries
- Max page size: 1,000

## SDKs and Libraries

- **Node.js**: `totango-tracker` npm package — track activities, modules, attributes
- **iOS**: `totango/totango-ios-api` on GitHub
- **Go**: Third-party library at `github.com/BenjaminRH/totango`
- **Python**: Community scripts at `github.com/r0hitacharya/Totango`

## JavaScript Tracking (Client-Side)

Totango provides a JavaScript collector for tracking user activity in web applications. Configure via the Totango admin panel. Used for product usage data that feeds health scores.

## Integration via Zapier

- **Triggers**: Account attribute changed, new account added, user attribute changed, new user added
- **Actions**: Send Data (HTTP API — account attributes, user attributes, activity tracking)
- **Webhooks**: Use "Webhooks by Zapier" (Pro required) as trigger to leverage other Totango APIs (e.g., Search API)

## Webhook Support

Customer Data Hub supports execution reporting via webhooks. Use this to monitor data import job success/failure. Example: https://support.totango.com/hc/en-us/articles/360029056871
