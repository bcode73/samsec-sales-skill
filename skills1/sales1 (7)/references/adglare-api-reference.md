<!-- Source: https://www.adglare.com/api-docs/v2/introduction -->
<!-- Source: https://www.adglare.com/api-docs/v2/campaigns -->
<!-- Source: https://www.adglare.com/api-docs/v2/zones -->
<!-- Source: https://www.adglare.com/api-docs/v2/creatives -->
<!-- Re-verified 2026-06-13 against live api-docs.adglare.com (docs moved from /docs/api to /api-docs/v2). Targeting/Reports/Advertisers/Folders/Audit Trails detail still partial on the live pages. -->

# AdGlare API v2 Reference

## Overview

- **Management API base URL**: `https://{yourname}.api.adglare.app/v2`
- **Authentication**: Bearer token — `Authorization: Bearer {api_key}`
- **API keys**: created in the dashboard under **Settings => API Keys**. Each key can be scoped per-endpoint, per-HTTP-method, and restricted to allow-listed server IPs.
- **Format**: JSON request and response bodies
- **Plan requirement**: Management API, Reporting API, and Ad Decision API are available on **Enterprise and Custom** plans only. (The JavaScript display-ad API/ad tags are available on all plans.)
- **Two APIs**: the Management API documented here automates AdOps (campaigns, creatives, zones, reports) but does **not serve ads**. Ad delivery uses the separate **Ad Decision API**.

## Status codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Bad request — invalid parameters |
| 401 | Unauthorized — invalid or missing token |
| 403 | Forbidden — plan doesn't include API access |
| 404 | Not found |
| 429 | Rate limited |
| 500 | Server error |

## Workspaces

Workspaces provide multi-tenant isolation for agencies managing multiple clients.

### List workspaces

```
GET /workspaces
```

Response:
```json
{
  "data": [
    {
      "id": 1,
      "name": "My Workspace",
      "timezone": "Europe/Amsterdam",
      "currency": "EUR"
    }
  ]
}
```

### Create workspace

```
POST /workspaces
```

Request body:
```json
{
  "name": "Client ABC",
  "timezone": "America/New_York",
  "currency": "USD"
}
```

### Update workspace

```
PUT /workspaces/{id}
```

### Delete workspace

```
DELETE /workspaces/{id}
```

## Campaigns

Campaigns contain delivery (flight) settings, pricing, pacing, and targeting.

```
GET    /campaigns           List campaigns
GET    /campaigns/{id}      Retrieve a single campaign
POST   /campaigns           Create campaign
PUT    /campaigns/{id}      Update campaign
DELETE /campaigns/{id}      Delete campaign
```

### Create campaign

```
POST /campaigns
```

**Required fields**: `name` (string), `folder_id` (integer), `ad_format` (string — one of `display`, `native`, `vast`, `redirect`).

Most settings (status, weighting, pricing, pacing, delivery window, linked zones, targeting) are then set via **Update** (PUT). Fields available on update include:

```json
{
  "name": "Summer Promotion",
  "is_active": true,
  "tier": 1,
  "weight": 10,
  "zone_ids": [1, 2],
  "conversion_tracker_id": 0,
  "advertiser_id": 123,
  "delivery": {
    "start": 1717200000,
    "end": 1719792000
  },
  "pricing": {
    "model": "CPM",
    "value": 5.00
  },
  "pacing": {
    "event": "impressions",
    "period": "due_date",
    "speed": "spread",
    "value": 100000
  },
  "targeting": []
}
```

- **delivery**: `start` / `end` are **unix timestamps** (`0` = immediate start / infinite end), not date strings.
- **pricing.model**: `CPM` or `CPC` only. The rate field is `value` (not `rate`). No CPA model is documented.
- **pacing** is an **object** (not a `"even"`/`"asap"` string): `event` = `impressions` | `clicks` | `conversions`; `period` = `due_date` | `day`; `speed` = `spread` | `asap`; `value` = integer cap.
- **targeting**: appears as an array/object on the campaign. The campaign doc shows it as `[]`; the creatives doc enumerates the targeting sub-fields (`geo`, `languages`, `keywords`, `keyvalues`, `devices`).

## Zones

Zones define where ads appear. Each zone has an `ad_format` and format-specific `data`.

```
GET    /zones           List zones
GET    /zones/{id}      Retrieve a single zone
POST   /zones           Create zone
PUT    /zones/{id}      Update zone
DELETE /zones/{id}      Delete zone
```

