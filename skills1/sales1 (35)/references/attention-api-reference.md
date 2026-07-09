<!-- Source: https://docs.attention.com/llms.txt, https://docs.attention.com/api-authentication, https://docs.attention.com/api-reference/openapi.json -->

# Attention API Reference

## Overview

**Base URL**: `https://api.attention.tech/v2`
**OpenAPI Version**: 3.0.1
**API Version**: 1.8.0 (re-verified 2026-06-13 against the live OpenAPI spec)
**Authentication**: APIKeyHeader — `Authorization` header, security scheme `APIKeyHeader` (`type: apiKey`, `name: Authorization`, `in: header`). The api-authentication doc and security scheme both use the `Authorization` header; pass the key as a Bearer token.

```
Authorization: Bearer YOUR_API_KEY
```

## API Key Management

### Obtaining a key
1. Log into https://app.attention.tech
2. Navigate to avatar → Settings → Organization → API Keys (requires Admin permissions)
3. Click "+ Create API Key", provide a descriptive name
4. Copy immediately — key displays only once

### Security best practices
- Use environment variables, never hardcode
- Separate keys per environment (dev/staging/prod)
- Audit usage regularly
- Never commit keys to version control

### Error responses
- `401 Unauthorized` — invalid key, expired key, or missing auth header
- `429 Too Many Requests` — rate limit exceeded, contact account manager for increases

## Endpoints

### API Keys

- `GET /api_keys` — List API keys
- `POST /api_keys` — Create API key
- `DELETE /api_keys` — Delete API key

### Calendar

- `GET /calendar_events/{user_uuid}` — List calendar events for a specific user (paginated). Path now takes the user UUID as a path param (was `/calendar/events` in earlier captures).

### Conversations

- `GET /conversations` — List conversations with filtering (date ranges, participants, teams, status, pagination)
- `GET /conversations/list` — List conversations, optimized variant (lighter payload for large pulls)
- `GET /conversations/{id}` — Get conversation details (transcription, participants, metadata; customizable includes/excludes via query params)
- `GET /conversations/by-external-id/{externalId}` — Look up a conversation by your external system's ID (useful for CRM/warehouse reconciliation)
- `PUT /conversations/{id}` — Update conversation metadata (title, participants, associated metadata)
- `DELETE /conversations/{id}` — Archive conversation
- `PUT /conversations/{id}/title` — Change conversation title
- `PUT /conversations/{id}/labels` — Change conversation labels
- `PUT /conversations/{id}/change_privacy` — Toggle conversation privacy (private ↔ public)
- `PUT /conversations/{id}/linked-crm-records` — Update the CRM records linked to a conversation
- `POST /conversations/{id}/crm/confirm` — Confirm AI-extracted CRM intelligence before it is pushed to the CRM
- `POST /conversations/{id}/trigger-native-integration` — Re-run / trigger a native integration for the conversation
- `POST /conversations/{id}/media/download` — Generate presigned URL for media file download (organization-level auth only)
- `GET /conversations/upload-url` — Get signed URL for uploading conversation files
- `POST /conversations/import` — Import conversation from external source (Gong, Salesforce, etc.) — creates new conversation and runs through transcription/analysis pipeline
- `GET /conversations/workflow-logs` — Retrieve workflow processing logs

### Email

- `GET /emails` — List emails with filtering
- `GET /email-templates` — List email templates

### Generalized Insights (GI)

- `GET /gi/history` — Retrieve generalized insights history for a user (tracks evolution of insights over time, pagination support)

### Organization Management

- `GET /organizations/users` — List org users (filter by team UUID)
- `POST /organizations/users` — Create user (assign to team with role, returns UUID)
- `PATCH /organizations/users/{userId}` — Update user (name, email, team, role)
- `DELETE /organizations/users/{userId}` — Delete user (permanent, revokes all access)
- `GET /organizations/teams` — List teams
- `POST /organizations/teams` — Create team (optional parent team for hierarchy)
- `PATCH /organizations/teams/{teamId}` — Update team (name, parent assignment)
- `GET /organizations/roles` — List available roles

### SCIM Provisioning (Okta, Azure AD)

- `GET /scim/ServiceProviderConfigs` — SCIM capabilities (path is now plural `ServiceProviderConfigs`)
- `GET /scim/Users` — List users (filter, paginate)
- `GET /scim/Users/{id}` — Get user
- `POST /scim/Users` — Create user
- `PUT /scim/Users/{id}` — Replace user
- `PATCH /scim/Users/{id}` — Partial update user
- `GET /scim/Groups` — List groups (filter, paginate)
- `GET /scim/Groups/{id}` — Get group
- `POST /scim/Groups` — Create group
- `PUT /scim/Groups/{id}` — Replace group
- `PATCH /scim/Groups/{id}` — Partial update group

### Scorecards

- `POST /createScorecardResult` — Create scorecard result for a conversation
- `POST /scorecards/summary` — Retrieve scorecard usage statistics for users/teams within a time period (method is **POST**, not GET — filters go in the request body)
- `GET /scorecards` — List scorecards
- `POST /scorecards` — Create a scorecard
- `GET /scorecards/{id}` — Get a scorecard
- `PATCH /scorecards/{id}` — Update a scorecard
- `GET /scorecards/{id}/items` — List scorecard items
- `POST /scorecards/{id}/items` — Create a scorecard item
- `GET /scorecards/{id}/items/{itemId}` — Get a scorecard item
- `PATCH /scorecards/{id}/items/{itemId}` — Update a scorecard item
- `DELETE /scorecards/{id}/items/{itemId}` — Delete a scorecard item

