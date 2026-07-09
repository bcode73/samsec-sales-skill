<!-- Source: https://api.app.reclaim.ai/swagger/reclaim-api-0.1.yml (live OpenAPI 3.0.1 spec, publicly downloadable — authoritative), https://help.reclaim.ai/en/articles/10008727-webhooks-for-scheduling-links-overview, https://help.zapier.com/hc/en-us/articles/39428286934413-How-to-get-started-with-Reclaim-AI-on-Zapier, https://apps.make.com/reclaim-ai. Re-verified against the live spec 2026-06-13. -->

# Reclaim.ai API Reference

## Authentication

**Method**: API Key (Bearer token). The OpenAPI spec models this as an OAuth2 `Authorization` security scheme; in practice you pass the developer API key as a bearer token.
**Token location**: `https://app.reclaim.ai/settings/developer`
**Header format**: `Authorization: Bearer {API_KEY}`

```bash
# Quick test — list all tasks
curl "https://api.app.reclaim.ai/api/tasks" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Rate limit**: 100 requests/minute (all plans).

## Base URL

```
https://api.app.reclaim.ai
```

Swagger/OpenAPI spec: `https://api.app.reclaim.ai/swagger/reclaim-api-0.1.yml`

## Endpoints

### Tasks

CRUD lives under `/api/tasks`; **planner actions** (start, stop, complete, snooze, plan-work, log-work, prioritize, reschedule) live under `/api/planner/...`, NOT under `/api/tasks/{id}/...`. Verified against the live OpenAPI spec 2026-06-13.

| Method | Path | Description |
|---|---|---|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get a task by ID |
| DELETE | `/api/tasks/{id}` | Delete a task |
| PUT | `/api/tasks/{taskId}` | Update a task (full replace) |
| PATCH | `/api/tasks/{taskId}` | Update a task (partial) |
| PATCH | `/api/tasks/{taskId}/reindex` | Reindex a task |
| GET | `/api/tasks/at-time` *(POST)* | Tasks at a given time |
| DELETE | `/api/tasks/batch` | Batch delete |
| PATCH | `/api/tasks/batch/archive` | Batch archive |
| PATCH | `/api/tasks/batch/complete` | Batch complete |
| GET | `/api/tasks/min-index` | Min task index |
| PATCH | `/api/tasks/reindex-by-due` | Reindex tasks by due date |
| POST | `/api/recommended-tasks` (GET/related) | Recommended/proactive tasks |

#### Task planner actions (all POST under `/api/planner/`)

| Path | Action |
|---|---|
| `/api/planner/start/task/{taskId}` | Start a task |
| `/api/planner/stop/task/{taskId}` | Stop a task |
| `/api/planner/done/task/{taskId}` | Mark task done/complete |
| `/api/planner/restart/task/{taskId}` | Restart a task |
| `/api/planner/plan-work/task/{taskId}` | Plan work for a task |
| `/api/planner/log-work/task/{taskId}` | Log work on a task |
| `/api/planner/add-time/task/{taskId}` | Add time to a task |
| `/api/planner/prioritize/task/{taskId}` | Prioritize a task |
| `/api/planner/unarchive/task/{taskId}` | Unarchive a task |
| `/api/planner/task/{taskId}/snooze` | Snooze a task |
| `/api/planner/task/{taskId}/clear-snooze` | Clear a task snooze |
| `/api/planner/task/reschedule/bulk` | Bulk reschedule tasks |
| `/api/planner/reschedule/task/event/{eventId}` | Reschedule a task instance |
| `/api/planner/task/{calendarId}/{eventId}/reschedule` | Reschedule a scheduled task event |

### Habits (Daily Habits)

Habits live under `/api/assist/habits/daily`, NOT `/api/habits`. Start/stop/restart/toggle/reschedule/skip actions live under `/api/planner/...`. Verified against the live OpenAPI spec 2026-06-13.

