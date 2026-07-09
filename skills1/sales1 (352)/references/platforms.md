# Merchant of Record (MoR) & Payments-Provider Comparison Reference

Detailed comparison for choosing how to bill global customers for SaaS/digital products. Best-effort from
research (2026-06) — **fees and tax coverage change frequently; verify on each provider's live pricing.**

## What "Merchant of Record" means

A **Merchant of Record (MoR)** is the legal seller of your product. The MoR — not you — is liable for
collecting and **remitting sales tax / VAT / GST** in every jurisdiction, handles payment processing, fraud,
chargebacks, and (usually) subscription billing. You get one payout and one relationship; they take a higher
fee in exchange for absorbing global tax compliance.

A **payment processor** (Stripe, PayPal) only moves money. **You** remain the seller of record and are
responsible for registering, calculating, collecting, and remitting tax everywhere you have nexus (Stripe
Tax *calculates* but does **not** remit or take liability).

**The core decision:** pay ~5% (MoR) to never think about global tax, or pay ~3% (processor) + the
operational + accounting cost of managing tax registration/remittance yourself.

## Decision matrix

| | Paddle | Lemon Squeezy | Polar | Creem | Stripe (+ Tax) |
|---|---|---|---|---|---|
| **Model** | MoR | MoR | MoR | MoR | Processor (you're seller) |
| **Headline fee** | ~5% + $0.50 | ~5% + $0.50 | ~10% + $0.50 + proc. | lower (~3.x% + $0.40) | ~2.9% + $0.30 |
| **Tax remittance** | ✅ (most mature, 300+ mkts) | ✅ (good; some CA/India edge cases) | ✅ (inherits Stripe Tax: US+EU) | ✅ (growing) | ❌ calc only, **you remit** |
| **B2B invoicing / PO / net terms** | ✅ strongest | ❌ limited | ❌ limited | ❌ limited | ✅ (Stripe Invoicing) |
| **Best fit** | mature/B2B SaaS, enterprise | simple self-serve SaaS ≤~$500k ARR | indie/dev tools, cheap start | indie/micro-SaaS, lowest MoR fee | scale + control, has tax/finance ops |
| **Owned by** | Paddle (acq. ProfitWell) | Stripe (acq. 2024) | independent | independent | Stripe |

## Paddle (detailed)

**Positioning:** The most mature MoR for SaaS/apps/games — deepest tax-jurisdiction coverage and the only
one with real **B2B invoicing / purchase-order / net-terms** support.
- **Fee:** ~5% + $0.50/transaction, all-inclusive (global tax handled).
- **Strengths:** broadest tax coverage (US states, EU VAT, UK, AU GST, parts of Asia); subscriptions depth;
  Retain (dunning); free ProfitWell Metrics; B2B/enterprise billing; mature API (**Paddle Billing**), signed
  webhooks, sandbox, Docs MCP.
- **Weaknesses:** higher fee than a bare processor; **Classic vs Billing** product split confuses new devs;
  acceptable-use review can decline high-risk categories; payouts on Paddle's schedule.
- **Best for:** SaaS scaling past self-serve into B2B/enterprise, or anyone who wants zero tax ops globally.
- **Platform skill:** `/sales-paddle`

## Lemon Squeezy

**Positioning:** Developer-friendly MoR for indie hackers and self-serve SaaS; clean UX, fast setup.
- **Fee:** ~5% + $0.50 (matches Paddle). Owned by **Stripe** since 2024.
- **Strengths:** simplest onboarding, nice DX/API, license keys, digital-product + subscription support,
  built-in affiliate management, email/checkout.
- **Weaknesses:** **no purchase orders / net terms / enterprise invoicing**; a few reported tax edge cases
  (Canadian provincial, Indian GST); roadmap uncertainty post-Stripe acquisition.
- **Best for:** self-serve SaaS and digital products up to ~$500k ARR with simple card-subscription billing.
- **Platform skill:** `/sales-lemonsqueezy`

## Polar

**Positioning:** Open-source-friendly MoR aimed at developers and devtool products.
- **Fee:** ~10% + $0.50 **plus** the underlying Stripe/PayPal processing fee — the highest here.
- **Strengths:** great DX, usage-based + digital products, open-source ethos, fast-moving.
- **Weaknesses:** highest effective fee; **inherits Stripe Tax** coverage (US + EU strong, rest expanding);
  lighter subscription/enterprise depth.
- **Best for:** developer-focused products that value DX/OSS and accept a higher fee for simplicity.

## Creem

**Positioning:** Newer low-fee MoR targeting indie/micro-SaaS.
- **Fee:** lower than Paddle/LS (≈3.x% + $0.40, verify) — undercuts the incumbents.
- **Strengths:** cheapest MoR option, indie-friendly, fast setup.
- **Weaknesses:** youngest/least proven; thinner tax-jurisdiction coverage and enterprise features; vendor
  longevity risk.
- **Best for:** cost-sensitive indie hackers who want MoR tax handling at the lowest fee and can tolerate a
  newer vendor.

## Dodo Payments

**Positioning:** Developer-first MoR for SaaS / AI / digital products — the most API/SDK-rich of the indie MoRs.
- **Fee:** ~4% + $0.40/txn, no monthly fee (verify); between Creem (~3.x%) and Paddle/LS (~5%).
- **Strengths:** deepest **developer experience** — full REST API, **9 SDKs** (TS/Python/Go/PHP/Java/Kotlin/C#/Ruby/RN), framework adapters (Next.js/Express/SvelteKit/…), **Standard Webhooks** signing, a **CLI**, and an **MCP server**; 220+ countries / 40+ methods; subscriptions + usage/credit billing + license keys; strong "AI-first"/indie positioning.
- **Weaknesses:** younger vendor (longevity/enterprise-coverage risk vs Paddle); confirm tax-jurisdiction depth + B2B invoicing if you need them.
- **Best for:** developers/AI-SaaS founders who want MoR tax handling **with a Stripe-grade API/SDK + MCP** and don't need Paddle's enterprise depth. **Platform skill:** `/sales-dodo-payments`.

## FastSpring

**Positioning:** Established, enterprise-heritage all-in-one MoR for **SaaS, downloadable software, games, and
digital goods** — deep B2B features and a long track record (3,200+ customers incl. Adobe, Intel, Rovio).
- **Fee:** **quote-based / negotiable** — no public rate card. Reported rates ≈ **8.9%** or **5.9% + $0.95** per
  transaction, assigned by their **sales team** based on transaction type + volume; no monthly fee, no minimum.
  **Effective subscription rates often reach ~10–12%+** on low/mid-ticket recurring charges.
- **Strengths:** mature MoR (tax remittance across 200+ regions / 35+ currencies); strong **B2B** — digital
  invoicing, **interactive quotes with e-signatures**, POs; built-in **affiliate** network; **Store Builder
  Library** (JS popup/embedded checkout); solid **REST API** (`api.fastspring.com`, HTTP Basic) + **HMAC-SHA256
  webhooks** (`X-FS-Signature`); Salesforce/HubSpot connectors.
- **Weaknesses:** **opaque quote-based pricing** slows evaluation; **keeps its fee on refunds** (top complaint);
  effective subscription cost is high for low-ticket plans; product/UX feels heavier for PLG teams; mixed support
  reviews; legacy **Classic API deprecated** (build on the modern API).
- **Best for:** software/SaaS/games sellers who want a **proven enterprise-grade MoR with B2B invoicing/quotes**
  and can negotiate a rate — less ideal for lowest-fee indie subscriptions. **Platform skill:** `/sales-fastspring`.

## Gumroad

**Positioning:** Creator-first MoR marketplace for digital products (less of a SaaS-subscription tool).
- **Fee:** flat ~10% + processing on most plans; acts as MoR (handles tax since 2025).
- **Best for:** creators selling ebooks/templates/courses/one-offs with a built-in discovery marketplace,
  not structured SaaS billing. **Platform skill:** `/sales-gumroad`.

## Stripe (+ Stripe Tax) — the DIY/self-managed path

**Positioning:** The dominant payment **processor** — maximum control + lowest processing fee, but **you are
the seller of record**.
- **Fee:** ~2.9% + $0.30 (US cards); +1.5% international, +1% FX, +0.5% Stripe Tax — international **effective
  rate climbs toward ~5%**, narrowing the gap to a MoR.
- **You handle:** tax **registration** in each jurisdiction, **filing**, and **remittance** (Stripe Tax only
  *calculates*); plus chargebacks and global compliance.
- **Best for:** companies with finance/tax operations (or a tax tool like Avalara/Anrok), or at a scale where
  the fee delta on a MoR is large and you can absorb the compliance burden. Stripe Billing/Invoicing is the
  strongest for complex B2B.

## Billing engines (Chargebee / Recurly / Maxio) — NOT a MoR, but adjacent

A **subscription-billing engine** sits **on top of** a processor (usually Stripe) and adds recurring-billing
depth — flexible catalog/pricing, dunning, proration, revenue recognition — but it is **NOT a Merchant of
Record**. With a billing engine you stay the **seller of record** and still own tax registration/remittance
(same liability as bare Stripe). It's the path for teams that want **billing depth while keeping tax in-house**
(or pairing with a tax engine like Anrok/Avalara).

- **Chargebee** — broadest subscription + usage billing, dunning (Smart Retry), proration, RevRec (add-on);
  orchestrates 40+ gateways. Free Starter (cumulative ~$250K cap → 0.75%), Performance ~$7,188/yr. **Platform
  skill:** `/sales-chargebee`.
- **Recurly** — churn/recovery-focused billing engine (from ~$149/mo + fees).
- **Maxio** — B2B SaaS billing tied to RevOps + revenue recognition (ex-Chargify + SaaSOptics).

**Decision shortcut:** want tax remittance off your plate → **MoR** (Paddle/LS/Polar/Creem/Dodo). Want billing
depth but keep tax in-house → **billing engine** (Chargebee/Recurly/Maxio) on your own gateway. For choosing
*among billing engines* (incl. Stripe Billing/Zuora/Orb/Lago), use **`/sales-subscription-billing`**.

## When to choose MoR vs self-managed (Stripe)

- **Choose a MoR (Paddle/LS/Polar/Creem)** when: you sell **internationally** and don't want to register/file
  VAT/GST/sales-tax in many jurisdictions; you're a small team without finance ops; you want one payout and
  zero tax liability. The ~5% fee buys away an entire operational + legal burden.
- **Choose Stripe (self-managed)** when: you have (or will hire) **tax/finance operations** or use a tax
  engine (Anrok/Avalara); you need maximum payment control, the lowest processing fee at scale, complex B2B
  invoicing, or you're mostly domestic (one tax jurisdiction).
- **Switching cost is real:** moving MoRs (or MoR→Stripe) means re-tokenizing payment methods (often a forced
  re-subscribe), migrating subscriptions, and a tax-registration transition. Pick deliberately; don't churn.

## Quick picks

- **Indie hacker, lowest fee, simple:** Creem or Lemon Squeezy.
- **Self-serve SaaS, great DX, will stay simple:** Lemon Squeezy.
- **Devtool/OSS audience, DX over fee:** Polar.
- **Scaling into B2B/enterprise, deepest tax coverage, invoicing:** Paddle.
- **Software/games/SaaS wanting a proven enterprise MoR with B2B quotes/invoicing (negotiate the rate):** FastSpring.
- **Creator selling one-off digital products:** Gumroad.
- **Have finance ops / need control / mostly domestic:** Stripe + Stripe Tax (self-managed).
- **Want billing depth but keep tax in-house (not a MoR):** Chargebee/Recurly/Maxio on your own gateway — choose among them with `/sales-subscription-billing`.
