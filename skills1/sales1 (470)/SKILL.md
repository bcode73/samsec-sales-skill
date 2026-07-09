---
name: sales-referral-factory
description: "Referral Factory (referral-factory.com) platform help — no-code referral program builder for SaaS, ecommerce, and service businesses: 100+ branded campaign templates, referral links + codes, reward issuing (cash, gift cards, Stripe credits/coupons, commissions, custom), fraud detection, and white-label. REST API (api.referral-factory.com/api/v2, Bearer token, POST /users with referrer attribution, PUT /users/qualification, /rewards endpoints), outbound + inbound webhooks (no documented HMAC), and native HubSpot/Salesforce/Stripe/Zapier/Make/n8n syncs. Use when adding referrers via the API and attributing the referrer, qualifying referred users to trigger rewards, reacting to webhooks, issuing or canceling due rewards, deciding referral vs affiliate, or choosing the Basic/Pro/Enterprise plan. Do NOT use for referral/audience-growth strategy across tools (use /sales-audience-growth), affiliate program design (use /sales-affiliate-program), or email deliverability (use /sales-deliverability)."
argument-hint: "[describe what you need help with in Referral Factory]"
license: MIT
version: 1.0.0
tags: [sales, audience-growth, referral, platform]
---

# Referral Factory Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Add referrers / referred users via the API (and attribute the referrer)
   - B) Qualify a referred user to make a reward become due, then issue/cancel rewards
   - C) Send users out (outbound webhook) or qualify them in (inbound webhook)
   - D) Pick + set up a campaign type — single/double-sided, invite-only, refer-to-win
   - E) Connect Referral Factory to a CRM/ESP/Stripe (native, Zapier, Make, n8n)
   - F) Decide referral vs affiliate, or measure whether referrals are incremental
   - G) Fix a problem — referrals not attributing, custom-domain fees, payout methods, plan limits

2. **API or no-code?** A code integration → REST API (`Authorization: Bearer`) + webhooks. No endpoint to host → native connectors or Zapier/Make/n8n.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Referral / audience-growth **strategy** across tools (which tool, viral mechanics, incrementality) | `/sales-audience-growth {question}` |
| Designing a commission-based **affiliate** program across tools | `/sales-affiliate-program {question}` |
| Email **deliverability** of referral/notification emails | `/sales-deliverability {question}` |
| Connecting Referral Factory to a CRM/ESP/Stripe generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-audience-growth measure whether my referral program is incremental vs organic word-of-mouth`".

## Step 3 — Referral Factory platform reference

**Read `references/platform-guide.md`** for the full reference — the campaign-type + module map (what's API vs widget vs UI-only), the user-based pricing model and plan-gated features, the user/campaign/reward data model with JSON shapes, and quick-start recipes (create + attribute a referrer; qualify to trigger a reward; issue a due reward).

**Read `references/referral-factory-api-reference.md`** for the integration surface — base `https://api.referral-factory.com/api/v2`, **Bearer** auth (one token per account), `POST /users` with the `referrer` field, `PUT /users/qualification`, the `/rewards/{due,issue,cancel,dashboard,issued}` endpoints, cursor pagination (`per_page` ≤250, `links.next`), the 600-calls/min limit, and the outbound/inbound webhooks (no documented HMAC).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Attribute the referrer on create.** `POST /users` makes a **Person Referring** by default; pass `referrer: {field: "code"|"id"|"email", value: ...}` to make it a **Person Invited** credited to that referrer. Omit it and the referral isn't attributed — the #1 integration bug.
- **Qualifying is what triggers rewards.** A referral only becomes a *qualified* referral (and a reward becomes *due*) when you call `PUT /users/qualification` (by id, code, or email+`campaign_id`) or send the inbound qualify webhook. Adding the user is not enough.
- **Rewards are a two-step flow.** Qualification makes a reward **due**; you then `POST /rewards/issue/{id}` to actually issue it (or `/rewards/cancel/{id}`). List what's owed via `GET /rewards/due/{metric}`.
- **Use webhooks, not polling.** Outbound fires on new user and on qualified referral — pipe those to your CRM/ESP. There's **no documented HMAC**, so treat the endpoint as a secret URL, dedupe, and re-verify via `GET /users/{identifier}` before paying out.
- **Mind the plan gates.** API/webhooks are on every plan, but **white-label, custom domain, and SSO need Pro**; custom HTML and on-prem need Enterprise. Pricing scales by **users** (Basic ~$200 / Pro ~$400 / Enterprise ~$1,000).
- **Payout reality.** Rewards go out as PayPal cash, gift cards (200+ countries), Stripe credits/coupons, commissions, or custom — **no direct bank transfer**; pick a reward type your audience can actually redeem.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — pricing/features verified against the marketing site + reviews; confirm specifics in-account.*

