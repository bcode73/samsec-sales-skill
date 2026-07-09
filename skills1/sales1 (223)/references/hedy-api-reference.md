<!-- Source: https://www.hedy.ai/help/hedy-api/ + https://www.hedy.ai/integrations/ + https://www.hedy.ai/help/webhooks/ -->
<!-- Re-verified 2026-06-13 against live docs above. Full SwaggerHub docs + raw OpenAPI at https://api.hedy.bot/v1/docs (could not WebFetch). -->

# Hedy API Reference

## Base URL

- **US**: `https://api.hedy.bot` (v1 paths under `/v1`)
- **EU**: `https://eu-api.hedy.bot` — EU data residency option; same endpoints

Pick the regional host that matches your account's data residency.

## Authentication

Include API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

Generate API keys from Hedy Settings → API Access.

**Requires Pro subscription.**

## Rate Limits

200 requests per minute per API key.

## Pagination

List endpoints support cursor pagination:
- `limit` — page size, default 50, max 100
- `after` — cursor for the next page

## Endpoints

### Sessions

- `GET /sessions` — List and retrieve meeting sessions with transcripts and summaries
- `GET /sessions/{id}` — Retrieve a specific session's details

### Highlights

- `GET /highlights` — Retrieve important moments with AI-generated insights

### Topics

- `GET /topics` — List all topics with insights and session counts
- `GET /topics/{id}` — Retrieve a specific topic's details
- `POST /topics` — Create a topic (body: `name`, `description`, `color`, `icon`)
- `PATCH /topics/{id}` — Update topic properties or custom context
- `DELETE /topics/{id}` — Delete a topic
- `GET /topics/{id}/sessions` — List sessions within a topic

Topics support custom context instructions up to 20,000 characters.

### Todos

- `GET /todos` — Retrieve action items across sessions

### Session Contexts

- `GET /contexts` — List session contexts
- `GET /contexts/{id}` — Retrieve a specific session context
- `POST /contexts` — Create a session context (body: `title`, `content`)
- `PATCH /contexts/{id}` — Update a session context
- `DELETE /contexts/{id}` — Delete a session context

Free tier is limited to 1 session context.

### Webhooks

- `GET /webhooks` — List webhooks
- `POST /webhooks` — Create a webhook
- `DELETE /webhooks/{id}` — Delete a webhook

### User

- `GET /me` — Retrieve account details

## Webhooks

### Event Types

| Event | When it fires | Payload contains |
|---|---|---|
| `session.created` | Recording starts | Session title, start time |
| `session.ended` | Recording finishes | Full session data: transcript, recap, meeting minutes, highlights, topic info, speaker-by-speaker conversations |
| `session.exported` | Manual session export | Transcript, recap, highlights |
| `highlight.created` | Highlight captured during session | Highlight text, AI insight, timestamp |
| `todo.exported` | Action item exported | Todo text, due date, associated session |

### Payload Format

All webhooks send HTTP POST requests with JSON body.

`session.ended` payloads contain:
- Session details (title, times, duration)
- Full transcript text
- Speaker-by-speaker conversations
- Meeting minutes
- AI-generated recap
- Highlights with insights and timestamps
- Topic assignment and insights (if applicable)

### Security

Every webhook request includes:
- `X-Hedy-Signature` header — raw, hex-encoded HMAC-SHA256 hash of the request body, signed with your webhook's unique secret (no `sha256=` prefix in the value)
- `X-Hedy-Event` header — event type identifier

HTTPS required for all webhook URLs.

### Limits

- Maximum 10 webhooks per account
- Requires Pro subscription
- Cloud sync must be enabled

### Retry Policy

- Server errors (5xx): retried up to 2 times with increasing delays
- Rate limited (429): retried once, respecting retry timing
- Client errors (4xx): not retried

### Setup

1. Settings → API Access → Manage Webhooks
2. Click **+** to create new webhook
3. Enter optional name and HTTPS URL
4. Choose events to subscribe to
5. Confirm creation

Use built-in test function in Settings → API Access to verify webhook functionality.

## MCP Server

- **Endpoint**: `https://api.hedy.bot/mcp` (US) or `https://eu-api.hedy.bot/mcp` (EU)
- **Auth**: OAuth 2.1 with PKCE — browser sign-in, no static API key to rotate
- **Compatible clients**: direct OAuth support in Claude Desktop, Claude Code, Cursor, Windsurf, Zed, Cline, Perplexity (paid), plus web-based platforms; clients needing a local server can use the open-source `mcp-remote` bridge
- **18 tools** across 5 categories:
  - **Sessions**: view sessions, retrieve details, see highlights, list action items
  - **Highlights**: browse all highlights, get full context for any moment
  - **Tasks**: see all action items across meetings
  - **Topics**: view, create, update, remove topics
  - **Session Contexts**: list, view, create, update, remove contexts
- **Permissions**: can organize topics and contexts, cannot delete recordings or transcripts
- **Requires**: Pro subscription + cloud sync enabled
