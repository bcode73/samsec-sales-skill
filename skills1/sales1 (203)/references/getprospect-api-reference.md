### GetProspect APIs — Comprehensive Reference

GetProspect provides a REST API for email discovery, email verification, lead/company search, contact and company management, list management, and LinkedIn-based prospecting.

> **Note**: Endpoints/paths re-verified 2026-06-13 against the live OpenAPI specs at https://getprospect.readme.io/llms.txt and the per-endpoint `reference/*.md` definitions. The API reports version `v1` with a separate `v2` email surface. Verify parameters against the official documentation before building production integrations.

---

## Base URL

```
https://api.getprospect.com
```

---

### Authentication

API key obtained from your GetProspect account settings (Integration / API section). Sent as an `apiKey` **header** on every request (OpenAPI `securitySchemes`: `type: apiKey`, `in: header`, `name: apiKey`).

```bash
curl --request GET \
  --url "https://api.getprospect.com/api/v1/health/test" \
  --header "apiKey: yourApiKey"
```

---

### Rate Limits

Not publicly documented in the API reference (no rate-limit headers or numeric limit appear in the OpenAPI specs as of 2026-06-13). The `HttpException` schema does enumerate `429` (Too Many Requests) among possible status codes, so handle 429s defensively with exponential backoff. Monitor usage through your GetProspect account dashboard and contact support for limit details.

---

### Response Format

All responses return JSON.

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

#### 1. Email Services

Discover, verify, and look up email addresses.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v2/email-finder` | Find a professional email from name + domain/company (V2) |
| GET | `/v2/email-verifier` | Verify email deliverability (V2) |
| GET | `/public/v1/email/find` | Find a professional email (V1) |
| GET | `/public/v1/email/verify` | Verify email deliverability (V1) |
| GET | `/public/v1/email/lookup` | Reverse email lookup — find person/company from an email address |

**`GET /v2/email-finder` parameters** (all query params; provide *either* `full_name` *or* `first_name` + `last_name`, and *either* `domain` *or* `company`):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `full_name` | string | No | Full name (e.g. "Dana Hošková"). Use instead of `first_name` + `last_name` |
| `first_name` | string | No | First name. Required if `full_name` not provided |
| `last_name` | string | No | Last name. Required when `first_name` is provided |
| `domain` | string | No | Company domain (e.g. `sprinx.com`). Provides the best results |
| `company` | string | No | Company name. Fallback when `domain` is not provided |

V2 find/verify return an envelope with `email`, `status`, `account`, `domain`, `domain_status`, `smtp_provider`, and (verify) `free_email`.

**`GET /v2/email-verifier` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `email` | string | Yes | Email address to verify |

**`GET /public/v1/email/find` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `name` | string | Yes | Person's full name |
| `company` | string | Yes | Company name or company domain |

**`GET /public/v1/email/lookup` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `email` | string | Yes | Email address to look up |

---

#### 2. Search

Search for leads, companies, and contacts across GetProspect's database.

These query GetProspect's B2B insights (leads/companies) database — distinct from the saved contacts/companies in your own workspace (see sections 3–4).

| Method | Endpoint | Description |
|---|---|---|
| POST | `/public/v1/insights/contacts` | Search the B2B leads database with filters (returns contacts with emails) |
| POST | `/public/v1/insights/companies` | Search the B2B companies database with filters |
| GET | `/public/v1/insights/contact` | Find a contact's data from a LinkedIn profile URL |
| GET | `/api/v1/insights/search/fast-search/{search}` | Quick search across insight contacts and companies |

**`POST /public/v1/insights/contacts`** — pagination/sort via **query** params, filters via **JSON body**:

| Parameter | Type | In | Required | Description |
|---|---|---|---|---|
| `apiKey` | string | header | Yes | API key |
| `pageSize` | int | query | No | Results per page |
| `pageNumber` | int | query | No | Page number |
| `sort` | string | query | No | Field to sort by |
| `order` | string | query | No | Sort order |

JSON body fields (each is a filter object, typically `{ "value": [...], "operator": "..." }`): `contactName`, `companyName`, `jobTitle`, `seniority`, `domain`, `industry`, `location`, `keywords`, `headquarters`, `employees`, `lastUpdated` (full-date), `email` (enum `all` | `all_contacts`).

**`POST /public/v1/insights/companies`** — same `pageSize`/`pageNumber`/`sort`/`order` query params; JSON body holds company filter objects (industry, size, location, etc.).

**`GET /public/v1/insights/contact` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `linkedinUrl` | string | Yes | LinkedIn profile URL |

**`GET /api/v1/insights/search/fast-search/{search}` parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `search` | string | Yes (path) | Search value (in the URL path) |

---

#### 3. Contact Management

CRUD operations for managing contacts in your GetProspect account.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/contacts/contact` | Create a new contact |
| GET | `/api/v1/contacts/contact/{contactId}` | Get a single contact by ID |
| PATCH | `/api/v1/contacts/contact/{contactId}` | Update a contact |
| DELETE | `/api/v1/contacts/contact/{contactId}` | Delete a contact |
| POST | `/api/v1/contacts/contact/search` | Search contacts saved in your workspace |
| POST | `/api/v1/contacts/contact/{contactId}/companies` | Add companies to a contact |

**`POST /api/v1/contacts/contact` body** (`CreateContactDto`) — fields are passed as a `properties` array of `{ "property", "value" }` items, **not** flat keys:

