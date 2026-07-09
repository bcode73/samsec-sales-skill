---
name: sales-waitlister
description: "Waitlister platform help — pre-launch waitlist platform with hosted landing pages, points-based viral referrals, built-in email broadcasts, REST API, and five HMAC-signed webhook events. Use when choosing Free (100 subscribers) vs Launch $15/mo (unlimited subs, referrals + broadcasts) vs Growth $49/mo (API, webhooks, Klaviyo/Mailchimp/Kit sync, fraud detection unlock here) vs Business $129/mo, building a webhook handler that verifies X-Webhook-Signature, webhooks auto-disabled after 10 consecutive failures, API signups bypassing referral fraud detection because client_ip/fingerprint weren't forwarded, granting bonus points or pulling top referrers via the API for reward fulfillment, broadcast send caps forcing an ESP handoff, automating without Zapier (Waitlister has none — webhooks/API only), or comparing Waitlister vs LaunchList/KickoffLabs/GetWaitlist/Prefinery. Do NOT use for list-growth strategy (use /sales-audience-growth) or LaunchList help (use /sales-launchlist)."
argument-hint: "[describe what you need help with in Waitlister]"
license: MIT
version: 1.0.0
tags: [sales, waitlist, referral-program, viral-marketing, platform]
---

# Waitlister Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Pick a tier — Free (100 subs) vs Launch $15/mo (unlimited subs, referrals + broadcasts) vs Growth $49/mo (API + webhooks) vs Business $129/mo
   - B) Build the waitlist — hosted landing page vs embedded form vs custom form via API
   - C) Set up referrals — points, leaderboard, position inflation, milestones
   - D) Wire data out — webhooks, REST API, Klaviyo/Mailchimp/Kit connectors, CSV
   - E) Email the list — welcome emails, broadcasts, send caps, double opt-in
   - F) Fight referral fraud — built-in detection, API fraud params
   - G) Compare Waitlister vs LaunchList / KickoffLabs / GetWaitlist / Prefinery / Viral Loops

2. **Where will signups happen?** Hosted page / embed on your site (which builder?) / your own backend via API — drives install path and whether fraud params matter.

3. **Where must the data end up?** Stays in Waitlister / ESP (which?) / CRM / warehouse — drives whether you need Growth ($49) for API/webhooks/connectors.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list growth strategy across platforms | `/sales-audience-growth [question]` |
| LaunchList (one-time-pricing waitlists, no API) | `/sales-launchlist [question]` |
| KickoffLabs (waitlists + giveaways, Zapier, fraud webhooks) | `/sales-kickofflabs [question]` |
| UpViral (B2C sweepstakes/points campaigns) | `/sales-upviral [question]` |
| Multi-level referral/affiliate (L1/2/3, coupon groups) | `/sales-referralhero [question]` |
| No-code merge-tag newsletter referrals | `/sales-referralkit [question]` |
| ESP setup (Klaviyo, Mailchimp, Kit) | `/sales-klaviyo`, `/sales-mailchimp`, `/sales-kit` |
| Email marketing strategy once the list exists | `/sales-email-marketing [question]` |

If the question is Waitlister-specific, continue to Step 3.

## Step 3 — Waitlister platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities tagged by automation surface, pricing and plan gates, integrations, subscriber data model, quick-start recipes (server-side signup with fraud params, signed webhook handler, reward fulfillment via points API), integration patterns, and the comparison grid.

**Read `references/waitlister-api-reference.md`** for the API — base URL `https://waitlister.me/api/v1`, `X-Api-Key` auth, 5 endpoints with verbatim request/response JSON, page/limit pagination (max 100), per-plan rate limits (60/120 RPM), and all five webhook event payloads verbatim with the HMAC SHA-256 verification scheme.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **API, webhooks, ESP connectors, and fraud detection all unlock at Growth ($49/mo).** Free and Launch are UI + CSV only. Any programmatic pipeline = Growth minimum.
- **No Zapier/Make/MCP** — automation means webhooks (5 signed events) or the REST API. If the user expects Zapier, KickoffLabs or UpViral have it; with Waitlister they write a small handler instead.
- **Always verify `X-Webhook-Signature`** (HMAC SHA-256 over the raw body) and dedupe on `X-Waitlister-Delivery` — deliveries retry and are at-least-once.
- **Respond to webhooks in <15s with a 2xx** — 10 consecutive failures auto-disables the webhook and it stays off until manually re-enabled.
- **API signups skip fraud detection unless you forward `metadata.client_ip` and `fingerprint`** — server-side integrations silently lose referral fraud protection without them.
- **`points` on update-subscriber is absolute, not incremental** — read current points, then write the new total.
- **Broadcasts are capped monthly** (2,500 Launch / 10K Growth / 50K Business) with no documented overage — for segmented or high-volume email, sync to Klaviyo/Mailchimp/Kit and send from there.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06-06) — review these, especially plan-gated features and pricing that may shift.*

