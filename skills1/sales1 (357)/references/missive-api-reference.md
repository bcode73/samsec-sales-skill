<!-- Source: https://missiveapp.com/docs/developers/rest-api -->
<!-- Source: https://missiveapp.com/docs/developers/rest-api/endpoints -->
<!-- Source: https://missiveapp.com/docs/developers/rest-api/rate-limits -->
<!-- Source: https://missiveapp.com/docs/developers/webhooks -->

# Missive API Reference

## Authentication

Bearer token via `Authorization: Bearer YOUR_API_TOKEN` header.

API tokens are generated in Missive Settings → API (Connect). Tokens are prefixed `missive_pat-` (personal access token). **Requires Productive plan ($24/user/mo) or above** — the docs state: "You need to be part of an organization subscribed to the Productive plan in order to generate API tokens."

```bash
curl https://public.missiveapp.com/v1/organizations \
  -H "Authorization: Bearer missive_pat-YOUR_API_TOKEN"
```

## Base URL

`https://public.missiveapp.com/v1/`

> The web app lives at `mail.missiveapp.com`, but REST API requests must go to `public.missiveapp.com`. Calling `mail.missiveapp.com` will not work for the API.

## Rate Limits

Officially documented (`/docs/developers/rest-api/rate-limits`):
- **5 concurrent requests** at any time
- **300 requests per minute** (5 req/sec)
- **900 requests per 15 minutes** (1 req/sec sustained)

Exceeding any limit returns `429 Too Many Requests` with headers:
- `Retry-After` — seconds to wait before retrying
- `X-RateLimit-Limit` — the applicable ceiling
- `X-RateLimit-Remaining` — requests left in the current window
- `X-RateLimit-Reset` — UTC epoch (seconds) when the window resets

Missive recommends sustained 1 req/sec for continuous querying, or bursts up to 5 req/sec spread over time. Honor `Retry-After`; fall back to exponential backoff on 429.

## Pagination

Uses `limit` and `offset` parameters. Defaults and maximums differ per endpoint:
- Conversations: default `limit` 25, max 50
- Contacts / contact books: default `limit` 50, max 200
- Messages: default `limit` 10, max 10
- Some endpoints use `until` (Unix timestamp) for cursor-based pagination

## Endpoints

### Analytics

| Method | Path | Description |
|---|---|---|
| POST | `/v1/analytics/reports` | Create analytics report |
| GET | `/v1/analytics/reports/:id` | Get analytics report (Productive/Business) |

### Contacts

| Method | Path | Description |
|---|---|---|
| POST | `/v1/contacts` | Create contact(s) |
| PATCH | `/v1/contacts/:id1,:id2,...` | Update contact(s) — comma-separated IDs |
| GET | `/v1/contacts` | List contacts |
| GET | `/v1/contacts/:id` | Get a single contact |

### Contact Books

| Method | Path | Description |
|---|---|---|
| GET | `/v1/contact_books` | List contact books |

### Contact Groups

| Method | Path | Description |
|---|---|---|
| GET | `/v1/contact_groups` | List contact groups / organizations |

### Conversations

| Method | Path | Description |
|---|---|---|
| GET | `/v1/conversations` | List conversations (requires at least one mailbox filter) |
| GET | `/v1/conversations/:id` | Get a single conversation |
| PATCH | `/v1/conversations/:id` | Update conversation(s) silently — close, reopen, move, assign, label, recolor, rename without creating a post |
| GET | `/v1/conversations/:id/messages` | List messages in a conversation |
| GET | `/v1/conversations/:id/comments` | List internal comments on a conversation |
| GET | `/v1/conversations/:id/drafts` | List drafts in a conversation |
| GET | `/v1/conversations/:id/posts` | List posts in a conversation |
| POST | `/v1/conversations/:id/merge` | Merge two or more conversations |

**Mailbox filter (required on list):** pass exactly one of `inbox`, `all`, `assigned`, `closed`, `snoozed`, `flagged`, `trashed`, `junked`, `drafts`, `shared_label`, `team_inbox`, `team_closed`, or `team_all`.

