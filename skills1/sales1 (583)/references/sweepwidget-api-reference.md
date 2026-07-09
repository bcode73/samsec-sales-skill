<!-- Source: https://sweepwidget.com/docs/sweepwidget-api and https://sweepwidget.com/docs/webhooks (captured 2026-07-05) -->

# SweepWidget API Reference

Captured from the SweepWidget API documentation and Webhooks Integration Guide. Request/response examples are reproduced from the docs; some field values are illustrative examples from the docs themselves. Verify exact schemas against the live docs / your account (the API + server-side webhooks are **Enterprise-plan-only**).

## Authentication & base URL

**Base URL:** `https://sweepwidgetapi.com/sw_api/`

Obtain your API key from **Integrations → API Access** in your dashboard. Send it as a Bearer token:

```
Authorization: Bearer YOUR_API_KEY
```

Alternatively, pass `api_key` as a **query parameter** (GET) or **form field** (POST).

- **GET requests:** parameters as query-string values.
- **POST requests:** parameters in the request body as JSON with `Content-Type: application/json`.

**Pagination:** list endpoints return **50 rows per page**; navigate with the `page_start` parameter. Loop until a page returns fewer than 50 rows.

### Auth quick-start (simplest GET)

```bash
curl -i -H "Authorization: Bearer $SWEEPWIDGET_API_KEY" \
  "https://sweepwidgetapi.com/sw_api/giveaways?type=live&page_start=1"
```

---

## Read endpoints (GET)

### List all users for a giveaway — `GET /users`

```
GET https://sweepwidgetapi.com/sw_api/users?page_start=1&competition_id=123
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
{
  "data": [
    {
      "user_id": 123,
      "user_name": "Test User",
      "user_email": "jane@example.com",
      "birthday": "04-25-1994",
      "custom_identifier": "your-reference-id",
      "entry_type": "Twitter Follow",
      "timestamp": "2020-06-26 11:18:21",
      "country": "United States"
    }
  ]
}
```

### List all winners for a giveaway — `GET /winners`

```
GET https://sweepwidgetapi.com/sw_api/winners?page_start=1&competition_id=123
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
{
  "data": [
    {
      "user_id": 123,
      "user_name": "Test User",
      "user_email": "jane@example.com",
      "birthday": "04-25-1994",
      "custom_identifier": "your-reference-id",
      "country": "United States"
    }
  ]
}
```

### List all entries for a giveaway — `GET /entries`

```
GET https://sweepwidgetapi.com/sw_api/entries?page_start=1&competition_id=123
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
{
  "data": [
    {
      "user_id": 123,
      "user_name": "Test User",
      "user_email": "jane@example.com",
      "birthday": "04-25-1994",
      "custom_identifier": "your-reference-id",
      "entry_type": "Twitter Follow",
      "action": "Follow @SweepWidget On Twitter",
      "value": "@MyTwitter",
      "entry_amount": "5",
      "timestamp": "2020-06-26 11:18:21",
      "country": "United States"
    }
  ]
}
```

### List all giveaways — `GET /giveaways`

```
GET https://sweepwidgetapi.com/sw_api/giveaways?type=live&page_start=1
Authorization: Bearer YOUR_API_KEY
```

`type` can be `live`, `scheduled`, or `expired`. Response:

```json
{
  "data": [
    {
      "competition_id": 123,
      "competition_url": "ahej14f9",
      "type": "Live",
      "title": "My Giveaway Title",
      "description": "This is the description of my awesome giveaway!",
      "rules": "US, CA, 18+",
      "start_time": "2020-07-28 00:00:00",
      "end_time": "2020-08-28 00:00:00",
      "time_zone": "America/Chicago",
      "number_of_winners": "5",
      "image_loc": "https://sweepwidget.com/images/my-image.jpg",
      "giveaway_embed_code": "PGRpdiBpZD0i..."
    }
  ]
}
```

### List all entries for a single user — `GET /user-entries`

```
GET https://sweepwidgetapi.com/sw_api/user-entries?competition_id=123&user_email=test@example.com
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
[
  {
    "entry_type": "User Details",
    "action": "Login",
    "value": "Auto Verified",
    "entry_amount": 1,
    "timestamp": "2024-02-29 15:13:51"
  },
  {
    "entry_type": "Instagram Follow",
    "action": "NULL",
    "value": "Test",
    "entry_amount": 1,
    "timestamp": "2024-03-01 19:44:58"
  }
]
```

### List all giveaways a user has entered — `GET /user-entered-giveaways`

