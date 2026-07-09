### Seismic REST API — Comprehensive Reference

**Developer Portal**: https://developer.seismic.com/seismicsoftware/ (re-verified 2026-06-13 — the portal lives under the `/seismicsoftware/` path)
**Production host**: `https://api.seismic.com/` — the Integration API is served under `https://api.seismic.com/integration/v2/...`
**Sandbox/testing host**: `https://api-sandbox.seismic.com/`
**API versioning**: Each route is versioned **independently** — there is no single global API version. In practice you will see e.g. Integration v2, Reporting v2, Document Generator V3, Engagement V2, and a separate LiveDocs Express host (`https://api.seismic.com/livedocs-express/v2/...`). Treat each route's version segment as authoritative.

> Note: Seismic groups its public APIs into three families — **Authentication APIs**, **Integration APIs** (real-time content/users/links), and **Reporting APIs** (async/ETL bulk extraction). See the per-section notes below.

---

## Authentication

OAuth 2.0 / OpenID Connect. All endpoints require a Bearer token in the `Authorization` header. Auth is per-tenant — the token and authorization endpoints embed the tenant name.

| Detail | Value |
|---|---|
| Protocol | OAuth 2.0 / OpenID Connect |
| Token endpoint | `https://auth.seismic.com/tenants/{tenant}/connect/token` |
| Auth authority | `https://auth.seismic.com/auth` (OIDC discovery via the tenant's OpenID configuration) |
| Supported flows | Authorization Code, Authorization Code + PKCE, Client Credentials, Implicit, Password |
| Token type | Bearer |
| Token lifetime | Typically ~1 hour (verify per-tenant) |
| Refresh tokens | Supported for Authorization Code and Password flows |

> **Verified 2026-06-13**: the OAuth2 token URL pattern is `https://auth.seismic.com/tenants/{tenant}/connect/token` (an OIDC `connect/token` endpoint), NOT a `/oauth2/token` path. The five flows above match the current Authentication Overview. For Client Credentials, the app installer consents to a delegated user, and tokens are retrieved as that user (machine-to-machine "user delegation").

**Recommended flow by use case**:

| Use case | Flow |
|---|---|
| Server-to-server integrations | Client Credentials |
| Web applications (with backend) | Authorization Code |
| Single-page applications | Authorization Code with PKCE |
| Mobile applications | Authorization Code with PKCE |
| Legacy integrations (discouraged) | Password |

**Authorization Code Flow**:

1. Redirect the user to the tenant authorize endpoint (under `https://auth.seismic.com/tenants/{tenant}/connect/authorize`) with:
```
client_id=YOUR_CLIENT_ID&
response_type=code&
redirect_uri=YOUR_REDIRECT_URI&
scope=...
```

2. User approves and is redirected back with a `code` parameter.

3. Exchange the code for tokens:
```
POST https://auth.seismic.com/tenants/{tenant}/connect/token
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
code=AUTHORIZATION_CODE&
grant_type=authorization_code&
redirect_uri=YOUR_REDIRECT_URI
```

4. Token response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "dGhp...",
  "expires_in": 3600,
  "token_type": "Bearer",
  "scope": "seismic.library.read seismic.library.manage"
}
```

**Client Credentials Flow** (server-to-server, "user delegation"):
```
POST https://auth.seismic.com/tenants/{tenant}/connect/token
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
grant_type=client_credentials&
scope=seismic.library.read
```

**Common scopes**:

| Scope | Access |
|---|---|
| `seismic.library.read` | Read content library |
| `seismic.library.manage` | Create, update, delete content |
| `seismic.workspace.read` | Read workspaces |
| `seismic.workspace.manage` | Manage workspaces |
| `seismic.user.read` | Read user/group information |
| `seismic.user.manage` | Manage users and groups (SCIM) |
| `seismic.reporting.read` | Access reporting data |
| `seismic.livedocs.manage` | Generate LiveDocs |
| `seismic.delivery.manage` | Create LiveSend links and DSRs |

---

## Request & Response Format

### Requests

- **Standard REST methods**: GET for reads, POST for creates, PUT/PATCH for updates, DELETE for deletes
- **Content-Type**: `application/json` for request bodies
- **Authorization**: `Authorization: Bearer {access_token}` header on all requests

### Response Format

Successful responses return the resource directly or a collection wrapper:

**Single resource**:
```json
{
  "id": "abc123",
  "name": "Q1 Battlecard",
  "type": "document",
  ...
}
```

**Collection**:
```json
{
  "items": [...],
  "totalCount": 150,
  "continuationToken": "opaque_cursor_string"
}
```

### Error Responses

Errors return a standard error object:

```json
{
  "error": {
    "code": "ResourceNotFound",
    "message": "The requested content item was not found.",
    "target": "contentId",
    "details": []
  }
}
```

**Common HTTP status codes**:

| Code | Description |
|---|---|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful delete) |
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — invalid or expired token |
| 403 | Forbidden — insufficient permissions/scope |
| 404 | Not Found — resource doesn't exist |
| 429 | Too Many Requests — rate limit exceeded |
| 500 | Internal Server Error — retry with backoff |

---

## Pagination

**Type**: Cursor-based (`continuationToken`)

| Parameter | Type | Description |
|---|---|---|
| `continuationToken` | string (query param) | Opaque cursor returned from the previous response. Pass to fetch the next page. |
| `limit` | integer (query param) | Number of results per page. Default varies by endpoint (typically 25-100). |

**How to paginate**:
1. Make the initial request without `continuationToken`
2. If `continuationToken` in the response is not `null`, pass it as a query parameter in your next request
3. Continue until `continuationToken` is `null` or absent

---

## Rate Limits

Verified 2026-06-13 against the developer portal Rate Limiting page. Limits are **tiered by endpoint type**, measured over a rolling **60-second window**, and enforced per tenant.

| Tier | Limit (per 60s) | Applies to |
|---|---|---|
| Tier 1 | 10 calls / 60s | LiveDoc (Document Generator) generation endpoints |
| Tier 1.5 | 30 calls / 60s | LiveSend link creation |
| Tier 2 | 60 calls / 60s | Library and workspace folder listing |
| Tier 3 | 600 calls / 60s | All other endpoints |

**When exceeded**: HTTP `429 Too Many Requests`.

**Response headers on every call**:

| Header | Meaning |
|---|---|
| `X-Seismic-Remaining-Calls` | Remaining calls in the current 60-second window |
| `X-Seismic-Total-Calls` | Calls made so far in the current 60-second window |

> Note: the older "~100 req/min, honor `Retry-After`" guidance is **out of date**. Seismic does not advertise a `Retry-After` header for these limits; pace requests against `X-Seismic-Remaining-Calls` and back off on 429. Organizations needing higher limits can request temporary or permanent exceptions from Seismic support.

---

## All API Endpoints

All paths are relative to `https://api.seismic.com/integration/v2` unless otherwise noted.

