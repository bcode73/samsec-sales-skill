<!-- Source: https://api.palabra.ai/docs/openapi.json, https://docs.palabra.ai/, https://github.com/PalabraAI/palabra-ai-python | Re-verified against live OpenAPI spec 2026-06-13 -->

# Talo / Palabra API Reference

Talo's developer API is provided by Palabra AI (parent company). Base URL: `https://api.palabra.ai`. OpenAPI 3.0.2 spec at `https://api.palabra.ai/docs`.

## Authentication

Client credentials model — two API keys passed as headers. Per the live OpenAPI spec (`components.securitySchemes`), the header names are exactly `ClientID` and `ClientSecret` (apiKey type, `in: header`):

| Header | Description |
|---|---|
| `ClientID` | Your client ID |
| `ClientSecret` | Your client secret |

```bash
# Simplest GET — check your credit balance
curl https://api.palabra.ai/payments/v2/balance \
  -H "ClientID: $PALABRA_CLIENT_ID" \
  -H "ClientSecret: $PALABRA_CLIENT_SECRET"
```

Some operations accept a JWT instead — the in-spec cURL examples (e.g. `/saas/upload`, `/saas/voice/clone`) show an `Authorization: Bearer <JWT_TOKEN>` alternative, and the deprecated `GET /billing/balance` also accepts `HTTPBearer`. The Python SDK reads `PALABRA_CLIENT_ID` / `PALABRA_CLIENT_SECRET` env vars and handles the header construction for you.

Response:
```json
{
  "ok": true,
  "data": {
    "credits": 120,
    "usd_equivalent": 120.00
  }
}
```

## Endpoints

### Blob Upload

**POST /saas/upload** — Upload audio/video files (max 10 per request, 0.1-10 MB each)

Supported MIME: `audio/mpeg`, `audio/aac`, `audio/wav`, `audio/webm`, `audio/mp3`, `video/webm`, `video/mp4`, `video/mpeg`

Returns pre-signed URLs for each uploaded file.

### Voice Cloning & Management

Note: per-voice endpoints are namespaced under `/saas/voice/m/{voice_id}` (the `/m/` segment is required — `/saas/voice/{voice_id}` without it is not a valid path).

| Method | Path | Description |
|---|---|---|
| POST | `/saas/voice/clone` | Create a cloned voice from audio/video sample (1 sample limit) |
| GET | `/saas/voice` | List your voices (paginated) |
| DELETE | `/saas/voice` | Delete all voices |
| GET | `/saas/voice/m/{voice_id}` | Get voice details |
| POST | `/saas/voice/m/{voice_id}` | Update voice metadata |
| DELETE | `/saas/voice/m/{voice_id}` | Delete a voice |
| POST | `/saas/voice/m/{voice_id}/tts-sample` | Regenerate the TTS sample for a voice |
| POST | `/saas/voice/m/{voice_id}/favorite` | Add a voice to favorites |
| DELETE | `/saas/voice/m/{voice_id}/favorite` | Remove a voice from favorites |
| GET | `/saas/voice/hidden` | List hidden voices |
| GET | `/saas/voice/limits` | Get voice creation quotas |
| GET | `/saas/voice/builtin` | List built-in voices |
| GET | `/saas/voice/sample/tts` | Get TTS samples from cloned voices |

### Glossary Management

| Method | Path | Description |
|---|---|---|
| POST | `/saas/glossary` | Create glossary (types: `translation`, `asr`, `asr_hot`) |
| POST | `/saas/glossary/{glossary_id}/upload` | Upload CSV glossary content |
| GET | `/saas/glossary/{glossary_id}/upload` | Download glossary CSV |
| GET | `/saas/glossary/{glossary_id}` | Get glossary details |
| POST | `/saas/glossary/{glossary_id}` | Update glossary |
| DELETE | `/saas/glossary/{glossary_id}` | Delete glossary |
| GET | `/saas/glossaries` | List glossaries (paginated) |

### Session Management

| Method | Path | Description |
|---|---|---|
| POST | `/session-storage/session` | Create streaming session (WebRTC/WebSocket) |
| POST | `/session-storage/sessions` | **Deprecated** — old session-create path; use `/session-storage/session` |
| GET | `/session-storage/sessions` | List sessions |
| GET | `/session-storage/sessions/{session_id}` | Get session details |
| DELETE | `/session-storage/sessions/{session_id}` | Delete session |
| POST | `/session-storage/sessions/{session_id}` | Update session expiration/TTL |

