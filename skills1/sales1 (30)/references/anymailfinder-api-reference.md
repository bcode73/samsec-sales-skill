### Anymail Finder APIs — Comprehensive Reference

Anymail Finder provides a REST API for finding verified professional email addresses by person name, company domain, decision-maker role, or LinkedIn URL, plus email verification and bulk search capabilities.

> **Note**: Re-verified 2026-06-13 against the live official docs at https://anymailfinder.com/email-finder-api/docs — endpoint paths, parameters, and the GeoLead/account/domain/report endpoints (previously documentation gaps) are now confirmed. Full API docs index: https://anymailfinder.com/email-finder-api/docs.

---

## Base URL

```
https://api.anymailfinder.com/v5.1
```

---

### Authentication

API key passed via the `Authorization` header (no "Bearer" prefix).

```bash
curl --request POST \
  --url "https://api.anymailfinder.com/v5.1/find-email/person" \
  --header "Authorization: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{"domain": "example.com", "first_name": "John", "last_name": "Doe"}'
```

---

### Rate Limits

No rate limits. Requests are queued and the system auto-scales. Use a 180-second timeout for individual requests.

---

### Response Format

All responses return JSON.

```json
{
  "credits_charged": 1,
  "email": "john.doe@example.com",
  "email_status": "valid",
  "...": "endpoint-specific data"
}
```

---

### Error Handling

Standard HTTP status codes. Common codes:

| Status | Error Key | Meaning |
|---|---|---|
| 400 | `bad_request` | Invalid or missing parameters |
| 401 | `unauthorized` | Missing or invalid API key |
| 402 | `upgrade_needed` | Insufficient credits |

Error response format:
```json
{
  "error": "bad_request",
  "message": "Description of the problem."
}
```

---

### Credit Costs

| Action | Cost |
|---|---|
| Person email found (valid) | 1 credit |
| Person email not found | Free |
| Decision-maker email found (valid) | 2 credits |
| Decision-maker email not found | Free |
| Email verification | 0.2 credits (re-verify within 30 days: free) |
| Company emails | 1 credit |

---

### Endpoints

---

#### 1. Find Person Email

Find a specific person's professional email address by name and company.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/find-email/person` | Find email for a named person at a company |

**`POST /find-email/person` body parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | One of `domain`/`company_name` | Company domain to search |
| `company_name` | string | One of `domain`/`company_name` | Company name to search |
| `first_name` | string | See note | Person's first name |
| `last_name` | string | See note | Person's last name |
| `full_name` | string | See note | Person's full name |
| `linkedin_url` | string | See note | Person's LinkedIn profile URL — used as a fallback (name + company is attempted first, LinkedIn second) |

> **Note**: Provide name + company (either `full_name` or both `first_name`/`last_name`, plus at least one of `domain`/`company_name`), OR a `linkedin_url` alone, OR both (name/company tried first, LinkedIn as fallback). This endpoint supersedes the standalone LinkedIn endpoint.

**Headers**:

| Header | Required | Description |
|---|---|---|
| `Authorization` | Yes | API key |
| `Content-Type` | Yes | `application/json` |
| `x-webhook-url` | No | URL for async delivery of results |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `credits_charged` | number | Credits consumed (1 if valid, 0 otherwise) |
| `email` | string | Discovered email address (or null) |
| `email_status` | string | Status: `valid`, `risky`, `not_found`, `blacklisted` |
| `valid_email` | string | The verified email (present when status is `valid`) |
| `person_full_name` | string | Full name (populated only when matched via LinkedIn) |
| `person_company_name` | string | Company name (populated only when matched via LinkedIn) |
| `person_job_title` | string | Job title (populated only when matched via LinkedIn) |

---

#### 2. Find Decision Maker Email

