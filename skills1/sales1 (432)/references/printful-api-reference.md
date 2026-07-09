<!-- Source: https://developers.printful.com/docs/v2-beta/ and https://developers.printful.com/docs/ -->

# Printful API Reference (v2 beta + v1)

This file captures the Printful v2 (beta) REST API surface from the official developer docs, enriched with developer quick-start context. Treat all pricing/limits as best-effort and verify against the live docs.

## Authentication

- **Method:** Private token authorization (same model as v1). Two options:
  1. **OAuth 2.0 (recommended)** — `Authorization: Bearer <access_token>`.
  2. **HTTP Basic Auth** — username = API token, empty password, i.e. `Authorization: Basic base64(<api_token>:)`.
- **Base URL (v2):** `https://api.printful.com/v2/` — all v2 endpoints require the `/v2` prefix.
- **Base URL (v1, legacy):** `https://api.printful.com/` (e.g. `https://api.printful.com/orders`).
- Create/manage tokens in the Printful Dashboard. v1 API keys were migrated to tokens; new private tokens carry OAuth scopes.

### Auth quick-start — simplest GET (cURL)

```bash
# List catalog products (v2)
curl -X GET "https://api.printful.com/v2/catalog-products?limit=5" \
  -H "Authorization: Bearer $PRINTFUL_TOKEN"
```

Check the scopes on a token:

```bash
curl -X GET https://api.printful.com/v2/oauth-scopes \
  -H "Authorization: Bearer $PRINTFUL_TOKEN"
```

## Rate limiting

- **Algorithm:** leaky bucket (v2), vs v1's simple reset.
- **Default limit:** 120 requests per 60 seconds.
- **Headers:** `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset`, `X-Ratelimit-Policy`.
- **Reset behavior:** the bucket refills gradually (not all at once), so reset times shrink after the initial burst.
- **On 429:** read the `retry-after` header to determine when to retry.

### Retry snippet

```python
import time, requests

def call(method, url, **kw):
    while True:
        r = requests.request(method, url, **kw)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("retry-after", 2)))
            continue
        r.raise_for_status()
        return r.json()
```

## Core endpoints

### Catalog v2 — base `/v2/catalog-products`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/catalog-products` | GET | List products (filter, sort, paginate) |
| `/catalog-products/{id}` | GET | Single product details |
| `/catalog-products/{id}/catalog-variants` | GET | All variants for a product |
| `/catalog-variants/{id}` | GET | Single variant details |
| `/catalog-categories` | GET | List all categories |
| `/catalog-categories/{id}` | GET | Single category |
| `/catalog-products/{id}/catalog-categories` | GET | Product's categories |
| `/catalog-products/{id}/sizes` | GET | Size guide |
| `/catalog-products/{id}/prices` | GET | Product pricing |
| `/catalog-variants/{id}/prices` | GET | Variant pricing |
| `/catalog-products/{id}/images` | GET | Product images |
| `/catalog-variants/{id}/images` | GET | Variant images |
| `/catalog-products/{id}/availability` | GET | Stock availability |
| `/catalog-variants/{id}/availability` | GET | Variant stock |
| `/catalog-products/{id}/mockup-styles` | GET | Available mockup styles |

**Query params (products list):** `limit` (1–100, default 20), `offset` (default 0), `category_ids` (csv), `colors` (csv), `placements` (csv), `techniques` (`dtg`, `digital`, `cut-sew`, `uv`, `embroidery`, `sublimation`, `dtfilm`), `types`, `sort_type` (`new`, `rating`, `price`, `bestseller`), `sort_direction` (`ascending`, `descending`), `selling_region_name` (`worldwide`, `north_america`, `canada`, `europe`, `spain`, `latvia`, `uk`, `france`, `germany`, `australia`, `japan`, `new_zealand`, `italy`, `brazil`, `southeast_asia`, `republic_of_korea`), `destination_country` (ISO 3166-1 alpha-2), `new` (bool), `bestseller` (bool).

**Header:** `X-PF-Language` (`en_US`, `en_GB`, `en_CA`, `es_ES`, `fr_FR`, `de_DE`, `it_IT`, `ja_JP`).

### Orders v2 — base `/v2/orders`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/orders` | GET | List orders (paginated) |
| `/orders` | POST | Create new order (draft status) |
| `/orders/{id}` | GET | Single order details |
| `/orders/{id}` | PATCH | Update order (draft/failed only) |
| `/orders/{id}` | DELETE | Delete order |
| `/orders/{id}/confirm` | POST | Confirm order for fulfillment |
| `/orders/{id}/order-items` | GET | List order items |
| `/orders/{id}/order-items` | POST | Add item to order |
| `/orders/{id}/order-items/{item_id}` | GET | Single item |
| `/orders/{id}/order-items/{item_id}` | PATCH | Update item |
| `/orders/{id}/order-items/{item_id}` | DELETE | Remove item |
| `/orders/{id}/shipments` | GET | List shipments for order |
| `/orders/{id}/invoice` | GET | Order invoice |
| `/order-estimation-tasks` | POST | Estimate order costs (async) |
| `/order-estimation-tasks` | GET | Retrieve estimation task status |

**Order states:** `draft` (not charged, not picked up), `confirmed`, `failed`, `canceled`.

**Order item schema:**
```json
{
  "quantity": 1,
  "catalog_variant_id": 4011,
  "source": "catalog",
  "placements": [
    {
      "placement": "front",
      "technique": "dtg",
      "layers": [
        { "type": "file", "url": "{{image_url}}" }
      ]
    }
  ]
}
```

