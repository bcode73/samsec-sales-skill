---
name: sales-bigcommerce
description: "BigCommerce platform help — open SaaS commerce platform for makers and growing DTC/B2B stores: products, orders, customers, carts, checkout, and headless storefronts via REST Management APIs (v3 plus legacy v2 Orders), GraphQL Storefront and Admin APIs, and thin notification-style webhooks. Use when building a BigCommerce REST or webhook integration, a webhook fired but its payload only has a resource id so orders or products aren't syncing, webhooks silently deactivated after repeated failures or inactivity, hitting 429 rate limits (150 req/30s on Standard/Plus, 450 on Pro) and needing backoff, a request 403s from a trailing slash or missing OAuth scope, syncing orders or customers into a CRM or data warehouse, or comparing BigCommerce plans and transaction fees. Do NOT use for checkout-conversion strategy across carts (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in BigCommerce — e.g. 'webhook only sends an id, how do I get the order' or 'sync orders to my CRM']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/bigcommerce"
---

# BigCommerce Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging an API or webhook integration, choosing a plan, a checkout/conversion question, or a store-ops task?
- **Surface** — REST Management API (v3 / legacy v2), GraphQL Storefront API, GraphQL Admin API, webhooks, or the no-code control panel?
- **Account type** — store-level API account (token from control panel), app-level (OAuth, Dev Portal), or account-level (GraphQL Account API across stores)?
- **Plan** — Standard, Plus, Pro, or Enterprise? (Rate limits and a few features scale by tier; some plan names appear as Core/Growth/Scale/Performance on the current pricing page.)

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Digital-product pricing & launch strategy | `/sales-digital-products {question}` |
| Wiring BigCommerce into another tool via iPaaS | `/sales-integration {question}` |
| Post-purchase email / abandoned-cart sequences | `/sales-email-marketing {question}` |

Otherwise it's a BigCommerce-specific question — answer it here.

## Step 3 — BigCommerce platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and what's API vs webhook vs UI-only, pricing/plan gates, data model with JSON shapes, and quick-start recipes. For raw endpoint/auth/rate-limit/webhook detail, read `references/bigcommerce-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Treat webhooks as a doorbell, not a delivery.** Every callback carries only `scope`, `store_id`, and `data.{type,id}` — fetch the real record with a follow-up REST call. Budget for that extra call against your rate limit; consider de-duping on the resource id + `created_at`.
- **Know the version split.** Most resources are v3 (`/v3/catalog/products`, `/v3/customers`, `/v3/carts`, `/v3/hooks`), but the classic **Orders API is v2** (`/v2/orders`). New work should prefer v3 where it exists.
- **Pace requests to the 30-second window.** Standard/Plus get ~150 requests/30s, Pro ~450; read `X-Rate-Limit-Requests-Left` and sleep for `X-Rate-Limit-Time-Reset-Ms` on a 429.
- **Use the minimum OAuth scopes.** A missing scope returns 403, not empty data; and a stray trailing slash on a path also 403s.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify plan gates, fees, rate limits, and API versions against live docs.*

- **Thin webhook payloads.** Callbacks never include the changed object — only the id. You must call the API to get the data, which effectively doubles API usage per event.
- **No webhook delivery logs.** There is no activity dashboard or delivery-history endpoint; if an event goes missing you can't trace it on BigCommerce's side. Log everything you receive and reconcile against the API.
- **Webhooks auto-deactivate.** Repeated 4XX/5XX responses (or long inactivity) deactivate a subscription — respond 2XX fast (do work async) and re-check `is_active`.
- **No HMAC signing.** Unlike Shopify/Stripe, BigCommerce does not sign payloads. Secure the callback with a secret in a custom header you set at creation, and only accept HTTPS on port 443 (custom ports are rejected).
- **403 traps.** A trailing slash on an endpoint, or a missing OAuth scope, both return 403 — not a 404 or empty body.
- **Transaction fees.** $0 on embedded payment providers, but using an "open"/third-party gateway adds a per-GMV fee (e.g. ~2% on entry tier, scaling down by plan).

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery).
- `/sales-shopify` — The other leading hosted commerce backend; compare if you're choosing a platform.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing.
- `/sales-digital-products` — Pricing, packaging, and launch strategy for digital products.
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Webhook only sends an id (developer/automation)
**User**: "My BigCommerce `store/order/created` webhook fires but the payload has no order details — orders aren't syncing to my CRM."
**Approach**: Explain that BigCommerce webhooks are intentionally thin — the payload is just `{scope, store_id, data:{type, id}, hash, created_at, producer}`. In the handler, read `data.id` and make a follow-up `GET /v2/orders/{id}` (Orders is v2) to fetch the full record, then upsert into the CRM. Respond 2XX immediately and do the fetch async so the subscription doesn't deactivate; de-dupe on `data.id` since redelivery is possible.

### Example 2: Bulk-syncing the catalog without 429s (developer/automation)
**User**: "How do I pull every product into my warehouse without getting rate-limited?"
**Approach**: Page `GET /v3/catalog/products?limit=250&page=N` using the `meta.pagination` cursor, and pace to the 30-second quota — on a `429`, sleep for `X-Rate-Limit-Time-Reset-Ms` and resume. Show watching `X-Rate-Limit-Requests-Left`. Standard/Plus ≈150 req/30s, Pro ≈450; for very large/ongoing sync prefer incremental `store/product/updated` webhooks over full re-crawls.

### Example 3: Choosing a plan
**User**: "I'm starting a store and on the entry plan a gateway is charging me extra — is upgrading worth it?"
**Approach**: Explain the $0 fee on embedded payment providers vs the open-gateway per-GMV surcharge that drops by tier, that GMV thresholds auto-upgrade you, and that API rate limits rise with the plan (Standard/Plus ~150 → Pro ~450 req/30s). Map their actual order volume and gateway choice to the breakeven rather than upgrading by default.

## Troubleshooting

### "My webhook fires but I get no order/product data"
By design — payloads carry only the resource id. Fetch the object with a follow-up REST call (`/v2/orders/{id}`, `/v3/catalog/products/{id}`, `/v3/customers?id:in={id}`). Respond 2XX within a few seconds and do the fetch asynchronously, or the subscription will deactivate after repeated slow/failed responses.

### "Getting 429 Too Many Requests"
Rate limits are a quota per 30-second window (≈150 on Standard/Plus, ≈450 on Pro, custom on Enterprise). Read `X-Rate-Limit-Requests-Left` to throttle proactively and, on a 429, sleep for the `X-Rate-Limit-Time-Reset-Ms` value before retrying with incremental backoff. Spread bulk imports across windows.

### "I'm getting a 403 on a request that looks correct"
Two common causes: a trailing slash on the endpoint path (remove it), or an OAuth scope your token wasn't granted (regenerate the store-level API account with the right read/modify scopes). 403 — not 404 — is BigCommerce's signal for both.
