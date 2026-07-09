---
name: sales-fourfour
description: "Four/Four (fourfour.ai) platform help — AI customer-research / voice-of-customer copilot that unifies conversations (calls, tickets, emails, chat) from 30+ sources into searchable Insights and Topics, with an AI Analyst for natural-language Q&A and workflows that route findings to Slack/Jira/email. Developer surface: an OData REST API (`/odata`, OAuth2 authorization-code, `api:read` scope, `@odata.nextLink` paging), a CRM Importer API (`/import/crm/{type}`, PAT bearer, CSV, async jobs), HMAC-SHA256-signed webhooks (`Signature` header, 3x retry), and an MCP server (`fourfour.ai/mcp`). Use when pulling Insights or Conversations through the OData API, importing CRM accounts/contacts, verifying signed webhooks, wiring the MCP server into Claude/Cursor, picking an AI Analyst vs AI Researcher plan, or centralizing voice-of-customer data. Do NOT use for VoC survey-program strategy across tools (use /sales-customer-feedback) or feedback-board/roadmap voting (use /sales-frill)."
argument-hint: "[describe what you need help with in Four/Four]"
license: MIT
version: 1.0.0
tags: [sales, customer-feedback, voc, platform]
---

# Four/Four Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Read/sync Insights, Topics, or Conversations via the OData REST API
   - B) Push CRM accounts/contacts/opportunities in via the CRM Importer API
   - C) Verify a signed webhook (HMAC-SHA256) and react to insight/conversation events
   - D) Wire the MCP server into Claude / Cursor for natural-language Q&A
   - E) Use the AI Analyst / Workflows to route insights to Slack/Jira/email
   - F) Pick a plan (AI Analyst vs AI Researcher vs Enterprise) or understand usage limits

2. **API or no-code?** Code → OData API + CRM Importer + signed webhooks. AI assistant → MCP server. No endpoint → native connectors / Zapier / visual Workflows.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Voice-of-customer / survey **program** strategy (NPS/CSAT/CES) across tools | `/sales-customer-feedback {question}` |
| Feedback **boards** / feature voting / public roadmap | `/sales-frill {question}` |
| Aggregating **unsolicited** feedback across reviews/social/support | `/sales-noisely {question}` |
| Account health / churn-prevention **program** strategy | `/sales-customer-success {question}` |
| Connecting Four/Four to a CRM/PM tool generically (iPaaS) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-customer-feedback design a closed-loop VoC program`".

## Step 3 — Four/Four platform reference

**Read `references/platform-guide.md`** for the full reference — the Discovery/Validation/AI Analyst/Workflows/Competitive-Intelligence/Customer-Success module map (what's API vs webhook vs UI), plan tiers and usage limits, the Conversations→Insights→Topics→TopicModels data model, integrations by data-flow direction, and quick-start recipes.

**Read `references/fourfour-api-reference.md`** for the integration surface — OData base `https://fourfour.ai/odata`, **OAuth2 authorization-code** auth (`/oauth/token`, scope `api:read`, Bearer, 24h tokens), the entity sets (Insights/Topics/TopicModels/Conversations/Participants + CRM objects), **OData query options** (`$select`/`$filter`/`$top`/`$skip`/`$expand`, `@odata.nextLink` paging), the **CRM Importer API** (`/import/crm/{type}`, PAT bearer, CSV, async jobs), **HMAC-SHA256-signed webhooks** (`{timestamp, event, tenant, payload}`, `Signature` header, 3x retry), and the **MCP server** (`fourfour.ai/mcp`, OAuth discovery).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **OAuth2 + Bearer for reads.** Exchange the auth code at `/oauth/token` for a 24h Bearer token (scope `api:read`), refresh with the `refresh_token` grant. Keep `client_secret` server-side. Basic auth exists for BI tools but prefer OAuth for integrations.
- **OData paging is `@odata.nextLink`.** Page with `$top`/`$skip`; follow `@odata.nextLink` until it's absent — don't assume one page is the full set. Use `$filter` (e.g. `created ge {iso}`) and `$expand` to shape the pull.
- **Writes go through the CRM Importer, not OData.** The OData API is read-only; to push accounts/contacts/leads/opportunities/users use `PUT /import/crm/{type}` with **CSV** (required `id` column, ISO-8601 UTC dates). It's **async** — poll `/import/job/{jobId}`.
- **Verify webhooks (HMAC-SHA256).** Compute `HMAC-SHA256(rawBody, secret)`, constant-time compare to the `Signature` header, ack 2xx fast (it retries 3x with backoff), dedupe on `payload.id` + `timestamp`.
- **MCP for Claude/Cursor.** Add `https://fourfour.ai/mcp` as a remote MCP server; OAuth discovery handles auth and you get search tools over conversations/insights/accounts/contacts — no token plumbing.
- **It's VoC analysis, not a survey or feedback-board tool.** Four/Four mines *existing conversations* into insights; it doesn't run NPS/CSAT survey programs (→ `/sales-customer-feedback`) or host a public feedback board (→ `/sales-frill`).

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API captured from fourfour.ai/developers; pricing from fourfour.ai/pricing. Confirm in-account; the dev portal is JS-rendered so per-entity schemas may differ.*

