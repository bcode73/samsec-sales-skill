<!-- Source: https://api.brandmentions.com/documentation.html + https://help.brandmentions.com/en/articles/12814640-what-are-the-available-brandmentions-api-endpoints + https://help.brandmentions.com/en/articles/3585630-does-brandmentions-provide-api-access (re-verified 2026-06-13) -->

# BrandMentions API Reference

## Base URL

```
https://api.brandmentions.com/command.php
```

All requests use the `command` parameter to specify the endpoint. Requests can be sent as GET or POST. Authentication via `api_key` query parameter.

**API access is available on Expert ($499/mo) and Enterprise (custom) plans.** Starter and Pro do not include API access. Contact support@brandmentions.com to activate your API key once your plan includes it. (Verified 2026-06-13 against help.brandmentions.com: "BrandMentions provides API access on the Expert and custom subscription packages.")

## Authentication

```bash
curl "https://api.brandmentions.com/command.php?api_key=YOUR_API_KEY&command=GetRemainingCredits"
```

- `api_key` — required on every request
- Error code 3 = missing API key
- Error code 4 = invalid API key

## Endpoints

### PostSearch
Create an on-demand search job. Processing is asynchronous.

Parameters use numbered (`keyword1`..`keyword5`) and bracketed-array (`active_sources[]`, `languages[]`) notation — NOT `keywords[0]`-style indexing. Verbatim example request from the docs:

```
https://api.brandmentions.com/command.php?api_key=API_KEY&command=PostSearch&keyword1=brandmentions&keyword2=brand+mentions&match_type1=broad&time_range=day&languages[]=en&countries[]=US&stop_web_at=50&stop_social_at=50&required_keywords1[]=brand&excluded_keywords2[]=seo&active_sources[]=web&active_sources[]=twitter&callback=https://brandmentions.com
```

| Param | Type | Required | Description |
|---|---|---|---|
| `keyword1`..`keyword5` | string | Yes | Up to 5 keywords, 3-50 chars each (numbered, not array-indexed) |
| `match_type1`..`match_type5` | string | No | Per-keyword match type: `exact` (default), `broad`, `case_sensitive` |
| `required_keywordsN[]` | string | No | Per-keyword required terms (AND/include — noise reduction) |
| `excluded_keywordsN[]` | string | No | Per-keyword excluded terms (NOT/exclude — noise reduction) |
| `time_range` | string | No | Time range filter (e.g. `day`) |
| `languages[]` | string | No | Language filter, two-char codes (array, plural) |
| `countries[]` | string | No | Country filter, two-char codes (array, plural) |
| `active_sources[]` | string | No | Sources to include (array): web, facebook, twitter, instagram, linkedin, reddit, youtube, tiktok, bluesky |
| `stop_web_at` | int | No | Cap web results |
| `stop_social_at` | int | No | Cap social results |
| `callback` | string | No | Callback URL — when the search completes BrandMentions sends a POST to this URL with `search_hash` set in the body |

**Cost**: 1 credit per search.

**Response (verbatim shape from docs):**
```json
{
  "status": "success",
  "search_hash": 3186302626
}
```

**Note**: `search_hash` is returned as a number, valid for 1 hour.

### GetMentions
Retrieve complete results of a PostSearch. Best used after callback receipt.

| Param | Type | Required | Description |
|---|---|---|---|
| `search_hash` | string | Yes | Hash from PostSearch response |

**Cost**: 0 credits.

**Response fields (from docs):** `status`, `mentions` (array of objects with `date`, `type`, `title`, `url`, `performance`, `social`, `text`, `sentiment`, `found_keyword`), `number_of_mentions` (e.g. `{"web":13,"social":16}`), `keywords`, `language`, `country`, `remaining_credits`.

### GetProcessedMentions
Poll partial results while search is still processing. Use 13-second intervals.

| Param | Type | Required | Description |
|---|---|---|---|
| `search_hash` | string | Yes | Hash from PostSearch response |

