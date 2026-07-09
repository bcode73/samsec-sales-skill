<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/home.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/getstarted/basics/api-basics.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/getstarted/basics/authentication.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/users/user-orgs.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/apps/push-new-app.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/apps/stop-app.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/apps/check-app-status.html -->
<!-- Source: https://integration.cloud.tibco.com/docs/Subsystems/tci-api/monitor/view-app-inst-metrics.html -->
<!-- Re-verified against live official docs: 2026-06-13 -->

# TIBCO Cloud Integration API Reference

## Overview

The TIBCO Cloud Integration API adheres to the principles of RESTful Web services. You can use it to automate administration, deployment, and monitoring of TCI — integrate TCI into your CI/CD pipeline, build custom dashboards, or manage apps programmatically.

The TIBCO Cloud Integration REST API:
- Uses SSL (HTTPS) to ensure all data is secure.
- Uses **OAuth 2.0** and **Bearer Token** to validate API users.
- Validates that API users have the same rights and restrictions as they do in the TIBCO Cloud Integration user interface for all Organization-based methods.
- Uses TIBCO Cloud Integration interface entities, such as Organizations and Apps, as REST resources that exchange data with the API as JSON objects.

Select endpoints on the TIBCO Cloud Integration Swagger page to try out the available functions before you start coding.

## Regional base URLs

There are multiple instances for the API site available in different regions. Each region has its own API URL and a dedicated Swagger page. **Be sure to use the API URL and Swagger page associated with the region for your subscription or no data will be returned when you make an API call.**

| Region | API URL |
|--------|---------|
| AWS US | `https://api.cloud.tibco.com/tci/v1` |
| AWS US East | `http://us-east.api.cloud.tibco.com/tci/v1` |
| AWS Europe | `https://eu.api.cloud.tibco.com/tci/v1` |
| AWS Australia | `https://au.api.cloud.tibco.com/tci/v1` |
| Azure US | `https://api.us.azure.cloud.tibco.com/tci/v1` |

### Swagger documentation pages

Each region maintains a dedicated Swagger page. Replace `api` with `api/tci/docs/` on your regional host, or browse from the TCI console. Complete endpoint specifications, request/response schemas, and interactive "Try it out" are available only through the region-specific Swagger pages.

## API basics

### Transport
- All HTTP calls to the API are redirected to HTTPS.
- Requests to the TIBCO Cloud Integration API **time out after 120 seconds**.

### Subscription Locator
All HTTP calls to the API, **except the `GET /v1/userinfo` call**, require a Subscription Locator to identify the organization. The Subscription Locator is a **path parameter** in the resource URL — `{subscriptionLocator}` in paths like `/v1/subscriptions/{subscriptionLocator}/apps` — not a header. Obtain it from `GET /v1/userinfo` (the `subscriptionLocator` field for each org). **If you pass `0` or omit it, the API defaults to the Subscription Locator of the organization associated with your OAuth Token.** (Verified 2026-06-13.)

### Naming convention
TIBCO Cloud Integration uses the **lower camel case** naming convention for JSON data across the TIBCO Cloud Integration API and endpoints (e.g., `lastName`).

### Datetime format
Datetime field values are returned in **Epoch time** (seconds since 1970-01-01 UTC, or milliseconds depending on endpoint — verify per-endpoint).

### Authorization
Any role requirements imposed in the TIBCO Cloud Integration User Interface are also imposed by the TIBCO Cloud Integration API — i.e., a user without Admin role cannot call admin-only endpoints even with a valid token.

### Authentication (OAuth 2.0 + Bearer Token)
TCI authenticates API callers with OAuth 2.0 Bearer tokens. Pass the token in the `Authorization: Bearer <token>` header on every call. Generate the OAuth token from **user settings** in the TCI UI (configure an OAuth client + Client Secret, generate the access token, enable it for the Integration domain). The token is bound to the organization you were in when you generated it (plus its parent/child orgs where you have membership).

**Token lifetimes (verified 2026-06-13):** OAuth **access tokens are valid for a maximum of 8 hours**; **refresh tokens are valid for 7 days**. Refresh the access token periodically with the refresh token before it expires, and re-issue/rotate the refresh token within 7 days. (Source: TCI API Authentication page.)

### HTTP response codes
- `2xx` — success (200 OK, 201 Created, 204 No Content).
- `4xx` — client errors (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict).
- `5xx` — server errors (500 Internal Server Error, 503 Service Unavailable).
- A detailed HTTP Response Codes section is available in the TCI API docs at `/Subsystems/tci-api/http-response.html`.

