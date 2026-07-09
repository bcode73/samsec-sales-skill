# TexAu V3 API Reference

<!-- Source: https://github.com/texauhq/texau-n8n-apis-nodes (official TexAu V3 community n8n nodes — credentials, transport, operations) -->
<!-- Source: https://github.com/texauhq/texau-gtm-skills/blob/HEAD/_lib/mcp-catalog.json (MCP tool catalog: credit costs, batch limits, sync/async flags) -->
<!-- Source: https://www.texau.com/api-platform and https://docs.texau.com (V3 API portal — base URL, MCP endpoint) -->
<!-- Captured 2026-06. Endpoint paths/fields are reproduced verbatim from the official n8n node definitions. Verify against docs.texau.com before relying on exact response shapes. -->

> Note: TexAu's newer API/MCP is also published by the same team under a `richapi.ai` brand (`api.richapi.ai/api/v1`, `mcp.richapi.ai/mcp`). The TexAu-branded hosts below are what the official n8n credential test and product pages use. Use whichever host issued your key.

## Base URL & authentication

- **Base URL:** `https://v3-api.texau.com/api/v1`
- **Auth:** API key in the `x-api-key` request header (the MCP server / Claude desktop connector uses OAuth instead and needs no key).
- **Credential test endpoint:** `GET https://v3-api.texau.com/api/v1/my-endpoints`
- **Unauthenticated:** `GET /health` requires no auth.

```bash
# Auth quick-start — list the endpoints your key can call
curl https://v3-api.texau.com/api/v1/my-endpoints \
  -H "x-api-key: $TEXAU_API_KEY"
```

## MCP server

- **Endpoint:** `https://mcp.texau.com/mcp` — exposes the endpoints below as Claude/Cursor tools (`enrich_profile`, `people_search`, `find_emails`, etc.). OAuth; works with Claude Code / Cursor.

## System endpoints

| Operation | Method | Path | Auth | Notes |
|---|---|---|---|---|
| Get Health | GET | `/health` | none | Health check |
| Get Usage | GET | `/usage` | apiKey | Query `month` in `YYYY-MM` format; credit usage |
| Get My Endpoints | GET | `/my-endpoints` | apiKey | Lists endpoints available to this key |

## Enrichment endpoints

| Operation | Method | Path | Body fields | Credits |
|---|---|---|---|---|
| Enrich Profile | POST | `/enrich_profile` | `url` (LinkedIn profile URL, required), `useCache` (bool, default true) | 1/call |
| Enrich Company | POST | `/enrich_company` | `url` (LinkedIn company URL, required), `useCache` | 1/call |
| Enrich Profiles Bulk | POST | `/enrich_profiles_bulk` | `urns` (JSON array of profile URNs, e.g. `["ACoAA..."]`) | 1/result, ≤50 |
| Enrich Companies Bulk | POST | `/enrich_companies_bulk` | `urns` (JSON array of company ids, e.g. `["1586","1035"]`) | 1/result, ≤50 |

## Search / discovery endpoints

| Operation | Method | Path | Key fields | Credits |
|---|---|---|---|---|
| People Search | POST | `/people_search` | `page` (0-based, req), `size` (req), `account{linkedin,domain,industry,employeeSize{start,end}}`, `contact{jobTitle,location}` | 0.1/result (700M+ cached index) |
| LinkedIn Profile Search | GET | `/profile_search` | query: `search,firstName,lastName,title,currentCompany,pastCompany,school,location,geoId,industryId,keywordsCompany,keywordsSchool,followerOf,page` (1-based); ≥1 filter required | 0.1/result (live LinkedIn) |
| Lead Search | POST | `/lead_search` | `search`, array fields `currentJobTitles,pastJobTitles,currentCompanies,pastCompanies,seniority,industries,functions,companySize,geoIds,locations,companyHeadquarterLocations,firstNames,lastNames,schools,yearsOfExperience,yearsAtCurrentCompany,profileLanguages`; `recentlyChangedJobs` (bool), `salesNavUrl`, `sessionId`, `page` (1-based), `exclude` (JSON) | 0.5/result, 30+ filters |
| Reference Data | GET | `/search_reference_data` | none — returns valid labels for `lead_search` (seniority, industries, functions, companySize, profileLanguages) | free |
| Post Keyword Search | POST | `/post_keyword_search` | `keyword` (req), `sort` (RELEVANCE/DATE_POSTED), `datePosted` (PAST_24_HOURS/PAST_WEEK/PAST_MONTH), `contentType`, `fromPerson`, `fromCompany`, `authorIndustry`, `authorKeyword`, `page`, `size` | 6/call |
| Search Bing | POST | `/search_bing` | `query` (req), `num_results`, `page`, `cache` | — |
| Search Google Trends | POST | `/search_google_trends` | `keyword` (req), `geo`, `timeframe` (e.g. `today 12-m`), `cache` | — |

## Posts & activities

| Operation | Method | Path | Key fields | Credits |
|---|---|---|---|---|
| Post Details | POST | `/post_details` | `url` or `urn` (one required), `comments` (bool), `reactions` (bool) | 1/call |
| Profile Activities | POST | `/profile_activities` | `urn` (req), `type` (POST/COMMENT/REACTION), `paginationToken`, `size`, `useCache` | 2/call |