1. **Referrals don't attribute without `referrer`.** A bare `POST /users` is a standalone Person Referring; you must pass the `referrer` object (or route signups through the referral link) to credit the referrer.
2. **Adding ≠ qualifying.** Rewards only become due after `PUT /users/qualification` (or the inbound qualify webhook). Forgetting this is why "my referrals never trigger rewards."
3. **No documented webhook HMAC.** Don't trust an unsigned webhook blindly — secret URL, re-verify via the API, and make handlers idempotent (a new-user and a later qualified event can both arrive for the same person).
4. **One API token per account.** Generating a new token deactivates the old one — rotating a key breaks every existing integration using the previous token.
5. **Custom domain & white-label cost more.** Removing branding/using your own domain requires **Pro**; reviewers specifically flag custom-domain fees. Budget the plan, not just the base price.
6. **No direct bank payouts.** Rewards are PayPal/gift card/Stripe/commission/custom — some users want bank transfer and it isn't offered. Set reward expectations accordingly.
7. **Unique-link skepticism.** Some referred people sign up off-link (organic WOM) and it's hard to tell program-driven from organic — measure incrementality, don't assume every signup is the program's. Route the strategy question to `/sales-audience-growth`.
8. **Referral ≠ affiliate.** Referral Factory runs **customer referrals** (rewards/discounts); for a commission-based **affiliate/partner** program with a partner portal, compare dedicated tools via `/sales-affiliate-program`.
9. **`api.` host vs help-doc example.** The OpenAPI base is `api.referral-factory.com/api/v2`; one help article shows `referral-factory.com/api/v2`. Use the `api.` host and verify in-account.

## Related skills

- `/sales-audience-growth` — Referral / audience-growth strategy across tools (Referral Factory is one of the referral platforms covered) — viral mechanics, tool selection, incrementality
- `/sales-affiliate-program` — Designing a commission-based affiliate (partner) program across tools — the affiliate counterpart to Referral Factory's customer referrals
- `/sales-email-marketing` — Email sequences for the referral list you sync out of Referral Factory
- `/sales-integration` — Connecting Referral Factory to a CRM/ESP/Stripe via webhooks/Zapier/Make/n8n
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Add a referred user and attribute the referrer via the API (developer/automation)
**User says**: "When someone signs up through a friend's link in my app, how do I add them to my Referral Factory campaign and credit the friend?"
**Skill does**: Walks Recipe 1 — `POST /api/v2/users` with `campaign_id`, `first_name`, `email`, and the **`referrer` object** (`{field: "code", value: "<friend's code>"}`), authenticated by `Authorization: Bearer <token>`. Stresses that omitting `referrer` makes a standalone Person Referring (no attribution), and that you must later `PUT /users/qualification` to turn it into a qualified referral that makes a reward due. Notes the no-code native/Zapier path as an alternative.
**Result**: The friend is correctly credited and the referral is ready to qualify.

### Example 2: Qualify a referral and issue the reward
**User says**: "A referred trial converted to paid — how do I mark it qualified and pay the reward?"
**Skill does**: `PUT /api/v2/users/qualification` with `{email, campaign_id, qualified: true}` (or by `id`/`code`). Explains qualification makes the reward **due**; then `GET /rewards/due/{metric}` to find it and `POST /rewards/issue/{id}` to issue (or `/rewards/cancel/{id}`). Flags idempotency (re-verify before issuing) and that payout is PayPal/gift card/Stripe, not bank transfer.
**Result**: The converted referral is qualified and its reward issued through the API.

### Example 3: Referral or affiliate — which do I need?
**User says**: "Should I use Referral Factory or set up an affiliate program?"
**Skill does**: Distinguishes the models — Referral Factory runs **customer referrals** (existing customers refer friends for rewards/discounts), whereas an **affiliate/partner** program pays commissions to recruited promoters with a partner portal and tracking links. Recommends Referral Factory for customer word-of-mouth and routes the affiliate decision: "run: `/sales-affiliate-program design a commission-based affiliate program`." Notes Referral Factory *can* pay commissions but isn't a full affiliate-partner platform.
**Result**: User picks the right model and is handed to the right skill.

## Troubleshooting

### My referrals are added but never trigger a reward
**Symptom**: Users appear in the campaign but no reward ever becomes due.
**Cause**: The referred user was created but never **qualified** — adding a user does not qualify it, and rewards only become due on qualification.
**Solution**: Call `PUT /api/v2/users/qualification` with the user's `id`/`code` (or `email` + `campaign_id`) and `qualified: true`, or send the inbound qualify webhook with their code/coupon. Then `GET /rewards/due/{metric}` and `POST /rewards/issue/{id}`. Also confirm the original `POST /users` included the `referrer` so the referral is attributed in the first place.

### My reward webhook fired twice / paid out twice
**Symptom**: A referrer's reward was issued more than once.
**Cause**: A new-user event and a later qualified event (and retries) can arrive for the same person, and there's no HMAC to dedupe on a signature.
**Solution**: Make the handler **idempotent** — key on the user `id`/`code` (or the due-reward `id`), persist what you've already issued, and re-verify the user via `GET /users/{identifier}` before calling `POST /rewards/issue`. Restrict the webhook endpoint to a secret URL.

### I can't use my own domain / branding looks like Referral Factory
**Symptom**: Referral pages show Referral Factory branding or won't run on your domain.
**Cause**: White-label (remove branding) and custom domain are **plan-gated to Pro+**; custom HTML upload is Enterprise-only.
**Solution**: Upgrade to Pro for white-label + custom domain (or Enterprise for custom HTML). If you only need API/webhooks and reward logic, Basic already includes those — weigh the branding gates against cost (reviewers flag custom-domain fees), or compare alternatives via `/sales-audience-growth`.
