---
name: sales-samcart
description: "SamCart platform help — hosted checkout/cart for digital-product creators (conversion templates, order bumps, 1-click upsells, A/B testing, Subscription Saver dunning, Affiliate Center) with a read-mostly REST API (api.samcart.com/v1, sc-api key header, official OpenAPI spec — private beta, key via support) and unsigned Notify URL webhooks (~15 triggers). Use when integrating SamCart orders/subscriptions into a CRM or data warehouse, a Notify URL webhook needs verification or a polling backup, canceling or scheduling subscription cancellation via the API, watching failed charges and dunning recovery, deciding between Core and Pro (upsells, order bumps, A/B testing and affiliates are Pro-gated), attributing funnel/upsell/affiliate revenue, or planning a migration off SamCart when recurring payments can't port. Do NOT use for checkout-conversion strategy across carts (use /sales-checkout) or digital-product pricing/launch strategy (use /sales-digital-products)."
argument-hint: "[describe what you need help with in SamCart]"
license: MIT
version: 1.0.2
tags: [sales, digital-products, checkout, platform]
github: "https://github.com/samcart"
---

# SamCart Platform Help

SamCart is a hosted checkout/cart platform for digital-product creators: conversion-optimized checkout pages with order bumps, 1-click upsells, subscription billing with dunning ("Subscription Saver"), and a built-in Affiliate Center — subscription-priced (vs ThriveCart's lifetime license). Automation runs through a read-mostly REST API plus "Notify URL" webhooks.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you can't infer from the user's prompt:

1. **What are you trying to do?**
   - A) Integrate SamCart data (orders/subscriptions/customers) with a CRM, warehouse, or your app
   - B) Set up or debug Notify URL webhooks
   - C) Manage subscriptions programmatically (cancel, schedule-cancel, dunning visibility)
   - D) Decide on a plan (Core vs Pro vs Enterprise) or understand fees
   - E) Checkout/upsell/affiliate configuration questions

2. **Do you have an API key yet?** The API is a support-gated private beta — keys come from support@samcart.com, not self-serve settings.

Skip-ahead rule: if the user's prompt already has enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user's question is about… | Route to |
|---|---|
| Which cart/checkout platform to pick (SamCart vs ThriveCart/Checkout Page/Gumroad) | `/sales-checkout {question}` |
| Checkout-conversion strategy (bump/upsell design, cart abandonment) across tools | `/sales-checkout {question}` |
| Digital-product pricing, validation, launch strategy | `/sales-digital-products {question}` |
| Migrating active subscriptions between billing platforms without double-billing | `/sales-subscription-billing {question}` |
| Running an affiliate program (commission design, recruiting) | `/sales-affiliate-program {question}` |

When routing, give the exact command: "This is a {domain} question — run: `/sales-checkout {original question}`"

Otherwise, answer SamCart-specific questions directly using Step 3.

## Step 3 — SamCart platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model (orders → cart_items → charges/subscriptions), and quick-start recipes (nightly order sync, verified webhook listener, subscription cancellation).

For raw endpoint detail, auth, pagination, webhook triggers, and payload shapes, read `references/samcart-api-reference.md`.

Answer using only the relevant section — don't dump the full reference.

## Step 4 — Actionable guidance

- **Treat webhooks as hints, the API as truth.** Notify URL payloads are unsigned — verify by re-fetching the order/subscription with your `sc-api` key before granting access or moving money.
- **The API reads; the UI writes.** You can pull orders/charges/customers/subscriptions and refund/cancel — but products, pages, bumps, and upsells are configured only in the UI (or via Zapier/Make actions).
- **Build self-serve cancellation on `scheduleCancel`.** Billing-after-cancellation is SamCart's loudest public complaint — a logged, API-driven cancel path plus the `Subscription Canceled` webhook protects both you and your buyers.
- **Model Pro-gating before committing.** Order bumps, upsells, A/B testing, and the Affiliate Center — the features SamCart markets — need Pro ($199/mo). Always present plan pricing as best-effort and tell the user to verify current numbers at samcart.com/pricing — SamCart has restructured plans before.

If you discover a gotcha or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-07) — review these, especially plan pricing and beta-API status that may have changed.*

