<!-- Source: https://help.epom.com/reference/get_ads-api-v3, https://help.epom.com/reference/get_analytics-format-username-hash-timestamp-do, https://help.epom.com/reference/post_user-sign-up-key-hash-timestamp-do — re-verified 2026-06-13 -->

# Epom Ad Server API Reference

## Authentication

Epom uses **MD5 signature-based** authentication (NOT HMAC, NOT Bearer tokens). The auth
credentials are passed as **path segments** in the request URL — `username`, `hash`, and
`timestamp` are part of the path, and management/REST endpoints end in a **`.do`** suffix.

| Parameter | Description |
|-----------|-------------|
| `username` | Your Epom account username (for most management/analytics endpoints) |
| `key` | Your Epom Ad Server **public key** (used in place of username on some endpoints, e.g. user sign-up) |
| `hash` | MD5 signature (computation varies per endpoint — see below) |
| `timestamp` | Current **UNIX milliseconds** timestamp (NOT seconds) |

**Hash computation (verified):**
- Analytics & most management endpoints: `hash = MD5( MD5(password) + timestamp )` — i.e. MD5
  of the concatenation of the user's MD5-hashed password and the UNIX-milliseconds timestamp.
- User sign-up endpoint: `hash = MD5( username + password + email + privateKey + timestamp )`
  where `privateKey` is the Epom Ad Server **private key** (the secret paired with the public key).

The timestamp guards against replay; keep it current. There is a public key / private key pair:
the public key (`key`) identifies the account, the private key is the never-transmitted secret.

**Auth quick-start (cURL)** — analytics report (path-parameter auth, `.do` suffix):
```bash
# UNIX MILLISECONDS timestamp
TIMESTAMP=$(($(date +%s) * 1000))
# MD5 of (MD5(password) + timestamp)
PWD_MD5=$(printf '%s' "your_password" | md5sum | cut -d' ' -f1)
HASH=$(printf '%s' "${PWD_MD5}${TIMESTAMP}" | md5sum | cut -d' ' -f1)

curl "https://n9999.epom.com/rest-api/analytics/JSON/your_username/$HASH/$TIMESTAMP.do?range=LAST_7_DAYS&groupBy=CAMPAIGN"
```

## Base URLs

- **Management / Analytics REST API**: `https://nXXXX.epom.com/rest-api/.../{username}/{hash}/{timestamp}.do`
- **Ad Serving API**: `https://your-adserver.epom.com/ads-api-v3`

The REST API domain is your white-label domain or Epom-assigned subdomain (e.g., `n9999.epom.com`).
The canonical analytics path is `/rest-api/analytics/{format}/{username}/{hash}/{timestamp}.do`,
and the user sign-up path is `/rest-api/user-sign-up/{key}/{hash}/{timestamp}.do`. The simplified
`/rest-api/<resource>` query-string forms shown elsewhere in this file are illustrative — the live
auth/path convention is the `.do` path-parameter form above.

## API Endpoint Categories

### Analytics API

**Verified endpoint (2026-06-13):** `GET /rest-api/analytics/{format}/{username}/{hash}/{timestamp}.do`

