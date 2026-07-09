<!-- Source: https://devdocs.instapage.com/ (captured 2026-06-28) -->
<!-- Webhook section source: https://help.instapage.com/hc/en-us/articles/360001722428-Integrating-with-Webhooks and Instapage form-integration docs (homepage help center is 403 to WebFetch; details cross-checked via third-party integration docs) -->
<!-- Secret-shaped example values redacted to placeholders (e.g. API_KEY). -->

# Instapage API Reference

The Instapage API is RESTful. It lets you create, update, retrieve, and delete resources within Instapage — workspaces, pages, collections, groups, team members, form submissions, and analytics.

Official docs: https://devdocs.instapage.com/

## Authentication

Instapage expects the API key to be included in all API requests to the server in a header. To authorize, use this code (replace `API_KEY` with your personal API key):

```
curl "api_endpoint_here" \
  -H "Authorization: Bearer API_KEY"
```

- **Header**: `Authorization: Bearer API_KEY`
- **Personal API Token**: Each Instapage account (including each team member) has its own Personal API Token. The token can fetch information about all the workspaces the user has access to (whether they own them or not) and has the same permission level as the team member who generated it.
- Generate / find the token in the Instapage account/dashboard (`app.instapage.com/account`).

## Base URL

```
https://api.instapage.com/v1
```

## Rate limiting & plan quotas

Instapage enforces both rate limits and daily usage quotas based on your subscription plan. Exceeding either results in a `429 Too Many Requests` response.

**Daily Plan Quota** — Each plan has a daily quota of API calls, which resets every day at 00:00 UTC (midnight GMT). If your token exceeds the daily quota, the response includes a `Retry-After` header indicating when you can try again. The daily limit can be checked in the Subscription section of the app by the account owner.

**Per-Minute Rate Limit** — You may send up to 200 requests per minute. This limit is enforced per token and per IP address. High-frequency requests may be throttled even before reaching the limit.

## Response / status codes

```
200 - Request was processed successfully
201 - Created / The resource was created successfully
400 - Bad request / Validation error
401 - Unauthorized / Authentication failed or missing credentials
403 - Forbidden / User lacks necessary permissions
404 - Not Found / Resource could not be located
409 - Conflict / Resource already exists or name taken
429 - Too Many Requests / Rate limit or plan quota exceeded
500 - Internal Server Error / Unexpected condition occurred
```

## Pagination

List endpoints accept a `page` query parameter (number, default: `1`). Some accept a `name` (string, optional) filter. Responses include a `meta.pagination` object.

Example query parameters for "Get All Workspaces": `page` (number, default: 1), `name` (string, optional).

Response `meta`:
```json
{
  "meta": {
    "pagination": {
      "currentPage": 1,
      "perPage": 100,
      "totalItemsCount": 4,
      "totalPagesCount": 1
    }
  }
}
```

## Endpoints

### Workspaces

```
GET    https://api.instapage.com/v1/workspaces                 # List all workspaces
GET    https://api.instapage.com/v1/workspaces/{workspaceId}   # Retrieve a single workspace
POST   https://api.instapage.com/v1/workspaces                 # Create a new workspace
PATCH  https://api.instapage.com/v1/workspaces/{workspaceId}   # Rename a workspace
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}   # Delete a workspace
```

**Get all workspaces — response:**
```json
{
  "data": [
    {
      "workspaceId": 1177,
      "ownerId": 1319,
      "workspaceName": "Personal Projects",
      "accessLevel": "owner",
      "createdAt": 1262304000
    }
  ],
  "meta": {
    "pagination": {
      "currentPage": 1,
      "perPage": 100,
      "totalItemsCount": 4,
      "totalPagesCount": 1
    }
  }
}
```

### Team members

```
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/team-members   # List team members
POST   https://api.instapage.com/v1/workspaces/{workspaceId}/team-members   # Invite members
PUT    https://api.instapage.com/v1/workspaces/{workspaceId}/team-members   # Update roles
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/team-members   # Remove members
```

**List team members — response:**
```json
{
  "data": [
    {
      "userId": 4379,
      "email": "example_user@example.com",
      "invitedAt": 1685608225,
      "fullName": "John Smith",
      "accessLevel": "editor",
      "inheritOwnerContextInPublicApi": true,
      "invitationStatus": "accepted",
      "lastLoginAt": 1685608226,
      "lastActivityInWorkspaceAt": null
    }
  ],
  "meta": []
}
```

**Invite members — request (POST):**
```json
[
  {
    "email": "user1@example.com",
    "accessLevel": "viewer"
  },
  {
    "email": "user2@example.com",
    "accessLevel": "manager",
    "inheritOwnerContextInPublicApi": true
  }
]
```

