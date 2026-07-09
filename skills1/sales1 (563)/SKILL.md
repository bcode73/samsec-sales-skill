---
name: sales-square-online
description: "Square Online platform help — the free-to-start online store in the Square ecosystem, automated through the Square commerce APIs (Catalog, Orders, Inventory, Payments/Checkout) that also power Square POS, plus HMAC-signed webhooks, OAuth, and an official MCP server. Use when Square Online inventory won't sync with POS or items oversell, wiring Square orders or catalog into a CRM or data warehouse via the API, a Square webhook fails HMAC signature verification, your Square OAuth token expired after 30 days, choosing a Square Online plan (Free vs Plus vs Premium) or weighing the 3.3%+30¢ online fee against upgrading, setting up the Square MCP server in Claude or Cursor, or comparing Square Online vs Shopify/Wix/Squarespace/Ecwid for a retail-plus-online seller. Do NOT use for cross-tool checkout-conversion strategy (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Square Online]"
license: MIT
version: 1.0.0
tags: [sales, ecommerce, checkout, platform]
github: "https://github.com/square"
---

# Square Online Platform Help

Square Online is the online store inside the Square ecosystem — a free-to-start storefront that shares one catalog, inventory, customer directory, and order book with Square POS. You don't automate the *site builder* (that's UI-only); you automate the **commerce layer** with the standard Square APIs (Catalog, Orders, Inventory, Payments/Checkout) plus webhooks, OAuth, and the official Square MCP server. This skill covers that integration surface and the pain points — POS↔online inventory sync, processing-fee math, plan gates — that trip people up.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you need (skip if the prompt already says):

1. **What's the goal?** (a) automate/integrate via the API or webhooks, (b) fix an inventory/POS-sync or store problem, (c) pick a Square Online plan or weigh fees vs upgrading, (d) compare Square Online vs another store builder, (e) set up the Square MCP server.
2. **Build context** — automating your own account (personal access token) or a multi-merchant app (OAuth)? Which objects matter — catalog items, orders, inventory counts, customers, payments?
3. **Sandbox or production?** Square has a full sandbox at `connect.squareupsandbox.com`.

Skip-ahead rule: if the user's prompt already contains enough context, go straight to Step 2.

## Step 2 — Route or answer directly

Map the request to the right home. When routing, give the exact command.

| The user's real problem | Route to |
|---|---|
| Checkout-conversion strategy across tools (order bumps, AOV, cart abandonment tactics) | `/sales-checkout {question}` |
| Migrating a store off (or onto) Square Online — data export, redirects | `/sales-checkout {question}` (migration mechanics) |
| Choosing a Merchant of Record for global tax instead | `/sales-merchant-of-record {question}` |
| General website / landing-page / funnel strategy | `/sales-funnel {question}` |
| Post-purchase / abandoned-cart email sequences | `/sales-email-marketing {question}` |
| Not sure which skill | `/sales-do {question}` |

Anything Square-specific (API, webhooks, inventory sync, plan gates, MCP) — answer here using Step 3.

## Step 3 — Square Online platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities & automation surface, pricing/plan gates, the data model with JSON shapes, integration recipes (cURL + Python), and integration patterns.

For raw API detail (endpoints, request/response JSON, auth headers, webhook HMAC verification, MCP setup), read `references/square-online-api-reference.md`.

Answer using only the relevant section — don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide loaded — focus on the user's situation:

- **Integration:** Own account → **personal access token** (Bearer). Multi-merchant app → **OAuth** (tokens expire in **30 days** — refresh them). Always send `Square-Version: YYYY-MM-DD`. Base URL `https://connect.squareup.com/v2` (sandbox `connect.squareupsandbox.com`). For purchase-driven automation, prefer **webhooks** over polling; verify the HMAC and follow up with a GET.
- **Inventory:** Treat the **Inventory API** as the source of truth, not the UI sync toggle. Enable stock tracking per item variation, react to `inventory.count.updated`, and reconcile counts on a schedule to prevent overselling.
- **Plan/fee math:** Free has **no monthly fee but a higher online rate (~3.3% + 30¢)**; Plus/Premium lower the rate and unlock custom domain, abandoned-cart emails, and advanced features. Above a few thousand dollars/month in online sales, the lower rate can pay for the subscription — do the break-even.
- **Builder limits:** The storefront design and pages are UI-only (Weebly heritage) — there is no site-builder API. Don't promise programmatic page edits.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

