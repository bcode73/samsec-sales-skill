---
name: sales-ruzuku
description: "Ruzuku platform help — course + membership platform for coaches, educators, and creators (ruzuku.com): course builder (video, quizzes, assignments, discussions), drip scheduling, certificates, live/cohort courses via Zoom, communities, and direct Stripe/PayPal with 0% transaction fees. No public REST API — automation is Zapier only (auth = API Key + API Secret + Site URL, free on every plan; 7 triggers incl. New Student Enrolled and Subscription Canceled, 3 actions: Enroll/Unenroll/Find a Student). Use when wiring a Ruzuku Zapier integration to enroll buyers from an external cart or sync students into a CRM/ESP, routing course-completion or cancellation events to follow-ups, setting up affiliate tracking (no dashboard — coupons or price points per affiliate), choosing Free vs Core vs Pro (certificates/white-label/storefront are Pro-gated), or the course builder feeling tedious. Do NOT use for course/membership strategy across tools (use /sales-membership) or checkout optimization (use /sales-checkout)."
argument-hint: "[describe what you need help with in Ruzuku]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
---

# Ruzuku Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/unenroll a student from an external purchase or app (Zapier action)
   - B) Route events out — New Student Enrolled, Course Completed, Subscription Canceled — into a CRM, ESP, or Slack (Zapier trigger)
   - C) Set up affiliate tracking (Ruzuku has no built-in affiliate dashboard)
   - D) Configure a module — courses, drip, quizzes/assignments, community, webinars, certificates
   - E) Pick a plan — Free (≤5 students) vs Core vs Pro (certificates, white-label, storefront, Zoom)
   - F) Fix a problem — tedious course builder, payments, student access, video limits

2. **Where does data need to flow?** Into Ruzuku (enroll a student) or out of Ruzuku (sync a student, route a completion) — this decides Zapier action vs trigger.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, completion, or platform comparison | `/sales-membership {question}` |
| Email sequence/broadcast strategy (in Ruzuku or a connected ESP) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Designing an affiliate program (commission structure, recruiting) across tools | `/sales-affiliate-program {question}` |
| Webinar-based launch strategy | `/sales-webinar {question}` |

When routing, give the exact command, e.g. "This is a retention question — run: `/sales-membership how do I reduce course churn`".

## Step 3 — Ruzuku platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's Zapier-accessible vs UI-only), plan gates (the Free 5-student cap and the Pro-gated certificates/white-label/storefront/Zoom), the payment model (direct Stripe/PayPal, 0% fees, coupons, price points), the student/course data model with JSON shapes, and quick-start recipes (enroll from an external cart; route new enrollments into a CRM/ESP; run dunning off Subscription Canceled).

