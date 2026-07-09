<!-- Source: https://developers.printify.com/ (single-page API reference, fetched 2026-07-04). Official OpenAPI spec: https://developers.printify.com/openapi.json · Postman collection: https://developers.printify.com/postman/printify_postman_collection.json -->

# Printify API Reference

Curated verbatim capture of the key sections of the official docs. The full reference is one large page at developers.printify.com; endpoint list below is extracted from the official OpenAPI 3.0.3 spec (`Printify Public API`, version 1.0.0).

## API basics (verbatim)

> All requests are done via HTTPs. Requests via insecure HTTP are not supported.
> Printify API works with UTF-8 encoded data. Please make sure everything you send over in API calls also uses UTF-8.
> All data received from API and submitted to API is JSON, so the content type should be: `application/json;charset=utf-8`
> Date/time values returned by Printify API are in UTC unless stated otherwise.
> The base URL for all endpoints is `https://api.printify.com/v1/`.
> The API currently does not support CORS and requests from a frontend application will not be processed for security reasons. You will need to set up a server-side application to access the API and ensure secure storing of the API token.

All requests must also specify a **`User-Agent` header** — the type of client ("NodeJS", "PHP") or the name of your application. Requests without it can be rejected.

## Rate limits (verbatim)

> Printify has the following global limit in place for API requests: **600 requests per minute.** Customers exceeding this limit will receive error responses with a 429 response code.
> All Catalog API endpoints have a separate rate limit of **100 requests per minute** per integration (per account, not per access token) in addition to the global API limit.
> The product publishing endpoint has a limit of **200 requests per 30 minutes**; product creation as a result of Order creation is not limited.
> Requests resulting in an error response may not exceed 5% of your total requests.

Limits are per **account**, not per access token — multiple tokens don't multiply your quota.

## Authentication

Two methods; unless an endpoint says otherwise, both work everywhere.

### Personal Access Token (individual merchants)

Generated in **My Profile → Connections** with selectable access scopes. Verbatim notes:

> For security purposes, this token will only be visible immediately after generating only.
> Access tokens are valid for **one year**, they expire after that timeframe and you will need to generate a new one to replace it.

Quick-start cURL (verbatim example from docs):

```bash
curl -X GET https://api.printify.com/v1/shops.json --header "Authorization: Bearer $PRINTIFY_API_TOKEN"
```

Response:

```json
[
  { "id": 5432, "title": "My new store", "sales_channel": "My Sales Channel" },
  { "id": 9876, "title": "My other new store", "sales_channel": "disconnected" }
]
```

Use the shop `id` in every `{shop_id}` placeholder, e.g. `GET /v1/shops/5432/products.json`.

### OAuth 2.0 (platforms managing multiple merchants)

Requires app registration (review takes up to 1 week). Flow: send merchant to `https://printify.com/app/authorize?app_id=x&accept_url=…&decline_url=…&state=123` → grant code appended to `accept_url` → exchange at `POST /v1/app/oauth/tokens` (`app_id`, `code`) → returns `access_token`, `refresh_token`, `expire_at`. **Access tokens expire after 6 hours**; refresh at `POST /v1/app/oauth/tokens/refresh` (`app_id`, `refresh_token`). Verbatim caveats:

> Printify access tokens will fluctuate in size as we change the information that is encoded in the tokens. We recommend allowing for tokens to be up to 3,000 characters.
> For security reasons, the accept and decline URL must use https in production. … you must use a domain, as IP addresses are not supported.

### Access scopes (verbatim table)

| Scope | Notes |
|---|---|
| `shops.read` | Access shops in a Merchant's account |
| `catalog.read` | See Products and Print Providers from the Printify Product Catalog |
| `products.read` | See products created in a Merchant's shop |
| `products.write` | Create products in a Merchant's shop |
| `orders.read` | See orders created in a Merchant shop |
| `orders.write` | Create orders in a Merchant's shop |
| `webhooks.read` | Read installed webhooks |
| `webhooks.write` | Install, update and delete Webhooks |
| `uploads.read` | See uploaded files in a Merchant's account |
| `uploads.write` | Upload image files and archive them |
| `print_providers.read` | See available print providers |

