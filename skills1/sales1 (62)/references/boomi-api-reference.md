<!-- Source: https://developer.boomi.com/docs/APIs/PlatformAPI/Introduction/Platform_API -->
<!-- Source: https://developer.boomi.com/docs/APIs/PlatformAPI/Introduction/Platform_API_and_Partner_API_authentication -->
<!-- Source: https://developer.boomi.com/docs/api/platformapi/ExecutionRequest -->
<!-- Source: https://developer.boomi.com/docs/APIs/PlatformAPI/Introduction/OpenAPI_3_0 -->
<!-- Source: https://help.boomi.com/docs/Atomsphere/Data_Integration/RESTAPI/dataintegration-api-overview -->
<!-- Re-verified against live docs 2026-06-13 -->

# Boomi Platform API Reference

## Authentication

**Primary method**: HTTP Basic Authentication

Two Basic Auth options:
1. **Username + Password**: Your Boomi Enterprise Platform sign-in credentials. Available for non-SSO users and SSO administrators.
2. **API Token** (recommended): In the Basic Auth header, use `BOOMI_TOKEN.<username>:<token_value>` (e.g. `BOOMI_TOKEN.user@boomi.com:123aab45-67b8-...`). The `BOOMI_TOKEN.<username>` is the user field and the token is the password.

SSO users **without** Administrator privileges must use an API token (username/password won't work). API tokens are also recommended when 2FA is enabled.

Generate tokens: Settings → Account Information and Setup → AtomSphere API Tokens

**Additional auth methods (per current docs):**
- **JWT tokens**: Generated via a GET to regional endpoints for certain APIs (Data Hub Repository API and GraphQL APIs). JWTs expire after **5 minutes** and must be regenerated for longer-lived integrations.
- **Two-factor (2FA)**: For ad-hoc calls, supply the one-time passcode via the `X-Boomi-OTP` header.

## Base URLs

| Region | Base URL |
|---|---|
| US | `https://api.boomi.com/api/rest/v1/{accountID}` |
| GB | `https://api.platform.gb.boomi.com/api/rest/v1/{accountID}` |

## Request/Response Formats

- **Default**: XML
- **JSON requests**: Set `Content-Type: application/json` header
- **JSON responses**: Set `Accept: application/json` header
- XML schemas available at: `https://api.boomi.com/api/soap/v1/{accountID}?xsd=1`

## Rate Limits

**Maximum**: 10 requests per second

Exceeding this returns HTTP 503 (Service Temporarily Unavailable). Boomi connectors automatically retry up to 5 times on 503.

## API Architecture

The API follows an **object/verb hierarchy**:

- **Objects**: Account, Atom, Environment, Component, Process, Deployment, etc.
- **Verbs**: GET (retrieve), QUERY (search), CREATE, UPDATE, DELETE, plus action objects (e.g., POST to the `ExecutionRequest` object to run a process)

## API Categories

### Account Administration
Manage accounts, users, roles, API tokens, and account-level settings.

### Cloud Management
Manage Atom Clouds, Cloud Atom attachments, and cloud-specific configurations.

### Component Management
CRUD operations on integration components: Processes, Maps, Profiles, Connector Operations, API Service Components.

### Deployed Process Management
Manage deployed processes across environments, view deployment history, and undeploy.

### Deployment
Package components, deploy packages to environments, manage deployment schedules.

### Environment Management
CRUD operations on environments, environment extensions, and environment-to-Atom attachments.

### Execution Statistics
Query process execution records — status, timing, document counts, error details.

### Integration Packs
Manage pre-built integration pack configurations and deployments.

### Process Execution
Execute processes programmatically and retrieve execution results.

Key operation: `POST /{accountID}/ExecutionRequest` — triggers a deployed process. This is the **ExecutionRequest** object (not a verb named `executeProcess`).

- **Request body**: `atomId` (required — the Runtime ID to run on), `processId` (required — the process component ID), optional `DynamicProcessProperties` (dynamic process property name/value pairs) and `ProcessProperties` (process component property values with keys).
- **Response (200)**: returns a `requestId` (unique identifier) plus a `recordUrl` (URI to fetch the corresponding execution record).
- **Async**: the POST returns immediately without waiting for completion. Poll the **Execution Record** object using the `requestId` for detailed run results; that endpoint may return HTTP 202 until the record is ready.

### Runtime Management
Manage Atoms, Molecules, and Atom Clouds — status, properties, logs, restart.

## OpenAPI 3.0

OpenAPI specification available for programmatic discovery of Platform API and Partner API endpoints:

```
GET https://api.boomi.com/api/rest/v1/{accountID}/openapi.json          (US)
GET https://api.platform.gb.boomi.com/api/rest/v1/{accountID}/openapi.json   (GB)
```

Use this with Postman, Swagger UI, or any OpenAPI-compatible tool to explore available endpoints.

## Postman Collection

Boomi provides an importable Postman collection for testing API endpoints. Available in the developer documentation at developer.boomi.com.

## SOAP API

SOAP interface also available for legacy integrations:
- WSDL: `https://api.boomi.com/api/soap/v1/{accountID}?wsdl`
- Authentication: WS-Security with UsernameToken
- Same operations as REST API

## Partner API

Separate API for Boomi partners managing multiple customer accounts:
- Provision customer accounts
- Manage partner-level configurations
- Same auth pattern, different endpoint prefix

## Data Integration API (separate product)

For Boomi Data Integration (formerly Rivery — acquired Dec 2024, ELT/reverse-ETL pipeline product), a separate API exists:

- **Auth**: Bearer token — `Authorization: Bearer {token}`
- **Base URLs**:
  - US: `https://api.rivery.io`
  - EU: `https://api.eu-west-1.rivery.io`
  - IL: `https://api.il-central-1.rivery.io`
  - AU: `https://api.ap-southeast-2.rivery.io`
- **Path structure**: `/v1/accounts/{account_id}/environments/{environment_id}/[resource]`. Example for a flow: `/v1/accounts/{account_id}/environments/{environment_id}/data_flows/{river_id}/[action]`.
- **Resource groups**: Data Flows (the core workflow objects — "Rivers" in legacy terminology), Sub Data Flows, Runs, Run Groups, Activities Statistics (environment/data-flow activity metrics incl. RPU consumption), Activities Targets (target table names + status), Environments.