- **Inventory sync lag → overselling is the #1 complaint.** Online stock can fail to decrement after an online order, items show "sold out" when in stock, and the per-item sync toggle silently turns off. Don't trust the UI toggle — drive stock from the **Inventory API** and reconcile via `inventory.count.updated`.
- **No Square Online site-builder API.** You automate catalog/orders/inventory/payments, not the storefront pages/theme. The site itself is UI-only.
- **Free plan = higher online fee + branding.** ~**3.3% + 30¢** online on Free, a `*.square.site` subdomain, and Square ads; custom domain and ad removal need **Plus+**.
- **OAuth access tokens expire after 30 days.** Long-lived integrations break unless you refresh with the refresh token. Personal access tokens (own account) don't expire the same way.
- **Webhook HMAC is computed over notification URL + raw body.** A trailing slash, http-vs-https mismatch, or re-serialized body fails verification. Use the SDK `WebhooksHelper`; signature header is `x-square-hmacsha256-signature`.
- **API-created orders need fulfillment + payment to show in the Dashboard.** A bare order won't appear until it has a fulfillment and a completed payment.
- **Tax auto-calc is US/Canada only.** Selling elsewhere means manual tax setup or an external tax tool.
- **Rate limits aren't published.** Expect `429 RATE_LIMITED` under load — retry with exponential backoff + jitter.

## Related skills

- `/sales-checkout` — Cross-tool checkout-conversion strategy, order bumps, AOV, and cart-abandonment tactics (Square Online is one platform among Shopify/BigCommerce/Wix/Medusa).
- `/sales-shopify` — Shopify commerce backend (GraphQL Admin API, HMAC webhooks) — the scale-oriented alternative.
- `/sales-wix` — Wix eCommerce, the other no-code website-builder-plus-store option.
- `/sales-merchant-of-record` — Choosing a MoR (Paddle/Lemon Squeezy) for global tax vs owning tax yourself.
- `/sales-email-marketing` — Post-purchase and abandoned-cart email sequences.
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: "Sync every new Square Online order into my CRM"
A developer/automation question. Recommend a **webhook** (`order.created` / `order.updated`, plus `payment.created` if you need paid confirmation) over polling. Walk through: subscribe in the Developer Dashboard, verify the **HMAC-SHA256** signature (`x-square-hmacsha256-signature`) over the notification URL + raw body with the subscription signature key, then GET the full order from `POST /v2/orders/search` or RetrieveOrder. Show the Bearer + `Square-Version` headers, dedupe on the event/order ID, and return 2xx fast. Point to `references/square-online-api-reference.md` for the JSON.

### Example 2: "My online store keeps overselling — stock doesn't match the POS"
The top Square Online pain point. Explain that Square Online and POS share one catalog but the UI sync can lag or the per-item tracking toggle flips off. Fix: enable inventory tracking per **item variation**, treat the **Inventory API** (`BatchRetrieveInventoryCounts`) as source of truth, subscribe to `inventory.count.updated` to catch changes in real time, and run a scheduled reconciliation. If a count is wrong, push a `BatchChangeInventory` adjustment rather than fixing it by hand each sale.

### Example 3: "Free vs Plus vs Premium — and is the free plan actually free?"
Pricing/plan-gate question (answer from the guide). Free is $0/mo but charges a **higher online processing rate (~3.3% + 30¢)**, uses a `*.square.site` subdomain, and shows Square ads. **Plus (~$49/mo)** adds a custom domain, ad removal, and abandoned-cart emails; **Premium (~$149/mo)** lowers fees further and adds real-time shipping rates + advanced reporting. Do the break-even: subscription cost ÷ (fee delta) = the monthly online sales where upgrading pays off. Flag all pricing as best-effort and tell them to confirm current rates.

## Troubleshooting

### "Inventory isn't syncing between POS and my online store / items oversell"
Square Online and POS read from one shared catalog, but sync glitches are common: online orders not decrementing stock, items stuck "sold out," sync toggles turning themselves off, and 24h+ delays. Don't rely on the dashboard toggle. Confirm **inventory tracking is on per variation**, use `BatchRetrieveInventoryCounts` as the truth, subscribe to `inventory.count.updated`, and reconcile on a schedule. For a known-bad count, post a `BatchChangeInventory` physical-count adjustment. If sync is system-wide broken, it's usually a Square-side bug — log it with support and rely on the API in the meantime.

### "My webhook signature verification keeps failing"
The HMAC-SHA256 is generated over the **notification URL string concatenated with the raw request body**, signed with that subscription's signature key — not the body alone. The most common causes: hashing a re-serialized/parsed body instead of the raw bytes, a notification URL mismatch (trailing slash, http vs https, wrong path), or using the wrong subscription's key. Use the official SDK `WebhooksHelper.verifySignature` (Node/Python/PHP/Ruby), pass the exact configured notification URL, and compare with a constant-time function. Header name is `x-square-hmacsha256-signature`.

### "I'm getting 401 Unauthorized after my integration worked for weeks"
OAuth **access tokens expire after 30 days**. If you stored a token and stopped refreshing, it's now dead — exchange the **refresh token** for a new access token (`POST /oauth2/token` with `grant_type=refresh_token`) and store the new pair. Other 401 causes: missing/short token, calling production with a sandbox token (or vice versa), or a scope you didn't request at authorization. For your own single account, a non-expiring **personal access token** from the Developer Dashboard avoids the refresh dance.
