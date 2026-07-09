<!-- Source: https://developer.transkriptor.com/ — re-verified 2026-06-13 -->

# Transkriptor API Reference

**Base URL**: `https://api.tor.app/developer/`
**Auth**: Bearer token in Authorization header (`Authorization: Bearer {api_key}`)
**API key location**: https://app.transkriptor.com/account
**Rate limit**: 1,000 requests/minute (429 Too Many Requests when exceeded, with temporary block)
**Plan gate**: Paid subscription required. The official docs do NOT state a specific tier; treat the exact gating plan as unverified and confirm in-app before relying on it.
**Machine-readable index**: https://developer.transkriptor.com/llms.txt (page list + OpenAPI endpoints, for AI agents)

## Authentication

```
Authorization: Bearer {api_key}
```

API keys are user-scoped. Generate from the account settings page.

## Endpoints

### Transcribe Local File

**Step 1: Get upload URL**
```
POST /transcription/local_file/get_upload_url
```
Parameters:
- `file_name` (string, required) — the name of the file to upload

Returns an `upload_url` (pre-signed URL) and a `public_url` for the uploaded file.

**Step 2: Upload file**
```
PUT {returned upload_url}
Content-Type: application/octet-stream
Body: binary file data
```

**Step 3: Initiate transcription**
```
POST /transcription/local_file/initiate_transcription
```
Parameters:
- `url` (string, required) — the `public_url` obtained after uploading in step 1
- `language` (string, required) — language code in ISO format (e.g., `en-US`, `tr-TR`)
- `service` (string, required) — `Standard` or `Subtitle`
- `folder_id` (string, optional) — target folder ID; defaults to "Recent Files"
- `triggering_word` (string, optional) — a word that triggers automatic line breaks in the transcript

### Transcribe via URL

Transcribe from a remote file URL (e.g., YouTube, Google Drive, Dropbox, OneDrive).
```
POST /transcription/url
```
Parameters:
- `url` (string, required) — the URL of the file to be transcribed
- `service` (string, required) — `Standard` or `Subtitle`
- `language` (string, required) — language code in ISO format (e.g., `en-US`, `tr-TR`)
- `folder_id` (string, optional) — target folder; defaults to "Recent Files"
- `file_name` (string, optional) — output file name; defaults to the original source name

### Transcribe Meeting

Start a meeting bot recording on Google Meet, Microsoft Teams, or Zoom.
```
POST /transcription/meeting
```
Parameters:
- `meetingUrl` (string, required) — the meeting link (Google Meet / Teams / Zoom)
- `meeting_bot_name` (string, optional) — custom bot name (Teams or Zoom only; not available for Google Meet)
- `meeting_language` (string, optional) — language for transcription (e.g., `en-US`); uses platform default if unspecified
- `summary_template_id` (string, optional) — ID of a summary template to apply

Returns `order_id` to track transcription progress.

### Get Transcription Result (Content)
```
GET /files/{order_id}/content
```
Returns a `content` array of segments with:
- `text` (string) — transcribed text
- `StartTime` (number) — segment start time in milliseconds
- `EndTime` (number) — segment end time in milliseconds
- `VoiceStart` (number) — voice activity start in milliseconds
- `VoiceEnd` (number) — voice activity end in milliseconds
- `Speaker` (string) — speaker identifier (e.g., `SPK_1`)

### Update Transcription Content
```
PUT /files/{order_id}/content
```
Replace the transcription segments (e.g., after corrections).
Body:
- `content` (array, required) — array of segment objects, each with `text`, `StartTime`, `EndTime`, `VoiceStart`, `VoiceEnd`, `Speaker`

### Export Transcription
```
POST /files/{order_id}/content/export
```
Parameters:
- `export_type` (string) — `txt`, `srt`, `pdf`, or `docx`
- `include_speaker_names` (boolean) — include speaker labels
- `include_timestamps` (boolean) — include timestamps
- `merge_same_speaker_segments` (boolean) — combine adjacent segments from the same speaker
- `is_single_paragraph` (boolean) — output as a single paragraph
- `paragraph_size` (number) — paragraph length: `1`, `2`, `4`, or `8` sentences

