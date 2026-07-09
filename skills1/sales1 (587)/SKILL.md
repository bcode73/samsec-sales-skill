---
name: sales-syncgtm
description: "SyncGTM (syncgtm.com) platform help — AI-native GTM data engine that unifies buying signals (job changes, funding, hiring, LinkedIn posts, web-traffic, custom AI signals), waterfall enrichment (verified emails/mobiles, 40+ providers), AI lead scoring (0–100 vs ICP), AI research agents, and a no-code Workflow Builder. Developer surface: an MCP server (api.syncgtm.com/mcp, OAuth browser sign-in, free-plan — works with Claude Code/Cursor to enrich, find emails/phones, read signals), a REST API (api.syncgtm.com, API key), webhooks, and 40+ integrations (HubSpot/Salesforce/Slack/Attio). Use when connecting the MCP server to an AI agent, enriching contacts via the API, acting on buyer signals, scoring leads vs an ICP, building a signal→enrich→outreach workflow, or choosing SyncGTM vs Clay/Trigify. Do NOT use for intent-data strategy across tools (use /sales-intent), prospect-list building (use /sales-prospect-list), or enrichment strategy across vendors (use /sales-enrich)."
argument-hint: "[describe what you need help with in SyncGTM]"
license: MIT
version: 1.0.0
tags: [sales, intent, gtm, platform]
github: "https://github.com/syncgtm"
---

# SyncGTM Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Use the MCP server from an AI agent (Claude Code, Cursor) to enrich / read signals
   - B) Enrich people/companies or find verified emails/phones via the REST API
   - C) Monitor + act on buying signals (job changes, funding, LinkedIn, web traffic)
   - D) Score leads 0–100 against your ICP, or build a signal→enrich→outreach workflow
   - E) Push results into a CRM/Slack (40+ integrations) or react via webhooks
   - F) Decide SyncGTM vs Clay / Trigify / Common Room / Koala, or pick a plan

2. **AI agent or app?** Agent → **MCP server** (token-free OAuth). Code/automation → **REST API** + webhooks. No-code → native integrations + Workflow Builder.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Intent-data / buyer-signal **strategy** across tools (which signals, how to act) | `/sales-intent {question}` |
| Building a **prospect list** across tools | `/sales-prospect-list {question}` |
| Contact **enrichment** strategy across vendors | `/sales-enrich {question}` |
| Outbound **sequence/cadence** strategy for the outreach step | `/sales-cadence {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-intent which buying signals predict pipeline for PLG SaaS`".

## Step 3 — SyncGTM platform reference

**Read `references/platform-guide.md`** for the full reference — the signal/enrichment/scoring/workflow model (what's MCP vs REST vs UI), the credit/plan model, the data model, and quick-start recipes (connect the MCP server; enrich via API; trigger a workflow on a signal).

**Read `references/syncgtm-api-reference.md`** for the integration surface — the **MCP server** (`https://api.syncgtm.com/mcp`, **OAuth browser sign-in, no token**, free-plan access; tools to enrich, find verified emails/phones, pull LinkedIn, read signals), the **REST API** (base `api.syncgtm.com`, API key), **webhooks**, the **signals** catalog, and the 40+ native integrations.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **For AI agents, use the MCP server — it's token-free.** Add `https://api.syncgtm.com/mcp` to Claude Code/Cursor; first connect does an **OAuth browser sign-in** (no long-lived API key to leak), and the **free plan** already grants MCP access. The tools enrich people/companies, find verified emails/phones, pull LinkedIn, and read signals.
- **For code, use the REST API.** Base `api.syncgtm.com` with an **API key** (from Settings → API). Use it for batch enrichment, signal reads, and scoring; confirm exact endpoints in the docs portal.
- **Signals → score → workflow is the core loop.** Configure prospect/account signals (job change, funding, LinkedIn post, web traffic, custom AI), let AI **score leads 0–100 vs your ICP** (HOT/WARM/COOL/COLD), and trigger a **Workflow Builder** automation (enrich → write → push to CRM/sequencer) when a signal fires.
- **Enrichment is waterfall.** It queries 40+ providers / 20+ databases sequentially for verified work email + mobile — expect higher hit rates than a single provider, but it consumes **credits**; scope what you enrich.
- **Push, don't poll.** Use **webhooks** (or native HubSpot/Salesforce/Slack) to act when a signal qualifies or a score crosses a threshold, instead of polling.
- **Right-size the plan.** Free (incl. MCP + core enrichment) is real; ~$99/mo adds deeper enrichment + signal-driven outbound; Enterprise above. It's **credit-based** — estimate usage before scaling.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — features/pricing verified against the marketing site + docs; the REST per-endpoint docs are JS-rendered, so confirm those in-account.*

1. **MCP server has no API token.** Auth is **OAuth browser sign-in** — there's no Authorization header; you approve once and the client stores the session. Revoke from the dashboard. (Great for agents; means you can't "paste a key" for MCP.)
2. **MCP vs REST are different auth.** REST uses an **API key**; MCP uses OAuth. Don't look for a REST bearer token for the MCP endpoint or vice-versa.
3. **It's credit-based.** Waterfall enrichment across 40+ providers burns credits fast — scope enrichment to scored/qualified leads, not your whole list. Use the credits estimator.
4. **REST endpoint detail is in the docs portal.** Exact paths/params/pagination/webhook events aren't on the marketing pages — pull them from `docs.syncgtm.com` (JS-rendered).
5. **Signal quality depends on configuration.** Custom AI signals and ICP definition drive scoring — vague ICPs produce noisy HOT/COLD labels. Invest in the ICP + signal setup.
6. **It overlaps Clay/Trigify.** SyncGTM bundles signals + enrichment + scoring + workflow + outreach; Clay is more of a flexible data canvas, Trigify is LinkedIn-signal-focused. For the *which-tool* decision, use `/sales-intent`.
7. **Enrichment ≠ deliverability.** Verified emails still need sending hygiene — route the email-sending side to `/sales-deliverability`.