## Pagination

Page-based. Responses wrap `data` with (verbatim property examples): `"first_page_url": "/?page=1"`, `"prev_page_url": "/?page=2"`, `"next_page_url": "/?page=4"`, `"last_page_url": "/?page=5"`, `"current_page": 3`, `"last_page": 5`, `"total": 49`, `"per_page": 10`, `"from": 21`, `"to": 30`. Iterate by following `next_page_url` until `null`, or pass `?page=N` (+ `?limit=N` where supported, e.g. products max 100/page, orders 10/page).

## Endpoints (from the official OpenAPI spec)

### Shops
| Method | Path | Summary |
|---|---|---|
| GET | `/v1/shops.json` | Retrieve list of shops in a Printify account |
| DELETE | `/v1/shops/{shop_id}/connection.json` | Disconnect a shop |

### Catalog (100 req/min limit)
| Method | Path | Summary |
|---|---|---|
| GET | `/v1/catalog/blueprints.json` | Retrieves list of blueprints in the catalog |
| GET | `/v1/catalog/blueprints/{blueprint_id}.json` | Retrieve a specific blueprint |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers.json` | Print providers that fulfill orders for a blueprint |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers/{print_provider_id}/variants.json` | Variants of a blueprint from a specific print provider |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers/shipping.json` | Retrieve shipping information |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers/shipping/standard.json` | Standard shipping method information |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers/shipping/priority.json` | Priority shipping method information |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers/shipping/express.json` | Express shipping method information |
| GET | `/v1/catalog/blueprints/{blueprint_id}/print_providers/shipping/economy.json` | Economy shipping method information |
| GET | `/v2/catalog/blueprints/{blueprint_id}/print_providers/{print_provider_id}/shipping.json` | Available shipping list information (v2) |
| GET | `/v1/catalog/print_providers.json` | Retrieve a list of available print providers |
| GET | `/v1/catalog/print_providers/{print_provider_id}.json` | Retrieve a specific print provider |

### Products
| Method | Path | Summary |
|---|---|---|
| GET | `/v1/shops/{shop_id}/products.json` | Retrieve a list of products |
| POST | `/v1/shops/{shop_id}/products.json` | Create a new product |
| GET | `/v1/shops/{shop_id}/products/{product_id}.json` | Retrieve a product |
| PUT | `/v1/shops/{shop_id}/products/{product_id}.json` | Update a product |
| DELETE | `/v1/shops/{shop_id}/products/{product_id}.json` | Delete a product |
| POST | `/v1/shops/{shop_id}/products/{product_id}/publish.json` | Publish a product (200 req/30 min limit) |
| POST | `/v1/shops/{shop_id}/products/{product_id}/publishing_succeeded.json` | Set product publish status to succeeded |
| POST | `/v1/shops/{shop_id}/products/{product_id}/publishing_failed.json` | Set product publish status to failed |
| POST | `/v1/shops/{shop_id}/products/{product_id}/unpublish.json` | Notify that a product has been unpublished |
| GET | `/v1/shops/{shop_id}/products/{product_id}/gpsr.json` | Retrieve product GPSR information |

### Orders
| Method | Path | Summary |
|---|---|---|
| GET | `/v1/shops/{shop_id}/orders.json` | Retrieve a list of orders |
| POST | `/v1/shops/{shop_id}/orders.json` | Submit an order |
| GET | `/v1/shops/{shop_id}/orders/{order_id}.json` | Get order details by ID |
| POST | `/v1/shops/{shop_id}/orders/{order_id}/cancel.json` | Cancel an order |
| POST | `/v1/shops/{shop_id}/orders/{order_id}/send_to_production.json` | Send an existing order to production |
| POST | `/v1/shops/{shop_id}/orders/shipping.json` | Calculate the shipping cost of an order |
| POST | `/v1/shops/{shop_id}/orders/express.json` | Submit a Printify Express order |

