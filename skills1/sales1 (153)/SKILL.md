---
name: sales-drupal-commerce
description: "Drupal Commerce platform help — the open-source (GPL) commerce framework built on Drupal/PHP (drupalcommerce.org, by Centarro): stores, products/variations, orders, carts, checkout, payments, and promotions as Drupal entities, exposed headlessly through core JSON:API (UUID-addressed, page[offset]/page[limit] paging) plus the Commerce Cart API module (cart tokens, add/update items, checkout, Commerce-Current-Store header, order-transition webhooks). Auth via Simple OAuth (Bearer), Basic, or JWT. Use when building a headless/decoupled Drupal Commerce storefront, fixing add-to-cart failing over JSON:API without granting anonymous users admin-store permission, authenticating with Simple OAuth, wiring orders into a CRM or warehouse, reacting to an order state transition, or choosing Drupal Commerce vs Shopify/Magento/WooCommerce for a content-heavy store. Do NOT use for cross-cart checkout strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Drupal Commerce]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, checkout, headless, platform]
github: "https://github.com/drupalcommerce"
---

# Drupal Commerce Platform Help

Drupal Commerce (drupalcommerce.org, maintained by **Centarro** since 2010) is an open-source (GPL)
commerce framework built **on Drupal/PHP** — everything (stores, products/variations, orders, carts,
promotions, customer profiles) is a **Drupal entity**, so commerce and content share one system. Its
sweet spot is content-heavy, custom-catalog, or unusual-checkout stores that a **developer/agency**
builds. It's headless-capable via Drupal core **JSON:API** plus the **Commerce Cart API** module. It's
free/self-hosted (you own hosting + dev), and **not a Merchant of Record**. Most integration friction
is Drupal's permission model and its entity/JSON:API structure, not a vendor limit.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Build a **headless/decoupled storefront** (cart & checkout over the API)
   - B) Read/write back-office data (products, orders, customers) via **JSON:API**
   - C) React to an event (order placed/paid, product changed) — webhook or Drupal event subscriber
   - D) Authenticate the API (Simple OAuth / Basic / JWT) or debug a 401/403
   - E) Configure the store itself (product types, checkout flow, payment gateways) in Drupal admin
   - F) Decide Drupal Commerce vs another platform, or scope a build
2. **Which Drupal + Commerce major (Drupal 10/11, Commerce 2/3), and is the Commerce Cart API /
   Simple OAuth module installed?** Headless cart and OAuth are contrib modules, not on by default.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/commerce platform to pick, or checkout-conversion strategy (Drupal Commerce vs Shopify/Magento/WooCommerce; bumps, upsells, cart abandonment) | `/sales-checkout {question}` |