| Method | Path | Description |
|---|---|---|
| GET | `/api/assist/habits/daily` | List all habits |
| POST | `/api/assist/habits/daily` | Create a habit |
| GET | `/api/assist/habits/daily/{id}` | Get a habit by ID |
| PUT | `/api/assist/habits/daily/{id}` | Update a habit (full replace) |
| PATCH | `/api/assist/habits/daily/{id}` | Update a habit (partial) |
| DELETE | `/api/assist/habits/daily/{id}` | Delete a habit |
| POST | `/api/assist/habits/daily/{id}/migrate-to-smart-series` | Migrate habit to a smart series |
| GET | `/api/assist/habits/templates` | List habit templates |

#### Habit planner actions (all POST under `/api/planner/`)

| Path | Action |
|---|---|
| `/api/planner/start/habit/{habitId}` | Start a habit |
| `/api/planner/stop/habit/{habitId}` | Stop a habit |
| `/api/planner/restart/habit/{habitId}` | Restart a habit |
| `/api/planner/toggle/habit/{habitId}` | Toggle habit on/off |
| `/api/planner/done/habit/{habitId}` | Mark a habit instance done |
| `/api/planner/reschedule/habit/event/{eventId}` | Reschedule a habit instance |
| `/api/planner/skip/habit/event/{eventId}` | Skip a habit instance |
| `/api/planner/habit/{calendarId}/{eventId}/reschedule` | Reschedule a scheduled habit event |
| `/api/planner/clear-exceptions/habit/{habitId}` | Clear habit scheduling exceptions |

> **Note**: Reclaim also exposes a newer **Smart Habits** surface at `/api/smart-habits/planner/...` and templates at `/api/templates/smart-habit`. Daily habits can be migrated to smart series via the migrate endpoint above.

### Hours / Time schemes

| Method | Path | Description |
|---|---|---|
| GET | `/api/account-time-schemes` | List time schemes (work hours, meeting hours, etc.) |
| POST | `/api/account-time-schemes` | Create a time scheme |
| PATCH | `/api/account-time-schemes/{accountTimeSchemeId}` | Update a time scheme |

### Events

| Method | Path | Description |
|---|---|---|
| GET | `/api/events` | List events (supports date range filtering) |

### Changelog

| Method | Path | Description |
|---|---|---|
| GET | `/api/changelog` | Combined change feed |
| GET | `/api/changelog/tasks` | Task change feed |
| GET | `/api/changelog/events` | Event change feed |
| GET | `/api/changelog/smart-habits` | Smart-habit change feed |
| GET | `/api/changelog/smart-meetings` | Smart-meeting change feed |
| GET | `/api/changelog/scheduling-links` | Scheduling link change feed |

> Verified against the live spec 2026-06-13: there is no `/api/changelog/habits` or `/api/changelog/meetings` — they are `smart-habits` and `smart-meetings`.

### Webhooks (API-level — manage subscriptions)

Webhook subscriptions are managed under `/api/team/current/webhooks`, NOT `/api/webhooks`. Verified against the live spec 2026-06-13.

| Method | Path | Description |
|---|---|---|
| GET | `/api/team/current/webhooks` | List webhook subscriptions |
| POST | `/api/team/current/webhooks` | Create webhook subscription |
| GET | `/api/team/current/webhooks/{id}` | Get a webhook subscription |
| PUT | `/api/team/current/webhooks/{id}` | Update a webhook subscription |
| DELETE | `/api/team/current/webhooks/{id}` | Delete a webhook subscription |
| GET | `/api/team/current/webhooks/{id}/associations` | List scheduling links attached to a webhook |
| GET | `/api/team/current/webhooks/messages` | List recent webhook delivery messages |
| POST | `/api/team/current/webhooks/messages/retry` | Retry failed webhook deliveries |
| GET | `/api/team/current/webhooks/versions` | List supported webhook API versions |
| GET | `/api/team/webhook/generate-secret` | Generate a signing secret |

## Webhook Events (Scheduling Links)

Available on **Business and Enterprise plans** only.

### Event types

- `SchedulingLink.Meeting.Created` — new meeting booked
- `SchedulingLink.Meeting.Updated` — meeting rescheduled
- `SchedulingLink.Meeting.Cancelled` — meeting cancelled

