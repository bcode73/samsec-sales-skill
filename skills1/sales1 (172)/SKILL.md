---
name: sales-fastspring
description: "FastSpring (fastspring.com) platform help — all-in-one Merchant of Record (MoR) for SaaS, software, games, AI, and digital products: sells on your behalf and remits global sales tax/VAT/GST across 200+ regions, with subscriptions + dunning, branded checkout (Store Builder Library + hosted), B2B invoicing/quotes, affiliates, and fraud protection. REST API (base https://api.fastspring.com, HTTP Basic auth, 250 calls/min) covers orders/subscriptions/products/accounts/coupons/checkout sessions, plus HMAC-SHA256-signed webhooks (X-FS-Signature). Use when integrating the FastSpring API or Store Builder Library, verifying webhook signatures, provisioning access on order.completed / subscription.activated, handling subscription dunning or refunds (FastSpring keeps its fee on refunds), or modeling its quote-based MoR fees vs a plain processor. Do NOT use for choosing a Merchant of Record across vendors (use /sales-merchant-of-record) or checkout-conversion strategy (use /sales-checkout)."
argument-hint: "[describe what you need help with in FastSpring]"
license: MIT
version: 1.0.0
tags: [sales, payments, merchant-of-record, platform]
github: "https://github.com/FastSpring"
---

# FastSpring Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Integrate the **REST API** (orders/subscriptions/products/accounts) or launch checkout
   - B) Build **checkout** — Store Builder Library (popup/embedded) or a hosted checkout session
   - C) **Verify webhooks** (`X-FS-Signature` HMAC-SHA256) and react to order/subscription events
   - D) Handle **subscription lifecycle** — dunning, overdue rebills, cancel/pause/resume
   - E) MoR concerns — tax/VAT remittance, refunds (fee is kept), payouts, chargebacks
   - F) Decide MoR (FastSpring) vs a raw processor, or compare to Paddle/Lemon Squeezy/Dodo

2. **API or no-code?** Code → REST API + SBL / webhooks. Low-code → hosted checkout + Zapier off webhooks.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| **Choosing** a Merchant of Record across vendors (FastSpring vs Paddle/Lemon Squeezy/Dodo/Stripe) | `/sales-merchant-of-record {question}` |
| Checkout/cart **conversion** strategy across platforms (order bumps, upsells, cart recovery) | `/sales-checkout {question}` |
| General **digital-product** selling strategy across tools | `/sales-digital-products {question}` |
| Subscription **churn / retention** strategy (not FastSpring dunning mechanics) | `/sales-membership {question}` |
| Generic iPaaS wiring to a CRM/ESP | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a selection question — run: `/sales-merchant-of-record FastSpring vs Paddle for a global SaaS`".

## Step 3 — FastSpring platform reference

**Read `references/platform-guide.md`** for the full reference — the MoR model (what FastSpring takes liability
for), capabilities + automation surface (API / webhook / UI), quote-based pricing + the refund-fee gotcha, the
data model, and quick-start recipes (provision on `order.completed`; sync subscriptions; SBL checkout).

**Read `references/fastspring-api-reference.md`** for the integration surface — base `https://api.fastspring.com`,
**HTTP Basic auth** (Developer Tools > APIs > API Credentials; password shown once), **250 calls/IP/min** (`429`),
the endpoint catalog (products/offers/prices, orders, subscriptions, accounts, coupons, checkout sessions,
quotes, returns, events, webhooks), the **Store Builder Library** (Access Key), and **HMAC-SHA256 webhooks**
(`X-FS-Signature`, `events` array, dedupe on `id`) with the full event list.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **MoR = FastSpring handles tax liability.** It's the legal seller and **remits** global VAT/GST/sales tax — you
  don't register/file per jurisdiction. That's the reason to pick it over a raw processor, at a higher fee.
- **Pricing is quote-based.** Reported rates are **8.9%** or **5.9% + $0.95**, assigned by their sales team by
  transaction type + volume — no public rate card. Effective subscription rates can exceed **10–12%**; model it.
- **Refunds keep the fee.** FastSpring retains its transaction fee on refunds — reconcile net revenue from
  `return` events; don't assume the fee reverses.
- **Verify webhooks over the raw body.** Set an HMAC secret, check `X-FS-Signature` (Base64 HMAC-SHA256), dedupe
  on `event.id` (redelivery happens), switch on `event.type`, return `2xx` fast and process async.
- **SBL for embedded checkout, API for server flows.** Use the Store Builder Library (Access Key to sign carts) on
  the site; use the checkout-session / subscriptions endpoints server-side. FX refreshes every 6h → re-pull pricing daily.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-07) — pricing is quote-based/negotiable and docs are largely JS-rendered; verify specifics in-account.*

1. **Pricing is quote-based, not public.** ~**8.9%** or **5.9% + $0.95** assigned by sales; the pricing page shows
   no percentages. Get your rate in writing and model effective subscription cost (often **10–12%+** on small charges).
2. **Refunds don't refund the fee.** FastSpring keeps its transaction fee when you refund a customer — a top complaint.
3. **Webhooks: verify `X-FS-Signature` over the RAW body.** Signature is Base64 HMAC-SHA256; re-serializing the
   body before hashing is the common bug. Set a secret (verification is optional but treat it as mandatory).
