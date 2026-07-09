<!-- Source: https://checkoutpage.com/docs/api , https://checkoutpage.com/docs/articles/webhooks , https://checkoutpage.com/docs/build/mcp (fetched 2026-07-04) -->

# Checkout Page API Reference

> Captured from the live docs on 2026-07-04. The docs site is partly JS-rendered — the
> endpoint list and object fields below are transcribed from what rendered; **re-verify
> exact request/response bodies against `https://checkoutpage.com/docs/api` before relying
> on them.** JSON blocks marked `<!-- Constructed from docs — verify against live API -->`
> were assembled from documented field lists, not copied from a live response.

## Base URL & versioning

```
https://api.checkoutpage.com
```

The API is REST-oriented: predictable resource URLs, JSON request/response bodies, standard
HTTP verbs and status codes. The current stable version is **v1**, and every endpoint is
prefixed with the version:

```
https://api.checkoutpage.com/v1/{endpoint}
```

## Authentication

API-key authentication with a Bearer token. Generate a key in the dashboard, then send it on
every request:

```
Authorization: Bearer YOUR_API_KEY
```

Minimal auth check (simplest GET):

```bash
curl https://api.checkoutpage.com/v1/payments \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Rate limits

- **Store-level**: 500 requests / minute (default)
- **API-key-level**: 100 requests / minute (default)
- Exceeding either returns **`429 Too Many Requests`**.

Retry strategy: on a 429, back off and retry. (The docs don't publish a `Retry-After` value —
use exponential backoff starting ~1s; keep bulk pulls incremental with pagination cursors
rather than re-reading history.)

## Pagination

Cursor-based, newest-first:

| Param | Meaning |
|---|---|
| `limit` | Page size, **1–100** (default 20) |
| `starting_after` | Cursor — return records after this object id |
| `ending_before` | Cursor — return records before this object id |

Walk forward by passing the last returned object's `id` as `starting_after` on the next call.

## Timestamps

All timestamps are **ISO 8601** strings (e.g. `2023-05-17T12:43:51.251Z`).

## Status codes & error shape

Standard HTTP codes: `200`, `201`, `400`, `401`, `403`, `404`, `429`, `500`. Errors return a
JSON object with `status`, `type`, and `message`:

```json
<!-- Constructed from docs — verify against live API -->
{
  "status": 401,
  "type": "authentication_error",
  "message": "Invalid API key provided."
}
```

## Endpoints

> The docs render endpoints in an action style (e.g. `/v1/checkout-pages/list`,
> `/v1/checkout-pages/create`) in some views and a REST style (e.g. `GET /v1/checkout-pages`,
> `POST /v1/checkout-pages`) in others. **Confirm the exact path style against the live docs**
> — the resources and operations below are stable, the surface spelling may differ.

### Checkout Pages

| Method | Path | Description |
|---|---|---|
| GET | `/v1/checkout-pages` | List checkout pages |
| GET | `/v1/checkout-pages/{id}` | Get a checkout page |
| POST | `/v1/checkout-pages` | Create a checkout page |
| PATCH | `/v1/checkout-pages/{id}` | Update a checkout page |
| DELETE | `/v1/checkout-pages/{id}` | Archive a checkout page |

### Events / Tickets / Bookings

| Method | Path | Description |
|---|---|---|
| GET | `/v1/events` | List events |
| GET | `/v1/events/{id}` | Get an event |
| POST | `/v1/events` | Create an event |
| PATCH | `/v1/events/{id}` | Update an event |
| DELETE | `/v1/events/{id}` | Archive an event |
| GET | `/v1/tickets/validate` | Validate a ticket (mobile check-in) |
| GET | `/v1/bookings` | List bookings (attendee + ticket info) |

### Forms

| Method | Path | Description |
|---|---|---|
| GET | `/v1/forms` | List forms |
| GET | `/v1/forms/{id}` | Get a form |
| POST | `/v1/forms` | Create a form |
| PATCH | `/v1/forms/{id}` | Update a form |
| DELETE | `/v1/forms/{id}` | Archive a form |

### Customers

| Method | Path | Description |
|---|---|---|
| GET | `/v1/customers` | List customers |
| GET | `/v1/customers/{id}` | Get customer details |
| PATCH | `/v1/customers/{id}` | Update a customer |

### Coupons

| Method | Path | Description |
|---|---|---|
| GET | `/v1/coupons` | List coupons |
| POST | `/v1/coupons` | Create a coupon |

### Invoices

| Method | Path | Description |
|---|---|---|
| GET | `/v1/invoices` | List invoices |
| POST | `/v1/invoices/regenerate` | Regenerate an invoice PDF |

### Tax rates

| Method | Path | Description |
|---|---|---|
| GET | `/v1/tax-rates` | List tax rates |
| POST | `/v1/tax-rates` | Create a tax rate |
| PATCH | `/v1/tax-rates/{id}` | Update a tax rate |
| DELETE | `/v1/tax-rates/{id}` | Delete a tax rate |

### Files

| Method | Path | Description |
|---|---|---|
| POST | `/v1/files/upload` | Upload a file |
| GET | `/v1/files/download` | Download a file |
| DELETE | `/v1/files/{id}` | Delete a file |

### Payments & Subscriptions

Payments and Subscriptions appear in the docs navigation as read resources (list/get). The
richest payment/subscription data is delivered via the `conversion` webhook (below) — its
`payment` / `subscription` payloads mirror these objects field-for-field.

```bash
# List recent payments
curl "https://api.checkoutpage.com/v1/payments?limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Webhooks

