<!-- Source: https://doc.tldv.io/index.html -->

# tl;dv API v1alpha1 — Complete Reference

## Authentication

**API Key Header**: `x-api-key: YOUR_API_KEY`
- Obtain keys at: `https://tldv.io/app/settings/personal-settings/api-keys`
- Required for all requests; HTTPS-only
- API access requires Pro plan or higher

## Base Endpoint

`https://pasta.tldv.io`

## Meetings Endpoints

### Import Meeting

- **Method**: POST
- **Path**: `/v1alpha1/meetings/import`
- **Auth**: Api Key
- **Response**: `{success, jobId, message}`

### List Meetings

- **Method**: GET
- **Path**: `/v1alpha1/meetings`
- **Auth**: Api Key
- **Response**: Paginated results with `{page, pages, total, pageSize, results[]}`

### Get Meeting by ID

- **Method**: GET
- **Path**: `/v1alpha1/meetings/{meetingId}`
- **Auth**: Api Key
- **Response**: Meeting object with organizer, invitees, duration

### Download Recording

- **Method**: GET
- **Path**: `/v1alpha1/meetings/{meetingId}/download`
- **Auth**: Api Key
- **Response**: 302 redirect to signed URL (6-hour TTL)

## Transcripts Endpoints

### Get Transcript

- **Method**: GET
- **Path**: `/v1alpha1/meetings/{meetingId}/transcript`
- **Auth**: Api Key
- **Response**: `{id, meetingId, data[]}` with speaker, text, timestamps

## Notes Endpoints

### Get Notes

- **Method**: GET
- **Path**: `/v1alpha1/meetings/{meetingId}/notes`
- **Auth**: Api Key
- **Response**: `{structuredNotes[], markdownContent, topics[]}`

## Highlights (Deprecated)

### Get Highlights

- **Method**: GET
- **Path**: `/v1alpha1/meetings/{meetingId}/highlights`
- **Status**: Deprecated; use `/notes` endpoint instead

## Health Check

- **Method**: GET
- **Path**: `/v1alpha1/health`
- **Auth**: Api Key

## Webhooks

Webhook access requires the Pro or Business plan (same gate as the API). Configure in the dashboard: **Settings → Webhooks → Configure New Webhook** → choose the event, provide an HTTPS endpoint URL (HTTP is rejected), optionally add custom request headers (e.g. `Authorization: Bearer ...` or `x-api-key: ...` sent on every delivery), then **Save and Activate Webhook**.

**Available Triggers**:
1. `MeetingReady` — when a meeting finishes processing and is ready to use
2. `TranscriptReady` — when a transcript has been generated and is available

**Scope Levels**: User, Team, Organization

**Payload shape** (POST to your endpoint):
```json
{
  "id": "webhook job id",
  "event": "MeetingReady",
  "executedAt": "ISO-8601 timestamp",
  "data": { }
}
```
- `MeetingReady` `data` includes meeting id, title, organizer details, invitees, and meeting URL.
- `TranscriptReady` `data` includes transcript id, meeting id, and speaker/timestamp transcript segments.

No HMAC/signature signing is documented — authenticate inbound deliveries using a custom header you configure on the webhook (above). Retry/failure behavior is not documented.

## Error Responses

**Validation (400)**:
```json
{
  "message": "Invalid query params, check 'errors' property",
  "errors": [{"property": "field", "constraints": {}}]
}
```

**Other Errors (401, 403, 404, 500)**:
```json
{"name": "ErrorType", "message": "description"}
```

## Authorization Rules

- Free plan: UI access only (if shared)
- Pro/Business/Enterprise: Full API access
- Meeting organizer's plan determines API exportability
