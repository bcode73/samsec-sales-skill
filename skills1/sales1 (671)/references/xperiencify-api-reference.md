<!-- Source: https://intercom.help/xperiencify/en/articles/9888509-integrating-with-the-api -->
<!-- Source: https://zapier.com/apps/xperiencify/integrations -->
<!-- Captured 2026-06-27. The Help Center renders the API article via Intercom; field lists below are
     copied from that article. JSON request/response bodies are CONSTRUCTED from the documented field
     lists and marked as such — verify against the live API before relying on exact shapes. -->

# Xperiencify API Reference

Xperiencify exposes a small **public REST API** for managing students, course access, tags, and
gamification points, plus a **Zapier/Pabbly/Make** automation surface and **webhook export** of
student data. The API is intentionally minimal — it is built around enrolling/removing students,
reading their progress (XP + completion), and pushing/pulling tags. The docs themselves warn:
*"API code is usually pretty complicated, and programmers usually need to get involved"* — support for
API issues is limited, so treat this as a thin integration layer, not a full platform SDK.

## Base URL & authentication

- **Base URL:** `https://api.xperiencify.io`
- **Auth:** every request takes your API key as a **query parameter**: `?api_key={your_key}`
- **Where to find the key:** Xperiencify app → **Account → Advanced** tab.
- **Transport:** HTTPS only.

> The API key is a bearer-equivalent secret passed in the URL. Because it travels in the query string,
> never expose it in client-side code, browser requests, or logs/analytics that capture full URLs.
> Use it only from a server.

### Auth quick-start (simplest GET)

List all your courses — the simplest read to confirm your key works:

```bash
curl -s "https://api.xperiencify.io/api/public/coach/courses/?api_key=YOUR_API_KEY"
```

<!-- Constructed from docs — verify against live API -->
```json
{
  "courses": [
    { "course_id": 12345, "name": "The Gamified Launch Course", "published": true },
    { "course_id": 12346, "name": "Membership Vault",            "published": true }
  ]
}
```

## Endpoints

### Student management

| Operation | Method | Path | Parameters |
|---|---|---|---|
| Add student to course | POST | `/api/public/student/create/` | `student_email`, `course_id`, `first_name`, `last_name` (opt), `phone` (opt), `password` (opt) |
| Get student info | POST | `/api/public/student/info/` | `email`, `course_id` (opt) |
| Update student info | PATCH | `/api/public/student/update/` | `student_email`, `first_name` (opt), `last_name` (opt), `phone` (opt), `password` (opt) |
| Update custom field | POST | `/api/public/student/customfield/` | `student`, `field`, `value` |
| Remove from course | POST | `/api/public/student/course/remove/` | `student_email`, `course_id` |
| Remove from all courses | POST | `/api/public/student/course/remove/all/` | `student_email` |

- **Add student to course** creates the account if the email doesn't exist yet and **returns a magic
  link** for direct, password-less course access.
- **Update student info** explicitly **cannot change the email address** — email is the identity key.

### Tag management

| Operation | Method | Path | Parameters |
|---|---|---|---|
| List a student's tags | GET | `/api/public/student/tag/list/` | `student_email` |
| Add tag(s) to student | POST | `/api/public/student/tag/manager/` | `student_email`, `tagname` (comma-separated for multiple) |
| Remove tag from student | DELETE | `/api/public/student/tag/manager/` | `student_email`, `tagname` |
| Create a tag | POST | `/api/public/coach/tag/` | `tagname` |
| Remove a tag | DELETE | `/api/public/coach/tag/` | `tagname` |

### Account-level reads

| Operation | Method | Path | Parameters |
|---|---|---|---|
| Get all courses | GET | `/api/public/coach/courses/` | — |
| Get all students | GET | `/api/public/coach/students/` | `course_id` (opt filter) |

### Points operations (the gamification hook)

| Operation | Method | Path | Parameters |
|---|---|---|---|
| Redeem points | POST | `/api/public/student/redeem_points/` | `course_ids`, `student_ids`, `points_type` (`xp`/`xxp`/`bp`), `operation_type` (`REDEEM_POINTS`), `value` |
| Unredeem points | POST | `/api/public/student/unredeem_points/` | `course_ids`, `student_ids`, `points_type`, `operation_type` (`UNREDEEM_POINTS`), `value` |

`points_type` values: **xp** (experience points), **xxp** (the variable/bonus points), **bp** (badge
points). These let an external system award or claw back gamification currency programmatically — e.g.
grant bonus XP when a buyer completes an action in another tool.

## Top-5 endpoint request/response examples

<!-- All JSON below is Constructed from docs — verify against live API -->

### 1. Create / enroll a student (POST)

```bash
curl -s -X POST "https://api.xperiencify.io/api/public/student/create/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "student_email": "buyer@example.com",
        "first_name": "Sam",
        "last_name": "Rivera",
        "course_id": 12345
      }'
```
```json
{
  "status": "ok",
  "student_email": "buyer@example.com",
  "course_id": 12345,
  "magic_link": "https://app.xperiencify.io/login/magic/abc123def456"
}
```

