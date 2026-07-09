---
name: sales-shopify
description: "Shopify platform help — the leading commerce platform for makers and DTC sellers: products, orders, customers, checkout, discounts, and headless storefronts via the GraphQL Admin API (REST is now legacy) plus HMAC-signed webhooks and the Storefront API. Use when building a Shopify Admin API or webhook integration, webhook HMAC verification failing the mandatory GDPR/compliance automated checks, hitting GraphQL query-cost throttling or a 429/THROTTLED and needing backoff or bulk operations, migrating an integration off the legacy REST Admin API to GraphQL, checkout customization gated to Shopify Plus (checkout.liquid deprecated for Checkout Extensibility), third-party payment-provider transaction fees eating margin, syncing orders or customers into a CRM or data warehouse, or choosing between Basic, Grow, Advanced, and Plus. Do NOT use for checkout-conversion strategy across carts (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Shopify — e.g. 'verify a webhook HMAC' or 'sync orders to my CRM']"
license: MIT
version: 1.0.1
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/Shopify"
---

# Shopify Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging an API or webhook integration, choosing a plan, a checkout/conversion question, or a store-ops task?
- **Surface** — GraphQL Admin API, REST Admin API (legacy), Storefront API, webhooks, or the no-code admin?
- **App type** — custom app (token from admin) or public app (OAuth, Dev Dashboard)?
- **Plan** — Basic, Grow, Advanced, or Plus? (Some features — Checkout Extensibility, higher API limits, B2B — are Plus-gated.)

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really about a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Digital-product pricing & launch strategy | `/sales-digital-products {question}` |
| Wiring Shopify into another tool via iPaaS | `/sales-integration {question}` |
| Post-purchase email / abandoned-cart sequences | `/sales-email-marketing {question}` |

Otherwise it's a Shopify-specific question — answer it here.

## Step 3 — Shopify platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and what's API vs webhook vs UI-only, pricing/plan gates, data model with JSON shapes, and quick-start recipes. For raw endpoint/auth/rate-limit/webhook detail, read `references/shopify-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Build on GraphQL.** REST Admin API is legacy as of 2024-10-01; new public apps must be GraphQL-only since 2025-04-01, and new features ship GraphQL-first. Don't start a new integration on REST.
- **Verify every webhook.** Compute HMAC-SHA256 over the *raw* request body with your app's API secret, base64-encode, and timing-safe-compare to `X-Shopify-Hmac-Sha256`. The three mandatory GDPR/compliance webhooks must pass this or app review fails.
- **Treat webhooks as hints, not source of truth.** Delivery isn't guaranteed and ordering isn't either — reconcile against the API and order by `updated_at` / `X-Shopify-Triggered-At`.
- **Budget GraphQL cost, not request count.** Watch `extensions.cost.throttleStatus`; back off on `THROTTLED`; use bulk operations for large exports.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify plan gates, fees, and the current API version against live docs.*

- **REST is legacy.** As of 2026 the latest version is `2026-04`; REST endpoints still work but are frozen. GraphQL only for anything new.
- **HMAC trap:** must hash the *raw, unparsed* body. Frameworks that JSON-parse the body before you reach it (Express `body-parser`, etc.) silently break verification — capture the raw buffer first.
- **Throttling is cost-based on GraphQL.** A query can request up to 1,000 points; mutations cost 10 each; connections scale with `first`/`last`. A 100-point/sec bucket (Basic) refills 50/sec at the standard rate.
- **Checkout is locked down.** `checkout.liquid` customization and `additional scripts` are deprecated — checkout UI changes now go through Checkout Extensibility, and fully customizable checkout is effectively Plus-tier.
- **Transaction fees** apply on top of card rates when you use a third-party payment gateway instead of Shopify Payments (e.g. ~2% on Basic) — they vanish with Shopify Payments.
- **API access scopes** must be requested at install; a missing scope returns an access-denied error, not empty data.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery).
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing.
- `/sales-digital-products` — Pricing, packaging, and launch strategy for digital products.
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Verifying a webhook signature (developer/automation)
**User**: "My Shopify webhook HMAC check keeps failing — Shopify's automated GDPR checks won't pass."
**Approach**: Confirm they're hashing the *raw* request body (not a re-serialized JSON object) with the app's API secret, HMAC-SHA256, base64-encoded, compared timing-safely to `X-Shopify-Hmac-Sha256`. Point them at the verify snippet in `references/shopify-api-reference.md`, and remind them the three mandatory compliance topics (`customers/data_request`, `customers/redact`, `shop/redact`) must each return 200 with a valid HMAC.

### Example 2: Syncing orders into a warehouse (developer/automation)
**User**: "How do I pull every order into BigQuery without getting rate-limited?"
**Approach**: Use a `orders/create` + `orders/updated` webhook for incremental sync, and a GraphQL **bulk operation** for the historical backfill (no per-query cost limit). Show the bulkOperationRunQuery pattern from the guide, and reconcile with `updated_at` since webhook delivery isn't guaranteed.

### Example 3: Picking a plan
**User**: "I'm on Basic and a third-party gateway is charging me extra — is Advanced or Plus worth it?"
**Approach**: Explain the third-party transaction fee drops by tier (and disappears with Shopify Payments), Advanced raises staff seats and lowers card rates, and Plus unlocks fully customizable checkout + ~500% higher API limits + B2B. Map their actual order volume and gateway choice to the breakeven.

## Troubleshooting

### "Webhook HMAC verification fails / compliance checks won't pass"
The #1 cause is hashing a parsed/re-serialized body. Read the raw bytes before any JSON middleware, HMAC-SHA256 with the API secret, base64-encode, timing-safe compare to `X-Shopify-Hmac-Sha256`. Ensure the three mandatory GDPR topics are subscribed and each responds 200.

### "Getting 429 / THROTTLED errors"
GraphQL throttles by **calculated query cost**, not request count. Inspect `extensions.cost.throttleStatus.currentlyAvailable`, request fewer fields, and implement exponential backoff with jitter. For large reads switch to bulk operations, which bypass the per-query cost cap. REST uses a leaky bucket (~2 req/sec, 40 burst) — read `Retry-After`.

### "My REST integration broke / a feature is GraphQL-only"
REST Admin API is legacy since 2024-10-01 and newer features are GraphQL-exclusive. Migrate the affected calls to GraphQL (see Shopify's REST→GraphQL migration mapping); pin a recent version like `2026-04` and budget for the quarterly version cadence.
