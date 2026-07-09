# Shopify Platform Reference

## Overview

Shopify is the leading hosted commerce platform — storefronts, products, orders, customers, checkout, discounts, fulfillment, and headless/B2B commerce — used by everyone from solo makers on the Basic plan to enterprises on Plus. For GTM engineers and makers the value is its deep, well-versioned **GraphQL Admin API**, signed **webhooks**, and a **Storefront API** for custom front-ends. Primary differentiator vs hosted carts (ThriveCart, SamCart) and MoRs (Paddle, Lemon Squeezy): Shopify is a full commerce backend you build on, not just a checkout page — but you remain the seller of record (it is *not* a Merchant of Record, so you own tax compliance).

## Capabilities & automation surface

| Capability | Automation surface |
|---|---|
| Products, variants, collections, inventory | **API-accessible** (GraphQL Admin: `products`, `productVariants`, `inventoryLevels`) |
| Orders, draft orders, transactions, refunds | **API-accessible** + **webhook-accessible** (`orders/create`, `orders/updated`, `orders/paid`, `refunds/create`) |
| Customers, addresses, customer segments | **API-accessible** + **webhook-accessible** (`customers/create`, `customers/update`) + mandatory GDPR webhooks |
| Discounts, price rules, automatic discounts | **API-accessible** (GraphQL `discountCodeBasicCreate`, etc.) |
| Checkout (the buyer-facing payment flow) | **UI-only for layout**; customize via **Checkout Extensibility** (UI extensions, Functions) — fully customizable checkout is effectively **Plus-tier**. `checkout.liquid` + `additional scripts` are **deprecated**. |
| Storefront (themes, custom/headless front-ends) | **API-accessible** via the **Storefront API** (GraphQL, public token) + Liquid themes (UI) |
| Fulfillment, shipping, locations | **API-accessible** (GraphQL `fulfillmentOrders`, `fulfillmentCreateV2`) |
| Webhook subscriptions | **API-accessible** (GraphQL `webhookSubscriptionCreate`) or declared in `shopify.app.toml` |
| Bulk data export/import | **API-accessible** via **bulk operations** (`bulkOperationRunQuery` / `bulkOperationRunMutation`) — no per-query cost limit |
| Apps / OAuth / access scopes | **API-accessible** (OAuth for public apps; admin-generated token for custom apps) |
| Payments (Shopify Payments / 3rd-party gateways) | UI-configured; transaction data **API/webhook-accessible** |

## Pricing, limits & plan gates

*Best-effort, 2026 — pricing is region-dependent (the live page returned EUR for this run); verify current local prices and fees on shopify.com/pricing.*

| Plan | Approx. monthly (USD, billed yearly) | Online card rate (Shopify Payments) | Third-party gateway fee | Staff | API limits |
|---|---|---|---|---|---|
| **Basic** | ~$29–39 | ~2.9% + 30¢ (region-dependent) | ~2% | 0 extra | Standard (100 pts/sec GraphQL) |
| **Grow** (formerly "Shopify") | ~$79–105 | lower than Basic | ~1% | up to 5 | Standard |
| **Advanced** | ~$299–399 | lowest standard | ~0.6% | up to 15 | Advanced (200 pts/sec GraphQL) |
| **Plus** | ~$2,300+ (custom) | most competitive | ~0.2% | unlimited | **Up to ~500% higher** (1,000 pts/sec) + full data access |

Plan-gated highlights:
- **Checkout customization**: limited on Basic–Advanced; **fully customizable checkout** on Plus.
- **Headless storefronts**: 1 on Basic–Advanced; 25 on Plus.
- **B2B catalogs**: up to 3 on Basic–Advanced; unlimited on Plus.
- **Inventory locations**: 10 on Basic–Advanced; 200 on Plus.
- **Third-party transaction fees disappear** entirely if you use Shopify Payments instead of an external gateway.

**Rate limits** (see api-reference for detail): GraphQL = calculated query cost / leaky bucket (100 / 200 / 1,000 / 2,000 points/sec by plan tier; 1,000-point max per query; restore 50/sec standard). REST (legacy) = request-based leaky bucket, ~2 req/sec with a 40-request burst bucket. `429 Too Many Requests` (REST) / `THROTTLED` error (GraphQL) → exponential backoff.

## Integrations

- **Reads from / writes to**: bidirectional over the Admin API — your app can both pull (orders, customers, products) and push (create discounts, fulfill orders, update inventory).
- **Webhooks** push event data to your HTTPS endpoint, a **Google Pub/Sub** URI, or an **Amazon EventBridge** ARN.
- **Storefront API** (read-mostly for buyers) powers headless/custom front-ends with a public access token.
- **iPaaS**: large Zapier/Make ecosystems; thousands of apps in the Shopify App Store. For CRM/warehouse sync, prefer native webhooks + Admin API over polling.
- **Not a Merchant of Record** — Shopify Tax calculates tax and Shopify Payments collects, but you remit and remain the legal seller. For VAT/GST remittance handled *for* you, that's a MoR (see `/sales-merchant-of-record`).

## Data model

Key objects (GraphQL IDs are global GIDs like `gid://shopify/Order/1234567890`). Examples below are <!-- Constructed from docs — verify against live API --> unless noted.