## LinkedIn ads

| Operation | Method | Path | Key fields |
|---|---|---|---|
| Geo ID Search | GET | `/geo_id_search` | `search` (location name, req) |
| Ad Search | GET | `/ad_search` | `searchUrl`, `keyword`, `accountOwner`, `countries`, `dateOption` (last-30-days/current-month/current-year/last-year/custom-date-range), `startdate`, `enddate`, `paginationToken` (0.2/result) |
| Ad Details | GET | `/ad_details` | `url` (Ad Library detail URL, req) (2/call) |

## Email endpoints (async — webhook + poll)

| Operation | Method | Path | Body / params | Credits |
|---|---|---|---|---|
| Email Finding | POST | `/email_finding` | `webhook` (URL, required), `data` array of `{ refId, firstname, lastname, domain }` (domain required; first or last name required) | 2/person found |
| Email Finding Inquiry | GET | `/email_finding_inquiry/{id}` | path `id` = job id | free |
| Email Verification | POST | `/email_verification` | `webhook` (required), `data` array of `{ refId, email }` | 0.5/email |
| Email Verification Inquiry | GET | `/email_verification_inquiry/{id}` | path `id` = job id | free |

The submit (`POST`) returns a job id; per-record results are POSTed to your `webhook` and are also fetchable via the matching `*_inquiry/{id}` endpoint.

```bash
# Submit
curl -X POST https://v3-api.texau.com/api/v1/email_finding \
  -H "x-api-key: $TEXAU_API_KEY" -H "Content-Type: application/json" \
  -d '{"webhook":"https://your-app.com/hooks/texau",
       "data":[{"refId":"r1","firstname":"Ada","lastname":"Lovelace","domain":"example.com"}]}'
# Poll
curl https://v3-api.texau.com/api/v1/email_finding_inquiry/<jobId> \
  -H "x-api-key: $TEXAU_API_KEY"
```

## Web scraping endpoints

| Operation | Method | Path | Key fields |
|---|---|---|---|
| Web Meta Tags | POST | `/web_meta_tags` | `url` (req), `cache` |
| Web JSON-LD | POST | `/web_json_ld` | `url` (req), `cache` |
| Web Pixels | POST | `/web_pixels` | `url` (req), `cache` |
| Web Scrape | POST | `/web_scrape` | `url` (req), `formats` (html/markdown/links), `cache` |
| Web Social Links | POST | `/web_social_links` | `url` (req), `cache` |
| Web Tech Stack | POST | `/web_tech_stack` | `url` (req), `cache` |
| Web Emails | POST | `/web_emails` | `url` (req), `max_pages` (default 10), `cache` |
| Web Sitemap | POST | `/web_sitemap` | `url` (req), `max_urls` (default 1000), `cache` |
| Website Intelligence | POST | `/website_intelligence` | `url` (req), `cache` — flagship combined workflow |

## Directory / YouTube / Social

| Operation | Method | Path | Key fields |
|---|---|---|---|
| Yellow Pages Search | POST | `/directory_yellowpages` | `query` (req), `location` (req), `page`, `max_pages`, `cache` |
| YouTube Search | POST | `/youtube_search` | `query` (req), `max_results`, `cache` |
| YouTube Video | POST | `/youtube_video` | `url` (req), `include_captions` (bool), `cache` |
| YouTube Channel | POST | `/youtube_channel` | `url` (req), `cache` |
| YouTube Channel Videos | POST | `/youtube_channel_videos` | `url` (req), `max_results`, `cache` |
| Slack Channel Members | POST | `/slack_channel_members` | `workspace`, `channel_id`, `cookie` (d= cookie), `token` (xoxc), `max_members`, `cache` |

## Pagination

- **Offset/page:** most search endpoints take `page` (note: `people_search`/`post_keyword_search` are **0-based**; `profile_search`/`lead_search` are **1-based**) and `size`.
- **Token:** `profile_activities` and `ad_search` use `paginationToken` from the previous response.
- **Session:** `lead_search` returns a `sessionId` — pass it back to page deeper into the same result set.

## Rate limits & retry

- Monthly ~100,000 calls per endpoint; per-minute 30–3,000 and per-day 800–1,000,000 by action.
- 429 responses include `limit` and `current` fields — read them to back off. Retry async inquiry polls with exponential backoff; don't re-submit the job.

```python
import time, requests
def with_retry(call, tries=5):
    for i in range(tries):
        r = call()
        if r.status_code != 429:
            return r
        time.sleep(2 ** i)   # exponential backoff
    return r
```

## Billing semantics

- **Pay-on-match:** failed lookups return `billed: false` and the credit is refunded.
- **per_call** tools bill once per request; **per_result** tools (search, bulk enrich, email finding) bill per row returned/found.
- Status/inquiry/`search_reference_data`/`health` endpoints are free.

## Error handling

Standard HTTP status codes with JSON error bodies: `401` (auth), `429` (quota — includes `limit`/`current`), `5xx` (server). `GET /health` (no auth) is the liveness check.

## Notes from the official n8n package

- `GET /health` is available without authentication.
- Admin and inbound-webhook endpoints are intentionally excluded from the public n8n package.
- Complex nested payloads (e.g. `lead_search` exclusions, bulk `urns`) are passed as JSON.
