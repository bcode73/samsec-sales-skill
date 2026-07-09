# ReddGrow Platform Reference

## Overview

ReddGrow is a Reddit marketing platform focused on AI search visibility (GEO — Generative Engine Optimization). It identifies Reddit threads that AI platforms (ChatGPT, Perplexity, Gemini, Claude, Grok) already cite in their answers, then helps brands add relevant comments to those threads. Target audience: SaaS companies and marketing teams seeking to appear in AI-generated recommendations. 200+ customers.

## Capabilities & automation surface

| Capability | Description | Surface |
|---|---|---|
| AI Visibility Scanning | Scans 220+ countries daily, queries 4+ AI platforms, tracks which Reddit sources get cited, daily visibility reports, geographic variations | UI + email reports |
| Subreddit discovery | AI finds 10-100 relevant subreddits automatically, continuous re-scoring as community relevance shifts | UI-only |
| AI comment drafting | Generates human-sounding, on-brand Reddit comments using product context and thread analysis | UI + Chrome Extension |
| Chrome Extension posting | Drafting overlay directly in Reddit UI, human review before posting (~30 seconds per approved comment) | Chrome Extension |
| Brand monitoring | Alerts for brand/competitor mentions on Reddit across specified domains | UI + email/Slack alerts |
| Karma warmup | Systematic account warmup from 0% to 50% promotional safely, 6-step compliance checklist | UI-only |
| Community management | Subreddit moderation with AI assistance, knowledge base integration for support responses | UI-only |
| Analytics | Engagement tracking, reach metrics, citation growth monitoring, share-of-voice | UI-only |
| Agent API | Reddit intelligence — 19 GET endpoints across Meta, Subreddits (10), Posts (4), Users (3), Domains (1) for AI agent workflows | API (REST, `/agent/*`) |
| AEO API | AI-visibility / answer-engine-optimization data — prompts, runs, visibility, citations, sources, brands, topics, scores (Pro plan only) | API (REST, `/v1/aeo/*`) |
| CLI | Terminal access to Reddit data via `@reddgrow/cli` npm package (also yarn/pnpm/bun); human + agent JSON output modes | CLI |

## Pricing, limits & plan gates

<!-- Verified against https://reddgrow.ai/pricing/ on 2026-06-13. Card prices below are the annual-billed effective monthly rate ("SAVE 20%" toggle); monthly billing is roughly 20% higher. NOTE: the page's prose/FAQ still show stale $59/$149/$299 and 10/100/200 prompts — the cards and the structured JSON-LD ("price":"79"/"159"/"319") are authoritative. -->

| Feature | Starter ($79/mo) | Growth ($159/mo) | Pro ($319/mo) | Agency / Enterprise |
|---|---|---|---|---|
| Annual billing | $948/yr | $1,908/yr | $3,828/yr | Agency from $1,000/mo |
| Reddit accounts | 1 | 3 | Unlimited | Unlimited |
| Monthly comments | 150 | 450 | 750 | Custom |
| AI Visibility prompts | 50 | 200 | 300 | Custom |
| Domains tracked | 1 | 3 | 5 | Custom |
| Subreddits monitored | 10 | 30 | 100 | Custom |
| Campaigns | 1 | 5 | 10 | Custom |
| AI Visibility | Yes | Yes | Yes | Yes |
| Chrome Extension | Yes | Yes | Yes | Yes |
| Brand Monitoring | Yes | Yes | Yes | Yes |
| Unlimited seats | Yes | Yes | Yes | Yes |
| Slack integration | No | Yes | Yes | Yes |
| Support | Community | Email | Priority | — |
| AEO API (`/v1/aeo/*`) | No | No | Yes | Yes |

- Card prices shown are **billed annually** ("SAVE 20%" vs monthly billing); monthly billing is ~20% higher.
- Campaign counts are inconsistent on the live page: the visible feature cards say Growth/Pro = 3 campaigns, but the structured data and plan-description prose say 5/10. The 1/5/10 figures (2 of 3 official sources) are used here.
- 14-day free trial on all plans; cancel anytime; no prorated refunds for partial months.
- Agent API access (`/agent/*`, credit-based) is available on all plans. The **AEO API (`/v1/aeo/*`) requires the Pro plan.**

