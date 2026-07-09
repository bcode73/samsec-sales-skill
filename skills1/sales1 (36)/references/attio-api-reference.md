# Attio API Reference

Quick reference for the Attio REST API. For full documentation, see [docs.attio.com](https://docs.attio.com/).

## Authentication

| Detail | Value |
|---|---|
| Method | OAuth 2.0 / API key (Bearer token) |
| Header | `Authorization: Bearer {access_token}` |
| API key generation | Workspace Settings → Developers → Create integration → Generate token |
| OAuth endpoints | Authorization, token, and introspection endpoints available |

## Base URL

```
https://api.attio.com/v2
```

## Rate Limits

| Operation | Limit |
|---|---|
| Read requests | 100/second |
| Write requests | 25/second |
| Over limit response | HTTP 429 with `Retry-After` header |

**Score-based limits (List records / List entries endpoints):** These two endpoints
(`POST /objects/{object}/records/query` and `POST /lists/{list}/entries/query`) also have
a separate complexity-score limit. Each request is scored by its sorts, filters, and the
total record/entry count. A single overly-complex query can exceed the per-query limit, and
summed scores across queries are throttled with a sliding-window algorithm over a 10-second
window. Scores aggregate across all apps and access tokens using the API. Limits may be
temporarily reduced during incidents or permanently lowered for high-data endpoints.

## Core Endpoints

### Records (People, Companies, Deals, Custom Objects)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/objects/{object}/records/query` | Search/filter records |
| POST | `/objects/{object}/records` | Create a record |
| GET | `/objects/{object}/records/{record_id}` | Get a record |
| PATCH | `/objects/{object}/records/{record_id}` | Update a record |
| DELETE | `/objects/{object}/records/{record_id}` | Delete a record |

### Objects

| Method | Endpoint | Description |
|---|---|---|
| GET | `/objects` | List all objects |
| GET | `/objects/{object}` | Get object schema |
| POST | `/objects` | Create custom object |
| PATCH | `/objects/{object}` | Update object |

### Attributes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/objects/{object}/attributes` | List attributes |
| POST | `/objects/{object}/attributes` | Create attribute |
| PATCH | `/objects/{object}/attributes/{attribute}` | Update attribute |

### Lists

| Method | Endpoint | Description |
|---|---|---|
| GET | `/lists` | List all lists |
| GET | `/lists/{list}` | Get list details |
| POST | `/lists/{list}/entries/query` | Query list entries |
| POST | `/lists/{list}/entries` | Add entry to list |

### Notes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notes` | List notes |
| POST | `/notes` | Create note |
| DELETE | `/notes/{note_id}` | Delete note |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create task |
| PATCH | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

### Comments & Threads

| Method | Endpoint | Description |
|---|---|---|
| GET | `/comments` | List comments |
| POST | `/comments` | Create comment |
| GET | `/threads/{thread_id}` | Get thread |

### Webhooks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/webhooks` | List webhooks |
| POST | `/webhooks` | Create webhook |
| DELETE | `/webhooks/{webhook_id}` | Delete webhook |

### Meetings, Calls & Transcripts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/meetings` | List meetings (beta; scopes `meeting:read` + `record_permission:read`) |
| — | Call recordings | Store video, audio, transcript, and speaker info for calls; linked to meetings |
| — | Transcripts | Speech segments + speaker info for a call recording; linked to call recordings |

Additional endpoint-reference families exposed by the API include **Files**, **Workspaces**,
**Workspace Members**, **Meta** (self/identity), and **SCIM** (Groups, Users, Schemas) for
enterprise provisioning. See the OpenAPI spec or `docs.attio.com/llms.txt` for the full list.

## Webhook Events

| Category | Events |
|---|---|
| Records | `record.created`, `record.updated`, `record.deleted`, `record.merged` |
| Lists | `list.created`, `list.updated`, `list.deleted` |
| List entries | `list-entry.created`, `list-entry.updated`, `list-entry.deleted` |
| List attributes | `list-attribute.created`, `list-attribute.updated` |
| Object attributes | `object-attribute.created`, `object-attribute.updated` |
| Notes | `note.created`, `note.updated`, `note.deleted` |
| Note content | `note-content.updated` |
| Comments | `comment.created`, `comment.deleted`, `comment.resolved`, `comment.unresolved` |
| Tasks | `task.created`, `task.updated`, `task.deleted` |
| Workspace members | `workspace-member.created` |
| Call recordings | `call-recording.created` |

**Note:** Attribute events are split into two families — `list-attribute.*` (attributes on a
list) and `object-attribute.*` (attributes on an object). There is no generic `attribute.*`
event. Comments use `comment.resolved`/`comment.unresolved` (not `comment.updated`). The
deprecated v1 events `entry.created`, `entry.deleted`, and `entry-attribute.updated` still
fire but should be migrated to their v2 `list-entry.*` equivalents.

## Webhook Signing & Delivery

| Detail | Value |
|---|---|
| Signature header | `Attio-Signature` (also sent as `X-Attio-Signature` for legacy clients) |
| Algorithm | SHA256 HMAC of the raw request body, keyed with the webhook secret; hex-encoded |
| Secret source | Shown in developer settings and in the API response when the webhook is created |
| Verification | Use a timing-safe comparison against the recomputed HMAC |
| Success codes | 2xx (200–299); anything else is a failed delivery |
| Timeout | 5 seconds per request to the target URL |
| Retries | Up to 10 attempts with exponential back-off over ~3 days; then marked degraded + email alert |
| Delivery | At-least-once; `Idempotency-Key` header distinguishes unique messages from retries |
| Per-URL rate | Up to 25 requests/second to a single target URL |

## SDKs

Attio does **not** publish official REST-API client libraries. The only official SDK is the
**App SDK** (TypeScript & React) for building embedded apps inside Attio — it is not a REST
client. For programmatic REST access, call the JSON API directly or use a community library.

| Library | Type | Languages |
|---|---|---|
| App SDK | Official — embedded React apps (not a REST client) | TypeScript, React |
| `attio-js` (d-stoll/attio-js) | Community-maintained REST client (beta) | JavaScript, TypeScript |

The Attio GitHub org (`github.com/attio`) hosts docs and React component repos but no
official Node/Python/PHP/.NET/Java REST SDK. Generate a client from the OpenAPI spec if you
need typed bindings in another language.

## MCP Server

Attio provides an MCP (Model Context Protocol) server for AI agent integration:
- **URL**: `mcp.attio.com/mcp`
- **Capabilities**: Search, update, and manage Attio workspace data via AI agents (Claude, Cursor, etc.)

## Pagination

API responses are paginated. Use `offset` and `limit` parameters for cursor-based pagination.

## Data Formats

- All requests and responses are JSON
- Dates use ISO 8601 format
- IDs are UUIDs
- Objects and attributes can be referenced by slug or ID

## OpenAPI Specification

Machine-readable API spec available at `api.attio.com/openapi` for code generation and tooling.

## Useful Resources

- [Attio Docs](https://docs.attio.com/) — Full API documentation
- [LLMs.txt](https://docs.attio.com/llms.txt) — AI-friendly documentation index
- [App SDK](https://docs.attio.com/sdk) — Build embedded React apps
- [OAuth Guide](https://docs.attio.com/rest-api/guides/authentication) — Set up OAuth flows
