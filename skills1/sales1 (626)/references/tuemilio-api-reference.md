<!-- Source: https://docs.tuemilio.com/api/ (REST), https://docs.tuemilio.com/javascript-api/ (JS SDK), https://docs.tuemilio.com/webhooks/ (webhooks) — fetched 2026-06 -->

# Tuemilio API Reference

Tuemilio exposes three programmatic surfaces: a **REST API** (server-side), a **JavaScript SDK** (browser/frontend), and **Webhooks** (egress). Per the docs: **"Never expose or use the REST API on your frontend, for that use the Javascript API."**

---

## REST API

### Base URL
`https://tuemilio.com/api/v1`

### Authentication
API token is passed as a **query parameter** on every request:
```
?api_token=XXXXXXXX-XXX-XXX-XXX-XXXXXXXXXXXX
```
Get your token at `https://tuemilio.com/profile#api-token`. List IDs are at `https://tuemilio.com/profile#list-ids`.

⚠️ Server-side only — the token is a secret. Because it rides in the URL, keep it out of browser code, logs, and `Referer` headers.

### Auth quick-start (cURL — simplest GET)
```bash
curl "https://tuemilio.com/api/v1/lists?api_token=$TUEMILIO_TOKEN"
```

### Emails endpoints

#### Get All Emails — `GET /lists/{LIST_ID}/emails`
Retrieves emails from a waitlist in descending creation order.
- `list_id` (required)

Response:
```json
[
  {
    "id": 111,
    "address": "hello@mail.com",
    "ip": "111.170.111.12",
    "points": 1,
    "anti_points": 0,
    "source": "email-form",
    "referrer_id": 109,
    "referrer_url": "https://instagram.com/",
    "subscribed": 1,
    "click_time": 5,
    "created_at": "2020-06-21 16:42:13",
    "blocked": 0,
    "custom_fields": [],
    "shared_on": [],
    "dashboard_link": "https://yourpage.com?email=hello@mail.com"
  }
]
```

#### Get Single Email — `GET /lists/{LIST_ID}/emails` (with `address`) or `GET /lists/{LIST_ID}/emails/{EMAIL_ID}`
- `list_id` (required), and `address` (required) OR `email_id` (required)

Response:
```json
{
  "address": "hello@mail.com",
  "ip": "192.164.102.13",
  "source": "api",
  "referrer_id": 0,
  "custom_fields": null,
  "points": 1,
  "created_at": "2020-11-09 20:24:09",
  "id": 1112,
  "position": 186,
  "position_ordinal": "186th",
  "people_ahead": 185,
  "dashboard_link": "https://yourapp.com?email=hellome@sdf.com",
  "referral_link": "https://yourapp.com?r=AvzMb",
  "referral_id": "AvzMb",
  "waiters": [
    { "address": "h××××@××××××××××××.com", "points": 0, "deleted_at": null, "position": 184 }
  ]
}
```

#### Create Email — `POST /lists/{LIST_ID}/emails`
Adds a new email. Automatically increments the referrer's points if `referrer_id` or `referral_id` is provided.
- `list_id` (required), `address` (required)
- `referral_id`: unique code from a referral link (the value after `?r=`)
- `referrer_id`: integer email ID of the referrer
- `custom_fields`: flat JSON object, e.g. `{"name": "rob", "age": 27}`
- `points`: initial points
- `ip`: subscriber's IP

Response: same shape as Get Single Email.

#### Update Email — `PUT /lists/{LIST_ID}/emails/{EMAIL_ID}`
- `list_id`, `email_id` (required); optional `address`, `points` (sets absolute value), `custom_fields`, `subscribed` (bool), `blocked` (bool)

Response: updated email object.

#### Delete Email — `DELETE /lists/{LIST_ID}/emails/{EMAIL_ID}`
- `list_id`, `email_id` (required). Response: `200 OK`.

#### Add Points to Email — `PUT /lists/{LIST_ID}/emails/{EMAIL_ID}/add-points`
**Additive** (not absolute): "If a user has 5 points and we pass `points = 2`, the user will be updated with a total of 7 points."
- `list_id`, `email_id`, `points` (required). Response: updated email object.

### Wait Lists endpoints

#### Get All Wait Lists — `GET /lists`
Response:
```json
[
  {
    "id": 724,
    "name": "Watape",
    "host": "https://voxremover.com/hardware-on-the-cloud",
    "created_at": "2020-06-21 08:03:47",
    "emails_count": 194,
    "visits_count": 2124,
    "unique_visits": 1599,
    "conversion": 0.12,
    "referrals_count": 20,
    "uuid": "98f5535f-32bc-425c-a3d1-af950f8ac4e6"
  }
]
```

#### Get Single Wait List — `GET /lists/{LIST_ID}`
- `list_id` (required). Response: a single object with the same shape as above.

### Pagination / rate limits / errors
Not documented. Treat `GET /emails` as returning the full list (descending by `created_at`) — verify volume behavior on large lists before relying on it.

---

## JavaScript SDK

The Tuemilio script loads globally and powers the form, dashboard modal, and referral widget. **Use this on the frontend — not the REST API.**

