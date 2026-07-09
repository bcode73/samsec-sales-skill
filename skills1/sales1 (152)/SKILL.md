---
name: sales-dodo-payments
description: "Dodo Payments (dodopayments.com) platform help — developer-first Merchant of Record (MoR) for SaaS, AI, and digital products: sells on your behalf and handles global sales tax/VAT/GST across 220+ countries / 40+ payment methods, with subscriptions, usage/credit billing, one-time payments, embeddable checkout, and license keys. Full REST API (test/live.dodopayments.com, Bearer key) for payments/subscriptions/products/customers/checkout/license-keys/refunds/payouts, Standard-Webhooks-signed events, 9 SDKs, framework adapters, a CLI, and an MCP server. Per-transaction MoR fee, no monthly fee. Use when integrating payments/subscriptions via the API or SDK, verifying webhooks with the standardwebhooks library, choosing MoR vs a payment processor, handling tax/VAT as MoR, or issuing license keys. Do NOT use for merchant-of-record selection across vendors (use /sales-merchant-of-record), checkout-conversion strategy (use /sales-checkout), or general digital-product strategy (use /sales-digital-products)."
argument-hint: "[describe what you need help with in Dodo Payments]"
license: MIT
version: 1.0.1
tags: [sales, payments, merchant-of-record, platform]
github: "https://github.com/dodopayments"
---

# Dodo Payments Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Take a payment / create a subscription via the REST API or an SDK
   - B) Build checkout — hosted Checkout Session, embeddable checkout, or a framework adapter
   - C) Verify webhooks (Standard Webhooks) and react to payment/subscription events
   - D) Sell digital products — license keys, entitlements, digital delivery
   - E) Handle MoR concerns — tax/VAT/GST, refunds, disputes, payouts
   - F) Decide MoR (Dodo) vs a raw payment processor, or compare to Paddle/Lemon Squeezy

2. **API/SDK or no-code?** Code → REST API + a language SDK / framework adapter. Low-code → hosted Checkout Sessions + short links.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| **Choosing** a Merchant of Record across vendors (Paddle/Lemon Squeezy/Polar/Creem/Dodo) | `/sales-merchant-of-record {question}` |
| Checkout/cart **conversion** strategy across platforms | `/sales-checkout {question}` |
| General **digital-product** selling strategy across tools | `/sales-digital-products {question}` |
| Generic iPaaS wiring to a CRM/ESP | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a selection question — run: `/sales-merchant-of-record MoR vs Stripe for a global SaaS`".

## Step 3 — Dodo Payments platform reference

