<!-- Source: https://support.ruzuku.com/article/796-how-to-set-up-your-zapier-intergration -->
<!-- Source: https://support.ruzuku.com/article/990-zapier-integration -->
<!-- Source: https://zapier.com/apps/ruzuku/integrations -->
<!-- Source: https://www.ruzuku.com (pricing/features) -->

# Ruzuku Integration & API Reference

> **There is no documented public REST API for Ruzuku.** Ruzuku is a no-code course platform; the supported programmatic surface is **Zapier** (triggers + actions). A REST API exists *internally* — Zapier authenticates with an **API Key + API Secret + Site URL** — but Ruzuku does not publish endpoint documentation, so build against Zapier, not raw HTTP. Everything below was captured from Ruzuku's own Zapier setup docs and the Zapier app listing. Where exact payload keys weren't documented, that is flagged — nothing is invented.

## Integration surface at a glance

| Mechanism | Direction | Use it for |
|---|---|---|
| **Zapier triggers** | Ruzuku → external | Enrollment, lesson/course completion, quiz/assignment submission, comments, cancellations |
| **Zapier actions** | external → Ruzuku | Enroll, unenroll, or find a student |
| **Webhooks by Zapier** | Ruzuku → external (custom) | Bridge to systems with no native Zapier app (POST event JSON to your endpoint) |
| **Native: Stripe / PayPal** | into Ruzuku | Payment processing, 0% Ruzuku fee |
| **Native: Zoom** | bidirectional | Live webinars/classes (Pro plan) |

**No public REST API docs. No native inbound/outbound webhook product feature. No MCP server.**

## Authentication (Zapier connection)

To connect Ruzuku to Zapier you generate a credential triple in-app:

1. Go to **Account → Integrations → Configure Zapier**.
2. Generate your **API Key**, **API Secret**, and note your **Site URL**.
3. Enter all three when adding the Ruzuku connection in Zapier.

> The credential is used **once** in Zapier but you need it again to **reconnect** — store the API Key + API Secret securely (they authorize student writes). The Zapier integration is **free on every Ruzuku plan**, including Free.

There is no documented Bearer/OAuth scheme for direct API calls — the Key/Secret/Site-URL triple is consumed by Zapier's connection layer, and Ruzuku does not publish the underlying request format.

## Zapier triggers (events Ruzuku emits)

Each trigger provides the student's **name and email** plus course context, with filtering by specific course or lesson.

1. **New Student Enrolled** — fires on enrollment; includes **pricing and coupon** information (the coupon/price-point is how affiliate referrals are attributed).
2. **Lesson Completed** — a student finishes a selected lesson.
3. **Course Completed** — a student finishes all lessons in a course.
4. **Quiz Submitted** — includes the student's **score**.
5. **Assignment Submitted** — includes the student's **answers**.
6. **Comment Posted** — lesson/discussion activity.
7. **Subscription Canceled** — a recurring payment is canceled.

## Zapier actions (writes into Ruzuku)

1. **Enroll a Student** — adds a student to a course; **creates their account automatically if they don't already have one**.
2. **Unenroll a Student** — removes a student's access to a course.
3. **Find a Student** — searches for a student by **email or ID** (use as a search step before another action).

## Representative payloads

Reconstructed from the documented Zapier field lists — confirm exact keys in the Zapier editor before parsing.

```json
// New Student Enrolled
{
  "student": {
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
  },
  "course": "Signature Course",
  "price": 197.00,
  "coupon": "AFFILIATE-MARIA"   // present when a coupon/price-point link was used
}
```
<!-- Constructed from docs — verify against the live Zapier app -->

```json
// Quiz Submitted
{
  "student": { "email": "jane@example.com" },
  "course": "Signature Course",
  "lesson": "Module 2 Quiz",
  "score": 8
}
```
<!-- Constructed from docs — verify against the live Zapier app -->

```json
// Enroll a Student (action input)
{
  "email": "jane@example.com",     // required — identity; account created if new
  "first_name": "Jane",
  "last_name": "Doe",
  "course": "Signature Course"      // the target course
}
```
<!-- Constructed from docs — verify against the live Zapier app -->

## Bridging to non-native systems (Webhooks by Zapier)

When the destination (or source) has no native Zapier app, chain **Webhooks by Zapier**:

- **Outbound:** Ruzuku trigger → *Webhooks by Zapier: POST* → your endpoint receives the event JSON.
- **Inbound:** your system → *Webhooks by Zapier: Catch Hook* → *Ruzuku: Enroll a Student*.

```bash
# Inbound example: a custom cart POSTs a sale to a Zapier Catch Hook,
# whose next step is the Ruzuku "Enroll a Student" action.
curl -X POST "https://hooks.zapier.com/hooks/catch/XXXXX/yyyyy/" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","first_name":"Jane","last_name":"Doe","course":"Signature Course"}'
```

> There is **no signing secret** on these hooks — keep the catch-hook URL private and treat inbound payloads as untrusted.

## Auth, pagination, rate limits

- **Auth:** API Key + API Secret + Site URL, consumed by the Zapier connection. No documented direct-HTTP auth scheme.
- **Pagination:** N/A — there is no list/read REST API. Use **Find a Student** (single lookup) in Zapier, or the **in-app CSV export** for bulk student/enrollment data.
- **Rate limits:** none documented on Ruzuku's side; throughput is governed by your **Zapier plan's** task limits, not Ruzuku.

## Gaps

- No published REST endpoint reference, base URL, or error-response schema — the internal API that Zapier uses is undocumented for public use.
- Exact Zapier payload field keys (e.g. whether it's `student.email` vs `email`, `course` vs `course_name`) are not published — confirm in the Zapier editor's sample data.
- No native webhooks, no MCP server, no Make/n8n first-party modules documented (reach those via Webhooks by Zapier or community connectors).
- For any need beyond enroll/unenroll/find + lifecycle triggers (e.g. reading lesson content, editing courses, querying revenue), there is no programmatic path — it's UI-only.
