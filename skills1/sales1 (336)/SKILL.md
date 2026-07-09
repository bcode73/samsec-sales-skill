---
name: sales-medusa
description: "Medusa platform help — open-source (MIT) headless commerce engine for developers and makers: products, orders, carts, customers, and checkout via REST Admin and Store APIs, an in-codebase event/subscriber system in place of native outbound HTTP webhooks, and self-hosted or Medusa Cloud hosting. Use when building a Medusa Admin or Store API integration, authenticating requests (JWT bearer vs API-key Basic vs cookie session), wiring an order.placed event to notify an external system or CRM since Medusa has no built-in outbound webhooks, choosing between self-hosting and Medusa Cloud plans (Develop/Launch/Scale), migrating from v1 to v2, paginating with limit/offset, or comparing Medusa to Shopify/BigCommerce. Do NOT use for cross-cart checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Medusa — e.g. 'notify my CRM when an order is placed' or 'JWT vs API key auth']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/medusajs"
---

# Medusa Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging an API integration, reacting to a commerce event, choosing self-host vs Medusa Cloud, a checkout/conversion question, or a store-ops task?
- **Surface** — Admin API (`/admin`), Store API (`/store`), the auth routes (`/auth/...`), the event/subscriber system, the JS SDK, the MCP server, or the Admin dashboard UI?
- **Version** — v2 (current, modular framework) or legacy v1? Endpoints, auth, and the module system differ.
- **Hosting** — self-hosted (own infra: Postgres + Redis + Node) or Medusa Cloud (Develop / Launch / Scale / Enterprise)?

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really a cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Digital-product pricing & launch strategy | `/sales-digital-products {question}` |
| Post-purchase email / abandoned-cart sequences | `/sales-email-marketing {question}` |
| Comparing Medusa against another commerce backend | `/sales-checkout {question}` (platform selection) |

Otherwise it's a Medusa-specific question — answer it here.

## Step 3 — Medusa platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and what's API vs event vs UI-only, pricing/plan gates, data model with JSON shapes, and quick-start recipes. For raw auth/endpoint/pagination/event detail, read `references/medusa-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **There are no native outbound webhooks.** Medusa emits *internal* events (e.g. `order.placed`); you react in a **subscriber** file (`src/subscribers/*.ts`) or build outbound HTTP yourself in that handler. To push to an external URL/CRM, write the `fetch` in the subscriber or install a community webhook plugin — don't expect a "webhooks" settings page like Shopify/Stripe.
- **Pick the right auth for the surface.** Admin/Store APIs accept a **JWT Bearer** token (from `/auth/{actor}/{provider}`), an **API key in the `Authorization: Basic` header** (admin secret keys), or a **cookie session** (`/auth/session`). Storefronts also send a **publishable API key** header to scope sales channels.
- **Know the v1/v2 split.** v2 is the modular framework (workflows, modules, `@medusajs/framework`); v1 endpoints and the old JS client differ. Confirm the version before quoting paths.
- **Self-host is free; Cloud is for not running infra.** The engine is MIT and 0% GMV fee everywhere; Medusa Cloud (from $29/mo Develop) sells managed Postgres/Redis/deploys — custom domains, autoscaling, and background workers are gated to higher tiers.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify plan gates, fees, auth, and API versions against live docs.*

