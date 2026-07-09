<!-- Source: https://developer.calendly.com/api-docs, https://developer.calendly.com/schedule-events-with-ai-agents, https://developer.calendly.com/frequently-asked-questions, https://calendly.com/blog/api-dev-portal, https://community.calendly.com/api-webhook-help-61/scheduling-api-now-available-4825, https://community.calendly.com/api-webhook-help-61/new-event-type-management-apis-4109 -->
<!-- Re-verified 2026-06-13 against live official docs. -->
<!-- MAJOR UPDATE: Calendly now has a Scheduling API (POST /invitees) that CREATES bookings, plus write endpoints for event types and availability schedules. The old "API is read-only / cannot create bookings" framing is OBSOLETE. -->


# Calendly API Reference

## Base URL

```
https://api.calendly.com
```

API v2 (current, actively maintained). API v1 deprecated August 2025.

## Authentication

Two methods:

### Personal Access Token (internal apps)
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.calendly.com/users/me
```
Generate at: Settings → Integrations → API & Webhooks → Personal Access Tokens

### OAuth 2.0 (public apps)
- Authorization: `https://auth.calendly.com/oauth/authorize`
- Token exchange: `https://auth.calendly.com/oauth/token`
- Access tokens expire after **2 hours** — use refresh tokens
- Scopes: determined by Calendly subscription tier, not per-token

```bash
# Token exchange
curl -X POST https://auth.calendly.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=YOUR_REDIRECT&client_id=CLIENT_ID&client_secret=CLIENT_SECRET"
```

## Rate Limits

| Plan | Limit |
|---|---|
| Free | 60 requests/minute |
| Standard | 60 requests/minute |
| Teams | 60 requests/minute |
| Enterprise | 120 requests/minute |

Rate limit headers:
- `X-RateLimit-Limit` — max requests per minute
- `X-RateLimit-Remaining` — requests remaining
- `X-RateLimit-Reset` — UTC epoch seconds until reset

On 429 Too Many Requests: honor `Retry-After` header (seconds to wait).

> Re-verification note (2026-06-13): the official rate-limits page is JS-rendered and did not yield a clean quote, and third-party guides disagree (some cite 60/min, others ~100/min or per-token figures). Treat the exact per-plan numbers above as approximate and confirm against the live `/api-docs` rate-limits page before building hard throttling logic. The header names and 429/`Retry-After` behavior are corroborated.

## Endpoints

### Users

| Method | Path | Description |
|---|---|---|
| GET | `/users/me` | Get current authenticated user |
| GET | `/users/{uuid}` | Get a specific user |

### Organization

| Method | Path | Description |
|---|---|---|
| GET | `/organization_memberships` | List org members (filter by `organization`) |
| GET | `/organization_memberships/{uuid}` | Get specific membership |

### Event Types

| Method | Path | Description |
|---|---|---|
| GET | `/event_types` | List event types (filter by `user` or `organization`) |
| GET | `/event_types/{uuid}` | Get specific event type |

### Scheduled Events

| Method | Path | Description |
|---|---|---|
| GET | `/scheduled_events` | List scheduled events (filter by `user`, `min_start_time`, `max_start_time`, `status`) |
| GET | `/scheduled_events/{uuid}` | Get specific scheduled event |
| POST | `/scheduled_events/{uuid}/cancellation` | Cancel a scheduled event |

### Invitees

| Method | Path | Description |
|---|---|---|
| GET | `/scheduled_events/{event_uuid}/invitees` | List invitees for an event |
| GET | `/scheduled_events/{event_uuid}/invitees/{invitee_uuid}` | Get specific invitee |

### Scheduling API — Create a booking (NEW)

Calendly's **Scheduling API** lets you book meetings programmatically — no redirects, iframes, or Calendly-hosted UI. This is the **Create Event Invitee** endpoint, introduced after the original API was read-only.

| Method | Path | Description |
|---|---|---|
| POST | `/invitees` | Create a scheduled event by booking an invitee onto an event type at a chosen time |

