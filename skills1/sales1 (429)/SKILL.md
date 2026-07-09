---
name: sales-preshiplist
description: "Preshiplist platform help — a no-code pre-launch waitlist builder for SaaS and app makers (preshiplist.co): hosted waitlist landing pages from validated templates, custom domains, AI-written copy, built-in email drip sequences, signup analytics, and multi-product portfolios. Unlike most waitlist tools it sends the launch emails itself, but has no public API, no webhooks, and no Zapier — data only leaves via CSV export. Use when standing up a pre-launch waitlist to validate a SaaS idea, choosing Preshiplist vs Waitlister/GetWaitlist/Waitlistly/LaunchList, pointing a custom domain at a Preshiplist page, getting signups into a CRM when there is no API (CSV only), setting up the built-in drip emails for launch day, or figuring out what the free draft-only plan allows. Do NOT use for cross-platform list-growth strategy (use /sales-audience-growth) or a waitlist with a documented API (use /sales-waitlister or /sales-getwaitlist)."
argument-hint: "[describe what you need help with in Preshiplist]"
license: MIT
version: 1.0.0
tags: [sales, waitlist, idea-validation, email-marketing, platform]
---

# Preshiplist Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Spin up a pre-launch waitlist landing page to validate a SaaS/app idea and collect emails
   - B) Point your own custom domain at the Preshiplist page
   - C) Set up the built-in email drip sequence (confirmation, launch-day, updates)
   - D) Get signups OUT of Preshiplist and into a CRM/ESP (there's no API — CSV export only)
   - E) Manage several products/waitlists from one account (portfolio)
   - F) Figure out pricing / what the free plan does and doesn't allow
   - G) Decide whether Preshiplist is the right fit vs a more developer-friendly waitlist tool

2. **Where will the page live?** A Preshiplist-hosted page vs your own custom domain — drives the DNS/custom-domain path.

3. **Where do signups need to end up?** Stay in Preshiplist and get the launch email from Preshiplist itself / need to reach a CRM or another ESP — drives whether the built-in drips are enough or you need the CSV-export workaround.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General audience/list-growth strategy across platforms | `/sales-audience-growth [question]` |
| A waitlist with a documented REST API + built-in email broadcasts | `/sales-waitlister [question]` |
| A developer waitlist with an unauthenticated signup API + leaderboard | `/sales-getwaitlist [question]` |
| A validation-first waitlist with on-signup webhooks → Zapier/Make/Slack | `/sales-waitlistly [question]` |
| One-time-pricing waitlist, form POST + webhooks | `/sales-launchlist [question]` |
| Waitlists + giveaways/contests with a REST API + fraud webhooks | `/sales-kickofflabs [question]` |
| Designing the broader launch email campaign strategy | `/sales-email-marketing [question]` |

When routing, give the exact command, e.g.: "This is a list-growth-strategy question — run: `/sales-audience-growth [your question]`."

If the question is Preshiplist-specific, continue to Step 3.

## Step 3 — Preshiplist platform reference

**Read `references/platform-guide.md`** for the full reference — what's verified vs unconfirmed, capabilities tagged by automation surface, the built-in email-drip model, the CSV-only egress reality, the validation playbook, and a fit comparison vs Waitlister / GetWaitlist / Waitlistly / LaunchList.

