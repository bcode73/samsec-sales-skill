<!-- Source: https://productlane.readme.io/reference (ReadMe-hosted API reference) + https://productlane.com/docs/api-reference/authentication. Captured 2026-06-29. Endpoint field lists are verbatim where the docs exposed them; representative JSON bodies are constructed from those field lists and marked. -->

# Productlane API & Integration Reference

> **Bottom line:** Productlane ships a **documented REST API** at **`https://productlane.com/api/v1`** with **Bearer-token auth** (key from `productlane.com/settings/api`). Resources: **Companies, Customers, Insights, Portal, Workspaces**. One endpoint — **`POST /api/v1/feedback`** — is **public (no auth)** for widget/portal capture. There is **no MCP server**, and Productlane's **own outbound webhooks are not documented publicly** (Linear's webhooks are a separate system). Verify base path, pagination, and rate limits in-account before building.

## Authentication

- **Base URL:** `https://productlane.com/api/v1`
- **Method:** Bearer token. Set the header:
  ```
  Authorization: Bearer API_KEY
  ```
- **Get the key:** from the API settings page at `productlane.com/settings/api`.
- **Public exception:** `POST /api/v1/feedback` requires **no** authorization (designed for public feedback widgets/portals).

### Auth quick-start — simplest authenticated call

```bash
# Read your workspace (auth required)
curl https://productlane.com/api/v1/workspaces \
  -H "Authorization: Bearer $PRODUCTLANE_API_KEY"
```

## Endpoint inventory

> Paths below combine the documented resource groups with the `/api/v1` base. Where the ReadMe reference exposed an explicit method/path it's used verbatim; resource sub-paths marked `(confirm)` should be verified in-account.

### Companies

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/companies` | List companies | Bearer |
| `GET` | `/api/v1/companies/{id}` (confirm) | Get a company | Bearer |
| `POST` | `/api/v1/companies` | Create a company | Bearer |
| `DELETE` | `/api/v1/companies/{id}` (confirm) | Delete a company | Bearer |

### Customers

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/customers/{id}` (confirm) | Get a customer | Bearer |
| `POST` | `/api/v1/customers` | Create a customer (`name` 1–255, `email` required, `segments[]` optional) | Bearer |
| `PATCH` | `/api/v1/customers/{id}` (confirm) | Update a customer | Bearer |
| `DELETE` | `/api/v1/customers/{id}` (confirm) | Delete a customer | Bearer |

### Insights (feedback notes)

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/insights/{id}` (confirm) | Get an insight | Bearer |
| `GET` | `/api/v1/insights` | List insights | Bearer |
| `POST` | `/api/v1/insights` | Create an insight (`text` req, `painLevel` req, `customerEmail` req; `customerName`/`projectId`/`notify` optional) | Bearer |
| `PATCH` | `/api/v1/insights/{id}` (confirm) | Update an insight | Bearer |

### Portal

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/portal/projects` (confirm) | List projects (roadmap = Linear projects) | Bearer |
| `GET` | `/api/v1/portal/projects/{id}/upvotes` (confirm) | Get project upvotes | Bearer |
| `GET` | `/api/v1/portal/changelogs` (confirm) | List changelogs | Bearer |
| `POST` | `/api/v1/feedback` | **Create feedback — PUBLIC, NO AUTH** (`workspaceId` req, `text` req, `painLevel` req, `email` req; `projectId`/`notify` optional) | **none** |
| `POST` | `/api/v1/portal/projects/{id}/upvote` (confirm) | Upvote a project | Bearer |

### Workspaces

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/api/v1/workspaces` | Get workspace | Bearer |

## Request / response examples

> <!-- Constructed from documented field lists — verify exact response envelopes against the live API. -->

### Create a customer

```bash
curl -X POST https://productlane.com/api/v1/customers \
  -H "Authorization: Bearer $PRODUCTLANE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Jane Doe", "email": "jane@acme.com", "segments": ["enterprise"] }'
```

### Create an insight (authenticated, prioritized feedback)

```bash
curl -X POST https://productlane.com/api/v1/insights \
  -H "Authorization: Bearer $PRODUCTLANE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Wants a Kanban view for requests",
    "painLevel": "HIGH",
    "customerEmail": "jane@acme.com",
    "customerName": "Jane Doe"
  }'
```

### Create public feedback (NO auth — widget/portal)

```bash
curl -X POST https://productlane.com/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "workspaceId": "YOUR_WORKSPACE_ID",
    "text": "Dark mode please",
    "painLevel": "MEDIUM",
    "email": "user@example.com"
  }'
```

**`painLevel` enum (all feedback/insight endpoints):** `UNKNOWN` | `LOW` | `MEDIUM` | `HIGH`.

The ReadMe reference renders multi-language samples (Shell, Node, Ruby, PHP, Python) and a "Try It!" console per endpoint — use those to confirm exact request/response envelopes for your account.

## Integrations (no-code)

- **Zapier** (**Scale-tier**): documented **action — "Create Note"** (inputs: Note Text, Importance, Customer Email, Project ID, optional notification settings) → maps to the Insights API. Trigger inventory not surfaced publicly — confirm in the live Zap editor.
- **HubSpot** (**Scale-tier**): advanced integration.
- **Linear** (mandatory, core): the issue/project/changelog backbone — use **Linear's own API + webhooks** for issue/status events, since Linear is the source of truth.
- **Slack / MS Teams / Discord / shared email / live chat**: support-inbox channels (Pro+).

## Gaps

The following could **not** be confirmed from public sources and must be verified in-account or via the in-app API console:

- Exact sub-paths for get/update/delete on Companies, Customers, Insights, and the precise Portal paths/params (`getprojects`, `getprojectupvotes`, `listchangelogs`, `upvoteproject`) — the ReadMe nav exposed operation names, not always full paths.
- **Pagination model** (page/offset vs cursor) and default/maximum page sizes for `list` endpoints.
- **Rate limits** and `429`/`Retry-After` behavior.
- **Error response shape** (4xx/5xx envelope).
- Whether the API is **plan-gated** (no explicit API plan gate was found; some advanced integrations like Zapier/HubSpot are Scale-tier — confirm whether raw API access is too).
- **Productlane's own outbound webhooks** — event catalog, payload schema, and signing/HMAC are not publicly documented. Do not assume signed webhooks exist; for real-time events prefer **Linear webhooks** or **poll** the Portal endpoints. Consider Zapier (Scale) for push.
- Whether the feedback **widget** supports an `identify` call / SSO to attach feedback to known users (SSO is JWT, Scale-tier).

**If a fully documented, lower-cost standalone API is the requirement** (e.g. the team isn't on Linear): evaluate **Frill** (`api.frill.co/v1`, signed webhooks, ~$25/mo), **UserJot** (`api.userjot.com/v1`, MCP server, free tier), **Sleekplan** (REST + MCP server), or **FeatureOS** (REST API v3 + OAuth apps).
