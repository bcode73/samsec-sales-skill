<!-- Source: https://developer.medallia.com/medallia-apis/reference/integrations -->
<!-- Note: Developer portal is JS-rendered — full API docs could not be copied verbatim. -->
<!-- This reference is reconstructed from search results and platform documentation pages. -->
<!-- For the authoritative, complete API reference, see: https://developer.medallia.com -->

# Medallia API Reference

## Authentication

All Medallia APIs use **OAuth 2.0** with the `client_credentials` grant.

**Token endpoint**: `POST https://{instance}.medallia.com/oauth/{company}/token` — note the token is issued by the **MEC reporting instance host** (`{instance}.medallia.com`), NOT the API gateway host (`{instance}-{company}.apis.medallia.com`). The path segment is your **company / tenant name**, not the instance name.

**Required**: client ID + client secret (per instance — production, sandbox, and developer environments each need their own credentials, obtained from the Medallia admin portal).

**Token request** — credentials go in the **HTTP Basic Authentication header** (not the body):
```
curl "https://{instance}.medallia.com/oauth/{company}/token" \
  -X POST \
  -u 'client_id:client_secret' \
  -d 'grant_type=client_credentials'
```

**Response**: JSON with `access_token`, `token_type` (`Bearer`), and `expires_in` (`3600` seconds / 1 hour). Implement token refresh logic — do not hardcode tokens.

```json
{ "access_token": "...", "token_type": "Bearer", "expires_in": 3600 }
```

## REST APIs

**Base / gateway URL pattern**: `https://{instance}-{company}.apis.medallia.com/{path}` — the gateway host is `{instance}-{company}` followed by the constant suffix `apis.medallia.com` (independent of the data center). Admin REST APIs sit under `/admin/v1/<rest-api>` (e.g. `/admin/v1/users`); Import APIs sit under `/inbound/...` (see below).

REST APIs are used for:
- Object manipulation (users, roles, units) — Admin APIs
- Bulk data import — Import API
- Program administration
- Survey management

### Import API

Upload data files for processing into Medallia Experience Cloud. Import APIs are accessed under the `/inbound/...` namespace — NOT under `/admin/v1/import`.

**Key endpoints**:
- `POST /inbound/{version}/{importer-name}` — submit a data import (synchronous; `{importer-name}` identifies the specific Import API / importer being targeted)
- `POST /inbound/v2/async/{importer-name}` — **asynchronous** import. Returns the **feed file ID** of the created feed file so processing status can be queried later. (Opt-in / Early Adopter feature introduced in the 2023 Summer Release — contact your Medallia rep to enable.)

The returned **feed file ID** identifies the import job. Use it with the Feed File APIs to query aggregate stats (records successfully created / updated / discarded) or detailed per-record results. Detailed results return up to the first **5,000 input records per result status**.

**Use cases**: Import operational data (CRM records, transaction data), import historical feedback, bulk update customer records.

### Admin APIs

Manage users, roles, and organizational hierarchy under `/admin/v1/<rest-api>` (e.g. `/admin/v1/users`, `/admin/v1/roles`):
- User creation and role assignment
- Unit hierarchy management
- Program configuration

## GraphQL Query API

**Endpoint**: `POST https://{instance}-{company}.apis.medallia.com/data/v0/query` (single GraphQL endpoint on the API gateway host)

**Purpose**: Real-time analytics and data extraction through a single GraphQL endpoint.

**Key capabilities**:
- Extract survey responses with filtering (date range, feedback type, score range)
- Pull aggregated analytics (NPS by unit, CSAT trends over time)
- Access text analytics results
- Custom data extraction for data warehouse loading

**Example query structure**:
```graphql
{
  records(filter: {dateRange: {from: "2026-01-01", to: "2026-03-31"}}) {
    edges {
      node {
        npsScore
        commentText
        surveyDate
        unit {
          name
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

**Pagination**: Cursor-based. Use `pageInfo.endCursor` as the `after` parameter in subsequent queries.

**Altair GraphQL Client**: Medallia recommends the Altair GraphQL Client for testing queries against the Query API.

## Webhooks

Medallia can POST data to your endpoint on configured events. Outbound webhook calls can authenticate to your API using OAuth 2.0, HTTP Basic Authentication, or other shared-token schemes.

**Activation flow** (required before you receive data):
- When a webhook is created, Medallia first fires a `Webhook.Created` event to your URL. This first request carries the **`X-Hook-Key`** header.
- Pick up the `X-Hook-Key` value and activate the webhook with `POST .../hooks/{WebhookId}/activate`. You receive no further data until activation succeeds (this guards against registering a wrong URL).
- Subsequent webhook requests include the webhook authentication header — validate it, since it is the only way to confirm the request originated from Medallia.

HTTPS with TLS v1.2 is required for webhook delivery. (Medallia Agile Research exposes a fuller Webhooks REST API at `https://api-us.agileresearch.medallia.com/WebHooks` / `api-eu.` for the EU region.)

## Web Feeds (Import API legacy)

More versatile than standard RESTful APIs — includes a flexible ETL process for data validation and transformation for both inbound and outbound data flows. Being superseded by the v2 Import API for new integrations.

## Rate Limits

- **Minimum**: 60,000 API calls per 24-hour window (all instances)
- **Simultaneous / burst**: 10 API calls per second per API (e.g. 10/sec to the Users API and 10/sec to the Roles API on the production instance)
- **Query API cost throttle**: in addition to call counts, Query API calls have a cost structure and are throttled once the **3,000,000 cost-units-per-query** limit is reached
- **Rate-limit headers**: Experience Cloud APIs return HTTP rate-limit headers per the IETF `draft-polli-ratelimit-headers` spec — read them to track remaining quota
- **Higher limits**: Available by contract negotiation
- **Recommendation**: Batch operations where possible, implement exponential backoff for rate limit errors

## SDKs

### MEC CLI
Command-line interface for Medallia Experience Cloud (reference implementation, repo `medallia/mec-cli`):
```bash
brew tap medallia/mec-cli
brew install mec
mec --help
```

### Mobile SDKs
- **iOS**: `medallia/digital-ios-sdk` — Swift, available via CocoaPods/SPM
- **Android**: `medallia/mxo-android-sdk` — Kotlin, available via Maven
- **React Native**: `medallia/dxa-react-native-sample-apps` — cross-platform DXA

### GitHub repositories
Organization: https://github.com/medallia (128 public repos)

Key repos:
- `public-api-swaggers` — Swagger/OpenAPI files describing the APIs available to Medallia clients and developer partners (authoritative machine-readable spec source)
- `query-api-data-extract` — reference implementation for streaming data out via the Query API
- `mec-cli` — MEC command-line reference implementation (Homebrew: `brew tap medallia/mec-cli && brew install mec`)
- `Anywhere-SampleApps` — reference implementations for Experience Cloud services
- `digital-ios-sdk` / `mxo-android-sdk` — mobile SDKs
- `merci` — Go/gRPC rate limiting service
