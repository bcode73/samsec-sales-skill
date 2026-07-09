# Supernormal Platform Reference

## Platform overview

Supernormal is an AI platform for agencies and client-facing teams that captures meetings without a bot joining the call, then uses that context — along with uploaded files, emails, and documents — to generate client-ready deliverables. Originally a pure meeting note-taker, it has pivoted toward an "AI agent for agencies" positioning, with AI Agents that can create pitch decks, project briefs, follow-up emails, spreadsheets, and more from meeting context. 700K+ users. SOC 2 certified, AES-256 encryption.

## Key modules

### Desktop App (Bot-Free Capture)
- Records scheduled calls automatically without joining as a participant
- Runs in the background capturing system audio
- Manual "New note" option for in-person and ad-hoc conversations
- Supports Google Meet, Zoom, Microsoft Teams
- Mac and Windows

### AI Meeting Notes
- Automatic transcription in 60+ languages
- AI-generated summaries with action items and key discussion points
- Customizable note templates (paid plans)
- Custom vocabulary for industry-specific terminology (paid plans)
- Notes organized by project for contextual reference

### AI Agents
- Generate deliverables from simple natural-language requests
- Reference meeting transcripts, emails, and uploaded documents as context
- Create their own task lists and execute independently
- Deliverable types: follow-up emails, project briefs, strategic plans, pitch decks, presentations, research reports, mood boards, spreadsheets, slide decks, documents, images
- Export to Google Drive or other formats

### Norma (AI Assistant)
- Conversational AI assistant providing real-time insights during meetings
- Can answer questions and assist with brainstorming during calls

### Voice Agents
- AI participants that can actively participate in meetings
- Answer questions and provide assistance in real-time

## Pricing and limits

*Re-verified 2026-06-13 against supernormal.com/pricing and help.supernormal.com. Supernormal moved to "Supernormal 2.0" credit-based pricing: seat-based per-user pricing is gone — you pay for credits and invite unlimited teammates who share the credit pool. The legacy "Pro" tier is now named **Team**.*

### Current pricing — Supernormal 2.0 (credit-based)

| Tier | Price | Credits | Daily limit | Key additions |
|---|---|---|---|---|
| Free | $0/mo | 15/month | 5/day | Meeting notetaker (no bots), generate presentations/images/spreadsheets, unlimited projects, MCP to connect Supernormal to other tools |
| Team | $20/mo | 50/month | None | Everything in Free, plus credit rollover (next month, up to 2 years on annual), unlimited seats sharing credits, remove Supernormal badge |
| Business | $40/mo | 50/month | None | Everything in Team, plus SSO, audit logs, data retention, member visibility and admin controls |

How credits work (verbatim from the 2.0 pricing article): "Credits are used to perform tasks within Supernormal. Usage will depend on the type and complexity of tasks performed. Credits are shared between teams." There is no fixed "1 credit = 1 meeting" mapping — cost scales with task type/complexity.

The pricing rollout was announced mid-to-late April 2026; affected users were given one month to choose a new plan. Annual billing offers credit rollover for up to two years.

### Legacy pricing (pre-2.0, retained for reference — superseded)

The earlier per-seat model used Starter (Free), Pro ($10/$18), and Business ($19/$29) tiers, where Starter/Pro ran on GPT 3.5-Turbo and Business unlocked GPT-4. This legacy structure has been replaced by the credit-based 2.0 plans above. Supernormal no longer publishes the underlying AI model per tier on its current pricing or 2.0 pricing pages — treat any "GPT-4 is Business-only" claim as a legacy artifact unless re-confirmed.

## Integrations

*Re-verified 2026-06-13. MAJOR CHANGE: as part of the agentic-model pivot, Supernormal discontinued most native CRM/PM/automation integrations as of March 2, 2026.*

### Discontinued native integrations (removed 2026-03-02)
Verbatim from Supernormal support: "As of March 2, we will no longer support the following native integrations: ClickUp, Hubspot, Github, Salesforce, Pipedrive, Workable, Zapier, Asana." Rationale: "As we evolve towards an agentic model, we are reassessing the tools we partner with and how they fit into the new vision."

This means **native HubSpot, Salesforce, and Pipedrive CRM sync no longer exists** — the prior claims of auto-syncing recordings/notes/highlights to deals/contacts and auto-updating leads are no longer accurate. Native Zapier and Asana are also gone. For CRM sync today, use the MCP connection (have your AI tool read Supernormal context and write to the CRM) or a third-party Zapier/n8n connector that may still wrap Supernormal.

