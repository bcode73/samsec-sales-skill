---
name: sales-swell
description: "Swell platform help — API-first headless SaaS commerce backend (swell.is, github.com/swellstores) with a native subscription engine: products, carts, orders, checkout, coupons/promotions, gift cards, B2B/wholesale, and custom data models via a REST Backend API (api.swell.store, secret-key auth, swell-node/PHP libs, port 8443) plus a Frontend API (swell-js + GraphQL at {store}.swell.store/graphql/v2) and Swell Apps functions. Use when building a Swell Backend or Frontend API integration, choosing public vs secret API keys, wiring a Swell webhook to a CRM or warehouse (events are IP-allowlisted, no HMAC), migrating active subscribers without double-billing (the $migrate:true footgun), checkout forcing a shipping address on a digital-only order, hitting a plan's monthly API-request limit, or comparing Swell pricing/subscriptions vs Shopify/BigCommerce/Medusa. Do NOT use for cross-cart checkout-conversion tactics (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Swell — e.g. 'sync new orders to my CRM' or 'public vs secret API key']"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/swellstores"
---

# Swell Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out what the user actually needs before diving in:

- **Goal** — building/debugging an API integration, reacting to a commerce event, a subscription/billing question, a checkout/conversion question, a migration, or a store-ops task?
- **Surface** — **Backend API** (`api.swell.store`, secret key, server-side), **Frontend API** (swell-js or GraphQL, public key, client-side), **webhooks**, **Swell Apps** (serverless functions + custom models), the **Swell CLI**, or the **dashboard UI**?
- **Key type** — a **secret key** (full backend access — server-only) vs a **public key** (storefront/read scope — safe in the browser)? Using the wrong one is the most common auth mistake.
- **Plan** — Starter / Basic / Standard / Unlimited / Custom? Subscriptions, multi-currency, and API-request limits are plan-gated.

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2.

## Step 2 — Route or answer directly

If the question is really cross-platform strategy, hand off with the exact command:

| If the user wants… | Route to |
|---|---|
| Checkout conversion / order bumps / cart-abandonment tactics across carts | `/sales-checkout {question}` |
| Choosing a recurring-billing engine across tools (Swell vs Recharge/Chargebee/Stripe Billing) | `/sales-subscription-billing {question}` |
| Whether to use a Merchant of Record for global VAT/sales tax | `/sales-merchant-of-record {question}` |
| Digital-product pricing & launch strategy | `/sales-digital-products {question}` |
| Comparing Swell against another commerce backend | `/sales-checkout {question}` (platform selection) |

Otherwise it's a Swell-specific question — answer it here.

## Step 3 — Swell platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and what's API vs webhook vs UI-only, pricing/plan gates, data model with JSON shapes, and quick-start recipes. For raw auth/endpoint/pagination/webhook detail, read `references/swell-api-reference.md`.

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

You no longer need the full guide — focus on the user's situation.

- **Pick the key by where the code runs.** Server-side (Node/PHP/scripts) → **secret key** + `swell-node`/`swell-php` against `https://api.swell.store`. Browser/storefront → **public key** + `swell-js` or GraphQL (`https://{store}.swell.store/graphql/v2`). Never ship a secret key to the client.
- **Official libraries need port 8443 open.** `swell-node`/`swell-php` use a custom wire protocol on **port 8443** for performance/caching — if a server can't reach it, fall back to plain REST over 443 or fix the egress firewall.
- **Webhooks are thin and unsigned.** The payload carries `model`, `type`, and `data` (with the record `id`); there's **no HMAC** — secure the endpoint with the **Swell IP allowlist** + a secret URL/header, return **2xx within 10s**, and look the full record up by id via the Backend API.
- **Never set `$migrate: true` when importing subscriptions.** It skips the events that schedule billing — import them as normal records so billing anchors and next-charge dates are set correctly.
- **Mind plan gates.** Subscriptions need **Basic+**, multi-currency/price-lists need **Standard+**, and every tier has a **monthly API-request cap** ($5 / 100K over) — check the plan before promising an integration.

If you discover a gotcha or fix not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — re-verify plan gates, fees, auth, port, and webhook signing against live docs.*