## Related skills

- `/sales-intent` — Buyer-signal / intent-data strategy across tools (SyncGTM is one of the signal platforms) — which signals, how to act, tool selection vs Clay/Trigify/Common Room
- `/sales-prospect-list` — Building a prospect list across tools (SyncGTM sources + enriches leads)
- `/sales-enrich` — Contact/account enrichment strategy across vendors
- `/sales-cadence` — Outbound sequence strategy for the outreach step SyncGTM triggers
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Use SyncGTM from Claude Code via the MCP server (developer/automation)
**User says**: "How do I let Claude Code enrich a prospect and pull their buying signals with SyncGTM?"
**Skill does**: Walks the MCP setup — create a free account at app.syncgtm.com, add **`https://api.syncgtm.com/mcp`** as an MCP server in Claude Code, and approve the **OAuth browser sign-in** on first connect (no API token to manage; free plan includes MCP). Then the agent can call the SyncGTM tools to **enrich the person/company, find verified email/phone, pull LinkedIn, and read signals** inline. Notes revoking access from the dashboard and that enrichment uses credits.
**Result**: Claude Code enriches + reads signals directly, no key juggling.

### Example 2: Act on a buying signal automatically (workflow/webhook)
**User says**: "When a target account raises funding, I want it enriched and pushed to HubSpot."
**Skill does**: Configures a **funding signal** (account-level), an AI **lead score** gate (only HOT/WARM), and a **Workflow Builder** automation: signal → waterfall enrich → AI message → push to **HubSpot** (native) — or a **webhook** to a custom endpoint. Flags deduping, credit scope (enrich only scored accounts), and routing the *outreach* sequence design to `/sales-cadence`.
**Result**: Funding events become enriched, scored HubSpot records (and outreach) automatically.

### Example 3: SyncGTM vs Clay/Trigify — which do I need?
**User says**: "I already use Clay — is SyncGTM worth adding?"
**Skill does**: Frames the overlap — **SyncGTM** is an all-in-one signals + waterfall-enrichment + scoring + workflow + outreach engine (with an MCP server) at ~$99/mo, while **Clay** is a flexible data/enrichment canvas and **Trigify** is LinkedIn-signal-focused infrastructure. Recommends SyncGTM when you want signals→action in one tool (and agent/MCP access), and routes the cross-tool decision: "run: `/sales-intent signals + enrichment stack for a lean GTM team`."
**Result**: A grounded build-vs-add decision.

## Troubleshooting

### My AI client won't connect to the MCP server
**Symptom**: Adding `api.syncgtm.com/mcp` doesn't authenticate.
**Cause**: The **OAuth browser sign-in** didn't complete, your network blocks outbound HTTPS to `api.syncgtm.com`, or you have no SyncGTM account.
**Solution**: Create an account at **app.syncgtm.com** (free plan includes MCP), add `https://api.syncgtm.com/mcp` in your client, and complete the **browser** approval on first connect (it stores the session). Allow outbound HTTPS to `api.syncgtm.com`. There's **no API token** for MCP — don't add an Authorization header. Re-approve from the dashboard if you revoked it.

### My enrichment credits disappear fast
**Symptom**: Credits drain quickly during enrichment.
**Cause**: Waterfall enrichment queries 40+ providers per record, so enriching large/unscored lists is expensive.
**Solution**: Enrich **only scored/qualified leads** (gate on the AI ICP score), narrow which fields you request, and use the **credits estimator** before bulk runs. Cache results and avoid re-enriching unchanged records.

### My HOT/COLD scores look wrong
**Symptom**: Lead scores don't match reality.
**Cause**: A vague **ICP definition** or noisy/over-broad **signal** configuration.
**Solution**: Tighten the ICP (firmographics, techstack, must-have signals) and curate which **signals** count — custom AI signals should be specific. Re-score after tuning. For which signals actually predict pipeline, use `/sales-intent`.
