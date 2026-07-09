<!-- Source: https://docs.buysellads.com/advertiser-api, https://docs.buysellads.com/advertiser-api/endpoints, https://docs.buysellads.com/ad-serving-api -->

# BuySellAds API Reference

## Authentication

All API requests require HTTPS. The Advertiser API uses private key authentication — append your API key as a URL parameter: `?key=YOUR_API_KEY`.

To obtain an API key, contact your BuySellAds account manager. Keys cannot be self-generated.

All dates use UTC timezone.

## Error responses

| Status | Meaning |
|---|---|
| 200 | Success with requested data |
| 400 | Bad request — invalid or missing API key |
| 401 | Unauthorized — `{"response": {"error": "HTTP Error 401 Unauthorized"}}` |
| 404 | Endpoint not found |

---

## Advertiser API

**Base URL:** `https://papi.buysellads.com`

No pagination — endpoints return all matching records. Use `startDate` and `endDate` to limit results.

### GET /lineitems

Returns details for all active line items in the current month.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | API authentication key |
| `startDate` | string | No | `yyyy-mm-dd` format |
| `endDate` | string | No | `yyyy-mm-dd` format |
| `type` | string | No | Set to `csv` for CSV output |

**Example request:**
```
GET https://papi.buysellads.com/lineitems?key=api_test&startDate=2020-09-01&endDate=2020-09-30
```

**Response fields:** `lineitem_id`, `lineitem_name`, `order_id`, `order_name`, `placements`, `paused`, `goal_unit`, `goal_quantity`, `unit_cost`, `ratified`, `budget`, `notes`, `scheduled_start`, `scheduled_end`, `scheduled_start_iso`, `scheduled_end_iso`

### GET /daily-stats

Returns stats by day for all active line items in the current month.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | API authentication key |
| `lineitemId` | int | No | Filter to a specific line item |
| `startDate` | string | No | `yyyy-mm-dd` format |
| `endDate` | string | No | `yyyy-mm-dd` format |
| `type` | string | No | Set to `csv` for CSV output |

**Example request:**
```
GET https://papi.buysellads.com/daily-stats?key=api_test&startDate=2020-09-01&endDate=2020-09-30
```

**Response fields:** `lineitem_id`, `lineitem_name`, `order_id`, `order_name`, `placements`, `date`, `impressions`, `clicks`, `ctr`, `spend`, `notes`

### GET /creatives

Returns creative stats for all line items in the current month.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | API authentication key |
| `lineitemId` | int | No | Filter to a specific line item |
| `startDate` | string | No | `yyyy-mm-dd` format |
| `endDate` | string | No | `yyyy-mm-dd` format |
| `type` | string | No | Set to `csv` for CSV output |

**Example request:**
```
GET https://papi.buysellads.com/creatives?key=api_test&startDate=2020-09-01&endDate=2020-09-30
```

**Response fields:** `order_name`, `order_id`, `lineitem_id`, `lineitem_name`, `creative_id`, `link`, `weight`, `impressions`, `clicks`, `ctr`, `spend`, `image`, `small_image`, `description`, `company_tagline`, `tracking_pixel`

### GET /creatives-daily-stats

Returns creative stats by day for all line items in the current month.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | API authentication key |
| `lineitemId` | int | No | Filter to a specific line item |
| `startDate` | string | No | `yyyy-mm-dd` format |
| `endDate` | string | No | `yyyy-mm-dd` format |
| `type` | string | No | Set to `csv` for CSV output |

**Example request:**
```
GET https://papi.buysellads.com/creatives-daily-stats?key=api_test&startDate=2020-09-01&endDate=2020-09-30
```

**Response fields:** `order_name`, `order_id`, `lineitem_id`, `lineitem_name`, `creative_id`, `date`, `link`, `weight`, `impressions`, `clicks`, `ctr`, `spend`, `image`, `small_image`, `description`, `company_tagline`, `tracking_pixel`

---

## Ad Serving API

**Base URL:** `https://srv.buysellads.com/ads/{zonekey}.json`

Used by publishers to serve ads on websites and in newsletters.

### GET /ads/{zonekey}.json

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `useragent` | string | Yes | URL-encoded browser user agent of the viewer |
| `forwardedip` | string | Yes | IPv4 address of the viewer (not your server IP) |
| `ignore` | string | No | Set to `yes` for test mode (impressions not counted) |
| `callback` | string | No | Function name for JSONP response |
| `embedassets` | string | No | Set to `yes` for base64-encoded images instead of URLs |

