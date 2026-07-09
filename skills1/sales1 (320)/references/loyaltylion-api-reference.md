# LoyaltyLion API Reference

## Overview

LoyaltyLion provides two APIs:
- **Admin API** — backend data operations (orders, customers, points, webhooks)
- **Headless API** — shopper-facing custom UIs (loyalty widgets, mobile apps, headless storefronts)

## Admin API

### Authentication

Three methods (current docs, verified 2026-06-13):

1. **API keys (recommended for single-store/merchant integrations)** — create a key in the LoyaltyLion dashboard at **Manage → API keys → Create API key**. The token is shown once and cannot be retrieved later. Pass it as a **Bearer token**:
   ```
   Authorization: Bearer YOUR_API_KEY
   ```
   Keys are scoped — select only the scopes you need (e.g. `read_customers`, `write_customers`, `read_orders`, `write_orders`, plus scopes for unsubscribes, reviews, and `write_configuration`).

2. **OAuth (partners only)** — for partners building apps used across many stores. Flow: redirect to `https://app.loyaltylion.com/oauth/authorize` (client_id, scopes, redirect_uri) → exchange the returned code via `POST https://app.loyaltylion.com/oauth/access-token` (client_id, secret, code) → receive `access_token`. Use it as `Authorization: Bearer <access_token>` with `Content-Type: application/json`.

3. **Token & Secret (DEPRECATED)** — each site has a single token/secret usable via HTTP Basic auth (`Authorization: Basic base64(token:secret)`). LoyaltyLion states this method "is deprecated and will be removed in future, because it doesn't support permissions or credential rotation." Migrate existing integrations to API keys.

### Base URL

```
https://api.loyaltylion.com
```

All Admin API endpoints are under the **`/v2`** path prefix (e.g. `https://api.loyaltylion.com/v2/customers`).

### Rate Limits

- **20 requests per second** for all endpoints (unless otherwise stated)

### IP Addresses (for allowlisting)

- `35.71.187.221`
- `52.223.19.105`

### Resources

