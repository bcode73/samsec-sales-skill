---
name: sales-phantombuster
description: "PhantomBuster (phantombuster.com) platform help — code-free web/LinkedIn automation + scraping + lead-gen: 'Phantoms' (LinkedIn search export, scrapers, auto-connect, email finder), Flows that chain them, AI Agents + a cloud LinkedIn Leads database. Developer surface: a REST API (base phantombuster.com/api/v2, X-Phantombuster-Key-1 header) to launch agents (POST /agent/{id}/launch → container id) and fetch run results (/containers/fetch-result-object), plus the Leads storage and per-agent webhooks (secret param, 11s timeout) on run completion. Billed by execution time + slots; API on all paid plans. Use when launching a Phantom or fetching its scraped output via the API, wiring a run-finished webhook, handling the async agent→container model, managing slots/execution-time, or LinkedIn cookie/safety issues. Do NOT use for prospect-list / lead-sourcing strategy across tools (use /sales-prospect-list), enrichment strategy across vendors (use /sales-enrich), or outbound cadence strategy (use /sales-cadence)."
argument-hint: "[describe what you need help with in PhantomBuster]"
license: MIT
version: 1.0.1
tags: [sales, prospecting, automation, platform]
github: "https://github.com/phantombuster"
---

# PhantomBuster Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Launch a Phantom via the API and fetch its scraped output (agent → container → result)
   - B) Get notified when a run finishes (per-agent webhook)
   - C) Pick/configure a Phantom (LinkedIn search export, profile scraper, auto-connect, email finder)
   - D) Chain Phantoms into a Flow/Workflow, or add an AI Agent step
   - E) Manage slots + execution-time limits, or the LinkedIn Leads storage
   - F) Handle LinkedIn session cookies / avoid getting an account flagged

2. **API or no-code?** Code → REST API (`X-Phantombuster-Key-1`) + webhooks. No endpoint → run Phantoms in-app, or Zapier/Make/n8n.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| Prospect-list / lead-sourcing **strategy** across tools (which scraper, ICP) | `/sales-prospect-list {question}` |
| Contact **enrichment** strategy across vendors | `/sales-enrich {question}` |
| Outbound **sequence/cadence** for the leads you scrape | `/sales-cadence {question}` |
| LinkedIn outreach **strategy** / account safety across tools | `/sales-cadence {question}` |

When routing, give the exact command, e.g. "This is a strategy question — run: `/sales-prospect-list build a LinkedIn ICP list safely`".

## Step 3 — PhantomBuster platform reference

**Read `references/platform-guide.md`** for the full reference — the Phantom/Flow/Agent model, the slots + execution-time + email-credits limits, the LinkedIn-cookie + safety model, plan tiers, and quick-start recipes (launch a Phantom; fetch results; wire a webhook).

