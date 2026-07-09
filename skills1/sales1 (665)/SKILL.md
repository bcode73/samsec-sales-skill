---
name: sales-woocommerce
description: "WooCommerce platform help — the open-source WordPress commerce plugin (woocommerce.com): products, orders, customers, coupons, and the REST API v3 (/wp-json/wc/v3, HTTP Basic consumer key/secret over HTTPS or OAuth 1.0a), signed webhooks (X-WC-Webhook-Signature, HMAC-SHA256 base64), the headless Store API, and batch endpoints. Use when setting up or debugging WooCommerce REST API access, fixing 401 Unauthorized or a stripped Authorization header, wiring orders or customers into a CRM or warehouse, catching an order.created webhook that is not firing, building a headless storefront on the Store API, paginating a large product catalog, or budgeting a store cost beyond the free plugin. Do NOT use for checkout-conversion strategy across cart platforms (use /sales-checkout) or picking a hosted Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in WooCommerce]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, checkout, wordpress, platform]
github: "https://github.com/woocommerce"
---

# WooCommerce Platform Help

WooCommerce (woocommerce.com) is the open-source, **self-hosted** commerce plugin for WordPress —
the most-installed cart on the web. You own the code and the database; there's no platform
transaction fee. It sells physical, digital, variable, and subscription products through Products,
Orders, Customers, and Coupons, and exposes almost everything through a **REST API v3**
(`/wp-json/wc/v3`), **signed webhooks**, and a separate headless **Store API**. Because it runs on
*your* WordPress host, most integration pain is server/auth config, not a vendor limit.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Read/write store data (products, orders, customers) from a script, CRM, or warehouse via the REST API
   - B) Set up or debug a webhook (order/product/customer events)
   - C) Build a headless / custom storefront (Store API cart & checkout)
   - D) Bulk-import or export a large catalog (pagination, batch endpoints)
   - E) Configure the store itself (products, tax, shipping, gateways) in wp-admin
   - F) Understand real cost / plan choices (self-hosted vs Woo Express hosted)