> All paths below are under the `/v2` prefix. The customer ID path parameter is named `{merchant_id}` (the customer's ID in your platform/store).

#### Customers

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v2/customers` | List customers |
| PUT | `/v2/customers/{merchant_id}` | Update customer (birthday, metadata) |
| POST | `/v2/customers/{merchant_id}/points` | Add points to customer (body: `points` 1–1,000,000 required, `reason` optional) |
| DELETE | `/v2/customers/{merchant_id}/points` | Remove points from customer |
| GET | `/v2/customers/{merchant_id}/transactions` | List customer transactions |
| GET | `/v2/customers/{merchant_id}/available_rewards` | List available rewards for customer |
| POST | `/v2/customers/{merchant_id}/claimed_rewards` | Redeem (claim) a reward |
| POST | `/v2/customers/{merchant_id}/claimed_rewards/{claimed_reward_id}/refund` | Refund a claimed reward |

#### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v2/orders` | Create order (trigger earning rules) |
| GET | `/v2/orders/{id}` | Get order details |
| GET | `/v2/orders` | List orders |
| PUT | `/v2/orders/{id}` | Update order |

#### Activities

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v2/activities` | Create activity (custom earning action) |
| GET | `/v2/activities` | List activities |
| PUT | `/v2/activities/{id}` | Update activity |

#### Reviews

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v2/reviews` | Create review |
| PUT | `/v2/reviews/{id}` | Update review |
| DELETE | `/v2/reviews/{id}` | Delete review |

#### Rewards

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v2/rewards/{reward_id}/enable` | Enable reward |
| POST | `/v2/rewards/{reward_id}/disable` | Disable reward |

#### Transactions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v2/transactions` | List all transactions |

#### Email Unsubscribes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v2/unsubscribes` | Create email unsubscribe |
| GET | `/v2/unsubscribes` | List unsubscribes |

#### Webhooks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v2/webhooks` | Create webhook |
| GET | `/v2/webhooks` | List webhooks |
| DELETE | `/v2/webhooks/{id}` | Delete webhook |

#### Sites & WebViews

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v2/sites` | List sites |
| POST | `/v2/sites/{site_id}/webviews/sessions` | Create WebView session |

#### Utility

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v2/whoami` | Return authenticated account info |

### Pagination

Two schemes on list endpoints:

- **Cursor-based (recommended)** — pass a `cursor` query parameter. The response returns `cursor: { prev, next }`; when a direction is `null` there are no more pages. The cursor preserves any filters from the initial request.
- **`since_id` based** — pass `since_id` (start at `0`) and `limit`; the collection is ordered by `id` ascending. Keep paging until the number of resources returned is less than your `limit`.

Docs: https://developers.loyaltylion.com/api-reference/pagination

### Webhook Signing & Verification

- **Signature header:** `x-loyaltylion-hmac-sha256`
- **Algorithm:** base64-encoded SHA-256 HMAC of the raw JSON request body and the relevant secret key.
- **Secret key:** OAuth client secret (for partner apps) or your site secret (for site-level webhooks).
- **Verify** by recomputing the HMAC over the raw body and comparing to the header value (docs give TypeScript, Ruby, and PHP examples).
- **Acknowledge** by responding `200` within **5 seconds**.
- **Retries:** failed deliveries retry with exponential backoff. After **5 failures** you get an email alert; after **30 failures** the webhook subscription is removed (with notification).

Docs: https://developers.loyaltylion.com/api-reference/v2/webhooks/overview

### Webhook Events

Current event names (from the v2 webhooks reference, verified 2026-06-13):

**Program events (`customer.*`):**
- `customer.enrolled`
- `customer.points_earned`
- `customer.approaching_points_expiration`
- `customer.approaching_reward_expiration`
- `customer.claimed_reward`
- `customer.reward_available_notification`
- `customer.tier_upgraded`
- `customer.tier_downgraded`
- `customer.approaching_tier_upgrade`
- `customer.moved_to_at_risk_segment`
- `customer.moved_to_defected_segment`
- `customer.moved_to_loyal_segment`
- `customer.receipt_approved`
- `customer.receipt_declined`
- `customer.rule_completed`
- `customer.referral_complete`
- `customer.recurring_reward_available_reminder`

**Other events:**
- `customers/update` — customer update
- `loyalty_emails/unsubscribe` — loyalty email unsubscribe
- `receipts/manual_approval_required` — receipt needs manual approval
- `rewards/store_fulfilment` — reward store fulfilment

## Headless API

For building custom shopper-facing loyalty experiences. The Headless API uses **date-based versioning** in the path, e.g. `GET /headless/2025-06/{site_id}/configuration` (current version `2025-06`). OpenAPI spec: https://developers.loyaltylion.com/headless-api/2025-06/openapi.json

### TypeScript Client

```bash
npm install @loyaltylion/headless-api-client
```

GitHub: `github.com/loyaltylion/typescript-headless-api-client`

### Use Cases

- Custom loyalty widgets on headless storefronts (Hydrogen, custom React)
- Native mobile app loyalty features
- POS app integration
- Custom loyalty page embedded in storefront

### SDK UI Components

**Pages & panels:** Loyalty page, loyalty panel, rewards list, history table, tier comparison, tier progress

**Modals:** Redeem rewards, claim confirmation, referral flow, transaction details

**Simple elements:** Point displays, product point values, cart point projections, referral URLs, loyalty widgets

### Reference Store

Hydrogen reference store: `github.com/loyaltylion/hydrogen-reference-store`

## Developer Portal

Full documentation: https://developers.loyaltylion.com/
- Admin API reference: https://developers.loyaltylion.com/api-reference/introduction
- Authentication (API keys / OAuth / deprecated token+secret): https://developers.loyaltylion.com/api-reference/authentication/overview
- Pagination: https://developers.loyaltylion.com/api-reference/pagination
- Webhooks overview (signing): https://developers.loyaltylion.com/api-reference/v2/webhooks/overview
- Headless API reference: https://developers.loyaltylion.com/headless-api/introduction
- LLM-friendly docs index: https://developers.loyaltylion.com/llms.txt
