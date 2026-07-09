# Modash API Reference

## Overview

Modash offers two API product lines for building custom influencer marketing integrations: the **Discovery API** and the **Raw API**. API access is priced separately from the platform subscription.

**Version**: 1.5.0
**Base URL**: `https://api.modash.io/v1/`
**Documentation**: https://docs.modash.io/
**Postman collection**: https://www.postman.com/modashio/modash/documentation/6u0ujia/modash-io-api-v1-5-0
**Help center**: https://help.modash.io/en/collections/3623833-modash-api

## Authentication

**Method**: Bearer token

Get your access token from: https://marketer.modash.io/developer

Three ways to authenticate:
1. **Authorization header** (recommended): `Authorization: Bearer {token}`
2. **Body parameter**: `access_token={token}`
3. **Query parameter**: `?access_token={token}`

## API Products

> Modash organizes its API as two product lines: **Discovery API** and **Raw API**. AI Search, Collaborations, Lookalikes, and email/handle search are sections *within* the Discovery API — not separate standalone products.

### Discovery API

Search and analyze Modash's 380M+ creator database. Built for finding new creators and understanding their audience and performance.

**Starting price**: $16,200/year (3,000 credits/month, annual commitment)
**Credit system**: Different endpoints consume varying credit amounts (e.g. ~0.01 credit per influencer found in a search; collaborations endpoints cost 0.2 credit per request).

**Example endpoints** (base `https://api.modash.io/v1/`, platform path segment is `instagram`, `tiktok`, or `youtube`):
- `POST /v1/{platform}/search` — search creators with filters, lookalikes, sort, pagination (`page` parameter, `calculationMethod`, `sort`, `filter`)
- `GET /v1/{platform}/interests` — list available audience/creator interest dictionary values
- `GET /v1/{platform}/locations` — list location dictionary values
- `GET /v1/{platform}/brands` — list brand dictionary values
- Email / handle / user-ID lookup and AI Search endpoints (see docs.modash.io)
- `POST /collaborations/posts` — collaborated posts where influencers mention brands (0.2 credit/request)
- `POST /collaborations/summary` — aggregated performance across collaborated posts: likes, shares, views, collects, plays (0.2 credit/request)

**Capabilities**:
- Search creators with filters (location, demographics, engagement, follower count, content topics)
- AI Search — find creators by content/intent rather than keywords (a Discovery API section)
- Get detailed creator profiles with audience demographics
- Audience analysis: location, age, gender, language, interests
- Fake follower detection and engagement authenticity scores
- Brand collaboration history (Collaborations endpoints)
- Lookalike search
- Engagement rates and performance benchmarks

### Raw API

Live, unfiltered data from influencer profiles. Best for real-time monitoring and tracking.

**Starting price**: $10,000/year (40,000 requests/month)

**Capabilities**:
- Live profile data (follower counts, bio, recent posts)
- Real-time campaign post tracking
- Mention monitoring
- Content analysis and live metrics
- Market intelligence

**Best practices**: See https://help.modash.io/en/articles/10871299-raw-api-best-practices-onboarding-for-developers

### AI Search (Discovery API section)

Natural-language creator search for AI agents and innovative applications. This is a feature within the Discovery API, not a separate product.

**Capabilities**:
- Describe the creator you need in plain language / find creators by content rather than keywords
- AI interprets intent and returns ranked results
- Designed for integration into AI-powered tools and agents

### Collaborations (Discovery API section)

Maps brand and creator partnership history. Exposed via the Discovery API `collaborations` endpoints (0.2 credit per request).

**Capabilities**:
- Query which brands a creator has worked with (`POST /collaborations/posts`)
- Aggregate collaborated-post performance — views, engagement rate, EMV, post count (`POST /collaborations/summary`)
- Identify competitive conflicts or alignment

## Error Handling

- **429 Too Many Requests** — rate limit exceeded. Implement exponential backoff.
- **5xx Server Error** — non-billable. These don't consume credits. Retry with backoff.
- Always check the HTTP status code and handle errors before processing the response body.

## Rate Limits

Rate limiting errors return HTTP status code 429. Specific rate limits are not publicly documented — implement exponential backoff for 429 responses.

## Pagination

Discovery API search endpoints (e.g. `POST /v1/{platform}/search`) accept a `page` parameter for paging through results, alongside `sort`, `calculationMethod`, and `filter`. For exact page-size limits and per-endpoint pagination behavior, check the interactive docs at docs.modash.io.

## Webhooks

No webhook support documented in the current API version.

## Notes

- API pricing is completely separate from the Modash platform subscription (platform plans start at $299/mo monthly billing)
- The API has two product lines (Discovery, Raw); AI Search, Collaborations, and Lookalikes are Discovery API sections, not separate products
- Failed requests (5xx errors) do not consume credits/limits ("you will not incur any charges or consume any credits/limits"); a "You don't have enough credits for this action" error is returned when credits are exhausted
- The Postman collection provides interactive testing for all endpoints
- For detailed endpoint schemas, use the interactive documentation at docs.modash.io