> **VERIFIED PATH STRUCTURE (2026-06-13)** — IMPORTANT: the Integration v2 content/library paths below are organized by **teamsite** and content-type, not a single `/library/content` route. Confirmed live path shapes from the developer portal:
> - List/get a file's properties: `GET /integration/v2/teamsites/{teamsiteId}/files/{libraryContentId}`
> - List/get/change a URL item: `GET|PATCH /integration/v2/teamsites/{teamsiteId}/urls/{libraryContentId}`, add: `POST /integration/v2/teamsites/{teamsiteId}/urls`
> - Workspace URL item: `/integration/v2/workspace/urls/{workspaceContentId}`
> - Run a Document Generator (LiveDoc): `POST /integration/v2/teamsites/{teamsiteId}/livedocVersions/{libraryContentVersionId}` (with an `outputs` array)
>
> The simplified `/library/content`, `/livedocs/generate`, etc. paths in the tables below are **illustrative groupings, not exact live routes** — resolve the precise route + verb for a given resource against developer.seismic.com before coding. Items individually re-verified on 2026-06-13 are flagged inline.

---

### Authentication & Permissions

The OAuth token/authorize/revoke endpoints live on the **auth host**, NOT under `api.seismic.com`:

| Method | Endpoint | Description |
|---|---|---|
| GET | `https://auth.seismic.com/tenants/{tenant}/connect/authorize` | Authorization endpoint — redirect users here to grant access |
| POST | `https://auth.seismic.com/tenants/{tenant}/connect/token` | Exchange authorization code or credentials for an access token (verified 2026-06-13) |
| — | OIDC discovery via the tenant's OpenID configuration under `https://auth.seismic.com/auth` | Discover endpoints/keys |

