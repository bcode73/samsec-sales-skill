---
name: sales-launchlist
description: "LaunchList platform help — viral pre-launch waitlist platform with one-time lifetime pricing, gamified referrals (queue jumping, leaderboard, position inflation), embed widget + custom form POST endpoint, new_user/email_verify webhooks, Zapier, and spam protection. Use when choosing Free (100 submissions) vs paid Launch (500) vs Grow one-time (10K — webhooks, Zapier, team unlock here), wiring waitlist signups into Mailchimp/Kit/HubSpot or a CRM because LaunchList has no email broadcast system, needing programmatic access when there is no public REST API yet (form POST + webhook workaround), building a webhook handler with referred_by referral attribution, blocking disposable-email or bot signups on a viral waitlist, a custom signup form not submitting or not tracking referrals, or comparing LaunchList vs KickoffLabs/Viral Loops/Prefinery/GetWaitlist on one-time vs subscription pricing. Do NOT use for list-growth strategy (use /sales-audience-growth) or KickoffLabs help (use /sales-kickofflabs)."
argument-hint: "[describe what you need help with in LaunchList]"
license: MIT
version: 1.0.1
tags: [sales, waitlist, referral-program, viral-marketing, platform]
---

# LaunchList Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Pick a tier — Free (100 submissions) vs Launch $29 one-time (500) vs Grow $79 one-time (10K) vs Scale custom (100K+)
   - B) Install the waitlist — embed widget vs custom DIY form vs hosted landing page
   - C) Get signups out of LaunchList — webhooks, Zapier, Slack, or CSV export into an ESP/CRM
   - D) Set up referral rewards, leaderboard, or position inflation
   - E) Fight spam — disposable emails, bots, fake referrals
   - F) Programmatic access — what works given there's no public REST API
   - G) Compare LaunchList to KickoffLabs / Viral Loops / Prefinery / GetWaitlist / Waitlister

2. **Where will the form live?** Hosted LaunchList page / your own site (which builder?) / custom-coded form — drives widget vs DIY vs landing-page setup.

3. **Where do signups need to end up?** ESP (which?), CRM, spreadsheet, or just the dashboard — drives whether you need Grow ($79) for webhooks/Zapier.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list growth strategy across platforms | `/sales-audience-growth [question]` |
| Newsletter monetization | `/sales-newsletter [question]` |
| KickoffLabs (waitlists + giveaways with REST API + fraud webhooks) | `/sales-kickofflabs [question]` |
| UpViral (B2C sweepstakes/points campaigns) | `/sales-upviral [question]` |
| Full-stack multi-level referral/affiliate (L1/2/3, coupon groups) | `/sales-referralhero [question]` |
| No-code merge-tag newsletter referrals | `/sales-referralkit [question]` |
| SparkLoop paid recommendations + partner network | `/sales-sparkloop [question]` |
| ESP setup (Mailchimp, Kit, MailerLite, ActiveCampaign) | `/sales-mailchimp`, `/sales-kit`, `/sales-mailerlite`, `/sales-activecampaign` |

If the question is LaunchList-specific, continue to Step 3.

## Step 3 — LaunchList platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities tagged by automation surface, pricing and plan gates, integrations, data model, quick-start recipes (custom form, webhook→ESP handler, Zapier), integration patterns, and the comparison grid vs KickoffLabs / UpViral / Viral Loops / Prefinery / GetWaitlist / Waitlister / Referlist / Tuemilio.

**Read `references/launchlist-api-reference.md`** for the programmatic surface — there is **no public REST API** (roadmap: planned). What exists: the form POST endpoint (`https://getlaunchlist.com/s/FORM_KEY`), verbatim `new_user` + `email_verify` webhook payloads, Zapier triggers (New Submission / Email Verified), and the spam-protection mechanisms.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Webhooks and Zapier are Grow-tier ($79 one-time).** Any signup→ESP/CRM automation forces Grow minimum. Free/Launch users get CSV export only.
- **No email broadcast system** — LaunchList only sends welcome/verification emails. Launch announcements come from your ESP; wire signups over via webhook or Zapier, gate on `email_verify` if verification is on.
- **No public REST API** — ingress is the form POST endpoint, egress is webhooks/Zapier/CSV. There is no way to read, update, or delete submissions programmatically.
- **Custom forms have three hard rules**: email input named exactly `email`, form class `launchlist-form`, and `widget-diy.js` in the page head (otherwise referral attribution breaks silently).
- **Webhooks have no documented signing or retries** — use an unguessable URL, check `waitlist_key`, dedupe on `id`, reconcile against CSV exports.
- **One-time pricing is per project/tier** — going over your submission cap means buying up a tier, not a monthly overage.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06-06) — review these, especially plan-gated features and pricing that may shift.*

