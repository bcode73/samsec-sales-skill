---
name: sales-referlist
description: "Referlist platform help — no-code pre-launch waitlist with gamified Dropbox/Robinhood-style referrals (referlist.co): visitors join, see their place in line, and move up the queue by sharing a unique referral link. Use when adding a viral referral waitlist to a landing page without coding, embedding Referlist on Webflow/Squarespace/Wix or in a React/Next.js app via the npm SDK, fixing a Next.js 'window is not defined' SSR error from the SDK, the manual window.referlist.addToWaitlist(domain, email, referralCode) call not crediting referrals or moving people up, using the REST API (Pro plan) to add signups / look up an email's place in line / list the whole waitlist, exporting signups to Mailchimp/Airtable/CSV, seeding a waitlist so it doesn't look empty, or choosing between the Free, Growth, Pro, and Enterprise plans. Do NOT use for general list-growth strategy across platforms (use /sales-audience-growth) or picking the ESP you broadcast the launch from (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in Referlist]"
license: MIT
version: 1.0.1
tags: [sales, waitlist, referral-program, viral-marketing, platform]
---

# Referlist Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Add a viral referral waitlist to a landing page — which of the 5 install methods (embedded form, npm SDK, JS snippet + element IDs, manual `addToWaitlist` call, REST API)
   - B) Integrate the npm SDK in a React/Next.js app (incl. the SSR `window` workaround)
   - C) Use the REST API (Pro+) — add signups, get an email's place in line, list the waitlist, attach a referral code
   - D) Get signups out — export to Mailchimp / Airtable / CSV
   - E) Set up referral mechanics — unique links, queue jumping, position display, seeding
   - F) Pick a tier — Free (100) vs Growth $29 (500) vs Pro $59 (3,000, API) vs Enterprise (unlimited)
   - G) Compare Referlist to Waitlister / GetWaitlist / LaunchList / Viral Loops

2. **Where will the form live?** Hosted Referlist page / a no-code builder (Webflow, Squarespace, Wix) / a React/Next.js app — drives embed vs SDK vs API.

3. **Where do signups need to end up?** Stay in Referlist / Mailchimp / Airtable / your own backend — drives export vs the Pro REST API.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list-growth strategy across platforms | `/sales-audience-growth [question]` |
| A waitlist with built-in email broadcasts + HMAC-signed webhooks | `/sales-waitlister [question]` |
| A developer waitlist with an unauthenticated signup API + censored leaderboard | `/sales-getwaitlist [question]` |
| One-time-pricing waitlist (form POST + webhooks, no API) | `/sales-launchlist [question]` |
| Waitlists + giveaways/contests with fraud webhooks | `/sales-kickofflabs [question]` |
| Sending the actual launch/nurture campaign to the list | `/sales-email-marketing [question]` |

When routing, give the exact command, e.g.: "This is a list-growth-strategy question — run: `/sales-audience-growth [your question]`."

If the question is Referlist-specific, continue to Step 3.

## Step 3 — Referlist platform reference

**Read `references/platform-guide.md`** for the full reference — the 5 install methods, capabilities tagged by automation surface, pricing and plan gates, referral/seeding mechanics, export integrations, quick-start recipes (Next.js SDK with SSR workaround; manual `addToWaitlist` with referral attribution; signups→Mailchimp), and a fit comparison vs Waitlister / GetWaitlist / LaunchList / Viral Loops.

