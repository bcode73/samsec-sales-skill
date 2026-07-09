---
name: sales-tuemilio
description: "Tuemilio platform help — early-access waitlist and pre-launch validation tool with a built-in viral referral loop, leaderboards, white-labeled subscriber dashboards, and email marketing (tuemilio.com). Use when embedding the Tuemilio waitlist with referral position tracking on a landing page or React/Next.js app via the JavaScript SDK, hitting the 'never use the REST API on your frontend' warning, building a server-side REST integration (base tuemilio.com/api/v1, ?api_token= query auth) to create/list/update/delete subscriber emails or add referral points, handling the new-subscriber / grant-access / confirmed-subscriber webhooks into a CRM or Slack, syncing subscribers to Mailchimp or Zapier, granting early access in batches at launch, fighting referral fraud (anti_points, blocked, fraud_id), or choosing Founder $29 vs Startup $49 vs Enterprise. Do NOT use for list-growth strategy across platforms (use /sales-audience-growth) or the launch email campaign itself (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in Tuemilio]"
license: MIT
version: 1.0.0
tags: [sales, waitlist, referral-program, viral-marketing, platform]
---

# Tuemilio Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Embed the waitlist + referral widget on a site or React/Next.js app (JavaScript SDK)
   - B) Build a server-side integration via the REST API (list/create/update/delete emails, add points)
   - C) Handle webhooks — `new-subscriber` / `grant-access` / `confirmed-subscriber` into a CRM, Slack, or warehouse
   - D) Wire up Zapier / Mailchimp / Typeform / Google Analytics
   - E) Run the referral loop — points, leaderboard, position tracking, custom dashboards
   - F) Launch — grant early access in batches and trigger downstream automation
   - G) Fight referral fraud — `points` vs `anti_points`, `blocked`, `fraud_id`
   - H) Pick a tier — Founder $29 vs Startup $49 vs Enterprise

2. **Where will the form live?** Hosted page / a no-code builder / a React/Next.js app — drives the JS SDK install path.

3. **Where do subscribers need to end up?** Stay in Tuemilio / Mailchimp / a CRM / your warehouse — drives webhook vs REST API vs Zapier.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list-growth strategy across platforms | `/sales-audience-growth [question]` |
| A waitlist with built-in email broadcasts + HMAC-signed webhooks | `/sales-waitlister [question]` |
| A developer waitlist with an unauthenticated signup API + censored leaderboard | `/sales-getwaitlist [question]` |
| A cheap no-code referral waitlist with an npm SDK | `/sales-referlist [question]` |
| Waitlists + giveaways/contests with fraud webhooks | `/sales-kickofflabs [question]` |
| The launch/nurture email campaign strategy itself | `/sales-email-marketing [question]` |

When routing, give the exact command, e.g.: "This is a list-growth-strategy question — run: `/sales-audience-growth [your question]`."

If the question is Tuemilio-specific, continue to Step 3.

## Step 3 — Tuemilio platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities tagged by automation surface, pricing and plan gates, the Wait List / Email / Dashboard data model, quick-start recipes (Next.js JS SDK with referral attribution; webhook→CRM handler; server-side REST sync + batch access grant), integration patterns, and a fit comparison vs Waitlister / GetWaitlist / Referlist / LaunchList.

**Read `references/tuemilio-api-reference.md`** for the verbatim API — REST base `https://tuemilio.com/api/v1` with `?api_token=` query auth (Emails: list/get/create/update/delete/add-points; Wait Lists: list/get), the JavaScript SDK (`Tuemilio('init'|'createSubscriber'|'getDashboard'|…)`, config object, event listeners), and the three webhook events with their `X-Tuemilio-Event` header and payload schema.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Frontend = JS SDK, backend = REST API.** The docs are explicit: *never call the REST API from the browser* — the `api_token` is a secret. Use the JS SDK (`createSubscriber`, `getDashboard`, event listeners) client-side; reserve REST for your server.
- **`api_token` rides in the query string**, not a header — keep it out of client code, logs, analytics, and `Referer` headers; rotate it if it leaks.
- **Referral attribution is explicit.** Pass `referralId` to `createSubscriber` (JS) or `referral_id`/`referrer_id` to `POST /emails` (REST) — capture it from the inbound `?r=` link. Omit it and the referrer earns no points and doesn't move up.
- **`add-points` is additive; `PUT /emails` sets points absolutely.** Pick the right one for rewards vs corrections.
- **Webhooks are unsigned.** Use an unguessable URL, switch on `X-Tuemilio-Event`, validate `User-Agent: Tuemilio-Hookshot/1.0`, and dedupe on subscriber `id`.
- **Launch via `grant-access`.** Grant early access in batches (configurable frequency/size); the `grant-access` webhook is your hook for provisioning + a "you're in" email.
- **Fraud signals:** `anti_points`, `blocked`, and `fraud_id` are how Tuemilio flags gaming — gate rewards on clean records.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing that may shift.*

