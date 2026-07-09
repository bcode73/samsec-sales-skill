<!-- Source: memberful.com/docs/api-reference/memberful-api, /docs/api-reference/webhooks, /docs/api-reference/webhook-event-reference/ (fetched 2026-06). GraphQL endpoint, auth, pagination, webhook events + payload, and HMAC-SHA256 signature scheme are verbatim from the official docs. -->

# Memberful API Reference

Memberful exposes a **GraphQL API** (queries + mutations) plus **webhooks** and **OAuth** sign-in. There is no REST API — everything goes through one GraphQL endpoint.

## GraphQL endpoint

```
POST https://ACCOUNT-URL.memberful.com/api/graphql
```

`ACCOUNT-URL` is your Memberful subdomain (e.g. `https://yoursite.memberful.com/api/graphql`).

## Authentication

Include a Bearer header with every request:

```
Authorization: Bearer <your-api-key>
```

Generate the API key by creating a **Custom Application** in **Settings → Custom applications** in your Memberful dashboard. Keep it server-side only.

cURL example:

```bash
curl https://ACCOUNT-URL.memberful.com/api/graphql \
  -H "Authorization: Bearer $MEMBERFUL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { member(id: 1) { id fullName email } }"}'
```

## API Explorer (live docs)

After creating a Custom App, click **Open API Explorer** to construct/test queries and mutations, then **Show Documentation Explorer** to browse the full schema (always up to date). This is the canonical, live documentation — the schema is the source of truth.

## Queries vs mutations

- **Queries** retrieve data (members, subscriptions, plans, coupons, …).
- **Mutations** create, update, or delete data (e.g. `memberCreate`).

All requests are `POST` with a `query` field containing the GraphQL operation.

### Example query

```graphql
query {
  member(id: 1) {
    id
    fullName
    email
    subscriptions {
      id
      pass { id name }
    }
  }
}
```

### Example mutation

```graphql
mutation {
  memberCreate(email: "john@example.com", fullName: "John Doe") {
    member { id username }
  }
}
```

## ⚠️ Terminology: dashboard vs API

The dashboard and the API use **different names for the same things**:

| Dashboard term | API type | Meaning |
|---|---|---|
| **Plan** | `Pass` | the thing members subscribe to (a membership) |
| **Price** | `Plan` | a pricing variant of a Pass (e.g. "$10/month") |

So a dashboard "Plan" is an API **`Pass`**, and a dashboard "Price" is an API **`Plan`**. This trips up almost every first integration.

## Pagination

Large result sets use **Relay-style cursor pagination** with `after`, `before`, `first`, `last` arguments and `pageInfo { hasNextPage endCursor }` / `edges { node }` connection fields.

## Member metadata

You can store custom JSON **metadata** on a member **via the API only** (not the dashboard):

- max **50 keys**
- key length ≤ **40 characters**
- value length ≤ **500 characters**

## Error handling

The endpoint returns **HTTP 200 even on failure** — errors come back in an `"errors"` array in the JSON body (standard GraphQL). Check the body, not the status code.

```json
{ "data": null, "errors": [{ "message": "..." }] }
```

---

# Webhooks

Real-time notifications for membership lifecycle events.

## Setup (per the docs)

1. Decide which events you want.
2. Create an endpoint to receive POSTs.
3. In **Settings → Webhooks**, create a webhook, select events, and set the endpoint URL.
4. Implement **signature verification** (below).
5. **Fetch the latest data from the GraphQL API** for the affected record.
6. Take action per event type.
7. Test with realistic scenarios.

> Memberful's recommended pattern: treat the webhook as a **trigger**, then re-query the GraphQL API for authoritative current state (payloads can be a point-in-time snapshot).

## Signature verification (HMAC-SHA256)

- **Header:** `X-Memberful-Webhook-Signature`
- **Algorithm:** HMAC with **SHA-256**, key = your **Webhook secret**, message = the **raw request body**.

Ruby (from docs):

