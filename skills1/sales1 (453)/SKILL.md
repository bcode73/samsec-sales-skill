---
name: sales-rafflepress
description: "RafflePress (rafflepress.com) platform help — WordPress giveaway & contest plugin for viral list growth: drag-and-drop builder, 30+ bonus-entry actions (email signup, social follows, refer-a-friend, shares), hosted giveaway landing pages, fraud protection, and 15+ native ESP/CRM integrations. Self-hosted WordPress only — no REST API; the developer surface is outbound webhooks (JSON/FORM, fields fullname/email/giveaway_id/sign_up_date, no HMAC), a Zapier 'New Contestant Created' trigger (API key from the Join-an-Email-Newsletter action), Uncanny Automator, and WordPress hooks + URL-parameter prefill. Use when wiring entrants to an endpoint via webhooks, syncing contestants to an ESP/CRM or Zapier, attributing refer-a-friend entries, handling giveaway fraud, picking entry actions, or choosing the Lite vs Pro license. Do NOT use for giveaway/audience-growth strategy across tools (use /sales-audience-growth), generic iPaaS wiring (use /sales-integration), or email deliverability (use /sales-deliverability)."
argument-hint: "[describe what you need help with in RafflePress]"
license: MIT
version: 1.0.0
tags: [sales, audience-growth, giveaway, platform]
---

# RafflePress Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Send entrants out to your own endpoint (outbound webhook) as they sign up
   - B) Sync contestants to an ESP/CRM (native integration) or to Zapier (500+ apps)
   - C) Set up entry actions / refer-a-friend viral mechanics and a giveaway landing page
   - D) Pre-fill the entry form or gate access via WordPress hooks / URL parameters
   - E) Handle giveaway fraud / fake entries, or pick a winner fairly
   - F) Decide Lite (free) vs Pro license, or which entry actions to enable

2. **Code or no-code?** Hosting your own endpoint → outbound webhooks. No endpoint → native ESP integration, Zapier, or Uncanny Automator.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Giveaway / audience-growth **strategy** across tools (which tool, viral mechanics) | `/sales-audience-growth {question}` |
| Connecting RafflePress to a CRM/ESP generically (iPaaS) | `/sales-integration {question}` |
| Email sequences for the list you collect | `/sales-email-marketing {question}` |
| Deliverability of giveaway/notification emails | `/sales-deliverability {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-audience-growth maximize referrals on a viral giveaway`".

## Step 3 — RafflePress platform reference

