<!-- Source: https://docs.userback.io/reference/overview + /reference/authentication + /reference/pagination + per-endpoint .md pages + /docs/webhooks + /docs/javascript-sdk + /docs/userback-mcp (fetched 2026-06-29) -->

# Userback REST API Reference

Captured verbatim from the Userback developer docs where possible, then enriched with
working examples. Re-verify specifics against `https://docs.userback.io/reference` before
relying on them — Userback ships changes frequently.

## Overview

- **Base URL (production):** `https://rest.userback.io/1.0/`
- RESTful, **HTTPS only**, **UTF-8 only**. Accepts JSON or form-encoded request bodies;
  responses are always JSON (including errors).
- Endpoints are described with **OpenAPI 3.0** + JsonSchema definitions for validation.
- **Model names** use PascalCase (singular by default, pluralized for arrays);
  **properties** use camelCase.
- A Postman config is available at `/1.0/postman`.
- An AI-agent index (Markdown) is published at `https://docs.userback.io/llms.txt`.

> **Plan gate:** REST API access requires a **Business Plus** plan with **Admin** permissions.
> Webhooks also require Business Plus. Zapier requires Team or higher.

## Authentication

Bearer token authentication. Generate a token in the Userback Dashboard under
**Workspace Settings → API Token → Create API Token**, name it, and copy it.

- **Header:** `authorization: Bearer <YOUR API TOKEN>`
- Tokens carry **full account-level permissions** for all API actions.
- For multiple Userback accounts, use a separate bearer token per account.

```bash
# Simplest GET — list your projects
curl --request GET \
     --url https://rest.userback.io/1.0/project \
     --header 'authorization: Bearer <YOUR_API_TOKEN>'
```

## Pagination

All list endpoints use page/limit pagination plus HATEOAS links.

- `page` — integer, default `1`, range 1–2147483647
- `limit` — integer, default `25`, range **1–50** (max 50 records per page)
- `sort` — `fieldname,asc|desc`
- `filter` — OData filter syntax

```
GET https://rest.userback.io/1.0/feedback/?page=2&limit=10
```

Every paginated response includes `_links` (self/first/last/next/previous) and
`_pagination`:

```json
{
  "_links": {
    "self": "https://rest.userback.io/1.0/feedback/?page=2",
    "first": "https://rest.userback.io/1.0/feedback?page=1",
    "last": "https://rest.userback.io/1.0/feedback?page=5",
    "next": "https://rest.userback.io/1.0/feedback?page=3",
    "previous": "https://rest.userback.io/1.0/feedback?page=1"
  },
  "_pagination": {
    "totalPages": 12,
    "totalRecords": 126,
    "pageSize": 10,
    "records": 10,
    "pageNumber": 2
  },
  "data": [ /* ... */ ]
}
```

## Error responses

All list/CRUD endpoints can return:

| Status | Meaning |
|--------|---------|
| 401 | Not Authorized (bad/missing bearer token) |
| 422 | Validation Error (malformed body / params) |
| 429 | Too Many Requests (rate limited — back off and retry) |
| 500 | Internal Server Error |

Errors return JSON. Userback states rate limits are in place but does not publish exact
numbers; treat `429` as the signal and apply exponential backoff. <!-- Constructed: exact rate-limit numbers not documented; verify in-account. -->

---

## Resource: Feedback

`feedbackType` is one of `General`, `Bug`, `Idea`. Each Feedback object includes id,
projectId, feedbackType, email, title, description, name, created, modified, dueDate,
assigneeId, workflow status, assignee member details, screenshots, session data, location
data, and integration URLs.

### List feedback — `GET /feedback`

Query params: `page`, `limit` (1–50), `sort`, `filter` (OData). Returns
`FeedbackListResponse` (`_links` + `_pagination` + `data[]`).

```bash
curl -s 'https://rest.userback.io/1.0/feedback?limit=50&sort=created,desc' \
  -H 'authorization: Bearer <TOKEN>'
```

### Retrieve feedback — `GET /feedback/{id}`

### Create feedback — `POST /feedback`

Required body fields:
- `projectId` (integer)
- `email` (string) — submitter's email
- `feedbackType` (string) — `General` | `Bug` | `Idea`
- `title` (string)
- `description` (string)

Optional: `name`, `pageUrl`, `isShared` (bool), `allowPublicComment` (bool),
`priority` (`low`|`neutral`|`high`|`urgent`), `category`, `rating` (`star_1`…`star_5`),
`assigneeId` (int), `dueDate` (`YYYY-MM-DD`), `notify` (bool, default `true` — set `false`
to suppress notifications).

