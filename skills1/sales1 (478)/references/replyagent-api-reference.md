<!-- Source: https://www.replyagent.ai/docs -->

# ReplyAgent API Reference

## Authentication

All requests require a Bearer token in the Authorization header.

```
Authorization: Bearer sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

API keys use the `sk_` prefix and are generated from the ReplyAgent dashboard (API Key page → Generate API Key). Keys are shown only once upon creation — store securely.

## Base URL

```
https://www.replyagent.ai
```

## Product ID

All API calls embed the Product ID in the path (`/api/products/{productId}/...`). Find it in the dashboard URL:
```
/dashboard/products/{productId}/setup
```

## Rate Limits

- **100 requests per minute per API key**
- Contact support@replyagent.ai for higher limits

## Endpoints

> Endpoint paths are product-scoped: the `{productId}` is part of the path, not a body/query field.

### Import Comment

Import Reddit posts/comments and create preview comments. Omit `reply` to have the AI generate the comment (costs 1 credit on import); provide your own `reply` text to skip AI generation (no credit charge). Maximum 10 imports per batch.

```
POST /api/products/{productId}/ai-comments/manual-import
```

**Request:**
```json
{
  "imports": [
    {
      "url": "https://www.reddit.com/r/SaaS/comments/abc123/best_tools_for_startups/",
      "reply": "I have been using MyProduct for this exact use case."
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully imported 2 comment(s) (1 manual, 1 AI-generated)",
  "totalProcessed": 2,
  "totalErrors": 0,
  "results": [
    {
      "success": true,
      "commentId": "cm_abc123...",
      "url": "https://www.reddit.com/r/SaaS/comments/abc123/post1/",
      "aiGenerated": true
    }
  ]
}
```

### Approve Comment

Approve a preview comment for posting via managed accounts. The `commentId` is part of the path.

```
POST /api/products/{productId}/ai-comments/{commentId}/approve
```

**Request:**
```json
{
  "scheduleType": "peak_hours"
}
```

**Body fields:**
- `scheduleType` (required) — `"immediate"`, `"peak_hours"`, or `"custom"`
- `customDateTime` (required when `scheduleType` is `"custom"`) — ISO 8601 timestamp

**Response:**
```json
{
  "success": true,
  "message": "Comment approved for immediate posting",
  "comment": {
    "id": "cm_abc123...",
    "isApproved": true,
    "scheduleType": "immediate",
    "scheduledTime": null
  },
  "scheduledTime": null
}
```

**Errors:** Approving with no credits returns `Insufficient credit balance. Please add credits to enable comment posting.`

### List Comments

List comments filtered by product and status, with pagination.

```
GET /api/products/{productId}/ai-comments?status=preview&page=1&pageSize=5
```

**Query parameters:**
- `status` (optional) — `preview`, `queue`, or `posted` (default `preview`)
- `search` (optional) — string filter
- `page` (optional) — page number (default `1`)
- `pageSize` (optional) — items per page, max `100` (default `5`)
- `executionId` (optional) — filter to a discovery run (preview only)
- `moderatorRemoved` (optional) — `true` (removed/failed) or `false` (active)

**Response (200 OK):**
```json
{
  "aiComments": [
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
      "postMeta": {
        "upvotes": 45,
        "numComments": 23,
        "createdUtc": "2024-01-15T08:00:00.000Z",
        "source": "reddit"
      },
      "extra": { "searchSource": "reddit" }
    }
  ],
  "availableExecutions": ["exec_001", "exec_002"],
  "pagination": {
    "page": 1,
    "pageSize": 5,
    "totalCount": 42,
    "totalPages": 9,
    "hasNext": true,
    "hasPrev": false
  }
}
```

## Gaps

- No webhook or callback support documented (confirmed absent as of 2026-06-13)
- No documented batch/bulk approve endpoint — approve is per-comment via `{commentId}` path
- No documented error-response JSON schema or full status-code table (only the insufficient-credit message is shown)
