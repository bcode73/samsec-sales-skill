---
name: sales-supernormal
description: "Supernormal platform help — AI agent for agencies that turns meeting context into deliverables (pitch decks, briefs, emails, spreadsheets). Use when setting up Supernormal desktop app for bot-free recording, Supernormal AI agents not generating deliverables, Supernormal credits running out or credit system confusion, Supernormal bot joining Zoom calls uninvited, comparing Supernormal to Sembly or Fathom or Fireflies for agency work, Supernormal MCP integration, Supernormal Slack or CRM sync to HubSpot or Salesforce, or Supernormal transcription accuracy issues with accents. Do NOT use for choosing between AI note-takers (use /sales-note-taker) or general meeting transcript API integration (use /sales-note-taker)."
argument-hint: "[describe what you need help with in Supernormal]"
license: MIT
version: 1.0.0
tags: [sales, note-taker, ai-agent, platform]
---

# Supernormal Platform Help

## Step 1 — Gather context

If `references/learnings.md` exists, read it first for accumulated platform knowledge.

1. **What are you trying to do?**
   - A) Set up Supernormal for my team (desktop app, recording, projects)
   - B) Use AI Agents to generate deliverables from meetings
   - C) Integrate Supernormal with my CRM or other tools
   - D) Troubleshoot a specific issue (bot joining uninvited, credits, transcription)
   - E) Compare Supernormal to another tool

2. **What's your team type?**
   - A) Agency / creative team (client work, deliverables)
   - B) Sales team (demos, discovery calls)
   - C) Internal / cross-functional meetings
   - D) Solo / freelancer

3. **Which plan are you on?**
   - A) Free
   - B) Team (formerly "Pro", $20/mo)
   - C) Business ($40/mo)
   - D) Not sure / evaluating

Skip-ahead rule: if the user's prompt already contains enough context, skip to Step 2.

## Step 2 — Route or answer directly

| Problem domain | Route to |
|---|---|
| Choosing between AI note-takers (Supernormal vs Fathom vs Fireflies etc.) | `/sales-note-taker {user's question}` |
| Building a transcript API pipeline to CRM/warehouse | `/sales-note-taker {user's question}` |
| General CRM integration patterns (Zapier, webhooks, iPaaS) | `/sales-integration {user's question}` |
| Reviewing a specific call for coaching | `/sales-call-review {user's question}` |

Otherwise, answer directly below.

## Step 3 — Supernormal platform reference

**Read `references/platform-guide.md`** for the full platform reference — modules, pricing, integrations, credit system, AI agents, deliverables.

Answer the user's question using only the relevant section. Don't dump the full reference.

## Step 4 — Actionable guidance

You no longer need the platform guide — focus on the user's specific situation.

**For setup**: Start with the desktop app (bot-free capture), organize meetings into projects by client, configure auto-capture for calendar events.

**For AI Agents**: Be specific in requests — reference which meeting/client. Upload supporting files (brand guidelines, past decks) for better output. Start with follow-up emails before attempting complex deliverables.

**For integrations**: Slack is the primary native integration. CRM sync to HubSpot/Salesforce is available. Zapier extends to other tools. MCP is listed but documentation is limited.

**For credit management**: Track daily vs monthly credit usage. The Team plan ($20/mo, formerly "Pro") removes daily limits and enables rollover. Prioritize high-value meetings for credit-limited plans.

If you discover a gotcha, workaround, or tip not covered in `references/learnings.md`, append it there.

## Gotchas

> *Best-effort from research — review these, especially items about plan-gated features and integration gotchas that may be outdated.*

- **Bot auto-join can surprise participants.** If you connect Zoom/Teams accounts, Supernormal may auto-join all future meetings with a bot participant — even external meetings. Disable auto-join in settings and use the desktop app for bot-free capture instead.
- **Transcripts are not editable.** Unlike Grain or tl;dv, you cannot manually correct transcription errors. Accuracy drops with poor audio, accents, or technical jargon.
- **Credit system is confusing.** Free plan has both daily (5) and monthly (15) credit limits. Team and Business each have 50 monthly credits with rollover and no daily limit. Credits scale with task type and complexity — there is no fixed "1 credit = 1 meeting/task" mapping.
- **Pricing moved to "Supernormal 2.0" credit-based plans (verified 2026-06-13).** Seat-based pricing is gone. Tiers are now Free ($0), **Team** ($20/mo — this replaced the old "Pro"), and Business ($40/mo); invite unlimited teammates who share the credit pool.
- **Native CRM/PM integrations were removed 2026-03-02.** ClickUp, HubSpot, GitHub, Salesforce, Pipedrive, Workable, Zapier, and Asana native integrations are gone. Current native integrations: Gmail, Google Calendar, Outlook Calendar, Google Drive, Slack, and Linear (via MCP). For CRM sync, use the MCP connection or a third-party Zapier/n8n connector.
- **MCP is now the primary documented integration.** Server URL `https://api.supernormal.com/mcp`; authenticate via your AI tool's connector settings. There is still no public REST/GraphQL API and no documented webhook system.
- **Desktop app is required for bot-free recording.** The Chrome extension alone won't capture audio without the desktop app running.
- **"No notes for my meeting" is common.** Recordings under ~1 minute may not generate notes. If notes don't appear after 10 minutes, contact support.
- **Per-tier AI model is no longer published.** The old "GPT-3.5 on lower tiers, GPT-4 on Business" split was a legacy artifact and is not stated on the current 2.0 pricing pages — don't promise a specific model per plan.

