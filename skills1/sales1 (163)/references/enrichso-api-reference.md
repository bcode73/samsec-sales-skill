### Enrich.so APIs — Comprehensive Reference

Enrich.so provides a REST API for LinkedIn profile enrichment, email/phone finding, company intelligence, bulk enrichment, IP-to-company resolution, and verification services.

> **Note**: Best-effort from research — full API docs at https://docs.enrich.so/. Verify endpoints and parameters against the official documentation.

---

## Base URL

```
https://api.enrich.so
```

---

### Authentication

Bearer token passed via the `Authorization` header. Obtain your API key from your Enrich.so account dashboard.

```bash
curl --request GET \
  --url "https://api.enrich.so/v1/api/linkedin-by-url?url=https://linkedin.com/in/example&type=person" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

---

### Rate Limits

Documented at https://docs.enrich.so/introduction/rate-limit — **300 requests per minute**, with a 5-minute window allowing bursts up to **1500 requests per 5 minutes**. During periods of high load the system may temporarily tighten limits for all accounts. Also monitor `credits_remaining` in responses to track credit consumption.

---

### Response Format

All responses return JSON. Every response includes credit tracking fields:

```json
{
  "credits_used": 1,
  "credits_remaining": 4999,
  "...": "endpoint-specific data"
}
```

---

### Error Handling

Standard HTTP status codes. On failure, the response includes:

```json
{
  "error": true,
  "message": "Description of the error"
}
```

**Common HTTP status codes**:

| Status | Meaning |
|---|---|
| 200 | Success |
| 202 | Accepted (bulk job queued) |
| 400 | Bad request — invalid parameters |
| 401 | Unauthorized — invalid or missing API key |
| 404 | Not found — no data for the given identifier |
| 500 | Internal server error |

---

### Endpoints

---

#### 1. People Enrichment

Find and enrich individual profiles from LinkedIn URLs, emails, names, or phone numbers.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/api/person` | Reverse Email Lookup — LinkedIn profile + 50+ data points from email (params `email`, optional `in_realtime`) |
| GET | `/v1/api/linkedin-by-url` | LinkedIn profile enrichment by URL |
| GET | `/v2/api/linkedin-to-email` | Find work email from LinkedIn profile URL (v2) |
| GET | `/v1/api/find-email` | Email Finder — find business email from `fullName` + `companyDomain` |
| GET | `/v1/api/mobile-finder` | Phone Number Finder — find phone from `linkedin_profile` (async, may return 202) |
| GET | `/v1/api/email-to-phone-number` | Email to Phone — find phone number from email address |

> **Verified 2026-06-13**: The reverse email lookup endpoint is `/v1/api/person` (docs page also titled "Email to Profile data"), **not** `/v1/api/reverse-email-lookup`. The docs route `docs.enrich.so/reference/reverse-email-lookup` documents the `/v1/api/person` path.

**`GET /v1/api/person` (Reverse Email Lookup) parameters**:

| Parameter | Type | Description |
|---|---|---|
| `email` | string | Email address to look up |
| `in_realtime` | boolean | Set `false` to allow cached results; real-time fetch otherwise |

**`GET /v1/api/find-email` (Email Finder) parameters**:

| Parameter | Type | Description |
|---|---|---|
| `fullName` | string | First and last name of the individual |
| `companyDomain` | string | Company domain (e.g. `example.com`) |

**`GET /v1/api/mobile-finder` (Phone Number Finder) parameters**:

| Parameter | Type | Description |
|---|---|---|
| `linkedin_profile` | string | LinkedIn profile URL |

> Phone Number Finder is asynchronous — it may return HTTP 202; retry the same request after a short delay to get the result.

**`GET /v1/api/linkedin-by-url` parameters**:

| Parameter | Type | Description |
|---|---|---|
| `url` | string | LinkedIn profile or company URL |
| `type` | string | `person` or `company` |

**Response fields** (person):