**Read `references/platform-guide.md`** for the full reference — the giveaway/entry-action model (what's webhook vs native-integration vs UI-only), the one-time/lifetime pricing and Lite-vs-Pro gates, the entrant data model with JSON shapes, and quick-start recipes (receive a webhook; sync to an ESP; prefill the form via URL params).

**Read `references/rafflepress-api-reference.md`** for the integration surface — RafflePress is **WordPress-only (no REST API)**: outbound webhooks (Settings → Webhooks; JSON/FORM; fields `fullname`/`first_name`/`last_name`/`email`/`giveaway_id`/`giveaway_name`/`sign_up_date`; **no HMAC**), the Zapier **New Contestant Created** trigger (API key from the Join-an-Email-Newsletter action), the 15+ native ESPs, Uncanny Automator, and WordPress hooks + URL-parameter prefill.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Webhooks only carry the email-signup identity.** The payload has name/email/giveaway fields, but **third-party social-action data (Facebook/X/YouTube/Instagram/Pinterest) is NOT sent.** Don't expect per-action analytics from the webhook — use it to capture the contestant + which giveaway.
- **No HMAC on webhooks.** Secure the Request URL as a secret and/or add a custom auth header (RafflePress lets you add headers per webhook); dedupe on `email` + `giveaway_id` since a signup can re-fire.
- **Zapier needs the per-action API key.** The key lives on the giveaway's **Join an Email Newsletter** action (pick Zapier from its dropdown). The only trigger is **New Contestant Created**, and you can have **one** Join-an-Email-Newsletter action per giveaway when using Zapier.
- **Prefer a native ESP integration when you can.** RafflePress syncs directly to 15+ ESPs (Mailchimp, Kit, ActiveCampaign, MailerLite, Brevo…) — simpler than a webhook if you just need the list.
- **It's WordPress-only.** No SaaS API/MCP — everything runs on your WordPress site. To pre-identify a user or carry UTM/identity from a landing page, use **URL-parameter prefill**; to gate who can manage giveaways, use the access-permission filter.
- **Plan for fraud.** Viral giveaways attract fake/disposable entries and self-referral abuse. Built-in fraud protection helps, but validate emails before fulfilling and review the leaderboard before awarding refer-a-friend prizes.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — pricing/feature specifics verified against the marketing site, docs, and reviews; confirm in-account.*

1. **Webhook omits social-action data.** Only `fullname`/`first_name`/`last_name`/`email`/`giveaway_id`/`giveaway_name`/`sign_up_date` are sent; data from Facebook/X/YouTube/Instagram/Pinterest actions is explicitly **not** shared.
2. **No documented webhook HMAC.** Treat the Request URL as a secret, add a custom auth header, and make handlers idempotent (key on `email` + `giveaway_id`).
3. **One newsletter action per giveaway with Zapier.** You can't wire multiple Join-an-Email-Newsletter actions to Zapier on the same giveaway — plan a single sync action.
4. **WordPress-only.** No hosted REST API, no MCP — automation is webhooks/Zapier/native integrations/Automator/PHP hooks. You need a self-hosted WordPress site.
5. **Pro is a paid license.** The free **Lite** plugin runs basic giveaways; webhooks, refer-a-friend, many entry actions and integrations are **Pro**. Pro is sold as a one-time/lifetime license (~$299 single site / ~$349 unlimited — best-effort).
6. **Giveaways attract fraud.** Fake/disposable emails and self-referrals are common — validate before rewarding; built-in fraud protection isn't a guarantee.
7. **Email is the identity.** Entrants are keyed by email across webhooks/Zapier/ESPs — design your dedupe and reward logic around it.

## Related skills

- `/sales-audience-growth` — Giveaway / audience-growth strategy across tools (RafflePress is one of the giveaway/contest platforms covered) — viral mechanics, tool selection
- `/sales-email-marketing` — Email sequences for the list you grow with a giveaway
- `/sales-integration` — Connecting RafflePress to a CRM/ESP via webhooks/Zapier/Automator
- `/sales-deliverability` — Inbox placement and list quality for the emails you collect
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Capture entrants to my own endpoint via webhook (developer/automation)
**User says**: "When someone enters my RafflePress giveaway, how do I POST their email to my own API?"
**Skill does**: Walks Recipe 1 — enable **Settings → Webhooks**, set the **Request URL**, pick **JSON**, and (since there's **no HMAC**) add a secret **custom header** for auth. Explains the payload carries `fullname`/`first_name`/`last_name`/`email`/`giveaway_id`/`giveaway_name`/`sign_up_date` but **not** social-action data, and to dedupe on `email`+`giveaway_id`. Offers the native ESP integration or Zapier **New Contestant Created** as no-code alternatives.
**Result**: Entrants stream to the user's endpoint securely and idempotently.

### Example 2: Sync giveaway entrants into an ESP
**User says**: "I want everyone who enters added to my Mailchimp list automatically."
**Skill does**: Recommends the **native Mailchimp integration** via the giveaway's **Join an Email Newsletter** action (simplest), or Zapier's **New Contestant Created** → Mailchimp if more routing is needed (noting the one-newsletter-action-per-giveaway Zapier limit and that the Zapier API key comes from that action). Flags double-opt-in and fraud filtering before nurture, and routes deliverability to `/sales-deliverability`.
**Result**: Entrants land on the right list, ready to nurture.

### Example 3: Refer-a-friend or affiliate — which, and how do entries count?
**User says**: "Does RafflePress do referrals, and should I use it instead of an affiliate program?"
**Skill does**: Explains RafflePress **refer-a-friend** is a *giveaway entry mechanic* (+10 entries per referral, share actions +2–5) to grow a list/virality — not a commission-based affiliate program. Recommends RafflePress for viral list growth and routes commission-based partner programs to `/sales-affiliate-program`. Notes entries are credited via the referral link and to watch for self-referral fraud.
**Result**: User picks the right mechanic and understands how referral entries are counted.

## Troubleshooting

### My webhook isn't receiving social-follow data
**Symptom**: The webhook fires on signup but never includes which social accounts the entrant followed.
**Cause**: By design — RafflePress does **not** share data from third-party social actions (Facebook/X/YouTube/Instagram/Pinterest) over the webhook; only the email-signup fields are sent.
**Solution**: Use the webhook for the contestant identity (`email`, `giveaway_id`, name, `sign_up_date`) and read social-action completion inside the RafflePress dashboard/reporting. If you need per-action automation, use Uncanny Automator on the WordPress side instead.

### My Zapier zap won't connect / no trigger data
**Symptom**: RafflePress won't authenticate in Zapier, or "New Contestant Created" returns nothing.
**Cause**: The API key wasn't taken from the **Join an Email Newsletter** action (it's per-action, not a global key), the website URL was wrong, or there's more than one newsletter action on the giveaway.
**Solution**: Add a **Join an Email Newsletter** action, choose **Zapier** in its dropdown, copy that API key, and connect with your **website URL + API key**. Keep to **one** newsletter action per giveaway. Use a sample contestant to test the trigger.

### My giveaway is full of fake entries
**Symptom**: A spike of disposable-email or duplicate entries.
**Cause**: Viral giveaways attract fraud — disposable emails, multi-entry, self-referral.
**Solution**: Rely on built-in fraud protection but add your own checks — validate/verify emails before counting, watch for refer-a-friend self-referrals, require double opt-in, and review entrants before awarding prizes. For list quality/deliverability afterward, use `/sales-deliverability`.