**Example request:**
```
GET https://srv.buysellads.com/ads/CVADC53U.json?ignore=yes&forwardedip=1.2.3.4&useragent=Mozilla%2F5.0
```

**Test zone key:** `CVADC53U`

**Response:** Returns an `ads` array. When no ad is available the response includes a top-level `zonekey` field (and the ad object omits `statlink`) — treat missing `statlink` / presence of `zonekey` as "no ad, show fallback." Each ad object contains:
- `statlink` — click tracking URL (**check this exists before rendering; if missing, no ad available**)
- `statimp` — impression tracking URL
- `longlink` — email-safe click tracking path (prefix with `https://srv.buysellads.com/ads/long/x/`)
- `longimp` — email-safe impression tracking path (prefix with `https://srv.buysellads.com/ads/long/x/`)
- `description` — ad copy text
- `company` — advertiser company name
- `callToAction` — CTA button text
- `image` — ad image URL
- `logo` — advertiser logo URL
- `backgroundColor` — hex color
- `textColor` — hex color
- `pixel` — third-party tracking pixels, `||`-separated. Replace `[timestamp]` with current epoch time.

### Email-specific endpoint

For newsletter integrations (e.g., Buttondown):
```
GET https://srv.buysellads.com/ads/get/ids/{zonekey}.json
```

Returns the same structure but formatted for ESP template consumption.

Multiple zones can be batched in one request, semicolon-separated:
```
GET https://srv.buysellads.com/ads/get/ids/ZONEID1;ZONEID2.json?ignore=yes
```

**Limitation:** This is **not** a per-email-sent integration. The ad is pulled once at send/runtime and the same ad fetched for each zone is displayed to all subscribers in that send — there is no per-recipient ad rotation through this endpoint.

---

## Optimize (JavaScript)

Optimize is BuySellAds' programmatic/header-bidding publisher product. Beyond the dashboard it exposes a **client-side JS API** via the `window.optimize` global. (Docs: https://docs.buysellads.com/optimize)

### Install

A single async loader script is added once per page before `</head>`, then zone divs reference the zone ID:
```html
<div id="bsa-zone_[YOUR_ZONE_ID]"></div>
```

### Single-page apps

Refresh ads on route change:
```js
window.optimize.queue.push(() => { window.optimize.pushAll() })
```

### Events

Register with `window.optimize.addEventListener(eventType, eventListener)`:

| Event | Fires when |
|---|---|
| `rewardedSlotReady` | A rewarded-slot ad is ready to be made visible (provides a function to display the ad) |
| `rewardedSlotGranted` | A rewarded-slot reward has been granted (payload carries reward amount and type) |
| `rewardedSlotClosed` | A rewarded-slot ad has been closed |

### Advanced functions

`push` / `pushAll` (push ads into containers on new page loads) and `refresh` (refresh ad containers otherwise) — only needed when you want manual control over loading.

### Identifier (email hashing)

Hashed email values are passed to the frontend via the `window.optimizeIdentityHashes` JS variable, using client-side hashing with the native Web Crypto API.

---

## Monetization Framework (JavaScript)

Client-side JS library for website ad integration. Provides a `_bsa` global object.

### Methods

| Method | Description |
|---|---|
| `_bsa.init(type, zoneKey, options)` | Load a single ad unit on the page |
| `_bsa.initBatch(type, zoneKey, options)` | Queue an ad request for batch loading |
| `_bsa.loadBatch()` | Execute all queued batch requests as one network call |
| `_bsa.reload('#containerId')` | Refresh/reload a specific ad by container selector |
| `_bsa.close('containerId', timeInMs)` | Hide an ad for a duration (default: 6 hours) |

---

## Zapier Integration

**Triggers:**
- Deal sent
- Deal marked as won
- Spot sold via Self-Serve Direct or Marketplace

No Zapier actions documented (BSA is trigger-only).

---

## Gaps

- **Rate limits**: Not documented in public API docs
- **Webhook support**: None found — use Zapier triggers as workaround
- **Campaign creation API**: Does not exist — campaigns are created via UI or managed by BSA team
- **Make/n8n integration**: None found
- **MCP server**: None found
- **Publisher API**: No endpoints for publishers to manage zones, view revenue, or configure settings programmatically
- **AI assistants**: The docs site publishes an `llms.txt` index for AI coding assistants (documentation index, not an API spec)