Find the email of a decision maker at a company by role category.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/find-email/decision-maker` | Find email for a decision maker by role |

**`POST /find-email/decision-maker` body parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | One of `domain`/`company_name` | Company domain to search |
| `company_name` | string | One of `domain`/`company_name` | Company name to search |
| `decision_maker_category` | string[] | Yes | Role categories to search |

**Decision maker categories**: `ceo`, `engineering`, `finance`, `hr`, `it`, `logistics`, `marketing`, `operations`, `buyer`, `sales`

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `credits_charged` | number | Credits consumed (2 if valid, 0 otherwise) |
| `decision_maker_category` | string | Matched category |
| `email` | string | Discovered email address |
| `email_status` | string | Status: `valid`, `risky`, `not_found`, `blacklisted` |
| `person_full_name` | string | Decision maker's full name |
| `person_job_title` | string | Decision maker's job title |
| `person_linkedin_url` | string | Decision maker's LinkedIn profile URL |
| `valid_email` | string | The verified email (present when status is `valid`) |

---

#### 3. Find Company Emails

| Method | Endpoint | Description |
|---|---|---|
| POST | `/find-email/company` | Find up to 20 email addresses at a company |

Find up to 20 email addresses at a given domain or company. Costs 1 credit (charged only when at least one valid email is found; free if all results are risky/blacklisted/not_found, and free on repeat within 30 days).

**Body parameters**: `domain` or `company_name` (at least one required). Optional `x-webhook-url` header for async delivery.

---

#### 4. Find Email by LinkedIn URL

| Method | Endpoint | Description |
|---|---|---|
| POST | `/find-email/linkedin-url` | Find a person's email from their LinkedIn profile URL |

Find a person's email from their LinkedIn profile URL. Costs 1 credit if valid (free otherwise; free on repeat within 30 days).

**Body parameter**: `linkedin_url` (string, required). Optional `x-webhook-url` header.

**Response fields**: `credits_charged`, `email`, `email_status` (`valid`/`risky`/`not_found`/`blacklisted`), `valid_email`, `person_full_name`, `person_company_name`, `person_job_title`.

> **Note**: This endpoint is superseded by Find Person Email (which now accepts `linkedin_url` directly) but remains functional in v5.1.

---

#### 5. Email Verification

Verify whether an email address is valid and deliverable.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/verify-email` | Verify an email address |

**`POST /verify-email` body parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to verify |

**Headers**:

| Header | Required | Description |
|---|---|---|
| `Authorization` | Yes | API key |
| `Content-Type` | Yes | `application/json` |
| `x-webhook-url` | No | URL for async delivery of results |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `credits_charged` | number | Credits consumed (0.2; free if re-verified within 30 days) |
| `email_status` | string | Status: `valid`, `risky`, `invalid` |

---

#### 6. Bulk Email Search — Create with JSON

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bulk/json` | Create a bulk email search from JSON rows |

Submit up to 100,000 rows for async bulk email search. The search type per row (person/company/decision-maker/linkedin) is inferred from the fields you map. Processing speed is approximately 1,000 rows in 5 minutes. Supports webhook notification on completion via `x-webhook-url`. **Free to create — credits are charged the first time results are downloaded.**

---

#### 7. Bulk Email Search — Create with File

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bulk/multipart` | Create a bulk email search by uploading a CSV or Excel file (multipart form data) |

Upload a CSV or Excel file for bulk processing. Same credit/charging model as the JSON variant (charged on first download).

---

#### 8. Bulk Email Search — Get Info

| Method | Endpoint | Description |
|---|---|---|
| GET | `/bulk/{searchId}` | Retrieve status/info for a bulk search job |

Check the status of an async bulk search job by its `searchId`.

---

#### 9. Bulk Email Search — Download Results

| Method | Endpoint | Description |
|---|---|---|
| GET | `/bulk/{searchId}/download` | Download completed bulk search results |

Download completed bulk search results. Credits are charged the first time results are downloaded (1 credit/valid row for person/company/linkedin, 2 credits/valid row for decision-maker; risky/blacklisted/not-found and 30-day duplicates are free).

---

#### 10. GeoLead Finder

