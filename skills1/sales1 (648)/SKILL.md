---
name: sales-viral-loops
description: "Viral Loops (viral-loops.com) platform help — referral & viral-marketing campaign builder for startups/SaaS/ecommerce: templates for referral programs, pre-launch waitlists, giveaways, milestone referrals, ambassador programs, and leaderboards, plus an embeddable widget. REST API (app.viral-loops.com/api/v3, per-campaign publicToken, POST /campaign/participant), webhooks (participant/referral-count/convert/reward), and two-way Zapier. Use when adding or syncing participants to a campaign via the API or Zapier, attributing referrers so referrals count, reacting to referral-milestone or conversion webhooks to fulfill rewards, running a pre-launch waitlist with viral referral, deciding referral vs affiliate program, handling fake signups in a giveaway, or choosing the Build vs Accelerate plan. Do NOT use for audience-growth/referral strategy across tools (use /sales-audience-growth), designing an affiliate program across tools (use /sales-affiliate-program), or email deliverability (use /sales-deliverability)."
argument-hint: "[describe what you need help with in Viral Loops]"
license: MIT
version: 1.0.0
tags: [sales, audience-growth, referral, platform]
github: "https://github.com/viralloops"
---

# Viral Loops Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Add/sync participants to a campaign via the API or Zapier (and attribute referrers)
   - B) React to referral-milestone / conversion / reward webhooks to fulfill rewards
   - C) Pick + set up a campaign type — referral, pre-launch waitlist, giveaway, milestone, ambassador
   - D) Connect Viral Loops to a CRM/ESP so the referral list lives where you nurture
   - E) Decide referral vs affiliate program (different tools/strategy)
   - F) Fix a problem — referrals not crediting, fake/disposable signups, plan/participant limits

2. **API or no-code?** A code integration → REST API (`publicToken`) + webhooks. No endpoint to host → two-way Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Referral / waitlist / audience-growth **strategy** across tools (which tool, viral mechanics) | `/sales-audience-growth {question}` |
| Designing an **affiliate** program (commissions, recruiting) across tools | `/sales-affiliate-program {question}` |
| Email **deliverability** of referral/notification emails | `/sales-deliverability {question}` |
| Connecting Viral Loops to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-audience-growth viral waitlist mechanics to maximize referrals`".

## Step 3 — Viral Loops platform reference

**Read `references/platform-guide.md`** for the full reference — the campaign-template + module map (what's API vs widget vs UI-only), the participant-based pricing model, the participant/webhook data model with JSON shapes, and quick-start recipes (add a participant; react to milestone webhooks; push leads via Zapier).

**Read `references/viral-loops-api-reference.md`** for the integration surface — base `https://app.viral-loops.com/api/v3`, the **per-campaign `publicToken`** auth, `POST /campaign/participant`, the leaderboard/convert/reward endpoints, the webhook events (new participant / referral-count / converted / reward-redeemed), and the two-way Zapier triggers/actions. Note the docs are partly JS-rendered — the reference marks unconfirmed paths.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **It's campaign-scoped.** Each campaign has its own `publicToken`, widget, participants, and leaderboard.
  Grab the token from *that* campaign's install settings; multiple programs = multiple tokens.
- **Attribute the referrer on create.** A participant only earns a referral if you pass the referrer's code
  (or they arrive via the referral link). Forgetting it silently breaks attribution — the #1 integration bug.
- **Use webhooks, not polling.** Subscribe to New Referral Count / Participant Converted / Reward Redeemed
  to fulfill rewards and sync conversions. There's **no documented HMAC** — restrict to a secret URL,
  re-verify via `GET /campaign/participant` before paying out, and dedupe on (email, referralCountTotal).
- **Pipe participants into your ESP/CRM.** Viral Loops' built-in email is basic — send New Participant to
  Kit/Mailchimp/your CRM so nurture and segmentation happen where you already work.
- **Plan for fraud.** Viral referral/giveaway campaigns attract fake/disposable signups and same-IP abuse —
  validate emails and review before fulfilling rewards.
- **Mind the participant cap.** Pricing scales by participants (Build ~$49 → Accelerate ~$229); size the
  plan to expected signup volume, especially for a giveaway spike.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — the marketing site/pricing blocked automated fetches; verify pricing and API specifics in-account.*

