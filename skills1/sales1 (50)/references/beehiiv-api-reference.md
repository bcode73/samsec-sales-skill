<!-- Source: https://developers.beehiiv.com/api-reference/ — re-verified 2026-06-13 -->
# Beehiiv API Reference

Base URL: `https://api.beehiiv.com/v2`

Authentication: Bearer token. Two supported methods:
- **API key** (simplest): `Authorization: Bearer <api_key>`. Create at Settings > API under Workspace Settings; the key is shown only once.
- **OAuth2** (recommended for integrations): authorization code flow with PKCE for public clients. Endpoints live under `/oauth`: `GET /oauth/authorize`, `POST /oauth/token`, `POST /oauth/revoke`, `POST /oauth/introspect`, `GET /oauth/token/info`. Use the returned `access_token` as `Authorization: Bearer <access_token>`. Scopes are `<resource>:read` / `<resource>:write`.

API access is available on all plans. Send API (programmatic email sending) is in beta and available on request to Enterprise plans. The Create post endpoint is Enterprise-only.

OpenAPI spec: https://developers.beehiiv.com/openapi.json and https://developers.beehiiv.com/openapi.yaml
Full machine-readable docs index: https://developers.beehiiv.com/llms.txt
MCP server (Claude Code, Cursor, etc.): `https://developers.beehiiv.com/_mcp/server`

---

## Publications

### List publications
**GET** `/publications`

OAuth Scope: `publications:read`

Query Parameters:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| expand | array | No | Add stats: `stats`, `stat_active_subscriptions`, `stat_active_premium_subscriptions`, `stat_active_free_subscriptions`, `stat_average_open_rate`, `stat_average_click_rate`, `stat_total_sent`, `stat_total_unique_opened`, `stat_total_clicked` |
| limit | integer | No | Results per page (1-100, default: 10) |
| page | integer | No | Page number (default: 1) |
| direction | string | No | Sort direction: `asc` or `desc` (default: `asc`) |
| order_by | string | No | Sort by: `created` or `name` (default: `created`) |

Response (200 OK):
```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "organization_name": "string",
      "referral_program_enabled": "boolean",
      "created": "integer (Unix timestamp)",
      "stats": { /* optional, if expanded */ }
    }
  ],
  "limit": "integer",
  "page": "integer",
  "total_results": "integer",
  "total_pages": "integer"
}
```

---

## Subscriptions

### List subscriptions
**GET** `/publications/{publicationId}/subscriptions`

OAuth Scope: `subscriptions:read`

Path Parameters:
| Parameter | Type | Description |
|-----------|------|-------------|
| publicationId | string | The prefixed ID of the publication |

Query Parameters:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| expand[] | string | No | Expandable: `stats`, `custom_fields`, `referrals`, `newsletter_lists`, `subscription_premium_tiers` |
| status | string | No | Filter: `validating`, `invalid`, `pending`, `active`, `inactive`, `all` (default: `all`) |
| tier | string | No | Filter: `free`, `premium`, `all` (default: `all`) |
| premium_tiers[] | string | No | Filter by premium tier names |
| premium_tier_ids[] | string | No | Filter by premium tier IDs |
| limit | integer | No | 1-100 (default: 10) |
| cursor | string | No | Cursor for pagination (recommended) |
| page | integer | No | Page number (deprecated, max 100 pages) |
| email | string | No | Exact match email search (case insensitive) |
| order_by | string | No | Sort: `created` (default) |
| direction | string | No | Sort: `asc`, `desc` (default: `asc`) |
| creation_date | string | No | Filter by date (YYYY/MM/DD) |