Configure two kinds:

- **Store-level webhooks** — receive events from **all** pages in a store.
  Store settings → Integrations → Webhooks → add URL + select events.
- **Page-level webhooks** — receive events from **one** page. Currently supports only the
  `conversion` event. Pages → select page → After payment/submission → Integrations → Add Webhooks.

Every delivery is a JSON `POST` with `event`, `object` (the conversion type), and a `data`
object. The `data.livemode` boolean distinguishes live from test payments — use the dashboard
"Test payments" tool to simulate `conversion` events.

> **Signature verification**: the public webhooks article does **not** document an HMAC
> signature header, signing secret, or retry policy. Until confirmed otherwise, treat payloads
> as **unsigned**: post to an unguessable/tokenized endpoint URL, re-verify anything that
> gates access or moves money by re-fetching the object via the REST API, dedupe on the object
> `id` / `orderId`, and keep a polling reconciliation. Re-check the live docs for a signing
> scheme before trusting deliveries.

### `conversion` — one-time payment (`object: "payment"`)

```json
{
  "event": "conversion",
  "object": "payment",
  "data": {
    "fields": {
      "customer_email": "test@checkoutpage.co",
      "quantity": "1",
      "shipping_address_line1": "357 Elm Drive",
      "shipping_address_city": "New York",
      "shipping_address_country": "United States",
      "shipping_address_postal_code": "10025"
    },
    "variants": {
      "size": {
        "name": "Size",
        "selectedOption": "Medium ",
        "price": "10.00",
        "sku": "100"
      },
      "color": {
        "name": "Color",
        "selectedOption": "Green",
        "sku": ""
      }
    },
    "amount": "23.99",
    "currency": "usd",
    "orderId": "02009743",
    "customerName": "Sander",
    "customerEmail": "test@checkoutpage.co",
    "customerCreatedDate": "2021-08-19T13:58:27.604Z",
    "customerId": "611e6383cf7d2c0020380e53",
    "stripeCustomerId": "cus_K4KQBkiwC8LG9E",
    "licenseKey": "1234567890",
    "licenseKeyUses": 0,
    "licenseKeyEnabled": true,
    "couponId": "645136a20779606f5a659dec",
    "couponCode": "COUPON",
    "couponPercentOff": 20,
    "couponAmountOff": "0",
    "couponDiscount": "4.80",
    "createdDate": "2023-05-17T12:43:51.251Z",
    "status": "paid",
    "id": "6464cc07822f15f2aca067dd",
    "stripePaymentId": "pi_1N3LpOJ7i86GeQKlEcsyGnwY",
    "productPrice": "13.99",
    "queryParameters": {
      "utm_source": "google"
    },
    "livemode": false,
    "productTitle": "T-shirt",
    "productTotalRevenue": "23.99",
    "productTotalNumberOfSales": 1,
    "checkoutId": "6464cbba822f15f2aca06734",
    "checkoutSlug": "t-shirt"
  }
}
```