1. **Never use the REST API on the frontend** (documented warning) — the `api_token` query param is a secret. Client-side work goes through the JS SDK; REST is server-only.
2. **`api_token` is a query parameter, not a header** — it can leak via logs, browser history, and `Referer`. Treat the URL as sensitive and rotate on exposure.
3. **Webhooks have no documented signing or retries.** Identify via `X-Tuemilio-Event`, validate the `Tuemilio-Hookshot/1.0` user-agent, use a secret URL, and make handlers idempotent on `id`.
4. **Next.js / SSR:** the loader touches `window` — initialize inside a `useEffect` with a `typeof window !== 'undefined'` guard, and use the **Widget List UUID** (not the numeric list ID) in the snippet.
5. **`add-points` vs `PUT` differ:** `add-points` increments (5 + 2 = 7); `PUT /emails` with `points` overwrites. Using the wrong one silently corrupts leaderboard standings.
6. **Referral code must be forwarded** — `referralId` (JS) / `referral_id` or `referrer_id` (REST), parsed from `?r=`. Missing it = no referral credit.
7. **`confirmed-subscriber` only fires if confirmation emails are enabled** — if you gate access on it without that automation on, the event never arrives.
8. **Pricing is best-effort.** Current public tiers are Founder $29 / Startup $49 / Enterprise (custom), API+webhooks on all tiers, 30-day free trial. Tuemilio previously offered a free tier — verify the live pricing page before quoting.

## Related skills

- `/sales-audience-growth` — List-growth strategy (lead magnets, referral design, cross-promotion across all platforms)
- `/sales-waitlister` — Waitlister (built-in email broadcasts, HMAC-signed webhooks, points-based referrals)
- `/sales-getwaitlist` — GetWaitlist (developer widget, unauthenticated signup API, censored public leaderboard)
- `/sales-referlist` — Referlist (cheap no-code referral waitlist with an npm SDK)
- `/sales-kickofflabs` — KickoffLabs (waitlists + giveaways with REST API + fraud webhooks)
- `/sales-email-marketing` — Email marketing strategy (what to send once you have the list)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Embed the waitlist with referral tracking in Next.js (developer)
**User says**: "I'm adding Tuemilio to my Next.js landing page. How do I show the signup + referral position, and make sure referrals actually credit the referrer?"
**Skill does**: Walks through the JS SDK loader inside a `useEffect` with a `typeof window` guard (Recipe 1), using the Widget List UUID and the `t-signup` div. For attribution, captures the inbound `?r=` value and passes it to `Tuemilio('createSubscriber', { address, referralId })`, and uses `onSubscriberCreated` / `onDashboardData` to render position + leaderboard. Stresses not to call the REST API from the browser.
**Result**: Working client-side widget with referral attribution and a live position dashboard.

### Example 2: Sync new subscribers into a CRM via webhook (developer/automation)
**User says**: "Every new Tuemilio subscriber should create a contact in HubSpot and ping Slack. What's the cleanest way?"
**Skill does**: Recommends the `new-subscriber` webhook (no-code path: Zapier New Subscriber trigger; coded path: your endpoint). Shows the handler from `references/platform-guide.md` Recipe 2 — switch on `X-Tuemilio-Event`, validate `User-Agent: Tuemilio-Hookshot/1.0` and a secret URL (no HMAC exists), dedupe on `id`, map `address`/`position`/`referral_id` into HubSpot, then post to Slack. Notes the `grant-access` event for launch day.
**Result**: New signups flow to HubSpot + Slack idempotently, with a launch-day path ready.

### Example 3: Tier choice + getting subscribers into Mailchimp
**User says**: "Which Tuemilio plan do I need, and how do I keep Mailchimp in sync with my waitlist?"
**Skill does**: Notes API, webhooks, custom domains, and unbranded forms are on **all** tiers, so Founder ($29) covers most solo launches; Startup ($49) adds teams + priority support. For Mailchimp, points to the native auto-sync integration, or a `new-subscriber` webhook / REST `GET /lists/{id}/emails` pull for custom field mapping. Hands the launch campaign itself to `/sales-email-marketing`.
**Result**: User picks Founder and has Tuemilio→Mailchimp sync running.

## Troubleshooting

### Referrals aren't crediting points / positions don't move
**Symptom**: Friends sign up through a referral link but the referrer's `points` and `position` don't change.
**Cause**: The referral code isn't being forwarded — the JS `createSubscriber` call omits `referralId`, or the REST `POST /emails` omits `referral_id`/`referrer_id`, so there's nothing to attribute.
**Solution**: Capture the inbound `?r=` value from the visitor's URL and pass it (`referralId` in the SDK, `referral_id` or `referrer_id` in REST). Confirm in the dashboard that the referrer's points increment; use `add-points` only for manual bonuses (it's additive).

### "Is it safe that my API token is in the URL / can I call the API from the browser?"
**Symptom**: You're tempted to call `tuemilio.com/api/v1/...?api_token=...` from frontend JavaScript.
**Cause**: The REST API authenticates with a secret `api_token` query param and is **not** meant for the browser.
**Solution**: Use the JavaScript SDK client-side (`createSubscriber`, `getDashboard`, events). Keep the REST API and token strictly server-side, out of logs and `Referer` headers; rotate the token at `/profile#api-token` if it was ever exposed.

### Webhook isn't firing or I can't verify it's really Tuemilio
**Symptom**: Your endpoint gets nothing, or you can't tell which event arrived / whether it's authentic.
**Cause**: Either the event isn't subscribed (`confirmed-subscriber` needs confirmation emails enabled), or you're looking for a signature that doesn't exist.
**Solution**: Subscribe to the right event (`new-subscriber` / `grant-access` / `confirmed-subscriber`), read the `X-Tuemilio-Event` header to branch, and since there's no HMAC, authenticate with a secret URL + the `Tuemilio-Hookshot/1.0` user-agent and dedupe on `id`. Test with a real signup and reconcile against `GET /lists/{id}/emails`.
