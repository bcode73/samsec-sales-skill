---
name: sales-saleor
description: "Saleor platform help — open-source (BSD-3), GraphQL-first headless commerce platform on Python/Django: products with variants, channels, checkout, orders, and 160+ webhook events; self-hosted (free) or on Saleor Cloud. Use when building a Saleor GraphQL API integration, authenticating with JWT or OIDC and long-lived App tokens (tokenCreate, JWKS, Authorization: Bearer), verifying webhook signatures (JWS RS256 default, HMAC SHA-256 deprecated), modeling the checkoutCreate → orderCreateFromCheckout flow, building a Saleor App with the App SDK, self-hosting the Docker/Postgres/Redis-Celery stack or debugging ALLOWED_HOSTS 'Invalid host header' errors, choosing self-host vs Saleor Cloud (Sandbox/Select/Volume/Enterprise), or comparing Saleor to Medusa/Vendure/commercetools. Do NOT use for cross-cart checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Saleor — e.g. 'verify a webhook signature' or 'self-host vs Saleor Cloud']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/saleor"
---

# Saleor Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging a GraphQL integration, reacting to a commerce event via webhooks, building a Saleor App/dashboard extension, self-hosting, choosing self-host vs Saleor Cloud, or a checkout/conversion question?
- **Surface** — the **GraphQL API** (single `/graphql/` endpoint), **webhooks** (sync + async, 160+ events), the **Apps framework** (App SDK / dashboard extensions), the **Auth SDK** (storefront), the **Configurator CLI**, or the Dashboard UI?
- **Actor** — a **User** (short-lived JWT from `tokenCreate`) or an **App** (long-lived token, machine-to-machine)? Many mutations (e.g. `orderCreateFromCheckout`) require an **app token**, not a user token.
- **Hosting** — **self-hosted** (own infra: Postgres + Redis/Celery + Django) or **Saleor Cloud** (Sandbox / Select / Volume / Enterprise)?

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Comparing Saleor against another commerce backend | `/sales-checkout {question}` (platform selection) |
| Post-purchase email / abandoned-cart sequences | `/sales-email-marketing {question}` |

Otherwise it's a Saleor-specific question — answer it here.

## Step 3 — Saleor platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and what's API vs webhook vs UI-only, pricing/plan gates, the data model with JSON/GraphQL shapes, and quick-start recipes. For raw auth/endpoint/webhook/signature detail, read `references/saleor-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Everything is one GraphQL endpoint.** There is no REST surface — read/write via `https://{your-store}.saleor.cloud/graphql/` (Cloud) or `http://localhost:8000/graphql/` (self-host). Public product reads need no token; mutations need a token. Use the network inspector / API playground in the Dashboard to build queries.
- **Pick the right actor + token.** **Users** authenticate with `tokenCreate(email, password)` and get a short-lived **access token** + a **refresh token** (RS256-signed JWT); refresh with `tokenRefresh`. **Apps** get a **long-lived token** at install/creation for server-to-server work. Send either as `Authorization: Bearer <token>` (or `Authorization: JWT <token>`). Verify tokens against the **JWKS** at `/.well-known/jwks.json` or via `tokenVerify`.
- **Checkout is a multi-step mutation flow, keyed by variant.** `checkoutCreate` takes **variant IDs** (not product IDs — variants carry inventory + price) and a `channel`; then `checkoutEmailUpdate`, `checkoutShippingAddressUpdate`/`checkoutBillingAddressUpdate`, `checkoutDeliveryMethodUpdate`, a payment/transaction step, and finally **`orderCreateFromCheckout`** (requires an **app token**) → `orderMarkAsPaid`.
- **Saleor HAS native outbound webhooks** (unlike Medusa). Register them on an **App**, choose **sync** (blocks the request — taxes, shipping, payment) or **async** (fires after, e.g. `ORDER_CREATED`), and shape the payload with a **GraphQL `subscription`**. Verify the **`Saleor-Signature`**: default is **JWS RS256 (detached payload)** verified via JWKS; **HMAC SHA-256 is deprecated** and only used when a `secretKey` was set. Always verify against the **raw request body**, never a re-serialized object.
- **Self-host is free; Cloud is for not running infra.** Saleor Core is **BSD-3 / open-source** with **no per-sale fee** when self-hosted. The **`saleor-platform`** repo is **dev-only** — production needs Postgres, Redis (Celery worker + beat), the Core Dockerfile (which is production-ready), and real `ALLOWED_HOSTS`/secrets. **Saleor Cloud** sells managed infra: **Sandbox is free but non-commercial**; commercial Cloud starts at **Select ~$1,599/mo**.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify plan gates, fees, auth, webhook-signature behavior, and API shapes against live docs.*

