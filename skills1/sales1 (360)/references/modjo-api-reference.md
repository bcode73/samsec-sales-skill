<!-- Source: https://api.modjo.ai/v1/swagger.json (Swagger/OpenAPI spec) + https://help.modjo.ai/en/articles/9310645-modjo-api + https://help.modjo.ai/en/articles/10470126-webhooks. Re-verified 2026-06-13. -->

# Modjo API Reference (V1 + V2)

> **⚠️ V1 is deprecated.** As of 2026-06-13 the V1 Swagger UI (`https://api.modjo.ai/v1`) carries a verbatim banner: "Modjo API V1 is deprecated. We recommend migrating to the latest version" and links to the **Modjo API V2 documentation at `https://api.modjo.ai/v2/docs`**. V1 endpoints below still function, but new integrations should target V2. See the [API V2](#api-v2) section.

## Overview

The Modjo API enables programmatic access to call management, user administration, and team operations. API V2 (launched ~April 2026) is the current recommended version and lets you query any Modjo object — Accounts, Opportunities, Users, Tags, and more — with advanced filters to build custom workflows. The V1 `calls/exports` endpoint (still marked BETA) provides selective-relation call export.

## Authentication

API key via `X-API-KEY` header on every request.

```
X-API-KEY: YOUR_API_KEY
```

- **Key generation**: Settings > Integrations > Public API
- **Permissions required**: Administrator or Manager
- **Key must be copied immediately** — cannot be retrieved later
- Store securely — treat as a secret

## Base URL

```
https://api.modjo.ai/v1/
```

## Endpoints

### Calls

#### POST /v1/calls — Upload a call

Two workflows:
1. **Provide recording URL**: Include `recordingUrl` in request body. Modjo downloads within 30 minutes.
2. **Direct upload**: Omit `recordingUrl`. Response includes a signed URL for direct file upload.

**Request body** (`ApiCallUploadDto`):
- `contacts` (required) — array of contact objects
- `users` (required) — array of user identifiers
- `date` (required) — call date/time
- `fileExtension` (required) — one of: wav, mp3, mpeg, m4a, mp4, webm
- `tags` (required) — array of tag strings
- `recordingUrl` (optional) — URL for Modjo to download
- `name` (optional) — call name/title
- `provider` (optional) — source system
- `direction` (optional) — inbound/outbound
- `duration` (optional) — call duration
- `account` (optional) — CRM account reference
- `deal` (optional) — CRM deal/opportunity reference

**Responses**:
- `ApiCallUploadDtoResponse` — includes signed URL for direct upload
- `ApiCallUploadAcknowledgementResponse` — success confirmation (when recordingUrl provided)

#### POST /v1/calls/exports — Export call data (BETA)

Query calls with filtering, pagination, and selective data loading. Returns `ApiV1CallExportPaginationResult` (HTTP 201).

**Request body**:
- `pagination` — `page`, `perPage`
- `filters` — `callStartDateRange`, `minimumCallDuration`, `callTitle`, `callIds`, `deletedRecording`
- `relations` (selective loading): recording, contacts, account, deal, users, libraries, tags, transcript, topics, speakers, summary, highlights, reviews, `aiScoringResults`

### Users

#### GET /v1/users — List users (paginated)

**Parameters**:
- `page` (required, minimum 1)
- `perPage` (required, maximum 100)

**Response**: `ApiV1PublicGetUserPaginationResult`

#### POST /v1/users/bulk — Create multiple users

**Request body** (`CreateBulkUsersDto`):
- `users` — array of user objects

Per-user fields:
- `email` (required)
- `firstName` (optional)
- `lastName` (optional)
- `hasLicense` (optional) — recording license
- `role` (optional)
- `teamIds` (optional) — array of team IDs
- `language` (optional)
- `sendOnboardingEmail` (optional)

#### DELETE /v1/users — Delete users

**Request body** (`ApiV1PublicDeleteUsersDto`):
- `userIds` — array of user IDs to delete

### Teams

#### GET /v1/teams — List teams (paginated)

**Parameters**:
- `page` (required, minimum 1)
- `perPage` (required, maximum 100)

## API V2

API V2 is the current recommended version (V1 is deprecated). Interactive docs: `https://api.modjo.ai/v2/docs`. The OpenAPI spec at `https://api.modjo.ai/v2/swagger.json` requires authentication (returns 401 to anonymous fetches), so the full endpoint schema below the object level was not captured anonymously — confirm exact paths/params against the authenticated docs.

**What V2 adds** (from official "What's New" notes, ~April 2026): query **any Modjo object — Accounts, Opportunities, Users, Tags, and more — with advanced filters** to build specialized workflows on top of your data. Auth is the same `X-API-KEY` header scheme. Pagination and relation/filter selection follow the V1 export pattern.

> Not captured anonymously (authenticated docs required): exact V2 endpoint paths, per-object request/response field schemas, and any V2-specific rate limits.

## Webhooks

Three event types available. All include HMAC-SHA256 signature verification.

Each webhook request is delivered with these HTTP headers (in addition to the body fields below):
- `x-modjo-payload-signature` — the HMAC-SHA256 signature (also mirrored in the body as `payloadSignature`)
- `x-modjo-timestamp` — the timestamp used in the signed data (also mirrored in the body as `timestamp`)

You may verify against either the header or body copy. Endpoints must be HTTPS (official requirement: "Always provide a secure HTTPS endpoint to encrypt data in transit").

### Events

| Event | Triggered when |
|---|---|
| `call_summarized` | AI summary has been generated for a call |
| `call_transcript_deleted` | A call transcript has been deleted |
| `call_recording_deleted` | A call recording has been deleted |

### Webhook payload structure

```json
{
  "timestamp": "2026-01-15T10:30:00Z",
  "payloadSignature": "sha256-hash-string",
  "webhookUuid": "uuid-string",
  "webhookUrl": "https://your-endpoint.com/webhook",
  "tenantName": "your-org",
  "eventName": "call_summarized",
  "payload": { ... }
}
```

### Signature verification

Compute: `SHA256(timestamp + JSON.stringify(payload) + secretToken)`

Compare result against `payloadSignature` in the webhook request. Reject requests that don't match.

## CRM integrations (via native connectors, not API)

Salesforce, HubSpot, Pipedrive, Zoho, Sellsy, Microsoft Dynamics

## Rate limits

Not publicly documented in the API spec. Design conservatively — implement exponential backoff on 429 responses.

## Notes

- V1 Swagger/OpenAPI spec at `https://api.modjo.ai/v1/swagger.json` (renders via the V1 docs UI), now showing a deprecation banner pointing to V2.
- **API V2 is the current recommended version** — docs at `https://api.modjo.ai/v2/docs`; it broadens querying to Accounts, Opportunities, Users, Tags, and more. The V1 `calls/exports` endpoint remains BETA.
- MCP server also available for embedding conversation data into AI workflows.
