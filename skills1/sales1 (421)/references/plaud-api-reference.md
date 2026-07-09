<!-- Source: https://docs.plaud.ai/documentation (official, public docs) + https://github.com/arbuzmell/plaud-api (unofficial Python client). Re-verified 2026-06-13. -->

# Plaud API Reference

## Official Developer Platform (public docs, Beta v1.0.0 — launched 2026-05-12)

The Plaud Developer Platform is publicly documented at **docs.plaud.ai/documentation**. The Embedded SDK + API launched as **Developer Platform Beta v1.0.0 on 2026-05-12** (per the changelog). Core SDK and transcription services are described as Generally Available. Access to credentials is **gated**: request access via the contact form in the developer console at **dev.plaud.ai**; once reviewed you receive setup instructions and console access. There is no fully self-serve signup as of 2026-06-13.

**Documented capabilities**:
- **Transcription** — convert audio to text with speaker diarization (112 languages)
- **Device Management** — start, stop, and monitor recordings from your app; audio file transfer over Bluetooth/WiFi
- **AI Summary / multidimensional summaries** — structured outputs from transcripts (templates)
- **File Management** — manage recordings and files (presigned upload/download)

**SDKs** (official):
- **iOS SDK** — Swift, Swift Package Manager, iOS 13.0+ (arm64 device only; Simulator unsupported)
- **Android SDK** — Kotlin, Maven, Android 5.0 (API 21)+
- **Swift SDK public repo**: github.com/Plaud-AI/plaud-sdk-public
- No official Python SDK published (see unofficial `plaud-api` below)

**MCP server + CLI** (for Plaud App account data — separate from the Embedded API):
- **Remote MCP URL**: `https://mcp.plaud.ai/mcp` (Claude Web / ChatGPT Web via custom connector + OAuth)
- **Local install**: `npx -y @plaud-ai/mcp@latest install` (auto-configures Claude Desktop, Claude Code, Codex, Cursor, Windsurf, VS Code, Zed)
- **MCP tools**: `login`, `logout`, `get_current_user`, `list_files`, `get_file`, `get_note`, `get_transcript`
- **Official CLI**: `@plaud-ai/cli` (`npm install -g @plaud-ai/cli`, Node ≥20), browser OAuth login. Commands: `plaud files`, `plaud recent`, `plaud today`, `plaud search <keyword>`, `plaud transcript`, `plaud summary`, `plaud audio`, `plaud me`, `plaud login`, `plaud logout`. Env: `PLAUD_API_BASE`, `PLAUD_TIMEOUT`.

**Credentials**: create an application in the dev.plaud.ai console to obtain a **Client ID** and **Secret Key** (Secret Key shown once only). Server-side config keys: `PLAUD_CLIENT_ID`, `PLAUD_API_KEY`, plus a per-user `USER_ACCESS_TOKEN` minted by your backend.

---

## Embedded REST API (region-scoped)

**Base URL**: `https://platform-<region>.plaud.ai/developer/api`
- US (live): `https://platform-us.plaud.ai/developer/api`
- Japan (live): `https://platform-jp.plaud.ai/developer/api`
- Europe: `https://platform-eu.plaud.ai/developer/api` (coming soon)
- Singapore: `https://platform-sg.plaud.ai/developer/api` (coming soon)

Credentials and the user JWT are region-specific — target the matching regional host.

### Authentication (two-step OAuth)

1. **Partner token** — `POST /oauth/partner/access-token`
   - Header: `Authorization: Basic base64(client_id:secret_key)`
   - Returns a partner access token (expiry ~3600s)
   - Refresh via `POST /oauth/partner/access-token/refresh`
2. **Per-user token** — `POST /open/partner/users/access-token`
   - Header: `Authorization: Bearer <partner_access_token>`
   - Body: `{"user_id": "<6-120 chars>", "expires_in": 86400}`
   - Returns a per-user JWT used for SDK init / file upload

For transcription API calls, send the API-key headers **`X-Client-Id`** and **`X-Client-Api-Key`**.

### Transcription endpoints

#### Submit audio
```
POST /open/partner/ai/transcriptions/
X-Client-Id: <client_id>
X-Client-Api-Key: <api_key>
Content-Type: application/json

{
  "file_url": "<pre-signed URL from file upload>",
  "params": {
    "transcribe": { "language": "auto", "model": "plaud-fast-whisper" },
    "diarization": { "enabled": false }
  }
}
```
- `file_url` (required) — pre-signed URL of the uploaded audio
- `params.transcribe.language` — BCP-47 code, defaults to `auto`
- `params.transcribe.model` — defaults to `plaud-fast-whisper`
- `params.diarization.enabled` — boolean, default `false`

