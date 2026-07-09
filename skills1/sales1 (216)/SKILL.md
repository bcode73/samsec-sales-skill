---
name: sales-groupapp
description: "GroupApp platform help — learning-focused community platform for creators and coaches (group.app): communities/channels plus a deep LMS (drag-and-drop curriculum builder, enforced completion, branded certificates, progress tracking), events, B2B group subscriptions, and 0% transaction fees via Stripe. Integration surface: an API token + webhooks + OAuth (login/SSO) plus Zapier (11 triggers incl. New Payment, Course completed, Membership Questionnaire; 10 actions incl. Enroll a member in a course); native Stripe/Zoom/email. Use when wiring a GroupApp Zapier or webhook integration to enroll buyers from an external cart, syncing course-completion or payment events to a CRM, running dunning on Payment Failed, generating an API token, or choosing GroupApp vs Circle/Skool/Mighty Networks. Do NOT use for community/course-platform strategy or comparison across tools (use /sales-membership), checkout-conversion optimization (use /sales-checkout), or email-marketing strategy (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in GroupApp]"
license: MIT
version: 1.0.0
tags: [sales, membership, community, platform]
---

# GroupApp Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/create members from an external cart or app (Zapier action / webhook / API token)
   - B) React to events — New Payment, Course completed, Payment Failed, Subscription canceled — into a CRM/ESP
   - C) Configure a module — communities/channels, the LMS/curriculum builder, certificates, events, group (B2B) subscriptions
   - D) Set up auth/SSO via OAuth, or generate an API token
   - E) Pick a plan / compare GroupApp vs Circle/Skool/Mighty Networks
   - F) Fix a problem — webhook payloads, dunning, segments, membership questionnaire

2. **Into or out of GroupApp?** Grant access/enroll (in) vs sync events to other tools (out) — this decides Zapier action vs webhook/trigger.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Choosing/comparing community or course platforms, retention strategy | `/sales-membership {question}` |
| Email sequences and broadcasts (the ESP you connect) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Wiring GroupApp into a CRM/warehouse or other tools | `/sales-integration {question}` |

When routing, give the exact command, e.g. "Platform comparison — run: `/sales-membership GroupApp vs Circle vs Skool`".

## Step 3 — GroupApp platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (Zapier/webhook/API vs UI-only), the plan gates and 0%-fee model, the member/enrollment/payment data model with JSON shapes, and quick-start recipes (enroll a buyer from an external cart; route Course completed to a CRM/credential system; run dunning on Payment Failed).

**Read `references/groupapp-api-reference.md`** for the integration surface — the API token (Admin → Settings & Data → Integrations), webhooks, OAuth, and the full verbatim Zapier trigger (11) + action (10) lists, plus the note that a full public REST endpoint reference wasn't found.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Think Zapier + webhooks + API token, not a documented REST API.** The richest documented surface is Zapier (11 triggers / 10 actions); webhooks push events; an API token (Admin → Settings & Data → Integrations) powers custom integrations. Confirm any direct REST endpoints in-account — they aren't publicly documented.
- **Identity is email.** Members, enrollments, and payments key on email — match/dedupe on it. **Segments** are the tag primitive that drives automations.
- **Fulfill on New Payment (success), not enrollment intent.** Use **Payment Failed** for dunning and **Subscription canceled** for win-back/access removal.
- **Lean into the LMS depth.** GroupApp's edge is the curriculum builder + enforced completion + branded certificates + B2B group subscriptions — that's why teams pick it over Circle/Skool.
- **0% GroupApp fee, but Stripe fees still apply.** Connect your own Stripe.
- **It doesn't send marketing email.** Drive an ESP off the payment/enrollment triggers.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **No published full REST endpoint reference.** Generate an API token and confirm endpoints in-account; for most automations use Zapier/webhooks. Don't assume REST paths.
2. **Webhook payload schemas aren't published.** Capture one delivery against a request bin (webhook.site) to confirm field keys before parsing.
3. **It's not an email tool.** No marketing-email sending — connect an ESP and trigger it off GroupApp events.
4. **Lighter branding/white-label than Circle, lighter gamification than Skool.** Choose GroupApp for LMS depth + community, not the flashiest design or game mechanics.
5. **Pricing entry point is fuzzy across sources** (~$24 vs $49 start). Verify the tier that includes advanced LMS, B2B group subscriptions, and branding before committing.
6. **0% is the GroupApp fee, not Stripe's.** Standard Stripe processing fees still apply.
7. **Fulfill on payment success, not enrollment.** Granting access on enrollment/intent rather than the New Payment event can give product away.
8. **Marketing/pricing pages are JS-rendered** — re-verify features/pricing live, not from cached third-party roundups.