1. **No public REST API.** "API Access" is a *planned* roadmap item. Don't design an integration around endpoints that don't exist — use form POST (ingress) + webhooks (egress).
2. **Webhooks + Zapier gated to Grow ($79 one-time).** The free tier's "export" is manual CSV only.
3. **`referred_by.positon` is a verbatim typo** in the documented webhook payload (top level uses `position`). Parse both spellings.
4. **`is_email_verified` is null-or-timestamp, not boolean.** `null` = unverified; a `"YYYY-MM-DD HH:MM:SS"` string = verified.
5. **`referred_by` is absent for direct signups** — guard before dereferencing in webhook handlers.
6. **Server-to-server POSTs to `/s/FORM_KEY` lose referral attribution** — `widget-diy.js` does the browser-side referral parsing. Only bypass it for testing.
7. **No webhook signing documented** — validate `waitlist_key` and payload shape; don't treat webhook data as authenticated.
8. **Pricing sources disagree** — live page says $29/$79; LaunchList's own blog and third-party comparisons have cited $19/$39/$149/$299 volume steps and a $19 custom-domain add-on. Verify on the pricing page before budgeting.
9. **Email verification starts at Launch ($29)** — Free-tier lists accumulate unverified (typo'd, disposable-beating) addresses; clean before importing to your ESP.
10. **Refund only with zero signups** — the 7-day money-back guarantee is void once you've collected a single signup.

## Related skills

- `/sales-audience-growth` — List-growth strategy (lead magnets, referrals, cross-promotion across all platforms)
- `/sales-kickofflabs` — KickoffLabs (waitlists + giveaways with REST API v1+v2, fraud webhooks, $13–202/mo)
- `/sales-upviral` — UpViral (viral sweepstakes/rewards campaigns, API at Business+, $79–319/mo)
- `/sales-referralhero` — ReferralHero (full-stack referral/affiliate with multi-level L1/2/3 + REST API)
- `/sales-referralkit` — ReferralKit (no-code merge-tag newsletter referrals, free first 10K leads)
- `/sales-sparkloop` — SparkLoop (newsletter referrals + paid recommendations)
- `/sales-mailchimp` — Mailchimp platform help (common Zapier destination)
- `/sales-kit` — Kit platform help (common Zapier destination)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Tier choice for a side-project launch
**User says**: "I'm collecting signups for a SaaS I'm launching in 3 months. I want referral rewards and the emails need to end up in Kit. Which LaunchList plan?"
**Skill does**: Recommends Grow ($79 one-time) because Zapier/webhooks — the only automated path to Kit — unlock there, and 10K submissions covers most pre-launch lists. Notes Launch ($29) works if a manual CSV export into Kit at launch day is acceptable, and that reward/milestone settings start at Launch. Flags that LaunchList can't send the launch announcement itself.
**Result**: User picks Grow, sets up the Zapier New Submission → Kit Zap with an `is_spam = 0` filter.

### Example 2: Webhook handler with referral attribution (developer)
**User says**: "How do I build a webhook handler that pushes LaunchList signups into HubSpot with referral attribution?"
**Skill does**: Walks through Plugins → Create a webhook, then the handler pattern from `references/platform-guide.md` Recipe 2: validate `waitlist_key` (no HMAC signing exists), dedupe on `id`, skip `is_spam == 1`, guard `referred_by` for direct signups, map `referred_by.referral_code` (and the `positon` typo) into HubSpot contact properties, and gate launch emails on the `email_verify` event.
**Result**: User has a working Flask handler with idempotency, spam filtering, and referrer fields in HubSpot.

### Example 3: Custom form not tracking referrals
**User says**: "I built my own signup form on Framer posting to LaunchList. Signups arrive but everyone shows as a direct signup — referral links don't credit anyone."
**Skill does**: Diagnoses the missing `widget-diy.js` script (it parses the referral code from the visitor's URL); checks the form has class `launchlist-form` and the email field is named `email`; explains a bare POST records the signup but drops browser-side referral context.
**Result**: User adds the tracking script to the page head and referral attribution starts crediting referrers.

## Troubleshooting

### Signups land in LaunchList but never reach my ESP/CRM
**Symptom**: Dashboard shows submissions; Mailchimp/HubSpot/Kit shows nothing
**Cause**: Webhooks and Zapier are Grow-tier ($79+) — on Free/Launch nothing fires. Or the Zapier access token was regenerated (breaking existing Zaps), or the webhook was disabled after errors.
**Solution**: Confirm plan is Grow+. In Plugins, check the webhook's enabled state and use "Send a test request". For Zapier, re-authenticate with the current access token and check the Zap's task history. As a stopgap, export CSV and import manually.

### Waitlist is filling with disposable emails and obvious bots
**Symptom**: Spike of signups from temp-mail domains or with no referrer, `is_spam` flags rising
**Cause**: Public waitlists attract bots; referral rewards attract fake-signup gaming
**Solution**: Enable temporary-email blocking (Blocks settings — 3,000+ disposable domains), add the `_gotcha` honeypot to custom forms, enable ReCaptcha v2 (Launch+) and email verification (Launch+), and route the domain through Cloudflare. Downstream, filter `is_spam == 1` in your webhook/Zapier flow and only fulfill referral rewards for verified referees (`email_verify` received).

### I need to update or delete a submission programmatically
**Symptom**: Looking for an API endpoint to modify or remove a signup (GDPR delete, typo fix, position change)
**Cause**: No public REST API exists — ingress-only form POST plus egress-only webhooks
**Solution**: Manage submissions in the dashboard (Manage Submissions) manually. For bulk needs, export CSV, fix externally, and treat your ESP/warehouse as the source of truth. Watch the roadmap's "API Access" item before building long-lived workarounds.
