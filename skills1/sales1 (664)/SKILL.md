---
name: sales-wix
description: "Wix eCommerce (Wix Stores) platform help — the native online store inside the Wix website builder, with REST APIs (Stores v3 + eCommerce Orders), API-key/OAuth auth, and signed-JWT webhooks. Use when wiring Wix orders or products into a CRM or data warehouse via the API, verifying a signed-JWT Wix webhook, a Wix store loads slowly or hurts SEO, you're locked into a template after publishing, abandoned-cart recovery or advanced merchandising is gated above your plan, choosing a Wix plan for ecommerce (Light vs Core vs Business), or weighing Wix vs Shopify/BigCommerce/Squarespace/Ecwid for a small store. Covers products/variants/inventory, custom checkout (Wix Payments or Stripe), subscriptions, dropshipping, multichannel selling, the @wix/sdk, and the Wix MCP server. Do NOT use for cross-tool checkout-conversion strategy (use /sales-checkout) or general website/funnel strategy (use /sales-funnel)."
argument-hint: "[describe what you need help with in Wix eCommerce]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, checkout, platform]
github: "https://github.com/wix"
---

# Wix eCommerce Platform Help

Wix eCommerce (Wix Stores) is the commerce layer built into the Wix website builder — an easy-setup Shopify/BigCommerce alternative for small stores and solopreneurs. This skill covers running and automating a Wix store: the Stores and eCommerce REST APIs, webhooks, plan gates, and the pain points (SEO/performance, template lock-in, paywalled features) that trip people up.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you need (skip if the prompt already says):

1. **What's the goal?** (a) automate/integrate via the API or webhooks, (b) fix a store/SEO/performance problem, (c) pick a Wix plan or compare Wix vs another platform, (d) configure a store feature (checkout, subscriptions, dropshipping, multichannel).
2. **Build context** — self-managed/headless (API keys) or a 3rd-party Wix app (OAuth)? Which objects matter — products, orders, inventory, abandoned carts?
3. **Plan** — Light, Core, Business, or Business Elite? (eCommerce needs **Core or higher**.)

Skip-ahead rule: if the user's prompt already contains enough context, go straight to Step 2.

## Step 2 — Route or answer directly

Map the request to the right home. When routing, give the exact command.

| The user's real problem | Route to |
|---|---|
| Checkout-conversion strategy across tools (order bumps, AOV, cart abandonment tactics) | `/sales-checkout {question}` |
| General website / landing-page / funnel strategy | `/sales-funnel {question}` |
| Migrating a store off (or onto) Wix — data export, redirects | `/sales-checkout {question}` (migration mechanics) |
| Choosing a Merchant of Record for global tax instead | `/sales-merchant-of-record {question}` |
| SEO strategy / Core Web Vitals / technical audit | `/sales-seo {question}` |
| Post-purchase email / abandoned-cart email sequences | `/sales-email-marketing {question}` |
| Not sure which skill | `/sales-do {question}` |

Anything Wix-specific (API, webhooks, plan gates, store features) — answer here using Step 3.

## Step 3 — Wix platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities & automation surface, pricing/plan gates, the data model with JSON shapes, integration recipes (cURL + Python), and integration patterns.

For raw API detail (endpoints, request/response JSON, auth headers, webhook JWT verification), read `references/wix-api-reference.md`.

Answer using only the relevant section — don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide loaded — focus on the user's situation:

- **Integration:** Self-managed/headless → **API key** (`Authorization` + `wix-site-id`). 3rd-party app → **OAuth**. For purchase-driven automation, prefer **webhooks** (signed JWT) over polling; always make a follow-up GET because some payloads are partial. Dedupe on event/entity ID and return 200 within 1250 ms.
- **Plan choice:** eCommerce is gated to **Core ($29/mo) or higher** — Light won't sell. Advanced shipping + automated tax are **Business+**. Confirm the feature you need isn't paywalled before committing.
- **SEO/performance:** Wix is JS-heavy; if rankings/Core Web Vitals are the bottleneck at scale, that's a `/sales-seo` (or migration) decision, not a settings toggle.
- **Lock-in:** Changing template after publishing can lose content, and there's no clean export of a working storefront — design for that before you scale.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

