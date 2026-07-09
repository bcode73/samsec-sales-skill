---
name: sales-prestashop
description: "PrestaShop platform help — open-source, self-hosted PHP/MySQL commerce platform for developers, agencies, and makers: products/combinations, orders, customers, carts, stock, taxes, CMS, multistore, and a 300+ feature back office extended by modules and a hook system. Its CRUD Webservice REST API sits at `/api/` with HTTP Basic auth (32-character key, empty password) and XML-or-JSON output. Use when enabling the Webservice and generating an API key, a call 401s because the Authorization header is stripped (CGIPassAuth/.htaccess), building a product/order/stock sync to a CRM or warehouse, reacting to a new order when there are no native webhooks (module hook, a Webhooks module, or polling), a 1-Click or PHP-8 upgrade breaking overrides/modules, or choosing PrestaShop Classic vs Hosted vs Shopify/WooCommerce/OpenCart/Magento. Do NOT use for cross-cart checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in PrestaShop — e.g. 'sync products in via the Webservice API' or 'notify my CRM on a new order without webhooks']"
license: MIT
version: 1.0.1
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/PrestaShop"
---

# PrestaShop Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — standing up a store, building/debugging a **Webservice API** integration, syncing products/orders/stock to a CRM or warehouse, reacting to an order event, a module/override/upgrade problem, or a platform-selection decision?
- **Surface** — the **Webservice REST API** (`/api/`, CRUD over ~70 resources), a **module + hook** (for event push or custom logic), the **admin back office** UI, or a **theme** (Smarty)?
- **Auth** — HTTP **Basic** with a **32-character key** as username and an **empty password**; a `401` usually means the key's permissions are wrong or the `Authorization` header is being stripped (**CGIPassAuth**).
- **Hosting** — **Classic** (self-hosted, you own PHP/MySQL + hosting) or **Hosted / "Ready"** (managed ~€29/mo)? Which **PrestaShop version** (1.6 / 1.7 / 8.x / 9.x) and **PHP version**?

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Comparing PrestaShop against another commerce backend at a high level | `/sales-checkout {question}` (platform selection) |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Post-purchase / abandoned-cart email sequences | `/sales-email-marketing {question}` |
| Selling one catalog across Amazon/eBay/Etsy/marketplaces | `/sales-multichannel-selling {question}` |

Otherwise it's a PrestaShop-specific question — answer it here.

## Step 3 — PrestaShop platform reference