```
GET https://sweepwidgetapi.com/sw_api/user-entered-giveaways?search_value=123&search_key=user_id
Authorization: Bearer YOUR_API_KEY
```

Response:

```json
{
  "competition_id": [ "20234", "20165", "20137", "20108" ]
}
```

### Fetch referral link for a user — `GET /fetch-user-referral-link`

```
GET https://sweepwidgetapi.com/sw_api/fetch-user-referral-link?competition_id=123&user_email=test@example.com
Authorization: Bearer YOUR_API_KEY
```

---

## Write endpoints (POST)

### Enter user into a giveaway — `POST /new-entry`

```
POST https://sweepwidgetapi.com/sw_api/new-entry
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 123,
  "user_email": "jane@example.com",
  "user_name": "Jane",
  "entry_amount": 1,
  "giveaway_link": "https://yoursite.com"
}
```

### Add manual entries for a user — `POST /add-manual-entries`

```
POST https://sweepwidgetapi.com/sw_api/add-manual-entries
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 123,
  "entry_amount": 1,
  "user_email": "jane@example.com"
}
```

### Create a giveaway — `POST /create-giveaway`

```
POST https://sweepwidgetapi.com/sw_api/create-giveaway
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "title": "Summer Giveaway 2026",
  "start_time": "2026-03-01 00:00:00",
  "end_time": "2026-03-31 23:59:59",
  "time_zone": "America/New_York",
  "description": "Enter to win amazing prizes this summer!",
  "number_of_winners": 3,
  "language": "en",
  "buttons_background_color": "4CAF50",
  "title_font_color": "222222"
}
```

Response:

```json
{
  "message": "Successfully created giveaway.",
  "competition_id": 12345,
  "competition_url": "a1b2c3d4",
  "giveaway_link": "https://sweepwidget.com/view/12345-a1b2c3d4",
  "embed_code": "<div id=\"12345-a1b2c3d4\" class=\"sw_container\"></div><script type=\"text/javascript\" src=\"https://sweepwidget.com/w/j/w_init.js\"></script>"
}
```

### Update a giveaway — `POST /update-giveaway`

```
POST https://sweepwidgetapi.com/sw_api/update-giveaway
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 12345,
  "title": "Updated Giveaway Title",
  "end_time": "2026-04-15 23:59:59",
  "buttons_background_color": "FF5722"
}
```

Response:

```json
{ "message": "Successfully updated giveaway 12345." }
```

### Delete a giveaway — `POST /delete-giveaway`

```
POST https://sweepwidgetapi.com/sw_api/delete-giveaway
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{ "competition_id": 12345 }
```

Response:

```json
{ "message": "Successfully deleted giveaway 12345." }
```

### Add a prize to a giveaway — `POST /create-prize`

```
POST https://sweepwidgetapi.com/sw_api/create-prize
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 12345,
  "prize_name": "$100 Amazon Gift Card",
  "prize_winners_allowed": 1,
  "prize_value": "100.00",
  "prize_currency": "USD"
}
```

Response:

```json
{
  "message": "Successfully added prize to competition id: 12345",
  "prize_id": 1,
  "prize_order": 1
}
```

### Add an unlock reward to a giveaway — `POST /create-reward`

```
POST https://sweepwidgetapi.com/sw_api/create-reward
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 12345,
  "unlock_rewards_type": 2,
  "unlock_rewards_title": "10% Off Coupon",
  "unlock_rewards_entries_required": 5,
  "unlock_rewards_coupon_code": "SAVE10",
  "unlock_rewards_coupon_directions": "Use code SAVE10 at checkout.",
  "unlock_rewards_if_send_email": 2
}
```

Response:

```json
{
  "message": "Successfully added reward to competition id: 12345",
  "unlock_rewards_id": 1,
  "unlock_rewards_order": 1
}
```

### Add new entry method — `POST /create-entry-method`

```
POST https://sweepwidgetapi.com/sw_api/create-entry-method
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 123,
  "entry_order": 5,
  "entry_method_type": "facebook_page_visit",
  "entry_method_handle": "Visit Us On Facebook",
  "mandatory": 0,
  "entries_worth": 10,
  "entry_link": "https://facebook.com/SweepWidget",
  "input_header": "Visit and follow SweepWidget on Facebook by manually clicking on the button below.",
  "widget_display": 1,
  "icon_color": "#3b5998",
  "require_verification": 1,
  "language": "en"
}
```

### Update an entry method — `POST /update-entry-method`

