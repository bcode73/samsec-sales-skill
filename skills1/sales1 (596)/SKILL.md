---
name: sales-teachery
description: "Teachery (teachery.co) platform help — minimalist, design-first course builder for solopreneurs, designers, and coaches: course builder, drip, Course Hubs (memberships), digital downloads, branded Landing & Payment Pages, custom domains, and basic email — flat-rate with 0% transaction fees and unlimited courses/students. No public REST API; integration is an API key (Account → Integrations) for Zapier (3 triggers / 4 actions: enroll or revoke a Course or Theme), Make, and Pabbly. Use when auto-enrolling buyers from an external cart via Zapier, routing new-order or course-completion events into a CRM/ESP, revoking access when a subscription cancels, Teachery not hosting your videos (embed-only), missing quizzes or multiple instructors, the basic 3-type email needing a real ESP, setting up the built-in course affiliate feature, or choosing monthly vs annual vs lifetime. Do NOT use for course/membership strategy across tools (use /sales-membership) or email-marketing strategy (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in Teachery]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
github: "https://github.com/teachery"
---

# Teachery Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/revoke a student from an external purchase or app (Zapier Add/Revoke User to Course or Theme)
   - B) Route events out — Completed Course, New Lead, New Order — into a CRM/ESP/Slack (Zapier trigger)
   - C) Configure a module — courses/content blocks, drip, Course Hubs (Themes), Payment Pages, digital downloads, course affiliates
   - D) Decide on media — Teachery doesn't host video/files; pick an embed host (YouTube/Vimeo/Bunny/Drive)
   - E) Pick a plan — Monthly ($49) vs Annual ($470) vs Lifetime ($550); all flat-rate, unlimited, 0% fees
   - F) Fix a problem — embed/video issues, no quizzes/multi-instructor, basic email, no API

2. **Where does data need to flow?** Into Teachery (grant access) → Zapier **Add User to Course/Theme** action. Out of Teachery (sync an order, route a completion/lead) → Zapier trigger.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, completion, or platform comparison | `/sales-membership {question}` |
| Email sequence/broadcast strategy (Teachery's email is minimal — use a connected ESP) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Designing an affiliate program (commission structure, recruiting) across tools | `/sales-affiliate-program {question}` |
| Landing-page / funnel strategy across tools | `/sales-funnel {question}` |

When routing, give the exact command, e.g. "This is a retention question — run: `/sales-membership how do I reduce course churn`".

## Step 3 — Teachery platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's Zapier-accessible vs UI-only), the flat-rate pricing model (all features on every tier, unlimited everything, 0% fees), the **no-media-hosting** model (embed from external hosts), the order/enrollment data shapes, and quick-start recipes (enroll from a cart; route leads/orders to an ESP; revoke on cancellation).

**Read `references/teachery-api-reference.md`** for the integration surface — there's **no public REST API**; it documents the API-key-for-Zapier setup (Account → Integrations), the full 3-trigger / 4-action Zapier inventory (Course vs Theme enroll/revoke), the Make/Pabbly equivalents, and the Webhooks-by-Zapier bridge for systems the native connector can't reach.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **There's no REST API — think in Zapier.** Push students in with **Add User to Course** (or **Add User
  to Theme** for a membership hub); pull events out with **New Order**, **New Lead**, **Completed Course**.
  For systems Zapier can't reach, chain **Webhooks by Zapier**. Make/Pabbly are cheaper alternatives.
- **Identity is email.** Enroll actions create/locate the student by email — match and dedupe on it everywhere.
- **"Theme" means Course Hub.** Enroll/revoke comes in a per-Course and a per-Theme (membership) flavor;
  pick the one matching how you packaged the offer.
- **Plan for media hosting separately.** Teachery stores the *embed*, not the file — budget for Vimeo/Bunny
  (privacy + clean player) or use YouTube unlisted (free). A broken/region-blocked source breaks the lesson.
- **Connect an ESP for real email.** Built-in email is only welcome/completion/lesson-unlock; route New
  Order / New Lead into Kit/Mailchimp/ActiveCampaign for actual nurture.
- **The API key links the account once.** It's in Account → Integrations — paste it into Zapier carefully
  (no trailing spaces). It is not a REST credential.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **No public REST API.** The only programmatic surface is Zapier/Make/Pabbly (+ Webhooks by Zapier). Don't promise API endpoints — plan around triggers/actions.