**Read `references/platform-guide.md`** for the full reference — modules and what's
API-accessible vs UI-only, pricing/infra posture, data model with JSON shapes, and
quick-start recipes. For raw auth/endpoint/resource detail, read
`references/prestashop-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **The API is a CRUD Webservice at `/api/`, XML by default.** Enable it (Advanced Parameters → Web service → Yes), create a **32-char key** with per-resource permissions, and call with HTTP **Basic** (key as username, **empty password**). Add `output_format=JSON` for JSON. `GET /api/` lists every resource you can reach.
- **If every call 401s, it's almost always CGIPassAuth.** Apache/PHP-FPM strips the `Authorization` header — add `CGIPassAuth On` (or the `SetEnvIf Authorization` fallback) to `.htaccess`. Otherwise check the key's per-resource rights.
- **Reads trim + filter; writes are XML and PUT is a full replace.** Use `display=[…]`, `filter[field]=…` (OR `[a|b]`, interval `[min,max]`, `%pattern%`), `sort=[field_ASC]`, `limit=start,count` (offset paging — no cursor). Create from `?schema=blank`; **PUT replaces the whole entity** (GET→mutate→PUT); set stock via `stock_availables`, not `products`.
- **There are no native outbound webhooks.** To push on a new order, write a small **module** that registers a hook (`actionValidateOrder`, `actionOrderStatusUpdate`) and cURLs out (add your own HMAC), install a **third-party Webhooks module**, or **poll** orders. Keep hook handlers fast — they run in-process during checkout.
- **It's self-host: infra and upgrades are yours.** Match the **PHP version** to the PrestaShop version, keep **overrides thin**, and test the **1-Click Upgrade** on staging — third-party modules/overrides are what break on major upgrades. Not a Merchant of Record — you own tax.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — re-verify the resource list/verbs, auth behaviour, pricing, and PHP/version compatibility against live docs.*

- **401 on every call = stripped Authorization header.** The classic cause is Apache/PHP-FPM dropping the header before PHP sees it. Add `CGIPassAuth On` to `.htaccess` (or `SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1`). Second cause: the key lacks permission on that resource/verb.
- **The key is the username; the password is empty.** With cURL use `-u "KEY:"` (trailing colon). Never put the key in the URL for production — it leaks into logs/history.
- **No outbound webhooks in core.** There is no "add a webhook URL" screen. Push events via a **module hook**, a 3rd-party Webhooks module, or poll — nothing signs the payload for you, so add your own secret/HMAC.
- **PUT replaces the entire entity.** A partial PUT wipes unspecified fields. GET the full record, mutate, PUT it back (keep the `<id>`). Only some resources (`stock_availables`, `warehouses`) accept `PATCH`.
- **Stock isn't on the product.** Quantity lives on `stock_availables` (or ASM `warehouses`/`stock_movements`) — updating `products` won't change what's sellable.
- **XML-first, per-language fields.** Input is XML (JSON is output-only in practice); translatable fields (`name`, `link_rewrite`) are wrapped per `<language id="…">`, and slugs must be clean (lowercase/hyphenated) or you get validation errors.
- **Upgrades break modules/overrides.** The 1.6→1.7 Symfony shift and PHP 7→8 deprecations (e.g. `Tools::jsonEncode`) leave third-party modules and heavy overrides throwing 500s. Test the 1-Click Upgrade on staging; keep overrides minimal.
- **Advanced Stock Management is optional.** `warehouses`/`supply_orders`/`stock_movements` resources only exist when ASM is enabled.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and high-level platform selection.
- **WooCommerce** — the other big self-hosted PHP store (WordPress plugin); compare data ownership, REST API + webhooks, and ecosystem. For cart-platform selection across tools, use `/sales-checkout`.
- `/sales-bagisto` — Open-source **Laravel/PHP** commerce framework — the other PHP-stack option; also no native outbound webhooks (Laravel events instead of PrestaShop hooks).
- `/sales-evershop` — Open-source Node/TypeScript commerce platform — contrast the JS stack + in-process event subscribers with PrestaShop's PHP + hook system.
- `/sales-medusa` — Open-source headless Node/TS commerce engine — compare against PrestaShop's bundled storefront+admin+API.
- `/sales-shopify` — The leading hosted commerce backend — compare against PrestaShop's self-hosted/open-source model and infra ownership.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (PrestaShop is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync a product catalog in via the Webservice API (developer/automation)
**User**: "I'm writing a nightly script to push products and stock into PrestaShop. Which API and how do I authenticate?"
**Approach**: Use the **Webservice** at `/api/`. Enable it (Advanced Parameters → Web service), generate a **32-char key**, and grant it GET/POST/PUT on `products`, `combinations`, and `stock_availables`. Authenticate with HTTP **Basic** — key as username, **empty password** (`curl -u "KEY:"`). To create, GET `products?schema=blank`, fill the XML (price, reference, and `name`/`link_rewrite` per `<language>`), and POST it; to update, GET the full record, mutate, and **PUT it back** (PUT replaces the whole entity). Set quantities on **`stock_availables`**, not on the product. If calls 401 despite a valid key, add `CGIPassAuth On` to `.htaccess`. Verify/export with `output_format=JSON&display=[…]`.

### Example 2: Notify a CRM when an order is placed without webhooks (developer/automation)
**User**: "Where do I add a webhook URL in PrestaShop so my CRM gets pinged on each new order?"
**Approach**: Explain there's **no outbound-webhook screen** in core. The reliable path is a **small custom module** that registers on `actionValidateOrder` (and `actionOrderStatusUpdate` for status changes) and cURLs a JSON payload to your CRM with an **HMAC `X-PS-Signature`** header. Because hooks run **in-process during checkout**, keep the call fast (short timeout) or enqueue it so a slow CRM never blocks the buyer. No-code alternatives: a **third-party "Webhooks" module** from Addons, or a **Zapier/Make** "new order" trigger. If you can't deploy code, **poll** `orders?sort=[id_DESC]&filter[date_add]=[…]` and track the last-seen `id`.

### Example 3: Choose PrestaShop vs other self-hosted stores
**User**: "I'm a solo founder who can run a server. PrestaShop, WooCommerce, or Shopify for a small EU store?"
**Approach**: **PrestaShop (Classic)** is free, self-hosted PHP/MySQL with a 300+ feature back office, a big module marketplace, and a stable CRUD API — strong for EU merchants and anyone already in its ecosystem, but you own hosting, PHP-version matching, and upgrade pain (modules/overrides break on majors). **WooCommerce** wins if the store lives inside WordPress/content. **Shopify** is hosted (no infra, faster launch) but has platform + possible gateway fees and less data ownership. If they want zero-infra, lean Shopify; if they want control/no-per-sale-fee and can run PHP, PrestaShop or WooCommerce. For cross-cart conversion tactics or MoR-tax decisions, route to `/sales-checkout` or `/sales-merchant-of-record`. Re-verify pricing/versions before committing.

## Troubleshooting

### "Every Webservice call returns 401 Unauthorized"
Two usual causes. (1) **Stripped auth header** — Apache/PHP-FPM drops `Authorization` before PHP reads it, so the key never arrives. Add `CGIPassAuth On` to the shop-root `.htaccess`, or `SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1`. (2) **Permissions** — the key isn't granted that verb on that resource (Advanced Parameters → Webservice → your key → Permissions). Confirm the Webservice itself is **enabled**, use `-u "KEY:"` (key as username, empty password, trailing colon), and check the key **Status** is active.

### "A PUT wiped fields / my product-create fails validation"
`PUT /api/{resource}/{id}` is a **full replace**, not a patch — any field you omit is cleared. Fetch the record with `display=full`, change only what you need, and PUT the **entire** document back (keep `<id>`). For create/validation errors ("… is not valid"), start from `GET /api/{resource}?schema=synopsis` to see required fields/format rules; the most common trip-ups are non-slug `link_rewrite`/`reference` (must be lowercase, hyphenated) and forgetting the per-`<language>` wrapper on translatable fields. Set stock on `stock_availables`, not `products`.

### "After a 1-Click Upgrade my modules/back office throw 500 errors"
Major upgrades (1.6→1.7 Symfony migration, PHP 7→8) break third-party modules and overrides that use deprecated classes/functions (e.g. `Tools::jsonEncode`) or namespace assumptions. Always run the upgrade on a **staging copy** first, then: match the **PHP version** to the target PrestaShop version, disable overrides and re-enable them one at a time to isolate the culprit, update or replace incompatible modules, clear the cache (`var/cache`), and enable **debug mode** to read the real stack trace. Keep overrides thin so the next upgrade survives.
