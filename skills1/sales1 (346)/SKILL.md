---
name: sales-membervault
description: "MemberVault platform help — \"binge & buy\" course/membership platform for creators (membervault.co): host all paid + free products in one marketplace, gamification, warm/hot lead tagging, communities, drip content, and direct Stripe/PayPal with 0% fees. There is no public REST API — integration is Zapier (7 triggers incl. Hot Lead, 2 actions) plus inbound webhooks (grant access from an external cart) and outbound webhooks (push contacts to an ESP). Use when wiring a MemberVault webhook or Zapier integration to grant access on external purchase, routing hot leads into a CRM, connecting an email service because MemberVault doesn't send email, choosing a plan (Free 100-member cap vs 5/15/Unlimited), or hitting limits (video hosting, member cancellation, marketplace design). Do NOT use for course/membership strategy across tools or platform comparison (use /sales-membership), email-marketing strategy (use /sales-email-marketing), or checkout optimization across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in MemberVault]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
---

# MemberVault Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Grant/revoke product access from an external purchase (inbound webhook / Zapier action)
   - B) Route engagement signals out — Hot Lead, Completed Lesson, Earned EP — into a CRM or outreach tool
   - C) Connect an email service (MemberVault doesn't send email)
   - D) Configure a module — products, communities, gamification, drip, marketplace page
   - E) Pick a plan — Free (100-member cap) vs 5 / 15 / Unlimited
   - F) Fix a problem — video hosting, member cancellation, marketplace design, search

2. **Where does data need to flow?** Into MemberVault (grant access) / out of MemberVault (sync contact, route lead) — this decides inbound vs outbound webhook vs Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, or platform comparison | `/sales-membership {question}` |
| Email sequences and broadcasts (the ESP you connect) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Selling digital products (pricing, launch) across tools | `/sales-digital-products {question}` |

When routing, give the exact command, e.g. "This is a retention-strategy question — run: `/sales-membership how do I reduce course churn`".

## Step 3 — MemberVault platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's webhook/Zapier-accessible vs UI-only), the plan gates (the Free 100-member cap and the product-count tiers), the email/Stripe/PayPal model, the member/product data model with JSON shapes, and quick-start recipes (grant access via inbound webhook; route hot leads into a CRM; sync members to an unsupported ESP).

**Read `references/membervault-api-reference.md`** for the integration surface — there's **no public REST API**; it documents the inbound webhook ("API URL" from Integrations → Advanced), the outbound webhook ("Call a web hook" product action), and the full Zapier trigger/action list.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **No REST API — think in webhooks + Zapier.** Grant access with the inbound webhook (or the Zapier "Add User to Product" action); push data out with outbound webhooks (or Zapier triggers). For bulk reads, use the in-app CSV export.
- **Identity is email.** A member is one login; products attach to that email. Match/dedupe on email everywhere.
- **The "Hot Lead" trigger is the killer automation.** MemberVault tags users who repeatedly view the sales info of products they don't own — pipe the `Hot Lead` Zapier trigger into a CRM or outreach sequence to act on buying intent in real time.
- **MemberVault doesn't send email — connect an ESP.** Kit/MailerLite/ActiveCampaign integrate natively; others go through Zapier/webhooks. Factor the Zapier cost into thin margins.
- **Mind the Free-plan 100-member cap.** An auto-add Zap can silently hit it; size the plan to product count, not features (all plans have all features).
- **0% transaction fees** on direct Stripe/PayPal — a real edge for low-margin creators vs platforms that take a cut.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **No public REST API.** Don't promise API endpoints — integration is Zapier + inbound/outbound webhooks only. Plan around those.
2. **It doesn't send marketing email.** Every "send a sequence" flow lives in a separate ESP. Connecting a non-native ESP usually means paying for Zapier, which eats margin — a top complaint.
3. **Free plan caps members at ~100.** Auto-add automations can hit the ceiling silently; watch member count.
4. **Video hosting is limited.** Most users host on YouTube/Vimeo/Wistia and embed rather than uploading to MemberVault.
5. **Member self-cancellation is clunky.** Subscribers often can't cancel cleanly on their own — document the steps or handle cancellations in your payment processor to avoid disputes.
6. **Marketplace page design is fairly fixed.** Don't promise heavy visual customization; the trade-off for the binge-&-buy layout is limited styling.
7. **Search is weak with a big library.** Lean on marketplace structure, products, and tags rather than search for discovery.
8. **Inbound webhook URL is the credential.** It embeds account routing — treat it as a secret; don't expose it client-side.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (MemberVault is one of the creator platforms covered), retention, and platform comparison
- `/sales-email-marketing` — Email sequence and broadcast strategy (the ESP you connect to MemberVault)
- `/sales-digital-products` — Selling digital products: pricing, packaging, launch
- `/sales-checkout` — Checkout, order-bump, and upsell optimization (external carts that feed MemberVault)
- `/sales-deliverability` — Inbox placement and domain authentication for your connected ESP
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Grant course access when someone buys on my external cart (developer/automation)
**User says**: "I sell via Gumroad but host the course in MemberVault. How do I auto-grant access on purchase?"
**Skill does**: Points to the **inbound webhook** (Recipe 1): copy the "API URL" from Integrations → Advanced, then have Gumroad's Ping/Zapier POST `email` + the product/`course_id` to it on each sale. Notes the URL is the credential (keep it secret), identity is email, and the alternative is the Zapier "Add User to Product" action.
**Result**: External purchases grant MemberVault access automatically.

