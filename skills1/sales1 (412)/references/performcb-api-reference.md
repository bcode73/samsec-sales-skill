# Perform[cb] Partner API Reference

## Overview

The Perform[cb] Partner API enables affiliates to automate campaign discovery, link generation, suppression list management, and reporting. Available in JSON and XML formats.

## Authentication

- **Method**: API Key + Account ID (query parameters)
- **Credentials location**: In the platform, click the three vertical dots next to your name (top-right) → your **Account ID** and **API Key**
- **Parameters**: `api_key` and `user_id` on every request
  - IMPORTANT: the parameter name carrying the Account ID value is **`user_id`** (not `account_id`). Verified against the official partner docs example URL on 2026-06-13.

## Base URL

```
https://login.performcb.com/api/v7/performcb_api
```

The API is a single base endpoint; the operation is selected with the `get=` query parameter (e.g. `get=findMyApprovedCampaigns`).

## Endpoints

### FindMyApprovedCampaigns (v7)

Retrieve all campaigns you're approved to run — "links to start running traffic ASAP."

**Example request (verbatim from official partner docs):**
```
https://login.performcb.com/api/v7/performcb_api?get=findMyApprovedCampaigns&api_key=API_KEY&user_id=ACCOUNT_ID&status=active&campaign_type=cpi,cpe&contain[]=CampaignUrl&contain[]=TrackingLink&contain[]=Country&trackinglink_traffic_type=TRAFFIC_TYPE&page=1&paginate_by=1000
```

**Parameters:**
- `get` (required) — operation selector, e.g. `findMyApprovedCampaigns`
- `api_key` (required) — your API key
- `user_id` (required) — your account ID
- `status` — filter by campaign status (e.g. `active`)
- `campaign_type` — filter by pricing model; comma-separated (e.g. `cpi,cpe`)
- `trackinglink_traffic_type` — filter by allowed traffic type
- `contain[]` — repeatable field-selector to limit/expand the returned fields (e.g. `contain[]=CampaignUrl`, `contain[]=TrackingLink`, `contain[]=Country`)
- `page` — pagination page number (default: 1)
- `paginate_by` — results per page (default: 1000)

**Response fields** (sample): `id`, `name`, `description`, `preview_url`, `status`, `campaign_operating_system`, `Country`, `pricing_model`, `TrackingLink`, plus events, allowed/blocked traffic types, and payouts (first commissionable, main conversion, event-level).

### Create Links

Generate tracking links for approved campaigns.

### Pull Suppression Lists

Retrieve suppression/exclusion lists for compliance and targeting.

### Pull Reports

Access reporting data programmatically — conversions, clicks, revenue, by date range and segmentation.

### Campaign management (pause / change rates)

Per Perform[cb], the Partner API can also **automate campaign setups, pauses, and rate changes** — e.g. turn off media buying when an offer runs out of daily/weekly budget and automatically resume once new budget is allotted. (Capability is documented in Perform[cb] content; exact endpoint/parameter names are in the login-gated API documentation library.)

## Data Formats

- **JSON** (recommended for modern integrations)
- **XML** (legacy support)

## Pagination

Use `page` and `paginate_by` parameters:
```
?page=1&paginate_by=1000
```

## Rate Limits

Not publicly documented. Best practice: cache campaign data locally and refresh periodically (daily or hourly) rather than making real-time calls on every user request.

## Webhooks

Not publicly documented. Use postback URLs for server-to-server conversion tracking instead.

## Postback URLs

Server-to-server conversion notification. Set up in your Perform[cb] dashboard under tracking settings. Supports dynamic macros for:
- Conversion ID
- Payout amount
- Sub-ID parameters
- Event type

**Whitelist the postback source IP:** Perform[cb] postbacks originate from **`52.4.177.89`** — whitelist this IP in your tracking platform so postbacks aren't blocked (verified in the partner quick-start guide, 2026-06-13).

## Tracking-link parameters (sub-IDs)

Append these to tracking links for attribution:

**CPA traffic:**
- `subid1` — Sub Source Info
- `subid2` — ClickID
- `subid3`, `subid4` — additional sub-ID data
- `subid5` — extra variable
- `creative_id` — creative ID

**CPI/CPE app-install traffic:**
- `source_id` — source info
- `google_aid` — Android advertising ID
- `ios_ifa` — iOS IDFA

## Notes

- Full API documentation requires an active Perform[cb] account (docs are behind login at login.performcb.com)
- The API is designed primarily for affiliate partners, not advertisers
- Rate limits and webhook support may be available but aren't publicly documented — check with your Account Manager
