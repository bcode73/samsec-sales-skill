---
name: sales-spree
description: "Spree Commerce platform help — open-source (BSD-3) headless commerce framework on Ruby on Rails for B2B, marketplace, and multi-store stores: products/variants, price lists, Markets (multi-currency), promotions, sales channels, and digital products; self-host the free Community Edition or buy Enterprise. Use when authenticating to the Platform API with OAuth2 client-credentials (`/spree_oauth/token`, Bearer token), wiring the Store API publishable key (`pk_xxx`) + order token, subscribing to Platform-API webhooks (Webhooks 2.0), using the new open-source Admin API or the AI-agent CLI / agent-skills / docs MCP server in Claude Code or Cursor, surviving a Spree version upgrade without breaking customizations or extensions, self-hosting the Rails/Postgres/Redis/Sidekiq stack, or choosing Community vs Enterprise. Do NOT use for cross-cart checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Spree — e.g. 'get a Platform API token' or 'self-host vs Enterprise']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/spree"
---

# Spree Commerce Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging an API integration, reacting to a commerce event via webhooks, using the AI-agent tooling (agent skills / docs MCP / Admin API CLI), upgrading a Spree version without breaking customizations, self-hosting, choosing Community vs Enterprise, or a checkout/conversion question?
- **Which API** — the **Store API** (`/api/v3/store`, customer-facing, publishable key), the **Platform API** (`/api/v2/platform`, machine-to-machine, OAuth2), the new **Admin API** (`/api/v3/admin`, open-sourced in 5.5, scoped keys), or the legacy **Storefront API v2** (`/api/v2/storefront`)?
- **Actor / auth** — a storefront client (**publishable key `pk_xxx`** + per-cart **order token**) or a backend integration (**OAuth2 client-credentials** → `Authorization: Bearer`)?
- **Hosting / edition** — **self-hosted Community Edition** (free, BSD-3, you run Rails + Postgres + Redis/Sidekiq) or **Enterprise Edition** (custom license, managed hosting, SSO, advanced B2B/marketplace)?

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Comparing Spree against another commerce backend | `/sales-checkout {question}` (platform selection) |
| Post-purchase email / abandoned-cart sequences | `/sales-email-marketing {question}` |

Otherwise it's a Spree-specific question — answer it here.

## Step 3 — Spree platform reference

**Read `references/platform-guide.md`** for the full reference — modules and what's API vs webhook vs UI-only, pricing/edition gates, the data model with JSON shapes, and quick-start recipes. For raw auth/endpoint/webhook detail, read `references/spree-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Pick the right API for the actor.** The **Store API** (`/api/v3/store`) is for storefronts — authenticate with a **publishable key** (`pk_xxx`, header) plus a per-cart **order token**; public catalog reads need no key. The **Platform API** (`/api/v2/platform`) is for backend/admin work and uses **OAuth2 client-credentials**. The **Admin API** (`/api/v3/admin`, new in 5.5) reads/writes every back-office resource with **scoped API keys**. Don't try to drive admin work with a publishable key — it can't.
- **Platform API auth is OAuth2, two steps.** Create an OAuth application in **Admin → Apps → OAuth Applications**, copy the Client ID + Secret, then `POST {store_url}/spree_oauth/token` with `grant_type=client_credentials`, `client_id`, `client_secret`, `scope=admin`. Send the returned token as `Authorization: Bearer {access_token}`. Tokens expire — refresh by requesting a new one.
- **Spree HAS native outbound webhooks.** Register a **webhook subscriber** via the Platform API (`/api/v2/platform/webhooks/subscribers`) with a URL and a `subscriptions` array (`['*']` for all events, or specific names like `order.canceled`). Each delivery is logged as a **Webhook Event** (name, response_code, success, request_errors) so you can debug failures. ⚠️ Confirm the current signature/HMAC scheme against live docs before relying on it (see Gotchas).
- **AI-agent tooling is a first-class surface (5.5+).** Spree ships ~25 installable **agent skills**, a **docs MCP server** (`https://spreecommerce.org/docs/mcp`), an **Admin API CLI** that lets an agent operate the whole back office, and auto-generated `CLAUDE.md`/`AGENTS.md` in scaffolded projects. For "how do I build/operate Spree with Claude Code or Cursor", point them at these first — they cut token use vs scanning Rails source.
- **Upgrades are the #1 historical pain.** Pinning to a major and using the **automatic upgrade tool** (5.5) plus universal (version-agnostic) extensions avoids the classic "upgrade broke my customizations" trap. Keep overrides thin (decorators/overrides, not forks of core).
- **Community Edition is free; Enterprise is a quote.** Self-host CE for $0 license (you own Rails/Postgres/Redis ops, ~$200–2,000/mo hosting). Enterprise adds SSO, managed hosting, and advanced B2B/marketplace/multi-tenant for a custom 5–6-figure/yr fee. **Spree is NOT a Merchant of Record** — you own tax remittance.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify edition gates, fees, auth, webhook-signature behavior, and API shapes against live docs at https://spreecommerce.org/docs.*

