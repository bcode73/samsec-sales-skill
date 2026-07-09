# Bagisto — Learnings

Accumulated, dated knowledge from research and real usage. Append new findings with the date.

**2026-06-29**: Research baseline. Bagisto is a free, open-source (MIT) Laravel/PHP + Vue.js eCommerce framework by Webkul — a self-hosted/headless commerce backend, not a hosted SaaS or drop-in cart. Actively maintained (v2.4.7 released 2026-06-24; 27.5k+ GitHub stars, 90 releases). Maps to `/sales-checkout` strategy skill (same family as Medusa/Saleor/Shopify).

**2026-06-29**: API has **two generations**. (1) Current unified REST+GraphQL (api-docs.bagisto.com): Shop/Admin split, `X-STOREFRONT-KEY` (`pk_storefront_...`, `php artisan bagisto-api:generate-key`) + Laravel **Sanctum** bearer auth, guest **cart tokens** (`POST /api/shop/cart-tokens`), REST base `/api/shop` + `/api/admin`, GraphQL at `/api/graphql` + playground `/api/graphiql`, REST pagination via `?page=&per_page=` (max 50) with `X-Total-*` headers, GraphQL cursor pagination. (2) Legacy standalone `bagisto/graphql-api` (Mobikul): `/graphql` endpoint, **JWT** + `x-app-secret-key` header, configured via `JWT_TTL`/`MOBIKUL_API_KEY`, built on Laravel Lighthouse. Don't mix headers between the two.

**2026-06-29**: **No native outbound webhooks in core.** Integrate via Laravel events/listeners (e.g. `checkout.order.save.after`), polling `/api/admin/orders`, or a community webhook package. You own retries/signing/logging.

**2026-06-29**: Top real-user pain points (from GitHub issues): (a) **broken images / mixed-content** → `APP_URL` mismatch in `.env`; fix + `php artisan optimize:clear`. (b) **extreme slowness** (fresh installs, 10–25 min loads reported) → build caches (`php artisan optimize`), use Redis, run a queue worker; **bundle-product price calculation** is a known slow path on category pages. (c) **install fails at last step / "Impossible to create the root directory"** → file permissions on `storage/` + `bootstrap/cache/` and PHP extensions. (d) update/upgrade errors that auto-rollback.

**2026-06-29**: Pricing — engine free (MIT). Bagisto Cloud has **Starter Pack** + **Pro Pack** (Pro ≈99.9% uptime SLA vs Starter ≈99.5%; migration/tech assistance are paid add-ons); **public monthly prices not listed — contact sales / verify live**. Multi-Vendor Marketplace, POS, B2B, mobile apps are **paid Webkul extensions**.

**2026-06-29**: Ecosystem (Webkul): Krayin CRM (Laravel CRM), UnoPim (PIM), Aureus ERP, QloApps (hospitality). Krayin CRM queued to backlog for `/sales-crm-selection`. Adjacent open-source commerce engines queued: Sylius (Symfony/PHP), Evershop (Node.js). Vendure/Magento/WooCommerce already in backlog; Medusa/Saleor already have skills.