### Current native integrations (verified on supernormal.com/integrations, 2026-06-13)
- **Meeting capture**: Google Meet, Zoom, Microsoft Teams (desktop app, bot-free)
- **Calendar**: Google Calendar, Outlook Calendar — every meeting gets notes automatically
- **Email**: Gmail — inbox context in, drafted replies out
- **Storage**: Google Drive — reads Drive for context, saves outputs
- **Communication**: Slack — auto-share new meeting notes/videos to a channel via group settings (still active)
- **Project management**: Linear — listed as an **MCP** integration ("turn meeting action items into Linear issues")
- **AI / automation**: MCP (Model Context Protocol) — now the primary documented integration surface (see MCP section below)

### MCP (Model Context Protocol) — now documented
- **Server URL**: `https://api.supernormal.com/mcp`
- **Auth**: authenticate with your Supernormal account through your AI platform's connector settings (OAuth-style consent in the client; no public API key documented)
- **Capabilities**: lets Claude, Cursor, ChatGPT, or any MCP-capable tool read your meeting history and projects directly — query meetings/projects, retrieve action items, pull discussion summaries, draft follow-ups from meeting context
- **Claude Web note**: only Claude Pro, Max, Team, and Enterprise plans can add custom connectors (add at claude.ai/customize/connectors, name it Supernormal, paste the server URL, authenticate)
- **Zapier MCP**: Zapier also exposes a Supernormal MCP endpoint to wire Supernormal actions into MCP-capable tools without glue code

### Still missing (commonly requested)
- No public REST/GraphQL developer API (MCP is the only documented programmatic surface)
- No documented webhook system / no HMAC-signed event delivery
- No native Make connector; no developer portal with endpoint/auth/rate-limit docs

## Data model

No public API means no documented data model. Internally, Supernormal organizes:
- **Projects** — group meetings by client/initiative
- **Meetings** — individual captured sessions with transcript, summary, action items
- **Notes** — AI-generated or manual notes attached to meetings
- **Deliverables** — AI Agent outputs (decks, briefs, emails) linked to project context
- **Credits** — usage currency for meeting captures and AI Agent tasks

## Workflow setup

### Initial setup
1. Download desktop app (Mac or Windows)
2. Connect calendar (Google Calendar / Outlook)
3. Configure auto-capture settings (which meetings to record)
4. Create projects for each client/initiative
5. Set up Slack integration for team sharing

### Client deliverable workflow
1. Capture client call via desktop app (bot-free)
2. Review AI-generated notes and action items
3. Upload supporting files (brand guidelines, past work, brief docs)
4. Ask AI Agent: "Draft the follow-up email from today's call with [client]"
5. Review and export deliverable (Google Drive, PDF, etc.)
6. Share via Slack or directly to CRM

### CRM sync workflow (post-2026-03-02: native CRM sync removed)
Native HubSpot, Salesforce, and Pipedrive integrations were discontinued on 2026-03-02. There is no longer a "connect HubSpot/Salesforce in settings" auto-sync path. To get meeting context into a CRM today:
1. Set up the MCP connection (`https://api.supernormal.com/mcp`) in your AI tool
2. Have the AI tool read the relevant meeting/project and draft the CRM update or follow-up
3. Push to the CRM via that AI tool's own CRM connector, or via a third-party Zapier/n8n flow that still wraps Supernormal
4. Native Zapier was also removed — confirm any Zapier path uses a currently-working connector before relying on it

## Deep dives

### Bot-free vs bot recording
Supernormal offers two recording modes:
- **Desktop app (bot-free)**: Captures audio from your computer without any participant joining the call. Preferred for client meetings where a bot would be disruptive. Requires the desktop app running on your machine.
- **Bot mode**: An AI participant joins the meeting (visible to all participants). Enabled when you connect Zoom/Teams accounts. Can cause issues — bot may auto-join all calendar meetings.

**Recommendation**: Use desktop app (bot-free) for client calls. Reserve bot mode for internal meetings where visibility doesn't matter.

### AI Agent best practices
- Be specific in requests — reference which meeting, which client
- Upload context files (brand guidelines, past deliverables, templates) to improve output quality
- Start with simple deliverables (follow-up emails) before complex ones (pitch decks)
- Review all AI-generated client deliverables before sending — output quality varies (the legacy GPT-3.5-vs-GPT-4 per-tier split is no longer published on the 2.0 pricing pages; do not promise a specific model per plan)
- Credits are consumed per task and scale with task type/complexity — not a fixed "1 credit per task" — so plan usage around high-value outputs

### Competitive positioning
Supernormal's closest competitors for agency/deliverable use cases:
- **Sembly** — Also generates client deliverables (proposals, briefs, pitch decks). Stronger on API/webhooks (10 CRM connectors, MCP access). Weaker on deliverable variety.
- **Fathom** — Stronger on pure meeting notes and free tier (unlimited recordings). No AI agent/deliverable generation.
- **Fireflies** — Better API (GraphQL), conversation search, analytics. No AI agent/deliverable generation.
- **Fellow** — Better for internal meetings, 1:1s, and meeting management. Not agency-focused.
