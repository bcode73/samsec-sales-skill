<!-- Source: https://developer.paddle.com/api-reference/overview -->
<!-- Source: https://developer.paddle.com/api-reference/about/authentication -->
<!-- Source: https://developer.paddle.com/webhooks/overview -->
<!-- Captured 2026-06-27. Base URLs, auth, entity list, webhook signing + ordering rules are from the
     official docs. Request/response JSON is CONSTRUCTED from documented entities and marked — verify
     against the live reference / Postman collection. THIS IS THE PADDLE BILLING API (not Paddle Classic). -->

# Paddle (Billing) API Reference

Paddle has **two incompatible products**: **Paddle Classic** (legacy) and **Paddle Billing** (current).
They have **different base URLs, auth models, object schemas, and webhooks** — code/tutorials for one do
**not** work on the other. **Build on Paddle Billing.** Because Paddle is a **Merchant of Record**, the API
manages *your* catalog/customers/subscriptions while Paddle remains the legal seller (it collects + remits
sales tax/VAT for you).

## Base URLs & authentication

- **Production:** `https://api.paddle.com`
- **Sandbox:** `https://sandbox-api.paddle.com` (separate account + keys; test here first)
- **Auth:** `Authorization: Bearer YOUR_API_KEY`. Create keys in **Paddle → Developer Tools →
  Authentication → API keys**. Treat like a password; **set an expiry**. Client-side tokens exist for
  browser checkout (separate from secret API keys).
- **Methods:** REST — `GET` (list/read), `POST` (create), `PATCH` (update). Most entities aren't hard-deleted;
  you **archive** them via `PATCH status=archived`.

### Auth quick-start (list products)

```bash
curl -s "https://api.paddle.com/products?per_page=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Core entities

| Group | Entities |
|---|---|
| Catalog | **products**, **prices**, discounts, discount groups |
| Customers | **customers**, addresses, businesses, payment methods |
| Billing | **transactions**, **subscriptions**, adjustments (refunds/credits), pricing-preview |
| Events | events, event-types, **notifications**, notification-settings (webhook destinations), logs |
| Reports | subscribers, MRR, churn, chargebacks, conversions, refunds, revenue |
| Dev tools | client-side tokens, IP-address lookup, webhook simulator |

## Pagination & includes

- **List responses are paginated:** pass `per_page` and follow `meta.pagination.next` (cursor-style URL).
  Responses wrap data as `{ "data": [...], "meta": { "pagination": { "next": "...", "has_more": true } } }`.
- **`include`** fetches related entities in one call (e.g. `GET /subscriptions/{id}?include=next_transaction`).
- Filter with query params (e.g. `?status=active&customer_id=ctm_...`).

## Top endpoint examples

<!-- JSON CONSTRUCTED from documented entities — verify against the live reference / Postman -->

### 1. Create a product (POST /products)
```bash
curl -s -X POST "https://api.paddle.com/products" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Pro plan", "tax_category": "saas", "type": "standard" }'
```
```json
{ "data": { "id": "pro_01h...", "name": "Pro plan", "tax_category": "saas", "status": "active" } }
```

### 2. Create a price (POST /prices)
```json
{ "data": { "id": "pri_01h...", "product_id": "pro_01h...",
  "unit_price": { "amount": "2000", "currency_code": "USD" },
  "billing_cycle": { "interval": "month", "frequency": 1 } } }
```
> Amounts are **strings in the smallest currency unit** (e.g. `"2000"` = $20.00). A common bug is sending
> dollars instead of cents.

### 3. Get a subscription with its next transaction (GET /subscriptions/{id}?include=next_transaction)
```bash
curl -s "https://api.paddle.com/subscriptions/sub_01h...?include=next_transaction" -H "Authorization: Bearer $KEY"
```
```json
{ "data": { "id": "sub_01h...", "status": "active", "customer_id": "ctm_01h...",
  "items": [ { "price_id": "pri_01h...", "quantity": 1 } ],
  "current_billing_period": { "starts_at": "2026-06-01T00:00:00Z", "ends_at": "2026-07-01T00:00:00Z" } } }