### Teams

- `GET /teams` — List all teams (name, UUID, parent team, hierarchy)
- `GET /teams/{id}` — Get team details
- `GET /teams/{id}/members` — List team members (user details + roles)

### Tools

- `POST /ask_attention` — Analyze conversations/prompts for insights (DEPRECATED — use v2)
- `POST /ask_attention/v2` — Analyze conversations/prompts for insights (current)
- `POST /create_deck` — Generate presentation deck from conversations/deals (path is now `create_deck`, not `createDeck`)
- `POST /snippets` — Create shareable conversation snippet
- `POST /changeConversationOpportunity` — Link conversation to CRM opportunity
- `GET /connectionReport` — Show which users have connected calendar/email (no params; path is now `connectionReport`)
- `GET /usageReport` — Usage statistics for users/teams within time period (path is now `usageReport`)

### CRM

- `POST /crm/query` — Execute a CRM query against the connected CRM (Salesforce/HubSpot) and return matching records

### Labels

- `GET /labels` — List call labels
- `POST /labels` — Create a label
- `GET /labels/{id}` — Get a label
- `PATCH /labels/{id}` — Update a label
- `DELETE /labels/{id}` — Delete a label

### Field Configurations

- `GET /field-configurations` — List field configurations (the schema that drives CRM auto-update field mapping)
- `POST /field-configurations` — Create a field configuration
- `GET /field-configurations/{id}` — Get a field configuration
- `PATCH /field-configurations/{id}` — Update a field configuration
- `DELETE /field-configurations/{id}` — Delete a field configuration
- `GET /field-configurations/{id}/items` — List items within a field configuration
- `POST /field-configurations/{id}/items` — Create a field configuration item
- `GET /field-configurations/{id}/items/{itemId}` — Get a field configuration item
- `PATCH /field-configurations/{id}/items/{itemId}` — Update a field configuration item
- `DELETE /field-configurations/{id}/items/{itemId}` — Delete a field configuration item

### Knowledge Base

- `GET /knowledge-base/sources` — List knowledge base sources
- `POST /knowledge-base/sources` — Create a knowledge base source
- `POST /knowledge-base/sources/upload` — Request a presigned upload URL for a KB source
- `GET /knowledge-base/sources/{sourceId}` — Get a KB source
- `PATCH /knowledge-base/sources/{sourceId}` — Update a KB source
- `DELETE /knowledge-base/sources/{sourceId}` — Delete a KB source
- `POST /knowledge-base/sources/{sourceId}/confirm-upload` — Confirm a completed KB source upload

### Super Agent

- `POST /super-agent/messages` — Send a message to the Super Agent; returns 202 Accepted with a session ID for polling. Optionally accepts a `callback_url` for a webhook-style notification when the assistant response is ready.
- `GET /super-agent/sessions` — List Super Agent sessions
- `GET /super-agent/sessions/{sessionId}/messages` — Get a session's message history
- `DELETE /super-agent/sessions/{sessionId}` — Delete a Super Agent session

### Other

- `GET /chats` — List chats
- `GET /integration-workflows` — List integration workflows
- `GET /library/folders` — List the library folder structure
- `PUT /teams/{id}/opportunity` — Update a team's opportunity association

### Users

- `GET /users` — List users (filter by id, email, team UUID)

## Response formats

Supports `application/json` and `application/vnd.api+json`.

## Code examples

### cURL
```bash
curl https://api.attention.tech/v2/conversations \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Python
```python
import requests

headers = {"Authorization": "Bearer YOUR_API_KEY"}
response = requests.get("https://api.attention.tech/v2/conversations", headers=headers)
```

### Node.js
```javascript
const response = await fetch("https://api.attention.tech/v2/conversations", {
  headers: { "Authorization": "Bearer YOUR_API_KEY" }
});
```

## MCP Server

Official **hosted/remote** MCP server for Claude, ChatGPT, Cursor, and other MCP clients.

- **Server URL**: `https://api.attention.tech/mcp` (MCP over HTTP Streamable transport)
- **Auth (interactive clients)**: OAuth 2.1 with Dynamic Client Registration (DCR) — users authenticate through Attention's login flow (e.g. in Claude.ai)
- **Auth (programmatic)**: API Key JWTs sent as Bearer tokens on the `Authorization` header
- Docs: https://docs.attention.com/mcp/authentication (MCP tool sections: AI Analysis, API Keys, Calls, CRM, Forecasting, Identity, Intelligence, Labels, Organization, Reports, Scorecards, Snippets, Super Agent, Teams, Users & Roles)
- Capabilities: Search calls, get transcripts, analyze deals/forecasting, review scorecards, query CRM, surface coaching insights via natural language
- Community self-host repo (older, not the hosted server): https://github.com/highgravitas/attention-mcp

## Workflow Builder API

Workflows can be configured via the UI (docs.attention.com/builder-101/):
- **Triggers**: After call ends, on schedule, Attention-specific triggers
- **Action steps**: CRM update, email, Slack, webhook, custom
- **Monitoring**: Workflow run logs for debugging

## Documentation index

Full docs at https://docs.attention.com. OpenAPI spec at https://docs.attention.com/api-reference/openapi.json.
