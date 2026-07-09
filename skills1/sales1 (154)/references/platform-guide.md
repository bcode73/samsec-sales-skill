# Dume.ai Platform Reference

## Overview

Dume.ai is a chat-first AI executive assistant that connects 50+ workplace tools (Gmail, Calendar, Slack, Jira, Notion, GitHub, WhatsApp) into a unified conversational interface. Users issue natural language commands and Dume fetches real data, executes actions, and automates workflows. It includes a visual no-code workflow builder, custom AI agent creation, MCP server integration, and multi-model AI selection.

## Capabilities & automation surface

| Capability | Description | Automation surface |
|---|---|---|
| Email triage | Reads, sorts, labels incoming emails; drafts context-aware replies | **Connected service** (Gmail, Outlook via OAuth) |
| Morning briefing | Daily summary of meetings, messages, reminders at 8:00 AM | **Automated** (schedule-based) |
| Workflow Studio | Visual node-based workflow builder with triggers, delays, loops, conditionals | **Webhook triggers** (PRO+), **schedule triggers**, **integration triggers** |
| Custom AI agents | Purpose-configured autonomous agents with custom tools and instructions | **UI-only** (MAX plan for unlimited) |
| Multi-model AI | Choose GPT-5, Gemini 3.1, Perplexity, Mistral, Kimi, MiniMax, Qwen, GLM | **UI-only** (premium models on PRO+) |
| MCP integration | Connect external MCP servers for real-time data access in workflows | **HTTP-streamable / SSE** (PRO+) |
| WhatsApp | Voice, video, location, contact messages; slash commands; workflow triggers | **Connected service** (WhatsApp Business) |
| Dume Cowork | Desktop agent for multi-step computer automation (macOS + Windows) | **Desktop app** |
| Chrome extension | Page summarization, web scraping, cross-tab workflows | **Browser extension** |
| Voice input | Dictation and voice chat with real-time text-to-speech | **UI-only** |
| People Search | Find contact information and company data | **Built-in tool** |
| Web Scraper | Extract structured data from websites without coding | **Built-in tool** |
| Memory | Persistent context across conversations with user-controlled storage (plan-capped: 1–10 Mb) | **Automatic** |
| AI Phone Calls | Reach the assistant by phone and have it call you when something needs attention — full voice access, no typing (Web/Desktop v3.0, Jun 2026) | **Voice / phone** |
| Autonomous Routines | Describe a repeatable task in plain language and Dume automates it — no visual builder or code required (Web/Desktop v3.0, Jun 2026) | **Natural-language automation** |
| GitHub integration | PR analysis, code review, task generation from commits | **Connected service** |
| Task management | Create/assign tasks in Jira, Linear, Notion via chat | **Connected service** |

**Key limitation**: No public REST API. The developer surface is webhook triggers (PRO+) and consuming external MCP servers. Data cannot be programmatically extracted from Dume.

## Pricing, limits & plan gates

Prices verified from dume.ai/pricing on 2026-06-13. Monthly price shown is the standard (month-to-month) rate; the lower number is the effective monthly rate when paid yearly. Annual totals: GO $96/yr, PRO $180/yr, MAX $396/yr.

| Feature | Free ($0) | GO ($9/mo, $8 yearly) | PRO ($18/mo, $15 yearly) | MAX ($40/mo, $33 yearly) |
|---|---|---|---|---|
| Credits | 1,200/year | 30,000/year | 60,000/year | 144,000/year |
| Messages | 20/day | Unlimited | Unlimited | Unlimited |
| Integrations | 1 | All | All | All |
| MCP connections | 1 | 5 | 10 | Unlimited |
| Agents | 5 | 10 | Unlimited | Unlimited |
| AI models | Basic | Standard | Premium | All Frontier AI Models |
| Webhooks / triggers | None | None | All Triggers | All Triggers |
| Memory | 1 Mb | 2 Mb | 5 Mb | 10 Mb |
| Custom builds (AI workflow creation) | None | None | 5 AI Workflow Creations/mo | Unlimited |
| Dume Cowork | Basic | Standard | Full | Full |

Enterprise tier available with custom pricing, dedicated development, and tailored solutions.

**Plan selection guidance**:
- Free is a trial — 20 msgs/day, 1 integration, and 1 MCP connection prevent real use
- GO is the sweet spot for solopreneurs — unlimited messages, all integrations, 5 MCP connections, 10 agents
- PRO justified if you need webhook/trigger workflows, more MCP connections (10), unlimited agents, premium AI models, or AI workflow creation (5/mo)
- MAX for power users — unlimited MCP connections, unlimited AI workflow creation, all frontier models, 10 Mb memory

Note: webhooks/triggers and the "AI Workflow Creation" custom-build allowance both start at PRO. Agents are unlimited from PRO up (Free 5, GO 10).

**AppSumo lifetime deal** has been available at ~$59 — check AppSumo for availability.

## Integrations

| Integration | Direction | What it does |
|---|---|---|
| Gmail | Read/Write | Email triage, draft replies, send messages, morning briefing |
| Outlook/O365 | Read/Write | Email management for Microsoft ecosystem |
| Google Calendar | Read/Write | Meeting scheduling, daily planning, briefing |
| Microsoft Calendar | Read/Write | Meeting management for Microsoft ecosystem |
| Slack | Read/Write | Post updates, receive notifications, standups |
| Jira | Read/Write | Create/assign tickets, track issues, PR review |
| Notion | Read/Write | Create/update pages, task management |
| GitHub | Read | PR analysis, code review, task generation |
| Confluence | Read | Documentation access and search |
| WhatsApp | Read/Write | Messaging, voice, video, workflow triggers |
| Google Drive | Read/Write | File organization, document access |
| Linear | Read/Write | Task creation and management |
| MCP servers | Read | External data via Composio.dev or custom endpoints |

