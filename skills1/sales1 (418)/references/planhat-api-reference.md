<!-- Source: https://www.planhat.com/developers/api/introduction, https://www.planhat.com/developers/api/authentication-limits, https://www.planhat.com/developers/api/company, https://www.planhat.com/developers/api/enduser, https://www.planhat.com/developers/api/bulk-upsert, https://www.planhat.com/developers/api/deal, https://www.planhat.com/developers/automations/triggers, https://www.planhat.com/developers/ai/mcp-server/ -->
<!-- Fetched: 2026-04-14; re-verified against live official docs 2026-06-13. -->

# Planhat REST API Reference

## Overview

- **Auth**: Bearer token — `Authorization: Bearer {access_token}`
- **Access token**: Generated via Service Accounts (Private Apps) in Settings → App Center
- **Main API base URL**: `https://api.planhat.com`
- **Analytics base URL**: `https://analytics.planhat.com` (for open endpoints — user activities, metrics, call logs)
- **MCP Server URL**: `https://api.planhat.com/v1/mcp`
- **Rate limit**: 200 API calls/min (soft limit), ~150 req/sec hard limit, up to 50 parallel requests
- **Analytics rate limit**: separate, higher limits (handles high-volume data)
- **GET list limit**: `limit` query param defaults to **100**; max **5,000** for Companies, **2,000** for most other models (e.g. Endusers)
- **Bulk upsert limit**: 5,000 objects per request (all models)
- **Body size limit**: 32MB per POST (~150,000 items) — applies to all POSTs to Planhat
- **Pagination**: offset-based. Query params: `limit`, `offset`, `sort`, `select`
- **Error codes**: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 429 (rate limited), 500 (server error)

## Authentication methods

### Service Account (Private App) tokens
1. Settings → App Center → Create Private App
2. Assign model-level permissions (read/write per object type)
3. Generate access token
4. Use in header: `Authorization: Bearer {token}`

### Personal Access Tokens
- Per-user tokens for individual API access
- Generated from user settings

### OAuth Clients
- For third-party app integrations (ChatGPT, Claude Web, etc.)
- Create OAuth app in App Center
- Standard OAuth 2.0 flow

### Tenant Token (open endpoints only)
- Found in Settings
- Used for unauthenticated analytics endpoints (activities, metrics, call logs)
- No bearer auth required — pass as URL parameter or in body

## Data models

The API exposes these models (per the live docs nav): Asset, Campaign, Churn, Company, Conversation, Custom Field, **Deal**, Enduser, Invoice, Issue, **Line Item**, Metrics, Note, NPS, Objective, Opportunity, **Product**, Project, Sale, Task, Ticket, Time Entry, Timesheet, User, License.

**Bulk upsert is `PUT /{model}` with an array body** — NOT a `/{model}/bulk` path. The same collection endpoint (`PUT /companies`, `PUT /endusers`, `PUT /deals`, …) accepts either a single object (update) or an array (bulk upsert, up to 5,000 items). Getting a single record by external identifier uses URL prefixes: `extid-{externalId}` and `srcid-{sourceId}` (e.g. `GET /companies/extid-SF12345`).

### Company
Core customer account object.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/companies` | List companies (default limit 100, max 5,000 per request) |
| GET | `/leancompanies` | Lightweight company list (id/name only) |
| GET | `/companies/:id` | Get by Planhat `_id`, or `extid-{externalId}` / `srcid-{sourceId}` prefix |
| POST | `/companies` | Create company |
| PUT | `/companies/:id` | Update single company |
| PUT | `/companies` | Bulk upsert (array body, up to 5,000) |
| DELETE | `/companies/:id` | Delete company |

Key fields: `_id`, `externalId`, `sourceId`, `name`, `phase`, `owner`, `custom` (custom fields), health score fields, revenue fields.

### Enduser
Individual users within a customer company.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/endusers` | List endusers (default limit 100, max 2,000 per request) |
| GET | `/endusers/:id` | Get by `_id`, or `extid-{externalId}` / `srcid-{sourceId}` prefix |
| POST | `/endusers` | Create enduser |
| PUT | `/endusers/:id` | Update single enduser |
| PUT | `/endusers` | Bulk upsert (array body, up to 5,000) |
| DELETE | `/endusers/:id` | Delete enduser |

