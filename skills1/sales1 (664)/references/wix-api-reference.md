<!-- Source: https://dev.wix.com/docs/rest (REST API reference); https://dev.wix.com/docs/api-reference/business-solutions/e-commerce/orders/orders/search-orders.md; https://dev.wix.com/docs/api-reference/business-solutions/stores/catalog-v3/products-v3/query-products.md; https://dev.wix.com/docs/api-reference/articles/authentication/api-keys/make-api-calls-with-an-api-key.md; https://dev.wix.com/docs/build-apps/develop-your-app/api-integrations/events-and-webhooks/about-webhooks.md — captured 2026-06-29 -->

# Wix eCommerce — API Reference

Base host: `https://www.wixapis.com`. REST + an official JavaScript SDK (`@wix/sdk` + domain packages). Wix docs tip: **append `.md` to any `https://dev.wix.com/docs/` URL** for the markdown version; full index at `https://dev.wix.com/docs/llms.txt`, full concat at `https://dev.wix.com/docs/llms-full.txt`.

---

## Authentication

Two methods:

- **API keys** — for self-managed/headless projects, the Wix CLI, n8n, and the **Wix MCP server**. Only **account owners/co-owners** can create keys (API Keys Manager: `manage.wix.com/account/api-keys`). **API keys are NOT available to 3rd-party Wix apps** — those must use OAuth.
- **OAuth** — for published 3rd-party apps; site owners grant explicit permission on install.

### API key headers (verbatim)

Include the key in `Authorization`, plus **one** of `wix-site-id` (site-level calls — most APIs) or `wix-account-id` (account-level calls), not both.

Account-level request:
```sh
curl <GET/POST> \
  '<endpoint>' \
  -H 'Authorization: <API_KEY>' \
  -H 'wix-account-id: <ACCOUNT_ID>'
```

Site-level request:
```sh
curl <GET/POST> \
  '<endpoint>' \
  -H 'Authorization: <API_KEY>' \
  -H 'wix-site-id: <SITE_ID>'
```

### Auth quick-start — list visible products (verbatim)

```sh
curl -X POST \
  'https://www.wixapis.com/stores/v3/products/query' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <API_KEY>' \
  -H 'wix-site-id: <SITE_ID>' \
  -d '{
    "query": {
      "filter": { "visible": { "$eq": true } },
      "sort": [{ "fieldName": "createdDate", "order": "DESC" }],
      "cursorPaging": { "limit": 10 }
    }
  }'
```

### SDK equivalent (verbatim)

```js
import { createClient, ApiKeyStrategy } from "@wix/sdk";
import { productsV3 } from "@wix/stores";

const myWixClient = createClient({
  auth: ApiKeyStrategy({
    apiKey: "<API_KEY>",
    siteId: "<SITE_ID>",
    accountId: "<ACCOUNT_ID>",
  }),
  modules: { productsV3 },
});

const { products } = await myWixClient.productsV3.queryProducts({
  filter: { visible: { $eq: true } },
  cursorPaging: { limit: 10 },
});
```

### Retrieving IDs
- **Site ID** — use the account-level **Query Sites** method, or read it from the dashboard URL (after `/dashboard/`).
- **Account ID** — shown in the API Keys Manager.

---

## Stores — Query Products (v3)

- **Method/Path:** `POST https://www.wixapis.com/stores/v3/products/query`
- **Permission scopes:** `SCOPE.STORES.PRODUCT_READ` (read v3 catalog), `SCOPE.STORES.PRODUCT_READ_ADMIN` (read admin / non-visible products)

### Request body (verbatim)
```json
{
  "fields": ["URL", "CURRENCY", "DESCRIPTION", "MEDIA_ITEMS_INFO"],
  "query": {
    "cursorPaging": { "limit": 100, "cursor": "string" },
    "filter": {},
    "sort": [ { "fieldName": "createdDate", "order": "ASC" } ]
  }
}
```

