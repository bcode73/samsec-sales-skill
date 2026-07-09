<!-- Source: https://www.newzenler.com/api/documentation/public/api-doc.html -->
<!-- Source: https://support.newzenler.com/en/articles/7668719-developers-creating-an-api-key-and-reading-the-documentation -->
<!-- Source: https://zapier.com/apps/zenler/integrations  |  https://apps.make.com/zenler -->
<!-- Captured 2026-06-27. Endpoint list, auth, pagination, rate limit, roles, and the sample Add-User
     request/response are copied from the public API doc page. JSON bodies beyond the documented sample
     are CONSTRUCTED from the field lists and marked as such — verify against the live API. -->

# New Zenler API Reference

New Zenler exposes a **public REST API (v1)** for managing users, course/funnel/webinar enrollment, and
pulling reports, plus a **Zapier / Make / Integrately** automation surface. **API access is gated to the
Pro plan and above** — the key is generated in-app at **Site → Developers**. There are **no native
webhooks**; outbound eventing is done through Zapier triggers (see below).

## Base URL & authentication

- **Base URL:** `https://api.newzenler.com/api/v1/`
- **Auth headers (required on every request):**
  - `X-API-Key: {your_api_key}`
  - `X-Account-Name: {your_subdomain}`  ← your Zenler site subdomain, e.g. `myschool` for `myschool.newzenler.com`
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Key management:** Site → Developers → **Generate Key** (also Reset / Copy / Access API Documentation).
  The in-app note warns: people without API knowledge should refrain from using this area.
- **Plan gate:** API access requires **Pro** or **Premium**. On Starter the key area is unavailable.
- **API version:** v1.0 (published 2018-12-14). **Date format:** `YYYY-MM-DD`. **Data format:** JSON.

### Auth quick-start (simplest GET — list users)

```bash
curl -s "https://api.newzenler.com/api/v1/users" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Account-Name: YOUR_SUBDOMAIN" \
  -H "Accept: application/json"
```

## Standard response envelope

Every response is wrapped:

```json
{
  "response_code": 200,
  "message": "Success",
  "data": { "...": "items or entity details" },
  "pagination": {
    "total_items": 142,
    "items_per_page": 15,
    "page_index": 1,
    "total_pages": 10
  }
}
```

`pagination` is present on list responses only.

## Endpoints

### Users
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/users` | List users (paginated) |
| POST | `/api/v1/users` | Create a user |
| GET | `/api/v1/users/{user_id}` | Get a specific user |
| PUT | `/api/v1/users/{user_id}` | Update a user |
| DEL | `/api/v1/users/{user_id}` | Delete a user |
| POST | `/api/v1/users/{user_id}/enroll` | Enroll a user in a course |
| POST | `/api/v1/users/{user_id}/unenroll` | Unenroll a user from a course |

### Courses
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/courses` | List courses (with filters) |
| GET | `/api/v1/courses/{course_id}` | Get course details |
| POST | `/api/v1/courses/{course_id}/enroll` | Bulk-enroll multiple users into a course |

### Funnels
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/funnels` | List marketing funnels |
| GET | `/api/v1/funnels/enrollments/{funnel_id}` | Get a funnel's subscribers |
| POST | `/api/v1/funnels/{funnel_id}/subscribe` | Subscribe a lead to a funnel |
| POST | `/api/v1/funnels/{funnel_id}/unsubscribe` | Unsubscribe a lead from a funnel |

### Live Classes
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/live-class/get-live-classes-list` | List upcoming live classes |
| POST | `/api/v1/live-class/{liveclass_id}/register` | Register an attendee |
| POST | `/api/v1/live-class/{liveclass_id}/unregister` | Cancel a registration |

### Live Webinars
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/live-webinar/get-live-webinars-list` | List webinars |
| POST | `/api/v1/live-webinar/{webinar_id}/register` | Register an attendee |
| POST | `/api/v1/live-webinar/{webinar_id}/unregister` | Cancel a registration |

### Reports
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/reports/enrollments/brief` | Enrollment summary |
| GET | `/api/v1/reports/enrollments/detailed` | Full enrollment records |
| GET | `/api/v1/reports/sales/brief` | Sales overview |
| GET | `/api/v1/reports/sales/detailed` | Detailed transactions |
| GET | `/api/v1/reports/course-progress/brief` | Course-completion summary |
| GET | `/api/v1/reports/course-progress/detailed` | Individual progress tracking |
| GET | `/api/v1/reports/affiliates/brief` | Affiliate-performance summary |
| GET | `/api/v1/reports/affiliates/detailed` | Detailed affiliate transactions |

## User roles (the `roles` array)

`2` Site Admin · `3` Course Instructor · `4` Student · `7` Affiliate · `8` Lead · `11` Assistant ·
`12` Support. A created user can hold multiple roles (e.g. `[3, 7]` = instructor + affiliate).

## Top-5 endpoint request/response examples

### 1. Create a user (POST `/api/v1/users`) — verbatim from docs

```bash
curl -s -X POST "https://api.newzenler.com/api/v1/users" \
  -H "X-API-Key: YOUR_API_KEY" -H "X-Account-Name: YOUR_SUBDOMAIN" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@example.com",
        "password": "123456",
        "commission": 10,
        "roles": [3, 7]
      }'
```
```json
{
  "response_code": 201,
  "message": "People added successfully",
  "data": {
    "id": "313.5c109f1b58473",
    "first_name": "test",
    "last_name": "test",
    "email": "test123456@example.com"
  }
}
```
> Note the `id` is a string (e.g. `313.5c109f1b58473`), not an integer — store it as text.

