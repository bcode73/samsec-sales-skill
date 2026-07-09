---
name: sales-qwilr-automation
description: "Builds automations connecting Qwilr to CRM and other tools via API, Zapier, or native integrations. Use when reps manually copy deal data into proposals, Qwilr and your CRM are out of sync, proposal status isn't updating in Salesforce or HubSpot, you want proposals auto-created when deals hit a stage, or webhooks aren't triggering on proposal views or acceptance. Do NOT use for writing proposal content (use /sales-proposal-page), designing reusable templates (use /sales-proposal-template), or interpreting engagement signals (use /sales-proposal-analytics)."
argument-hint: "[describe what you want to automate — e.g., 'auto-create proposals when a deal hits Stage 3 in HubSpot']"
license: MIT
version: 1.0.0
tags: [sales, proposal, automation, crm, qwilr]
---
# Automate Qwilr with CRM & Tools

Help the user build automations that connect Qwilr to their CRM and other tools — via the Qwilr REST API, Zapier, or native integrations.

## Qwilr API overview

The Qwilr REST API lets you create pages from saved blocks with token substitutions, manage quote sections with interactive pricing, and subscribe to webhooks for real-time engagement signals.

**Quick reference**: Base URL `https://api.qwilr.com/v1`, JWT Bearer auth. Key endpoints: `POST /pages` (create), `GET /blocks/saved` (discover templates), `POST /webhooks` (subscribe to events).

For the complete API reference — endpoints, curl examples, token mapping, quote block structure, and testing checklist — consult `references/qwilr-api-reference.md`.

## Step 1 — Gather context


If `references/learnings.md` exists, read it first for accumulated knowledge.

Ask the user:

1. **What do you want to automate?**
   - A) Auto-create proposals when a deal reaches a certain stage
   - B) Sync proposal status/acceptance back to CRM
   - C) Get notified when prospects view or accept proposals
   - D) Full round-trip: create from CRM data + sync engagement back
   - E) Something else — describe it

2. **What CRM/tools are you using?**
   - A) HubSpot
   - B) Salesforce
   - C) Pipedrive
   - D) Zoho CRM
   - E) Other CRM (specify)
   - F) No CRM — just API/webhooks

3. **What automation platform do you prefer?**
   - A) Zapier
   - B) Make (Integromat)
   - C) Direct API (code/scripts)
   - D) Native Qwilr integration (HubSpot/Salesforce/Pipedrive)
   - E) Not sure — recommend what fits

4. **What Qwilr plan are you on?** (affects API access and native integrations)

**If the user's request already provides most of this context, skip directly to the relevant step.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end — don't gate your response behind gathering complete context.

## Step 2 — Architecture recommendation

Based on the user's answers, recommend the right approach with trade-offs:

### Native integrations (simplest)
- **HubSpot**: Qwilr's native integration auto-populates templates with HubSpot deal/contact data, syncs acceptance status back to deal properties
- **Salesforce**: Native integration maps Salesforce opportunity fields to Qwilr tokens, creates proposals from opportunity records
- **Pipedrive**: Native integration connects deal data to Qwilr templates
- **Best for**: Teams that want zero-code setup and use a supported CRM
- **Limitation**: Less customizable than API, limited to supported field mappings

### Zapier / Make (medium complexity)
- **Best for**: Multi-tool workflows (e.g., create proposal when Stripe payment received, or notify Slack when proposal viewed)
- **Approach**: Use Qwilr's Zapier triggers (page viewed, accepted) and actions (create page)
- **Limitation**: Slower execution, may hit rate limits at scale, costs per task

### Direct API (most powerful)
- **Best for**: Custom workflows, high volume, complex logic (conditional sections, dynamic pricing calculations)
- **Approach**: Call Qwilr REST API directly from your backend, serverless functions, or scripts
- **Limitation**: Requires development effort

## Step 3 — Build the automation

The build process follows four stages. For curl examples, JSON payloads, and token mapping details, consult `references/qwilr-api-reference.md`.

### 3a. Discover available blocks
List saved blocks via `GET /blocks/saved` to find the block `id` values for page creation.

### 3b. Create pages from CRM data
Use `POST /pages` with either a `templateId` or a `blocks` array. Pass CRM field values in a single top-level `substitutions` object (the API calls variables "substitutions", not "tokens"), set `published` (not `isPublished`), and put quote sections INSIDE a saved block for interactive pricing. See `references/qwilr-api-reference.md` for the exact field names.

### 3c. Subscribe to webhook events
Subscribe to `pageFirstViewed`, `pageViewed`, `pageAccepted`, and `pagePartiallyAccepted` events to get real-time engagement signals.

### 3d. Check page status
Use `GET /pages/{id}?expand=acceptance,metadata` to poll page details and acceptance status.

## Step 4 — Token/substitution mapping

Design the mapping between CRM fields and Qwilr template tokens. Common tokens include `{{company_name}}`, `{{contact_first_name}}`, `{{deal_amount}}`, `{{rep_name}}`, etc. For the full token reference and guidelines, see `references/qwilr-api-reference.md`.

Key principles:
- **Always auto-populate**: company_name, contact names, rep info, deal amount
- **Semi-auto** (verify after population): industry, company_size, product
- **Always manual**: executive summary, pain points, custom scope
- **Set fallback values** for optional tokens so pages don't show raw `{{token}}` text

## Step 5 — Testing checklist

Walk through end-to-end before going live: auth verification, block discovery, token rendering, quote block accuracy, webhook delivery, CRM sync, error handling, and publish flow. Full checklist in `references/qwilr-api-reference.md`.