### Delivery

- **Semantics**: At most once (may in rare cases deliver successfully more than once), with exponential backoff retries
- **Retry-After**: If your response includes a `Retry-After` header, Reclaim honors it instead of the default exponential backoff
- **Timeout**: Must respond 2xx within 10 seconds
- **Suspension**: Endpoint suspended after more than 24 hours of continuous failures
- **Ordering**: Events may arrive out of order

### Headers

| Header | Description |
|---|---|
| `x-reclaim-webhook-type` | Event type identifier |
| `x-reclaim-api-version` | One of `v2024-10-02`, `v2025-01-15`, or `v2025-09-26` (latest). Query supported versions via `GET /api/team/current/webhooks/versions`. |
| `x-reclaim-signature-256` | `sha256=` + base64-encoded HMAC-SHA256 |

### Signature verification (Node.js)

```javascript
import crypto from 'crypto';

function verifySignature(headers, body, secret) {
  const sig = headers['x-reclaim-signature-256'];
  if (!sig) return false;

  const signature = Buffer.from(sig.substring(7)); // strip "sha256="
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(body);
  const hash = Buffer.from(hmac.digest('base64'));

  return signature.length === hash.length &&
    crypto.timingSafeEqual(signature, hash);
}
```

### Custom data passthrough

Scheduling link URLs accept up to 5 `data-` prefixed query parameters (max 512 bytes minified JSON). These flow through to the `custom_data` field in webhook payloads with the `data-` prefix stripped.

Errors: `TRUNCATED` (exceeded 5 params or 512 bytes), `UNSERIALIZABLE` (non-JSON value).

## Webhook Events (Task/Habit — via API)

The API-level webhook subscriptions support additional event types for tasks and habits:
- `TaskWebhookEvent` — task created, updated, completed, deleted
- `HabitWebhookEvent` — habit created, updated, toggled, deleted

These use the same HMAC-SHA256 signature verification.

## Data Models

### Enums

| Enum | Values |
|---|---|
| `PriorityLevel` | `P1` (Critical), `P2` (High), `P3` (Normal), `P4` (Low) |
| `TaskStatus` | `NEW`, `IN_PROGRESS`, `COMPLETE`, `ARCHIVED`, `CANCELLED` |
| `EventCategory` | `WORK`, `PERSONAL` |
| `EventColor` | Calendar color identifiers |

### Duration format

All duration fields use ISO 8601: `PT1H` = 1 hour, `PT30M` = 30 minutes, `PT1H30M` = 1.5 hours.

## Gaps

- No human-readable public API docs page, but the OpenAPI 3.0.1 spec at `https://api.app.reclaim.ai/swagger/reclaim-api-0.1.yml` IS publicly downloadable (~1 MB, 100+ paths) and is the authoritative source — the endpoint tables above were re-verified against it on 2026-06-13
- The spec declares the `Authorization` security scheme as `type: oauth2` but does not expose the flow/token URLs; the developer API key is used as a bearer token in practice
- Pagination pattern for list endpoints not fully documented — note `/api/reclaim-tasks/page` and `/api/events/v2` suggest paged variants exist for some resources
- Error response shapes (4xx/5xx) not documented
- Focus Time, Buffer Time, Smart Meetings, and Calendar Sync have no API endpoints — UI-only configuration
- SCIM endpoints exist at `https://api.app.reclaim.ai/scim/v2` for Enterprise SSO provisioning (separate from main API)

## iPaaS Surface

### Zapier

| Type | Name | Description |
|---|---|---|
| Action | Create Task | Create a new task with title, due date, priority, duration, category, notes |
| Action | API Request (Beta) | Raw HTTP request with Reclaim auth — access any endpoint |

No Zapier triggers available.

### Make (Integromat)

| Module | Description |
|---|---|
| Create a Task | Create task with full field configuration |
| Get a Task | Retrieve task by ID |
| List Tasks | List all tasks |
| List Events | List events with date range filter |
| Make an API Call | Custom API request with auth |

No Make triggers/watchers available.