### 2. List users (GET `/api/v1/users`) <!-- Constructed from docs — verify against live API -->
```bash
curl -s "https://api.newzenler.com/api/v1/users?limit=15&page=2" \
  -H "X-API-Key: YOUR_API_KEY" -H "X-Account-Name: YOUR_SUBDOMAIN" -H "Accept: application/json"
```
```json
{
  "response_code": 200,
  "message": "Success",
  "data": [
    { "id": "313.5c109f1b58473", "first_name": "Test", "last_name": "Test", "email": "test@example.com", "roles": [4] }
  ],
  "pagination": { "total_items": 142, "items_per_page": 15, "page_index": 2, "total_pages": 10 }
}
```

### 3. Enroll a user in a course (POST `/api/v1/users/{user_id}/enroll`) <!-- Constructed from docs — verify against live API -->
```bash
curl -s -X POST "https://api.newzenler.com/api/v1/users/313.5c109f1b58473/enroll" \
  -H "X-API-Key: YOUR_API_KEY" -H "X-Account-Name: YOUR_SUBDOMAIN" \
  -H "Content-Type: application/json" -d '{ "course_id": 12345 }'
```
```json
{ "response_code": 200, "message": "User enrolled successfully", "data": { "course_id": 12345, "user_id": "313.5c109f1b58473" } }
```

### 4. Subscribe a lead to a funnel (POST `/api/v1/funnels/{funnel_id}/subscribe`) <!-- Constructed from docs — verify against live API -->
```bash
curl -s -X POST "https://api.newzenler.com/api/v1/funnels/6789/subscribe" \
  -H "X-API-Key: YOUR_API_KEY" -H "X-Account-Name: YOUR_SUBDOMAIN" \
  -H "Content-Type: application/json" \
  -d '{ "first_name": "Sam", "email": "lead@example.com" }'
```
```json
{ "response_code": 200, "message": "Subscribed to funnel", "data": { "funnel_id": 6789, "email": "lead@example.com" } }
```

### 5. Detailed sales report (GET `/api/v1/reports/sales/detailed`) <!-- Constructed from docs — verify against live API -->
```bash
curl -s "https://api.newzenler.com/api/v1/reports/sales/detailed?from=2026-06-01&to=2026-06-27&limit=15" \
  -H "X-API-Key: YOUR_API_KEY" -H "X-Account-Name: YOUR_SUBDOMAIN" -H "Accept: application/json"
```
```json
{
  "response_code": 200,
  "message": "Success",
  "data": [ { "order_id": "ord_001", "email": "buyer@example.com", "amount": 97.00, "date": "2026-06-15", "course_id": 12345 } ],
  "pagination": { "total_items": 30, "items_per_page": 15, "page_index": 1, "total_pages": 2 }
}
```

## Pagination

- Default **15 items per page**; adjust with `limit`. Page through with `page` (the response echoes
  `page_index` / `total_pages` in `pagination`).
- Reports accept date filters (`from`/`to`, `YYYY-MM-DD`) <!-- Constructed from docs — verify param names against live API -->.

```python
import requests

def all_users(api_key, subdomain):
    h = {"X-API-Key": api_key, "X-Account-Name": subdomain, "Accept": "application/json"}
    page, out = 1, []
    while True:
        r = requests.get("https://api.newzenler.com/api/v1/users",
                         headers=h, params={"limit": 15, "page": page}, timeout=30)
        r.raise_for_status()
        body = r.json()
        out += body["data"]
        if page >= body["pagination"]["total_pages"]:
            break
        page += 1
    return out
```

## Rate limits & error handling

- **1000 calls/minute.** Exceeding it returns **HTTP 403** with body message **"Rate Limited Exceeded"**.
  (Note: 403 here means rate-limit, not auth failure — branch on the message, not just the status.)
- Other errors surface in the same envelope via `response_code` + `message`.

```python
import requests, time

def zenler_call(method, path, api_key, subdomain, **kw):
    url = f"https://api.newzenler.com/api/v1/{path.lstrip('/')}"
    h = {"X-API-Key": api_key, "X-Account-Name": subdomain,
         "Content-Type": "application/json", "Accept": "application/json"}
    for attempt in range(5):
        r = requests.request(method, url, headers=h, timeout=30, **kw)
        if r.status_code == 403 and "Rate Limited" in r.text:
            time.sleep(2 ** attempt)         # back off: 1,2,4,8,16s
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()
```

## Webhooks / outbound eventing

No native webhooks are documented. Get events out via **Zapier** (Zenler is both a trigger and action
app) or Make. Connecting requires the **API key + subdomain**.

**Zapier triggers (7):** Course Complete, Lesson Complete, New Live Class Registration, New Live
Interactive Webinar Registration, New Sale (paid or unpaid enrollment), New User, New Funnel Subscription.

**Zapier actions (7):** Create User, Enroll User, Register Live Class, Register Live Webinar, Register
Live Interactive Webinar, Subscribe Funnel, Unenroll User.

**Make modules** mirror these (Create/Get/Update/Delete user, Enroll user, Register live class/webinar,
Subscribe to a funnel, Search users/funnels/live classes/webinars, List enrollments for a funnel) plus a
generic **"Make an API call"** module for any endpoint not covered natively.

## Gaps / not documented

- No native webhook payload schema/signature (use Zapier/Make for eventing).
- Exact request-body field names for enroll/subscribe/report-filter endpoints aren't all published —
  the constructed JSON above is best-effort; verify against the live doc page / Make modules.
- No published auth-error (401) vs rate-limit (403) disambiguation beyond the message string.
- No OpenAPI/Swagger file or MCP server found at capture time.
