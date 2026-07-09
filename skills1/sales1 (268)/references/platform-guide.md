# Juma Platform Reference

<!-- Best-effort from research (2026-07). Juma is the rebrand of Team-GPT; verify pricing, credit rules,
and the MCP tool list against juma.ai before relying on specifics. -->

## Overview

Juma (**juma.ai**, formerly **Team-GPT**) is an **AI marketing workspace** for marketing teams, agencies,
and solo marketers — a team-first place to run marketing work with AI. Its primary differentiators: **Flows**
(700+ pre-built, end-to-end marketing workflows), **Projects** (persistent, shared context that keeps every
chat on-brand), **multi-model chat** (Claude, GPT-5, Gemini, Perplexity, Nano Banana, etc. from one seat),
and — uniquely in the persona/idea-validation cluster — a **real MCP server** (`mcp.juma.ai`) that exposes
40+ tools to Claude Code, Claude Desktop, ChatGPT, and Cursor. Buyer/user **persona generation** is one of
its Flows, which is why it belongs in this catalog alongside the persona generators.

## Capabilities & automation surface

Tag legend: **MCP** = drivable from the MCP server (Claude Code/Cursor/ChatGPT) · **UI-only** = web app only.

- **Flows** — 700+ pre-built marketing workflows that run a task end-to-end (research → generate →
  deliverable). Runnable in the UI; many equivalent capabilities are exposed as MCP tools. **UI + MCP**
- **Projects** — persistent workspaces holding brand voice, briefs, assets, and client context; applied
  automatically to chats in that Project. Create/list and search/read knowledge over MCP; **uploading files
  as knowledge is UI-only**. **MCP** (create/list/search/read) / **UI-only** (file upload)
- **Multi-model chat** — Claude, GPT-5, Gemini, Perplexity, Nano Banana and more; pick the model per task.
  Threads/replies/history are MCP-accessible. **UI + MCP**
- **Persona generation (Prompt Builder)** — describe the persona → answer follow-up questions → get a
  refined, editable prompt → pick a model → generate → convert to an editable page → save reusable custom
  instructions. Buildable in the UI; over MCP, compose it from `write_content` + project knowledge + brand
  tools. **UI + MCP**
- **Content & deliverables** — on-brand copy, structured reports/PDFs, presentations (PDF/PPTX), responsive
  web/landing pages, multi-asset campaigns, image generation, data analysis/charts. **MCP** (creation) /
  **UI-only** (editing an *existing* image)
- **Brand profiles** — colors, fonts, voice; import a profile from a URL; attach assets; assign to a
  project. **MCP**
- **SEO / GEO** — GEO (AI-answer citability) audits, visibility scores, keyword research, organic
  competitor discovery, on-page SEO (Lighthouse), LLM top-cited domains, AI search volume. **MCP**
- **Integrations runner** — discover and execute connected apps (Google Analytics, HubSpot, Slack, Asana,
  Google Ads, Meta/Facebook Ads, LinkedIn, Notion, Google Drive, SharePoint, OneDrive, Ahrefs, Webflow,
  n8n, and 100+ more) as tools. **MCP + UI**
- **Web tools** — open web search and web scraping as callable tools. **MCP**
- **Workspace administration** — user/seat management, security settings. **UI-only**

## Pricing, limits & plan gates

*Best-effort (2026-07) — confirm at juma.ai/pricing.* Juma is **credit-metered** and notably **does not
gate features by tier**: "every Flow, every integration, every AI model, every connection is available from
the free plan." What changes across tiers is the **credit allowance** and **enterprise controls**.

| Plan | Price | Credits | Seats | Notes |
|---|---|---|---|---|
| **Free** | $0 | ~300 free credits per user | Unlimited | Full access to Flows, integrations, and all AI models; MCP included |
| **Pro** | ~$49/mo | 5,000–100,000 credits/mo (multiple tiers) | Unlimited | Credits **roll over**; **auto-recharge** option; usage reports |
| **Enterprise** | Custom | Custom | Unlimited | **Private cloud** (AWS/Azure/GCP), **SSO/SAML** + admin, custom SLA/DPA, dedicated onboarding |

**Credit rules that matter (top support/complaint area):**
- **Only successful runs charge** — a failed Flow consumes **zero** credits.
- Simple tasks (a rewrite, a chat reply) cost **~1–10 credits**; full end-to-end **Flows cost ~10–150
  credits** depending on complexity.
- Over **MCP**: **reading knowledge/brand profiles is free**; **running agent sessions consumes credits.**
- Credits **pool at the workspace level** (no per-seat pricing); Pro credits **roll over**.

**Security/compliance:** SOC 2 Type II, ISO 27001, HIPAA, GDPR; **data is never used for model training**;
per-seat scoping and per-project isolation; instant access revocation.

## Integrations

Juma reads from and writes to marketing/productivity tools; the flow direction depends on the connector:

- **Knowledge/assets (read):** Google Drive, Notion, SharePoint, OneDrive — pull briefs, assets, strategy
  docs into Projects.
- **Marketing data & execution (read/execute):** Google Analytics, Google Ads (incl. Keyword Planner),
  Meta/Facebook Ads, LinkedIn (Ads), Google Search Console, Ahrefs, HubSpot, Slack, Asana, Webflow.
