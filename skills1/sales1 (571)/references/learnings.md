# Subscription & Usage-Billing Engine Learnings

Accumulated tips, gotchas, and corrections discovered during use. Claude reads this at the start of each invocation and appends new learnings as they're discovered.

<!-- Add entries below in format: **YYYY-MM-DD**: Learning description -->

**2026-06-29**: Research baseline — engine landscape (Chargebee, Recurly, Maxio, Zuora, Stripe Billing, Orb, Lago, Zoho Billing; adjacent: Metronome), the four deciding distinctions (subscription-first vs usage-first; build-on-Stripe vs dedicated; SaaS vs open-source self-host; RevRec need), and operational realities (involuntary churn → dunning, proration credit type depends on invoice state, idempotent/deduped usage metering) captured from comparison sources on this date. None of these are Merchant of Record — that's a separate decision (`/sales-merchant-of-record`). Re-verify pricing and feature depth against each vendor before relying on them.
