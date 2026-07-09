---
name: sales-squarespace
description: "Squarespace platform help — the design-first website builder's ecommerce/online-store backend, automated through the Squarespace Commerce APIs (Orders, Inventory, Products, Transactions, Contacts) plus OAuth-gated webhooks with HMAC-SHA256 signature verification. Use when wiring Squarespace orders, inventory, or customers into a CRM or data warehouse via the API, a Squarespace webhook fails Squarespace-Signature HMAC verification, an order.create webhook won't register (it needs OAuth, not an API key), the Commerce API returns nothing because the site is below the required commerce plan, payments stuck on a Squarespace Payments hold, choosing a Squarespace plan (Basic vs Core vs Plus vs Advanced) or weighing transaction/digital-product fees, or comparing Squarespace vs Shopify/Wix/Square Online for a creative or service business. Do NOT use for cross-tool checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Squarespace]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, checkout, platform]
github: "https://github.com/Squarespace"
---

# Squarespace Platform Help

Squarespace is a design-first, all-in-one website builder with a built-in commerce layer — online store, memberships, digital downloads, gift cards, donations, subscriptions, and (via bundled Acuity Scheduling) bookings. You don't automate the *site builder* (pages/themes are UI-only); you automate the **commerce layer** with the Squarespace **Commerce APIs** (Orders, Inventory, Products, Transactions, Contacts) plus OAuth-gated webhooks. It's **not a Merchant of Record** (you own tax). This skill covers that integration surface and the pain points — the commerce-plan API gate, OAuth-only webhooks, HMAC verification, Squarespace Payments holds — that trip people up.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you need (skip if the prompt already says):

1. **What's the goal?** (a) automate/integrate via the API or webhooks, (b) fix a store/payments/inventory problem, (c) pick a Squarespace plan or weigh fees, (d) compare Squarespace vs another platform.
2. **Build context** — automating your *own* site (an **API key** works, OAuth for webhooks) or a third-party app across *other* sites (**OAuth**)? Which objects — orders, products, inventory, transactions, contacts?
3. **What plan is the site on?** Commerce APIs require a paid commerce plan; a personal/Basic plan has no API.

Skip-ahead rule: if the user's prompt already contains enough context, go straight to Step 2.

## Step 2 — Route or answer directly

Map the request to the right home. When routing, give the exact command.

| The user's real problem | Route to |
|---|---|
| Checkout-conversion strategy across tools (order bumps, AOV, cart abandonment tactics) | `/sales-checkout {question}` |
| Migrating a store off (or onto) Squarespace — data export, redirects, SEO | `/sales-checkout {question}` (migration mechanics) |
| Choosing a Merchant of Record for global tax / VAT instead | `/sales-merchant-of-record {question}` |
| Memberships / paid gated-content strategy across tools | `/sales-membership {question}` |
| Selling digital downloads strategy across tools | `/sales-digital-products {question}` |
| Appointment booking strategy (Acuity is a separate product) | `/sales-meeting-scheduler {question}` |
| General website / landing-page / funnel strategy | `/sales-funnel {question}` |
| Post-purchase / abandoned-cart email sequences | `/sales-email-marketing {question}` |
| Not sure which skill | `/sales-do {question}` |

Anything Squarespace-specific (Commerce APIs, webhooks, plan gates, payments holds) — answer here using Step 3.

## Step 3 — Squarespace platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities & automation surface, pricing/plan gates, the data model with JSON shapes, integration recipes (cURL + Python), and integration patterns.

For raw API detail (endpoints, request/response JSON, auth headers, webhook HMAC verification), read `references/squarespace-api-reference.md`.

Answer using only the relevant section — don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide loaded — focus on the user's situation:

- **Integration:** Own site → an **API key** (Bearer) for reads/writes; **OAuth** is *required* to register webhooks and for multi-site apps. Always send a **custom `User-Agent`** (a default one draws stricter rate limiting) and `Content-Type: application/json` on writes. Base URL `https://api.squarespace.com/{version}/{path}` — versions are per-endpoint (Orders `1.0`, Products `2`). HTTPS only.
- **Real-time vs polling:** For purchase-driven automation prefer the `order.create`/`order.update` **webhook**, but its payload is thin — verify the HMAC, then **GET the full order**. If you can't host a listener or you're API-key-only, poll `GET /commerce/orders` with paired `modifiedAfter`+`modifiedBefore`.
- **Plan/fee math:** Commerce APIs, abandoned-cart recovery, and subscriptions need a paid commerce plan (Core+ / Advanced). Transaction fees drop by tier (Basic 2% → Core/Plus/Advanced 0%; digital-product fee 7%→5%→1%→0%). Do the break-even before recommending a tier; flag pricing as best-effort.
- **Don't promise page edits:** the site builder is UI-only — there's no site-builder API. Automate commerce objects, not pages/themes.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

