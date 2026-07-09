# SyncGTM — Learnings

Accumulated, dated platform knowledge. Append new findings with a date stamp so staleness is auditable.

---

**2026-06-27**: Research baseline. Built from the marketing site (syncgtm.com), the docs (docs.syncgtm.com — intro + MCP server pages), and review/comparison content (vs Clay/Trigify/Common Room/Koala/Unify).

- **Category:** **AI-native GTM data engine** — one workspace for **buying signals + waterfall enrichment + AI lead scoring + AI research/writing + no-code Workflow Builder + outbound**. Positioned as signal-driven outbound at much lower cost than incumbents. Audience: Sales/RevOps/agencies/startups/**GTM Engineers** (Cloudflare/GitLab logos). Active (2026; MCP launch).
- **MCP server is the headline developer surface:** endpoint **`https://api.syncgtm.com/mcp`**, **OAuth browser sign-in (NO long-lived API token / Authorization header)** — first connect opens the browser to approve; client stores the session. **Free plan includes MCP access.** Works with Claude Code, Cursor, ChatGPT, Gemini CLI, Codex, Manus. Tools: enrich people/companies, find **verified emails + phones**, pull **LinkedIn data**, **read buying signals**. Tool catalog at `docs.syncgtm.com/mcp_server/tools`. Revoke per-client from the dashboard. (This is the most directly relevant feature for this repo's Claude-Code audience.)
- **REST API:** base **`api.syncgtm.com`**, **API key** (from in-app, docs `/core_concepts/api_key`) — distinct from MCP's OAuth. Per-endpoint paths/params/pagination/webhook-events live in the JS-rendered docs portal (not on marketing pages) — pull from `docs.syncgtm.com` when implementing.
- **Signals:** prospect + account level — job changes, promotions, headcount growth, funding rounds, product launches, LinkedIn posts (prospect + company), web-traffic shifts, tech-stack adoption, **custom AI signals**. Feed **AI lead scoring (0–100 vs ICP → HOT/WARM/COOL/COLD)** and **workflows**.
- **Enrichment:** **waterfall** across **40+ providers / 20+ databases** for verified work email + mobile + personal email; firmographics/techstack/revenue/headcount; AI research agents + web scrapers. **Credit-based** — scope to scored leads (credits estimator exists).
- **Integrations (40+):** HubSpot, Salesforce, Slack, Attio, email-sequencers, comms, **HTTP API webhooks**, custom API-key support for select providers; **browser extension** for LinkedIn.
- **Pricing:** **Free** (incl. MCP + core enrichment/agents/workflows) → **~$99/mo** (deeper enrichment, signal-driven outbound, CRM integrations) → Enterprise. 4.4/5 review verdict. Credit-based.
- **Competitive set:** Clay (flexible data/enrichment canvas), **Trigify** (LinkedIn-signal infra, from $40/mo), Common Room (community signals), Koala (intent + visitor ID), Unify (warm outbound), People Data Labs, Intentsify, Demandbase. SyncGTM's angle: **all-in-one signals→enrich→score→act + an MCP server**, cheap.

⚠️ **Fetch note for future runs:** marketing site fetches fine; the **docs portal is JS-rendered** (intro page readable, but per-endpoint REST pages need the in-app portal). The **MCP server docs are clear and verbatim-capturable via search**. Confirmed: MCP endpoint + OAuth + setup + tools, REST base `api.syncgtm.com` + API-key concept, signals catalog, integrations, pricing. Gaps: exact REST endpoint paths/JSON, webhook event catalog + signing.
