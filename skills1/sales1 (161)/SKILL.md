---
name: sales-engagebay
description: "EngageBay platform help — affordable all-in-one CRM + marketing + sales + service suite for startups and SMBs (Marketing Bay, Sales & CRM Bay, Service Bay): email automation, landing pages, deals/pipelines, helpdesk tickets, and a REST API (raw API-key Authorization header, base app.engagebay.com, JSON only via Accept header, cursor pagination, outbound-only webhooks). Use when an EngageBay API call returns XML instead of JSON, you can't push data INTO EngageBay because it has no incoming webhooks, a deal created via the API doesn't show in the pipeline (track/milestone name case mismatch), you hit a 429 from the plan-gated monthly API quota, per-user/per-contact pricing keeps climbing, automation-node or contact limits are too low on your tier, or you're weighing EngageBay as a cheaper HubSpot/Keap/Ontraport alternative. Do NOT use for comparing CRMs across vendors (use /sales-crm-selection) or email-marketing strategy across tools (use /sales-email-marketing)."
argument-hint: "[describe what you need help with in EngageBay]"
license: MIT
version: 1.0.0
tags: [sales, crm, platform]
github: "https://github.com/engagebay"
---

# EngageBay Platform Help

EngageBay is an affordable all-in-one CRM + marketing + sales + service suite for startups and SMBs — Marketing Bay (email, automations, landing pages, forms), Sales & CRM Bay (contacts, deals, pipelines, tasks), and Service Bay (helpdesk tickets, live chat), on one shared contact database with a REST API and outbound webhooks.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Figure out which of these the user needs (ask only if their prompt doesn't already say):

1. **What kind of problem is this?**
   - A) API / webhook / integration build (auth, JSON vs XML, pagination, syncing data)
   - B) Automation, sequences, or landing pages not behaving
   - C) Pricing, plan, contact/automation-node limits, or which Bay to buy
   - D) Deliverability / email sending limits
   - E) Choosing whether EngageBay is the right tool at all

2. **Which module(s)?** Marketing Bay, Sales & CRM Bay, Service Bay, or the All-in-One Suite — features and limits differ by module and tier.