| Field | Type | Description |
|---|---|---|
| `profile_id` | string | Unique LinkedIn profile identifier |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `sub_title` | string | LinkedIn headline |
| `summary` | string | Profile summary/about section |
| `location` | string | Geographic location |
| `industry` | string | Industry |
| `education` | array | Education history |
| `position_groups` | array | Work experience groups |
| `contact_info` | object | Contact details (email, phone, etc.) |
| `network_info` | object | Connection count and network data |
| `premium` | boolean | Whether profile has LinkedIn Premium |
| `influencer` | boolean | Whether profile is a LinkedIn Influencer |

**`GET /v2/api/linkedin-to-email` parameters**:

| Parameter | Type | Description |
|---|---|---|
| `url` | string | LinkedIn profile URL |

---

#### 2. Company Enrichment

Look up company details, funding data, traffic metrics, similar companies, and employees.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/api/company` | Company Data Lookup — details by `name` and/or `domain` (or LinkedIn URL) |
| GET | Company Funding & Traffic | Funding rounds, investors, amounts, web traffic |
| POST | `/v1/api/similar-companies` | Find lookalike companies |
| GET | Search Company / Search People | Find companies or decision-makers by filters |

> **Verified 2026-06-13**: Company data lookup is at `/v1/api/company` (not `/v1/api/company-lookup`). Employee/company discovery is exposed via the **Search Company** and **Search People** endpoints (docs.enrich.so/reference/search-company, /reference/search-people).

**`POST /v1/api/similar-companies` body**:

| Parameter | Type | Description |
|---|---|---|
| `url` | string | LinkedIn company URL to find similar companies for |
| `account.location` | string[] | Filter by company locations |
| `account.employeeSize` | object | Employee size range with `start` and `end` fields |
| `page` | int | Page number for pagination |
| `num` | int | Number of results per page |

**Response fields** (similar companies):

| Field | Type | Description |
|---|---|---|
| `url` | string | LinkedIn company URL |
| `name` | string | Company name |
| `type` | string | Company type |
| `staff.total` | int | Total employee count |
| `relevancy.score` | float | Similarity score |
| `relevancy.value` | string | Similarity label |

---

#### 3. Verification & Detection

Validate emails and detect disposable or temporary addresses.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/api/verify-email` | Email Verification — deliverability + catch-all detection (param `email`) |
| GET | Disposable/Spam Email Check | Detect temporary/spam email addresses (param `email`) |
| GET | `/v1/api/reverse-hash-lookup` | Reverse Email Append — convert an email `hash` to an address |

> **Verified 2026-06-13**: Email verification is at `/v1/api/verify-email` (not `/v1/api/email-validation`), and reverse-email-append is at `/v1/api/reverse-hash-lookup` (param `hash`).

---

#### 4. IP Intelligence

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/api/ip-to-company-lookup` | Identify company from IP address (param `ip`; supports remote workers) |

> **Verified 2026-06-13**: The IP-to-company endpoint is `/v1/api/ip-to-company-lookup` (not `/v1/api/ip-to-company`).

---

#### 5. Job Data

| Method | Endpoint | Description |
|---|---|---|
| — | Job Listings | Search real-time company job postings |

---

#### 6. Bulk Operations

Batch enrichment for processing large volumes of records.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/api/bulk-enrichment` | Submit bulk enrichment job |
| GET | `/v1/api/bulk-enrichment-results` | Retrieve bulk enrichment results |

**`POST /v1/api/bulk-enrichment` body**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `enrichment_type` | string | Yes | `person`, `company`, `find-email`, `mobile-finder`, or `linkedin-to-email` |
| `name` | string | Yes | Label for the enrichment job |
| `values` | string[] | One of three | Array of identifiers (URLs, emails, etc.) |
| `csvFileUrl` | string | One of three | URL to a CSV file with identifiers |
| `file` | file | One of three | Multipart form file upload |
| `webhookUrl` | string | No | URL to receive results when processing completes |

**Response** (202 Accepted):
```json
{
  "uid": "bulk-job-id-abc123",
  "credits_used": 0,
  "credits_remaining": 4999
}
```

**`GET /v1/api/bulk-enrichment-results` parameters**:

| Parameter | Type | Description |
|---|---|---|
| `uid` | string | Bulk job ID returned from the submit endpoint |
| `page` | int | Page number for paginated results |
| `limit` | int | Number of records per page |

