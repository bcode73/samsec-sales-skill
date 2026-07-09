<!-- Source: https://shopify.dev/docs/api/admin -->
<!-- Source: https://shopify.dev/docs/api/admin-rest -->
<!-- Source: https://shopify.dev/docs/api/usage/rate-limits -->
<!-- Source: https://shopify.dev/docs/apps/build/webhooks -->
<!-- Captured 2026-06-27 via WebFetch. Shopify dev docs are partly JS-rendered; sections below are quoted verbatim where the fetch returned text and clearly marked where JSON/code is constructed from the documented fields. Re-verify against live docs before relying on specifics. -->

# Shopify Admin API Reference

## GraphQL Admin API — overview (verbatim)

The Shopify Admin API is available in GraphQL format. GraphQL is the primary interface for "building apps and integrations that extend and enhance the Shopify admin."

### Base URL structure
Requests are sent via POST to:
```
https://{store_name}.myshopify.com/admin/api/{version}/graphql.json
```
The current API version referenced is `2026-04`.

### API versioning
Shopify uses a calendar-based versioning scheme. The endpoint structure incorporates the specific API version, allowing developers to target particular release cycles. (Versions are released quarterly as `YYYY-MM` and each is supported for ~12 months.)

### Authentication
"All GraphQL Admin API requests require a valid Shopify access token."

Authentication methods include:
- **OAuth**: Used for "public and custom apps created in the Dev Dashboard."
- **Admin-generated tokens**: Custom apps created within Shopify admin receive direct authentication.
- **Access scopes**: Apps must "request specific access scopes during the install process."

Tokens are passed via the `X-Shopify-Access-Token` header for direct requests.

### Auth quick-start (cURL, verbatim example)
```bash
curl -X POST \
  https://{shop}.myshopify.com/admin/api/2026-04/graphql.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}' \
  -d '{"query": "query { shop { name } }"}'
```

---

## REST Admin API — status & deprecation (verbatim)

### Legacy status
"The REST Admin API is a legacy API as of October 1, 2024."

### New apps & GraphQL requirement
"Starting April 1, 2025, all new public apps must be built exclusively with the GraphQL Admin API."

### Base URL pattern
```
https://{store_name}.myshopify.com/admin/api/2026-01/{resource}.json
```
The current API version shown in examples is `2026-01`.

### Migration guidance
Shopify provides a migration guide for developers transitioning from REST to GraphQL, acknowledging that "Some newer platform features may only be available in GraphQL."

> Practical note: REST endpoints still respond, but are frozen — no new fields/features. Build new integrations on GraphQL.

---

## Rate limiting (verbatim)

### GraphQL Admin API — calculated query cost (leaky bucket)
"Each app has access to a bucket. It can hold, say, 60 'marbles'. Each API request tosses some number of marbles into the bucket. Each second, a marble is removed from the bucket (if there are any)."

#### Points per second by plan
| Plan Tier | Rate Limit |
|-----------|-----------|
| Standard | 100 points/second |
| Advanced Shopify | 200 points/second |
| Shopify Plus | 1000 points/second |
| Shopify for enterprise (Commerce Components) | 2000 points/second |

#### Query cost structure
Field costs vary by return type:
- Scalars/Enums: 0 points
- Objects: 1 point
- Mutations: 10 points
- Connections: Sized by `first` and `last` arguments

A single query cannot exceed 1,000 points regardless of plan.

#### Response format — cost metadata in the `extensions` key (verbatim)
```json
"extensions": {
  "cost": {
    "requestedQueryCost": 101,
    "actualQueryCost": 46,
    "throttleStatus": {
      "maximumAvailable": 1000,
      "currentlyAvailable": 954,
      "restoreRate": 50
    }
  }
}
```

#### Error handling
When rate limits are exceeded, apps receive a `429 Too Many Requests` response (REST) or a `THROTTLED` error (GraphQL), requiring exponential backoff retry logic (add jitter).

### REST Admin API — request-based leaky bucket
Uses the "Leaky Bucket" algorithm with a bucket that holds **40 requests** with a refill rate of **2 requests per second**. On overflow you receive `429 Too Many Requests`; honor the `Retry-After` header.

### Bulk operations
"To query and fetch large amounts of data, developers should use bulk operations instead of single queries. Bulk operations are designed for handling large amounts of data and don't have the max cost limits or rate limits that single queries have."

---

## Webhooks (verbatim + documented fields)

### How webhooks work
1. App subscribes to a topic (e.g. `orders/create`)
2. App specifies an endpoint to receive webhooks
3. When the event occurs, Shopify publishes a webhook
4. Shopify delivers the webhook with headers and payload to the subscription endpoint

### Subscription methods
Subscriptions can be declared through:
- the **`shopify.app.toml`** configuration file
- the **GraphQL Admin API** (`webhookSubscriptionCreate`)

"A subscription declares which topic to watch and where to send deliveries: a URL, Google Pub/Sub URI, or Amazon EventBridge ARN."