### Event V2 (managed multilingual events/streams)

| Method | Path | Description |
|---|---|---|
| POST | `/saas/v2/event` | Create a new event |
| GET | `/saas/v2/events` | List your events |
| GET | `/saas/v2/event/{event_id}` | Get event details |
| PATCH | `/saas/v2/event/{event_id}` | Update an event |
| DELETE | `/saas/v2/event/{event_id}` | Delete an event |
| GET | `/saas/v2/event/{event_id}/stats` | Get aggregate event metrics |
| GET | `/saas/v2/event/{event_id}/stats/export` | Download event stats as CSV |
| GET | `/saas/v2/event/public/{event_id}` | Get public event data (no auth required) |
| GET | `/saas/v2/event/{event_id}/requests` | List pending listener join requests |
| POST | `/saas/v2/event/{event_id}/requests/{request_id}/approve` | Approve a listener request |
| POST | `/saas/v2/event/{event_id}/requests/{request_id}/reject` | Reject a listener request |

### Channels

| Method | Path | Description |
|---|---|---|
| POST | `/saas/channel` | Create a new channel |
| GET | `/saas/channels` | List your channels |
| GET | `/saas/channel/{channel_id}` | Get channel details |
| PATCH | `/saas/channel/{channel_id}` | Update a channel |
| DELETE | `/saas/channel/{channel_id}` | Delete a channel |
| POST | `/saas/channel/{channel_id}/retry` | Retry channel creation |

### Billing

| Method | Path | Description |
|---|---|---|
| GET | `/payments/v2/balance` | Get credit balance and USD equivalent |
| GET | `/billing/balance` | **Deprecated** — legacy balance endpoint (accepts HTTPBearer + ClientID/ClientSecret) |

## Streaming API

Real-time speech-to-speech translation via:
- **WebRTC** — for browser and client apps (handled by LiveKit)
- **WebSocket** — for server-side integration

Flow:
1. Create a session via REST (`POST /session-storage/session`)
2. Connect to the streaming endpoint using session credentials
3. Publish audio (source language)
4. Set source and target languages
5. Receive translated audio + transcription text

**Audio formats:**
- Input: Opus, PCM_S16LE, WAV
- Output: PCM_S16LE, ZLIB_PCM_S16LE

## SDKs

| Language | Package | Install |
|---|---|---|
| Python | `palabra-ai` | `pip install palabra-ai` |
| JavaScript | `@palabra-ai/translator` | `npm install @palabra-ai/translator` |
| Java | `ai.palabra` (repo `palabra-ai-java`) | Maven/Gradle (see GitHub) |

GitHub org: https://github.com/PalabraAI (Python: `palabra-ai-python`, JS: `palabra-ai-javascript`, Java: `palabra-ai-java`)

### Python SDK quick reference

```python
from palabra_ai import PalabraAI, Config, SourceLang, TargetLang, EN, ES

# Auth via env vars: PALABRA_CLIENT_ID, PALABRA_CLIENT_SECRET
palabra = PalabraAI()

# I/O adapters: FileReader, FileWriter, DeviceReader, DeviceWriter, BufferReader, BufferWriter, RunAsPipe
# Execution: palabra.run(config) (sync) or await palabra.arun(config) (async)
# Result: RunResult with ok, exc, log_data, eos fields
```

## Pagination

List endpoints (`GET /saas/voice`, `GET /saas/glossaries`, `GET /session-storage/sessions`) support pagination. Pattern not fully documented in OpenAPI — assume offset-based with `limit` and `offset` query params.

## Rate Limits

No documented rate limits in the OpenAPI spec or developer docs. Assume conservative limits for production integrations — add retry logic with exponential backoff on 429 responses.

## Error Response Format

```json
{
  "ok": false,
  "errors": [
    {
      "error_code": 401,
      "detail": "Invalid client credentials"
    }
  ]
}
```

Common error codes: 400 (bad request), 401 (auth failure), 404 (not found), 422 (validation error).

## Webhooks

**No webhook support.** Palabra API is request/response only. For monitoring, poll the billing endpoint or use streaming session events.

## Gaps

- Rate limits undocumented — no published req/sec or daily limits
- Pagination pattern details missing (cursor vs offset)
- WebSocket/WebRTC message schemas not fully documented in OpenAPI (live in separate streaming docs)
- No webhook/event system for async notifications
- Voice cloning quality and language support per voice not documented
