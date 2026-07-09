<!-- Source: https://developer.fastspring.com/reference/getting-started-with-your-api , https://developer.fastspring.com/reference/webhooks-overview , https://developer.fastspring.com/reference/createsession , https://fastspring.com/docs/classic/fastspring-s-apis/ (captured 2026-07-02) -->

# FastSpring API Reference

FastSpring exposes a **modern REST API** (`https://api.fastspring.com`) plus the **Store Builder Library (SBL)**
JavaScript library for client-side checkout, and **webhooks** for event-driven integration. The legacy
**Classic Commerce API** was moved to GitHub (`https://github.com/fastspring/fastspring-api`) and is deprecated —
build on the modern API.

> Much of developer.fastspring.com is JS-rendered; the endpoint-level request/response schemas below are
> captured from the live docs where fetchable and otherwise marked `<!-- Constructed from docs — verify against live API -->`.
> Re-verify exact fields against the live docs before relying on them.

## Base URL & environment

- **Base URL:** `https://api.fastspring.com`
- **Test vs live:** there is no separate host — a single store has **test mode** and **live mode**; API calls
  and webhooks are scoped by a `live` boolean (webhook configs choose live / test / both).

## Authentication

FastSpring uses **HTTP Basic Authentication** with Base64-encoded credentials:

- **Method:** Basic Auth — `Authorization: Basic base64(username:password)`.
- **Generation:** create credentials in the FastSpring app under **Developer Tools > APIs > API Credentials**
  (Create command). **The password is displayed only during the initial creation session** — store it then.
- Credentials are **specific to your store**.

### Required headers on every request

| Header | Value |
|---|---|
| `Authorization` | `Basic <base64 username:password>` |
| `User-Agent` | **Mandatory** — an identifier for your integration |
| `Content-Type` | `application/json` |
| (TLS) | **TLS 1.2 or later required** |

### Auth quick-start (cURL — simplest GET)

```bash
# List/query orders (Basic auth = -u user:pass, which curl base64-encodes for you)
curl https://api.fastspring.com/orders \
  -u "$FS_API_USER:$FS_API_PASSWORD" \
  -H "User-Agent: my-integration/1.0" \
  -H "Content-Type: application/json"
```

## Rate limits

- **250 calls per IP per minute.** Exceeding it returns **`429 Too Many Requests`**.
- Docs recommend **batch requests** for high-volume operations (many endpoints accept comma-separated ID lists,
  e.g. `GET /orders/{id1},{id2},{id3}`).

### Rate-limit retry (Python)

```python
import time, requests

def fs_get(path, auth, params=None, attempts=5):
    url = f"https://api.fastspring.com{path}"
    headers = {"User-Agent": "my-integration/1.0", "Content-Type": "application/json"}
    for i in range(attempts):
        r = requests.get(url, auth=auth, headers=headers, params=params)
        if r.status_code == 429:
            time.sleep(2 ** i)   # exponential backoff; no documented reset header — back off blind
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate-limited after retries")
```

## Data format conventions

- **Encoding:** UTF-8.
- **Numeric precision:** 2-decimal-point precision for all prices and discounts.
- **String length:** max VARCHAR 255.
- **Country codes:** ISO 3166-2, uppercase (e.g. `US`, `CA`, `DE`).
- **Language codes:** ISO 639-1, lowercase (e.g. `en`, `fr`).
- **Responses:** JSON over HTTPS.

## Endpoint catalog

Endpoints (resource groups) exposed by the modern API. Paths follow `https://api.fastspring.com/{resource}`.