---

#### 7. Search

General-purpose search endpoints across web, news, maps, and media.

| Method | Endpoint | Description |
|---|---|---|
| — | Web Search | Search the web |
| — | News Search | Search news articles |
| — | Maps Search | Search map listings |
| — | Places Search | Search places |
| — | Video Search | Search videos |
| — | Image Search | Search images |
| — | Serp / Shopping Search | SERP and shopping result search |

> The Search family also includes LinkedIn-data search endpoints: **Search People**, **Search Company**, **Search Posts**, **Search People Activities**, **Search Post Reactions by URL**, and **Find Post Details by URL** (docs.enrich.so/reference/*).

---

#### 8. Account / Credits

| Method | Endpoint | Description |
|---|---|---|
| GET | Check Credit Usage | Returns remaining credits and usage for the account (docs.enrich.so/reference/check-credit-usage) |

> **Added 2026-06-13**: A dedicated **Check Credit Usage** endpoint exists for polling remaining credits programmatically (see also docs.enrich.so/introduction/credit-usage for per-endpoint credit costs).

---

### Webhook Support

Pass `webhookUrl` on bulk enrichment endpoints. When processing completes, Enrich.so POSTs the results to your URL.

```bash
curl --request POST \
  --url "https://api.enrich.so/v1/api/bulk-enrichment" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "enrichment_type": "person",
    "name": "Q1 prospect enrichment",
    "values": ["https://linkedin.com/in/prospect1", "https://linkedin.com/in/prospect2"],
    "webhookUrl": "https://your-app.com/enrich-callback"
  }'
```

---

## Quick Reference — Common Workflows

### Enrich a LinkedIn profile
```bash
curl --request GET \
  --url "https://api.enrich.so/v1/api/linkedin-by-url?url=https://linkedin.com/in/johndoe&type=person" \
  --header "Authorization: Bearer YOUR_API_KEY"
```

**Response** (200 OK):
```json
{
  "profile_id": "abc123",
  "first_name": "John",
  "last_name": "Doe",
  "sub_title": "VP of Sales at Acme Corp",
  "summary": "Experienced sales leader...",
  "location": "San Francisco, California",
  "industry": "Software",
  "education": [
    {
      "school": "Stanford University",
      "degree": "MBA"
    }
  ],
  "position_groups": [
    {
      "company": "Acme Corp",
      "title": "VP of Sales",
      "start_date": "2022-01"
    }
  ],
  "contact_info": {
    "email": "john@acme.com"
  },
  "network_info": {
    "connections_count": 500
  },
  "premium": true,
  "influencer": false,
  "credits_used": 1,
  "credits_remaining": 4998
}
```

### Find similar companies
```bash
curl --request POST \
  --url "https://api.enrich.so/v1/api/similar-companies" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "url": "https://linkedin.com/company/acme-corp",
    "account.location": ["United States"],
    "account.employeeSize": {"start": 50, "end": 500},
    "page": 1,
    "num": 10
  }'
```

**Response** (200 OK):
```json
{
  "data": [
    {
      "url": "https://linkedin.com/company/similar-co",
      "name": "Similar Co",
      "type": "Privately Held",
      "staff": {
        "total": 230
      },
      "relevancy": {
        "score": 0.92,
        "value": "High"
      }
    }
  ],
  "credits_used": 1,
  "credits_remaining": 4997
}
```

### Submit bulk enrichment
```bash
# Step 1: Submit the bulk job
curl --request POST \
  --url "https://api.enrich.so/v1/api/bulk-enrichment" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "enrichment_type": "person",
    "name": "March prospect batch",
    "values": [
      "https://linkedin.com/in/prospect1",
      "https://linkedin.com/in/prospect2",
      "https://linkedin.com/in/prospect3"
    ]
  }'

# Response: {"uid": "bulk-abc123", ...}

# Step 2: Retrieve results
curl --request GET \
  --url "https://api.enrich.so/v1/api/bulk-enrichment-results?uid=bulk-abc123&page=1&limit=50" \
  --header "Authorization: Bearer YOUR_API_KEY"
```