4. **Dedupe on `event.id`.** Events can be redelivered; payloads carry `created` in **milliseconds** and an `events` array.
5. **Enable webhook expansion** if you need full JSON — otherwise events can carry references, forcing extra API reads.
6. **Basic-auth password is shown once.** Generate credentials in Developer Tools > APIs; store the password immediately.
7. **Classic Commerce API is deprecated** (moved to github.com/fastspring/fastspring-api) — build on the modern
   `api.fastspring.com`, not Classic.
8. **MoR ≠ instant payouts.** As seller of record, FastSpring pays out on a schedule — model cash flow.

## Related skills

- `/sales-merchant-of-record` — Choosing a Merchant of Record across vendors (FastSpring vs Paddle/Lemon Squeezy/Dodo/Polar/Creem/Gumroad vs Stripe+Tax) — selection strategy, MoR-vs-processor tradeoffs
- `/sales-paddle` — Paddle platform help (MoR API/webhooks, Billing vs Classic) — the closest enterprise/B2B MoR alternative
- `/sales-dodo-payments` — Dodo Payments platform help (developer-first MoR — REST API, 9 SDKs, MCP server)
- `/sales-checkout` — Checkout/cart conversion strategy (order bumps, upsells, cart recovery) across platforms
- `/sales-digital-products` — Selling digital products (license keys, delivery, pricing) across tools
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Provision access when a purchase completes (developer/automation)
**User says**: "When someone buys my SaaS through FastSpring, how do I unlock their account automatically?"
**Skill does**: Points to a **webhook** listener on `order.completed` (and `subscription.activated` for
subscriptions): configure the webhook with an **HMAC secret**, verify the **`X-FS-Signature`** header (Base64
HMAC-SHA256) over the **raw** body, **dedupe on `event.id`**, then grant access from `event.data`. Notes returning
`2xx` quickly and processing async, and enabling **webhook expansion** for full payloads. References the Python
verification snippet in `references/fastspring-api-reference.md`.
**Result**: Authenticated, replay-safe automatic provisioning.

### Example 2: Sync subscriptions to a CRM / warehouse via the API
**User says**: "I want a nightly job that pulls all my active FastSpring subscriptions into HubSpot."
**Skill does**: Uses `GET /subscriptions` with `status=active&begin=&end=&live=true` against
`https://api.fastspring.com`, **HTTP Basic auth**, backing off on **`429`** (250 calls/IP/min, no reset header —
exponential backoff). Maps `account` → contact/company and `subscription` → subscription object, and recommends
treating webhooks as the realtime signal with the **daily API pull as reconciliation** (FX refreshes every 6h).
**Result**: A resilient scheduled sync with rate-limit handling.

### Example 3: MoR vs a processor — is FastSpring's fee worth it?
**User says**: "FastSpring quoted me around 8-9%. Stripe is way cheaper — why would I use FastSpring?"
**Skill does**: Frames the **Merchant-of-Record** tradeoff — FastSpring becomes seller of record and **remits**
global VAT/GST/sales tax (no per-country registration), whereas with Stripe you own tax compliance (Stripe Tax
calculates but doesn't remit). Flags FastSpring's **quote-based** rate (5.9%+$0.95 or 8.9%), the **10–12%+
effective** subscription cost, and that **refunds keep the fee**, then routes the cross-vendor decision: "run:
`/sales-merchant-of-record FastSpring vs Paddle vs Dodo for a global SaaS`."
**Result**: A clear MoR-vs-processor decision grounded in tax liability + real effective fees.

## Troubleshooting

### My webhook signature verification fails
**Symptom**: Events arrive but `X-FS-Signature` never matches.
**Cause**: Hashing a **re-serialized** body instead of the raw bytes, the wrong secret, or no secret configured on
the webhook.
**Solution**: Compute **Base64(HMAC-SHA256(raw_body, secret))** over the **exact raw request body** and compare to
`X-FS-Signature` with a constant-time check. Set the HMAC secret in Developer Tools > Webhooks; rotate it via the
"update a webhook key secret" API (validate the new key before discarding the old). Dedupe on `event.id`.

### My API calls return 401 (or 429)
**Symptom**: Requests to `api.fastspring.com` are rejected.
**Cause**: `401` — bad/missing **Basic auth** (wrong store credentials, or the password wasn't saved when
generated) or a missing **`User-Agent`** header (mandatory). `429` — over 250 calls/IP/min.
**Solution**: Send `Authorization: Basic base64(user:pass)` with credentials from Developer Tools > APIs (the
password shows only once — regenerate if lost), always include a `User-Agent`, and use TLS 1.2+. On `429`, back off
exponentially and batch by comma-separating IDs where supported.

### Why did FastSpring keep its fee when I refunded a customer / why is my effective rate so high?
**Symptom**: Refunds cost you the fee, and subscription revenue nets far below the headline rate.
**Cause**: FastSpring **retains its transaction fee on refunds**, and the per-transaction component (5.9% + $0.95
or 8.9%) spreads poorly across **small recurring charges**, pushing effective rates to 10–12%+.
**Solution**: Reconcile **net** revenue from `return`/`payout` events (don't assume the fee reverses), get your
negotiated rate in writing, and model effective cost on your actual price points. If the fee structure doesn't fit
low-ticket subscriptions, compare alternatives via `/sales-merchant-of-record`.