## Related skills

- `/sales-membership` — Community/course platform strategy, retention, and choosing GroupApp vs Circle/Skool/Mighty Networks
- `/sales-email-marketing` — Email sequences for members (GroupApp doesn't send email — connect an ESP)
- `/sales-checkout` — Checkout, subscription, and upsell optimization (external carts that feed GroupApp)
- `/sales-integration` — Wiring GroupApp's API/webhooks/Zapier into a CRM, warehouse, or other tools
- `/sales-deliverability` — Inbox placement and domain authentication for your connected ESP
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Enroll buyers from my external cart into GroupApp (developer/automation)
**User says**: "I sell on Stripe/SamCart but deliver my course in GroupApp. How do I auto-enroll buyers?"
**Skill does**: Points to the Zapier **"Enroll a member in a course"** action (Recipe 1) triggered by the cart's purchase event, mapping buyer email → member and product → course (creates the member if new). Notes identity is email, to fulfill on payment success, and that an API token/webhook is the alternative for custom code.
**Result**: External purchases auto-enroll into the right GroupApp course.

### Example 2: Sync course completions to my CRM and issue a credential
**User says**: "When someone finishes a course in GroupApp I want it logged in my CRM."
**Skill does**: Explains GroupApp auto-issues branded certificates, then shows routing the **Course completed** trigger (Zapier or webhook) to your CRM/credential system (Recipe 2). Flags that webhook payload keys aren't published — capture one delivery to confirm fields.
**Result**: Completions flow to the CRM with a clear field-mapping caveat.

### Example 3: Should I use GroupApp or Circle/Skool?
**User says**: "I run a cohort coaching program — GroupApp, Circle, or Skool?"
**Skill does**: Frames GroupApp's edge (deep LMS/curriculum builder, enforced completion, branded certificates, B2B group subscriptions, 0% fees) vs Circle (branding/white-label) and Skool (gamification/discovery), then routes the full comparison: "run: `/sales-membership GroupApp vs Circle vs Skool for cohort coaching`." Flags pricing as best-effort.
**Result**: User gets GroupApp's positioning plus the strategy skill for the full decision.

## Troubleshooting

### I can't find GroupApp's REST API docs / which endpoint to call
**Symptom**: You want to call GroupApp directly from code but can't find a full endpoint reference.
**Cause**: GroupApp documents an API token and webhooks, but a comprehensive public REST reference wasn't found in research.
**Solution**: Generate an API token (Admin Panel → Settings & Data → Integrations → API Token → Generate New Token) and check the in-account API docs/help center for endpoints. For most flows, use the documented Zapier actions/triggers or webhooks instead of raw REST.

### My webhook fires but I can't map the fields
**Symptom**: You receive a GroupApp webhook but don't know the payload shape.
**Cause**: Payload schemas aren't published.
**Solution**: Point the webhook at a request bin (webhook.site) once, inspect the real JSON, then map fields (member email, course, amount) in your handler. Key on the member's email.

### Buyers paid but didn't get access (or got access without paying)
**Symptom**: Access and payment are out of sync.
**Cause**: Fulfillment was wired to enrollment/intent instead of a successful payment.
**Solution**: Grant access on the **New Payment** (success) trigger; use **Payment Failed** to start dunning and **Subscription canceled** to remove access / trigger win-back. For the dunning sequence itself, use `/sales-email-marketing`.

### Members aren't getting emails
**Symptom**: No welcome/nurture emails after joining or enrolling.
**Cause**: GroupApp doesn't send marketing email.
**Solution**: Connect an ESP and trigger it off the **New community member** / **Course enrollment** events (Zapier/webhook). Build the sequence in the ESP — see `/sales-email-marketing`.