Key fields: `_id`, `externalId`, `sourceId`, `companyId`, `name`, `email`, `custom`. Keyables (match priority): `_id` > `sourceId` > `externalId` > `email`.

**Note**: Not all endusers sent via API get added — Planhat may skip duplicates based on email or externalId matching. Check the help center article on "Not all End Users sent over API get added."

### License
Recurring revenue / subscription records.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/licenses` | List licenses |
| GET | `/licenses/:id` | Get by ID |
| POST | `/licenses` | Create license |
| PUT | `/licenses/:id` | Update single license |
| PUT | `/licenses` | Bulk upsert (array body) |
| DELETE | `/licenses/:id` | Delete license |

Key fields: `_id`, `externalId`, `companyId`, `product`, `mrr`, `startDate`, `renewalDate`, `custom`.

### Opportunity
Pipeline / deal records.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/opportunities` | List opportunities |
| GET | `/opportunities/:id` | Get by ID |
| POST | `/opportunities` | Create opportunity |
| PUT | `/opportunities/:id` | Update opportunity |
| DELETE | `/opportunities/:id` | Delete opportunity |

### Deal
Sales opportunity or contract associated with a customer (distinct from `Opportunity`; used by the revenue/sales pipeline).

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/deals` | List deals (default limit 100) |
| GET | `/deals/:id` | Get by `_id` / `extid-`/`srcid-` prefix |
| POST | `/deals` | Create deal |
| PUT | `/deals/:id` | Update single deal |
| PUT | `/deals` | Bulk upsert (array body, up to 5,000) |
| DELETE | `/deals/:id` | Delete deal |

### Product
Catalog of products/services available to sell (referenced by Line Items and Licenses).

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/products` | List products |
| POST | `/products` | Create product |
| PUT | `/products/:id` | Update product |
| PUT | `/products` | Bulk upsert |
| DELETE | `/products/:id` | Delete product |

### Line Item
Individual product line on a Deal / License (quantity, price, product reference).

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/lineitems` | List line items |
| POST | `/lineitems` | Create line item |
| PUT | `/lineitems/:id` | Update line item |
| PUT | `/lineitems` | Bulk upsert |
| DELETE | `/lineitems/:id` | Delete line item |

### Asset
Products/services the customer uses.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/assets` | List assets |
| POST | `/assets` | Create asset |
| PUT | `/assets/:id` | Update asset |
| DELETE | `/assets/:id` | Delete asset |

### Note
Rich-text notes linked to companies/endusers.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/notes` | List notes |
| POST | `/notes` | Create note |
| PUT | `/notes/:id` | Update note |
| DELETE | `/notes/:id` | Delete note |

### Task
Action items with assignee and due date.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create task |
| PUT | `/tasks/:id` | Update task |
| DELETE | `/tasks/:id` | Delete task |

### Ticket
Support tickets synced from external systems.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/tickets` | List tickets |
| POST | `/tickets` | Create ticket |
| PUT | `/tickets/:id` | Update ticket |
| DELETE | `/tickets/:id` | Delete ticket |

### Conversation
Email/chat thread records.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/conversations` | List conversations |
| POST | `/conversations` | Create conversation |
| PUT | `/conversations/:id` | Update conversation |
| DELETE | `/conversations/:id` | Delete conversation |

### NPS
Net Promoter Score survey responses.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/nps` | List NPS responses |
| POST | `/nps` | Create NPS response |
| PUT | `/nps/:id` | Update NPS response |
| DELETE | `/nps/:id` | Delete NPS response |

### Campaign
Marketing campaign tracking.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/campaigns` | List campaigns |
| POST | `/campaigns` | Create campaign |
| PUT | `/campaigns/:id` | Update campaign |

### Invoice
Billing records.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/invoices` | List invoices |
| POST | `/invoices` | Create invoice |
| PUT | `/invoices/:id` | Update invoice |
| DELETE | `/invoices/:id` | Delete invoice |

