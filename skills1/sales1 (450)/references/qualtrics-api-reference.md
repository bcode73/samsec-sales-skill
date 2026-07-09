<!-- Source: https://www.qualtrics.com/support/integrations/api-integration/overview/ and https://api.qualtrics.com/ -->
<!-- Note: The full API reference at api.qualtrics.com is JS-rendered and couldn't be fetched in full. This reference is compiled from support documentation and Postman collections. Refresh from https://api.qualtrics.com/ for complete endpoint details. -->

# Qualtrics API Reference

## Authentication

### API Token (simpler)
- Header: `X-API-TOKEN: {your-token}`
- Generated in: Account Settings → Qualtrics IDs → Generate Token
- **Single-use generation**: Regenerating invalidates the previous token and breaks existing integrations
- Each user must generate their own token
- Requires "Access API" permission on the account

### OAuth 2.0 (recommended for production)
Qualtrics supports **two OAuth 2.0 grant types** for the public APIs (verified 2026-06-13):
- **Client Credentials** — for backend automations; makes calls as the user account that created the credentials. Set this up in: Account Settings → Qualtrics IDs → OAuth Client Manager → Create Client → Grant Type "Client Credentials".
- **Authorization Code (AuthCode)** — for apps acting on behalf of a signed-in user.
- **Client Secret is shown only once** — irretrievable after closing the dialog. Store the Client ID and Client Secret immediately.
- Returns a Bearer token for API requests.

## Base URL

```
https://{datacenterid}.qualtrics.com/API/v3/
```

Common datacenter IDs: `iad1` (US East), `sjc1` (US West), `ca1` (Canada), `eu` (Europe), `gov1` (FedRAMP)

Find yours in: Account Settings → Qualtrics IDs

## API Categories

### Survey Management
- `GET /surveys` — List all surveys
- `GET /surveys/{surveyId}` — Get survey details
- `POST /surveys` — Create a survey
- `PUT /surveys/{surveyId}` — Update survey metadata
- `DELETE /surveys/{surveyId}` — Delete a survey

### Response Export (3-step async)
1. `POST /surveys/{surveyId}/export-responses` — Start export (returns `progressId`)
   - Body: `{"format": "csv"}` (or `json`, `tsv`, `spss`, `xml`)
   - Optional filters: `startDate`, `endDate`, `limit`, `useLabels`
2. `GET /surveys/{surveyId}/export-responses/{exportProgressId}` — Check progress
   - Returns `percentComplete` and `fileId` when done
3. `GET /surveys/{surveyId}/export-responses/{fileId}/file` — Download file (ZIP)
   - **Important**: Use correct datacenter in URL or download fails

### Distribution
- `POST /distributions` — Create a distribution (email, SMS, or link)
- `GET /distributions?surveyId={id}` — List distributions for a survey
- `POST /distributions/{distributionId}/links` — Generate individual survey links
- Default link expiration: 60 days if unspecified

### Contact Management (XM Directory)
- `POST /directories/{directoryId}/contacts` — Create a contact
- `GET /directories/{directoryId}/contacts` — List directory contacts
- `PUT /directories/{directoryId}/contacts/{contactId}` — Update a contact
- `DELETE /directories/{directoryId}/contacts/{contactId}` — Delete a contact
- `POST /directories/{directoryId}/mailinglists/{mailingListId}/contacts` — Add contact to mailing list

### Contact Import (Bulk)
- `POST /directories/{directoryId}/contacts/import` — Bulk import contacts (JSON array)
- `GET /directories/{directoryId}/contacts/import/{importId}` — Check import status

### Mailing Lists
- `POST /directories/{directoryId}/mailinglists` — Create a mailing list
- `GET /directories/{directoryId}/mailinglists` — List mailing lists
- `GET /directories/{directoryId}/mailinglists/{mailingListId}/contacts` — List contacts in a mailing list

### Webhooks / Event Subscriptions
- Subscribe to events like `surveyengine.completedResponse`
- **Known issue** (Sept 2025): Webhook `Status` field changed from `Complete` to `Full` without notice, breaking ~70-80% of downstream handlers. Always handle both values.

### Users & Groups
- `GET /users` — List users
- `POST /users` — Create a user
- `GET /groups` — List groups
- `POST /groups` — Create a group

## Request Format

- Content-Type: `application/json` (most endpoints) or `multipart/form-data` (file uploads)
- All IDs follow patterns: surveys `SV_xxxxx`, distributions `EMD_xxxxx`, mailing lists `ML_xxxxx`, directories `POOL_xxxxx`

## Rate Limits

Documented in the public API docs (verified 2026-06-13):
- **Brand-level default: up to 3000 API requests per minute**, enforced across all users in the brand/organization.
- When the limit is exceeded the API returns **HTTP 400 with error value `rate_limit_reached`** (note: not 429). Implement backoff and retry on this error.
- **Per-user limits** (released Feb 5, 2025): Brand Admins can cap how many requests an individual user may call per minute. By default there is no per-user cap, only the brand-level limit.
- Rate-limit increases are not granted by default — Qualtrics recommends optimizing/throttling requests instead.
- High-volume operations (bulk imports, response exports) should use the batch/async endpoints.

## SDKs & Developer Tools

### Official SDKs
- **iOS SDK**: `qualtrics-experience-ios` (Swift Package Manager)
- **Android SDK**: Available via Maven
- **React Native**: Sample apps at `github.com/qualtrics/QualtricsSDKReactNativeSampleApps`
- **DXA iOS SDK**: `qualtrics-dxa-ios` for digital experience analytics

### MCP (Model Context Protocol)
- Qualtrics provides MCP servers for AI application integration
- Enables AI tools to access Qualtrics APIs programmatically
- Supports "every JSON-based API" currently available

### Developer Portal
- URL: `https://developer.qualtrics.com/`
- Build custom integrations and apps using APIs or Extension SDK
- Sample apps: `github.com/qualtrics/Qualtrics-Developer-Platform-Sample-Apps`

### Postman Collection
- Public workspace: `postman.com/qualtrics-public-apis/qualtrics-public-workspace`
- Includes all public API endpoints with examples

## Common Patterns

### Web Service in Survey Flow
Execute API calls directly within a survey:
1. Add Web Service element to Survey Flow
2. Specify HTTP method, URL, headers (`X-API-TOKEN`)
3. Use Piped Text for dynamic values from responses
4. **Gotcha**: Works in Test mode but may fail in Preview/Live due to CORS. Move complex API calls server-side.

### Embedded Data
Pass data into surveys via URL parameters or API:
- URL: `?Q_EED_name=value`
- API: Include in distribution creation payload
- Access in survey via `${e://Field/name}` piped text

### Automating Recurring Exports
1. Schedule a cron job or cloud function
2. POST to create export with date range filter
3. Poll for completion (typically 30 seconds to a few minutes)
4. Download and load into data warehouse
5. Store last export timestamp for incremental pulls
