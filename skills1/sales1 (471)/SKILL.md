---
name: sales-referralhero
description: "ReferralHero platform help — full-stack referral, affiliate, waitlist, contest, and NPS platform with REST API, webhooks, Zapier, native ESP connectors, multi-level referral tracking (Level 1/2/3), coupon groups, anti-fraud, and a 5,000 calls/hour limit. Use when referrals aren't tracking, deciding between Free (no API) vs PRO (API + webhooks) vs PREMIUM (ReCaptcha + SMS Verification), auth failing with `no_token` or `Bearer` vs `X-API-Key`, Level 2/3 counts off from calling `level_2_all_referrals` not `level_2_referrals`, bulk 429s from not chunking the 500-transaction `add_bulk_transactions` limit, coupon endpoints 404 without a coupon group, reward fulfillment (`promote` then `unlock_promoted_reward`) failing, or comparing to SparkLoop/ReferralKit/GrowSurf. Do NOT use for newsletter audience growth (use /sales-audience-growth), merge-tag referrals (use /sales-referralkit), SparkLoop recommendations (use /sales-sparkloop), or affiliate strategy across tools (use /sales-affiliate-program)."
argument-hint: "[describe what you need help with in ReferralHero]"
license: MIT
version: 1.0.1
tags: [sales, referral-program, affiliate, audience-growth, waitlist, platform]
---

# ReferralHero Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Pick a tier — Free (25 subs) vs PRO $199/mo (10K) vs PREMIUM $399/mo (50K)
   - B) Set up the REST API — authentication, base URL, first request
   - C) Add or track subscribers via API (single, bulk, with transaction data)
   - D) Configure webhooks for referral confirmation events
   - E) Integrate a native ESP connector (Mailchimp, Kit, AWeber, Klaviyo, ActiveCampaign, SendLane)
   - F) Multi-level referral tracking (Level 1/2/3) — counts not appearing or downline math is off
   - G) Coupon codes — create coupon groups and bulk-import codes
   - H) Compare ReferralHero against SparkLoop / ReferralKit / Viral Loops / GrowSurf / KickoffLabs
   - I) Hit the 5,000 calls/hour rate limit — getting 429 too_many_calls
   - J) Reward fulfillment workflow — promote subscriber + unlock_promoted_reward

2. **What's your campaign type?** Referral / Affiliate / Waitlist / Contest / NPS — the data model and which endpoints matter differ.

3. **What's your ESP?** Drives whether the native integration applies (Mailchimp, Kit, AWeber, Klaviyo, ActiveCampaign, SendLane) or you need Zapier/webhook/API patterns.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General newsletter audience growth strategy across all platforms | `/sales-audience-growth [question]` |
| General newsletter monetization | `/sales-newsletter [question]` |
| No-code newsletter-only referrals with merge-tag insertion (Copyhackers) | `/sales-referralkit [question]` |
| SparkLoop paid recommendations + partner network | `/sales-sparkloop [question]` |
| Affiliate program strategy across many tools | `/sales-affiliate-program [question]` |
| ESP setup (Mailchimp, Kit, MailerLite, AWeber, Klaviyo, ActiveCampaign) | `/sales-mailchimp`, `/sales-kit`, `/sales-mailerlite`, `/sales-klaviyo`, `/sales-activecampaign` |

If the question is ReferralHero-specific, continue to Step 3.

## Step 3 — ReferralHero platform reference

**Read `references/platform-guide.md`** for the full reference — feature gating, tier comparison, ESP integration flow, multi-level referral mechanics, anti-fraud controls, and comparisons with SparkLoop / ReferralKit / Viral Loops / GrowSurf / KickoffLabs.

**Read `references/referralhero-api-reference.md`** for the verbatim REST API documentation — authentication (Bearer token / X-API-Key), base URL (`https://app.referralhero.com/api/v2`), full endpoint reference (Lists, Subscribers, Coupons, Rewards, Levels 1/2/3 referrals, transactions, bulk transactions, qualify/unqualify, promote/unlock_promoted_reward), rate limits (5,000 req/hr soft), and error codes.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Free tier (25 subscribers max)** — useful only for proof of concept. Real campaigns need PRO ($199/mo, 10K members) or PREMIUM ($399/mo, 50K members). The Waitlist/Contest variant of PREMIUM is also $199/mo for 50K subscribers and adds broadcasts.
- **API available from PRO upward** — the Free tier excludes API access, so don't promise programmatic workflows on the Free tier. Confirm the user's plan before recommending API-driven recipes.
- **Auth**: `Authorization: Bearer YOUR_API_TOKEN` is the canonical form. `X-API-Key: YOUR_API_TOKEN` is the documented fallback when the client can't send `Authorization`. Don't mix headers.
- **Rate limit is per-token, 5,000/hr soft** — contact ReferralHero support to raise it. Returns HTTP 429 with `too_many_calls` error code on overage.
- **Bulk transactions are capped at 500 per request** (`POST .../subscribers/add_bulk_transactions`) — chunk larger imports.
- **Multi-level referral mechanics**: separate endpoints for Level 1 / 2 / 3 referrals and Level 2 / 3 "all referrals" (qualified + unqualified). Use the right endpoint or the count will look wrong.
- **Promote → unlock_promoted_reward** is a two-step manual reward fulfillment flow — for milestone-based rewards, configure them on the campaign and call `promote` after the subscriber crosses the threshold, then `unlock_promoted_reward` with the `reward_id`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features that may shift.*

