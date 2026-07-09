---
name: sales-upviral
description: "UpViral platform help — viral referral marketing and list-building platform (by Emarky) for viral sweepstakes, giveaway/reward campaigns, pre-launch waiting lists, and milestone referrals, with REST API (`app.upviral.com/api/v1/`, form-encoded `uvapikey` + `uvmethod`), Callback-URL webhooks, IP-based fraud detection, and 30+ ESP/CRM integrations. Use when campaigns aren't tracking referral points, deciding between Starter $79/mo (10K leads, NO API) vs Business $119/mo (API + webhooks) vs Premium $319/mo, the API erroring because you're on Starter where API/webhooks are gated, building a pipeline with `add_contact`/`get_leads`/`get_leads_points`, interpreting same-IP suspicious-referral flags, or picking UpViral over Viral Loops/Vyper/Gleam. Do NOT use for newsletter audience growth (use /sales-audience-growth), KickoffLabs help (use /sales-kickofflabs), merge-tag referrals (use /sales-referralkit), SparkLoop recommendations (use /sales-sparkloop), or multi-level Level 1/2/3 tracking (use /sales-referralhero)."
argument-hint: "[describe what you need help with in UpViral]"
license: MIT
version: 1.0.0
tags: [sales, referral-program, viral-marketing, waitlist, giveaway, platform]
---

# UpViral Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Pick a tier — Starter $79/mo (10K leads, no API) vs Business $119/mo (25K, API+webhooks) vs Premium $319/mo (100K, dedicated AM)
   - B) Launch a viral sweepstakes (point competition with a grand prize)
   - C) Run a giveaway / viral rewards campaign for lead gen
   - D) Build a pre-launch viral waiting list (Dropbox-style queue jumping)
   - E) Set up an evergreen milestone referral program
   - F) Connect API or webhooks — `add_contact` / `get_leads` / `add_points` / Callback URL
   - G) Interpret fraud flags (same-IP suspicious referrals) and decide activate/delete/blacklist
   - H) Integrate with Mailchimp / ActiveCampaign / ConvertKit / Klaviyo / HubSpot / Zapier
   - I) Compare UpViral to Viral Loops / KickoffLabs / Vyper / Prefinery / Gleam

2. **What's your campaign type?** Sweepstakes / giveaway-rewards / waiting-list / milestone — drives which points, reward, and verification settings matter.

3. **What's your ESP and site stack?** Drives whether a native ESP integration is enough or you need API/webhooks/Zapier glue — and whether you're forced onto the Business tier to unlock the API.

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| General newsletter/audience growth strategy across all platforms | `/sales-audience-growth [question]` |
| Newsletter monetization (paid subs, sponsorships, ad networks) | `/sales-newsletter [question]` |
| KickoffLabs viral campaigns specifically | `/sales-kickofflabs [question]` |
| No-code newsletter-only referrals with merge-tag insertion | `/sales-referralkit [question]` |
| SparkLoop paid recommendations + partner network | `/sales-sparkloop [question]` |
| Full-stack referral/affiliate with multi-level Level 1/2/3 + coupon groups | `/sales-referralhero [question]` |
| Affiliate program strategy across many tools | `/sales-affiliate-program [question]` |
| ESP setup (Mailchimp, ActiveCampaign, Klaviyo, HubSpot) | `/sales-mailchimp`, `/sales-activecampaign`, `/sales-klaviyo`, `/sales-hubspot` |

If the question is UpViral-specific, continue to Step 3.

## Step 3 — UpViral platform reference

**Read `references/platform-guide.md`** for the full reference — tier gating (especially the API/webhooks Business+ gate), campaign type selection (sweepstakes / rewards / waiting-list / milestone / custom), presentation formats, fraud detection model, ESP/CRM integrations, the ClickFunnels/Shopify integration caveats, and comparisons with Viral Loops / KickoffLabs / Vyper / Prefinery / Gleam.

