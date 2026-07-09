---
name: sales-surfe
description: "Surfe (formerly Leadjet) platform help — a LinkedIn-to-CRM Chrome extension plus waterfall enrichment API (15+ providers) that pushes LinkedIn and Sales Navigator contacts into HubSpot, Salesforce, Pipedrive, or Copper and finds verified emails and mobile numbers. Use when Surfe enrichment credits run out faster than expected, the Chrome extension won't pull data on a LinkedIn profile, contacts aren't syncing to HubSpot or Salesforce, a bulk Sales Navigator export is incomplete, the async people/company enrichment job (enrichmentID) returns nothing, Surfe webhook x-surfe-signature HMAC verification keeps failing, or you're choosing between Surfe and Apollo or Lusha for LinkedIn CRM sync. Do NOT use for cross-tool enrichment strategy (use /sales-enrich) or building prospect lists from scratch (use /sales-prospect-list)."
argument-hint: "[describe what you need help with in Surfe]"
license: MIT
version: 1.0.0
tags: [sales, enrichment, platform]
github: "https://github.com/surfe"
---

# Surfe Platform Help

Surfe (formerly Leadjet) is a LinkedIn-to-CRM Chrome extension plus a waterfall enrichment API. It pushes LinkedIn/Sales Navigator contacts into HubSpot, Salesforce, Pipedrive, or Copper and finds verified emails and mobiles across 15+ providers.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what you still need:

1. **What are you trying to do?**
   - A) Push LinkedIn/Sales Navigator contacts into a CRM
   - B) Enrich a batch of people/companies via the API
   - C) Debug the Chrome extension (not pulling data, not syncing)
   - D) Wire up webhooks or troubleshoot signature verification
   - E) Understand credits/pricing or compare Surfe vs alternatives
2. **CRM in play?** HubSpot / Salesforce / Pipedrive / Copper / Google Sheets / none
3. **Surface?** Chrome extension (in-session) or REST API (background/bulk)

Skip-ahead rule: if the prompt already says what they need, go straight to Step 2/3.

## Step 2 — Route or answer directly

| If the user wants… | Route to |
|---|---|
| Enrichment strategy across many providers/tools | `/sales-enrich {question}` |
| Build a prospect list from scratch | `/sales-prospect-list {question}` |
| CRM data hygiene / dedup before enriching | `/sales-data-hygiene {question}` |
| Interpreting buying / job-change signals | `/sales-intent {question}` |
| Designing the outreach sequence after enrichment | `/sales-cadence {question}` |
| Choosing a CRM | `/sales-crm-selection {question}` |

When routing, give the exact command, e.g.: "This is a cross-tool enrichment question — run: `/sales-enrich how do I waterfall-enrich 5k leads cheaply`". Anything Surfe-specific, answer here.

## Step 3 — Surfe platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and automation surface, pricing/credit gates, data model (JSON shapes), and quick-start API recipes. **Read `references/surfe-api-reference.md`** for verbatim endpoint docs (auth, enrich/search endpoints, webhooks with HMAC verification, credits).

Answer using only the relevant section — don't dump the whole guide.

## Step 4 — Actionable guidance

- **Credits run out fast?** Remember Surfe credits are billed **per year**, not per month, across 3 separate pools (email/mobile/search). Reveal mobiles only for must-call contacts; set `skipMobileEnrichmentIfNoEmailFound: true`; poll `GET /v1/credits` before big batches.
- **"Surfe can't bulk-enrich"?** The *extension* enriches in-session only; the *API* does background bulk (≤10,000 people / ≤500 companies per job). Point API-capable users there.
- **Need data in the CRM?** The public REST API returns enriched data but does **not** write to your CRM — use the native extension/connector, or pipe the API result into the CRM's own API and map by `externalID`.
- **Webhooks > polling** for async jobs; verify `x-surfe-signature` before trusting any payload.

If you discover a gotcha or workaround not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and integration details that may be outdated.*

- **Credits are annual, not monthly.** Essential's "150 email credits/year" is ~12/month — easy to exhaust in two weeks. Budget against the annual number.
- **Three separate credit pools** (email, mobile, search) — running out of one doesn't free up another.
- **Extension is in-session only.** No background bulk enrichment from the extension; that's API-only.
- **API never writes to the CRM.** Enrichment is read-only data out; CRM writes go through the extension/connector.
- **Niche CRMs unsupported** — only HubSpot, Salesforce, Pipedrive, Copper (+ Google Sheets).
- **Per-seat pricing** scales up quickly for teams.
- Enrichment is **async**: a start call returns an `enrichmentID`; results come from the `GET .../enrich/{id}` endpoint or the webhook.

## Related skills

- `/sales-enrich` — Cross-tool contact/company enrichment strategy, waterfall and credit optimization
- `/sales-prospect-list` — Build the prospect list before enriching
- `/sales-data-hygiene` — Dedupe and clean CRM records (do this before enriching)
- `/sales-intent` — Act on job-change and buying signals
- `/sales-cadence` — Sequence the enriched contacts
- `/sales-crm-selection` — Pick the CRM Surfe should sync into
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Credits vanishing
**User:** "My Surfe email credits are already gone and it's only the 10th — what's going on?"
**Skill:** Explains Surfe credits are an **annual** quota (not monthly) split into email/mobile/search pools; shows how to check the balance via `GET /v1/credits`, recommends `skipMobileEnrichmentIfNoEmailFound`, revealing mobiles only for must-call contacts, and weighing a higher tier or a higher-credit alternative.

### Example 2 (developer/automation): Bulk-enrich via the API with a webhook
**User:** "How do I enrich 3,000 leads with Surfe in the background and get notified when each batch is done?"
**Skill:** Walks through `POST /v2/people/enrich` (Bearer auth, `include`/`people` arrays, `externalID` mapping, ≤10,000/job), capturing the returned `enrichmentID`, setting `notificationOptions.webhookUrl`, handling the `person.batch-enrichment.completed` event, and verifying the `x-surfe-signature` HMAC-SHA256 header before trusting the payload.

### Example 3: Contacts not landing in HubSpot
**User:** "I enriched a list with the Surfe API but nothing shows up in HubSpot."
**Skill:** Clarifies the public API returns enriched data but doesn't write to the CRM; CRM sync happens through the extension/native connector. Recommends using the extension for sync, or piping API results into HubSpot's API keyed on `externalID`.

## Troubleshooting

### Enrichment credits drain unexpectedly
**Cause:** Credits are an annual allocation across 3 pools, and mobile reveals are pricier than email.
**Fix:** Check `GET /v1/credits`; set `skipMobileEnrichmentIfNoEmailFound: true`; reveal mobiles only for prioritized contacts; gate large jobs on remaining `totalEmail`/`totalMobile`.

### Chrome extension won't pull data on a LinkedIn profile
**Cause:** Extension works in-session and depends on an active LinkedIn session/login; it can't bulk-enrich in the background.
**Fix:** Reload the LinkedIn tab and re-auth the extension; for background/bulk work, switch to the REST API (`POST /v2/people/enrich`).

### Webhook signature verification keeps failing
**Cause:** Signing the wrong string, or missing the webhook secret.
**Fix:** Sign exactly `"{timestamp}.{raw_request_body}"` with HMAC-SHA256 using the webhook secret (retrievable from API settings **after the first webhook fires**), compare to the `v0=` value in `x-surfe-signature`, and reject stale timestamps.
