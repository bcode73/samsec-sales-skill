---
name: sales-merchant-of-record
description: "Merchant of Record (MoR) and payments-provider selection for SaaS and digital products — when to let a MoR (Paddle, Lemon Squeezy, FastSpring, Polar, Creem, Gumroad) handle global sales tax/VAT for you vs running a self-managed processor (Stripe + Stripe Tax), and which provider fits. Use when deciding how to bill global customers, unsure whether a Merchant of Record should own tax compliance or you should manage it yourself, comparing Paddle vs Lemon Squeezy vs Polar vs Creem vs Stripe on fees and tax coverage, worried about EU VAT / US sales tax / GST nexus, picking a billing provider for a new SaaS, the ~5% MoR fee feeling high, or weighing a costly switch between providers. Do NOT use for Paddle-specific API/config (use /sales-paddle), Lemon Squeezy-specific setup (use /sales-lemonsqueezy), checkout-conversion optimization (use /sales-checkout), subscription churn/dunning tactics (use /sales-membership), or two-sided marketplace seller payouts (use /sales-marketplace-payouts)."
argument-hint: "[describe your billing/tax situation — e.g., 'MoR vs Stripe for a global SaaS' or 'Paddle vs Lemon Squeezy for B2B']"
license: MIT
version: 1.0.0
tags: [sales, payments, merchant-of-record, strategy]
---

# Merchant of Record & Payments-Provider Selection

Helps choose **how to bill global customers** for SaaS/digital products: whether to use a **Merchant of
Record** (which absorbs global sales-tax/VAT liability for a higher fee) or a **self-managed processor**
like Stripe (lower fee, but you own tax registration + remittance), and which specific provider fits.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user (lead with a best-effort answer if they've already told you most of this):

1. **What's the decision?**
   - A) MoR vs self-managed (Stripe) — the strategic call
   - B) Which MoR — Paddle vs Lemon Squeezy vs FastSpring vs Dodo vs Polar vs Creem vs Gumroad
   - C) Switching providers — is it worth it / how painful
   - D) Tax-compliance worry — VAT/GST/sales-tax nexus and who's liable

2. **What are you selling?** Self-serve SaaS subscriptions · B2B SaaS (invoices/POs/net terms) · one-off
   digital products · usage-based · mobile-app purchases.

3. **Where are your customers?** Mostly domestic (one tax jurisdiction) · global (many) — this is the single
   biggest factor in the MoR-vs-DIY call.

4. **Stage / team?** Solo/indie · small team (no finance/tax ops) · scaling with finance ops · enterprise.

5. **Fee sensitivity?** Lowest possible fee · willing to pay ~5% to never touch tax.

**Skip-ahead rule:** if the prompt already provides most of this, go straight to Step 4 with stated
assumptions, then ask 1–2 critical clarifiers.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Paddle-specific API, webhooks, Billing-vs-Classic, or config | `/sales-paddle {question}` |
| Lemon Squeezy-specific setup/API | `/sales-lemonsqueezy {question}` |
| Gumroad-specific setup/API | `/sales-gumroad {question}` |
| Checkout-conversion optimization (order bumps, upsells, cart recovery) | `/sales-checkout {question}` |
| Subscription churn / dunning / retention tactics | `/sales-membership {question}` |
| Two-sided **marketplace** seller payouts (paying out many suppliers) | `/sales-marketplace-payouts {question}` |
| Choosing a **billing engine** (stay seller of record, keep tax in-house): Chargebee/Recurly/Maxio/Stripe Billing/Zuora/Orb/Lago | `/sales-subscription-billing {question}` |
| **Chargebee**-specific API/webhooks/config | `/sales-chargebee {question}` |

Otherwise, answer from the framework below.

## Step 3 — Provider comparison reference

**Read `references/platforms.md`** for the full comparison — the MoR-vs-processor distinction, the decision
matrix (Paddle / Lemon Squeezy / Polar / Creem / Gumroad / Stripe) plus the FastSpring and Dodo Payments
sections, per-provider fees, tax coverage, B2B support, and switching costs.

Answer using only the relevant section. Don't dump the whole reference.