1. **Referrals don't credit without the referrer.** Passing the participant but not the `referrer` code (or not routing through the referral link) means the referral isn't counted — check attribution first.
2. **`publicToken` is per-campaign.** A token from campaign A won't work on campaign B; pull each from its own install settings.
3. **No documented webhook HMAC.** Don't trust an unsigned webhook blindly — secret URL, re-verify via the API before granting a reward, and make handlers idempotent (referral-count events repeat).
4. **Built-in email/automation is basic.** Email-only notifications; for SMS/advanced flows/A-B testing, route to an ESP or compare with ReferralHero/UpViral via `/sales-audience-growth`.
5. **Giveaways attract fraud.** Fake/disposable emails and same-IP abuse are common — validate before rewarding, or you'll pay out to bots.
6. **Pricing scales by participants.** A viral spike can push you over a tier mid-campaign; size Build vs Accelerate to peak signups.
7. **Referral ≠ affiliate.** Viral Loops is customer-referral (rewards/discounts), not commission-based affiliate tracking — for affiliates use a dedicated tool (`/sales-affiliate-program`).
8. **Docs are partly JS-rendered.** Some endpoint paths (convert/reward/leaderboard) need confirming in the live developer reference; the participant POST + webhook events are solid.

## Related skills

- `/sales-audience-growth` — Audience-growth / referral / waitlist strategy across tools (Viral Loops is one of the referral platforms covered) — viral mechanics, tool selection
- `/sales-affiliate-program` — Designing an affiliate (commission) program across tools — the affiliate counterpart to Viral Loops' customer referrals
- `/sales-email-marketing` — Email sequences for the referral list you sync out of Viral Loops
- `/sales-integration` — Connecting Viral Loops to a CRM/ESP via webhooks/Zapier
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Add participants and reward referrals via the API (developer/automation)
**User says**: "When someone signs up in my app, add them to my Viral Loops referral campaign and credit whoever referred them."
**Skill does**: Walks Recipe 1 — `POST /api/v3/campaign/participant` with the user's email + the **`referrer`'s referral code**, authenticated by the campaign's **`publicToken`** (from install settings). Stresses that omitting the referrer breaks attribution, and to fulfill rewards via the **New Referral Count** webhook (idempotent, re-verify before paying out). Offers the Zapier Create-Participant action as a no-code path.
**Result**: Signups join the campaign with referrals correctly credited.

### Example 2: Run a pre-launch waitlist with viral referral
**User says**: "I want a waitlist where people move up by referring friends, before my launch."
**Skill does**: Points to the **pre-launch/waitlist + milestone** templates (move-up-the-line mechanics), the embeddable widget for the landing page, and the leaderboard for gamification. Notes attribution via referral links, syncing signups to an ESP for launch-day email, and watching for fake signups. Routes deeper viral-mechanics strategy: "run: `/sales-audience-growth maximize referrals on a pre-launch waitlist`."
**Result**: A working viral waitlist with referral-driven queue jumping.

### Example 3: Referral or affiliate — which do I need?
**User says**: "Should I use Viral Loops or set up an affiliate program?"
**Skill does**: Distinguishes the models — Viral Loops runs **customer referrals** (existing users refer friends for rewards/discounts), whereas an **affiliate** program pays commissions to promoters/partners. Recommends Viral Loops for word-of-mouth/waitlist virality and routes the affiliate-program-design decision: "run: `/sales-affiliate-program design a commission-based affiliate program`."
**Result**: User picks the right model and is handed to the right skill.

## Troubleshooting

### My referrals aren't being counted
**Symptom**: Participants get added but referral counts stay at zero.
**Cause**: The participant was created **without the referrer** — you didn't pass the referrer's `referralCode` and they didn't arrive through the referral link, so there's nothing to attribute.
**Solution**: On create, include `referrer: { referralCode: ... }` (or ensure signups come through the campaign's referral link). Verify with `GET /campaign/participant` that the referrer is linked. Confirm you're using the correct campaign's `publicToken`.

### My reward webhook fired twice / paid out twice
**Symptom**: A referrer got the same reward more than once.
**Cause**: Referral-count / reward webhooks can be delivered repeatedly, and there's no HMAC to dedupe on a signature.
**Solution**: Make the handler **idempotent** — key on (email, referralCountTotal) or a reward id, persist what you've already fulfilled, and re-verify the participant via the API before granting. Restrict the webhook endpoint to a secret URL.

### My campaign is full of fake signups
**Symptom**: A giveaway/referral campaign is flooded with junk or disposable-email entries.
**Cause**: Viral incentives attract fraud — disposable emails, same-IP multi-signups, bot entries.
**Solution**: Validate emails (verification/disposable-domain checks) before counting/rewarding, watch for same-IP clusters, add friction (double opt-in), and review the leaderboard before paying out top referrers. For list-quality/deliverability of the resulting list, use `/sales-deliverability`.