| Method | Endpoint | Description |
|---|---|---|
| POST | `/geo-lead` | Create a location-based lead search |

Create a GeoLead search around a geographic point. **Free to create — credits charged on first download.** Status/download follow the same pattern as bulk jobs.

**Body parameters**: `query` (business type/search term), `latitude`, `longitude`, `radius_km`, `find_company_emails` (bool), `find_decision_maker_categories` (string[] — pass `[]` to disable), optional `result_limit` and `file_name`. Optional `x-webhook-url` header.

---

#### 11. Get Account Details

| Method | Endpoint | Description |
|---|---|---|
| GET | `/account` | Return account info and remaining credit balance |

Free to call (no credits consumed). **Response fields**: `credits_left` (integer), `email` (string).

---

#### 12. Domain Email Count / Order / Download

| Method | Endpoint | Description |
|---|---|---|
| GET | `/domain/{domain}/email` | Count known emails at a domain + credits required to download the full list |
| POST | `/domain/{domain}/email/order` | Pay for / order the full email file for a domain |
| GET | `/domain/{domain}/email/download` | Download the ordered domain email file |

The count endpoint is free; response includes `domain`, `email_count`, `credits_required`, and `status` (`null`/`queued`/`ready`). **The ordered file's emails are NOT verified** — validate before use.

---

#### 13. Report Bad Email

| Method | Endpoint | Description |
|---|---|---|
| POST | `/report/bad-email` | Report an incorrect/bounced email result |

Free to call. **Body parameters**: `email` (string, required), `additional_info` (string, required — why the email is bad), `bounce_message` (string, optional).

---

### Webhook Support

Anymail Finder supports async delivery via webhooks. Add the `x-webhook-url` header to a request, and results will be POSTed to your URL when processing is complete. Per the official webhook docs, this is supported on five endpoints: Find Person Email, Find Company Emails, Find Decision Maker Email, Find Email by LinkedIn URL, and Email Verification. (Bulk and GeoLead jobs also accept `x-webhook-url` for completion notification.)

> **No request signing**: The official docs do not document any HMAC/signature header on webhook deliveries — validate by using an unguessable callback URL and treating the payload as untrusted.

```bash
curl --request POST \
  --url "https://api.anymailfinder.com/v5.1/find-email/person" \
  --header "Authorization: yourApiKey" \
  --header "Content-Type: application/json" \
  --header "x-webhook-url: https://your-server.com/webhook" \
  --data '{"domain": "example.com", "first_name": "John", "last_name": "Doe"}'
```

---

## Quick Reference — Common Workflows

### Find a person's email by name and domain
```bash
curl --request POST \
  --url "https://api.anymailfinder.com/v5.1/find-email/person" \
  --header "Authorization: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{"domain": "microsoft.com", "first_name": "John", "last_name": "Doe"}'
```

**Response** (200 OK):
```json
{
  "credits_charged": 1,
  "email": "john.doe@microsoft.com",
  "email_status": "valid",
  "valid_email": "john.doe@microsoft.com"
}
```

### Find a decision maker at a company
```bash
curl --request POST \
  --url "https://api.anymailfinder.com/v5.1/find-email/decision-maker" \
  --header "Authorization: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{"domain": "example.com", "decision_maker_category": ["ceo"]}'
```

**Response** (200 OK):
```json
{
  "credits_charged": 2,
  "decision_maker_category": "ceo",
  "email": "jane.smith@example.com",
  "email_status": "valid",
  "person_full_name": "Jane Smith",
  "person_job_title": "Chief Executive Officer",
  "person_linkedin_url": "https://linkedin.com/in/janesmith",
  "valid_email": "jane.smith@example.com"
}
```

### Verify an email address
```bash
curl --request POST \
  --url "https://api.anymailfinder.com/v5.1/verify-email" \
  --header "Authorization: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{"email": "john.doe@microsoft.com"}'
```

**Response** (200 OK):
```json
{
  "credits_charged": 0.2,
  "email_status": "valid"
}
```
