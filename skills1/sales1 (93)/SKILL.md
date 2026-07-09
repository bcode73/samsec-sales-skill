---
name: sales-chargebee
description: "Chargebee platform help — subscription billing & revenue-management orchestration on top of your own payment gateway; you stay seller of record (NOT a Merchant of Record). REST API (`{site}.chargebee.com/api/v2`, HTTP Basic auth: API key as username, empty password), webhooks, three MCP servers + AgentKit, 40+ gateways, smart dunning, proration, revenue recognition (ASC 606), Product Catalog 1.0 vs 2.0. Use when building a Chargebee API or webhook integration, Chargebee webhooks have no HMAC signature to verify, handling out-of-order or duplicate webhook events, migrating Product Catalog 1.0 to 2.0, configuring smart dunning/retries for failed payments, confused by prorated credits on a mid-cycle upgrade, syncing subscriptions or MRR to a CRM or warehouse, or setting up the Chargebee MCP server in Claude or Cursor. Do NOT use for choosing a recurring-billing engine across tools (use /sales-subscription-billing) or Merchant-of-Record vs self-managed tax selection (use /sales-merchant-of-record)."
argument-hint: "[describe what you need help with in Chargebee]"
license: MIT
version: 1.0.0
tags: [sales, payments, billing, platform]
github: "https://github.com/chargebee"
---

# Chargebee Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build an API integration — create customers/subscriptions, manage invoices, pull data
   - B) Set up + consume webhooks to provision access / drive dunning
   - C) Migrate **Product Catalog 1.0 → 2.0** (plans/addons → items/item-prices)
   - D) Configure **dunning / smart retries** for failed payments
   - E) Understand **proration** on mid-cycle upgrades/downgrades
   - F) Set up the **Chargebee MCP server / AgentKit** for Claude or Cursor
   - G) Decide Chargebee vs another billing tool — that's a *selection* question (route in Step 2)

2. **Which Product Catalog?** PC 2.0 uses **items + item prices** (current default for new sites); PC 1.0 uses **plans + addons** (legacy). The API endpoints differ — confirm which your site is on before coding.

3. **Test or live?** Use your **test site** + test API keys first. The Time Machine (test clocks) only exists on test sites.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing a recurring-billing engine across tools (Chargebee vs Recurly vs Maxio vs Stripe Billing) | `/sales-subscription-billing {question}` |
| Merchant-of-Record vs self-managed tax, who remits VAT/GST | `/sales-merchant-of-record {question}` |
| Checkout-conversion optimization (order bumps, upsells, cart recovery) | `/sales-checkout {question}` |
| Subscription retention / win-back / churn strategy beyond billing | `/sales-customer-success {question}` |
| Connecting Chargebee to a CRM/other tools generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a billing-engine selection question — run: `/sales-subscription-billing Chargebee vs Recurly for usage-based SaaS`".

## Step 3 — Chargebee platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API vs webhook vs UI-only), the pricing/limits model (free Starter cumulative $250K cap, Performance, overages), the data model with JSON shapes, and quick-start recipes (create customer+subscription; provision/revoke access on a webhook; sync subscriptions/MRR to a warehouse).

**Read `references/chargebee-api-reference.md`** for the integration surface — base URL `https://{site}.chargebee.com/api/v2/`, **HTTP Basic auth** (API key as username, empty password), form-encoded requests + JSON envelope responses, offset/limit pagination, the `chargebee-idempotency-key` header, the **events/webhooks** model (no HMAC — basic-auth/URL-key + IP allowlist), error shape, rate limits, and the **MCP servers / AgentKit**.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

- **Auth is HTTP Basic, key-as-username.** `curl https://{site}.chargebee.com/api/v2/customers -u {api_key}:` — the API key is the username and the password is **empty** (note the trailing colon). Keys are environment-specific (test vs live) and come in full-access/publishable/read-only types — use the least-privileged key.
- **Webhooks have NO HMAC signature.** Unlike Paddle/Stripe, you can't verify an HMAC. Protect the URL with **basic auth and/or a secret URL key**, restrict to Chargebee's published **IP ranges**, then **dedupe on the event `id`** and **order by `resource_version`** (events are async, out-of-order, and redelivered for ~2–3 days).
- **Know your Product Catalog version.** PC 2.0 calls operate on **items/item_prices**; PC 1.0 on **plans/addons**. A PC 1.0 tutorial/SDK call won't work on a PC 2.0 site. Migration is **one-way** and not automatic.
- **Make writes idempotent.** Send a UUID in `chargebee-idempotency-key` (30-minute window) so retried create/charge calls don't double-bill.
- **Proration is automatic, but credit *type* varies.** Mid-cycle changes issue Adjustment credits (if the current invoice is unpaid) or Refundable credits (if paid). Verify the invoice state before assuming a refund.
- **Reconcile, don't just listen.** Because webhooks can be missed/late, periodically pull current state via the API to repair drift.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially pricing tiers and the API/webhook specifics, which change.*

