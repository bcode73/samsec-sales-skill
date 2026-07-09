<!-- Source: https://gumroad.com/api (official API reference, antiwork Mintlify docs) -->
<!-- Verified against: https://github.com/antiwork/gumroad/blob/main/config/routes.rb (v2 namespace) + app/controllers/api/v2/ controllers -->
<!-- Re-verified 2026-06-13. Supplemented by: https://rollout.com/integration-guides/gumroad/api-essentials -->

# Gumroad API v2 Reference

## General

- **Base URL:** `https://api.gumroad.com/v2/`
- **Protocol:** REST, all responses are JSON
- **Authentication:** OAuth 2.0 via Doorkeeper. Pass `access_token` as a parameter or in the Authorization header.
- **Rate Limiting:** HTTP 429 "Too Many Requests" (no published numeric limits)
- **Pagination:** Cursor-based via `page_key` parameter (Base64-encoded); responses include `next_page_url` when more results exist
- **Error format:** `{ "success": false, "message": "..." }`
- **Soft deletes:** Most DELETE operations set a `deleted_at` timestamp rather than hard-deleting

## OAuth Scopes

| Scope | Used By |
|---|---|
| `view_public` | Products, Offer Codes, Custom Fields, Variant Categories, Variants, SKUs, Categories, User |
| `view_sales` | Sales, Subscribers, Resource Subscriptions |
| `view_payouts` | Payouts (add `view_sales` to include per-sale detail) |
| `edit_products` | Product CRUD, Offer Codes, Custom Fields, Variants, Covers, Thumbnail, Files, Bundle Contents, Licenses, Refund Policy |
| `edit_sales` | Resend Receipt, Refund |
| `refund_sales` | Refund |
| `mark_sales_as_shipped` | Mark as Shipped |

---

## 1. Products

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products` | `view_public` | List all products (paginated via `page_key`) |
| POST | `/products` | `edit_products` | Create a product |
| GET | `/products/:id` | `view_public` | Get a single product |
| PUT | `/products/:id` | `edit_products` | Update a product |
| DELETE | `/products/:id` | `edit_products` | Delete a product (soft delete) |
| PUT | `/products/:id/enable` | `edit_products` | Publish a product (member action, **PUT** not POST) |
| PUT | `/products/:id/disable` | `edit_products` | Unpublish a product (member action, **PUT** not POST) |

**Create/Update parameters:**
- `name` (string, required on create)
- `description` (HTML string)
- `native_type` (string, default "digital")
- `price` (integer, cents)
- `price_currency_type` (currency code)
- `custom_permalink` (string)
- `customizable_price` (boolean — enables pay-what-you-want)
- `suggested_price_cents` (integer)
- `max_purchase_count` (integer)
- `quantity_enabled` (boolean)
- `is_adult` (boolean)
- `display_product_reviews` (boolean)
- `should_show_sales_count` (boolean)
- `taxonomy_id` (integer)
- `custom_receipt` (string)
- `custom_summary` (string)
- `tags` (array of strings)
- `subscription_duration` (membership type only)
- `files` (array: `{ url, id, display_name, extension, position, stream_only, description }`)
- `rich_content` (array of page objects: `{ id, title, description }`)
- `has_same_rich_content_for_all_variants` (boolean, update only)
- `cover_ids` (array, update only — reorder covers)

**Response:** `{ "success": true, "product": { ... } }`

---

## 2. Sales

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/sales` | `view_sales` | List sales (paginated) |
| GET | `/sales/summary` | `view_sales` | Aggregated sales summary |
| POST | `/sales/exports` | `view_sales` | Trigger a sales CSV export |
| GET | `/sales/:id` | `view_sales` | Get a single sale |
| PUT | `/sales/:id/mark_as_shipped` | `mark_sales_as_shipped` | Mark sale as shipped (member action, **PUT** not POST) |
| PUT | `/sales/:id/refund` | `refund_sales` or `edit_sales` | Refund a sale (member action, **PUT** not POST) |
| POST | `/sales/:id/resend_receipt` | `edit_sales` | Resend purchase receipt |

**List parameters:**
- `before` (string, "YYYY-MM-DD")
- `after` (string, "YYYY-MM-DD")
- `email` (string)
- `product_id` (string)
- `order_id` (string)
- `page_key` (string, cursor pagination)
- `page` (integer, **deprecated** offset pagination — prefer `page_key`)

**Mark as Shipped parameters:**
- `tracking_url` (string, optional)

**Refund parameters:**
- `amount_cents` (integer, optional — for partial refund)

---

