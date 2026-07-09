---
name: sales-bagisto
description: "Bagisto platform help — open-source (MIT) Laravel/PHP eCommerce framework for developers and makers: products, orders, carts, customers, and checkout via a REST API and a GraphQL API (Shop + Admin), plus multi-vendor marketplace, POS, B2B, and multi-channel/headless storefronts, self-hosted or on Bagisto Cloud. Use when building a Bagisto REST or GraphQL integration, authenticating requests (Laravel Sanctum bearer token, X-STOREFRONT-KEY storefront key, or JWT for the headless package), creating a guest cart token, pulling products/orders into a CRM or warehouse, fixing a broken install or slow page loads, fixing broken images after an APP_URL change, choosing self-host vs Bagisto Cloud, or comparing Bagisto to Medusa/Saleor/Shopify. Do NOT use for cross-cart checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Bagisto — e.g. 'pull all orders into my warehouse via the REST API' or 'Sanctum vs storefront-key auth']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/bagisto/bagisto"
---

# Bagisto Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging an API integration, syncing orders/products to a CRM or warehouse, a checkout/conversion question, an install/ops problem, or a platform-selection decision?
- **Surface** — REST API (`/api/shop`, `/api/admin`), GraphQL API (`/api/graphql`), the older headless `bagisto/graphql-api` package (`/graphql`), the admin panel UI, or a marketplace/POS add-on?
- **Auth** — Laravel **Sanctum bearer token**, the **`X-STOREFRONT-KEY`** storefront key, a guest **cart token**, or **JWT** (legacy headless package)?
- **Hosting** — self-hosted (own infra: PHP/Laravel + MySQL/MariaDB + Redis) or **Bagisto Cloud** (managed)?
- **Version** — Bagisto 2.x line (current; v2.4.x as of mid-2026)? API packages need 2.3.0+.

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Digital-product pricing & launch strategy | `/sales-digital-products {question}` |
| Post-purchase email / abandoned-cart sequences | `/sales-email-marketing {question}` |
| Comparing Bagisto against another commerce backend | `/sales-checkout {question}` (platform selection) |

Otherwise it's a Bagisto-specific question — answer it here.

## Step 3 — Bagisto platform reference

**Read `references/platform-guide.md`** for the full reference — modules and what's API vs event vs UI-only, pricing/plan posture, data model with JSON shapes, and quick-start recipes. For raw auth/endpoint/pagination detail, read `references/bagisto-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Pick the right auth for the surface.** The current unified API uses a public **`X-STOREFRONT-KEY`** (`pk_storefront_...`, generated at install or via `php artisan bagisto-api:generate-key`) on every Shop call, plus a **Laravel Sanctum bearer token** (`Authorization: Bearer 1|...`) for customer/admin-scoped routes. Guests get a **cart token** (`POST /api/shop/cart-tokens`). The older standalone `bagisto/graphql-api` (Mobikul) package instead uses **JWT** + an `x-app-secret-key` header — don't mix the two.
- **Two API flavors, same engine.** REST (`/api/shop/...`, `/api/admin/...`) and GraphQL (`/api/graphql`, playground at `/api/graphiql`) both split into a public **Shop API** and a protected **Admin API**. Choose REST for simple CRUD/scripts, GraphQL when a headless storefront wants to request exactly the fields it needs.
- **There are no native outbound webhooks in core.** Bagisto is a Laravel app — to notify a CRM/warehouse on an order, react to the **Laravel event** (e.g. `checkout.order.save.after`) in a listener and `fetch()` out yourself, schedule a polling job against `/api/admin/orders`, or add a community webhook package. Don't expect a Shopify-style "webhooks" settings page.
- **Self-host is free; Cloud is for not running infra.** The engine is **MIT and free** with no per-sale fee. **Bagisto Cloud** (Starter / Pro) sells managed, scalable hosting (uptime SLA, backups, support) so you don't run the LAMP/Redis stack yourself.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify plan gates, fees, auth headers, and API package versions against live docs.*

