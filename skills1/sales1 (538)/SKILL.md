---
name: sales-snipcart
description: "Snipcart platform help — developer-first embeddable shopping cart for static/JAMstack/custom sites (Hugo, Gatsby, Next.js, Astro, WordPress): define products with data-item-* HTML attributes and Snipcart injects the cart/checkout, validating prices by crawling your product URLs. REST API (app.snipcart.com/api, Basic auth with the secret key as username), webhooks with token-callback validation, a JS SDK, and an official hosted MCP Server for Claude/Cursor. Use when checkout fails with product-crawling-failed or a price-mismatch error, cart items won't add because data-item-id/price/name/url attributes are missing, products on a JS-rendered or headless-CMS page can't be validated, verifying webhooks via the X-Snipcart-RequestToken callback, managing orders/discounts through the MCP server or REST API, or weighing the 2% transaction fee against the flat fee at low volume. Do NOT use for cart-platform selection or checkout strategy (use /sales-checkout) or widget-store platforms like Ecwid (use /sales-ecwid)."
argument-hint: "[describe what you need help with in Snipcart]"
license: MIT
version: 1.0.0
tags: [sales, checkout, ecommerce, platform]
github: "https://github.com/snipcart"
---

# Snipcart Platform Help

Snipcart is a developer-first embeddable cart: a JS snippet plus `data-item-*` buy-button attributes turn any static/JAMstack/custom site into a store. Its signature mechanic — and #1 error class — is **price validation by crawling your product URLs**. Automation runs through a REST API, webhooks with token-callback verification, a JS SDK, and an **official hosted MCP server**.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Add Snipcart to a site (which stack — Hugo/Gatsby/Next/Astro/WordPress/custom?)
   - B) Fix a checkout/validation error (`product-crawling-failed`, price mismatch, missing attributes)
   - C) Integrate orders with a CRM/fulfillment/warehouse (API, webhooks, MCP)
   - D) Understand pricing (2% vs $20/mo minimum) or Test vs Live modes
   - E) Custom shipping/taxes/subscriptions

2. **Is the product page server-rendered?** JS-rendered pages break the price crawler — the fix differs (JSON crawling endpoint vs SSR).

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/commerce platform to pick (Snipcart vs Ecwid/Foxy/Shopify Buy Button/Stripe Checkout) | `/sales-checkout {question}` |
| Widget-store platforms (Ecwid) | `/sales-ecwid {question}` |
| Checkout-conversion strategy across tools | `/sales-checkout {question}` |
| Selling digital downloads strategy | `/sales-digital-products {question}` |
| Tax / Merchant-of-Record obligations | `/sales-merchant-of-record {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer Snipcart-specific questions directly using Step 3.

## Step 3 — Snipcart platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing, data model (products live in your markup), and quick-start recipes (token-validated webhook listener, order pulls, the JSON-crawling-endpoint fix).

For raw auth detail, endpoint groups, webhook mechanics, and the MCP server, read `references/snipcart-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat every `product-crawling-failed` as a crawler-visibility problem**: check, in order — all four mandatory attributes present (`data-item-id/price/name/url`), the `data-item-url` reachable server-side with the exact same price, the domain in the allowed list, and no JS mutating attributes after render. JS-rendered/headless-CMS pages need a **JSON crawling endpoint** (Recipe 3).
- **Auth is Basic with the key as username and an empty password** — not a Bearer header. Test-mode keys see only Test data.
- **Verify webhooks by the token callback**: take `X-Snipcart-RequestToken`, `GET /api/requestvalidation/{token}` — 200 means genuine. There's no HMAC and no documented auto-retry; keep a `GET /api/orders` reconciliation poll and use the dashboard's "Send this hook again" for redelivery.
- **Quote pricing as `max($20/mo, 2% of sales)` plus payment-gateway fees, and flag it best-effort** — tell the user to verify at snipcart.com/pricing; at meaningful volume compare the 2% against flat-fee carts via `/sales-checkout`.
- **Offer the MCP server when the user works in Claude Code/Cursor** — official, hosted (`snipcart-mcp.azurewebsites.net`), authenticated with the private key in the `X-Snipcart-Api-Key` header; ~38 tools for orders/stock/discounts/refunds.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially pricing and MCP client support.*