- **Plan gate:** the target Calendly account must be on a **paid plan** to use the Scheduling API.
- **Auth:** works with a Personal Access Token (book within your own org) or an OAuth app (book on behalf of end-users — recommended for multi-tenant/public apps).
- Calendly handles the standard post-booking actions automatically (calendar invites, confirmations, reminders, notifications).

**Minimum request body:**
```json
{
  "event_type": "https://api.calendly.com/event_types/ETC123",
  "start_time": "2026-07-02T18:30:00Z",
  "invitee": {
    "name": "Alex Prospect",
    "email": "prospect@example.com",
    "timezone": "America/New_York"
  },
  "location": { "kind": "zoom" }
}
```

```bash
curl -X POST "https://api.calendly.com/invitees" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "https://api.calendly.com/event_types/ETC123",
    "start_time": "2026-07-02T18:30:00Z",
    "invitee": {"name": "Alex Prospect", "email": "prospect@example.com", "timezone": "America/New_York"},
    "location": {"kind": "zoom"}
  }'
```

- `event_type` (required) — URI of the event type to book onto.
- `start_time` (required) — ISO 8601 UTC timestamp for the slot.
- `invitee.name`, `invitee.email`, `invitee.timezone` (required) — invitee details.
- `location.kind` — required unless the event type itself omits a location.

> Field shapes for some optional parameters (e.g. custom questions/answers, guests) are not fully captured here — confirm against the live Create Event Invitee doc.

### Event Types — write endpoints (NEW)

The original API was read-only for event types; Calendly added management endpoints. **Create/Update support one-on-one event types only**, limited to basic fields (owner, title, description, duration, duration options, locations, visibility, color, locale).

| Method | Path | Description |
|---|---|---|
| POST | `/event_types` | Create a one-on-one event type |
| PATCH | `/event_types/{uuid}` | Update a one-on-one event type |
| POST | `/one_off_event_types` | Create a one-off (single-use) event type |
| GET | `/location` | List available meeting locations |

### Availability schedules — write endpoints (NEW)