2. **No native video/file hosting — embed only.** You host video/audio/PDF elsewhere (YouTube/Vimeo/Drive) and embed; that's a separate recurring cost and the top user complaint.
3. **No quizzes, no multiple instructors, no live sessions.** Teachery is deliberately minimal — if a course needs assessments, co-instructors, or live classes, it's the wrong tool.
4. **Email is basic (3 types only).** Welcome, completion, and lesson-unlock — connect an ESP for real campaigns; don't expect drip marketing from Teachery itself.
5. **Limited analytics.** Customer/sales analytics are basic and there's no list API — export CSV for deeper reporting.
6. **No native cancellation trigger.** Subscription-cancel handling lives in your payment processor; revoke access in Teachery via the **Revoke Course/Theme Access** action off the processor's event.
7. **Course Hubs are called "Themes" in Zapier.** Don't confuse the Add User to **Theme** action (membership) with Add User to **Course** (single course).
8. **API key paste errors.** A trailing space when copying the key from Account → Integrations breaks the Zapier connection — paste cleanly.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (Teachery is one of the minimalist creator platforms covered), retention, completion, and platform comparison
- `/sales-email-marketing` — Email sequence and broadcast strategy (the ESP you connect to Teachery via Zapier, since built-in email is minimal)
- `/sales-affiliate-program` — Designing an affiliate program (commission structure, recruiting) — pairs with Teachery's built-in course-affiliate feature
- `/sales-checkout` — Checkout, order-bump, and upsell optimization (external carts that enroll into Teachery)
- `/sales-funnel` — Landing-page and funnel strategy across tools (Teachery's Landing & Payment Pages)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Auto-enroll a buyer from my external cart (developer/automation)
**User says**: "I sell my course on ThriveCart but host it in Teachery. How do I auto-enroll buyers?"
**Skill does**: Explains Teachery has **no REST API**, so use Zapier (Recipe 1): trigger on the ThriveCart sale, map the buyer's `email` + first name + target course into the **Add User to Course** action (or **Add User to Theme** for a membership hub). Notes identity is email, the API key (Account → Integrations) links the account once (watch for trailing spaces), and Make/Pabbly are cheaper alternatives.
**Result**: External purchases enroll students in Teachery automatically.

### Example 2: Teachery won't host my course videos
**User says**: "Where do I upload my lesson videos in Teachery?"
**Skill does**: Clarifies Teachery **doesn't host media** — you embed from an external host. Recommends Vimeo or Bunny for privacy + a clean player (or YouTube unlisted for free), explains you paste the embed into a video content block, and flags that a broken/region-blocked source URL breaks the lesson. Notes this is a separate cost on top of the subscription.
**Result**: User hosts video externally and embeds it, with realistic cost expectations.

### Example 3: Send Teachery orders to my CRM and email tool
**User says**: "When someone buys my Teachery course, I want them in HubSpot and tagged in Kit."
**Skill does**: Uses the **New Order** Zapier trigger (with the optional Course/Theme filter) fanned out to a HubSpot create-contact action and a Kit add-subscriber action (Recipe 2). Notes Teachery's built-in email is only welcome/completion/lesson-unlock, so the real sequence belongs in Kit — routes: "run: `/sales-email-marketing my new-student onboarding sequence`."
**Result**: Every order flows into the CRM and ESP with no manual entry.

## Troubleshooting

### My auto-enroll Zap isn't adding students
**Symptom**: Buyers aren't getting course access via Zapier.
**Cause**: The API-key connection broke (trailing space when pasted), the wrong action was used (Course vs Theme), or the email field is empty/mismatched.
**Solution**: Reconnect Teachery in Zapier with a clean copy of the key from **Account → Integrations**. Confirm you're using **Add User to Course** for a single course or **Add User to Theme** for a membership hub, and that the buyer's exact `email` + first name are mapped. Check **Zap History** for the failing step.

### My course videos won't play / disappeared
**Symptom**: Lessons show broken or blank video.
**Cause**: Teachery doesn't host video — it embeds an external source. The source was deleted, set private, or region-blocked, or the embed code was pasted wrong.
**Solution**: Re-check the external host (YouTube/Vimeo/Drive) — confirm the video is public/unlisted and embedding is allowed, then re-paste the embed into the video block. For reliability and privacy, host on Vimeo or Bunny rather than a personal Drive link.

### I need quizzes / multiple instructors / real email automation
**Symptom**: A feature you expected isn't in Teachery.
**Cause**: Teachery is intentionally minimal — no quizzes, no multiple instructors, no live sessions, and only 3 automated email types.
**Solution**: For assessments or co-instructors, Teachery is the wrong fit — compare alternatives with `/sales-membership`. For email, connect an ESP (Kit/Mailchimp/ActiveCampaign) via the New Order / New Lead Zapier triggers and run sequences there (`/sales-email-marketing`).
