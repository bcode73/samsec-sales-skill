<!-- Source: https://apidocs.salesmate.io/ (Salesmate Public APIs — published Postman collection, v4) -->
<!-- Captured 2026-06-28. Secret-shaped example header values redacted to placeholders. -->

# Salesmate API Reference (v4)

Salesmate's public API docs are a published Postman collection at `https://apidocs.salesmate.io/`.
Content below is reproduced verbatim from that collection (Getting Started sections and the v4
request/response examples), with example credential values redacted.

> **Version note (verbatim from the collection):** "We will be deprecating the v1 and v3 versions
> of the Salesmate APIs by May 1, 2023." **Use the `v4` endpoints.** Some resources (Products, Lookup
> Fields) still expose `v1`/`v3` paths.

---

## Base URL

```
https://{link_name}.salesmate.io/apis/{module}/v4/...
```

`{link_name}` is your Salesmate account subdomain (the hostname in your dashboard URL, e.g. `demo`).
The full host you pass in `x-linkname` is `{link_name}.salesmate.io` (e.g. `demo.salesmate.io`).

## Authentication (verbatim)

> APIs use authentication to ensure that client requests access data securely. ... Salesmate uses
> **API Key Authentication**. Using the API key auth, you send a key-value pair to the API either in
> the request headers or query parameters. In the request Authorization tab, select API Key from the
> Type list. Enter your key name and value, and select either Header or Query Params from the Add to
> dropdown list.

**Access Rights and Keys (verbatim):** "Using the APIs, Users would only be able to view data that
they have access to. ... Each user in Salesmate is provided with a set of unique Access Keys. To find
your Access keys — Click your profile picture and select **My Account**. Click the **Access Key** tab."

Every v4 request sends these headers:

| Header | Value |
|---|---|
| `accessToken` | Your Access Key (from My Account → Access Key). |
| `x-linkname` | Your account host, e.g. `demo.salesmate.io`. |
| `Content-Type` | `application/json` |

> Note: in the official Postman collection the `accessToken` header value is stored in a variable the
> collection labels `{{sessionToken}}` — the **header key is `accessToken`** and its value is your
> Access Key. (Make.com's connector surfaces three fields: API Key, API Token, Session Token.)

### Auth quick-start (cURL)

```bash
curl "https://demo.salesmate.io/apis/core/v4/users?status=active" \
  -H "accessToken: YOUR_ACCESS_KEY" \
  -H "x-linkname: demo.salesmate.io" \
  -H "Content-Type: application/json"
```

## Response envelope

Success:
```json
{ "Status": "success", "Data": { /* object or { data:[], totalRows, totalPages } */ } }
```
Failure:
```json
{ "Status": "failure", "Error": { "Code": "4001", "Name": "ValidationError", "Message": "Last Name is required" } }
```

## Error Codes (verbatim)

| Code | Description |
|---|---|
| 400 | Client or Validation Error — request is not in the correct format (e.g. Create a contact requires a valid email; a missing `@` returns this). |
| 401 | Authentication Failure — the Authorization header is either missing or incorrect. |
| 403 | Access Denied — the user's credentials were not authorized for this API call (may require admin-level credentials, or the feature isn't enabled on the portal). |
| 404 | Requested Resource not Found — invalid ID / Salesmate domain in the URL, or an invalid URL itself. |

## API Call Limit (verbatim)

> You can make upto **1500 api calls per hour for each link**.

## Module Ids (verbatim)

| Id | Module |
|---|---|
| 1 | Contact |
| 2 | Task |
| 3 | Email |
| 4 | Deal |
| 5 | Company |
| 6 | Product |
| 7 | Team Inbox |

Module IDs are used in nested paths (e.g. notes on a contact use module `1`). Get a module's IDs:
`GET https://{link_name}.salesmate.io/apis/module/v4/modules/{internal_name}`.

## Date Formats (verbatim)

Accepted: `dd mm yyyy`, `mm dd yyyy`, `yyyy mm dd`, `yyyy dd mm`. Deal datetime fields use ISO-8601
(e.g. `estimatedCloseDate: "2024-11-29T09:34:00Z"`).

## Pagination

Search endpoints are **offset-based** via query params `rows` (page size, up to 250) and `from`
(starting offset). The response `Data` carries `totalRows` and `totalPages` to drive iteration.

