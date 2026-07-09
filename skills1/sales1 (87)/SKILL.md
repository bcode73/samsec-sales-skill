---
name: sales-catchintent
description: "CatchIntent platform help — AI-powered B2B buyer-intent monitoring, now LinkedIn-exclusive (Reddit/X/HN/Bluesky now sunset). Detects 8 intent signals (job changes, funding, hiring, exec moves, acquisitions, competitor engagement, keywords, ICP-fit), scores leads (Warmth/ICP/Intent/Recency), drafts openers, Bedrock-powered enrichment, HubSpot CRM push (Pipedrive/Close/Zoho coming), 27-tool OAuth MCP server at engine.catchintent.com/mcp for Claude/Cursor/Codex, alerts via Email/Slack/Discord/Telegram. Use when tuning intent monitoring, managing lead-volume quotas (Growth 1k / Scale 4k / Enterprise 25k+ leads/mo), MCP server connection isn't working with Claude or Cursor, CRM push isn't reaching HubSpot, drafted openers sound generic, or comparing CatchIntent vs Octolens vs Syften vs Brand24. Do NOT use for social listening strategy across tools or choosing between social listening platforms (use /sales-social-listening)."
argument-hint: "[describe what you need help with in CatchIntent]"
license: MIT
version: 1.0.1
tags: [sales, social-listening, intent-signals, lead-generation, platform]
github: "https://github.com/CatchIntent"
---

# CatchIntent Platform Help

Helps the user with CatchIntent platform questions — from listener setup and intent tuning through CRM integrations, MCP server, webhooks, and lead enrichment.

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

Ask the user:

1. **What area of CatchIntent do you need help with?**
   - A) Intent monitoring — configuring ICP, signal types, tuning which LinkedIn buyers surface
   - B) Leads — understanding scores (Warmth/ICP/Intent/Recency), filtering, lead-volume quota
   - C) Drafted openers — improving quality, customizing tone
   - D) CRM push — HubSpot (live); Pipedrive/Close/Zoho (coming soon)
   - E) MCP server — connecting to Claude, Cursor, or Codex (`engine.catchintent.com/mcp`)
   - F) Alerts — Email, Slack, Discord, Telegram notification setup
   - G) Browser extension — sending LinkedIn DMs / outreach
   - H) Team & billing — plan/tier features, lead-volume quota, products & outreach accounts
   - I) Something else — describe it

   *Note: CatchIntent is now LinkedIn-exclusive — Reddit/X/Hacker News/Bluesky monitoring was sunset in 2026-05. For those surfaces, route to `/sales-social-listening`, `/sales-octolens`, or `/sales-syften`.*

2. **What's your goal?** (describe your specific question or problem)

**If the user's request already provides most of this context, skip directly to Step 2.** Lead with your best-effort answer using reasonable assumptions (stated explicitly), then ask only the most critical 1-2 clarifying questions at the end.

## Step 2 — Route or answer directly

If the request maps to a specialized skill, route:
- Social listening strategy or tool comparison → `/sales-social-listening [question]`
- Buyer intent signals and prioritization → `/sales-intent [question]`
- Contact enrichment → `/sales-enrich [question]`
- CRM selection → `/sales-crm-selection [question]`
- HubSpot-specific config → `/sales-hubspot [question]`

Otherwise, answer directly from the platform reference below.

## Step 3 — CatchIntent platform reference

**Read `references/platform-guide.md`** for the full platform reference — capabilities, pricing, data model, integration recipes, MCP setup.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

1. **Intent tuning** — refine ICP/keywords and signal types to surface the right LinkedIn buyers; drop broad terms that generate low-fit leads
2. **Lead-volume management** — you're capped by leads/month per tier (Growth 1k / Scale 4k / Enterprise 25k+), not signal quotas; prioritize the highest-fit signals
3. **CRM push** — HubSpot is live; Pipedrive/Close/Zoho are coming soon. Check field mapping on push
4. **MCP setup** — add `https://engine.catchintent.com/mcp`, OAuth flow, no API key needed; 27 tools across leads/agents/outreach/workspace
5. **Alert routing** — match channels (Email/Slack/Discord/Telegram) to urgency; Slack/Telegram support interactive Reached-Out/Ignore buttons

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

*Re-verified 2026-06-13 against the live changelog, pricing page, and MCP listing. See `references/learnings.md` for the audit trail.*