### Queryable fields & operators (verbatim)
| Field | Operators | Sortable |
|-------|-----------|----------|
| `id` | `$eq, $ne, $exists, $in, $hasSome, $startsWith, $gt, $lt, $lte, $gte` | No |
| `handle` | `$eq, $ne, $exists, $in, $hasSome, $startsWith, $gt, $lt, $lte, $gte` | No |
| `options.id` | `$eq, $ne, $exists, $in, $hasSome, $startsWith, $gt, $lt, $lte, $gte` | No |
| `slug` | `$eq, $ne, $exists, $in, $hasSome, $startsWith, $gt, $lt, $lte, $gte` | Yes (ASC, DESC) |
| `createdDate` | `$eq, $ne, $exists, $in, $hasSome, $lt, $lte, $gt, $gte` | Yes (ASC, DESC) |
| `updatedDate` | `$eq, $ne, $exists, $in, $hasSome, $lt, $lte, $gt, $gte` | Yes (ASC, DESC) |
| `visible` | `$eq, $ne, $exists, $in, $hasSome` | Yes (ASC, DESC) |

### Product object (verbatim)
```json
{
  "id": "string (GUID)",
  "revision": "string (int64)",
  "createdDate": "string (date-time)",
  "updatedDate": "string (date-time)",
  "name": "string (1-80 chars)",
  "slug": "string (2-300 chars)",
  "url": { "relativePath": "string", "url": "string" },
  "description": { "nodes": [] },
  "plainDescription": "string (HTML, max 16000 chars)",
  "visible": true,
  "visibleInPos": true,
  "media": {
    "main": {
      "id": "string or url: string",
      "altText": "string",
      "displayName": "string",
      "mediaType": "IMAGE|VIDEO",
      "thumbnail": { "url": "string", "height": 0, "width": 0, "altText": "string" },
      "uploadId": "string (GUID)"
    },
    "itemsInfo": { "items": [] }
  },
  "seoData": {
    "tags": [ { "type": "string", "props": {}, "meta": {}, "children": "string", "custom": true, "disabled": false } ],
    "settings": { "preventAutoRedirect": false, "keywords": [ { "term": "string", "isMain": true, "origin": "string" } ] }
  },
  "taxGroupId": "string (GUID)",
  "options": [
    { "id": "string", "name": "string", "choices": [ { "id": "string", "value": "string" } ] }
  ],
  "productType": "PHYSICAL|DIGITAL|SERVICE",
  "physicalProperties": {
    "pricePerUnit": { "quantity": 0, "measurementUnit": "ML|CL|L|CBM|MG|G|KG|MM|CM|M|SQM|OZ|LB|FLOZ|PT|QT|GAL|IN|FT|YD|SQFT" },
    "fulfillerId": "string (GUID)",
    "shippingWeightRange": { "minValue": 0, "maxValue": 0 },
    "pricePerUnitRange": { "minValue": {}, "maxValue": {} },
    "weightMeasurementUnitInfo": { "weightMeasurementUnit": "UNSPECIFIED_WEIGHT_UNIT|KG|LB" },
    "deliveryProfileId": "string (GUID)"
  }
}
```

### Response (verbatim)
```json
{
  "products": [
    {
      "id": "string",
      "revision": "string",
      "createdDate": "2024-01-01T00:00:00Z",
      "updatedDate": "2024-01-01T00:00:00Z",
      "name": "Product Name",
      "slug": "product-name",
      "visible": true,
      "visibleInPos": true
    }
  ],
  "pagingMetadata": {
    "count": 0, "offset": 0, "total": 0,
    "cursors": { "next": "string", "prev": "string" },
    "hasNext": true, "hasPrev": false
  }
}
```

**Key notes (verbatim):** returns up to **100 products** per request; does **not** return variant data (use Get Product / Get Product By Slug / the Read-Only Variants API); non-visible products need `SCOPE.STORES.PRODUCT_READ_ADMIN`; only a narrow set of fields is filterable/sortable (unsupported fields return `Field '<fieldName>' is not declared as filterable`); for name/brand lookup use **Search Products** instead.

Related Stores endpoints (same `/stores/v3/products` base): Create / Get / Get By Slug / Update / Delete / Bulk operations / Search Products; plus Variants, Inventory, and Categories APIs.

---

## eCommerce — Search Orders

- **Method/Path:** `POST https://www.wixapis.com/ecom/v1/orders/search`
- **Permission scope:** `SCOPE.DC-STORES.READ-ORDERS`
- **Header:** `Authorization: <AUTH>`

### Request body (verbatim)
```json
{
  "search": {
    "cursorPaging": { "limit": 100, "cursor": "string" },
    "filter": {},
    "sort": [ { "fieldName": "string", "order": "ASC|DESC" } ]
  }
}
```
- `limit` 0–100 (default 100); `cursor` from a prior response; `sort` max 4 items.
- **Default:** `createdDate DESC`, `limit` 100. **Search does not return orders with `status: "INITIALIZED"`.**