---

# Endpoints

## Contacts  `/apis/contact/v4`

### Add a contact — `POST /apis/contact/v4`
Request body:
```json
{
  "firstName": "Test 3", "lastName": "Gupta", "mobile": "985632159",
  "email": "mohit1@example.com", "company": 1, "owner": 1,
  "website": "example.com", "otherPhone": "7489652117",
  "linkedInHandle": "linkedin id", "currency": "INR",
  "billingAddressLine1": "303, city centre", "billingCity": "Ahmedabad",
  "billingZipCode": "380060", "billingState": "IA", "tags": "mudit"
}
```
Success `200`:
```json
{ "Status": "success", "Data": { "id": 1588 } }
```
Validation error `400`:
```json
{ "Status": "failure", "Error": { "Code": "4001", "Name": "ValidationError", "Message": "No such currency exists" } }
```

### Get a contact — `GET /apis/contact/v4/{id}`
Success `200` (abridged):
```json
{
  "Status": "success",
  "Data": {
    "id": 40, "name": "Chaitali Chouhan", "mobile": "",
    "company": { "id": 38, "name": "test company", "owner": { "id": 1, "name": "Sweta Kumari" } },
    "email": "", "designation": "",
    "owner": { "id": 1, "name": "Sweta Kumari", "email": "sweta@example.com" },
    "currency": { "code": "USD", "rate": "1.00", "symbol": "$" },
    "billingCity": "", "billingState": ""
  }
}
```

### Update a contact — `PUT /apis/contact/v4/{id}`
Same body shape as Add. `lastName` is required (omitting it returns `400 "Last Name is required"`).

### Search contacts — `POST /apis/contact/v4/search?rows=250&from=0`
Body specifies the columns to return (`displayingFields`), a `filterQuery` rule group, and `sort`:
```json
{
  "displayingFields": ["contact.name","contact.email","contact.mobile","contact.company.name","contact.id"],
  "filterQuery": {
    "group": {
      "operator": "AND",
      "rules": [
        { "condition": "IS_AFTER", "moduleName": "Contact",
          "field": { "fieldName": "contact.createdAt", "displayName": "Created At", "type": "DateTime" },
          "data": "Jan 01, 1970 05:30 AM", "eventType": "DateTime" }
      ]
    }
  },
  "sort": { "fieldName": "contact.name", "orderType": "asc" }
}
```
Success `200`:
```json
{
  "Status": "success",
  "Data": {
    "data": [
      { "id": 8, "name": "Benjamin Jobs", "Owner": { "id": 1 }, "mobile": "7878839370", "email": "email@example.com", "Company": {} },
      { "id": 9, "name": "Cris Fowler", "Owner": { "id": 1 }, "mobile": "704256986", "email": "email1@example.com", "Company": {} }
    ],
    "selectedView": 25, "totalRows": 2, "totalPages": 1
  }
}
```

### Delete a contact — `DELETE /apis/contact/v4/{id}`

## Companies  `/apis/company/v4`
- `GET /apis/company/v4/{id}` — Get a company
- `POST /apis/company/v4` — Add a company → `{ "Status":"success","Data":{ "id": 371 } }`
- `PUT /apis/company/v4/{id}` — Update a company
- `POST /apis/company/v4/search?rows=250&from=0` — Search companies
- `DELETE /apis/company/v4/{id}` — Delete a company

## Deals  `/apis/deal/v4`
### Add a deal — `POST /apis/deal/v4`
```json
{
  "title": "Bags Deal with VIP", "primaryContact": 1540, "primaryCompany": 1, "owner": 1,
  "source": "Ads", "dealValue": "7410000", "estimatedCloseDate": "2024-11-29T09:34:00Z",
  "pipeline": "Sellers", "currency": "USD", "status": "Open", "priority": "High",
  "stage": "Property Listed", "description": "Bags Deal with VIP Bags.", "tags": "VIP,Bags",
  "followers": [ { "userId": 1 }, { "contactId": 3 } ],
  "associatedProducts": [ { "id": 6, "name": "test-2", "sellingPrice": 888, "quantity": 1, "discount": 0 } ]
}
```
Success `200`: `{ "Status": "success", "Data": { "id": 341 } }`
- `GET /apis/deal/v4/{id}` — Get a deal
- `PUT /apis/deal/v4/{id}` — Update a deal
- `POST /apis/deal/v4/search` — Search deals
- `DELETE /apis/deal/v4/{id}` — Delete a deal