### `conversion` — subscription (`object: "subscription"`)

```json
{
  "event": "conversion",
  "object": "subscription",
  "data": {
    "fields": {
      "customer_name": "Test",
      "customer_email": "test@checkoutpage.co"
    },
    "variants": {
      "tier": {
        "name": "Tier",
        "selectedOption": "Grow",
        "price": "49.00",
        "sku": "grow-tier",
        "stripePriceId": "price_1N3KttJ7i86GeQKlrttqR7gj",
        "stripeProductId": "prod_NoyrrdTsenY3qK"
      }
    },
    "amount": "49.00",
    "currency": "usd",
    "orderId": "16635413",
    "customerName": "Test",
    "customerEmail": "test@checkoutpage.co",
    "customerCreatedDate": "2023-05-02T16:13:22.190Z",
    "customerId": "645136a20779606f5a659dec",
    "stripeCustomerId": "cus_NozpnZaByGmgr7",
    "licenseKey": "1234567890",
    "licenseKeyUses": 0,
    "licenseKeyEnabled": true,
    "couponId": "645136a20779606f5a659dec",
    "couponCode": "COUPON",
    "couponPercentOff": 20,
    "couponAmountOff": "0",
    "couponDuration": "forever",
    "couponDurationInMonths": null,
    "couponDiscount": "9.80",
    "createdDate": "2023-05-02T16:13:22.234Z",
    "status": "active",
    "id": "645136a20779606f5a659dfc",
    "productPrice": "49.00",
    "discountedFrom": "69.00",
    "interval": "month",
    "intervalCount": 1,
    "endsAfterPayments": 4,
    "setupFee": "0",
    "trailStart": "2023-05-02T16:13:21.000Z",
    "trialEnd": "2023-05-09T16:13:21.000Z",
    "canceledAt": "2023-05-02T16:13:21.000Z",
    "cancelAt": "2023-09-02T16:13:21.000Z",
    "currentSubscriptionPeriodStart": "2023-05-02T16:13:21.000Z",
    "currentSubscriptionPeriodEnd": "2023-06-02T16:13:21.000Z",
    "sku": "",
    "paymentGateway": "stripe",
    "paymentMethod": "card",
    "queryParameters": {
      "utm_source": "google"
    },
    "livemode": true,
    "stripeSubscriptionId": "sub_1N3LpOJ7i86GeQKlEcsyGsmD",
    "productTitle": "Subscription",
    "productStock": 100,
    "productTrialPeriodDays": null,
    "productNumberOfSubscribers": 4,
    "productStripePlanId": "price_Noyr6dXsenY3qK",
    "productStripeProductId": "prod_NoyrrdTsenY3qK",
    "checkoutId": "64512687dd63fb2fac1e281c",
    "checkoutSlug": "subscription"
  }
}
```

> Note the field is spelled **`trailStart`** in the live payload (a vendor typo for
> "trialStart"); `trialEnd` is spelled correctly. Read both exactly as sent.

### `conversion` — form submission (`object: "submission"`)

```json
{
  "event": "conversion",
  "object": "submission",
  "data": {
    "fields": {
      "customer_name": "Test",
      "customer_email": "test@checkoutpage.co"
    },
    "variants": {
      "tier": {
        "name": "Tier",
        "selectedOption": "Grow",
        "sku": "grow-tier"
      }
    },
    "orderId": "52560220",
    "customerName": "Test",
    "customerEmail": "test@checkoutpage.co",
    "customerCreatedDate": "2023-05-02T16:13:22.190Z",
    "customerId": "645136a20779606f5a659dec",
    "stripeCustomerId": "cus_NozpnZaByGmgr7",
    "licenseKey": "1234567890",
    "licenseKeyUses": 0,
    "licenseKeyEnabled": true,
    "createdDate": "2023-05-02T16:13:22.234Z",
    "id": "6464b541822f15f2aca06477",
    "sku": "",
    "queryParameters": {
      "utm_source": "google"
    },
    "livemode": false,
    "productTitle": "Lead",
    "productTotalNumberOfSales": 1,
    "checkoutId": "645a4af4ef36dfae673f283f",
    "checkoutSlug": "lead-3"
  }
}
```

