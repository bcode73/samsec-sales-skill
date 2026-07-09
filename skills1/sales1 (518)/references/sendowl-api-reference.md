<!-- Source: https://dashboard.sendowl.com/developers/api/introduction (and /products, /orders, /subscriptions, /licenses); https://help.sendowl.com/help/using-web-hooks -->
<!-- Captured 2026-07-02. Copied/condensed from live SendOwl developer docs. Some request/response JSON is reproduced verbatim from the docs; a few field lists are summarized where the source page was prose. Verify against the live API before relying on specifics. -->

# SendOwl API Reference

## Authentication

API calls use **HTTP Basic Auth** with an **API key and secret**. Enable and retrieve credentials at **Settings → SendOwl API** (`https://dashboard.sendowl.com/settings/api_credentials`). Credentials must be enabled before use.

```
curl -H "Accept: application/json" https://KEY:SECRET@api.sendowl.com/api/v1/products
```

## Base URL & versions

- Base: `https://api.sendowl.com/`
- Most resources: `/api/v1/...`
- **Orders resource uses `/api/v1_3/...`** (e.g. `/api/v1_3/orders`). Some order sub-actions remain on `/api/v1/` (refund, resend_email, cancel_subscription, download_restrictions, override_country). Match the version shown per endpoint below.

## Formats

Both **XML** and **JSON** are supported. Set the format via headers:
- `Accept: application/json` or `Accept: text/xml`
- `Content-Type` required on POST/PUT.

You can also suffix the path (`.xml` / `.json`) as shown in some examples.

## Pagination

Results default to **10 per page**, starting at **page 1**. Use `per_page` (max **50**) and `page`:

```
GET /api/v1/products?per_page=50&page=2
```

## Rate limiting

> "Generally speaking you should not call the API more than once per second or your IP address may be blocked."

Contact support for higher rates.

## Errors

Invalid requests return **HTTP 422** with error details in the requested format (XML or JSON). Other codes appear per endpoint (400, 403, 409, etc.).

---

## Products

### GET /api/v1/products
Retrieves all products.

```json
[
  {
    "product": {
      "id": 1,
      "name": "Curing RSI:Beta (first version)",
      "product_type": "digital",
      "price": 17,
      "currency_code": "USD",
      "created_at": "2010-08-30T16:53:10Z",
      "updated_at": "2011-05-28T14:08:20Z",
      "instant_buy_url": "https://www.sendowl.com/products/1/X4J5B018/purchase",
      "add_to_cart_url": "https://www.sendowl.com/products/1/X4J5B018/add_to_cart",
      "pdf_stamping": true,
      "price_is_minimum": false,
      "attachment": { "filename": "cure-rsi.pdf", "size": 1087311 },
      "drip_items": []
    }
  }
]
```

### GET /api/v1/products/{product_id}
Returns one product (same shape as above, single object).

### GET /api/v1/products/search?term={term}
Searches products by name; returns list-format results.

### GET /api/v1/products/shopify_lookup?variant_id={variant_id}
Looks up products associated with a Shopify variant ID; list-format results.

### POST /api/v1/products
Creates a product. Use a **multi-part form** request with `product[field]` syntax.

```
curl -X POST https://KEY:SECRET@api.sendowl.com/api/v1/products.xml \
  -F "product[name]=Test" \
  -F "product[product_type]=digital" \
  -F "product[price]=12.50" \
  -F "product[attachment]=@/filepath.png"
```
Response: **201** with the created product and a `Location` header.

### PUT /api/v1/products/{product_id}
Updates a product.
```json
{ "product": { "name": "My new product" } }
```
Response: **200** on success, **422** on error.

### DELETE /api/v1/products/{product_id}
Deletes a product. Response: **200** on success.

### POST /api/v1/products/{product_id}/issue
Issues an order for a product (custom gateways / third-party integrations).
```json
{
  "order": {
    "buyer_name": "Mr Buyer",
    "buyer_email": "myemail@myprovider.com",
    "financial_transaction": {
      "payment_gross": 9.99,
      "payment_tax": 0.99,
      "payment_currency": "USD"
    }
  }
}
```
Response: the created order object.

---

## Orders (v1_3)

