---
name: sales-subscription-billing
description: "Recurring-billing engine selection and operation for SaaS — picking and running a subscription/usage-billing platform (Chargebee, Recurly, Maxio, Zuora, Stripe Billing, Orb, Lago, Zoho Billing) on top of your own payment gateway, where you stay seller of record. Use when choosing a billing engine, deciding whether to build billing on Stripe Billing vs a dedicated tool, adding usage-based / metered / hybrid pricing, automating dunning and failed-payment retries, getting proration right on mid-cycle upgrades/downgrades, needing revenue recognition (ASC 606 / IFRS 15), weighing open-source self-hosted billing (Lago) vs SaaS, or planning a billing-platform migration. Do NOT use for Chargebee-specific API/config (use /sales-chargebee), Merchant-of-Record vs self-managed tax — who remits VAT/GST (use /sales-merchant-of-record), checkout-conversion optimization (use /sales-checkout), or churn/retention strategy beyond billing mechanics (use /sales-membership)."
argument-hint: "[describe your billing decision — e.g., 'usage-based billing engine for B2B SaaS' or 'Stripe Billing vs Chargebee']"
license: MIT
version: 1.0.0
tags: [sales, payments, billing, strategy]
---

# Subscription & Usage-Based Billing Engine Selection

Helps **choose and operate a recurring-billing engine** — the system that turns subscriptions and usage
into invoices, retries failed payments (dunning), handles proration, and (optionally) does revenue
recognition — running **on top of your own payment gateway** so **you stay the seller of record**. This is
a different decision from a Merchant of Record (who absorbs global tax liability — see
`/sales-merchant-of-record`).

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user (lead with a best-effort answer if they've already told you most of this):

1. **What's the decision?**
   - A) Which billing engine — Chargebee vs Recurly vs Maxio vs Zuora vs Stripe Billing vs Orb vs Lago
   - B) Build on **Stripe Billing** vs adopt a dedicated engine
   - C) Add **usage-based / metered / hybrid** pricing to existing billing
   - D) **Migrate** off / onto a billing platform
   - E) An operational need — **dunning**, **proration**, or **revenue recognition (ASC 606)**

2. **Pricing model?** Flat-rate subscriptions · per-seat · **usage/metered** · credits/prepaid · hybrid
   (subscription + overage). Usage-heavy products narrow the field hard (Orb/Metronome/Lago/Maxio).

3. **Stage / team?** Solo/indie · small team (no RevOps/finance) · scaling B2B with finance ops ·
   enterprise needing a GAAP system of record.

4. **Constraints?** Already on Stripe for payments? · need open-source / data ownership / self-host? ·
   need RevRec or ERP/accounting sync? · budget sensitivity.

5. **Seller-of-record or Merchant-of-Record?** If you want someone else to **remit** global VAT/GST/sales
   tax, that's a MoR decision — route to `/sales-merchant-of-record`. Billing engines here leave tax to you.

