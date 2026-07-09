# Buzzabout Platform Reference

## Overview

Buzzabout is an AI-powered social media intelligence platform that analyzes billions of conversations across Reddit, TikTok, YouTube, Instagram, LinkedIn, and X to produce audience insights, sentiment analysis, trend tracking, and competitive intelligence. Target audience: marketers, product teams, and founders who need to understand what audiences actually think and feel about topics — not just mention counts. Primary differentiator: AI-first analysis that surfaces motivations and reasoning behind conversations, plus synthetic audience segmentation.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| **Multi-platform research** | Analyze conversations across Reddit, TikTok, YouTube, Instagram, LinkedIn, X | UI (all plans) |
| **Profile analysis** | Analyze specific social profiles by direct URL | UI (all plans) |
| **Sentiment analysis** | AI-powered sentiment that goes beyond pos/neg to understand motivations | UI (all plans) |
| **Trend & narrative tracking** | Identify emerging narratives and track topic shifts over time | UI (all plans) |
| **Synthetic audience segmentation** | AI-generated audience segments for personalized messaging | UI (all plans) |
| **Competitive research** | Reverse-engineer competitor strategies from social conversations | UI (all plans) |
| **AI Chat interface** | Conversational data exploration — ask follow-up questions about analyzed data | UI (all plans) |
| **Chart builder** | Create and share visualizations within the platform | UI (all plans) |
| **Language localization** | Filter results by language preference | UI (all plans) |
| **Alerts (Slack / email / webhook)** | Tracking-agent alerts delivered to Slack, email, or a webhook URL; daily & weekly digests | UI/Webhook (all plans) |
| **MCP server** | Native MCP (`https://mcp.buzzabout.ai/mcp/`) for Claude, ChatGPT, Cursor, Claude Code, Codex, custom agents; 15 read-only + ask tools | MCP (Pro+) |
| **REST API** | Public REST API at `https://api.buzzabout.ai/v1` (datasets, runs, mentions, audience datasets/profiles, tracking agents, pattern detections, custom parameters, ask/chats) | API (Business+) |
| **Custom data sources** | Add proprietary or custom data sources to analysis | Enterprise only |

## Pricing, limits & plan gates

*Verified against buzzabout.ai/pricing on 2026-06-13. Pricing is now per-seat with a monthly **credit** allowance (not the older "Research Hours" model).*

| Feature | Starter ($50/mo, $40/mo yearly) | Pro ($150/mo, $100/mo yearly) | Business ($350/mo, $250/mo yearly) | Enterprise (custom) |
|---|---|---|---|---|
| Credits / month | 2,000 | 10,000 | 50,000 | Custom volume |
| Mentions per research | 300 | 1,000 | 1,000 | 10,000+ |
| Overage rate | $0.025 / credit | $0.02 / credit | $0.015 / credit | Custom |
| Seats | 1 | 5 | Unlimited | Unlimited |
| AI Assistant / narrative tracking | Yes | Yes | Yes | Yes |
| Parallel researches | Yes | Yes | Yes | Yes |
| Custom date range / audience analysis | Yes | Yes | Yes | Yes |
| Webhooks (alerts) | Yes | Yes | Yes | Yes |
| MCP connectors | No | Yes | Yes | Yes (custom sources & agents) |
| REST API access | No | No | Yes | Yes |
| Custom data sources | No | No | No | Yes |
| Premium support | No | No | No | Dedicated CSM + Slack channel |

**Billing options**: Monthly or yearly (yearly shown as the discounted per-month rate). Credits are consumed per analysis.

**Free trial**: 500 credits to spend over 3 days, no payment required upfront.

**Credit system**: Credits are consumed per analysis; each plan also caps the **number of mentions analyzed per research**. Broader queries and longer date ranges consume more credits. Exact per-query consumption is not publicly documented — monitor usage in-dashboard. The API and chargeable operations return HTTP `402 insufficient_credits` when the balance is too low.

**Plan gates that matter**: MCP connectors unlock at **Pro**; the **REST API unlocks at Business** (Starter and Pro have no programmatic API access — only webhook alerts and, on Pro, the MCP server). Custom data sources are Enterprise-only.

## Integrations