- **No built-in outbound webhooks.** Medusa's "events" fire *inside* your app and are handled by subscribers in code — there is no UI to register an external webhook URL. Outbound delivery (retries, signing, logging) is your responsibility unless you add a plugin.
- **Events ≠ critical-path.** Subscribers run async for side-effects (emails, syncs). For logic that must affect the order flow, use a **workflow hook**, not a subscriber — a failing subscriber won't roll back the order.
- **Local Event Module is dev-only.** The default in-memory event bus loses events on restart and doesn't scale across processes; production needs the **Redis Event Module** (and Redis for the workflow/cache infra too).
- **v1 vs v2 confusion.** Lots of tutorials and the old `medusa-react`/JS client target v1. v2 uses `@medusajs/js-sdk`, `@medusajs/framework`, and a different module/auth model.
- **Storefront calls need a publishable API key.** Store API requests without the `x-publishable-api-key` header (scoping the sales channel) return errors or empty data.
- **It's a framework, not a turnkey store.** Expect a real dev setup (Node, Postgres, Redis) and a learning curve; there are no drag-and-drop themes — you build the storefront (e.g. the Next.js starter).

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and platform selection.
- `/sales-bigcommerce` — Another API-first commerce backend; compare if you're choosing a platform (BigCommerce is SaaS, Medusa is self-hostable).
- `/sales-spree` — Open-source (BSD-3) self-hostable headless engine on Ruby on Rails; compare by language (Ruby vs Node.js/TypeScript) and note Spree ships native outbound webhooks while Medusa uses in-process events/subscribers.
- `/sales-shopify` — The leading hosted commerce backend; compare against Medusa's self-hosted/open-source model.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (Medusa is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Notify a CRM when an order is placed (developer/automation)
**User**: "I set up a webhook in Medusa to POST to my CRM when an order completes, but I can't find where to add the webhook URL. How do I do this?"
**Approach**: Explain Medusa has **no outbound-webhook settings page** — you react to the internal `order.placed` event in a subscriber. Create `src/subscribers/order-placed.ts` exporting a handler (`SubscriberArgs<{ id: string }>`) plus `export const config = { event: "order.placed" }`; inside, resolve the order service to load the full order by `event.data.id`, then `fetch()` your CRM endpoint. Note the subscriber runs async (it won't block/roll back the order), and to use the **Redis Event Module** in production so events survive restarts.

### Example 2: Authenticating an Admin API script (developer/automation)
**User**: "I'm writing a Node script to pull all my Medusa orders into a warehouse. What auth do I use and how do I page through them?"
**Approach**: For server-to-server, create an **admin API key** and send it in `Authorization: Basic {key}` (base64 optional in v2), or obtain a **JWT** from `POST /auth/user/emailpass` and send `Authorization: Bearer {token}`. Call `GET /admin/orders?limit=100&offset=0`, read `count` in the response, and walk `offset` in steps of `limit` (sort with `order=-created_at`). Mention there's no documented hard rate limit, so still throttle politely.

### Example 3: Self-host vs Medusa Cloud
**User**: "Should I self-host Medusa or pay for Medusa Cloud? I'm a solo founder launching a small store."
**Approach**: The engine is **MIT/free with 0% GMV fee** either way — Cloud just sells managed infra. The $29/mo **Develop** tier is dev-grade (no custom domain, no autoscaling, capped compute/email) so it's for previews, not production; production starts at **Launch ($99/mo)** which adds custom domains, autoscaling, and zero-downtime deploys. If they're comfortable running Postgres + Redis + a Node host (Railway/Render/Fly), self-hosting is cheaper; if not, Launch removes the ops burden. Match the choice to their infra appetite, not defaults.

## Troubleshooting

### "Where do I register a webhook URL to notify an external system?"
You don't — Medusa has no outbound-webhook UI. Listen to the internal event in a **subscriber** (`src/subscribers/<name>.ts` with `config.event` set to e.g. `order.placed`) and make the outbound HTTP call yourself, or install a community webhook plugin (e.g. a `medusa-webhooks`/`medusa-events-webhooks` package). Use the **Redis Event Module** in production and add your own retry/signing/logging — none of that is built in.

### "My Store API request returns an error or empty data"
The Store API is scoped by sales channel via a **publishable API key** — send it in the `x-publishable-api-key` header. Also confirm you're hitting `/store/...` (not `/admin/...`) and that the resource is published to the channel your key maps to.

### "I followed a tutorial but the endpoints/imports don't exist"
You're likely mixing **v1 and v2**. v2 uses `@medusajs/js-sdk` and `@medusajs/framework`, a new module/workflow system, and the `/auth/{actor_type}/{provider}` auth routes; v1's `medusa-react`/old JS client and many older blog posts won't match. Check the version of your project (`@medusajs/medusa` in `package.json`) and read v2 docs specifically.