- `format` (path): `HTML`, `CSV`, `PDF`, `XLSX`, `JSON` (note: `XLSX`, not `XLS`).
- Query parameters (verified):
  - `range` — `TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`, `LAST_MONTH`, `LAST_3_MONTH`, `LAST_6_MONTH`, `CURRENT_YEAR`, `LAST_YEAR`, `CUSTOM`. Default `TODAY`.
  - `customFrom` / `customTo` — `YYYY-MM-DD`, required when `range=CUSTOM` (these replace the older `dateFrom`/`dateTo`).
  - `groupBy` — grouping dimensions: `SITE`, `ZONE`, `CAMPAIGN`, `COUNTRY`, etc.
  - `statisticType` — report type: `HADOOP_ADREQUESTS`, `IMPRESSIONS_LOG`, `CLICKS_LOG`, `CONVERSIONS_LOG`. Omit for the General report.
  - `groupRange` — time granularity: `NONE`, `HOUR`, `DAY`, `MONTH`, `YEAR`.
  - `limit` / `offset` — pagination controls.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/{format}/{username}/{hash}/{timestamp}.do` | Get analytics report (40+ metrics; filter via `range`/`groupBy`/`statisticType`) |
| GET | `/analytics-reports-layout-settings` | Get report column configuration |
| GET | `/reporting-api-settings-list` | List third-party reporting API settings |
| POST | `/reporting-api-settings-save` | Save third-party reporting API settings |
| DELETE | `/reporting-api-settings/{id}` | Delete third-party reporting API settings |

### Advertiser Management API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/advertisers` | Get all advertisers |
| PUT | `/advertisers-update` | Create or update an advertiser |
| GET | `/advertisers/{advertiserId}` | Get advertiser by ID |
| DELETE | `/advertisers/{advertiserId}` | Delete advertiser |
| GET | `/advertiser/{advertiserId}/campaigns` | Get campaigns for advertiser |
| GET | `/advertisershares` | Get advertiser revenue shares |
| POST | `/advertisershares-update` | Update advertiser revenue shares |
| GET | `/categories-advertising` | Get advertiser categories |

### Advertiser Limits API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/advertiser-limits` | Get advertiser limits |
| DELETE | `/advertiser-limits` | Disable advertiser limits |
| POST | `/advertiser-limits` | Set advertiser limits |
| DELETE | `/advertiser-limits-reset` | Reset advertiser limits |

### Advertiser Capping API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/advertiser-capping/{advertiserId}` | Get capping list for advertiser |
| POST | `/advertiser-capping/{advertiserId}` | Create capping rule for advertiser |
| POST | `/capping/{cappingId}` | Update capping rule |
| DELETE | `/advertiser-capping` | Remove capping rule by ID |

### Advertiser Rules API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rules-advertiser/{advertiserId}-enable` | Enable advertiser rules |
| GET | `/rules-advertiser/{advertiserId}-disable` | Disable advertiser rules |
| GET | `/rules-advertiser/{advertiserId}-add` | Add rules group |
| GET | `/rules-advertiser/{advertiserId}-get` | Get all rules groups |
| GET | `/rules-advertiser/{advertiserId}-remove` | Remove rules group |

### Campaign Management API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/campaign` | Get campaign by ID |
| POST | `/campaign-create` | Create campaign |
| POST | `/campaign/{campaignId}-update` | Update campaign |
| GET | `/campaign/{campaignId}-operation/{advertiserId}` | Copy/move campaign |
| DELETE | `/campaign/{campaignId}` | Delete campaign |
| GET | `/campaign/{campaignId}/banners` | Get all banners in campaign |
| GET | `/campaigns` | Get all campaigns |
| GET | `/security-settings-campaign` | Get campaign security settings |
| POST | `/security-settings-campaign-save` | Update campaign security settings |
| POST | `/security-settings-campaign-disable` | Disable campaign security settings |

### Campaign Limits API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/campaign-limits` | Get campaign limits |
| POST | `/campaign-limits` | Set campaign limits |
| POST | `/campaign-limits-update` | Update campaign limits |
| DELETE | `/campaign-limits-reset` | Reset campaign limits |
| DELETE | `/campaign-limits-disable` | Disable campaign limits |

### Campaign Targeting API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/campaign-targeting-enable` | Enable targeting for campaign |
| GET | `/campaign-targeting` | Get targeting by ID |
| GET | `/campaign-targetings` | Get all targetings for campaign |
| GET | `/campaign-targeting-types` | Get available targeting types |
| DELETE | `/campaign-targeting` | Remove targeting rule |
| POST | `/campaign-targeting-disable` | Disable targeting |
| GET | `/campaign/{campaignId}/targeting/browsers-values` | Get browsers for targeting |
| POST | `/campaign/{campaignId}/targeting/browser-create` | Create browser targeting |
| POST | `/campaign/{campaignId}/targeting/channel-create` | Create channel targeting |
| POST | `/campaign/{campaignId}/targeting/cookie-create` | Create cookie targeting |

