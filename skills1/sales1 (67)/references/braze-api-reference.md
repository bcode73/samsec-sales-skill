# Braze API Reference

## Overview

- **Base URL**: `https://rest.{instance}.braze.com` — instance-specific. **US/APAC instances use `.braze.com`; EU instances use `.braze.eu`.** Verified instance→endpoint map (2026-06-13): US-01 `rest.iad-01.braze.com`, US-02 `rest.iad-02`, US-03 `rest.iad-03`, US-04 `rest.iad-04`, US-05 `rest.iad-05`, US-06 `rest.iad-06`, US-07 `rest.iad-07`, US-08 `rest.iad-08`, US-10 `rest.us-10.braze.com`, EU-01 `rest.fra-01.braze.eu`, EU-02 `rest.fra-02.braze.eu`, AU-01 `rest.au-01.braze.com`, ID-01 `rest.id-01.braze.com`, JP-01 `rest.jp-01.braze.com`, KR-01 `rest.kr-01.braze.com`. (No US-09; always confirm yours in Settings → APIs and Identifiers.)
- **Protocol**: REST over HTTPS
- **Auth**: Bearer token — `Authorization: Bearer YOUR_REST_API_KEY`
- **Format**: JSON request and response bodies
- **Content-Type**: `application/json`
- **Rate limit**: Default **250,000 requests/hour** for most APIs, but many endpoints have their own limits (see Rate Limits section) — resets on the clock hour, not a rolling window.
- **Pagination**: Cursor-based using `page` parameter or `next_uri` in response; some newer list endpoints (e.g. CDI) page via the `Link` response header.
- **SDKs**: iOS (Swift), Android (Kotlin/Java), Web (JS), React Native, Flutter, Cordova, Unity, Unreal Engine, Roku, .NET MAUI/Xamarin, Expo (legacy: iOS Obj-C, macOS, tvOS)

## Authentication

### API Key Setup
Dashboard → Settings → APIs and Identifiers → Create New API Key.

Each key has granular permissions scoped to specific endpoint groups. Use principle of least privilege — only enable permissions the key needs.

### Request Format
```
curl -X POST "https://rest.iad-01.braze.com/users/track" \
  -H "Authorization: Bearer YOUR_REST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"attributes": [{"external_id": "user123", "first_name": "John"}]}'
```

## HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | OK — request succeeded |
| 201 | Created — resource created |
| 400 | Bad Request — invalid parameters |
| 401 | Unauthorized — invalid or missing API key |
| 403 | Forbidden — key lacks required permission |
| 404 | Not Found — resource doesn't exist |
| 429 | Rate Limit Exceeded — back off and retry |
| 500 | Internal Server Error |

## Error Response Format

```json
{
  "message": "Description of error",
  "errors": ["specific error detail"]
}
```

---

## User Data

### Track users (attributes, events, purchases)
`POST /users/track`

The primary endpoint for ingesting user data. Each request can contain up to **75 total objects combined** across `attributes`, `events`, and `purchases` (the per-array 75-each / 225-combined structure is now a *legacy* limit for older contracts only). Base speed limit: **3,000 requests per 3 seconds**. For larger batches use `POST /users/track/bulk` (payload limit 2 MB, up to 1,000 objects total per request, max 100 objects per user profile).