### Uploads
| Method | Path | Summary |
|---|---|---|
| GET | `/v1/uploads.json` | Retrieve a list of uploaded images |
| GET | `/v1/uploads/{image_id}.json` | Retrieve an uploaded image by id |
| POST | `/v1/uploads/images.json` | Upload an image (by `url` or base64 `contents`) |
| POST | `/v1/uploads/{image_id}/archive.json` | Archive an uploaded image |

### Webhooks
| Method | Path | Summary |
|---|---|---|
| GET | `/v1/shops/{shop_id}/webhooks.json` | Retrieve a list of webhooks |
| POST | `/v1/shops/{shop_id}/webhooks.json` | Create a new webhook |
| PUT | `/v1/shops/{shop_id}/webhooks/{webhook_id}.json` | Modify a webhook |
| DELETE | `/v1/shops/{shop_id}/webhooks/{webhook_id}.json?host={webhook_host}` | Delete a webhook (`host` param required — deletion only succeeds if the webhook's URL host matches, preventing accidental deletion of another host's webhooks) |
| POST | `/v1/shops/{shop_id}/webhooks/{webhook_id}/simulate` | Simulate a webhook (request body is echoed in the webhook `resource` property) |

## Key request examples (verbatim from docs)

### Create a new product — `POST /v1/shops/{shop_id}/products.json`

```json
{
  "title": "Product",
  "description": "Good product",
  "blueprint_id": 384,
  "print_provider_id": 1,
  "variants": [
    { "id": 45740, "price": 400, "is_enabled": true },
    { "id": 45742, "price": 400, "is_enabled": true },
    { "id": 45744, "price": 400, "is_enabled": false }
  ],
  "print_areas": [
    {
      "variant_ids": [45740, 45742, 45744],
      "placeholders": [
        {
          "position": "front",
          "images": [
            { "id": "5d15ca551163cde90d7b2203", "x": 0.5, "y": 0.5, "scale": 1, "angle": 0 }
          ]
        }
      ]
    }
  ]
}
```

Notes: `price` is in **cents**. `variants[].id` and image placeholder `position` values come from the catalog variants endpoint. A `safety_information` field (GPSR contact + care instructions) is supported and required for EU sales. Embroidery is supported — pick an embroidery blueprint/variant and check supported positions/decoration methods via the variants endpoint.

### Submit an order (existing product) — `POST /v1/shops/{shop_id}/orders.json`

```json
{
  "external_id": "2750e210-39bb-11e9-a503-452618153e4a",
  "label": "00012",
  "line_items": [
    { "product_id": "5bfd0b66a342bcc9b5563216", "variant_id": 17887, "quantity": 1, "external_id": "line-item-abc-001" }
  ],
  "shipping_method": 1,
  "is_printify_express": false,
  "is_economy_shipping": false,
  "send_shipping_notification": false,
  "address_to": {
    "first_name": "John", "last_name": "Smith",
    "email": "example@example.com", "phone": "0574 69 21 90",
    "country": "BE", "region": "", "address1": "ExampleBaan 121", "address2": "45",
    "city": "Retie", "zip": "2470"
  }
}
```

Response: `{ "id": "5a96f649b2439217d070f507" }`

### Submit an order that creates the product on the fly (simple positioning)

```json
{
  "external_id": "2750e210-39bb-11e9-a503-452618153e5a",
  "line_items": [
    {
      "print_provider_id": 5,
      "blueprint_id": 9,
      "variant_id": 17887,
      "print_areas": { "front": "https://images.example.com/image.png" },
      "quantity": 1
    }
  ],
  "shipping_method": 1,
  "address_to": { "…": "same shape as above" }
}
```

Advanced positioning: `print_areas.front` can instead be an array of `{ "src", "scale", "x", "y", "angle" }` layers. Product creation via order submission is **not** counted against the publishing rate limit.

## Webhooks & events

### Rules (verbatim)