### Action Management API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/actions` | Get all available actions (conversions) |
| GET | `/action-by-actionkey` | Get action by key |
| POST | `/action` | Create or update an action |
| DELETE | `/action` | Delete an action |
| POST | `/actions-campaign` | Enable actions for campaign |
| GET | `/actions-campaign` | Get actions for campaign |
| POST | `/actions-campaign-disable` | Disable actions for campaign |

### Template Management API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/template-list` | Get all templates |
| POST | `/template-import` | Import a template |
| GET | `/template/{templateId}-properties` | Get template properties |

### Ad Serving API (Placement)

**Base URL**: `https://your-adserver.epom.com/ads-api-v3`

**Method**: GET

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `key` | Yes | string | Placement key (from zone settings) |
| `clientIp` | Yes | string | End-user IP address |
| `requestUrl` | Yes | string | Page URL where ad appears |
| `format` | No | string | Response format: `html`, `json`, `jsonp`, `xml`, `xml-bids` (default: html) |
| `requestRef` | No | string | Referrer URL |
| `clientUa` | No | string | User-Agent string |
| `maxBids` | No | string | Number of banners for xml-bids format (default: 1) |
| `callback` | No | string | JSONP callback function name |
| `tz` | No | string | Client timezone |
| `latitude` | No | string | Client latitude |
| `longitude` | No | string | Client longitude |
| `didsha1` | No | string | SHA1-hashed device ID |
| `didmd5` | No | string | MD5-hashed device ID |
| `dpidsha1` | No | string | SHA1-hashed platform ID (Android ID/UDID) |
| `dpidmd5` | No | string | MD5-hashed platform ID |
| `model` | No | string | Device model (e.g., "iPhone") |
| `make` | No | string | Device make (e.g., "Apple") |
| `devicetype` | No | integer | 1=Mobile, 2=PC, 3=Connected TV |
| `clientOs` | No | string | Operating system |
| `osv` | No | string | OS version |
| `apn` | No | string | App package name (mobile apps) |

**Response codes**: 200 (success), 401 (auth error), 403 (insufficient permissions)

## Gaps

The following API categories exist but their endpoint details were truncated during documentation fetch:

- **Banner Management API** — CRUD for creative assets (banners)
- **Publisher Management API** — CRUD for publishers and sites
- **Zone/Placement Management API** — CRUD for zones and placements
- **User Management API** — account and role management

For complete endpoint documentation, visit: https://help.epom.com/reference

## Pagination

Pagination pattern not explicitly documented in fetched pages. For large result sets, check response metadata for pagination fields. Contact Epom support for guidance on paginating Analytics API responses.

## Rate Limits

Epom describes "high-frequency usage with generous rate thresholds" — specific limits are adjustable per account. No standard rate limit headers documented. Contact Epom support to adjust limits if you hit throttling.

## Error Response Shape

<!-- Constructed from docs — verify against live API -->
```json
{
  "error": {
    "code": 401,
    "message": "Unauthorized – authentication error."
  }
}
```

**Auth-error triage (verified 2026-06-13):** A 401 almost always means the MD5 hash was computed
wrong. Recompute as `MD5(MD5(password) + timestamp)` for analytics/management endpoints, use a
**fresh UNIX-milliseconds** timestamp (not seconds), and place `username`/`hash`/`timestamp` in the
URL **path** (with `.do` suffix), not the query string.

## SDKs & Developer Tools

- **No official SDKs** documented (no npm, pip, or Maven packages found)
- **No Postman collection** found
- **No OpenAPI/Swagger spec** publicly available
- **VAST Inspector** tool available at epom.com for testing video ad tags
- **GitHub**: https://github.com/epom (organization exists but limited public repos)