**Read `references/upviral-api-reference.md`** for the REST API documentation — base `https://app.upviral.com/api/v1/`, `uvapikey` + `uvmethod` form-encoded POST authentication, the eight methods (`add_contact`, `get_lead_details`, `get_lead_details_by_email`, `get_leads`, `get_leads_points`, `add_points`, `get_custom_fields`, `lists`), pagination (`start`/`size`), the Callback URL webhook payload, the PHP SDK, and the Business+ API gate.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **API and webhooks are gated to Business ($119/mo annual) and above.** Starter ($79/mo) has NO API/webhooks. If your project is a CRM sync, a data-warehouse pipeline, or any server-side automation, you must budget Business minimum — this is the single most common surprise. Verify before promising an integration.
- **Auth is two form-encoded params, not a header.** Every request POSTs `uvapikey` (your key) + `uvmethod` (the method name) + `campaign_id` (for most methods) as form-encoded fields to `https://app.upviral.com/api/v1/`. There is no Bearer header. Responses are JSON.
- **Use `get_leads_points` for reward fulfillment.** To find everyone who crossed a points threshold (e.g. unlocked a reward), call `get_leads_points` with an operator (`<`, `>`, `=`) and a points value rather than pulling all leads and filtering client-side.
- **Webhook = "Callback URL".** UpViral calls webhooks "Callback URL." Set it per campaign; it fires on events such as a lead unlocking a reward. Pair it with `get_lead_details` to enrich the payload, since the callback is lean.
- **Fraud detection is IP-based and semi-manual.** UpViral flags a referral as "suspicious" when the referred signup comes from the **same IP** as the referrer. Flagged leads land in the Fraud Detection section for you to **activate, delete, or blacklist**. It is not fully automatic — budget review time for high-volume campaigns.
- **Set aside real time for the first campaign.** Reviewers consistently describe setup as "long and complicated" — expect several hours for your first campaign. The drag-and-drop builder has known broken-widget and customization complaints; keep the design simple to avoid them.
- **It's a B2C viral tool.** UpViral is built for consumer viral sharing (Facebook/WhatsApp/X). It's a poor fit for B2B audiences who won't share for points — don't recommend it for B2B lead gen.
- **No native WordPress plugin; ClickFunnels/Shopify integrations are flaky.** Use the embedded-form or pop-up presentation formats, or post via Zapier/API, rather than relying on a deep funnel-builder integration.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features and pricing that may shift.*

1. **API/webhooks require Business tier ($119/mo annual) or higher.** Starter ($79/mo) cannot call the API or receive callbacks. If a Starter user reports "API not working," the fix is usually an upgrade, not a code change.
2. **Auth params, not headers.** `uvapikey` and `uvmethod` are form-encoded POST fields. Developers used to `Authorization: Bearer` headers will get auth failures — UpViral does not use a header scheme.
3. **Fraud detection is IP-matching + manual triage.** Same-IP referral → "suspicious." You must manually activate/delete/blacklist. Legitimate users behind shared NAT/office IPs can be false-flagged — review before mass-deleting.
4. **Long setup / learning curve.** First campaign commonly takes several hours. Budget for it; don't promise a same-hour launch.
5. **Drag-and-drop builder is fragile.** Reviewers report broken widgets and limited customization. For pixel-perfect pages, build the landing page elsewhere (Unbounce/Leadpages/Framer) and use UpViral's embedded form or pop-up.
6. **No native WordPress plugin.** Despite "WordPress" appearing in integration lists, there's no first-party plugin — embed the form/script manually.
7. **ClickFunnels / Shopify / funnel-builder integrations break.** Multiple reviews flag these. Prefer Zapier or the API over deep native funnel integrations.
8. **$1/14-day trial is short.** Two weeks rarely shows a viral campaign's true performance. Plan to commit to at least one paid month to evaluate properly.
9. **B2C-only fit.** Point-for-share mechanics don't translate to B2B buyers. Wrong tool for enterprise/B2B lead gen.
10. **AI Credits are metered and scarce.** Starter gets 1/mo, Business 3/mo, Premium 10/mo — the AI copy/asset features are not unlimited.
11. **No MCP server.** Programmatic access is the REST API + Callback URL webhook + iPaaS (Zapier/Make/Pipedream/Integrately/Pabbly) only.
12. **Brand limits per tier.** Starter = 1 brand, Business = 2, Premium = 5. Agencies running many clients hit this fast — Premium or multiple accounts.

## Related skills