Availability is no longer read-only. In addition to the read endpoints under [Availability](#availability) below:

| Method | Path | Description |
|---|---|---|
| GET | `/event_type_availability_schedules` | List availability schedules for an event type |
| PATCH | `/event_type_availability_schedules` | Update an event type's availability schedule |

### Enterprise-only data endpoints (NEW)

These require the **Enterprise** plan:

| Method | Path | Description |
|---|---|---|
| GET | (activity log) | List activity log entries |
| DELETE | (invitee data) | Delete invitee data |
| DELETE | (scheduled event data) | Delete scheduled event data |

> Exact paths for the Enterprise activity-log and data-deletion endpoints are not captured verbatim — confirm against the live developer docs before relying on them.

### Availability

| Method | Path | Description |
|---|---|---|
| GET | `/event_type_available_times` | List available times for an event type |
| GET | `/user_busy_times` | Get busy times for a user |
| GET | `/user_availability_schedules` | List user availability schedules |
| GET | `/user_availability_schedules/{uuid}` | Get specific availability schedule |

### Webhooks

| Method | Path | Description |
|---|---|---|
| POST | `/webhook_subscriptions` | Create a webhook subscription |
| GET | `/webhook_subscriptions` | List webhook subscriptions |
| GET | `/webhook_subscriptions/{uuid}` | Get specific subscription |
| DELETE | `/webhook_subscriptions/{uuid}` | Delete a subscription |

### Routing Forms

| Method | Path | Description |
|---|---|---|
| GET | `/routing_forms` | List routing forms |
| GET | `/routing_forms/{uuid}` | Get specific routing form |
| GET | `/routing_form_submissions` | List routing form submissions |
| GET | `/routing_form_submissions/{uuid}` | Get specific submission |

### Scheduling Links

| Method | Path | Description |
|---|---|---|
| POST | `/scheduling_links` | Create a single-use scheduling link |

### Invitee No-Shows

| Method | Path | Description |
|---|---|---|
| POST | `/invitee_no_shows` | Mark an invitee as a no-show |
| GET | `/invitee_no_shows/{uuid}` | Get no-show record |
| DELETE | `/invitee_no_shows/{uuid}` | Unmark a no-show |

## Webhook Events

| Event | Description |
|---|---|
| `invitee.created` | New booking made |
| `invitee.canceled` | Booking canceled |
| `routing_form_submission.created` | Routing form submitted (fires whether or not the visitor goes on to book) |

**Note:** Rescheduling fires `invitee.canceled` + `invitee.created` (two separate events).

**Scope note:** `invitee.created` and `invitee.canceled` subscriptions accept either `user` or `organization` scope. `routing_form_submission.created` only accepts `organization` scope.

### Webhook Signature Verification

Header: `Calendly-Webhook-Signature`
Format: `t={timestamp},v1={hash}`

```python
import hmac, hashlib

def verify_calendly_webhook(payload_body: str, signature_header: str, signing_key: str) -> bool:
    parts = dict(p.split("=", 1) for p in signature_header.split(",") if "=" in p)
    timestamp = parts.get("t", "")
    received_sig = parts.get("v1", "")
    expected = hmac.new(
        signing_key.encode(),
        f"{timestamp}.{payload_body}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, received_sig)
```

### Webhook Subscription Request
```json
{
  "url": "https://your-server.com/webhooks/calendly",
  "events": ["invitee.created", "invitee.canceled"],
  "organization": "https://api.calendly.com/organizations/ORG123",
  "user": "https://api.calendly.com/users/USER123",
  "scope": "user",
  "signing_key": "your-hmac-secret"
}
```

Scope options: `"user"` (events for one user) or `"organization"` (all events in org, requires admin).

## Pagination

All list endpoints use cursor-based pagination:

```json
{
  "collection": [...],
  "pagination": {
    "count": 20,
    "next_page": "https://api.calendly.com/scheduled_events?page_token=abc123",
    "next_page_token": "abc123",
    "previous_page": null,
    "previous_page_token": null
  }
}
```

Query parameters:
- `count` — items per page (default 20, max 100)
- `page_token` — cursor token from `next_page_token`

## Error Responses

| Code | Description |
|---|---|
| 400 | Bad request — invalid parameters |
| 401 | Unauthorized — expired/invalid token |
| 403 | Forbidden — insufficient permissions or plan |
| 404 | Not found — resource doesn't exist or not accessible |
| 409 | Conflict — e.g., webhook subscription already exists |
| 422 | Unprocessable — validation error |
| 429 | Rate limited — check `Retry-After` header |
| 500 | Server error |

Error response shape:
```json
{
  "title": "Resource Not Found",
  "message": "The server could not find the requested resource.",
  "details": [
    {
      "parameter": "uuid",
      "message": "not found"
    }
  ]
}
```

## Capabilities & limitations (updated 2026-06-13)

The API is **no longer read-only**. As of the 2025 Scheduling API / Event Type Management API releases:

- **CAN create bookings via API** — use the Scheduling API (`POST /invitees`). Embeds/`scheduling_url` are still an option but no longer the only path. Requires a paid plan.
- **CAN create/update event types via API** — `POST /event_types`, `PATCH /event_types/{uuid}`, `POST /one_off_event_types`. **One-on-one event types only**, basic fields only; group/collective/round-robin creation is still UI-only.
- **CAN update availability via API** — `PATCH /event_type_availability_schedules`.
- **GET + POST requests work on any plan including Free** — except the Enterprise-only endpoints (activity log, delete invitee data, delete scheduled event data).
- **Webhooks require a paid plan** (Standard, Teams, or Enterprise) — Free plan has no webhook access.
- **No Apple Calendar support** — Google Calendar, Outlook, Exchange only.

## Gaps

- Full OpenAPI spec not publicly available (developer portal is JS-rendered)
- Exact request/response fields for some endpoints may vary — constructed from multiple sources, verify against live API
- Activity log / audit trail endpoints not documented in public API