- **The crawler is the security model.** Snipcart validates cart prices against what it fetches from your `data-item-url` — that's what stops DOM price-tampering. Every convenience that hides products from server-side fetching (SPA rendering, client-side price updates, blocked domains) breaks checkout.
- **All four `data-item-*` attributes are mandatory** (`id`, `price`, `name`, `url`) — items silently refuse to add without them.
- **Webhooks have no HMAC and no documented retries** — token-callback verification + reconciliation polling is the reliable pattern; the dashboard's request history is your redelivery tool.
- **Shipping/tax webhooks are synchronous** — your endpoint's latency sits inside the buyer's checkout; a timeout breaks the purchase.
- **Fee floor**: months under $1,000 in sales cost a flat ~$20 — Snipcart is never free in Live mode. Test mode is free forever.
- **MCP client support needs custom headers** — Claude Desktop/Code, Cursor, Windsurf work; ChatGPT and Claude.ai web don't (no custom-header support).

## Related skills

- `/sales-checkout` — Cart/checkout platform selection (Snipcart vs Ecwid vs Foxy vs Shopify Buy Button) and conversion strategy
- `/sales-ecwid` — Ecwid platform help (the widget-store alternative — hosted storefront UI instead of markup-defined products)
- `/sales-foxy` — Foxy platform help (the signed-links alternative — HMAC-signed cart links instead of crawler validation; hosted checkout pages)
- `/sales-digital-products` — Digital-product strategy (Snipcart delivers digital goods; pricing/launch live here)
- `/sales-merchant-of-record` — Tax/VAT handling (Snipcart automates tax calc but is not a Merchant of Record)
- `/sales-subscription-billing` — Recurring billing strategy across platforms
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Checkout dies with product-crawling-failed (developer/automation)
**User says**: "Orders fail at payment with 'product-crawling-failed' — my products are in Storyblok and the site is client-rendered."
**Skill does**: Explains the crawler-based price validation (Snipcart fetches `data-item-url` server-side, so client-rendered attributes are invisible), and applies Recipe 3: serve a JSON crawling endpoint (static file or serverless function) with matching ids/prices, point `data-item-url` at it, confirm the domain is allowed, and stop mutating attributes with JS.
**Result**: The crawler validates against the JSON endpoint and checkout completes.

### Example 2: Wire orders into fulfillment with verified webhooks
**User says**: "How do I trigger my fulfillment flow when a Snipcart order completes, and make sure the request is really from Snipcart?"
**Skill does**: Sets up the `order.completed` webhook, verifies each request by calling `GET /api/requestvalidation/{X-Snipcart-RequestToken}` with Basic auth (key as username), acts on the event content, returns 200 fast, and adds a paginated `GET /api/orders` reconciliation poll since retries aren't documented — using Recipe 1's Flask listener.
**Result**: Fulfillment fires only on genuine, verified events with a polling safety net.

### Example 3: Is Snipcart the right cost model?
**User says**: "I sell about $8k/month from my Astro site — what does Snipcart actually cost me?"
**Skill does**: Computes `max($20, 2% × $8,000) = $160/mo` plus gateway fees, flags pricing as best-effort with a pointer to snipcart.com/pricing, and notes the crossover logic — at rising volume a flat-fee cart may win, comparing via `/sales-checkout`.
**Result**: User sees the real monthly cost and the volume threshold where the model flips.

## Troubleshooting

### `product-crawling-failed` at checkout
**Symptom**: Payment step fails; dashboard shows a crawling error.
**Cause**: The crawler couldn't fetch the product at `data-item-url`, found a different price, hit a JS-rendered page, or the domain isn't allowed.
**Solution**: Verify the URL returns the product server-side (curl it), match prices exactly, add the domain to allowed domains, and for SPA/headless-CMS pages serve a JSON crawling endpoint (Recipe 3). Never update `data-item-*` values with client-side JS.

### Items won't add to the cart
**Symptom**: Clicking the buy button does nothing or errors.
**Cause**: One of the mandatory attributes (`data-item-id`, `data-item-price`, `data-item-name`, `data-item-url`) is missing or malformed.
**Solution**: Add all four; check the browser console — Snipcart logs which attribute is missing. Keep ids stable across builds.

### API returns 401
**Symptom**: REST calls rejected despite a valid key.
**Cause**: Key sent as a Bearer token instead of Basic-auth username, or a Test key used against Live data (or vice versa).
**Solution**: Send `Authorization: Basic base64("{key}:")` — the key is the *username* with an empty password (`-u KEY:` in cURL). Match key mode to the data mode you're querying.
