<!-- Source: https://karax.ai, https://karax.ai/pricing, https://karax.ai/real-time-meeting-assistant, https://karax.ai/onechat, https://karax.ai/about, https://karax.ai/ai-workspace-faq (the /faq path now redirects here), https://karax.ai/blog/otter-ai-vs-fathom-vs-karaxai-best-ai-powered-meeting-tool. Re-verified 2026-06-13. -->

# KaraX.ai Platform Reference

## Overview

KaraX.ai is an agentic AI workspace that combines multi-model AI chat (Gemini 3 family — Gemini 3 Flash on free, Gemini 3.1 Pro / 3 Flash / 3.1 Flash Lite on Pro, plus Private models on Business+), real-time meeting transcription, and AI workflow automation across 800+ (marketed as "1000+") integrations — all from a single "OneChat" interface. Differentiator: intent-based computing where users describe outcomes and AI agents execute multi-step workflows across connected tools, replacing manual Zapier-style rule setups. NVIDIA Inception member. NOTE (re-verified 2026-06-13): the live pricing page now lists ONLY Gemini-family models — no Claude/Anthropic or other-vendor models are named. HQ now shown as "New York • Hyderabad" on the About page.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| OneChat AI Workspace | Unified AI chat interface (Gemini-family models — 1 on free, 3 on Pro, 3+Private on Business), context-aware search across meetings/files/emails | UI (all plans, model count varies) |
| Meeting Transcription | Real-time transcription for Zoom, Google Meet, Microsoft Teams | UI (all plans, duration varies) |
| AI Summaries | Auto-extract decisions, action items, key points from meetings | UI (all plans) |
| AI Workflow Automation | Multi-step agentic workflows across connected tools — describe outcome, AI executes | UI (Pro+, tool count varies by plan) |
| AI Agents | Persistent context-aware agents that execute tasks across your tool stack | UI (Pro+) |
| Document Integration | Google Drive, OneDrive file connectivity and searchability | UI (Pro+) |
| Email Integration | Gmail, Outlook email thread context and search | UI (Pro+) |
| CRM Integration | Salesforce, HubSpot native connectors | UI (Business+) |
| Collaboration Tools | Notion, Linear, ClickUp, Trello, Jira, Slack integration | UI (Pro+) |
| Workflow Builder | Visual workflow builder for custom automation | UI (Business+) |
| API | No documented public API or developer portal (no REST/GraphQL endpoints published). The meeting-assistant page lists "Internal APIs"/"Custom Systems" as integration targets, but no developer-facing API docs exist. | N/A |
| Webhooks | Webhooks ARE offered as part of the Business-plan workflow builder ("Advanced + Webhooks" on the pricing page) — re-verified 2026-06-13. No public webhook event/payload/signing docs are published, so treat them as a workflow-builder feature, not a documented developer webhook surface. | UI (Business+) |

## Pricing, limits & plan gates

| Feature | Starter (Free) | Pro ($14.99/mo annual) | Business ($39.99/mo annual) | Enterprise (Custom) |
|---|---|---|---|---|
| AI Models | 1 (Gemini 3 Flash) | 3 (Gemini 3.1 Pro, Gemini 3 Flash, Gemini 3.1 Flash Lite) | 3 + Private models | All |
| Daily AI Chats | 25 | 100 | 500 | Unlimited |
| Meeting capacity | 5 meetings/day, 30 min max each | 8 hours/day | 16 hours/day | Custom |
| App integrations | 4 apps | 800+ apps | All apps + CRM | All |
| Tools per workflow | 3 | 5 | 8 | Unlimited |
| Workflow builder | Basic | No-Code Shortcuts | Advanced + Webhooks | Unlimited |
| Data retention | 7 days | Unlimited | Unlimited | Unlimited |
| Encryption | AES-256 | AES-256 + TLS 1.3 | AES-256 + TLS 1.3 | Full E2EE |
| CRM (SF/HubSpot) | No | No | Yes | Yes |
| Monthly price (monthly billing) | $0 | $19.99 | $49.99 | Custom |

<!-- Pricing/models re-verified against karax.ai/pricing on 2026-06-13. Annual Pro = $179.88/yr (pay 9 months, get 12). Webhooks confirmed on Business via the "Advanced + Webhooks" workflow-builder row. AI models are now Gemini-family only — no Claude/Anthropic listed. -->


- Annual billing saves ~25% (9 months paid, 12 months received)
- No credit card required for Starter
- SOC 2 Type II, HIPAA compliant, GDPR-ready across all plans
- Enterprise adds: full E2EE, private AI models, custom infrastructure, dedicated support

## Integrations

**Meeting platforms (all plans):**
- Zoom
- Google Meet
- Microsoft Teams

**Productivity (Pro+):**
- Google Drive, OneDrive — file search and context
- Gmail, Outlook — email thread integration
- Notion, Linear, ClickUp, Trello, Jira — task/project management
- Slack — notifications and sharing

**CRM (Business+):**
- Salesforce — meeting summaries, action items, deal updates
- HubSpot — same as Salesforce

