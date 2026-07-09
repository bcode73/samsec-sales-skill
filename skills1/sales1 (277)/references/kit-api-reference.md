# Kit API Reference

## Overview

- **Base URL**: `https://api.kit.com/v4/`
- **Legacy URL**: `https://api.convertkit.com/v3/` (deprecated, still functional; v4 keys are NOT compatible with v3)
- **Authentication**: OAuth 2.0 (refresh-token flow for web servers, PKCE flow for SPAs/mobile) for apps, or API key for personal/simple integrations
- **Rate limit**: 120 requests per rolling 60-second window for API-key auth; **600 requests per rolling 60-second window for OAuth**
- **Pagination**: Cursor-based (v4)
- **Content-Type**: `application/json`
- **Developer docs**: https://developers.kit.com/v4

## Authentication

### OAuth 2.0 (recommended for apps / public integrations)

Register an OAuth app through the Kit App Store (enable "API access" in app settings). Configure the Authorization URL, Redirect URI(s), and the "secure application" toggle (determines PKCE enforcement). Two flows are supported: the refresh-token flow for web servers and the PKCE flow for SPAs/mobile apps. OAuth gets the higher 600 req/60s rate limit, and **some endpoints require OAuth** — notably the bulk endpoints and purchase creation.

Include the access token in requests:
```
Authorization: Bearer {access_token}
```

### API Key (simple personal integrations / testing)

Create a v4 API key in the **Developer** tab of account settings (`https://app.kit.com/account_settings/developer_settings`). Pass it in the **`X-Kit-Api-Key`** request header:
```
curl --request GET \
  --url https://api.kit.com/v4/account \
  --header 'X-Kit-Api-Key: <YOUR_V4_API_KEY>'
```
API keys are intended for personal account automation/testing only — Kit does not officially support public apps built on API-key auth. Creators on any plan can generate API keys.

## Subscribers

### List subscribers
```
GET /v4/subscribers
```
Pagination is cursor-based: `after` (next page, from `end_cursor`), `before` (previous page, from `start_cursor`), `per_page` (default 500, max 1000). There is NO `page` param in v4.

Filter/sort params: `status` (active, inactive, bounced, complained, cancelled, or `all`; defaults to active), `email_address` (comma-separated), `created_after`, `created_before`, `updated_after`, `updated_before` (yyyy-mm-dd), `sort_field`, `sort_order` (asc/desc), `include` (comma-separated: `attribution`, `tags`, `location`, `canceled_at`), `include_total_count` (true adds total count but slows responses), `slim` (true omits expensive optional fields).

### Get a subscriber
```
GET /v4/subscribers/{id}
```

### Create a subscriber (upsert)
```
POST /v4/subscribers
```
```json
{
  "email_address": "jane@example.com",
  "first_name": "Jane",
  "state": "active",
  "fields": {
    "company": "Acme Inc"
  }
}
```
If the email already exists, the subscriber is updated (upsert behavior).

### Update a subscriber
```
PUT /v4/subscribers/{id}
```

### Unsubscribe
```
POST /v4/subscribers/{id}/unsubscribe
```

### Bulk create subscribers
```
POST /v4/bulk/subscribers
```
```json
{
  "subscribers": [
    {"email_address": "jane@example.com", "first_name": "Jane"},
    {"email_address": "john@example.com", "first_name": "John"}
  ]
}
```
Processed asynchronously. Returns a bulk operation ID.

### List tags for a subscriber
```
GET /v4/subscribers/{id}/tags
```

## Tags

### List tags
```
GET /v4/tags
```

### Create a tag
```
POST /v4/tags
```
```json
{
  "name": "purchased-ebook"
}
```

### Tag a subscriber
```
POST /v4/tags/{tag_id}/subscribers
```
```json
{
  "email_address": "jane@example.com"
}
```

### Remove tag from subscriber
By subscriber ID:
```
DELETE /v4/tags/{tag_id}/subscribers/{subscriber_id}
```
By email address (pass `email_address` in the body; returns 422 if neither id nor email is supplied):
```
DELETE /v4/tags/{tag_id}/subscribers
```
Returns 204 on success.

### Bulk tag subscribers
```
POST /v4/bulk/tags/{tag_id}/subscribers
```

## Broadcasts

### List broadcasts
```
GET /v4/broadcasts
```

### Get a broadcast
```
GET /v4/broadcasts/{id}
```

### Create a broadcast
```
POST /v4/broadcasts
```
```json
{
  "subject": "My Newsletter Issue #42",
  "content": "<p>Hello {{ subscriber.first_name }}</p>",
  "email_template_id": "template_id",
  "send_at": "2025-01-15T10:00:00Z"
}
```

### Update a broadcast
```
PUT /v4/broadcasts/{id}
```

### Delete a broadcast
```
DELETE /v4/broadcasts/{id}
```

### Get broadcast stats
```
GET /v4/broadcasts/{id}/stats
```
Returns: recipients, open_rate, click_rate, unsubscribes, complaints, revenue.

## Sequences

### List sequences
```
GET /v4/sequences
```

### Add subscriber to a sequence
```
POST /v4/sequences/{id}/subscribers
```
```json
{
  "email_address": "jane@example.com"
}
```

### Bulk add to sequence
```
POST /v4/bulk/sequences/{id}/subscribers
```

## Forms

### List forms
```
GET /v4/forms
```

