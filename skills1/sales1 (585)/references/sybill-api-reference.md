# Sybill API Reference

*Captured 2026-06-13 from the public developer docs at https://api.sybill.ai/docs (REST), https://api.sybill.ai/docs/mcp.html (MCP), and the webhook help article. The REST API is in **alpha** — Sybill states "Endpoints, request/response schemas, rate limits, and behavior may change at any time without prior notice."*

## Access / plan gating

- The developer docs are now **public**, but on the pricing comparison **API + MCP access is listed under Enterprise only**. Webhook automations are available on **Pro and up**. Treat REST/MCP as Enterprise-gated for access, even though the schemas are documented openly.

## Base URL & auth

- Base URL: `https://api.sybill.ai`
- Auth: `Authorization: Bearer sk_live_<YOUR_KEY>`
- Keys: created in the dashboard at **Settings → Integrations → API Keys**; full key shown once at creation. Org-scoped.
- Scopes: `read` (GET), `ingest` (POST/PATCH/DELETE), `ask_sybill` (AI assistant).
- Errors: missing/invalid key → `401 Unauthorized`; valid key lacking the required scope → `403 Forbidden`. Key revocation is permanent and immediate.
- All requests except `/v1/health` require a valid key.

## Rate limiting

Per-key moving-window counters, shared across all endpoints:

- 60 requests / minute
- 1,000 requests / hour
- 10,000 requests / day

Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (Unix ts), `Retry-After` (seconds). Exceeding limits returns `429` with body `{"detail": "Rate limit exceeded"}`; back off and retry after `Retry-After`. The MCP server shares these same limits.

## Pagination

Cursor-based. Query params: `limit` and `cursor`. Defaults: 20 (conversations, deals, accounts), 50 (messages, rows, documents). Max page size: 50 for all endpoints. Response `pagination` object has `hasMore` (bool) and `nextCursor` (opaque token, null when exhausted). Pass `nextCursor` back as `cursor`; do not parse/construct cursors. Filters apply only to the first request — the cursor preserves query context.

## REST endpoints

### Health
- `GET /v1/health` — verifies the API key; returns org ID and granted scopes. (No auth-scope required beyond a valid key.)

### Conversations
- `GET /v1/conversations` — paginated list. Filters: `startedAfter`, `startedBefore`, `type`, `title`, `attendees`, `crmName`, `sourceId`, `cursor`, `limit` (default 20).
- `GET /v1/conversations/{conversationId}` — full detail (summary, transcript, recording URLs, participants, CRM info).
- `POST /v1/conversations` — upload a conversation with transcript and/or recording URL → `201 Created`.
- `DELETE /v1/conversations` — soft-delete via `remoteId` + `sourceId` query params.

### Deals
- `GET /v1/deals` — paginated list. Filters: `name`, `stage`, `closed`, `owner`, `closeDateAfter`, `closeDateBefore`, `amountMin`, `amountMax`, `lastActivityAfter`, `lastActivityBefore`, `cursor`, `limit`.
- `GET /v1/deals/{dealId}` — full detail incl. summary, CRM-autofill suggestions, contacts.

### Accounts
- `GET /v1/accounts` — paginated list. Filters: `name`, `website`, `owner`, `createdAfter`, `createdBefore`, `lastActivityAfter`, `lastActivityBefore`, `cursor`, `limit`.
- `GET /v1/accounts/{accountId}` — detail incl. contacts and synced CRM fields.

### Messages
- `GET /v1/messages` — paginated list. Filters: `sourceId`, `remoteId`, `threadId`, `participantEmail`, `createdAfter`, `createdBefore`, `cursor`, `limit` (default 50).
- `GET /v1/messages/{messageId}` — full message body + attachment metadata.
- `POST /v1/messages` — create → `201 Created`.
- `DELETE /v1/messages` — soft-delete via `remoteId` + `sourceId`.