- **The Commerce API is plan-gated — the #1 trap.** No API on a free trial or personal/Basic plan. Docs list Orders/Inventory on **Core/Plus/Advanced/Commerce Advanced**; some reviews say **Advanced ($99/mo) only**. Confirm the site's plan before promising an integration.
- **Webhooks require OAuth, not an API key.** An API key can read/write and *poll* orders, but only an OAuth app can create webhook subscriptions. This is the usual "why won't my webhook register" cause.
- **Thin webhook payloads.** `data` carries an `orderId`, not the order — make a follow-up `GET /commerce/orders/{id}`. Dedupe on `order.id`; retries duplicate.
- **HMAC secret is hex — decode it to bytes.** Verify `Squarespace-Signature` as HMAC-SHA256 over the **raw** body using `hexToBytes(secret)`. Using the hex string directly, or hashing a re-serialized body, fails.
- **Money is a `{currency, value}` decimal object, not integer cents** (unlike Square/Sellfy). Don't divide by 100.
- **`modifiedAfter`/`modifiedBefore` are paired and mutually exclusive with `cursor`** — date window on the first page, cursor-only after.
- **Donations bypass the Orders API** — read them via the **Transactions API**.
- **Squarespace Payments holds** are a recurring complaint with slow support — don't rely on a single processor for a time-sensitive launch.
- **No multi-currency** and a limited gateway set (Squarespace Payments / Stripe / PayPal). **Not a Merchant of Record** — you own tax (US auto-calc via TaxJar).

## Related skills

- `/sales-checkout` — Cross-tool checkout-conversion strategy, order bumps, AOV, and cart-abandonment tactics (Squarespace is one platform among Shopify/BigCommerce/Wix/Square Online/Medusa).
- `/sales-square-online` — Square Online, the other free-to-start website-builder-plus-store (and the closest API analog — shared-catalog commerce backend, HMAC webhooks).
- `/sales-wix` — Wix eCommerce, the other no-code website-builder-plus-store option.
- `/sales-shopify` — Shopify commerce backend (GraphQL Admin API), the scale-oriented alternative for product-heavy stores.
- `/sales-merchant-of-record` — Choosing a MoR (Paddle/Lemon Squeezy) for global VAT/GST vs owning tax yourself.
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Sync every new Squarespace order into my CRM"
A developer/automation question. Recommend the **`order.create`** webhook over polling, but note Squarespace webhooks need **OAuth** (an API key can't subscribe). Walk through: register the subscription (store the one-time hex `secret`), verify the **HMAC-SHA256** signature in the **`Squarespace-Signature`** header over the **raw** body using `hexToBytes(secret)`, then `GET /1.0/commerce/orders/{orderId}` (the payload is just a pointer), and upsert deduping on `order.id`. If they can't host a listener, show the `modifiedAfter`/`modifiedBefore` polling loop instead. Point to `references/squarespace-api-reference.md` for the JSON + verification code.

### Example 2: "My Commerce API calls return nothing / 'not available on your plan'"
The top integration trap. Explain the Commerce APIs are **plan-gated** — no API on a free trial or personal/Basic plan; you need a paid commerce plan (Squarespace docs say Core/Plus/Advanced/Commerce Advanced, some reviews say Advanced-only). Have them confirm the site's plan and that the API key has the right permission scopes, and that they're hitting `https://api.squarespace.com/1.0/commerce/orders` over HTTPS with `Authorization: Bearer` + a **custom `User-Agent`**. Flag the plan ambiguity as best-effort and tell them to verify against current docs.

### Example 3: "Basic vs Core vs Plus vs Advanced — which plan, and what are the fees?"
Pricing/plan-gate question (answer from the guide). Walk the tiers (best-effort 2026): **Basic ~$16** has a **2% commerce fee + 7% digital fee** and no Commerce API; **Core ~$23** removes the commerce fee (5% digital); **Plus ~$39** (1% digital, lower processing); **Advanced ~$99** (0%/0%, plus **abandoned-cart recovery, subscriptions, advanced shipping, Commerce APIs**). Do the break-even on the fee deltas vs the monthly jump, and note no multi-currency and limited gateways. Flag all pricing as best-effort and tell them to confirm current rates.

## Troubleshooting

### "My webhook won't register / I get nothing on order events"
Two causes. **(1) Auth:** the Webhook Subscriptions API is **OAuth-only** — you can't create a subscription with an API key. Register an OAuth app, authorize scopes matching your topics (`order.create`/`order.update`), then `POST /1.0/webhook_subscriptions`. **(2) Plan/verification:** confirm the site is on an API-eligible commerce plan and that your listener returns 2xx fast over **HTTPS**. Use the "Send test notification" endpoint to validate. If you only need your own site and can't do OAuth, poll `GET /commerce/orders?modifiedAfter=…&modifiedBefore=…` instead.

### "My webhook signature verification keeps failing"
`Squarespace-Signature` is **HMAC-SHA256 over the raw request body**, keyed by the subscription **`secret`** — which is **hex-encoded and must be decoded to raw bytes** first. Common mistakes: using the hex string directly as the key, hashing a parsed/re-serialized JSON object instead of the raw bytes, or comparing non-constant-time. Capture the raw body before any JSON parsing, do `HMAC-SHA256(hexToBytes(secret), rawBody)`, hex-encode, and `timingSafeEqual`/`compare_digest`. If it still fails, rotate the secret (returns a new one once) and re-store it.

### "Payments are stuck on a Squarespace Payments hold"
A documented, recurring complaint (Trustpilot/Reddit/BBB) with slow support resolution. Holds are a risk-review on the **Squarespace Payments** processor — there's no API to release them; you contact support and provide requested verification. Mitigations: don't run a time-sensitive launch on a brand-new Squarespace Payments account, keep a fallback gateway (Stripe/PayPal) connected, and reconcile payouts via the **Transactions API** so you can see what's actually settled vs held.
