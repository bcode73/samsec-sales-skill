---
name: sales-shopware
description: "Shopware platform help — the open-source PHP/Symfony commerce platform (shopware.com, Shopware 6): products, orders, customers, and two APIs — the Admin API (/api/*, OAuth 2.0 client-credentials via an Integration, 300 req/min) and the headless Store API (/store-api/*, sw-access-key), plus app webhooks (shopware-shop-signature HMAC-SHA256) and Flow Builder automation. Use when generating an Admin API OAuth token or debugging a 401 from extension-generated keys, searching entities via POST /api/search/{entity} with Criteria, wiring orders or customers into a CRM or warehouse, registering an app webhook for checkout.order.placed, building a headless storefront on the Store API, hitting the 300-req/min rate limit or random admin logouts, or choosing between the free Community Edition and the paid Rise/Evolve/Beyond plans under the GMV fair-usage policy. Do NOT use for checkout-conversion strategy across carts (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Shopware]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, checkout, headless, platform]
github: "https://github.com/shopware"
---

# Shopware Platform Help

Shopware (shopware.com) is an open-source **PHP/Symfony** commerce platform (Shopware 6) aimed at
mid-market and B2B merchants, strong in Europe, and built for **dev/agency-owned** stores rather
than click-together SaaS. The **Community Edition is free (MIT)** and self-hosted; paid **Rise /
Evolve / Beyond** tiers and Shopware Cloud add automation, B2B, and support. It exposes two
distinct HTTP APIs — the **Admin API** (`/api/*`, back-office) and the **Store API**
(`/store-api/*`, headless storefront) — plus a **webhook-capable App system** and Flow Builder
automation. It is heavier than EverShop/Medusa: expect to run PHP/Symfony infra.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Read/write back-office data (products, orders, customers) via the **Admin API**
   - B) Build a headless / custom storefront (**Store API** cart & checkout)
   - C) React to events (order placed, product changed) via an **app webhook** or Flow Builder
   - D) Bulk-import/sync a catalog (Sync API, search Criteria, pagination)
   - E) Configure the store itself (sales channels, products, plugins) in the Administration
   - F) Choose an edition (Community vs Rise/Evolve/Beyond, self-host vs Cloud) or understand the GMV fair-usage policy
2. **Self-hosted or Shopware Cloud, and which version (6.5 / 6.6 / 6.7)?** Field shapes and the admin
   stack differ across majors; Cloud restricts plugin installs to the store and the App system.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/commerce platform to pick, or checkout-conversion strategy (Shopware vs Shopify/Magento/Medusa; bumps, upsells, cart abandonment) | `/sales-checkout {question}` |
