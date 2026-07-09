<!-- Source: https://www.temi.com/api/reference/v1 -->

# Temi API Reference (v1)

## Base Information

- Base URL: `https://api.temi.com/v1`
- All dates use ISO-8601 UTC format
- Authorization: Bearer token in header — `Authorization: Bearer <Api Key>`
- API key generated from Temi account developer page

## Job Operations

### Submit Job

**POST** `/jobs`

Accepts either JSON with `media_url` or multipart form data with media file.

Supported formats:
- Audio: WAV, MP3, MP4, WebM, OGG
- Video: AVI, MP4, MOV, WebM, WMV, FLV

**Options object fields:**
- `media_url` (optional, 1024 char limit) — URL to audio/video file
- `callback_url` (optional) — webhook URL for completion notification
- `metadata` (optional, 256 char limit) — user-provided metadata string

**Errors:**
- 400 — `invalid-parameters`, `unsupported-media-content-type`, `media-missing-filename`
- 403 — `out-of-credit` (not enough account balance)

### Get Job Status

**GET** `/jobs/<id>`

Returns job object with fields:
- `id` — unique identifier (e.g. `sd233343`)
- `status` — `in_progress`, `transcribed`, `failed`
- `created_on` — ISO-8601 UTC timestamp (time the job was created)
- `callback_url` — webhook URL if set (called when the job completes)
- `web_url` — link to Temi online editor (to edit the transcript)
- `duration_seconds` — duration of the file; `null` when not available
- `name` — file name as Temi shows it; `null` when not available
- `metadata` — user-provided metadata
- `failure` — failure reason on failed jobs; one of `unspecified`, `download_failure`, `insufficient_balance`, `invalid_media`
- `failure_detail` — human-readable reason why the job failed
- `last_modified_on` — ISO-8601 UTC timestamp (last edited in the editor)

**Errors:**
- 400 — invalid parameters
- 404 — job not found

### List Jobs

**GET** `/jobs?limit=<100>&starting_after=<id?>`

Returns array of jobs sorted by descending date. Maximum 100 per page.

**Errors:**
- 400 — invalid parameters

### Delete Job

**DELETE** `/jobs/<id>`

Returns 204 status code. Job must be in `transcribed` or `failed` state.

**Errors:**
- 400 — invalid parameters
- 404 — not found
- 409 — invalid state (job still processing)

## Transcript Operations

### Get Transcript

**GET** `/jobs/<id>/transcript?version=[latest|machine]`

**Version parameter:**
- `latest` — includes all changes made in the Temi editor
- `machine` — original transcript produced by the AI (no edits)

**Accept header determines format:**
- `text/plain` — plain text
- `application/json` — structured JSON with speakers and timestamped monologues
- `application/msword` — Word document
- `application/pdf` — PDF document

**JSON format structure:**
```json
{
  "speakers": [
    { "id": 0, "name": "Speaker 1" }
  ],
  "monologues": [
    {
      "speaker": 0,
      "elements": [
        { "type": "text", "value": "Hello", "ts": 0.0, "end_ts": 0.5 },
        { "type": "punct", "value": "." }
      ]
    }
  ]
}
```

**Errors:**
- 400 — invalid format
- 409 — invalid job state (not yet transcribed)

### Share Transcript Editor URL

**POST** `/jobs/<id>/share`

Returns: `{ "editor_url": "..." }`

**Errors:**
- 400 — invalid parameters
- 404 — not found
- 409 — invalid state

## Account Operations

### Get Account Details

**GET** `/account`

Returns: `{ "balance": 10.50, "email": "user@example.com" }`

## Webhooks

When a `callback_url` is provided during job submission, Temi sends a POST request to that URL when transcription completes or fails.

**Payload:** `{ "job": <Job Object> }`

The job object in the webhook payload has the same structure as the response from `GET /jobs/<id>`.

## Error Responses

Errors follow RFC 7807 problem details structure:

```json
{
  "type": "https://api.temi.com/errors/invalid-parameters",
  "title": "Invalid Parameters",
  "detail": "The 'media_url' parameter is required",
  "parameters": ["media_url"],
  "allowed_values": [...],
  "current_value": "...",
  "current_balance": 0.0
}
```

Properties vary by error type:
- `type` — URI identifying the error type
- `title` — human-readable error title
- `detail` — human-readable description
- `parameters` — list of invalid parameters (on validation errors)
- `allowed_values` — permitted values (on validation errors)
- `current_value` — the value that was provided (on validation errors)
- `current_balance` — account balance (on insufficient balance errors)

**Documented error types (slug, HTTP status):**
- `invalid-parameters` — 400 (API method invoked with invalid parameters)
- `unsupported-media-content-type` — 400 (media type not in accepted list)
- `media-missing-filename` — 400 (multipart upload missing filename)
- `out-of-credit` — 403 (not enough account balance)
- `job-not-found` — 404 (could not locate the job)
- `invalid-job-state` — 409 (job state incompatible with operation)
- `unsupported-transcript-format` — 409 (requested transcript format not supported)