- **Broken images / mixed-content after setup or a move.** The #1 post-install issue: `APP_URL` in `.env` must exactly match the real site URL (scheme + host). A mismatch breaks asset/image URLs; serving assets over HTTP on an HTTPS site triggers browser mixed-content blocking. Fix `APP_URL`, then `php artisan optimize:clear`.
- **Slow first loads / extreme slowness.** Fresh installs can crawl until caches are built and a queue worker + Redis are configured. Run `php artisan optimize` / route+view+config caching, use Redis for cache & sessions, and run a real queue worker. **Bundle-product price calculation is a known slow path** on category pages — cache aggressively or limit bundles per listing.
- **Install fails at the last step / "Impossible to create the root directory."** Almost always file-permission/ownership or PHP-extension gaps. Ensure `storage/` and `bootstrap/cache/` are writable by the web user and required PHP extensions are present before re-running the installer.
- **Two API generations exist.** The current docs (api-docs.bagisto.com) describe a unified REST+GraphQL with `X-STOREFRONT-KEY` + Sanctum; the older `bagisto/graphql-api` package uses JWT + `x-app-secret-key` and a `/graphql` endpoint. Tutorials mix them — confirm which package is installed before quoting headers/endpoints.
- **API is a separate install.** REST/GraphQL aren't always on by default — `composer require bagisto/rest-api` (or `bagisto/graphql-api`) then run the package's `php artisan ...:install`. The GraphQL package needs middleware tweaks in `bootstrap/app.php`.
- **GraphQL schema must be cached in prod.** Run `php artisan lighthouse:cache` for production and `php artisan lighthouse:clear-cache` after schema changes, or queries get slow / stale.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and platform selection.
- `/sales-medusa` — Another open-source, self-hostable headless commerce engine (Node.js/TypeScript, MIT) — compare if you're choosing a stack; Bagisto is Laravel/PHP.
- `/sales-saleor` — Open-source GraphQL-first headless commerce (Python/Django) with native webhooks — compare against Bagisto's Laravel/event model.
- `/sales-spree` — Open-source (BSD-3) headless commerce on Ruby on Rails with REST APIs and native outbound webhooks — compare if your team is choosing between the Ruby and PHP/Laravel stacks.
- `/sales-shopify` — The leading hosted commerce backend; compare against Bagisto's self-hosted/open-source model.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (Bagisto is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull all orders into a warehouse via the API (developer/automation)
**User**: "I'm writing a script to sync every Bagisto order into BigQuery nightly. What auth do I use and how do I page through them?"
**Approach**: Use the **Admin REST API**. Authenticate with a **Laravel Sanctum bearer token** (`Authorization: Bearer {token}`) obtained from the admin login endpoint, and send `Accept: application/json`. Call `GET /api/admin/orders?page=1&per_page=50` (per-page is capped at 50) and walk pages using the response headers `X-Total-Pages` / `X-Total-Count` / `X-Page`. There's no documented hard rate limit, so still throttle politely and back off on errors. If you're on the GraphQL package instead, query `orders` under the Admin API and page with Relay cursors (`first`/`after` + `pageInfo`).

### Example 2: Notify a CRM when an order is placed (developer/automation)
**User**: "Where do I add a webhook URL in Bagisto so my CRM gets pinged on every new order?"
**Approach**: Explain Bagisto core has **no outbound-webhook settings page**. Because it's a Laravel app, register a **listener** on the `checkout.order.save.after` event (in a service provider's `$listen` map or an `EventServiceProvider`), load the order in the handler, and `fetch()`/`Http::post()` to your CRM — you own retries/signing/logging. Alternatives: a scheduled job that polls `GET /api/admin/orders?per_page=50` for new IDs since the last run, or a community webhook package. Run a real **queue worker** so the outbound call doesn't block checkout.

### Example 3: Self-host vs Bagisto Cloud
**User**: "Should I self-host Bagisto or use Bagisto Cloud? I'm a solo founder launching a small store."
**Approach**: The engine is **MIT/free with no per-sale fee** either way — Cloud just sells managed infra. Self-hosting means you run **PHP/Laravel + MySQL/MariaDB + Redis + a queue worker** on a VPS (Railway/Render/DigitalOcean) and own updates, backups, and scaling. **Bagisto Cloud** (Starter vs Pro tiers — Pro adds a higher uptime SLA and advanced support) removes the ops burden. If they're comfortable with a LAMP+Redis stack and Laravel ops, self-host is cheapest; if not, Cloud is the lower-friction path. Match the choice to their infra appetite, not defaults — and note pricing should be re-verified on the live page.

## Troubleshooting

### "My product images are broken after install (or after moving the site)"
Set `APP_URL` in `.env` to the exact live URL (correct scheme **and** host), then run `php artisan optimize:clear` (or `config:clear` + `cache:clear`). Broken images and HTTPS "mixed content" warnings are almost always an `APP_URL`/scheme mismatch causing assets to load from the wrong origin. Confirm the storage symlink exists (`php artisan storage:link`).

### "Pages take forever to load / the store is extremely slow"
Build caches (`php artisan optimize`, plus route/view/config caching), move cache & sessions to **Redis**, and run a **queue worker** so deferred work isn't done in-request. Category pages with **bundle products** are a known slow path — limit bundles per listing or cache the computed prices. If still slow, profile the DB and add indexes; very large catalogs benefit from the search/indexer being kept warm.

### "I followed a tutorial but the API headers/endpoints don't exist"
You're likely mixing the **two API generations**. The current unified API uses `/api/shop` + `/api/admin` (REST) and `/api/graphql` (GraphQL) with **`X-STOREFRONT-KEY`** + **Sanctum bearer** auth. The older standalone **`bagisto/graphql-api`** (Mobikul) package uses a `/graphql` endpoint with **JWT** and an **`x-app-secret-key`** header. Check which package is in `composer.json` and read that package's docs specifically; install the REST/GraphQL package and run its `php artisan ...:install` if the routes are missing entirely.
