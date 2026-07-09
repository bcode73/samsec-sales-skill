---
name: sales-thrivecart
description: "ThriveCart (thrivecart.com) platform help — checkout/cart platform for creators selling digital products, courses & subscriptions — order bumps, 1-click upsells/downsells, A/B testing, dunning, and a built-in affiliate center; sold as a lifetime (one-time) license. Event-driven — standard webhooks + an Event Subscription API and a REST API (token/OAuth, 60 req/min); webhook auth is a shared secret (order.success and subscription events), not HMAC. Use when granting product/course access on an order.success webhook, the 'lifetime deal' surprising you with a $295/yr Pro+ renewal, affiliate/tax/dunning/custom-domain features missing on Standard, ThriveCart Learn being deprecated (move to ThriveAcademy/external LMS), files shared because there's no download protection, or choosing Standard vs Pro+ vs Ultimate. Do NOT use for checkout-conversion strategy across tools (use /sales-checkout), course/membership strategy (use /sales-membership), or affiliate-program design across tools (use /sales-affiliate-program)."
argument-hint: "[describe what you need help with in ThriveCart]"
license: MIT
version: 1.0.0
tags: [sales, checkout, payments, platform]
github: "https://github.com/thrivecart"
---

# ThriveCart Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Grant product/course access (or revoke) from purchase events via webhook/API
   - B) Route purchases into a CRM/ESP (Zapier or native integration)
   - C) Understand pricing — Standard vs Pro+ vs Ultimate, the $295/yr renewal, what's gated
   - D) Deal with ThriveCart Learn deprecation (move courses to ThriveAcademy or an external LMS)
   - E) Configure a module — bumps, upsells/downsells, A/B test, dunning, affiliate center
   - F) Fix a problem — webhook auth, duplicate orders, missing features, no download protection

2. **Webhook or REST?** Reacting to a purchase → **webhooks** (standard = all events; Event Subscription API = targeted). Pulling/reconciling history → **REST API** (token, 60 req/min).

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Checkout-conversion strategy across tools (which cart, AOV optimization) | `/sales-checkout {question}` |
| Course/membership strategy or picking an LMS (Learn replacement) | `/sales-membership {question}` |
| Designing an affiliate program across tools (commissions, recruiting) | `/sales-affiliate-program {question}` |
| Subscription churn / dunning strategy across tools | `/sales-membership {question}` |
| Connecting ThriveCart to other tools generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a cart-selection question — run: `/sales-checkout ThriveCart vs SamCart for my course business`".

## Step 3 — ThriveCart platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API/webhook vs UI-only), the **lifetime-pricing model with the Pro+ $295/yr renewal** and what each tier gates, the order/subscription data model with JSON shapes, and quick-start recipes (grant access on purchase; send orders to a CRM; reconcile via REST).

**Read `references/thrivecart-api-reference.md`** for the integration surface — API-token vs OAuth auth, the **60 req/min** limit, **standard webhooks vs the Event Subscription API**, the event-type list (`order.success`, `order.subscription_*`, `affiliate.*`), the webhook payload shape, and **secret-based webhook validation** (no HMAC).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Drive everything off purchase events.** Grant access on `order.success`; revoke on `order.refund` /
  `order.subscription_cancelled`. Use **standard webhooks** for everything, or the **Event Subscription API**
  to receive only the events you care about.
- **Validate the secret — there's no HMAC.** ThriveCart authenticates webhooks with a shared
  **`thrivecart_secret`** you configure; reject any POST whose secret doesn't match, keep it private, and
  **dedupe on `order_id`** since events can repeat.
- **Match on product id, not name.** Names change; the numeric `base_product` (and bump/upsell ids) are stable.
- **"Lifetime" has a $295/yr asterisk.** Affiliates, sales tax, dunning, custom checkout domain, and advanced
  reporting are **Pro+** ($295/yr from year 2). Standard is genuinely one-time but minimal — budget the renewal.
- **Don't build on ThriveCart Learn.** It's deprecated (no new features) — deliver courses via **ThriveAcademy**
  or grant access to an external LMS off the purchase webhook. (LMS choice → `/sales-membership`.)
- **Protect delivery yourself.** ThriveCart has **no download/link protection** — gate files behind login in
  your own app/LMS rather than emailing a shareable link.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially pricing and the Learn deprecation, which change.*

