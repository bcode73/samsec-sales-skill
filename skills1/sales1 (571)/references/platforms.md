# Subscription & Usage-Billing Engines — Comparison Reference

Tool-agnostic comparison of recurring-billing engines. All of these run **on top of your own payment
gateway** (you stay seller of record) — none is a Merchant of Record. For the MoR decision (who *remits*
tax), see `/sales-merchant-of-record`.

> Best-effort from research (2026-06) — pricing and feature depth change; verify on each vendor's site.

## The distinctions that decide it

1. **Subscription-first vs usage-first.** Flat/per-seat/tiered recurring → almost any engine. Metered/usage
   as the *core* model → usage-native engines (Orb, Metronome, Lago, Maxio) beat subscription-first tools
   whose usage support is bolted on.
2. **Build-on-Stripe vs dedicated.** Stripe Billing is cheapest and zero-integration if you're already on
   Stripe and your pricing is simple. Dedicated engines orchestrate Stripe (or 40+ gateways) and add catalog
   flexibility, dunning depth, and RevRec.
3. **SaaS vs open-source/self-host.** Lago is open-source — no revenue tax, full control, but you own infra
   and upgrades.
4. **Do you need Revenue Recognition (ASC 606 / IFRS 15)?** Maxio and Zuora treat it as first-class;
   Chargebee offers it as a (separately-priced) add-on; Stripe Billing/Orb/Lago lean on external RevRec.

## Engine matrix

| Engine | Best for | Usage-based | Dunning | RevRec | Pricing model | Notes |
|--------|----------|-------------|---------|--------|---------------|-------|
| **Chargebee** | Subscription-first SaaS adding usage; full lifecycle | Yes (hybrid) | Smart Retry (decline-aware) | Add-on | Free Starter (cumulative $250K cap → 0.75%); Performance ~$7,188/yr caps $100K/mo; Enterprise custom | Broadest features; UI/setup involved. See `/sales-chargebee` |
| **Recurly** | High-volume subs prioritizing churn/recovery | Yes | Best-in-class dunning/recovery | Limited/partner | From ~$149/mo + fees | Revenue-recovery focus |
| **Maxio** | B2B SaaS tying usage billing to RevOps + RevRec | Yes | Yes | First-class (SaaSOptics lineage) | Custom | ex-Chargify + SaaSOptics merger |
| **Zuora** | Enterprise GAAP system of record, global | Yes | Yes | First-class | Enterprise custom | Most powerful + heaviest; long implementation |
| **Stripe Billing** | Simple subs already on Stripe | Basic/metered | Smart Retries | External | ~0.7% of billed volume | Cheapest, zero integration; shallow on catalog/RevRec |
| **Orb** | Usage metering as the product | Native (event metering) | Via gateway | External | Custom | Accurate metering first; pair with rest of stack |
| **Lago** | Open-source control, no revenue tax | Native | Yes | External | Open-source (self-host) or cloud | You own Postgres/Redis/upgrades |
| **Zoho Billing** | SMB already in Zoho | Yes (basic) | Yes | Basic | Low, suite-bundled | Tight Zoho integration; lighter on advanced needs |
| **Swell** (commerce platform, not a bolt-on engine) | Storefront + subscriptions in one — DTC/subscription brands | Limited | Yes (built-in) | External | $29–$2,250/mo (annual sales caps; no transaction fee) | Native subscription engine baked into an API-first commerce backend — pause/resume, separate billing/fulfillment schedules. Use *instead of* bolting Recharge/Chargebee onto a separate cart. See `/sales-swell`. Subscriptions gated to Basic+ |

**Adjacent metering tool:** **Metronome** — usage/event-metering and billing for usage-heavy infra/AI products
(similar lane to Orb). Worth a look when metering accuracy and scale dominate.

## How each handles the operational pieces

### Usage / metered billing
- **Native (meter ingestion + aggregation as core):** Orb, Metronome, Lago, Maxio.
- **Supported but secondary:** Chargebee, Recurly, Zuora, Stripe Billing (metered prices), Zoho.
- Whichever you pick, ingest usage events **idempotently and deduped** — double-counted events produce wrong
  invoices, and these are hard to claw back after a customer sees them.

### Dunning / failed-payment recovery
- **Recurly** is built around recovery; **Chargebee** has decline-type-aware **Smart Retry** (up to ~12
  attempts by decline type) plus a custom-retry mode (~5 scheduled attempts). Most subscription "churn" is
  **involuntary** — turn dunning on before reaching for discounts.

### Proration
- All prorate mid-cycle changes, but the **credit type/timing depends on invoice state** (paid → refundable
  credit on future invoices; unpaid → adjustment on the current invoice). Always **preview with the estimate
  API** and test on a sandbox/test clock before trusting amounts.

### Revenue Recognition (ASC 606 / IFRS 15)
- **First-class:** Maxio, Zuora. **Add-on:** Chargebee RevRec (priced separately). **External:** pair Stripe
  Billing/Orb/Lago with a RevRec tool or your accounting system.

## Migration cost (why not to switch lightly)

Switching engines forces: **payment-method re-tokenization** (gateway-dependent; can require customer
re-subscribe), **subscription + invoice-history migration**, **webhook + RevRec re-wiring**, and a parallel
run to reconcile. Migrate only for a structural reason — outgrowing the catalog, needing usage/RevRec, or fee
materiality at scale — not a small fee delta.

## Quick picks

- **On Stripe, simple subs, small team →** Stripe Billing.
- **Subscription-first SaaS adding usage, want full lifecycle →** Chargebee.
- **Churn/recovery is the priority →** Recurly.
- **B2B SaaS needing usage + RevOps/RevRec →** Maxio.
- **Enterprise GAAP system of record →** Zuora.
- **Usage metering is the product →** Orb or Metronome.
- **Open-source / data ownership / no revenue tax →** Lago.
- **SMB already in Zoho →** Zoho Billing.
- **Want subscriptions native in your storefront (one platform for commerce + billing, no bolt-on engine) →** a commerce backend with a built-in subscription engine like **Swell** (see `/sales-swell`), rather than wiring a standalone engine onto a separate cart.
- **Want tax remittance off your plate →** not a billing-engine decision; go to `/sales-merchant-of-record`.
