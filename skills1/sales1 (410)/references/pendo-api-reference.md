<!-- Source: https://app.pendo.io/api/v1 — Engage API docs at engageapi.pendo.io, Feedback API docs at feedbackapi.pendo.io -->
<!-- Re-verified 2026-06-13 against official Pendo Help Center pages (developer documentation, Webhooks, MCP server, Feedback API Key, host name list) plus engageapi.pendo.io / feedbackapi.pendo.io; corroborated by https://www.stitchflow.com/user-management/pendo/api -->

# Pendo API Reference

## Authentication

**Method**: API Key (Integration Key)
**Header**: `X-Pendo-Integration-Key: <YOUR_KEY>`
**Scopes**: `read` (GET operations), `write` (POST/PUT/DELETE operations)

Generate keys in: Settings > Integrations > Integration Keys (admin only). Keys are shown only once at creation.

**Important**: Integration keys should be kept secret. Never share in client-side code or public repositories.

## Base URLs

The base URL corresponds to the region/web address you use to log into the Pendo UI.

| Region (data environment) | Base URL |
|---|---|
| US (default) | `https://app.pendo.io/api/v1` |
| US1 | `https://us1.app.pendo.io/api/v1` |
| EU | `https://app.eu.pendo.io/api/v1` |
| Japan | `https://app.jpn.pendo.io/api/v1` |
| Australia | `https://app.au.pendo.io/api/v1` |

Alternatively, the dedicated `https://engageapi.pendo.io/api/v1` host can be used for Engage API calls (e.g. `https://engageapi.pendo.io/api/v1/pageViews`).

## Core Endpoints

### Visitors

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/visitor/{visitorId}` | Retrieve a single visitor |
| PUT | `/metadata/visitor/{visitorId}` | Update a single visitor's metadata |
| POST | `/metadata/visitor/bulk` | Batch update visitor metadata (recommended, <1,000 records) |
| DELETE | `/visitor/{visitorId}` | Remove visitor and all event history |

#### Visitor Object

| Field | Type | Required | Mutable | Notes |
|---|---|---|---|---|
| `visitorId` | string | Yes (create) | No | Maps to internal user ID; must match install script value |
| `accountId` | string | No | Yes | Links visitor to account |
| `metadata.auto.email` | string | No | Yes | Set by install script; overwritten on page load |
| `metadata.auto.firstName` | string | No | Yes | Set by install script |
| `metadata.auto.lastName` | string | No | Yes | Set by install script |
| `metadata.auto.role` | string | No | Yes | Set by install script |
| `metadata.custom.*` | string/number/boolean | No | Yes | Must pre-define in Pendo UI first |
| `metadata.auto.lastvisit` | number (epoch ms) | System-set | No | Read-only |
| `metadata.auto.firstvisit` | number (epoch ms) | System-set | No | Read-only |

### Accounts

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/account/{accountId}` | Retrieve an account object |
| POST | `/metadata/account/bulk` | Batch update account metadata |

### Users (Admin)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/user` | List Pendo application (admin) users |

### Metadata Schema

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/metadata/schema/visitor` | Get visitor metadata schema |
| GET | `/metadata/schema/account` | Get account metadata schema |

## Aggregation API

The most powerful Pendo API. Uses a MongoDB-style pipeline to query any Pendo data.

**Endpoint**: `POST /api/v1/aggregation`

**Required headers**:
```
Content-Type: application/json
X-Pendo-Integration-Key: <YOUR_KEY>
```

### Query structure

Aggregation queries are JSON objects with a `pipeline` array and a `source` specification:

```json
{
  "response": {
    "mimeType": "application/json"
  },
  "request": {
    "pipeline": [
      {
        "source": {
          "visitors": null
        }
      },
      {
        "filter": "visitorId != \"\""
      },
      {
        "count": "visitorCount"
      }
    ]
  }
}
```

### Available sources

| Source | Returns |
|---|---|
| `visitors` | All visitors in the subscription |
| `accounts` | All accounts |
| `features` | All tagged features |
| `pages` | All tagged pages |
| `guides` | All guides |
| `featureEvents` | Feature click events |
| `pageEvents` | Page view events |
| `guideEvents` | Guide interaction events |
| `pollEvents` | Poll/survey response events |
| `trackEvents` | Custom Track Events |
| `events` | General events |
| `visitorHistory` | Visitor session history |
| `trackTypes` | Track Event type definitions |

### Pipeline operators

| Operator | Purpose | Example |
|---|---|---|
| `source` | Define data source | `{"source": {"visitors": null}}` |
| `filter` | Filter rows | `{"filter": "accountId == \"acme\""}` |
| `group` | Group by field | `{"group": {"field": "accountId"}}` |
| `count` | Count rows | `{"count": "total"}` |
| `sort` | Sort results | `{"sort": ["total"]}` |
| `limit` | Limit results | `{"limit": 100}` |
| `select` | Select/compute fields | `{"select": {"visitorId": "visitorId"}}` |
| `timeSeries` | Time-based grouping | See below |

### Time series example

```json
{
  "response": {"mimeType": "application/json"},
  "request": {
    "pipeline": [
      {
        "source": {
          "featureEvents": null,
          "timeSeries": {
            "period": "dayRange",
            "first": "1714521600000",
            "last": "1717200000000"
          }
        }
      },
      {
        "group": {
          "group": ["featureId"],
          "fields": [
            {"count": "numEvents"},
            {"count": {"distinctVisitorId": "numVisitors"}}
          ]
        }
      },
      {"sort": ["-numEvents"]},
      {"limit": 20}
    ]
  }
}
```

### ETL example: Monthly active visitors by account

```json
{
  "response": {"mimeType": "application/json"},
  "request": {
    "pipeline": [
      {
        "source": {
          "events": null,
          "timeSeries": {
            "period": "monthRange",
            "first": "1714521600000",
            "last": "1717200000000"
          }
        }
      },
      {
        "group": {
          "group": ["accountId"],
          "fields": [
            {"count": {"distinctVisitorId": "mau"}}
          ]
        }
      },
      {"sort": ["-mau"]}
    ]
  }
}
```

## SCIM API

For automated user provisioning (SSO environments).

**Endpoint**: `https://app.pendo.io/scim/v2`
**Version**: SCIM 2.0
**Auth**: Separate bearer token (Settings > Integrations > SCIM)
**Requirements**: Premium tier/add-on + SSO (SAML/OIDC) enabled

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/Users` | List users |
| POST | `/Users` | Create user |
| GET | `/Users/{id}` | Get user |
| PUT | `/Users/{id}` | Replace user |
| PATCH | `/Users/{id}` | Update user |
| DELETE | `/Users/{id}` | Delete user |
| GET | `/Groups` | List groups |
| POST | `/Groups` | Create group |
| GET | `/Groups/{id}` | Get group |
| PUT | `/Groups/{id}` | Replace group |
| PATCH | `/Groups/{id}` | Update group |
| DELETE | `/Groups/{id}` | Delete group |

## Feedback API

Separate API for Pendo Feedback (Listen module). Lets you retrieve and manage feedback requests and access product areas and classic roadmap data.

**Base URL (region-specific)**:

| Region | Base URL |
|---|---|
| US | `https://api.feedback.us.pendo.io` |
| EU | `https://api.feedback.eu.pendo.io` |

