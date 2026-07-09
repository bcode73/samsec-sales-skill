# Bazzly API & MCP Reference

*Verified against the official bazzly.ai site and `/mcp` page on 2026-06-13. The
full request/response schema lives in Bazzly's public Postman collection (link
below); some fields below are best-effort because the Postman documenter renders
client-side and could not be fully scraped.*

## Capture note

Bazzly added a public REST API and an MCP server **after** the original 2026-05
skill baseline (which stated "no API, no webhooks, no MCP"). The API surface,
auth, and MCP details here come from the official `https://www.bazzly.ai/mcp`
page and homepage footer (API Docs / MCP links). Treat unconfirmed details (rate
limits, full endpoint list, response shapes) as UNVERIFIED until checked against
the live Postman docs.

## REST API

- **Base URL**: `https://api.bazzly.ai`
- **Auth**: `Authorization: Bearer bzly_live_...` **or** `X-Bazzly-Api-Key: <key>`
- **API keys**: generated in the Bazzly dashboard with selectable **scopes**:
  `read`, `write`, `top-ups`
- **Public docs**: https://documenter.getpostman.com/view/3358302/2sBXqKof1B
  (titled "Bazzly Public API — Reddit Marketing Automation")

### Endpoints

| Method | Path | Purpose | Scope |
|---|---|---|---|
| GET | `/public/v1/opportunities` | List discovered Reddit lead opportunities (supports filters such as top-ranked, sort, and limit) | `read` |
| POST | `/mcp` | MCP transport endpoint (streamable-HTTP) | — |

> The Postman collection exposes the same opportunity → reply → queue workflow as
> the MCP tools below; additional REST endpoints for generating and queueing
> replies are expected to mirror `generate_opportunity_reply` / `queue_reply` /
> `list_reply_queue` but the exact REST paths are **UNVERIFIED** (Postman docs are
> JS-rendered). Confirm in the live Postman collection before coding against them.

### Example request

```bash
curl https://api.bazzly.ai/public/v1/opportunities \
  -H "Authorization: Bearer bzly_live_..." \
  --get \
  --data-urlencode "filter=top-ranked" \
  --data-urlencode "sort=score" \
  --data-urlencode "limit=10"
```

### Rate limits

**Not documented** on the public pages — UNVERIFIED. Apply conservative client-side
throttling and exponential backoff.

### Webhooks

**None documented.** Egress is pull-based (poll `GET /public/v1/opportunities` or
the `list_opportunities` MCP tool). There is no push/webhook or Zapier path as of
2026-06-13.

## MCP server

- **Endpoint**: `https://api.bazzly.ai/mcp`
- **Transport**: streamable-HTTP
- **Auth**: `Authorization: Bearer bzly_live_...` (same keys/scopes as REST)

### Tools

| Tool | Purpose |
|---|---|
| `list_opportunities` | List lead opportunities (filters: top-ranked, sort options, limit) |
| `generate_opportunity_reply` | Draft a contextual reply/DM for an opportunity |
| `queue_reply` | Queue an approved reply for posting |
| `list_reply_queue` | Inspect the pending reply queue |

Typical workflow: `list_opportunities` → `generate_opportunity_reply` → `queue_reply`.
Bazzly also advertises scheduled searches (cron), automated comment/DM generation,
lead tracking, and performance reporting through the API.

### Claude Desktop config (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "bazzly": {
      "url": "https://api.bazzly.ai/mcp",
      "headers": {
        "Authorization": "Bearer bzly_live_..."
      }
    }
  }
}
```

### Cursor config (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "bazzly": {
      "url": "https://api.bazzly.ai/mcp",
      "headers": {
        "Authorization": "Bearer bzly_live_..."
      }
    }
  }
}
```

## Known gaps / UNVERIFIED

- Full REST endpoint list and response JSON shapes (Postman docs are
  client-rendered; only `GET /public/v1/opportunities` is confirmed by name).
- Rate limits (none published).
- Whether the `top-ups` scope corresponds to a billing/credit-purchase endpoint.
- Any HMAC signing or webhook events (none documented — assume polling only).