**Rate limits (API):** 60 requests/minute, 1,000 requests/hour (enforced per API key, both windows independently). 429 returns `{"statusCode":429,"message":"Too many requests"}`. Credit usage headers `X-Credits-Used` / `X-Credits-Remaining` / `X-Credits-Limit` are returned on responses. Credit costs are tiered: 1 (lookups: about/rules/traffic/widgets/profile), 2 (posts/comments feeds), 3 (searches + check-url), 5 (wiki/duplicates/batch/domain mentions).

## Integrations

| Integration | Direction | Plan required | Details |
|---|---|---|---|
| Chrome Extension | Write | All | Post AI-drafted comments directly on Reddit |
| Slack | Push | Growth+ | Brand monitoring alerts and notifications |
| Email alerts | Push | All | Daily visibility reports, brand mention alerts |
| Agent API | Read | All | Reddit intelligence data (subreddits, posts, domains, users) — `/agent/*` |
| AEO API | Read | Pro+ | AI-visibility data — `/v1/aeo/*` (returns 402 below Pro) |
| CLI | Read | All | Terminal access via `@reddgrow/cli` |

No Zapier, Make, MCP server, webhooks, or native CRM integrations. Both APIs are read-only (GET-only); no push/webhook capability.

## Data model

### Subreddit search result (array element)

`GET /agent/subreddits/search` returns a JSON array. Each item uses `display_name` (not `name`) and has NO `relevance_score`:

```json
{
  "display_name": "SaaS",
  "subscribers": 125000,
  "public_description": "Discussion about SaaS businesses...",
  "over18": false,
  "subreddit_type": "public",
  "active_user_count": 847,
  "submission_type": "any",
  "restrict_posting": true,
  "link_flair_enabled": true
}
```

### Domain mention (array element)

`GET /agent/domains/{domain}/mentions` returns a flat JSON **array of post objects** (not an object with a `mentions` key):

```json
{
  "id": "abc123",
  "title": "Looking for a tool to automate...",
  "author": "some_user",
  "created_utc": 1704067200,
  "url": "https://example.com/blog/post",
  "permalink": "/r/SaaS/comments/abc123/...",
  "subreddit": "SaaS",
  "score": 42,
  "num_comments": 12,
  "domain": "example.com",
  "is_self": false
}
```

### User profile

`GET /agent/users/{username}` returns separate `link_karma`/`comment_karma` (no combined `karma`, no `post_history` — use `/users/{username}/posts`):

```json
{
  "id": "string",
  "name": "example_user",
  "created_utc": 1356998400,
  "link_karma": 5000,
  "comment_karma": 10230,
  "is_gold": false,
  "icon_img": "https://...",
  "subreddit": {"public_description": "..."}
}
```

## Quick-start recipes

### Recipe 1: Monitor your domain mentions on Reddit

**Trigger:** Scheduled (daily cron)
**Steps:** Call the domain mentions endpoint, filter for new mentions, send to Slack

```bash
# Check domain mentions — response is a flat array of post objects
curl -s -H "x-api-key: rg_your_key_here" \
  "https://api.reddgrow.ai/agent/domains/yourdomain.com/mentions?limit=100" \
  | jq '.[] | {subreddit, title, permalink}'
```

```python
import requests

API_KEY = "rg_your_key_here"
DOMAIN = "yourdomain.com"

resp = requests.get(
    f"https://api.reddgrow.ai/agent/domains/{DOMAIN}/mentions",
    params={"limit": 100},
    headers={"x-api-key": API_KEY}
)
posts = resp.json()  # flat array of post objects
for p in posts:
    print(f"r/{p['subreddit']}: {p['title']}")
    print(f"  https://reddit.com{p['permalink']}")
```

**Gotcha:** This endpoint costs 5 credits (heavy/batch tier) and `limit` maxes at 100. Rate limit is 60 req/min; one call per domain per day is sufficient for monitoring.

### Recipe 2: Find relevant subreddits for your product