**Order** (abridged):
```json
{
  "id": "gid://shopify/Order/1234567890",
  "name": "#1001",
  "email": "buyer@example.com",
  "createdAt": "2026-06-27T18:24:00Z",
  "updatedAt": "2026-06-27T18:25:10Z",
  "displayFinancialStatus": "PAID",
  "displayFulfillmentStatus": "UNFULFILLED",
  "totalPriceSet": { "shopMoney": { "amount": "129.00", "currencyCode": "USD" } },
  "lineItems": { "edges": [ { "node": { "title": "Starter Kit", "quantity": 1 } } ] },
  "customer": { "id": "gid://shopify/Customer/987654321", "email": "buyer@example.com" }
}
```

**Product**:
```json
{
  "id": "gid://shopify/Product/555",
  "title": "Starter Kit",
  "handle": "starter-kit",
  "status": "ACTIVE",
  "variants": { "edges": [ { "node": { "id": "gid://shopify/ProductVariant/777", "price": "129.00", "sku": "KIT-01", "inventoryQuantity": 42 } } ] }
}
```

**Webhook envelope** — the HTTP body is the resource JSON (e.g. an order); identity/verification lives in headers: `X-Shopify-Topic`, `X-Shopify-Shop-Domain`, `X-Shopify-Hmac-Sha256`, `X-Shopify-Webhook-Id`, `X-Shopify-Triggered-At`, `X-Shopify-Api-Version`.

## Quick-start recipes

### Recipe 1 — Read shop + recent orders (auth smoke test)

cURL (GraphQL Admin):
```bash
curl -X POST \
  https://your-store.myshopify.com/admin/api/2026-04/graphql.json \
  -H 'Content-Type: application/json' \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -d '{"query":"{ shop { name } orders(first: 5, sortKey: CREATED_AT, reverse: true) { edges { node { name displayFinancialStatus totalPriceSet { shopMoney { amount currencyCode } } } } } }"}'
```

Python:
```python
import os, requests
url = "https://your-store.myshopify.com/admin/api/2026-04/graphql.json"
headers = {"X-Shopify-Access-Token": os.environ["SHOPIFY_ACCESS_TOKEN"]}
query = """
{ orders(first: 5, sortKey: CREATED_AT, reverse: true) {
    edges { node { name displayFinancialStatus totalPriceSet { shopMoney { amount currencyCode } } } } } }
"""
r = requests.post(url, json={"query": query}, headers=headers, timeout=30)
data = r.json()
print(data["extensions"]["cost"]["throttleStatus"])  # watch your budget
for e in data["data"]["orders"]["edges"]:
    print(e["node"]["name"], e["node"]["totalPriceSet"]["shopMoney"]["amount"])
```
Gotcha: check `extensions.cost.throttleStatus.currentlyAvailable` and back off before it hits zero.

### Recipe 2 — Subscribe to an order webhook and verify it

Create the subscription (GraphQL):
```bash
curl -X POST https://your-store.myshopify.com/admin/api/2026-04/graphql.json \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" -H 'Content-Type: application/json' \
  -d '{"query":"mutation { webhookSubscriptionCreate(topic: ORDERS_CREATE, webhookSubscription: { callbackUrl: \"https://example.com/webhooks/orders\", format: JSON }) { userErrors { field message } webhookSubscription { id } } }"}'
```

Verify the delivery (Python/Flask) — hash the **raw** body:
```python
import hmac, hashlib, base64
from flask import request, abort

APP_SECRET = b"shpss_your_app_secret"

@app.post("/webhooks/orders")
def orders():
    raw = request.get_data()  # RAW bytes — before any JSON parsing
    digest = hmac.new(APP_SECRET, raw, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    got = request.headers.get("X-Shopify-Hmac-Sha256", "")
    if not hmac.compare_digest(expected, got):
        abort(401)  # spoofed / tampered
    # ... process request.get_json() now that it's trusted ...
    return "", 200
```
Gotcha: any middleware that parses/re-serializes the body first will break the HMAC. The three mandatory compliance topics (`customers/data_request`, `customers/redact`, `shop/redact`) must pass this check or app review fails.

### Recipe 3 — Backfill all orders without throttling (bulk operation)

```bash
curl -X POST https://your-store.myshopify.com/admin/api/2026-04/graphql.json \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" -H 'Content-Type: application/json' \
  -d '{"query":"mutation { bulkOperationRunQuery(query: \"{ orders { edges { node { id name createdAt totalPriceSet { shopMoney { amount } } } } } }\") { bulkOperation { id status } userErrors { field message } } }"}'
```
Then poll `currentBulkOperation { status url }`; when `COMPLETED`, download the JSONL from `url`. Bulk operations have **no per-query cost limit and aren't rate-limited like single queries** — this is the right tool for warehouse backfills.

## Integration patterns

- **CRM/warehouse sync**: webhooks (`orders/create`, `orders/updated`, `customers/update`) for incremental events + a periodic bulk operation as a reconciliation backstop (webhook delivery isn't guaranteed). Key on the resource `id`; dedupe with `X-Shopify-Webhook-Id`; resolve conflicts by `updated_at`.
- **Webhook listener**: respond `200` fast (queue work async — Shopify expects a quick ack); verify HMAC on raw body first; ordering is **not** guaranteed across topics, so sequence by `updated_at` / `X-Shopify-Triggered-At`. Failed deliveries are retried, then the subscription can be auto-removed after sustained failures — monitor and re-subscribe.
- **Rate-limit handling**: GraphQL — read `extensions.cost.throttleStatus`, throttle client-side to stay under the restore rate, retry `THROTTLED` with backoff+jitter. REST (legacy) — honor `Retry-After` on `429`. Large reads → bulk operations.
- **Versioning**: API versions are calendar-based and released quarterly (`YYYY-MM`, current stable `2026-04`); each version is supported ~12 months. Pin a version and schedule upgrades.
