<!-- Source: https://help.gong.io/docs/what-the-gong-api-provides, https://help.gong.io/apidocs/introduction-2, https://help.gong.io/docs/gong-engage-api-capabilities, https://help.gong.io/docs/manage-your-crm-api-integration, https://help.gong.io/docs/payload-sent-to-webhooks. Re-verified 2026-06-13. -->

# Gong API Reference

## Overview

Gong provides a REST API for accessing call data, transcripts, user information, CRM integration, and Engage (sales engagement) functionality.

**Base URL**: `https://api.gong.io/v2/` is the common default, but the base URL is **company/region-specific** — Gong's own intro page tells you to read your exact base URL from Gong admin (`https://<your-domain>.app.gong.io/company/api-authentication`). Some orgs are issued region hosts (e.g. `https://us-XXXX.api.gong.io`). Always confirm the base URL shown on your API authentication page rather than hard-coding `api.gong.io`.

**Rate limits** (per official docs): **3 API calls per second** and **10,000 API calls per day**. Gong's docs do NOT publish an hourly limit — there is no "~1,000/hour" tier. HTTP 429 is returned with a `Retry-After` header when exceeded. There is effectively a small concurrency ceiling, so a parallel ingestion pipeline should use a semaphore (queue, don't fan out). To raise limits, contact Gong support via the Gong support request form (per Gong's API intro docs).

**Rate limit headers** (on every response):
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

## Authentication

### Basic Auth (internal integrations)
```
Authorization: Basic <base64(access_key:access_key_secret)>
```

### OAuth 2.0 (public/multi-tenant integrations)
Required when building integrations that serve multiple Gong customers. Bearer token with scoped permissions.

### API Scopes
Gong uses granular per-resource scopes. Common ones:
- `api:calls:read:basic` — list/get call metadata
- `api:calls:read:transcript` — required for `POST /v2/calls/transcript`
- `api:calls:read:extensive` — required for `POST /v2/calls/extensive` (rich call content)
- `api:users:read` — list/get users
- `api:flows:read` — list flows/folders, read prospect assignments (Engage)
- `api:flows:write` — assign/unassign prospects to flows (Engage)
- `api:crm:upload` — upload CRM objects/entities
- `api:crm:schema` — upload CRM object schema
- Additional scopes exist for stats, workspaces, meetings, data privacy, etc.

## Endpoints

### Calls & Recordings

**List calls**
```
GET /v2/calls
```
Filters: date range, users, deal, workspace. Returns paginated call list with metadata.

**Get call details (basic metadata)**
```
GET /v2/calls/{id}
```
Returns: participants, topics, tracker matches, scorecard data, duration, direction, media type, language, recording system.

**Get extensive call data** (rich content — POST with filter body)
```
POST /v2/calls/extensive
```
The supported way to pull detailed call data (trackers, topics, points of interest, parties, CRM context, etc.) in bulk. Takes a `filter` (date range and/or `callIds`) plus a `contentSelector` describing which content sections to include. Requires `api:calls:read:extensive`.

**Get transcript** (⚠️ POST with filter body — NOT a per-id path)
```
POST /v2/calls/transcript
```
The transcript endpoint is `POST /v2/calls/transcript` (no `{id}` in the URL). Pass a `filter` object in the request body containing the date window (`fromDateTime`/`toDateTime`) and optionally a `callIds` array; Gong returns transcripts for matching calls. Response is per-call monologue structure: speaker attribution (`speakerId`), timestamps, and text segments, with cursor pagination. Requires `api:calls:read:transcript`. **This is the most common integration gotcha — it's POST (every other vendor uses GET) AND the callId goes in the body, not the path.**

### Users & Teams

**List users**
```
GET /v2/users
```
Requires `api:users:read` scope. Cursor-based pagination, max 100 per page. Returns users within the company.

**Get a single user**
```
GET /v2/users/{id}
```
Returns one user by Gong-assigned numeric ID.

**Batch user lookup**
```
POST /v2/users/extensive
```
Accepts a filter with a `userIds` array for retrieving multiple users in one request.

### Statistics

User activity/interaction stats are exposed via the `/v2/stats` endpoints (NOT a per-user `/v2/users/{id}/stats` path).

**Activity statistics**
```
POST /v2/stats/activity
```

**Day-by-day activity**
```
POST /v2/stats/activity/day-by-day
```
Daily activity for multiple users over a date range.

**Interaction statistics**
```
POST /v2/stats/interaction
```

### CRM Integration (Generic CRM API)

Register a generic CRM integration first, then upload schema and entities. Endpoints (see Gong's CRM API tag in the in-app API docs):
```
POST /v2/crm/integrations            # register a generic CRM integration
GET  /v2/crm/integration/list        # list registered integrations
POST /v2/crm/integration/delete      # delete an integration
POST /v2/crm/object/schema           # upload object schema (api:crm:schema)
GET  /v2/crm/object/schema/list      # list schema fields
POST /v2/crm/object/entities         # upload CRM objects/entities, LDJSON (api:crm:upload)
GET  /v2/crm/object/list             # list CRM objects
GET  /v2/crm/request-status          # poll status of an async upload request
```
Deprecated: `/v2/crm/map/users` (map users), `/v2/crm/stages` (upload stages). There is no `/v2/crm/object` read/write pair or `/v2/crm/map-fields` endpoint — use the entity/schema endpoints above.

### Engage Flows (Engage API)

The Engage flow API manages flows/folders and prospect assignment (it does NOT create/update flow definitions via `POST /v2/flows` or `PUT /v2/flows/{id}` — those endpoints do not exist).

**List flows / folders** (requires `api:flows:read`)
```
GET  /v2/flows                 # company, personal, and shared flows for a user
GET  /v2/flows/folders         # flow folders
POST /v2/flows/prospects       # flows assigned to given prospects
```

**Assign / unassign prospects** (requires `api:flows:write`)
```
POST /v2/flows/prospects/assign                          # add up to 100 prospects to a flow
POST /v2/flows/prospects/unassign-flows-by-crm-id        # remove prospects by CRM prospect ID
POST /v2/flows/prospects/unassign-flows-by-instance-id   # remove by flow instance ID (up to 100)
```

## Webhook Automation

### Setup
Configure in Gong's Automations tab (Developer Hub). Select "Fire webhook" action.

### Payload format
```json
{
  "callData": {
    "metaData": {
      "id": "string",
      "url": "string",
      "title": "string",
      "scheduled": "datetime",
      "started": "datetime",
      "duration": "number (seconds)",
      "primaryUserId": "string",
      "direction": "Inbound|Outbound",
      "system": "Zoom|Teams|...",
      "scope": "Internal|External",
      "media": "Video|Audio",
      "language": "en-US|...",
      "workspaceId": "string",
      "sdrDisposition": "string",
      "clientUniqueId": "string",
      "customData": "string",
      "meetingUrl": "string",
      "isPrivate": "boolean",
      "calendarEventId": "string"
    },
    "context": [
      {
        "system": "Salesforce",
        "objects": [
          {
            "objectType": "Opportunity",
            "objectId": "string",
            "fields": [{"name": "string", "value": "string"}],
            "timing": "string"
          }
        ]
      }
    ],
    "parties": [
      {
        "id": "string",
        "emailAddress": "string",
        "name": "string",
        "title": "string",
        "userId": "string",
        "speakerId": "string",
        "context": [],
        "affiliation": "Internal|External",
        "phoneNumber": "string",
        "methods": ["Video|Audio|..."]
      }
    ],
    "content": {
      "trackers": [
        {
          "id": "string",
          "name": "string",
          "count": "number",
          "type": "string",
          "phrases": [
            {
              "count": "number",
              "occurrences": [
                {"startTime": "number", "endTime": "number"}
              ],
              "speakerIds": ["string"],
              "text": "string"
            }
          ]
        }
      ],
      "topics": [
        {
          "name": "string",
          "duration": "number",
          "startTimes": ["number"]
        }
      ]
    },
    "interaction": {
      "speakers": [
        {
          "id": "string",
          "userId": "string",
          "talkTime": "number"
        }
      ],
      "interactionStats": {
        "talkRatio": "number",
        "longestMonologueDuration": "number",
        "interactivity": "number"
      },
      "video": [
        {
          "name": "string",
          "duration": "number"
        }
      ]
    },
    "collaboration": {
      "publicComments": [
        {
          "id": "string",
          "audioStartTime": "number",
          "audioEndTime": "number",
          "commenterUserId": "string",
          "comment": "string",
          "posted": "datetime",
          "inReplyTo": "string"
        }
      ]
    }
  },
  "isTest": "boolean"
}
```

### Authentication
Webhook payloads include a Signed JWT header. Copy the public key from Gong Developer Hub and verify the digital signature before trusting the payload.

## Error Codes

| Code | Meaning |
|---|---|
| 400 | Malformed request |
| 401 | Authentication failed |
| 403 | Forbidden (insufficient scopes) |
| 404 | Resource not found |
| 429 | Rate limited — check `Retry-After` header |
| 500+ | Server error — retry with backoff |

## Important Notes

- **Transcript endpoint uses POST with a body filter**: `POST /v2/calls/transcript` — not GET, and the callId(s) go in the request body filter, not the URL path. This is the most common integration mistake.
- **Rate limits**: 3/sec and 10K/day are the only published limits (no hourly tier). Honor `Retry-After`; use a semaphore to respect Gong's low concurrency ceiling. Contact Gong support to raise limits.
- **Backfilling history burns daily quota**: Paginate nightly, not all at once.
- **Call data structure is identical between API and webhooks**: Same schema, same field definitions.
- **OAuth required for multi-tenant**: Basic Auth is for single-org integrations only.
- **Base URL is org/region-specific**: read it from your Gong API authentication page; don't assume `api.gong.io`.
