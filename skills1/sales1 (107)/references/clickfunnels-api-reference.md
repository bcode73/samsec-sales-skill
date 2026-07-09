<!-- Source: https://developers.myclickfunnels.com/docs/intro + https://developers.myclickfunnels.com/docs/getting-started + https://developers.myclickfunnels.com/llms.txt + https://developers.myclickfunnels.com/openapi/clickfunnels-api.json + https://support.myclickfunnels.com/docs/accessing-the-clickfunnels-api -->
<!-- The developer hub is a ReadMe-style site; the endpoint list below is captured from the official llms.txt index + getting-started page. An OpenAPI schema is published at developers.myclickfunnels.com/openapi/clickfunnels-api.json — fetch it for exact request/response schemas. Example JSON here is CONSTRUCTED from documented fields and marked; verify against the OpenAPI spec / live API. -->

# ClickFunnels V2 API Reference

REST API for ClickFunnels 2.0 — programmatic access to workspaces, funnels, pages, products, contacts, orders, subscriptions, courses, and webhooks. **The Classic (1.0) V1 API (`apidocs.clickfunnels.com`) is deprecated — build on V2.**

## Base URLs

Two base URLs depending on the request:

| Base URL | Use for |
|---|---|
| `https://accounts.myclickfunnels.com/api/v2` | Non-workspace / team-level data (`/teams`, `/workspaces`, `/me`) |
| `https://{workspace}.myclickfunnels.com/api/v2` | Workspace-scoped data (contacts, orders, funnels, products, …) |

## Authentication

- **Header:** `Authorization: Bearer {YOUR_API_TOKEN}`
- **Required:** a `User-Agent` header naming your app/org — e.g. `User-Agent: YourAppYourOrg`. Calls without it fail.
- **OAuth 2.0** is supported for public/multi-user apps (act on behalf of other ClickFunnels users); Bearer tokens are best for single-account service apps.
- **Token generation:** Team Settings → **Developer Portal** → **Add new platform application** → copy the API access token. Tokens are **generated per team** and grant access to all associated workspace data.
- **Plan gate:** API access is available on the higher tier (Pro; or Scale/Optimize/Dominate in other plan generations).

## Bootstrap flow

```
1. GET https://accounts.myclickfunnels.com/api/v2/teams                      -> team id
2. GET https://accounts.myclickfunnels.com/api/v2/teams/{team_id}/workspaces -> workspace id + subdomain
3. GET https://{workspace}.myclickfunnels.com/api/v2/workspaces/{id}/contacts -> workspace data
```

> Use `id` fields in POST/PATCH payloads, not the `public_id` values exposed in URLs.

## Auth quick-start (simplest call)

```bash
curl -X GET "https://accounts.myclickfunnels.com/api/v2/me" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "User-Agent: YourApp/YourOrg"
```

## Endpoints (V2)

Captured from the official `llms.txt` index. `:id` = resource id; `workspaces/:id` = workspace-scoped.

**Contacts** — `POST/GET /api/v2/workspaces/:id/contacts`, `GET/PATCH/DELETE /api/v2/contacts/:id`, `POST /api/v2/contacts/:id/upsert` (create-or-update by email). Tags: `/api/v2/contact_tags`, `/api/v2/contacts/:id/applied_tags`. GDPR: **Redact Contact** (destroys PII without deleting the record).

**Products / Variants / Prices** — `POST/GET /api/v2/workspaces/:id/products`, `GET/PATCH /api/v2/products/:id`, archive/unarchive, `/products/:id/variants`, `/variants/:id/prices`, `/prices/:id/change_options` (upgrade/downgrade).

**Orders / Invoices / Transactions / Subscriptions** — `POST/GET /api/v2/workspaces/:id/orders` (POST creates an external order), `GET/PATCH /api/v2/orders/:id`, `/orders/:id/invoices`, `/orders/:id/transactions`, `GET /api/v2/transactions/:id`. Subscription changes: `POST /api/v2/line_items/:id/changes` (preview) and `/changes/perform` (commit).

**Funnels / Pages** — `POST/GET /api/v2/workspaces/:id/funnels`, `GET/PATCH /api/v2/funnels/:id`, `/funnels/:id/stats`, `/funnels/:id/structure`. Pages: `/api/v2/workspaces/:id/pages` (+ `/pages/external` for SDK pages), `GET/PATCH/DELETE /api/v2/pages/:id`, `/pages/:id/stats`. Split tests: `/funnels/:id/split_test_steps`; conditional splits: `/funnels/:id/conditional_split_steps`.