---

### Content Management — Library (8 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/library/content` | List content items in the library with optional filters (type, profile, status) |
| GET | `/library/content/{contentId}` | Get a single content item by ID with metadata and version info |
| POST | `/library/content` | Create a new content item in the library |
| PUT | `/library/content/{contentId}` | Update content item metadata |
| DELETE | `/library/content/{contentId}` | Delete a content item from the library |
| GET | `/library/content/{contentId}/versions` | List all versions of a content item |
| GET | `/library/content/{contentId}/url` | Get a download/access URL for content |
| POST | `/library/content/{contentId}/publish` | Publish a content item from workspace to library |

**GET `/library/content` — Key parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `type` | string | No | Filter by content type (document, video, image, etc.) |
| `contentProfileId` | string | No | Filter by content profile |
| `status` | string | No | Filter by status (published, draft, archived) |
| `modifiedSince` | datetime | No | Filter by last modified date (ISO 8601) |
| `limit` | integer | No | Results per page |
| `continuationToken` | string | No | Pagination cursor |

---

### Content Management — Workspaces (6 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workspaces` | List all workspaces the authenticated user has access to |
| GET | `/workspaces/{workspaceId}` | Get workspace details |
| GET | `/workspaces/{workspaceId}/content` | List content items in a workspace |
| POST | `/workspaces/{workspaceId}/content` | Upload content to a workspace |
| PUT | `/workspaces/{workspaceId}/content/{contentId}` | Update content in a workspace |
| DELETE | `/workspaces/{workspaceId}/content/{contentId}` | Delete content from a workspace |

---

### Content Management — Custom Content (4 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/customContent` | List custom content types configured for the tenant |
| GET | `/customContent/{typeId}` | Get a specific custom content type definition |
| POST | `/customContent` | Create content with a custom content type |
| PUT | `/customContent/{contentId}` | Update custom content |

---

### Content Profiles & Taxonomy (4 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/contentProfiles` | List all content profiles (metadata schemas) |
| GET | `/contentProfiles/{profileId}` | Get a content profile definition with all fields |
| GET | `/contentClasses` | List all content classes (taxonomy categories) |
| GET | `/contentClasses/{classId}` | Get a content class definition |

---

### Engagement — Delivery / LiveSend (6 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/delivery/liveSend` | Create a LiveSend tracked link for content |
| GET | `/delivery/liveSend/{linkId}` | Get LiveSend link details and engagement analytics |
| GET | `/delivery/liveSend` | List all LiveSend links with optional filters |
| DELETE | `/delivery/liveSend/{linkId}` | Revoke/delete a LiveSend link |
| GET | `/delivery/liveSend/{linkId}/analytics` | Get detailed engagement analytics for a LiveSend link |
| GET | `/delivery/liveSend/{linkId}/recipients` | List recipients and their individual engagement data |

**POST `/delivery/liveSend` — Parameters**:

| Field | Type | Required | Description |
|---|---|---|---|
| `contentId` | string | Yes | ID of the content item to share |
| `recipientEmail` | string | Yes | Email address of the recipient |
| `recipientName` | string | No | Display name of the recipient |
| `expirationDate` | datetime | No | When the link expires (ISO 8601) |
| `notifyOnView` | boolean | No | Send notification when recipient views content |
| `allowDownload` | boolean | No | Allow recipient to download the content |

---