Response: `{"transcription_id": "task_exec_xxx", "status": "PENDING", "data": {}}`

#### Get results
```
GET /open/partner/ai/transcriptions/{transcription_id}
X-Client-Id: <client_id>
X-Client-Api-Key: <api_key>
```
Status values: `PENDING` / `RECEIVED` / `STARTED` / `PROGRESS` (poll), `SUCCESS` (ready), `FAILURE` / `REVOKED` (terminal). Output is JSON (transcript, summary, metadata).

**Rate limits**: not documented in the public docs as of 2026-06-13.
**Webhooks**: not documented as of 2026-06-13 — completion is detected by polling `GET /open/partner/ai/transcriptions/{id}`.

---

## Unofficial Python Client (`plaud-api`)

**Disclaimer**: Reverse-engineered, not affiliated with Plaud Inc. Use at your own risk. Prefer the official Embedded REST API above when you can get credentials; this client targets the consumer `api.plaud.ai` backend (web.plaud.ai session token) and remains the only Python option since Plaud ships no official Python SDK.

**Install**: `pip install plaud-api` (Python 3.10+)

### Authentication

Token resolution order:
1. Explicit `token=` parameter
2. `PLAUD_TOKEN` environment variable
3. `.env` file in current directory
4. `~/.config/plaud/token` file

**Obtaining a token**:
1. Visit web.plaud.ai
2. Open DevTools → Network tab
3. Find any api.plaud.ai request
4. Copy the Authorization header value (without "bearer " prefix)
5. Run `plaud auth setup`

### Endpoints

#### Recordings

| Method | Endpoint | Description |
|---|---|---|
| `client.recordings.list(limit=50)` | List recordings | Returns recent recordings, default limit 50 |
| `client.recordings.get(file_id)` | Get recording | Single recording by ID |
| `client.recordings.get_audio_url(file_id)` | Get audio URL | Returns S3 download URL |
| `client.recordings.upload(path, name=...)` | Upload file | Upload MP3/OPUS file |

#### Transcriptions

| Method | Endpoint | Description |
|---|---|---|
| `client.transcriptions.start(file_id, language="en")` | Start analysis | Begin transcription processing |
| `client.transcriptions.wait(file_id, timeout=600)` | Wait for completion | Block until transcription completes |
| `client.transcriptions.save_results(file_id, result)` | Save results | Persist transcription results |
| `client.transcriptions.get(file_id)` | Get transcript | Retrieve transcript segments |
| `client.transcriptions.get_summary(file_id)` | Get summary | Retrieve AI-generated summary |
| `client.transcriptions.get_status(file_id)` | Check status | Check analysis status |

#### Speakers

| Method | Endpoint | Description |
|---|---|---|
| `client.speakers.list()` | List speakers | All known speakers |
| `client.speakers.get_for_recording(file_id)` | Recording speakers | Speakers in a specific recording |
| `client.speakers.rename(file_id, old, new)` | Rename speaker | Rename a speaker label |

#### Tags

| Method | Endpoint | Description |
|---|---|---|
| `client.tags.list()` | List tags | All tags |
| `client.tags.get_recordings(tag_id)` | Tag recordings | Recording IDs in a tag |

### CLI Commands

```
plaud recordings list          # List recent recordings
plaud recordings get <id>      # Get recording details
plaud recordings upload <path> # Upload audio file
plaud recordings download <id> # Download recording audio
plaud transcription start <id> # Start transcription
plaud transcription status <id># Check transcription status
plaud transcription get <id>   # Get transcript
plaud transcription summary <id> # Get AI summary
plaud speakers list            # List all speakers
plaud speakers rename <id> <old> <new> # Rename speaker
plaud tags list                # List all tags
plaud auth setup               # Configure authentication
```

### Quick Example

```python
from plaud import PlaudClient

client = PlaudClient()

# List recent recordings
recordings = client.recordings.list(limit=5)

# Get transcript and summary for the latest recording
transcript = client.transcriptions.get(recordings[0].id)
summary = client.transcriptions.get_summary(recordings[0].id)

# Rename a speaker
client.speakers.rename(recordings[0].id, "Speaker 1", "John Smith")
```