**Trigger:** One-time setup or periodic review
**Steps:** Search for subreddits by keyword, review rules, add to monitoring

```bash
# Search subreddits by keyword (returns an array; field is display_name)
curl -s -H "x-api-key: rg_your_key_here" \
  "https://api.reddgrow.ai/agent/subreddits/search?q=project+management" \
  | jq '.[] | {display_name, subscribers, active_user_count}'

# Check a subreddit's posting rules before engaging
curl -s -H "x-api-key: rg_your_key_here" \
  "https://api.reddgrow.ai/agent/subreddits/SaaS/rules" \
  | jq '.'
```

```python
import requests

API_KEY = "rg_your_key_here"

# Search for relevant subreddits (3 credits per search)
resp = requests.get(
    "https://api.reddgrow.ai/agent/subreddits/search",
    params={"q": "project management"},
    headers={"x-api-key": API_KEY}
)
for sub in resp.json():
    print(f"r/{sub['display_name']} ({sub['subscribers']} subscribers)")

# Check rules before engaging
rules_resp = requests.get(
    "https://api.reddgrow.ai/agent/subreddits/SaaS/rules",
    headers={"x-api-key": API_KEY}
)
print(rules_resp.json())
```

**Gotcha:** Always check subreddit rules before adding to monitoring. Subreddits with strict no-promotion rules will get your comments removed.

### Recipe 3: Search Reddit posts by keyword (via CLI)

**Trigger:** Ad-hoc research or pipeline input
**Steps:** Install CLI, authenticate, search posts

```bash
# Install the CLI (npm/yarn/pnpm/bun all supported)
npm install -g @reddgrow/cli

# Authenticate (pass the key inline) and verify
reddgrow auth login rg_your_key_here
reddgrow auth whoami

# Search posts (alias for subreddits is `r`, users is `u`, domains is `d`)
reddgrow posts search "best CRM for startups"

# Check if a URL was already posted to a subreddit
reddgrow subreddits check-url SaaS "https://yourdomain.com/blog/crm-guide"

# Force raw JSON for piping into an agent pipeline
reddgrow posts search "best CRM" --mode agent
```

**Gotcha:** The CLI uses the same credit system as the API — searches and check-url cost 3 credits, feeds cost 2, domain mentions cost 5. Output auto-detects human vs agent JSON; force it with `--mode agent` / `--mode human`.

## Integration patterns

### AI agent workflow

ReddGrow's API is designed for AI agent consumption. Typical pattern:

1. **Discover** — `GET /agent/subreddits/search` to find relevant communities
2. **Monitor** — `GET /agent/domains/{domain}/mentions` to track brand mentions
3. **Research** — `GET /agent/subreddits/{name}/posts` to read post feeds
4. **Validate** — `GET /agent/subreddits/{name}/check-url` to check if content was already shared
5. **Enrich** — `GET /agent/users/{username}` to understand who's posting

Feed results into your AI agent for analysis, then use the Chrome extension for human-reviewed posting.

### GEO (Generative Engine Optimization) workflow

1. **Scan** — AI Visibility Scanning identifies Reddit posts that AI platforms cite
2. **Match** — Filter by relevance to your brand; benchmark against competitors
3. **Draft** — AI generates contextual comments based on your product context
4. **Post** — Human reviews and posts via Chrome extension (~30 seconds per comment)
5. **Track** — Monitor citation count and share-of-voice growth over time

**Key insight:** Focus on threads AI platforms *already* cite rather than creating new threads. Existing citations indicate the thread has retrieval authority.

**Programmatic GEO tracking (Pro plan):** The AEO API (`/v1/aeo/*`) exposes the AI-visibility data programmatically — `GET /v1/aeo/visibility/timeline`, `/visibility/by-brand`, `/visibility/by-engine`, `/citations`, `/sources/top-domains`, `/brands/ranking`, and `/runs/{scan_result_id}/explain` for score transparency. Use it to pull share-of-voice and citation data into a warehouse or dashboard instead of relying on the UI/email reports. Same `x-api-key` auth; returns 402 below Pro.