Response (200 OK):
```json
{
  "data": [
    {
      "id": "string",
      "email": "string",
      "status": "active|inactive|pending|validating|invalid|needs_attention|paused",
      "created": "integer (Unix timestamp)",
      "subscription_tier": "free|premium",
      "subscription_premium_tier_names": ["string"],
      "utm_source": "string",
      "utm_medium": "string",
      "utm_channel": "string",
      "utm_campaign": "string",
      "utm_term": "string",
      "utm_content": "string",
      "referring_site": "string",
      "referral_code": "string",
      "subscription_premium_tiers": [{ "id": "string", "name": "string", "status": "string" }],
      "custom_fields": [{ "name": "string", "kind": "string", "value": "string" }],
      "stats": { "emails_received": "integer", "open_rate": "float", "click_through_rate": "float" },
      "newsletter_list_ids": ["string"]
    }
  ],
  "limit": "integer",
  "has_more": "boolean",
  "next_cursor": "string",
  "page": "integer",
  "total_pages": "integer",
  "total_results": "integer"
}
```

### Create subscription
**POST** `/publications/{publicationId}/subscriptions`

OAuth Scope: `subscriptions:write`

Request Body:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Subscriber's email address |
| reactivate_existing | boolean | No | Reactivate previously unsubscribed (default: false) |
| send_welcome_email | boolean | No | Send welcome message (default: false) |
| utm_source | string | No | Acquisition tracking |
| utm_medium | string | No | Acquisition tracking |
| utm_campaign | string | No | Acquisition tracking |
| utm_term | string | No | Acquisition tracking |
| utm_content | string | No | Acquisition tracking |
| referring_site | string | No | Referrer website |
| referral_code | string | No | Credit referral to existing subscriber |
| custom_fields | array | No | Pre-existing custom field name-value pairs |
| double_opt_override | string | No | `on`, `off`, or `not_set` |
| tier | string | No | `free` or `premium` |
| premium_tiers | array | No | Premium tier names |
| premium_tier_ids | array | No | Premium tier IDs |
| stripe_customer_id | string | No | Associated Stripe customer |
| automation_ids | array | No | Automation enrollment IDs |
| newsletter_list_ids | array | No | Newsletter list IDs (Beta) |
| skip_newsletter_list_auto_subscribe | boolean | No | Opt out of auto-subscribe (default: false) |

Response: 200 OK with SubscriptionResponse object.

---

## Posts

### Create post (Beta — Enterprise only)
**POST** `/publications/{publicationId}/posts`

OAuth Scope: `posts:write`

Content (choose one):
- `blocks`: Array of structured content blocks
- `body_content`: Raw HTML string

Block types: `paragraph`, `image`, `heading`, `button`, `table`, `list`, `columns`, `html`, `embed_link`, `poll`, `quote`, `content_break`, `paywall_break`, `rss`, `advertisement`

Request Body:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Post title |
| subtitle | string | No | Post subtitle |
| blocks OR body_content | array/string | Yes | Content |
| post_template_id | string | No | Template ID |
| status | string | No | `draft` or `confirmed` (default: `confirmed`) |
| scheduled_at | string | No | ISO 8601 datetime |
| override_scheduled_at | string | No | Display date different from publish date |
| custom_link_tracking_enabled | boolean | No | Enable link tracking |
| email_capture_type_override | string | No | `none`, `gated`, `popup` |
| social_share | string | No | `comments_and_likes_only`, `with_comments_and_likes`, `top`, `none` |
| thumbnail_image_url | string | No | Thumbnail URL |
| recipients | object | No | `web` and `email` targeting (tier_ids, include/exclude segment_ids) |
| newsletter_list_id | string | No | Target list (Beta) |
| email_settings | object | No | Subject line, preview text, from address |
| web_settings | object | No | Slug, thumbnail display, feed visibility |
| seo_settings | object | No | Meta descriptions/titles |
| content_tags | array | No | Tag strings |
| custom_fields | object | No | Custom field key-value pairs |

HTML sanitization: `<style>` and `<link>` tags are removed. Inline `style` attributes are preserved. CSS classes have no effect.

Response: 201 Created with `{ "data": { "id": "post_<prefixed-id>" } }`

---

## Webhooks

