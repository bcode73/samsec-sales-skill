---
name: sales-kickofflabs
description: "KickoffLabs platform help — viral marketing for pre-launch waitlists, bonus-entry giveaways, milestone-reward referral programs, and leaderboard giveaways with REST API v1 + v2, server-side webhooks (`__fraudulent`/`__referral`), AnyForm + KOL.js, and native ESP/Shopify/Zapier integrations. Use when viral campaigns aren't tracking referrers, deciding between Hobby $13/mo (500 leads, no A/B no reward emails) vs Premium $48/mo (A/B + reward emails) vs Business $99/mo vs Enterprise $202/mo, the API key is rejected for being embedded client-side, webhook `__fraudulent` codes (`duplidate_email`/`duplicate_ip`/`bounced`) need a triage workflow, choosing v1 vs v2 endpoints, leaderboard capped at 50, lead-cap auto-upgrade inflating bills, or comparing to Viral Loops/UpViral/Prefinery. Do NOT use for newsletter audience growth (use /sales-audience-growth), merge-tag referrals (use /sales-referralkit), SparkLoop paid recommendations (use /sales-sparkloop), or multi-level Level 1/2/3 referrals (use /sales-referralhero)."
argument-hint: "[describe what you need help with in KickoffLabs]"
license: MIT
version: 1.0.0
tags: [sales, referral-program, viral-marketing, waitlist, giveaway, platform]
---

# KickoffLabs Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Pick a tier — Hobby $13/mo (500 leads) vs Premium $48/mo (2.5K) vs Business $99/mo (10K) vs Enterprise $202/mo (25K)
   - B) Launch a pre-launch waitlist with viral referrals (Dropbox-style queue jumping)
   - C) Set up a bonus-entry giveaway (Gleam-style)
   - D) Build a milestone-reward referral program (Morning Brew style)
   - E) Set up a leaderboard giveaway with top-N winners
   - F) Connect API or webhooks — v1 `/subscribe` vs v2 `/v2/{CAMPAIGN_ID}/...`
   - G) Configure AnyForm to post existing site forms to KickoffLabs
   - H) Interpret webhook `__fraudulent` reasons (duplicate_ip / bounced / duplidate_email)
   - I) Integrate with Klaviyo / Mailchimp / ActiveCampaign / Brevo / Zapier
   - J) Compare KickoffLabs to Viral Loops / UpViral / Prefinery / ReferralCandy

2. **What's your campaign type?** Waitlist / giveaway / milestone-reward / leaderboard / opt-in — drives which scoring + reward + verification settings matter.

3. **What's your ESP and website stack?** Drives whether native ESP integration is enough or you need API/webhooks/Zapier glue.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General newsletter audience growth strategy across all platforms | `/sales-audience-growth [question]` |
| Newsletter monetization | `/sales-newsletter [question]` |
| No-code newsletter-only referrals with merge-tag insertion | `/sales-referralkit [question]` |
| SparkLoop paid recommendations + partner network | `/sales-sparkloop [question]` |
| Full-stack referral/affiliate with multi-level Level 1/2/3 + coupon groups + REST API | `/sales-referralhero [question]` |
| Affiliate program strategy across many tools | `/sales-affiliate-program [question]` |
| ESP setup (Klaviyo, Mailchimp, ActiveCampaign, Brevo) | `/sales-klaviyo`, `/sales-mailchimp`, `/sales-activecampaign`, `/sales-brevo` |

If the question is KickoffLabs-specific, continue to Step 3.

## Step 3 — KickoffLabs platform reference

**Read `references/platform-guide.md`** for the full reference — feature gating per tier, campaign type selection (waitlist / giveaway / milestone / leaderboard / opt-in), AnyForm vs direct-API, fraud detection signals, SMS verification, ESP integrations, and comparisons with Viral Loops / UpViral / Prefinery / ReferralCandy / Voucherify.