### Engagement — Digital Sales Rooms (6 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/delivery/digitalSalesRooms` | Create a new Digital Sales Room |
| GET | `/delivery/digitalSalesRooms/{dsrId}` | Get DSR details including content and recipients |
| PUT | `/delivery/digitalSalesRooms/{dsrId}` | Update DSR settings, content, or recipients |
| DELETE | `/delivery/digitalSalesRooms/{dsrId}` | Delete a Digital Sales Room |
| GET | `/delivery/digitalSalesRooms/{dsrId}/analytics` | Get engagement analytics for a DSR |
| GET | `/delivery/digitalSalesRooms` | List all Digital Sales Rooms with optional filters |

**POST `/delivery/digitalSalesRooms` — Parameters**:

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Name of the Digital Sales Room |
| `recipients` | array | Yes | Array of recipient objects (email, name, role) |
| `contentItems` | array | Yes | Array of content item IDs to include |
| `branding` | object | No | Custom branding settings (logo, colors) |
| `expirationDate` | datetime | No | When the DSR expires |

---

### Engagement — Email (3 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/delivery/email` | Send content via email with tracking |
| GET | `/delivery/email/{emailId}/analytics` | Get engagement analytics for a sent email |
| GET | `/delivery/email` | List sent emails with analytics |

---

### Reporting API v2 (verified 2026-06-13)

The Reporting API is a separate API family built for **ETL / bulk data extraction** into an external database / data lake / warehouse — NOT for high-frequency, interactive use. Data is refreshed **no less than every 24 hours**. Endpoints are exposed as queryable tables/fields rather than a submit-and-poll job queue.

- **Data dictionary**: "Fields and Tables" endpoints describe the available report tables and their columns.
- **Activity / history tables**: e.g. Content Usage History, Generated Livedocs, External Content Details, AI activity/metrics, content interactions, user/group data, and admin impersonation sessions.
- **Output formats**: each endpoint supports both `application/json` and `text/csv` via the `Accept` request header.

> Correction (2026-06-13): the live Reporting API is described as **ETL-oriented and table/field-based with a ≥24h refresh**, not an async "POST a report → poll `reportId` → download results" job pattern. The `/reporting/reports` job-queue endpoints below are **UNVERIFIED** and likely incorrect — pull from the Reporting table endpoints (e.g. Content Usage History, Generated Livedocs) instead.

| Method | Endpoint | Status |
|---|---|---|
| GET | `/reporting/v2/...` table endpoints (Content Usage History, Generated Livedocs, External Content Details, etc.) | Verified family (exact paths per developer portal) |
| POST | `/reporting/reports` (submit report job) | UNVERIFIED — likely not a live route |
| GET | `/reporting/reports/{reportId}` / `/results` (poll/download) | UNVERIFIED — likely not a live route |

---

### Users & Groups — SCIM (8 endpoints)

Seismic supports SCIM 2.0 for user and group provisioning.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users` | List all users in the tenant |
| GET | `/users/{userId}` | Get a specific user's details |
| POST | `/users` | Create a new user (SCIM provisioning) |
| PUT | `/users/{userId}` | Update a user's profile |
| DELETE | `/users/{userId}` | Deactivate/delete a user |
| GET | `/groups` | List all groups |
| POST | `/groups` | Create a new group |
| PUT | `/groups/{groupId}` | Update group membership |

---

### Meetings & Recordings (5 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/meetings` | List recorded meetings with filters (date, participant, deal) |
| GET | `/meetings/{meetingId}` | Get meeting details including AI summary and key moments |
| GET | `/meetings/{meetingId}/transcript` | Get the full meeting transcript |
| GET | `/meetings/{meetingId}/actionItems` | Get AI-extracted action items from a meeting |
| GET | `/meetings/{meetingId}/recording` | Get the meeting recording URL |

---

### Learning & Skills (7 endpoints)