- **LinkedIn-only now.** CatchIntent sunset Reddit/HN/Bluesky monitoring for new buyers (v3.0.0, 2026-05-13) and X/Twitter (v3.1.0, 2026-05-25). It is a LinkedIn-exclusive B2B intent/outbound product. Don't expect Reddit/HN/X/Bluesky coverage anymore — route those to `/sales-octolens`, `/sales-syften`, or `/sales-social-listening`.
- **Pricing is three lead-volume tiers, not signal quotas.** Growth (1,000 leads/mo), Scale (4,000), Enterprise (25,000+). Gated by Products and Outreach accounts (1/3/25). Exact dollar prices are no longer shown publicly — start a trial or book a demo. The old Basic/Pro $49/$69 signal-quota model is gone.
- **MCP server is on all plans, no add-on.** Endpoint `https://engine.catchintent.com/mcp`, OAuth (no API key), Streamable HTTP, **27 typed tools** (leads, agents, outreach, workspace) for Claude, Cursor, Codex, any MCP client. This is the primary programmatic surface — there is no traditional REST API.
- **CRM push: HubSpot is live; Pipedrive/Close/Zoho are "coming soon."** Current pricing lists CRM push on all tiers, but only HubSpot is confirmed shipped. Don't promise Pipedrive/Close/Zoho yet.
- **Webhooks are UNVERIFIED.** Current docs/changelog/pricing list alert delivery only via Email, Slack, Discord, and Telegram (with temperature + interactive buttons). Outbound webhooks to a custom endpoint are not confirmed — don't build a pipeline on them without testing.
- **Enrichment is Bedrock-powered.** Drafted openers and lead scoring (Warmth / ICP Fit / Intent / Recency) are core to all plans.
- **7-day trial requires card on file.** 50 trial leads. Cancel before day 7 to avoid charges (full refund policy in terms). Done-for-you service starts at $1,999/mo, 3-month minimum.

## Related skills

- `/sales-social-listening` — Social listening strategy — monitoring setup, Boolean queries, sentiment analysis, competitive intelligence, crisis detection, tool comparison
- `/sales-octolens` — Octolens — developer-first social listening with MCP server, REST API, webhooks across Reddit, GitHub, HN, X, LinkedIn, Bluesky
- `/sales-syften` — Syften — AI-filtered keyword monitoring across Reddit, HN, X, Bluesky, 15+ platforms, sub-minute alerts, REST API, webhooks
- `/sales-brand24` — Brand24 — social listening with MCP server, sentiment analysis, Share of Voice
- `/sales-reddinbox` — Reddinbox — AI audience intelligence with intent scoring across Reddit, X, Bluesky, HN
- `/sales-intent` — Buyer intent signals and prioritization from monitoring data
- `/sales-enrich` — Contact enrichment strategy across tools
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Set up LinkedIn intent monitoring
**User says**: "I want to find people on LinkedIn who are likely buyers for my project management tool"
**Skill does**:
1. Notes CatchIntent is LinkedIn-exclusive now (Reddit/HN/X/Bluesky were sunset in 2026-05) — if they need Reddit/HN coverage, routes to `/sales-social-listening`
2. Configures ICP + the relevant intent signals (e.g. hiring spikes, competitor engagement, category-keyword discussions) for project-management buyers
3. Configures Slack alerts (with interactive buttons) for immediate notification
4. Recommends reviewing the first batch of leads and tightening ICP/signal filters based on fit
**Result**: LinkedIn intent monitoring running with tuned signal detection and drafted openers

### Example 2: Connect CatchIntent to HubSpot CRM
**User says**: "How do I push CatchIntent leads into my HubSpot pipeline automatically?"
**Skill does**:
1. Confirms HubSpot is the live CRM connector (Pipedrive/Close/Zoho are coming soon); CRM push is listed on all current tiers
2. Walks through HubSpot native integration setup
3. Maps CatchIntent lead fields to HubSpot contact/deal properties
4. Notes the MCP server (27 tools) is the path for automating push, since outbound webhooks aren't a confirmed feature
**Result**: Qualified leads create contacts in HubSpot with intent context

### Example 3: MCP server integration
**User says**: "I want to use CatchIntent from Claude Code to check my latest signals"
**Skill does**:
1. Points to the CatchIntent MCP server at `https://engine.catchintent.com/mcp` (OAuth-based, no API key needed, Streamable HTTP, 27 typed tools)
2. Walks through connecting the MCP server in Claude settings; OAuth flow authorizes on first connect
3. Shows example natural language queries: "Show me today's high-intent LinkedIn leads" or "Draft an opener for this lead and push it to HubSpot"
**Result**: CatchIntent data and outreach actions accessible directly from Claude via MCP

## Troubleshooting

### Too many low-fit leads
**Symptom**: Most surfaced leads aren't real buyers — wrong seniority, wrong company size, off-ICP
**Cause**: ICP definition too broad or too many signal types enabled
**Solution**: Tighten the ICP (role, seniority, company size, industry). Narrow to the signal types that map to real buying motion for you (e.g. hiring spikes, competitor engagement, funding). Review the first batch and refine filters based on false positives.

### Lead quota exhausted mid-month
**Symptom**: You've hit your monthly lead cap before the billing cycle resets
**Cause**: Filters too broad, surfacing high-volume / low-fit leads
**Solution**: Tighten ICP and signal filters to capture only high-fit leads. CatchIntent meters by leads/month per tier (Growth 1,000 / Scale 4,000 / Enterprise 25,000+), not signal quotas. Upgrade tiers if you genuinely need more volume.

### CRM push not reaching the CRM
**Symptom**: Leads appear in CatchIntent but don't show up in HubSpot
**Cause**: Integration not authorized, or you're expecting a connector that isn't live yet
**Solution**: HubSpot is the live CRM connector; Pipedrive/Close/Zoho are announced as coming soon, so they may not work yet. Re-authorize the HubSpot connection in Settings > Integrations, confirm the target pipeline/list exists, and test with a single manual push. CRM push is a manual/one-click action, not continuous auto-sync — for automation use the MCP server.
