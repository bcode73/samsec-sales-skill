<!-- Source: https://help.customcat.com/getting-started-with-customcat-api and https://customcat-beta.mylocker.net/api/v1/ (CustomCat API v1, captured 2026-06-29 via WebFetch). The CustomCat homepage and pricing page bot-block WebFetch (HTTP 403); this reference was assembled from the fetchable help/API-docs pages. Re-verify endpoint shapes and field names against the live docs (which the API summarizer condensed) before relying on them. CustomCat states "you must work with a qualified software developer" — they do not offer dev services. -->

# CustomCat API v1 — Reference

## Base URL

```
https://customcat-beta.mylocker.net/api/v1/
```

## Authentication

- **Method**: API key passed in the request (query parameter for GETs, body for POSTs as `api_key`).
- **Key types**: a **read-only** key and a **read-write** key. Most write actions (submit/cancel order, register webhook) require the **read-write** key. Generate/manage both in **Settings > Store > API**; treat them like passwords.
- **Transport**: **TLS required** — plain HTTP requests are rejected.

## Endpoints

### Catalog

- `GET /catalog` — list all products (paginated, filterable by category/subcategory). Returns images, weights, inventory status, etc.
- `GET /catalog/{catalog_product_id}` — single product details
- `GET /catalog/sku/{catalog_sku_id}` — product by SKU

**Parameters**: `api_key` (required), `category`, `subcategory`, `page`, `limit` (max 250)

### Catalog Categories

- `GET /catalogcategory` — all categories/subcategories (filter the catalog by decoration method or style)
- `GET /catalogcategory/{category_url_slug}` — a specific category

### Design

- `GET /design` — list designs (paginated)

**Parameters**: `api_key`, `page`, `limit`, `since_id`, `updated_since`

### Product (your created products)

- `GET /product` — list the user's products (paginated)
- `GET /product/{product_id}` — single product

**Parameters**: `api_key`, `page`, `limit`, `since_id`, `updated_since`

### Order

- `POST /order/{order_id}` — create/submit an order
- `DELETE /order/{order_id}` — cancel an order
- `GET /order/status/{order_id}` — order status
- `POST /order/replacement/{order_id}` — replacement order (requires special permission)

**Required fields (POST)**: `shipping_first_name`, `shipping_last_name`, `shipping_email`, `shipping_phone`, `shipping_address1`, `shipping_city`, `shipping_state`, `shipping_zip`, `shipping_country`, `shipping_method`, `items` (array)

**Items array**:
- Using CustomCat products: `sku`, `quantity`
- Using external designs: `catalog_sku`, `design_url`, `quantity` (optional: `design_url_back`, `mockup_url`, `mockup_url_back`, `preset_id`, `use_embedded_dpi`)

**Optional order fields**: `shipping_address2`, `shipping_label`, `seller_name`, `seller_phone`, `seller_address*`, `sandbox`

### Shipping

- `GET /shipping` — available shipping methods
- `POST /shipping/{shipping_id}` — calculate shipping cost

**Parameters**: `api_key`, `country`/`country_code`, `state`, `items` (array)

### Webhook

- `GET /webhook` — list webhooks
- `POST /webhook` — register a webhook
- `PUT /webhook` — update a webhook
- `DELETE /webhook/{webhook_id}` — remove a webhook

**Required**: `api_key`, `topic`, `url`

**Available topics**:
- `order-shipped`
- `order-partial-shipment`
- `product-created`, `product-deleted`, `product-updated`
- `design-rejected`

> Webhooks are delivered as HTTP POSTs by CustomCat. They are **not HMAC-signed** — the payload embeds your **read-only** `api_key` so you can verify it originated from CustomCat. Keep a `GET /order/status/{order_id}` polling backup; delivery is best-effort.

## Response schemas

### Order create response

```json
{
  "ORDER_ID": "Your_Order_ID",
  "MSG": "Order added successfully",
  "CUSTOMCAT_ORDER_ID": "UUID"
}
```

### Order status response

```json
{
  "ORDER_ID": "TestOrder1",
  "CUSTOMCAT_ORDER_ID": "UUID",
  "ORDER_DATE": "March, 27 2018 12:14:45",
  "ORDER_STATUS": "Pending|Verified|Shipped",
  "ORDER_TOTAL": 19.47,
  "CUSTOMER_NAME": "Joe Testing",
  "CUSTOMER_ADDRESS1": "1300 Rosa Parks Blvd",
  "CUSTOMER_ADDRESS2": "",
  "CUSTOMER_CITY": "Detroit",
  "CUSTOMER_STATE": "MI",
  "CUSTOMER_ZIP": "48216",
  "CUSTOMER_COUNTRY": "USA",
  "LINE_ITEMS": [{
    "STATUS": "Processing|Picked/Received|Printed|Binned|Ready to Ship|Shipped|Failed QA|Cancelled",
    "PRODUCT_NAME": "...",
    "PRODUCT_COLOR_ID": 10258
  }],
  "SHIPMENTS": [{
    "TRACKING_ID": "92748901790443643406596477",
    "METHOD": "Expedited Mail Innovations",
    "VENDOR": "UPS",
    "NUMBER_ITEMS": 1
  }]
}
```

