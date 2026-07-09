---
name: sales-checkoutpage
description: "Checkout Page platform help — no-code Stripe-based hosted checkout builder (checkoutpage.com) for digital products, subscriptions, payment plans, pay-what-you-want, and event tickets, with order bumps, 1-click upsells, cart-abandonment recovery, and form/lead capture; a REST API (api.checkoutpage.com/v1, Bearer auth, cursor pagination), conversion webhooks, and a native MCP server for AI assistants. Use when setting up a Checkout Page checkout or event-ticket page, syncing Checkout Page payments or subscriptions into a CRM or warehouse, verifying or backing up the unsigned conversion webhook, building a paid checkout via the Checkout Page MCP, choosing between the Launch and Grow plans or forecasting the sales-volume cap, or troubleshooting Stripe-only limits and owning your own tax (not a Merchant of Record). Do NOT use for checkout-conversion strategy across carts (use /sales-checkout) or picking a Merchant of Record for global tax (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Checkout Page]"
license: MIT
version: 1.0.0
tags: [sales, checkout, payments, ecommerce, platform]
github: "https://github.com/checkout-page"
---

# Checkout Page Platform Help

Checkout Page (checkoutpage.com) is a no-code, **Stripe-based** hosted checkout builder for
creators and small teams: branded checkout pages for digital products, subscriptions, payment
plans, pay-what-you-want, and **event tickets**, plus form/lead capture — with order bumps,
1-click upsells, and cart-abandonment recovery. **0% platform transaction fees**, but it is
**not a Merchant of Record** (runs on your Stripe account → you own tax). Its edge is that forms,
checkout, events, and customers share one **REST API + native MCP server**.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Integrate Checkout Page data (payments/subscriptions/customers) with a CRM, warehouse, or app
   - B) Set up or debug the `conversion` webhook
   - C) Build/query checkouts, forms, or coupons via the native MCP server
   - D) Configure a checkout, event-ticket page, upsell, or form in the product
   - E) Decide on a plan (Launch vs Grow vs Enterprise) or understand fees/caps