### Request example — filter + sort (verbatim)
```sh
curl -X POST \
  'https://www.wixapis.com/ecom/v1/orders/search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: <AUTH>' \
  -d '{
    "search": {
      "filter": { "paymentStatus": "PAID", "fulfillmentStatus": "FULFILLED" },
      "sort": [ { "fieldName": "billingInfo.contactDetails.firstName", "order": "DESC" } ],
      "cursorPaging": { "limit": 2 }
    }
  }'
```

### Order object — key fields (abbreviated from the verbatim model)
```json
{
  "id": "string (GUID)",
  "number": "number",
  "createdDate": "string (date-time)",
  "updatedDate": "string (date-time)",
  "lineItems": [
    {
      "id": "string",
      "productName": { "original": "string", "translated": "string" },
      "catalogReference": { "catalogItemId": "string", "appId": "string", "options": {} },
      "quantity": "integer",
      "price": { "amount": "string", "formattedAmount": "string" },
      "itemType": { "preset": "UNRECOGNISED|PHYSICAL|DIGITAL|GIFT_CARD|SERVICE" },
      "paymentOption": "FULL_PAYMENT_ONLINE|FULL_PAYMENT_OFFLINE|MEMBERSHIP|DEPOSIT_ONLINE|...",
      "subscriptionInfo": {
        "id": "string (GUID)",
        "subscriptionSettings": { "frequency": "DAY|WEEK|MONTH|YEAR", "interval": "integer", "autoRenewal": "boolean", "billingCycles": "integer" }
      },
      "physicalProperties": { "weight": "number", "sku": "string", "shippable": "boolean" }
    }
  ],
  "buyerInfo": { "visitorId": "string", "memberId": "string", "contactId": "string", "email": "string (EMAIL)" },
  "paymentStatus": "UNSPECIFIED|NOT_PAID|PAID|PARTIALLY_REFUNDED|FULLY_REFUNDED|PENDING|PARTIALLY_PAID|PENDING_MERCHANT|CANCELED|DECLINED",
  "fulfillmentStatus": "NOT_FULFILLED|FULFILLED|PARTIALLY_FULFILLED",
  "currency": "string (CURRENCY)",
  "priceSummary": {
    "subtotal": { "amount": "string", "formattedAmount": "string" },
    "shipping": { "amount": "string", "formattedAmount": "string" },
    "tax": { "amount": "string", "formattedAmount": "string" },
    "discount": { "amount": "string", "formattedAmount": "string" },
    "total": { "amount": "string", "formattedAmount": "string" }
  },
  "billingInfo": { "address": {}, "contactDetails": { "firstName": "string", "lastName": "string", "phone": "string" } },
  "shippingInfo": { "title": "string", "logistics": { "deliveryTime": "string" }, "cost": {} },
  "status": "INITIALIZED|APPROVED|CANCELED|PENDING|REJECTED",
  "archived": "boolean",
  "appliedDiscounts": [ { "coupon": { "code": "string" }, "discountType": "GLOBAL|SPECIFIC_ITEMS|SHIPPING" } ],
  "activities": [ { "activityType": "ORDER_PLACED|ORDER_PAID|ORDER_FULFILLED|ORDER_CANCELED|ORDER_REFUNDED|...", "createdDate": "string" } ],
  "channelInfo": { "type": "UNSPECIFIED|WEB|POS|EBAY|AMAZON|OTHER_PLATFORM|WIX_APP_STORE|FACEBOOK|ETSY|TIKTOK|...", "externalOrderId": "string", "externalOrderUrl": "string" },
  "checkoutId": "string (GUID)",
  "balanceSummary": { "balance": {}, "paid": {}, "refunded": {} }
}
```

### Response (verbatim)
```json
{
  "orders": [ /* ...order objects... */ ],
  "metadata": {
    "count": "integer",
    "cursors": { "next": "string", "prev": "string" },
    "hasNext": "boolean"
  }
}
```