### Rows (custom structured records)
- `GET /v1/rows` — filters: `sourceId`, `objectTypeId`, `remoteId`, `name`, `createdAfter`, `createdBefore`, `cursor`, `limit` (default 50).
- `GET /v1/rows/{rowId}` — single row.
- `POST /v1/rows` — create.
- `PATCH /v1/rows` — partial update via `remoteId` + `sourceId`.
- `DELETE /v1/rows` — soft-delete via `remoteId` + `sourceId`.

### Documents
- `GET /v1/documents` — filters: `sourceId`, `name`, `cursor`, `limit` (default 50).
- `GET /v1/documents/{documentId}` — full document + processed-text links.
- `POST /v1/documents` — create from URL or base64 → `201 Created`.
- `PATCH /v1/documents` — update via `remoteId` + `sourceId`.
- `DELETE /v1/documents` — soft-delete via `remoteId` + `sourceId`.

### Sources
- `POST /v1/sources` — create with `name` + `displayName`.
- `GET /v1/sources` — list (optional `name` filter).
- `GET /v1/sources/{sourceId}` — fetch one.
- `PATCH /v1/sources/{sourceId}` — rename via `displayName`.
- `DELETE /v1/sources/{sourceId}` — delete.

### Object Types (schemas for Rows)
- `POST /v1/object-types` — create schema with field definitions.
- `GET /v1/object-types` — list (optional `sourceId` filter).
- `GET /v1/object-types/{objectTypeId}` — fetch one.
- `PATCH /v1/object-types/{objectTypeId}` — update `displayName` and/or `fieldDefinitions`.
- `DELETE /v1/object-types/{objectTypeId}` — delete.

## MCP server

- Endpoint: `https://mcp.sybill.ai/mcp` (Streamable HTTP transport).
- Auth: OAuth — the MCP client prompts you to sign in with your Sybill account.
- Tools: `ask_sybill`, `get_ask_sybill_result`, `list_conversations`, `get_conversation`, `list_deals`, `get_deal`, `list_accounts`, `get_account`.
- Shares the REST API rate limits.

## Webhooks (Pro+)

- Configure under **Settings → Integrations → Automations**. Filter by participants, topic trackers, meeting type, deal parameters.
- Delivery: HTTP `POST` to your endpoint via **Svix**.
- Event today: `meeting.new_recording.v1` ("New Meeting Recording"). Payload includes metadata (title, duration, platform, participants, start time), summary (key takeaways, next steps, outcome, conversation starters), per-participant insights (name, email, interests, pain points), full transcript with speaker IDs + timestamps, and CRM info (account/opportunity IDs + names when linked).
- **Signing: HMAC via Svix.** Verify the webhook signature and timestamp before processing; the signing secret is available in the Sybill dashboard. Svix client libraries handle verification.
- Retries: exponential backoff — immediately, then 5s, 5m, 30m, 2h, 5h, then 10h intervals; stops when the endpoint is removed/disabled.

## Known gaps / unverified

- Exact Svix header names (`svix-id` / `svix-timestamp` / `svix-signature`) are not named in the Sybill help article (standard Svix headers, but not quoted by Sybill).
- Full request/response JSON schemas per endpoint live in the published OpenAPI spec at `https://api.sybill.ai/docs/openapi.yaml` (not transcribed here).
- Whether REST API access is purchasable below Enterprise is not stated; pricing page gates API + MCP to Enterprise.

## Sources

- https://api.sybill.ai/docs/introduction.html
- https://api.sybill.ai/docs/authentication.html
- https://api.sybill.ai/docs/rate-limiting.html
- https://api.sybill.ai/docs/pagination.html
- https://api.sybill.ai/docs/endpoints.html
- https://api.sybill.ai/docs/data-models.html
- https://api.sybill.ai/docs/mcp.html
- https://help.sybill.ai/en/articles/9925117-webhook-automations-with-sybill
- https://www.sybill.ai/pricing
- https://www.sybill.ai/integrations