| The headless-vs-monolith / composable architecture decision itself | `/sales-checkout {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Choosing a hosted Merchant of Record so someone else owns global VAT/GST (Shopware is NOT one) | `/sales-merchant-of-record {question}` |
| Migrating an existing store's catalog/customers/orders into or out of Shopware | `/sales-store-migration {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer Shopware-specific questions directly using Step 3.

## Step 3 — Shopware platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface
(what's Admin-API-, Store-API-, webhook-accessible vs Administration-only), editions/pricing and the
GMV fair-usage gate, data model (UUID-hex IDs, the search-Criteria query model, translatable
fields), and quick-start recipes (OAuth token + entity search, Sync API bulk upsert, app webhook
with signature verification).

For raw endpoint detail, the OAuth flows, Criteria/pagination, Sync API, and verbatim webhook
events/signature, read `references/shopware-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Authenticate the Admin API with a manually-created Integration, and read a 401 as the wrong
  credential source.** Get the OAuth token via `POST /api/oauth/token` with
  `grant_type=client_credentials`, `client_id`=Access Key ID, `client_secret`=Secret Access Key from
  **Settings → System → Integrations**. If a 401/"token invalid" appears, the usual cause is using
  **keys returned by a plugin/extension install** (which often can't mint tokens) or a stale token —
  create a dedicated Integration instead, and refresh the Bearer token before it expires (`expires_in`
  is ~3600s). For the Store API, authenticate with the **`sw-access-key`** sales-channel key, not OAuth.
- **Query with the search-Criteria model, not REST filters in the URL.** Most reads are
  `POST /api/search/{entity}` with a JSON **Criteria** body (`filter`, `sort`, `limit`, `page`,
  `associations`, `aggregations`) — plain `GET /api/{entity}` exists but real queries go through
  `/search`. Paginate with `limit` + `page` (not offset) and set `total-count-mode` when you need a
  count. IDs are **32-char hex UUIDs**, and translatable fields resolve by the request's language context.
- **Bulk-write through the Sync API, and respect 300 req/min.** For imports/upserts/deletes use
  `POST /api/_action/sync` (batched operations in one call) rather than one request per row. The
  **Admin API is capped at 300 requests/minute** — on `429` back off and resume; keep syncs
  incremental and batched. Store API limits vary by server config.
- **For outbound events, register an App-system webhook and verify the signature.** Events fire from
  the **App system** (manifest `<webhooks>` with `name`/`url`/`event`), e.g. **`checkout.order.placed`**,
  `state_enter.order_transaction.state.paid`, `product.written`, `order.written`. Every delivery
  carries a **`shopware-shop-signature`** header = **HMAC-SHA256 of the raw request body** keyed by
  the app secret assigned at registration — recompute and compare (constant-time) before trusting it,
  then re-fetch the entity via the Admin API. Add **`onlyLiveVersion: true`** so order drafts don't
  fire, and keep a polling backup. Flow Builder can also POST to an HTTP endpoint as an action.
- **Warn about the GMV fair-usage gate and self-host reality.** Present all pricing as best-effort:
  Community Edition is free/MIT, but under the **Fair Usage Policy (from March 2026) a store over
  ~€1M GMV must move to a paid plan** (Rise/Evolve/Beyond) — flag this early for anyone scaling.
  Self-hosting means running PHP/Symfony + MySQL/OpenSearch + a message queue; it needs developers
  and real hosting/PCI budget. Verify current numbers at shopware.com/pricing.
- **If the admin keeps logging out, it's the known token-refresh race, not the user.** Randomly
  losing the Administration session (especially across multiple tabs) is a long-standing refresh-token
  race condition — reduce to a single admin tab, clear the session, and check for the latest patch;
  it's not a misconfiguration on their end.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially edition pricing, the GMV fair-usage
threshold, and the auth behaviors, which change across versions.*

- **Admin API auth = OAuth via an Integration, Store API = `sw-access-key`.** Don't mix them; a 401 is
  usually keys from a plugin-install response (can't mint tokens) — use a manual Integration.
- **The query model is `POST /api/search/{entity}` with a Criteria body** — filters/sort/pagination
  go in JSON, not URL query params. Pagination is `limit`+`page`, not offset.
- **300 requests/minute on the Admin API** — batch with the Sync API (`/api/_action/sync`) and back off on 429.
- **Webhooks come from the App system, signed with `shopware-shop-signature`** (HMAC-SHA256 of the raw
  body). Use `onlyLiveVersion` to skip order drafts; verify before trusting.
- **GMV fair-usage gate** — Community Edition is free, but from March 2026 a store over ~€1M GMV must
  buy a paid plan. Flag for scaling merchants.
- **Random admin logouts** = the refresh-token race condition (multi-tab), not a config error.
- **Self-hosting is heavy** — PHP 8.2+/Symfony, MySQL/MariaDB, OpenSearch, message queue; needs devs.
  It's **not a Merchant of Record** (you own VAT/tax).
- **IDs are 32-char hex UUIDs** and many fields are translatable by language context — don't assume
  integer IDs or a single locale.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy and cart/commerce-platform selection (Shopware vs Shopify/BigCommerce/Magento/Medusa; the headless-vs-monolith decision)
- `/sales-merchant-of-record` — Choosing a Merchant of Record for global tax (Shopware is not one)
- `/sales-store-migration` — Migrating a store's catalog, customers, and orders between platforms
- `/sales-woocommerce` — WooCommerce platform help (the self-hosted WordPress-plugin alternative)
- `/sales-prestashop` — PrestaShop platform help (the other self-hosted PHP commerce platform)
- `/sales-medusa` — Medusa platform help (the Node/TS headless alternative for lighter self-hosted stacks)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new Shopware orders into a CRM/warehouse (developer/automation)
**User says**: "How do I push every placed Shopware order into my CRM automatically and reliably?"
**Skill does**: Registers an **App-system webhook** on **`checkout.order.placed`** (with
`onlyLiveVersion: true` so drafts don't fire) to a tokenized HTTPS endpoint, verifies each delivery
by recomputing **HMAC-SHA256 of the raw body** against the **`shopware-shop-signature`** header, then
re-fetches the order with `POST /api/search/order` (OAuth Bearer from an Integration) before writing —
deduping on the order id. Adds a batched **Sync API** / paginated `/search` reconciliation pull as a
backstop and notes the **300 req/min** Admin-API cap.
**Result**: CRM stays in sync with verified data even if a delivery is missed, within the rate limit.

### Example 2: Every Admin API call returns 401 "token invalid"
**User says**: "I got an access key and secret from a Shopware plugin but I can't generate an OAuth token — 401 every time."
**Skill does**: Explains that **plugin/extension-returned keys often can't mint tokens**; walks the
user to create a dedicated **Integration** under **Settings → System → Integrations**, then
`POST /api/oauth/token` with `grant_type=client_credentials` + that Integration's Access Key ID
/ Secret Access Key, and to send the resulting **Bearer** token (refreshing before `expires_in`).
Notes the Store API uses `sw-access-key` instead, not OAuth.
**Result**: Token generation works with a proper Integration; the 401 was the wrong key source.

### Example 3: Community Edition vs a paid plan for a scaling store
**User says**: "We're on free Shopware Community Edition doing about €1.5M/year — do we have to pay now?"
**Skill does**: Flags the **Fair Usage Policy (from March 2026)** — CE is free only **under ~€1M GMV**,
so at €1.5M they fall into a paid tier (Rise/Evolve/Beyond), where the choice is driven by B2B/support
needs and GMV, not core features; notes CE is still self-hosted (they cover hosting/dev). Presents all
figures as best-effort to verify at shopware.com/pricing.
**Result**: The team plans for a paid plan they now legally need, chosen by needs rather than feature FOMO.

## Troubleshooting

### 401 / "token invalid" on the Admin API
**Symptom**: `POST /api/oauth/token` or authenticated calls return 401.
**Cause**: Using Access Key/Secret returned by a **plugin install** (which frequently can't generate
tokens), an expired Bearer token, or hitting the Store API path with OAuth (or vice-versa).
**Solution**: Create a dedicated **Integration** (Settings → System → Integrations) and use its
Access Key ID as `client_id` and Secret Access Key as `client_secret` with
`grant_type=client_credentials`; refresh the Bearer before `expires_in` (~3600s). Use `sw-access-key`
for the Store API, OAuth only for `/api/*`.

### Randomly logged out of the Administration
**Symptom**: The admin session drops unexpectedly, especially with multiple tabs open.
**Cause**: A long-standing **refresh-token race condition** — not a misconfiguration.
**Solution**: Work in a single admin tab, clear the session/cookies, and update to the latest patch
release; if scripting the Admin API, manage one token per client and refresh serially rather than racing.

### Slow responses / 429 Too Many Requests
**Symptom**: Bulk reads/writes slow down or start returning 429.
**Cause**: The **Admin API caps at 300 requests/minute**; unbatched per-row writes and uncached
queries compound it.
**Solution**: Batch writes through the **Sync API** (`POST /api/_action/sync`), paginate reads with
Criteria `limit`+`page`, enable HTTP cache/Redis/OpenSearch, and back off on 429 before resuming.