### Response example (verbatim, abbreviated)
```json
{
  "orders": [
    {
      "id": "e0e2e0e2-e0e2-e0e2-e0e2-e0e2e0e2e0e2",
      "number": 1001,
      "lineItems": [ { "id": "item-001", "productName": { "original": "Premium Wireless Headphones" }, "quantity": 1, "price": { "amount": "199.99", "formattedAmount": "$199.99" } } ],
      "buyerInfo": { "email": "customer@example.com", "contactId": "c0c0c0c0-c0c0-c0c0-c0c0-c0c0c0c0c0c0" },
      "paymentStatus": "PAID",
      "fulfillmentStatus": "FULFILLED",
      "currency": "USD",
      "priceSummary": { "subtotal": { "amount": "199.99" }, "tax": { "amount": "20.00" }, "total": { "amount": "219.99" } },
      "status": "APPROVED",
      "channelInfo": { "type": "WEB" }
    }
  ],
  "metadata": { "count": 2, "cursors": { "next": "next_cursor_token_here", "prev": "prev_cursor_token_here" }, "hasNext": true }
}
```

### Other Orders endpoints
Get Order, Update Order (only contact/address/metadata — use **Draft Orders API** to change pricing/line items), Cancel Order, Create Order (record external/POS/marketplace orders; set `channelInfo.type`). Events: **Order Approved**, **Order Updated**, **Order Canceled** (webhooks).

---

## Webhooks (verbatim, abbreviated)

Webhooks fire on real-time events (e.g. product created, order paid, app installed). Explore available events in the API Reference (the sidebar lists events next to their related methods). Register them in the Wix Developers Center.

### Verification
Event data is sent as a **signed JSON Web Token (JWT)** in the body of the webhook request. Verify authenticity using your **public key** from the Webhooks page of the app dashboard (`manage.wix.com/account/custom-apps`). The JS SDK offers a `process` method on `WixClient` to verify and decode the JWT.

Every verified/parsed webhook includes:
- `instanceId` — your app's unique identifier within the site.
- `eventType` — a description of the event.
- The rest of the data varies by event. **Webhooks don't always return the full entity** (some legacy webhooks return only updated fields) — you may need a follow-up GET to the related endpoint.

### Event delivery & redundancy
- **Timeout:** respond with **200 within 1250 ms** or delivery is retried.
- **Duplicates:** multiple copies are stored on different servers; you may receive the same event more than once — store processed event IDs and check before processing.
- **Out of order:** resent webhooks can arrive after later events.

### Resend policy (verbatim)
Up to **12** additional attempts after a failure (timeout or non-200):

| Attempt | Time |
|--|--|
| 1 | 1 minute after failure |
| 2 | 10 minutes after previous failure |
| 3 | 1 hour after previous failure |
| 4 | 2 hours after previous failure |
| 5 | 2 hours after previous failure |
| 6 | 2 hours after previous failure |
| 7 | 4 hours after previous failure |
| 8 | 4 hours after previous failure |
| 9 | 4 hours after previous failure |
| 10 | 8 hours after previous failure |
| 11 | 8 hours after previous failure |
| 12 | 12 hours after previous failure |

### Best practices (verbatim)
- Send a 200 on receipt.
- Make periodic API requests to confirm webhooks are accurate.
- Handle out-of-order and duplicate webhooks; store processed event IDs.
- Keep webhooks/app version up to date (the dashboard's **Webhooks → Logs** tab lists all deliveries).

---

## Common errors

### 403 Forbidden (verbatim)
Check that you have: an `Authorization` header with your API key; the correct **permissions** on the key; a `wix-site-id` header for site-level methods (or `wix-account-id` for account-level); a key that can access the site you're calling (site-scoped keys only work for those sites); and a key created by the **Wix user** (account owner), not a co-owner.

## Pagination
Cursor-based. Request `cursorPaging.limit` (≤ 100) and an optional `cursor`. Read the next cursor from `metadata.cursors.next` (Orders) / `pagingMetadata.cursors.next` (Products) and loop while `hasNext` is true.

## Rate limits / retry strategy
Wix doesn't publish a single global REST quota here; on `429`/`5xx` use exponential backoff. For **webhooks**, the platform side retries on your behalf (12 attempts) — your job is to return 200 within 1250 ms, be idempotent, and reconcile via periodic Search Orders pulls.

## Gaps
- Per-endpoint rate-limit headers aren't documented in the captured pages — verify against `https://dev.wix.com/docs/rest` for your specific endpoints.
- Full Create/Update Order, Cart, Checkout, Draft Orders, Inventory, and Variants request/response bodies weren't captured verbatim here — fetch the `.md` version of each from `https://dev.wix.com/docs/rest` when you need them.