### Create zone

```
POST /zones
```

**Required fields**: `name` (string), `folder_id` (integer), `ad_format` (string).

The zone API documents `ad_format` values **`display`, `native`, `vast`, `redirect`**. (The product/UI also offers a 5th `catalog` format for retail product feeds — see user-guide/zones — but it is not enumerated in the zone API field description.)

```json
{
  "name": "Sidebar Banner",
  "folder_id": 1,
  "ad_format": "display"
}
```

### Update zone

```
PUT /zones/{id}
```

**Required on update**: `name`, `is_active` (boolean), `folder_id`, and `data` (object, structure varies by `ad_format`).

Format-specific `data` fields:
- **All formats**: `blocked_creatives` (array of creative IDs)
- **Display**: `ad_sizes`, `auto_refresh`, `lazy_loading`
- **Native**: `log_impression`, `max_ads`
- **VAST**: `vast_version` (supported versions 2.0 through 4.3)

### Delete zone

```
DELETE /zones/{id}
```

## Creatives

Creatives are **nested under a campaign** (not a top-level resource). They inherit the campaign's `ad_format`.

```
GET    /campaigns/{cid}/creatives           List creatives
GET    /campaigns/{cid}/creatives/{id}      Retrieve a single creative
POST   /campaigns/{cid}/creatives           Create creative
PUT    /campaigns/{cid}/creatives/{id}      Update creative
DELETE /campaigns/{cid}/creatives/{id}      Delete creative
```

### Create creative

```
POST /campaigns/{cid}/creatives
```

**Required fields**: `name` (string), `ad_type` (string). Allowed `ad_type` values depend on the parent campaign's `ad_format`:

| Campaign ad_format | Allowed `ad_type` values |
|---|---|
| display | `image`, `code`, `video`, `zip`, `external` |
| native | `json` |
| vast | `video`, `url`, `wrapper` |
| redirect | `url` |

### Update creative

```
PUT /campaigns/{cid}/creatives/{id}
```

Update fields include `name`, `is_active`, and a `data` object whose contents vary by `ad_type`, e.g.:

- `data.filehash`, `data.width`, `data.height`
- `data.landing_page`, `data.target_window`, `data.use_iframe`, `data.alt_text`
- `data.ad_verification_code`
- `delivery` (`start` / `end` unix timestamps)
- `targeting` (`geo`, `languages`, `keywords`, `keyvalues`, `devices`)

### Delete creative

```
DELETE /campaigns/{cid}/creatives/{id}
```

## API resource groups (per live overview)

The Management API is organized into four groups:

1. **Campaign API** — Campaigns, Creatives
2. **Inventory API** — Zones
3. **Reporting API** — Real-time reports, Data Shipping (export), Anomalies (anomaly detection)
4. **Additional APIs** — Advertisers, Workspaces, Folders, Audit Trails

The following endpoints exist but their request/response schemas were not fully captured from the live pages:

- **Advertisers** — CRUD operations for advertiser accounts
- **Reports / Real-time** — Query reporting data (impressions, clicks, conversions, viewability, fill rates)
- **Data Shipping** — Export data
- **Anomalies** — Anomaly detection
- **Folders** — Organize campaigns and zones into folders
- **Audit Trails** — Track changes and actions

## PHP class

AdGlare publishes a small PHP helper class at `github.com/adglare/ad-server-api` (`AdGlareAPI.php`, GPL-3.0). Per its README it is scoped to **pulling statistical data** from the Ad Server API to your own server — it is not a full fluent CRUD SDK covering campaigns/zones/creatives. For full Management API automation, call the REST endpoints directly (Bearer auth, base URL above). No official SDK for other languages is published in the `adglare` GitHub org.

> Note: an earlier version of this reference showed a fictional `new AdGlare\Client(...)->campaigns()->list()` fluent API. That signature is **not** what `AdGlareAPI.php` exposes; treat the repo as a stats-pull helper, not a CRUD client.

## Gaps / unverified

- Rate limit specifics (requests per minute/hour) not documented on the live API pages.
- Pagination pattern not documented in fetched pages.
- Webhook support not documented (no events/payload/signing surface found).
- **Ad Decision API** (ad delivery) base path/parameters not captured — only referenced as a separate API in the overview.
- Reports / Advertisers / Folders / Audit Trails request/response schemas remain partial on the live pages.
- Exact constructor signature of `AdGlareAPI.php` not captured.
