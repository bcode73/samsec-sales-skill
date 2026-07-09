# ReplyAgent Platform Reference

## Overview

ReplyAgent.ai is a Reddit marketing automation platform that monitors subreddits for high-intent conversations, generates AI comments, and posts them using professionally managed Reddit accounts. The key differentiator is managed accounts — users never risk their own Reddit accounts getting banned. Target audience: SaaS and B2B companies seeking Reddit lead generation and brand awareness.

**Not to be confused with** replyagent.com (a separate white-label CRM product).

## Capabilities & automation surface

| Capability | Description | Surface |
|---|---|---|
| Subreddit monitoring | 24/7 monitoring of target subreddits for relevant conversations | UI + API (Import) |
| AI comment generation | Contextual, human-like comments based on product description and thread context | UI + API (Import triggers generation) |
| Managed account posting | Posts via pre-warmed Reddit accounts with established karma/history | UI-only (managed by ReplyAgent) |
| Google-ranking post detection | Identifies Reddit posts that rank on Google search results | UI-only |
| Manual approval workflow | Review and approve/edit AI drafts before posting | UI + API (Approve) |
| UTM tracking | Attach UTM parameters to track conversions from Reddit engagement | UI-only (configuration) |
| Daily email digests | Curated post recommendations delivered via email | UI-only (email delivery) |
| Anti-spam protections | Rate limiting (max 5 comments/account/day), smart timing during peak hours | Automatic |

## Pricing, limits & plan gates

<!-- Verified against replyagent.ai/pricing 2026-06-13 -->

ReplyAgent now uses a **hybrid model: a monthly subscription for AI/platform access PLUS pay-as-you-go credits for each posted action.**

| Item | Details |
|---|---|
| **Basic subscription** | $79/month, or $699/year (save 26%, ≈ $58/mo). 3-day free trial, cancel anytime. Required to unlock AI content generation. Includes 24/7 post discovery & monitoring, AI content generation, up to 3 products, analytics. |
| **Manual mode** | No subscription required if you find posts and write content yourself (no AI features). |
| **Comment cost** | $4 per comment (pay-as-you-go credits) |
| **Post cost** | $8 per post (pay-as-you-go credits) |
| **Credit deduction** | $5 held/deducted when a comment is posted, $10 when a post is published; the difference vs the $4/$8 price relates to the removal-check/refund mechanics. |
| **Refund** | 70% refund if removed by moderators — $2.80 per comment, $7 per post. Single removal check runs 24h after a comment, 48h after a post. Full refund if posting fails immediately and never goes live. |
| **AI import credit** | AI-generated comment import costs 1 credit; providing your own reply text incurs no AI charge. |
| **Enterprise** | Custom plans for agencies managing 10+ products, with volume discounts and dedicated support. |
| **Posting limit** | Max 5 comments per managed Reddit account per day (additional accounts assigned for higher volume). |

> Earlier pricing was pure pay-per-post at $3/comment and $6/post with a 30-day full-refund "warranty." As of 2026-06-13 the live page shows the $79/mo subscription + $4/$8 pay-as-you-go + 70% refund on a single 24h/48h check.

**Monthly cost estimation (subscription + posting, comments only):**
- Light usage (5 comments/day): $79 + ~$600 ≈ ~$680/month
- Moderate (10 comments/day): $79 + ~$1,200 ≈ ~$1,280/month
- Heavy (20 comments/day): $79 + ~$2,400 ≈ ~$2,480/month

## Integrations

| Integration | Direction | Details |
|---|---|---|
| Reddit (via managed accounts) | Write | Comments posted through ReplyAgent's account network |
| Email digests | Read | Daily curated post recommendations |
| UTM / Google Analytics | Read | Track conversions from Reddit engagement |
| REST API | Read/Write | Import posts, approve comments, list comments |

No Zapier, Make, MCP, or native CRM integrations.

## Data model

<!-- Verified against replyagent.ai/docs (List Comments response) 2026-06-13 -->

The `aiComments` object returned by `GET /api/products/{productId}/ai-comments` uses these fields:

```json
{
  "id": "cm_abc123...",
  "productId": "prod_123",
  "postId": "post_456",
  "postTitle": "Best tools for SaaS startups?",
  "postUrl": "https://www.reddit.com/r/SaaS/comments/abc123/best_tools/",
  "subreddit": "SaaS",
  "postContent": "Looking for recommendations...",
  "suggestedReply": "I've been using MyProduct for this...",
  "isApproved": false,
  "isPosted": false,
  "isDeleted": false,
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z",
  "submittedAt": null,
  "commentId": null,
  "commentUrl": null,
  "redditAccount": null,
  "postMeta": { "upvotes": 45, "numComments": 23, "createdUtc": "...", "source": "reddit" },
  "extra": { "searchSource": "reddit" }
}
```

