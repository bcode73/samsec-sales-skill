---
name: sales-xperiencify
description: "Xperiencify platform help — gamified online course/membership platform (xperiencify.com) whose Experience Engine (XP points, badges, leaderboards, variable rewards, countdowns) is built to drive course completion. Public REST API (api.xperiencify.io, ?api_key= query auth; ~18 endpoints — enroll/remove/suspend students, tags, custom fields, and redeem/unredeem XP/XXP/BP points) plus Zapier (4 triggers / 8 actions), Pabbly, Make, and webhook export; Stripe/PayPal. Use when auto-enrolling buyers from an external cart via the API or Zapier, syncing course-completion or canceled-subscription events into a CRM, awarding gamification points programmatically, students not finishing your course, the API feeling complicated, hitting active-monthly-student plan limits, affiliates not getting paid out automatically, or choosing Growth vs Pro vs Lifetime. Do NOT use for course/membership strategy across tools (use /sales-membership) or checkout optimization across platforms (use /sales-checkout)."
argument-hint: "[describe what you need help with in Xperiencify]"
license: MIT
version: 1.0.0
tags: [sales, membership, courses, platform]
---

# Xperiencify Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Enroll/remove a student from an external purchase or app (API create-student or Zapier action)
   - B) Route events out — Student Added, Student Completed Course, Canceled Subscription, Tag Added — into a CRM, ESP, or Slack (Zapier trigger / webhook export)
   - C) Award or claw back gamification points programmatically (`redeem_points`/`unredeem_points`)
   - D) Configure a module — gamification engine, courses, community, certificates, email, affiliates
   - E) Pick a plan — Growth ($99) vs Pro ($199) vs Lifetime ($1,499), or understand active-monthly-student limits
   - F) Fix a problem — low completion, complicated API, affiliate payouts, billing/student-count surprises

2. **Where does data need to flow?** Into Xperiencify (enroll, tag, award points) → API write / Zapier action. Out of Xperiencify (sync a student, route a completion) → Zapier trigger / webhook export.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Course/membership strategy, retention, completion design, or platform comparison | `/sales-membership {question}` |
| Email sequence/broadcast strategy (in Xperiencify or a connected ESP) | `/sales-email-marketing {question}` |
| Email deliverability / inbox placement | `/sales-deliverability {question}` |
| Checkout / order-bump / upsell optimization across tools | `/sales-checkout {question}` |
| Designing an affiliate program (commission structure, recruiting) across tools | `/sales-affiliate-program {question}` |
| Webinar-based launch strategy | `/sales-webinar {question}` |

When routing, give the exact command, e.g. "This is a retention question — run: `/sales-membership how do I reduce course churn`".

## Step 3 — Xperiencify platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API-accessible vs Zapier vs UI-only), plan gates (the **active-monthly-student** metering, published-course caps, Growth/Pro/Lifetime tiers), the payment model (Stripe for subscriptions/installments, PayPal one-time only), the student/course/points data model with JSON shapes, and quick-start recipes (enroll from an external cart; sync completions to a CRM; award bonus XP from another tool).

**Read `references/xperiencify-api-reference.md`** for the integration surface — base URL `https://api.xperiencify.io`, `?api_key=` query auth (key from Account → Advanced), the full endpoint inventory (student create/info/update/customfield/remove, tag manager, account-level course/student reads, and the gamification `redeem_points`/`unredeem_points`), plus the Zapier 4-trigger / 8-action surface and webhook-export pattern.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Think in two surfaces.** The REST API is best for direct, code-driven writes (enroll, tag, award points) and progress reads. Zapier (also Pabbly/Make) is best for no-code eventing and is slightly **broader** than the API (Suspend/Unsuspend students are Zapier actions). For systems Zapier can't reach, chain Webhooks by Zapier.
- **Identity is email.** Create-student makes an account if none exists and returns a magic link; `update` can change everything **except** the email. Match/dedupe on email everywhere.
- **The API key lives in the URL.** It's generated at Account → Advanced and passed as `?api_key=`. Treat it like a password — server-side only, never in client code or anything that logs full URLs.
- **Gamification is the product — and it's automatable.** Points come in three currencies (XP, XXP/variable, BP/badge). The `redeem_points` endpoint takes `student_ids`/`course_ids` arrays, so resolve IDs via `GET /coach/students/` first.
- **Size the plan to peak _monthly active_ students, not total enrolled.** A launch spike can push you over a tier even if lifetime enrollment is modest.
- **Affiliates are tracked, not paid.** Built-in tracking is a `?ref=` link recorded against the sale + CSV export; payouts are manual. For a real engine, run payouts from the export or bolt on a tool (`/sales-affiliate-program`).

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently and conflict across sources.*