### 2. Get student info (POST)

```bash
curl -s -X POST "https://api.xperiencify.io/api/public/student/info/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "email": "buyer@example.com", "course_id": 12345 }'
```
```json
{
  "email": "buyer@example.com",
  "first_name": "Sam",
  "last_name": "Rivera",
  "courses": [
    {
      "course_id": 12345,
      "xp_earned": 480,
      "xp_total": 1200,
      "xxp_earned": 60,
      "completion_percent": 40
    }
  ]
}
```

### 3. Update a student (PATCH)

```bash
curl -s -X PATCH "https://api.xperiencify.io/api/public/student/update/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "student_email": "buyer@example.com", "first_name": "Samantha", "phone": "+15551234567" }'
```
```json
{ "status": "ok", "updated": ["first_name", "phone"] }
```
> `student_email` identifies the record but **cannot itself be changed** by this call.

### 4. Add tag(s) to a student (POST)

```bash
curl -s -X POST "https://api.xperiencify.io/api/public/student/tag/manager/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "student_email": "buyer@example.com", "tagname": "vip,early-bird" }'
```
```json
{ "status": "ok", "student_email": "buyer@example.com", "tags_added": ["vip", "early-bird"] }
```

### 5. Remove a student from a course (POST)

```bash
curl -s -X POST "https://api.xperiencify.io/api/public/student/course/remove/?api_key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "student_email": "buyer@example.com", "course_id": 12345 }'
```
```json
{ "status": "ok", "student_email": "buyer@example.com", "course_id": 12345, "removed": true }
```

## Pagination

The documented account-level reads (`/coach/courses/`, `/coach/students/`) return collections; the
public docs do **not** specify a cursor/offset/page parameter or page-size cap. **Filter** `/coach/students/`
with `&course_id={id}` to scope the result to one course rather than pulling the whole roster.

<!-- Gap: pagination params are not documented. For large rosters, prefer the in-app CSV export
     (Students page → export, filterable by affiliate/course) over paging the API, and re-verify
     whether a `page`/`cursor` param exists before building a paginated sync. -->

## Error handling & rate limits

The public docs do **not** publish an error-response schema, HTTP status conventions, or rate-limit
headers. Defensive pattern:

```python
import requests, time

def xp_post(path, api_key, payload, retries=4):
    url = f"https://api.xperiencify.io{path}?api_key={api_key}"
    for attempt in range(retries):
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** attempt)          # exponential backoff: 1s, 2s, 4s, 8s
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()

# Enroll a buyer
xp_post("/api/public/student/create/", "YOUR_API_KEY",
        {"student_email": "buyer@example.com", "first_name": "Sam", "course_id": 12345})
```

<!-- Gap: error shape and rate limits undocumented. Treat any non-2xx as retryable for 429/5xx and
     fatal otherwise; verify actual status codes against live responses. -->

## Webhook export (outbound)

Xperiencify can **export student data to a webhook** (Help Center → "Export Student data to Webhook").
In practice the eventing surface is exposed through **Zapier triggers** (below) — Xperiencify POSTs the
student record to the configured URL when the event fires. There is **no published HMAC signature
scheme** for these webhooks; validate by checking the student exists via `GET /coach/students/` or
`POST /student/info/` before granting downstream access, and/or restrict your listener to a secret URL.

<!-- Constructed from docs — verify against live API -->
```json
{
  "event": "student_completed_course",
  "student_email": "buyer@example.com",
  "first_name": "Sam",
  "last_name": "Rivera",
  "course_id": 12345,
  "completion_percent": 100,
  "xp_earned": 1200
}
```

## Zapier automation surface

Xperiencify works as **both a trigger app and an action app** on Zapier (also available on Pabbly and
Make). Use this when you don't want to call the REST API directly.

**Triggers (4):**
1. **Student Added to Course** — fires when a new student is added to a course.
2. **Removed (Canceled) Subscription** — fires when a subscription is cancelled by the customer at Stripe.
3. **Student Completed Course** — fires when a student completes a course.
4. **Tag Added to a Student** — fires when a tag is added to a student.

**Actions (8):**
1. **Add Tag to Student**
2. **Add Student to a Course** (creates the student in the course)
3. **Remove Student From a Specific Course**
4. **Remove Student From All Courses**
5. **Remove Tag From Student**
6. **Suspend Student From Course**
7. **Unsuspend Student From Course**
8. **Update Student Custom Fields**

> Note the Zapier action set is slightly **broader** than the documented REST API — Suspend/Unsuspend
> are exposed on Zapier; confirm whether equivalent REST endpoints exist before assuming API parity.

## Gaps / not documented

- No published pagination params for `/coach/students/` and `/coach/courses/`.
- No published error-response schema, status-code conventions, or rate-limit headers.
- No published webhook signature/verification scheme.
- No OpenAPI/Swagger spec or Postman collection found at capture time (the Zapier/Pabbly/Pipedream
  connectors are the most reliable third-party documentation of the action surface).
- No MCP server found.