**Read `references/phantombuster-api-reference.md`** for the integration surface — base `https://phantombuster.com/api/v2`, **`X-Phantombuster-Key-1`** auth, the **Agents** (`/agents/fetch-all`, `/agent/{id}/launch`, `/agent/{id}/fetch-output`), **Containers** (`/containers/fetch`, `/containers/fetch-result-object`), and **Storage** (LinkedIn Leads DB) endpoints, **JSend** responses, the **Agent-ID vs Container-ID** model, and per-agent **webhooks** (secret query param, 11s timeout).

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Agent → container → result.** `POST /agent/{id}/launch` queues a run and returns a **container id**; the scraped data isn't ready until that container finishes. Pick the **`output`** param deliberately, then read **`/containers/fetch-result-object?id=…`** for the structured leads.
- **Use a webhook, not tight polling.** Set the per-agent webhook (Advanced Notification Settings). It POSTs on completion — but **verify the `secret` query param** (webhooks can't send custom headers) and **return 200 within 11s** (ack fast, process async) or it's treated as an error.
- **Auth is the `X-Phantombuster-Key-1` header.** From Workspace settings, shown once. Anyone with it can launch your agents — keep it server-side, rotate if leaked.
- **Mind slots + execution time.** Phantom **slots** = concurrent automations (5/15/50 by tier); **execution time** = monthly run-hours (20/80/300). Long scrapes eat hours; you can't run more concurrent Phantoms than your slots. API is on all paid plans.
- **Scraping runs as you (session cookie).** Phantoms use your LinkedIn `li_at` cookie — runs act as your account, so respect human-like limits to avoid restriction, and refresh the cookie when it expires. For account-safety strategy, route to `/sales-cadence`.
- **It's a scraper/automator, not a CRM/sequencer.** Pipe the scraped leads to your CRM/sequencer (or Clay) — for outreach design use `/sales-cadence`.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — API verbatim from the docs; pricing/features from support + reviews. Confirm in-account.*

1. **Async: launch ≠ results.** `/agent/{id}/launch` returns a **container id** immediately; the data lands when the container finishes — webhook or poll `/containers/fetch`, then read `fetch-result-object`.
2. **Webhooks use a `secret` query param + have an 11s timeout.** No custom headers → verify the secret, not a header signature; respond 200 in <11s or it's a server error (ack then process async).
3. **`X-Phantombuster-Key-1` is the auth header.** Not `Authorization: Bearer`. Key from Workspace settings, shown once; rotate if leaked.
4. **v2, milliseconds.** v1 timestamps are seconds, v2 are ms — use v2 and don't mix.
5. **Session-cookie scraping has account risk.** Phantoms act as your logged-in account (LinkedIn `li_at`); over-aggressive runs can get the account restricted, and cookies expire. Keep volumes human, refresh cookies.
6. **Slots + execution-time cap throughput.** You can't exceed concurrent **slots**, and long scrapes burn monthly **execution hours** — size the plan to volume.
7. **Compliance gray area.** Scraping LinkedIn/sites can violate their ToS; use responsibly and within data-protection law.

## Related skills

- `/sales-prospect-list` — Prospect-list / lead-sourcing strategy across tools (PhantomBuster is one of the scrapers) — which tool, ICP, list hygiene
- `/sales-enrich` — Contact/account enrichment strategy across vendors (pair scraped leads with enrichment)
- `/sales-cadence` — Outbound sequence strategy for the leads you scrape- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Launch a Phantom and fetch its scraped leads via the API (developer/automation)
**User says**: "How do I run my LinkedIn Search Export Phantom from my backend and get the results?"
**Skill does**: Walks Recipe 1 — `POST https://phantombuster.com/api/v2/agent/{id}/launch` with the **`X-Phantombuster-Key-1`** header (and a chosen **`output`**), which returns a **container id**; then poll **`/containers/fetch?id=…`** until done and read **`/containers/fetch-result-object?id=…`** for the structured leads (JSend `data`). Recommends a **webhook** instead of tight polling, and keeping the key server-side.
**Result**: Backend launches the scrape and ingests the leads reliably.

### Example 2: Get notified when a run finishes (webhook)
**User says**: "I want my system pinged when a PhantomBuster run completes."
**Skill does**: Sets the per-agent webhook in **Advanced Notification Settings**, configures a **`secret`** (since webhooks can't send custom headers → **verify the secret query param**), and stresses the **11-second timeout** — the handler must **return 200 fast** and process async, then call `fetch-result-object` for the data. Offers Zapier/Make as a no-code alternative.
**Result**: Run-completion events drive ingestion without polling.

### Example 3: My LinkedIn account got a warning from PhantomBuster
**User says**: "LinkedIn flagged my account after running Phantoms — what happened?"
**Skill does**: Explains Phantoms run **as your account** via your **session cookie**, so aggressive volumes (connects/messages/scrapes) trigger LinkedIn's limits. Recommends staying within human-like daily caps, spacing launches, not maxing connection requests, refreshing the cookie when it expires, and warming new accounts. Routes account-safety strategy: "run: `/sales-cadence safe LinkedIn automation limits`."
**Result**: Safer automation settings and a recovery plan.

## Troubleshooting

### My launch succeeds but I get no data
**Symptom**: `/agent/{id}/launch` returns success but the results are empty/missing.
**Cause**: The run is **asynchronous** — launch only **queues** it and returns a **container id**; the data isn't ready until the container finishes (and you must read the *result object*, not the launch response).
**Solution**: Take the `containerId` from the launch response, poll **`/containers/fetch?id=…`** until it's finished (or use a webhook), then fetch **`/containers/fetch-result-object?id=…`** for the structured leads. Make sure the Phantom's **`output`** setting actually produces a result object.

### My webhook isn't firing / times out
**Symptom**: The completion webhook never arrives or errors.
**Cause**: The URL wasn't set in **Advanced Notification Settings**, the handler took **>11 seconds** (cancelled → server error), or you're checking for a header signature that doesn't exist.
**Solution**: Set the agent's webhook URL, **return 200 within 11s** (ack immediately, do work async), and **verify the `secret` query parameter** (webhooks can't send custom request headers). Re-test by launching the agent.

### I've run out of execution time / slots
**Symptom**: Phantoms won't launch or queue up.
**Cause**: You hit your monthly **execution-time** hours or your **Phantom slot** (concurrency) cap.
**Solution**: Check usage in the dashboard; reduce scrape scope (fewer profiles, narrower search), stagger launches, and free up slots by pausing idle Phantoms. Upgrade the tier if volume genuinely needs more hours/slots. For list-building strategy that minimizes wasted runs, use `/sales-prospect-list`.