1. **Webhooks are NOT HMAC-signed.** Chargebee only supports basic-auth or a random URL key + its published IP ranges. Don't expect a `Signature` HMAC like Paddle/Stripe — design verification around basic auth + IP allowlisting.
2. **Webhooks are async, unordered, and redelivered.** Order by `resource_version`, dedupe on event `id`, and keep an idempotency window of 3+ days (final retry lands ~3 days 7 hours out). Not for time-critical flows.
3. **Product Catalog 1.0 vs 2.0 is a hard split.** Plans/addons (PC1) vs items/item-prices (PC2) have different API calls. Migration is one-way (no rollback) and existing plans aren't auto-converted.
4. **The free Starter tier is *cumulative*, not monthly.** It covers total billing since signup up to ~$250K; past that Chargebee charges **0.75% on all billing** with no grace wall — model this before relying on "free."
5. **Smart Retry vs custom retry differ.** Smart Retry auto-schedules up to ~12 attempts by decline type (hard vs soft); custom retry caps at ~5 attempts you schedule by day.
6. **Amounts are in the smallest currency unit (cents).** `4900` = $49.00.
7. **UI is often called complex and support slow** in reviews — the **API/webhooks** are the praised, reliable surface, so prefer automating over clicking.

## Related skills

- `/sales-subscription-billing` — Choosing & operating a recurring-billing engine across tools (Chargebee vs Recurly vs Maxio vs Zuora vs Stripe Billing vs Orb/Lago; billing models, dunning, proration, RevRec)
- `/sales-merchant-of-record` — MoR vs self-managed tax selection (Chargebee is NOT a MoR — you stay seller of record and own tax)
- `/sales-checkout` — Checkout-conversion optimization across tools (order bumps, upsells, cart recovery)
- `/sales-customer-success` — Subscription retention / churn / health-score strategy beyond billing mechanics
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Provision access when a customer subscribes (developer/automation)
**User says**: "How do I grant my app's Pro plan when someone subscribes through Chargebee, and revoke it when payment fails?"
**Skill does**: Walks Recipe 2 — configure a webhook (protect the URL with **basic auth / secret key**, allowlist Chargebee's IPs since there's **no HMAC**), then on `subscription_activated`/`subscription_created` grant access by `customer_id`, and on `payment_failed`/`subscription_cancelled` start dunning or revoke. Stresses ordering by **`resource_version`**, deduping on event **`id`** (redelivery), and reconciling via `GET /subscriptions` for missed events.
**Result**: Reliable, replay-safe entitlement provisioning despite unsigned, unordered webhooks.

### Example 2: My subscription create call double-billed a customer
**User says**: "My retry logic created two subscriptions and charged twice. How do I stop that?"
**Skill does**: Identifies the missing idempotency key — shows adding the **`chargebee-idempotency-key`** header (a UUID) so retries within the 30-minute window are treated as the same request, and notes the smallest-unit (cents) amount format. Points to safe-retry handling on 429/5xx.
**Result**: Idempotent writes; no duplicate subscriptions or charges.

### Example 3: Moving from Product Catalog 1.0 to 2.0
**User says**: "We're on plans/addons and want to switch to items. Will my API integration still work?"
**Skill does**: Explains PC1 (plans/addons) → PC2 (items + item prices + price points + product families): the **API endpoints change**, multiple currency/frequency variants collapse into one item with price points, migration is **one-way** with no rollback and existing plans aren't auto-migrated. Recommends testing the PC2 calls on a test site first and flags the full billing-engine view in `/sales-subscription-billing`.
**Result**: A clear migration expectation and an updated integration plan.

## Troubleshooting

### My webhook endpoint can't verify requests are really from Chargebee
**Symptom**: You're looking for an HMAC signature header to validate webhooks and can't find one.
**Cause**: Chargebee does **not** sign webhooks with HMAC (unlike Paddle/Stripe). It only supports basic-auth on the URL or a random key embedded in the URL.
**Solution**: Enable "Protect webhook URL with basic authentication," and/or add a secret path/query key, and restrict inbound traffic to Chargebee's **published IP ranges**. Then dedupe on the event `id` and reconcile via the API. Treat the basic-auth credentials + IP allowlist as your authenticity check.

### A mid-cycle upgrade gave the customer a credit I didn't expect
**Symptom**: Upgrading/downgrading produced a proration credit that behaved differently than last time.
**Cause**: Chargebee proration depends on the current invoice state — an **unpaid** invoice gets an **Adjustment** credit applied to it; a **paid** invoice gets a **Refundable** credit applied to *future* invoices.
**Solution**: Check the current term's invoice status before changing the subscription. Use the `prorate`/`invoice_immediately`/`end_of_term` options to control timing, and preview with the estimate API before committing.

### Events show up out of order or twice in my database
**Symptom**: A `subscription_changed` arrives before `subscription_created`, or you process the same event twice.
**Cause**: Webhook delivery order isn't guaranteed and Chargebee retries (redelivers) failed/timed-out calls for ~2–3 days.
**Solution**: Make handlers **idempotent on the event `id`**, compare the `resource_version` (process only if newer than stored), keep the idempotency window ≥3 days, and run a periodic reconciliation pulling current state from the API.