**Read `references/platform-guide.md`** for the full reference — the MoR model (what Dodo takes liability for), the billing models (subscriptions/usage/credit/one-time), the object map (what's API vs hosted vs SDK), pricing, and quick-start recipes (create a payment; verify a webhook; spin up a checkout session).

**Read `references/dodo-payments-api-reference.md`** for the integration surface — base `test/live.dodopayments.com`, **Bearer** auth (Developer → API Keys, read-only/read-write), tiered rate limits, the endpoint catalog (payments, subscriptions, products, customers, **checkout sessions**, **license keys/entitlements**, discounts, refunds, disputes, payouts, webhooks management), **Standard Webhooks** signing (`webhook-id`/`webhook-signature`/`webhook-timestamp` via the `standardwebhooks` library), the 9 SDKs + framework adapters + **MCP server** + CLI.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **MoR = Dodo handles tax liability.** Dodo is the seller of record and **remits global sales tax/VAT/GST** — you don't register/file in each jurisdiction. That's the core reason to pick it over a raw processor (Stripe), at a higher fee (~4% + $0.40 vs ~2.9% + 30¢).
- **Use the SDK / framework adapter, not raw HTTP, when you can.** Official SDKs (TS/Python/Go/PHP/Java/Kotlin/C#/Ruby/React Native) + adapters (Next.js/Express/Hono/SvelteKit/…) wrap checkout + webhook verification — far less to get wrong.
- **Verify webhooks with `standardwebhooks`.** Events are signed per the **Standard Webhooks** spec (`webhook-id`/`webhook-signature`/`webhook-timestamp`). Use the library (don't hand-roll HMAC); get the signing key from the dashboard or `GET /webhooks/{id}/signing-key`.
- **Test mode is first-class.** Use a `test.dodopayments.com` key + the **Dodo CLI** (`dodo wh trigger`) to forward events locally. CLI mocks are **unsigned** → use `unsafe_unwrap()` in tests only, never in prod.
- **Sell software via license keys + entitlements.** Dodo issues/activates/deactivates license keys and handles digital delivery — wire activation to the license + entitlement endpoints.
- **There's an MCP server.** For AI agents, Dodo exposes an MCP server (and "Agent Skills") — a first-class programmatic surface, not just REST.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API/pricing verified against docs.dodopayments.com; confirm current terms in-account.*

1. **MoR fee is higher than a processor.** ~**4% + $0.40/txn** (no monthly) — you pay for tax handling/remittance. If you don't want MoR, a raw processor is cheaper; decide via `/sales-merchant-of-record`.
2. **Two hosts, two keys.** `test.dodopayments.com` (test key) vs `live.dodopayments.com` (live key) — mixing host + key mode 401s.
3. **Webhooks use Standard Webhooks — verify with the library.** Headers are `webhook-id`/`webhook-signature`/`webhook-timestamp`; the `standardwebhooks` lib checks signature + timestamp (replay). Hand-rolled checks are the common bug.
4. **CLI mock payloads are unsigned.** `dodo wh trigger` mocks aren't signed — `unsafe_unwrap()` is test-only; production must verify.
5. **Confirm exact webhook event names.** Switch on event types from the Webhooks doc, not guesses (payment/subscription/refund/dispute/license lifecycle).
6. **Rate limits are tiered + dual-window.** Default 40/sec + 240/min; read `X-RateLimit-*`, back off on `429`.
7. **MoR ≠ instant payouts.** As seller of record, Dodo pays you out on a schedule (see Payouts endpoints) — model cash flow accordingly.

## Related skills

- `/sales-merchant-of-record` — Choosing a Merchant of Record across vendors (Dodo vs Paddle/Lemon Squeezy/Polar/Creem/Gumroad vs Stripe+Tax) — selection strategy, MoR-vs-processor tradeoffs
- `/sales-checkout` — Checkout/cart conversion strategy (order bumps, upsells, AOV) across platforms
- `/sales-digital-products` — Selling digital products (license keys, delivery, pricing) across tools
- `/sales-integration` — Wiring Dodo events into a CRM/ESP via webhooks/Zapier
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Take a one-time payment / subscription via the API (developer/automation)
**User says**: "How do I charge for my SaaS subscription with Dodo Payments from my backend?"
**Skill does**: Points to the official **SDK** (or `POST /subscriptions` / `POST /payments` against `live.dodopayments.com` with `Authorization: Bearer`), or a **hosted Checkout Session** (`POST /checkouts`) / framework adapter (Next.js/Express) for the front end. Stresses verifying the **subscription.* webhooks** with the `standardwebhooks` library to provision access, and that Dodo (MoR) handles the **tax** on the charge. Notes test-mode key + CLI for local dev.
**Result**: A working subscription charge with reliable event-driven provisioning.

### Example 2: Verify a Dodo webhook so I can trust it
**User says**: "Dodo is POSTing events to my endpoint — how do I verify them?"
**Skill does**: Explains events follow **Standard Webhooks**: headers `webhook-id`, `webhook-signature`, `webhook-timestamp`; verify with the **`standardwebhooks`** library using the **signing key** (dashboard or `GET /webhooks/{id}/signing-key`), which checks the signature and timestamp (replay protection). Recommends a framework adapter (which wraps this), deduping on `webhook-id`, and `dodo wh trigger` for local testing (mocks unsigned → `unsafe_unwrap()` in tests only).
**Result**: Authenticated, replay-safe webhook intake.

### Example 3: MoR vs Stripe — should I use Dodo?
**User says**: "I'm a solo dev selling a global SaaS. Dodo Payments or Stripe?"
**Skill does**: Frames the **Merchant-of-Record** tradeoff — Dodo becomes seller of record and **remits VAT/GST/sales tax** worldwide (no per-country tax registration), at ~**4% + $0.40** vs Stripe's ~2.9% + 30¢ (where you own tax compliance, even with Stripe Tax which calculates but doesn't remit). Recommends Dodo when global tax compliance overhead outweighs the fee, and routes the cross-vendor decision: "run: `/sales-merchant-of-record Dodo vs Paddle vs Lemon Squeezy for indie SaaS`."
**Result**: A clear MoR-vs-processor decision grounded in tax liability + fees.

## Troubleshooting

### My API calls return 401
**Symptom**: Requests to `*.dodopayments.com` are rejected.
**Cause**: Wrong host/key mode (test key against `live.` or vice-versa), a missing `Authorization: Bearer` header, or a read-only key used for a write.
**Solution**: Match host to key — **`test.dodopayments.com` + test key**, `live.dodopayments.com` + live key. Send `Authorization: Bearer YOUR_API_KEY`, and use a **read-write** key for create/update. Keys come from Developer → API Keys.

### My webhook signature verification fails
**Symptom**: Events arrive but verification rejects them.
**Cause**: Hand-rolled verification, wrong signing key, or verifying a re-serialized body — Dodo uses the **Standard Webhooks** scheme (`webhook-id`/`webhook-signature`/`webhook-timestamp`).
**Solution**: Use the **`standardwebhooks`** library with the **signing key** (dashboard or `GET /webhooks/{id}/signing-key`) over the **raw** body; it validates signature + timestamp. For local testing use `dodo wh trigger` (CLI mocks are unsigned — `unsafe_unwrap()` in tests only). Dedupe on `webhook-id`.

### Is Dodo charging me tax / why is the fee higher than Stripe?
**Symptom**: Confusion about MoR fees and tax.
**Cause**: Dodo is a **Merchant of Record** — it's the legal seller and remits global VAT/GST/sales tax, so its fee (~4% + $0.40) is higher than a raw processor (~2.9% + 30¢).
**Solution**: That premium replaces your own multi-jurisdiction tax registration/filing. If you'd rather own tax compliance for a lower fee, a raw processor fits better — weigh it via `/sales-merchant-of-record`. Payouts are on a schedule (Payouts endpoints), not instant.
