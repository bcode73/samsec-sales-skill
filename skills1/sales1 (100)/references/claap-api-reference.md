<!-- Source: https://docs.claap.io/api-reference/openapi.json -->
<!-- Fetched: 2026-04-17 -->
<!-- Re-verified: 2026-06-13 against https://docs.claap.io/api-reference/openapi.json, https://docs.claap.io/api-reference/authentication, https://help.claap.io/en/articles/10335261-claap-webhooks-documentation, https://help.claap.io/en/articles/11786373-using-claap-s-mcp-server -->

# Claap API Reference

OpenAPI 3.1.0 specification for the Claap API.

## Base URL

`https://api.claap.io/`

## Authentication

All requests must include the `X-Claap-Key` HTTP header.

```
X-Claap-Key: cla_abcdefghijkl
```

API keys follow the pattern `cla_xxxxx`. Keys are only active for customers in free trials or with an active paid subscription. Free plan requests receive `401 Unauthorized`.

Create API keys in workspace Settings → API & Webhooks → API tab (admin/owner only). The complete key is shown only once — store it immediately.

## Endpoints

### Recordings

#### List Recordings
`GET /v1/recordings`

Returns recordings accessible by workspace members and visible in global search.

Query parameters:
- `channelId` — filter by folder identifier
- `createdAfter` / `createdBefore` — creation-timestamp bounds
- `cursor` — pagination cursor
- `labels` — comma-separated label names
- `limit` — results per page, 1-100 (default 20)
- `recorderEmail` / `recorderId` — filter by recorder
- `sort` — `created_asc`, `created_desc` (default), `duration_asc`, `duration_desc`, `title_asc`, `title_desc`

Response is an array of recording objects with pagination metadata (use `cursor` to page).

#### Create Recording
`POST /v1/recordings`

Create a recording via video/audio file upload (or by supplying a `downloadUrl`). Returns a recording object including an upload URL and processing `state`.

Request body:
- `authorEmail` (required) — creator's email
- `title` — recording title
- `channelId` — target folder ID
- `downloadUrl` — video source URL (alternative to direct upload)
- `meeting` — object with `startedAt`, `endedAt`, `participants`
- `deal` — CRM deal reference object with `type` and `id`
- `transcript` — set `type: "upload"` to supply a transcript separately
- `source` — origin platform: one of `Aircall`, `Allo`, `Call`, `GoogleMeet`, `LemlistVoip`, `Loom`, `MsTeams`, `Ringover`, `Zoom`

#### Get Recording
`GET /v1/recordings/{recordingId}`

Retrieve a specific recording by ID. Returns the `ApiRecording` object with metadata, transcript, insights, video URL, and action items.

Query parameters:
- `returnAiFields` — `true`/`1` returns AI insight fields; `false`/`0` (default) returns template-grouped insights.

#### Delete Recording
`DELETE /v1/recordings/{recordingId}`

Delete a specific recording. Returns `{"result": {"ok": <boolean>}}`.

#### Get Transcript
`GET /v1/recordings/{recordingId}/transcript`

Retrieve the transcript for a recording. Returns a transcript object whose segments include speaker, timestamps, language, and word-level timing.

Query parameters:
- `lang` — 2-letter language code to return a translated transcript
- `format` — `json` (default) or `text`

### Workspace

#### Get Workspace
`GET /v1/workspaces/mine`

Retrieve workspace details and configuration. Response includes `id`, `name`, `createdAt`, `membersCount`, `recordingsCount`.

### Webhooks

#### Trigger Webhook
`POST /v1/webhooks/{webhookId}/trigger`

Manually trigger a webhook event for testing. Request body:
- `type` — `recording_added` or `recording_updated`
- `recordingId` — the recording to fire the event for

Returns `{"result": {"ok": <boolean>}}`.

### OAuth

#### Register
`POST /oauth/register`