1. **API access starts at PRO ($199/mo).** Free tier (25 subs) has NO API access — don't quote programmatic workflows to anyone still on Free. Webhooks also start at PRO.
2. **Rate limit is 5,000 calls/hour (soft) per token.** Exceeding returns HTTP 429 with `too_many_calls` error code. For high-volume imports, use `add_bulk_transactions` (500/request) instead of per-subscriber calls and request a limit increase via support.
3. **ReCaptcha and SMS Verification are PREMIUM-only ($399/mo).** PRO has anti-fraud, coupon codes, custom sender domain, and automation emails — but not the strongest abuse controls. If your program is a target for fraud, budget PREMIUM from day one.
4. **Bulk transactions max 500 per request.** Larger imports must be chunked. The endpoint expects a JSON `transactions` array, not multipart.
5. **Multi-level endpoints have separate "all" vs "confirmed" variants.** `level_2_all_referrals` includes unqualified referrals; `level_2_referrals` shows only confirmed. Calling the wrong one explains "the count is off" complaints. Same pattern at Level 3.
6. **Promote + unlock_promoted_reward is a two-step flow.** First `POST .../subscribers/:id/promote`, then `POST .../subscribers/:id/unlock_promoted_reward` with the `reward_id`. Skipping `promote` causes `unlock_promoted_reward` to silently fail.
7. **Coupons live under coupon groups, not standalone.** `POST .../coupon_groups` first, then `POST .../coupons` with the `coupon_group_id`. Importing flat lists without a group fails.
8. **Lifetime-deal customers got migrated to monthly subs.** Capterra reviews show frustration with the pricing transition — if the user mentions a "lifetime" plan they bought years ago, that's the context; current plans are subscription-only.
9. **Authentication header is single-header, not both.** Send EITHER `Authorization: Bearer ...` OR `X-API-Key: ...` — sending both has undocumented behavior. Prefer `Authorization` unless your client strips it.
10. **Native ESP integrations may double-add subscribers.** If you connect Mailchimp (or Kit/AWeber/etc.) AND also POST to `/subscribers` via API, you'll get duplicate adds. Pick one mechanism per campaign.
11. **No MCP server.** AdButler and some newsletter tools ship MCP — ReferralHero does not, as of research date 2026-06-01. Confirm before claiming MCP support.

## Related skills