- **Automation:** **n8n** for building custom workflow automations ("thousands of custom automation
  workflows").
- **Programmatic:** the **MCP server** (`mcp.juma.ai`) — see `references/juma-api-reference.md`. There is
  **no documented REST API, no webhooks, and no Zapier/Make** surface; MCP is the automation path.

## Data model

Juma exposes objects through MCP tools rather than a REST schema. The practical objects:

**Brand profile** (via `get_brand` / `create_brand_profile`):
```json
{
  "id": "brand_abc123",
  "name": "Acme B2B",
  "colors": ["#0A2540", "#635BFF"],
  "fonts": ["Inter", "Source Serif"],
  "voice": "confident, plain-spoken, no hype",
  "assets": ["logo_primary.svg", "logo_mark.png"]
}
```
<!-- Constructed from documented tool fields — verify against live MCP responses -->

**Project + knowledge item** (via `create_project` / `add_knowledge_item` / `search_knowledge_items`):
```json
{
  "project": { "id": "proj_9f2", "name": "Q3 Persona Research", "brand_id": "brand_abc123" },
  "knowledge_item": {
    "id": "know_51a",
    "type": "text",
    "title": "ICP notes — SMB founders",
    "content": "Solo founders, 1–10 employees, buy tools that save a weekend of work..."
  }
}
```
<!-- Constructed from documented tool fields — verify against live MCP responses -->

**Thread** (via `create_thread` / `reply_in_thread` / `read_conversation`):
```json
{
  "thread_id": "thr_77c",
  "project_id": "proj_9f2",
  "model": "claude",
  "messages": [
    { "role": "user", "content": "Generate a buyer persona for a solo-founder analytics tool" },
    { "role": "assistant", "content": "..." }
  ]
}
```
<!-- Constructed from documented tool fields — verify against live MCP responses -->

## Quick-start recipes

### Recipe 1 — Connect the MCP server and generate an on-brand persona from Claude Code
Trigger: you want to drive Juma's persona/content tools from your terminal.

```bash
# 1) Add the Juma MCP server (HTTP transport, OAuth — no API keys)
claude mcp add --transport http juma "https://mcp.juma.ai/mcp"

# 2) In Claude Code, authenticate:
#    run /mcp, then complete the Juma OAuth sign-in in your browser.
#    If you lack access, open https://juma.ai/mcp/connect first.
```
Then, in Claude Code, ask it to use the Juma tools in sequence:
1. `list_projects` (or `create_project`) → pick/create "Q3 Persona Research"
2. `import_brand_profile_from_url` → build a brand profile from your website, then `assign_brand_to_project`
3. `add_knowledge_item` → drop in ICP notes / customer quotes (this **read/add** step is cheap)
4. `write_content` → generate the persona using the project's brand + knowledge as context

Gotcha: **reading** knowledge/brand is free; the **`write_content` agent run consumes credits**. A failed
run charges nothing.

### Recipe 2 — Run a GEO/SEO audit and turn it into a report over MCP
Trigger: you want to know if your site is citable by AI answer engines and produce a shareable report.

From Claude Code (after connecting the MCP server):
1. `run_geo_audit` (or `check_geo_visibility`) on your domain → citability/visibility signals
2. `research_keywords` + `find_organic_competitors` → context
3. `create_report` → structured PDF you can hand to a client

Gotcha: audits/keyword/competitor tools are **MCP-accessible**; there's no REST endpoint to hit directly.

### Recipe 3 — Persist brand context so chats stop "forgetting"
Trigger: long chats lose brand voice and you keep re-pasting context.

1. `create_project` → one project per brand/client
2. `add_knowledge_item` / (UI) upload brand guidelines, tone-of-voice docs, examples
3. `import_brand_profile_from_url` → `assign_brand_to_project`

Now every `create_thread` / `reply_in_thread` in that project starts with brand context loaded — no
re-pasting, and it's reachable over MCP as knowledge.

Gotcha: **uploading files as knowledge is UI-only**; adding text notes (`add_knowledge_item`) works over MCP.

## Integration patterns

- **MCP-as-API:** treat the MCP server as your integration surface. Sequence tools (project → brand →
  knowledge → content) and remember the **cost boundary**: reads (knowledge/brand) are free, agent runs
  (content/campaigns/audits) burn credits, and failed runs refund automatically.
- **Long tasks:** the MCP connection waits ~30 seconds; longer Flows continue in the **background** with
  automatic agent check-ins. Don't treat a non-immediate return as a failure — poll for the result.
- **Web-app-only actions:** three things never work over MCP — **uploading files as knowledge, editing an
  existing image, and workspace administration**. Design flows so those steps happen in the UI.
- **No webhooks:** there is no event/webhook surface. If you need "on completion" behavior, drive the run
  from your own MCP client and act on the returned result, or use **n8n** for scheduled/triggered
  automations against connected apps.
- **Persona = hypothesis:** whatever you generate (persona, positioning, content) is an AI artifact. Keep
  the structured parts to sharpen messaging; validate the audience with a real demand test
  (`/sales-idea-validation`, `/sales-funnel`).