Note: Learning endpoints may use a different base URL if the tenant's Seismic Learning instance was originally a standalone Lessonly deployment.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/learning/lessons` | List all lessons with optional filters |
| GET | `/learning/lessons/{lessonId}` | Get lesson details including content and completion stats |
| GET | `/learning/paths` | List all learning paths |
| GET | `/learning/paths/{pathId}` | Get learning path details with lessons and progress |
| POST | `/learning/assignments` | Assign lessons or paths to users/groups |
| GET | `/learning/completions` | List completion records with filters (user, lesson, date range) |
| GET | `/learning/certifications` | List certifications and their status per user |

---

### Search (3 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/search` | Core search — search content library by keyword, filters, and facets |
| POST | `/search/generative` | Generative AI search — natural language query with AI-synthesized answer |
| GET | `/search/suggestions` | Search suggestions/autocomplete based on partial query |

**GET `/search` — Key parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | Search query string |
| `contentType` | string | No | Filter by content type |
| `contentProfileId` | string | No | Filter by content profile |
| `limit` | integer | No | Results per page |
| `continuationToken` | string | No | Pagination cursor |

---

### LiveDocs / Document Generator (verified 2026-06-13)

The live API calls these "Document Generator" operations. Two surfaces exist:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/integration/v2/teamsites/{teamsiteId}/livedocVersions/{libraryContentVersionId}` | **Run a Document Generator** — generate a LiveDoc. Each desired output is specified in an `outputs` array; omitting `outputs` returns a 4xx. Generated outputs are downloadable for **24 hours** only. |
| GET | `/integration/v2/teamsites/{teamsiteId}/livedocVersions/{libraryContentVersionId}/...inputs` | Get the list of inputs (merge fields) for a Document Generator |
| GET | `/integration/v2/teamsites/{teamsiteId}/livedocVersions/.../outputs/...` | Download a particular generated output (.pptx, .docx, .pdf, .xlsx) |

**LiveDocs Express** is a separate host/version — `https://api.seismic.com/livedocs-express/v2/teamsites/{teamsiteId}/livedocVersions/{libraryContentVersionId}/variants` (and related variant endpoints). Use Express for batch/variant generation; use the Document Generator run endpoint above for single-doc generation.

> Correction (2026-06-13): there is no `/livedocs/generate` or `/livedocs/process` route, and "Express vs Process" is not the live API split — the live split is **Document Generator (Integration v2)** vs **LiveDocs Express (livedocs-express/v2)**. The "Express vs Process" framing is a product/UI concept; map it to these endpoints when coding.

**POST `/livedocs/generate` (Express) — Parameters**:

| Field | Type | Required | Description |
|---|---|---|---|
| `templateId` | string | Yes | ID of the LiveDoc template |
| `mergeData` | object | Yes | Key-value pairs mapping merge fields to values |
| `outputFormat` | string | No | Output format: `pdf`, `pptx`, `docx` (defaults to template default) |
| `dataSourceId` | string | No | ID of a connected data source (CRM) to pull merge data from |
| `recordId` | string | No | CRM record ID to pull data from (used with `dataSourceId`) |

**POST `/livedocs/process` (Process) — Parameters**:

| Field | Type | Required | Description |
|---|---|---|---|
| `templateId` | string | Yes | ID of the LiveDoc template |
| `mergeData` | object | No | Initial merge data (can be supplemented during workflow) |
| `approvers` | array | No | List of user IDs who must approve |
| `contributors` | array | No | List of user IDs who can edit sections |
| `dueDate` | datetime | No | Deadline for the workflow |

---

### Programs & Tasks (6 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/programs` | List all enablement programs |
| GET | `/programs/{programId}` | Get program details with tasks and progress |
| POST | `/programs` | Create a new enablement program |
| PUT | `/programs/{programId}` | Update a program |
| GET | `/programs/{programId}/analytics` | Get program analytics (completion, impact) |
| POST | `/programs/{programId}/tasks` | Add tasks to a program |

---

### Channel Management (3 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/channels` | List content distribution channels |
| POST | `/channels/{channelId}/publish` | Publish content to a specific channel |
| GET | `/channels/{channelId}/content` | List content published to a channel |

---

### CRM Activity Logging (3 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/crm/activities` | Log a content-related activity to CRM |
| GET | `/crm/activities` | List logged CRM activities |
| GET | `/crm/mappings` | Get CRM field mapping configuration |

