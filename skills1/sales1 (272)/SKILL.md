---
name: sales-kartra
description: "Kartra platform help — all-in-one for coaches, consultants, and course creators (kartra.com): funnels/pages, email + SMS automation, checkout with order bumps and upsells, memberships/courses, video, webinars, affiliate management, helpdesk, and calendars. Covers the inbound API (POST app.kartra.com/api with app_id/api_key/api_password and an actions[] array, 20 calls/sec) and outbound IPN webhooks. Use when building a Kartra API integration to sync leads or tags into a CRM, your API key only works after upgrading to the Professional plan, you hit the 20-calls-per-second 429 limit, IPN webhooks aren't firing on purchase or tag events, custom-domain redirects slow page load, your account is throttled for crossing the 0.03% spam-complaint threshold, the calendar drops appointments, or choosing a plan (Essentials vs Starter vs Growth vs Professional). Do NOT use for funnel strategy across tools or comparing Kartra against other all-in-one platforms (use /sales-funnel)."
argument-hint: "[describe what you need help with in Kartra]"
license: MIT
version: 1.0.0
tags: [sales, funnel, all-in-one, platform]
github: "https://github.com/GenesisDigital"
---

# Kartra Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build an inbound API integration — sync leads, tags, lists, sequences, transactions, or subscriptions in/out of Kartra
   - B) Set up outbound IPN webhooks — react to purchase, tag, lead, sequence, or membership events
   - C) Configure a module inside Kartra — funnels/pages, email/SMS automations, checkout, memberships, webinars, affiliates, helpdesk, calendars
   - D) Pick a plan — Essentials vs Starter vs Growth vs Professional (note: API + advanced automations are plan-gated)
   - E) Fix a problem — deliverability/spam-complaint throttling, slow custom-domain pages, calendar reliability, rate limits
   - F) Something else — describe it

2. **Where does data need to flow?** Stay inside Kartra / sync to a CRM or warehouse / drive an external app — this decides API vs webhook vs Zapier.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Multi-step funnel strategy/structure across tools | `/sales-funnel {question}` |
| Email-marketing strategy, sequences, deliverability | `/sales-email-marketing {question}` |
| Inbox-placement / spam-complaint deliverability | `/sales-deliverability {question}` |
| Checkout/order-bump/upsell conversion optimization | `/sales-checkout {question}` |
| Membership-site / course structure and retention | `/sales-membership {question}` |
| Webinar funnel strategy (live + evergreen) | `/sales-webinar {question}` |
| Comparing Kartra vs other all-in-one platforms | `/sales-funnel {question}` |

When routing, give the exact command, e.g. "This is a funnel-strategy question — run: `/sales-funnel {your question}`".

## Step 3 — Kartra platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API-accessible vs webhook-accessible vs UI-only), pricing and plan gates, the lead/tag/transaction data model with JSON shapes, and quick-start recipes (create a lead + assign a tag via the API; listen for a purchase IPN webhook; bulk-export transactions).

**Read `references/kartra-api-reference.md`** for the inbound API — base `https://app.kartra.com/api`, the `app_id`/`api_key`/`api_password` auth, the `actions[]` array and every `cmd` (leads, custom fields, lists, tags, sequences, pages, transactions, subscriptions, calendars, points), the 20-calls/sec rate limit, and the outbound IPN webhook events.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Confirm the plan gate first.** On current Kartra plans, API access and advanced automations appear gated to higher tiers (Professional for API). If their key 401s or the menu is missing, it's usually a plan issue, not a code bug — verify the plan before debugging the integration.
- **The API is form-POST, not REST-per-resource.** Everything goes to one endpoint (`POST https://app.kartra.com/api`) with `app_id`, `api_key`, `api_password`, and an `actions[]` array. To create-then-act on a lead in one call, the first action's `cmd` must be `create_lead`.
- **Throttle to 20 calls/sec/app.** Batch multiple `actions` into one request where possible and back off on `429`.
- **Use IPN webhooks instead of polling** for purchase/tag/membership events — it's lower-latency and avoids burning rate limit. Respond `2xx` fast and process async.
- **Deliverability is enforced platform-wide.** Kartra holds a ~0.03% spam-complaint standard across the whole platform; a cold or unengaged list can get your sending throttled. Warm up and clean lists before bulk sends.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing, which change frequently.*

