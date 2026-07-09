---
name: sales-bitrix24
description: "Bitrix24 (bitrix24.com) platform help — free-forever all-in-one business suite with a full CRM (leads, deals, pipelines/funnels, contacts, companies, Smart Process Automation), plus tasks/projects, omnichannel contact center, sites/store builder, marketing, and collaboration; cloud or self-hosted on-prem. Method-based REST API (`/rest/{user_id}/{webhook_code}/{method}`) with inbound + outbound webhooks, OAuth 2.0 for apps, a 740+ app Market, and an MCP server. Use when adding/updating leads or deals via the API or a webhook, reacting to CRM events (ONCRMDEALADD/UPDATE) with outbound webhooks, batching calls to dodge rate limits, choosing inbound webhook vs OAuth, mapping pipelines/stages (CATEGORY_ID/STAGE_ID), migrating onto the free plan as a Keap/Ontraport alternative, or deciding cloud vs on-prem. Do NOT use for CRM selection or RevOps strategy across vendors (use /sales-crm-selection), or generic iPaaS wiring (use /sales-integration)."
argument-hint: "[describe what you need help with in Bitrix24]"
license: MIT
version: 1.0.1
tags: [sales, crm, platform]
github: "https://github.com/bitrix24"
---

# Bitrix24 Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Add/update/list leads or deals (and map pipelines/stages) via the REST API
   - B) React to CRM changes with outbound webhooks (ONCRMDEALADD/UPDATE, ONCRMLEADADD)
   - C) Pick an auth method — inbound webhook (your own portal) vs OAuth 2.0 (an app)
   - D) Batch many calls / handle rate limits
   - E) Set up CRM structure — pipelines, stages, Smart Process Automation, contact center
   - F) Decide Free vs paid tier, or cloud vs self-hosted on-prem

2. **Your portal or someone else's?** Automating *your* account → **inbound webhook**. Building an app others install → **OAuth 2.0**.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| **Choosing** a CRM across vendors (Bitrix24 vs HubSpot/Pipedrive/Zoho/Keap), or CRM/RevOps strategy tradeoffs across tools | `/sales-crm-selection {question}` |
| Generic iPaaS wiring to an ESP/other app | `/sales-integration {question}` |
| Omnichannel/contact-center or marketing **strategy** | `/sales-do {describe the goal}` |

When routing, give the exact command, e.g. "This is a selection question — run: `/sales-crm-selection free CRM for a solo founder`".

## Step 3 — Bitrix24 platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (CRM vs tasks vs contact center vs sites), the free-vs-paid + cloud-vs-on-prem model, the CRM data model (lead/deal/pipeline shapes), and quick-start recipes (create a deal; subscribe to a deal event; batch).

**Read `references/bitrix24-api-reference.md`** for the integration surface — the **method-based REST API** (`https://{portal}.bitrix24.com/rest/{user_id}/{webhook_code}/{method}`), **inbound vs outbound webhooks**, **OAuth 2.0** for apps, the core `crm.*` methods (`crm.deal.add`/`.list`/…, `crm.lead.*`, `crm.item.*` for SPA), `{result,time}` responses, **`batch`** (50 commands/request), and rate limits.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **It's RPC, not resource-REST.** You call methods (`crm.deal.add`, `crm.lead.list`) on a URL, not `GET /deals`. Each entity has `*.add/.update/.get/.list/.delete/.fields`.
- **Inbound webhook for your own portal.** A static URL with a secret code (Developer resources → Incoming webhook), **no expiry**, scoped by permissions — simplest for automating your account. Use **OAuth 2.0** only for multi-tenant/Market apps.
- **Pipelines = `CATEGORY_ID`, stages = `STAGE_ID`.** A deal's funnel is `CATEGORY_ID` (0 = default) and its column is `STAGE_ID` (a `crm_status`) — get valid values from `crm.dealcategory.*` / `crm.status.*` before writing.
- **Events carry only the ID.** Outbound webhooks (`ONCRMDEALUPDATE`, …) POST `{event, data:{FIELDS:{ID}}}` + an app token — verify the token, then `crm.deal.get` for current data; dedupe.
- **Batch to survive rate limits.** Bitrix24 throttles (~2 req/sec) — use **`batch`** (up to 50 commands, with `$result[...]` chaining) and back off on errors.
- **Free-forever is the hook.** Unlimited users on the free plan makes it a popular free **Keap/Ontraport/Zoho alternative**; paid tiers add automation/SPA depth, and **on-prem (Self-Hosted)** is available if you need to host it.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — features/pricing verified against the marketing site + API docs; confirm in-account.*

