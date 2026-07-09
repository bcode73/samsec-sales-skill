<!-- Source: https://docs.moosend.com/api-documentation?lang=en_US and https://github.com/moosend/api-wrappers-php (re-verified 2026-06-13) -->
# Moosend API Reference

## Overview

REST API v3 at `https://api.moosend.com/v3/`. Authentication via API key as query parameter (`?apikey=YOUR_KEY`). Response format is part of the path — append `.json` (or `.xml`) to every endpoint. Note: Moosend uses `POST` for create AND update operations (not `PUT`). No webhook subscription endpoint — use automation workflows with HTTP POST actions instead.

## Authentication

API key passed as a query parameter on every request:

```bash
curl "https://api.moosend.com/v3/lists.json?apikey=YOUR_API_KEY"
```

Find your API key: Moosend dashboard > Settings > API Key.

**Important**: The key goes in the URL query string, NOT in an Authorization header.

## Endpoints by category

### Campaigns API (~20 methods)

| Method | Path | Description |
|---|---|---|
| GET | `/v3/campaigns.json` | Get all campaigns |
| GET | `/v3/campaigns/{Page}.json` | Get campaigns by page |
| GET | `/v3/campaigns/{Page}/{PageSize}.json` | Get campaigns by page and page size |
| GET | `/v3/campaigns/{id}/view.json` | Get campaign details |
| GET | `/v3/campaigns/{id}/view_summary.json` | Get campaign summary |
| GET | `/v3/campaigns/{id}/view_ab_summary.json` | Get A/B test summary |
| POST | `/v3/campaigns/create.json` | Create a draft campaign |
| POST | `/v3/campaigns/{id}/update.json` | Update a draft campaign (POST, not PUT) |
| DELETE | `/v3/campaigns/{id}/delete.json` | Delete a campaign |
| POST | `/v3/campaigns/{id}/clone.json` | Clone a campaign |
| POST | `/v3/campaigns/{id}/send.json` | Send a campaign |
| POST | `/v3/campaigns/{id}/send_test.json` | Send a test email |
| POST | `/v3/campaigns/{id}/schedule.json` | Schedule a campaign |
| POST | `/v3/campaigns/{id}/unschedule.json` | Unschedule a campaign |
| GET | `/v3/campaigns/{id}/stats/{Type}.json` | Get activity by type (Sent, Opened, Clicked, Bounced, etc.) |
| GET | `/v3/campaigns/{id}/stats/countries.json` | Get activity by location |
| GET | `/v3/campaigns/{id}/stats/links.json` | Get link click activity |

### Mailing Lists API (~10 methods)

| Method | Path | Description |
|---|---|---|
| GET | `/v3/lists.json` | Get all active mailing lists |
| GET | `/v3/lists/{Page}/{PageSize}.json` | Get all lists with paging |
| GET | `/v3/lists/{id}/details.json` | Get list details with statistics |
| POST | `/v3/lists/create.json` | Create a mailing list |
| POST | `/v3/lists/{id}/update.json` | Update a mailing list (POST, not PUT) |
| DELETE | `/v3/lists/{id}/delete.json` | Delete a mailing list |
| POST | `/v3/lists/{id}/customfields/create.json` | Add a custom field to a list |
| POST | `/v3/lists/{id}/customfields/{field_id}/update.json` | Update a custom field (POST, not PUT) |
| DELETE | `/v3/lists/{id}/customfields/{field_id}/delete.json` | Delete a custom field |

**Note**: the custom-field path segment is `customfields` (one word), not `custom_fields`.

### Subscribers API (~12 methods)

| Method | Path | Description |
|---|---|---|
| GET | `/v3/subscribers/{list_id}/view.json?Email={email}` | Get subscriber by email |
| GET | `/v3/subscribers/{list_id}/find/{subscriber_id}.json` | Get subscriber by ID |
| GET | `/v3/lists/{list_id}/subscribers/{status}.json` | Get subscribers by status (Subscribed, Unsubscribed, Bounced, Removed) |
| POST | `/v3/subscribers/{list_id}/subscribe.json` | Add a subscriber (upserts — re-subscribing an existing email updates it) |
| POST | `/v3/subscribers/{list_id}/subscribe_many.json` | Add multiple subscribers |
| POST | `/v3/subscribers/{list_id}/unsubscribe.json` | Unsubscribe a member from the list |
| POST | `/v3/subscribers/{list_id}/{campaign_id}/unsubscribe.json` | Unsubscribe a member from a list AND a specific campaign |
| POST | `/v3/subscribers/unsubscribe.json` | Unsubscribe a member from the whole account |
| POST | `/v3/subscribers/{list_id}/remove.json` | Remove a member |
| POST | `/v3/subscribers/{list_id}/remove_many.json` | Remove multiple members |
| POST | `/v3/subscribers/{list_id}/update/{subscriber_id}.json` | Update subscriber (POST, not PUT) |