## 3. Subscribers

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products/:product_id/subscribers` | `view_sales` | List subscribers for a product |
| GET | `/subscribers/:id` | `view_sales` | Get a single subscriber |

**List parameters:**
- `email` (string, filter by purchase email)
- `page_key` (string, cursor)
- `paginated` ("1" or "true" to enable pagination)

---

## 4. Licenses

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| POST | `/licenses/verify` | *public (no auth required)* | Verify a license key |
| PUT | `/licenses/enable` | `edit_products` | Enable a license |
| PUT | `/licenses/disable` | `edit_products` | Disable a license |
| PUT | `/licenses/rotate` | `edit_products` | Rotate (regenerate) a license key |
| PUT | `/licenses/decrement_uses_count` | `edit_products` | Decrement license uses count |

**Parameters (all endpoints):**
- `license_key` (string, required)
- `product_id` or `product_permalink` (required for enable/disable/rotate/decrement)

**Verify additional parameters:**
- `increment_uses_count` (boolean, **default true** — the counter increments unless you explicitly pass `false`; verified in `licenses_controller.rb`, which treats any value other than `"false"`/`false` as true)

**Verify response includes:** `success`, `uses`, `purchase` object (id, created_at, variants, custom_fields, offer_code, refunded, chargebacked, subscription status fields `subscription_ended_at`/`subscription_cancelled_at`/`subscription_failed_at`, test)

**Important:** Products created on or after a server-side cutoff (Jan 9, 2023) require `product_id` — verifying such a product with only `product_permalink` returns **HTTP 500** with a message telling you to set `product_id`. Older products still accept `product_permalink`.

---

## 5. Offer Codes

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products/:product_id/offer_codes` | `view_public` | List offer codes (includes universal codes) |
| GET | `/products/:product_id/offer_codes/:id` | `view_public` | Get a single offer code |
| POST | `/products/:product_id/offer_codes` | `edit_products` | Create an offer code |
| PUT | `/products/:product_id/offer_codes/:id` | `edit_products` | Update an offer code |
| DELETE | `/products/:product_id/offer_codes/:id` | `edit_products` | Delete an offer code (soft delete) |

**Create parameters:**
- `name` (string, required — the code itself)
- `offer_type` ("percent" or fixed amount)
- `amount_off` or `amount_cents` (one required)
- `universal` ("true" for all products)
- `max_purchase_count` (integer)

**Update parameters:**
- `max_purchase_count` (integer)

---

## 6. Custom Fields

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products/:product_id/custom_fields` | `view_public` | List custom fields |
| POST | `/products/:product_id/custom_fields` | `edit_products` | Create a custom field |
| PUT | `/products/:product_id/custom_fields/:id` | `edit_products` | Update a custom field |
| DELETE | `/products/:product_id/custom_fields/:id` | `edit_products` | Delete a custom field |

**Create parameters:**
- `name` (string, optional if `url` or `label` provided)
- `url` (string, optional)
- `label` (string, optional)
- `required` (boolean, default false)
- `type` (string, default "text")

---

## 7. Variant Categories

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products/:product_id/variant_categories` | `view_public` | List variant categories |
| POST | `/products/:product_id/variant_categories` | `edit_products` | Create a variant category |
| GET | `/products/:product_id/variant_categories/:id` | `view_public` | Get a single variant category |
| PUT | `/products/:product_id/variant_categories/:id` | `edit_products` | Update a variant category |
| DELETE | `/products/:product_id/variant_categories/:id` | `edit_products` | Delete (soft delete) |

**Create/Update parameters:**
- `title` (string)

---

## 8. Variants

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products/:pid/variant_categories/:vc_id/variants` | `view_public` | List variants |
| POST | `/products/:pid/variant_categories/:vc_id/variants` | `edit_products` | Create a variant |
| GET | `/products/:pid/variant_categories/:vc_id/variants/:id` | `view_public` | Get a single variant |
| PUT | `/products/:pid/variant_categories/:vc_id/variants/:id` | `edit_products` | Update a variant |
| DELETE | `/products/:pid/variant_categories/:vc_id/variants/:id` | `edit_products` | Delete (soft delete) |

**Create/Update parameters:**
- `name` (string)
- `price_difference_cents` (integer)
- `description` (string)
- `max_purchase_count` (integer)
- `rich_content` (JSON array, update only)

---

## 9. SKUs

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/products/:product_id/skus` | `view_public` | List SKUs for a product |

---

## 10. User & Categories

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/user` | `view_public` | Get authenticated user info |
| GET | `/categories` | `view_public` | List Discover taxonomy categories |

---

## 11. Resource Subscriptions (Webhooks via API)

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/resource_subscriptions` | `view_sales` | List resource subscriptions |
| PUT | `/resource_subscriptions` | `view_sales` | Create a resource subscription (**PUT** not POST) |
| DELETE | `/resource_subscriptions/:id` | `view_sales` | Delete a resource subscription |

**List parameters:**
- `resource_name` (string, required)

**Create parameters:**
- `resource_name` (string, required)
- `post_url` (string, required — URL to receive POSTs; must be a public HTTP/HTTPS URL, **not** localhost/127.0.0.1/0.0.0.0)

**Supported resource names:**
1. `sale`
2. `refund`
3. `dispute`
4. `dispute_won`
5. `cancellation`
6. `subscription_updated`
7. `subscription_ended`
8. `subscription_restarted`

---

