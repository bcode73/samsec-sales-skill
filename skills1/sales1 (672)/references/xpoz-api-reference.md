<!-- Source: https://github.com/xpozpublic/xpoz-mcp, https://www.xpoz.ai/social-data-api/, https://www.xpoz.ai/social-listening-api/ -->

# Xpoz API Reference

## Access methods

Xpoz exposes social data through three interfaces:

1. **MCP Server** (primary) — remote Model Context Protocol server at `https://mcp.xpoz.ai/mcp`
2. **TypeScript SDK** — `@xpoz/xpoz` on npm
3. **Python SDK** — `xpoz` on PyPI

There is no traditional REST API with documented HTTP endpoints. The MCP server IS the API — clients connect via streamable HTTP and call tools by name.

## Authentication

### MCP — OAuth 2.1 (Google)
- Used by clients that support OAuth: Claude Desktop, Cursor, Windsurf, ChatGPT
- Google login popup triggered on first connection; no API key to manage
- Single auth covers all platforms

### MCP — API key (Bearer header)
- **Required** for agents that do NOT support OAuth: **Claude Code, Gemini CLI, n8n**
- Get your key from your account settings at `xpoz.ai/settings`
- Pass it in the `Authorization: Bearer <key>` HTTP header

### SDK (API Key)
- Get your key from your account settings at `xpoz.ai/settings` (free, no credit card)
- Pass as environment variable `XPOZ_API_KEY`
- Same key works for all platforms and tools

## MCP Server Configuration

OAuth clients (Claude Desktop, Cursor, Windsurf, ChatGPT):

```json
{
  "mcpServers": {
    "xpoz": {
      "type": "streamable-http",
      "url": "https://mcp.xpoz.ai/mcp"
    }
  }
}
```

Claude Code / Gemini CLI / n8n (API key required — run from your system terminal, not inside the agent CLI):

```bash
claude mcp add --transport http --scope user xpoz \
  https://mcp.xpoz.ai/mcp \
  --header "Authorization: Bearer <your Xpoz API token>"
```

Compatible with: Claude Desktop, Claude Code, Cursor, Windsurf, Cline, OpenAI Codex, ChatGPT, Gemini CLI.

## Tools (MCP endpoints)

### Twitter/X — 14 tools

| Tool | Description | Key parameters |
|---|---|---|
| `searchTwitterUsers` | Search users by name/bio | keywords, limit |
| `getTwitterUser` | Get user profile | username |
| `getTwitterUsersByKeywords` | Find users by topic | keywords, limit |
| `getTwitterUserConnections` | Followers/following | username, type |
| `getTwitterPostsByKeywords` | Search posts | keywords, limit, date_from, date_to |
| `getTwitterPostsByAuthor` | User's posts | username, limit |
| `getTwitterPostsByIds` | Fetch by ID | ids[] |
| `getTwitterPostComments` | Replies to post | post_id, limit |
| `getTwitterPostRetweets` | Retweet details | post_id, limit |
| `getTwitterPostQuotes` | Quote tweets | post_id, limit |
| `getTwitterPostInteractingUsers` | Engagers | post_id |
| `countTweets` | Count matching tweets | keywords, date_from, date_to |
| `checkOperationStatus` | Poll async ops | operation_id |
| `cancelOperation` | Cancel export | operation_id |

### Instagram — 9 tools

`searchInstagramUsers`, `getInstagramUser`, `getInstagramUsersByKeywords`, `getInstagramUserConnections`, `getInstagramPostsByKeywords`, `getInstagramPostsByUser`, `getInstagramPostsByIds`, `getInstagramPostInteractingUsers`, `getInstagramCommentsByPostId`.

### Reddit — 9 tools

`searchRedditUsers`, `getRedditUser`, `getRedditUsersByKeywords`, `getRedditPostsByKeywords`, `getRedditPostWithCommentsById`, `getRedditCommentsByKeywords`, `searchRedditSubreddits`, `getRedditSubredditWithPostsByName`, `getRedditSubredditsByKeywords`. Subreddit-level search and retrieval supported.

### TikTok — 7 tools (fully available)

`searchTiktokUsers`, `getTiktokUser`, `getTiktokUsersByKeywords`, `getTiktokPostsByKeywords`, `getTiktokPostsByUser`, `getTiktokPostsByIds`, `getTiktokCommentsByPostId`. Live — no longer "coming soon."

### Tracking & monitoring — 3 tools

`addTrackedItems`, `getTrackedItems`, `removeTrackedItems` — register keywords/users for continuous server-side collection of new matching posts (capped by tier's tracked-item limit). Pull-only: you still read results by querying the platform tools (no webhooks/push).

## Common parameters

| Parameter | Type | Description |
|---|---|---|
| `keywords` | string | Search terms (natural language or quoted phrases) |
| `limit` | number | Max results to return |
| `date_from` | string | Start date filter (ISO 8601) |
| `date_to` | string | End date filter (ISO 8601) |
| `forceLatest` | boolean | Bypass cache for fresh data |
| `sort_by` | string | Sort order (e.g., "recent", "engagement") |

## Pagination

Server-side pagination. For MCP, handled automatically. For SDKs, use the `limit` parameter — server returns paginated chunks. Exact cursor/offset mechanism not publicly documented.

## Rate limits

Not publicly documented. The MCP server handles rate limiting internally. SDK users should implement reasonable delays (1-2 seconds between requests recommended).

## Async operations (CSV export)

Large data exports run asynchronously:

1. Initiate export (returns `operation_id`)
2. Poll `checkOperationStatus` with the `operation_id`
3. When status is "completed", retrieve the result URL
4. Download CSV — row cap is **per tier**: Free 10,000 (500 rows/file), Pro 50,000/mo, Max 250,000/mo, Enterprise custom. Extra rows bill at $1/1k on paid tiers.

Use `cancelOperation` to abort a running export.

## Error handling

Not publicly documented. Expected patterns:
- OAuth failures → re-authenticate
- Rate limit exceeded → back off and retry
- Invalid parameters → error message in response
- Operation timeout → cancel and retry with smaller scope

## SDKs

### TypeScript

```typescript
import { XpozClient } from '@xpoz/xpoz';

const client = new XpozClient({ apiKey: process.env.XPOZ_API_KEY });
await client.connect();

const results = await client.twitter.searchPosts({
  keywords: 'your brand',
  limit: 100
});

console.log(results.data.length);
await client.close();
```

### Python

```python
from xpoz import XpozClient

client = XpozClient(api_key=os.environ["XPOZ_API_KEY"])
results = client.twitter.search_posts(keywords="your brand", limit=100)
print(len(results.data))
```

## Gaps

- No publicly documented REST API endpoints (HTTP method + path format)
- Rate limit numbers not published
- Pagination cursor/offset mechanism not documented
- Error response schema not documented
- Webhook/push notifications: none — pull only (use `addTrackedItems` for continuous server-side collection, but reads are still via tool queries)
- Per-tool parameter schemas for Instagram/Reddit/TikTok tools not individually documented (tool names confirmed; param lists not published)
- Credit cost is per query by platform (Reddit/Twitter 2, TikTok 5, Instagram 12); rows returned do not affect credit spend