2. **Do you have your API key / Stripe connected?** The API key comes from the dashboard; the MCP
   connects via OAuth and needs a Stripe-connected account.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/checkout platform to pick, or checkout-conversion strategy across tools (bump/upsell design, cart abandonment) | `/sales-checkout {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Choosing a Merchant of Record for global tax/VAT (Checkout Page is NOT one) | `/sales-merchant-of-record {question}` |
| Migrating active subscriptions between billing platforms without double-billing | `/sales-subscription-billing {question}` |
| Running an affiliate program (Checkout Page integrates Rewardful/Tolt) | `/sales-affiliate-program {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer Checkout Page-specific questions directly using Step 3.

## Step 3 — Checkout Page platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation
surface (what's API-, webhook-, MCP-accessible vs UI-only), pricing/plan gates and the
sales-volume cap, data model (decimal-string money, Stripe id cross-reference), and quick-start
recipes (webhook listener, nightly incremental pull, MCP event-checkout build).

For raw endpoint detail, auth, pagination, rate limits, verbatim `conversion` webhook payloads,
and MCP tool list, read `references/checkoutpage-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat the webhook as a hint, the API as truth.** Register a **store-level** webhook (fires for
  every page) and **branch on `object`** — `payment`, `subscription`, or `submission` — to route
  each conversion type. The `conversion` payload has **no documented HMAC signature or retry
  policy** — post to a tokenized/unguessable endpoint URL, re-fetch the object by id via the REST
  API before provisioning access or moving money, dedupe on `orderId`, and keep a polling backup.
  Re-check the live docs for a signing scheme before trusting deliveries.
- **Parse money as a decimal string, not cents.** Amounts arrive as `"23.99"` in the display
  currency — unlike SamCart/Sellfy (cents). Read Stripe object ids (`stripePaymentId`,
  `stripeSubscriptionId`, `stripeCustomerId`) straight from the payload to reconcile in Stripe.
- **Say it's not a Merchant of Record.** Checkout Page runs on the user's own Stripe account, so
  **they** are the seller of record and own sales-tax/VAT (Stripe Tax can calculate). For global
  tax handled for them, point to `/sales-merchant-of-record`.
- **Model the sales-volume cap, not features.** ~99% of features are on every plan; plans differ
  mainly by **monthly sales volume**, support, and custom domains — forecast expected sales when
  choosing Launch vs Grow. Present all pricing as best-effort and tell the user to verify current
  numbers at checkoutpage.com/pricing.
- **Reach for the native MCP for build/query tasks.** `claude mcp add --transport http checkoutpage
  https://mcp.checkoutpage.com` then `/mcp` to authenticate — because forms + Stripe checkout share
  one MCP (13 tools), an agent can build a paid event-registration page end-to-end from a prompt.
- **Respect the rate limits.** 500 req/min per store, 100 req/min per key → on `429`, back off and
  resume from the last cursor (`starting_after` = last `id`); keep bulk pulls incremental.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan pricing/caps and the
webhook-signature status, which may have changed.*

- **Conversion webhooks appear unsigned** — no documented HMAC header, signing secret, or retry
  policy. Tokenize the endpoint URL, verify by re-fetching via the API, and keep a polling backup.
- **Money is a decimal string in the display currency** (`"23.99"`), not cents — don't divide by 100.
- **Stripe-only.** Payments run exclusively through Stripe; there's no PayPal/other-gateway option.
  If the user needs an alternate processor, this is a hard limit — flag it early.
- **Not a Merchant of Record** — the seller owns VAT/GST/sales tax (Stripe Tax available).
- **Volume-cap pricing.** Crossing a plan's monthly sales ceiling forces an upgrade; features are
  mostly not gated — forecast sales, not features.
- **`trailStart` is a vendor typo** in the subscription payload (trial start); `trialEnd` is
  spelled correctly. Read fields exactly as sent.
- **Docs are partly JS-rendered** and show both REST (`GET /v1/checkout-pages`) and action
  (`/v1/checkout-pages/list`) path styles — confirm the exact spelling against live docs before coding.

## Related skills

- `/sales-checkout` — Checkout-page strategy and cart-platform selection (Checkout Page vs ThriveCart vs SamCart vs Gumroad; bumps, upsells, cart abandonment)
- `/sales-digital-products` — Digital-product strategy: pricing, validation, launch
- `/sales-merchant-of-record` — Choosing a Merchant of Record for global tax (Checkout Page is not one)
- `/sales-subscription-billing` — Subscription billing engines and migrating active subscribers without double-billing
- `/sales-samcart` — SamCart platform help (the subscription-priced dedicated cart, feature-gated instead of volume-capped)
- `/sales-thrivecart` — ThriveCart platform help (the lifetime-license cart alternative)
- `/sales-affiliate-program` — Affiliate program strategy (Checkout Page integrates Rewardful/Tolt)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync Checkout Page sales into a CRM (developer/automation)
**User says**: "How do I get every Checkout Page sale and subscription into HubSpot automatically?"
**Skill does**: Sets up a **store-level** webhook at a tokenized URL, branches on `object`
(payment/subscription/submission), ignores `livemode:false` in production, and — because the
payload is unsigned — re-fetches the customer/payment by id via `GET /v1/customers/{id}` before
upserting; parses `amount` as a decimal string, maps `queryParameters` UTMs for attribution, and
adds a nightly cursor-paginated `GET /v1/payments` reconciliation pull (per the platform-guide recipes).
**Result**: HubSpot stays in sync with verified data even if an unsigned webhook is missed or spoofed.

### Example 2: Build a paid event-registration page from a prompt (MCP)
**User says**: "Can I make a ticketed workshop checkout with an attendee name and dietary field without clicking around?"
**Skill does**: Walks them through `claude mcp add --transport http checkoutpage https://mcp.checkoutpage.com`
+ `/mcp` OAuth, then prompts the agent to call `create_checkout_page` for the ticket, `create_form`
for the attendee fields, and `create_coupon` for a launch code — noting forms + Stripe checkout
share one MCP so the whole flow runs in chat.
**Result**: A live paid event page with custom fields, built end-to-end from a single prompt.

### Example 3: Launch vs Grow plan decision
**User says**: "I'm doing about $8K/mo in digital sales — is Checkout Page's Launch plan enough or do I need Grow?"
**Skill does**: Flags that Launch caps around ~$3K/mo in sales while $8K/mo lands in a Grow volume
tier, so the cap — not features (which are ~all shared) — forces the choice; notes 0% platform fees
(Stripe's ~2.9%+30¢ still applies) and presents pricing as best-effort to verify at checkoutpage.com/pricing.
**Result**: User picks Grow from their sales volume, not feature FOMO.

## Troubleshooting

### The conversion webhook fired but I don't trust it (or it never arrived)
**Symptom**: Payloads look spoofable, occasionally missing, or contain test data in production.
**Cause**: No documented HMAC signature or retry policy; `livemode:false` events come from the
dashboard "Test payments" tool; there's no documented delivery log.
**Solution**: Put a secret token in the endpoint URL path, verify every payload by re-fetching the
object via the REST API, drop `livemode:false` in prod, return `200` fast, dedupe on `orderId`, and
reconcile nightly with a cursor-paginated `GET /v1/payments` pull.

### 401 Unauthorized on every API call
**Symptom**: All requests fail with 401 even with a key.
**Cause**: Key not sent as a Bearer token, or generated for the wrong store/environment.
**Solution**: Send `Authorization: Bearer YOUR_API_KEY` over HTTPS with a key generated in the
dashboard for the correct store. For the MCP, authenticate via OAuth (`/mcp`) on a Stripe-connected account.

### 429 Too Many Requests on a bulk export
**Symptom**: Large payment/customer pulls start returning 429.
**Cause**: 500 req/min per store, 100 req/min per API key.
**Solution**: Back off on 429 (exponential, start ~1–2s) and resume from the last cursor
(`starting_after` = last object `id`); page at `limit=100`; keep pulls incremental rather than
re-reading history.
