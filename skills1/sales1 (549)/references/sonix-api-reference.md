<!-- Source: https://sonix.ai/docs/api -->

# Sonix API Reference

## Overview

- **Base URL**: `https://api.sonix.ai/v1`
- **Auth**: Bearer token via `Authorization: Bearer {api_key}` header
- **API key management**: https://my.sonix.ai/api (paid subscribers only — trial users must email support)
- **Plan restriction**: "The Sonix API is available to all paying subscribers." The 403 error reads "API access is not available on your current plan. Please upgrade to Core or higher." → API works on any paid subscription plan (Core/Advanced/Pro/Enterprise). Pay-As-You-Go (no subscription) does NOT have API access.
- **Rate limits**: Main REST endpoints have no publicly documented rate limits — design conservatively. The OAuth-only endpoints (used by MCP, see below) are capped at: token endpoint 120 req/min/IP, registration endpoint 30 req/hour/IP.
- **File upload limit**: 100 MB direct (`file`); unlimited via `file_url`.

## Endpoints

### Media

#### Submit media for transcription
```
POST /media
```
Upload an audio/video file for transcription. Supports direct file upload (multipart, 100 MB max) or URL-based upload (no size limit).

Parameters:
- `language` (string, required) — language code for transcription
- `file` (file) — audio/video file (multipart upload)
- `file_url` (string) — URL to audio/video file (alternative to direct upload)
- `name` (string) — optional display name
- `folder_id` (string) — optional folder to place the media in
- `keywords` (string) — optional keywords/custom vocabulary hints
- `custom_data` (string) — optional arbitrary metadata stored with the media
- `callback_url` (string) — URL Sonix POSTs to when transcript status changes (failed or completed). This is the completion webhook/callback path and is available to ALL API users — you do NOT need an Enterprise dashboard webhook to be notified on completion. Without it, poll `GET /media/{id}`.

#### Get media details
```
GET /media/{id}
```
Retrieve details and processing status for a media item.

Media `status` values: `preparing`, `transcribing`, `aligning` (aligning a provided transcript), `completed`, `blocked` (account issue), `failed` (invalid format), `duplicate` (matched an existing file).

#### List media
```
GET /media
```
List media items in the account. Paginated — returns 100 files per page.

#### Update media
```
PUT /media/{id}
```
Update a media item's `name`, `label`, or `folder_id`.

#### Delete media
```
DELETE /media/{id}
```
Delete a media file.

### Transcripts

#### Get transcript
```
GET /media/{id}/transcript          # plain text
GET /media/{id}/transcript.srt      # SRT subtitle format
GET /media/{id}/transcript.vtt      # VTT subtitle format
GET /media/{id}/transcript.json     # structured JSON with word-level timing
GET /media/{id}/transcript?format=avid_ds   # Avid DS caption format
```
Retrieve the transcript for a completed media item. Format is selected via the path extension (`.srt`/`.vtt`/`.json`) or the `format` query parameter.

#### Update transcript
```
PUT /media/{id}/transcript
```
Update/overwrite the transcript text.

#### Auto-split transcript into subtitles
```
PUT /media/{id}/transcript/split
```
Auto-split the transcript into subtitle-length segments.

### Media exports

#### Export edited media
```
POST /media/{id}/media_exports
```
Export media with applied edits (mp3 / wav / mp4 output).

#### Get export status
```
GET /media_exports/{id}
```

### Translations

#### Request translation
```
POST /media/{id}/translations
```
Request automated translation of a transcript.

Parameters:
- `language` (string) — target language code

#### Get translation status
```
GET /media/{id}/translations/{language}
```

### Summarizations

#### Request summarization
```
POST /media/{id}/summarizations
```
Generate AI summary, chapter markers, sentiment analysis, or other AI-workspace outputs. Accepts an optional `callback_url`.

Parameters:
- `type` (string) — `summary`, `chapters`, `sentiment`, etc.

Note: Requires the AI workspace/AI Analysis capability (included with subscription AI-workspace hours; add-on on some plans).

#### Get summarization result
```
GET /summarizations/{id}
```

### Batch summarizations

#### Summarize all files in a folder
```
POST /folders/{id}/batch_summarizations
```

#### Check batch status
```
GET /batch_summarizations/{id}
```

#### List batch jobs for a folder
```
GET /folders/{id}/batch_summarizations
```

### Video burn-ins

#### Request subtitle burn-in
```
POST /media/{id}/video_burn_ins
```
Embed subtitles directly into a video file.

#### Get burn-in status
```
GET /video_burn_ins/{id}
```

### Folders

#### List folders
```
GET /folders
```

#### Create folder
```
POST /folders
```

#### Update folder
```
PUT /folders/{id}
```

### Users

#### List users
```
GET /users
```

#### Invite user
```
POST /users
```

#### Update user role
```
PUT /users/{id}
```

### Shares

#### Share media
```
POST /media/{id}/shares
```

#### List shares
```
GET /media/{id}/shares
```

#### Revoke share
```
DELETE /media/{id}/shares
```

## Status codes & errors

| Code | Meaning |
|---|---|
| 400 | Invalid request parameters |
| 401 | Invalid/missing API key |
| 402 | Payment error or insufficient permissions |
| 403 | API access unavailable on current plan ("upgrade to Core or higher") |
| 404 | Resource not found |
| 409 | Media still transcribing |

Errors return JSON: `{"error": "message", "code": 400}`

## Languages

The API supported-languages table lists 80+ languages and variants (marketing pages say "54+"). Set `language` explicitly on upload rather than relying on auto-detect.

## Webhooks / completion callbacks

There are two distinct mechanisms — don't conflate them:

1. **Per-request `callback_url`** (available to ALL API users) — pass `callback_url` to `POST /media` (and summarizations). Sonix POSTs to it when the transcript status changes (failed or completed). This is the documented "no polling required" completion webhook.
2. **Dashboard Webhooks** (select Enterprise accounts only) — workspace-level event subscriptions for:
   - `Transcription finished`
   - `Translation finished`
   - `Label change`
   - `Folder change`
   When a webhook `Secret` is configured, payloads are signed with HMAC-SHA256 in the `X-Webhook-Signature` header for verification.

## MCP server

Sonix runs an MCP server so LLM clients (Claude, Cursor, Codex, etc.) can read your Sonix media library, transcripts, and account state.

- **URL**: `https://api.sonix.ai/mcp`
- **Auth**: OAuth 2.1 — independent from REST API keys. REST API keys are NOT valid for MCP; the two surfaces have separate auth.
- **Tools** (read-only): `list_media`, `read_transcript`, `export_transcript`, `get_account_info`.

## SDKs

No official SDK/client libraries documented. The API page references code samples in multiple languages; otherwise use raw REST calls.

## Notes

- API key is per-user, not per-workspace.
- API is available to any paid subscriber (Core and up), not just a top tier — but NOT to Pay-As-You-Go.
- Prefer `callback_url` over polling for completion notifications; dashboard event Webhooks remain Enterprise-only.
- Main REST endpoints have no documented rate limits — design conservatively.
- For files over 100 MB, use the `file_url` parameter instead of direct upload.