- **Two API keys, two scopes.** A **secret key** has full backend access and must stay server-side; a **public key** is for storefront/GraphQL and is browser-safe. Get both from **Settings → API** (store ID is shown there too).
- **Webhooks have no HMAC signature.** Verify origin with the published **Swell IP allowlist** and a secret URL/path or custom header — don't assume a signing secret like Stripe/Shopify. Endpoints **auto-disable** after repeated failures (hourly retries ~2 days, warnings, then off ~day 3; `auto_disabled` after 7 days).
- **Digital-only carts still ask for shipping.** Swell has historically forced shipping fields even on digital goods — set the product `delivery` to `giftcard`/`subscription`/none and handle the address requirement in your storefront logic.
- **No custom SMTP.** Transactional email sends from Swell's infrastructure — you can't point it at your own SMTP; route critical mail through a webhook + your own ESP if you need full control.
- **API/docs maturity varies.** Reviewers report rough edges and slow support on niche areas (some integration docs thin, content-model editor bugs). Prefer driving the store via the **Backend API** over the dashboard, and keep a fallback for undocumented behavior.
- **Subscription import = double-bill risk.** See `$migrate: true` above — get a sandbox import right before touching live subscribers.

## Related skills

- `/sales-checkout` — Checkout-conversion strategy across carts (order bumps, upsells, cart-abandonment recovery) and platform selection; has an *In Swell* section.
- `/sales-subscription-billing` — Choosing/operating a recurring-billing engine; compare Swell's native subscriptions vs Recharge/Chargebee/Stripe Billing.
- `/sales-medusa` — Open-source, self-hostable headless engine; compare against Swell's managed SaaS model.
- `/sales-bigcommerce` — Another API-first SaaS commerce backend; the platform Swell most directly positions against.
- `/sales-merchant-of-record` — Whether to use a MoR (Paddle, Lemon Squeezy) for global tax instead of self-managing (Swell is not a MoR).
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new Swell orders into a CRM (developer/automation)
**User**: "I want my CRM to get a record every time someone places an order in Swell. I set up a webhook but the payload only has an id — where's the rest of the order?"
**Approach**: Explain Swell webhooks are **thin** — the POST body is `{id, date_created, model:"order", type:"order.created", data:{id, ...}}`, so use `data.id` to fetch the full order from the **Backend API** (`swell.get('/orders/{id}')` with the secret key, server-side). Configure the webhook at **Developer → Webhooks** (or via a Swell App) on the `order.created` event. Since there's **no HMAC**, restrict the endpoint to Swell's **IP allowlist** + a secret path/header, return **2xx within 10s** (do the CRM write async), and remember the hook **auto-disables** after repeated non-2xx responses.

### Example 2: Public vs secret key for a Next.js storefront (developer/automation)
**User**: "I'm building a headless storefront on Next.js. My product list works locally but I'm nervous I'm leaking a key. Which key goes where?"
**Approach**: Use the **public key** with `swell-js` (`swell.init('<store-id>', '<public_key>')`) or GraphQL (`https://<store-id>.swell.store/graphql/v2`, public key in the `Authorization` header) for anything that runs in the **browser** — product lists, cart, account session. Keep the **secret key** strictly in **server code** (route handlers / server actions) with `swell-node` against `https://api.swell.store` for admin reads/writes. If a secret key ever shipped to the client, **revoke and rotate** it in Settings → API.

### Example 3: Migrating active subscribers without double-billing
**User**: "I'm moving ~400 active subscriptions into Swell from another tool. How do I import them so people aren't charged twice or skipped?"
**Approach**: Import each subscription as a **normal record** and **do NOT pass `$migrate: true`** — that flag suppresses the events Swell uses to schedule billing, which corrupts next-charge dates and anchors. Set the existing billing interval, the current period/anchor, and payment method, then verify the computed **next charge date** on a **sandbox** store before running it live. Reconcile against the old system's renewal dates, and watch the first billing cycle closely. (For the cross-platform billing-engine decision, route to `/sales-subscription-billing`.)

## Troubleshooting

### "My webhook fired but the payload doesn't contain the data I need"
Swell payloads are intentionally thin: `{id, date_created, model, type, data}` where `data` includes the record `id` and a subset of fields. Use `data.id` to **GET the full record** from the Backend API (e.g. `swell.get('/orders/{id}')`). Don't rely on the webhook body alone for full order/customer detail.

### "My webhook keeps getting disabled"
Swell retries non-2xx deliveries hourly for ~2 days, then sends warning emails, then **auto-disables** the hook around day 3 (and `auto_disabled` trips after 7 days of failures). Make your handler return **2xx within the 10s timeout** — acknowledge fast and process asynchronously — and confirm your endpoint accepts Swell's allowlisted IPs over HTTPS. Re-enable the hook in **Developer → Webhooks** once fixed.

### "My official-library calls hang or time out"
`swell-node` and `swell-php` use a custom wire protocol on **port 8443** (not 443). If your server/firewall blocks outbound 8443 the calls hang. Open egress to `api.swell.store:8443`, or use the plain REST/GraphQL HTTP interface over 443 instead. Also confirm you're using the **secret** key server-side (a public key will fail or return scoped/empty data on admin endpoints).