- **HMAC webhook signatures are deprecated.** New webhooks default to **JWS RS256 with a detached payload** (verify with the public key from `/.well-known/jwks.json`). Only webhooks that had a `secretKey` set use **HMAC SHA-256** — and that path is deprecated. Code that assumes a simple HMAC header will silently fail to verify JWS-signed events.
- **Verify the raw body, not a parsed object.** Both JWS and HMAC verification require the **exact raw request bytes**. In Next.js you must disable `bodyParser`; re-serializing JSON breaks the signature.
- **`orderCreateFromCheckout` needs an app token, not a user token.** Converting a checkout to an order is an app-permissioned mutation — a customer/user JWT will hit an `AUTHENTICATED_APP`/permission error.
- **`saleor-platform` is not production.** That docker-compose repo is for local development only; deploying it as-is is a common mistake. Use the Core Dockerfile and provision Postgres/Redis/Celery yourself (or use Saleor Cloud).
- **"Invalid host header" / blank storefront** usually means **`ALLOWED_HOSTS`** isn't set correctly for your domain (Django setting) — set it via env, not only in the Dockerfile.
- **Sandbox is non-commercial.** The free Cloud tier is for prototyping; you cannot run a real store on it. Commercial Cloud starts at Select (~$1,599/mo) — for low budgets, self-host instead.
- **Sync webhooks are on the critical path.** A slow/failing **synchronous** webhook (tax, shipping, payment) delays or breaks the originating request — there's a **~20s total round-trip cap** (2s connect + 18s response). Keep sync handlers fast; use async for side-effects.
- **Not a Merchant of Record.** Saleor doesn't remit your sales tax/VAT — you own compliance (wire a tax app like Avalara/TaxJar via the tax webhooks, or use a MoR upstream). See `/sales-merchant-of-record`.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and platform selection.
- `/sales-medusa` — The other dev-favorite open-source headless engine (Node.js/REST); compare if you're choosing between self-hostable backends. Medusa has no native outbound webhooks; Saleor does.
- `/sales-spree` — Open-source (BSD-3) headless engine on Ruby on Rails with REST APIs and native outbound webhooks; compare by stack (Ruby vs Python) and API style (REST vs Saleor's GraphQL).
- `/sales-shopify` — The leading hosted commerce backend; compare against Saleor's open-source/self-hosted model.
- `/sales-bigcommerce` — API-first open-SaaS backend; another platform-selection comparison point.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (Saleor is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Verify a Saleor webhook signature (developer/automation)
**User**: "My Saleor `ORDER_CREATED` webhook handler keeps rejecting the signature even though the secret matches. What am I doing wrong?"
**Approach**: Check whether the webhook actually uses HMAC at all — Saleor **defaults to JWS RS256 (detached payload)** and only uses **HMAC SHA-256 when a `secretKey` was set** (and that path is deprecated). If no secret is configured, you must verify the `Saleor-Signature` as a **JWS**: fetch the public key from `https://<domain>/.well-known/jwks.json`, then verify with `jose.flattenedVerify()` using the **raw request body** as the detached payload. The most common bug is verifying against parsed/re-serialized JSON instead of the raw bytes — in Next.js, disable `bodyParser` so you can read the raw string. For Saleor Apps, prefer `withWebhookSignatureVerified()` from `@saleor/app-sdk`, which handles both paths.

### Example 2: Pull all orders into a warehouse via the GraphQL API (developer/automation)
**User**: "I'm writing a script to export every Saleor order into BigQuery. What auth do I use and how do I paginate?"
**Approach**: Use an **App token** (long-lived, machine-to-machine) sent as `Authorization: Bearer <app-token>` to the single `/graphql/` endpoint — create the app and grant `MANAGE_ORDERS`. Query `orders(first: 100, after: $cursor)` and page with **Relay-style cursor pagination**: read `pageInfo { hasNextPage endCursor }` and pass `endCursor` as `after` until `hasNextPage` is false. Select only the fields you need (orders are deep objects). Note many list queries are **channel-scoped**, so filter by `channel` where relevant, and throttle politely (Cloud applies request limits).

### Example 3: Self-host vs Saleor Cloud
**User**: "I'm a solo founder. Should I self-host Saleor or pay for Saleor Cloud?"
**Approach**: Saleor Core is **BSD-3/free with no per-sale fee** if you self-host — but it's a real Django app needing **Postgres + Redis (Celery worker + beat)** and ops (upgrades, scaling, backups). The **`saleor-platform` repo is dev-only**; production means the Core Dockerfile + provisioned infra (Railway/Render/Fly/K8s). Saleor **Cloud Sandbox is free but non-commercial**, and commercial Cloud starts at **Select (~$1,599/mo, up to $200k GMV)** — steep for a solo founder. Recommendation: if they're comfortable running Django/Postgres/Redis, **self-host** (cheapest, full control); if their budget is tiny and they want zero ops but Cloud is too pricey, point them to a simpler hosted backend or a drop-in cart instead, and reserve Saleor Cloud for once GMV justifies it.

## Troubleshooting

### "My webhook signature won't verify"
Confirm the signature scheme first. Saleor's `Saleor-Signature` is a **JWS (RS256, detached payload)** by default — verify it with the public key from `/.well-known/jwks.json` against the **raw body**. **HMAC SHA-256** is only used (and is deprecated) when the webhook had a `secretKey`; verify that with `echo -n "<raw-body>" | openssl dgst -sha256 -hmac "<secret>"`. The usual failure is verifying parsed JSON instead of the raw request bytes (disable `bodyParser` in Next.js), or assuming HMAC when the webhook is actually JWS-signed.

### "I get AUTHENTICATED_APP or a permission error on a mutation"
The mutation requires an **App token** with the right permission, not a user token — e.g. `orderCreateFromCheckout`, order/fulfillment, and most management mutations are app-permissioned. Create an App, grant it the needed permission (`MANAGE_ORDERS`, `MANAGE_PRODUCTS`, …), and send its long-lived token as `Authorization: Bearer`. Also confirm the token isn't expired (refresh user tokens with `tokenRefresh`).

### "My storefront returns 'Invalid host header' or a blank page after deploy"
That's Django's `ALLOWED_HOSTS` rejecting the request host. Set `ALLOWED_HOSTS` to include your real domain via environment/runtime config (setting it only in the Dockerfile often doesn't take effect). Also remember the **`saleor-platform`** compose repo is **development-only** — don't deploy it to production; use the Core Dockerfile with proper env, Postgres, and Redis/Celery.