### Add subscriber to a form
```
POST /v4/forms/{id}/subscribers
```
```json
{
  "email_address": "jane@example.com",
  "first_name": "Jane"
}
```

### Bulk add to form
```
POST /v4/bulk/forms/{id}/subscribers
```

## Custom Fields

### List custom fields
```
GET /v4/custom_fields
```

### Create a custom field
```
POST /v4/custom_fields
```
```json
{
  "label": "Company"
}
```

### Update a custom field
```
PUT /v4/custom_fields/{id}
```

### Delete a custom field
```
DELETE /v4/custom_fields/{id}
```

## Segments

### List segments
```
GET /v4/segments
```

## Purchases

### Create a purchase
```
POST /v4/purchases
```
```json
{
  "email_address": "jane@example.com",
  "transaction_id": "txn_123",
  "products": [
    {
      "name": "Ebook: Creator Guide",
      "pid": "prod_123",
      "lid": "line_123",
      "quantity": 1,
      "unit_price": 29.00
    }
  ],
  "currency": "USD",
  "transaction_time": "2025-01-15T10:00:00Z",
  "subtotal": 29.00
}
```

### List purchases
```
GET /v4/purchases
```

### Get a purchase
```
GET /v4/purchases/{id}
```

## Account

### Get current account
```
GET /v4/account
```
Returns: name, plan_type, primary_email_address, subscriber_count.

### Get email stats
```
GET /v4/account/email_stats
```

### Get growth stats
```
GET /v4/account/growth_stats
```
Returns subscriber growth data for the last 90 days.

## Webhooks

> **v4 path change**: webhooks moved from the v3 path `/automations/hooks` to `/v4/webhooks`. Use `/v4/webhooks`.

### Create a webhook
```
POST /v4/webhooks
```
```json
{
  "target_url": "https://your-app.com/webhooks/kit",
  "event": {
    "name": "subscriber.subscriber_activate",
    "form_id": null,
    "tag_id": null,
    "sequence_id": null,
    "product_id": null,
    "initiator_value": null,
    "custom_field_id": null
  }
}
```
Only the event-specific parameter for your chosen event needs a value (see the required-parameter column below).

### List webhooks
```
GET /v4/webhooks
```
Cursor-paginated response (`has_previous_page`, `has_next_page`, `start_cursor`, `end_cursor`, `per_page`).

### Delete a webhook
```
DELETE /v4/webhooks/{id}
```

### Webhook events

| Event | Required event param | Fires when |
|---|---|---|
| `subscriber.subscriber_activate` | — | Subscriber confirms opt-in |
| `subscriber.subscriber_unsubscribe` | — | Subscriber unsubscribes |
| `subscriber.subscriber_bounce` | — | Email bounces |
| `subscriber.subscriber_complain` | — | Spam complaint received |
| `subscriber.form_subscribe` | `form_id` | Subscriber opts in via form |
| `subscriber.course_subscribe` | `sequence_id` | Subscriber added to sequence |
| `subscriber.course_complete` | `sequence_id` | Subscriber completes sequence |
| `subscriber.link_click` | `initiator_value` (link URL) | Subscriber clicks a tracked link |
| `subscriber.product_purchase` | `product_id` | Subscriber purchases a product |
| `subscriber.tag_add` | `tag_id` | A tag is added to a subscriber |
| `subscriber.tag_remove` | `tag_id` | A tag is removed from a subscriber |
| `purchase.purchase_create` | — | A purchase is created |
| `custom_field.field_created` | — | A custom field is created |
| `custom_field.field_deleted` | — | A custom field is deleted |
| `custom_field.field_value_updated` | `custom_field_id` | A subscriber's custom-field value changes |

Webhook delivery is a `POST` of JSON containing `id` (int), `account_id` (int), the `event` object (`name` + the relevant id), and `target_url`. No HMAC/signature scheme is documented — validate by verifying the event against the API or use a hard-to-guess `target_url`.

## Pagination (v4)

All list endpoints use cursor-based pagination:

```json
{
  "data": [...],
  "pagination": {
    "has_previous_page": false,
    "has_next_page": true,
    "start_cursor": "abc123",
    "end_cursor": "xyz789"
  }
}
```

Use `?after={end_cursor}` for the next page, `?before={start_cursor}` for the previous page.

## Error handling

| Status | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 204 | No content (successful delete) |
| 401 | Unauthorized — invalid or expired token |
| 404 | Resource not found |
| 422 | Validation error — check response body for details |
| 429 | Rate limited — wait and retry |
| 500 | Server error |

Rate limit headers (limit reflects your auth type — 120 for API key, 600 for OAuth):
```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 115
X-RateLimit-Reset: 1705312800
```

## Notes

- **v3 → v4 migration**: v3 at `api.convertkit.com` is deprecated. Key differences: v4 uses cursor pagination with `before`/`after` (not `page`), OAuth 2.0 (not just API key), `X-Kit-Api-Key` header for API-key auth, the `api.kit.com` domain, and webhooks moved from `/automations/hooks` to `/webhooks`. v4 API keys are not compatible with v3.
- **Bulk operations**: Processed asynchronously, require OAuth auth. Poll the returned operation ID for status.
- **Webhook payloads**: `POST` with `id`, `account_id`, `event` object, and `target_url`. No documented HMAC signing — test with a webhook inspector.
- **Liquid templating**: Email content supports Liquid syntax (`{{ subscriber.first_name }}`, `{% if %}` blocks).