| Integration | Direction | Plans | Notes |
|---|---|---|---|
| **Slack alerts** | Buzzabout → Slack (push alerts) | All | Tracking-agent alerts to Slack; daily & weekly digests |
| **Email alerts** | Buzzabout → email | All | Tracking-agent alerts to email; daily & weekly digests |
| **Webhooks** | Buzzabout → your endpoint (push) | All | Tracking-agent alerts to a webhook URL; payload schema and signature verification not publicly documented |
| **MCP server** | Bidirectional (read + ask) | Pro+ | `https://mcp.buzzabout.ai/mcp/` — OAuth for Claude Desktop/Claude.ai/ChatGPT, `x-api-key` for Claude Code/Codex/Cursor/custom agents; 15 tools (read-only lookups + ask→get_message→render), no create/update/delete |
| **REST API** | Bidirectional | Business+ | `https://api.buzzabout.ai/v1`, `x-api-key: bz_live_...` auth |
| **Custom data sources / agents** | Varies | Enterprise only | Via API and managed service |

**Automation for Starter/Pro (no REST API)**: route tracking-agent alerts to a webhook URL (e.g. a Zapier "Catch Hook") to pipe alerts into any connected app. Common pattern: Buzzabout alert → webhook → OpenAI (generate content ideas) → Slack channel. On **Pro**, the MCP server also lets Claude/ChatGPT/Cursor read datasets, mentions, and audience profiles directly. Programmatic create/run/query requires the **REST API on Business+**.

## REST API (Business+)

*Verified against docs.buzzabout.ai on 2026-06-13.*

- **Base URL**: `https://api.buzzabout.ai` — all endpoints live under `/v1`.
- **Auth**: API-key header `x-api-key: bz_live_...` (generate in the web app under Settings → API keys). Not Bearer.
- **Content type**: JSON in, JSON out. Send `Content-Type: application/json` on any request with a body.
- **Plan gate**: API access starts on the **Business** plan. (You can create a key on lower tiers to run quickstart walkthroughs, but the API-access feature is gated to Business+ on the pricing page.)
- **Response envelope** (discriminated on a top-level `status`):
  - Success (single): `{"status":"success","data":{...}}`
  - Success (paginated): `{"status":"success","data":[...],"has_next":true,"cursor":"..."}`
  - Error: `{"status":"client_error","error_code":"...","detail":"...","transient":false}`
  - `status` maps HTTP classes: 2xx→success, 4xx→client_error, 5xx→server_error.
- **Pagination**: cursor-based — `limit` (default 10–25 by resource, max 100), `cursor` (opaque base64url), `order` (`asc`|`desc`); responses carry `has_next` and `cursor`.
- **Rate limit**: **5 requests/second per API key**, shared across REST (`/v1/...`) and MCP (`/mcp/...`). Headers `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` on every authenticated request. A `429` returns `transient: true` plus `retry_after_seconds` (and a `Retry-After` header); use exponential backoff with jitter. Higher sustained rates require Enterprise (contact support).
- **Credit pre-check**: chargeable operations return `402 insufficient_credits` (with required vs. available credits) when the balance is too low.
- **Concurrency**: audience datasets allow only one in-flight run; a concurrent attempt returns `409 audience_dataset_run_already_in_flight`.
- **Account scoping**: datasets, mentions, audience datasets/profiles, tracking agents, pattern detections, and custom parameters are shared across every key on the account; chats are user-owned.

### Endpoint groups (under `/v1`)
Datasets · Tracking agents · Audience datasets · Mentions · Audience profiles · Pattern detections · Custom parameters · Ask + chats · Account/pricing (`me`).

Concrete paths verified from the quickstart:

```
POST /v1/datasets                                  # create a dataset (research project)
POST /v1/datasets/{dataset_id}/runs                # trigger a run
GET  /v1/datasets/{dataset_id}/runs/{run_id}       # poll run status
POST /v1/mentions                                   # list mentions (JSON body, e.g. topic + platforms)
```

```python
import os, httpx
client = httpx.Client(
    base_url="https://api.buzzabout.ai",
    headers={"x-api-key": os.environ["BUZZABOUT_KEY"]},
    timeout=30.0,
)
```

## MCP server (Pro+)

