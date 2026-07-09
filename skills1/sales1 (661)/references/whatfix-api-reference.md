<!-- Sources: https://developer.whatfix.com/ (JS-rendered, "API Reference Beta"), https://support.whatfix.com/docs/developer-api, https://support.whatfix.com/docs/developer-guide, https://support.whatfix.com/docs/generatingtheapitoken, https://support.whatfix.com/docs/downloading-report-analytics-data-using-api -->
<!-- Re-verified 2026-06-13 against live support.whatfix.com docs. The full developer.whatfix.com reference is JS-rendered and could not be fetched verbatim; endpoint/header/base-URL facts below are corroborated across the support docs and current curl examples. -->

# Whatfix API Reference (Partial)

## Overview

Whatfix Developer APIs v1 let you exchange information between Whatfix and your web application or any 3rd-party application. The APIs are built using REST principles and follow HTTP rules — every resource is exposed as a URL. The full reference is published at https://developer.whatfix.com/ ("Whatfix API Reference Beta").

## Authentication

- **Method**: User API token ("Integration Key") passed via header. **Two headers are required on authenticated calls:**
  - `x-whatfix-integration-key` — your User API token (the Integration Key)
  - `x-whatfix-user` — the email address of the Whatfix user the token belongs to
- **Content-Type**: `application/json` on requests with a JSON body
- **Token generation**: The API Token must first be **enabled for your account by Whatfix support** (contact `support@whatfix.com`). Once enabled, on the Whatfix Guidance dashboard go to **Settings → API token** and copy the generated token.
- **Transport**: "The APIs are served only via HTTPS to secure this authentication method, and the key must be kept secret." HTTPS-only.
- **Type**: Stateless — all requests are validated against the API token.
- **Note**: Some endpoints do not require authentication, but most do.

## Base URL

There are two documented hosts:

- **Content / core API**: `https://api.whatfix.com/v1/`
- **Report analytics API**: `https://whatfix.com/api/v1/`

Both embed your **Account ID** in the path (e.g. `c5eerfd0-db6f-11e9-a037-d43b0489acab`). Contact `support@whatfix.com` to obtain your Account ID. The host/region may vary by deployment — confirm in your Whatfix instance settings.

## Format

- **Output**: JSON (CSV for report-analytics downloads via `?format=csv`)
- **CORS**: Enabled — handles cross-origin requests

## Endpoints

### Content

`/v1/accounts/{accountId}/content`

- **GET** — retrieve content (Flows, Smart Tips, etc.) for the account.
- **POST** — create content. Accepts a JSON array of objects with properties like `title`, `url`, and `type` (e.g. `"type": "link"`).

Example (GET):

```
curl -X GET 'https://api.whatfix.com/v1/accounts/{accountId}/content' \
  -H 'x-whatfix-integration-key: YOUR_API_KEY' \
  -H 'x-whatfix-user: user@example.com' \
  -H 'Content-Type: application/json'
```

Example (POST):

```
curl -X POST 'https://api.whatfix.com/v1/accounts/{accountId}/content' \
  -H 'Content-Type: application/json' \
  -H 'x-whatfix-integration-key: YOUR_API_KEY' \
  -H 'x-whatfix-user: user@example.com' \
  -d '[{"title": "Page Title", "url": "https://example.com", "type": "link"}]'
```

### Report Analytics (download)

`https://whatfix.com/api/v1/{accountId}/reports/summary/{reportName}?format=csv`

- **GET** — download a report summary. Example report name: `mostPopularFlows`. Append `?format=csv` to download as CSV.
- Same two auth headers required (`x-whatfix-integration-key`, `x-whatfix-user`).

Example:

```
curl -X GET 'https://whatfix.com/api/v1/{accountId}/reports/summary/mostPopularFlows?format=csv' \
  -H 'x-whatfix-integration-key: YOUR_API_KEY' \
  -H 'x-whatfix-user: user@example.com'
```

## API Capabilities

### Content Management
- Create, update, delete Flows
- Create, update, delete Smart Tips
- Manage Pop-ups and Beacons
- Manage Task Lists

### Content Tagging
- Apply and manage tags on content
- Tag types: Role, Page, Auto, Miscellaneous

### Enterprise Integration Attributes
- Manage user attributes for segmentation
- Sync external system data for content targeting

### Report Analytics
- Download analytics data via API (CSV)
- Available metrics:
  - Number of queries served by Self Help
  - Number of times a Pop-up was shown
  - Number of times a Flow was played
  - Number of times a Smart Tip was shown
  - User engagement and completion data

## Integration Hub

The Integration Hub is a separate feature (not the raw API) for creating integrations:
- Create custom uni- or bi-directional data flows
- Listen to multiple APIs and Webhooks from external apps (inbound)
- Schedule integrations with configurable frequency
- Pre-built connectors for Salesforce, Oracle, SAP, Workday, Azure AD, etc.

## SDKs

Whatfix provides mobile SDKs (GitHub org `github.com/whatfix`, verified, ~8 public repos):
- **Android**: `whatfix-android` ("Whatfix Android SDK. DAP solution for mobile apps")
- **iOS**: Multiple packages — `Whatfix-iOS`, `core-ios`, `creator-ios`, plus `ios`
- **Xamarin iOS**: `whatfix-xamarin-ios`
- **React**: `ReactReference`

## Gaps in This Reference

- The full developer.whatfix.com reference is JS-rendered and could not be captured verbatim; the complete endpoint catalog (beyond content + report-analytics) is not enumerated here.
- Request/response payload schemas are only partially documented (content POST array shape above).
- **Rate limits** — not publicly documented (UNVERIFIED).
- **Error codes** — not publicly documented (UNVERIFIED).
- **Pagination** — not publicly documented (UNVERIFIED).
- **Outbound/emitted webhooks with signing** — no official Whatfix-emitted webhook event list, payload, or HMAC signing spec was found; the Integration Hub only documents *listening to* external webhooks (inbound), not Whatfix publishing signed webhooks (UNVERIFIED).

For complete API documentation, visit https://developer.whatfix.com/ (requires a browser — content is JavaScript-rendered).
