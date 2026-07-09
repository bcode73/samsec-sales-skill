---
name: sales-graphy
description: "Graphy platform help — all-in-one course/membership platform for creators (graphy.com; formerly Spayee): courses, memberships, communities, coaching, webinars, branded mobile apps, and AI tools. Developer surface: a REST API gated to the top plan (Merchant ID + API key auth; Create/Enroll Learner; Postman docs) plus webhooks (9 triggers incl. Success/Init Transaction — auto-disabled after 5 failures) and Zapier/Pabbly. Use when wiring a Graphy webhook or API integration to enroll buyers from an external cart, granting access on payment, syncing learners into a CRM, deciding between the API (top plan) and webhooks, evaluating mobile-app or transaction-fee plan gates, or troubleshooting slow post-sale support. Do NOT use for course/membership strategy across tools or platform comparison (use /sales-membership), email-marketing strategy (use /sales-email-marketing), or checkout optimization across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Graphy]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
---

# Graphy Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/create learners programmatically from an external cart or app (REST API — top plan)
   - B) Grant access or sync data on events via webhooks (any plan)
   - C) Route learner/transaction events into a CRM or ESP (Zapier/Pabbly)
   - D) Configure a module — courses, memberships, communities, coaching, webinars, branded app
   - E) Pick a plan — Launch vs Rise vs Scale (mobile apps, API, transaction fees)
   - F) Fix a problem — webhook disabled, slow support, fee confusion, mobile-app publishing

2. **Which plan are you on?** API access is gated to the top (Advanced/Scale) plan — this decides API vs webhooks/Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, or platform comparison | `/sales-membership {question}` |
| Email sequences and broadcasts (the ESP you connect) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Webinar funnel strategy | `/sales-webinar {question}` |

When routing, give the exact command, e.g. "This is a retention question — run: `/sales-membership how do I cut course churn`".

## Step 3 — Graphy platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (API/webhook/UI-only), the plan gates (mobile apps on Rise+, API on the top plan, the murky transaction-fee story), the learner/enrollment/transaction data model with JSON shapes, and quick-start recipes (enroll a buyer via the API; grant access on Success Transaction via webhook; sync new learners to a CRM via Zapier/Pabbly).

**Read `references/graphy-api-reference.md`** for the API + webhooks — the Merchant ID + API key auth (Integration API menu, Advanced plan only), the iPaaS operations (Create Learner, Enroll Learner to Course), the canonical Postman docs, and the full 9-trigger webhook list with the 5-failures-auto-disable behavior.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **API vs webhooks is a plan question.** The REST API needs the top (Advanced/Scale) plan; below that, integrate via webhooks + Zapier/Pabbly. Don't promise API access on Launch/Rise.
- **Auth is Merchant ID + API key.** Both come from the Integration API menu; treat the key as a secret. Confirm exact base URL/paths in the Postman collection — the public docs are JS-rendered.
- **Fulfill on Success Transaction, never Init Transaction.** Init fires when checkout starts; granting access on Init gives product to abandoned carts.
- **Watch the 5-failures rule.** A webhook auto-disables after 5 failed deliveries — keep the endpoint reliable and alert when one disables, or fulfillment silently stops.
- **Email is the learner identity.** Create Learner + Enroll Learner to Course key on email; dedupe on it.
- **Set support + mobile-app expectations.** Post-sale support is slow and on India timezone; branded apps are DIY and gated to Rise+. Verify the real transaction fee before pricing offers.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **API access is top-plan only.** The REST API (Integration API credentials) requires the Advanced/Scale plan. On lower tiers, plan around webhooks + Zapier/Pabbly.
2. **Webhooks auto-disable after 5 failures.** A flaky endpoint silently turns the webhook off — monitor and re-enable. This is the most common silent breakage.
3. **Init vs Success Transaction.** Use `Success Transaction` to fulfill; `Init Transaction` only means checkout started. Confusing them grants access to non-payers.
4. **Transaction fees are murky on lower tiers.** Graphy markets "0% platform fee," but third-party reviews report ~10% on Launch / ~5% on Rise. Verify the real cut before pricing.
5. **Branded mobile apps are DIY and gated to Rise+.** You build them in the no-code App Builder and publish under your own Apple/Google accounts — the "$49 plan with an app" expectation is wrong.
6. **Post-sale support is the top complaint.** Responsive pre-sale, slow afterward, India timezone. Don't promise fast fixes.
7. **Smaller ecosystem than Kajabi.** Fewer native integrations, tutorials, and advanced marketing tools — bridge marketing via Zapier/Pabbly + your ESP.
8. **Public API docs are JS-rendered.** Exact base URL/endpoint paths live in the Postman collection / your in-account Integration API page — don't assume paths.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (Graphy is one of the creator platforms covered), retention, and platform comparison
- `/sales-email-marketing` — Email sequence and broadcast strategy (the ESP you connect to Graphy)
- `/sales-webinar` — Live and evergreen webinar selling strategy
- `/sales-checkout` — Checkout, order-bump, and upsell optimization (external carts that feed Graphy)
- `/sales-deliverability` — Inbox placement and domain authentication for your connected ESP
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Enroll buyers from my external checkout into Graphy (developer/automation)
**User says**: "I sell on my own Stripe page but host the course in Graphy. How do I auto-enroll buyers?"
**Skill does**: Two paths by plan. On the **Advanced/Scale plan**, use the REST API (auth `mid` + `key` from Integration API): **Create Learner** then **Enroll Learner to Course**, mapping email → course URL (Recipe 1). Below that, register a **Success Transaction** webhook (or a Zap/Pabbly flow) and enroll in the handler (Recipe 2). Notes email is the identity key and to confirm exact endpoints in the Postman collection.
**Result**: User picks the API or webhook path based on their plan and auto-enrolls buyers.