### List Files
```
GET /files
```
Returns all transcription files.

### Get File Detail
```
GET /files/{order_id}
```
Returns file metadata.

### Delete File
```
DELETE /files/{order_id}
```

### Rename File
```
PUT /files/{order_id}
```
Body:
- `file_name` (string) — the new name for the transcription file

### Recognize Speakers (Speaker Profiles)

Speaker recognition is managed through speaker profiles under `annotations/profiles`, not a single re-run endpoint.

**Create profile from an audio sample (get upload URL):**
```
POST /annotations/profiles/create_url
```
Parameter: `speaker_name` (required)

Then `PUT {upload_url}` the audio binary, and finalize:
```
POST /annotations/profiles
```
Parameter: `speaker_name` (required, must match the name used above)

**Create profile from an existing transcription:**
```
POST /annotations/profiles/create_from_transcription
```
Parameters: `order_id`, `old_speaker_name`, `new_speaker_name`, `start_time` (ms), `end_time` (ms)

### Get Meeting Details
```
GET /meetings/{order_id}
```

### Get Summary
```
GET /transcription/summary?order_id={order_id}
```
Returns the AI-generated summary for a transcription. `order_id` is a required query parameter.

### AI Chat
Query transcribed content via knowledge-base chat sessions. First create a session, then send messages.
```
POST /ai_chat/knowledgebases/{knowledge_base_id}/sessions/{session_id}
```
Body:
- `query` (string) — the question/prompt

### Get Folders
```
GET /folders
```

### Get User Details
```
GET /users
```
Returns: remaining minutes, email, account info.

### Text to Speech (Speaktor)
```
POST /text_to_speech
```
Parameters:
- `text` (string, required) — text to convert
- `language` (string, required) — language code (e.g., `en-US`)
- `voice_name` (string, required) — voice identifier from your dashboard
- `speed_rate` (number, optional) — playback speed, range 0.5 (half) to 2.0 (double)
- `generate_subtitle` (boolean, optional) — generate an SRT file alongside audio
- `emotion` (string, optional) — emotional tone (Pro voices only)

### Webhooks
Webhooks fire when transcriptions complete and POST the formatted transcript to your URL.
```
POST   /integrations/webhooks          — Create webhook
GET    /integrations/webhooks          — List webhooks (optional webhookType query param for a single webhook)
PUT    /integrations/webhooks          — Update webhook (webhookType in body identifies the webhook)
DELETE /integrations/webhooks          — Delete webhook (webhookType query param identifies the webhook)
```
Create body parameters:
- `url` (string, required) — the endpoint that receives notifications
- `export_format` (string, optional) — `Txt`, `Json`, or `Csv` (default `Txt`)
- `include_timestamps` (boolean, optional) — default `false`
- `include_speaker_names` (boolean, optional) — default `false`
- `merge_same_speaker_segments` (boolean, optional) — default `false`
- `is_single_paragraph` (boolean, optional) — default `false`
- `paragraph_size` (integer, optional) — default `1`
- `folder_id` (string, optional) — scope notifications to a specific folder

The webhook identifier (`webhookType`) is formatted like `wh 2025-05-02 12:34:56`. The docs describe only the transcription-completion trigger; no discrete event-type names are listed, and **no HMAC/signature header is documented** — validate delivery by other means (allowlist, shared secret in the URL, etc.).

### Custom Vocabulary
```
POST   /custom_vocabulary    — Set custom vocabulary
GET    /custom_vocabulary    — Get custom vocabulary
DELETE /custom_vocabulary    — Delete custom vocabulary
```
Set body parameters:
- `words` (array, required) — list of words/phrases. Maximum 1,000 items, up to 6 words per phrase.

## Code Examples

Official code examples are provided per endpoint in multiple languages (e.g., Python, JavaScript/Node, Java, C#, Go, Ruby, PHP, Kotlin, Swift, Dart).

See https://developer.transkriptor.com/ for language-specific samples.

## Error Handling

- `401` — Invalid or missing API key
- `403` — Insufficient permissions or plan does not include API access
- `429` — Rate limit exceeded (1,000 req/min); temporary block applied
- `5xx` — Server error, retry with exponential backoff
