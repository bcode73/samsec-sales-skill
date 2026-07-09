---
name: sales-ahrefs
description: "Ahrefs (ahrefs.com) platform help — industry-leading SEO toolset: Site Explorer (backlinks, organic keywords, Domain Rating), Keywords Explorer, Rank Tracker, Site Audit, Content Explorer, and Brand Radar AI-visibility. REST API v3 (api.ahrefs.com/v3, Bearer key, metered API units; v2 now discontinued) plus an official MCP server (Claude/ChatGPT/Cursor, Lite+). Use when building an Ahrefs API integration, your API units or monthly credits keep running out, setting up the Ahrefs MCP server with Claude, migrating off the dead v2 API to v3, getting throttled or locked by the 'suspicious activity' system within your limits, pulling backlinks/keywords/DR into a warehouse or report, deciding if you need the paid API subscription vs Enterprise, or choosing Starter vs Lite vs Standard vs Advanced. Do NOT use for SEO strategy or tool selection across vendors (use /sales-seo), AI-search-visibility tracking strategy across tools (use /sales-ai-visibility), or content optimization strategy (use /sales-seo)."
argument-hint: "[describe what you need help with in Ahrefs]"
license: MIT
version: 1.0.1
tags: [sales, seo, content, platform]
github: "https://github.com/ahrefs"
---

# Ahrefs Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Build an API integration — pull backlinks, organic keywords, Domain Rating, rank data
   - B) Set up the **MCP server** so Claude/ChatGPT can query your Ahrefs account by prompt
   - C) Fix **API units / monthly credits** running out, overage fees, or "suspicious activity" throttling
   - D) Migrate a dead **v2** integration to **v3**
   - E) Pick/understand a plan — Starter vs Lite vs Standard vs Advanced vs Enterprise; the credit + API-unit model
   - F) Use a specific tool — Site Explorer, Keywords Explorer, Rank Tracker, Site Audit, Content Explorer, Brand Radar

2. **REST or MCP?** Scheduled pipelines/exports → REST API (tight `select`). Ad-hoc agent questions → the MCP server. Both spend the same **API units**.

Skip-ahead rule: if the user's prompt already provides enough context, skip to Step 2.

## Step 2 — Route or answer directly

| If the question is about... | Route to... |
|---|---|
| SEO strategy, tool selection, or content optimization across vendors | `/sales-seo {question}` |
| AI-search-visibility (Brand Radar–style) tracking strategy across tools | `/sales-ai-visibility {question}` |
| Connecting Ahrefs data to other tools generically (iPaaS/warehouse) | `/sales-integration {question}` |

When routing, give the exact command, e.g. "This is an SEO-tool-selection question — run: `/sales-seo Ahrefs vs Semrush for a small content team on a budget`".

## Step 3 — Ahrefs platform reference