---

### Events & Webhooks (4 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/webhooks` | Create a webhook subscription |
| GET | `/webhooks` | List all webhook subscriptions |
| GET | `/webhooks/{webhookId}` | Get webhook subscription details |
| DELETE | `/webhooks/{webhookId}` | Delete a webhook subscription |

**POST `/webhooks` — Parameters**:

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | The URL to receive webhook payloads |
| `events` | array | Yes | Array of event types to subscribe to |
| `secret` | string | No | Shared secret for payload verification (HMAC) |

**Supported webhook events (verified 2026-06-13 against the Events & Webhooks docs)**:

Seismic event type names are **PascalCase with a version suffix** (e.g. `...V1`), NOT dot-delimited. Confirmed event types by category:

| Category | Event types |
|---|---|
| **ContentManager** | `ContentManagerActiveVersionChangedV1`, `ContentManagerContentVersionExpiredV1`, `ContentManagerCopyFileV1`, `ContentManagerCopyFolderV1`, `ContentManagerCreateFileV1`, `ContentManagerCreateFileVersionV1`, `ContentManagerDeleteFileV1`, `ContentManagerMoveFileV1`, `ContentManagerUpdateContentCustomPropertyV1` |
| **ContentProfile** | `ContentProfileAddToProfileV1`, `ContentProfileRemoveFromProfileV1` |
| **CustomSchema** | `CustomSchemaCreateV1`, `CustomSchemaDeleteV1`, `CustomSchemaUpdateV1` |
| **DSR** | `DSRCreatedV1`, `DSRUpdatedV1`, `DSRContentUpdatedV1`, `DSRExpiredV1` |
| **Document Generator / Express** | `LiveDocCompletedV2`, `LDXJobStatusV1` |
| **Livesend** | `LivesendCreatedV1`, `LivesendUpdatedV1`, `LivesendContentUpdatedV1`, `LivesendExpiredV1` |
| **Planner** | `PlannerProjectCreateV1/DeleteV1/UpdateV1`, `PlannerRequestCreateV1/DeleteV1/UpdateV1`, `PlannerTaskCreateV1/DeleteV1/UpdateV1` |
| **Program** | `ProgramCreateV1/DeleteV1/UpdateV1`, `ProgramRequestCreateV1/DeleteV1/UpdateV1`, `ProgramTaskCreateV1/DeleteV1/UpdateV1` |
| **User / UserGroup** | `UserCreatedV1`, `UserDeletedV1`, `UserUpdatedV1`, `UserGroupCreatedV1`, `UserGroupDeletedV1`, `UserGroupMemberChangeV1`, `UserGroupUpdatedV1` |
| **Workflow** | `WorkflowSubmitV1`, `WorkflowApproveStepV1`, `WorkflowRejectStepV1`, `WorkflowRecallV1`, `WorkflowRevokeStepV1` |
| **Other** | `ReadinessArchivalEventV1` |

> Correction (2026-06-13): the previous dot-style names (`content.published`, `livesend.viewed`, `dsr.contentViewed`, `learning.completed`, etc.) are **not** the live event identifiers — use the PascalCase `...V1`/`...V2` names above. Note there is no Learning-completion webhook in this list; pull Learning completion from the Reporting API instead. Legacy email/interaction-session webhooks also exist on a separate "Legacy Webhooks" surface.

**Event payload structure**: every event is wrapped in a common event **super-structure**; the event-specific fields live inside that wrapper's `data` object (shape varies per event type). The example below is illustrative only — confirm exact fields per event in the developer portal.
```json
{
  "eventType": "LivesendCreatedV1",
  "timestamp": "2026-01-15T10:30:00Z",
  "tenantId": "your-tenant-id",
  "data": { "...": "event-specific fields" }
}
```