### GET /api/v1_3/orders
Returns all orders. Query parameters:
- `from` / `to` — date range for order creation
- `updated_after` — ISO 8601 datetime; orders updated at/after this time (use for incremental sync)
- `orderable` — filter by `Product-{id}`, `Package-{id}` (bundle), or `Subscription-{id}`
- `state` — filter by order state
- `referred_by` — filter by affiliate ID
- `sort` — `newest_first` to reverse order

```json
[{
  "order": {
    "id": 3101,
    "state": "complete",
    "gateway": "PayPal",
    "buyer_email": "testuser@gmail.com",
    "buyer_name": "Test User",
    "settled_currency": "GBP",
    "settled_gross": "64.90",
    "settled_tax": "5.90",
    "refunded": false,
    "created_at": "2011-05-17T06:05:56Z",
    "updated_at": "2011-05-17T06:15:13Z"
  }
}]
```

### GET /api/v1_3/orders/search
- `?term={term}` — searches buyer email, name, giftee details, business name, or transaction ID
- `?email={email}` — orders matching exact buyer email

### GET /api/v1_3/orders/{order_id}
Returns one order with full detail, including refund transactions:
```json
{
  "order": {
    "id": 3101,
    "state": "complete",
    "gateway": "PayPal",
    "buyer_email": "testuser@gmail.com",
    "buyer_name": "Test User",
    "settled_gross": "64.90",
    "refunded": true,
    "refund_transactions": [
      { "refund_transaction": {
          "amount": "-3.00", "currency": "GBP",
          "occurred_at": "2011-05-20T09:30:00Z",
          "reason": "requested_by_customer" } }
    ]
  }
}
```

### PUT /api/v1_3/orders/{order_id}
Updates editable fields: `buyer_name`, `buyer_email`, `giftee_name`, `giftee_email`, `tag`, `shipping_address1`, `shipping_address2`, `shipping_city`, `shipping_region`, `shipping_postcode`.
```json
{ "order": { "buyer_name": "Lee Sang-hyeok", "buyer_email": "faker@example.org", "tag": "custom-value", "shipping_address1": "10 Example Street" } }
```
Response: **200** on success, **422** on error.

### POST /api/v1/orders/{order_id}/refund
Params: `amount` (required, string e.g. `"14.99"`), `cancel_subscription` (optional bool), `revoke_access` (optional bool). Response **200**, or **422** on invalid amount.

### PUT /api/v1/orders/{order_id}/cancel_subscription
Cancels a subscription order. Response **200**, or **409** if not in a cancellable state.

### POST /api/v1/orders/{order_id}/resend_email
Param: `type` (required) — `"order"`, `"transactions"`, or `"all"`. Response **200**, or **400** for an invalid option.

### PUT /api/v1/orders/{order_id}/download_restrictions
Resets download restrictions based on product/account settings. Response **200**, or **422** if the order is not download-restricted.

### PUT /api/v1/orders/{order_id}/override_country
Param: `country_code` (required). Response **200**, or **422** on error.

### POST /api/v1_3/orders/{order_id}/access
Grants access to a revoked order and linked membership services. Response **200**, or **422** on error.

### DELETE /api/v1_3/orders/{order_id}/access
Revokes order access and linked membership services. Response **200**, or **422** on error.

---

## Subscriptions

### GET /api/v1/subscriptions
Returns all subscriptions.

### GET /api/v1/subscriptions/search?term={term}
Searches subscriptions by name.

### GET /api/v1/subscriptions/{subscription_id}
Returns one subscription.

### POST /api/v1/subscriptions
Creates a subscription. Body includes: `name`, `trial_price`, `trial_frequency`, `trial_no_of_occurrences`, `recurring_price`, `frequency`, `recurring_type`, `access_all_products`.

### PUT /api/v1/subscriptions/{subscription_id}
Updates a subscription. Response **200**, or **422** on error.

### DELETE /api/v1/subscriptions/{subscription_id}
Deletes a subscription. Response **200** on success.

### POST /api/v1/subscriptions/{subscription_id}/issue
Issues an order for the subscription. Required: `order[buyer_email]`, `order[buyer_name]`. Optional: shipping/billing addresses, `buyer_id`, `buyer_status`, `can_market_to_buyer`, `buyer_ip_address`, `dispatched_at`, `tag`, `issued_at`.

---

## Licenses

<!-- Constructed JSON shape from documented field list — verify against live API -->

### GET /api/v1/orders/{order_id}/licenses
All licenses for an order. Fields: `id`, `key`, `order-id`, `order-refunded`, `product-id`.

