<!-- Source: https://github.com/Ecwid/ecwid-api-docs (official docs markdown source, includes/_overview.md, _authentication.md, _webhooks.md, fetched 2026-07-04) + live docs at https://docs.ecwid.com/api-reference. -->

# Ecwid API Reference

Curated verbatim capture of the official Ecwid REST API docs. The complete reference is huge (per-entity markdown files: `_orders.md` 130KB, `_products.md` 138KB, etc. in the GitHub repo) — this file covers auth, limits, pagination, and webhooks; fetch entity files from the repo for full field lists.

## Basics

- Base URL: `https://app.ecwid.com/api/v3/{storeId}` — e.g. `https://app.ecwid.com/api/v3/1003/profile`
- All REST API calls require an **access token** passed as a **Bearer token** in the `Authorization` header (header only — not query parameters).
- JSON in/out; gzip supported via `Accept-Encoding: gzip`.
- **Rate limit: up to 600 requests per minute per token.** Exceeding returns `429` with a `Retry-After: N` header (seconds).
- **API access requires a paid plan** — the docs note you need "a registered application and a test Ecwid store on a paid plan."

Quick-start cURL:

```bash
curl "https://app.ecwid.com/api/v3/$STORE_ID/profile" \
  -H "Authorization: Bearer $ECWID_SECRET_TOKEN"
```

## Authentication & token types

| Token | Prefix | Use |
|---|---|---|
| Secret token | `secret_*` | "grants full REST API access (must be kept private; never expose publicly)" |
| Public token | `public_*` | "safe for storefront use, but limited to public/low-risk operations and data" |

**Your own store (custom app)**: in the Ecwid admin, open the app dashboard → your custom app **Details** page and copy the access token — these are **non-expiring**.

**Public apps (OAuth 2.0)** — verbatim flow from `_authentication.md`:

> 2. Your code requests an access token from Ecwid in the background. This access_token will be used as API key in all API calls.

Exchange the temporary `code` (single-use, lives a few minutes) for the token; response shape:

```json
{ "access_token": "secure_123453lasdADSKasasdjasdklasASkmns" }
```

> access_token | Private authorization token. This is a key your app will use to access Ecwid API on behalf of the user.

Access scopes gate both API calls and webhooks (e.g. `read_catalog` for product webhooks, `read_orders` for order webhooks).

## Main endpoint groups

Store profile · Products (+ variations/combinations, categories, product classes, filters) · Orders (+ abandoned/unfinished sales) · Customers (+ customer groups) · Coupons/Promotions · Batch API · Application storage · Custom Payment API · Custom Shipping API · SSO · Storefront JS API. Full per-entity docs: `https://github.com/Ecwid/ecwid-api-docs/tree/master/includes` and `https://docs.ecwid.com/api-reference`.

Pagination on list endpoints: `offset` + `limit` query params (default/max limit 100), responses carry `total`, `count`, `offset`, `limit` — iterate until `offset + count >= total`.
<!-- Pagination pattern constructed from docs conventions — verify against live API -->

## Webhooks

### How they work (verbatim)

> - Ecwid will use the `Webhook URL` from your application details to send any available webhooks to that single URL
> - When a merchant installs your application, the webhooks for this store are automatically enabled
> - Each supported event in the store (e.g. new order is placed) triggers an HTTP POST request to the URL your specified

Endpoints must be HTTPS, accept POST, and reply `200 OK`. Events use the `entity.action` format.

### Supported entities (verbatim)

> - Abandoned sale (created, updated, deleted)
> - Order (created, updated, deleted)
> - Product (created, updated, deleted)
> - Category (created, updated, deleted)
> - Customer (created, updated, deleted)
> - Store profile (updated, subscription plan updated)
> - Application (installed, subscription status updated, uninstalled)

### Request (verbatim example)

```http
POST https://www.myapp.com/callback?eventtype=order.updated HTTP/1.1
Host: www.myapp.com
Content-Type: application/json; charset=UTF-8
Content-Length: 243
Cache-Control: no-cache
X-Ecwid-Webhook-Signature: MeV28XtFal4HCkYFvdilwckJinc6Dtp4ZWpPhm/pzd4=
```

Custom HTTP headers can be added to webhook requests (configured via Ecwid support); they're **added** to the defaults.

### Payload (verbatim example)

```json
{
  "eventId": "80aece08-40e8-4145-8764-6c2f0d38678",
  "eventCreated": 1234567,
  "storeId": 1003,
  "entityId": -1,
  "eventType": "unfinished_order.created"
}
```

Payloads are thin — an ID + event type. Re-fetch the entity via the REST API for actual data. Verbatim guidance:

> Receive a request from Ecwid every time a new product is created or an existing product is changed; so you can synchronize the store catalog with your local database. Decide if you need to update your database. If yes, get the updated product data from Ecwid REST API and make your app in sync in one HTTP request instead of downloading the whole catalog.

> Don't use webhooks themselves as actionable items.

### Signature verification (verbatim)

> The signature is an encoded string generated by concatenating the following webhook data (delimiter is a dot `.`):
> - eventCreated (webhook event timestamp)
> - eventId (webhook event ID)
> The resulting string is encoded using HMAC SHA-256 and using `client_secret` as the shared secret key.
> **Important: `client_secret` is not your access token that looks like `secret_*`. It is a separate value you received, when you registered the application with Ecwid.**

Validation steps (verbatim):

> 1. Get the signature from the request headers
> 2. Get `eventCreated` and `eventId` values from the request body
> 3. Encode the string *'{eventCreated}.{eventId}'* using HMAC SHA256 (using `client_secret` as the shared secret key) and pass it through Base64 encoding
> 4. Compare the resulting string with the received webhook signature

Official PHP example (verbatim, abridged):

```php
<?php
// Get contents of webhook request
$requestBody = file_get_contents('php://input');
$client_secret = 'abcde123456789'; // your client_secret value sent to you after the app registration. NOT your 'secret_*' access token.

// Parse webhook data
$decodedBody = json_decode($requestBody, true);

$eventId = $decodedBody['eventId'];
$eventCreated = $decodedBody['eventCreated'];
$storeId = $decodedBody['storeId'];
$entityId = $decodedBody['entityId'];
$eventType = $decodedBody['eventType'];
```

Python equivalent:

```python
import base64, hmac, hashlib

def verify(headers, body_json, client_secret):
    msg = f"{body_json['eventCreated']}.{body_json['eventId']}".encode()
    digest = hmac.new(client_secret.encode(), msg, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(headers.get("X-Ecwid-Webhook-Signature", ""), expected)
```

## Errors & retry strategy

- `429 Too Many Requests` → wait the seconds given in `Retry-After`, then retry. Limit is per token (600/min).
- `401` — missing/invalid Bearer token; `403` — token lacks the required scope or the plan doesn't include API access.
- Standard HTTP codes with JSON error bodies (`errorMessage`/`errorCode` fields per `_errors.md`).

## Gaps

- The GitHub markdown repo is the docs *source* but the live reference (docs.ecwid.com/api-reference) is periodically restructured — verify endpoint details there before building.
- Full request/response models for orders/products/customers are in the repo's per-entity files (too large to inline here).
- No MCP server found; Zapier and Make apps exist for no-code automation.