## Common automation recipes

Three common patterns (detailed implementation in `references/qwilr-api-reference.md`):

1. **Auto-create proposal when deal hits Stage 3**: CRM trigger → `POST /pages` → update CRM with Qwilr URL
2. **Notify Slack when proposal is viewed**: `pageFirstViewed` webhook → Slack message → rep follows up
3. **Update CRM when proposal is accepted**: `pageAccepted` webhook → update deal stage to Closed Won → trigger onboarding

## Gotchas

- **Don't overcomplicate with custom API when Zapier works.** If the user's automation is a simple trigger-action (deal hits stage → create proposal), Zapier or the native integration is faster to set up and maintain. Reserve direct API work for custom logic, high volume, or complex conditional workflows.
- **Don't forget webhook retry and deduplication.** Qwilr webhooks may retry on failure, sending the same event multiple times. Any webhook handler must be idempotent — check for duplicate event IDs before processing. Claude often generates webhook handlers without this.
- **Don't assume CRM field names without checking.** Salesforce custom fields end in `__c`, HubSpot uses internal property names that differ from display names, and Pipedrive uses custom field keys. Always tell the user to verify their actual field names/IDs before building the mapping.
- **Don't skip testing with sandbox/test data.** Claude tends to generate API code that goes straight to production. Always recommend creating test pages with `published: false` first, using test deals in the CRM, and verifying substitutions render correctly before going live.

- **Substitutions are strings only.** Qwilr applies no formatting to variable values — dates and numbers must be passed as the exact final string (e.g. `"$48,000"`, `"March 30, 2026"`). Format CRM values before sending; omitted variables render as empty strings.

- **API is plan-gated and paid.** Per Qwilr's docs and API page, API access requires an Enterprise account with API access enabled and extra fees apply (contact Qwilr sales). Confirm the user has API access before recommending a direct-API build; otherwise steer to native integrations or Zapier.
- **Don't hardcode API tokens in scripts.** Use environment variables (`$QWILR_TOKEN`) for authentication. Claude sometimes generates examples with placeholder tokens inline — make sure the user knows to use env vars or a secrets manager.

- **Self-improving**: If you discover something not covered here, append it to `references/learnings.md` with today's date.

## Examples

### Example 1: Auto-create a Qwilr proposal when a HubSpot deal hits Stage 3
**User says**: "When a deal moves to 'Proposal' stage in HubSpot, I want a Qwilr proposal created automatically and the link written back to the deal."

**Skill does**:
1. Asks which automation platform fits — recommends the native HubSpot integration or Zapier here since this is a simple trigger-action, reserving direct API for custom logic.
2. Maps HubSpot deal/contact fields to Qwilr substitutions (`company_name`, `contact_first_name`, `deal_amount`, `rep_name`), warning that HubSpot internal property names differ from display names.
3. Configures the trigger on the deal-stage change, then `POST /pages` with a `templateId` and a top-level `substitutions` object (strings only, with fallback values), set to `published: false` for testing first.
4. Writes the returned Qwilr page URL back to a HubSpot deal property.

**Result**: Each deal entering Stage 3 gets a pre-filled Qwilr proposal, with its URL on the deal record — no manual copy-paste.

### Example 2: Notify Slack and sync CRM when a prospect views or accepts a proposal
**User says**: "I want a Slack ping when someone opens my proposal, and the deal to move to Closed Won when they accept it."

**Skill does**:
1. Subscribes to webhook events via `POST /webhooks` — `pageFirstViewed` for the view signal and `pageAccepted` for acceptance.
2. Builds an idempotent webhook handler that dedupes on event ID (Qwilr may retry and resend the same event) before acting.
3. Routes `pageFirstViewed` to a Slack message so the rep can follow up promptly.
4. Routes `pageAccepted` to update the CRM deal stage to Closed Won and trigger onboarding.

**Result**: Real-time view alerts in Slack and automatic Closed Won updates, with no duplicate Slack pings or double deal-stage changes.

## Troubleshooting

### Pages render raw `{{token}}` text instead of values
**Cause**: A substitution variable was omitted, misnamed, or sent with no fallback — Qwilr leaves unmatched tokens visible and renders omitted variables as empty strings.
**Solution**: Verify every template token has a matching key in the top-level `substitutions` object, pass values as preformatted strings (e.g. `"$48,000"`, since Qwilr applies no number/date formatting), and set fallback values for optional tokens so nothing shows as raw `{{token}}`.

### Webhook fires multiple times for the same proposal view or acceptance
**Cause**: Qwilr retries webhook delivery on failure, so the same `pageViewed`/`pageAccepted` event can arrive more than once, and a non-idempotent handler reprocesses it.
**Solution**: Make the handler idempotent — store and check the event ID before processing, and skip events already seen so Slack pings and CRM updates fire exactly once.

### Direct API calls return auth or access errors
**Cause**: The Qwilr REST API is plan-gated — it requires an Enterprise account with API access enabled (extra fees apply) — or the JWT Bearer token is missing/invalid.
**Solution**: Confirm the account has API access enabled before recommending a direct-API build; otherwise steer to the native CRM integration or Zapier. Supply the JWT as a Bearer token from an environment variable (`$QWILR_TOKEN`), never hardcoded in scripts.

## Related skills

- `/sales-proposal-page` — Write the actual proposal content and quote block design
- `/sales-proposal-analytics` — Interpret engagement signals and decide follow-up actions
- `/sales-proposal-template` — Design reusable templates for API auto-population
- `/sales-deal-room` — For complex multi-page deal rooms
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`
