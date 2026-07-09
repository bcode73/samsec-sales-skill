---
name: sales-getwaitlist
description: "GetWaitlist platform help — developer-friendly pre-launch waitlist + referral widget (getwaitlist.com): priority queue, referral leaderboard, automatic emails, REST API (api.getwaitlist.com/api/v1), and new_signup/offboarded_signup webhooks. Use when choosing the Basic tier (API included) vs Advanced (custom domain + viral referrals) vs Pro (custom email-sending domain + email automation), the free tier disappeared for a new account (removed recently, existing grandfathered), adding signups via the unauthenticated POST /signup endpoint, generating an api-key or JWT to list/offboard/advance/delete signups, building a webhook handler for new_signup/offboarded_signup events, embedding the widget in Webflow/Wix/Shopify/Carrd/Notion, or syncing signups to HubSpot/Airtable/Slack via Zapier. Do NOT use for general list-growth strategy (use /sales-audience-growth) or Waitlister help (use /sales-waitlister)."
argument-hint: "[describe what you need help with in GetWaitlist]"
license: MIT
version: 1.0.0
tags: [sales, waitlist, referral-program, viral-marketing, platform]
---

# GetWaitlist Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Pick a tier — Basic $15/mo (API) vs Advanced $50/mo (custom domain + viral referrals) vs Pro $250/mo (custom email domain + email automation)
   - B) Build the waitlist — embed widget (HTML/iframe/React) vs hosted page vs no-code embed (Webflow/Wix/Shopify/Carrd/Notion)
   - C) Set up referrals — referral links, queue jumping (`spots_to_move_upon_referral`), leaderboard
   - D) Wire data out — `new_signup`/`offboarded_signup` webhooks, REST API, Zapier, HubSpot/Airtable/Slack
   - E) Add signups programmatically — unauthenticated `POST /signup`
   - F) Manage the queue — list, advance, offboard, or delete signups (authenticated)
   - G) Compare GetWaitlist vs Waitlister / LaunchList / KickoffLabs / Prefinery

2. **Where will signups happen?** Hosted page / embed on your site (which builder?) / your own backend via API — drives install path.

3. **Where must the data end up?** Stays in GetWaitlist / ESP / CRM / warehouse — drives whether you need webhooks vs Zapier vs the authenticated list API.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list growth strategy across platforms | `/sales-audience-growth [question]` |
| Waitlister (built-in broadcasts, HMAC-signed webhooks, API) | `/sales-waitlister [question]` |
| LaunchList (one-time pricing, no API) | `/sales-launchlist [question]` |
| KickoffLabs (waitlists + giveaways, Zapier, fraud webhooks) | `/sales-kickofflabs [question]` |
| UpViral (B2C sweepstakes / points campaigns) | `/sales-upviral [question]` |
| Multi-level referral/affiliate (L1/2/3, coupon groups) | `/sales-referralhero [question]` |
| Email marketing strategy once the list exists | `/sales-email-marketing [question]` |

If the question is GetWaitlist-specific, continue to Step 3.

## Step 3 — GetWaitlist platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities tagged by automation surface, pricing and plan gates, integrations, the Waitlist/Signup/Leaderboard data model, and quick-start recipes (server-side signup with referral attribution, webhook→CRM handler, bulk offboarding at launch).