- **API access is a support-gated private beta** — email support@samcart.com and plan for approval lead time; there's no self-serve key page. Keys go in the `sc-api` header (not `Authorization`).
- **Webhooks are unsigned with no documented retries** — use an unguessable endpoint token + API verification, and keep a polling reconciliation; the Integration Engine only logs the last 1,000 events.
- **Recurring revenue doesn't port off SamCart** — payment tokens stay behind when you leave, so subscribers must re-consent on the next platform. Weigh this before building a large subscription base here (see `/sales-subscription-billing`).
- **Conversion features are Pro-gated** — Core ($79/mo) excludes order bumps, 1-click upsells, A/B testing, and the Affiliate Center; those need Pro ($199/mo). Legacy Launch/Grow/Scale plans reportedly scaled with revenue.
- **Cancellation/billing disputes are the #1 public complaint** (including Creator U trials converting into paid SamCart accounts) — as a seller, keep your own cancellation logs; as a buyer of SamCart, calendar your trial/renewal dates.
- **Quirky event timing**: "Checkout failed" fires after a 10-minute built-in delay; "Prospect created" fires ~2 hours after creation. Don't treat them as real-time.
- **All API money values are in cents** — a $250 order is `"total": 25000`.

## Related skills

- `/sales-checkout` — Checkout-page strategy and cart-platform selection (SamCart vs ThriveCart vs Checkout Page vs Gumroad; bumps, upsells, cart abandonment)
- `/sales-thrivecart` — ThriveCart platform help (the lifetime-license competitor)
- `/sales-digital-products` — Digital-product strategy: pricing, validation, launch
- `/sales-subscription-billing` — Subscription billing engines and migrating active subscribers without double-billing
- `/sales-affiliate-program` — Affiliate program strategy (SamCart's Affiliate Center is one implementation)
- `/sales-merchant-of-record` — Tax/VAT handling (SamCart is not a Merchant of Record)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync SamCart sales into a CRM (developer/automation)
**User says**: "How do I get SamCart orders and subscription status into HubSpot automatically?"
**Skill does**: Sets up Notify URL webhook rules (Product Purchased, Subscription Charged/Canceled) pointing at a tokenized endpoint, verifies each payload by re-fetching via `GET /orders/{id}` with the `sc-api` header, and adds a nightly incremental `GET /orders?created_at_min=…` reconciliation pull following `pagination.next` — with the Python recipes from the platform guide.
**Result**: CRM stays in sync with verified data even when an unsigned webhook is missed or spoofed.

### Example 2: Dunning and failed payments
**User says**: "Subscribers keep failing payments — how do I see and reduce involuntary churn on SamCart?"
**Skill does**: Explains Subscription Saver's recovery flow, wires `Subscription Delinquent`/`Recovered` webhook triggers into alerts, adds a daily `GET /failed-charges` poll for dunning visibility, and reviews retry/email settings.
**Result**: User watches delinquency in near-real-time and recovers more failed charges.

### Example 3: Core vs Pro decision
**User says**: "Is SamCart Pro worth $199/mo, or is Core enough for my course launch?"
**Skill does**: Maps the user's needs against the plan gates — order bumps, 1-click upsells, A/B testing, and the Affiliate Center all require Pro — then models whether projected bump/upsell revenue (typically 10–30% AOV lift when configured) exceeds the $120/mo difference; flags the 25% annual discount and payment-processing fees on top.
**Result**: User picks a plan from expected AOV lift, not feature FOMO.

## Troubleshooting

### Webhook payload arrived but looks untrustworthy (or never arrived)
**Symptom**: Notify URL POSTs are unsigned, occasionally missing, or contain NULL fields.
**Cause**: SamCart doesn't sign payloads or document retries; missing values are sent as NULL; some triggers are delayed by design (checkout-failed +10 min, prospect-created ~2 h).
**Solution**: Put a secret token in the endpoint URL, verify every payload by re-fetching the object via the API, return 200 fast, and reconcile with date-filtered `GET /orders` polls. Check the Integration Engine's event log (last 1,000 events) when debugging.

### 401 Unauthorized on every API call
**Symptom**: All requests fail with 401 even with a key.
**Cause**: Key not passed in the `sc-api` header (it's not a Bearer token), missing `Accept: application/json` header, or the key was never issued (private beta).
**Solution**: Send `sc-api: {key}` and `Accept: application/json` over HTTPS. If you have no key, request beta access via support@samcart.com and plan integration timelines around approval.

### Getting rate-limited (429) on bulk pulls
**Symptom**: Large order/charge exports start returning 429.
**Cause**: All endpoints are rate-limited; numeric limits aren't published.
**Solution**: Read the 429 response header for the seconds remaining, sleep that long, and resume from the last `pagination.next` URL. Keep pulls incremental with `created_at_min`/`created_at_max` instead of re-reading history.
