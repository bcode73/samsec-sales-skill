<!-- Source: https://api.wave.co/ and https://api.wave.co/v1/openapi.json -->

# Wave API Reference

## Base information

- **Version**: 1.0.0
- **Base URL**: `https://api.wave.co/v1/`
- **Authentication**: Bearer token in `Authorization` header
- **Token format**: `wave_api_...`
- **Token creation**: `app.wave.co/settings/integrations/api`
- **Token expiry**: 1 year (can be revoked anytime)
- **OpenAPI spec**: `https://api.wave.co/v1/openapi.json`

## API scopes

| Scope | Access |
|---|---|
| `sessions:read` | List sessions, get metadata, stats, bulk export |
| `sessions:write` | Update title, notes, tags, favorite status, action items |
| `sessions:delete` | Permanently remove sessions |
| `sessions:search` | Semantic search across sessions |
| `folders:write` | Create folders; add/remove sessions from folders |
| `events:read` | Pull and acknowledge the per-token event feed |
| `transcripts:read` | Full transcripts with speaker attribution and timestamps |
| `media:read` | Signed audio/video URLs (expire after 1 hour) |
| `account:read` | Profile, subscription status, session count |
| `webhooks:manage` | Create, list, update, delete, test webhook endpoints |

## Rate limits

- **60 requests per minute** per token
- **10,000 requests per day** per token
- Higher limits are available for production integrations on request.
- Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Exceeding limits returns `429 rate_limit_exceeded`

## Sessions endpoints

### List sessions
```
GET /v1/sessions
```
Scope: `sessions:read`
Cursor pagination. Filter by type, date range.

### Get session
```
GET /v1/sessions/{id}
```
Scope: `sessions:read`
Returns metadata, summary, notes.

### Update session
```
PATCH /v1/sessions/{id}
```
Scope: `sessions:write`
Update title, notes, tags, favorite status, and structured action items. Supports an `If-Match` header for optimistic concurrency control — useful when agents write back action items extracted from a session so users can edit them.

### Get action items
```
GET /v1/sessions/{id}/action-items
```
Scope: `sessions:read`
Returns the session's structured action items with version tracking for optimistic concurrency. Action items can be written back via `PATCH /v1/sessions/{id}` (`sessions:write`).

### Delete session
```
DELETE /v1/sessions/{id}
```
Scope: `sessions:delete`
Permanently removes session and all associated data.

### Semantic search
```
POST /v1/sessions/search
```
Scope: `sessions:search`
Vector similarity search across all sessions. Send a natural-language query, get ranked results.

### Session statistics
```
GET /v1/sessions/stats
```
Scope: `sessions:read`
Aggregated statistics (default: last 30 days).

### Bulk export
```
POST /v1/sessions/bulk
```
Scope: `sessions:read`
Export up to 50 sessions by ID in a single request. Pass `include_transcript: true` to include transcripts/summaries.

## Folders

Folders are non-exclusive — a single session can sit in many folders at once (Gmail-labels model). Filter the session list with `GET /v1/sessions?folder=<id|name>` (or `?tag=<name>`).

### List / create folders
```
GET /v1/folders
POST /v1/folders
```
Scope: `folders:write` (create)

### Add / remove session from folder
```
POST /v1/sessions/{id}/folders/{folderId}
DELETE /v1/sessions/{id}/folders/{folderId}
```
Scope: `folders:write`

## Event feed

A pull-based alternative to webhooks. Wave tracks a per-token cursor server-side so you can poll for changes without registering an endpoint.

### List events
```
GET /v1/events
```
Scope: `events:read`
Returns events since the token's current cursor.

### Acknowledge events
```
POST /v1/events/ack
```
Scope: `events:read`
Advances the cursor (monotonic) past acknowledged events.

## Transcripts & media

### Get transcript
```
GET /v1/sessions/{id}/transcript
```
Scope: `transcripts:read`
Full transcript with speaker segments and timestamps.

### Get media
```
GET /v1/sessions/{id}/media
```
Scope: `media:read`
Returns signed URLs for audio and video files. **URLs expire after 1 hour** — download immediately, don't cache URLs.

## Account

### Get account
```
GET /v1/account
```
Scope: `account:read`
Returns user profile, subscription status, and session count.

## Webhooks

Register HTTPS endpoints to receive real-time notifications when sessions are completed, updated, or deleted.

### List webhooks
```
GET /v1/webhooks
```
Scope: `webhooks:manage`

### Create webhook
```
POST /v1/webhooks
```
Scope: `webhooks:manage`
Maximum 5 webhooks per user. Returns signing secret **once** — store it immediately.

### Update webhook
```
PATCH /v1/webhooks/{id}
```
Scope: `webhooks:manage`
Update URL, events, or active status.

### Delete webhook
```
DELETE /v1/webhooks/{id}
```
Scope: `webhooks:manage`

### Rotate signing secret
```
POST /v1/webhooks/{id}/rotate-secret
```
Scope: `webhooks:manage`
Regenerate the HMAC signing secret.

### Test webhook
```
POST /v1/webhooks/{id}/test
```
Scope: `webhooks:manage`
Send a test event and report delivery status.

## Webhook events

| Event | Fires when |
|---|---|
| `session.completed` | A session finishes processing (summary, notes, and tags are queryable) |
| `session.updated` | Session metadata is modified (title, notes, tags) |
| `session.action_items.updated` | Action items are written or edited; payload carries the full session with the new items |
| `session.deleted` | A session is permanently deleted |

## Webhook signature verification

Payloads are signed with HMAC-SHA256. Three headers are included:

| Header | Contents |
|---|---|
| `X-Wave-Webhook-Id` | Unique event ID (for idempotency) |
| `X-Wave-Webhook-Timestamp` | Unix timestamp |
| `X-Wave-Webhook-Signature` | HMAC-SHA256 signature |

**Verification formula:**
```
signature = HMAC-SHA256(secret, "{webhookId}.{timestamp}.{body}")
```

Compare the computed signature against `X-Wave-Webhook-Signature` using a timing-safe comparison.

## Error codes

| Code | HTTP Status | Meaning |
|---|---|---|
| `invalid_request` | 400 | Missing or invalid parameters |
| `unauthorized` | 401 | Missing or malformed Authorization header |
| `invalid_token` | 401 | Token invalid, expired, or revoked |
| `insufficient_scope` | 403 | Token lacks required permission for this endpoint |
| `not_found` | 404 | Resource does not exist |
| `limit_exceeded` | 400 | Resource limit reached (e.g., max 5 webhooks) |
| `rate_limit_exceeded` | 429 | Too many requests — check rate limit headers |
| `internal_error` | 500 | Server-side error — retry with backoff |

## MCP server & CLI

Wave provides an MCP server at `mcp.wave.co` for integration with Claude Desktop, Claude Code, and ChatGPT. Paste `mcp.wave.co` into your client's Connectors UI, sign in via browser OAuth, and it's connected. Allows AI assistants to search and query Wave recordings directly.

There is also a CLI: `npm install -g @waveai/cli`. It uses browser OAuth login, tab-completes every command, and supports `--json` output designed to be piped.
