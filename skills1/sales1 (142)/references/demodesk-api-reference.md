<!-- Source: https://demodesk.com/api/docs/v2/generated.yaml, https://help.demodesk.com/en/articles/8518816-api-reference, https://help.demodesk.com/en/articles/13989763-download-past-transcripts-via-api-v2 -->

# Demodesk API Reference

## Overview

Two API versions:
- **V1** (legacy): `https://demodesk.com/api/v1/` — meetings, users, scheduling
- **V2** (recommended): `https://demodesk.com/api/v2/` — recordings, transcripts, summaries, scorecards

## Authentication

API key passed as a Bearer token in the `Authorization` HTTP header (current scheme per the V2 OpenAPI spec):
```
Authorization: Bearer YOUR_API_KEY
```

The legacy `api-key: YOUR_API_KEY` custom header is **deprecated but still accepted** for backward compatibility. The help-center API Reference article still documents only the `api-key` header; new integrations should use `Authorization: Bearer`.

Generate keys at: Settings > Integrations > Other > Demodesk API

Three key types:
- **MASTER_3RD_PARTY_API_KEY**: Creates new accounts (white-label only)
- **COMPANY_ADMIN_USER_API_KEY**: Manages company accounts
- **USER_API_KEY**: Individual user administration

API key inherits permissions of the creating user. Admin users should be members of all restricted groups for full company access.

## Rate Limits

- Global: 120 requests/minute per API key
- Recordings endpoint: 60 requests/minute per API key
- Listing endpoints: 20 requests/minute
- Returns HTTP 429 with optional `Retry-After` header

## V2 Endpoints (Recommended)

### Current User
```
GET /api/v2/me
```
Returns the user that owns the API key (the authenticated user).

### List Users
```
GET /api/v2/users
```
Lists active users. Supports `search`, `cursor`, and `limit` query parameters.

### List Recordings
```
GET /api/v2/recordings
```

Parameters:
- `filter[postprocessing_status_eq]=done` — only fully processed
- `filter[status_eq]=ready` — available recordings only
- `filter[created_at_gteq]=<date>` — filter by creation date
- `filter[demo_user_id_eq]=<USER_ID>` — single user's recordings
- `filter[demo_id_eq]=<DEMO_ID>` — specific meeting
- `filter[group_id_in]=<ID1>,<ID2>` — by group
- `limit=1-100` (default 25)

Response includes `meta.hasNext` and `meta.nextCursor` for pagination.

Recording object fields: recordingToken, recordingId, demoId, userId, name, status (pending/ready/failure/cancelled/expired), createdAt, updatedAt, demoStartDate, durationMs, postprocessingStatus, access level.

### Get Recording Detail
```
GET /api/v2/recordings/{token}
```

Extended fields: audioOnly flag, attendeeClassification, meetingLocation, participants array, groups, engagement/feedback scores.

### Get Transcript
```
GET /api/v2/recordings/{token}/transcript?format=plaintext
```

Parameters:
- `format`: `plaintext` or `json`
- Supports language translation parameter

Response codes:
- 200 — ready
- 202 — still processing
- 204 — empty/too short
- 404 — not found

JSON format includes paragraphs with speaker info, sentences with `startInSeconds`, `endInSeconds`, `text`.

### Batch Transcripts
```
POST /api/v2/transcripts/batch
Content-Type: application/json

{
  "recordingTokens": ["TOKEN_1", "TOKEN_2", ...],
  "format": "plaintext"
}
```

Up to 100 recording tokens per request.

### Get Summaries
```
GET /api/v2/recordings/{token}/summaries
```

Returns: summaryId, promptId, promptName, languageCode, content (plaintext + HTML), timestamps.

### Get Scorecards
```
GET /api/v2/recordings/{token}/scorecards
```

Returns non-deleted scorecards: template info, score (1-5), questions with criteria and comments, giver/receiver user IDs.

## V1 Endpoints (Legacy)

### Company & User Management
- `POST /api/v1/auth` — Create account
- `POST /api/v1/companies` — Create company
- `GET /api/v1/companies/<id>/users` — List users
- `POST /api/v1/users` — Add user
- `PATCH /api/v1/users/<id>` — Update user
- `DELETE /api/v1/users/<id>` — Remove user

### Meeting Management
- `POST /api/v1/scheduled_demos` — Schedule meeting
- `GET /api/v1/scheduled_demos/<token>` — Fetch meeting details
- `GET /api/v1/demos` — List meetings (paginated, supports filters)
- `PATCH /api/v1/scheduled_demos/<id>` — Update meeting
- `POST /api/v1/scheduled_demos/<id>/cancel` — Cancel meeting
- `DELETE /api/v1/scheduled_demos/<id>` — Delete meeting
- `GET /api/v1/demo_templates` — List event types

## Webhooks

10 events per the V2 OpenAPI spec:
- `demo.scheduled`
- `demo.rescheduled`
- `demo.handovered`
- `demo.canceled`
- `demo.started`
- `demo.ended`
- `demo.call_note_updated`
- `demo.event_response_updated`
- `recording.uploaded`
- `recording.transcription_postprocessed`

> Note: the help-center API Reference article currently lists only the 8 core events (it omits `demo.call_note_updated` and `demo.event_response_updated`). The two extra events appear in the V2 OpenAPI spec. Confirm event availability with support when setting up.

**Setup**: Email support@demodesk.com with endpoint URLs and desired events. Self-service webhook configuration is not available.

## Query Filters (Ransack-style)

Operators: `eq`, `not_eq`, `cont`, `gteq`, `lteq`, `in`

Examples:
- `filter[status_eq]=ready`
- `filter[postprocessing_status_eq]=done`
- `filter[created_at_gteq]=2026-01-01`
- `filter[demo_id_eq]=12345`
- `filter[group_id_in]=1,2,3`

## Error Codes

- 400 `bad_request` — malformed request
- 401 `unauthorized` — invalid API key
- 403 `forbidden` — insufficient permissions
- 404 `not_found` — resource not found
- 422 `unprocessable_entity` — validation error
- 429 — rate limited (check Retry-After header)

## OpenAPI/Swagger Specs

- V2: `https://demodesk.com/api/docs/v2/generated.yaml`
- V1: `https://demodesk.com/api/docs/v1/swagger.json`

Interactive docs: `https://demodesk.com/api/docs/index.html`
