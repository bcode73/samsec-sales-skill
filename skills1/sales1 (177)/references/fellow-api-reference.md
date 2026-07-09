<!-- Source: https://developers.fellow.ai/reference (llms.txt index + per-endpoint .md pages), https://help.fellow.ai/en/articles/11817206-developer-api, https://fellow.ai/features/api -->
<!-- Re-verified against live official docs on 2026-06-13. The developers.fellow.ai docs publish a machine-readable index at https://developers.fellow.ai/llms.txt with each page/endpoint as Markdown (.md) and OpenAPI — fetch those .md URLs directly rather than the JS-rendered HTML. -->

# Fellow Developer API Reference

## Overview

Fellow captures everything from before, during, and after your meetings. The Developer API opens that data: transcripts, structured AI notes, action items, recordings, and meeting metadata — all available through standard REST calls.

**Project**: Fellow Developer API
**Version**: v1.0
**Docs URL**: https://developers.fellow.ai/reference
**AI/agent index**: https://developers.fellow.ai/llms.txt (Markdown + OpenAPI for every page and endpoint)

## Authentication

### API Key
- **Type**: API Key (scheme name `DeveloperAPIKeyAuth` in the OpenAPI spec)
- **Header**: `X-API-KEY` (send the key as the value of the `X-API-KEY` request header on every call). Unauthenticated requests return `401 Unauthorized`.
- **Base URL**: `https://{subdomain}.fellow.app/api/v1/` — `{subdomain}` is your workspace subdomain (server variable). Note the host is `fellow.app`, and all endpoints are under `/api/v1/`.

### Key management
1. Admin enables Developer API in **Workspace Settings > Security**
2. Each developer creates a personal key in **User Settings > Developer API**
3. API key is shown only once at creation — copy immediately
4. Create a new key for every application for granular access control
5. Admins can view key metadata: name, owner email, status, creation date, last usage
6. Users can disable or delete their own keys
7. Disabling or deleting a user in the workspace automatically disables their API keys

### Access control
- The API only provides access to data that each user can access directly through Fellow's interface
- API access is scoped strictly to the same access the user has in-app
- No workspace-wide admin key exists — each key is user-scoped

## Plan requirements

- **Free**: No API access
- **Team ($7/user/mo annual)**: API access enabled
- **Business ($15/user/mo annual)**: API + CRM sync (Salesforce, HubSpot) + Zapier triggers
- **Enterprise ($25/user/mo annual)**: API + all features

## Endpoints

All endpoints live under the base URL `https://{subdomain}.fellow.app/api/v1/` and require the `X-API-KEY` header. List endpoints use `POST` with a JSON body (filters/include/pagination), not `GET` query strings.

### Recordings
- `POST /recordings` — list recordings. Body: `pagination` (cursor + `page_size`), `include` (booleans `transcript`, `ai_notes`), `filters` (`event_guid`, `created_at`/`updated_at` ranges, `channel_id`, `title`), `media_url` (pre-signed URL expiry, 1–24h, default 12h). Response: `recordings.data[]` (id, title, timestamps, transcript, ai_notes, media_url) + `recordings.page_info`.
- `GET /recording/{recording_id}` — get one recording by id.
- `DELETE` recording — delete a recording (see llms.txt `delete_recording`).

### Notes (AI notes)
- `POST /notes` — list notes. Body: `pagination`; `filters` (`event_guid`, `created_at_start/end`, `updated_at_start/end`, `channel_id`, `title`, `event_attendees[]`); `include` (`event_attendees`, `content_markdown`, both default false). Response: `notes.data[]` (id, created_at, updated_at, title, event details, `recording_ids`, attendees, markdown content) + `notes.page_info`.
- `GET /note/{note_id}` — get one note by id.
- `DELETE` note — delete a note (see llms.txt `delete_note`).

### Action items
- `POST /action_items` — list action items. Body: `pagination`; `filters` (`completed`, `archived`, `ai_detected`, `ai_suggestion_accepted_by_user`, `scope`); `order_by` (`created_at_desc` default, `created_at_asc`, `due_date`); `include`. Response: items with id, text, status (Done/Archived/Incomplete), created_at, updated_at, due_date, `assignees[]` (id, full_name, email), completion_type, AI-detection metadata.
- `GET /action_item/{action_item_id}` — get one action item by id.
- `POST /action_item/{action_item_id}/complete` — mark complete/incomplete (body: `completed` boolean).
- `POST /action_item/{action_item_id}/archive` — archive an action item.

### User
- `GET /me` — authenticated user. Response: `user` (id, email, full_name) + `workspace` (id, name, subdomain).