### GET /api/v1/products/{product_id}/licenses
All licenses for a product (nested path requires product ID).

### POST /api/v1/products/{product_id}/licenses
Creates licenses for a product. Accepts an array of keys (XML or JSON). The response reports any `invalid-keys` (rejected duplicates).
```json
{ "licenses": ["AY3C-7C9E-BC3E-J2MA", "AY3C-7C9E-BC3E-J2MB", "AY3C-7C9E-BC3E-J2MC"] }
```

### GET /api/v1/products/{product_id}/licenses/check_valid?key={key}
Validates whether a key exists for a product; returns matching license data or an empty collection.
```
https://www.sendowl.com/api/v1/products/1/licenses/check_valid?key=AY3C-7C9E-BC3E-J2MA
```
> Security note: "Do not include calls to this API endpoint in your software" — calling it from distributed client code exposes your credentials. Validate server-side.

---

## Other documented resources

The developer navigation also lists **Bundles**, **Drip items**, and **sendowl.js** (a JS embed for buy buttons/cart). Bundles and drip items follow the same CRUD conventions as products/subscriptions; consult the live docs for their exact fields.

---

## Webhooks

Configure at **Settings → Webhooks** (`https://dashboard.sendowl.com/settings/web_hooks`). Add a webhook with: Name (internal), Status (enabled/disabled), URL, Event (dropdown), and optional Conditions (specific product, discount code, or affiliate referral).

### Delivery
- Sent **immediately** when an order changes state.
- Payload is **raw JSON POST** ("order Liquid") — read the **raw request body**, not parsed form params.
- **Retries**: on non-2XX/3XX responses, SendOwl retries the request **10 times with exponential backoff**.

### Headers
- **`X-SENDOWL-HMAC-SHA256`** — signature for origin verification.
- **`X-SENDOWL-EVENT`** — the triggering event in snake_case (e.g. `order_completed`, `subscription_active`, `fraud_review`).
- Note: "When an event triggers a webhook, the payload we send contains the state of the order as it is at that moment. The event trigger is in the header. The order's state (at the time of event) is in the payload."

### HMAC verification
Create a SHA256 HMAC over the **raw request body** using your **API Signing Key Secret** (from the SendOwl API page) as the key, base64-encode, and compare to the header.

```ruby
digest = OpenSSL::Digest::Digest.new('sha256')
calculated_hmac = Base64.encode64(
  OpenSSL::HMAC.digest(digest, YOUR_SIGNING_KEY_SECRET, request.raw_post)
).strip
calculated_hmac == request.headers["HTTP_X_SENDOWL_HMAC_SHA256"]
```
Rails renames the header to `HTTP_X_SENDOWL_HMAC_SHA256`.

### Events (14)
**Order:** Fraud review · Free order issued · In dispute (PayPal) · New payment · Order charged back · Order completed · Order failed · Order imported · Refund issued.
**Subscription:** Subscription active · Subscription cancelled (access revoked immediately) · Subscription cancelling (access continues to period end) · Subscription complete · Subscription setup.

### Payload example
```json
{
  "order": {
    "id": "0000123456",
    "state": "complete",
    "buyer_name": "Mr Buyer",
    "buyer_email": "mrbuyer@gmail.com",
    "buyer_country": "GB",
    "price_at_checkout": "£15.00",
    "cart": {
      "cart_items": [{
        "product": { "id": 2811, "name": "My Product", "product_type": "digital" },
        "quantity": 1,
        "tax_rate": 20.0
      }],
      "completed_checkout_at": "2016-01-05T10:59:24Z"
    },
    "transactions": [{
      "gateway_transaction_id": "ch_fake001",
      "payment_gross": "£18.00",
      "payment_tax": "£3.00"
    }]
  }
}
```

### Deletion
- **User-created**: Webhooks page → select the webhook → Delete.
- **Zapier-created**: delete the corresponding Zap; this removes the SendOwl webhook automatically.

---

## Gaps

- Full Bundles / Drip items / discounts field-level schemas were not captured verbatim — the resources exist and follow REST CRUD conventions; verify fields against the live docs.
- Some money fields are formatted strings with a currency symbol (`"£15.00"`) while others are numeric (`price: 17`) — normalize per endpoint.
- Code samples: `https://github.com/SendOwl`.