## Step 4 — Actionable guidance

### The core decision: MoR vs self-managed (Stripe)
- **Sell globally + small/no finance team → MoR.** The ~5% buys away registering, calculating, filing, and
  **remitting** VAT/GST/sales-tax in every jurisdiction, plus fraud/chargeback liability. You're the product
  builder, not a tax department.
- **Mostly domestic, or have finance/tax ops (or a tax engine like Anrok/Avalara), or need max control/low
  fee at scale → Stripe (self-managed).** Stripe Tax *calculates* but does **not remit** — you stay the
  seller of record and own compliance.
- **Reframe the fee:** MoR ~5% vs Stripe ~2.9% looks like a 2% gap, but international Stripe (intl card +FX
  +Stripe Tax) effectively reaches ~5%, and *then* you still owe the compliance work. The real comparison is
  "~2% extra" vs "an accountant + registrations in N countries."

### Which MoR (quick picks)
- **Lowest fee, indie/micro-SaaS:** Creem (newest — weigh vendor risk) or Lemon Squeezy.
- **Self-serve SaaS, great DX, staying simple:** Lemon Squeezy (now Stripe-owned).
- **Devtool/OSS audience, DX over fee:** Polar (highest fee, ~10%).
- **Scaling into B2B/enterprise — POs, net terms, deepest tax coverage:** Paddle.
- **Software/games/SaaS wanting a proven enterprise MoR with B2B quotes/invoicing (rate is negotiated):** FastSpring — mind the quote-based pricing and that refunds keep the fee.
- **Creator selling one-off digital products with a marketplace:** Gumroad.

### Don't churn providers lightly
Switching MoRs (or MoR→Stripe) forces payment-method re-tokenization (often a customer re-subscribe),
subscription migration, and a tax-registration transition. Choose deliberately; migrate only for a real
structural reason (outgrowing B2B support, fee at scale, vendor risk).

If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Gotchas

> *Best-effort from research (2026-06) — fees and tax coverage change frequently; verify on each provider.*

1. **Stripe Tax ≠ tax compliance.** It calculates rates but does **not** remit or take liability — with bare
   Stripe you are the seller of record and must register + file + remit yourself.
2. **The fee gap narrows internationally.** Stripe's effective international rate (intl card + FX + Stripe
   Tax) approaches a MoR's ~5%, before counting your compliance labor.
3. **Lemon Squeezy lacks enterprise billing.** No purchase orders / net terms — a wall for B2B selling to
   larger companies; Paddle (or Stripe Invoicing) is the move there.
4. **Polar's headline fee is ~10% + processing** — much higher than Paddle/LS; great DX, but model the cost.
5. **Newer MoRs (Creem) carry vendor + coverage risk.** Lowest fee, but thinner tax-jurisdiction coverage and
   longevity uncertainty — fine for indie, riskier for a business you're betting on.
6. **Switching is expensive and customer-visible.** Re-tokenization can force re-subscribes; plan migrations
   carefully and rarely.
7. **MoRs control payouts + acceptable use.** You're paid on their schedule (not instant), and high-risk
   categories can be declined at onboarding — verify your product is allowed before committing.

## Related skills