| Resource | Typical operations |
|---|---|
| **Products** | Create or update products; list all product paths; retrieve a product; delete a product; create/update **offers**; list all **product prices**; retrieve offers; retrieve a product price. Pricing is returned **adjusted by country + currency** (VAT/GST inclusive per region). |
| **Orders** | Retrieve orders (single, comma-separated batch, or by date/search); orders are read-oriented (created by checkout, not the API). |
| **Subscriptions** | Query subscriptions (filters below); retrieve; **update** (plan/quantity/price); **cancel**; **pause / resume**; get subscription entries/instances. |
| **Accounts** | Create; update; retrieve; list customer accounts; generate a customer **authenticated URL** (management/portal). |
| **Coupons / promotions** | Manage coupon codes and generated codes. |
| **Sessions / Checkouts** | Create a **checkout session** (server-side) to launch a branded checkout — see below. |
| **Quotes** | B2B interactive quotes (create/manage) with e-signature. |
| **Returns** | Retrieve returns/refunds. |
| **Events** | Retrieve/replay stored webhook events (processed/unprocessed). |
| **Webhooks** | Manage webhook configuration and rotate the HMAC key secret via the API. |

### Products — pricing note (verbatim)

> "FastSpring updates its currency exchange rates every 6 hours." The docs recommend **calling the pricing
> endpoint at least daily** so your app reflects current exchange rates. Request region-specific pricing with an
> ISO 2-char **country** code (returns price with VAT/GST for that region) and an ISO 3-char **currency** code
> (converts regardless of the country's default currency).

### Subscriptions — query parameters (verbatim)

Core parameters:
- `accountId` — filter by account association
- `begin` / `end` — date-range filter (`yyyy-mm-dd`)
- `product` — filter by specific product IDs

Event types (used with a date range): `canceled`, `charged`, `created`, `deactivated`, `trialended`, `trialstarted`

Scope: `live` (production only) · `test` (test-mode only)

Status filters: `active` (incl. trial) · `canceled` (canceled, not yet deactivated) · `deactivated` (fully
deactivated) · `overdue` (failed rebill) · `trial`

### Checkout session (create)

<!-- Captured from https://developer.fastspring.com/reference/createsession — verify path against live docs; SBL is the more common embed path -->

```
POST https://api.fastspring.com/v2/checkouts/{checkoutPath}/sessions
```

- **Path param `checkoutPath`** (required): format `store-id/checkout-id` (e.g. `fastspring/main`).
- **Request body:**

| Param | Type | Notes |
|---|---|---|
| `locale` | string | Language code (max 5 chars); defaults to browser locale |
| `country` | string | 2-letter ISO country code |
| `buyerIp` | string | IPv4/IPv6 (max 39 chars); infers country/currency |
| `live` | boolean | `true` = live, `false` = test (defaults `true`) |
| `customer` | object | Customer + billing information applied to the order session |
| `orderTags` | object | Custom metadata key-value map (**authenticated requests only**) |
| `cart` | object | Line items and promotions |
| `paymentMethodsOrder` | array | Payment-method sort order (**authenticated only**) |
| `hidePaymentMethods` | array | Filter payment methods from the buyer UI (**authenticated only**) |

- **Responses:** `201` created (returns `id`, `checkoutUrls.webcheckoutUrl` to redirect the buyer, and
  `checkoutStatus`); `400` bad request; `401` unauthorized.

## Store Builder Library (SBL)

- JavaScript library for **client-side checkout** (popup or embedded) — the common way to launch checkout from a
  website without a server round-trip.
- **Access Key** obtained under **Developer Tools > Store Builder Library** — used to encrypt secure payloads
  (e.g. server-signed carts) so buyers can't tamper with prices.
- Loads a store storefront (`{store}.onfastspring.com`) and drives it via JS (`fastspring.builder.push(...)`,
  add/remove products, tags, checkout).

## Webhooks

### Configuration

1. **Developer Tools > Webhooks > Configuration** → **Add Webhook**.
2. Enter a title; choose **live / test / both** orders.
3. Add a URL endpoint — **HTTPS recommended**, port **443** default (alternatives: 3443, 8282, 9191, 9000, 9999).
4. Select the event types to receive.
5. Optionally enable **webhook expansion** to receive full JSON payloads (otherwise events may carry references).

### Security — HMAC SHA256

- Optionally set a **secret** on the webhook config → FastSpring signs each payload with **HMAC SHA256**.
- The signature arrives in the **`X-FS-Signature`** header as a **Base64-encoded HMAC-SHA256 of the raw request body**.
- **Verify the signature on your backend over the raw body before processing** — treat verification as mandatory.
- Rotate the secret via **`Update a webhook key secret`** in the API; ensure your server can validate the new key
  before switching, then discard the old one.

### Payload structure

A webhook request is a JSON object with an **`events` array**. Each event contains:

| Field | Meaning |
|---|---|
| `id` | Unique event id — **use for deduplication** (events can be redelivered) |
| `live` | Boolean — production vs test |
| `processed` | Boolean flag |
| `type` | Event name (see list below) |
| `created` | Timestamp in **milliseconds** |
| `data` | Event-specific payload |

<!-- Constructed from docs — verify against live API -->
```json
{
  "events": [
    {
      "id": "abc123DEF456",
      "live": true,
      "processed": false,
      "type": "order.completed",
      "created": 1719000000000,
      "data": {
        "order": "AB1-CD2-EF3",
        "account": { "id": "acct_123", "contact": { "email": "buyer@example.com" } },
        "items": [{ "product": "my-saas-pro", "quantity": 1 }],
        "total": 49.00,
        "currency": "USD"
      }
    }
  ]
}
```

### Event types

**Account:** `account.created`, `account.updated`

**Order:** `order.completed`, `order.failed`, `order.canceled`, `order.approval.pending`,
`order.payment.pending`, `chargeback.created`

**Subscription:** `subscription.activated`, `subscription.updated`, `subscription.canceled`,
`subscription.uncanceled`, `subscription.deactivated`, `subscription.charge.completed`,
`subscription.charge.failed`, `subscription.payment.overdue`, `subscription.payment.reminder`,
`subscription.trial.reminder`, `subscription.paused`, `subscription.resumed`

**Co-term / grouped subscriptions:** `subscription.group.created`, `subscription.group.prorated`,
`subscription.group.updated`, `subscription.group.payment.charge.completed`,
`subscription.group.payment.charge.failed`, `subscription.group.deactivated`

**Additional domains:** quote, payout, return, fulfillment, and mailing-list events.

### Webhook verification snippet (Python)

<!-- Constructed from docs — verify against live API -->
```python
import base64, hashlib, hmac
from flask import Flask, request, abort

app = Flask(__name__)
FS_SECRET = b"your-webhook-hmac-secret"

@app.post("/fastspring/webhook")
def fastspring_webhook():
    raw = request.get_data()  # RAW body — do not re-serialize
    sig = request.headers.get("X-FS-Signature", "")
    expected = base64.b64encode(hmac.new(FS_SECRET, raw, hashlib.sha256).digest()).decode()
    if not hmac.compare_digest(sig, expected):
        abort(401)
    payload = request.get_json()
    for event in payload.get("events", []):
        # dedupe on event["id"] (events can be redelivered); switch on event["type"]
        if event["type"] == "order.completed":
            provision_access(event["data"])
        elif event["type"] == "subscription.charge.failed":
            start_dunning(event["data"])
    return ("", 200)
```

## Integrations & extensions

- **Native extensions / connectors:** Salesforce, HubSpot, and other out-of-the-box integrations (Developer
  Tools > Extensions / Integrations).
- **iPaaS:** Zapier (triggers/actions) and similar via webhooks.
- **Mobile / game checkout:** FastSpring **Steer Safe** integrations for React Native and Unity/UGS (iOS & Android).
- **Community SDKs:** Laravel Cashier driver (`bgultekin/cashier-fastspring`); license-management integrations
  (e.g. Cryptlex).

## Error handling

- Standard HTTP status codes: `400` (bad request / invalid fields), `401` (bad/missing auth), `429` (rate limit).
- Error bodies are JSON; validate field-level errors from the response body.
<!-- The docs did not expose a single canonical error envelope; capture the exact shape from a live 4xx before coding against it. -->

## Gaps / not captured verbatim

- Full request/response JSON for **each** endpoint (orders, subscriptions update/cancel/pause, accounts) — the
  reference pages are JS-rendered; the operations and parameters above are captured, but confirm exact field
  names and payloads against the live docs.
- Exact canonical **error envelope** shape.
- Whether the checkout-session path is `/v2/checkouts/{checkoutPath}/sessions` in all store configurations vs the
  classic `POST /sessions` — verify against your store's live docs.