- **Endpoint**: `https://mcp.buzzabout.ai/mcp/` (trailing slash required).
- **Auth**: OAuth for Claude Desktop / Claude.ai / ChatGPT (just sign in); `x-api-key` for Claude Code / Codex / Cursor / custom agents.
- **Tools**: 15 total — read-only lookups (list/fetch datasets, runs, mentions, audience profiles, tracking agents) plus an assistant flow `ask → get_message → render`. **No create/update/delete** — mutations require the REST API.
- **Claude Code wiring**:

```bash
claude mcp add --transport http buzzabout \
  https://mcp.buzzabout.ai/mcp/ \
  --header "x-api-key: bz_live_..."
```

## Quick-start recipes

### Recipe 1: Daily trending topic alerts to Slack via webhook

**Trigger**: Buzzabout tracking-agent alert (daily digest) → webhook
**Steps**:
1. In Buzzabout, create a tracking agent for your niche (e.g., "AI writing tools")
2. Set a daily alert/digest schedule
3. Create a Zapier Zap with trigger "Webhooks by Zapier" → "Catch Hook"
4. Copy the Zapier webhook URL
5. In Buzzabout, add the webhook URL as the alert destination (or send the alert straight to Slack via the native Slack alert)
6. Add a Zapier action: "Slack" → "Send Channel Message"
7. Map the alert content to the Slack message body

**Gotcha**: The webhook payload format is not publicly documented. Test with a sample alert first to map fields in Zapier. Note Slack and email are native alert destinations, so for a simple Slack alert you may not need Zapier at all.

### Recipe 2: Competitive narrative analysis

**Steps**:
1. Create separate research topics for your brand and each competitor
2. Set identical date ranges and platform filters
3. Compare sentiment breakdowns — where are competitors perceived more positively?
4. Use the AI Chat to ask: "What unmet needs do users express about [competitor]?"
5. Export charts for stakeholder reports

**Gotcha**: Each research consumes credits independently, and each plan caps the number of mentions analyzed per research (300 on Starter, 1,000 on Pro/Business). Running 4 competitor analyses at once burns credits proportionally to data volume.

### Recipe 3: Idea validation via Reddit conversation analysis

**Steps**:
1. Create a research topic with your product category keywords
2. Filter to Reddit only (strongest data source)
3. Set date range to last 90 days
4. Review pain points and unmet needs in the AI analysis
5. Use synthetic audience segments to identify which user groups have the strongest demand signals
6. Use AI Chat to drill into specific pain points: "Show me what solo founders say about [problem]"

**Gotcha**: Synthetic audiences are derived from conversation patterns — they represent discussion participants, not verified buyer personas. Cross-reference with actual customer data.

## Integration patterns

### Webhook alert pattern (all plans)

Tracking agents can deliver alerts to Slack, email, or a webhook URL on daily/weekly digests. This is the automation surface for Starter (and a complement to MCP on Pro). Point the alert at a webhook (e.g. a Zapier "Catch Hook") to fan out into downstream tools.

**Setup**:
1. Create a tracking agent for your topic
2. Add a webhook URL (e.g. Zapier "Webhooks by Zapier" → Catch Hook) as the alert destination
3. Test by triggering the agent
4. Map payload fields to downstream actions

**Limitations**:
- Push-only (Buzzabout → your endpoint), no pull/query capability
- Payload schema and signature verification are **not publicly documented** — inspect a test payload
- Tied to the alert/digest schedule, not real-time event streaming

### MCP pattern (Pro+)

Connect `https://mcp.buzzabout.ai/mcp/` so Claude/ChatGPT/Cursor can read datasets, mentions, and audience profiles and run the `ask` flow directly. Read-only plus `ask` — no mutations. Best for exploratory analysis from an AI assistant without writing API code.

### REST API pattern (Business+)

Programmatic create/run/query at `https://api.buzzabout.ai/v1` with `x-api-key` auth. Typical flow: `POST /v1/datasets` → `POST /v1/datasets/{id}/runs` → poll `GET /v1/datasets/{id}/runs/{run_id}` → `POST /v1/mentions` to pull results. Respect the 5 req/s per-key limit and handle `402 insufficient_credits` and `429` (with `retry_after_seconds`).