### Install / initialize (React/Next.js — guard for SSR)
```javascript
import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (function(t,u,e,m,i,l,io){
        t['TuemilioObject']=m;t[m]=t[m]||function(){(t[m].q=t[m].q||[]).push(arguments);};
        t[m].id='XXXXXXXXX';l=u.createElement(e),io=u.getElementsByTagName(e)[0];
        l.id=m;l.src=i;l.async=1;io.parentNode.insertBefore(l,io);
      }(window,document,'script','Tuemilio','https://tuemilio.com/assets/js/modal/4.0/tuemilio-modal.js'));
      Tuemilio('init', {});
      Tuemilio('sendVisit');
    }
  }, []);

  return <div className="t-signup"></div>;
}
```
Replace `XXXXXXXXX` with your **Widget List UUID**.

### Core methods
- `Tuemilio('init', configObject)` — required; enables all widget components
- `Tuemilio('sendVisit')` — logs a visit
- `Tuemilio('createSubscriber', { address: 'email@example.com', referralId: 'optional' })`
- `Tuemilio('getDashboard', { address: 'email@example.com' })`
- `Tuemilio('showDashboard')` / `Tuemilio('closeModal')`
- `Tuemilio('redirect', url)` / `Tuemilio('confetti')`

### Config object
```javascript
let configObject = {
  form: { disabled: false, loginFormOnUserIdentified: false, forceLoginForm: false, style: { inline: false } },
  dashboard: {
    type: 'modal', // or 'page'
    disabled: false, hideButton: false, loadOnUserIdentified: true,
    modal: { preventShowAfterSubscribing: false, preventShowAfterLogin: false },
    listAnimation: true,
    survey: { secondURL: 'https://...' }
  },
  cookies: { disabled: false },
  user: { identified: false },
  confetti: { disabled: false }
};
```

### Event listeners
```javascript
Tuemilio('onVisitCreated', function(visit) {});
Tuemilio('onSubscriberCreated', function(subscriber) {});      // new signup
Tuemilio('onSubscriberIdentified', function(subscriber) {});   // returning user
Tuemilio('onSubscriberUnidentified', function() {});
Tuemilio('onDashboardData', function(dashboard) {});           // build a custom dashboard
Tuemilio('onDashboardShown', function() {});
Tuemilio('onDashboardClosed', function() {});
Tuemilio('onSurveySubmitted', function() {});
Tuemilio('onInvalidEmail', function(input) {});
Tuemilio('onEmptyEmail', function() {});
Tuemilio('onError', function(error) {});
```

### Returned objects
- **Subscriber**: `id`, `address`, `points`, `created_at`, `referrer_id`, `dashboard_link`, surveys array
- **Dashboard**: subscriber data, `referreds` array, `position`, `subscriber_count`, leaderboard (`waiters`), social shares, config, point rates
- **Visit**: `ga_enabled`, `redirect_url`, `redirect` flag, nested subscriber data

---

## Webhooks

After adding a webhook URL, Tuemilio pings it on the events you subscribe to.

### Events
| Event | Fires when |
|---|---|
| `new-subscriber` | A new subscriber joins the waitlist |
| `grant-access` | Access is granted to subscribers (frequency / batch size configurable) — wire launch automation here |
| `confirmed-subscriber` | A subscriber verifies their email (requires confirmation-email automation enabled) |

### Request format
- **Method:** POST · **Content-Type:** `application/json`
- **Header:** `X-Tuemilio-Event` (identifies the event type)
- **User-Agent:** `Tuemilio-Hookshot/1.0`

### Payload schema (subscriber data)
Core: `id`, `address`, `ip`, `position`, `points`, `anti_points`, `source`. Referral: `referrer_id`, `referrer_url`, `referral_link`, `referral_id`. Status: `subscribed`, `blocked`, `fraud_id`, `created_at`. Links: `dashboard_link`, `referral_link`. Nested: `referrer` (object), `waiters` (array). Additional fields vary by event type.

```json
<!-- Representative shape assembled from the documented field list — verify against a live delivery. -->
{
  "id": 1112,
  "address": "hello@mail.com",
  "ip": "192.164.102.13",
  "position": 186,
  "points": 1,
  "anti_points": 0,
  "source": "email-form",
  "referrer_id": 109,
  "referrer_url": "https://instagram.com/",
  "referral_link": "https://yourapp.com?r=AvzMb",
  "referral_id": "AvzMb",
  "subscribed": 1,
  "blocked": 0,
  "fraud_id": null,
  "created_at": "2026-06-19 12:00:00",
  "dashboard_link": "https://yourapp.com?email=hello@mail.com",
  "referrer": {},
  "waiters": []
}
```

### Verification / retries
No signing/HMAC or retry policy is documented. Identify the event via `X-Tuemilio-Event`, use an unguessable webhook URL, validate the `User-Agent`, and dedupe on subscriber `id`.

---

## Integrations (non-API)
- **Zapier** — 3,000+ apps; trigger: New Subscriber.
- **Mailchimp** — automatic subscriber sync.
- **Typeform** — interactive surveys.
- **Google Analytics** — events sent automatically (`ga_enabled` on the visit object).
- **MCP server:** none found.

## Gaps (not documented — verify before relying)
- Pagination, rate limits, and error response shapes for the REST API.
- Webhook signing/verification and retry/timeout behavior.
- Full JSON for the JS SDK returned objects (field-level).
