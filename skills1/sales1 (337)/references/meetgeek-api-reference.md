<!-- Source: https://docs.meetgeek.ai — re-verified 2026-06-13 against the official Markdown docs (docs.meetgeek.ai/llms.txt + /api/... .md pages). -->

# MeetGeek API Reference

## Overview

MeetGeek provides a REST API for programmatic access to meetings, transcripts, highlights, summaries, and recordings. The API also supports webhooks for event-driven automation and an MCP Server for AI tool integration.

## Regional Endpoints

MeetGeek offers three API endpoints hosted in different regions:

| Region | Base URL |
|---|---|
| Europe (default) | `https://api.meetgeek.ai` |
| Europe (explicit) | `https://api-eu.meetgeek.ai` |
| United States | `https://api-us.meetgeek.ai` |

Requests to `https://api.meetgeek.ai` are routed to the European data center by default.

**Important**: API keys are region-specific. Each region requires its own API key. If you need to make requests to multiple regions, generate and use a separate API key for each.

## Authentication

Bearer token authentication.

```
Authorization: Bearer YOUR_API_KEY
```

Generate your API key at: Integrations → Public API Card in the MeetGeek dashboard.

Optionally configure a webhook URL for meeting analysis notifications during key setup.

## Endpoints

### Get meetings
```
GET /v1/meetings
```
Retrieve paginated past meetings of a user. Query params: `limit` (integer, min 1, max 500 — number of records to fetch) and `cursor` (string — cursor to continue reading from for pagination).

### Get meeting
```
GET /v1/meetings/{meetingId}
```
Get meeting details given a meeting ID.

### Delete meeting
```
DELETE /v1/meetings/{meetingId}
```
Delete a meeting.

### Get transcript
```
GET /v1/meetings/{meetingId}/transcript
```
Retrieve the transcript for a meeting.

### Get highlights
```
GET /v1/meetings/{meetingId}/highlights
```
Retrieve highlights for a meeting.

### Get summary
```
GET /v1/meetings/{meetingId}/summary
```
Get the AI-generated summary for a meeting.

### Get insights
```
GET /v1/meetings/{meetingId}/insights
```
Get all conversation-intelligence insights (KPIs) for a meeting. Response includes `kpi_meeting` (per-participant performance metrics — talk time, words per minute, longest monologue, scores + interpretations), `kpi_popular_themes` (frequently discussed topics with mention counts), `kpi_improvement` (practices to keep + recommendations), and an `old_view` boolean flag. Returns `204 No Content` for meetings before December 2024 (insights not available for older meetings).

### Download recording
```
POST /v1/meetings/{meetingId}/download
```
Generate a temporary download link for the meeting recording.

### Upload recording
```
POST /v1/upload
```
Upload an audio/video recording for analysis. Request body: `download_url` (required — a publicly accessible URL that triggers a direct download of the file), `language_code` (optional — see language-codes appendix), `template_name` (optional — see template-names appendix). The file is fetched from `download_url`; this is not a multipart binary upload.

### Get teams
```
GET /v1/teams
```
List teams in the workspace.

### Get team meetings
```
GET /v1/teams/{teamId}/meetings
```
Retrieve meetings for a specific team.

## Rate limits

| Plan | Requests | Uploads |
|---|---|---|
| Free & Pro | 100 requests/day | 10 uploads/day |
| Business & Enterprise | 100 requests/minute | 10 uploads/minute |

Need more? MeetGeek directs higher-volume / service-account use to their contact form for a custom quote.

## Webhooks

Configure a webhook URL in the MeetGeek dashboard at Integrations → Public API section. Webhooks fire once a meeting's analysis (transcript, highlights, summary, insights) is complete.

### Events / payloads
Two events are delivered as `POST` requests with a JSON body:

- **Successful analysis**:
  ```json
  { "message": "File analyzed successfully", "meeting_id": "<uuid>" }
  ```
- **Failed analysis**:
  ```json
  { "message": "File analyzed failed" }
  ```
  (Note: the failure payload does NOT include `meeting_id`.)

### Acknowledgement & retries
Your endpoint must respond with `HTTP 200 OK` and an empty body. MeetGeek sends up to **3 POST attempts total** — the initial request plus two retries — and only retries if it does not receive a `200 OK` acknowledgement.

### Signature verification
Each webhook includes an `X-MG-Signature` header. MeetGeek computes an **HMAC SHA-256** of the exact raw request body (`body_bytes`) using the configured webhook secret. Verify by recomputing the HMAC over the raw body with your secret and comparing with a **constant-time** comparison (`hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node.js, `hmac.Equal` in Go) to avoid timing attacks.

### Team-level delivery
For shared meetings, the webhook fires for all team members with view access — provided the meeting owner has granted Share Access to those teams.

## MCP Server

MeetGeek provides an official MCP (Model Context Protocol) server for AI tool integration:

- **Cloud MCP**: Hosted endpoint `https://mcp.meetgeek.ai/mcp`. Connect in Claude via Settings → Connectors (find MeetGeek) or add the endpoint manually in developer mode; in ChatGPT via the Apps store or developer mode. Complete the OAuth flow at `auth.meetgeek.ai`. No local install.
- **Local MCP**: Runs on your machine using your API key. Install with `npm install -g @meetgeek/mcp-server`; the client config command is `meetgeek-mcp`.

Available tools: list meetings, retrieve transcripts, get summaries, search across meeting history.

## Additional Resources

- Docs index (Markdown, LLM-friendly): `https://docs.meetgeek.ai/llms.txt`
- OpenAPI specification: `https://docs.meetgeek.ai/api-reference/openapi.json`
- Per-endpoint Markdown docs: `https://docs.meetgeek.ai/api/api-reference/v1/<endpoint>.md`
- Appendices: language codes, template names, and webhooks under `/api/api-reference/v1/appendix-*.md`
- Enterprise/service account access: contact form for a custom quote (link in docs)

## Gaps

- The GitHub repo previously cited (`github.com/meetgeekai/meetgeek-mcp-server`) is no longer referenced by the official docs; the documented local install is the `@meetgeek/mcp-server` npm package. Repo URL left in learnings but treat the npm package as canonical.
- Full response schemas for transcript/highlights/summary verified to exist via the per-endpoint Markdown docs; only the fields most useful for integration are summarized here.