1. **Billing is by _active monthly students_, not total.** Dormant students don't count, but a login spike during a launch can bump you over a tier mid-month. Plan for peak monthly active.
2. **The API is deliberately thin and "programmer-required."** The docs themselves warn API work is complicated with limited support. Don't promise endpoints that aren't in the reference; for non-developers, push them to Zapier/Pabbly/Make instead.
3. **No published error schema, rate limits, or webhook signature.** Build idempotent handlers, retry on 429/5xx with backoff, and re-verify a student via `POST /student/info/` before granting access on a webhook (it isn't signed).
4. **PayPal is one-time only; Stripe drives subscriptions.** The Canceled-Subscription trigger fires on **Stripe** cancellations — PayPal recurring isn't supported.
5. **Affiliate payouts are manual.** There's no payout dashboard — only `?ref=` tracking + CSV export. Don't promise automatic commission payments.
6. **API key travels in the query string.** Anything that captures full URLs (logs, analytics, browser history) leaks it. Keep all calls server-side.
7. **Pagination isn't documented.** For large rosters use the in-app CSV export rather than paging `/coach/students/`; filter the API read with `&course_id=` when you can.
8. **Sparse third-party reviews.** Limited G2/Capterra/Trustpilot presence (App Store ~3.3/5) — evaluate via the free Sandbox plan before committing, not via review aggregate.

## Related skills

- `/sales-membership` — Course/membership strategy across tools (Xperiencify is one of the gamified-completion platforms covered), retention, completion design, and platform comparison
- `/sales-email-marketing` — Email sequence and broadcast strategy (in Xperiencify or the ESP you connect via Zapier)
- `/sales-affiliate-program` — Designing an affiliate program (commission structure, recruiting) — pairs with Xperiencify's manual `?ref=` tracking
- `/sales-checkout` — Checkout, order-bump, and upsell optimization (external carts that enroll into Xperiencify)
- `/sales-webinar` — Webinar-based selling and live launch events
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Auto-enroll a buyer from my external cart (developer/automation)
**User says**: "I sell my course on ThriveCart but host it in Xperiencify. How do I auto-enroll buyers?"
**Skill does**: Points to **Recipe 1** — trigger on the ThriveCart purchase, then either call `POST /api/public/student/create/?api_key=…` with the buyer's `student_email` + `course_id` (creates the account if new, returns a magic link to email them) or use the **Add Student to a Course** Zapier action for a no-code path. Notes identity is email, the key comes from Account → Advanced and must stay server-side, and that the create call's magic link gives password-less access.
**Result**: External purchases enroll students in Xperiencify automatically.

### Example 2: Get notified when someone finishes and push it to my CRM
**User says**: "When a student completes a course, I want them tagged in HubSpot and sent a certificate email."
**Skill does**: Uses the **Student Completed Course** Zapier trigger (or webhook export), maps `student_email` + `course_id` into a HubSpot create/update-contact action with a completion property, and fans out to a certificate/upsell email. Flags that the webhook isn't signed, so verify via `POST /student/info/` before anything sensitive, and routes nurture-sequence design to `/sales-email-marketing`.
**Result**: Completions flow into the CRM and trigger follow-up with zero manual entry.

### Example 3: My students aren't finishing the course
**User says**: "Completion is terrible — barely anyone gets past module 2."
**Skill does**: Frames this as Xperiencify's core job — explains the Experience Engine levers (XP/variable rewards on lesson completion, badges + leaderboards for momentum, countdowns for urgency, celebrations at milestones) and how to award bonus XP programmatically (Recipe 3) for off-platform wins. For the broader completion/retention playbook across tools, routes: "run: `/sales-membership my course completion rate is low`."
**Result**: A concrete gamification setup plus a route to deeper retention strategy.

## Troubleshooting

### My auto-enroll stopped adding students
**Symptom**: New buyers aren't being enrolled via the API or a Zap.
**Cause**: You've hit your plan's active-monthly-student capacity, the API key was regenerated, the wrong `course_id` is mapped, or (Zapier) the connection dropped.
**Solution**: Check your active monthly student count against the tier and upgrade if you're at the cap. Re-copy the key from **Account → Advanced** and reconnect. Confirm the create-student call/action targets the correct `course_id` and sends the buyer's exact `student_email`. Make the handler idempotent so retries don't double-enroll.

### The API call fails or behaves unexpectedly
**Symptom**: Requests error, time out, or you can't tell why a call didn't work.
**Cause**: The public API has no documented error schema or rate limits, and support for API issues is limited. Common culprits: key not appended as `?api_key=`, calling from the browser (key exposure / CORS), or sending `redeem_points` with an email instead of `student_ids`/`course_ids` arrays.
**Solution**: Call server-side with the key in the query string, resolve student IDs via `GET /coach/students/` before points operations, and retry 429/5xx with exponential backoff. If a no-code path is enough, switch to the Zapier/Pabbly/Make connector instead of raw API.

### I can't pay my affiliates automatically
**Symptom**: You expected commission payouts but there's no payout dashboard.
**Cause**: Xperiencify only **tracks** affiliates via a `?ref=affiliate_name` link recorded against the sale, surfaced in the Students page and CSV export — it does not run payouts.
**Solution**: Export the affiliate-attributed sales (filter by affiliate/course) and pay commissions manually via PayPal/Stripe/bank transfer. For a real affiliate engine with automated tracking and payouts, design the program with `/sales-affiliate-program` and consider a dedicated tool.
