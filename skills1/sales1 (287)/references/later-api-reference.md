# Later Influence Reporting API Reference

## Overview

The Later Influence Reporting API provides programmatic access to campaign performance data, creator metrics, and social media analytics. It is designed for pulling Later Influence data into reporting/BI tools (Looker, Microsoft BI, Oracle Analytics Cloud, SAP Analytics Cloud, Tableau, and more).

**Note**: Later Social (scheduling, Linkin.bio, content calendar) does not have a public API. Only Later Influence exposes an API.

**Current version**: v2.0, hosted at `reporting.api.later.com`. The legacy v1 API (previously documented under Mavrck at `api.mavrck.co`) is being deprecated — Later states v1 will be deprecated "within the next 6 months" (as of the 2026-06-13 re-verification) with a firm migration date communicated in advance. See "Migration from v1" below.

## Base URL

`https://reporting.api.later.com`

Interactive API reference, full parameter details, and downloadable OpenAPI specs (JSON & YAML) live at `https://docs.reporting.api.later.com/api-reference`. A documentation-search MCP server is exposed at `https://docs.reporting.api.later.com/mcp` (`@Latermedia/reporting-api-docs`, http transport, `search-documentation` tool) — note this MCP searches docs, it does not query campaign data.

## Authentication

- **Method**: JWT (JSON Web Tokens), passed as a Bearer token.
- **Flow**: Exchange `clientId` and `clientSecret` for a temporary access token.
- **Token endpoint**: `POST https://reporting.api.later.com/oauth/token`
  - Request body (JSON): `{ "clientId": "<id>", "clientSecret": "<secret>" }` with `Content-Type: application/json`.
  - Response: `{ "jwt": "<JWT>" }`.