**Recipient schema:**
```json
{
  "name": "John Smith",
  "address1": "19749 Dearborn St",
  "city": "Chatsworth",
  "country_code": "US",
  "state_code": "CA",
  "zip": "91311"
}
```

**Order lifecycle:** Draft → Confirm → Processing → Shipment → Delivered. Cost is calculated **asynchronously** — an order's cost may be `calculating` initially, and it **cannot be confirmed until calculation completes**.

### Files v2 — base `/v2/files`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/files` | POST | Upload file to library |
| `/files/{id}` | GET | Retrieve file details |

### Shipping rates v2 — base `/v2/shipping-rates`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/shipping-rates` | POST | Calculate shipping rates |

```json
{
  "recipient": {
    "address1": "string", "city": "string",
    "country_code": "string", "state_code": "string", "zip": "string"
  },
  "items": [ { "catalog_variant_id": 1, "quantity": 1 } ],
  "currency": "USD"
}
```
Response includes shipping methods, rates, delivery estimates, and a `customs_fees_possible` flag.

### Mockup generator v2 — base `/v2/mockup-tasks`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mockup-tasks` | POST | Create mockup generation task |
| `/mockup-tasks` | GET | Retrieve task status/results |

```json
{
  "format": "jpg",
  "products": [
    {
      "source": "catalog",
      "mockup_style_ids": [16652],
      "catalog_product_id": 294,
      "catalog_variant_ids": [9231],
      "placements": [
        {
          "placement": "front",
          "technique": "dtg",
          "layers": [ { "type": "file", "url": "{{image_url}}" } ]
        }
      ]
    }
  ]
}
```
**Task statuses:** `pending`, `completed`, `failed`. Poll the task or subscribe to the `mockup_task_finished` webhook.

### Warehouse products v2 — base `/v2/warehouse-products`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/warehouse-products` | GET | List warehouse products |
| `/warehouse-products/{id}` | GET | Single warehouse product |

### Countries v2 — base `/v2/countries`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/countries` | GET | List countries (ISO codes, names) |

### Stores v2 — base `/v2/stores`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/stores` | GET | List stores |
| `/stores/{id}` | GET | Single store details |
| `/stores/{id}/statistics` | GET | Store statistics |

### Approval sheets v2 — base `/v2/approval-sheets`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/approval-sheets` | GET | List approval sheets |
| `/approval-sheets/{id}/download` | GET | Download PDF |

### OAuth scopes v2 — base `/v2/oauth-scopes`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/oauth-scopes` | GET | Retrieve scopes for the token |

## Webhooks v2 — base `/v2/webhooks`

v2 webhooks improve on v1: **HTTPS enforced**, **request signing**, **expiration date**, and **per-event configuration**.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhooks` | GET | Get webhook configuration |
| `/webhooks` | POST | Set up webhook |
| `/webhooks` | DELETE | Disable webhook |
| `/webhooks/events` | GET | Get event configuration |
| `/webhooks/events` | POST | Set up event |
| `/webhooks/events/{event_id}` | DELETE | Disable event |

**Webhook event types:**
`shipment_sent`, `shipment_delivered`, `shipment_returned`, `shipment_out_of_stock`, `shipment_canceled`, `order_created`, `order_updated`, `order_failed`, `order_canceled`, `catalog_stock_updated`, `catalog_price_changed`, `order_put_hold`, `order_put_hold_approval`, `order_remove_hold`, `order_refunded`, `mockup_task_finished`, `shipment_put_hold`, `shipment_put_hold_approval`, `shipment_remove_hold`.

> Reliability note from the docs: even when using webhook events, use the GET endpoint as a backup in case a message is never received. For mockup tasks, set the server up to poll task status to improve reliability.

## Pagination

Uniform across endpoints — offset/limit with HATEOAS `_links`:

```json
{
  "paging": { "total": 100, "offset": 10, "limit": 20 },
  "_links": {
    "self": {"href": "..."},
    "next": {"href": "..."},
    "previous": {"href": "..."},
    "first": {"href": "..."},
    "last": {"href": "..."}
  }
}
```

## Error format

Follows **RFC 9457 (Problem Details for HTTP APIs)**; content type `application/problem+json`:

```json
{
  "type": "https://developers.printful.com/docs/v2-beta/#errors/not-found",
  "status": 404,
  "title": "Not Found",
  "detail": "The resource that you tried to access does not exist.",
  "instance": "unique-error-id"
}
```

## Response conventions

- Times: ISO 8601, UTC.
- Prices: string with up to 2 decimal points.
- All responses include `_links` (HATEOAS).

## Key concepts

- **Catalog product vs variant:** products are blank templates; variants are physical items (specific color/size). **Always use variant IDs when creating orders.**
- **Cost calculation:** asynchronous; status may be `calculating` initially. Cannot confirm an order until calculation completes.
- **Embroidery:** v2 supports auto thread-color detection and multi-layer designs with positioning.
- **Mockups:** generated asynchronously via the task system; retrieve via polling or the `mockup_task_finished` webhook.

## Gaps

- Exact v1 endpoint paths/JSON were not captured verbatim here; v2-beta is the primary reference. For legacy v1, consult `https://developers.printful.com/docs/`.
- v2 is labeled **beta**; field names and availability can change — re-verify against live docs before relying on specifics.
- Webhook payload field schemas (per event) are summarized from docs, not pasted field-by-field — confirm the exact JSON for each event in the live reference.