1. **OData API is read-only; writes use the CRM Importer.** Don't try to POST/PATCH entities on `/odata` — push CRM records via `PUT /import/crm/{type}` (CSV) instead.
2. **Follow `@odata.nextLink`.** Server-driven paging — a single response is not the whole collection. Loop on `nextLink` until absent.
3. **CRM Importer is asynchronous.** `PUT` returns `202` + a `jobId`; row-level errors only show up when you poll `/import/job/{jobId}`. A 202 is not a success confirmation.
4. **Verify the webhook HMAC over raw bytes.** Hash the raw request body (not a re-serialized one) with the secret; constant-time compare to the `Signature` header. Wrong body bytes = signature mismatch.
5. **Two different credentials.** OData uses OAuth2 Bearer (`api:read`); the CRM Importer uses a Personal Access Token. Don't mix them.
6. **Plan gates: integrations are capped.** 40+ integrations exist but entry plans (AI Analyst £199/mo, AI Researcher £250/mo) cap active integrations (~2) and processing hours (50 hrs/mo, 100 tickets/mo). Notetaker is AI Researcher+; unlimited hours and embedded CRM apps are Enterprise.
7. **Usage-based, not per-seat.** You pay for content processed (hours/tickets), not seats — a big team on a small content volume can be cheap, and vice versa.

## Related skills

- `/sales-customer-feedback` — Voice-of-customer / survey-program strategy across tools (Four/Four is the conversation-mining option) — program design, metric selection, tool comparison
- `/sales-frill` — Feedback boards / feature voting / public roadmap (solicited board feedback vs Four/Four's conversation mining)
- `/sales-noisely` — AI aggregation of unsolicited feedback across reviews/social/support
- `/sales-customer-success` — Account-health / churn-prevention program strategy (Four/Four feeds the signals)
- `/sales-integration` — Connecting Four/Four to a CRM/PM tool via API/webhooks/Zapier
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull all of this quarter's insights into our warehouse (developer/automation)
**User says**: "How do I export every customer insight from Four/Four since April into BigQuery?"
**Skill does**: Shows the OData read flow — `GET https://fourfour.ai/odata/Insights?$top=100&$filter=created ge 2026-04-01T00:00:00Z` with `Authorization: Bearer {token}`, following **`@odata.nextLink`** until absent, then landing rows in the warehouse. Notes OAuth2 token (scope `api:read`, 24h) + refresh, and that `$expand` can inline the linked account/topic. Points to a nightly full pull reconciled with webhooks for freshness.
**Result**: A complete, paginated insight export.

### Example 2: Verify Four/Four webhooks so I can trust them
**User says**: "Four/Four is POSTing events to my endpoint — how do I make sure they're real?"
**Skill does**: Explains the **HMAC-SHA256** check — compute `hmac_sha256(rawBody, secret)`, constant-time compare to the **`Signature`** header, reject on mismatch. Notes the payload shape `{timestamp, event, tenant, payload}`, deduping on `payload.id` + `timestamp`, acking 2xx fast (it retries **3x with backoff**), and that the secret comes from Settings → Connections → Webhooks.
**Result**: Authenticated, tamper-evident webhook intake.

### Example 3: Four/Four vs a survey tool — which do I need?
**User says**: "We already record sales calls — should we use Four/Four or just send NPS surveys?"
**Skill does**: Frames the difference — **Four/Four mines conversations you already have** (calls/tickets/emails) into Insights/Topics with an AI Analyst and links them to deals, billed on content processed (no per-seat). A survey tool *solicits* structured NPS/CSAT. Recommends Four/Four when you have rich conversation data and want it queryable, and routes program/metric strategy: "run: `/sales-customer-feedback choose between solicited surveys and conversation mining`."
**Result**: A grounded build-vs-survey decision.

## Troubleshooting

### My OData export only returns the first batch of insights
**Symptom**: You get ~100 rows and think that's everything.
**Cause**: OData uses **server-driven paging** — the response carries an `@odata.nextLink` for the next page.
**Solution**: Read `@odata.nextLink` from each response and re-request it until it's absent (or page manually with `$top`/`$skip`). Accumulate across pages. Use `$count` to sanity-check the total.

### My CRM import "succeeded" (202) but records aren't showing up
**Symptom**: `PUT /import/crm/account` returned `202` but data is missing or partial.
**Cause**: The Importer is **asynchronous** — `202` only means *queued*, and row-level failures surface in the job, not the initial response. Common causes: missing required `id` column, non-ISO-8601 dates, or wrong record type.
**Solution**: Poll `GET /import/job/{jobId}` until `completed` and check the `errors` count; fix the CSV (required `id`, ISO-8601 UTC dates, supported type: account/contact/lead/opportunity/user) and re-upsert.

### My webhook signature check keeps failing
**Symptom**: The HMAC you compute doesn't match the `Signature` header.
**Cause**: Hashing a re-serialized body instead of the raw bytes, or using the wrong secret.
**Solution**: Compute **HMAC-SHA256 over the raw request body** with the webhook secret (Settings → Connections → Webhooks), then constant-time compare to the `Signature` header. Once verified, dedupe on `payload.id` + `timestamp` and ack 2xx quickly so Four/Four doesn't retry.
