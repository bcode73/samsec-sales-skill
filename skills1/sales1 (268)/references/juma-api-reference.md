<!-- Source: https://juma.ai/mcp (captured 2026-07) -->

# Juma MCP Server Reference

Juma's programmatic surface is a **Model Context Protocol (MCP) server**, not a REST API. There is **no
documented public REST API, no webhooks, and no Zapier/Make** — everything below is how you automate Juma
(from Claude Code, Claude Desktop, ChatGPT, Cursor, or any MCP-compatible client).

## Connection

- **Server URL:** `https://mcp.juma.ai/mcp`
- **Transport:** HTTP (Streamable HTTP)
- **Authentication:** OAuth sign-in via browser — **no API keys required**. Access is included in your
  existing Juma seat; unlimited seats across all plans.
- **Initial setup:** if you lack access, visit `https://juma.ai/mcp/connect` first.

### Claude Code (terminal)
```bash
claude mcp add --transport http juma "https://mcp.juma.ai/mcp"
```
Then run `/mcp` inside Claude Code and complete the Juma OAuth sign-in in your browser.

### Claude Desktop / other MCP clients
Connect via **Streamable HTTP** to the server URL above and complete OAuth authentication when prompted.
No API keys.

### Supported clients
Claude Desktop · Claude Code · Claude Mobile (via a Desktop connection) · ChatGPT · Cursor · any
MCP-compatible tool (Windsurf, etc.).

## Credit consumption

- **Running agent sessions:** consume credits.
- **Reading knowledge / brand profiles:** **no credit cost.**
- Failed runs charge nothing (only successful runs consume credits).

## Task-completion window

The connection **waits ~30 seconds**; longer tasks continue in the **background** with automatic agent
check-ins rather than blocking the call. Poll for the completed result rather than assuming failure.

## Functions that remain in the Juma web app (NOT available over MCP)

1. Uploading files as knowledge
2. Editing existing images
3. Workspace administration

## Tool inventory (40+ tools by category)

*Captured 2026-07 from juma.ai/mcp — tool names/counts may change; verify with `/mcp` in your client.*

### Brand (7)
- `get_brand` — Retrieve colors, fonts, voice
- `list_brand_profiles` — View all workspace profiles
- `create_brand_profile` — Add new profile
- `update_brand_profile` — Modify existing profile
- `import_brand_profile_from_url` — Auto-build a profile from a website
- `add_brand_assets` — Attach logos/assets
- `assign_brand_to_project` — Apply a profile to a project

### Knowledge & Projects (8)
- `search_knowledge_items` — Semantic search across project knowledge
- `read_knowledge_items` — Access full content
- `list_knowledge_items` — Browse items
- `add_knowledge_item` — Add text notes
- `upload_knowledge_file` — Import files *(note: uploading files as knowledge is otherwise a web-app action)*
- `list_projects` — View team projects
- `create_project` — Start a new project
- `get_folder_contents` — Browse files/folders

### Content & Deliverables (7)
- `write_content` — On-brand copy
- `create_report` — Structured report / PDF
- `create_presentation` — Slide deck (PDF/PPTX)
- `create_web_page` — Responsive landing page
- `create_campaign` — Multi-asset campaign
- `generate_image` — On-brand imagery
- `analyze_data` — Charts and insights

### SEO / GEO (7)
- `run_geo_audit` — AI-answer citability report
- `check_geo_visibility` — Quick visibility score
- `research_keywords` — Volume and intent data
- `find_organic_competitors` — Domain competitors
- `analyze_page_seo` — Lighthouse audit
- `get_llm_top_cited_domains` — AI-engine citations
- `get_ai_search_volume` — AI search frequency

### Analytics & Integrations (2)
- `search_integration_tools` — Discover connected apps by capability
- `run_integration_tool` — Execute a connected app (Google Analytics, HubSpot, Slack, Asana, etc.)

### Conversations & History (6)
- `create_thread` — Start a conversation
- `reply_in_thread` — Continue with context
- `read_conversation` — Access past exchanges
- `search_chat_history` — Query previous work
- `web_search` — Open web search
- `web_scrape` — Extract webpage content

## Security & compliance

SOC 2 Type II · ISO 27001 · HIPAA · GDPR. Per-seat scoping, per-project isolation (for agencies), instant
access revocation, **no model training on user data**.

## Gaps / not documented

- **No REST API** — no base URL, endpoints, or API-key auth are published. The MCP server is the
  programmatic interface.
- **No webhooks / no event stream** — there is no "on completion" callback; drive runs from your MCP
  client and act on the returned result (or use n8n for scheduled/triggered automations against connected
  apps).
- **No Zapier / Make modules** documented.
- **Tool request/response JSON shapes** are not published; call each tool via your MCP client to inspect
  its schema. The shapes under "Data model" in `platform-guide.md` are constructed from documented field
  lists and must be verified against live MCP responses.