```ruby
computed_signature = OpenSSL::HMAC.hexdigest("SHA256", secret, request.body.read)
```

JavaScript (from docs):

```javascript
const computedSignature = crypto
  .createHmac('sha256', secret)
  .update(payload)
  .digest('hex');
```

Constant-time compare `computed_signature` to the header; reject on mismatch.

## All webhook events (21)

**Member events**
- `member_signup` — a new member account is created
- `member_updated` — a member's profile info is updated
- `member.deleted` — a member is deleted
- `tax_id.updated` — a member adds/changes/removes their tax ID
- `custom_fields.updated` — a member answers/updates custom fields

**Subscription events**
- `subscription.created` — a new subscription is added to a member
- `subscription.updated` — a subscription is updated
- `subscription.renewed` — a subscription is renewed or reactivated
- `subscription.activated` — a suspended order is marked complete by staff
- `subscription.deactivated` — a subscription fails to renew, expires, or becomes inactive
- `subscription.deleted` — staff deletes a subscription

**Order events**
- `order.purchased` — a member places an order (or staff adds one)
- `order.refunded` — staff refunds an order
- `order.suspended` — an order is suspended by staff
- `order.completed` — a suspended order is marked complete by staff

**Plan (price) events**
- `subscription_plan.created` — a new price is created
- `subscription_plan.updated` — a price is updated
- `subscription_plan.deleted` — a price is deleted

**Download events**
- `download.created` / `download.updated` / `download.deleted`

> ⚠️ **Event names mix `snake_case` and `dot.case`** (e.g. `member_signup` and `member_updated` use underscores, but `member.deleted`, `subscription.created`, etc. use dots). Match the exact strings — don't normalize them.

## Example payload (`member_signup`)

```json
{
  "event": "member_signup",
  "member": {
    "address": {
      "street": "Street",
      "city": "City",
      "state": "State",
      "postal_code": "Postal code",
      "country": "City",
      "line2": ""
    },
    "created_at": 1234567890,
    "credit_card": { "exp_month": 1, "exp_year": 2040 },
    "custom_field": "Custom field value",
    "discord_user_id": "000000000000000000",
    "email": "john.doe@example.com",
    "first_name": "John",
    "full_name": "John Doe",
    "id": 6945121,
    "last_name": "Doe",
    "phone_number": "555-12345",
    "signup_method": "checkout",
    "stripe_customer_id": "cus_00000",
    "tracking_params": {
      "utm_term": "shoes",
      "utm_campaign": "summer_sale",
      "utm_medium": "social",
      "utm_source": "instagram",
      "utm_content": "textlink"
    },
    "unrestricted_access": false,
    "username": "john_doe"
  }
}
```

---

# OAuth (Sign in with Memberful)

Memberful supports **OAuth** so members can "Sign in with Memberful" on your app (single sign-on). The OAuth **callback requires server-side middleware** (Node.js, Python, or a serverless function on Cloudflare Workers / AWS Lambda) — the exchange can't run purely client-side. Use the same API-key/Custom-Application setup. Use this when you want member identity in your own app rather than just gating content on a Memberful-hosted/WordPress site.

# Integrations

Native: **WordPress** (plugin), **Discord** (role sync), **Mailchimp**, **Kit** (ConvertKit), **Stripe** (bring your own account — Memberful never holds funds), plus **Zapier**. Content delivery: gated pages, **private podcasts** (per-member RSS), **newsletters**, and **digital downloads**.

# Pricing (best-effort, 2026)

| Plan | Price | Memberful fee | Notes |
|---|---|---|---|
| Free | $0/mo | **10%** | get started, higher per-transaction cut |
| Pro | **$25/mo** | **4.9%** | lower fee, more features |
| Premium | **$100/mo** | **4.9%** | highest tier |

All plans **also** incur **Stripe** processing (2.9% + 30¢). You connect **your own Stripe account**. Verify current numbers on memberful.com/pricing.
