# ZoomInfo API Reference

> **Re-verified 2026-06-13 against live official docs** ([docs.zoominfo.com](https://docs.zoominfo.com/)). ZoomInfo's CURRENT developer API is the **GTM API** under `https://api.zoominfo.com/gtm` with **OAuth 2.0** auth. The older **Enterprise API** (PKI/JWT `/authenticate`, root-level singular paths like `/enrich/contact`) is now published under [api-docs.zoominfo.com](https://api-docs.zoominfo.com/) and labeled **"ZoomInfo API — Legacy"**. Prefer the GTM API for new builds; the legacy surface is documented at the bottom for existing integrations.

## Overview (current — GTM API)

| Property | Value |
|----------|-------|
| Base URL | `https://api.zoominfo.com/gtm` (data endpoints under `/gtm/data/v1/`, OAuth token under `/gtm/oauth/v1/`, agent endpoints under `/gtm/agent/v1/`) |
| Auth | **OAuth 2.0** — Client Credentials, Authorization Code with PKCE, or Refresh Token. Bearer access token (RFC 6750). |
| Token endpoint | `POST https://api.zoominfo.com/gtm/oauth/v1/token` |
| Token lifetime | Short-lived access token (~1000 s `expires_in` in the documented example); re-fetch/refresh on expiry. |
| Rate limit | 25 req/s default · 30 req/s Premium add-on · 35 req/s Premium+ add-on (per tenant, across all endpoints) |
| Rate-limit headers | **Not currently returned** (per official docs). On `429`, back off (exponential backoff with jitter); honor `Retry-After` if provided. |
| Response format | JSON (JSON:API-style envelope with `data`/`type`/`attributes`; `application/json` accepted) |
| Developer portal | `https://developer.zoominfo.com` (create OAuth app → `client_id` + `client_secret`, configure redirect URIs + scopes) |
| MCP server | `https://mcp.zoominfo.com/mcp` (remote, OAuth Authorization Code) — see [docs](https://docs.zoominfo.com/docs/mcp) and the Claude Code guide |
| OpenAPI/agent index | [docs.zoominfo.com/llms.txt](https://docs.zoominfo.com/llms.txt) |
| SDKs (legacy auth helpers) | [Java](https://github.com/Zoominfo/api-auth-java-client), [Node.js](https://github.com/Zoominfo/api-auth-nodejs-client), [Python](https://github.com/Zoominfo/api-auth-python-client), [C#](https://github.com/Zoominfo/api-auth-csharp-client) |
| MCP Plugin (repo) | [zoominfo-mcp-plugin](https://github.com/Zoominfo/zoominfo-mcp-plugin) |

## Authentication (current — OAuth 2.0)

Register an app at the [developer portal](https://developer.zoominfo.com) to obtain a `client_id` and `client_secret`. Three OAuth 2.0 flows are supported:

- **Client Credentials** — server-to-server, no user context (most common for backend enrichment pipelines).
- **Authorization Code with PKCE** — route many authorized users through one app (used by the MCP server).
- **Refresh Token** — refresh user access tokens without re-prompting.

### Client Credentials Flow (server-to-server)

```
POST https://api.zoominfo.com/gtm/oauth/v1/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {base64(client_id:client_secret)}

grant_type=client_credentials
```

(Credentials may alternatively be sent as `client_id` / `client_secret` body parameters; HTTP Basic is preferred.)

**Response (shape):**
```json
{
  "access_token": "eyJhbGciOiJ...",
  "token_type": "Bearer",
  "expires_in": 1000
}
```

### Using the Token

Include the bearer token on every GTM API call:

```
Authorization: Bearer {access_token}
```

**Important**: Access tokens are short-lived (the documented example shows `expires_in: 1000` seconds). Re-fetch via Client Credentials, or use the Refresh Token flow for user-context tokens, before expiry. Implement automatic refresh in production. Calls respect your ZoomInfo package, user entitlements, OAuth scopes, and credit access.

## Rate Limiting (current)

Rate limits are enforced per tenant, across all endpoints.

| Tier | Limit |
|------|-------|
| Default | 25 requests/second |
| Premium limit add-on | 30 requests/second |
| Premium+ limit add-on | 35 requests/second |

**Rate-limit headers are NOT currently returned** by the GTM API (confirmed in the official Credit Usage & Limits and Error Handling docs — do not rely on `X-RateLimit-Remaining`/`X-RateLimit-Reset`).

When rate limited, the API returns `429 Too Many Requests` (`"retryable": true`). Back off using exponential backoff with jitter; honor a `Retry-After` delay if one is provided. Retryable statuses: `429`, `500`, `504`. Non-retryable: `400`, `401`, `403`.

## Endpoints by Category (current — GTM Data API)

All data endpoints sit under `https://api.zoominfo.com/gtm/data/v1/`. Recommended workflow per official docs: **Lookup → Search → Enrich** (use ZoomInfo IDs from Search/Lookup, not names, on subsequent calls).

> **Path change (verified 2026-06-13)**: GTM paths are pluralized and entity-first — e.g. `/gtm/data/v1/contacts/search` and `/gtm/data/v1/contacts/enrich`. The old root-level singular paths (`/search/contact`, `/enrich/contact`) belong to the **legacy** Enterprise API (see bottom section).

### Search

Search endpoints discover contacts/companies/signals matching your criteria. **Search does not return emails, phone numbers, or other engagement data** — it returns IDs and hints; call the matching Enrich endpoint for full data.

Current search endpoints:
- `POST /gtm/data/v1/contacts/search` — Search Contacts
- `POST /gtm/data/v1/companies/search` — Search Companies
- `POST /gtm/data/v1/intent/search` — Search Intent
- `POST /gtm/data/v1/news/search` — Search News
- `POST /gtm/data/v1/scoops/search` — Search Scoops

#### Search Contacts

```
POST /gtm/data/v1/contacts/search
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "data": {
    "jobTitle": ["VP Sales", "Director Sales"],
    "managementLevel": ["VP", "Director"],
    "department": ["Sales"],
    "companyRevenue": { "min": 10000000, "max": 500000000 },
    "companyEmployeeCount": { "min": 50, "max": 1000 },
    "companyIndustry": ["Software", "SaaS"],
    "companyLocation": { "country": "US", "state": ["CA", "NY"] }
  },
  "page": { "number": 1, "size": 25 }
}
```

**Key parameters**:
- `data` — (required) the contact search criteria object
- `managementLevel` — C-Level, VP, Director, Manager, Staff
- `department` — Sales, Marketing, Engineering, Finance, HR, IT, Operations
- `companyRevenue` / `companyEmployeeCount` — min/max ranges
- `sort` — e.g. `contactAccuracyScore`, `lastName`, `companyName`, `hierarchy`, `sourceCount`, `lastMentioned`, `relevance`; prefix `-` for descending
- Pagination: `page[number]` (≥1) and `page[size]` (1–100). **Max page size is 100** (the legacy API capped at 25).

**Response**: Contact records with IDs, name, title, company hints — no emails/phones (use Enrich Contacts for those).

#### Search Companies

```
POST /gtm/data/v1/companies/search
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "data": {
    "companyName": "Acme",
    "revenue": { "min": 5000000 },
    "employeeCount": { "min": 100 },
    "industry": ["Technology"],
    "location": { "country": "US" },
    "techStack": ["Salesforce", "AWS"]
  },
  "page": { "number": 1, "size": 25 }
}
```

Search Companies returns only basic info (name, limited location, website, a few data points). Use Enrich Companies for revenue, employee count, full firmographics, tech stack.

### Enrich

Enrich endpoints take partial/ID records and return complete data. Best practice: Search first to get IDs, then Enrich.

Current enrich endpoints (all `POST` under `/gtm/data/v1/`):
- `contacts/enrich` — Enrich Contacts
- `companies/enrich` — Enrich Companies
- `intent/enrich` — Enrich Intent
- `news/enrich` — Enrich News
- `scoops/enrich` — Enrich Scoops
- `org-charts/enrich` — Enrich Org Charts
- `technologies/enrich` — Enrich Technologies
- `corporate-hierarchy/enrich` — Enrich Corporate Hierarchy
- `hashtags/enrich` — Enrich Hashtags

#### Enrich Contacts

```
POST /gtm/data/v1/contacts/enrich
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "data": [
    { "firstName": "Jane", "lastName": "Smith", "companyName": "Acme Corp" },
    { "emailAddress": "jane.smith@acme.com" }
  ],
  "outputFields": ["id", "firstName", "lastName", "email", "phone", "jobTitle", "department", "managementLevel", "companyId", "companyName"],
  "requiredFields": ["email"]
}
```

**Notes**:
- `data` (required) holds the match criteria; `outputFields` controls returned fields; `requiredFields` filters out records missing those fields even if matched.
- **Up to 25 contact records per request.**
- Match by name+company, email, or ZoomInfo contact ID.
- Consumes 1 bulk credit per new contact record returned; no extra credit for records already "Under Management" (within one year of initial enrichment).

#### Enrich Companies

```
POST /gtm/data/v1/companies/enrich
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "data": [
    { "companyName": "Acme Corp" },
    { "companyWebsite": "acme.com" }
  ],
  "outputFields": ["companyId", "companyName", "website", "revenue", "employeeCount", "industry", "subIndustry", "techStack", "location"]
}
```

**Notes**:
- Up to 25 company records per request.
- Match by company name, domain, or ZoomInfo company ID (domain is most accurate).
- 1 bulk credit per new company record returned.

#### Enrich Intent

```
POST /gtm/data/v1/intent/enrich
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "data": [ { "companyId": "123456789" } ]
}
```

**Response** includes intent topics the company is researching, signal score (relative to baseline), signal start date, audience strength, and recommended contacts.

**Notes**:
- Only returns topics configured in your ZoomInfo subscription.
- Intent data refreshes weekly.

### Lookup

Lookup endpoints resolve valid filter values and reference data (the first step in the Lookup → Search → Enrich flow):
- `GET /gtm/data/v1/lookup/search` — Lookup Search Fields (valid values for search filters)
- `GET /gtm/data/v1/lookup/enrich` — Lookup Enrich Fields (valid `outputFields`)
- `GET /gtm/data/v1/lookup/data` — Lookup Data

> The legacy Enterprise API exposed `GET /lookup/contact/{personId}` and `GET /lookup/company/{companyId}` to fetch a full profile by ID. In the GTM API, fetch full records via the Enrich endpoints using the ZoomInfo ID. (Legacy lookup-by-ID is in the bottom section.)

### Discovery & recommendation endpoints (GTM — new)

- `GET /gtm/data/v1/contact-recommendations` — Get Contact Recommendations
- `GET /gtm/data/v1/company-lookalikes` — Find Similar Companies
- `GET /gtm/data/v1/contact-lookalikes` — Get Contact Lookalikes

### Batching (current)

The GTM data API is **synchronous** — there is no documented async bulk job with a `callbackUrl`. Batch by sending up to **25 records per Enrich request** (`contacts/enrich`, `companies/enrich`) and looping with `page[size]` up to 100 on Search. Account/Contact Research endpoints process **1 record per request** (they consume AI action credits, not bulk credits).

> The legacy `POST /bulk/enrich` async-callback pattern is documented in the bottom (legacy) section.

### WebSights / Compliance (surface not confirmed in the GTM index)

WebSights anonymous visitor identification and Compliance opt-out management are documented as platform features, but **dedicated GTM API endpoints for them are not listed in the current GTM index** ([llms.txt](https://docs.zoominfo.com/llms.txt), checked 2026-06-13). The request shapes below reflect the **legacy** Enterprise API and may not map 1:1 to the GTM API — verify against [api-docs.zoominfo.com](https://api-docs.zoominfo.com/) (Legacy) or contact ZoomInfo before relying on them.

```
POST /websights/search   (legacy)
{ "startDate": "2026-03-01", "endDate": "2026-03-31", "page": 1, "rpp": 25 }
```
Identifies companies (not individuals); requires the WebSights pixel; pair with Contact Search.

```
POST /compliance/optout   (legacy)
{ "emailAddress": "optout@example.com", "action": "add" }
```
Actions: `add`, `remove`, `check`.

### Usage / Credits (current)

```
GET /gtm/data/v1/users/current/usage
Authorization: Bearer {access_token}
```

Returns credit/usage data for the current user. (The legacy endpoint was `GET /usage`.) Credit model: Search and Lookup are free; Enrich consumes **1 bulk credit per new contact/company record** (no extra charge for records already Under Management within one year); Research/Account-summary endpoints consume **AI action credits**.

## Pagination (current)

Search endpoints use JSON:API-style page parameters:

| Parameter | Description | Default | Max |
|-----------|-------------|---------|-----|
| `page[number]` | Page number (1-indexed) | 1 | — |
| `page[size]` | Results per page | 25 | **100** |

Responses include a JSON:API envelope: a `data` array, a `links` object (`first`/`last`), and metadata with `page.number`, `page.total`, and `totalResults`.

> The legacy Enterprise API used `page` / `rpp` (max 25) instead.

## Error Handling (current)

| Status | Meaning | Retryable | Action |
|--------|---------|-----------|--------|
| 400 | Bad Request — validation/missing/invalid fields | No | Fix the request body, then retry |
| 401 | Unauthorized — invalid/expired token, missing auth header | No | Re-authenticate (new bearer token) |
| 403 | Forbidden — insufficient scope/entitlement | No | Adjust app scopes / account access |
| 429 | Too Many Requests — rate limit exceeded | Yes | Exponential backoff with jitter; honor `Retry-After` if present |
| 500 | Internal Server Error — transient | Yes | Retry with exponential backoff |
| 504 | Gateway Timeout | Yes | Retry with exponential backoff |

Error responses include `code`, `message`, `status`, `requestId`, and `retryable`. **No rate-limit headers are returned** — do not depend on `X-RateLimit-*`.

## Webhooks & Events (current — GTM)

ZoomInfo GTM webhooks notify your application when **long-running jobs complete, records change, credit thresholds are reached, or new GTM signals become available**. Webhook/automation configuration is managed through **Agent Teams** — retries, frequencies, and throttling are configured per event type, object type, and run.

- Trigger an Agent Team run: `POST https://api.zoominfo.com/gtm/agent/v1/agent-teams/{agentTeamId}/runs`
- Poll run status/results: `GET https://api.zoominfo.com/gtm/agent/v1/agent-teams/{agentTeamId}/runs/{runId}`
- List runs: `GET /gtm/agent/v1/agent-teams/{agentTeamId}/runs`
- List/get agent teams: `GET /gtm/agent/v1/agent-teams`, `GET /gtm/agent/v1/agent-teams/{agentTeamId}`

> **Verified 2026-06-13**: Webhooks ARE now publicly documented (see [docs.zoominfo.com/docs/webhooks-and-events](https://docs.zoominfo.com/docs/webhooks-and-events)) — a change from the prior "callbacks only, not documented" state. The official page does NOT yet enumerate exact event-type identifier strings, payload JSON schema, or a signature/HMAC verification header — treat those as **unverified** and confirm in the live docs / OpenAPI spec before depending on them.

## MCP Server (current)

ZoomInfo ships a remote MCP server at **`https://mcp.zoominfo.com/mcp`** (OAuth Authorization Code). Supported clients include Claude Code, Cursor, Windsurf, and Claude Desktop. For Claude Code:

```
claude mcp add --transport http \
  --callback-port 8080 \
  --client-id <your-client-id> \
  --client-secret \
  zoominfo https://mcp.zoominfo.com/mcp
```

Create an MCP app in the [DevPortal](https://developer.zoominfo.com) with redirect URI `http://localhost:8080/callback`, get `client_id`/`client_secret`, run the command, then `/mcp` to complete browser login (credentials or SSO). MCP calls respect your ZoomInfo package, entitlements, scopes, and credit access. See [docs.zoominfo.com/docs/mcp](https://docs.zoominfo.com/docs/mcp).

## Other GTM endpoint groups (current — see llms.txt for full specs)

- **Agent Teams** — automation runs (the webhook mechanism above).
- **Audiences / Columns / Folders / Rows** — build and enrich list audiences (`POST /gtm/.../audiences`, `POST /audiences/{id}/enrich`, etc.).
- **ICP segments** — `GET/POST /segments`, archive/unarchive.
- **Buyer Personas, Competitors, Products/Services (Offerings), Customer Settings** — GTM configuration objects.
- **Account Summary** — `GET /accounts/{accountId}/summary`, `POST /accounts/{accountId}/summary-questions` (AI action credits).
- **Insights** — `GET /insights`; **Pulses** — `GET /pulses`; **Engagements** — content-interaction tracking.

## Common Patterns

### OAuth token + auto-refresh middleware (Client Credentials)

```python
import time
import base64
import requests

class ZoomInfoClient:
    BASE = "https://api.zoominfo.com/gtm"
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expires = 0

    def authenticate(self):
        basic = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()).decode()
        resp = requests.post(
            f"{self.BASE}/oauth/v1/token",
            headers={"Authorization": f"Basic {basic}",
                     "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"})
        data = resp.json()
        self.token = data["access_token"]
        # tokens are short-lived (example expires_in ~1000s); refresh early
        self.token_expires = time.time() + data.get("expires_in", 1000) - 60

    def request(self, method, path, **kwargs):
        if time.time() > self.token_expires:
            self.authenticate()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        return requests.request(method, f"{self.BASE}{path}",
                                headers=headers, **kwargs)
```

### Lookup → Search → Enrich workflow

1. `GET /gtm/data/v1/lookup/search` to resolve valid filter values for your criteria.
2. `POST /gtm/data/v1/contacts/search` to find prospects matching your ICP (returns IDs/hints, no emails/phones).
3. Collect ZoomInfo contact IDs from the results.
4. `POST /gtm/data/v1/contacts/enrich` with those IDs to get full profiles (email, phone, etc.).
5. Export or push to CRM/sequence tool.

Enrich only the records you actually need — Search/Lookup are free, Enrich spends credits.

## Gaps & Limitations

- **Webhook event catalog**: webhooks are now documented (Agent Teams), but exact event-type strings, payload schema, and signature verification header are not yet enumerated publicly — treat as unverified.
- **WebSights / Compliance**: dedicated GTM endpoints not listed in the current index; shapes shown are legacy.
- **Marketing / Copilot / Platform APIs**: surfaces such as advertising audience management and Copilot AI recommendations are partly exposed via GTM groups (Audiences, Account Summary, Insights, Agent Teams) but full specs live behind the OpenAPI registry — see [docs.zoominfo.com/llms.txt](https://docs.zoominfo.com/llms.txt).

## Legacy Enterprise API (api-docs.zoominfo.com — labeled "Legacy")

The previous Enterprise API is still published for existing integrations but is now labeled **"ZoomInfo API — Legacy"**. Differences from the current GTM API:

- **Base URL**: `https://api.zoominfo.com` (root, no `/gtm` prefix).
- **Auth**: PKI (`clientId` + `privateKey`) or username/password `POST /authenticate` → JWT; JWT expired every 60 minutes (`expiresIn: 3600`); `Authorization: Bearer {jwt}`. The Java/Node/Python/C# `api-auth-*-client` SDKs above were built for this PKI/JWT flow.
- **Endpoints**: singular root paths — `POST /search/contact`, `POST /search/company`, `POST /enrich/contact`, `POST /enrich/company`, `POST /enrich/intent`, `GET /lookup/contact/{personId}`, `GET /lookup/company/{companyId}`, `POST /bulk/enrich` (async, `callbackUrl`), `GET /usage`.
- **Pagination**: `page` + `rpp` (max 25).

For new builds use the GTM API + OAuth above. Full legacy spec: [api-docs.zoominfo.com](https://api-docs.zoominfo.com/).