**Signature & delivery (verified 2026-06-13)**:
- Payloads are signed with **HMAC-SHA256** of the raw request body using the app's signing secret.
- The signature is sent in the **`x-seismic-signature`** request header.
- During secret rotation, the previous signature is sent in **`x-seismic-signature-old`** so you can validate against either secret during the transition.
- Your endpoint must return an HTTP **2xx within 10 seconds**; any non-2xx (or timeout) is a failure.
- **Retry policy**: up to **26 total attempts** — first retry at 1 minute, then 10 minutes, then hourly for 24 hours.

---

## Common Automation Patterns

**Content publishing pipeline**: Upload content to workspace via POST `/workspaces/{id}/content` -> review and approve -> publish to library via POST `/library/content/{id}/publish` -> distribute via LiveSend or DSR.

**LiveDocs Express generation**: Get template details via GET `/livedocs/templates/{id}` to understand required merge fields -> POST `/livedocs/generate` with merge data from CRM -> receive generated document URL in response.

**DSR lifecycle**: Create DSR via POST `/delivery/digitalSalesRooms` with recipients and content -> monitor engagement via GET `/{dsrId}/analytics` -> update content as deal progresses via PUT -> clean up expired DSRs.

**Reporting pipeline**: List available report types via GET `/reporting/reportTypes` -> submit report via POST `/reporting/reports` -> poll status via GET `/{reportId}` -> download results when complete.

**User provisioning (SCIM)**: Create users via POST `/users` -> assign to groups via PUT `/groups/{id}` -> assign learning paths via POST `/learning/assignments` -> monitor completion via GET `/learning/completions`.

**Webhook-driven engagement alerts**: Create webhook subscriptions for `livesend.viewed` and `dsr.contentViewed` -> receive real-time engagement signals -> trigger follow-up workflows in CRM or Slack.

---

## Known Gaps & Caveats

- **Developer portal auth required**: Full endpoint details, request/response schemas, and interactive API explorer are behind developer portal authentication at developer.seismic.com. This reference is best-effort from public documentation and may not reflect the latest API changes.
- **Tenant-specific base URLs**: Some tenants may have custom base URLs. Check your tenant's API settings in the Seismic admin panel.
- **Learning API divergence**: Seismic Learning (formerly Lessonly) may use a different base URL and authentication mechanism if the instance predates the Seismic acquisition. Check with your admin.
- **Rate limits are tiered, not flat** (verified 2026-06-13): 10/30/60/600 calls per 60s by endpoint tier (see Rate Limits). Track `X-Seismic-Remaining-Calls`; there is no `Retry-After` header.
- **Seismic-Highspot merger**: the **definitive merge agreement was announced February 12, 2026** (not "late 2025"). The combined company will operate under the **Seismic** name, led by Seismic's CEO; Permira remains controlling shareholder. The deal is subject to closing conditions/regulatory approval and **both platforms continue to be supported until close** — so the Seismic API surface above remains current for now. Monitor developer.seismic.com for any post-close unification/deprecations.

---

## Source URLs (re-verified 2026-06-13)

- Developer Portal: https://developer.seismic.com/seismicsoftware/
- API Overview (3 API families): https://developer.seismic.com/seismicsoftware/reference/introduction-overview
- Authentication Overview: https://developer.seismic.com/seismicsoftware/reference/authentication-overview
- Client Credentials flow: https://developer.seismic.com/seismicsoftware/reference/login-with-client-credentials-user-delegation-flow
- Versioning & Testing (hosts/sandbox): https://developer.seismic.com/seismicsoftware/reference/versioning
- Rate Limiting: https://developer.seismic.com/seismicsoftware/reference/rate-limiting
- Reporting Overview (ETL): https://developer.seismic.com/seismicsoftware/reference/h1-reporting-api-overview
- Events & Webhooks: https://developer.seismic.com/seismicsoftware/docs/events
- Webhooks Overview (signature/retries): https://developer.seismic.com/seismicsoftware/docs/webhooksoverview
- Run a Document Generator (LiveDoc): https://developer.seismic.com/seismicsoftware/reference/seismiclivedocgeneratealivedoc
- Seismic↔Highspot merger announcement (2026-02-12): https://www.seismic.com/newsroom/press-releases/seismic-highspot-merger-intent/