1. **API access is plan-gated.** On the current tiered plans, the API (and advanced automations / custom-code pages) appears restricted to the **Professional** tier — building an integration on Essentials/Starter can fail before any code runs. Verify against the live account.
2. **One endpoint, `actions[]` array.** It's not REST — don't expect `/leads/{id}`. Send POST form data to `https://app.kartra.com/api` with the action commands in an array. First `cmd` must be `create_lead` when creating.
3. **Rate limit: 20 calls/sec per App → `429`.** Bulk syncs need throttling, batching multiple actions per call, and backoff.
4. **0.03% spam-complaint standard is platform-wide.** Sending to cold/purchased lists can throttle or suspend your account — this is account-protection, separate from inbox placement.
5. **Custom domains add a redirect.** Kartra routes custom-domain pages through a redirect that can slow load time; compress assets and expect the hop.
6. **Calendar reliability is a known pain point** — users report missed/dropped appointments. For mission-critical booking, validate against a dedicated scheduler.
7. **HTTPS is mandatory** — the API rejects `http://`. Always call over SSL.

## Related skills

- `/sales-funnel` — Funnel strategy across tools (Kartra is one of the all-in-one funnel builders covered) and Kartra-vs-alternatives comparisons
- `/sales-email-marketing` — Email/SMS sequence strategy and deliverability
- `/sales-deliverability` — Inbox placement and spam-complaint-rate management (relevant to Kartra's 0.03% standard)
- `/sales-checkout` — Checkout, order-bump, and upsell conversion optimization
- `/sales-membership` — Membership-site and course structure, pricing, and retention
- `/sales-webinar` — Live and evergreen webinar funnel strategy
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Sync new app signups into Kartra and tag them (developer/automation)
**User says**: "When someone signs up in my app, I want to create the lead in Kartra and tag them 'app-trial'. What's the cleanest API call?"
**Skill does**: Confirms the account is on a plan with API access, then shows the single form-POST to `https://app.kartra.com/api` with `app_id`/`api_key`/`api_password` and an `actions[]` array whose first `cmd` is `create_lead` (carrying `lead[email]`, `lead[first_name]`) followed by an `assign_tag` action (Recipe 1 in `references/platform-guide.md`). Notes the 20-calls/sec limit and to upsert by email to avoid duplicate leads.
**Result**: One API call creates-and-tags the lead; the user understands the actions-array model.

### Example 2: React to a purchase without polling (developer)
**User says**: "I want my fulfillment system to fire the moment someone buys in Kartra, not on a cron. How?"
**Skill does**: Points to the **outbound IPN webhook** — configured under My Integrations » API — that fires on the purchase event with the lead + transaction payload. Explains responding `2xx` fast and processing async, and deduping on the transaction ID since deliveries can repeat (Recipe 2). Contrasts with polling `search transactions`, which burns the 20/sec limit.
**Result**: User sets up an event-driven webhook instead of a polling loop.

### Example 3: My emails keep getting throttled
**User says**: "Kartra warned me my spam complaints are too high and slowed my sending. What now?"
**Skill does**: Explains the platform-wide ~0.03% spam-complaint standard (account protection, not just inbox placement), then routes the strategy: "This is a deliverability problem — run: `/sales-deliverability my Kartra account is throttled for spam complaints`." Adds Kartra-specific first steps: suppress unengaged segments, slow the send cadence, and re-permission cold imports before bulk blasts.
**Result**: User gets both the platform context and the right strategy skill.

## Troubleshooting

### API key returns 401 / "API access" menu is missing
**Symptom**: A valid-looking key fails to authenticate, or there's no API section in Settings.
**Cause**: API access is plan-gated — current plans appear to restrict it to the Professional tier — or you're missing one of the three required params (`app_id`, `api_key`, `api_password`), or you're calling over `http://`.
**Solution**: Verify the account's plan includes API access; confirm all three auth params are sent in the POST body; ensure the call uses `https://`. The App ID must match the app registered under Settings » Integrations » My API.

### Hitting 429 "Too many requests"
**Symptom**: Bulk syncs start failing with 429s.
**Cause**: The inbound API caps at 20 calls/second per App.
**Solution**: Throttle below 20/sec, batch multiple `actions` into a single request, and add exponential backoff on 429. For large migrations, queue and pace the writes rather than firing them in a tight loop.

### IPN webhooks aren't firing (or arrive twice)
**Symptom**: Your endpoint never receives purchase/tag events, or processes the same event repeatedly.
**Cause**: The outbound IPN isn't enabled/pointed at your URL, the event type isn't selected, or your handler isn't idempotent.
**Solution**: Enable the outbound API under My Integrations » API, select the events you need (purchase, tag applied, lead created, sequence complete, membership granted, etc.), and confirm the target URL is reachable over HTTPS. Respond `2xx` quickly and dedupe on the transaction/lead identifier so retries don't double-process.