1. **Method-based RPC API.** No `GET /deals`; it's `crm.deal.list` on the webhook/OAuth URL. The verb set (`add/update/get/list/delete/fields`) is consistent across entities.
2. **Inbound webhook ≠ OAuth.** Webhook = your portal, static URL + secret, no expiry, but **some methods are blocked** (telephony, certain app-only ops). OAuth = apps, tokens expire (refresh).
3. **Pipelines/stages are IDs.** `CATEGORY_ID` (funnel) + `STAGE_ID` (`crm_status`) — using a label or a stage from the wrong funnel fails silently/odd. Read `crm.status.*`/`crm.dealcategory.*` first.
4. **Rate limits are real.** ~2 req/sec sustained + per-method operating-time limits — **batch** (50/req) and back off, or you'll get throttled.
5. **Outbound webhook payload is thin.** Only the entity ID arrives — re-fetch via `*.get`. Verify the application token; dedupe (events can repeat).
6. **It's a sprawling suite.** CRM is one of many modules; the breadth means a learning curve. For just-CRM selection, weigh vs focused CRMs via `/sales-crm-selection`.
7. **Cloud vs on-prem differ.** Self-Hosted unlocks source/extra control + outbound webhooks need an active license; cloud is managed. Pick deliberately.

## Related skills

- `/sales-crm-selection` — Choosing a CRM across vendors (Bitrix24 vs HubSpot/Pipedrive/Zoho/Keap/Ontraport) — selection strategy, free-tier tradeoffs
- `/sales-forecast` — Pipeline forecasting & RevOps analytics on top of your CRM data
- `/sales-data-hygiene` — Keeping CRM records clean (dedupe, enrichment, normalization)
- `/sales-integration` — Wiring Bitrix24 into an ESP/other app via webhooks/OAuth/Zapier
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Create a deal in the right pipeline via the API (developer/automation)
**User says**: "When a form is submitted, how do I create a Bitrix24 deal in a specific pipeline and stage via the API?"
**Skill does**: Walks Recipe 1 — create an **Incoming webhook** (Developer resources, scope CRM), then `POST …/rest/{user_id}/{code}/crm.deal.add` with `FIELDS:{TITLE, CATEGORY_ID:<pipeline>, STAGE_ID:<crm_status>, OPPORTUNITY, CONTACT_IDS, ASSIGNED_BY_ID}`. Stresses fetching valid `CATEGORY_ID`/`STAGE_ID` from `crm.dealcategory.*`/`crm.status.*` first, that the response `result` is the new deal ID, and using `batch` if creating the contact + deal together.
**Result**: Deals land in the correct funnel/stage from the form.

### Example 2: React to a deal moving stages (outbound webhook)
**User says**: "I want my system notified when a Bitrix24 deal is updated."
**Skill does**: Explains **Outbound webhook** setup (Developer resources → Outgoing webhook): handler URL + event `ONCRMDEALUPDATE`; Bitrix24 POSTs `{event, data:{FIELDS:{ID}}}` + an **application token**. The handler verifies the token, then calls `crm.deal.get?ID=…` for current fields (the event carries only the ID), and dedupes. Notes on-prem needs an active license.
**Result**: Real-time, verified deal-change notifications.

### Example 3: Is the free plan really enough, and cloud or on-prem?
**User says**: "I'm a solo founder — is Bitrix24 free actually usable, and should I self-host?"
**Skill does**: Confirms the **free-forever (unlimited users)** plan includes CRM + tasks + contact center basics — a genuine free Keap/Zoho alternative — with paid tiers adding automation/SPA/throughput. Frames **cloud (managed) vs on-prem Self-Hosted (you host, more control, license for outbound webhooks)**, and routes the cross-vendor decision: "run: `/sales-crm-selection free all-in-one CRM vs HubSpot free`."
**Result**: A grounded free-tier + hosting decision.

## Troubleshooting

### My API call returns an error / 401
**Symptom**: Calls to `/rest/{user_id}/{code}/{method}` fail.
**Cause**: Wrong/secret-rotated webhook code, the webhook lacks the **permission scope** for that method, or the method is one webhooks can't call (telephony/app-only).
**Solution**: Recreate/copy the **Incoming webhook** URL exactly (Developer resources), enable the right **scopes** (e.g. CRM), and confirm the method is webhook-eligible — if not, build an **OAuth** local app. Test with the docs' request generator / Execute button.

### My deals are created but land in the wrong place
**Symptom**: Deals appear in the default funnel/stage, not the intended one.
**Cause**: `CATEGORY_ID` (pipeline) and `STAGE_ID` weren't set, or `STAGE_ID` belongs to a different funnel.
**Solution**: Read valid funnels via `crm.dealcategory.list` and their stages via `crm.status.list` / `crm.dealcategory.stage.*`, then pass the matching `CATEGORY_ID` + `STAGE_ID` on `crm.deal.add`. A stage id from another funnel won't route correctly.

### I'm hitting rate limits / it's slow
**Symptom**: Throttling errors or slow bulk operations.
**Cause**: Too many sequential calls — Bitrix24 throttles (~2 req/sec + per-method operating-time limits).
**Solution**: Use the **`batch`** method (up to 50 commands per request, chaining with `$result[...]`), page `*.list` with `start`, add exponential backoff, and spread bulk jobs. For heavy syncs, prefer `batch` + selective `select` fields.