## Endpoints (verified against current public docs 2026-06-13)

Paths are identical across regions — only the host (base URL) differs. Every path except `GET /v1/userinfo` carries the org's `{subscriptionLocator}` as a path segment (pass `0` to default to your token's org).

### Discovery / user
- **`GET /v1/userinfo`** — list all organizations the calling user can access, each with its `subscriptionLocator`. The ONLY endpoint that does not require a Subscription Locator. Use it first to discover the locator for subsequent calls.

### Managing apps
- **`POST /v1/subscriptions/{subscriptionLocator}/apps`** — push a **new** app (and, with the same path, push an **updated** existing app). `multipart/form-data` body. Query params: `appName`, `instanceCount` (default 0), `retainAppProps`, optional `tunnelKey` (hybrid agent access key id), optional `forceOverwrite=true`. Form fields: `artifact` (EAR for BusinessWorks, ZIP for Node.js, JSON for Flogo), `manifest.json` (required for Node.js/Flogo, optional if in the EAR), optional `overrides` (variable value overrides). **Asynchronous** — poll the status endpoint afterward.
- **`POST /v1/subscriptions/{subscriptionLocator}/apps/{appId}/stop`** — stop an app by scaling its running instances to zero. Asynchronous — poll status. (Scaling up/starting is driven by `instanceCount` on the push/scaling operations.)
- **`GET /v1/subscriptions/{subscriptionLocator}/apps/{appId}/status`** — check deploy/scale status of an app. Poll until status is complete.
- **`PUT /v1/subscriptions/{subscriptionLocator}/apps/{appId}/pin`** — restore a pinned Flogo app; **`DELETE .../apps/{appId}/pin`** — remove a pin from a Flogo app.

### App endpoints
- **`GET /v1/subscriptions/{subscriptionLocator}/apps/{appId}/endpoints`** — list all public and private endpoints for an app.
- **`PUT /v1/subscriptions/{subscriptionLocator}/apps/{appId}/endpoints/{endpointId}`** — update an app endpoint's service name and description.

### Monitoring
- **`GET /v1/subscriptions/{subscriptionLocator}/apps/{appId}/instances/{instanceId}/monitoring/metrics/resource`** — resource metrics for one app instance (execution count, CPU, memory, last-execution time). Optional `since` query param (hours; defaults to 24).

### Organization
- **Enable/disable API access for an org** — there is a dedicated org-API-access method (see `/Subsystems/tci-api/organization/org-api-access.html`).

Role enforcement: Admins and (standard) Users can manage/scale apps in their org; read-only users cannot scale apps. Other resource groups (organizations/child orgs, users/roles, connections, agents) are exposed in the UI-equivalent API surface; consult your region's Swagger page for their exact paths. Because paths are the same across regions but the host differs, the common failure is calling the wrong-region host — wrong-region calls return no data even with a valid token.

## Related tooling

- **TIBCO Cloud CLI** (`cic-cli-main` on GitHub) — command-line front-end to the TCI API. Plugin architecture for API Management, AsyncAPI conversion, and more.
- **Maven plugin** (`flogo-maven-plugin`) — build/deploy Flogo apps in Maven projects.
- **Helm charts** (`tp-helm-charts`) — deploy TIBCO Platform components on Kubernetes.

## Gaps in this reference

- **Partial endpoint catalog**: the public docs DO document concrete endpoint paths for the common app-management/monitoring operations (captured above as of 2026-06-13). They do NOT publish a single exhaustive catalog of every resource (connections, users/roles, child-org admin, agent registration); for those, consult the Swagger page for your subscription region for definitive paths, request/response schemas, and examples.
- **OAuth flow specifics**: token lifetimes are now confirmed (access ≤8h, refresh 7 days) but the public docs do not publish the raw token endpoint URL / scope catalog — the OAuth client + token are generated in the TCI UI (user settings), with deeper OAuth setup at `account.cloud.tibco.com`.
- **Rate limits**: not publicly specified beyond the 120-second request timeout. (Hybrid plan bundles API Management included up to 100k QPM, but that is a gateway throughput allowance, not a TCI control-plane API rate limit.)
- **Webhooks**: TCI's control-plane API has no documented webhook/event-push mechanism; eventing is done in-app via Flogo triggers (Kafka/Pulsar/etc.), not via platform webhooks. No HMAC webhook signing applies at the platform-API layer.
