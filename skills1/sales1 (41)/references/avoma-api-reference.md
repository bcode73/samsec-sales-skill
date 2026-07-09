<!-- Source: https://dev.avoma.com/ and https://help.avoma.com/api-documentation and https://help.avoma.com/api-integration-for-avoma and https://help.avoma.com/avoma-mcp-server-user-guide -->
<!-- Note: dev.avoma.com is JS-rendered and could not be fully captured via WebFetch. This reference is compiled from the help center articles and partial dev portal info. Auth, key limits, scopes, and MCP re-verified 2026-06-13 against the help center. The exact endpoint paths/schemas still live only on the JS-rendered dev.avoma.com. -->

# Avoma API Reference

## Overview

The Avoma API provides REST access to meetings, recordings, transcripts, notes, scorecards, and webhooks. API access is available on Organization plan and above.

## Authentication

**Method**: API key in HTTP Authorization header

**Format**: `CLIENT_KEY:CLIENT_SECRET` (combined string), passed in the `Authorization` header as a bearer token

**How to create keys**:
1. Navigate to Settings → Organization → Developer (admin-only)
2. Click "Add API Key"
3. Enter a name identifying the key's purpose or owner
4. **Select a scope** (permanent — cannot be changed after creation) and optionally assign a user
5. Copy and securely store the generated credentials

**Scoped API keys** (scope chosen at creation, immutable afterward):

| Scope | Tied to | Access | Best for |
|-------|---------|--------|----------|
| User – limited | Single user | Non-private meetings only | User-level tools that should not see private data |
| User – full | Single user | All meetings incl. private | Personal automations needing full user visibility |
| Organization – limited | Whole org | Non-private meetings org-wide | Reporting/analytics tools using shared data only |

**Key management**:
- **Max 10 API keys per organization**
- One key per integration recommended (not shared across tools)
- Keys can be renamed (pencil icon) without affecting active integrations
- Deleting a key immediately revokes access for all integrations using it
- Regenerating a key issues new credentials while keeping the key name
- **Legacy (pre-scoped) keys**: still functional but read-only in the Developer UI; all legacy keys migrate to "Organization – limited" access by **May 31, 2026** — re-issue scoped keys before then

**Zapier authentication**: Provide "API (Client) Key" and "API (Client) Secret" as separate fields during setup.

## Base URL

`https://dev.avoma.com` (primary API reference and endpoint documentation)

## Rate Limits

- **60 requests per minute** per API key
- Standard REST pagination on list endpoints
- Queue outbound calls for production integrations — 60/min is tight at scale

## Core Entities

| Entity | Description |
|--------|-------------|
| Meetings | Core entity — metadata (title, date, duration, participants), linked to recordings |
| Recordings | Audio/video capture of a meeting; auto-recorded or manually uploaded |
| Transcriptions | Speaker-diarized transcript of a recording |
| Notes | AI-generated meeting notes, structured by template |
| Scorecards | Conversation intelligence scoring results (CI add-on required) |
| Webhooks | Event subscriptions for meeting lifecycle events |

## Webhook Events

| Event | Description |
|-------|-------------|
| New note generated | Fires when AI notes are ready for a meeting |
| New meeting scheduled | Fires when a meeting is booked (via Avoma scheduler or calendar) |
| Meeting rescheduled | Fires when a meeting time/date changes |
| Meeting cancelled | Fires when a meeting is cancelled, includes cancellation reason |

## Integration Patterns

### Webhook-first (recommended)
Subscribe to webhook events and react to meeting lifecycle changes in real time. Preferred over polling for volume.

### Polling (backup)
Use list endpoints with pagination for backfilling history or catching missed webhook events. Rate limit of 60/min constrains backfill speed — queue and throttle.

### Zapier
Pre-built triggers and actions available. Uses separate Client Key and Client Secret fields.

### MCP server
Avoma offers an official MCP (Model Context Protocol) server for surfacing meeting data to LLM clients without building a REST pipeline.

- **Endpoint**: `https://mcp.avoma.com/mcp`
- **Clients**: Claude Desktop (API-key auth, run via npx), plus Claude Web/Mobile and ChatGPT Web/Mobile (admin-managed OAuth)
- **Auth (Claude Desktop)**: the `CLIENT_KEY:CLIENT_SECRET` string used as a bearer token
- **Tools**: list meetings/metadata, fetch full transcripts with timestamps, pull structured notes (key points, decisions, action items), scorecard evaluations, and team usage/engagement metrics
- Access is governed by the same scoped-key permissions as the REST API

## Gaps in This Reference

The full endpoint specification (paths, parameters, response schemas) is documented at dev.avoma.com but could not be captured via automated fetch (JS-rendered). For complete endpoint documentation:

1. Visit https://dev.avoma.com/ in a browser
2. Navigate to the API Reference section
3. Key sections to review: endpoint paths, request/response schemas, pagination parameters, webhook payload formats

The help center at https://help.avoma.com/api-documentation provides a guided overview with links to the full reference.