Available on Scale plan and above. Configure via Settings > Integrations > Webhooks, or via the Webhooks API (full CRUD):
- **POST** `/publications/{publicationId}/webhooks` — Create. Required body: `url` (string, URI), `event_types` (array). Optional: `description`. OAuth scope: `webhooks:write`.
- **GET** `/publications/{publicationId}/webhooks` — List. **GET** `/publications/{publicationId}/webhooks/{id}` — Get.
- **PUT** `/publications/{publicationId}/webhooks/{id}` — Update. **DELETE** `/publications/{publicationId}/webhooks/{id}` — Delete.

### Event types

The exact `event_types` enum (verbatim from the Create webhook reference). Tier events use **dot** notation, and the "added" event is named **`subscription.tier.created`**.

**Subscription events:**
- `subscription.created` — New subscriber
- `subscription.confirmed` — Subscriber confirmed (double opt-in)
- `subscription.deleted` — Subscriber removed
- `subscription.upgraded` — Free → premium
- `subscription.downgraded` — Premium → free
- `subscription.paused` — Subscription paused
- `subscription.resumed` — Subscription resumed
- `subscription.tier.paused` — Specific tier paused
- `subscription.tier.resumed` — Specific tier resumed
- `subscription.tier.created` — Tier added to subscription
- `subscription.tier.deleted` — Tier removed from subscription

**Post events:**
- `post.sent` — Post published/sent
- `post.updated` — Post updated
- `post.scheduled` — Post scheduled

**Survey events:**
- `survey.response_submitted` — Survey response received

**Newsletter list events:**
- `newsletter_list_subscription.subscribed`
- `newsletter_list_subscription.unsubscribed`
- `newsletter_list_subscription.paused`
- `newsletter_list_subscription.resumed`

Note: beehiiv's published webhook docs do not document an HMAC/signature header or retry policy. Treat payloads as unsigned — validate against the API by re-fetching the subscription/post by ID rather than trusting the payload blindly.

---

## Rate limits

- **180 requests per minute**, enforced **per organization** (not per API key). Exceeding it returns **429 Too Many Requests**.
- Every response includes rate-limit headers: `RateLimit-Limit` (max requests in the current window), `RateLimit-Remaining` (requests left), and `RateLimit-Reset` (Unix epoch seconds when the window resets).
- beehiiv recommends client-side rate limiting plus exponential backoff on 429.

## Error responses

| Status | Description |
|--------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 429 | Too Many Requests (rate limit exceeded — see Rate limits above) |
| 500 | Internal Server Error |

---

## Pagination

**Cursor-based (recommended)**: Use `cursor` parameter. Response includes `has_more` and `next_cursor`.

**Offset-based (deprecated)**: Use `page` parameter. Limited to 100 pages maximum.

---

## Other endpoints (v2)

The API surface is much broader than the resources detailed above. Current resources (all under `/publications/{publicationId}/...` unless noted), with `:read`/`:write` OAuth scopes:

- **Subscriptions**: get by email, get by id, update by id (PUT), update by email, delete; add subscription tag.
- **Bulk subscriptions**: bulk create; bulk update; bulk update status; list/get bulk update jobs.
- **Tiers** (premium tiers): create, list, get, update.
- **Segments**: create, list, get, update, recalculate, delete; list segment subscribers; list segment subscriber IDs.
- **Automations**: list, get, list automation emails; **Automation journeys**: add subscription to automation (create), list, get.
- **Custom fields**: create, list, get, update, delete.
- **Posts**: create (Enterprise), update, list, get, delete, get aggregate stats, send test email; **Post templates**: list.
- **Polls**: list, get, list poll responses.
- **Newsletter lists** + **Newsletter list subscriptions**: list/get lists; create/list/get/update list subscriptions.
- **Authors**: list, get. **Referral program**: get. **Engagements**: get publication engagements.
- **Complimentary access**: list, get. **Condition sets**: list, get. **Advertisement opportunities**: list. **Post templates**: list.
- **Data deletion** (GDPR): create deletion request, get, list.
- **OAuth/workspace**: identify user, identify workspace, get publications by subscription email.

For exact request/response shapes use the OpenAPI spec or the per-endpoint docs at `https://developers.beehiiv.com/api-reference/`.