### Segments API (~8 methods)

| Method | Path | Description |
|---|---|---|
| GET | `/v3/lists/{list_id}/segments.json` | Get all segments (with criteria) for a list |
| GET | `/v3/lists/{list_id}/segments/{segment_id}/details.json` | Get segment details |
| GET | `/v3/lists/{list_id}/segments/{segment_id}/members.json` | Get subscribers in a segment |
| POST | `/v3/lists/{list_id}/segments/create.json` | Create a segment |
| POST | `/v3/lists/{list_id}/segments/{segment_id}/update.json` | Update a segment (POST, not PUT) |
| DELETE | `/v3/lists/{list_id}/segments/{segment_id}/delete.json` | Delete a segment |
| POST | `/v3/lists/{list_id}/segments/{segment_id}/criteria/add.json` | Add a criterion (rule) to a segment |
| POST | `/v3/lists/{list_id}/segments/{segment_id}/criteria/{criteria_id}/update.json` | Update criteria (POST, not PUT) |

> The official PHP/Java/.NET wrappers expose no delete-criteria endpoint; criteria are managed via add/update only. Prior versions of this reference listed `DELETE …/criteria/{id}/delete.json` — it could not be re-verified against current docs (2026-06-13) and may not exist.

## Pagination

Page-based pagination (1-indexed). For list-collection endpoints, `Page` and `PageSize` are **path segments**, not query parameters:

```
GET /v3/lists/1/100.json?apikey=KEY
GET /v3/campaigns/1/50.json?apikey=KEY
```

Subscriber-by-status reads accept `Page`/`PageSize` and other filters as query params. Response includes:
```json
{
  "Code": 0,
  "Error": null,
  "Context": { ... },
  "Paging": {
    "PageSize": 100,
    "CurrentPage": 1,
    "TotalPageCount": 3,
    "TotalResults": 250
  }
}
```

Default PageSize: 10. Max PageSize: 500.

## Error responses

All responses use the same envelope:

```json
{
  "Code": 1,
  "Error": "Invalid API key",
  "Context": null
}
```

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Error (check Error field) |

HTTP status codes follow standard REST conventions (200, 400, 401, 404, 429, 500).

## Rate limits

Moosend now **publicly documents** per-resource rate limits (measured in calls per short window per API key). Examples from the official rate-limiting page:

| Operation | Limit |
|---|---|
| Add a subscriber | 10 calls / 10s |
| Add multiple subscribers (subscribe_many) | 2 calls / 10s |
| Unsubscribe | 20 calls / 10s |
| Remove (delete) a subscriber | 40 calls / 10s |
| Send a transactional campaign | 6 calls / 1s |

Limits are per endpoint/resource, not a single global cap. When exceeded, the API returns HTTP **429** with this envelope:

```json
{ "Code": 429, "Error": "RATE-LIMITING", "Context": null }
```

Implement exponential backoff (start at ~1s) and respect the per-resource limits above. Source: docs.moosend.com API rate-limiting page (re-verified 2026-06-13).

## SDKs

| Language | Repository | Notes |
|---|---|---|
| PHP | github.com/moosend/api-wrappers-php | Covers Campaigns, MailingLists, Subscribers, Segments |
| Java | github.com/moosend/api-wrappers-java | Full API coverage |
| .NET | github.com/moosend/api-wrappers-dotnet | Full API coverage |
| JavaScript | github.com/moosend/api-wrappers-js | Official JS wrapper |
| Python | No official SDK | Use `requests` library directly |

> The official wrapper repos were renamed from the old `phpwrapper`/`javawrapper`/`dotnetwrapper` names to the `api-wrappers-{lang}` convention; an official JS wrapper now exists.

## Gaps

- Official API reference now lives at docs.moosend.com (modern tri-pane docs); the legacy apiary.io URL still resolves but the docs.moosend.com pages and the `api-wrappers-*` repos are the authoritative source.
- Webhook payload schemas not documented (Moosend uses automation HTTP POST actions instead of traditional webhooks — no signed webhook subscriptions).
- Rate limits ARE now publicly documented per-resource (see Rate limits section) — older "not documented" guidance is superseded.
- Transactional email SMTP settings documented in dashboard only, not in API docs.
- Automation API (create/manage automations programmatically) does not appear to exist — automations are UI-only.
- A delete-criteria segment endpoint could not be re-verified in current wrappers/docs (2026-06-13).
