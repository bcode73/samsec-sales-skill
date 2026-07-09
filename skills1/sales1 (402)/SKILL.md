---
name: sales-paddle
description: "Paddle (paddle.com) platform help — Merchant of Record (MoR) billing for SaaS, apps, and digital products: localized checkout, subscriptions, global sales-tax/VAT compliance + remittance (300+ markets), invoicing, fraud, Retain dunning, and ProfitWell Metrics. Paddle Billing REST API (api.paddle.com, Bearer key, sandbox) with HMAC-SHA256 signed webhooks and a Docs MCP. Use when building a Paddle Billing API or webhook integration, migrating off the legacy Paddle Classic API to Billing, verifying webhook HMAC signatures or handling out-of-order/duplicate events, subscriptions or transactions not provisioning access, amounts wrong because money is cents-as-a-string, syncing MRR/subscriptions to a warehouse, or understanding the 5% + $0.50 MoR fee and payout timing. Do NOT use for choosing a Merchant of Record across providers (use /sales-merchant-of-record), checkout-conversion optimization across tools (use /sales-checkout), or Lemon Squeezy-specific help (use /sales-lemonsqueezy)."
argument-hint: "[describe what you need help with in Paddle]"
license: MIT
version: 1.0.0
tags: [sales, payments, checkout, platform]
github: "https://github.com/PaddleHQ"
---

# Paddle Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build an API integration — create products/prices, manage subscriptions/transactions, pull reports
   - B) Set up + verify webhooks (HMAC-SHA256) to provision access / run dunning
   - C) Migrate from the legacy **Paddle Classic** API to **Paddle Billing**
   - D) Understand the MoR model — fees (5% + $0.50), tax handled for you, payout timing
   - E) Fix a problem — wrong amounts (cents-as-string), out-of-order/duplicate webhooks, signature failures
   - F) Decide if Paddle vs another provider — that's a *selection* question (route in Step 2)

2. **Billing or Classic?** Build everything new on **Paddle Billing** (`api.paddle.com`). Only touch Classic to migrate an existing integration off it.

3. **Sandbox first?** Use `sandbox-api.paddle.com` with separate keys before production.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing a Merchant of Record / payments provider across tools (Paddle vs Lemon Squeezy vs Polar vs Stripe) | `/sales-merchant-of-record {question}` |
| Checkout-conversion optimization across tools (order bumps, upsells, cart recovery) | `/sales-checkout {question}` |
| Lemon Squeezy-specific setup/API | `/sales-lemonsqueezy {question}` |
| Subscription churn / dunning strategy across tools | `/sales-membership {question}` |
| Connecting Paddle to a CRM/other tools generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a provider-selection question — run: `/sales-merchant-of-record Paddle vs Lemon Squeezy for my B2B SaaS`".

## Step 3 — Paddle platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API vs MoR-handled vs UI-only), the MoR fee/payout model (5% + $0.50, global tax included, scheduled payouts), the data model with JSON shapes, and quick-start recipes (provision access on a subscription webhook; create a product+price; sync MRR to a warehouse).

**Read `references/paddle-api-reference.md`** for the integration surface — **Paddle Billing** base URLs (`api.paddle.com` + sandbox), Bearer auth, the entity list (products/prices/customers/transactions/subscriptions/adjustments/reports), pagination + `include`, the **HMAC-SHA256 webhook verification** pattern + event list, and the Classic-vs-Billing split. Plus the **Docs MCP**.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Build on Billing; Classic is dead weight.** New work uses `api.paddle.com` + a **Bearer** key (Paddle →
  Developer Tools → Authentication). Classic is a separate, incompatible legacy product — only touch it to migrate off.
- **Money is cents-as-a-string.** `unit_price.amount = "2000"` is $20.00. Sending dollars (or a number) is
  the #1 first-bug. Set the correct `tax_category` so Paddle taxes right.
