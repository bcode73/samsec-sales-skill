### Minelead APIs — Comprehensive Reference

Minelead provides a REST API for company email discovery, professional email finding, email validation, disposable email detection, lead management, campaign orchestration, and tag-based prospecting.

> **Note**: Best-effort from research — full API docs at https://minelead.io/docs/. Verify endpoints and parameters against the official documentation. Also available on RapidAPI as "minelead2" (username: imene22).

---

## Base URL

```
https://api.minelead.io/v1
```

---

### Authentication

API key passed as a query parameter `key` on every request.

```bash
curl --request GET \
  --url "https://api.minelead.io/v1/search?domain=example.com&key=yourApiKey"
```

---

### Rate Limits

Per the official pricing page: **"Guaranteed rate usage is 8 calls per seconds, or 2400 per 5 mins."** (verified 2026-06-13 at https://minelead.io/pricing/). Monitor usage through your Minelead account dashboard. The Free tier is more aggressively throttled in practice.

---

### Response Format

All responses return JSON with a consistent `status` field, data payloads, and descriptive messages.

```json
{
  "status": "success",
  "...": "endpoint-specific data"
}
```

---

### Error Handling

Standard HTTP status codes. Common codes:

| Status | Meaning |
|---|---|
| 200 | Success |
| 400 | Bad request — invalid or missing parameters |
| 401 | Unauthorized — invalid or missing API key |
| 404 | Not found — no data for the given identifier |
| 500 | Internal server error |

---

### Endpoints

---

#### 1. Email Discovery

Find company email addresses by domain or company name.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/search` | Locate company emails by domain or company name |

**`GET /search` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `domain` | string | One of `domain`/`name` | Company domain to search |
| `name` | string | One of `domain`/`name` | Company name to search (used if `domain` absent) |
| `key` | string | Yes | API key |
| `max-emails` | int | No | Display a maximum of 4 emails for a domain (capped at 4 per the spec) |
| `generic` | boolean | No | Display **only** generic/role-based emails (e.g., info@, support@) |
| `light-mode` | boolean | No | Return lighter response payload (pre-found emails only) |
| `enrich` | boolean | No | Add professional profile data to returned results |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `domain` | string | Company domain searched |
| `status` | string | Request status |
| `pattern` | string | Detected email pattern for the domain |
| `emails` | array | List of discovered email objects |
| `emails[].email` | string | Email address |
| `emails[].verified` | boolean | Whether the email has been verified |
| `emails[].saved` | boolean | Whether the email is saved in your leads |

---

#### 2. Professional Email Finder

Identify a specific person's professional email from their name and company domain.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/find` | Find professional email from first/last name and domain |

**`GET /find` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `firstname` | string | Yes | Person's first name |
| `lastname` | string | Yes | Person's last name |
| `domain` | string | Yes | Company domain |
| `key` | string | Yes | API key |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `email` | string | Matched email address |
| `person` | object | Person details |
| `company` | object | Company details |

---

#### 3. Email Validation

Verify whether an email address is legitimate and deliverable.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/validate` | Verify email legitimacy |

**`GET /validate` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to validate |
| `firstname` | string | No | First name for additional verification |
| `lastname` | string | No | Last name for additional verification |
| `key` | string | Yes | API key |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `status` | string | Validation result — `success` or `catch-all` |
| `form_valid` | boolean | Whether the email format is valid |
| `webmail` | boolean | Whether the email is a webmail provider (Gmail, Yahoo, etc.) |
| `mx_records` | array | MX records for the domain |
| `exists` | boolean | Whether the mailbox exists |

---

#### 4. Disposable Email Detection

Check if an email address belongs to a disposable/temporary email provider.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/detect-disposable` | Assess disposable email provider status |

**`GET /detect-disposable` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to check |
| `key` | string | Yes | API key |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `disposability_score` | int | Score from 0 (not disposable) to 5 (highly disposable) |
| `format_valid` | boolean | Whether the email format is valid |
| `spam` | boolean | Whether the address is associated with spam |
| `dns_records` | object | DNS record statuses for the domain |

---

#### 5. Lead Enrichment

Add professional profile data (job title, location, gender, industry, summary) for a known email.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/enrich` | Enrich a contact from their email address |

**`GET /enrich` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | Yes | Email address to enrich |
| `name` | string | No | Person's name for additional matching |
| `company` | string | No | Company name for additional matching |
| `key` | string | Yes | API key |

**Credit cost**: 2 credits per request.

---

#### 6. Social Email Finder

Extract verified email addresses from a YouTube or Twitter/X profile URL.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/social-email-finder` | Find emails from a social media profile URL |

**`GET /social-email-finder` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | YouTube or Twitter/X profile URL |
| `key` | string | Yes | API key |

**Credit cost**: 2 credits per successful request (emails found). No charge if no emails are found.

---

#### 7. Buying Intent

Analyze a company's purchase signals from news, jobs, and LinkedIn; returns an intent score (0–100).

| Method | Endpoint | Description |
|---|---|---|
| GET | `/buying-intent` | Detect real-time B2B buying signals for a company |

**`GET /buying-intent` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `company` | string | Yes | Company name |
| `domain` | string | Yes | Company domain |
| `level` | int | No | Filter signal sources — `1` = news only, `2` = site/LinkedIn only |
| `key` | string | Yes | API key |

**Credit cost**: 5 credits per request.

---

#### 8. Lead Management

CRUD operations for managing your saved leads collection.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/leads` | Retrieve saved leads collection |
| POST | `/leads` | Add emails to lead database |
| PUT | `/leads` | Modify lead information |
| DELETE | `/leads` | Remove leads from collection |

---

#### 9. Campaign Management

Manage email campaigns and recipient lists.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/campaigns` | List active campaigns |
| GET | `/campaigns-recipients` | View recipient list collections |
| POST | `/campaigns-recipients` | Create new recipient list |
| PUT | `/campaigns-recipients` | Modify recipient list (add/remove emails) |

---

#### 10. Tag-Based Prospecting

Generate lead prospects by submitting keyword tags (e.g., a location and a business category).

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tags` | Generate lead prospects from keyword tags |

**`POST /tags`**: send the API key as the `key` query parameter and a JSON body with a `tags` array, e.g. `{ "tags": ["new york", "hotel"] }`. There is no separate `location` query parameter — location is just another tag string in the array.

---

#### 11. Search History

Retrieve your past search activity. Pagination via `start` (offset) and `limit` is required.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/history` | Retrieve search activity timeline (paginated) |

**`GET /history` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | API key |
| `start` | int | Yes | Pagination offset |
| `limit` | int | Yes | Number of records to return |

---

#### 12. Account

Fetch account details and subscription information.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/account` | Fetch account credentials and subscription details |

---

### Webhook Support

Not documented. Check official docs for updates on webhook or callback support.

---

## Quick Reference — Common Workflows

### Search for company emails by domain
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/search?domain=example.com&max-emails=10&key=yourApiKey"
```

**Response** (200 OK):
```json
{
  "status": "success",
  "domain": "example.com",
  "pattern": "{first}.{last}@example.com",
  "emails": [
    {
      "email": "john.doe@example.com",
      "verified": true,
      "saved": false
    },
    {
      "email": "jane.smith@example.com",
      "verified": true,
      "saved": true
    }
  ]
}
```

### Find a professional email
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/find?firstname=John&lastname=Doe&domain=example.com&key=yourApiKey"
```

**Response** (200 OK):
```json
{
  "status": "success",
  "email": "john.doe@example.com",
  "person": {
    "firstname": "John",
    "lastname": "Doe"
  },
  "company": {
    "domain": "example.com"
  }
}
```

### Validate an email address
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/validate?email=john.doe@example.com&key=yourApiKey"
```

**Response** (200 OK):
```json
{
  "status": "success",
  "form_valid": true,
  "webmail": false,
  "mx_records": ["mx1.example.com", "mx2.example.com"],
  "exists": true
}
```

### Detect disposable email
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/detect-disposable?email=user@tempmail.io&key=yourApiKey"
```

**Response** (200 OK):
```json
{
  "status": "success",
  "disposability_score": 4,
  "format_valid": true,
  "spam": true,
  "dns_records": {
    "mx": true,
    "spf": false,
    "dmarc": false
  }
}
```

### Enrich a contact (2 credits)
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/enrich?email=john.doe@example.com&key=yourApiKey"
```

### Find emails from a social profile (2 credits if found, free if none)
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/social-email-finder?url=https://twitter.com/someprofile&key=yourApiKey"
```

### Detect buying intent for a company (5 credits)
```bash
curl --request GET \
  --url "https://api.minelead.io/v1/buying-intent?company=Acme&domain=example.com&key=yourApiKey"
```
