<!-- Source: https://fourfour.ai/developers and https://fourfour.ai/developers/api (captured 2026-06) -->
<!-- Captured via WebFetch; the live docs are a JS-rendered developer portal, so field-level
     payloads below marked "Constructed from docs" are representative shapes assembled from the
     documented field lists — verify against the generated schema at fourfour.ai/developers/api. -->

# Four/Four API Reference

Four/Four exposes three programmatic surfaces plus an MCP server:

1. **OData REST API** — read Insights, Conversations, CRM objects, and tracking data (`/odata`).
2. **CRM Importer API** — push accounts/contacts/leads/opportunities/users in (`/import`).
3. **Webhooks** — signed HTTP POST notifications on changes.
4. **MCP Server** — `https://fourfour.ai/mcp` for Claude / ChatGPT / Cursor.

Base host: `https://fourfour.ai`. All requests are HTTPS.

---

## 1. Authentication

### OAuth2 (for the OData API)

OAuth2 **authorization-code flow with refresh tokens** is used to authenticate OData API requests.

- **Authorization endpoint:** `https://fourfour.ai/oauth/authorize`
- **Token endpoint:** `https://fourfour.ai/oauth/token`
- **Supported scope:** `api:read`
- **Grant type:** `authorization_code` (plus `refresh_token` to renew)

Authorization request parameters:
- `response_type=code`
- `client_id`, `client_secret`
- `redirect_uri` — must be HTTPS (except `localhost`)
- `scope=api:read`
- `state` — recommended for CSRF protection

**Exchange the code for a token:**

```bash
curl https://fourfour.ai/oauth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -X POST \
  -d 'grant_type=authorization_code&code={code}&client_id={id}&client_secret={secret}&redirect_uri={uri}'
```

Token response (`token_type: Bearer`, `expires_in: 86400` = 24h):

```json
<!-- Constructed from docs — verify against live API -->
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "def502...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "scope": "api:read"
}
```

Use the token on every OData call: `Authorization: Bearer {access_token}`.

> The OData service also supports HTTP **Basic** auth over HTTPS for BI clients (PowerBI / Tableau / Excel). Prefer OAuth2 for server-to-server integrations and keep `client_secret` server-side.

### Personal Access Token (for the CRM Importer API)

The CRM Importer (`/import`) authenticates with a **Personal Access Token** sent as a bearer token: `Authorization: Bearer {pat}`.

---

## 2. OData REST API

Base: `https://fourfour.ai/odata`

OData v4 conventions. Integrates directly with PowerBI, Tableau, and Excel.

### Auth quick-start (simplest GET)

```bash
curl https://fourfour.ai/odata/me \
  -H 'Authorization: Bearer {access_token}'
```

### Entity sets

**Core**
- `Insights` — individual findings extracted from conversations; linked to participants and CRM objects
- `Topics` — groups of insights organized by common theme
- `TopicModels` — groups of topics built from a filtered set of insights
- `Conversations` — discussion records (calls, meetings, tickets, emails, chat) with participants and related entities
- `Participants` — conversation attendees with roles and token counts

**CRM**
- `Accounts`, `Contacts`, `Leads`, `Opportunities`, `Owners`, `Cases`, `Calls`, `CalendarEvents`

**Tracking**
- `TrackerProjects`, `TrackerIssues`, `TrackerComments`, `Labels`, `Objects`

**Communication**
- `Chats`, `ChatMessages`, `Fragments`

### Standard endpoints (per entity set)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/odata/me` | Info about the user and tenant that authorized the application |
| GET | `/odata/{EntitySet}` | List entities |
| GET | `/odata/{EntitySet}({id})` | Retrieve a single entity by id |
| GET | `/odata/{EntitySet}({id})/{RelatedEntity}` | Access related/expanded entities |

### Query options

All collection endpoints support standard OData query options:

- `$select` — choose returned properties
- `$filter` — filter by property values
- `$orderby` — sort
- `$top` / `$skip` — pagination (page size / offset)
- `$count` — include the total count
- `$expand` — include related entities inline
- `search` — full-text search

### Pagination

Server-driven paging. Pass `$top` (page size) and `$skip` (offset); responses include an `@odata.nextLink` you can follow until it is absent.

```bash
# first page of 50 insights, newest first
curl 'https://fourfour.ai/odata/Insights?$top=50&$orderby=created desc' \
  -H 'Authorization: Bearer {access_token}'
# next page
curl 'https://fourfour.ai/odata/Insights?$top=50&$skip=50' \
  -H 'Authorization: Bearer {access_token}'
```

### Response shape

