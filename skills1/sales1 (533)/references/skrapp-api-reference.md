### Skrapp.io APIs — Comprehensive Reference (API v2 / verifier v3)

Skrapp.io provides a REST API for email finding, email verification, bulk operations, account/credit data, and lead list management.

> **Verified 2026-06-13** against the official API reference at https://skrapp.io/api. Endpoint paths, HTTP methods, auth scheme, parameters, bulk caps, and response field names below match the current published docs.

> **Access**: API features are only available to paid accounts. Per the Skrapp pricing page, "API Integration" is listed as an Enterprise-plan feature — the Professional plan does not include API access. (The API docs phrase this generically as "paid accounts"; the pricing page is the authoritative gate.)

---

## Base URL

```
https://api.skrapp.io
```

All endpoints are HTTPS-secured — plain HTTP requests are rejected. Note the versioned paths differ by service: the finder/account/list endpoints live under `/api/v2/...`, while the verifier endpoints live under `/v3/...` (no `/api/` segment).

---

### Authentication

Authentication uses HTTP Basic Auth: the per-account API Access Key is passed via the `X-Access-Key` HTTP request header on every request. Find/manage your key in the Skrapp dashboard under Settings -> Integrations.

```bash
curl "https://api.skrapp.io/api/v2/account" \
  -H "X-Access-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

---

### Rate Limits

> **GAP**: Rate limits are not published in the official API docs. The docs state responses "follow standard HTTP response codes for success or failure." Monitor usage through your Skrapp account dashboard and contact Skrapp support for rate-limit details.

---

### Response Format

All responses return JSON.

```json
{
  "...": "endpoint-specific data"
}
```

> **GAP**: The exact response envelope structure (status fields, error wrapping) is not fully documented. Inspect live responses for the current format.

---

### Error Handling

> **GAP**: Error codes and error response format are not publicly documented. Expect standard HTTP status codes:

| Status | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request — invalid or missing parameters |
| 401 | Unauthorized — invalid or missing API key |
| 403 | Forbidden — plan does not include API access |
| 404 | Not found |
| 429 | Rate limited (assumed) |
| 500 | Internal server error |

---

### Pagination

The List Leads endpoint (`GET /api/v2/list/:listId/leads`) uses cursor pagination: pass `start` and `size` (default 25, max 500) as query parameters; the response returns `count_results` and a `next_start` cursor to fetch the following page.

> Other endpoints (find/verify/bulk) are not paginated; the bulk endpoints instead cap the per-request batch (100 for find_bulk, 50 for verify_bulk).

---

### Endpoints

---

#### 1. Email Finder

Find the most likely email address for a person at a given company domain.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/find` | Find a person's email from their name + company/domain |

**`GET /api/v2/find` query parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `firstName` | string | conditional | First name (pair with `lastName`) |
| `lastName` | string | conditional | Last name (pair with `firstName`) |
| `fullName` | string | conditional | Full name (alternative to `firstName`+`lastName`) |
| `company` | string | conditional | Company name (provide `company` or `domain`) |
| `domain` | string | conditional | Company domain, e.g. `example.com` (provide `company` or `domain`) |
| `country` | string | No | Country hint to improve matching |
| `includeCompanyData` | boolean | No | Include company firmographics in the response |

**Rules**: provide either `firstName`+`lastName` OR `fullName`; AND provide either `company` OR `domain`.

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `email` | string | Most likely email address |
| `pattern` | string | Detected email pattern for the domain |
| `quality` | object | Verification quality object |
| `quality.status` | string | Email status (e.g. `valid`, `catch-all`) |
| `quality.status_message` | string | Human-readable status message |

---

#### 2. Email Verifier

Verify whether an email address is valid and deliverable.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/verify` | Verify a single email address |

> Note: the verifier lives on the **v3** path with **no `/api/` segment** — `https://api.skrapp.io/v3/verify`.

**`GET /v3/verify` query parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to verify |
| `enrich` | boolean | No | Return additional enrichment data |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `email` | string | The verified email address |
| `domain` | string | Email domain |
| `email_status` | string | Overall status (`valid`, `catch-all`, `invalid`, ...) |
| `message` | string | Status message |
| `format` | string | Format check result (e.g. `valid`) |
| `mailbox_status` | string | Mailbox-level status |
| `mailbox_type` | string | Mailbox type (`professional`, `webmail`, `temporary`/disposable) |
| `mailbox_exchange` | string | Mail exchange (MX) server |

---

#### 3. Bulk Email Finder