2. **Is the site on HTTPS with pretty permalinks?** Both are effectively required for the REST API
   — 401s and 404s usually trace back to one of them or to a host that strips the `Authorization` header.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/checkout platform to pick, or checkout-conversion strategy (bump/upsell design, cart-abandonment recovery, reducing checkout fields) | `/sales-checkout {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Choosing a hosted Merchant of Record so someone else owns global VAT/GST (WooCommerce is NOT one) | `/sales-merchant-of-record {question}` |
| Comparing WooCommerce against Shopify / BigCommerce / a headless stack for a build decision | `/sales-checkout {question}` |
| Migrating an existing store's data into or out of WooCommerce | `/sales-store-migration {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer WooCommerce-specific questions directly using Step 3.

## Step 3 — WooCommerce platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface
(what's REST-, Store-API-, webhook-accessible vs wp-admin-only), real cost breakdown and plan gates,
data model (string money, integer IDs, `meta_data` arrays), and quick-start recipes (authenticated
REST call, order webhook listener with signature verification, cursor-safe catalog export).

For raw endpoint detail, auth flows, pagination, batch limits, and verbatim webhook headers, read
`references/woocommerce-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Sync to a CRM/warehouse with a webhook plus a reconciliation backstop.** To push store data
  out reliably, register an **`order.created`** (and `order.updated`) webhook to a tokenized HTTPS
  endpoint as the low-latency trigger, **and always add a periodic polling backup** — a nightly
  `per_page=100` paginated `GET /wc/v3/orders?after=<iso8601>` reconciliation pull — because a
  single delivery can be blocked or dropped. Dedupe on the resource `id`. Never rely on the webhook alone.
- **Diagnose a 401 as config, not credentials.** WooCommerce returns 401 when the site isn't on
  HTTPS or when the host **strips the `Authorization` header** (common on Apache/CGI and some
  managed hosts). Tell the user to (a) confirm HTTPS + a valid SSL cert, (b) test with credentials
  as **query-string params** (`?consumer_key=...&consumer_secret=...`) or set `queryStringAuth`, and
  (c) if query-string works but the header doesn't, add the `RewriteRule` that passes
  `Authorization` through (or use OAuth 1.0a for plain HTTP). Confirm the key's permission is
  read/write for the operation.
- **Treat a webhook that "won't fire" as a blocked REST endpoint.** The #1 cause is a security
  plugin or the "restrict REST API to authenticated users" setting rejecting the unauthenticated
  delivery — WooCommerce then logs a failed delivery and **auto-disables the webhook after 5
  consecutive failures**. Re-enable it, allowlist the delivery, and check
  WooCommerce → Status → Logs / the webhook's delivery log. Also verify the topic is `active`, not
  `paused`, and that the endpoint returns a fast `2xx`.
- **Verify every webhook by HMAC, then re-fetch by ID.** Compute
  `base64(HMAC-SHA256(raw_request_body, webhook_secret))` and compare to the
  **`X-WC-Webhook-Signature`** header before trusting a payload; the secret defaults to the API
  user's consumer secret if you didn't set one. Then re-fetch the object via `GET /wc/v3/orders/{id}`
  before provisioning access or moving money, and dedupe on the order/resource ID.
- **Parse money as a string and IDs as integers.** Amounts (`total`, `price`) come back as
  decimal **strings** (`"29.99"`) — don't divide by 100. Resource IDs are integers; dates are ISO8601.
  Custom fields live in the `meta_data` array (`[{ "key": "_pod", "value": "..." }]`), not top-level.
- **Page and batch within the limits.** Default `per_page` is 10, **max 100**; loop with `page=` and
  read `X-WP-Total` / `X-WP-TotalPages` (or the `Link` header) to know when to stop. For bulk writes
  use the `/batch` endpoint (`create`/`update`/`delete` arrays, **~100 items per call**) instead of
  one request per row. There's no vendor rate limit — but your host and DB are the ceiling, so throttle.
- **Reach for the Store API for headless carts, not the v3 API.** Cart/checkout for a custom
  storefront lives at `/wp-json/wc/store/v1` and needs **no consumer key** — it uses a `Nonce` and
  `Cart-Token` header per shopper. Use v3 for admin/back-office data, Store API for the buyer-facing flow.
- **Present cost as best-effort and total, not "free."** The plugin is free (GPL), but a real store
  pays for hosting, extensions (each roughly per-year, per-extension), a theme, and payment
  processing (~2.9%+30¢). Verify current numbers at woocommerce.com/pricing and note Woo Express is
  the hosted option if they don't want to self-manage.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan pricing and the auth/host
behaviors, which vary by server and may have changed.*

- **401 is usually the server, not the key** — no HTTPS, or the host strips the `Authorization`
  header. Try query-string auth; add the `Authorization` rewrite rule; use OAuth 1.0a for HTTP.
- **Webhooks auto-disable after 5 failed deliveries** — a security plugin blocking unauthenticated
  REST access (or a slow/500 endpoint) silently kills them. Re-enable and allowlist the delivery IP/URL.
- **Webhook secret defaults to the consumer secret** if you didn't set one — verify the signature
  with whatever secret is actually stored on the webhook, base64 HMAC-SHA256 of the **raw** body.
- **Money is a decimal string** (`"29.99"`), IDs are integers, dates ISO8601. Custom fields are in `meta_data`.
- **`per_page` max is 100** and total counts are in headers, not the body — large catalogs must paginate.
- **Pretty permalinks required** — `/wp-json/` 404s when WordPress is on "plain" permalinks.
- **It's not a Merchant of Record** — you (the store owner) own sales tax/VAT. WooCommerce Tax /
  extensions can calculate, but you remit.
- **Version skew** — WooCommerce and WordPress version bumps occasionally change field shapes;
  pin to `wc/v3` and re-verify field names against the live `System Status` before a big migration.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy and cart-platform selection (WooCommerce vs Shopify vs BigCommerce; bumps, upsells, cart-abandonment recovery)
- `/sales-digital-products` — Digital-product strategy: pricing, validation, launch
- `/sales-merchant-of-record` — Choosing a Merchant of Record for global tax (WooCommerce is not one)
- `/sales-store-migration` — Migrating a store's catalog, customers, and orders between platforms
- `/sales-shopify` — Shopify platform help (the hosted SaaS alternative)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new orders into a CRM/warehouse (developer/automation)
**User says**: "How do I push every new WooCommerce order into my CRM automatically without missing any?"
**Skill does**: Sets up an `order.created` (and `order.updated`) webhook to a tokenized HTTPS
endpoint, verifies each delivery by recomputing `base64(HMAC-SHA256(body, secret))` against
`X-WC-Webhook-Signature`, then re-fetches `GET /wp-json/wc/v3/orders/{id}` (Basic auth, consumer
key/secret) before writing — parsing `total` as a string and deduping on order `id`. Adds a nightly
`per_page=100` paginated `GET /orders?after=...` reconciliation pull as a backstop in case a
delivery was blocked, and flags that a security plugin can auto-disable the webhook after 5 failures.
**Result**: CRM stays in sync with verified data even if a webhook delivery is dropped or spoofed.

### Example 2: The REST API returns 401 no matter what
**User says**: "I generated a key but every WooCommerce API call comes back 401 Unauthorized."
**Skill does**: Walks the config checklist — HTTPS with a valid cert, key permission is read/write,
then tests credentials as query-string params (`?consumer_key=...&consumer_secret=...`); if that
works but the header doesn't, identifies the host stripping the `Authorization` header and gives the
`.htaccess` rewrite (or switches to OAuth 1.0a for HTTP). Confirms pretty permalinks are on so
`/wp-json/` resolves.
**Result**: Root cause is the server/host config, not the credentials — fixed without regenerating keys.

### Example 3: Bulk-import a large catalog
**User says**: "I need to load 8,000 products into WooCommerce from a CSV — one-by-one is too slow and timing out."
**Skill does**: Points to the `POST /wp-json/wc/v3/products/batch` endpoint with a `create` array of
~100 products per call (not one request each), notes money must be sent as strings and custom fields
go in `meta_data`, and to read `X-WP-Total`/`X-WP-TotalPages` when verifying — throttling because the
ceiling is the user's own host/DB, not a vendor rate limit.
**Result**: Import runs in ~80 batched calls instead of 8,000, without hammering the server.

## Troubleshooting

### 401 Unauthorized on every REST call
**Symptom**: All `/wp-json/wc/v3` requests fail with 401 even with a freshly generated key.
**Cause**: Site not on HTTPS, or the web host strips the `Authorization` header before WordPress
sees it (common on Apache/CGI, some managed hosts), or the key lacks write permission.
**Solution**: Confirm HTTPS + valid SSL and read/write key permission. Test with query-string auth
(`?consumer_key=...&consumer_secret=...`); if that succeeds, add the rewrite rule that passes
`Authorization` through, or use OAuth 1.0a for plain HTTP. Never send keys as query params over plain HTTP.

### Webhook stopped firing
**Symptom**: An `order.created`/`product.updated` webhook worked, then silently stopped.
**Cause**: A security plugin (or "restrict REST API to authenticated users") is returning 401 to the
unauthenticated delivery, or the endpoint returned a non-2xx/slow response — WooCommerce
auto-disables a webhook after **5 consecutive failed deliveries**.
**Solution**: Re-enable the webhook (set status `active`), allowlist the delivery to the REST route,
make the endpoint return a fast `2xx`, and inspect the per-webhook delivery log +
WooCommerce → Status → Logs. Add a polling reconciliation as a safety net.

### `/wp-json/` returns 404
**Symptom**: The REST base itself 404s before auth is even attempted.
**Cause**: WordPress is on "plain" permalinks, so the REST rewrite rules aren't registered (or a
caching/security layer is blocking `/wp-json/`).
**Solution**: Set Settings → Permalinks to a "pretty" structure (e.g. Post name) and re-save to
flush rewrite rules; confirm no server rule or plugin blocks `/wp-json/`.
