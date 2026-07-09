<!-- Source: https://docs.snaplogic.com/public-apis/public-apis-about.html -->
<!-- Re-verified 2026-06-13 against live docs.snaplogic.com. Base path confirmed /api/1/rest/public; JWT Bearer + aud claim confirmed; runtime apistats endpoint added; triggered-task rate limits (concurrent 10 default, daily, HTTP 429) and Client Throttling 1000/min added; SnapGPT audit-log Public API (45-day) added. -->
<!-- Note: Detailed per-endpoint specs are spread across multiple JS-rendered pages. This reference captures the API structure and categories from the documentation navigation. For full endpoint details, consult docs.snaplogic.com directly. -->

# SnapLogic Public APIs Reference

## Authentication

SnapLogic Platform authenticates Public API calls with:
- **Basic Authentication**: Email (SnapLogic user or service account) + password, base64-encoded.
  - Header: `Authorization: Basic {base64_encoded <email>:<password>}` with `Content-Type: application/json`.
- **JWT (JSON Web Token)**: Recommended for production. Supports Okta and Microsoft Entra ID as identity providers.
  - Header: `Authorization: Bearer Token {token}`.
  - Required JWT claims: `iat`, `exp`, `sub`, `aud`, `iss`, `org`.
  - The `aud` (audience) claim must equal the SnapLogic Public API base URL for your POD (e.g. `https://elastic.snaplogic.com/api/1/rest/public`). If you can't set the standard `aud`, a custom `snaplogic_aud` claim with the same value is supported.

All API calls require HTTPS.

## Base URL

Public APIs use the path prefix `/api/1/rest/public`:
- Org-specific: `https://{pod}.snaplogic.com/api/1/rest/public/...`
- POD (Point of Deployment) varies by region/instance — Prod US, EMEA, UAT, etc. (e.g., `elastic.snaplogic.com`).
- Example base URL: `https://elastic.snaplogic.com/api/1/rest/public`

## API Categories

### Activity APIs
- Retrieve activities in an Org/Environment
- Activity metadata reference

### API Management APIs (Classic and APIM 3.0)
- Create an API version from a project
- Delete API / Delete API version
- Publish / Unpublish / Deprecate / Retire API versions
- Migrate and Import/Export API versions
- Policy management (Export/Import)
- User approval workflows
- Response cache invalidation
- API Management logs retrieval
- Git operations (branch, checkout, pull, tag management)

### Asset APIs
- Project/space access control
- User privileges and ownership management
- Asset metadata operations

### Asset Catalog APIs
- Custom metadata operations
- Lineage retrieval
- Asset listings and search

### Log APIs
- Task log retrieval
- Execution history

### Runtime APIs
- Pipeline execution information
- Runtime metrics and performance data
- `GET /runtime/apistats/{org}` — retrieve concurrent and daily execution metrics
- `GET /runtime/apistats/{org}/daily` — daily execution metrics
- `GET /runtime/apistats/{org}/concurrent` — concurrent execution metrics

### Pipeline APIs
- Pipeline quality assessment
- Pipeline metadata and configuration

### Task APIs
- Task enablement / disablement
- Snaplex assignment for tasks
- Task scheduling and management

### Project APIs
- Git branch creation
- Project creation from Git files
- Git checkout operations
- Change discarding
- Git pull operations
- Git tagging
- Repository status retrieval
- Asset copying between projects
- Project migration across environments
- Migration status tracking
- Project export/import capabilities
- Individual asset export/import
- Git tracking removal

### Snaplex APIs
- Node management (add/remove/restart)
- Snaplex configuration
- Version management
- Health and status monitoring

### Snap Statistics API
- Snap execution statistics retrieval
- Performance metrics per Snap

### SnapGPT Audit Log API
- Retrieve SnapGPT usage events (audit logging), up to 45 days of history, accessible via the Public API (admin opt-in for sensitive-data handling). Added in the May 2026 release.

### User and Group APIs
- Account management (create/update/delete users)
- Group management (create/update/delete groups)
- Role assignment and permissions

## Rate Limits

Public Management API call limits are not published with a single fixed number; SnapLogic applies per-Org rate limiting and you contact your CSM/Support to raise them. Use of the Public APIs does **not** count against the environment limit for calling pipelines via the Cloud URL.

For **triggered task (Cloud URL) execution** there are two documented limits:
- **Concurrent API limit**: total triggered pipelines that can run concurrently — default **10**.
- **Daily API limit**: total triggered pipelines per day — resets at midnight UTC.
- Exceeding either returns **HTTP 429 (Rate limit exceeded)**. Contact your SnapLogic CSM to raise the limits.

The API Policy Manager **Client Throttling** policy caps calls at a maximum of **1000 per minute** when enabled.

## Response Format

All APIs return JSON responses over HTTPS.

## SDK and Tools

- **SnapLogic Public APIs**: REST APIs for programmatic management of the platform
- **Snap Developer Kit**: Java-based SDK for building custom Snaps (connector development)
- **GitHub**: https://github.com/SnapLogic — includes developer docs, demo Snap Packs, agent examples
- **Pipeline Linker**: Chrome extension for copying pipeline links (GitHub: SnapLogic/pipeline-linker)