**Read `references/kickofflabs-api-reference.md`** for the REST API documentation — v1 (`/subscribe`, `/info`) + v2 (`/v2/{CAMPAIGN_ID}/...` for tags, leads, actions, leaderboard, approve, block, waitlist, verify, SMS, bulk-tags), authentication via `api_key` + `CAMPAIGN_ID`, webhook payload schemas (including `__fraudulent`, `__referral`, `__reward_level`, `__score_change`, `__tagged`), and rate limits by tier.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Hobby tier excludes A/B testing, reward level emails, tracking pixels, and custom email templates** — for any campaign that needs milestone rewards (the main referral mechanic), start at Premium ($48/mo annual).
- **API key must be server-side only.** Don't embed in client-side JavaScript — KickoffLabs explicitly warns about this. Use AnyForm + KOL.js for browser-side, then have your backend call the API with the key.
- **v1 vs v2**: v1 (`/subscribe`, `/info`) is form-encoded and still active for simple adds. v2 (`/v2/{CAMPAIGN_ID}/...`) is JSON and covers tags, approve/block, bulk operations, leaderboard, waitlist, SMS verification. Use v2 for new integrations.
- **AnyForm vs direct API**: KickoffLabs' own guidance is "in most cases, use AnyForm for custom pages instead of adding leads directly via the API." AnyForm handles attribution (`?kid=` parsing), referrer cookies, and lead deduplication automatically. Reserve direct API for server-to-server flows your AnyForm can't capture.
- **SMS verification is Premium+ as a $50/mo add-on; Enterprise includes it.** If your fraud risk requires SMS verification, budget Premium + add-on ($98/mo annual) or Enterprise ($202/mo annual).
- **Lead-cap auto-upgrade at $8 per 1,000 overage** — if your campaign spikes (Product Hunt launch, press feature), expect auto-upgrade billing to kick in. Set a campaign-level cap if you want hard ceilings.
- **Fraud-detection flags in webhook**: `duplicate_ip` (same IP signing up multiple times), `bounced` (email bounced on verify), `duplidate_email` (their typo — duplicate email). Treat them as advisory; combine with `approve` / `block` endpoints for manual review.
- **Leaderboard endpoint caps at 50 results** — for larger top-N lists, paginate via leads endpoint and sort client-side.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features that may shift.*

1. **API key must be server-side.** "Your API Key should never be used in client side JavaScript." Browser-embedded keys leak to any attacker who reads page source. Use AnyForm + KOL.js for browser-side; reserve the API key for backend.
2. **`duplidate_email` is spelled with a typo in KickoffLabs's own webhook payload docs.** When parsing the `__fraudulent` array, match against the literal string `duplidate_email` as well as `duplicate_email` if KickoffLabs ever fixes it. Don't "correct" the typo client-side.
3. **v1 and v2 endpoints coexist.** v1 `/subscribe` is form-encoded; v2 `/v2/...` is JSON-first. Mixing them in one integration confuses parameter parsing. Pick one path per campaign workflow.
4. **Reward-level emails are Premium+.** Hobby tier ($13/mo) supports the autoresponder but NOT reward-level emails — so milestone-reward programs need Premium minimum.
5. **A/B testing is Premium+.** Hobby cannot A/B test campaign variants. Limits iteration on signup conversion early.
6. **Custom email templates + custom domains require Business+ ($99/mo).** Premium ($48/mo) gives one custom domain but uses default email templates.
7. **SMS Contests are Premium+ add-on at $50/mo extra** (Enterprise includes). Don't promise SMS verification on Hobby.
8. **Lead-cap auto-upgrade at $8 per 1,000 overage** — viral campaigns spike, billing follows. Capterra reviews flag pricing concerns; set a campaign-level cap and configure billing alerts.
9. **Leaderboard endpoint capped at 50 leads.** No pagination on `/leaderboard` itself — pull more via the leads endpoints and rank client-side.
10. **Rate limits scale with plan: ~10/min on Hobby up to ~100/min on Enterprise.** Use bulk endpoints (Bulk Tags, bulk Approve up to 200 emails) for batch operations.
11. **Webhook signing is undocumented in public material.** No HMAC/signature scheme published. Verify caller IP or use a shared-secret query param if signing matters; or contact support to confirm current behavior.
12. **AnyForm is preferred over direct API for custom pages.** KickoffLabs's own docs say so. Direct API is for server-to-server attribution flows AnyForm can't reach.
13. **Capterra reviewers complain about design customization limits** ("section mechanic requires more options") and a learning curve. If pixel-perfect landing pages matter, pair KickoffLabs with a standalone landing-page tool (Unbounce, Leadpages, Framer) and post results via AnyForm.

## Related skills

- `/sales-audience-growth` — Newsletter audience growth strategy (referrals + cross-promotion + lead magnets across all platforms)
- `/sales-newsletter` — Newsletter monetization (paid subs, sponsorships, ad networks)
- `/sales-referralkit` — ReferralKit (no-code merge-tag-driven newsletter referrals, free up to 10K leads)
- `/sales-sparkloop` — SparkLoop (newsletter referrals + paid recommendations + partner network)
- `/sales-referralhero` — ReferralHero (full-stack referral/affiliate/waitlist/contest with multi-level Level 1/2/3 + coupon groups + REST API + webhooks + Zapier)
- `/sales-affiliate-program` — General affiliate program strategy and platform selection
- `/sales-klaviyo` — Klaviyo platform help (native ESP integration)
- `/sales-mailchimp` — Mailchimp platform help (native ESP integration)
- `/sales-activecampaign` — ActiveCampaign platform help (native ESP integration)
- `/sales-brevo` — Brevo platform help (native ESP integration)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Tier picking for a Product Hunt launch waitlist
**User says**: "I'm launching on Product Hunt next month and want a viral waitlist with milestone rewards. Hobby or Premium?"
**Skill does**: Recommends Premium ($48/mo annual, 2,500 leads/mo) because reward-level emails are Premium+, A/B testing is Premium+, and a Product Hunt feature can spike well past Hobby's 500-leads cap. Warns about $8-per-1,000 auto-upgrade billing on spike and suggests setting a campaign cap if budget is tight. Mentions SMS Verification add-on ($50/mo extra) if fraud risk is high. Recommends Business ($99/mo) only if custom email templates/domains matter from day one.
**Result**: User picks Premium with annual billing, sets a 10K-lead campaign cap, plans SMS verification only if first 1K signups show fraud signals.