**Total: 800+ integrations on Pro+** (the FAQ and OneChat pages now market this as "1000+ tools" — re-verified 2026-06-13; the homepage header still says "800+ Integrations"). Appears to be a mix of native connectors and agentic AI-mediated connections (not traditional Zapier/Make — KaraX's AI agents handle the orchestration).

**No Zapier, no Make, no n8n, no iPaaS.** Automation is through the platform's own agentic AI, not external workflow tools.

## Data model

No public API — no programmatic data model. User-facing objects based on product documentation:

<!-- Constructed from marketing docs — verify against live product -->

**Meeting:**
```json
{
  "title": "Q2 Pipeline Review",
  "date": "2026-04-25T10:00:00Z",
  "platform": "zoom",
  "duration_minutes": 45,
  "transcript": "...",
  "summary": {
    "key_points": ["..."],
    "decisions": ["..."],
    "action_items": [
      {
        "description": "Follow up with ACME on pricing",
        "assignee": "Jane",
        "due_date": "2026-04-28"
      }
    ]
  }
}
```

**Workflow:**
```json
{
  "trigger": "meeting_ended",
  "description": "After each sales call, update Salesforce with notes and create ClickUp tasks for action items",
  "tools_used": ["salesforce", "clickup"],
  "status": "active"
}
```

## Quick-start recipes

Since KaraX has no public API, recipes are UI-workflow based using the OneChat interface.

### Recipe 1: Transcribe a Zoom sales call and auto-create tasks

1. Sign up at karax.ai (Starter is free)
2. Install the Chrome extension or desktop app (Windows/macOS/iOS/Android available)
3. Connect Zoom in OneChat settings
4. Join your Zoom call — KaraX auto-transcribes in real time
5. After the meeting, open OneChat and ask: "Create ClickUp tasks for all action items from my last meeting"
6. KaraX's AI agent extracts action items and creates tasks in connected ClickUp (Pro+ required)

**Gotchas:**
- Starter caps meetings at 30 min — upgrade to Pro for full sales calls
- ClickUp integration requires Pro plan ($14.99/mo)
- Transcripts auto-delete after 7 days on Starter

### Recipe 2: Auto-update Salesforce after meetings

1. Upgrade to Business plan ($39.99/mo) — CRM integration is not available on lower tiers
2. Connect Salesforce in OneChat settings
3. Describe the automation in OneChat: "After each meeting, log the summary and action items to the associated Salesforce opportunity"
4. KaraX's agentic AI handles the multi-step workflow: extract summary → match to SF contact/opportunity → update record
5. Verify by checking Salesforce activity feed

**Gotchas:**
- CRM integration is Business-only ($39.99/mo annual, $49.99/mo monthly)
- No API or webhook alternative — can't build a custom integration pipeline
- No Zapier/Make workaround since KaraX doesn't offer external iPaaS triggers

### Recipe 3: Multi-LLM research from meeting context

1. After a meeting, open OneChat
2. Ask a question that spans meeting context and external knowledge: "Based on today's call with ACME, draft a follow-up email addressing their budget concerns"
3. KaraX uses meeting transcript context + AI model to generate the email
4. Send via connected Gmail/Outlook, or copy to another tool
5. On Pro+, switch between the 3 Gemini-family models (Gemini 3.1 Pro / 3 Flash / 3.1 Flash Lite) to compare output quality

## Integration patterns

**No documented public developer integration surface.** KaraX publishes no public API docs, no OAuth flows, no SDK, and no MCP server. The Business plan's workflow builder does include "Advanced + Webhooks" (re-verified 2026-06-13), but there is no published webhook event catalog, payload schema, or signing documentation — so it is a workflow-builder feature rather than a documented developer webhook surface. All automation is otherwise mediated through the platform's agentic AI interface:

- **CRM sync**: Describe the desired data flow in OneChat → AI agent executes → no field mapping configuration, no manual sync rules
- **Task creation**: AI extracts action items from transcripts → creates tasks in connected tools → no Zapier zap required
- **Search**: Context-aware search across meetings, emails, files in OneChat — no external search API

**For teams needing programmatic/developer access**, KaraX is not suitable. Recommend:
- Fathom (REST API, webhooks, MCP server)
- Fireflies (GraphQL API, webhooks)
- Grain (REST API, MCP server)

## Company & compliance

- **Company**: KaraX.ai
- **HQ**: "New York • Hyderabad" (per the About page, re-verified 2026-06-13 — previously listed as a single NYC address; now dual-location)
- **NVIDIA Inception Program**: Member
- **Compliance**: The FAQ now states "SOC 2 and HIPAA-aligned practices" with role-based access control + audit logs, and "never uses customer data for AI model training"; the homepage still markets "SOC 2 Type II certified, HIPAA compliant, and GDPR-ready." Treat the stronger marketing wording with care — the FAQ language is softer ("aligned practices").
- **Encryption**: AES-256 (all plans), TLS 1.3 (Pro+), full E2EE (Enterprise). FAQ describes it generally as "256-bit AES and SSL/TLS."
- **Platforms**: Windows, macOS, iOS, Android, Chrome extension
- **Reviews**: 4.8/5 stars (127 reviews on website — no G2/Capterra presence found)
