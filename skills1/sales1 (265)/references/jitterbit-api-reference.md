<!-- Source: https://docs.jitterbit.com/management-console/audit-logging/ (login flow, authToken header, sessionTimeoutInSeconds, TFA code field) -->
<!-- Source: https://docs.jitterbit.com/getting-started/jitterbit-security/allowlist-information/ (per-region hosts, apac-southeast, gateway domains) -->
<!-- Source: https://docs.jitterbit.com/getting-started/support/my-region/ (region subdomains) -->
<!-- Source: https://docs.jitterbit.com/api-manager/key-concepts/ (custom API service URL format) -->
<!-- Source: https://www.linkedin.com/pulse/jitterbit-harmony-platform-api-george-jeffcock -->
<!-- Re-verified against live official docs 2026-06-13 -->
<!-- Note: Jitterbit's per-endpoint REST API reference is primarily documented via SwaggerHub (jitterbit/jitterbit-rest_api) and inside the Harmony portal. This reference captures the structure, authentication flow, and regional base URLs from public sources. For full per-endpoint specs, consult the SwaggerHub OpenAPI document or the Harmony Management API documentation inside your portal. -->

# Jitterbit Harmony Management API Reference

## Overview

The Harmony Management API is a REST API for programmatic management of the Jitterbit Harmony platform — orgs, environments, agent groups, agents, projects, operations, API Manager APIs, operation logs, and API analytics. It is distinct from APIs built and published by customers in Jitterbit API Manager (those have customer-defined paths and auth).

## Authentication

**Method**: Token-based login over HTTPS. Log in once to obtain an `authenticationToken`, then pass it as the `authToken` header on subsequent calls.

### Standard login flow

- **Endpoint**: `PUT /user/login`
- **Headers**: `Content-Type: application/json`
- **Payload**:
  ```json
  {
    "email": "user@example.com",
    "password": "...",
    "deviceId": "<unique-device-identifier>"
  }
  ```
- **Response**: JSON body containing `authenticationToken` (example: `"1_70dfe7f7-1d47-4ad5-be5d-bc4a222dd2g4"`) plus the list of orgs the user belongs to and `sessionTimeoutInSeconds` (documented as **14400** = 4 hours). Pass the token on every subsequent call as the header `authToken: <authenticationToken>`.
  - **Note**: Older third-party write-ups state the token "expires after 15 minutes"; the official login response now returns `sessionTimeoutInSeconds: 14400` (4 hours). For unattended access, still build refresh-on-401 logic.

### Subsequent calls

- **Header**: `authToken: <authenticationToken>` (plus `Content-Type: application/json`). The login endpoint is the only call that does not require `authToken`.

### Two-factor authentication (TFA) flow

If TFA is enabled on the account, two requests are required:

1. Submit `PUT /user/login` as above (the `deviceId` is required so the device can be confirmed). The response indicates a TFA code was emailed to the user.
2. Submit the emailed code:
   - **Endpoint**: `PUT /user/login/tfacode`
   - **Payload**: `{ "email": "...", "code": "<code received by email>", "deviceId": "<same device id>" }` — the TFA field is named `code`, not `tfaCode`.
3. Response returns the authenticated `authenticationToken`.

### SSO and API access caveats

- SSO (Okta, Azure AD, Google, Salesforce) is supported for portal login, but requires bypass rules configured by your Jitterbit admin for API access using service credentials.
- TFA configured as "on each login" is **incompatible with unattended API access**. For programmatic access, either:
  - Disable TFA on a dedicated service account.
  - Use a TFA setting that allows trusted devices.

## Base URLs

Regional base URL for the REST service:

| Region | Base URL |
|---|---|
| NA (North America, South America) | `https://na-east.jitterbit.com/jitterbit-cloud-restful-service` |
| EMEA (Europe, Middle East, Africa) | `https://emea-west.jitterbit.com/jitterbit-cloud-restful-service` |
| APAC (Asia-Pacific, including Australia) | `https://apac-southeast.jitterbit.com/jitterbit-cloud-restful-service` |

Portal/app URLs (browser login) use `apps.na-east.jitterbit.com`, `apps.emea-west.jitterbit.com`, `apps.apac-southeast.jitterbit.com`. `https://login.jitterbit.com` auto-redirects to the geolocation-matched portal.

## Representative endpoints

The API is organized around controllers. Representative operations include:

| Endpoint | Method | Purpose |
|---|---|---|
| `/user/login` | PUT | Authenticate and obtain `authenticationToken` |
| `/user/login/tfacode` | PUT | Submit TFA code to complete login |
| `/op-log-service-controller/queryOperationLogUsingPUT` | PUT | Query operation execution logs |
| `/api-analytics-controller/geDebugLogsUsingPUT` | PUT | Retrieve API analytics / debug logs |

