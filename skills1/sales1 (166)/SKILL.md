---
name: sales-evershop
description: "EverShop platform help — open-source (GPL-3.0) Node.js/TypeScript/React/GraphQL eCommerce platform on PostgreSQL for developers and makers: products, variants, categories, carts, orders, customers, promotions, and checkout in one self-hosted project (storefront + admin + API together, not headless-only). Use when installing EverShop with create-evershop-app, building a REST or GraphQL integration, authenticating with JWT (admin /api/user/tokens, customer /api/customer/tokens, 15-minute token expiry, Bearer header), creating/updating products via REST while reading via GraphQL, wiring an order event to a CRM or warehouse since there are no native webhooks, fixing a failed npm build or Node-version error, fixing the server going unresponsive, or comparing EverShop to Medusa/Saleor/Vendure/Bagisto/Shopify. Do NOT use for cross-cart checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in EverShop — e.g. 'sync products in via the REST API' or 'notify my CRM on a new order without webhooks']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/evershopcommerce"
---

# EverShop Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — installing/standing up a store, building/debugging an API integration, syncing products/orders to a CRM or warehouse, reacting to an order event, an install/build/ops problem, or a platform-selection decision?
- **Surface** — **REST API** (writes: `/api/products`, `/api/carts/...`, `/api/orders`), **GraphQL** (reads), the **event/subscriber** system (instead of webhooks), the **admin panel** UI, or a custom **extension/theme**?
- **Auth** — admin JWT (`POST /api/user/tokens`), customer JWT (`POST /api/customer/tokens`), or a token-refresh issue (the 15-minute default expiry)?
- **Hosting** — self-hosted (you run **Node 20+ + PostgreSQL 13+**); there is no managed cloud yet.
- **Version** — EverShop 2.x line (v2.1.2 as of mid-2026)? Node < 20 is unsupported.

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Post-purchase / abandoned-cart email sequences | `/sales-email-marketing {question}` |
| Comparing EverShop against another commerce backend | `/sales-checkout {question}` (platform selection) |

Otherwise it's an EverShop-specific question — answer it here.

## Step 3 — EverShop platform reference

**Read `references/platform-guide.md`** for the full reference — modules and what's REST-write vs GraphQL-read vs event-only, pricing/infra posture, data model with JSON shapes, and quick-start recipes. For raw auth/endpoint/event detail, read `references/evershop-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **REST writes, GraphQL reads.** Create/update/delete go through REST (`POST /api/products`, `PATCH /api/products/{uuid}`, `/api/orders`, `/api/carts/...`); **reading** data (list products, fetch an order) is **GraphQL** — there's no broad REST list/get surface. Address mutations by the resource **`uuid`**, not the integer id.
- **Auth is JWT and the admin token expires in 15 minutes.** Get it from `POST /api/user/tokens` → `{accessToken, refreshToken}`, send `Authorization: Bearer <token>`. For long-running jobs, store the refresh token and call `POST /api/user/token/refresh` on 401, or raise `JWT_ADMIN_TOKEN_EXPIRY`. Endpoints are **private by default** (no `access` property = auth required).
- **There are no outbound webhooks.** To notify a CRM/warehouse/Slack on an order, write an **event subscriber** (`subscribers/order_placed/handler.ts`, default-exported async fn) in an extension that `fetch()`es out — subscribers run async in-process, so you own retries/idempotency. Polling orders via GraphQL is the fallback when you can't deploy code.
- **It's self-host, and infra matters.** Node **20+**, PostgreSQL **13+**, run under pm2/systemd with auto-restart; large catalogs want 8 GB+ RAM. Software is free (GPL-3.0), no per-sale fee; it is **not** a Merchant of Record (you own tax).

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify Node/Postgres versions, token-expiry defaults, the event list, and that managed cloud is still unreleased against live docs.*

