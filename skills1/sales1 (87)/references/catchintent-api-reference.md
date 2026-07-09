<!-- Sources: https://catchintent.com/changelog/ , https://catchintent.com/pricing/ , https://catchintent.com/blog/introducing-the-intent-layer/ , https://www.pulsemcp.com/servers/catchintent — re-verified 2026-06-13 -->

# CatchIntent API & Integration Reference

> **2026-06-13 re-verification.** CatchIntent is now **LinkedIn-only** (Reddit/HN/Bluesky sunset v3.0.0 2026-05-13; X/Twitter sunset v3.1.0 2026-05-25). The original `catchintent.com/docs/getting-started/` path now 404s. The authoritative public sources are the changelog, the pricing page, and the PulseMCP/Stork MCP listings.

## No Traditional REST API

CatchIntent does not expose a traditional REST API with documented endpoints. Programmatic access is provided through:

1. **MCP Server** (primary) — OAuth-based, **27 typed tools** (leads, agents, outreach, workspace), at `https://engine.catchintent.com/mcp`, compatible with Claude, Cursor, Codex, and MCP-compatible tools. On all plans.
2. **Native CRM push** — **HubSpot live** (v1.7.0); Pipedrive, Close, Zoho listed as coming soon.
3. **Alert channels** — Email, Slack, Discord, Telegram (with temperature + interactive buttons).

<!-- UNVERIFIED: outbound webhooks to arbitrary endpoints (previously listed as a Pro+ feature) are NOT confirmed in the current changelog/docs/pricing. The CRM connectors Lemlist/Instantly/Apollo are also no longer listed. Retained below under their original headings but flagged. -->

## MCP Server

**Endpoint**: `https://engine.catchintent.com/mcp` (Streamable HTTP transport)

**Authentication**: OAuth flow (initiated on connect, no API key required) — "one command, one authorization, done"

**Tools**: **27 typed tools** spanning **leads, agents, outreach, and workspace** (changelog v2.5.0, 2026-03-30)

**Compatible clients**: Claude, Cursor, Codex, any MCP-compatible client supporting remote Streamable HTTP

**Plan availability**: All plans, no add-on, no separate pricing (Growth, Scale, Enterprise)

**Workspaces**: multi-brand, OAuth-scoped, isolated agents and leads per brand

**Setup**:
1. Add the CatchIntent MCP server (`https://engine.catchintent.com/mcp`) to your MCP client configuration
2. Complete the OAuth flow in browser when prompted
3. Query naturally — no endpoint construction needed

<!-- The GitHub org https://github.com/CatchIntent / a /skills repo were referenced in the earlier capture but not re-confirmed at re-verification — treat as unverified. -->

## Webhooks (UNVERIFIED — not confirmed in current docs)

> **2026-06-13:** Outbound webhooks to a custom endpoint are NOT documented in the current changelog, pricing page, or product copy, which describe alert delivery only via Email, Slack, Discord, and Telegram. The schema below was constructed from the older social-listening signal model and may not reflect any current capability. Do not rely on webhooks without confirming directly with CatchIntent.

**Trigger**: New signal captured by a listener

**Delivery**: HTTP POST to configured endpoint URL

**Payload schema**: Not formally documented. Based on the signal data model, expect:
<!-- Constructed from docs — verify against live API -->
```json
{
  "event": "signal.created",
  "signal": {
    "signal_id": "sig_abc123",
    "platform": "reddit",
    "source_url": "https://reddit.com/r/...",
    "content": "...",
    "relevance_score": 87,
    "intent_type": "buying",
    "surfacing_rationale": "...",
    "author": { "username": "...", "platform_profile_url": "..." },
    "enrichment": {
      "email": "...",
      "linkedin_url": "...",
      "company": "...",
      "icp_score": 82,
      "warmth_score": "high"
    },
    "listener_id": "lst_xyz789",
    "created_at": "2026-05-06T14:30:00Z"
  }
}
```

**Configuration**: Set webhook URL in Settings > Integrations > Webhooks

**Retry behavior**: Unknown — test and monitor for delivery reliability

## Native CRM Integrations

*Re-verified 2026-06-13. Current pricing lists "CRM push" on all tiers. Only HubSpot is confirmed live.*

| CRM/Tool | Integration type | Status |
|---|---|---|
| HubSpot | Push leads | Live (changelog v1.7.0, 2026-02-04) — creates contacts with signal context |
| Pipedrive | Push leads | Coming soon (pending as of v3.1.0) |
| Close | Push leads | Coming soon (pending as of v3.1.0) |
| Zoho | Push leads | Coming soon (pending as of v3.1.0) |

<!-- UNVERIFIED / HISTORICAL: Lemlist (push to sequences), Instantly (push to campaigns), and Apollo (push leads) were listed in the earlier capture but are not corroborated in current materials. -->

CRM push is a manual/one-click action from the dashboard, not a continuous auto-sync. The MCP server (27 tools) is the primary path for automated lead/outreach workflows.

## Gaps (as of 2026-06-13 re-verification)

- No REST API endpoint documentation exists; MCP is the programmatic surface.
- The 27 MCP tool names, parameters, and response schemas are not enumerated in public docs (only the four categories — leads, agents, outreach, workspace — are named).
- Outbound webhooks are not confirmed as a current feature (see Webhooks section) — alert delivery is documented only via Email/Slack/Discord/Telegram.
- Rate limits, pagination, and error-response schemas not documented.
- Exact Growth/Scale dollar prices are not shown publicly (trial/demo gated).
- Pipedrive/Close/Zoho CRM connectors are announced but unconfirmed as shipped.
- The signal/listener JSON shapes in platform-guide.md predate the LinkedIn-only pivot and reflect the older multi-platform schema.