**Update roles — request (PUT):**
```json
[
  {
    "email": "user1@example.com",
    "targetAccessLevel": "viewer",
    "inheritOwnerContextInPublicApi": true
  },
  {
    "email": "user2@example.com",
    "targetAccessLevel": "viewer"
  }
]
```

**Remove members — request (DELETE):**
```json
[
  { "email": "user1@example.com" },
  { "email": "user2@example.com" }
]
```

**Remove members — error response (e.g. trying to remove the owner):**
```json
{
  "title": "InvalidArgumentException",
  "details": "Email \"owner@example.com\" can't be removed from workspace because is owner",
  "meta": {
    "requestedUserId": 4373,
    "requestedPageId": 9910,
    "requestedWorkspaceId": 7068
  }
}
```

### Pages

```
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/pages                       # List pages
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}              # Retrieve a page
POST   https://api.instapage.com/v1/workspaces/{workspaceId}/pages/json                  # Create a page (from JSON)
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}/json         # Retrieve a page as JSON
PATCH  https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}              # Update a page
PUT    https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}/publication  # Publish a page
POST   https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}/publication  # Publish a page
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}/publication  # Unpublish a page
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/pages/{pageId}              # Delete a page
```

### Collections

```
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/collections
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/collections/{collectionId}
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/collections/{collectionId}/collection-pages
POST   https://api.instapage.com/v1/workspaces/{workspaceId}/collections/{collectionId}/collection-pages
POST   https://api.instapage.com/v1/workspaces/{workspaceId}/collections/{collectionId}/collection-pages/{id}/publication
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/collections/{collectionId}/collection-pages/{id}/publication
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/collections/{collectionId}/collection-pages/{id}
```

### Groups

```
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/groups
POST   https://api.instapage.com/v1/workspaces/{workspaceId}/groups
PUT    https://api.instapage.com/v1/workspaces/{workspaceId}/groups/{groupId}
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/groups/{groupId}
```

### Form submissions (leads)

```
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/submissions   # Retrieve form submissions
DELETE https://api.instapage.com/v1/workspaces/{workspaceId}/submissions   # Delete up to 100 submissions per request
```

> "Delete up to 100 form submissions in a single request. Deletion is irreversible, so use it with caution."

Response shape (envelope): `{ "data": [...], "meta": {...} }`.

### Analytics

```
GET    https://api.instapage.com/v1/workspaces/{workspaceId}/analytics   # Get statistical data
```

(No JSON response example is provided in the official documentation.)

## Webhooks — Form Submit WebHook

The public REST API does **not** expose webhook management; webhooks are configured per-form inside the page editor (form → integrations → Webhook). A WebHook is a push notification from Instapage's server to yours. The **Form Submit WebHook** sends a push notification to your server every time someone submits a form on one of your Instapage pages. The most common use is to feed leads into your CRM.

- **Trigger**: a form submission on a published Instapage page.
- **Delivery**: an HTTP **POST** to the endpoint URL you configure, carrying the lead data as a single data set (JSON or form-encoded depending on configuration).
- **Field naming**: Instapage uses internal field IDs (e.g. `field_1`, `field_2`) that do not always match the visible form labels — you must map your form fields to your webhook/CRM fields.
- **Timeout**: the server handling the webhook endpoint must respond within a **maximum of 20 seconds**, otherwise the form's "thank you" message or redirect will not work for the visitor.
- **Transport**: use **HTTPS** for your endpoint to safeguard the data and authenticate the connection.
- **Signing**: no documented HMAC/signature mechanism — validate inbound payloads yourself (shared secret, IP allowlist, or a required hidden field).

Example payload (constructed — internal field IDs, verify against a live test submission):
```json
{
  "field_1": "Jane Doe",
  "field_2": "jane@example.com",
  "field_3": "+1 555 0100",
  "page_id": 9910,
  "submitted_at": 1685608225
}
```

Zapier alternative: the Instapage "New Form Submission" trigger pushes leads to any connected app without writing a webhook receiver.

## Gaps

- Full request/response JSON for `POST /pages/json`, `GET /pages/{id}`, `GET /analytics`, and `GET /submissions` is not published in the official docs (only the endpoints + envelope shape were documented at capture time).
- The exact webhook payload schema is not published by Instapage; the example above is constructed from integration docs and should be confirmed with a live test submission.
- Per-plan daily API quotas are surfaced in the app's Subscription section rather than the docs (research baseline: Create 5,000 / Optimize 10,000–15,000 / Convert 30,000+ calls/day).