```json
{
  "attributes": [
    {
      "external_id": "user123",
      "first_name": "John",
      "email": "john@example.com",
      "custom_attribute": "value"
    }
  ],
  "events": [
    {
      "external_id": "user123",
      "name": "completed_purchase",
      "time": "2024-01-15T10:30:00Z",
      "properties": {"product_id": "SKU123", "price": 49.99}
    }
  ],
  "purchases": [
    {
      "external_id": "user123",
      "product_id": "SKU123",
      "currency": "USD",
      "price": 49.99,
      "time": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Identify users
`POST /users/identify`

Merge anonymous user profile with identified profile.

```json
{
  "aliases_to_identify": [
    {
      "external_id": "user123",
      "user_alias": {"alias_name": "anon_abc", "alias_label": "anonymous"}
    }
  ]
}
```

### Create user aliases
`POST /users/alias/new`

### Delete users
`POST /users/delete`

Delete user profiles by external_id, braze_id, or user_alias. Up to 50 per request.

### Merge users
`POST /users/merge`

Merge two user profiles into one.

### Export user data
`POST /users/export/ids`

Export user profiles by external_id or braze_id.

```json
{
  "external_ids": ["user123", "user456"],
  "fields_to_export": ["first_name", "email", "custom_events", "purchases"]
}
```

`POST /users/export/segment`

Export all users in a segment (async — triggers a file export).

### Global control group
`POST /users/export/global_control_group`

Export users in the global control group.

---

## Messaging

### Send messages immediately
`POST /messages/send`

Send a one-off message to specific users without a campaign.

```json
{
  "external_user_ids": ["user123"],
  "messages": {
    "email": {
      "app_id": "APP_ID",
      "from": "hello@example.com",
      "subject": "Welcome!",
      "body": "<html>...</html>"
    },
    "apple_push": {
      "alert": "Welcome to our app!",
      "badge": 1
    }
  }
}
```

### Schedule messages
`POST /messages/schedule/create`
`POST /messages/schedule/update`
`POST /messages/schedule/delete`

### API-triggered campaign send
`POST /campaigns/trigger/send`

Trigger a pre-built campaign via API with dynamic properties.

```json
{
  "campaign_id": "CAMPAIGN_ID",
  "recipients": [
    {
      "external_user_id": "user123",
      "trigger_properties": {"order_id": "A-12345", "total": "$99.00"}
    }
  ]
}
```

### API-triggered Canvas send
`POST /canvas/trigger/send`

```json
{
  "canvas_id": "CANVAS_ID",
  "recipients": [
    {
      "external_user_id": "user123",
      "canvas_entry_properties": {"signup_source": "web"}
    }
  ]
}
```

### Schedule API-triggered campaigns
`POST /campaigns/trigger/schedule/create`
`POST /campaigns/trigger/schedule/update`
`POST /campaigns/trigger/schedule/delete`

### Schedule API-triggered Canvas
`POST /canvas/trigger/schedule/create`
`POST /canvas/trigger/schedule/update`
`POST /canvas/trigger/schedule/delete`

### iOS Live Activities (remote start/update)
`POST /messages/live_activity/start` — Remotely start an iOS Live Activity for a segment, connected audience, or external user IDs (requires `messages.live_activity.start` permission; uses default 250,000/hour limit).
`POST /messages/live_activity/update` — Push updates to an already-running Live Activity.

### Transactional email
`POST /transactional/v1/campaigns/{campaign_id}/send`

Dedicated endpoint for time-sensitive 1:1 transactional emails with delivery SLA guarantees.

```json
{
  "external_send_id": "txn_order_123",
  "trigger_properties": {"order_id": "A-12345"},
  "recipient": {
    "external_user_id": "user123"
  }
}
```

---

## Campaigns

### List campaigns
`GET /campaigns/list?page=0&include_archived=false`

### Campaign details
`GET /campaigns/details?campaign_id={id}`

### Campaign analytics
`GET /campaigns/data_series?campaign_id={id}&length=14`

---

## Canvas

### List Canvas
`GET /canvas/list?page=0&include_archived=false`

### Canvas details
`GET /canvas/details?canvas_id={id}`

### Canvas analytics
`GET /canvas/data_series?canvas_id={id}&length=14`
`GET /canvas/data_summary?canvas_id={id}&length=30`

---

## Segments

### List segments
`GET /segments/list?page=0`

### Segment details
`GET /segments/details?segment_id={id}`

### Segment analytics
`GET /segments/data_series?segment_id={id}&length=14`

---

## Templates

### Email templates
`POST /templates/email/create`
`PUT /templates/email/update`
`GET /templates/email/info?email_template_id={id}`
`GET /templates/email/list`

### Content Blocks
`POST /content_blocks/create`
`PUT /content_blocks/update`
`GET /content_blocks/info?content_block_id={id}`
`GET /content_blocks/list`

---

## Catalogs

### Manage catalogs
`POST /catalogs` — Create catalog
`GET /catalogs` — List catalogs
`DELETE /catalogs/{catalog_name}` — Delete catalog

### Catalog items
`POST /catalogs/{catalog_name}/items` — Create items (up to 50 per request)
`PATCH /catalogs/{catalog_name}/items` — Update items
`DELETE /catalogs/{catalog_name}/items` — Delete items
`GET /catalogs/{catalog_name}/items` — List items
`GET /catalogs/{catalog_name}/items/{item_id}` — Get single item

### Catalog fields
`POST /catalogs/{catalog_name}/fields` — Create fields

### Async catalog operations
`POST /catalogs/{catalog_name}/items/async` — Bulk create (up to 10,000 items)
`PATCH /catalogs/{catalog_name}/items/async` — Bulk update
`DELETE /catalogs/{catalog_name}/items/async` — Bulk delete

---

## Subscription Groups

### Email subscription
`POST /subscription/status/set` — Set subscription status
`GET /subscription/status/get?external_id={id}&subscription_group_id={id}`
`GET /subscription/user/status?external_id={id}`

### SMS subscription
Same endpoints — subscription groups support both email and SMS types.

---

## Data Export

### Revenue data
`GET /purchases/revenue_series?length=30`
`GET /purchases/quantity_series?length=30`

### KPIs
`GET /kpi/new_users/data_series?length=30`
`GET /kpi/dau/data_series?length=30`
`GET /kpi/mau/data_series?length=30`
`GET /kpi/uninstalls/data_series?length=30`

### Events
`GET /events/list` — List custom events
`GET /events/data_series?event={name}&length=30`

### Sessions
`GET /sessions/data_series?length=30`

### Feed (News Feed — legacy)
`GET /feed/list`
`GET /feed/details?card_id={id}`
`GET /feed/data_series?card_id={id}&length=30`

---

## SCIM (User Management)

### Dashboard user accounts
`POST /scim/v2/Users` — Create dashboard user
`GET /scim/v2/Users/{id}` — Get user
`PUT /scim/v2/Users/{id}` — Update user
`DELETE /scim/v2/Users/{id}` — Deactivate user
`GET /scim/v2/Users?filter=userName eq "user@example.com"` — Search

---

## Preference Center

`POST /preference_center/v1` — Create preference center
`PUT /preference_center/v1/{id}` — Update
`GET /preference_center/v1/{id}` — Get details
`GET /preference_center/v1/list` — List all
`GET /preference_center/v1/{id}/url/{user_id}` — Get URL for user

---

## SDK Authentication

`POST /app_group/sdk_authentication/create` — Create SDK auth key (requires `sdk_authentication.create`)
`PUT /app_group/sdk_authentication/primary` — Set the primary SDK auth key (requires `sdk_authentication.primary`)
`GET /app_group/sdk_authentication/keys` — List SDK auth keys (requires `sdk_authentication.keys`)

Up to 3 SDK Authentication keys per app, enabling zero-downtime key rotation.

---

## Email Lists and Addresses

Bi-directional sync of email subscription/suppression state between Braze and external systems.

`GET /email/hard_bounces` — List hard-bounced email addresses (path may also be documented as `GET /lists/hard_bounces`)
`GET /email/unsubscribes` — Query unsubscribed email addresses
`POST /email/status` — Change an email address's subscription status
`POST /email/bounce/remove` — Remove email addresses from the hard-bounce list
`POST /email/spam/remove` — Remove email addresses from the spam list
`POST /email/blacklist` — Blocklist email addresses (also documented as `POST /email/blocklist`)

---

## Cloud Data Ingestion (CDI)

Manage warehouse→Braze sync integrations (Snowflake, Redshift, BigQuery, Databricks, Microsoft Fabric, S3) via API.

`GET /cdi/integrations` — List integrations (requires `cdi.integration_list`; 50 req/min; pages via `Link` header, 10 items/page)
`POST /cdi/integrations/{integration_id}/sync` — Trigger a sync (requires `cdi.integration_sync`; 20 req/min; returns 202 `{"message":"success"}`)
`GET /cdi/integrations/{integration_id}/job_sync_status` — List past sync statuses for an integration

---

## Rate Limits

Default for *most* APIs is **250,000 requests/hour**, but many endpoints have their own limits. Resets on the clock hour (not a rolling window). Documented per-endpoint limits (2026-06-13):

| Endpoint(s) | Limit |
|---|---|
| `/users/track` | 3,000 requests / 3 seconds; ≤75 objects total/request |
| `/users/track/bulk` | account-specific bulk policy; ≤1,000 objects, 2 MB/request |
| `/users/export/ids` | 250 or 2,500 req/min (depends on onboarding date) |
| `/users/delete`, `/identify`, `/merge`, `/alias/new`, `/alias/update` | 20,000 req/min **shared** across these |
| `/users/external_id/rename`, `/users/external_id/remove` | 1,000 req/min each |
| `/messages/send`, `/campaigns/trigger/send`, `/canvas/trigger/send` | 250 req/min broadcast; 10 req/min per unique audience; 250,000/hour non-broadcast |
| `/sends/id/create` | 100 requests/day |
| `/campaigns/data_series` | 50,000 req/min |
| `/events/list`, `/purchases/product_list` | 1,000 req/hour **shared** |
| `/subscription/status/set` | 5,000 req/min |
| Catalog management endpoints | 50 req/min |
| Catalog bulk item endpoints | 16,000 req/min |
| `/cdi/integrations` (list) | 50 req/min |
| `/cdi/integrations/{id}/sync` | 20 req/min |
| Media library | 100 req/hour |

- **`/users/export/segment`**: Async — limited concurrent exports
- **Headers**: Check `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` response headers

---

## Braze Currents (Streaming Export)

Currents is not accessed via REST API — it's configured in the dashboard:
Dashboard → Data Settings → Currents → Create New Current

### Supported destinations
- Amazon S3
- Azure Blob Storage
- Google Cloud Storage
- Snowflake Data Sharing
- Segment
- mParticle
- Amplitude
- Mixpanel
- Treasure Data

### Event types streamed
- **Email**: Send, delivery, open, click, bounce, soft_bounce, spam, unsubscribe
- **Push**: Send, open, bounce, foreground
- **In-app message**: Impression, click
- **Content Card**: Impression, click, dismiss
- **SMS**: Send, delivery, rejection, short_link_click
- **WhatsApp**: Send, delivery, read, failure
- **Webhook**: Send
- **Canvas**: Entry, conversion, exit
- **Campaign**: Send, conversion
- **Custom events**: All custom events
- **Purchases**: All purchases
- **Session**: Start, end
- **User**: State change, uninstall

---

## Notes

- API documentation home: https://www.braze.com/docs/api/home (rate limits: https://www.braze.com/docs/api/api_limits)
- Postman collection (Braze public workspace): https://www.postman.com/braze-inc/braze-public-workspace/collection/d7cw9d5/braze-endpoints
- Braze was formerly known as Appboy — some SDK packages may use old naming
- Connected Content (in-message API calls) is separate from the REST API — it executes at send time
- Always use your instance-specific REST endpoint, not the SDK endpoint
