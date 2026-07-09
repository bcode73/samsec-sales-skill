# ZeroBounce API Reference

## Overview

ZeroBounce is an email validation and deliverability platform. The API provides single and bulk email validation, email activity data, credit management, and usage reporting.

**SDKs**: Python, Java, JavaScript, PHP, C#, Ruby, Go, Delphi, C, C++, iOS, Android, Rust (13 official SDKs).

**Sandbox mode**: Available for testing without consuming credits.

## Base URLs

| Environment | URL |
|---|---|
| Default | `https://api.zerobounce.net/v2/` |
| USA | `https://api-us.zerobounce.net/v2/` |
| EU | `https://api-eu.zerobounce.net/v2/` |
| Bulk | `https://bulkapi.zerobounce.net/v2/` |

Use the Bulk URL for file-based bulk validation endpoints (`sendfile`, `filestatus`, `getfile`, `deletefile`). All other endpoints use the default, USA, or EU URLs.

## Authentication

All requests authenticate via the `api_key` query parameter.

```
GET /v2/validate?api_key=YOUR_API_KEY&email=user@example.com
```

Invalid API keys / out-of-credits on the **validate** endpoint return:

```json
{"error": "Invalid API Key or your account ran out of credits"}
```

The **getcredits** endpoint instead returns `{"Credits": "-1"}` (a `-1` Credits value) when the key is invalid.

## Rate Limits

Per the official validate-endpoint docs (re-verified 2026-06-13), the validation endpoints are throttled by a short burst window, not a per-hour cap:

| Limit | Threshold | Consequence |
|---|---|---|
| Validation requests | 80,000 requests in 10 seconds (100,000 for ZeroBounce ONE™ customers) | 1-minute temporary block |
| Bad API key requests | 200 requests in 1 hour | 1-hour block |

---

## Endpoints

### Email Validation

#### Single Email Validation

```
GET /v2/validate
```

Validates a single email address and returns detailed results.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `email` | string | Yes | Email address to validate |
| `ip_address` | string | No | IP address of the email owner (improves accuracy; can be blank or omitted) |
| `timeout` | integer | No | Timeout in seconds (3-60); returns unknown/greylisted if exceeded |
| `activity_data` | boolean | No | Appends Activity Data (`active_in_days`) to results |
| `verify_plus` | boolean | No | Enables the Verify+ enhanced validation method |

> **Re-verified 2026-06-13**: the official v2 validate doc lists exactly these six parameters (`email`, `api_key`, `ip_address`, `timeout`, `activity_data`, `verify_plus`). Greylist retry processing (`greylist_processing` / `callback_url`) is handled by the **separate Greylist API**, not as parameters on `/v2/validate` — see the Greylist section below. `domain_info` was not confirmed on the current validate doc; treat it as unverified.

**Example request**:

```
GET /v2/validate?api_key=YOUR_KEY&email=user@example.com&ip_address=127.0.0.1
```

**Example response**:

```json
{
  "address": "user@example.com",
  "status": "valid",
  "sub_status": "",
  "free_email": false,
  "did_you_mean": "",
  "account": "user",
  "domain": "example.com",
  "domain_age_days": "3650",
  "active_in_days": "60",
  "catchall_domain": "false",
  "smtp_provider": "example",
  "mx_found": "true",
  "mx_record": "mx.example.com",
  "firstname": "John",
  "lastname": "Doe",
  "gender": "male",
  "country": "US",
  "region": "California",
  "city": "Los Angeles",
  "zipcode": "90001",
  "processed_at": "2026-03-30 12:00:00.000",
  "domain_website_exists": true,
  "domain_registrant_company_name": "Example Inc"
}
```

**Status values**:

| Status | Meaning |
|---|---|
| `valid` | Email is valid and deliverable |
| `invalid` | Email is not deliverable |
| `catch-all` | Domain accepts all emails (delivery uncertain) |
| `unknown` | Could not determine validity |
| `spamtrap` | Known spam trap address |
| `abuse` | Known abuse/complaint address |
| `do_not_mail` | Should not be mailed (disposable, role-based, etc.) |

#### Batch Email Validation

```
POST /v2/validatebatch
```

Validates up to 200 emails in a single request.

**Parameters** (JSON body):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `email_batch` | array | Yes | Array of email objects (max 200) |
| `timeout` | integer | No | Timeout in seconds (10-120) |
| `activity_data` | boolean | No | Include activity data |
| `verify_plus` | boolean | No | Enable enhanced verification |

