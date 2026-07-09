# Jamy.ai Platform Reference

## Platform overview

Jamy.ai is an AI meeting assistant focused on multilingual teams. It records, transcribes, summarizes, and translates meetings in real time across Zoom, Google Meet, and Microsoft Teams. Key differentiator is real-time translation in 100+ languages with cross-language search — find insights from any meeting regardless of language spoken. SOC 2 Type II certified, enterprise-grade encryption, never trains AI on user data. Based in Europe, targets SMBs and global organizations.

## Key modules

### Meeting recording & transcription
- Automatic recording of audio and video on Zoom, Google Meet, MS Teams
- Real-time transcription with speaker labels in 100+ languages
- Auto-join via calendar integration (Pro+ for automatic, Starter requires manual)

### AI summaries & action items
- AI-generated meeting summaries customizable via templates
- Automatic action item extraction with assignment to participants
- Task syncing to Trello and Monday.com

### Translation & cross-language search
- Real-time bi-directional translation during meetings (100+ languages)
- Translation minutes are plan-gated (Starter: 60 min/mo, Pro: 300 min/mo, Global Business: unlimited)
- Cross-language search: find meeting insights regardless of source language
- 4-hour max meeting length on Global Business for translated sessions

> **2026-06-13 re-verify**: The live /pricing page no longer advertises "Unlimited"
> transcription on paid tiers — see the corrected pricing table below. Translation
> minutes (60 / 300 / Unlimited) are unchanged.

### AI Chat
- Natural language search and retrieval across meeting history
- Ask questions about past meetings and get AI-synthesized answers

### Phone call transcription
- Transcribe and generate reports from phone calls (not just video meetings)
- Details on plan availability unclear

## Pricing and limits

All prices per user/month. No credit card required for Starter. (Pricing verified
against live /pricing page 2026-06-13.)

| Feature | Starter (Free) | Pro ($14.99/mo) | Global Business ($29.99/mo) |
|---|---|---|---|
| Transcription | 300 min/mo | 300 + 500 min/mo | 800 + 500 min/mo |
| Recording | 300 min/mo | 300 + 500 min/mo | 800 + 500 min/mo |
| Translation | 60 min/mo | 300 min/mo | Unlimited (4-hr max meeting) |
| Storage | 1 workspace folder | Unlimited | Unlimited |
| Max meeting length | 60 min | Unlimited | Unlimited |
| Team members | 1 | Unlimited | Unlimited |
| Custom templates | 1 | Unlimited | Unlimited |
| Spaces | 1 | Unlimited | Unlimited |
| Auto-join | Manual | Automatic | Automatic |
| Audio/Video playback | Yes | Yes | Yes |
| Custom Words / White Label | — | — | Yes |
| **API Keys + Webhooks** | — | — | **Yes (Global Business only)** |
| Integrations | Zoom, Meet, Teams | All integrations | All integrations |

> **CRITICAL PLAN GATE (verified 2026-06-13)**: API Keys and Webhooks are listed as
> Global Business ($29.99/mo) features on the live pricing page — NOT available on
> Starter or Pro. Any programmatic/CRM-sync pipeline forces the Global Business tier.
> White Label and Custom Words are also Global-Business-only.

> **2026-06-13 correction**: The previous table claimed "Unlimited" transcription on
> Pro and Global Business. The live pricing page now lists capped monthly minute
> bundles ("300 + 500" on Pro, "800 + 500" on Global Business). The "60 days" Starter
> storage figure is also gone from the live page — Starter is now described by structural
> caps (1 workspace folder, 1 team member, 1 template, 1 Space).

**Not confirmed on live page (unverified)**: Annual billing discounts, any Enterprise
tier (a third-party listing mentioned one, but it is not shown on jamy.ai/pricing), add-ons.

## Integrations

### Video conferencing (native)
- **Zoom** — auto-record, transcribe, summarize, translate
- **Google Meet** — auto-join, notes, translation
- **Microsoft Teams** — AI summaries, transcription, translation

### CRM
- **HubSpot** — push call notes, transcripts, summaries, and tasks into deal/contact records
- **Salesforce** — Coming Soon
- **Pipedrive** — Coming Soon
- **Close.com** — Coming Soon

### Collaboration
- **Slack** — share summaries, clips, and next steps in channels
- **Notion** — save structured meeting notes and transcripts
- **Google Docs** — export summaries (via integration page mention)