**Read `references/getwaitlist-api-reference.md`** for the API — base URL `https://api.getwaitlist.com/api/v1/`, the unauthenticated signup-create/get + waitlist/leaderboard endpoints, the `api-key`/JWT authenticated list/advance/offboard/delete endpoints, offset/limit pagination, and both webhook payloads verbatim.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **The API is available from Basic ($15/mo)** — unlike rivals that gate it to a high tier. But **viral referrals and custom domains need Advanced ($50)**, and **sending email from your own domain needs Pro ($250)**.
- **There is no free tier for new accounts** (removed mid-2025). If a user expects free, they either have a grandfathered account or want a free competitor (LaunchList Free, Waitlister Free) — say so.
- **Signup create/get are unauthenticated** — anyone with your public `waitlist_id` can add signups. Don't rely on them for trusted data; gate referral rewards on `verified` signups and enable email verification.
- **Authenticated reads use an `api-key` header** (My Account → API Keys; keys don't expire) or a JWT from `POST /auth/create_tokens`.
- **Webhooks are unsigned with no documented retries** (`new_signup`, `offboarded_signup`; 30s connect / 90s response). Make handlers idempotent on `uuid`, respond fast, and reconcile via the list API.
- **Offboard ≠ delete.** Offboarding keeps history (`removed_date`/`removed_priority`); `DELETE /signup` (204) is permanent — use it for GDPR erasure.
- **No MCP server and no Make modules** — automation is webhooks + REST API + Zapier/native HubSpot/Airtable/Slack/Discord.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing that may shift.*

1. **No free tier for new accounts** (removed mid-2025; existing accounts grandfathered). New signups start at Basic $15/mo with a 7-day trial.
2. **Plan gates bite mid-build**: viral referrals + custom domain need Advanced ($50); custom email-sending domain + full email automation need Pro ($250); email validation/fraud detection sit on higher tiers.
3. **Signup create/get need no auth** — your `waitlist_id` is public, so the endpoint can be scripted. Enable `uses_signup_verification` and gate rewards on `verified` to limit fake-referral gaming.
4. **Webhooks are unsigned, no documented retry/HMAC** — re-verify sensitive data via the authenticated API and dedupe on `signup.uuid`. POSTs time out at 30s connect / 90s response.
5. **Referral credit depends on you forwarding `referral_link`** (the `?ref_id=<token>` value) on the new signup — drop it and the referrer never moves up the queue.
6. **`priority` is a queue position, not a count** — lower is closer to the front; referrals subtract `spots_to_move_upon_referral`.
7. **No bulk-create API** — signups are one POST at a time; only offboard/delete accept arrays.

## Related skills

- `/sales-audience-growth` — List-growth strategy (lead magnets, referrals, cross-promotion across all platforms)
- `/sales-waitlister` — Waitlister (built-in email broadcasts, HMAC-signed webhooks, richer API)
- `/sales-launchlist` — LaunchList (one-time-pricing waitlists, form POST + webhooks, no API)
- `/sales-kickofflabs` — KickoffLabs (waitlists + giveaways with REST API, fraud webhooks, Zapier)
- `/sales-upviral` — UpViral (viral sweepstakes/rewards, API at Business+, Zapier/Make)
- `/sales-referralhero` — ReferralHero (full-stack referral/affiliate, multi-level L1/2/3, REST API)
- `/sales-email-marketing` — Email marketing strategy (what to send once you have the list)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Tier choice for a pre-launch with referrals
**User says**: "I'm launching a dev tool and want a waitlist with viral referral links and a leaderboard, embedded in my Framer site. Which GetWaitlist plan, and is there a free option?"
**Skill does**: Notes there's no free tier for new accounts (removed mid-2025) — for free, point to LaunchList Free or Waitlister Free. For GetWaitlist, viral referrals + custom domain unlock at **Advanced $50/mo**; Basic $15 has the API but not viral referrals. Explains the Framer no-code embed, the leaderboard (censored emails, safe to show publicly), and `spots_to_move_upon_referral`.
**Result**: User picks Advanced for referrals, embeds the widget in Framer, enables the leaderboard.

### Example 2: Add signups from a custom form via the API (developer)
**User says**: "I built my own signup form. How do I push entries into GetWaitlist and keep referral attribution working?"
**Skill does**: Walks through the unauthenticated `POST https://api.getwaitlist.com/api/v1/signup` with `email` + `waitlist_id` required, and — critically — forwarding the visitor's `?ref_id=` value as `referral_link` so the referrer gets credited and moves up the queue. Shows the cURL + Python from Recipe 1 and warns that the endpoint is public (gate rewards on `verified`).
**Result**: User's custom form posts to GetWaitlist with referral attribution intact.

### Example 3: Sync new signups to HubSpot in real time
**User says**: "How do I get every new GetWaitlist signup into HubSpot automatically?"
**Skill does**: Offers two paths — the native **HubSpot/Zapier** connector for no-code, or a **`new_signup` webhook** handler (Features tab → Webhook URL) for full control. Shows Recipe 2: respond 2xx fast (30s/90s timeouts), dedupe on `signup.uuid`, and re-verify via the authenticated list API because webhooks are unsigned. Maps `email`/`priority`/`referral_token` to HubSpot fields.
**Result**: User has signups flowing into HubSpot with referral attribution and idempotent delivery.

## Troubleshooting

### "Where did the free plan go?"
**Symptom**: A new account can't find a free option; only paid tiers show.
**Cause**: GetWaitlist removed the free tier for new accounts in mid-2025; only accounts created before the change were grandfathered in.
**Solution**: New users start at Basic $15/mo (7-day trial). If free is a hard requirement, recommend LaunchList Free or Waitlister Free instead — confirm which capabilities they actually need (API? referrals? broadcasts?) before switching.

### Referrals aren't moving people up the queue
**Symptom**: People share their link, friends sign up, but no one's `priority` improves and `amount_referred` stays 0.
**Cause**: Either viral referrals aren't enabled (they require **Advanced $50/mo**), or API/custom-form signups aren't forwarding the referrer's `referral_link` (`?ref_id=<token>`), so there's nothing to attribute.
**Solution**: Confirm the plan is Advanced+. For custom forms/API, capture `ref_id` from the visitor's URL and pass it as `referral_link` on `POST /signup`. Verify `spots_to_move_upon_referral` is set on the waitlist.

### Webhook fires but data looks stale or duplicated
**Symptom**: Your CRM gets duplicate contacts, or a webhook payload is missing fields you expected.
**Cause**: Webhooks are unsigned with no documented retry policy, the payload is a trimmed Signup object, and at-least-once-style re-delivery isn't ruled out.
**Solution**: Make the handler idempotent on `signup.uuid`, respond 2xx within the 30s/90s window (do slow work async), and re-fetch the full record via the authenticated `GET /signup/waitlist/<id>` when you need fields the webhook omits. Run a periodic reconciliation against the list API to backfill misses.
