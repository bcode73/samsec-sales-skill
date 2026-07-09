# Xpoz Platform Reference

## Overview

Xpoz is a social data API and MCP server that gives AI agents and developers access to 1.5B+ indexed posts across Twitter/X, Instagram, TikTok, and Reddit. Primary differentiator: natural language queries via MCP protocol — no per-platform (Twitter/Instagram/etc.) API keys needed. Connect via Google OAuth (Claude Desktop, Cursor, Windsurf, ChatGPT) or via an Xpoz API key + Bearer header for agents that don't support OAuth (Claude Code, Gemini CLI, n8n). Targets developers, researchers, and GTM teams who want programmatic social data without enterprise pricing. Billed by credits (per query, by platform).

## Capabilities & automation surface

| Capability | Access method | Notes |
|---|---|---|
| Twitter/X search (posts, users, engagement) | MCP (14 tools) + SDK | Full coverage: keyword search, user profiles, comments, retweets, quotes |
| Instagram search (posts, users, comments) | MCP (9 tools) + SDK | Posts, user profiles, connections, comments, interacting users |
| Reddit search (posts, comments, users, subreddits) | MCP (9 tools) + SDK | Subreddit search + post/comment thread context preserved |
| TikTok search (posts, users, comments) | MCP (7 tools) + SDK | Fully available — search by keyword/user, comment threads |
| Tracked items (continuous monitoring) | MCP (3 tools) + SDK | `addTrackedItems`/`getTrackedItems`/`removeTrackedItems` — server auto-collects new posts matching tracked keywords/users |
| CSV export (tiered row caps) | MCP + SDK | Async operations with status polling; row cap per tier (Free 10K @ 500/file, Pro 50K/mo, Max 250K/mo) |
| Natural language queries | MCP only | AI optimizes queries automatically |
| Persistent monitoring | Tracked items + SDK (polling) | No webhooks — set up tracked items or poll for new data |
| User intelligence | MCP + SDK | Followers, engagement, authenticity scores |

## Pricing, limits & plan gates

Xpoz bills by **credits**, not result rows. Credits are charged **per query, by platform** — Reddit & Twitter cost **2 credits/query**, TikTok **5 credits/query**, Instagram **12 credits/query**. There is no charge for the number of rows a query returns (e.g. 100 Reddit queries = 200 credits regardless of rows).

| Plan | Price (month-to-month) | Price (annual) | Credits/month | Tracked items | CSV export rows |
|---|---|---|---|---|---|
| Free | $0 | $0 | 5,000 (one-time, does not refresh) | 1 | 10,000 (500/file) |
| Pro | $20/mo | $16/mo ($192/yr, 20% off) | 30,000 | 10 (+$5 each extra) | 50,000/mo (+$1/1k extra) |
| Max | $200/mo | $160/mo ($1,920/yr, 20% off) | 600,000 | 30 (+$2 each extra) | 250,000/mo (+$1/1k extra) |
| Enterprise | Custom | Custom | Custom | Unlimited | Custom |

The pricing page defaults to showing the annual-billed effective rate ($16 / $160); the page title and month-to-month toggle show $20 / $200.

**Feature gating:** Free includes **Core MCP Tools only**. **Premium Tools** and **Usage Analytics** (advanced analytics, sentiment, influence scoring) are gated to **Pro / Max / Enterprise**. Support response: Free = Community, Pro = 24h, Max = 12h, Enterprise = Dedicated SLA.

**Overage:** Pro continues at **+$0.80 per extra 1K credits**; Max at **+$0.40 per extra 1K credits**; Enterprise custom. **Free tier has a hard stop** when its one-time 5,000 credits run out — you must upgrade to continue.

**Rate limits:** Not publicly documented. The MCP server handles rate limiting server-side. SDK users should implement reasonable delays between requests.

## Integrations

| Integration | Direction | Notes |
|---|---|---|
| Claude Desktop/claude.ai | Read | MCP native (OAuth) — add as custom connector |
| Claude Code | Read | MCP via `claude mcp add --transport http` + `Authorization: Bearer <key>` header (no OAuth support) |
| Cursor / Windsurf / Cline | Read | MCP config (OAuth) |
| OpenAI Codex | Read | Via Xpoz MCP or SDK |
| ChatGPT | Read | Via MCP (OAuth) |
| Gemini CLI | Read | MCP via API key + Bearer header (no OAuth support) |
| n8n | Read | MCP via API key + Bearer header, or HTTP request nodes to SDK |
| Python pipelines | Read | `pip install xpoz` — typed client |
| TypeScript/Node | Read | `npm install @xpoz/xpoz` — typed client |