- `/sales-paddle` — Paddle platform help (MoR API/webhooks, Billing vs Classic, tax/fee model)
- `/sales-fastspring` — FastSpring platform help (enterprise-heritage MoR — REST API/HMAC webhooks, Store Builder Library, B2B invoicing/quotes; quote-based ~5.9%+$0.95 / 8.9% fee)
- `/sales-dodo-payments` — Dodo Payments platform help (developer-first MoR — full REST API, 9 SDKs, framework adapters, Standard-Webhooks signing, CLI + MCP server; ~4% + $0.40/txn)
- `/sales-lemonsqueezy` — Lemon Squeezy platform help (MoR for indie/self-serve SaaS, license keys, API)
- `/sales-gumroad` — Gumroad platform help (creator MoR marketplace, digital products)
- `/sales-subscription-billing` — Choosing & operating a billing engine (Chargebee/Recurly/Maxio/Stripe Billing/Zuora/Orb/Lago) when you stay seller of record and keep tax in-house — the *other* billing decision next to MoR
- `/sales-chargebee` — Chargebee platform help (subscription-billing engine on your own gateway — NOT a MoR; API/webhooks, dunning, proration, RevRec)
- `/sales-checkout` — Checkout-conversion optimization across tools (order bumps, upsells, cart recovery)
- `/sales-membership` — Subscription retention, churn, and dunning strategy
- `/sales-marketplace-payouts` — Paying out many suppliers in a two-sided marketplace (the supply side)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: MoR vs Stripe for a global SaaS
**User says**: "I'm launching a SaaS selling worldwide. Stripe is cheaper — why would I pay 5% for Paddle or Lemon Squeezy?"
**Skill does**: Explains the MoR value: with Stripe you're the seller of record and must register, calculate, file, and **remit** VAT/GST/sales-tax in every jurisdiction (Stripe Tax only calculates). For a global product with no finance team, a MoR's ~5% absorbs that entire burden + liability; the international effective Stripe rate also climbs toward ~5%. Recommends a MoR unless they have finance ops or are mostly domestic.
**Result**: A clear MoR-vs-DIY decision grounded in their geography and team.

### Example 2: Paddle vs Lemon Squeezy for B2B
**User says**: "B2B SaaS, some customers want to pay by invoice with net-30. Paddle or Lemon Squeezy?"
**Skill does**: Flags the decisive factor — **Lemon Squeezy has no purchase orders / net terms**, while Paddle supports B2B invoicing and has the deepest tax coverage. Recommends Paddle for B2B/enterprise selling, routes Paddle setup to `/sales-paddle`, and notes Lemon Squeezy stays great for the self-serve portion.
**Result**: Paddle recommended for the B2B requirement, with a setup hand-off.

### Example 3: Cheapest MoR for an indie hacker
**User says**: "Solo dev, tiny revenue, want a merchant of record but the fees hurt. Options?"
**Skill does**: Compares the low-fee end — **Creem** (lowest fee, newest, vendor risk) and **Lemon Squeezy** (proven, great DX) — vs **Polar** (best DX but ~10%). Recommends Creem or Lemon Squeezy for cost, with the caveat to verify Creem's tax coverage and longevity. Notes switching later is costly, so weigh stability.
**Result**: A fee-aware shortlist matched to an indie's risk tolerance.

## Troubleshooting

### "I got a surprise VAT/tax bill / a country says I owe tax"
**Symptom**: A tax authority (often EU VAT or a US state) claims you owe uncollected tax.
**Cause**: You were on a **processor** (Stripe/PayPal), so **you** were the seller of record and liable — Stripe Tax calculates but doesn't remit, and you hadn't registered/filed there.
**Solution**: This is the classic reason to move to a **MoR** (Paddle/Lemon Squeezy/etc.), which becomes the seller of record and remits going forward. For past liability, consult a tax professional; for the future, a MoR removes the registration/remittance burden. If staying on Stripe, add a tax engine (Anrok/Avalara) and register where you have nexus.

### "Which is actually cheaper — MoR or Stripe?"
**Symptom**: The 5% MoR fee looks far worse than Stripe's 2.9%.
**Cause**: Comparing headline rates only, ignoring international surcharges and your own compliance cost.
**Solution**: Compute Stripe's **effective international rate** (intl card +1.5%, FX +1%, Stripe Tax +0.5% ≈ ~4.9%) and add the labor/accountant cost of registrations + filings. Against that, a MoR's all-inclusive ~5% is often a wash or cheaper once compliance work is priced in — especially for a small team selling globally.

### "Should I switch providers?"
**Symptom**: Tempted to move for a lower fee or missing feature.
**Cause**: Switching MoRs/processors forces payment re-tokenization (possible customer re-subscribe), subscription migration, and tax-registration changes — real cost and churn risk.
**Solution**: Switch only for a structural reason (outgrowing B2B/invoicing support, fee material at scale, vendor risk), not a small fee delta. Quantify the migration cost and expected churn before moving; otherwise optimize within your current provider.