Each item in `email_batch`:

| Field | Type | Required | Description |
|---|---|---|---|
| `email_address` | string | Yes | Email to validate |
| `ip_address` | string | No | IP address of the email owner |

**Example request**:

```json
{
  "api_key": "YOUR_KEY",
  "email_batch": [
    {"email_address": "user1@example.com", "ip_address": ""},
    {"email_address": "user2@example.com", "ip_address": ""}
  ]
}
```

**Response**: Array of validation results, same structure as single validation.

---

### Bulk File Processing

All bulk endpoints use the **Bulk URL**: `https://bulkapi.zerobounce.net/v2/`

#### Upload File for Bulk Validation

```
POST /v2/sendfile
```

Upload a CSV or TXT file for asynchronous bulk validation.

**Parameters** (multipart form):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | file | Yes | CSV or TXT file to validate |
| `api_key` | string | Yes | Your API key |
| `email_address_column` | integer | Yes | Column index containing emails (1-indexed) |
| `first_name_column` | integer | No | Column index for first names |
| `last_name_column` | integer | No | Column index for last names |
| `gender_column` | integer | No | Column index for gender |
| `ip_address_column` | integer | No | Column index for IP addresses |
| `has_header_row` | boolean | No | Whether the file has a header row |

**Example response**:

```json
{
  "success": true,
  "message": "File accepted",
  "file_name": "contacts.csv",
  "file_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
}
```

#### Check File Processing Status

```
GET /v2/filestatus
```

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `file_id` | string | Yes | File ID from `sendfile` response |

**Example response**:

```json
{
  "success": true,
  "file_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  "file_name": "contacts.csv",
  "file_status": "Complete",
  "complete_percentage": "100%",
  "return_url": null
}
```

#### Download Validated Results

```
GET /v2/getfile
```

Downloads the validated results file once processing is complete.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `file_id` | string | Yes | File ID from `sendfile` response |

**Response**: CSV file download.

#### Delete Processed File

```
GET /v2/deletefile
```

Removes a processed file from ZeroBounce servers.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `file_id` | string | Yes | File ID to delete |

**Example response**:

```json
{
  "success": true,
  "message": "File deleted",
  "file_name": "contacts.csv",
  "file_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
}
```

---

### Account & Usage

#### Get Remaining Credits

```
GET /v2/getcredits
```

Returns the number of validation credits remaining on the account.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |

**Example response**:

```json
{
  "Credits": "50000"
}
```

**Note**: An invalid API key returns `{"Credits": "-1"}`. Validation/credit endpoints are throttled at 80,000 requests per 10 seconds (100,000 for ZeroBounce ONE™), with a 1-minute temporary block on exceeding the burst window.

#### Get API Usage Statistics

```
GET /v2/getusage
```

Returns API usage statistics for a date range.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `start_date` | string | Yes | Start date (YYYY-MM-DD) |
| `end_date` | string | Yes | End date (YYYY-MM-DD) |

**Example request**:

```
GET /v2/getusage?api_key=YOUR_KEY&start_date=2026-01-01&end_date=2026-03-30
```

---

### Email Activity

#### Get Email Activity Data

```
GET /v2/activity
```

Returns engagement/activity data for an email address.

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `email` | string | Yes | Email address to check |

**Response includes activity status within these windows**:

- Active in last 30 days
- Active in last 60 days
- Active in last 90 days
- Active in last 180 days
- Active in last 365 days
- Active 365+ days ago

---

### Additional APIs

#### Email Finder API (Guess Format)

```
GET /v2/guessformat
```

Finds the most likely email address for a person at a company, or returns the email format for a domain. Default/US/EU hosts apply (`api.zerobounce.net`, `api-us.zerobounce.net`, `api-eu.zerobounce.net`).

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `api_key` | string | Yes | Your API key |
| `domain` | string | Yes* | Email domain to search (e.g. `example.com`) |
| `company_name` | string | Yes* | Company name to search (alternative to `domain`) |
| `first_name` | string | No | Person's first name |
| `middle_name` | string | No | Person's middle name |
| `last_name` | string | No | Person's last name |

\* Either `domain` or `company_name` is required.