**No Zapier, Make, or native CRM connectors.** Build custom integrations via SDK.

## Data model

### Twitter post object

```json
{
  "id": "1234567890",
  "text": "Just tried the new feature and it's amazing!",
  "author": {
    "id": "987654321",
    "username": "techuser",
    "followers_count": 5200,
    "verified": false
  },
  "created_at": "2026-05-01T14:30:00Z",
  "metrics": {
    "likes": 42,
    "retweets": 8,
    "replies": 3,
    "quotes": 1
  },
  "language": "en",
  "hashtags": ["productlaunch", "saas"]
}
```
<!-- Constructed from docs — verify against live API -->

### Reddit post object

```json
{
  "id": "abc123",
  "title": "Looking for alternatives to X tool",
  "body": "I've been using X for 6 months but...",
  "subreddit": "SaaS",
  "author": "startup_founder",
  "created_at": "2026-05-02T09:15:00Z",
  "score": 87,
  "num_comments": 23,
  "url": "https://reddit.com/r/SaaS/comments/abc123"
}
```
<!-- Constructed from docs — verify against live API -->

## MCP tools inventory

### Twitter/X (14 tools)

| Tool | Purpose |
|---|---|
| `searchTwitterUsers` | Find users by name/bio keywords |
| `getTwitterUser` | Get profile details by username |
| `getTwitterUsersByKeywords` | Discover users matching topic keywords |
| `getTwitterUserConnections` | Get followers/following lists |
| `getTwitterPostsByKeywords` | Search posts by keyword with filters |
| `getTwitterPostsByAuthor` | Get posts from a specific user |
| `getTwitterPostsByIds` | Fetch specific posts by ID |
| `getTwitterPostComments` | Get replies to a post |
| `getTwitterPostRetweets` | Get retweet details |
| `getTwitterPostQuotes` | Get quote tweets |
| `getTwitterPostInteractingUsers` | Users who engaged with a post |
| `countTweets` | Count tweets matching criteria |
| `checkOperationStatus` | Poll async export status |
| `cancelOperation` | Cancel a running export |

### Instagram (9 tools)

`searchInstagramUsers`, `getInstagramUser`, `getInstagramUsersByKeywords`, `getInstagramUserConnections`, `getInstagramPostsByKeywords`, `getInstagramPostsByUser`, `getInstagramPostsByIds`, `getInstagramPostInteractingUsers`, `getInstagramCommentsByPostId`.

### Reddit (9 tools)

`searchRedditUsers`, `getRedditUser`, `getRedditUsersByKeywords`, `getRedditPostsByKeywords`, `getRedditPostWithCommentsById`, `getRedditCommentsByKeywords`, `searchRedditSubreddits`, `getRedditSubredditWithPostsByName`, `getRedditSubredditsByKeywords`. Subreddit-level search/retrieval is supported.

### TikTok (7 tools — fully available)

`searchTiktokUsers`, `getTiktokUser`, `getTiktokUsersByKeywords`, `getTiktokPostsByKeywords`, `getTiktokPostsByUser`, `getTiktokPostsByIds`, `getTiktokCommentsByPostId`. TikTok is live, not "coming soon."

### Tracking & monitoring (3 tools)

