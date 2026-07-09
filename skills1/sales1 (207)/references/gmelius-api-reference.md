<!-- Source: https://developers.gmelius.com/ -->

# Gmelius API Reference

## Base URL

`https://api.gmelius.com/public/v2`

## Authentication

OAuth 2.0 with OpenID Connect 1.0 and PKCE.

**Authorization URL**: `https://app.gmelius.com/oauth/authorize`
**Token endpoint**: `POST https://api.gmelius.com/public/v2/token`
**Token introspection**: `POST https://api.gmelius.com/public/v2/token/introspection`
**Token revocation**: `POST https://api.gmelius.com/public/v2/token/revocation`

Parameters:
- `client_id` — your app's client ID
- `redirect_uri` — registered callback URL
- `code_challenge` — PKCE challenge
- `scope` — space-separated scope list

**Token lifecycle**:
- Access token: expires after 1 hour
- Refresh token: valid for 60 days, renew at 30-day mark

**Plan requirement**: API access requires Growth plan ($25/user/mo) or above. Admin/manager credentials required. (Note: Gmelius developer docs phrase access as "restricted to Growth and Enterprise plans" — the live pricing page lists "Most Integrations + API" starting at Growth, so Growth/Pro/Enterprise all have API access.)

## Scopes

| Scope | Description |
|---|---|
| `https://api.gmelius.com/public/auth/boards/read` | Read board access |
| `https://api.gmelius.com/public/auth/boards/modify` | Read/write board access |
| `https://api.gmelius.com/public/auth/conversations/read` | Read conversations |
| `https://api.gmelius.com/public/auth/conversations/metadata` | Modify conversation metadata (assign, tag, status) |
| `https://api.gmelius.com/public/auth/conversations/insert` | Reply to and draft conversations |
| `https://api.gmelius.com/public/auth/sequences/enroll` | Manage sequence enrollments |
| `offline_access` | Obtain tokens without user interaction |

## Response format

All responses follow this structure:
```json
{
  "meta": {"status": 200, "code": "Ok"},
  "data": {}
}
```

## Endpoints

### Boards

| Method | Path | Description |
|---|---|---|
| GET | `/auth/boards` | List user's boards |
| POST | `/auth/boards` | Create board |
| GET | `/auth/boards/{id}` | Retrieve board |
| PUT | `/auth/boards/{id}` | Update board |
| DELETE | `/auth/boards/{id}` | Delete board |

### Board Columns

| Method | Path | Description |
|---|---|---|
| GET | `/auth/boards/{id}/columns` | List columns |
| POST | `/auth/boards/{id}/columns` | Create column |
| GET | `/auth/boards/columns/{id}` | Get column details |
| PATCH | `/auth/boards/columns/{id}` | Update column |
| DELETE | `/auth/boards/columns/{id}` | Delete column |

### Board Cards

| Method | Path | Description |
|---|---|---|
| GET | `/auth/boards/columns/{id}/cards` | List cards in column |
| POST | `/auth/boards/columns/{id}/cards` | Create card in column |
| GET | `/auth/boards/cards/{id}` | Get card details (`?format=minimal\|full`) |
| PATCH | `/auth/boards/cards/{id}` | Update card (subject, snippet, due_date, status, assignee_email) |
| DELETE | `/auth/boards/cards/{id}` | Delete card |
| POST | `/auth/boards/cards/{id}/tags` | Create tag on card |
| DELETE | `/auth/boards/cards/{id}/tags/{tag_id}` | Delete card tag |

**Pagination for cards**:
- `limit` (query, number): defaults to 50
- `from` (query, number): pagination start point
- `vri` (query, number): vertical row index (0 or 1)

### Conversations

| Method | Path | Description |
|---|---|---|
| GET | `/auth/shared-folders` | List user's shared folders |
| GET | `/auth/shared-folders/{id}` | Get shared folder |
| GET | `/auth/shared-folders/{id}/conversations` | List conversations in shared folder |
| GET | `/auth/conversations/{id}` | Get conversation |
| POST | `/auth/conversations/{id}/notes` | Create note on conversation |
| POST | `/auth/conversations/{id}/reply` | Reply to conversation |
| POST | `/auth/conversations/{id}/drafts` | Create draft on conversation |
| POST | `/auth/conversations/{id}/tags` | Add tag to conversation |
| POST | `/auth/conversations/{id}/assign` | Assign conversation |
| PATCH | `/auth/conversations/{id}/status` | Update conversation status |

### Notes & Tags (metadata)

| Method | Path | Description |
|---|---|---|
| POST | `/auth/notes` | Create note |
| PATCH | `/auth/notes/{id}` | Update note |
| DELETE | `/auth/notes/{id}` | Delete note |
| PATCH | `/auth/tags/{id}` | Update tag |

### User

| Method | Path | Description |
|---|---|---|
| GET | `/me` | Get authenticated user info |

### Sequences

| Method | Path | Description |
|---|---|---|
| GET | `/auth/sequences` | List user's sequences |
| GET | `/auth/sequences/{id}` | Get sequence details |
| POST | `/auth/sequences/{id}/enroll` | Enroll contact in sequence |
| POST | `/auth/sequences/{id}/disenroll` | Disenroll contact |

### Webhooks (Pro plan required)

| Method | Path | Description |
|---|---|---|
| GET | `/auth/webhooks` | List all webhooks |
| POST | `/auth/webhooks` | Create webhook |
| GET | `/auth/webhooks/{id}` | Get webhook |
| GET | `/auth/webhooks/{id}/events` | List webhook events |
| DELETE | `/auth/webhooks/{id}` | Delete webhook |

## Data Models

### SharedFolder
### User
### Conversation
### Note
### Tag
### Board
### Column
### Card
### Sequence
### SequenceVariable

## Rate Limits

Rate limits are referenced in documentation but specific values are not publicly documented. Implement exponential backoff on 429 responses.

## Gaps

- Webhook payload schema not documented in public API docs — test with real events to capture shapes
- Rate limit specific values (requests/minute, burst limits) not documented
- Conversation search/filter parameters not documented beyond folder listing
- Meli AI assistant has no API surface — all AI features are UI-only