```
POST https://sweepwidgetapi.com/sw_api/update-entry-method
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "competition_id": 123,
  "entry_method_id": 5,
  "entries_worth": 20,
  "entry_method_handle": "Follow Us On Instagram",
  "mandatory": 1
}
```

Response:

```json
{ "message": "Successfully updated entry method 5 for competition id: 123" }
```

### Delete an entry method — `POST /delete-entry-method`

```
POST https://sweepwidgetapi.com/sw_api/delete-entry-method
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{ "competition_id": 123, "entry_method_id": 5 }
```

Response:

```json
{ "message": "Successfully deleted entry method 5 from competition id: 123" }
```

### Update whitelisted emails — `POST /white-list-emails`

```
POST https://sweepwidgetapi.com/sw_api/white-list-emails
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "global": 0,
  "competition_id": 123,
  "whitelisted_emails": ["a@example.com", "b@example.com", "c@example.com"]
}
```

---

## Endpoint summary

| Method | Path | Purpose |
|---|---|---|
| GET | `/users` | List users for a giveaway |
| GET | `/winners` | List winners for a giveaway |
| GET | `/entries` | List entries for a giveaway |
| GET | `/giveaways` | List giveaways (`type=live`/`scheduled`/`expired`) |
| GET | `/user-entries` | List a single user's entries |
| GET | `/user-entered-giveaways` | List giveaways a user entered |
| GET | `/fetch-user-referral-link` | Fetch a user's referral link |
| POST | `/new-entry` | Enter a user into a giveaway |
| POST | `/add-manual-entries` | Add manual entries for a user |
| POST | `/create-giveaway` | Create a giveaway |
| POST | `/update-giveaway` | Update a giveaway |
| POST | `/delete-giveaway` | Delete a giveaway |
| POST | `/create-prize` | Add a prize |
| POST | `/create-reward` | Add an unlock reward / coupon |
| POST | `/create-entry-method` | Add an entry method |
| POST | `/update-entry-method` | Update an entry method |
| POST | `/delete-entry-method` | Delete an entry method |
| POST | `/white-list-emails` | Update whitelisted emails |

---

## Webhooks

Two notification methods (both fire on identical events with matching data structures):

1. **Server-side webhooks** — HTTP POST from SweepWidget to your HTTPS endpoint. Best for backend/CRM sync. **Enterprise-plan-only.**
2. **Client-side JavaScript callbacks** — browser events on the page where the widget is embedded. Best for frontend tracking/analytics. Available without Enterprise.

### Setup

Integrations → **Webhooks** card → enter your **HTTPS** endpoint URL → Save. A **signing secret** is generated automatically on first save; copy it to verify signatures. Use **Send Test** to send a test payload.

### Events

- `entry_submitted` — user completes the initial entry form
- `task_completed` — a bonus-entry task is finished (includes task details + remaining-task counts)
- `all_entries_completed` — every available task is done

### Payload (`entry_submitted`)

```json
{
  "event": "entry_submitted",
  "data": {
    "competition_id": "12345",
    "user": { "email": "jane@example.com", "name": "Jane Smith" },
    "entries": 5,
    "referral_url": "https://sweepwidget.com/c/my-giveaway-abc123"
  }
}
```

### Signature verification

Requests include the header `X-SweepWidget-Signature` containing an HMAC-SHA256 hash prefixed with `sha256=`. Compute a matching hash using your **signing secret** and the **raw request body**, then constant-time compare.

```python
import hmac, hashlib

def verify(raw_body: bytes, header: str, secret: str) -> bool:
    sent = header.split("=", 1)[1] if "=" in header else header   # strip 'sha256='
    digest = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, sent)
```

### Client-side JavaScript callback

```javascript
window.addEventListener('sweepwidget.entry_submitted', function (e) {
  console.log(e.detail.user.email);
});
```

Fires the same three events client-side; use for pixels/analytics/UI, not as a trusted server signal.

---

## Gaps / verify against live docs

- **Rate limits:** third-party sources mention ~60 calls/minute for some SweepWidget interfaces, but the published API docs page did not state an explicit rate-limit header or retry policy — confirm in-account. <!-- Constructed note — verify against live API -->
- **Error response shape:** the docs show success `message` envelopes; the exact 4xx/5xx error JSON was not published — capture a real failure to confirm.
- **`page_start` semantics:** examples use `page_start=1` (page number, 50/page). Confirm whether it's 1-indexed page number vs row offset against a live paged response.
- **Enterprise gate:** API access + server-side webhooks are Enterprise-only per the pricing comparison; confirm your plan before building.