- **eCommerce is plan-gated** — selling needs **Core or higher**; the Light plan can't run a store. Advanced shipping and automated sales tax are **Business+**.
- **Template lock-in** — you generally can't switch templates after publishing without rebuilding/losing content. Pick the template carefully up front.
- **JS-heavy → SEO/perf risk** — Wix sites lean on JavaScript; slower loads (esp. mobile) can hurt Core Web Vitals and rankings. Strong enough for small/simple stores, weaker at scale.
- **Walled garden / no clean export** — you don't own the code and there's no clean export of a working storefront; budget for migration pain if you outgrow Wix.
- **Webhooks are signed JWTs, not raw JSON** — verify with your app's **public key** from the Webhooks page; payloads can be partial (follow up with a GET); handle **duplicate and out-of-order** events and respond 200 within **1250 ms** or Wix retries up to 12 times.
- **API keys vs OAuth** — API keys are for self-managed/headless and CLI/n8n; **3rd-party Wix apps must use OAuth** (keys aren't available to them). Site-level calls need the `wix-site-id` header; a missing header or wrong scope returns **403**.
- **Products v3 query omits variants** — Query Products doesn't return variant data; use Get Product / the Variants API. Only a narrow set of fields is filterable/sortable (unsupported fields error out).

## Related skills

- `/sales-checkout` — Cross-tool checkout-conversion strategy, order bumps, AOV, and cart-abandonment tactics (Wix is one platform among Shopify/BigCommerce/Medusa).
- `/sales-funnel` — Website, landing-page, and funnel strategy across builders.
- `/sales-merchant-of-record` — Choosing a MoR (Paddle/Lemon Squeezy) for global tax vs owning tax yourself.
- `/sales-seo` — SEO strategy, technical audits, and Core Web Vitals.
- `/sales-email-marketing` — Post-purchase and abandoned-cart email sequences.
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Sync every new Wix order into my CRM"
A developer/automation question. Recommend a **webhook** (Order Approved / Order Updated) over polling. Walk through: register the webhook in the Wix Developers Center, verify the signed **JWT** with the app public key, read `eventType` + `instanceId`, then GET the full order from `POST /ecom/v1/orders/search` or Get Order (payloads can be partial). Show the API-key headers (`Authorization` + `wix-site-id`), dedupe on event ID, and return 200 within 1250 ms. Point to `references/wix-api-reference.md` for the JSON.

### Example 2: "My Wix store is slow and not ranking — should I stay on Wix?"
Upstream SEO/performance pain. Explain Wix's JS-heavy rendering and Core Web Vitals impact, the small-store-vs-scale tradeoff, and template lock-in / no clean export. For the technical-SEO playbook route to `/sales-seo`; if they're weighing a move, the migration mechanics live in `/sales-checkout`. Be honest that some limits are structural, not a settings toggle.

### Example 3: "Which Wix plan do I need to sell products, and what's gated?"
Pricing/plan-gate question (answer from the guide). eCommerce starts at **Core ($29/mo)**; Light can't sell. **Business ($39/mo)** adds advanced shipping + automated tax; **Business Elite ($159/mo)** raises dropshipping/review limits. Flag pricing as best-effort and tell them to confirm the specific feature isn't paywalled before subscribing.

## Troubleshooting

### "My Wix webhook fires but the data is incomplete / I can't trust it"
Wix sends event data as a **signed JWT**, and some (especially legacy) events return only changed fields. Verify the JWT with your app's public key, then make a **follow-up GET** to the entity endpoint for the full object. Store processed event IDs and skip duplicates — copies can arrive more than once and out of order. Respond 200 within **1250 ms** or you'll get up to 12 retries.

### "My store changes broke SEO / pages load slowly"
Wix's heavy client-side JavaScript slows first paint, especially on mobile, which feeds Core Web Vitals and rankings. Tighten images/apps, but accept that hosted-builder overhead caps how fast you can get. If rankings are business-critical at scale, treat it as an SEO-or-migration decision (`/sales-seo`, then `/sales-checkout` migration), not a single fix.

### "I'm getting 403 Forbidden on the API"
Check: (1) `Authorization` header carries a valid **API key**; (2) you sent `wix-site-id` for site-level calls (or `wix-account-id` for account-level) — **one or the other, not both**; (3) the key has the right **permission scope** (e.g. `SCOPE.STORES.PRODUCT_READ`, `SCOPE.DC-STORES.READ-ORDERS`); (4) the key was created by the account **owner** and is scoped to the site you're calling. 3rd-party apps can't use API keys at all — use **OAuth**.