### Webhook payloads

**Order Shipped** (`order-shipped`):
```json
{
  "api_key": "Read-Only API key",
  "order_id": "Your_Order_Id",
  "customcat_order_id": "CustomCat's_Order_Id",
  "tracker_number": "Tracking_Number",
  "tracking_url": "Tracking_URL"
}
```

**Order Partial Shipment** (`order-partial-shipment`):
```json
{
  "api_key": "Read-Only API key",
  "order_id": "Your_Order_Id",
  "customcat_order_id": "CustomCat's_Order_Id",
  "tracker_number": "Tracking_Number",
  "tracking_url": "Tracking_URL",
  "items_remaining": 5
}
```

**Product Created** (`product-created`):
```json
{
  "api_key": "Read-Only API key",
  "product_id": "Product_Id",
  "message": "Product Created",
  "product_url": "https://customcat-beta.mylocker.net/api/v1/product/{Product_Id}"
}
```

**Design Rejected** (`design-rejected`):
```json
{
  "design_url": "design_url",
  "reason": "Reason design was rejected",
  "orders": [{
    "order_id": "your_order_id",
    "customcat_order_id": "CustomCat_Order_id",
    "items": [{
      "catalog_sku": "catalog_sku",
      "quantity": "quantity ordered"
    }]
  }]
}
```

## Design placement presets

**Digisoft™**:
- No preset: exact placement; transparent space preserved
- `preset_id=1`: Left Chest (wider than tall)
- `preset_id=2`: Full Front
- `preset_id=3`: Full Back
- `preset_id=4`: Default Center Chest
- `preset_id=9`: Default Back Placement
- `preset_id=10`: Left Chest (taller than wide)

**Sublimation**:
- No preset: exact edge-to-edge placement
- `preset_id=4`: Default centered

**Hats/Caps with Leather Patches**:
- No preset / `preset_id=2`: Rectangle Patch
- `preset_id=12`: Oval Patch
- `preset_id=14`: Circle Patch
- `preset_id=18`: Small Circle Patch

## Maximum printable areas (Digisoft)

| Product | Max area (inches) |
|---|---|
| Adult Crewneck Front/Back | 11.41 × 15.11 |
| Adult V-Neck Front | 11.41 × 12.12 |
| Adult Hoodie Front | 11.41 × 11.41 |
| Youth Front/Back | 10 × 12 |
| Youth Hoodie Front | 10 × 10 |

## Sandbox mode

- Parameter: `sandbox=1` in the request body (use `sandbox=0` or omit for production orders).

## HTTP status codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 304 | Not Modified |
| 400 | Bad Request |
| 401 | Unauthorized (missing/incorrect API key) |
| 403 | Forbidden (read-only key on a write operation) |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |
| 502 | Bad Gateway |

## Common 400 error messages

- `Duplicate Order` — order id already processed (the `order_id` is the idempotency key)
- `Invalid state` — shipping state not found
- `Invalid Country` — country code invalid
- `There is an issue with the order. SKU: {sku}` — out of stock
- `Invalid Shipping Method` — method not in `/shipping` results
- `Customer Email Required` — email missing
- `Invalid Shipping Address` — failed AVS check (US addresses)
- `Charge Failed` — payment processor declined

## Address Verification (AVS)

All addresses are verified for completeness; US addresses are additionally validated against an authoritative postal database. When validation fails, the response includes a `suggestions` array for correction.

**Example error response**:
```json
{
  "error_description": "Conflicting ZIP Code/city/state information.",
  "suggestions": [{
    "address1": "123 Elm Street",
    "address2": "",
    "city": "Charlotte",
    "state": "MI",
    "zipcode": "48813",
    "country": "US"
  }]
}
```

## Design file requirements & fees

- Design files: **300 DPI**, or declare embedded DPI via `use_embedded_dpi`.
- **Back print adds a $5 fee per line item.**

## Setup workflows (documented)

1. Sellers using CustomCat mockups + fulfillment
2. Sellers with custom mockups, CustomCat fulfillment only
3. Platform operators (custom mockups, fulfillment only)
4. Platform operators managing seller integrations (CustomCat handles seller support)

## Notes / gaps

- **No explicit rate limits documented.** Be courteous; cache catalog reads.
- The homepage and `/pricing` page bot-block WebFetch (HTTP 403); pricing here is from third-party reviews and the help center — re-verify on the live site.
- "Custom API access" is called out as an **Enterprise** plan benefit for higher-touch integrations.