- **No webhooks — events are in-process only.** There is no UI to register a webhook URL. React to `order_placed`/`product_created`/`inventory_updated`/etc. with a code **subscriber** in an extension that makes the outbound call itself. Don't expect a Shopify-style webhooks page.
- **Reads are GraphQL, not REST.** Integrators expecting `GET /api/products` get surprised — the REST surface is for writes; querying is GraphQL (URQL on the frontend).
- **Admin token expires in 15 minutes.** Scripts that run longer must refresh the token (`/api/user/token/refresh`) or bump `JWT_ADMIN_TOKEN_EXPIRY`, or every call starts 401-ing mid-run.
- **Node < 20 breaks the build.** `npm run build` failures (e.g. missing `@babel/core`, a TailwindLoader "use process(css).then(cb)" async-plugin error) are usually an unsupported Node version or a dirty install — use Node 20+ LTS and reinstall.
- **The server can go unresponsive over time.** Reports of the process stopping responding every few minutes — run it under a process manager (pm2/systemd) with auto-restart, and watch memory on small boxes.
- **`url_key`/`sku` must be a clean slug.** Product-create "must match pattern" errors come from spaces/uppercase/invalid characters — use lowercase hyphenated slugs.
- **Docker quick-start has no admin/data by default.** After `docker compose up`, seed demo data (`npm run seed`) and create an admin (`npm run user:create -- ...`) or admin login won't work.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and platform selection.
- `/sales-medusa` — Another open-source, self-hostable Node/TypeScript commerce engine (MIT) — but headless-only; compare if you want the engine separate from the storefront.
- `/sales-saleor` — Open-source GraphQL-first headless commerce (Python/Django) with **native** outbound webhooks — compare against EverShop's no-webhook, in-process event model.
- `/sales-bagisto` — Open-source Laravel/PHP commerce framework — the PHP-stack alternative to EverShop's Node stack.
- `/sales-shopify` — The leading hosted commerce backend; compare against EverShop's self-hosted/open-source model.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (EverShop is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync a product catalog in via the API (developer/automation)
**User**: "I'm writing a nightly script to push my product catalog into EverShop. Which API do I use and how do I handle auth?"
**Approach**: Use the **REST API** for writes. Get an admin token from `POST /api/user/tokens` (`{email,password}` → `{accessToken, refreshToken}`) and send `Authorization: Bearer <token>`. For each SKU, `POST /api/products` (new) or `PATCH /api/products/{uuid}` (update) — persist the returned **`uuid`** keyed by your SKU so updates address the right record, and keep `url_key`/`sku` as clean lowercase slugs to avoid "must match pattern" errors. Because the admin **access token expires in 15 minutes**, store the refresh token and call `POST /api/user/token/refresh` on a 401, or raise `JWT_ADMIN_TOKEN_EXPIRY` for the job. To *read back* the catalog (verify/export), query **GraphQL**, not REST.

### Example 2: Notify a CRM when an order is placed without webhooks (developer/automation)
**User**: "Where do I add a webhook URL in EverShop so my CRM gets pinged on each new order?"
**Approach**: Explain EverShop has **no outbound-webhook settings page** — it has an in-process event system. Create an extension with `subscribers/order_placed/notifyCRM.ts` exporting a **default async function** that receives the order data and `fetch()`es your CRM endpoint; enable the extension, rebuild, restart. Subscribers run **async in-process**, so the call won't block checkout, but you own retries/idempotency/logging — for reliability, enqueue to Redis/BullMQ and process there. If you can't deploy code into the store, fall back to **polling** orders via GraphQL on a schedule, tracking the last-seen `order_id`.

### Example 3: Choose EverShop vs other open-source commerce engines
**User**: "I'm a solo founder. Should I use EverShop, Medusa, or Bagisto for a small self-hosted store?"
**Approach**: All are free/no-per-sale-fee and self-hosted. **EverShop** ships storefront + admin + API in **one Node/TypeScript project** — fastest to stand up and run if you just want a working store and are fine on Node + Postgres; its trade-offs are thinner docs for multi-currency/large-scale B2B and no deep customization framework. **Medusa** (Node/TS, MIT) is a headless engine — more flexible (Workflows SDK, modules) but you build/deploy the storefront separately. **Bagisto** (Laravel/PHP) fits a PHP team and adds marketplace/POS/B2B extensions. Match to the user's stack and how much they want bundled vs composable; for cross-platform checkout-conversion or MoR-tax decisions, route to `/sales-checkout` or `/sales-merchant-of-record`. Re-verify current versions/pricing before committing.

## Troubleshooting

### "`npm run build` fails (missing @babel/core / TailwindLoader async-plugin error)"
Almost always an **unsupported Node version or a dirty install**. EverShop needs **Node 20.x+** and NPM 9+. Check `node --version`, switch to a Node 20 LTS (e.g. via nvm), delete `node_modules` + lockfile, reinstall, then `npm run build`. The "Use process(css).then(cb) to work with async plugins" TailwindLoader error is the classic symptom of the wrong Node/toolchain.

### "The store stops responding every few minutes"
Run EverShop under a **process manager** (pm2/systemd) with auto-restart so a hung process recovers, and watch memory — small boxes (2 GB) can starve, especially with larger catalogs (8 GB+ RAM recommended at 10k+ products). Reproduce with `npm run start:debug` to capture the error, ensure a single instance owns port 3000, and make sure PostgreSQL is reachable and on SSD.

### "Product create returns 'must match pattern' / my API calls 401 mid-run"
Two common causes. (1) **Validation:** `url_key` and `sku` must be clean slugs — lowercase, hyphenated, no spaces or special characters; fix the value and retry. (2) **Auth expiry:** the admin **access token expires in 15 minutes** by default, so a long batch starts returning 401 — store the `refreshToken` from `POST /api/user/tokens`, call `POST /api/user/token/refresh` on 401 and retry once, or raise `JWT_ADMIN_TOKEN_EXPIRY` for server-to-server jobs. Remember endpoints are private by default, so a missing/expired Bearer token always 401s.
