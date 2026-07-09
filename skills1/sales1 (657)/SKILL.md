---
name: sales-waitlistly
description: "Waitlistly platform help — hosted pre-launch waitlist landing pages for validating a startup idea and collecting emails before you build (waitlistly.live), with custom domains and on-signup webhooks that push real-time lead data to Zapier, Make, Slack, or your own endpoint. Use when launching a waitlist landing page to validate demand before building, picking Waitlistly vs Waitlister/GetWaitlist/LaunchList for a simple idea-validation waitlist, pointing a custom domain at your Waitlistly page, wiring new-signup webhooks into a CRM/ESP/Slack when Waitlistly has no public REST API, figuring out how to send launch emails when Waitlistly only collects signups, or confirming what's free vs paid. Do NOT use for general list-growth strategy across platforms (use /sales-audience-growth) or a richer documented waitlist API/broadcasts (use /sales-waitlister or /sales-getwaitlist)."
argument-hint: "[describe what you need help with in Waitlistly]"
license: MIT
version: 1.0.0
tags: [sales, waitlist, idea-validation, viral-marketing, platform]
---

# Waitlistly Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Spin up a waitlist landing page to validate an idea before building
   - B) Point your own custom domain at the Waitlistly page
   - C) Get signups out of Waitlistly — on-join webhooks into Zapier / Make / Slack / your own API
   - D) Send launch or nurture emails to people who joined (Waitlistly collects; an ESP usually sends)
   - E) Figure out pricing / what's free vs paid
   - F) Decide whether Waitlistly is the right fit, or a richer waitlist tool is

2. **Where will the page live?** Hosted Waitlistly page on a Waitlistly subdomain vs your own custom domain — drives the DNS/custom-domain path.

3. **Where do signups need to end up?** Stay in Waitlistly / flow to an ESP (which?) / CRM / Slack — drives whether you wire the webhook to Zapier/Make or a custom endpoint.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list-growth strategy across platforms | `/sales-audience-growth [question]` |
| A waitlist with a documented REST API + built-in email broadcasts | `/sales-waitlister [question]` |
| A developer-friendly waitlist with an unauthenticated signup API + leaderboard | `/sales-getwaitlist [question]` |
| One-time-pricing waitlist, form POST + webhooks, no API | `/sales-launchlist [question]` |
| Waitlists + giveaways with REST API + fraud webhooks | `/sales-kickofflabs [question]` |
| Sending the actual launch/nurture emails once you have the list | `/sales-email-marketing [question]` |

When routing, give the exact command, e.g.: "This is a list-growth-strategy question — run: `/sales-audience-growth [your question]`."

If the question is Waitlistly-specific, continue to Step 3.

## Step 3 — Waitlistly platform reference

**Read `references/platform-guide.md`** for the full reference — what's verified vs unconfirmed, capabilities tagged by automation surface (custom domains, on-signup webhooks → Zapier/Make/Slack/custom endpoint), the idea-validation playbook, integration recipes (generic webhook→CRM handler), and a fit comparison vs Waitlister / GetWaitlist / LaunchList / KickoffLabs.

**Read `references/waitlistly-api-reference.md`** for the programmatic surface — there is **no public REST API** and **no public docs/pricing page** (the sitemap has only `/`, `/growth`, `/help`, `/contact`, `/login`, `/signup`, `/privacy`, `/terms`). What exists: on-signup **webhooks** ("real-time lead data to Zapier, Make, Slack, or your own API") and **custom domains**. The webhook payload schema is not publicly documented — inspect a live delivery before mapping fields.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **It's a validation-first waitlist builder, not an ESP.** The job is to stand up a landing page fast and capture emails before you build. Treat downstream email (launch/nurture) as a separate step through your ESP.
- **The only documented automation is the on-signup webhook** → Zapier, Make, Slack, or your own endpoint (Help → Webhooks/Integrations). There is **no public REST API** to read, update, or delete signups programmatically.
- **Don't hard-code the webhook payload.** The schema isn't published — log one real delivery, confirm the field names, then map into your CRM/ESP.
- **Custom domains are supported** (Help → Custom Domains): point a domain/subdomain via DNS at your Waitlistly page; allow for propagation.
- **Pricing isn't on the public site.** It's "free to start"; tiers and limits live behind sign-in — confirm in-app and treat any figure as best-effort, not quoted.
- **It's a young, ultra-niche tool with little public track record.** If the user needs a documented API, signed webhooks, built-in broadcasts, or a leaderboard/referral system they can rely on, point them to `/sales-waitlister` or `/sales-getwaitlist`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing that may shift. Waitlistly's marketing pages are JS-rendered and there are no third-party reviews, so several specifics below are unconfirmed.*