```json
{
  "projectId": 123,
  "email": "user@example.com",
  "feedbackType": "Bug",
  "title": "Button malfunction",
  "description": "The submit button doesn't respond",
  "name": "John Doe",
  "priority": "high"
}
```

Returns `201` with the complete Feedback object (generated id, timestamps, workflow status,
associated data).

### Update feedback — `PATCH/PUT /feedback/{id}`
### Delete feedback — `DELETE /feedback/{id}`

---

## Resource: Comments

### Create comment — `POST /feedback/comment`

Required: `feedbackId` (int), `comment` (string, max 65535 chars).
Optional: `replyCommentId` (int), `userId` (int), `isPublic` (bool), `guestEmail`,
`guestName`.

```json
{ "feedbackId": 4455, "comment": "We're investigating this issue", "isPublic": true, "userId": 1234 }
```

Response `201`:

```json
{
  "id": 7890,
  "userId": 1234,
  "screenshotNum": 0,
  "isResolved": false,
  "isPublic": true,
  "comment": "We're investigating this issue",
  "reaction": [],
  "created": "2024-01-15T10:30:00Z",
  "modified": "2024-01-15T10:30:00Z",
  "Feedback": {
    "id": 4455,
    "projectId": 1,
    "feedbackType": "Bug",
    "email": "user@example.com",
    "title": "Button malfunction",
    "description": "Submit button unresponsive",
    "name": "John Doe",
    "created": "2024-01-15T09:00:00Z",
    "modified": "2024-01-15T10:30:00Z",
    "dueDate": null
  }
}
```

Other comment endpoints: `GET /feedback/comment/{id}`, `GET /feedback/comment` (list),
`PATCH /feedback/comment/{id}` (update), `DELETE /feedback/comment/{id}`.

---

## Resource: Screenshots

`POST /feedback/screenshot` (create a screenshot associated with feedback).

---

## Resource: Projects

### List projects — `GET /project`

Query params: `page`, `limit` (1–50), `sort`, `filter`.

```json
{
  "_links": { "self": "https://rest.userback.io/1.0/project", "first": "...?page=1", "last": "...?page=5", "next": "...?page=2", "previous": "...?page=1" },
  "_pagination": { "pageNumber": 1, "pageSize": 25, "records": 25, "totalPages": 5, "totalRecords": 125 },
  "data": [
    {
      "id": 4455,
      "name": "My Project",
      "url": "https://myproject.com",
      "logo": "https://myproject.com/logo.png",
      "isArchived": false,
      "created": "2024-01-15T10:30:00Z",
      "createdBy": 1234
    }
  ]
}
```

Other project endpoints: `GET /project/{id}` (retrieve), `PATCH /project/{id}` (update).

---

## Resource: Members

`GET /member/{id}` (retrieve), `GET /member` (list), `PATCH /member/{id}` (update).

---

## Resource: Session Recordings

### List session recordings — `GET /sessionRecording`

Query params: `page`, `limit` (1–50), `sort`, `filter`.

```json
{
  "_links": { "self": "...", "first": "...", "previous": "...", "next": "...", "last": "..." },
  "_pagination": { "pageNumber": 1, "pageSize": 25, "records": 25, "totalPages": 1, "totalRecords": 12 },
  "data": [
    {
      "id": 999,
      "shareUrl": "https://app.userback.io/session/...",
      "duration": 84.5,
      "userAgent": "Mozilla/5.0 ...",
      "location": "Sydney, AU",
      "userIdentification": "user@example.com",
      "tag": "checkout,bug",
      "domain": "myproject.com",
      "created": "2024-01-15T10:30:00Z"
    }
  ]
}
```

`GET /sessionRecording/{id}` (retrieve). Session replay requires a **Business** plan or higher.

---

## Resource: Workflows (statuses)

Workflows model the feedback status columns (board view). Fields: `id`, `name`, `sort`,
`color` (hex `#RRGGBB`), nested `Project`.

```json
{
  "data": [
    {
      "id": 12,
      "name": "In Progress",
      "sort": 2,
      "color": "#3366FF",
      "Project": { "id": 4455, "name": "My Project", "url": "https://myproject.com", "logo": "...", "isArchived": false, "created": "2024-01-15T10:30:00Z", "createdBy": 1234 }
    }
  ]
}
```

Endpoints: `POST /workflow` (create), `GET /workflow` (list), `PATCH /workflow/{id}`
(update), `DELETE /workflow/{id}`.