**Read `references/preshiplist-api-reference.md`** for the programmatic surface — there is **no public REST API, no webhooks, and no Zapier/Make**. The sitemap holds only `/`, `/features`, `/pricing`, `/blog`, `/founder-letter`, `/use-cases/*`, `/legal` — no `/api`, `/docs`, or `/integrations`. The only way data leaves Preshiplist is a **manual CSV export**.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **There is no API, no webhooks, and no Zapier/Make.** State this plainly. The only way signup data leaves Preshiplist is a **manual CSV export** from the dashboard. To get signups into a CRM, export the CSV and import it (or script a CSV→CRM job over the exported file) — it is **batch, not real-time**. If real-time sync or an event webhook is a hard requirement, tell the user Preshiplist is the wrong tool and point them to `/sales-getwaitlist`, `/sales-waitlister`, or `/sales-waitlistly`.
- **It sends the launch emails itself — that's the differentiator.** Preshiplist has built-in, auto-branded **drip sequences** (signup confirmation, launch-day announcement, product updates) that you can add/remove/reschedule. So unlike capture-only waitlist tools, you do **not** need a separate ESP for the launch broadcast. Make sure the confirmation email fires immediately on signup (the window between signup and the first share is short).
- **The free plan is draft-only.** On the free tier you can build, customize, and preview a waitlist but **cannot publish it or collect signups** — going live requires a paid tier. Say this explicitly when anyone asks "is there a free plan."
- **Present all pricing as best-effort.** Exact paid prices aren't published on the pricing page (launch/quarterly pricing) — quote tier *names* and structure, flag figures as unconfirmed, and point the user to `preshiplist.co/pricing` to confirm. Refund windows are 30-day (monthly) / 60-day (quarterly) / 90-day (yearly).
- **Multiple products need the higher tier.** One product is allowed on the entry paid tier; **unlimited products + portfolio-wide metrics** require the Serious Builder tier (Lifetime Partner is a one-time-payment version).
- **It's a young indie tool with no public docs.** Verify plan gates, deliverability, and whether any referral mechanism exists in-app before committing a mission-critical launch — the marketing site advertises "no third-party integrations needed," which is a feature framing for a closed, self-contained tool.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-07) — review these, especially plan-gated features and pricing that may shift. Preshiplist publishes no API/docs and no exact prices, so several specifics below are unconfirmed against the live app.*

1. **Free plan can't publish or collect signups.** It's draft/preview only — you must upgrade to a paid tier to launch a live waitlist. Don't promise a "free working waitlist."
2. **No API, no webhooks, no Zapier — CSV export is the only egress.** There is no real-time way to push a new signup anywhere. Getting data into a CRM is a manual (or scripted-over-CSV) batch job. Configure expectations accordingly.
3. **Preshiplist sends the emails, not your ESP.** Drips are built in and auto-branded; you don't wire an external sender. The flip side: you can't easily route those contacts through your own ESP's automations without exporting them first.
4. **Exact prices aren't on the pricing page.** Tiers (Chill Builder / Serious Builder / Lifetime Partner) are named but figures are "limited-time launch pricing" — treat any number as best-effort and confirm in-app.
5. **No documented referral/viral mechanism.** The site markets social-proof signup counts/notifications, not a referral leaderboard or position-jumping. If a user needs viral referrals, verify it exists first or use `/sales-getwaitlist` / `/sales-kickofflabs`.
6. **Young, low-coverage tool.** Little third-party track record and no changelog/docs surfaced. For a launch you can't afford to have wobble, weigh a more established waitlist platform.

## Related skills