**Multi-account support**: Connect multiple Gmail accounts (added v3.6).

## MCP server integration

Dume consumes external MCP servers — it does NOT expose itself as an MCP server.

### Setup via Composio.dev (official partner)
1. Register at mcp.composio.dev and authenticate
2. Name your server and select desired actions/tools
3. Create the server instance
4. Select HTTP-Stream as client type and copy the generated URL
5. In Dume: Settings > MCP Configuration
6. Choose HTTP-Streamable type and enter server details
7. Test the connection (status changes from Disconnected to Connected)

### Custom MCP server
Supported protocols:
- **HTTP-streamable endpoints** for managed or custom servers
- **Server-Sent Events (SSE)** for custom implementations

Any MCP-compliant server with valid endpoints can be integrated. The connection is validated before production deployment.

### Use cases
- Inject live CRM/project data into chat prompts
- Trigger workflows based on external events
- Pull real-time status from GitHub, Notion, Google Sheets into conversations

## Workflow Studio

The visual workflow builder uses a node-based editor:

### Node types
- **Trigger Node** — starts workflow by webhook, schedule, or integration event (PRO+)
- **Delay Node** — waits a specified time before continuing
- **Loop Node** — repeats a set of actions
- **Conditional Node** — branches based on conditions
- **Action Node** — executes tasks (send email, create ticket, post to Slack)

### Pre-built templates
Templates available for common workflows — start from a template and customize.

### Example workflow: Email → Task → Notification
1. Trigger: New email matching label "Client Request"
2. Action: Extract action items using AI
3. Action: Create Jira ticket with extracted items
4. Delay: 1 hour
5. Action: Post summary to Slack channel

## Data model

Dume doesn't expose a data model via API. Core objects based on UI behavior:

- **Conversations** — chat threads with AI, persistent memory across sessions
- **Workflows** — node-based automation sequences with triggers and actions
- **Agents** — custom AI instances with specific tools, instructions, and memory
- **Integrations** — OAuth-connected external tools
- **Credits** — resource consumption metric for AI usage
- **Morning Briefing** — automated daily summary of meetings, messages, reminders

<!-- No JSON shapes available — no API exposes these objects -->

## Security & compliance

- AES-256 encryption for all connections
- OAuth authentication with no password storage
- Zero training on user data ("your data never trains our models")
- GDPR and CCPA compliance
- Revocable permissions with scope control

## Version history (key releases)

Versioning uses separate tracks per surface: **Web vX.Y**, **Desktop vX.Y**, **Chrome vX.Y** (verified from dume.ai/whats-new on 2026-06-13). There is no single "v4.x" build number — the latest release across surfaces is v3.0 (June 10, 2026).

| Version | Date | Key additions |
|---|---|---|
| Web v3.0 / Desktop v3.0 | Jun 10, 2026 | AI Phone Calls (call/get-called by the assistant, full voice access), Autonomous Routines (describe a repeatable task in plain language — no builder/code), rebuilt web app for hours-long task persistence |
| Desktop v1.2 / Web v2.9 | Mar 29, 2026 | Windows desktop app, desktop task automation, interactive widgets in chat |
| Desktop v1.1 | Mar 22, 2026 | Reliability & macOS improvements (MCP-tagged) |
| Chrome v0.1 / Desktop v1.0 / Web v2.8 | Mar 16, 2026 | Dume for Chrome extension, Dume Cowork desktop agent launch, expanded AI model lineup (GPT-5, Gemini 3.1) |
| Web v2.7 | Nov 19, 2025 | Frontier AI update — GPT-5.1 & Gemini 3 Pro |
| Web v2.6 | Nov 17, 2025 | WhatsApp voice/video/location/contact messages, native image generation |
| Web v2.5 | Nov 7, 2025 | Memory ("Dume Gets a Brain") — persistent context |
| Web v2.4 | Oct 31, 2025 | WhatsApp integration ("Dume Assistant on WhatsApp") |
| Web v2.3 | Oct 14, 2025 | Smarter assistant, calendar control, Trigger & Delay nodes, workflow upgrades |
| Web v2.2 | Sep 24, 2025 | Voice chat, multi-account support, agent upgrades |
| Web v2.1 | Aug 30, 2025 | Custom Agents & workflow scheduling |
| Web v2.0 | Aug 14, 2025 | Workflow Engine/Studio launch, MCP support, dashboard |
| Web v1.3 | Aug 2, 2025 | Deep Research & memory layer |
| Web v1.1 | Jun 6, 2025 | GitHub integration & advanced tools |
| Web v1.0 | May 25, 2025 | Core platform launch |

## Affiliate program

- **Commission**: Up to 15% recurring for every referral
- **Cookie duration**: 60 days
- **Payout**: PayPal, $50 minimum, monthly processing (first week of month)
- **Milestone bonuses**: $50 at 5 referrals, $120 at 10, $250 at 25
- **Sign up**: https://dume.endorsely.com (instant approval)
- **Restrictions**: No paid ads (Google Ads, Facebook Ads, PPC). Organic promotion allowed (social, content, email newsletters)