Find email addresses for multiple people in a single request.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v2/find_bulk` | Bulk email finding (JSON array payload) |

**Limit**: max **100** entries per request. Each entry accepts:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tId` | string | No | Caller-supplied tracking ID, echoed back in the response |
| `firstName` | string | conditional | First name (pair with `lastName`) |
| `lastName` | string | conditional | Last name (pair with `firstName`) |
| `name` | string | conditional | Full name (alternative to `firstName`+`lastName`) |
| `company` | string | conditional | Company name (provide `company` or `domain`) |
| `domain` | string | conditional | Company domain (provide `company` or `domain`) |
| `country` | string | No | Country hint |

**Response**: array of objects with `tId`, `firstName`, `lastName`, `name`, `company`, `domain`, `email`, and `quality`.

---

#### 4. Bulk Email Verifier

Verify multiple email addresses in a single request.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v3/verify_bulk` | Bulk email verification |

**Limit**: max **50** emails per request, passed as an `email` array query parameter. **Response**: array of verification objects with the same fields as the single `/v3/verify` endpoint.

---

#### 5. Account Data

Retrieve account information including the credit balance.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/account` | Retrieve account details and credit quota |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `package` | string | Current plan name |
| `packageRDate` | timestamp | Plan renewal date |
| `credit` | object | Credit object, e.g. `{ "quota": 10000, "used": 4991 }` (email quota and used) |
| `lists` | array | Array of the account's saved lists |

---

#### 6. List Data

Retrieve metadata about a saved lead list.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/list/:listId` | Get list metadata by list ID |

**Path parameter**: `listId` (required, in the URL path).

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `list_id` | string | List identifier |
| `name` | string | List name |
| `creation_date` | string | List creation date |
| `count_leads` | int | Number of leads in the list |

---

#### 7. List Leads

Access lead details from a specific list.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/list/:listId/leads` | Get leads from a list |

**Query parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `start` | int | No | Pagination cursor (default: most recent) |
| `size` | int | No | Page size (default 25, max 500) |
| `kw` | string | No | Keyword text filter |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `count_results` | int | Total matching leads |
| `next_start` | int | Cursor for the next page |
| `data` | array | Lead objects with `id`, `name`, `first_n`, `last_n`, `email`, `email_status`, `linkedin_url`, `location`, `domain`, and `company` fields |

---

### Webhook Support

> **GAP**: Webhook support is not documented. Check official docs for updates on webhook or callback support.

---

## Quick Reference — Common Workflows

### Find an email address by name and domain
```bash
curl "https://api.skrapp.io/api/v2/find?firstName=John&lastName=Doe&domain=example.com" \
  -H "X-Access-Key: YOUR_API_KEY"
```

**Response** (200 OK):
```json
{
  "email": "john.doe@example.com",
  "pattern": "{first}.{last}",
  "quality": {
    "status": "valid",
    "status_message": "Verified deliverable"
  }
}
```

### Verify an email address
```bash
curl "https://api.skrapp.io/v3/verify?email=john.doe@example.com" \
  -H "X-Access-Key: YOUR_API_KEY"
```

**Response** (200 OK):
```json
{
  "email": "john.doe@example.com",
  "domain": "example.com",
  "email_status": "valid",
  "message": "Deliverable",
  "format": "valid",
  "mailbox_status": "valid",
  "mailbox_type": "professional",
  "mailbox_exchange": "aspmx.l.google.com"
}
```

### Check account credit balance
```bash
curl "https://api.skrapp.io/api/v2/account" \
  -H "X-Access-Key: YOUR_API_KEY"
```

**Response** (200 OK):
```json
{
  "package": "Enterprise",
  "packageRDate": 1750000000,
  "credit": { "quota": 50000, "used": 4991 },
  "lists": []
}
```

---

## Summary of Documentation Gaps

| Area | Status |
|---|---|
| Endpoint paths / methods / params | **Verified 2026-06-13** against https://skrapp.io/api |
| Bulk caps (find_bulk 100, verify_bulk 50) | Verified |
| Account / list / list-leads endpoints | Verified (`/api/v2/account`, `/api/v2/list/:listId`, `/api/v2/list/:listId/leads`) |
| Pagination (List Leads) | Verified — `start`/`size`/`next_start` cursor |
| Rate limits | Not documented in official API reference |
| Error codes / error response format | Not enumerated — docs say "standard HTTP response codes" |
| Webhooks | Not documented / no webhook support shown |
| Response field names | Verified against the published API reference |

> **Note**: The earlier `GET /api/companyInfo` company-enrichment endpoint is not present in the current v2 API reference. Company firmographics are instead returned inline via the Email Finder's `includeCompanyData=true` parameter. The standalone company endpoint is unverified in current docs — treat as removed/unconfirmed.