Additional controllers cover: organization, environment, agent group, agent, project, deployment, schedule, API, security profile, and user/role management. Full per-endpoint documentation is in the SwaggerHub spec and the in-portal API docs.

## Content format

- **Request / response**: JSON.
- **HTTPS required** — TLS 1.2 or higher.
- Standard `Content-Type: application/json` / `Accept: application/json` headers.

## OpenAPI / Swagger

- **OpenAPI 3.0 spec**: Published on SwaggerHub under `jitterbit/jitterbit-rest_api` (e.g., `V9.1.0.2-oas3`).
- **Swagger 2.0 spec**: Importable to Postman from SwaggerHub JSON endpoint.

Use these specs to auto-generate client SDKs, explore endpoints in Postman, or run contract tests.

## Rate limits

Jitterbit does not publish specific per-endpoint rate limit numbers. Rate limiting is applied per-organization, with adjustments available for high-volume use cases via Jitterbit Support.

For published APIs in API Manager, rate limits are **configured by the customer** per API Group (requests per time window). Exceeding returns HTTP 429.

## Allowlisting

All agent and API traffic is outbound HTTPS. For firewall allowlisting, Jitterbit publishes an allowlist of host names per region that must be reachable on port 443. See the Jitterbit docs under "Allowlist Information" for the current list.

Hosts to allowlist per region (from the official Allowlist Information page):

| Surface | NA (`na-east`) | EMEA (`emea-west`) | APAC (`apac-southeast`) |
|---|---|---|---|
| Portal/App | `apps.na-east.jitterbit.com` | `apps.emea-west.jitterbit.com` | `apps.apac-southeast.jitterbit.com` |
| REST service | `na-east.jitterbit.com` | `emea-west.jitterbit.com` | `apac-southeast.jitterbit.com` |
| Identity | `login.jitterbit.com` | `login.jitterbit.com` | `login.jitterbit.com` |
| API gateway (cloud) | `*.jitterbit.net` | `*.jitterbit.eu` | `*.jitterbit.cc` |
| Messaging (MQ) | `mq.apps.na-east.jitterbit.com` | `mq.apps.emea-west.jitterbit.com` | `mq.apps.apac-southeast.jitterbit.com` |
| Cloud datastore | `cloud-datastore.apps.na-east.jitterbit.com` | `cloud-datastore.apps.emea-west.jitterbit.com` | `cloud-datastore.apps.apac-southeast.jitterbit.com` |

All on port 443. Note the cloud API gateway uses a region-specific top-level domain (`jitterbit.net` / `jitterbit.eu` / `jitterbit.cc`), not `jitterbit.com`.

## API Manager (customer-published APIs)

APIs built in Jitterbit API Manager are deployed on the regional cloud API gateway. The API service URL format is:

`<Protocol>://<Base URL>/<Environment URL Prefix>/<Version>/<Service Root>`

- **Base URL** = the API subdomain (organization name + org ID) plus the region's API-gateway domain: `jitterbit.net` (NA), `jitterbit.eu` (EMEA), or `jitterbit.cc` (APAC) — NOT `jitterbit.com`.
- **Environment URL Prefix** = the environment the API is published to (e.g., `Development`).
- **Version** = optional API version segment.
- **Service Root** = the public API name.

Example: `https://JBExample123456.jitterbit.net/Development/1/customer`

A Private API Gateway can replace the base URL with a subdomain of a domain you control. Customer APIs use their own Security Profiles (Anonymous, Basic, OAuth 2.0, API Key), with Trusted IP Groups for IP allowlisting. Rate limits and policies are configured per API Group in the Jitterbit portal.

## Postman and tooling

- **Postman collection**: Auto-generable from the SwaggerHub OpenAPI spec. Import the spec URL into Postman, then configure a collection variable for the session token.
- **Auth pattern in Postman**: Use a pre-request script to call `PUT /user/login` and save the session token to a collection variable. Apply the token as a header on subsequent requests.

## Notes on documentation

The primary Jitterbit docs site (`docs.jitterbit.com`) has historically used multiple URL structures, and some previously-public API reference pages return 404. For current official references:

1. SwaggerHub: `https://app.swaggerhub.com/apis-docs/jitterbit/jitterbit-rest_api`
2. In-portal API docs: Harmony portal → Help → API Documentation
3. Jitterbit Success Central: `https://success.jitterbit.com` (redirects to docs)

If endpoints in this reference drift from current Jitterbit docs, treat the SwaggerHub spec as canonical.