**Read `references/platform-guide.md`** for the full reference — the module map (what's API vs MCP vs UI-only), the pricing model (the **credit system** on lower tiers, **API-units** allocation vs the **paid API subscription/Enterprise** for heavy use, $199/$99 add-ons, no free trial), the data model with JSON shapes, and quick-start recipes (pull competitor keywords unit-aware; wire the MCP into Claude; bulk-score domains with batch-analysis).

**Read `references/ahrefs-api-reference.md`** for the integration surface — base `https://api.ahrefs.com/v3`, Bearer auth (keys from Account → API keys, owners/admins, 1-yr expiry), the **API-units** cost model (min 50 units, scales with rows × fields, free endpoints), the endpoint groups (Site Explorer, Keywords Explorer, Rank Tracker, Site Audit, Batch Analysis, limits-and-usage), and the official **MCP server** setup.

Answer using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

Focus on the user's specific situation:

- **Budget units like money.** Every data call costs **≥50 units**, scaling with rows × fields. Always pass
  **`select`** (only needed fields), cap **`limit`**, prefer **`batch-analysis`** for many targets, cache,
  and poll **`/subscription-info/limits-and-usage`**. This single discipline prevents most "ran out" pain.
- **v3 only.** v2 was fully shut off **2025-11-01** — any v2 tutorial/endpoint is dead. New keys + v3 paths.
- **Use the MCP for agents, REST for pipelines.** The official MCP (Lite+) lets Claude/ChatGPT pull data by
  prompt; it draws on the **same unit budget**, so keep agent queries specific.
- **Pace automated calls.** Ahrefs' anti-abuse "suspicious activity" system throttles bursty access even
  within plan limits — add jitter/backoff, don't hammer in parallel.
- **Know the real cost.** Lower tiers meter **credits** (1 per report); heavy **API** use needs a paid API
  subscription (~$500–$10k/mo) or Enterprise; Brand Radar/AI Content Helper/Report Builder are paid add-ons.
- **It's read-only.** No write API, no event webhooks — pull data out, push it into your own systems.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research (2026-06) — review these, especially pricing/credits and the unit model, which change often.*

1. **API units run out fast if you don't `select`.** Min 50/request and it scales with rows × fields. Request only the fields and rows you need; use `batch-analysis` and cache.
2. **API v2 is dead (since 2025-11-01).** Build only on v3 with a fresh key; old v2 integrations have no data access.
3. **"Suspicious activity" lockouts hit legit users.** Aggressive anti-abuse throttling can restrict you even inside plan limits — pace and back off automated calls.
4. **Credits ≠ API units.** The in-app **credit** system (1 per report, e.g. 500/mo on Lite) is separate from the **API-unit** allocation. Both can be exhausted; both cause overage/limits.
5. **Heavy API use is expensive.** The included unit allocation suits light use; production volume needs a paid API subscription ($500–$10k/mo) or Enterprise.
6. **No free trial; Starter is the cheap eval path.** Don't expect a trial — Starter ($29) is the lowest-cost way to evaluate.
7. **Add-ons stack.** Brand Radar ($199), AI Content Helper ($99), Report Builder ($99) are billed on top of the base plan.
8. **No affiliate program and no webhooks.** Don't look for either — Ahrefs is a read-only research tool that deliberately runs no affiliate program.

## Related skills

- `/sales-seo` — SEO strategy and tool selection across vendors (Ahrefs vs Semrush vs cheaper suites), content + technical SEO
- `/sales-ai-visibility` — AI-search-visibility tracking strategy across tools (Brand Radar is Ahrefs's add-on for this)
- `/sales-semrush` — Semrush platform help (the closest all-in-one competitor)
- `/sales-integration` — Connecting Ahrefs data to a warehouse/other tools (read-only pulls, no webhooks)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do -a claude-code`

## Examples

### Example 1: Pull a competitor's top keywords without blowing my units (developer/automation)
**User says**: "I want to export competitor.com's top 100 organic keywords from Ahrefs via the API."
**Skill does**: Walks Recipe 1 — `GET /api/v3/site-explorer/organic-keywords?target=competitor.com&country=us&limit=100&select=keyword,volume,position,traffic` with `Authorization: Bearer`. Stresses the **unit math** (min 50/request, scales with rows × fields), so a tight `select` + `limit` is essential, and to check `/subscription-info/limits-and-usage` first. Notes v3 only (v2 is dead) and keys come from Account → API keys (owners/admins).
**Result**: A unit-efficient keyword export.

### Example 2: Let Claude query Ahrefs directly
**User says**: "Can I connect Ahrefs to Claude so I can just ask for backlink data?"
**Skill does**: Points to the **official Ahrefs MCP server** (Recipe 2), available on **Lite+**: `claude mcp add --transport http ahrefs "https://mcp.ahrefs.com" --header "Authorization: Bearer $KEY"` (verify the hosted URL in the MCP docs). Warns that MCP queries spend the **same API units** as REST, so keep prompts specific. Frames MCP as best for ad-hoc exploration vs REST for scheduled pipelines.
**Result**: Claude pulls Ahrefs SEO data by prompt, unit-aware.

### Example 3: My Ahrefs bill/credits keep blowing up
**User says**: "I'm constantly hitting credit limits and overage fees on Ahrefs — is it just overpriced, or am I doing it wrong?"
**Skill does**: Separates the two meters — in-app **credits** (1 per report, 500/mo on Lite) vs **API units** — and gives concrete savings (use `select`/`limit`, batch-analysis, cache, monitor usage; upgrade tier or buy the API subscription only if genuinely needed). For the broader "is Ahrefs worth it vs Semrush/cheaper tools" decision, routes: "run: `/sales-seo Ahrefs credit limits — is a cheaper SEO suite enough for me`."
**Result**: User cuts usage waste and gets a path to the tool-selection decision.

## Troubleshooting

### My API calls fail or return "out of units"
**Symptom**: Requests error with a limits/units message, or stop returning data mid-month.
**Cause**: You've exhausted the monthly **API-unit** allocation — min 50 units/request scaling with rows × fields — or you're on a plan whose allocation suits only light use.
**Solution**: Add **`select`** to fetch only needed fields, lower `limit`, switch many single calls to **`batch-analysis`**, cache results, and watch **`/subscription-info/limits-and-usage`**. For sustained volume, move to a **paid API subscription or Enterprise**. Confirm you're on **v3** (v2 was shut off 2025-11-01).

### I keep getting throttled/locked even though I'm within my plan
**Symptom**: Restrictions or "suspicious activity" blocks despite staying within limits.
**Cause**: Ahrefs' anti-abuse system flags bursty/automated access patterns, sometimes catching legitimate API or heavy UI usage.
**Solution**: Pace requests (add delay + jitter), avoid heavy parallelism, back off on 429, and spread large jobs over time. If a legitimate workflow is blocked, contact Ahrefs support with your use case.

### My old Ahrefs API integration stopped returning data
**Symptom**: A previously working integration now returns nothing/errors.
**Cause**: It was built on **API v2**, which was **fully discontinued 2025-11-01** — v2 integrations no longer have data access.
**Solution**: Rebuild on **API v3** (base `https://api.ahrefs.com/v3`, Bearer key from Account → API keys), update endpoint paths to the v3 groups, and adopt the **API-units** discipline (`select`, `limit`, batch). For AI agents, consider the MCP server instead.