### Project management
- **Trello** — convert action items to cards with tags, owners, due dates
- **Monday.com** — sync follow-ups into project items

### Email
- **Gmail** — send meeting reports and follow-ups automatically
- **Outlook** — share summaries, control meeting participation from calendar

### Automation
- **API & Webhooks** — trigger custom automations, connect to Zapier/Make
- Zapier and Make flows supported for CRM updates, analytics pipelines, custom alerts

## API

### Overview
- Docs: `https://docs.jamy.ai/` (JS-rendered SPA — endpoint paths/methods/headers not extractable via fetch; guessed subpaths 404)
- Help center: `https://helpcenter.jamy.ai/articles/1664038-creating-a-meeting-or-call-report-with-jamys-api`
- Auth: API key generated at `https://app.jamy.ai/settings/apikeys` (OWNER user type required)
- **Plan gate (verified 2026-06-13)**: API Keys are a Global Business ($29.99/mo) feature — not available on Starter or Pro.

### Known endpoints
- **Create Report** — generate a Jamy report from a meeting/call recording uploaded via API. The recording must be at a **publicly accessible URL** (private/auth-gated URLs fail). The same Create-Report flow exists in the UI (Reports → Calendar View → "Create Report" → name + participants + recording file URL).
- **Answer Question** — query reports programmatically (ask questions about meeting content)
- *Exact base URL, HTTP methods, header names, and request/response field schemas are NOT published outside the JS-rendered docs site and remain unverified.*

### Webhooks (delivered via Svix — verified 2026-06-13)
- **Plan gate**: Webhooks are a Global Business ($29.99/mo) feature.
- Configure at **Settings → Webhooks → "Configure Webhooks"**, which redirects to the **Svix** app. Click **Add Endpoint**, enter your URL + description, and subscribe to the event.
- **Event**: `meeting.processed` — fires when a meeting report is generated. (This is the only event surfaced in the setup guide.)
- **Payload**: Jamy sends the **report object** to your endpoint. Available fields include `tasks`, `summary`, `url`, and `duration` (these are the fields Jamy exposes for selective mapping when wiring through Zapier). Full payload schema is viewable in the Svix **Event Catalog**, and example events can be fired from the Svix **Testing** tab.
- **Signing / verification (Svix standard)**: every delivery carries `svix-id`, `svix-timestamp`, and `svix-signature` headers. Signatures are HMAC-SHA256 over `{svix-id}.{svix-timestamp}.{body}` using the base64 portion of the endpoint signing secret (the part after the `whsec_` prefix). Svix libraries reject deliveries whose timestamp is more than 5 minutes from now (replay protection). Verify with the official `svix` SDK or manually.
- For no-code flows: create the webhook in Zapier/Make first ("Catch Hook" trigger), then paste that URL as the Svix endpoint.

### Limitations
- API docs site (`docs.jamy.ai`) is a JS-rendered SPA — endpoint paths, HTTP methods, and header schemas can't be scraped; only the help center exposes prose-level detail
- Only 2 endpoints surfaced via the help center (Create Report, Answer Question)
- Rate limits not publicly documented
- No OAuth — API key auth only
- Webhook delivery is outsourced to Svix (so signing/retries follow Svix conventions, not a Jamy-custom scheme)

## Security & compliance
- SOC 2 Type II certified
- Enterprise-grade encryption (in transit + at rest)
- No AI model training on user data
- Private data storage available for enterprise customers

## Affiliate program
- Portal: `https://affiliates.jamy.ai`
- Also accessible from `https://app.jamy.ai/settings`
- Features: referral link tracking, dashboard, automated payouts
- Commission details not publicly documented

## Known issues (from 29 AppSumo reviews, 3.3/5 stars)

### Critical
- **Calendar integration breaks silently** — bot stops recognizing meetings, multiple users affected
- **AppSumo onboarding reliability** — auto-join works for direct signups but breaks for AppSumo users
- **Chrome extension inconsistent** — "almost never works" per some users

### Feature gaps
- Phone recording not included at any tier (users want at least minimal minutes)
- UI described as "basic" and lacking polish
- Folders don't sort alphabetically
- No bulk report operations
- No keyword search within folders
- No manual language selection for output

### Positive signals
- Customer support responsive when it works (some users report rapid feature deployment)
- Template customization praised
- Translation feature genuinely differentiating
- Good value vs $30/mo competitors