- **Webhooks are the source of truth — and tricky.** Verify the **HMAC-SHA256** `Paddle-Signature`, then
  order processing by **`occurred_at`** (delivery order isn't guaranteed) and dedupe on **`event_id`**
  (Paddle redelivers). Reconcile periodically via the API in case a webhook is missed.
- **You don't build tax.** As MoR, Paddle calculates + remits sales tax/VAT — that's the whole point; don't
  reinvent it. The MoR-vs-DIY-tax decision lives in `/sales-merchant-of-record`.
- **Model payouts + the 5% + $0.50 fee.** Paddle pays you out on a schedule after collecting; it's not
  instant Stripe-style settlement.
- **Sandbox first.** Separate sandbox account + keys; never develop against production billing.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially fees and the API/webhook specifics, which change.*

1. **Paddle Classic ≠ Paddle Billing.** Separate products with incompatible endpoints, auth, schemas, and webhooks. Build on **Billing**; a Classic tutorial won't work on Billing (and vice-versa).
2. **Amounts are strings in the smallest unit (cents).** `"2000"` = $20.00 — sending dollars or a number breaks pricing.
3. **Webhook delivery order isn't guaranteed.** A `subscription.updated` can arrive before `subscription.created`; order by **`occurred_at`**.
4. **Webhooks can be redelivered.** Make handlers **idempotent on `event_id`** so you don't double-provision.
5. **Always verify the HMAC-SHA256 signature.** Unverified webhooks are a spoofing risk; sign `ts:rawbody` with the per-destination secret and compare to `Paddle-Signature`.
6. **As MoR, Paddle owns payouts + risk review.** You're paid on a schedule (not instantly), and high-risk/disallowed categories can be declined at onboarding.
7. **Sandbox and production are fully separate.** Different accounts and keys — don't mix them.
8. **Tax is Paddle's job.** Don't build sales-tax/VAT logic; set `tax_category` and let the MoR handle calc + remittance.

## Related skills

- `/sales-merchant-of-record` — Choosing a Merchant of Record / payments provider across tools (Paddle vs Lemon Squeezy vs Polar vs Creem vs Stripe; MoR vs self-managed tax)
- `/sales-checkout` — Checkout-conversion optimization across tools (order bumps, upsells, cart recovery)
- `/sales-lemonsqueezy` — Lemon Squeezy platform help (the closest MoR competitor)
- `/sales-membership` — Subscription retention / churn / dunning strategy (Paddle's Retain feeds this)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Provision access when a customer subscribes (developer/automation)
**User says**: "How do I grant my app's Pro access when someone subscribes through Paddle?"
**Skill does**: Walks Recipe 1 — register a webhook, **verify the HMAC-SHA256 `Paddle-Signature`**, then on `subscription.activated` / `transaction.completed` grant access by `customer_id`, and on `subscription.canceled` / `past_due` revoke or start dunning. Stresses ordering by **`occurred_at`** (delivery isn't ordered), idempotency on **`event_id`** (redelivery), reconciling via the API for missed events, and building on **Billing** in **sandbox** first.
**Result**: Reliable, signature-verified entitlement provisioning.

### Example 2: My prices are coming out 100x wrong
**User says**: "I set a $20 plan but Paddle shows $0.20 (or $2000)."
**Skill does**: Identifies the cents-as-a-string model — `unit_price.amount` is the **smallest currency unit as a string**, so $20.00 = `"2000"`. Shows the correct create-price body and notes the right `tax_category` so Paddle applies tax correctly. Flags this as the most common first-integration bug.
**Result**: Correct pricing via the API.

### Example 3: Should I use Paddle or Lemon Squeezy?
**User says**: "I'm launching a B2B SaaS — Paddle or Lemon Squeezy as my merchant of record?"
**Skill does**: Recognizes a cross-provider **selection** question and routes: "run: `/sales-merchant-of-record Paddle vs Lemon Squeezy for B2B SaaS with enterprise invoicing`." Briefly notes Paddle's edge (most mature tax coverage, B2B invoicing) but defers the full comparison + MoR-vs-DIY decision to the strategy skill.
**Result**: User is handed to the right strategy skill with a ready prompt.

## Troubleshooting

### My webhook signature verification keeps failing
**Symptom**: HMAC comparison never matches, so you reject valid Paddle webhooks.
**Cause**: Hashing a re-serialized body instead of the **raw request bytes**, mis-parsing the `Paddle-Signature` header (`ts=...;h1=...`), or using the wrong per-destination secret.
**Solution**: Sign the literal string `"{ts}:{raw_body}"` with HMAC-SHA256 using the destination's secret and compare to `h1`. Use the **raw, unparsed** request body (not your framework's parsed JSON), grab `ts`/`h1` from the header, and confirm you're using the secret for *that* notification destination.

### My old Paddle integration broke / docs don't match
**Symptom**: Endpoints, fields, or events from a tutorial don't exist in your account.
**Cause**: Mixing **Paddle Classic** (legacy) and **Paddle Billing** (current) — they're different products.
**Solution**: Confirm which product you're on. Build new integrations on **Paddle Billing** (`api.paddle.com`, Bearer key, the entities in the API reference). Migrate Classic integrations to Billing; don't expect Classic vendor-id/auth-code calls to work against Billing.

### Subscriptions look out of sync / duplicated in my DB
**Symptom**: A subscription shows updated before it shows created, or you provisioned twice.
**Cause**: Webhook **delivery order isn't guaranteed** and events can be **redelivered**.
**Solution**: Order processing by **`occurred_at`**, make handlers **idempotent on `event_id`**, and run a periodic reconciliation that pulls current state from `GET /subscriptions` to repair any drift from missed/late webhooks.
