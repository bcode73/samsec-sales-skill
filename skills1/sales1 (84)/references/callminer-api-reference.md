<!-- Source: https://developer.callminer.com/docs (JS-rendered — partial info only) -->
<!-- Additional source: https://apitracker.io/a/callminer -->
<!-- Additional source: https://www.macrosoftinc.com/callminer/api/ -->
<!-- Re-verified 2026-06-13: OAuth 2.0 client-credentials auth + /api/v2/audiosources Data API route confirmed via boost.ai integration docs (https://boost.elevio.help/en/articles/620-callminer) and Macrosoft (certified CallMiner partner) Data/Ingestion API pages. -->

# CallMiner API Reference

> **Note**: CallMiner's developer documentation at developer.callminer.com is JS-rendered and could not be fully fetched. This reference is compiled from available sources. For complete endpoint documentation, access the developer portal directly or request Swagger UI / OpenAPI spec access from CallMiner.

## Overview

CallMiner's platform is entirely API-driven — every use case in the system can be achieved by calling one or a set of APIs. The API is split into two collections.

## API collections

### 1. Data APIs (export)
Export data out of CallMiner for reporting, analytics, or integration with external systems. Versioned under `/api/v2/`.

**Capabilities**:
- Export interaction scores and metadata
- Export category match results
- Export agent performance data
- Export scorecard results
- Export trend and aggregate analytics

**Known endpoint**:
- `GET /api/v2/audiosources` — list the available audio sources configured for the account. (Equivalent to viewing sources under Analyze → Admin → Initial System Configuration in the UI.) This is the documented example of a `/api/v2` Data API route.

### 2. Ingestion APIs (import)
Import data into CallMiner for analysis.

**Capabilities**:
- Ingest audio recordings (WAV, MP3, and other formats)
- Ingest text-based interactions (chat transcripts, emails, social media)
- Ingest metadata associated with interactions (agent ID, customer ID, call reason, queue, etc.)
- Bulk ingestion for batch processing

## Authentication

CallMiner uses **OAuth 2.0** (not a static API key). The documented flow is the **client-credentials grant**:

- **Token endpoint**: `POST {Identity Provider Service URL}/connect/token`
  - Header: `Content-Type: application/x-www-form-urlencoded`
  - Body params: `grant_type=client_credentials`, `client_id=...`, `client_secret=...`, `scope=...`
- **Scope**: `https://callminer.net/auth/platform-ingestion` (ingestion scope)
- **Credentials**: `client_id` and `client_secret` are provisioned by CallMiner and delivered by email from `support@callminer.com`. The Identity Provider Service URL is provided with them.
- **Usage**: exchange the credentials for a bearer access token at the token endpoint, then send `Authorization: Bearer {access_token}` on Data/Ingestion API calls.
- **Registration / developer access**: the CallMiner Partner Portal (`partner.callminer.com`) is still the path to request developer access; credentials then arrive by email.

> Older versions of this reference described "API key authentication." That is superseded — current docs use OAuth 2.0 client-credentials with the token endpoint and ingestion scope above.

## Developer resources

- **Developer portal**: https://developer.callminer.com/docs — documentation, code samples, support forum
- **Swagger UI**: Available after authentication — full endpoint documentation with request/response schemas
- **Sandbox environment**: Dedicated testing environment available for developers to test API calls without affecting production data
- **Support forum**: Developer community for connecting with CallMiner's API team

## Integration patterns

### Audio ingestion workflow
1. Obtain `client_id`/`client_secret` (emailed from `support@callminer.com`) and exchange them at the token endpoint (`POST {Identity Provider Service URL}/connect/token`, `grant_type=client_credentials`, scope `https://callminer.net/auth/platform-ingestion`) for a bearer access token
2. Upload audio file to your account's Media Ingestion API URL with the bearer token and metadata (agent ID, customer ID, timestamp, queue)
3. CallMiner processes the audio through the configured transcription engine (OVTS)
4. Analytics (categories, scoring, sentiment) are applied automatically
5. Results available via Data API or in the Analyze UI

### Real-time alerting
- CallMiner's Real-time API supports alerting and next-best-action guidance during live interactions
- Alerts are pushed when configured categories match during a live call

### CRM integration
- Two-way data import/export with Salesforce, Zendesk, Oracle CX
- Interaction insights can be pushed to CRM records
- CRM data can be pulled into CallMiner for context enrichment

## Known limitations

- API documentation is not publicly browsable without authentication
- Rate limits are not publicly documented — contact CallMiner for specifics
- SDK availability is unconfirmed — API appears to be REST-only with no official client libraries
- Webhook support is mentioned but details require developer portal access
