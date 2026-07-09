<!-- Source: https://waitlister.me/docs/api, https://waitlister.me/docs/api/authentication, https://waitlister.me/docs/api/rate-limits, https://waitlister.me/docs/api/endpoints, https://waitlister.me/docs/api/endpoints/subscribers/add-subscriber, https://waitlister.me/docs/api/endpoints/subscribers/list-subscribers, https://waitlister.me/docs/api/endpoints/subscribers/update-subscriber, https://waitlister.me/docs/webhooks — captured 2026-06-06 -->

# Waitlister API Reference

REST API around standard HTTP methods returning JSON. **API access and webhooks require the Growth plan ($49/mo) or above** — Free and Launch have no API.

- **Base URL**: `https://waitlister.me/api/v1`
- **Auth**: `X-Api-Key: your-api-key` header on every request. Generate under Integrations → API access → "Generate API key". Regenerating invalidates the previous key.
- **Content-Type**: `application/json`
- `{waitlist-key}` path parameter comes from waitlist settings.
- "Never expose your API key in client-side code" — server-side only.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/waitlist/{waitlist-key}/sign-up` | Add subscriber |
| GET | `/waitlist/{waitlist-key}/subscribers` | List subscribers (paginated) |
| GET | `/waitlist/{waitlist-key}/subscribers/{id-or-email}` | Get subscriber |
| PUT | `/waitlist/{waitlist-key}/subscribers/{id-or-email}` | Update subscriber (incl. `points`) |
| POST | `/waitlist/{waitlist-key}/log-view` | Log a page view (analytics) |

No delete endpoint is documented.

### Add subscriber — `POST /waitlist/{waitlist-key}/sign-up`

Request body:

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "metadata": {
    "referred_by": "happy-star-4f3d",
    "referring_domain": "google.com",
    "client_ip": "203.0.113.42",
    "fingerprint": "abc123def456",
    "custom_field_1": "value1"
  }
}
```

**Required:** `email` (String). **Optional:** `name`, `phone`, `metadata` object with referral and custom fields.