- **Usage**: Send `Authorization: Bearer <jwt>` on all subsequent requests.
- **Token lifetime**: The developer docs state tokens **expire after 12 hours** (`docs.reporting.api.later.com/authentication`); decode the JWT `exp` claim to re-authenticate proactively, or request a new token when you receive a `401 Unauthorized`. (The help-center walkthrough article currently states 24 hours — treat the developer docs' 12 hours as authoritative for the v2 API.)
- **Credentials**: Contact your Account Manager / Customer Success Manager to obtain `clientId` and `clientSecret` (no self-serve provisioning).

### Token error codes

| Code | Meaning |
|---|---|
| `INVALID_CLIENT_CREDENTIALS` | Wrong `clientId` or `clientSecret` |
| `CLIENT_DISABLED` | Client account has been disabled |
| `NO_ACCESSIBLE_INSTANCES` | Client has no active instance associations |

## Endpoints (v2)

The API is organized around a data hierarchy: **Instance → Campaign → Platform / Creator / Post.**

| Business question | Endpoint |
|---|---|
| What instances can I query? | `GET /v2/instances` |
| Executive KPIs for the whole workspace | `GET /v2/instances/performance` |
| Performance trends over time | `GET /v2/instances/performance-over-time` |
| Campaign list (no metrics) | `GET /v2/campaigns` |
| Compare campaigns on ROI, spend, or affiliate | `GET /v2/campaigns/performance` |
| Channel mix / platform comparison | `GET /v2/platforms/performance` |
| ROI breakdown by platform (incl. ROAS) | `GET /v2/platforms/return-on-investment` |
| Creator leaderboards or benchmarks | `GET /v2/creators/performance` |
| Post-level content analysis | `GET /v2/posts/performance` |

Every request to a performance endpoint requires at least one `instanceId`; call `GET /v2/instances` first to retrieve the IDs associated with your credentials. Omit `instanceIds` to return data across all instances your credentials can access; pass multiple `instanceIds` values to aggregate across several Later Influence workspaces in one call.

### Query parameters

- **Date filtering**: `startDate` and `endDate` on any performance endpoint (date ranges may not exceed 2 years). Switch `dateBasis=performanceDate` (when the metric was recorded) vs `dateBasis=postDate` (when content was published).
- **Time-series granularity**: `GET /v2/instances/performance-over-time` takes `granularity` = `day` | `week` | `month` | `quarter` | `year`.
- **Sorting & pagination**: list/performance endpoints support `sortProperty`, `sortDirection` (`ASC`/`DESC`), `pageNumber`, and `pageSize`. The docs site also describes cursor-based pagination. Responses use a structured envelope: `{ "data": { ... }, "pagination": { ... } }`.
- **Platform filtering**: filter by social platform (Instagram, TikTok, YouTube, Facebook, and more) on most performance endpoints.

### Paid vs. organic metrics

Organic metrics use plain field names (`impressions`, `engagements`). Paid metrics always use the `paid` prefix and are available on `campaigns/performance`, `platforms/performance`, and `posts/performance`:

| Field | Description |
|---|---|
| `paidImpressions` | Total impressions from paid amplification |
| `paidEngagementRate` | Engagement rate on paid content |
| `paidCpm` | Cost per thousand paid impressions |
| `ROAS` | Available via `GET /v2/platforms/return-on-investment` |

`null` means the metric is not available for that row; `0` means it is defined but the value is zero.

## Rate limits

- **120 requests per minute, per IP** on the v2 Reporting API (`docs.reporting.api.later.com/errors`).
- Response headers: `X-Ratelimit-Limit` (max requests in the current window) and `X-Ratelimit-Window` (window duration in seconds).
- Exceeding the limit returns `429 Too Many Requests`; implement retry logic with exponential backoff.

## Error format

Errors use the `ANL_00xxx` namespace and are returned as `application/problem+json` (RFC 9457) with `type`, `title`, and `detail` fields:

| Type | HTTP status | Scenario |
|---|---|---|
| `ANL_00400` | 400 | Query parameter validation failed (invalid params, date range > 2 years, unsupported metrics) |
| `ANL_00422` | 400 | `sortProperty` not supported for this endpoint/filter |
| `ANL_00401` | 401 | JWT missing, malformed, invalid, or expired |
| `ANL_00403` | 403 | Valid JWT but insufficient scope or unbound `instanceIds` |
| `ANL_00404` | 404 | Requested resource or route not found |
| `ANL_00500` | 500 | Unexpected server-side failure |

## Webhooks

Not documented for the Reporting API (the v2 developer docs and help center describe only pull/request-response reporting endpoints, no event push).

## SDK availability

No language-specific SDKs are published, but the interactive API reference auto-generates request snippets for Shell (cURL), Ruby, Node.js, PHP, and Python. Use standard HTTP clients with JWT/Bearer auth.

## Supported BI integrations

The API is designed for integration with Looker, Microsoft Power BI, Oracle Analytics Cloud, SAP Analytics Cloud, and Tableau.

## Migration from v1 (Mavrck)

If your team uses the legacy Mavrck API (`api.mavrck.co`), plan migration to v2 (`reporting.api.later.com`). v1 will be deprecated within ~6 months of mid-2026.

| v1 route | v2 equivalent | Notes |
|---|---|---|
| `POST /oauth/token` | `POST /oauth/token` | Same concept, new base URL |
| `GET /v1/reporting-api/instance` | `GET /v2/instances` | Renamed; same purpose |
| `GET /v1/reporting-api/campaign` | `GET /v2/campaigns` | Renamed; richer response in v2 |
| `GET /v1/reporting-api/reporting-group` | (no direct equivalent) | Replaced by campaign/platform hierarchy |
| `GET /v1/reporting-api/report` | `GET /v2/campaigns/performance` or `GET /v2/instances/performance` | Replaced by purpose-specific endpoints |

Migration checklist: update the base URL; replace v1 route paths with v2 equivalents; parse the new `{ "data": {}, "pagination": {} }` envelope; remove reporting-group logic (replaced by campaign/platform filtering); add new paid/creator/post fields.

## Gaps

- **No public scheduling API** — Later Social does not expose endpoints for creating, editing, or deleting scheduled posts.
- **No content management API** — media library, Linkin.bio configuration, and calendar operations are UI-only.
- **Credentials require sales relationship** — no self-serve API key provisioning.
- **No webhooks** — reporting is pull-only.
- **Token-lifetime discrepancy** — developer docs say 12 hours, the help-center walkthrough says 24 hours; treat 12 hours as authoritative and re-auth on `401`.