### Example 2: Act on buying intent — route hot leads to my CRM
**User says**: "Can MemberVault tell me who's about to buy, and push them somewhere I can follow up?"
**Skill does**: Explains the binge-&-buy engine tags users who keep viewing sales info of products they don't own as warm/hot leads, then shows the **Hot Lead** Zapier trigger → CRM/outreach handler (Recipe 2). Frames it as MemberVault's standout automation.
**Result**: Hot leads flow into the user's CRM in real time for follow-up.

### Example 3: Why aren't my members getting emails?
**User says**: "I set up my membership in MemberVault but no welcome emails are going out."
**Skill does**: Clarifies MemberVault **doesn't send email** — it needs a connected ESP (Kit/MailerLite/ActiveCampaign native, others via Zapier/webhooks). Shows wiring the `User Added to a Product` trigger (or outbound webhook) to the ESP, then routes deeper sequence strategy: "For the sequence itself — run: `/sales-email-marketing my membership welcome sequence`."
**Result**: User connects an ESP and understands MemberVault's role vs the ESP's.

## Troubleshooting

### Access isn't being granted after an external purchase
**Symptom**: A buyer pays on the external cart but can't log into the product.
**Cause**: The inbound webhook URL is wrong/expired, the wrong product/`course_id` is referenced, or the email sent doesn't match.
**Solution**: Re-copy the API URL from **Integrations → Advanced**, confirm the `course_id` matches the target product, and ensure the cart sends the buyer's exact `email`. Check the webhook activity log for the delivery, and test with a request-bin to inspect what the cart actually sends.

### Members aren't getting any email
**Symptom**: No welcome/drip emails after signup.
**Cause**: MemberVault has no built-in email — nothing sends unless an ESP is connected.
**Solution**: Connect Kit/MailerLite/ActiveCampaign natively, or bridge others via Zapier/webhooks. Trigger the ESP off `User Added to a Product` (Zapier) or an outbound webhook. Build the actual sequence in the ESP (`/sales-email-marketing`).

### My auto-add automation stopped adding members
**Symptom**: New signups via Zap aren't being created.
**Cause**: You've hit the Free plan's ~100-member cap (or a product-count limit on a paid tier).
**Solution**: Check member/product counts. Upgrade to the tier whose product/community counts fit; remember all plans include all features, so you're only paying to raise limits.

### A member says they can't cancel their subscription
**Symptom**: Churn requests come to you manually; members can't self-serve.
**Cause**: MemberVault's self-cancellation flow is limited.
**Solution**: Document the cancellation steps for members, or cancel the subscription directly in your Stripe/PayPal dashboard. For retention strategy (winning them back before they churn), use `/sales-membership`.
