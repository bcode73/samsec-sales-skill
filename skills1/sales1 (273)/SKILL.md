---
name: sales-keap
description: "Keap platform help — small-business CRM + marketing automation (formerly Infusionsoft): Campaign Builder / When-Then automations, email + SMS marketing, sales pipeline, invoicing/payments, appointments, and a REST v2 API (OAuth 2.0, Personal Access Tokens, REST Hooks webhooks). Use when Keap automations or campaigns aren't triggering reliably, the Campaign Builder feels too complex to set up, per-contact pricing keeps climbing, Keap blocked or throttled your account over spam complaints, you're deciding between Max Classic and the new Keap/Ultimate interface, building a Keap API or webhook integration, syncing Keap contacts to another CRM or data warehouse, or pulling campaign/tag/order data through the API. Do NOT use for comparing Keap against other CRMs (use /sales-crm-selection) or multi-step funnel strategy across tools (use /sales-funnel)."
argument-hint: "[describe what you need help with in Keap]"
license: MIT
version: 1.0.0
tags: [sales, crm, platform]
github: "https://github.com/infusionsoft"
---

# Keap Platform Help

Keap (formerly Infusionsoft) is an all-in-one small-business CRM + marketing automation platform — contacts, the drag-and-drop Campaign Builder, email/SMS, sales pipeline, invoicing, and a REST v2 API.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out which of these the user needs (ask only if their prompt doesn't already say):

1. **What kind of problem is this?**
   - A) Automation/Campaign Builder behavior (triggers, sequences, tags not firing)
   - B) Deliverability / account got blocked or throttled
   - C) Pricing, plan, or which interface (Max Classic vs new Keap/Ultimate)
   - D) API / webhook / integration build
   - E) Choosing whether Keap is the right CRM at all

2. **Which interface are they on?** Max Classic (legacy Infusionsoft) vs the newer Keap (Pro/Max/Ultimate). Features and API behavior differ.