> Printify will send a POST request to the URL you specify when the event occurs. This POST request will contain a JSON payload with information about the event. The expected response is a `200 OK`.
> In case of a 4xx or 5xx response, Printify will retry the request up to 3 times, after which the webhook will be **blocked** for 1 hour. If the webhook is blocked, no new requests will be sent to the URL until the block is lifted.

### Event types (verbatim tables)

| Event | Description |
|---|---|
| `shop:disconnected` | The shop was disconnected. |
| `product:deleted` | The product was deleted. |
| `product:created` | The product was created. |
| `product:updated` | The product was updated. |
| `product:publish:started` | The product publishing was started. |
| `order:created` | The order was created. |
| `order:updated` | The order's status was updated. |
| `order:sent-to-production` | The order was sent to production. |
| `order:shipment:created` | Some/all items have been fulfilled. |
| `order:shipment:delivered` | Some/all items have been delivered. |

### Event payload shape (verbatim)

```json
{
  "id": "653b6be8-2ff7-4ab5-a7a6-6889a8b3bbf5",
  "type": "order:created",
  "created_at": "2017-04-18 13:24:28+00:00",
  "resource": {
    "id": "5cb87a8cd490a2ccb256cec4",
    "type": "order",
    "data": { "shop_id": 1234567 }
  }
}
```

`resource.type` is `shop`, `product`, or `order`. `product:*` events carry `data.shop_id` only (re-fetch the product via the API); `product:publish:started` also carries `publish_details` (`title`, `description`, `images`, `variants`, `tags`, `key_features`, `shipping_template`) and an `action` of `create`/`update`/`delete` — your integration must publish to the sales channel and then call the `publishing_succeeded`/`publishing_failed` endpoint to unlock the product.

### Create a webhook (verbatim)

```json
POST /v1/shops/{shop_id}/webhooks.json
{ "topic": "order:created", "url": "https://example.com/webhooks/order/created" }
```

Response: `{ "topic": "order:created", "url": "https://example.com/webhooks/order/created", "shop_id": "1", "id": "5cb87a8cd490a2ccb256cec4" }`

Webhook properties: `id` (read-only), `topic` (required, immutable), `url` (required), `shop_id` (read-only), `secret` (optional — enables signing).

### Securing webhooks — `X-Pfy-Signature` (verbatim)

> You can generate the secret by running `openssl rand -hex 20`. When your secret token is set, Printify will use it to create a hash signature with each payload body. Printify uses an HMAC hexdigest to compute the hash sha256 signature with your provided secret.
> This payload body signature is passed along with each request in the headers as `X-Pfy-Signature`. The signature format is: `sha256={digest}`.

Example header: `x-pfy-signature: sha256=4260d30ec4ee2a17181ae5072c846d8dfcb5ceb195e24de055fd9a21d8c6648f`

Validation sample (verbatim, Python):

```python
import os
import hmac

def sha256hash(request):
    hash = hmac.new(os.environ['SECRET_TOKEN'].encode('utf-8'),
                    request.data.encode('utf-8'),
                    'sha256')
    return 'sha256=' + hash.hexdigest()

def secure_compare(a, b):
    return hmac.compare_digest(a, b)

print('%r' % secure_compare(request.headers['x-pfy-signature'],
                            sha256hash(request)))
```

Always use constant-time comparison (`hmac.compare_digest`), never `==`.

## Errors & retry strategy

- `429 Too Many Requests` — over a rate limit (global 600/min, catalog 100/min, publish 200/30 min). Back off exponentially; no documented `Retry-After` header, so start at ~2s and double. Keep error responses under 5% of total traffic or the account can be throttled.
- `400` on OAuth token endpoints returns `{ "error": "error_code", "error_description": "A human readable error message" }`.
- Validation errors return standard HTTP codes with a JSON error body.

## Gaps

- Full JSON schemas for every endpoint live in the OpenAPI spec (`https://developers.printify.com/openapi.json`) — fetch it for exhaustive request/response models; only the highest-traffic examples are reproduced here.
- v2 API exists only for the catalog shipping endpoint above; everything else is v1.