### Delivery formats
- HTTPS endpoints (hosted by app server)
- Google Pub/Sub URIs
- Amazon EventBridge ARNs

### Webhook topics
"A topic identifies the resource and action that qualifies a delivery." Common examples include `products/create`, `products/update`, and `orders/create`. (Other common topics: `orders/updated`, `orders/paid`, `orders/cancelled`, `refunds/create`, `customers/create`, `customers/update`, `fulfillments/create`, `app/uninstalled`.)

### Mandatory compliance (GDPR) webhooks
Public apps must implement and pass automated checks for three mandatory topics:
- `customers/data_request`
- `customers/redact`
- `shop/redact`

Each must respond `200` with a valid HMAC or app review fails.

### Security: HMAC verification (verbatim)
Each delivery includes the header `X-Shopify-Hmac-Sha256` for signature verification. Use the app secret to validate deliveries: compute the HMAC-SHA256 of the **raw request body** using the app's API secret, base64-encode it, and compare to the header value using a timing-safe comparison.

Verification example <!-- Constructed from docs — verify against live API -->:
```python
import hmac, hashlib, base64
def verify(raw_body: bytes, hmac_header: str, app_secret: bytes) -> bool:
    digest = hmac.new(app_secret, raw_body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, hmac_header)
```

### Headers on each delivery
`X-Shopify-Topic`, `X-Shopify-Shop-Domain`, `X-Shopify-Hmac-Sha256`, `X-Shopify-Webhook-Id`, `X-Shopify-Triggered-At`, `X-Shopify-Api-Version`.

### Reliability (verbatim)
- **No guaranteed ordering**: "Events across topics may arrive out of sequence." Use timestamps (`X-Shopify-Triggered-At` header or payload `updated_at`) to organize events.
- **Implement reconciliation**: "Your app shouldn't rely on receiving data from Shopify webhooks. Webhook delivery isn't always guaranteed." Reconcile against the Admin API.

---

## Top-5 endpoint patterns (constructed from documented GraphQL operations)

<!-- Constructed from docs — verify operation names/fields against the live GraphQL reference for version 2026-04 -->

### 1. List orders (read)
```graphql
query {
  orders(first: 10, sortKey: CREATED_AT, reverse: true) {
    edges { cursor node { id name displayFinancialStatus totalPriceSet { shopMoney { amount currencyCode } } } }
    pageInfo { hasNextPage endCursor }
  }
}
```

### 2. Get one order (read)
```graphql
query { order(id: "gid://shopify/Order/1234567890") { id name email displayFulfillmentStatus } }
```

### 3. Create a product (mutation, costs 10)
```graphql
mutation { productCreate(input: { title: "Starter Kit", status: ACTIVE }) {
  product { id title } userErrors { field message } } }
```

### 4. Update a product (mutation)
```graphql
mutation { productUpdate(input: { id: "gid://shopify/Product/555", status: DRAFT }) {
  product { id status } userErrors { field message } } }
```

### 5. Delete a product (mutation)
```graphql
mutation { productDelete(input: { id: "gid://shopify/Product/555" }) {
  deletedProductId userErrors { field message } } }
```

### Pagination pattern
GraphQL connections use **cursor-based** pagination: pass `first: N` (or `last: N`) and follow `pageInfo.hasNextPage` + `pageInfo.endCursor` into the next request's `after:` argument. (Legacy REST used `Link` headers with `page_info` cursors.)

### Error response shape
GraphQL returns HTTP `200` with an `errors` array for query/validation problems and `userErrors` inside mutation payloads for business-rule failures; rate limiting surfaces as a `THROTTLED` error in `errors[].extensions.code`. Always check both `errors` and `userErrors`, not just the HTTP status.

### Rate-limit retry snippet
```python
import time, random
def with_backoff(call, max_tries=6):
    for attempt in range(max_tries):
        resp = call()
        cost = resp.get("extensions", {}).get("cost", {})
        throttled = any(e.get("extensions", {}).get("code") == "THROTTLED"
                        for e in resp.get("errors", []) or [])
        if not throttled:
            return resp
        time.sleep((2 ** attempt) + random.random())  # exp backoff + jitter
    raise RuntimeError("still throttled after retries")
```

---

## Storefront API (brief)

A separate **GraphQL Storefront API** powers custom/headless front-ends and the buyer experience (products, collections, cart, checkout). It authenticates with a **public Storefront access token** (not the Admin token) and is rate-limited separately. Use it for headless storefronts; use the Admin API for back-office automation.

## Gaps

- Exact per-field GraphQL costs and the full topic catalog are JS-rendered in the live reference; confirm against `shopify.dev/docs/api/admin-graphql/{version}`.
- Region-specific pricing and card rates were returned in EUR for this capture — verify USD/local rates on `shopify.com/pricing`.
- The official REST→GraphQL migration field mapping lives in Shopify's migration guide (not captured verbatim here).
