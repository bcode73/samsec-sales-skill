<!-- Source: https://docs.meetjamie.ai/llms-full.txt (full docs JS-rendered, extracted from LLM-optimized index) -->
<!-- Last fetched: 2026-04-17; re-verified 2026-06-13 -->

# Jamie API Reference

## Base URL

```
https://beta-api.meetjamie.ai
```

(The API is in beta; the host carries a `beta-api` prefix.)

## Authentication & API Access

Jamie provides programmatic access through REST/RPC-style APIs with two key types:

- **Personal API Keys** (`/v1/me/` routes): Access your own meetings plus shared ones. Supports semantic search and tag management.
- **Workspace Keys** (`/v1/workspace/` routes): Requires admin creation; accesses all workspace meetings and enables user-email filtering.

Both use simple header authentication: `x-api-key: jk_your_key`. Rate limits are 100 requests/minute per user (personal) or workspace (workspace key). Rate-limit headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`; exceeding the limit returns `429 Too Many Requests`.

API key generation: Jamie app → Settings → Developers → API Keys. All keys start with the `jk_` prefix. API access requires a Pro, Team, or Enterprise plan.

## Core API Endpoints

Endpoints use an RPC-style naming convention (`resource.action`). Reads are `GET`; deletes are `POST`. Each is available under the personal (`/v1/me/`) and/or workspace (`/v1/workspace/`) prefix.

**Meetings:**
- `GET /v1/me/meetings.list` / `GET /v1/workspace/meetings.list` — retrieve paginated meetings (both key types)
- `GET /v1/me/meetings.get` / `GET /v1/workspace/meetings.get` — get single meeting details (both key types); response includes summary (Markdown/HTML), full transcript, participants, tasks, tags, and calendar event details
- `POST /v1/me/meetings.delete` / `POST /v1/workspace/meetings.delete` — permanently delete a meeting (both key types)
- `GET /v1/me/meetings.search` — semantic search across meetings (**personal keys only**)

**Tasks:**
- `GET /v1/me/tasks.list` / `GET /v1/workspace/tasks.list` — query action items extracted from meetings (both key types)
- Filter by completion status, date range, assignee, or specific meeting

**Tags:**
- `GET /v1/me/tags.list` — list your available tags (**personal keys only**)
- Filter meetings by tag in list operations

### Request & response format

- **Reading data:** `GET` with optional query input — `?input={"json": { ... }}`
- **Deleting:** `POST` with JSON body — `{"json": { ... }}`
- **Response envelope:** all responses are wrapped — actual data is at `result.data.json`.
- **Pagination:** list endpoints return a `nextCursor` field; pass it on the next request for the following page.

### Error codes

`200` success · `400` bad request (invalid params/malformed dates) · `401` unauthorized (missing/invalid key) · `403` forbidden (wrong key type / insufficient access) · `404` not found · `429` rate limited · `500` server error (retry recommended).

## Webhook Integration

Webhooks enable real-time notifications when meetings complete. Configuration requires:

- HTTPS endpoint (HTTP unsupported)
- Plus plan or higher
- Choice between **API Key** authentication or **HMAC-SHA256 signature verification**

The `meeting.completed` event delivers summary, transcript, participants, tasks, and calendar attendee data.

### Webhook limits

- Personal: **3 webhooks per user**
- Workspace: **5 webhooks per workspace**
- Each webhook is scoped Personal or Workspace at creation.

### Webhook headers

Webhook requests include the following headers (exact names):
- `Content-Type: application/json`
- `user-agent: Jamie-Webhooks/1.0`
- `jamie-event: meeting.completed` — event type identifier
- `jamie-delivery: <delivery id>` — delivery identifier
- Authentication header (API key or HMAC signature depending on configuration)

### Authentication methods

**API Key**: Jamie sends a static API key in a header of your choice. Default header name is `x-jamie-api-key`; common alternatives are `x-make-apikey` or `Authorization`. Verify by comparing the header value against your stored secret.

**HMAC-SHA256 signature**: Jamie signs each request with HMAC-SHA256. The signature is sent in the `x-jamie-signature` header with the format:

```
x-jamie-signature: t=<timestamp>,v0=<signature>
```

To verify:
1. Extract `t` (timestamp) and `v0` (signature) from the header.
2. Reject the request if the timestamp is more than 5 minutes old (replay protection).
3. Reconstruct the signed message as `{timestamp}.{raw_body}` (raw, un-parsed body).
4. Compute HMAC-SHA256 over that message with your signing secret.
5. Compare to `v0` using a constant-time comparison.

### Payload structure

```json
{
  "metadata": { "id": "<delivery-id>", "event": "meeting.completed", "created": 1701234567 },
  "data": {
    "title": "string",
    "startTime": "ISO 8601",
    "endTime": "ISO 8601",
    "user": { "id": "...", "email": "..." },
    "summary": { "markdown": "...", "html": "...", "short": "..." },
    "transcript": [{ "speakerId": "...", "speakerName": "...", "text": "..." }],
    "participants": [{ "id": "...", "name": "...", "email": "..." }],
    "event": { "id": "...", "externalId": "...", "title": "...", "scheduledTime": "...", "endTime": "...", "attendees": [] },
    "tasks": [{ "content": "...", "completed": false, "assignee": "..." }],
    "tags": [{ "name": "...", "color": "..." }]
  }
}
```

### Delivery behavior

- Timeout: 30 seconds
- Success: requires 2xx HTTP status code
- Retries: up to 5 attempts with exponential backoff — immediate, then 10s, 60s, 10m, 1h
- After 5 failures: delivery is dead-lettered and an email notification is sent (rate-limited to 1/hour per endpoint)

### Webhook management

- Create: Jamie Settings → Integrations → Webhooks → Create Webhook
- URL and events cannot be updated after creation — delete and recreate if changes needed
- Regenerating the signing secret immediately invalidates the old one — update your receiving endpoint first
- Selected events are immutable after webhook creation

## Enterprise Features

- **SSO**: Microsoft Entra ID and Google Workspace supported
- **Team Sharing**: Share full meetings with workspace members
- **Admin Controls**: System-level access restrictions, verified domain management
- **Integrations**: CRM (HubSpot, Salesforce, Attio), note-taking (Notion, Google Docs, OneNote), task management (Asana), and AI tools via MCP protocol

## MCP / Agent

Jamie now ships a **native Agent** (Settings → Agent) that uses MCP to connect AI tools to your meeting data — the docs describe MCP as the "industry-standard way to connect AI tools (Claude, ChatGPT, Cursor) to your data." The Agent can also use MCP connectors to outbound services (Slack, Notion, Linear, GitHub, etc.), enabled per chat session. Native AI-assistant/MCP access is a Pro+ feature.

A **community-built MCP server** also exists: `vicampuzano-jamie-mcp`

Installation: `npx -y vicampuzano-jamie-mcp`
Environment variable: `JAMIE_API_KEY=jk_your_key`
Requirements: Pro, Team, or Enterprise plan (API key required)

Capabilities: List meetings, read summaries/transcripts, search across meetings, manage tasks.

## SDKs

No official SDKs are documented. Settings → Developers includes a visual Request Builder for constructing endpoint calls.