**Skip-ahead rule:** if the user's prompt already has enough context, skip to Step 2 or Step 3.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Comparing EngageBay vs HubSpot/Keap/Ontraport/Zoho or picking a CRM | `/sales-crm-selection {user's question}` |
| Email-marketing strategy (segmentation, deliverability) across platforms | `/sales-email-marketing {user's question}` |
| General inbox-placement / sender-reputation strategy | `/sales-deliverability {user's question}` |
| Multi-step funnel / landing-page strategy across tools | `/sales-funnel {user's question}` |
| Connecting EngageBay to other tools (Zapier/Make/native) | `/sales-integration {user's question}` |
| Contact enrichment for CRM records | `/sales-enrich {user's question}` |

When routing, give the exact command, e.g. "This is a CRM-comparison question — run: `/sales-crm-selection should I move from EngageBay to HubSpot`".

## Step 3 — EngageBay platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities & automation surface, pricing/plan gates, data model (JSON shapes), integration recipes (cURL + Python), and integration patterns. For raw API detail (endpoints, auth, webhooks, every resource), read `references/engagebay-api-reference.md`.

Answer using only the relevant section. Don't dump the whole reference.

## Step 4 — Actionable guidance

You no longer need the guide — focus on the user's situation.

- **Getting XML back?** Add `Accept: application/json` to every request. Auth is the raw REST API Key in the `Authorization` header (no `Bearer`); base URL `https://app.engagebay.com/`.
- **Can't write into EngageBay via webhook?** There are no incoming webhooks — push data in through the REST API. Webhooks are outbound only.
- **Deal created but not in the pipeline?** The `track_id`/`milestoneLabelName` is case-sensitive and must match the account exactly; a mismatch hides the deal from the milestone view.
- **Hitting 429?** The monthly API-call quota is plan-gated (~750k on Pro, far lower below). Cache reads, batch creates, and use webhooks for incremental sync instead of full re-pulls.
- **Cost creeping?** Plans are per-user *and* contact-capped — archive dead contacts, and consider buying just Marketing Bay or CRM Bay instead of the full suite.

If you discover a gotcha or workaround not in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially plan-gated features and pricing which change frequently.*

1. **API defaults to XML.** Without `Accept: application/json` every response is XML — the most common "my parser is broken" surprise. Auth is the raw key in `Authorization` (no `Bearer` prefix).
2. **No incoming webhooks.** EngageBay only *sends* webhooks; it cannot receive them. To update EngageBay from another app you must call the REST API.
3. **Outbound webhooks are unsigned.** There's no documented HMAC/signature header — secure your receiver with a secret URL path or IP allowlist, and treat the payload `id` as the source of truth (re-fetch for full data).
4. **Everything is case-sensitive.** Emails, names, tag names, and especially deal `milestoneLabelName`/track names. A wrong-case milestone silently creates the deal but hides it from the pipeline.
5. **Listing contacts is a POST**, not GET (`POST dev/api/panel/subscribers`), and the pagination `cursor` is inside the **last record** of each page (`page_size` max 100).
6. **Monthly API quota is plan-gated.** A high-volume integration can exhaust the free/Basic/Growth quota and return `429`; prefer incremental webhook-driven sync.

## Related skills

- `/sales-crm-selection` — CRM comparison & selection — is EngageBay right vs HubSpot, Keap, Ontraport, Zoho, Pipedrive?
- `/sales-keap` — Keap platform help — the small-business all-in-one CRM + marketing automation most often compared to EngageBay
- `/sales-ontraport` — Ontraport platform help — all-in-one CRM + marketing + payments alternative
- `/sales-hubspot` — HubSpot platform help — the inbound marketing+sales suite EngageBay positions against on price
- `/sales-email-marketing` — Email-marketing strategy across platforms
- `/sales-deliverability` — Inbox placement and sender-reputation strategy
- `/sales-funnel` — Multi-step funnel and landing-page strategy across tools
- `/sales-integration` — Connecting EngageBay to other tools — webhooks, Zapier, Make, custom API
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: API returns XML instead of JSON (automation)
**User says**: "I'm calling the EngageBay contacts endpoint and getting XML — my JSON parser keeps failing."
**Skill does**: Explains the API defaults to XML and you must send `Accept: application/json` on every request; confirms auth is the raw REST API Key in the `Authorization` header (no `Bearer`) and the base URL is `https://app.engagebay.com/`. Notes that listing contacts is a `POST dev/api/panel/subscribers` with `page_size`/`cursor` pagination. Points to the create/list recipes in the platform guide.
**Result**: User adds the Accept header, gets JSON, and parses successfully.

### Example 2: Sync deals out to a warehouse on close (automation)
**User says**: "When a deal closes in EngageBay I want to push it to BigQuery. What's the cleanest way?"
**Skill does**: Recommends an outbound webhook on "Deal updated" (Account Settings → Webhooks), shows the `deal.updated` payload shape, warns there's no HMAC so secure the endpoint via a secret path/IP allowlist, and to re-fetch by `id` for full fields. Adds that you can't write back into EngageBay via webhook — use the REST API — and to watch the plan-gated monthly API quota. References the Flask recipe in the platform guide.
**Result**: User has a webhook listener plus a strategy that respects the quota.

### Example 3: Is EngageBay the right CRM?
**User says**: "We're a 6-person startup priced out of HubSpot. Is EngageBay a real replacement?"
**Skill does**: Frames EngageBay as an affordable all-in-one (CRM + marketing + service) with a free tier and per-user/contact pricing, notes the trade-offs (XML-default API, no incoming webhooks, plan-gated quota, contact caps), and routes the head-to-head vendor comparison to `/sales-crm-selection` for a structured decision.
**Result**: User understands the fit and gets pointed to the comparison skill for the final call.

## Troubleshooting

### "The API gives me XML and I can't parse it"
**Symptom**: Every response is XML; JSON parsing fails.
**Cause**: EngageBay defaults responses to XML.
**Solution**: Send `Accept: application/json` on every request. Verify auth is the raw REST API Key in `Authorization` (no `Bearer`) and the host is `app.engagebay.com`. For lists, remember it's a `POST` and the `cursor` is in the last record.

### "I can't send data INTO EngageBay with a webhook"
**Symptom**: You set up an inbound webhook to create/update contacts and nothing happens.
**Cause**: EngageBay does not accept incoming webhooks — its webhooks are outbound only.
**Solution**: Write into EngageBay through the REST API (e.g. `POST dev/api/panel/subscribers/subscriber` to create a contact, or create-or-update by email). Reserve webhooks for pushing EngageBay events *out* to your systems.

### "My deal was created via the API but isn't in the pipeline"
**Symptom**: The API returns a created deal, but it doesn't appear in the milestone/pipeline view.
**Cause**: `milestoneLabelName` (and `track`/`track_id`) are case-sensitive and must match the account exactly; a mismatch creates the deal but hides it from the view.
**Solution**: Fetch the account's tracks (`GET .../deals/tracks`) and use the exact track and milestone names. Correct the case and the deal appears in the pipeline.