**Docs / OpenAPI spec**: https://feedbackapi.pendo.io/

**Auth**: Separate Feedback API key (generate in Feedback > vendor Settings > Integrate). Pass it on every request as the request header `auth-token` (preferred), or as a query parameter named `auth-token`. This is NOT the same key as the Engage `X-Pendo-Integration-Key`.

*Note: Pendo adds Feedback API endpoints to the docs as customers need them; consult the docs URL or contact support for endpoints not yet listed.*

## Rate limits

- Not publicly documented
- HTTP 429 response indicates rate limit exceeded
- No pagination on most endpoints — use aggregation pipeline for large datasets
- Recommendation: implement exponential backoff on 429 responses

## Webhooks

Webhooks push event data to other systems in real time. Configure them in the Pendo UI (Integrations > Webhooks). Common destinations include Twilio Segment, AWS Lambda, and Zapier.

**Events that can trigger a webhook**:
- Page loaded (select specific pages)
- Feature clicked (select specific features)
- Guide displayed (select specific guides)
- Track Event received (select specific Track Events)
- NPS survey displayed / submitted (select specific surveys)
- Poll displayed / submitted (select specific polls)
- Visitor first seen in-app (all visitors — "Visitors created")
- Account first seen in-app (all accounts — "Accounts created")
- Visitor unsubscribes from Orchestrate emails (all — "Emails")

For Pages, Features, Track Events, Guides, NPS Surveys, and Polls you choose specific items to fire on; the Accounts-created, Visitors-created, and Emails categories fire for all events.

Example payload fields (from the Pendo "Example Webhook Responses" tech note) include the event type and the associated visitor/account/Track Event data. No webhook payload signing scheme is documented — validate by source/IP or a shared secret in the URL if needed.

## MCP Server (official)

Pendo ships an official, hosted **MCP server** (beta) for connecting Pendo data to AI tools. It is listed in Claude's official Connectors Directory.

- **Endpoint** (regional, same pattern as the API host): `https://app.pendo.io/mcp/v0/shttp` (EU: `https://app.eu.pendo.io/mcp/v0/shttp`). A single connection covers all Pendo subscriptions you belong to within the same region; configure a separate connection per region.
- **Auth**: OAuth sign-in (respects your existing Pendo permissions — you can only access data you can already see in Pendo). For headless/automation, use a **service account** with the OAuth client-credentials grant: `POST https://app.pendo.io/oauth/v1/token` (EU: `https://app.eu.pendo.io/oauth/v1/token`) with `grant_type=client_credentials`, `client_id`, `client_secret`; then send the returned access token as a bearer token in the `Authorization` header on MCP requests.
- **Clients**: Claude (web/desktop), Claude Code, Cursor, VS Code with GitHub Copilot, ChatGPT (developer mode), and more.
- **Claude Code setup**: `claude mcp add --transport http pendo https://app.pendo.io/mcp/v0/shttp`
- **Capabilities**: visitor/account metadata, application analytics and user behavior, Pages/Features/Track Events lookups, and event-level aggregation queries on recent usage.

## SDKs and tools

- **Singer tap**: `tap-pendo` (open-source ETL connector)
- **ETL examples**: `pendo-io/pendo-ETL-API-calls` on GitHub (example folders for common aggregation queries)
- **Mobile SDKs**: iOS, Android, React Native, Flutter, Xamarin, MAUI — see `pendo-io/pendo-mobile-sdk` on GitHub