## Activities (Tasks)  `/apis/activity/v4`
- `GET /apis/activity/v4/{id}` — Get an activity
- `POST /apis/activity/v4` — Add an activity
- `PUT /apis/activity/v4/{id}` — Update an activity
- `POST /apis/activity/v4/search?rows=250&from=0&viewType=list` — Search activities
- `DELETE /apis/activity/v4/{id}?hardDelete=false` — Delete (soft by default)

## Users  `/apis/core/v4/users`
### Get active users — `GET /apis/core/v4/users?status=active`
```json
{
  "Status": "success",
  "Data": [
    { "id": 5, "firstName": "Chris", "lastName": "Evans", "email": "chris@example.com",
      "timezone": "Asia/Kolkata", "isActive": true, "Role": { "id": 1, "name": "CEO" },
      "Profile": { "id": 5, "name": "Intern" } }
  ]
}
```

## Notes (per record)
Notes hang off a record via its module id, e.g. contact (module `1`):
- `POST /apis/contact/v4/modules/1/object/{contactId}/notes` — add note
- `PUT  /apis/contact/v4/modules/1/object/{contactId}/notes/{noteId}` — update
- `PATCH .../notes/{noteId}/pin-it` and `.../unpin-it` — pin / un-pin
- `DELETE .../notes/{noteId}` — delete
- `GET /apis/module/v4/modules/{moduleId}/objects/{objectId}/notes` — list all notes of a record
Company notes use module `5`, Deal notes module `4`, Activity notes module `2`. Custom modules /
tickets / quotes use the generic `/apis/module/v4/modules/{moduleId}/objects/{objectId}/notes`.

## Custom modules  `/apis/module/v4`
- `POST /apis/module/v4/{moduleId}/records` — create a custom-module record
- `PUT  /apis/module/v4/{moduleId}/records/{recordId}` — update
- `GET  /apis/module/v4/{moduleId}/records/{recordId}?fieldsToQuery=name,owner` — get
- `DELETE /apis/module/v4/{moduleId}/records/{recordId}?hardDelete=false` — delete
- `POST /apis/module/v4/records/search?rows=25&from=0` — search

## Products (v1/v3)
- `POST /apis/v1/products` — add; `PUT /apis/v1/products/{id}` — update; `DELETE /apis/v1/products/{id}` — delete
- `POST /apis/v3/products/search?rows=25&from=0` — search; `PUT /apis/v1/products/bulkDelete` — bulk delete

---

## Rate-limit handling

The limit is 1500 calls/hour per link. There is no documented per-response rate-limit header, so
track your own call count and back off as you approach the cap. A simple guard:

```python
import time, requests

BASE = "https://demo.salesmate.io/apis"
H = {"accessToken": "YOUR_ACCESS_KEY", "x-linkname": "demo.salesmate.io",
     "Content-Type": "application/json"}

def get_all_contacts(page_size=250):
    out, frm = [], 0
    body = {"displayingFields": ["contact.name","contact.email","contact.id"],
            "filterQuery": {"group": {"operator": "AND", "rules": []}},
            "sort": {"fieldName": "contact.id", "orderType": "asc"}}
    while True:
        r = requests.post(f"{BASE}/contact/v4/search?rows={page_size}&from={frm}", headers=H, json=body)
        if r.status_code == 401:
            raise SystemExit("Check accessToken / x-linkname headers")
        data = r.json()["Data"]
        out += data["data"]
        frm += page_size
        if frm >= data["totalRows"]:
            break
        time.sleep(2.4)   # ~1500/hour budget
    return out
```

## Webhooks / outbound automation

Salesmate does not document inbound API webhooks in the public collection. To push events OUT, use
**Workflows** with an "API Call / Webhook" automation action (configured in-app), or the
**Zapier / Make / Pipedream** connectors. Make exposes "Watch Contacts/Companies/Deals/Activities"
triggers, full Create/Update/Get/Delete modules, and a generic "Make an API Call" action.

## Gaps

- Full v4 request/response schemas for every field, and any per-tier API throttling beyond the
  1500/hour link cap, are not in the public Postman collection — verify against your live portal.
- Inbound-webhook signing / HMAC is not documented publicly.