1. **"Lifetime" isn't fully lifetime.** Pro+ (affiliates, tax, dunning, custom domain, advanced reporting) **renews at $295/yr** from year 2 — model real cost, not just the one-time headline.
2. **ThriveCart Learn / Learn+ are deprecated.** No new features; **ThriveAcademy** replaces them. Don't build new course delivery on Learn.
3. **No download/link protection.** Delivered file links can be shared freely — gate real access in your own app off `order.success`.
4. **Webhook auth is a shared secret, not HMAC.** Validate `thrivecart_secret` on every call and keep it private; there's no signature header.
5. **Events can repeat — dedupe on `order_id`.** Don't double-provision; make handlers idempotent.
6. **Standard plan is bare.** No affiliate center, sales tax, dunning, or custom checkout domain — those need Pro+.
7. **60 requests/minute per account** on the REST API — batch/reconcile within that, back off on limits.
8. **History of instability + billing bugs.** Ownership changes caused past downtime/Stripe issues; reportedly stabilized, but test the full purchase + billing flow before a launch.

## Related skills

- `/sales-samcart` — SamCart platform help (the subscription-priced competitor: modern templates, Subscription Saver dunning, Affiliate Center on Pro; $79–199/mo vs ThriveCart's lifetime license)
- `/sales-checkout` — Checkout-conversion strategy across tools (ThriveCart vs SamCart vs Lemon Squeezy; order bumps, upsells, cart recovery)
- `/sales-membership` — Course/membership strategy + picking an LMS (the ThriveCart Learn replacement decision)
- `/sales-affiliate-program` — Designing an affiliate program across tools — pairs with ThriveCart's built-in Affiliate Center (Pro+)
- `/sales-email-marketing` — Post-purchase email sequences off ThriveCart purchase events
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Grant course access when someone buys (developer/automation)
**User says**: "When someone buys my course on ThriveCart, auto-enroll them in my external LMS."
**Skill does**: Walks Recipe 1 — handle the **`order.success`** webhook, **validate the `thrivecart_secret`** (no HMAC), then grant access by the buyer's email + numeric `base_product` (match on id, not name); revoke on `order.refund`/`order.subscription_cancelled`. Notes deduping on `order_id`, using the **Event Subscription API** to receive only `order.success`, and that ThriveCart Learn is deprecated so an external LMS or ThriveAcademy is the path.
**Result**: Purchases auto-enroll buyers reliably.

### Example 2: Why is my "lifetime" cart asking for $295/year?
**User says**: "I bought ThriveCart as a one-time deal — why am I being charged $295/year now?"
**Skill does**: Explains the 2025 model change — the base **Standard ($495)** is one-time, but the creator essentials (**affiliate center, sales tax, dunning, custom checkout domain, advanced reporting**) are **Pro+**, which **renews at $295/yr** from year 2. Helps them decide whether they need Pro+ features or can stay on Standard, and frames pricing as best-effort to verify live.
**Result**: User understands the real cost structure.

### Example 3: My customers are sharing the download link
**User says**: "People are passing around the file link to my paid PDF from ThriveCart."
**Skill does**: Identifies that ThriveCart has **no download/link protection** — a known limitation. Recommends gating the file behind login in your own app/membership/LMS, granting access off the **`order.success`** webhook (and revoking on refund), rather than delivering a raw shareable link. Routes membership/LMS setup to `/sales-membership`.
**Result**: Files are protected behind authenticated access tied to the purchase.

## Troubleshooting

### My webhook fires but I can't trust it / anyone could POST to it
**Symptom**: You're unsure a webhook really came from ThriveCart.
**Cause**: ThriveCart doesn't sign webhooks with HMAC — authenticity is a shared **secret** you set in the webhook config.
**Solution**: Configure a secret on the notification, and on every inbound POST reject any request whose **`thrivecart_secret`** doesn't match. Keep the secret out of client code/logs. Also dedupe on `order_id` so retries don't double-provision.

### Access isn't granted (or is granted twice) on purchase
**Symptom**: Buyers don't get access, or get provisioned multiple times.
**Cause**: Listening to the wrong event, matching on product **name** (which changes), or not handling repeated deliveries.
**Solution**: Grant on **`order.success`** (revoke on `order.refund`/`order.subscription_cancelled`), match the offer by the stable numeric **`base_product`**/bump/upsell id, and make the handler **idempotent on `order_id`**. Reconcile periodically via the REST API to catch missed webhooks (mind the 60/min limit).

### Features I expected are missing / it's costing more than "lifetime"
**Symptom**: No affiliate center, tax, dunning, or custom domain; surprise annual charge.
**Cause**: You're on **Standard** (those are **Pro+**), and Pro+ renews **$295/yr** from year 2 — the "lifetime" deal is partial.
**Solution**: Upgrade to **Pro+** for affiliates/tax/dunning/custom-domain/advanced reporting if you need them, and budget the $295/yr. If your courses are on **Learn**, plan a move to **ThriveAcademy** or an external LMS, since Learn is deprecated.
