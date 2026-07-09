<!-- Source: https://support.read.ai/hc/en-us/articles/49381161088659-API-Reference (Help Center 403 on direct WebFetch; details below quoted from current official-page search snippets, re-verified 2026-06-13) -->
<!-- Source: https://support.read.ai/hc/en-us/articles/49379985941523-Read-AI-API-and-MCP-Overview (403 direct; current snippets) -->
<!-- Source: https://support.read.ai/hc/en-us/articles/49380809380371-API-Keys-Authentication (403 direct; current snippets) -->
<!-- Source: https://www.read.ai/post/read-ai-mcp-your-meetings-just-became-your-most-powerful-dev-tool -->
<!-- Source: https://support.read.ai/hc/en-us/articles/16352415827219-Getting-Started-with-Webhooks (403 direct; current snippets) -->
<!-- Source: https://www.read.ai/plans-pricing (fetched 2026-06-13) -->

# Read.ai API Reference

**Note**: Read.ai's Help Center (support.read.ai) returns 403 on direct WebFetch. The REST API details below are quoted from current official Help Center search-result snippets (re-verified 2026-06-13); paths/field lists could not be loaded from the page itself, so treat exact request/response shapes as best-effort until you can open the live docs while signed in.

## REST API

- **Status**: Open beta
- **Base URL**: `https://api.read.ai/` (versioned under `/v1/`)
- **Auth**: Bearer token — include your access token in the `Authorization` header as `Authorization: Bearer ACCESS_TOKEN`. Tokens are issued via OAuth 2.1 with dynamic client registration (Authorization Code grant + refresh tokens). Save `client_id` / `client_secret` on registration; the `client_secret` is shown once. See the API Keys & Authentication page.
- **Rate limit**: 100 requests/minute per user. Exceeding it returns HTTP `429`.
- **Pagination**: cursor-based. Set the `cursor` query parameter to the `id` of the last meeting in the previous page's `data` array. List endpoints return results in reverse-chronological order (newest first).
- **Docs URL**: https://support.read.ai/hc/en-us/articles/49381161088659-API-Reference

### Endpoints

- **List Meetings** — `GET https://api.read.ai/v1/meetings`
  - Query params: `limit`, `cursor` (pagination), `start_time_ms.gte` (filter by start time), `expand` (e.g. `summary`, `metrics`).
  - Example: `curl "https://api.read.ai/v1/meetings?limit=5&start_time_ms.gte=1733700000000" -H "Authorization: Bearer ACCESS_TOKEN"`
  - Response item fields: `id`, `start_time_ms`, `end_time_ms`, `scheduled_start_time_ms`, `scheduled_end_time_ms`, `participants`, `owner`, `title`, `report_url`, `platform`, `platform_id`, `folders`, `live_enabled`.
- **Retrieve a Meeting** — `GET https://api.read.ai/v1/meetings/{meeting_id}`
  - Supports `expand` for `summary` and `metrics`. Active/live meetings have limited or no data for expandable fields (generated after the meeting concludes). Expanding multiple fields or expanding on large list requests is slower.
- **Retrieve a Live Meeting** — fetch real-time transcript and chapter summaries as the meeting progresses (Live-Enabled meetings only), optionally filtered by start time. Live transcription is not enabled for a meeting by default unless someone opens the live dashboard.

### Meeting states
- **Ended Meeting** — completed; identified by `end_time_ms` having a value.
- **Live-Enabled Meeting** — real-time data capture enabled; identified by `live_enabled: true`.

### Planned GA enhancements
- Additional endpoints, tools, and webhook/event support
- Setting to enable live transcription for all meetings
- Expanded documentation

## MCP Server

- **URL**: `https://api.read.ai/mcp/`
- **Transport**: Streamable HTTP
- **Auth**: OAuth — authenticate once; AI tools access securely without exposing API keys in config files
- **Compatible clients**: Claude Code, Claude Desktop, Cursor, VS Code, ChatGPT
- **Architecture**: Full FastAPI server — every tool is also reachable via standard REST HTTP endpoints, so non-MCP workflows can integrate through the REST interface

### Available MCP tools
- List available sessions
- Retrieve transcripts by session
- (Action items, summaries, engagement metrics — "following closely behind")

### Setup
1. Point MCP client at `https://api.read.ai/mcp/`
2. Complete the OAuth authentication flow when prompted
3. Connected — query meeting data via natural language

### Example queries
- "What did we decide about the timeline in yesterday's meeting?"
- "Pull the transcript from today's sprint planning meeting and generate the FastAPI endpoint we discussed"
- "What did [person] tell me about [topic]?"

## Webhooks

- **Setup**: Read dashboard → Integrations → Webhooks
- **Plan requirement**: Pro+ (premium integration)
- **Docs URL**: https://support.read.ai/hc/en-us/articles/16352415827219-Getting-Started-with-Webhooks

### Trigger events
- `meeting_end` — fires when a meeting ends
- `manual` — manually triggered by user

### Payload format
HTTP POST with raw JSON body:

```json
{
  "session_id": "unique-meeting-session-id",
  "trigger": "meeting_end",
  "chapter_summaries": [
    {
      "summary": "...",
      "topics": ["..."]
    }
  ],
  "transcript": [
    {
      "speaker": "Speaker Name",
      "timestamp": 1234567890000,
      "text": "..."
    }
  ]
}
```

Top-level properties:
- `session_id` — unique identifier for the meeting session
- `trigger` — event type (`meeting_end` or `manual`)
- `chapter_summaries` — detailed summaries broken into sequential chapters with associated topics
- `transcript` — full meeting transcript with speaker names and timestamps in Unix time (milliseconds)

### Available data types in webhook payload
- Meeting summary
- Chapters
- Topics
- Action items
- Key questions

### Security
- HMAC SHA-256 signature included in the `X-Read-Signature` request header
- Compute an HMAC SHA-256 hash of the **raw** request body (do not modify, reformat, or re-parse it first) using the signing key from your webhook configuration, then compare to `X-Read-Signature` with a timing-safe comparison
- Reject requests with a missing or invalid `X-Read-Signature` — this verifies the request originated from Read.ai and was not modified in transit

## Zapier Integration

- **Docs**: https://support.read.ai/hc/en-us/articles/18847506033171-Getting-Started-with-Zapier
- **Plan requirement**: Pro+
- **App**: Read AI on Zapier (8,000+ connected apps)

### Triggers
- Meeting report/summary available

### Available data fields
- Meeting summary
- Action items
- Key questions
- Transcript
- Meeting metadata

### Common Zaps
- Meeting notes → Google Docs
- Action items → Asana/Jira/Linear tasks
- Meeting summary → Slack channel
- Contact + meeting data → CRM (Salesforce, HubSpot, Zoho, Dynamics)
- Meeting data → Notion database

## n8n Integration

- Read AI is available as an integration on n8n
- Docs: https://n8n.io/integrations/read-ai/