- **Don't confuse the APIs.** Store API uses a **publishable key**, Platform API uses **OAuth2 client-credentials**, Admin API uses **scoped API keys**. A storefront `pk_xxx` can't perform admin operations, and a 401 usually means you're hitting the wrong API for your token type.
- **Platform API token comes from `/spree_oauth/token`, not a static key.** You must first create an OAuth application in the admin, then exchange `client_id`/`client_secret` for a Bearer token. Missing the OAuth-app step is the most common "can't authenticate" cause.
- **Webhook signature scheme — verify before trusting.** Spree's webhook docs (Platform API webhook subscribers + "Webhooks 2.0"/Event Bus) were partially JS-rendered during research; the exact signature/HMAC header wasn't captured verbatim. Confirm whether deliveries are signed (and how) against live docs before standing up a public listener, and secure the endpoint with a secret URL/header in the meantime.
- **Upgrades historically broke customizations and extensions.** Older Spree upgrades were painful and many extensions were version-locked. Spree rewrote extensions to be universal and (5.5) ships an automatic upgrade tool — but heavy forking of core still makes upgrades hard. Keep customizations as thin decorators/overrides.
- **Self-hosting needs real Rails ops.** CE is a Ruby on Rails app: Postgres + Redis + a Sidekiq worker + MeiliSearch. It's not a one-click host like Shopify — a non-Rails team will need a developer. Budget for upgrades, backups, and scaling.
- **The DB schema is large and not self-explanatory.** Spree's data model (orders, line items, shipments, variants, stock, promotions) is deep. Use the Platform/Admin API and the shipped agent skills rather than querying the schema directly when you can.
- **Not a Merchant of Record.** Spree doesn't remit your sales tax/VAT — wire a tax service or sit a MoR upstream. See `/sales-merchant-of-record`.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and platform selection.
- `/sales-saleor` — The Python/Django GraphQL-first open-source headless engine; compare stack + API style (GraphQL vs Spree's REST).
- `/sales-medusa` — The Node.js/TypeScript open-source headless engine; another self-hostable backend to compare on stack and webhook model.
- `/sales-bagisto` — The Laravel/PHP open-source commerce framework; compare if your team is PHP- vs Ruby-oriented.
- `/sales-shopify` — The leading hosted commerce backend; compare against Spree's open-source/self-hosted model.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (Spree is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Get a Platform API token and pull orders (developer/automation)
**User**: "I'm writing a script to sync Spree orders into our warehouse. How do I authenticate and paginate?"
**Approach**: Spree's **Platform API** uses **OAuth2 client-credentials**, not a static key. First create an OAuth application in **Admin → Apps → OAuth Applications** and copy the Client ID + Secret. Then `POST {store_url}/spree_oauth/token` with `grant_type=client_credentials`, `client_id`, `client_secret`, `scope=admin`; the response's `access_token` goes in `Authorization: Bearer {token}` on every request. Hit `GET /api/v2/platform/orders` and page with the JSON:API `page[number]` / `page[size]` params, following `links.next` until it's null. Tokens expire — catch a 401 and re-request a token. (For an AI agent, the new Admin API CLI can do this without writing the HTTP layer yourself.)

### Example 2: Subscribe to an order webhook (developer/automation)
**User**: "I want Spree to notify my app when an order is canceled. How do I set that up?"
**Approach**: Use the Platform API to create a **webhook subscriber**: `POST /api/v2/platform/webhooks/subscribers` with a JSON:API body containing your `url` and `subscriptions` (e.g. `["order.canceled"]`, or `["*"]` for everything). Authenticate with a Platform-API OAuth Bearer token. Deliveries are recorded as **Webhook Events** (`name`, `response_code`, `success`, `request_errors`) — query those to debug a failing endpoint. Before exposing the listener publicly, confirm Spree's current signature scheme in the live docs and gate the endpoint with a secret URL/header so you only accept genuine deliveries.

### Example 3: Self-host Community Edition vs buy Enterprise
**User**: "I'm a solo founder. Should I self-host Spree's free edition or pay for Enterprise?"
**Approach**: The **Community Edition is BSD-3 / free** — but it's a real **Ruby on Rails** app needing **Postgres + Redis + Sidekiq + MeiliSearch** and ongoing ops (upgrades, backups, scaling), so plan ~$200–2,000/mo hosting plus developer time, and expect to keep customizations thin so version upgrades don't break. **Enterprise Edition** is a custom 5–6-figure/yr license that adds SSO (SAML/OIDC), managed hosting, premium support, and advanced B2B/marketplace/multi-tenant modules — overkill for a solo founder. Recommendation: if you're comfortable running Rails, self-host CE (cheapest, full control) and lean on the shipped agent skills + docs MCP server to move fast; if you don't want to run a Rails stack at all, a hosted backend or drop-in cart is a better fit than Spree.

## Troubleshooting

### "I can't authenticate to the Platform API / I keep getting 401"
The Platform API doesn't accept a static key or a storefront publishable key. Create an **OAuth application** in **Admin → Apps → OAuth Applications**, then exchange its `client_id`/`client_secret` at `POST {store_url}/spree_oauth/token` (`grant_type=client_credentials`, `scope=admin`) for an **access token**, and send it as `Authorization: Bearer {token}`. A 401 means you're using the wrong token type for the API (publishable key → Store API; OAuth Bearer → Platform API; scoped key → Admin API), the token expired, or the OAuth app wasn't created.

### "My Spree upgrade broke my customizations / extensions"
Historically Spree version upgrades were the biggest pain point and some extensions were version-locked. Pin to a major version, use the **automatic upgrade tool** (5.5+), and switch any version-locked extensions to their universal (version-agnostic) builds. The durable fix is to keep customizations as thin **decorators/overrides** rather than forking core models/views — forks are what make every upgrade a rewrite. The shipped agent skills document "how to upgrade without breaking customizations" specifically.

### "Self-hosting is overwhelming / the store is slow or the schema is confusing"
Community Edition is a full Rails stack — confirm Postgres, Redis, a running **Sidekiq** worker, and MeiliSearch are all healthy before debugging app behavior; a missing background worker or search service causes most "it's broken/slow" reports. For the opaque data model, prefer the **Platform/Admin API** and the **docs MCP server** (`https://spreecommerce.org/docs/mcp`) + agent skills over reading the schema directly. If you have no Rails capacity at all, that's the signal to consider Enterprise (managed hosting) or a hosted platform instead.
