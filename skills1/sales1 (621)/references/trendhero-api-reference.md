# trendHERO API Reference

REST API for generating and retrieving influencer analytics reports programmatically.

> Verified 2026-06-13 against the official public help articles "How does the TrendHero API work?" (help.trendhero.io/en/article/how-does-the-trendhero-api-work-uzlm1/) and "API: How to Use It — Step-by-Step Guide" (help.trendhero.io/en/article/api-how-to-use-it-step-by-step-guide-1vhrn96/). Base URL, Bearer auth, the two endpoints, all status values, the response keys, and the webhook callback shape are confirmed current.

## Authentication

- **Method**: Bearer token
- **Header**: `Authorization: Bearer {access_token}`
- **Token management**: [API → Access Tokens](https://trendhero.io/app/api/access-tokens) in the trendHERO dashboard

## Base URL

```
https://api.trendhero.io/api/public/v1
```

## Endpoints

### Create Report

Generate an analytics report for an Instagram account.

```
POST /reports?username={username}
```

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | string | Yes | Instagram handle (without @) |

**Example:**

```bash
curl --location --request POST \
  'https://api.trendhero.io/api/public/v1/reports?username=davidrobsonyoga' \
  --header 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response includes:**
- `pk` / `account_pk` — unique Instagram account ID (use for webhook matching)
- `status` — report generation state (see status values below)
- Partial influencer data that updates progressively as the report generates

### Retrieve Report

Fetch a completed report.

```
GET /reports/{username}
```

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | string | Yes | Instagram handle (without @) |

**Response structure:**
- `preview` — initial/basic data
- `report` — full analytics report data (90+ metrics)
- `openai_report` — AI-generated narrative analysis
- `saves_shares_report` — engagement breakdown (saves, shares)

## Report Status Values

| Status | Meaning |
|---|---|
| `collecting` | Data gathering in progress — report not ready yet |
| `recollecting` | Re-generating an existing report with fresh data |
| `ready` | Report complete — all data available |
| `impossibleButReady` | Report ready but with limited data |
| `impossible` | Report failed — account is private or data unavailable |
| `preview` | Incomplete data — basic/preview report only (official docs: data under ~1000 rows, e.g. not yet purchased/fully requested) |

## Processing Times

| Account size | Expected time |
|---|---|
| Already cached | Instant |
| <10K followers | 30-60 minutes |
| 10K-1M followers | 1-2 hours |
| 1M+ followers | 2-4 hours |

## Webhooks

Configure a webhook URL in the Access Tokens page to receive notifications when reports finish processing.

**Callback payload** (field names and shapes per the official API help article):

```json
{
  "report_type": "overall_report",
  "notification_type": "report_ready",
  "account_pk": 209749858,
  "version": "1601367830"
}
```

- `version` is a **Unix timestamp string** (seconds since epoch), not an ISO-8601 datetime.
- Match `account_pk` from the callback to the `pk` value returned when you created the report.
- Per the official docs: if a report's status is `collecting` when you POST it, the system sends this callback once the report reaches `ready` — provided you have configured a webhook URL in the API → Access Tokens page.

## Common Errors

| Error | Cause | Solution |
|---|---|---|
| "Wrong token" | Invalid or expired API token | Regenerate token in Access Tokens page |
| "You already have the latest version" | Report already exists and is current | Use GET to retrieve the existing report |
| `impossible` status | Private account or restricted data | Verify the account is public and the username is correct |

## Rate Limits

No documented rate limits. Report generation is inherently throttled by processing time. For batch operations, implement reasonable delays (5-10 seconds) between POST requests to avoid overwhelming the API.

## Postman Collection

trendHERO provides a Postman collection for testing. Import it from the API documentation section in your dashboard to quickly test endpoints with demo accounts before consuming credits.

## Notes

- Reports consume credits from your plan's monthly allocation
- The API returns complex nested JSON with integers, strings, arrays, and objects
- AI-generated analysis (`openai_report`) provides a narrative summary of the analytics data
- First-time reports for uncached accounts take longer — subsequent requests for the same account return faster