## 12. Covers (Product Images)

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| POST | `/products/:product_id/covers` | `edit_products` | Upload a cover image |
| DELETE | `/products/:product_id/covers/:id` | `edit_products` | Delete a cover image |
| POST | `/products/:product_id/thumbnail` | `edit_products` | Create/replace the product thumbnail |
| DELETE | `/products/:product_id/thumbnail` | `edit_products` | Delete the product thumbnail |

**Create parameters (one required):**
- `signed_blob_id` (string — pre-signed blob)
- `url` (string — direct URL)

---

## 13. Files (Direct Upload)

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| POST | `/files/presign` | `edit_products` | Get presigned S3 upload URLs |
| POST | `/files/complete` | `edit_products` | Complete multipart upload |
| POST | `/files/abort` | `edit_products` | Abort an in-progress multipart upload |
| POST | `/direct_uploads` | `edit_products` | Create a direct (single-shot) upload |

(Note: file routes live at the v2 root — `/v2/files/presign`, `/v2/files/complete`, `/v2/files/abort`, `/v2/direct_uploads` — not nested under a product.)

**Presign parameters:**
- `filename` (string, required)
- `file_size` (integer, required, max 20 GB)

**Presign response:** `{ upload_id, key, file_url, parts: [{ part_number, presigned_url }] }`

**Complete parameters:**
- `upload_id` (string, required)
- `key` (string, required)
- `parts` (array: `[{ part_number, etag }]`)

---

## 14. Bundle Contents

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| PUT | `/products/:product_id/bundle_contents` | `edit_products` | Update bundle product contents |

**Parameters:**
- `products` (array, required): `[{ product_id, variant_id, quantity (default 1), position }]`

---

## 15. Payouts

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/payouts` | `view_payouts` | List completed payouts (paginated; up to ~10 per page) |
| GET | `/payouts/:id` | `view_payouts` | Get a single payout |
| GET | `/payouts/upcoming` | `view_payouts` | List upcoming (unprocessed) payouts |

**List parameters:**
- `after` / `before` (string, "YYYY-MM-DD")
- `page_key` (string, cursor pagination)
- `include_upcoming` (boolean — include upcoming payouts in the list)

**Get / upcoming parameters:**
- `include_sales` (boolean — embed associated sales; also requires `view_sales`)
- `include_transactions` (boolean — embed transaction lines)

**Payout object fields:** `id`, `amount`, `currency`, `status`, `created_at`, `processed_at`, `payment_processor`, `bank_account_visual`, `paypal_email`, plus optional `sales`, `refunded_sales`, `disputed_sales`, `transactions`.

**Status values:** `creating`, `processing`, `unclaimed`, `completed`, `failed`, `cancelled`, `reversed`, `returned`.

---

## 16. Refund Policy (account-wide)

Per-product refund policies were sunset; refund policy is now account-wide.

| Method | Endpoint | Scope | Description |
|---|---|---|---|
| GET | `/refund_policy` | `view_public` | Read the account refund policy |
| PUT | `/refund_policy` | `edit_products` | Update the account refund policy |

---

## 17. Ping / Webhooks (Dashboard-configured)

Configure at **Settings → Advanced → Ping endpoint**. Gumroad POSTs to your URL on events. Retries up to 3 times over 15–20 minutes if no response.

**Verification header:** `x-gumroad-signature` (HMAC-SHA256)

**Content-Type:** `application/x-www-form-urlencoded` (NOT JSON)

**Webhook POST payload fields:**

| Field | Type | Notes |
|---|---|---|
| `seller_id` | string | Seller's unique ID |
| `product_id` | string | Product unique ID |
| `product_name` | string | Product name |
| `permalink` | string | Product permalink |
| `product_permalink` | string | Original perma ID (never custom) |
| `email` | string | Buyer email |
| `full_name` | string | Buyer name (if present) |
| `price` | integer | Price paid in USD cents |
| `currency` | string | Currency code |
| `quantity` | integer | Quantity purchased |
| `order_number` | string | Order number |
| `sale_id` | string | Sale unique ID |
| `sale_timestamp` | string | ISO timestamp |
| `subscription_id` | string | Subscription ID (if recurring) |
| `variants` | object/array | Variant selections (if present) |
| `offer_code` | string | Discount code used (if any) |
| `license_key` | string | License key (if product has licensing) |
| `ip_country` | string | Buyer's country from IP |
| `recurrence` | string | Billing recurrence (monthly, yearly, etc.) |
| `is_gift_receiver_purchase` | boolean | Whether this is a gift redemption |
| `is_recurring_charge` | boolean | Whether this is a recurring charge |
| `is_preorder_authorization` | boolean | Whether this is a preorder auth |
| `refunded` | boolean | Whether the sale has been refunded |
| `resource_name` | string | Event type (sale, refund, dispute, etc.) |
| `disputed` | boolean | Whether sale is disputed |
| `dispute_won` | boolean | Whether dispute was won |
| `custom_fields` | object | Dictionary of custom field responses |
| `shipping_information` | object | Shipping details (if physical) |
| `url_params` | object | URL params passed during checkout |
| `test` | boolean | Whether this is a test ping |