Status is expressed via the booleans `isApproved` / `isPosted` / `isDeleted` (not a single `status` string) and filtered on the List endpoint via the `status` query param (`preview` / `queue` / `posted`). After posting, `commentId`, `commentUrl`, `redditAccount`, and `submittedAt` are populated.

## Quick-start recipes

### Recipe 1: Import a batch of Reddit posts for comment generation

**Trigger:** You found relevant Reddit posts through your own monitoring and want ReplyAgent to generate comments for them.

**cURL:**
```bash
curl -X POST https://www.replyagent.ai/api/products/YOUR_PRODUCT_ID/ai-comments/manual-import \
  -H "Authorization: Bearer sk_YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "imports": [
      { "url": "https://www.reddit.com/r/SaaS/comments/abc123/looking-for-tool/" },
      { "url": "https://www.reddit.com/r/startups/comments/def456/need-recommendation/" }
    ]
  }'
```

**Python:**
```python
import requests

API_KEY = "sk_YOUR_API_KEY"
PRODUCT_ID = "YOUR_PRODUCT_ID"

resp = requests.post(
    f"https://www.replyagent.ai/api/products/{PRODUCT_ID}/ai-comments/manual-import",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "imports": [
            {"url": "https://www.reddit.com/r/SaaS/comments/abc123/looking-for-tool/"},
            {"url": "https://www.reddit.com/r/startups/comments/def456/need-recommendation/"},
        ],
    },
)
print(resp.json())
```

**Gotchas:** URLs must be Reddit post permalinks. Omit `reply` per import to let the AI generate the comment (1 credit each); add `"reply": "..."` to supply your own text (no AI charge). Max 10 imports per batch. Imports land in "preview" state — you still need to approve them before ReplyAgent posts the comment.

### Recipe 2: Approve a preview comment for posting

**Trigger:** You reviewed a generated comment in the dashboard or via API and want to approve it for posting.

**cURL:**
```bash
curl -X POST https://www.replyagent.ai/api/products/YOUR_PRODUCT_ID/ai-comments/cm_abc123/approve \
  -H "Authorization: Bearer sk_YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "scheduleType": "peak_hours" }'
```

**Python:**
```python
COMMENT_ID = "cm_abc123"
resp = requests.post(
    f"https://www.replyagent.ai/api/products/{PRODUCT_ID}/ai-comments/{COMMENT_ID}/approve",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"scheduleType": "peak_hours"},  # "immediate" | "peak_hours" | "custom"
)
print(resp.json())  # Comment queued for posting via managed account
```

**Gotchas:** `scheduleType` accepts `immediate`, `peak_hours`, or `custom` (pass `customDateTime` as an ISO 8601 timestamp for `custom`). Approving with an empty credit balance returns `Insufficient credit balance. Please add credits to enable comment posting.`

### Recipe 3: List comments and filter by status

**cURL:**
```bash
curl "https://www.replyagent.ai/api/products/YOUR_PRODUCT_ID/ai-comments?status=posted&page=1&pageSize=100" \
  -H "Authorization: Bearer sk_YOUR_API_KEY"
```

**Python:**
```python
resp = requests.get(
    f"https://www.replyagent.ai/api/products/{PRODUCT_ID}/ai-comments",
    headers={"Authorization": f"Bearer {API_KEY}"},
    params={"status": "posted", "page": 1, "pageSize": 100},  # status: preview|queue|posted
)
data = resp.json()
for comment in data.get("aiComments", []):
    print(f"{comment['subreddit']}: posted={comment['isPosted']} url={comment['commentUrl']}")
# Paginate via data['pagination']['hasNext'] / increment page
```

## Integration patterns

### Custom monitoring → ReplyAgent pipeline

Use a dedicated monitoring tool (Octolens, Syften, CatchIntent) to find relevant Reddit posts, then push them to ReplyAgent via the Import endpoint for managed posting:

1. **Monitor** — tool of choice finds high-intent posts
2. **Filter** — your code scores/filters for relevance
3. **Import** — POST to ReplyAgent's Import endpoint
4. **Review** — check AI-generated comments in dashboard or via API
5. **Approve** — POST to Approve endpoint
6. **Track** — monitor UTM-tagged traffic in Google Analytics

### Handling the removal-check refund

ReplyAgent runs a single removal check — 24 hours after a comment, 48 hours after a post. If moderators removed it by then, you get a 70% refund ($2.80 per comment, $7 per post); if posting fails immediately and never goes live you get a full refund. Track which comments fail the check and reconcile against your credit balance. If removal rate is high, review your subreddit targeting and comment quality.