**Skip-ahead rule:** if the prompt already provides most of this, go straight to Step 4 with stated
assumptions, then ask 1–2 critical clarifiers.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Chargebee-specific API, webhooks, Product Catalog 1.0→2.0, config | `/sales-chargebee {question}` |
| Merchant-of-Record vs self-managed tax, who remits VAT/GST/sales tax | `/sales-merchant-of-record {question}` |
| Checkout-conversion optimization (order bumps, upsells, cart recovery) | `/sales-checkout {question}` |
| Subscription **retention / win-back / churn strategy** beyond billing | `/sales-membership {question}` |
| Connecting the billing engine to a CRM/warehouse/other tools (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is Chargebee-specific setup — run: `/sales-chargebee how do I verify webhooks`".

## Step 3 — Engine comparison reference

**Read `references/platforms.md`** for the full comparison — the per-engine matrix (Chargebee, Recurly,
Maxio, Zuora, Stripe Billing, Orb, Lago, Zoho Billing), how each handles usage vs subscriptions, dunning,
proration, RevRec, pricing model, and migration cost. Also lists adjacent metering tools (Metronome).

Answer using only the relevant section. Don't dump the whole reference.

## Step 4 — Actionable guidance

### The core decision: Stripe Billing vs a dedicated engine
- **Already on Stripe, simple flat/per-seat subscriptions, small team → Stripe Billing.** Cheapest
  (~0.7% of billed volume), zero extra integration, fine until pricing gets complex. It lacks deep dunning
  analytics, RevRec, and flexible catalog modeling.
- **Complex catalog, hybrid/usage pricing, want the full revenue lifecycle automated → dedicated engine**
  (Chargebee/Recurly/Maxio). They orchestrate *your* gateway (often Stripe) — you keep the processor and
  add billing depth on top.

### Pick by what dominates your model
- **Subscription-first, growing SaaS adding usage overages, want the whole lifecycle → Chargebee.** Broadest
  feature set; UI/setup are involved (route setup to `/sales-chargebee`).
- **High-volume subs where reducing churn / collecting variable invoices is the priority → Recurly.** Dunning
  and revenue-recovery focus; from ~$149/mo + fees.
- **B2B SaaS that must tie usage billing to RevOps + RevRec reporting → Maxio** (ex-Chargify + SaaSOptics).
- **Enterprise needing a GAAP-compliant global system of record → Zuora.** Most powerful, heaviest.
- **Usage metering IS the product, stack already built → Orb** (or Metronome) — accurate event metering first.
- **Want open-source control, no revenue tax, comfortable owning hosting/eng → Lago** (self-host or cloud).
- **SMB already in the Zoho suite → Zoho Billing** — cheapest, tightly integrated, lighter on advanced needs.

### Operational realities
- **Dunning beats discounting.** Most "churn" on these platforms is **involuntary** (failed cards). Smart,
  decline-type-aware retries + card-expiry reminders recover real revenue — turn them on before chasing offers.
- **Proration is where surprises hide.** Mid-cycle changes issue credits whose *type/timing* depends on
  invoice state — preview with the estimate API before committing, and test on a sandbox/test clock.
- **Usage billing needs idempotent, deduped metering.** Double-counted events = wrong invoices; design the
  meter ingestion to be replay-safe.

### Don't migrate lightly
Switching billing engines means re-tokenizing payment methods (sometimes a customer re-subscribe),
migrating subscription state + invoice history, and re-wiring webhooks/RevRec. Migrate only for a structural
reason (outgrowing the catalog, needing usage/RevRec, fee at scale), not a small fee delta.

If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Gotchas

> *Best-effort from research (2026-06) — fees, plans, and feature depth change; verify on each vendor.*

1. **A billing engine is NOT a Merchant of Record.** Chargebee/Recurly/Maxio/Zuora/Stripe Billing leave you
   the seller of record — *you* register/file/remit tax. Want tax off your plate? That's `/sales-merchant-of-record`.
2. **"Free" billing tiers have cumulative caps.** Chargebee's free Starter covers cumulative billing to ~$250K,
   then 0.75% on everything — model TCO, don't assume monthly-free.
3. **Headline price ≠ TCO.** RevRec, retention/analytics, and premium integrations are often **separate add-ons**
   ($200–$2,000+/mo). Add your gateway's ~2.9% + 30¢ on top — these engines don't process payments.
4. **Usage metering is the hard part.** Accuracy, idempotency, and late/duplicate events make or break
   usage-based billing — Orb/Metronome/Lago specialize here; bolt-on usage on a subscription-first tool can be shallow.
5. **Self-hosting (Lago) trades fees for ops.** No revenue tax, full control — but you own Postgres/Redis,
   upgrades, scaling, and uptime. Real cost is engineering time, not license.
6. **Proration + dunning configs are easy to get subtly wrong.** Always test on a sandbox / test clock before
   relying on credit amounts or retry schedules in production.

## Related skills

- `/sales-chargebee` — Chargebee platform help (API/webhooks, Product Catalog 1.0→2.0, dunning, proration, RevRec)
- `/sales-merchant-of-record` — MoR vs self-managed tax selection (who remits VAT/GST — the *other* billing decision)
- `/sales-checkout` — Checkout-conversion optimization across tools (order bumps, upsells, cart recovery)
- `/sales-swell` — Swell platform help (API-first commerce backend with a *native* subscription engine — pause/resume, dunning, separate billing/fulfillment schedules; an alternative to bolting a standalone engine onto a separate cart)
- `/sales-membership` — Subscription retention, churn, and win-back strategy beyond billing mechanics
- `/sales-integration` — Wiring a billing engine into a CRM, warehouse, or other tools (webhooks, iPaaS)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Stripe Billing vs a dedicated engine
**User says**: "We're on Stripe and our subscriptions are getting complicated — should we stay on Stripe Billing or move to Chargebee?"
**Skill does**: Frames it as complexity-driven, not fee-driven. Stripe Billing stays best for simple flat/per-seat subs at the lowest cost; a dedicated engine like Chargebee makes sense once you need flexible catalog modeling, hybrid/usage pricing, deep dunning, or RevRec — and it still orchestrates Stripe as the processor. Asks about pricing model + finance needs, then recommends accordingly and routes Chargebee setup to `/sales-chargebee`.
**Result**: A complexity-based decision, with the processor kept and billing depth layered on.

### Example 2: Usage-based billing engine for B2B SaaS
**User says**: "We're launching metered, usage-based pricing for an API product. Which billing platform?"
**Skill does**: Narrows to usage-first engines — Orb/Metronome for accurate event metering, Lago for open-source/self-host, Maxio if usage must tie into RevOps/RevRec. Stresses idempotent, deduped meter ingestion and that subscription-first tools' usage add-ons can be shallow. Recommends a shortlist by team/stage and notes you still own tax (not a MoR).
**Result**: A usage-billing shortlist matched to metering accuracy and team capacity.

### Example 3: Cheapest path for an indie selling globally
**User says**: "Solo founder, global customers, I just want recurring billing without becoming a tax department."
**Skill does**: Flags that this is actually a **Merchant-of-Record** question — a billing engine leaves tax to the seller. Routes to `/sales-merchant-of-record` for the MoR-vs-Stripe decision, and notes that if they're fine owning tax, Stripe Billing (cheapest) or Zoho Billing (if in Zoho) are the lean billing-engine picks.
**Result**: Correctly redirected to MoR for the tax-remittance need, with a fallback billing-engine pick.

## Troubleshooting

### "Customers are churning from failed payments, not cancellations"
**Symptom**: Revenue leaks but customers aren't actively quitting.
**Cause**: **Involuntary churn** — expired/declined cards with weak retry logic.
**Solution**: Turn on **smart, decline-type-aware dunning** (retry soft declines aggressively, hard declines once), card-expiry reminders, and a self-serve update-card flow. Recurly specializes here; Chargebee's Smart Retry does decline-aware scheduling. Measure recovered MRR, not just retry count.

### "Mid-cycle upgrades produce credits I can't predict"
**Symptom**: Proration credits vary unexpectedly between changes.
**Cause**: Credit **type and timing depend on the current invoice state** (paid vs unpaid) and your proration settings.
**Solution**: Preview with the engine's **estimate API** before committing the change, decide explicitly between immediate-charge vs end-of-term, and test on a **sandbox / test clock**. For Chargebee specifics, route to `/sales-chargebee`.

### "We picked a tool but our usage invoices are wrong"
**Symptom**: Metered charges don't match real usage.
**Cause**: Duplicate or out-of-order usage events, non-idempotent meter ingestion.
**Solution**: Make event ingestion **idempotent + deduped** (unique event ids, replay-safe), reconcile meter totals against source, and prefer a usage-native engine (Orb/Metronome/Lago) if metering is core. Validate a full billing cycle on a test clock before going live.