**Forms / Submissions** — `/api/v2/workspaces/:id/forms`, `/forms/:id/field_sets`, `/field_sets/:id/fields`, `/forms/:id/submissions`, `/submissions/:id/answers`.

**Courses** — `GET /api/v2/workspaces/:id/courses`, `/courses/:id/enrollments`, `/courses/:id/lessons`, `/lessons/:id/completions`, `/courses/:id/sections`.

**Email** — `/api/v2/workspaces/:id/email_broadcasts`, `/email_templates`, `/email_topics`, `/email_addresses`, `/email_settings`.

**Sales pipeline** — `/api/v2/workspaces/:id/sales_pipelines`, `/sales_pipelines/:id/stages`, `/api/v2/workspaces/:id/sales_opportunities`, `/sales_opportunities/:id/notes`.

**Fulfillments / Shipping** — `/api/v2/workspaces/:id/fulfillments`, `/fulfillments/locations`, `/shipping_profiles`, `/shipping_packages`, zones/rates.

**Workspaces / Admin** — `GET /api/v2/workspaces`, `GET/PATCH /api/v2/workspaces/:id`, `/domains`, `/site`, `/stores`, `/themes`, `/styles`, `/refine_filters`.

**Users / Teams** — `GET /api/v2/teams`, `/teams/:id`, `GET /api/v2/me`, `/users`, `/users/:id`.

**Webhooks** — `POST/GET /api/v2/workspaces/:id/webhook_endpoints`, `GET/PATCH/DELETE /api/v2/webhook_endpoints/:id`, `GET /api/v2/workspaces/:id/webhook_events`, `/scheduled_events`.

**Blogs** — `/api/v2/workspaces/:id/blogs`, `/blogs/:id/posts`, `/blogs/:id/tags`.

## Example requests & responses

<!-- Constructed from documented endpoints/fields — verify exact keys against the OpenAPI spec -->

**Upsert a contact** — `POST /api/v2/contacts/{id}/upsert` (or workspace-scoped create):
```json
{ "contact": { "email": "jane@example.com", "first_name": "Jane" } }
```
Response (shape):
```json
{ "data": { "id": "abc123", "public_id": "cont_9f3c", "email": "jane@example.com" } }
```

**Create a webhook endpoint** — `POST /api/v2/workspaces/{id}/webhook_endpoints`:
```json
{ "webhook_endpoint": { "url": "https://yourapp.com/hooks/cf",
                        "event_type_ids": ["order.created"] } }
```

**Error response** (shape):
```json
{ "errors": [ { "status": "401", "title": "Unauthorized",
                "detail": "Missing or invalid bearer token / User-Agent" } ] }
```

## Pagination

The API supports **cursor-based and offset-based** pagination; list responses include `meta.pagination` metadata for traversal.

- **Cursor (preferred for large/changing sets):** pass the returned `next_cursor` as `cursor` on the next call; stop when `has_more` is false.
- **Offset:** `page` / `per_page` style.
- Use `expand[]` to inline nested resources and `filter[...]` for server-side filtering (see the docs' filtering guide for gotchas).

## Rate limits

- Limits apply **per workspace or per user**. Exact numeric limits are documented in the API's rate-limiting guide (not captured verbatim here — see **Gaps**).
- On `429`, back off exponentially with jitter and retry. Reduce call volume with cursor pagination, `expand[]`, field filtering, and webhooks instead of polling.

## Webhooks

Register endpoints via `POST /api/v2/workspaces/:id/webhook_endpoints` with a `url` and `event_type_ids`. ClickFunnels POSTs JSON when subscribed events fire.

- **Events** cover contact, order, subscription, and funnel triggers (e.g. `order.created`). List event types via `GET /api/v2/workspaces/:id/webhook_events`.
- **Signature verification** — requests are signed; verify the signature against your endpoint secret before trusting the payload.
- **Handling:** at-least-once delivery — respond `2xx` quickly, process async, and dedupe on the event id.

## Gaps

- The developer hub is JS-rendered (ReadMe-style); full per-endpoint request/response **schemas** weren't fetched verbatim — but an **OpenAPI schema is published at `https://developers.myclickfunnels.com/openapi/clickfunnels-api.json`** (and an LLM index at `/llms.txt`). Fetch the OpenAPI spec for exact field-level schemas; example JSON here is constructed and marked.
- **Exact rate-limit numbers** and **webhook payload schemas / signature algorithm** are referenced but not captured verbatim — confirm against the docs/OpenAPI and a live test.
- **No MCP server** found. Official repos: `github.com/clickfunnels`.
- The Classic **V1 API** (`apidocs.clickfunnels.com`) is deprecated — don't build new integrations on it.
