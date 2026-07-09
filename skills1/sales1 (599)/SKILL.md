---
name: sales-texau
description: "TexAu platform help — GTM automation and data platform: cloud/desktop LinkedIn and web automation ('automations'/recipes, automation hours), waterfall enrichment (65+ endpoints), people and lead search, async email finding and verification, web scraping, plus a REST API (base v3-api.texau.com, x-api-key header) and an MCP server (mcp.texau.com/mcp) for Claude and Cursor. Use when a TexAu LinkedIn automation gets your account restricted or banned, automations stall or hit hour limits that don't roll over, enrichment returns low fill rates or no emails, an async email-finding job returns nothing inline, you're wiring TexAu into a CRM or n8n via the API or webhooks, choosing between Cloud, Desktop, and the credit-based API, or budgeting pay-on-match credits. Do NOT use for cross-tool prospect-list strategy (use /sales-prospect-list) or choosing an enrichment provider across tools (use /sales-enrich)."
argument-hint: "[describe what you need help with in TexAu]"
license: MIT
version: 1.0.0
tags: [sales, prospecting-enrichment, platform]
github: "https://github.com/texauhq"
---

# TexAu Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask only what's needed to route (skip if the prompt already says):

1. **Which TexAu are you on?**
   - A) Cloud / Desktop automations (the classic recipe + automation-hours product — LinkedIn, Sales Nav, Twitter, web scraping)
   - B) The V3 GTM data platform (table interface, waterfall enrichment, AI Column)
   - C) The REST API / MCP server (programmatic, credit-based)
2. **What's the goal?** Build a list · enrich/find emails · scrape a site or directory · wire into a CRM/n8n · pick a plan · debug an account-safety/ban issue.
3. **Hitting an error?** Account restricted · automation stuck · empty enrichment result · async job returns nothing · webhook not firing.

Skip-ahead rule: if the user's prompt already contains enough context, go straight to Step 2.

## Step 2 — Route or answer directly

| If the user wants… | Route to |
|---|---|
| Cross-tool prospect-list strategy (which tool, ICP filters) | `/sales-prospect-list {question}` |
| Enrichment-provider strategy / waterfall design across tools | `/sales-enrich {question}` |
| Interpreting job-change / hiring signals across tools | `/sales-intent {question}` |
| Designing the outbound sequence after the list is built | `/sales-cadence {question}` |
| Connecting TexAu to a CRM / Zapier / Make generically | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is a cross-tool enrichment question — run: `/sales-enrich {original question}`". Otherwise answer here using Step 3.

## Step 3 — TexAu platform reference

**Read `references/platform-guide.md`** for the full reference — capabilities and automation surface, pricing/credits, data model, the async email-job flow, and integration recipes. For raw endpoints, methods, and field-level request shapes, read `references/texau-api-reference.md`.

Answer using only the relevant section. Don't dump the whole guide.

## Step 4 — Actionable guidance

You no longer need the guide — focus on the user's situation.

- **Account safety first.** TexAu drives LinkedIn with your own session cookie. No safety feature makes a ban impossible — keep daily action volumes human-like, use the cloud's dedicated IP/proxy, and never run two tools on one LinkedIn account at once.
- **Match the product to the job.** One-off LinkedIn/Sales Nav scrapes → Cloud/Desktop automations. Enrich-and-score-a-list at scale → V3 table or the API. Agent/Claude-driven runs → the MCP server.
- **Budget on outcomes, not attempts.** Pay-on-match means failed lookups return `billed: false` (no charge); bulk/`per_result` tools bill per row returned. Cache is on by default — turn it off when you need fresh data.
- **Email finding is async.** Submit the job with a `webhook` URL (or poll the inquiry endpoint); never expect inline results.

If you discover a gotcha, workaround, or tip not in `references/learnings.md`, append it there with today's date.

## Gotchas