## Related skills

- `/sales-note-taker` — Compare Supernormal to Fathom, Fireflies, Avoma, Gong, and 30+ other AI note-takers, or build transcript API pipelines
- `/sales-sembly` — Sembly also generates client deliverables (proposals, briefs, pitch decks) from meetings — closest competitor for agency use cases
- `/sales-integration` — General CRM/tool integration patterns (Zapier, webhooks, iPaaS)
- `/sales-do` — Not sure which skill to use? The router matches any sales objective to the right skill. Install: `npx skills add sales-skills/sales --skill sales-do`

## Examples

### Example 1: Agency setting up Supernormal for client work
**User says**: "I run a marketing agency and want to use Supernormal to automatically create pitch decks and follow-up emails from client calls."
**Skill does**:
1. Recommends desktop app setup for bot-free client call capture
2. Explains project organization — one project per client for contextual AI
3. Walks through AI Agent usage: "Draft the follow-up from yesterday's call with Acme"
4. Notes that pitch deck quality improves when brand guidelines and past decks are uploaded as context
5. Flags credit limits on Free plan (15/month) and recommends the Team plan (formerly "Pro") for active agencies
**Result**: Clear setup path with client-organized projects and AI agent workflow.

### Example 2: Bot joining meetings uninvited
**User says**: "Supernormal AI Notetaker keeps joining my Zoom calls even when I don't want it to. How do I stop it?"
**Skill does**:
1. Explains that connecting Zoom account enables auto-join for all calendar meetings
2. Walks through disabling auto-join in Supernormal settings
3. Recommends switching to desktop app (bot-free) capture instead of bot mode
4. Notes that bot-free mode captures from your computer's audio without any participant joining
**Result**: Bot disabled, switched to bot-free desktop capture.

### Example 3: Comparing Supernormal to Sembly for deliverables
**User says**: "I need an AI meeting tool that can generate client proposals and briefs. Is Supernormal or Sembly better?"
**Skill does**:
1. Notes both generate deliverables from meetings — Supernormal positions as "AI agent for agencies", Sembly as "agentic meeting intelligence"
2. Compares: Supernormal has broader deliverable types (presentations, images, spreadsheets, mood boards) and a documented MCP server (api.supernormal.com/mcp) but no public REST API and — since 2026-03-02 — no native CRM connectors; Sembly has webhook automations, 10 CRM connectors, and MCP access
3. Flags Supernormal's credit system (Free/Team/Business) vs Sembly's tier-based pricing
4. Recommends Sembly if native CRM/REST/webhook integration matters, Supernormal if deliverable variety, bot-free capture, and MCP-into-Claude are priorities
**Result**: Clear comparison with decision criteria.

## Troubleshooting

### No notes generated after meeting
**Symptom**: Meeting ended but no notes appear, message says "This recording is too short"
**Cause**: Recordings under ~1 minute don't generate notes. Also, the desktop app must be running during the meeting.
**Solution**: Ensure the desktop app is running before the meeting starts. For short meetings, manually create notes via "New note" option. If notes don't appear after 10 minutes for a normal-length meeting, contact Supernormal support.

### Credit usage unclear — running out faster than expected
**Symptom**: Credits depleting quickly, unclear what counts as a credit
**Cause**: Both meeting captures and AI Agent tasks consume credits. Free plan has a 5-credit daily cap on top of the 15 monthly limit.
**Solution**: Check usage in account settings. Prioritize high-value meetings. Upgrade to Team ($20/mo, formerly "Pro") for 50 monthly credits with rollover and no daily cap. If running an agency with daily client calls, Team is the minimum viable plan.

### Transcription accuracy poor in technical discussions
**Symptom**: AI notes contain errors, especially with industry jargon, accents, or multiple speakers
**Cause**: Transcription accuracy varies with audio quality and vocabulary. Custom vocabulary is a paid feature.
**Solution**: Ensure good audio quality (headset > laptop mic). Enable custom vocabulary on paid plans to train the model on industry terms. Review and manually correct critical deliverables before sending to clients.