### Webhooks (management endpoints)
- `GET /webhooks` — list webhooks (supports filters + pagination).
- `POST /webhooks` — create a webhook (see Webhooks section below for body).
- `GET /webhooks/{id}` — get one webhook.
- `PATCH /webhooks/{id}` (update) and `DELETE /webhooks/{id}` (delete) — manage a webhook (see llms.txt `update_webhook`, `delete_webhook`).

## Pagination

Cursor-based. Send a `pagination` object in the request body:
- `cursor` — `null` on the first request, then the value returned in the previous response's `page_info.cursor`.
- `page_size` — integer 1–50, default 20.

Responses wrap results in a `page_info` object (`cursor`, `page_size`) alongside the `data` array. Keep paging until `page_info.cursor` is `null`.

## Rate limits

Documented per API key:
- **3 requests per second** per API key
- **10,000 requests per day** per API key

Exceeding either returns HTTP `429` with error code `rate_limited`. Fellow notes it may adjust limits over time and may set different limits per pricing plan. Handle `429` with exponential backoff.

## Status / error codes

- `200` — success
- `400` — input validation error (bad payload)
- `401` — unauthenticated (missing/invalid `X-API-KEY`)
- `403` — API key's user lacks API access or access to the requested resource
- `404` — resource not found
- `429` — `rate_limited`
- `500` — unexpected server error

## Webhooks

Fellow supports outbound webhooks (Svix-backed delivery).

### Event types
- `ai_note.generated` — AI notes created from a meeting recording
- `ai_note.shared_to_channel` — AI notes shared to a channel
- `action_item.assigned` — action item assigned to a user
- `action_item.completed` — action item marked complete

### Payloads
Event-specific. AI-note payloads include `event_title`, `ai_notes`, `transcript`, and `attendees`. Action-item payloads include `text`, `assignees`, `status`, and `due_date`.

### Signature verification (Svix)
HMAC-SHA256. Each delivery includes three headers:
- `svix-id` — unique message id
- `svix-timestamp` — Unix timestamp
- `svix-signature` — formatted `v1,<base64-signature>` (may carry multiple space-separated signatures)

Verify by computing HMAC-SHA256 over the string `{svix-id}.{svix-timestamp}.{raw-request-body}` using your webhook signing secret (a `whsec_`-prefixed, base64-encoded key), then comparing to the `v1,` signature. The secret is returned only once when the webhook is created.

### Creating a webhook
`POST /api/v1/webhooks` with the `X-API-KEY` header and body:
```json
{
  "url": "https://example.com/webhooks/fellow",
  "enabled_events": ["ai_note.generated"],
  "description": "optional description",
  "status": "active"
}
```
The response returns the signing secret — save it immediately; it is shown only once.

## Audit logging

- Complete audit logging for up to 90 days
- Real-time API logs page with export capabilities
- IP address logging and request body hashing
- Admin-only access to audit logs
- Supports e-discovery and compliance requirements

## Security

- All requests encrypted over HTTPS
- SOC 2 Type II compliant
- HIPAA and GDPR compliant
- Fellow never trains on customer data

## MCP Server (official)

Fellow hosts an **official** MCP server.
- **URL**: `https://fellow.app/mcp`
- **Auth**: OAuth (workspace admin must enable it before users connect)
- **Clients**: Claude (Custom Connectors), Cursor, ChatGPT (Custom Connectors / Developer Mode), and any AI tool that supports MCP connectors
- Access is scoped to the data the connecting user can already see in Fellow

A separate community/third-party MCP server (`github.com/liba2k/fellow-mcp`) also exists, wrapping the REST API locally.

## Zapier integration (alternative to direct API)

Available on Team, Business, and Enterprise plans:
- **Triggers**: New agenda, new AI notes, new transcript
- Supports multi-step automations: summarize with LLM, update CRM, enrich tickets
- 8,000+ downstream app connections
- Some triggers require manual kickoff

## n8n integration

Official Fellow n8n node: `fellowapp/n8n-nodes-fellow` on GitHub.

## Limitations / gaps not confirmed in live docs

- Exact request/response schemas for `delete_note`, `delete_recording`, and webhook `update`/`delete`/`get-by-id` bodies were not captured field-by-field — paths are inferred from the published endpoint index (llms.txt). Confirm against the live OpenAPI before relying on them.
- No OAuth flow for the REST API (API-key auth only); OAuth is used by the MCP server, not the REST endpoints.
- API key is user-scoped only — no workspace-wide key for team-level pipelines.