- `/sales-audience-growth` — Newsletter/audience growth strategy (referrals + cross-promotion + lead magnets across all platforms)
- `/sales-newsletter` — Newsletter monetization (paid subs, sponsorships, ad networks)
- `/sales-kickofflabs` — KickoffLabs (viral waitlists / giveaways / milestone rewards with REST API v1+v2, AnyForm, KOL.js)
- `/sales-referralkit` — ReferralKit (no-code merge-tag-driven newsletter referrals, free up to 10K leads)
- `/sales-sparkloop` — SparkLoop (newsletter referrals + paid recommendations + partner network)
- `/sales-referralhero` — ReferralHero (full-stack referral/affiliate/waitlist/contest with multi-level Level 1/2/3 + coupon groups + REST API)
- `/sales-affiliate-program` — General affiliate program strategy and platform selection
- `/sales-mailchimp` — Mailchimp platform help (native ESP integration)
- `/sales-activecampaign` — ActiveCampaign platform help (native ESP integration)
- `/sales-klaviyo` — Klaviyo platform help (native ESP integration)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Tier picking when an integration is required
**User says**: "I want to run a viral giveaway and sync new leads straight into HubSpot automatically. Is the $79 Starter plan enough?"
**Skill does**: Explains that Starter has NO API or webhooks — automated CRM sync requires the Business tier ($119/mo annual, 25K leads, 2 brands) which unlocks API + webhooks. Notes the cheaper path if budget is tight: a native HubSpot integration (UI-configured) or Zapier "New Lead" trigger may cover a simple sync, but webhooks/REST still need Business. Recommends Business and warns that the first campaign setup takes a few hours.
**Result**: User upgrades to Business, wires the New Lead → HubSpot Zap (or REST `get_leads` poll), and budgets setup time.

### Example 2: Reward-fulfillment pull via the API
**User says**: "I'm on Business. How do I get a list of everyone in my campaign who has 100+ points so I can ship their reward?"
**Skill does**: Provides a form-encoded POST to `https://app.upviral.com/api/v1/` with `uvapikey`, `uvmethod=get_leads_points`, `campaign_id`, operator `>`, points `99` (or `>=` semantics via `=`/`>`), plus `start`/`size` pagination. Shows parsing the JSON to extract emails, and suggests pairing with `get_lead_details` for shipping fields. Notes there's no MCP server, so this REST poll (or the Callback URL on reward-unlock) is the integration path.
**Result**: User scripts a paginated `get_leads_points` pull and exports reward-eligible contacts.

### Example 3: Fraud flags from same-IP referrals
**User says**: "A bunch of my referrals got marked suspicious. Why, and what should I do?"
**Skill does**: Explains UpViral flags a referral as suspicious when the referred signup's IP matches the referrer's IP (gaming the point system). Flagged leads sit in the Fraud Detection section with three actions: activate (legit — count them), delete, or blacklist. Warns about false positives from shared office/household NAT IPs and recommends reviewing rather than bulk-deleting. Suggests adding email verification and limiting points-per-IP for prevention.
**Result**: User reviews flagged leads, activates the legitimate shared-IP ones, blacklists obvious abusers, and tightens prevention settings.

## Troubleshooting

### API calls return errors / "unauthorized" even with a valid key
**Symptom**: Every API request fails despite a correct API key copied from the dashboard
**Cause**: Either the account is on the **Starter tier** (no API access — API/webhooks are Business+), or the request is sending the key as an `Authorization` header instead of the `uvapikey` form field, or `uvmethod`/`campaign_id` is missing
**Solution**: Confirm the plan is Business or Premium. Send a form-encoded POST to `https://app.upviral.com/api/v1/` with `uvapikey`, `uvmethod` (the method name), and `campaign_id`. Do not use a Bearer header. Check the JSON response for the specific error message.

### Callback URL (webhook) isn't firing
**Symptom**: The configured Callback URL never receives events
**Cause**: Webhooks are gated to Business+; or the callback is set on the wrong campaign; or the triggering event (e.g. reward unlock) hasn't occurred yet
**Solution**: Verify the plan tier. Set the Callback URL on the specific campaign under its settings. Test by triggering the event (have a test lead cross the reward threshold). If still nothing, fall back to a Zapier "New Lead" / "New Reward Unlocked" trigger, which is configured separately from the native callback.

### Leads aren't syncing to ClickFunnels / Shopify / my funnel builder
**Symptom**: The native funnel-builder integration drops leads or doesn't connect
**Cause**: Known flakiness — UpReviews repeatedly flag ClickFunnels, Shopify, and funnel-builder integrations as unreliable; there's also no native WordPress plugin
**Solution**: Route leads through Zapier (New Lead trigger → your destination) or the REST API instead of the deep native integration. For WordPress, embed the UpViral form/script manually rather than expecting a plugin.

### The campaign took hours to set up and widgets look broken
**Symptom**: First campaign is slow to build; drag-and-drop elements render incorrectly
**Cause**: Documented learning curve and builder fragility (broken widgets, limited customization)
**Solution**: Keep the design minimal inside UpViral. For polished landing pages, build externally (Unbounce/Leadpages/Framer) and use UpViral's embedded form or pop-up presentation format. Allocate a few hours for the first build and reuse it as a template afterward.