---

## Webhooks

Configure under **Connect → Webhooks → Connect** in your Userback project; add an endpoint
URL and use the built-in test feature. **Requires Business Plus.**

**Events**
- Feedback: new submission, assignment change, status update, priority change, vote change, deletion.
- Comment: new comment, edit, status change, removal.

**Request headers**
- `Content-Type: application/json; charset=utf-8`
- `User-Agent: Userback-Webhook`

**Payload shape**

```json
{
  "action": "create",          // create | update | remove
  "type": "feedback",          // feedback | comment
  "data": { /* entity details */ },
  "timestamp": 1705312200,      // Unix epoch
  "url": "https://app.userback.io/..."  // link to the entity in Userback
}
```

> **Security gotcha:** Userback's webhook docs do **not** document an HMAC signature secret.
> Treat the endpoint as unauthenticated — keep the URL secret, verify the `User-Agent`,
> and (best practice) re-fetch the entity via the REST API using `data.id` rather than
> trusting the payload body. <!-- Constructed guidance: no signature scheme is documented. -->

---

## MCP Server

- **Endpoint:** `https://mcp.userback.io/v1/mcp/` (HTTP transport, **OAuth** auth)
- **~12 tools:** feedback create/update, commenting, log retrieval, project/workflow
  management, user listings, semantic + filtered feedback search, status assignment.
- Auto-loads context: feedback details, comments, project/workflow info, console logs, and
  network logs — no manual ID copying.

**Claude Code**
```bash
claude mcp add Userback https://mcp.userback.io/v1/mcp/ -t http -s user
```

**Cursor / VS Code / Windsurf** — add an HTTP MCP server:
```json
{ "mcpServers": { "userback": { "url": "https://mcp.userback.io/v1/mcp/" } } }
```

**Claude (desktop/web):** add a custom web connector (requires Team/Business/Enterprise plan
+ org admin). **ChatGPT:** connect via the GPT Store. All clients use browser-based OAuth on
first use.

---

## JavaScript SDK (widget control)

The widget is installed with an **access token** (Project Settings). The SDK gives
programmatic control. Most SDK methods require a **Business** plan or higher.

```html
<script>
  (function(d){var s=d.createElement('script');s.async=true;
   s.src='https://static.userback.io/widget/v1.js';
   s.onload=function(){Userback.init('<ACCESS_TOKEN>');};
   d.head.appendChild(s);})(document);
</script>
```

**Identify the logged-in user** (so feedback is attributed):
```javascript
Userback.identify('123456', {
  name: 'Jane Doe',
  email: 'jane.doe@example.com',
  plan: 'Enterprise'
});
```

**Widget control & forms**
```javascript
Userback.showLauncher();     // show feedback button
Userback.hideLauncher();     // hide it
Userback.openForm('bug', 'screenshot');   // open a specific form
```

**Surveys**
```javascript
Userback.openSurvey('YOUR_SURVEY_ID');
Userback.closeSurvey();
```

**Session replay**
```javascript
Userback.startSessionReplay(options);
Userback.stopSessionReplay();
```

**Custom events & data**
```javascript
Userback.addCustomEvent('account_upgrade', { details: '...' });
Userback.setData({ orgId: 'acme', mrr: 4200 });   // call multiple times to update
```

The `widget_settings` object customizes language, theme, position, button styling, and
form-field visibility across general/bug/feature forms.

Framework packages: `@userback/widget` (npm), plus React, Vue, Next.js, and Angular guides.
Mobile SDKs (iOS/Android) require **Business Plus**.

---

## Common use cases (from docs)

- **Automate repetitive tasks** — organize feedback, set tags, or assign based on state;
  validate required fields before processing.
- **React to changes in real time** — event-driven "when this feedback changes, do X" via
  webhooks.
- **Custom reports** — pull data to track counts, workload distribution, status-change
  frequency, feature-level sentiment.
- **Sync across tools** — keep Userback consistent with other systems via Zapier or custom
  connectors.
- **Centralize collection** — import feedback from email, Zendesk, and direct submissions
  into one workspace.
- **Trigger actions on resolution** — when status → resolved, notify the reporter or create
  a follow-up task.

## Gaps

- Exact rate-limit numbers are not published (treat `429` as the backoff signal).
- Webhook signature/HMAC scheme is not documented.
- Per-endpoint full request/response schemas for update/delete and members live in the
  per-endpoint reference pages at `https://docs.userback.io/reference`.