*Best-effort from research (2026-06) — review these, especially plan-gated features and pricing that may be outdated.*

- **LinkedIn ban risk is real regardless of safety settings.** The #1 complaint. Use cloud dedicated IP/proxy, ramp limits slowly, and don't stack TexAu with another automation tool on the same account.
- **Two pricing models coexist.** Classic Cloud bills monthly *automation hours/minutes that do NOT roll over*; the V3/API product bills *pay-on-match credits that roll over up to 2× the monthly balance (Starter+)*. Don't assume one applies to the other.
- **API + webhooks are plan-gated.** On the V3 platform the API and webhooks come in on Starter and above — the entry (Solo) tier is UI + one-way daily CRM sync only (best-effort; verify on the pricing page).
- **Two endpoint brands.** The official API/MCP runs at `texau.com` (`v3-api.texau.com`, `mcp.texau.com/mcp`); the same team also publishes a `richapi.ai` MCP/skills variant. Use whichever host your dashboard issues your key for.
- **Cache defaults to on.** Most enrichment/scrape endpoints accept `useCache`/`cache` (default `true`) — stale data is a config issue, not a data-quality bug.

## Related skills

- `/sales-prospect-list` — Build the prospect list across tools (TexAu is one option among Apollo, Clay, PhantomBuster, Snov)
- `/sales-enrich` — Cross-tool enrichment strategy and waterfall design
- `/sales-intent` — Act on job-change / hiring signals from `lead_search`
- `/sales-cadence` — Design the outbound sequence once the list is built
- `/sales-integration` — Wire TexAu into a CRM, Zapier, Make, or n8n
- `/sales-phantombuster` — Closest competitor (Phantoms/Flows, agent→container→result API) for comparison
- `/sales-clay` — Competitor on the data-platform side (waterfall enrichment, Claygent)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Account got restricted after a LinkedIn automation
**User says**: "I ran a TexAu connection-request automation and now LinkedIn restricted my account."
**Skill does**: Explains bans are possible regardless of safety features; advises pausing all automations, lowering daily limits, running on the cloud's dedicated IP, and never stacking two tools on one account; covers safe ramp-up.

### Example 2 (developer/automation): Find emails in bulk via the API and collect results
**User says**: "How do I use the TexAu API to find emails for a list of people and get the results back in my app?"
**Skill does**: Points to `POST /email_finding` with `x-api-key`, a `webhook` URL, and a `data` array; explains it's async — results arrive at the webhook or via `GET /email_finding_inquiry/{id}`; notes pay-on-match billing (2 credits per person found) and shows the cURL.

### Example 3: Which TexAu plan/product to buy
**User says**: "Should I get TexAu Cloud, the Desktop one-time license, or the API?"
**Skill does**: Maps each to a use case (recurring team automations → Cloud; heavy solo runs with no monthly fee → Desktop $1,499 one-time; programmatic/agent enrichment → credit-based API/MCP), and flags that automation hours don't roll over while API credits do.

## Troubleshooting

### LinkedIn account restricted or banned after running an automation
**Cause**: Automated actions at non-human volume, shared IP, or two tools on one account.
**Solution**: Pause everything, let the account rest, then resume at low daily limits on the cloud's dedicated IP/proxy. Treat ban risk as inherent to LinkedIn automation — no setting removes it.

### Enrichment returns no data or a low fill rate
**Cause**: Waterfall exhausted all providers, or you're reading cached/empty results.
**Solution**: Confirm the input (LinkedIn URL/domain) is valid; failed lookups return `billed: false` so you weren't charged. Set `useCache: false` for fresh data and check `/usage` for remaining credits.

### Email-finding job returns nothing inline
**Cause**: Email finding/verification are async jobs, not synchronous responses.
**Solution**: The `POST /email_finding` call returns a job id; results are delivered to your `webhook` URL or fetched later via `GET /email_finding_inquiry/{id}`. Don't parse the initial response as the result.
