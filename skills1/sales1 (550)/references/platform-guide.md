# Sonnet AI Platform Reference

## Platform overview

Sonnet AI is a bot-free AI meeting assistant that records device audio, transcribes conversations, generates structured notes, and auto-updates your CRM. Founded by Ted Chai (CEO, ex-Uber/State Dept) and Dylan Feng (CTO, ex-OpenAI/BAIR) — UC Berkeley roommates. YC S22. 7 employees in San Francisco. Backed by Techstars, NVIDIA Inception Program, AWS Activate.

Target audience: Professionals who want structured meeting notes and CRM automation without a bot joining calls. Designed for sales teams, legal professionals, medical practitioners, and recruiters.

**Note:** YC lists the company status as "Inactive" as of 2026-04. Verify current product availability and support responsiveness before team-wide adoption.

## Key modules

### Bot-free recording
Captures audio directly from the macOS device — no bot joins the meeting. Works across Zoom, Google Meet, Microsoft Teams, Discord, Slack. Windows is in public beta.

### AI-powered notes
Sonnet records and transcribes in real-time (per the official homepage: "Sonnet records and transcribes in real-time"). Notes/insights are generated as the call progresses and finalized post-call:
- Structured summaries (customizable format)
- Action items with assignees and deadlines
- Concept maps (visual relationship views)
- Table-format notes
- Domain-specific templates (sales, legal, medical, recruiting)

### Template gallery
Domain-specific templates:
- **Sales**: Discovery calls, demos, follow-ups
- **Legal**: Consultations, depositions
- **Medical**: Patient notes
- **Recruiting**: Interviews, evaluations

Users can customize what information Sonnet focuses on capturing.

### CRM auto-update
The official homepage now frames this as a **built-in CRM** ("Sonnet has a built-in CRM, auto-updated with your conversation data" / "No integrations needed"). Sonnet auto-updates CRM records from conversation data:
- Meeting summaries logged to contacts/deals
- Action items with assignees and deadlines
- Follow-up tasks created automatically
- Participant context enrichment

The product ships its own built-in CRM that updates itself from conversation data, so no external CRM is required. HubSpot and Salesforce are still listed as supported external CRMs by third-party directories (G2/Capterra/SoftwareSuggest), but the homepage no longer names a specific external CRM — verify current external-CRM connector availability in-app before relying on it. No manual data entry required — Sonnet maps conversation data to CRM fields.

### Relationship tracker
Builds context-rich profiles of everyone you meet:
- Accumulates context across meetings
- Pre-meeting participant research/context
- Personal details for follow-up enhancement

### Meeting prep
Calendar integration sends notifications before meetings start with participant context and history from previous conversations.

## Pricing and limits

*Pricing UNVERIFIED as of 2026-06-13 re-check — the official sonnetai.com/pricing page is JS-rendered and did not expose plan numbers to fetch, and third-party directories disagree on the Plus price ($17 vs $25 vs $29). Treat the figures below as the 2026-04 baseline and confirm live on sonnetai.com/pricing before quoting.*

| Plan | Monthly | Annual (per mo) | Recordings/mo | Max per recording | Storage | AI insights/call |
|---|---|---|---|---|---|---|
| Free | $0 | $0 | 5 | 30 min | 2 months | 3 |
| Plus | $25 | $15 ($180/yr) | 40 | 90 min | 6 months | Unlimited |
| Pro | $35 | $20 ($240/yr) | 100 | Not specified | Unlimited | Unlimited + priority support |
| Enterprise | Custom | Custom | Custom | Custom | Custom | Team features, custom integrations, white glove onboarding, dedicated AM |

**Key plan gates:**
- Free: Very limited — 5 recordings at 30 min, 2-month storage, 3 AI insights per call
- Plus: Removes most limits but caps at 40 recordings/90 min
- Pro: 100 recordings, unlimited storage, priority support
- Enterprise: Team functionality, custom integrations, dedicated support

Phone call recording listed as "Coming soon" on Plus tier.

## Integrations

### Video/audio platforms
- Zoom
- Google Meet
- Microsoft Teams
- Discord
- Slack

### CRM
- HubSpot (auto-update)
- Salesforce (auto-update)

### Calendar
- Google Calendar (meeting prep, reminders, auto-capture triggers)

### Missing integrations
- No Zapier, Make, or n8n integration documented
- No Pipedrive, Attio, Zoho, or other CRM support
- No Slack workflow/channel posting beyond basic integration
- No data warehouse or API export

## API and developer access

**No public API.** There is no developer portal, REST/GraphQL API, webhooks, or MCP server. Custom integrations are not possible beyond the native CRM connectors. This is a significant limitation for teams needing to pipe meeting data into custom workflows, data warehouses, or non-supported tools.

## Platform availability

- **macOS**: Full support (desktop app, Apple Silicon + Intel). Requires macOS Ventura (13.0) or later.
- **Windows**: Public Beta (app v1.0.32, released 2026-06-13 per the official downloads page). Installers may show a security warning during install — expected/safe to proceed.
- **iOS**: Mobile companion app "launching soon"
- **Linux**: Not supported
- **Web-only**: Not supported — desktop app required for recording

## Language support

~10 languages. Third-party directories (Capterra/SoftwareSuggest) list a specific set of ~10: English, Arabic, Chinese (Simplified), Chinese (Traditional), Dutch, French, German, Greek, Hindi, Spanish — not confirmed on the official site, so verify before relying on a specific language. One directory lists "English only"; the official site does not publish a language list. Either way, significantly fewer than competitors (Fireflies 60+, Notta 58, Jamy 100+, Sembly 48).

## Workflow setup

### Initial setup
1. Download macOS desktop app from sonnetai.com
2. Grant system audio permissions (required for device-level audio capture)
3. Connect Google Calendar for meeting detection and auto-capture
4. Connect CRM (HubSpot or Salesforce) for auto-update

### Per-meeting workflow
1. Sonnet sends pre-meeting notification with participant context
2. Desktop app captures audio during the meeting (no bot visible to participants)
3. Post-call: AI processes audio → generates transcript, summary, action items
4. CRM auto-updated with meeting data, action items, follow-up tasks
5. Shareable summary available for team distribution

### Template customization
1. Browse template gallery for domain-specific formats
2. Select template matching your meeting type (sales/legal/medical/recruiting)
3. Customize output format (table, concept map, structured summary)
4. Template applies to all future meetings of that type

## Competitive positioning

**Strongest for**: Teams that want bot-free recording with auto-CRM update and domain-specific templates, especially sales teams tired of manually updating HubSpot/Salesforce after calls.

**Weakest for**: Teams needing API access, Windows/Linux support, 20+ language transcription, live captions, or enterprise compliance features. The no-API limitation is significant — if you need custom integrations, Sonnet is not viable.

**Closest competitors**:
- **Granola** — also bot-free with CRM sync, but has API + MCP, supports Windows/web, syncs to Attio/Affinity in addition to HubSpot. CRM push is manual per-note vs Sonnet's auto-update.
- **Jamie** — bot-free, EU privacy-first, has REST API and webhooks, supports 100+ languages, macOS/Windows/iOS. No auto-CRM update like Sonnet's.
- **Fathom** — free unlimited recordings, deeper CRM field-mapping on Business tier, has full REST API + webhooks + MCP. Uses a bot (configurable).
- **Claap** — CRM auto-enrichment + deal scoring, REST API + OAuth, but uses video recording (heavier than audio-only).