**Read `references/ruzuku-api-reference.md`** for the integration surface — there's **no public REST API**; it documents the Zapier connection (API Key + API Secret + Site URL), the full 7-trigger / 3-action inventory, and the Webhooks-by-Zapier pattern for systems Zapier can't reach natively.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **No REST API — think in Zapier.** Push students in with the **Enroll a Student** action; pull events out with triggers (New Student Enrolled, Lesson/Course Completed, Subscription Canceled). For systems Zapier can't reach, chain **Webhooks by Zapier**. For bulk reads, use the in-app student CSV export.
- **Identity is email.** Enroll a Student creates an account if one doesn't exist; match/dedupe on email everywhere.
- **The Zapier credential is three parts** — API Key + API Secret + Site URL, generated at Account → Integrations → Configure Zapier. You enter them once in Zapier but keep them to reconnect; treat the secret like a password.
- **Affiliates are manual.** There's no affiliate dashboard. Give each affiliate a unique coupon or a dedicated price-point link, then export sales and pay commissions yourself. Fine up to a few dozen affiliates; for a real engine, bolt on a tool (`/sales-affiliate-program`).
- **0% transaction fees** on direct Stripe/PayPal — a genuine edge for low-margin creators vs platforms that take a cut.
- **Mind the plan gates.** Certificates, white-label/custom domain, public storefront, digital products, multiple instructors, AI transcription, and Zoom are **Pro-only**; the Free plan caps you at 5 students.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **No public REST API.** Don't promise API endpoints — the only programmatic surface is Zapier (+ Webhooks by Zapier). Plan around triggers and actions.
2. **Course-building is the top complaint.** The teacher-facing builder is praised as easy to launch but tedious to design — set expectations and lean on templates/reusable activities rather than custom layouts.
3. **Free plan caps at 5 students.** An auto-enroll Zap can silently hit the ceiling; size the plan to enrollment volume.
4. **Certificates, white-label, custom domain, storefront, and Zoom are Pro-only.** Don't promise them on Free/Core.
5. **No built-in affiliate dashboard.** Tracking is DIY via per-affiliate coupons or price points; affiliates have no self-serve stats page.
6. **Video upload caps per file** (≈2 GB on Free/Core, ≈4 GB on Pro). Long lessons should be split or hosted externally and embedded.
7. **The Zapier API Key + Secret are credentials.** They authorize student writes — store them securely, never client-side.
8. **Automated emails are basic.** Ruzuku sends course/announcement emails, but for real nurture/marketing sequences connect an ESP via Zapier.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (Ruzuku is one of the creator platforms covered), retention, completion, and platform comparison
- `/sales-email-marketing` — Email sequence and broadcast strategy (the ESP you connect to Ruzuku via Zapier)
- `/sales-affiliate-program` — Designing an affiliate program (commission structure, recruiting) — pairs with Ruzuku's manual coupon/price-point tracking
- `/sales-checkout` — Checkout, order-bump, and upsell optimization (external carts that enroll into Ruzuku)
- `/sales-webinar` — Webinar-based selling and live launch events (Ruzuku runs live sessions via Zoom)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Enroll a student when someone buys on my external cart (developer/automation)
**User says**: "I sell my course through ThriveCart but host it in Ruzuku. How do I auto-enroll buyers?"
**Skill does**: Points to the **Enroll a Student** Zapier action (Recipe 1): trigger on the ThriveCart purchase, map the buyer's `email` (+ name + target course) into Ruzuku's Enroll a Student action, which creates the account if needed. Notes identity is email, the Zapier credential is the API Key + Secret + Site URL from Account → Integrations → Configure Zapier, and that Zapier is free on every Ruzuku plan.
**Result**: External purchases enroll students in Ruzuku automatically.

### Example 2: Sync new enrollments into my CRM and email tool
**User says**: "When someone enrolls in Ruzuku, I want them added to HubSpot and tagged in Mailchimp."
**Skill does**: Uses the **New Student Enrolled** trigger (includes name, email, course, pricing/coupon) fanned out to a HubSpot create-contact action and a Mailchimp add/update-subscriber action (Recipe 2). Routes deeper sequence strategy: "For the nurture sequence itself — run: `/sales-email-marketing my new-student onboarding sequence`."
**Result**: Every enrollment flows into the CRM and ESP with zero manual entry.

### Example 3: Recover failed/canceled subscriptions
**User says**: "Can Ruzuku tell me when a subscription cancels so I can run a win-back?"
**Skill does**: Explains the **Subscription Canceled** trigger fires on recurring-payment cancellations; pipe it into a Zap that adds the student to a win-back email sequence or a CRM task (Recipe 3). Notes Ruzuku itself has no dunning engine, so retry/recovery logic lives in the connected ESP/CRM, and routes retention strategy to `/sales-membership`.
**Result**: Cancellations trigger an automated win-back instead of going unnoticed.

## Troubleshooting

### My auto-enroll Zap stopped adding students
**Symptom**: New buyers aren't being enrolled via Zapier.
**Cause**: You've hit the Free plan's 5-student cap, the Zapier connection's API Key/Secret expired or was regenerated, or the wrong course is mapped.
**Solution**: Check the enrolled-student count and upgrade to Core/Pro if you've hit the cap. Re-copy the API Key + API Secret + Site URL from **Account → Integrations → Configure Zapier** and reconnect the Zap. Confirm the Enroll a Student action targets the correct course and sends the buyer's exact `email`.

### Students can't get a certificate / my domain isn't branded
**Symptom**: No completion certificate option, or courses still show Ruzuku branding/URL.
**Cause**: Certificates, white-label branding, and custom domain are **Pro-plan** features.
**Solution**: Upgrade to Pro to unlock certificates, white-label, custom domain, public storefront, digital-product sales, multiple instructors, and Zoom. On Free/Core these are unavailable — don't promise them to students.

### Building the course feels slow and tedious
**Symptom**: Setting up modules, activities, and drip is taking far longer than expected.
**Cause**: Ruzuku optimizes the student experience over the author workflow — the builder is the most-cited friction point in reviews.
**Solution**: Start with one module live and build as you go rather than completing everything first. Reuse activities/templates across courses, keep lessons short (split videos over ~10 minutes), and lean on drip to stagger the work. For course-structure strategy, use `/sales-membership`.