### Sale
Closed-won revenue records.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/sales` | List sales |
| POST | `/sales` | Create sale |
| PUT | `/sales/:id` | Update sale |

### Issue
Bug/feature request tracking.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/issues` | List issues |
| POST | `/issues` | Create issue |
| PUT | `/issues/:id` | Update issue |
| DELETE | `/issues/:id` | Delete issue |

### Project
Onboarding/implementation projects.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/projects` | List projects |
| POST | `/projects` | Create project |
| PUT | `/projects/:id` | Update project |
| DELETE | `/projects/:id` | Delete project |

### Objective
Customer success objectives/goals.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/objectives` | List objectives |
| POST | `/objectives` | Create objective |
| PUT | `/objectives/:id` | Update objective |

### Churn
Churn event records.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/churns` | List churn events |
| POST | `/churns` | Create churn event |

### Custom Field
Extend data models with custom fields.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/customfields` | List custom field definitions |
| POST | `/customfields` | Create custom field definition |
| PUT | `/customfields/:id` | Update custom field |
| DELETE | `/customfields/:id` | Delete custom field |

### User (Admin)
Planhat team members / admin users.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/users` | List Planhat users |

### Time Entry / Timesheet
Service time tracking.

| Method | Endpoint | Notes |
|---|---|---|
| GET | `/timeentries` | List time entries |
| POST | `/timeentries` | Create time entry |

### Metrics (Time Series)
Calculated time-series data.

| Method | Endpoint | Notes |
|---|---|---|
| POST (analytics) | `analytics.planhat.com/metrics` | Push metric data (open endpoint, tenant token) |

## Open endpoints (no auth required)

These endpoints use the Tenant Token and are designed for high-volume data ingestion:

| Endpoint | Purpose |
|---|---|
| `POST analytics.planhat.com/activities` | Push user activity events |
| `POST analytics.planhat.com/metrics` | Push time-series metric data |
| `POST analytics.planhat.com/calllogs` | Push telephony call logs |

**Body size limit**: 32MB per POST (~150,000 items).

## Bulk upsert

Available on most models — per the live bulk-upsert docs: Asset, Campaign, Churn, Company, Conversation, Custom Field, Deal, Enduser, Invoice, Issue, Line Item, Metrics, Note, NPS, Objective, Opportunity, Product, Project, Sale, Task, Ticket, Time Entry, Timesheet, User, License.
- **`PUT /{model}` with an array body** (up to 5,000 objects). There is NO `/{model}/bulk` path — the collection endpoint accepts a single object (update) or an array (bulk upsert).
- Uses keyable fields to match existing records
- Matched records are updated; unmatched records are created
- **Keyable gotcha**: if the keyable field isn't set on existing records, bulk upsert creates duplicates

## Data uniqueness and keyables

Planhat uses "keyables" to enforce data uniqueness. Match priority is generally **`_id` > `sourceId` > `externalId`** (Enduser adds `email` as the lowest-priority keyable). The exact keyables available depend on the resource:
- **`_id`**: Planhat's native identifier
- **`sourceId`**: an external system ID (e.g. from a CRM connector) — use `srcid-{sourceId}` in GET URLs
- **`externalId`**: your own system's ID — use `extid-{externalId}` in GET URLs
- **`email`**: Enduser only
- If no keyable is provided, or the provided key matches no existing record, the API creates a new record even if a logical duplicate exists
- This is the #1 cause of duplicate records from API/CRM sync

## Webhooks (via Automations)

Webhooks are handled through the Automations system in two directions:

**Outbound (Planhat → your endpoint)** — a webhook is an *action* step in an Automation:
- Supports HTTP methods **GET, POST, PUT, PATCH, DELETE**
- Dynamic headers and body payloads using replacement tokens (merge fields)
- Can call any third-party API, including Planhat's own API, inside a larger flow

**Inbound (external system → Planhat)** — an "incoming webhook" is a *trigger* type:
- Each gets a unique **UUID-based endpoint URL** over **HTTPS**
- Optional header/payload validation rules (no documented HMAC signature scheme)

**Automation trigger types**: event-driven (on create / update / delete, optionally scoped to specific fields), scheduled (interval/time), incoming webhook, and manual. The "Automation Events - Call A Webhook" permission gates both incoming-webhook triggers and call-a-webhook action steps.