1. **No public REST API.** Ingress is the hosted/custom-domain signup page; egress is the on-signup webhook + Zapier/Make/Slack. There's no documented endpoint to list, update, or delete signups in code.
2. **No public pricing page.** The sitemap has no `/pricing`; "free to start" is the only confirmed claim. Verify tiers and subscriber/limit caps inside the app before budgeting.
3. **Webhook payload schema is undocumented.** Treat it as opaque until you inspect a real delivery — don't build a handler against assumed field names.
4. **Not an email sender.** Waitlistly captures signups; the launch announcement and nurture sequence run from your ESP. Wire signups over via the webhook (or a Zapier/Make step) and gate launch sends there.
5. **`/growth` page wouldn't render** during research, so referral/viral mechanics couldn't be confirmed. If a user expects a leaderboard or position-jumping referrals, verify it exists before promising it — or use a tool where it's documented (`/sales-waitlister`, `/sales-getwaitlist`, `/sales-kickofflabs`).
6. **Young, low-coverage tool.** Limited track record and docs ("More Guides Coming Soon"). For mission-critical launches, weigh a more established waitlist platform.

## Related skills

- `/sales-audience-growth` — List-growth strategy (lead magnets, referrals, cross-promotion across all platforms)
- `/sales-waitlister` — Waitlister (built-in email broadcasts, REST API + HMAC-signed webhooks, points-based referrals)
- `/sales-getwaitlist` — GetWaitlist (developer-friendly widget, unauthenticated signup API, censored leaderboard)
- `/sales-launchlist` — LaunchList (one-time-pricing waitlists, form POST + webhooks, no API)
- `/sales-kickofflabs` — KickoffLabs (waitlists + giveaways with REST API + fraud webhooks)
- `/sales-email-marketing` — Email marketing strategy (what to send once you have the list)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Fast idea validation on my own domain
**User says**: "I want to test demand for a SaaS idea before I build it — a clean waitlist page on my own domain, free if possible. Is Waitlistly the right pick or should I use something else?"
**Skill does**: Confirms Waitlistly's sweet spot — a hosted waitlist landing page you can stand up in minutes for idea validation, with custom-domain support and "free to start" (tiers unconfirmed, verify in-app). Notes there's no public API and no confirmed referral leaderboard, so if they want viral referrals or a documented API they should compare `/sales-waitlister` or `/sales-getwaitlist`. Frames the validation goal: a signal threshold (e.g., signups/visitor) that tells them whether to build.
**Result**: User launches a custom-domain waitlist page and sets a demand threshold before writing code.

### Example 2: Pipe new signups into HubSpot and Slack (developer/automation)
**User says**: "How do I get every new Waitlistly signup into HubSpot and ping our #launch Slack channel in real time?"
**Skill does**: Points to Help → Webhooks/Integrations: enable the on-signup webhook to Zapier/Make (no-code → HubSpot + Slack steps) or to your own endpoint. Walks the generic receiver recipe from `references/platform-guide.md`: accept the POST, **log the first delivery to learn the payload shape** (schema is undocumented), dedupe on whatever stable id the payload carries, then map email/created-at into a HubSpot contact and post a Slack message. Warns there's no signature documented, so use an unguessable URL and validate payload shape.
**Result**: User has signups flowing to HubSpot and Slack, with a handler built against the real (inspected) payload rather than guessed fields.

### Example 3: Sending the launch email to everyone who joined
**User says**: "Launch day is here. How do I email everyone on my Waitlistly list?"
**Skill does**: Explains Waitlistly collects signups but isn't an ESP — the send goes through your email tool. Two paths: (a) if the on-signup webhook → Zapier/Make → ESP was set up from day one, the contacts are already in your ESP, so broadcast there; (b) otherwise, export/forward the list into your ESP first. Hands off the campaign itself to `/sales-email-marketing`.
**Result**: User sends the launch broadcast from their ESP, with Waitlistly as the capture layer.

## Troubleshooting

### Signups land in Waitlistly but never reach my CRM/email tool
**Symptom**: The Waitlistly dashboard shows signups; HubSpot/Slack/your ESP shows nothing.
**Cause**: No automation is wired up — Waitlistly's only documented egress is the on-signup webhook (to Zapier, Make, Slack, or your own API). Nothing flows out by default, and there's no REST API to pull from.
**Solution**: In Help → Webhooks/Integrations, enable the webhook and connect it to Zapier/Make (no-code) or your own endpoint. Inspect one real delivery to confirm the payload fields before mapping them, then dedupe on a stable id so retries don't double-create contacts.

### I can't find the pricing or what's included for free
**Symptom**: There's no pricing page; you can't tell what the free tier covers or where limits kick in.
**Cause**: Waitlistly has no public `/pricing` page — pricing and limits live behind sign-in. "Free to start" is the only confirmed public claim.
**Solution**: Sign in to see current tiers and caps, and treat any number you find elsewhere as best-effort, not quoted. If a hard free-forever guarantee or transparent published pricing matters, compare `/sales-launchlist` (one-time pricing) or `/sales-waitlister` (published tiers, free plan).

### My custom domain isn't resolving on the Waitlistly page
**Symptom**: You pointed a domain at Waitlistly but it doesn't load, or shows a certificate/404 error.
**Cause**: DNS records aren't pointed correctly yet, or propagation/SSL issuance hasn't completed.
**Solution**: Follow Help → Custom Domains to set the DNS record Waitlistly specifies, then allow time for propagation and certificate issuance (often up to 24–48h). Re-check in the dashboard's domain settings; if it persists, contact Waitlistly via the `/contact` page since there's no status API to query.