### Example 2: Webhook payload `__fraudulent` interpretation
**User says**: "I'm getting webhooks with `__fraudulent` arrays containing `duplidate_email` and `bounced` — what do these mean and what should I do?"
**Skill does**: Confirms `duplidate_email` is verbatim from KickoffLabs docs (yes, with the typo — match the literal string). `duplicate_ip` means another lead signed up from the same IP recently. `bounced` means the verification email bounced. Suggests a triage workflow: auto-block on `bounced`, manual-review on `duplicate_ip`/`duplidate_email`, and use `POST /v2/{CAMPAIGN_ID}/approve` (supports up to 200 emails per bulk call) to override after review.
**Result**: User builds a webhook handler that routes by fraud reason and queues borderline cases for human review with batch approve.

### Example 3: v1 cURL to add a lead with referrer attribution
**User says**: "Give me a cURL example to add a subscriber via the API with referrer attribution. I'm on Premium."
**Skill does**: Provides `POST https://api.kickofflabs.com/v1/{CAMPAIGN_ID}/subscribe` with `email`, `api_key`, `social_id` (the referrer's social_id, found in `?kid=` query param), `ip`, `__url`, and `__ref`. Notes the key must be server-side. Mentions v2 `/tags/{TAG_ID}/lead` as the JSON-based alternative for tag-based workflows. Reminds user to consider AnyForm + KOL.js if the signup happens in browser instead.
**Result**: User has a working server-side subscribe call with proper attribution and knows when to switch to AnyForm.

## Troubleshooting

### API returns "invalid api_key" even though the key is correct
**Symptom**: Calls fail with auth errors despite copying the key from Setup > Advanced Settings > API Access
**Cause**: Either the key was embedded in client-side JavaScript (which KickoffLabs explicitly disallows and may rotate-invalidate on detection), or the request is hitting a different campaign's API endpoint, or v1/v2 path mismatch
**Solution**: Verify the request comes from your server, not browser. Confirm the `CAMPAIGN_ID` in the URL matches the campaign whose key you copied. If you suspect key compromise, rotate it in Setup > Advanced Settings > API Access and update your backend env vars. Don't mix v1 and v2 in one call (v1 wants form-encoded, v2 wants JSON).

### Webhooks fire but the `__fraudulent` field is empty when I expected fraud
**Symptom**: A lead clearly looks fraudulent (same IP repeating, disposable email) but the webhook arrives without a `__fraudulent` array
**Cause**: KickoffLabs's fraud detection runs heuristics — `duplicate_ip` only fires if signups come from the same IP within KickoffLabs's window; `bounced` requires a verification bounce, which only happens if double-opt-in / verify is configured; `duplidate_email` catches exact duplicates, not lookalikes
**Solution**: Enable email verification / double-opt-in on the campaign for `bounced` flags. Use the `POST /v2/{CAMPAIGN_ID}/leads/verify` endpoint as a programmatic verification trigger. For weaker fraud signals (disposable domains, lookalike emails), add a server-side check before forwarding to KickoffLabs.

### Leaderboard endpoint only returns 50 leads — how do I get the top 100?
**Symptom**: `GET /v2/{CAMPAIGN_ID}/leaderboard` caps at 50 results
**Cause**: The endpoint enforces `limit ≤ 50` by design — pagination is not supported on `/leaderboard`
**Solution**: Pull more leads via `GET /v2/{CAMPAIGN_ID}/leads/...` (or use the leaderboard 50, then call individual leads beyond rank 50 via lead-by-ID endpoints), and rank client-side by `contest_score`. For most campaigns, top 50 is the meaningful slice — verify whether you actually need 100+.

### Lead-cap auto-upgrade billed me unexpectedly after a viral spike
**Symptom**: Monthly bill jumped after a Product Hunt feature pushed leads above the plan cap
**Cause**: KickoffLabs auto-upgrades plans at $8 per 1,000 overage leads — by default this is silent
**Solution**: Set a campaign-level lead cap in dashboard settings (where supported per plan). Configure billing alerts via your payment processor. Upgrade to the next plan tier proactively if you're consistently within 20% of the cap — annual billing at the higher tier is often cheaper than per-overage charges.