| The headless-vs-monolith / composable architecture decision itself | `/sales-checkout {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Choosing a hosted Merchant of Record so someone else owns global VAT/GST (Drupal Commerce is NOT one) | `/sales-merchant-of-record {question}` |
| Migrating a store's catalog/customers/orders into or out of Drupal Commerce | `/sales-store-migration {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer Drupal Commerce-specific questions directly using Step 3.

## Step 3 — Drupal Commerce platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface
(what's JSON:API-, Cart-API-, webhook-, event-subscriber-accessible vs Drupal-admin-only), the
free/self-host cost model, data model (UUID-addressed entities, `commerce_product` /
`commerce_order` / `commerce_order_item` shapes), and quick-start recipes (Simple OAuth token +
JSON:API read, headless add-to-cart with a cart token, order-event outbound integration).

For raw endpoint detail, the JSON:API conventions, auth flows, pagination, and the Commerce Cart API
endpoints/webhooks, read `references/drupal-commerce-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **For headless cart/checkout, use the Commerce Cart API module — never open store admin to
  anonymous users.** Adding an item straight through raw **JSON:API** fails unless anonymous users get
  the *administer stores* permission, which is a security hole — do NOT grant it. Instead install the
  **Commerce Cart API** (part of Commerce API) module, get a **cart token** for the shopper, and use
  its cart endpoints (get cart, add/update/remove items, checkout). Send the **`Commerce-Current-Store`**
  header in multi-store setups.
- **Authenticate with Simple OAuth and read a 401 vs 403 correctly.** For programmatic access install
  the **Simple OAuth** module and get a Bearer token from **`POST /oauth/token`** (password or
  client_credentials grant); send `Authorization: Bearer …`. A **401** means missing/invalid
  credentials; a **403** means authenticated but the Drupal **role/permission** doesn't allow that
  entity/operation (Drupal access control is per-permission) — fix the role, don't over-grant. Basic
  auth (basic_auth) and JWT are alternatives. Whenever you explain auth, also state the **JSON:API
  request conventions** the call must follow — resources at **`/jsonapi/{entity_type}/{bundle}`**,
  items addressed by **UUID**, and the **`Accept: application/vnd.api+json`** header — and, for a
  browser/decoupled client, that **CORS must be enabled** (add the front-end origin to `cors.config`
  in `services.yml`) or the token-authenticated request still fails in the browser.
- **Query JSON:API by its conventions, not REST-style URLs.** Resources live at
  **`/jsonapi/{entity_type}/{bundle}`** (e.g. `/jsonapi/commerce_product/default`,
  `/jsonapi/commerce_order/default`); individual items are addressed by **UUID**, headers are
  `application/vnd.api+json`, and there is **no PUT** (use PATCH). Filter with `?filter[…]`, embed
  relations with `?include=`, trim fields with `?fields[…]`, and paginate with
  **`?page[offset]=` + `?page[limit]=`** (JSON:API default limit ~50). IDs are **UUIDs** in URLs even
  though entities also have an internal integer id.
- **For outbound events, prefer the Commerce API order-transition webhook, else a Drupal event
  subscriber — and always keep a polling backup.** The **Commerce API** module can emit **order
  state-transition webhooks** to your endpoint. Treat the webhook payload as a hint, not truth:
  **re-fetch that single order by its UUID via `GET /jsonapi/commerce_order/default/{uuid}` (with your
  Bearer token) before you act on it** — provision, charge, or push to the CRM only from the re-fetched
  order, and dedupe on the order UUID so retries are idempotent. If a webhook doesn't fit, react in code
  to Drupal Commerce events (e.g. the order `place`/`fulfill` transition, `OrderEvents`) or
  `hook_ENTITY_TYPE_insert`, or use the contrib **Webhooks**/Rules module. Because a delivery can be
  missed, also pair any webhook with a nightly paginated `/jsonapi/commerce_order/default`
  (`page[offset]`/`page[limit]`) reconciliation pull.
- **Set expectations: it's a developer platform with a Drupal learning curve.** Drupal Commerce is
  module-driven, not turnkey — it needs Drupal/PHP developers, and the data model (entities, bundles,
  fields, profiles for billing/shipping) is powerful but not out-of-the-box. Frame cost as hosting +
  dev, present pricing as best-effort (the software is free/GPL), and point non-technical users at a
  turnkey option via `/sales-checkout`.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially module names and the permission
behaviors, which vary across Drupal/Commerce versions.*

- **Add-to-cart over raw JSON:API fails** unless anonymous users can *administer stores* — don't grant
  that. Use the **Commerce Cart API** module + a **cart token** for headless carts.
- **JSON:API addresses entities by UUID**, uses `application/vnd.api+json`, and has **no PUT** (PATCH
  to update). There's no `/jsonapi/{entity_type}` collision endpoint — always include the bundle.
- **401 ≠ 403.** 401 = bad/missing token; 403 = authenticated but the Drupal role lacks the permission.
  Fix roles/permissions rather than over-permissioning.
- **OAuth/JSON:API/Cart API are contrib or core-but-off** — Simple OAuth and Commerce Cart API must be
  installed and enabled; JSON:API is core but read-only by default until you allow writes.
- **Webhooks come from the Commerce API module** (order state transitions) — core Drupal has no native
  webhook UI; otherwise use an event subscriber, the Webhooks module, or Rules + HTTP. Keep a polling backup.
- **Multi-store needs the `Commerce-Current-Store` header** on Cart API calls, or operations hit the
  wrong/undefined store.
- **It's a Drupal build.** Needs PHP/Drupal devs and hosting; **not a Merchant of Record** (you own VAT/tax).

## Related skills

- `/sales-checkout` — Checkout-conversion strategy and cart/commerce-platform selection (Drupal Commerce vs Shopify/Magento/WooCommerce; the headless-vs-monolith decision)
- `/sales-merchant-of-record` — Choosing a Merchant of Record for global tax (Drupal Commerce is not one)
- `/sales-store-migration` — Migrating a store's catalog, customers, and orders between platforms
- `/sales-woocommerce` — WooCommerce platform help (the other CMS-plugin commerce, on WordPress)
- `/sales-shopware` — Shopware platform help (the PHP/Symfony mid-market/B2B alternative)
- `/sales-saleor` — Saleor platform help (a GraphQL-native headless alternative)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Build a headless add-to-cart against Drupal Commerce (developer/automation)
**User says**: "My decoupled front end can't add products to the cart via the Drupal Commerce API — it only works if I let anonymous users administer stores, which feels wrong."
**Skill does**: Confirms granting *administer stores* to anonymous is a security hole and not the fix;
installs the **Commerce Cart API** module, obtains a **cart token** for the anonymous shopper, and
uses the Cart API endpoints (get cart → add item → checkout) with the **`Commerce-Current-Store`**
header, authenticating reads/writes via **Simple OAuth** Bearer where needed — keeping store-admin
permissions off the anonymous role.
**Result**: Anonymous shoppers build carts through the Cart API without any over-permissioning.

### Example 2: Sync placed orders into a CRM/warehouse
**User says**: "How do I push every placed Drupal Commerce order into my CRM reliably?"
**Skill does**: Enables the **Commerce API order state-transition webhook** to a tokenized HTTPS
endpoint (or a Drupal event subscriber on the order `place` transition), re-fetches the order via
`GET /jsonapi/commerce_order/default/{uuid}` (Simple OAuth Bearer) before writing, dedupes on the
order UUID, and adds a nightly `page[offset]`/`page[limit]` paginated reconciliation pull as a
backstop in case a delivery is missed.
**Result**: CRM stays in sync with verified order data even if a webhook is dropped.

### Example 3: Drupal Commerce vs a turnkey platform for a content-heavy store
**User says**: "We run a big editorial site and want to add a store with unusual product attributes — is Drupal Commerce right, or should we use Shopify?"
**Skill does**: Frames Drupal Commerce's edge — commerce and content as one Drupal entity system, deep
custom attributes and checkout flows — against its cost: it's a **developer build** (Drupal/PHP + hosting),
free/GPL but not turnkey. Notes it's not a Merchant of Record, and routes the cross-platform tradeoff to
`/sales-checkout` for a turnkey (Shopify) comparison.
**Result**: The team chooses based on dev capacity and content-commerce fit, not feature lists.

## Troubleshooting

### Can't add to cart via the API (works only with admin-store permission)
**Symptom**: `POST` to add an order item over JSON:API 403s unless anonymous users can *administer stores*.
**Cause**: Raw JSON:API writes to `commerce_order`/`commerce_order_item` require broad entity
permissions; exposing them to anonymous users is unsafe. The cart flow is meant to go through the Cart API.
**Solution**: Install the **Commerce Cart API** module, request a **cart token** for the shopper, and
use its cart endpoints (add/update/remove items, checkout) with the `Commerce-Current-Store` header —
leave *administer stores* off the anonymous role.

### 401 or 403 on API calls
**Symptom**: Requests fail with 401 or 403.
**Cause**: **401** = missing/invalid token (or Simple OAuth not set up); **403** = authenticated but the
Drupal **role/permission** doesn't allow that entity/operation; sometimes CORS blocks a browser consumer.
**Solution**: Get a Bearer token from `POST /oauth/token` (Simple OAuth) and send it; for 403, grant the
specific permission to the API user's role (not a blanket admin role); configure CORS for browser clients.

### No native webhook to notify my system on a new order
**Symptom**: There's no webhook-URL screen in core Drupal.
**Cause**: Core Drupal has no outbound webhook UI; event delivery lives in the Commerce API module or in code.
**Solution**: Use the **Commerce API** module's **order state-transition webhook**, or write a Drupal
**event subscriber** on the order transition (`OrderEvents` / `commerce_order.place.post_transition`) /
`hook_ENTITY_TYPE_insert` that POSTs out, or the contrib **Webhooks**/Rules module. Add a polling
reconciliation pull as a safety net and dedupe on order UUID.