**Response includes `processing_ended` boolean** — poll until `true`, then call GetMentions for final results.

**Cost**: 0 credits.

### GetRemainingCredits
Check available API credits.

**Cost**: 0 credits.

```bash
curl "https://api.brandmentions.com/command.php?api_key=YOUR_API_KEY&command=GetRemainingCredits"
```

**Response (verbatim shape from docs):**
```json
{ "PostSearch": 99, "AddProject": 2, "Mentions": 3459 }
```
Read `PostSearch` and `AddProject` for remaining job credits and `Mentions` for the remaining monthly mention quota.

### AddProject
Create a saved daily monitoring project.

| Param | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Project name |
| `keyword1`..`keyword5` | string | Yes | Keywords to monitor (numbered, same notation as PostSearch) |
| `languages[]` | string | No | Language filter (array, two-char codes) |
| `countries[]` | string | No | Country filter (array, two-char codes) |
| `active_sources[]` | string | No | Sources to monitor (array) |
| `callback` | string | No | Callback URL — when project execution completes BrandMentions sends a POST with `project_id` set in the body |

**Cost**: 1 credit.

### ListProjects
List all projects in the account.

**Cost**: 0 credits.

### DeleteProject
Remove a project permanently.

**Cost**: 0 credits.

### EditProject
Modify project keywords, filters, and configuration. For boolean expression projects.

**Cost**: 0 credits.

### GetProjectMentions
Paginated retrieval of project mentions with filtering.

| Param | Type | Required | Description |
|---|---|---|---|
| `project_id` | string | Yes | Project identifier |
| `page` | int | No | Page number (default 1) |
| `per_page` | int | No | Results per page (max 100) |
| `date_from` | string | No | Start date filter |
| `date_to` | string | No | End date filter |

**Cost**: 0 credits.

### GetProjectInfluencers
Return top influencers/authors associated with a project by reach.

**Cost**: 0 credits.

### GetMentionsCount
Total mention count matching filters, without returning full mention data.

**Cost**: 0 credits.

### RunProjectHistorical
Run historical backfill for a project by month count.

**Cost**: Uses historical mention credits.

### AddReviewSourceToProject
Integrate review platforms into project monitoring.

**Cost**: 0 credits.

### GetMainKeywordsCount
Calculate keyword credits needed for a boolean expression.

**Cost**: 0 credits.

## Supported sources

Web, Facebook, Twitter/X, Instagram, LinkedIn, Reddit, YouTube, TikTok, Bluesky

## Callbacks (webhooks)

PostSearch and AddProject both accept an optional `callback` parameter. When the async job finishes, BrandMentions sends a **POST request to that URL**:

- **PostSearch callback** — body contains the `search_hash` field. Use it to call GetMentions instead of polling GetProcessedMentions.
- **AddProject callback** — body contains the `project_id` field once project execution is done.

No HMAC signature or callback authentication scheme is documented, so treat the payload as untrusted: re-fetch the result via GetMentions / GetProjectMentions using the supplied id rather than trusting the POST body, and restrict the callback endpoint to expected ids.

## Response format

All responses return JSON with a `status` field. Error codes range from 1 to 78 (e.g. code 1 "Missing command", code 3 "Missing API key", code 7 "Search not ready", code 73 "Start date greater than end date", code 78 "Invalid excluded country").

## Pagination

Offset-based: `page` + `per_page` (max 100 per page). Loop until empty `mentions` array.

## Rate limits

No documented rate limits. Recommend spacing requests by 1-2 seconds to be safe.

## Gaps

- Callbacks are documented (PostSearch/AddProject `callback` param) but there is NO documented signing/HMAC/auth on the callback POST — verify ids server-side
- Full 1-78 error code table is referenced in docs but not reproduced here in full (only sample codes captured)
- No documented rate limit headers or retry strategy (no rate limits published)
- PostSearch/GetRemainingCredits response shapes captured verbatim from docs; GetMentions field list captured from docs; project/mention object shapes in platform-guide.md are still partly reconstructed