### Webhook payload notes

- **Money is a decimal string in the display currency** (`"23.99"`), **not** cents — different
  from SamCart/Sellfy, which send cents. Parse as a decimal.
- The Stripe object ids (`stripePaymentId`, `stripeSubscriptionId`, `stripeCustomerId`,
  `stripePriceId`) let you cross-reference or re-fetch directly in Stripe — the seller is the
  Stripe merchant of record.
- `queryParameters` carries UTM/ad params from the checkout URL for attribution.
- `variants` captures product options (size/color/tier) chosen at checkout.

## MCP server (primary agentic interface)

Checkout Page ships a **native hosted MCP server** so an AI assistant can build and query
checkouts in natural language.

- **Endpoint**: `https://mcp.checkoutpage.com`
- **Auth**: OAuth, one-click sign-in (no API keys, no setup script). Requires a Stripe-connected
  account.
- **Add to Claude Code**:

  ```bash
  claude mcp add --transport http checkoutpage https://mcp.checkoutpage.com
  ```

  Then run `/mcp` in a Claude session and authenticate.

- **Access model**: read-only on customer/payment data; write access scoped to checkout and
  form creation (plus coupons).

### Tools exposed (13)

| Tool | Purpose |
|---|---|
| `create_checkout_page` | Create a checkout page with products + pricing |
| `get_checkout_page` | Fetch a single checkout page's configuration |
| `list_payments` | List/filter payments by date, customer, amount, status |
| `list_subscriptions` | List subscriptions with status + billing details |
| `list_bookings` | List event bookings with attendee + ticket info |
| `create_form` | Create a form (survey, application, lead capture, RSVP) |
| `get_form` | Fetch a single form's configuration |
| `list_submissions` | List captured form submissions |
| `get_submission` | Fetch a single submission with all field responses |
| `create_coupon` | Create a discount code for checkout |
| `list_customers` | Search customers by name, email, company, address, tax id |
| `get_customer` | Fetch an individual customer record |
| `upload_file` | Upload a file from a public URL into the account |

> A separate **Zapier Checkout Page MCP** (`zapier.com/mcp/checkout-page`) also exists, exposing
> Checkout Page actions through Zapier's network — use the native `mcp.checkoutpage.com` for
> direct access, Zapier's when you want to chain Checkout Page with other Zapier apps.

## iPaaS / no-code integrations

- **Zapier** — triggers/actions + the Zapier MCP endpoint above.
- **Webhooks** — store-level and page-level (see above).
- **Google Sheets** — push conversions to a sheet.
- **Rewardful** and **Tolt** — affiliate/referral tracking.
- **Meta Pixel**, **Google Analytics** — conversion tracking.
- **Stripe Tax** — tax calculation on the seller's Stripe account.

## Official SDK

- `checkout-page/checkoutpage-api-sdk` on GitHub (`https://github.com/checkout-page`).

## Gaps (couldn't fully capture from live docs on 2026-07-04)

- Exact `POST /v1/checkout-pages` request/response bodies (docs JS-rendered; object shape
  inferred from the webhook `payment`/`subscription` data and the MCP `create_checkout_page`
  tool — verify before coding).
- Whether the endpoint path style is REST (`GET /v1/checkout-pages`) or action
  (`/v1/checkout-pages/list`) — both appeared in different rendered views.
- Any webhook signature/HMAC scheme, signing secret, or retry policy (not documented publicly —
  treat as unsigned until confirmed).
- Full Payments / Subscriptions / Products endpoint list (nav-only in the excerpt).
