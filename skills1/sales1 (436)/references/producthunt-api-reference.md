# Product Hunt GraphQL API Reference

## Overview

Product Hunt uses a GraphQL API (v2). All queries go through a single endpoint.

- **Endpoint**: `https://api.producthunt.com/v2/api/graphql`
- **Auth**: OAuth 2.0 or Developer Token
- **Rate limit (GraphQL)**: 6,250 complexity points per 15 minutes
- **Rate limit (other `/v2/*` endpoints)**: 450 requests per 15 minutes
- **Docs**: `https://api.producthunt.com/v2/docs`
- **Explorer**: `https://ph-graph-api-explorer.herokuapp.com/` (interactive GraphiQL explorer)

## Authentication

### Developer Token (simplest)

1. Go to `https://www.producthunt.com/v2/oauth/applications`
2. Create a new application
3. Copy the Developer Token
4. Use in header: `Authorization: Bearer {token}`

### OAuth 2.0

For user-context operations (posting, voting):

1. Register an OAuth application
2. Redirect user to: `https://api.producthunt.com/v2/oauth/authorize?client_id={id}&redirect_uri={uri}&response_type=code&scope=public+private` (add `+write` only if your app has been granted write access)
3. Exchange code for token at: `POST https://api.producthunt.com/v2/oauth/token`

**Scopes** (three types per the official docs):
- `public` — access public information on Product Hunt (granted to all apps by default)
- `private` — access Product Hunt on behalf of the authenticated user
- `write` — take actions (post, vote, comment) on behalf of the user; **requires special approval from Product Hunt**

## Key Queries

### Get posts (launches)

The `posts` query accepts `order: PostsOrder` (enum values: `FEATURED_AT`, `NEWEST`, `RANKING`, `VOTES`), plus `first`/`last`/`after`/`before` (Relay pagination), `topic: String`, `featured: Boolean`, `postedAfter`/`postedBefore: DateTime`, and `twitterUrl: String`.

```graphql
query {
  posts(order: RANKING, first: 20) {
    edges {
      node {
        id
        name
        tagline
        url
        votesCount
        commentsCount
        createdAt
        website
        thumbnail {
          url
        }
        topics {
          edges {
            node {
              name
            }
          }
        }
        makers {
          id
          name
          username
        }
      }
    }
  }
}
```

### Get a specific post

```graphql
query {
  post(slug: "your-product-slug") {
    id
    name
    tagline
    description
    url
    votesCount
    commentsCount
    reviewsRating
    website
    makers {
      id
      name
      username
    }
    comments(first: 50) {
      edges {
        node {
          body
          createdAt
          user {
            name
            username
          }
        }
      }
    }
  }
}
```

### Search posts

```graphql
query {
  posts(topic: "artificial-intelligence", order: VOTES, first: 10) {
    edges {
      node {
        name
        tagline
        votesCount
        url
      }
    }
  }
}
```

### Get topics

```graphql
query {
  topics(first: 50) {
    edges {
      node {
        id
        name
        slug
        postsCount
      }
    }
  }
}
```

### Get user profile

```graphql
query {
  user(username: "rrhoover") {
    id
    name
    username
    headline
    profileImage
    madePosts(first: 10) {
      edges {
        node {
          name
          tagline
          votesCount
        }
      }
    }
  }
}
```

> **Note**: The `User` type does **not** expose scalar `followersCount` / `followingCount` fields. Follower data is available via the `followers(...)` and `following(...)` connections (Relay-style — page through `edges`/`pageInfo` and count or `totalCount` if needed). Don't request `followersCount`/`followingCount` directly or the query will fail schema validation.

## Rate Limiting

- Each GraphQL query has a complexity cost based on fields requested and pagination depth
- Budget (GraphQL `/v2/api/graphql`): 6,250 complexity points per 15-minute window
- Budget (all other `/v2/*` endpoints): 450 requests per 15-minute window
- Exceeding the limit returns HTTP `429`
- Every response includes three rate-limit headers:
  - `X-Rate-Limit-Limit` — your application's quota for the 15-minute window
  - `X-Rate-Limit-Remaining` — remaining quota for the current reset period
  - `X-Rate-Limit-Reset` — seconds until the rate limit resets
- Simple queries (single post lookup) cost ~5-10 points
- List queries with nested fields cost more (e.g., 20 posts with comments + makers ~ 100-200 points)
- Product Hunt reserves the right to throttle apps it deems outside fair use; contact them for higher limits

## Pagination

Uses Relay-style cursor pagination:

```graphql
query {
  posts(first: 20, after: "cursor_string") {
    edges {
      node { ... }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

## Common Patterns

### Monitor daily launches

Poll `posts(order: NEWEST)` filtered by today's date. No webhook support — use scheduled polling.

### Track competitor launches

Query by topic or search by keyword, then monitor votesCount and commentsCount over the 24-hour window.

### Export launch analytics

Query your post by slug, pull comments, votes over time (requires multiple polls), and makers list.

## Limitations

- **No webhooks**: Must poll for updates
- **No write operations via API for launches**: You cannot submit a product launch via the API — must use the web interface
- **Rate limits are per-application**: Shared across all users of your OAuth app
- **Historical data**: Some older posts may have incomplete data
- **No real-time ranking data**: The ranking algorithm is not exposed — you can only see votesCount and commentsCount, not the actual ranking score