### Example 2: My fulfillment webhook stopped firing
**User says**: "Access used to get granted automatically on purchase, now nothing happens."
**Skill does**: Explains Graphy **auto-disables a webhook after 5 failed deliveries** — a few endpoint errors will have turned it off. Walks through re-enabling (Integrations → Webhooks), adding endpoint monitoring/alerting, and confirming it's the **Success Transaction** event (not Init). 
**Result**: User re-enables the webhook and hardens the endpoint so it stops disabling.

### Example 3: Is Graphy's $49 plan enough for my branded app and clean payments?
**User says**: "I want a branded app and to keep 100% of revenue — is the Launch plan fine?"
**Skill does**: Clarifies the plan gates — **mobile apps are Rise+ (DIY build/publish), not Launch**, and the **0%-fee claim conflicts with third-party reports of ~10% on Launch / ~5% on Rise** — so verify the real fee on graphy.com/pricing before committing. Frames all pricing as best-effort. For choosing across platforms, routes to `/sales-membership`.
**Result**: User understands the true entry cost for an app + the fee uncertainty before buying.

## Troubleshooting

### Webhook stopped delivering / shows disabled
**Symptom**: Events that used to fire have silently stopped.
**Cause**: Graphy automatically disables a webhook after **5 failed delivery attempts**.
**Solution**: Re-enable it in Dashboard → Integrations → Webhooks, fix the endpoint (return 2xx fast), and add uptime monitoring/alerting so a few transient errors don't kill fulfillment. Remember only status + URL are editable; logs persist after deletion.

### Buyers get access before paying
**Symptom**: People who started but didn't finish checkout got enrolled.
**Cause**: You fulfilled on the **Init Transaction** event (checkout started) instead of **Success Transaction** (payment completed).
**Solution**: Switch the fulfillment trigger to **Success Transaction** and ignore Init, or check `status == "success"` in the payload before granting access.

### "Where's my API key / the API isn't available"
**Symptom**: No Integration API menu or credentials.
**Cause**: API access is gated to the **Advanced/Scale (top) plan**.
**Solution**: Upgrade to the top plan for the API + SSO, or integrate via webhooks + Zapier/Pabbly on your current tier (Create Learner / Enroll via the Zapier/Pabbly actions). Credentials live in Integration API once on the right plan.

### Support isn't responding after I bought
**Symptom**: Pre-sale was fast; post-sale tickets go quiet.
**Cause**: The most consistent Graphy complaint — slow post-sale support running on India timezone.
**Solution**: Set internal expectations (don't gate a launch on a fast Graphy reply), batch questions, and self-serve via the help center. For platform-selection second-guessing, use `/sales-membership`.