```

### 4. Cancel a subscription (POST /subscriptions/{id}/cancel)
```bash
curl -s -X POST "https://api.paddle.com/subscriptions/sub_01h.../cancel" -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d '{ "effective_from": "next_billing_period" }'
```

### 5. List transactions (GET /transactions)
```json
{ "data": [ { "id": "txn_01h...", "status": "completed", "customer_id": "ctm_01h...",
  "details": { "totals": { "grand_total": "2000", "tax": "350", "currency_code": "USD" } } } ],
  "meta": { "pagination": { "has_more": false, "next": null } } }
```

## Webhooks (notifications)

Configure a **notification destination** (webhook) in the dashboard or via `/notification-settings`. Paddle
sends **signed HTTP POST** events. Key events:

- **Subscriptions:** `subscription.created`, `subscription.activated`, `subscription.updated`,
  `subscription.canceled`, `subscription.paused`, `subscription.resumed`, `subscription.past_due`,
  `subscription.trialing`.
- **Transactions:** `transaction.created`, `transaction.updated`, `transaction.billed`,
  `transaction.completed`, `transaction.payment_failed`.
- **Customers/addresses:** `customer.created/updated`, `address.created/updated`, `business.created/updated`,
  `adjustment.created` (refunds/chargebacks).

**Verify every webhook (HMAC-SHA256).** Paddle signs the raw body with a per-destination secret; compute
`HMAC-SHA256(secret, "ts:body")` and compare to the `Paddle-Signature` header (`ts=...;h1=...`).

<!-- Verification pattern — confirm header parsing against the live webhook docs -->
```python
import hmac, hashlib
def verify(raw_body: bytes, signature_header: str, secret: str) -> bool:
    parts = dict(p.split("=", 1) for p in signature_header.split(";"))
    ts, h1 = parts["ts"], parts["h1"]
    signed = f"{ts}:{raw_body.decode()}".encode()
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, h1)
```

**Event payload (shape):** <!-- Constructed — verify -->
```json
{ "event_id": "evt_01h...", "event_type": "subscription.activated",
  "occurred_at": "2026-06-27T10:00:00Z", "notification_id": "ntf_01h...",
  "data": { "id": "sub_01h...", "status": "active", "customer_id": "ctm_01h..." } }
```

> **Ordering is NOT guaranteed** — a `subscription.updated` can arrive before `subscription.created`. Order
> your processing by **`occurred_at`**, and make handlers **idempotent on `event_id`** (Paddle can redeliver).

## Rate limits & errors

- The API is rate-limited (per-key); on `429` respect the rate-limit headers and back off. Errors return a
  standard `{ "error": { "type": "...", "code": "...", "detail": "..." } }` envelope.

```python
import requests, time
def paddle(method, path, key, base="https://api.paddle.com", **kw):
    h = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    for attempt in range(5):
        r = requests.request(method, f"{base}{path}", headers=h, timeout=30, **kw)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(2 ** attempt); continue
        r.raise_for_status(); return r.json()
    r.raise_for_status()
```

## Docs MCP

Paddle ships a **documentation MCP server** ("Docs MCP") so AI assistants (Claude/Cursor) can answer Paddle
API questions from the live docs. It's a docs-retrieval aid, not an account-data API — use the REST API +
Bearer key for actual billing operations.

## Gaps / not documented here

- Exact field schemas per entity: use the **Postman collection** / live reference — JSON above is constructed.
- Precise numeric rate limits and the full event-type enum: confirm in the live webhook/limits docs.
- **Paddle Classic** is a separate legacy API (`vendors.paddle.com`/`checkout.paddle.com`, vendor-id+auth-code,
  different events) — out of scope here; migrate Classic integrations to Billing.
