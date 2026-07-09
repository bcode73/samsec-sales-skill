<!-- Source: https://freshlearn.com/support/api -->
<!-- Source: https://zapier.com/apps/freshlearn/integrations  |  https://apps.make.com/freshlearn (operation surface) -->
<!-- Captured 2026-06-27. Base URL, auth, pagination envelope, and the section list are copied from the
     public API reference. The detailed REST endpoint paths/methods are JS-rendered in the doc and were
     NOT fetchable; the verified operation surface below is taken from the Zapier/Make connectors. JSON
     bodies are CONSTRUCTED from documented fields + the connector field lists and marked as such —
     confirm exact paths/shapes against the live reference at https://freshlearn.com/support/api. -->

# FreshLearn API Reference

FreshLearn exposes a **REST API (v1)** for managing members, course enrollments, courses, payments, and
assessments, plus **native webhooks** and a **Zapier / Make / Pabbly / Integrately** automation surface.
**API access is gated to the No Brainer+ plan and above.** The key lives at **Settings → User → API Key**
and is **account-scoped** (every response is limited to your academy's data).

## Base URL & authentication

- **Base URL:** `https://api.freshlearn.com/v1`
- **Auth:** every request must include your key in the **`api-key`** header.
- **Key location:** Admin app → **Settings → User → API Key**.
- **Plan gate:** **No Brainer+** or **Enterprise** (no API on Free / Pro / No Brainer).
- **Format:** JSON for all requests/responses.

### Auth quick-start (simplest GET — list members)

```bash
curl -s "https://api.freshlearn.com/v1/members?limit=50" \
  -H "api-key: YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Pagination (cursor-based) — envelope verbatim from docs

List endpoints return a `data` array plus a `pageInfo` object. To page, pass `pageInfo.nextCursor` back as
the `cursor` query param; stop when `hasMore` is `false`.

```json
{
  "data": [{ "/* resource */": "..." }],
  "pageInfo": {
    "limit": 50,
    "hasMore": true,
    "nextCursor": "eyJ0IjoxNzAwMDAwMDAwLCJpZCI6OTl9",
    "sort": "created_desc"
  }
}
```

**Query params:** `cursor` (from previous response), `limit` (1–200, default 50), `order` (`desc`/`asc`),
and date filters expressed as **Unix timestamps in seconds**.

```python
import requests

def paginate(path, api_key, params=None):
    params = dict(params or {})
    url = f"https://api.freshlearn.com/v1{path}"
    h = {"api-key": api_key, "Accept": "application/json"}
    out, cursor = [], None
    while True:
        if cursor: params["cursor"] = cursor
        body = requests.get(url, headers=h, params=params, timeout=30).json()
        out += body["data"]
        if not body["pageInfo"]["hasMore"]:
            break
        cursor = body["pageInfo"]["nextCursor"]
    return out
```

## Documented API sections

The public reference is organized into: **Getting Started · Members · Courses · Product Enrollments ·
Payments · Assessments · Reference.** The exact method+path for each operation is rendered client-side in
the doc (not fetchable here) — confirm against the live reference. The **verified operation surface**
(from the Zapier/Make connectors, which call these endpoints) is:

| Domain | Operation | Notes |
|---|---|---|
| Members | Create member | Establishes a learner profile (name + email) |
| Members | Update member | Modify name/contact info |
| Members | Get member data | Read a member |
| Enrollments | Enroll member in **course** product | Creates the member if new |
| Enrollments | Create course enrollment | Enroll an **existing** member into a course |
| Enrollments | Unenroll member from course product | Remove course access |
| Enrollments | Enroll member in **digital download** product | Creates member if new |
| Enrollments | Enroll member in **masterclass** product | Creates member if new |
| Enrollments | Enroll member in **product bundle** | Creates member if new |
| Courses | List / read courses | Course structure |
| Payments | Read payments | Transaction history |
| Assessments | Read assessments | Quiz/assessment results |

## Top endpoint request/response examples

<!-- All JSON below is CONSTRUCTED from documented fields + connector field lists — verify against live API -->

### 1. List members (GET `/v1/members`)
```bash
curl -s "https://api.freshlearn.com/v1/members?limit=50&order=desc" \
  -H "api-key: YOUR_API_KEY" -H "Accept: application/json"
```
```json
{
  "data": [
    { "id": "mem_8f3", "email": "buyer@example.com", "first_name": "Sam", "last_name": "Rivera", "created": 1718900000 }
  ],
  "pageInfo": { "limit": 50, "hasMore": false, "nextCursor": null, "sort": "created_desc" }
}
```

### 2. Create a member (POST `/v1/members`)
```bash
curl -s -X POST "https://api.freshlearn.com/v1/members" \
  -H "api-key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{ "email": "buyer@example.com", "first_name": "Sam", "last_name": "Rivera" }'
```
```json
{ "data": { "id": "mem_8f3", "email": "buyer@example.com", "first_name": "Sam", "last_name": "Rivera" } }
```

### 3. Enroll a member in a course product
```bash
# Enroll-in-course-product (creates the member if the email is new)
curl -s -X POST "https://api.freshlearn.com/v1/product-enrollments" \
  -H "api-key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{ "email": "buyer@example.com", "first_name": "Sam", "course_id": "crs_123", "product_type": "course" }'
```
```json
{ "data": { "member_id": "mem_8f3", "course_id": "crs_123", "status": "enrolled" } }
```

### 4. Update a member (PUT/PATCH `/v1/members/{id}`)
```bash
curl -s -X PUT "https://api.freshlearn.com/v1/members/mem_8f3" \
  -H "api-key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{ "first_name": "Samantha" }'
```
```json
{ "data": { "id": "mem_8f3", "first_name": "Samantha", "email": "buyer@example.com" } }
```

### 5. Unenroll a member from a course product
```bash
curl -s -X POST "https://api.freshlearn.com/v1/product-enrollments/unenroll" \
  -H "api-key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{ "email": "buyer@example.com", "course_id": "crs_123" }'
```
```json
{ "data": { "member_id": "mem_8f3", "course_id": "crs_123", "status": "unenrolled" } }
```

## Rate limits & error handling

The public reference does not publish explicit rate-limit headers or an error-response schema at capture
time. Defensive pattern — retry on 429/5xx with backoff, treat 4xx as fatal:

```python
import requests, time

def fl_call(method, path, api_key, **kw):
    url = f"https://api.freshlearn.com/v1{path}"
    h = {"api-key": api_key, "Content-Type": "application/json", "Accept": "application/json"}
    for attempt in range(5):
        r = requests.request(method, url, headers=h, timeout=30, **kw)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()
```

## Webhooks & iPaaS

FreshLearn supports **native webhooks** plus Zapier/Make/Pabbly/Integrately. The eventing surface
(mirrored across these) is:

**Zapier triggers (6):** Get Member Data (new member), Get Member Course Enrollments (course enroll), Get
Member Master Class Enrollments, Get Member Digital Download Enrollments, Get Member Product Bundle
Enrollments, Get Course Completed Members (course completion).

**Zapier actions (9):** Create Member, Update Member, Create Course Enrollment, Enroll Member in Course
Product, Enroll Member in Digital Download Product, Enroll Member in Master Class Product, Enroll Member in
Product Bundle Product, Unenroll Member From Course Product (each "enroll" action creates the member if new).

<!-- Constructed webhook payload from connector fields — verify against live webhook delivery -->
```json
{
  "event": "course_completed",
  "member": { "id": "mem_8f3", "email": "buyer@example.com", "first_name": "Sam" },
  "course": { "id": "crs_123", "title": "Launch Your Academy" },
  "completed_at": 1718900000
}
```

## Gaps / not documented

- Exact REST method+path per endpoint is JS-rendered in the reference — confirm at
  `https://freshlearn.com/support/api`. The paths in the examples above are **best-effort constructions**
  from the documented sections + connector operations.
- No published rate-limit headers or error-response schema.
- No published native-webhook payload signature/verification scheme (validate by re-reading the member via
  `GET /v1/members` before granting sensitive access).
- No OpenAPI/Swagger file or MCP server found at capture time.