**Response fields**: `email`, `email_confidence` (HIGH / MEDIUM / LOW), `domain`, `company_name`, `did_you_mean`, `failure_reason`.

**Credit cost**: a successful find consumes 1 subscription query or 20 credits. Undetermined responses cost 0.

#### Domain Search API (bulk)

Finds email addresses / formats across a list of domains in bulk. Uses the **Bulk host** with a dedicated path prefix:

| Endpoint | Method | Path |
|---|---|---|
| Submit file | POST | `https://bulkapi.zerobounce.net/domain-search/sendfile` |
| Check status | GET | `https://bulkapi.zerobounce.net/domain-search/filestatus` |
| Download results | GET | `https://bulkapi.zerobounce.net/domain-search/getfile` |

**Credit cost**: 20 credits per successful result on Pay-As-You-Go/credits, or 1 query with an active Email Deliverability Toolkit subscription. No restriction on file size, email count, or number of files.

#### A.I. Scoring API

Scores email-address quality on a **0–10** scale (0/1 = lowest quality, 10 = high probability of interaction). Primary workflow is **bulk CSV file processing**; a single-email real-time scoring endpoint also exists.

Bulk endpoints use the **Bulk host**:

| Endpoint | Method | Path |
|---|---|---|
| Submit file | POST | `https://bulkapi.zerobounce.net/v2/scoring/sendFile` |
| File status | GET | `https://bulkapi.zerobounce.net/v2/scoring/filestatus` |
| Get file | GET | `https://bulkapi.zerobounce.net/v2/scoring/getFile` |
| Delete file | GET | `https://bulkapi.zerobounce.net/v2/scoring/deletefile` |

Get File supports download-type options **PHASE_1**, **PHASE_2**, and **COMBINED**. The returned CSV adds a Quality Score column (0–10).

> Path casing/segments for the scoring endpoints follow the SDK conventions; confirm against the live A.I. Scoring API docs and the official wrappers before hard-coding.

#### List Evaluator API

Free email-list health assessment. Evaluates an uploaded list and provides aggregate quality metrics without consuming validation credits.

**Gap**: Exact endpoint path, upload format requirements, and response schema not confirmed on current docs — treat as unverified.

#### MCP Server (official)

ZeroBounce publishes an official Model Context Protocol server (`@zerobounce/mcp`, GitHub `zerobounce/zerobounce-mcp`) that exposes validation (single + batch), credit/usage checks, bulk file ops (validation + AI scoring), Email Finder, Domain Search, Activity Data, and AI Scoring as MCP tools for Claude/Cursor/VS Code. Install: `npm install -g @zerobounce/mcp`; configure the MCP client with `command: zerobounce-mcp` and `--api-key=YOUR_API_KEY`.

---

## Webhooks (Greylist API)

ZeroBounce supports callback webhooks for **greylist retry processing**, exposed via the separate **Greylist API** (not as parameters on `/v2/validate`).

**How it works**:

1. Submit an email to the Greylist API with a `callback_url=https://your-server.com/webhook`.
2. Greylisting causes mail servers to temporarily defer; ZeroBounce retries validation over time and posts the final result to the callback URL when complete.
3. Your server should respond with HTTP `200`/`201` to confirm delivery.

**Webhook payload**: validation-result structure, equivalent to the `/v2/validate` response.

> **Re-verified 2026-06-13**: greylist processing is documented as its own API/endpoint family, distinct from the standard validate call. No HMAC/signing scheme is documented for the callback — treat the callback as unauthenticated and validate by other means (e.g. a secret path or allowlist).

---

## Error Handling

**Authentication errors**:

- Validate endpoint: `{"error": "Invalid API Key or your account ran out of credits"}`
- `getcredits` endpoint: `{"Credits": "-1"}`

Returned when the API key is invalid (or credits are exhausted on validate). Exceeding 200 bad API key requests in 1 hour triggers a 1-hour block.

**Rate limit errors**: Exceeding 80,000 validation requests in 10 seconds (100,000 for ZeroBounce ONE™) triggers a 1-minute temporary block. Monitor usage to avoid interruptions.

**General error pattern**: Responses include a `success` field (boolean) and `message` field with details on failure for bulk endpoints.

---

## Pagination

The ZeroBounce API does not use cursor or offset-based pagination. Single validation returns one result, batch validation returns up to 200 results, and bulk file processing handles large lists asynchronously via file upload/download.
