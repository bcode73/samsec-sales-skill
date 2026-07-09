<!-- Source: https://help.graphy.com/support/solutions/articles/1060000131907-how-to-integrate-webhooks-within-your-course-platform- -->
<!-- Source: https://us.help.graphy.com/support/solutions/articles/1060000131905-how-to-use-apis-to-get-data-from-your-graphy-course-platform- -->
<!-- Source: https://documenter.getpostman.com/view/15796483/Tzz5vKKr (canonical REST API — JS-rendered) -->
<!-- Source: https://apitracker.io/a/graphy -->

# Graphy API & Webhook Reference

> **Accuracy note (research baseline 2026-06-22).** Graphy's canonical REST API docs live in a **Postman collection that is JavaScript-rendered** and did not return content to WebFetch. The auth model, plan gating, the iPaaS operation names, and the full webhook trigger list below were captured verbatim from Graphy's help center and integration listings. **The exact REST base URL and endpoint paths must be read from the Postman collection or your in-account Integration API page** — they are not reproduced here because they could not be captured verbatim, and this skill does not invent API details. Graphy was formerly **Spayee**.

## REST API

### Availability (plan gate)
**API access is gated to the Advanced/Scale (top) plan.** On lower tiers the Integration API menu / credentials are not available — integrate via webhooks + Zapier/Pabbly instead.

### Authentication
Each API call is secured with two credentials:
- **Merchant Id (MID)**
- **API token (key)**

**Where to find them:** log into the Graphy dashboard → **Integration API** (menu bar); the MID + API key appear in the right-hand panel.

> Treat the API key as a secret. The exact header/param names for passing MID + key are defined in the Postman collection — confirm there before building.

### Canonical docs
- Postman: `https://documenter.getpostman.com/view/15796483/Tzz5vKKr` (and an older collection `.../view/10740263/Szt8eA1V`).
- An OpenAPI/Swagger spec is referenced by third-party trackers but not publicly confirmed.

### Operations confirmed via iPaaS (Zapier / Pabbly)
These actions are exposed and are the most common automation use cases (the REST equivalents live in the Postman collection):
- **Create Learner** — create a learner/user record.
- **Enroll Learner to Course** — enroll by mapping the learner's **email** to a **course URL**.
- Read/"get data" endpoints exist for learners, enrollments, courses, and transactions (per the help-center "How to use APIs to get data" article) — confirm exact paths in Postman.

### Pagination / rate limits
Not documented in captured sources. Assume undocumented limits: batch writes, add retry/backoff, and avoid tight loops. Confirm in Postman / with support before high-volume syncs.

## Webhooks

**Setup:** Dashboard → **Integrations → Webhooks → New Webhook** → enter the third-party webhook URL, add a description, select one or more event triggers, Save.

**Reliability behavior (important):**
- **If a webhook fails 5 times, it is automatically disabled.** Monitor your endpoint's uptime and re-enable after fixing.
- Only the webhook's **status and URL** can be edited after creation.
- Deleting a webhook removes the webhook but **keeps its logs**.

### Webhook triggers (verbatim)

1. **New Learner Created** — "When a new learner signs up on your platform"
2. **New Enrollment** — "When a user purchases your course/package"
3. **New Course Published** — "Whenever a new course is published on the course platform"
4. **Course Completion** — "When a learner completes any of your courses"
5. **Course Item Completion** — "When a learner completes an item of your course"
6. **Learner Profile Updated** — "Whenever a learner's information is updated within the platform"
7. **New Subscriber** — "When a new user subscribes to your course platform"
8. **Success Transaction** — "When the process of the course purchase transaction is complete"
9. **Init Transaction** — "When the learner has initiated the transaction for purchasing the course"
10. **AI Agent** — priority learner concerns (surfaces AI-agent escalations)

> **Payload schemas / signature:** the help center does **not** publish per-event JSON payloads or a signing/HMAC scheme. Capture one real delivery against a request bin (e.g. webhook.site) to learn the exact field keys, and verify whether a shared secret/signature is available before trusting payloads.

## Native integrations

Zapier, Pabbly Connect, Webhooks, API, Zoom, Mailchimp, Facebook Pixel, Google Tag Manager. **No MCP server.**

## cURL example (representative — confirm exact endpoint in Postman)

Because the verbatim base URL/paths weren't captured, this shows the *shape* of an authenticated call, not a guaranteed contract:

```bash
# Confirm base URL, path, and how MID + key are passed in the Postman collection.
curl -X POST "https://<graphy-api-base>/<create-learner-path>" \
  -H "Content-Type: application/json" \
  -H "mid: <MERCHANT_ID>" \
  -H "key: <API_KEY>" \
  -d '{"email":"learner@example.com","name":"New Learner"}'
```

## Data model (representative — confirm in Postman)

```json
// Learner
{ "email": "learner@example.com", "name": "New Learner" }   // email is the identity key

// Enrollment (maps a learner to a course)
{ "learner_email": "learner@example.com", "course_url": "https://you.graphy.com/courses/..." }

// Transaction (surfaced via Init/Success Transaction webhooks)
{ "learner_email": "learner@example.com", "status": "success", "amount": 4900, "currency": "USD" }
```

## Notes that matter for integrations

- **API is top-plan only** — if a user is on Launch/Rise, the supported path is webhooks + Zapier/Pabbly, not REST.
- **Email is the learner identity** — Create Learner + Enroll Learner to Course both key on email; dedupe on it.
- **Use `Success Transaction` (not `Init Transaction`) to fulfill** — Init fires when checkout starts, Success when payment completes. Granting access on Init = giving away product to abandoned carts.
- **The 5-failures-auto-disable rule** is the #1 silent breakage: a flaky endpoint quietly turns the webhook off.