```json
<!-- Constructed from docs — verify against live API -->
{
  "@odata.context": "https://fourfour.ai/odata/$metadata#Insights",
  "@odata.nextLink": "https://fourfour.ai/odata/Insights?$top=50&$skip=50",
  "@count": 1280,
  "value": [
    {
      "id": "ins_8f31...",
      "text": "Customer wants SSO before they expand seats",
      "topicId": "top_22a...",
      "conversationId": "cnv_9c0...",
      "accountId": "acc_771...",
      "created": "2026-06-20T14:05:00Z"
    }
  ]
}
```

### `/odata/me` response

```json
<!-- Constructed from docs — verify against live API -->
{
  "user_id": "usr_123",
  "user_name": "Jordan Lee",
  "user_email": "jordan@acme.example",
  "tenant_id": "ten_456",
  "tenant_name": "Acme Inc"
}
```

---

## 3. CRM Importer API

Base: `https://fourfour.ai/import`

Push CRM records into Four/Four so insights can be linked to accounts/deals. Auth = Personal Access Token (bearer). Payloads are **CSV** with a required `id` column; dates are ISO 8601 in UTC. Standard + custom fields are supported. Processing is **asynchronous** — a write returns a job id you poll.

Supported record types: `account`, `contact`, `opportunity`, `lead`, `user`.

| Method | Path | Description |
|--------|------|-------------|
| PUT | `/import/crm/{type}` | Create/update records (CSV body) |
| GET | `/import/crm/{type}/{id}` | Read a single record |
| DELETE | `/import/crm/{type}` | Delete records |
| GET | `/import/job/{jobId}` | Poll async import job status |

**Upsert accounts (CSV):**

```bash
curl -X PUT https://fourfour.ai/import/crm/account \
  -H 'Authorization: Bearer {pat}' \
  -H 'Content-Type: text/csv' \
  --data-binary $'id,name,website,industry\nacc_771,Acme Inc,acme.example,Software'
```

Response (`202 Accepted` with a job id):

```json
<!-- Constructed from docs — verify against live API -->
{ "jobId": "job_5a2c", "status": "queued" }
```

**Poll the job:**

```bash
curl https://fourfour.ai/import/job/job_5a2c \
  -H 'Authorization: Bearer {pat}'
```

```json
<!-- Constructed from docs — verify against live API -->
{ "jobId": "job_5a2c", "status": "completed", "processed": 1, "errors": 0 }
```

---

## 4. Webhooks

Configure under **Settings → Connections → Webhooks**.

- **Signed, HTTP POST** delivery.
- **HMAC-SHA256** signature in the `Signature` header — compute `HMAC-SHA256(rawBody, secret)` and constant-time compare.
- **Retries:** automatic, up to **3x with exponential backoff**, on error status codes.
- Optional **OAuth client linking** so multi-tenant events carry which client/tenant they belong to.

### Payload structure

Top-level fields: `timestamp`, `event`, `tenant`, `payload` (event-specific).

```json
<!-- Constructed from docs — verify against live API -->
{
  "timestamp": "2026-06-20T14:05:00Z",
  "event": "insight.created",
  "tenant": "ten_456",
  "payload": {
    "id": "ins_8f31",
    "topicId": "top_22a",
    "conversationId": "cnv_9c0"
  }
}
```

### Verifying the signature (Python)

```python
import hmac, hashlib

def verify(raw_body: bytes, signature_header: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

Always hash the **raw request bytes** (not a re-serialized body). Return 2xx quickly and process async; a non-2xx triggers Four/Four's retry.

---

## 5. MCP Server

- **URL:** `https://fourfour.ai/mcp`
- **Auth:** automatic via OAuth discovery (no manual token wiring).
- **Capabilities:** tools for searching Conversations, Insights, Accounts, and Contacts — so Claude / Cursor can query the voice-of-customer data set in natural language.

Add it as a remote MCP server in Claude Desktop / Claude Code / Cursor and authenticate through the OAuth prompt.

---

## Errors & limits

- OAuth errors follow the standard OAuth2 error response (`{"error": "...", "error_description": "..."}`).
- A revoked/expired token returns `401`; refresh with the `refresh_token` grant.
- The CRM Importer returns `202` on accept; row-level errors surface in the job status (`errors` count) — poll `/import/job/{jobId}`.
- Specific numeric rate limits are not published in the captured docs; treat the API as rate-limited, honor `Retry-After` if returned, and back off on `429`/`5xx`.

## Gaps

- Exact per-entity field schemas, request bodies, and the full webhook event-type catalog live in the generated schema at `https://fourfour.ai/developers/api` (JS-rendered; not captured verbatim here).
- Numeric API rate limits were not documented in captured sources.
- Contact: `hello@fourfour.ai`.