**Skip-ahead rule:** if the user's prompt already has enough context, skip to Step 2 or Step 3.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Comparing Keap vs HubSpot/GoHighLevel/Attio or picking a CRM | `/sales-crm-selection {user's question}` |
| Multi-step funnel / landing-page strategy across tools | `/sales-funnel {user's question}` |
| Email-marketing strategy (segmentation, deliverability) across platforms | `/sales-email-marketing {user's question}` |
| SMS-marketing strategy / compliance (TCPA, opt-in) | `/sales-sms-marketing {user's question}` |
| General inbox-placement / sender-reputation strategy | `/sales-deliverability {user's question}` |
| Connecting Keap to other tools (Zapier/Make/native) | `/sales-integration {user's question}` |

When routing, give the exact command, e.g. "This is a CRM-comparison question — run: `/sales-crm-selection should I move from Keap to HubSpot`".

## Step 3 — Keap platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model (JSON shapes), integration recipes (cURL + Python), and integration patterns. For raw API detail (endpoints, OAuth, REST Hooks), read `references/keap-api-reference.md`.

Answer using only the relevant section. Don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide — focus on the user's situation.

- **Automation not firing?** Check the goal type first — Keap automations stall most often on a goal that never gets *met* (tag not applied, form not submitted), not on the sequence itself. Confirm the contact actually entered the campaign.
- **Account blocked over complaints?** Keap enforces a low complaint threshold and counts some unsubscribe reasons as complaints. Suppress cold/unengaged contacts and re-permission before sending broadcasts.
- **API build?** Prefer REST v2 + OAuth 2.0; use a Personal Access Token for a single-account internal script. Webhook payloads are thin (ID + change type) — always follow up with a GET.
- **Cost creeping?** Pricing scales with contact count — archive/delete dead contacts and keep marketing-only contacts out of the CRM count where possible.

If you discover a gotcha or workaround not in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing which change frequently.*

1. **Two products wear the "Keap" name.** Max Classic is the legacy Infusionsoft engine; the newer Keap (Pro/Max/Ultimate) is a rebuilt UI. Campaign Builder, reporting, and some API fields behave differently between them. Always confirm which one the user is on before giving steps.
2. **Aggressive deliverability enforcement.** Keap can throttle or block an account after a very small number of spam complaints (reports of blocks at ~13 complaints across 70k+ sends), and it counts unsubscribe-with-feedback ("too frequent") as a complaint. Warm up and suppress aggressively.
3. **Automations hinge on goals, not steps.** A "When-Then" automation or campaign sequence only runs once its goal is *met*. The #1 "it's not triggering" cause is a goal condition that's never satisfied — not a broken sequence.
4. **Per-contact pricing.** The bill rises with contact volume, so unmanaged list growth silently raises cost. This is the most common pricing complaint.
5. **Webhook payloads are minimal.** REST Hooks send `object_keys` (ID + apiUrl + timestamp), not the full record. You must call the `apiUrl` to get data.
6. **Rate limits differ by auth type.** OAuth apps get a far higher ceiling than Personal Access Tokens; a 25 req/sec spike cap applies on top. Batch and back off on `429`.

## Related skills

- `/sales-crm-selection` — CRM comparison & selection — is Keap right vs HubSpot, GoHighLevel, Attio, Pipedrive?
- `/sales-gohighlevel` — GoHighLevel platform help — the agency-first all-in-one most often compared to Keap
- `/sales-hubspot` — HubSpot platform help — the inbound marketing+sales alternative Keap positions against
- `/sales-funnel` — Multi-step funnel strategy across tools (Keap has no native funnel builder)
- `/sales-email-marketing` — Email-marketing strategy across platforms
- `/sales-sms-marketing` — SMS-marketing strategy and compliance
- `/sales-deliverability` — Inbox placement and sender-reputation strategy
- `/sales-integration` — Connecting Keap to other tools — webhooks, Zapier, Make, custom API
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Automation isn't firing
**User says**: "I built a Keap campaign to email new leads but nobody's getting the email."
**Skill does**: Asks whether the contact actually met the campaign's *goal* (form submit, tag applied), checks the sequence is published and the goal is connected, and whether they're on Max Classic or new Keap (Campaign Builder differs). Walks through verifying the contact entered the sequence and the email step isn't paused.
**Result**: User finds the goal was never met (tag misspelled), fixes it, emails send.

### Example 2: Sync Keap contacts to a warehouse via the API (automation)
**User says**: "How do I pull all my Keap contacts and tags into BigQuery on a schedule?"
**Skill does**: Points to REST v2 `GET /crm/rest/v2/contacts` with `pageToken` cursor pagination and OAuth 2.0 (or a Personal Access Token for a single account), shows the contacts JSON shape, notes the 1,500/min OAuth rate limit and 25 req/sec spike cap, and recommends REST Hooks (`contact.add/edit`) for incremental sync instead of full re-pulls. References the Python recipe in the platform guide.
**Result**: User has a paginated export plus an incremental webhook strategy.

### Example 3: Account blocked over complaints
**User says**: "Keap suspended my sending after one broadcast — I barely got any complaints."
**Skill does**: Explains Keap's low complaint threshold and that unsubscribe-with-feedback counts as a complaint, recommends suppressing unengaged/cold contacts, re-permissioning the list, and sending warmer segments first. Routes deeper sender-reputation work to `/sales-deliverability`.
**Result**: User cleans the list and resumes sending without re-tripping enforcement.

## Troubleshooting

### "My campaign/automation isn't triggering"
**Symptom**: Contacts sit in a campaign and never get the email/sequence.
**Cause**: The goal condition was never met, the sequence isn't published, or the contact never entered. Bugs after the Ultimate UI rollout have also hidden/mislabeled action options.
**Solution**: Confirm the goal fires (test with a known contact), republish the sequence, verify entry. If actions look wrong/missing in the Ultimate builder, toggle back to Max Classic as a workaround and check Keap's Known Issues page.

### "I can't pull campaign sequences through the API"
**Symptom**: Campaign sequence steps aren't returned or aren't editable via REST.
**Cause**: Campaign/sequence read support is limited and differs between v1, v2, and Max Classic; some campaign internals are UI-only.
**Solution**: Use the Campaign endpoints that *are* exposed to list campaigns and add/remove contacts to sequences; manage sequence *content* in the UI. Confirm you're calling the version that matches the account, and check the Keap Integration Q&A community for the current campaign-endpoint coverage.

### "My Keap bill keeps going up"
**Symptom**: Monthly cost rose without adding users.
**Cause**: Pricing scales with contact count; imported/duplicate/cold contacts inflate it.
**Solution**: Audit and archive/delete dead contacts, dedupe, and avoid storing marketing-only or list-rented contacts you won't sell to. Re-check the per-contact tier after cleanup.