Register an OAuth 2.0 client application. Parameters: `redirect_uris` (required), `client_name`, `client_uri`, `logo_uri`, `grant_types`, `response_types`, `token_endpoint_auth_method`.

#### Get Token
`POST /oauth/token`

Exchange an authorization code for an access token. Supports `authorization_code` and `refresh_token` grant types.

#### Revoke Token
`POST /oauth/revoke`

Revoke an existing token. Parameters: `token` (required), `token_type_hint: "refresh_token"`.

### Assets

#### Get Asset
`GET /x/asset`

Retrieve asset payloads (video files, thumbnails, etc.).

## Recording Schema (`ApiRecording`)

The recording object contains:
- `id` — unique identifier
- `title` — recording title
- `createdAt` — ISO 8601 timestamp
- `state` — processing state
- Meeting details (platform, duration, participant list)
- Transcript with speaker labels and timestamps
- Translations (if available)
- Video URL and thumbnail URL (**expire within 24 hours**)
- Action items extracted from the call
- Insights (pain points, next steps, objections, competitor mentions)
- CRM integration data (mapped fields, deal association)

## Webhook Events

Two event types exist. **Private recordings trigger neither event.**

### `recording_added`
Emitted when a new recording becomes available after transcoding, transcription, and analysis. Includes metadata, outline, insights, transcript links, participants, and company/CRM deal information.

### `recording_updated`
Emitted when recording properties change — folder, labels, attached deal, attached company, or insight template. The payload contains the complete Recording entity.

### Payload Shape
Both events share the same envelope (the `type` discriminates):

```json
{
  "eventId": "unique_identifier",
  "event": {
    "type": "recording_added",
    "recording": { /* Recording entity */ }
  }
}
```

- `eventId` — unique identifier, **shared across retries** (use it for idempotency/dedupe)
- `event.type` — `recording_added` or `recording_updated`
- `event.recording` — the full Recording entity (action items, companies, CRM info, deals, duration, insights, key takeaways, meeting data, outlines, participants, transcripts, workspace)

### Webhook Headers
Claap sends these request headers (lowercase):
- `x-claap-webhook-id` — webhook identifier
- `x-claap-webhook-secret` — webhook secret; compare it against your stored secret to verify the request originates from Claap (there is **no HMAC signature scheme** — verification is the shared secret only)

### Delivery Requirements
- Endpoint must return HTTP 200 within 5 seconds
- Failed deliveries retry: immediately → 1 minute → 5 minutes → then discarded (all retries share the same `eventId`)

## MCP Server

Claap exposes a hosted MCP server at `https://api.claap.io/mcp`.

- **Auth (default)**: OAuth — connecting a client prompts an OAuth flow after you sign in.
- **Auth (alternative)**: API key via `Authorization: Bearer cla_xxxxx` (the same `cla_` key minted in Settings → API & Webhooks). Note this is a `Bearer` header for MCP, distinct from the REST API's `X-Claap-Key` header.
- **Supported clients**: Claude.ai, Claude Desktop, ChatGPT (beta), n8n.
- **Tools**: List Workspaces, Search Companies, Search Contacts, Search Deals, Search Meeting Recordings (by topic/keyword/metadata), and Recording Views & AI Columns (reads smart-table insights).
- **Visibility rule**: a recording is retrievable via MCP only if it (or its folder) is accessible to workspace members and visible in global search — private recordings are not.

## Rate Limits

Rate limit details not publicly documented in the OpenAPI spec or help center (re-checked 2026-06-13). Design conservatively — queue outbound API calls and honor any `Retry-After` headers.

## Important Notes

- Private recordings cannot be accessed via API — only workspace-accessible recordings visible in global search
- Video and transcript URLs expire within 24 hours — fetch and store content immediately upon receipt
- API keys are workspace-scoped — one key per workspace
- Full OpenAPI 3.1.0 spec available at: `https://docs.claap.io/api-reference/openapi.json`