- `/sales-audience-growth` — Newsletter audience growth strategy (referrals + cross-promotion + lead magnets across all platforms)
- `/sales-newsletter` — Newsletter monetization (paid subs, sponsorships, ad networks)
- `/sales-referralkit` — ReferralKit (no-code Morning Brew-style merge-tag-driven referrals, free up to 10K leads, no API)
- `/sales-sparkloop` — SparkLoop (referrals + paid recommendations + partner network across 25+ ESPs)
- `/sales-affiliate-program` — General affiliate program strategy and platform selection
- `/sales-mailchimp` — Mailchimp platform help (one of ReferralHero's native ESP integrations)
- `/sales-kit` — Kit / ConvertKit platform help (native ESP integration)
- `/sales-mailerlite` — MailerLite platform help (Zapier-based integration)
- `/sales-klaviyo` — Klaviyo platform help (native ESP integration)
- `/sales-activecampaign` — ActiveCampaign platform help (native ESP integration)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: PRO vs PREMIUM decision for a fraud-prone giveaway campaign
**User says**: "I'm running a viral giveaway expecting 20K signups and worried about fake referrals. PRO or PREMIUM?"
**Skill does**: Recommends PREMIUM ($399/mo) because it adds ReCaptcha and SMS Verification — both essential for fraud-prone viral campaigns. Notes PRO ($199/mo, 10K members) wouldn't cover 20K anyway. Mentions PREMIUM Waitlist/Contest variant at $199/mo for 50K subscribers if the contest is the entire campaign and the standard referral feature mix isn't needed. Suggests turning on anti-fraud + coupon validation + reward review workflow regardless of tier.
**Result**: User picks PREMIUM with ReCaptcha + SMS Verification on, sets up reward review for top referrers.

### Example 2: Setting up API + first subscriber add
**User says**: "I'm on the PRO plan. How do I add a subscriber via the API and assign them a referrer?"
**Skill does**: Provides authentication header (`Authorization: Bearer YOUR_API_TOKEN`), base URL (`https://app.referralhero.com/api/v2`), and a cURL example: `POST /lists/:uuid/subscribers` with `email`, `name`, and `referrer` (the referrer's referral code or unique identifier). Notes that `double_optin=true` matches the campaign's setting if confirmation is required. Points to `references/referralhero-api-reference.md` for the full parameter list, and warns about double-adds if Mailchimp/Kit native integration is also connected.
**Result**: User makes a successful first API call, sees the new subscriber with attribution to the referrer, and knows to disable one of the dual subscription paths.

### Example 3: Multi-level referral counts look wrong
**User says**: "I have multi-level referrals enabled. My Level 2 count seems off — way higher than what I see in the dashboard."
**Skill does**: Asks which endpoint they're hitting. If they're calling `GET /lists/:uuid/subscribers/:subscriber_id/level_2_all_referrals` that includes UNqualified referrals — dashboard typically shows only qualified. Recommends `level_2_referrals` (confirmed only) for parity with the dashboard view. Notes the same pattern at Level 3. Suggests `qualify` / `unqualify` endpoints to manually re-classify suspicious referrals.
**Result**: User switches endpoint, counts match the dashboard, and adds qualify/unqualify into their fraud-review workflow.

## Troubleshooting

### Authentication failing with `no_token` error
**Symptom**: API requests return `no_token` despite sending the header
**Cause**: Header capitalization, missing `Bearer` prefix, or sending both `Authorization` and `X-API-Key`
**Solution**: Use exactly `Authorization: Bearer YOUR_API_TOKEN` (capital A, lowercase bearer per HTTP spec is also accepted, but `Bearer` with capital B is documented). If your HTTP client strips `Authorization` headers, fall back to `X-API-Key: YOUR_API_TOKEN` — but never send both. Verify the token from ReferralHero dashboard > Account > API; tokens are per-account, not per-list.

### `too_many_calls` (HTTP 429) on bulk import
**Symptom**: Bulk subscriber import errors out partway with HTTP 429 `too_many_calls`
**Cause**: Hit the 5,000 calls/hour soft rate limit by POSTing per-subscriber instead of using bulk endpoints
**Solution**: Switch single-subscriber loops to `POST /lists/:uuid/subscribers/add_bulk_transactions` (500 transactions per request). Add exponential backoff with `Retry-After` respect. For sustained high volumes, contact ReferralHero support to raise the rate limit.

### Webhook not firing on referral confirmation
**Symptom**: Configured a webhook for confirmation events but it never fires
**Cause**: Webhooks are PRO+ (not Free), the campaign's `double_optin` setting interacts with confirmation timing, or the subscriber was added without a `referrer` value
**Solution**: Confirm plan tier includes webhooks (PRO and PREMIUM do). Check that the campaign has `double_optin` configured correctly — if on, confirmation requires the referee to click the confirmation email. For API-added subscribers, ensure `referrer` is set to the referrer's referral code or unique identifier, otherwise no attribution event fires.

### Reward not unlocking after milestone
**Symptom**: Subscriber hit the milestone threshold but the reward email never sent
**Cause**: Reward fulfillment is a two-step manual flow on the API path — `promote` then `unlock_promoted_reward`
**Solution**: First call `POST /lists/:uuid/subscribers/:subscriber_id/promote` to mark the subscriber as eligible for the next reward, then `POST /lists/:uuid/subscribers/:subscriber_id/unlock_promoted_reward` with the `reward_id`. If you're using the UI-side automatic milestone rewards, check that the milestone threshold is set on the campaign and the subscriber's qualified-referral count actually exceeds it (NOT all-referrals count).

### Coupon import returns 404
**Symptom**: `POST /lists/:uuid/coupons` with an array of codes returns 404
**Cause**: Coupons must belong to a coupon group; the group ID is required in the request
**Solution**: First create a coupon group: `POST /lists/:uuid/coupon_groups` with `name`, `coupons` (initial array), and `active: true`. Capture the returned `id`. Then add more coupons via `POST /lists/:uuid/coupons` with `coupon_group_id` set to that ID.