**Read `references/referlist-api-reference.md`** for the programmatic surface — the client-side SDK (`referlist.initialize({ domain })`, element IDs `referlistemail`/`referlistbutton`, `window.referlist.addToWaitlist(domain, email, referralCode)`) verbatim, plus the **Pro-gated REST API** capabilities (add signup, get an email's place in line, list signups, referral code). The REST base URL, auth, and exact paths are **not in the public docs index** (docs.referlist.co is JS-rendered) — they're listed under `## Gaps` to verify, not invented.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Pick the lightest install that fits.** Pure no-code site → embedded form or JS snippet. React/Next.js → the npm SDK. Custom backend or server-side adds → the REST API (Pro only).
- **The REST API is Pro-gated ($59/mo).** Below Pro, programmatic access is the client-side SDK plus CSV/Mailchimp/Airtable export — there's no server-side read/write API on Free/Growth.
- **Next.js SSR breaks the SDK** unless you `dynamic(import, { ssr: false })` — the library touches `window`. This is the single most common integration failure.
- **Referral attribution is your job to forward.** Capture the visitor's referral code (from the URL) and pass it as the 3rd arg of `addToWaitlist` (or let the snippet handle it) — omit it and the referrer never moves up.
- **No confirmed webhooks/Zapier.** Treat egress as API polling (Pro) or export (Mailchimp/Airtable/CSV). If you need push notifications, verify webhooks exist before designing around them — or use `/sales-waitlister` / `/sales-kickofflabs`.
- **Seed the list (Pro+)** so a brand-new waitlist doesn't look empty, but keep seeds honest.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing that may shift. Referlist's docs site is JS-rendered, so REST API specifics below are flagged for verification.*

1. **REST API is Pro-gated ($59/mo).** Free and Growth have no server-side API — only the client-side SDK + export. Don't promise an API integration on a cheaper tier.
2. **Next.js "window is not defined".** The SDK runs client-side; import it with `dynamic(() => import(...), { ssr: false })` or guard on `typeof window !== 'undefined'`.
3. **REST base URL / auth aren't in the public docs index.** docs.referlist.co is a JS-rendered SPA; the SDK GitHub repo is client-side only (last updated 2022). Verify the base URL, auth header, and endpoint paths in the live (signed-in) docs before building — they are **not** documented in this skill, only the capabilities are.
4. **Referral code must be forwarded.** Manual `addToWaitlist(domain, email, referralCode)` calls that omit the code, or pages that don't capture the inbound `?ref` param, record the signup but credit no one — so positions never move.
5. **Plan caps are on signups, and export is gated.** Free = 100 signups, Growth = 500, Pro = 3,000, Enterprise = unlimited (usage-based ~$0.01/signup/mo). Collecting past your cap or exporting beyond Free's 100 needs an upgrade.
6. **Branded email-sending domain, waitlist seeding, and multi-language are Pro+.** On Free/Growth, confirmation emails come from a Referlist domain and there's a watermark on Free.
7. **No confirmed webhooks or Zapier.** Egress is the Pro REST API (poll) or CSV/Mailchimp/Airtable export. Verify before assuming real-time push exists.
8. **Pricing is best-effort.** An older Product Hunt listing cited "$50/mo unlimited"; current public pricing is Growth $29 / Pro $59 / usage-based Enterprise. Re-check the live pricing page.

## Related skills

- `/sales-audience-growth` — List-growth strategy (lead magnets, referral design, cross-promotion across all platforms)
- `/sales-waitlister` — Waitlister (built-in email broadcasts, documented REST API + HMAC-signed webhooks)
- `/sales-getwaitlist` — GetWaitlist (developer widget, unauthenticated signup API, censored public leaderboard)
- `/sales-launchlist` — LaunchList (one-time-pricing waitlists, form POST + webhooks, no API)
- `/sales-kickofflabs` — KickoffLabs (waitlists + giveaways with REST API + fraud webhooks)
- `/sales-email-marketing` — Email marketing strategy (what to send once you have the list)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: No-code viral waitlist on a Webflow landing page
**User says**: "I have a Webflow landing page and want a waitlist where people move up by referring friends, without writing code. How do I set it up with Referlist?"
**Skill does**: Recommends the embedded signup form or the JS-snippet method (add the snippet, then put `id="referlistemail"` on the email input and `id="referlistbutton"` on the button). Explains the visitor sees their place in line + a unique referral link, and each referred join moves them up. Notes Free covers 100 signups (Growth $29 for 500 + no watermark), and that confirmation emails come from a Referlist domain until Pro.
**Result**: User has a gamified referral waitlist live on Webflow with no code.

### Example 2: React/Next.js SDK integration with referral attribution (developer/automation)
**User says**: "I'm adding Referlist to my Next.js app via the npm package but I get 'window is not defined', and when I call addToWaitlist manually nobody gets referral credit."
**Skill does**: Fixes the SSR error by loading the SDK with `dynamic(() => import('referlist'), { ssr: false })` (or a `useEffect` mount guard), then calling `referlist.initialize({ domain: 'YOUR_DOMAIN' })`. For attribution, shows reading the inbound `?ref=` code from the URL and passing it as the 3rd arg: `window.referlist.addToWaitlist('YOUR_DOMAIN', email, referralCode)` — omitting it is why no one moved up. Points to Recipe 1/2 in `references/platform-guide.md`.
**Result**: SDK initializes client-side and referral codes credit the right referrer.

### Example 3: Tier choice + getting signups into Mailchimp
**User says**: "I expect ~2,000 signups and need them all in Mailchimp. Which Referlist plan, and how do I sync?"
**Skill does**: Recommends Pro ($59/mo, 3,000 signups) since Growth caps at 500; notes Pro also unlocks the REST API and branded email domains. For Mailchimp, points to the native export (CSV/Mailchimp/Airtable) for a one-shot/manual sync, or the Pro REST API to pull the list programmatically on a schedule. Hands off the launch broadcast itself to `/sales-email-marketing`.
**Result**: User picks Pro and has a path to keep Mailchimp in sync with the waitlist.

## Troubleshooting

### Next.js build/runtime fails with "window is not defined"
**Symptom**: Importing or initializing the Referlist SDK crashes during SSR/build.
**Cause**: The SDK accesses the browser `window` object and must run client-side.
**Solution**: Load it with `dynamic(() => import('referlist'), { ssr: false })`, or import inside a `useEffect`/`componentDidMount` that only runs in the browser, then call `referlist.initialize({ domain: 'YOUR_DOMAIN' })`. Don't import it at module top level in a server component.

### Referrals aren't crediting / positions don't move
**Symptom**: People share their link and friends join, but no one moves up the queue and referral counts stay flat.
**Cause**: The referral code isn't being captured/forwarded — either the inbound `?ref` param isn't read, or the manual `addToWaitlist` call omits the 3rd `referralCode` argument.
**Solution**: If using the auto element-ID method, confirm `referlistemail`/`referlistbutton` are set and the page is loaded with the referral URL. If calling the API manually, capture the referral code from the visitor's URL and pass it: `window.referlist.addToWaitlist('YOUR_DOMAIN', email, referralCode)`. Verify in the dashboard that the referrer's position updates.

### I can't export my signups (or hit a cap)
**Symptom**: Export is blocked, or you can't collect/export beyond a certain number.
**Cause**: Plan caps — Free is 100 signups and export beyond 100 is gated; Growth is 500; Pro is 3,000.
**Solution**: Upgrade to the tier that covers your volume (Growth $29 / Pro $59 / Enterprise usage-based), then export to CSV, Mailchimp, or Airtable. For ongoing programmatic sync, use the REST API on Pro rather than repeated manual exports.