`addTrackedItems`, `getTrackedItems`, `removeTrackedItems` — register keywords/users for continuous server-side collection of new matching posts (subject to your tier's tracked-item cap). This is the closest thing to push monitoring, but you still read results by querying the MCP tools (no webhooks).

## Quick-start recipes

### Recipe 1: Monitor brand mentions on Twitter (Python SDK)

**Trigger:** Cron job every hour
**Steps:** Search for brand keywords → filter by engagement → send to Slack

```python
# pip install xpoz requests
import os
from xpoz import XpozClient
import requests

client = XpozClient(api_key=os.environ["XPOZ_API_KEY"])

# Search for mentions
results = client.twitter.search_posts(
    keywords="YourBrand OR @yourbrand",
    limit=50,
    sort_by="recent"
)

# Filter high-engagement mentions
important = [p for p in results.data if p.metrics.likes > 5]

# Send to Slack
for post in important:
    requests.post(os.environ["SLACK_WEBHOOK"], json={
        "text": f"New mention by @{post.author.username}: {post.text[:200]}"
    })
```
<!-- Constructed from docs — verify against live API -->

**Gotchas:** No webhooks — you must poll (or register tracked items for server-side collection). Credits are charged **per query by platform** (Twitter = 2 credits/query), not per row, so cache locally and batch keywords to reduce the number of queries you spend credits on.

### Recipe 2: Export competitor mentions to CSV (MCP)

**Trigger:** Monthly report generation
**Steps:** Ask Claude via MCP to export all mentions of competitors

```
Prompt to Claude (with Xpoz MCP connected):
"Export all Twitter posts mentioning 'CompetitorA' OR 'CompetitorB' from the
last 30 days to CSV. Include author, text, likes, retweets, and date."
```

Claude will use `getTwitterPostsByKeywords` with date filters, then trigger a CSV export via the async operation system. Poll `checkOperationStatus` until complete. Note CSV export row caps are per-tier (Free 10K @ 500/file, Pro 50K/mo, Max 250K/mo) — extra rows bill at $1/1k on paid tiers.

### Recipe 3: Reddit lead monitoring (TypeScript SDK)

```typescript
// npm install @xpoz/xpoz
import { XpozClient } from '@xpoz/xpoz';

const client = new XpozClient({ apiKey: process.env.XPOZ_API_KEY! });

async function findLeads() {
  const results = await client.reddit.searchPosts({
    keywords: '"looking for" OR "recommend" OR "alternative to"',
    subreddit: 'SaaS',
    limit: 100,
    sort_by: 'recent'
  });

  // Filter for purchase-intent posts
  const leads = results.data.filter(post =>
    post.score > 5 && post.num_comments > 3
  );

  console.log(`Found ${leads.length} potential leads`);
  return leads;
}
```
<!-- Constructed from docs — verify against live API -->

**Gotchas:** Reddit context is preserved (subreddit, thread), but you can't filter by specific subreddits in all query types — check which tool supports subreddit filtering.

## Integration patterns

### MCP connection setup

The remote MCP server is at `https://mcp.xpoz.ai/mcp` (Streamable HTTP transport). There are **two auth paths**:

**OAuth 2.1 (sign in with Google)** — for clients that support OAuth (Claude Desktop, Cursor, Windsurf, ChatGPT). Auth happens via a Google login popup on first connection; no API key to manage.

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

**API key (Bearer header)** — **required** for agents that don't support OAuth, such as **Claude Code, Gemini CLI, and n8n**. Get your key from your account settings at `xpoz.ai/settings`, then:

```bash
# Run from your system terminal, NOT inside the agent CLI
claude mcp add --transport http --scope user xpoz \
  https://mcp.xpoz.ai/mcp \
  --header "Authorization: Bearer <your Xpoz API token>"
```

### SDK authentication

```bash
# Get your API key in your account settings at xpoz.ai/settings (free, no CC)
export XPOZ_API_KEY=your-api-key

# Python
pip install xpoz

# TypeScript
npm install @xpoz/xpoz
```

### Pagination pattern

Results use server-side pagination. For MCP, the server handles pagination automatically when you request large result sets. For SDKs:

```python
# SDK pagination (conceptual)
results = client.twitter.search_posts(keywords="brand", limit=100)
# Server returns paginated results in results.data
# Use limit parameter to control page size
```
<!-- Constructed from docs ��� verify against live API -->

### Async export pattern

```python
# Start export
operation = client.export.create(
    platform="twitter",
    keywords="brand",
    format="csv",
    limit=250000  # cap is per-tier: Free 10K, Pro 50K/mo, Max 250K/mo
)

# Poll for completion
import time
while True:
    status = client.operations.check(operation.id)
    if status.state == "completed":
        download_url = status.result_url
        break
    time.sleep(10)
```
<!-- Constructed from docs — verify against live API -->

### Caching strategy

Xpoz has smart caching built in. To bypass cache for fresh data:
- MCP: include "get the latest data" or "force refresh" in your prompt
- SDK: pass `forceLatest: true` parameter

Cache results locally between polling intervals — Xpoz bills per query (by platform), so fewer repeated queries means fewer credits spent.