Notes from the docs:
- Include `metadata.referred_by` (the referrer's referral code) for referral tracking
- Forward `metadata.client_ip` and optional `metadata.fingerprint` from end users to enable **referral fraud protection on API sign-ups** — omit them and server-side signups bypass fraud detection
- Check `is_pending_confirmation` to determine the user-experience flow when double opt-in is enabled

cURL:

```bash
curl -X POST "https://waitlister.me/api/v1/waitlist/your-waitlist-key/sign-up" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: your-api-key" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe"
  }'
```

Success (200, no double opt-in):

```json
{
  "success": true,
  "is_new_sign_up": true,
  "is_pending_confirmation": false,
  "message": "Successfully signed up",
  "position": 42,
  "inflated_position": 42,
  "points": 50,
  "referral_code": "happy-star-4f3d",
  "sign_up_token": "abc123xyz",
  "redirect_url": "https://waitlister.me/thank-you/waitlist-key/abc123xyz"
}
```

Success (200, double opt-in enabled):

```json
{
  "success": true,
  "is_new_sign_up": true,
  "is_pending_confirmation": true,
  "message": "Please check your email to confirm your sign-up",
  "redirect_url": "https://waitlister.me/confirm-pending/waitlist-key/confirmation-token"
}
```

Errors:

```json
{ "statusCode": 400, "message": "Valid email is required" }
```

```json
{
  "statusCode": 429,
  "message": "Too many sign-up attempts. Please try again later.",
  "data": { "retry_after": 3600 }
}
```

### List subscribers — `GET /waitlist/{waitlist-key}/subscribers`

Query parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | Number | 20 | Results per request (max 100) |
| `page` | Number | 1 | Page number for pagination |
| `sort_by` | String | `date` | Field to sort: `position`, `points`, `date`, `referral_count`, `email` |
| `sort_dir` | String | `desc` | `asc` or `desc` |

```bash
curl "https://waitlister.me/api/v1/waitlist/your-waitlist-key/subscribers?limit=50&page=2&sort_by=points&sort_dir=desc" \
  -H "X-Api-Key: your-api-key"
```

Response (200):

```json
{
  "success": true,
  "data": {
    "subscribers": [
      {
        "id": "xyzABC123",
        "email": "user@example.com",
        "deliverability": "unconfirmed",
        "name": "John Doe",
        "phone": "+1234567890",
        "position": 42,
        "inflated_position": 42,
        "points": 150,
        "referral_code": "happy-star-4f3d",
        "referred_by": "cool-moon-9e2a",
        "referral_count": 3,
        "sign_up_token": "abc123xyz",
        "thank_you_url": "https://waitlister.me/thank-you/...",
        "metadata": {},
        "referring_domain": "twitter.com",
        "ip_address": "192.168.1.1",
        "country": "US",
        "city": "San Francisco",
        "timezone": "America/Los_Angeles",
        "joined_with": "api",
        "joined_at": 1682345678901
      }
    ],
    "total": 245,
    "page": 1,
    "limit": 20,
    "pages": 13
  }
}
```

### Update subscriber — `PUT /waitlist/{waitlist-key}/subscribers/{id-or-email}`

Updatable fields: `name` (String), `phone` (String), **`points` (Number)**, `metadata` (Object with custom fields).

- Metadata fields **merge** with existing data; omitted fields remain unchanged
- **Points can be adjusted to modify subscriber position** — this is the programmatic reward/position lever
- Lookup by email is case-insensitive

```bash
curl -X PUT "https://waitlister.me/api/v1/waitlist/your-waitlist-key/subscribers/xyzABC123" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: your-api-key" \
  -d '{
    "name": "Updated Name",
    "points": 200
  }'
```

Response (200):

```json
{
  "success": true,
  "message": "Successfully updated subscriber",
  "data": {
    "subscriber": {
      "id": "xyzABC123",
      "email": "user@example.com",
      "name": "Updated Name",
      "points": 200,
      "updated_at": 1682345678901
    }
  }
}
```

Errors: `404` "Subscriber not found", `400` "At least one field to update must be provided".

### Error shape & status codes

Success responses include `"success": true`. Error responses: `"success": false` with an error object containing `code` and `message` (per-endpoint examples above show `statusCode` + `message`). Standard codes: 200, 400 (bad request), 401 (invalid/revoked API key), 403 (plan lacks endpoint access), 404, 429 (rate limit), 500.

## Rate limits

| Plan | Subscriber endpoints | Log view |
|---|---|---|
| Free / Launch | **No API access** | — |
| Growth | 60 requests/minute | 200 requests/minute |
| Business | 120 requests/minute | 400 requests/minute |

Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (Unix timestamp of window reset). On 429, docs recommend exponential backoff up to a 30-second max delay across 5 attempts. Higher limits: Business tier or contact support for enterprise.

## Webhooks (Growth plan+)

Setup: Integrations → Webhooks → Manage → enter HTTPS endpoint URL, optional secret, select event types. Requirements: **HTTPS only**, respond within **15 seconds**, return a **2xx** status, handle retry deliveries (dedupe on delivery ID).

Headers on every delivery:

```
X-Webhook-Signature: sha256=your-computed-signature
X-Waitlister-Event: [event type]
X-Waitlister-Delivery: unique-delivery-id
X-Waitlister-Timestamp: ISO 8601 timestamp
```

Status management: **Active** (working) → **Inactive** (failed last test/delivery) → **Disabled** (automatically disabled after **10 consecutive failures**; requires manual re-enabling after fixing the endpoint).

### Event: `waitlist.signup_created`

```json
{
  "event": "waitlist.signup_created",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "id": "signup_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1 123 4567",
    "position": 42,
    "inflated_position": 42,
    "points": 50,
    "referral_code": "happy-star-4f3d",
    "referred_by": "friend-code-123",
    "signup_token": "abc123xyz789token",
    "thank_you_url": "https://waitlister.me/thank-you/your-waitlist-key/abc123xyz789token",
    "waitlist": {
      "key": "your-waitlist-key"
    },
    "metadata": {
      "referring_domain": "google.com",
      "user_agent": "Mozilla/5.0...",
      "source": "landing-page",
      "origin_url": "https://yoursite.com",
      "ip_address": "192.168.1.1",
      "city": "New York",
      "region": "NY",
      "country": "US",
      "timezone": "America/New_York",
      "custom_fields": {},
      "signup_date": 1642248600000
    }
  }
}
```

### Event: `waitlist.referral_completed`

```json
{
  "event": "waitlist.referral_completed",
  "timestamp": "2025-01-15T11:45:00Z",
  "data": {
    "referrer": {
      "id": "signup_abc123",
      "email": "referrer@example.com",
      "name": "Jane Doe",
      "points": 80,
      "position": 15,
      "inflated_position": 15,
      "total_referrals": 2,
      "referral_code": "happy-star-4f3d",
      "signup_token": "referrer_token_abc123"
    },
    "new_signup": {
      "id": "signup_xyz789",
      "email": "newuser@example.com",
      "name": "Bob Smith",
      "referred_by": "happy-star-4f3d",
      "signup_token": "newsignup_token_xyz789"
    },
    "points_earned": 30,
    "waitlist": {
      "key": "your-waitlist-key"
    }
  }
}
```

### Event: `waitlist.milestone_reached`

```json
{
  "event": "waitlist.milestone_reached",
  "timestamp": "2025-01-15T12:00:00Z",
  "data": {
    "subscriber": {
      "id": "signup_abc123",
      "email": "user@example.com",
      "name": "John Doe",
      "points": 100,
      "previous_points": 85,
      "position": 12,
      "inflated_position": 12,
      "referral_code": "happy-star-4f3d",
      "signup_token": "subscriber_token_def456"
    },
    "milestone": {
      "points": 100,
      "reached_at": 1642249200000
    },
    "waitlist": {
      "key": "your-waitlist-key"
    }
  }
}
```

### Event: `waitlist.subscriber_unsubscribed`

```json
{
  "event": "waitlist.subscriber_unsubscribed",
  "timestamp": "2025-01-15T14:30:00Z",
  "data": {
    "subscriber": {
      "id": "signup_abc123",
      "email": "user@example.com",
      "name": "John Doe",
      "phone": "+1 123 4567",
      "position": 42,
      "inflated_position": 42,
      "points": 80,
      "referral_code": "happy-star-4f3d",
      "signup_token": "abc123xyz789token",
      "signed_up_at": 1642248600000
    },
    "unsubscribe": {
      "source": "manual",
      "unsubscribed_at": 1642335000000
    },
    "waitlist": {
      "key": "your-waitlist-key"
    },
    "metadata": {
      "ip_address": "192.168.1.1",
      "city": "New York",
      "region": "NY",
      "country": "US",
      "custom_fields": {}
    }
  }
}
```

### Event: `waitlist.subscriber_pending_expired`

Fires when a double-opt-in confirmation times out.

```json
{
  "event": "waitlist.subscriber_pending_expired",
  "timestamp": "2025-01-15T16:00:00Z",
  "data": {
    "id": "pending_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1 123 4567",
    "waitlist": {
      "key": "your-waitlist-key"
    },
    "pending": {
      "created_at": 1642248600000,
      "expired_at": 1642421400000,
      "email_sent": true
    },
    "metadata": {
      "source": "landing-page",
      "origin_url": "https://yoursite.com",
      "ip_address": "192.168.1.1",
      "city": "New York",
      "region": "NY",
      "country": "US",
      "timezone": "America/New_York",
      "custom_fields": {}
    }
  }
}
```

### HMAC verification (Python, verbatim from docs)

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected_signature = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
        
    return hmac.compare_digest(signature, expected_signature)

# Usage
is_valid = verify_webhook(
    request.get_data(as_text=True),
    request.headers.get('X-Webhook-Signature'),
    'your-secret'
)

# Handle different event types
event = request.json.get('event')
if event == 'waitlist.signup_created':
    # Handle new sign-up
    signup_token = request.json['data']['signup_token']
    thank_you_url = request.json['data']['thank_you_url']
elif event == 'waitlist.referral_completed':
    # Handle referral
    pass
elif event == 'waitlist.milestone_reached':
    # Handle milestone
    pass
elif event == 'waitlist.subscriber_unsubscribed':
    # Handle unsubscribe
    pass
elif event == 'waitlist.subscriber_pending_expired':
    # Handle expired pending sign-up
    pass
```

Compute the signature over the **raw request body**. Node.js and PHP examples also exist in the docs.

## iPaaS & MCP

- **No Zapier integration** (confirmed absent from integrations page and docs as of 2026-06-06) — webhooks/API are the automation path
- **No Make/Pabbly modules, no MCP server**
- Native data connectors (Growth+): Klaviyo, Mailchimp, Kit; site-builder embed guides for Framer, Webflow, Shopify, WordPress, Bubble, Squarespace, and ~20 others (embed installs, not data connectors)

## Gaps

- Get-subscriber endpoint detail page not captured — response shape presumed to match the list-subscribers subscriber object; verify against live API
- Log-view endpoint body not fully captured — used with a localStorage-persisted visitor ID to dedupe analytics views (per code-examples page)
- No documented delete-subscriber endpoint — unsubscribe appears UI/email-driven only
- Email send-cap overage behavior (2,500/10K/50K per month) undocumented
- Webhook retry schedule (intervals/count before the 10-failure disable) not specified