1. **No Zapier, Make, or MCP server.** The automation surface is webhooks + REST API only — budget a small handler if you'd normally reach for a Zap.
2. **API + webhooks gated to Growth ($49/mo).** Rate limits also differ by plan: 60 RPM (Growth) vs 120 RPM (Business) on subscriber endpoints; log-view gets 200/400 RPM.
3. **Webhooks auto-disable after 10 consecutive failures** and require manual re-enabling — a dead endpoint over a launch weekend means silently lost events. Monitor the webhook status.
4. **API signups bypass referral fraud detection** unless `metadata.client_ip` (and ideally `fingerprint`) are forwarded from the end user.
5. **`points` is a write-the-total field**, not an increment — concurrent bonus grants can race; serialize updates per subscriber.
6. **Broadcast caps are monthly and per-plan** (2,500/10K/50K); overage behavior undocumented. Referral reward customization and email segmentation are limited (AppSumo reviewer complaints) — complex reward tiers or segmented sends belong in your ESP.
7. **No delete-subscriber API endpoint** — GDPR erasure is a dashboard operation.
8. **Double opt-in changes the API response shape** — check `is_pending_confirmation`; pending signups that never confirm fire `subscriber_pending_expired`, not `signup_created` follow-ups.
9. **Custom domains need Growth+ ($49/mo)** — Launch keeps you on waitlister.me URLs (branding removed at Launch, domain not custom).

## Related skills

- `/sales-audience-growth` — List-growth strategy (lead magnets, referrals, cross-promotion across all platforms)
- `/sales-launchlist` — LaunchList (one-time-pricing waitlists, form POST + webhooks, no API)
- `/sales-kickofflabs` — KickoffLabs (waitlists + giveaways with REST API v1+v2, fraud webhooks, Zapier)
- `/sales-upviral` — UpViral (viral sweepstakes/rewards, API at Business+, Zapier/Make)
- `/sales-referralhero` — ReferralHero (full-stack referral/affiliate, multi-level L1/2/3, REST API)
- `/sales-referralkit` — ReferralKit (no-code merge-tag newsletter referrals)
- `/sales-klaviyo` — Klaviyo platform help (native connector destination)
- `/sales-mailchimp` — Mailchimp platform help (native connector destination)
- `/sales-kit` — Kit platform help (native connector destination)
- `/sales-email-marketing` — Email marketing strategy (what to send once you have the list)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Tier choice for a SaaS beta launch
**User says**: "Launching a SaaS beta in 8 weeks. I want referral-driven signups and everything synced into Klaviyo automatically. Which Waitlister plan?"
**Skill does**: Recommends Growth ($49/mo) — the Klaviyo connector, webhooks, API, and fraud detection all unlock there; Launch ($15/mo) covers referrals + broadcasts but exports are CSV-only. Notes unlimited subscribers from Launch up, the 10K/mo email cap on Growth, and that yearly billing is ~2 months free. Suggests sending segmented campaigns from Klaviyo rather than Waitlister broadcasts.
**Result**: User picks Growth annual, connects Klaviyo, keeps Waitlister broadcasts for simple all-list updates.

### Example 2: Signed webhook handler (developer)
**User says**: "How do I build a webhook handler for Waitlister signups that pushes them into HubSpot and credits referrers in real time?"
**Skill does**: Walks through Integrations → Webhooks → Manage with a secret set, then Recipe 2 from `references/platform-guide.md`: verify `X-Webhook-Signature` (HMAC SHA-256 over raw body, `hmac.compare_digest`), dedupe on `X-Waitlister-Delivery`, route `waitlist.signup_created` → HubSpot contact create and `waitlist.referral_completed` → referrer score bump, respond 2xx within 15s, and monitor for the 10-failure auto-disable.
**Result**: User has a verified, idempotent handler feeding HubSpot with referral attribution.

### Example 3: Referral rewards aren't protected from cheaters
**User says**: "People are gaming our waitlist referral rewards with fake signups. We add some subscribers through our own backend too. What do we do?"
**Skill does**: Confirms fraud detection requires Growth+; for API-added subscribers, shows the `metadata.client_ip` + `fingerprint` params (without them API signups bypass detection entirely). Recommends double opt-in so unconfirmed referrals don't count, watching `referral_completed` webhooks for same-IP velocity, and fulfilling rewards from verified milestones (`milestone_reached`) rather than raw referral counts.
**Result**: User enables double opt-in + fraud params and gates rewards on verified milestones.

## Troubleshooting

### Webhook stopped firing mid-campaign
**Symptom**: Events arrived for days, then silence — no deliveries at all
**Cause**: The webhook auto-disabled after 10 consecutive failures (endpoint down, >15s responses, or non-2xx replies); it does not self-recover
**Solution**: Fix the endpoint first (respond 2xx in <15s; do slow work async), then manually re-enable under Integrations → Webhooks → Manage. Backfill the gap via `GET /subscribers` sorted by date. Add monitoring on the webhook's Active/Inactive/Disabled status.

### Referral fraud detection isn't catching obvious fakes
**Symptom**: Same-IP or disposable signups counting toward rewards despite fraud detection being on
**Cause**: Signups came through the API without `metadata.client_ip`/`fingerprint` (detection has nothing to inspect), or plan is below Growth
**Solution**: Forward the real end-user IP and a browser fingerprint on every API signup. Enable double opt-in so unconfirmed emails never complete referrals. Gate reward fulfillment on `milestone_reached` events and spot-check top referrers via `GET /subscribers?sort_by=referral_count` before paying out.

### Hitting 429s during bulk export
**Symptom**: `Rate limit exceeded. 60 requests allowed per minute.` while paginating subscribers
**Cause**: Growth plan allows 60 requests/minute on subscriber endpoints (Business: 120); pagination max is 100 per page
**Solution**: Request `limit=100`, watch `X-RateLimit-Remaining`, and on 429 back off exponentially (docs suggest up to 30s max across 5 attempts) or sleep until `X-RateLimit-Reset`. For recurring syncs, prefer webhooks (push) over polling. Business doubles the limit if exports are routinely large.
