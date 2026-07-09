<!-- Source: https://developers.dialpad.com/docs/welcome -->
<!-- OpenAPI spec: https://dialpad.com/static/openapi/platform-v1.0.json -->
<!-- Python SDK: https://github.com/dialpad/dialpad-python-sdk -->

# Dialpad API Reference

## Overview

Dialpad APIs unlock the platform's capabilities for building custom integrations. Documentation is at developers.dialpad.com.

## Base URL

- **Production**: `https://dialpad.com/api/v2/`
- **Sandbox**: `https://sandbox.dialpad.com/api/v2/`

(Verified 2026-06-13 against developers.dialpad.com/docs/authentication-basics.)

## Authentication

Two methods:
1. **Manual API Key**: Generate in Admin Settings > My Company > Authentication > API Keys (Add Key → name + expiration + scopes → Save). For internal/single-company use.
2. **OAuth 2.0**: For multi-tenant apps where users across different companies connect Dialpad. Request OAuth access through the developer portal.

**Passing the token:**
- **Recommended**: bearer token in the header — `Authorization: Bearer {token}`.
- **Discouraged**: query parameter — `apikey=<token>` (exposes the key in logs).

## OpenAPI Specification

Download the full API collection for Postman/tooling:
- **Primary**: `https://dialpad.com/static/openapi/platform-v1.0.json`
- **Analytics**: `analytics-api.json` (Beta)
- **Reseller**: `platform-reseller-api.json`
- **Service Titan**: `platform-service-titan-api.json`

## Python SDK

PyPI package name is **`python-dialpad`** (the import name is `dialpad`):

```bash
pip install python-dialpad
# or: uv add python-dialpad
```

GitHub: github.com/dialpad/dialpad-python-sdk (latest 3.x as of 2026-06)

```python
from dialpad import DialpadClient

# token is the required arg (not api_key); set sandbox=True to hit sandbox.dialpad.com
client = DialpadClient(token="your_api_token")

# Async client also available:
# from dialpad import AsyncDialpadClient

# List contacts (paginated — use limit to avoid cursor corruption, see issue #13)
contacts = client.contacts.list(limit=100)

# Get call stats
# Note: Stats API is async — POST to start, GET to retrieve
```

**Known SDK issues (from GitHub):**
- #27: AI Recap endpoint not yet available in SDK (feature request)
- #26: No function to get SMS Opt Out List from Company resource
- #25: Installation fails on Windows (encoding issue)
- #13: Corrupt cursor in contacts list — add `limit` parameter to workaround

## API Categories

### Stats APIs
Async report generation for analytics data.

**Pattern**: POST to initiate → wait 15-20 seconds → GET to retrieve CSV.

**Export types:**
- `stats`: Aggregated data (call counts by status, averages)
- `records`: Individual call records with per-row detail

**Targeting parameters:**
- `office_id`: Filter by office
- `target_id`: Filter by call center or department (overrides office_id)

**Time parameters:**
- `is_today=true`: Real-time tables, refreshed every 30 minutes
- `days_ago`: Historical tables, updated every 4-5 hours
- `is_today` overrides `days_ago` when both specified
- Minimum `days_ago` value: 0

**Timezone**: Must use IANA "tz database name" entries (e.g., `America/New_York`).

**Caching:**
- `is_today=true`: Cached 30 minutes
- `days_ago`: Cached 3 hours
- Identical POST requests reuse cached results

**Best practices:**
- Wait 15-20s after POST before hitting GET
- Retry failed requests every 5-10 seconds (not every second)
- Don't send repeated identical POST requests
- Processing time varies by data volume

### SMS API
Send and receive SMS/MMS messages. A2P (Application-to-Person) compliance required.

### Digital Engagement API
Manage chat and messaging channel interactions.

### AI Virtual Agent API
Configure and manage autonomous AI agents for customer resolution.

### Event Subscriptions (Webhooks)
Real-time webhooks. Build an HTTP service on the public internet, then create an event subscription via the API (`developers.dialpad.com/reference/subscriptions`). Available event categories:
- **Call events** (start, end, transfer)
- **SMS events**
- **Contact events**
- **Agent status events**
- **Change log events** (with change-log action types)

**Signing / verification (verified 2026-06-13):**
- For security, events are sent in **JWT format** and signed with a **shared secret** you supply when creating the subscription.
- The secret is **different from your API key** — generate a unique secure string (recommended: unique per subscription).
- If a secret is provided, events are signed using the **HS256** algorithm; decode the JWT payload and verify the signature to confirm the event came from Dialpad.
- If **no secret** is provided, unencoded events are sent as plain **JSON** (not recommended — you can't verify authenticity).

**Subscription limits:**
- 100 subscriptions per type (across all targets under a Company).
- 10 subscriptions per type when targeting the Company itself.

### WFM APIs
Workforce management schedule data available via Surfboard integration.

## Rate Limits

Published at developers.dialpad.com/docs/rate-limits (verified 2026-06-13):

- **Global**: 20 requests/second per company.
- **Per-endpoint**:
  - Create contacts: 100/min
  - Initiate calls: 5/min per user target
  - Send SMS: 100/min
  - Callback requests to a specific number: 5/min
  - Callback requests to a specific call center: 100/min
  - Callback requests to a specific company: 1000/min
  - Update callrouter configuration: 1 per 5 min

Dialpad reserves the right to change these limits.

General guidance:
- Watch for HTTP 429 responses; implement exponential backoff on retries.
- Don't send identical requests in rapid succession.
- Stats API has built-in deduplication (identical POST requests return cached results).

## HTTP Status Codes

Standard REST status codes. 429 for rate limiting. Check developers.dialpad.com/docs for the full reference.