**`PATCH /v1/conversations/:id` parameters:** `subject`, `color`, `conversation_color`, `organization`, `team`, `force_team`, `add_users`, `add_assignees`, `remove_assignees`, `add_shared_labels`, `remove_shared_labels`, `add_to_inbox`, `add_to_team_inbox`, `close`, `reopen`. This is the dedicated silent-update path — no post/message is created.

### Drafts

| Method | Path | Description |
|---|---|---|
| POST | `/v1/drafts` | Create a draft (set `send: true` to send immediately) |
| DELETE | `/v1/drafts/:id` | Delete a draft |

**Key draft parameters:**
- `subject` — email subject
- `body` — HTML body
- `from_field` — `{ "address": "email@example.com" }`
- `to_fields` — array of `{ "address": "..." }`
- `cc_fields`, `bcc_fields` — same format
- `send` — `true` to send immediately
- `send_at` — Unix timestamp for scheduled send
- `conversation` — link to existing conversation ID
- `team` — link draft's conversation to a team
- `add_assignees` — array of user IDs
- `add_labels` — array of label IDs
- `organization` — organization ID
- `close` — `true` to close conversation after sending

### Messages

| Method | Path | Description |
|---|---|---|
| POST | `/v1/messages` | Create incoming custom channel message |
| GET | `/v1/messages/:id` | Get a message |
| GET | `/v1/messages` | List messages (filter by `email_message_id`) |

### Organizations

| Method | Path | Description |
|---|---|---|
| GET | `/v1/organizations` | List organizations the authenticated user belongs to |

### Responses (Canned Templates)

| Method | Path | Description |
|---|---|---|
| GET | `/v1/responses` | List response templates |
| GET | `/v1/responses/:id` | Get a response template |
| POST | `/v1/responses` | Create response template(s) |

**Response template fields:**
- `name` — template name
- `body` — HTML content
- `subject` — optional subject line
- `external_id`, `external_source` — for syncing with external systems

## Webhooks

### Setup

1. Go to Settings → Rules → New Rule
2. Select trigger condition (new message, label change, etc.)
3. Select "Webhook" as the action
4. Paste your endpoint URL
5. Missive validates the endpoint with a test POST request

**Requirements:**
- Productive or Business plan
- Admin/owner role in the organization
- Endpoint must respond within 15 seconds

### Signature Verification

Webhooks include `X-Hook-Signature` header: `sha256={HMAC-SHA256 hexdigest}`.

Verify using:
```python
import hmac, hashlib

def verify_signature(payload_bytes, signature_header, secret):
    expected = "sha256=" + hmac.new(
        secret.encode(), payload_bytes, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature_header, expected)
```

### Retry Behavior

- Failed requests retry up to 5 times over 8 minutes
- Rules auto-disable after 50+ consecutive failures
- Re-enable manually in Rules settings

### Payload Structure

See platform-guide.md for full webhook payload JSON schema.

### Teams

| Method | Path | Description |
|---|---|---|
| GET | `/v1/teams` | List teams |
| POST | `/v1/teams` | Create team(s) |
| PATCH | `/v1/teams/:id` | Update team(s) |

## Conversation Actions

Use `PATCH /v1/conversations/:id` for silent state changes (close/reopen/assign/label/move) — see the Conversations section above for the full parameter list. This is the preferred path when you do NOT want a post or message created.

Alternatively, the drafts endpoint accepts action parameters that take effect when the draft is created/sent (these DO create a message/post):

- `close: true` — close the conversation after sending
- `add_to_inbox: true` — move to inbox
- `add_assignees: [user_ids]` — assign to users
- `add_labels: [label_ids]` / `remove_labels: [label_ids]` — apply/remove labels

## Gaps

- No bulk export endpoint — must paginate through conversations
- Webhook event types not enumerated as a separate list — tied to Rule trigger conditions
- Webhook payload schema documented only via the rule/conversation/latest_message example shape