```json
{
  "properties": [
    { "property": "firstName", "value": "John" },
    { "property": "lastName",  "value": "Doe" },
    { "property": "email",     "value": "john.doe@example.com" },
    { "property": "title",     "value": "VP of Sales" }
  ],
  "listRelations": ["list-id-1"]
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `properties` | array | Yes | Array of `{ property, value }` items |
| `listRelations` | array | No | Array of list IDs to add the contact to |

**`PATCH /api/v1/contacts/contact/{contactId}` body**: same `properties` array shape, carrying only the fields to update.

---

#### 4. Company Management

CRUD operations for managing companies in your GetProspect account.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/companies/company/search/query` | Search companies saved in your workspace by name |
| GET | `/api/v1/companies/company/{companyId}` | Get a single company by ID |
| PATCH | `/api/v1/companies/company/{companyId}` | Update a company |
| DELETE | `/api/v1/companies/company/{companyId}` | Delete a company |
| POST | `/api/v1/companies/company` | Create a new company |

**`GET /api/v1/companies/company/search/query` parameters** (query): `name` (string, optional — company name to search), `limit` (int, optional). `apiKey` in header.

**`POST /api/v1/companies/company` parameters** (JSON body):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes | API key (header or body) |
| `name` | string | Yes | Company name |
| `domain` | string | No | Company domain |
| `industry` | string | No | Industry |
| `size` | string | No | Company size range |
| `location` | string | No | Company location |

---

#### 5. List Management

Manage contact lists for organizing and segmenting your prospects.

Lists live under the contacts namespace (`/api/v1/contacts/lists`).

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/contacts/lists` | Get all lists |
| POST | `/api/v1/contacts/lists` | Create a new list |
| DELETE | `/api/v1/contacts/lists` | Delete list(s) |
| POST | `/api/v1/contacts/lists/lists-sizes` | Get list size(s) (contact count) |
| PATCH | `/api/v1/contacts/lists/{listId}` | Update a list (name) |
| POST | `/api/v1/contacts/lists/{list}/add` | Add contacts to a list |
| GET | `/api/v1/contacts/lists/{list}/contacts/search` | Get contacts in a list |

**`POST /api/v1/contacts/lists` parameters** (JSON body, `CreateListDto`):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `name` | string | Yes | List name |

**`POST /api/v1/contacts/lists/{list}/add` parameters** (JSON body, `AddContactsDto`):

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | Yes (header) | API key |
| `contactsIds` | array | Yes | Array of contact IDs to add |

---

#### 6. Utility

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/properties` | Retrieve all custom property definitions in your workspace |
| GET | `/api/v1/health/test` | Health check — verify API connectivity |
| POST | `/api/v1/stripe/purchase/status` | Stripe purchase status (billing) |
| GET | `/internal/metrics` | Prometheus metrics (internal) |

---

### Webhook Support

No webhook or callback endpoints are listed in the current API reference (no `webhook`/event entries in the OpenAPI index as of 2026-06-13). Use polling or the iPaaS integrations (Zapier/Make) for event-driven workflows.

---

## Quick Reference — Common Workflows

### Find a professional email (V2)
```bash
curl --request GET \
  --url "https://api.getprospect.com/v2/email-finder?first_name=John&last_name=Doe&domain=example.com" \
  --header "apiKey: yourApiKey"
```

### Verify an email (V2)
```bash
curl --request GET \
  --url "https://api.getprospect.com/v2/email-verifier?email=john.doe@example.com" \
  --header "apiKey: yourApiKey"
```

### Reverse email lookup (V1)
```bash
curl --request GET \
  --url "https://api.getprospect.com/public/v1/email/lookup?email=john.doe@example.com" \
  --header "apiKey: yourApiKey"
```

### Search the B2B leads database with filters
```bash
curl --request POST \
  --url "https://api.getprospect.com/public/v1/insights/contacts?pageNumber=1&pageSize=25" \
  --header "apiKey: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{
    "jobTitle": { "value": ["VP Sales"] },
    "location": { "value": ["United States"] }
  }'
```

### Find contact by LinkedIn URL
```bash
curl --request GET \
  --url "https://api.getprospect.com/public/v1/insights/contact?linkedinUrl=https://linkedin.com/in/johndoe" \
  --header "apiKey: yourApiKey"
```

### Create a contact
```bash
curl --request POST \
  --url "https://api.getprospect.com/api/v1/contacts/contact" \
  --header "apiKey: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{
    "properties": [
      { "property": "firstName", "value": "John" },
      { "property": "lastName",  "value": "Doe" },
      { "property": "email",     "value": "john.doe@example.com" },
      { "property": "title",     "value": "VP of Sales" }
    ]
  }'
```

### Create a list and add contacts
```bash
# Create list
curl --request POST \
  --url "https://api.getprospect.com/api/v1/contacts/lists" \
  --header "apiKey: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{"name": "Q1 Outreach"}'

# Add contacts to list
curl --request POST \
  --url "https://api.getprospect.com/api/v1/contacts/lists/{listId}/add" \
  --header "apiKey: yourApiKey" \
  --header "Content-Type: application/json" \
  --data '{"contactsIds": ["contact-id-1", "contact-id-2"]}'
```

### Health check
```bash
curl --request GET \
  --url "https://api.getprospect.com/api/v1/health/test" \
  --header "apiKey: yourApiKey"
```