- `/sales-audience-growth` — List-growth strategy across all platforms (lead magnets, referral design, cross-promotion, driving traffic to the waitlist)
- `/sales-waitlister` — Waitlister (built-in email broadcasts, REST API + HMAC-signed webhooks, points-based referrals)
- `/sales-getwaitlist` — GetWaitlist (developer widget, unauthenticated signup API, censored leaderboard)
- `/sales-waitlistly` — Waitlistly (validation-first hosted page, custom domains, on-signup webhooks → Zapier/Make/Slack)
- `/sales-launchlist` — LaunchList (one-time-pricing waitlists, form POST + webhooks)
- `/sales-email-marketing` — Broader launch/nurture email campaign strategy
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Validate a SaaS idea with a waitlist that also emails people
**User says**: "I want to test demand for a SaaS idea before building it — a clean waitlist page, and ideally it emails everyone on launch day so I don't have to set up a separate tool. Is Preshiplist right?"
**Skill does**: Confirms Preshiplist's sweet spot — a fast, template-based pre-launch waitlist page (custom domain, AI copy) with **built-in drip emails** (confirmation + launch-day), so it's capture *and* send in one, no separate ESP. Frames the validation goal: a signup threshold that tells them whether to build. Flags two caveats: the free plan is draft-only (can't collect signups until you pay), and it's a closed tool with no API/webhooks, so if they later need CRM integration they'll be exporting CSVs. Sets pricing as best-effort and points to the pricing page.
**Result**: User launches a paid waitlist page, relies on the built-in launch-day drip, and knows the CSV-only limitation up front.

### Example 2: Get signups into HubSpot automatically (developer/automation)
**User says**: "How do I get every new Preshiplist signup into HubSpot automatically?"
**Skill does**: States plainly there is **no public API, no webhooks, and no Zapier** — the only egress is a **manual CSV export**, so there's no real-time path. Gives the realistic workflow: export the signups CSV from the dashboard and import into HubSpot, or automate over the *exported file* (a scheduled script that reads a periodically-exported CSV and upserts contacts via the HubSpot API) — while being explicit that it's batch, not event-driven. Recommends that if real-time CRM sync is a hard requirement, they use `/sales-getwaitlist` (unauthenticated signup API + `new_signup` webhook) or `/sales-waitlister` (REST API + HMAC-signed webhooks) instead.
**Result**: User sets up a periodic CSV export → HubSpot import and understands why a true real-time integration isn't possible on Preshiplist.

### Example 3: What does the free plan actually give me?
**User says**: "Is Preshiplist free? Can I collect emails without paying?"
**Skill does**: Explains the free plan is **draft-only** — you can build, customize, and preview a waitlist but **cannot publish it or collect signups**; going live requires a paid tier (Chill Builder for one product; Serious Builder for unlimited products + portfolio metrics; Lifetime Partner as a one-time payment). Presents prices as best-effort launch pricing and points to `preshiplist.co/pricing`, and notes the 30/60/90-day refund windows.
**Result**: User understands they must upgrade to actually launch, and picks a tier based on how many products they're running.

## Troubleshooting

### I built my waitlist but can't publish it / it won't go live
**Symptom**: The waitlist stays in draft; there's no way to make it public or start collecting signups.
**Cause**: You're on the free plan, which is **draft/preview only** — publishing and signup collection are gated to paid tiers.
**Solution**: Upgrade to a paid tier (Chill Builder for one product, Serious Builder for multiple). Confirm current pricing at `preshiplist.co/pricing` — figures are launch pricing and not fixed. If you only wanted a free forever waitlist, a tool with a genuine free published tier (compare `/sales-getwaitlist` history or `/sales-launchlist` one-time pricing) may fit better.

### My signups aren't reaching my CRM / email tool
**Symptom**: Preshiplist shows signups but nothing appears in HubSpot/your ESP.
**Cause**: Preshiplist has **no API, no webhooks, and no Zapier** — nothing flows out automatically, and its own drip emails send from Preshiplist, not your ESP.
**Solution**: Export the signups as CSV from the dashboard and import into your CRM/ESP, or run a scheduled job over a periodically-exported CSV. Accept that it's batch, not real-time. If you need real-time sync, switch to a waitlist tool with a documented API/webhooks (`/sales-getwaitlist`, `/sales-waitlister`, `/sales-waitlistly`).

### My launch-day / confirmation email isn't going out (or lands late)
**Symptom**: New signups don't get the confirmation, or the launch-day email doesn't fire.
**Cause**: The drip sequence isn't configured/enabled, or the confirmation step was removed/rescheduled; deliverability can also vary on a young sending platform.
**Solution**: In the email/drip settings, confirm the sequence exists and that the **confirmation email fires immediately** on signup (a late first email kills share intent). Add/reorder the launch-day step, send yourself a test signup, and check the deliverability indicator. If deliverability is critical and shaky, weigh sending the launch broadcast from a dedicated ESP after exporting the list (`/sales-email-marketing`).
