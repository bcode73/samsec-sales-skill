<!-- Source: https://www.upviral.com/api (JS-rendered — captured via WebFetch summary + corroborated against apitracker.io/a/upviral, support.upviral.com, and Zapier/Make/Pipedream listings, June 2026) -->

# UpViral API Reference

> **Capture note.** UpViral's official API page (`https://www.upviral.com/api`) is JavaScript-rendered; WebFetch returns a structured summary rather than the raw HTML, so per-endpoint request/response bodies are **not** available verbatim from the source. The endpoint list, method names, base URL, and auth scheme below are reproduced faithfully from that page and corroborated against third-party developer aggregators (apitracker.io, apirefs.com), the UpViral support center, and the Zapier/Make/Pipedream app listings. Field-level JSON shapes marked "indicative" are best-effort. Do not treat indicative shapes as authoritative — verify against a live response. **Flag any gaps to the user rather than inventing fields.**

## Overview

The UpViral API is a RESTful interface for managing referral campaigns programmatically — add/read/edit contacts, award points, read custom fields, and list campaigns.

- **Base URL**: `https://app.upviral.com/api/v1/`
- **Transport**: HTTPS only. Plain-HTTP calls fail.
- **Method**: POST with form-encoded (`application/x-www-form-urlencoded`) parameters.
- **Response**: JSON.
- **Plan gate**: API access is available on **paid plans from Business upward** (Business / Premium). The Starter plan does **not** include API or webhooks. (Historical docs reference "Pro" — current plan names are Starter / Business / Premium; the API-included tier is Business and above.)

## Authentication

Authentication uses two form fields on every request (there is **no** `Authorization` header):

| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey` | Yes (all requests) | Your unique UpViral API key. Get it by creating a developer account and copying the key from the dashboard. |
| `uvmethod` | Yes (all requests) | The method/endpoint name (e.g. `add_contact`, `get_leads`). |
| `campaign_id` | Most requests | The target campaign's ID (omitted only for account-wide methods like `lists`). |

Minimal authenticated call:

```bash
curl -X POST https://app.upviral.com/api/v1/ \
  --data-urlencode "uvapikey=YOUR_API_KEY" \
  --data-urlencode "uvmethod=lists"
```

## Methods (endpoints)

All methods POST to the single base URL `https://app.upviral.com/api/v1/`; the `uvmethod` field selects the operation.

### Contact / lead management

#### `add_contact` — add a contact to a campaign
Create a new contact (lead) in a campaign, optionally with referral attribution.

| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey` | Yes | API key |
| `uvmethod` | Yes | `add_contact` |
| `campaign_id` | Yes | Target campaign |
| `email` | Yes | Contact email |
| `name` | No | Contact name |
| `ip` | No | Signup IP (used by fraud detection) |
| `referral_code` | No | The referrer's referral code, for attribution + points |
| *custom field keys* | No | Any campaign custom fields (see `get_custom_fields`) |

#### `get_lead_details` — get one contact by lead ID
| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`get_lead_details`, `campaign_id` | Yes | — |
| `lead_id` | Yes | The contact's lead ID |

Returns the contact record including points, referral code, and fraud status.

#### `get_lead_details_by_email` — get one contact by email
| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`get_lead_details_by_email`, `campaign_id` | Yes | — |
| `email` | Yes | The contact's email address |

#### `get_leads` — list all contacts (paginated)
| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`get_leads`, `campaign_id` | Yes | — |
| `start` | No | Pagination offset (0-based) |
| `size` | No | Page size |

#### `get_leads_points` — filter contacts by points
Return contacts whose point total matches an operator + threshold — the right call for reward fulfillment.

| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`get_leads_points`, `campaign_id` | Yes | — |
| `operator` | Yes | One of `<`, `>`, `=` |
| `points` | Yes | Threshold value |
| `start`, `size` | No | Pagination |

#### `add_points` — award points to a contact
Award points to a specific contact (e.g. for actions taken outside UpViral).

| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`add_points`, `campaign_id` | Yes | — |
| `lead_id` | Yes | Target contact |
| `points` | Yes | Points to add |

### Custom fields

#### `get_custom_fields` — list a campaign's custom field definitions
| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`get_custom_fields`, `campaign_id` | Yes | — |

### Campaigns

#### `lists` — list all campaigns in the account
| Param | Required | Description |
|-------|----------|-------------|
| `uvapikey`, `uvmethod`=`lists` | Yes | No `campaign_id` needed |

Returns all campaigns with IDs and names.

## Pagination

List endpoints (`get_leads`, `get_leads_points`) use offset pagination via `start` (offset) and `size` (page size). Iterate by incrementing `start` by `size` until an empty page is returned.

## Webhooks — "Callback URL"

UpViral's webhook feature is called the **Callback URL**. Configure it per campaign (Settings → the campaign). It sends data to your service when specific events occur — notably when a **lead unlocks a reward**.

- **Gate**: Business tier and above.
- **Payload**: lean (event, campaign, lead identifiers). Enrich by calling `get_lead_details` with the returned `lead_id`. Indicative shape:

```json
{
  "event": "reward_unlocked",
  "campaign_id": "123456",
  "lead_id": "987654",
  "email": "jane@example.com",
  "points": 120
}
```

- **Signing**: no documented HMAC/signature scheme. Secure with a secret path/query param, source-IP allowlisting, and re-fetch authoritative state via the API.

## iPaaS triggers/actions

- **Zapier** — triggers: **New Lead**, **New Reward Unlocked**. (Also "Webhooks by Zapier" templates for POSTing new leads.) Advanced Zapier features are Business+.
- **Make / Integromat**, **Pipedream**, **Integrately**, **Pabbly Connect** — connectors available.

## SDKs

- **PHP SDK**: `composer require upviral/php-sdk`.
- No official JavaScript/Python SDK documented — use the REST API directly.

## Rate limits

No public rate-limit documentation found. Throttle conservatively on bulk pulls (e.g. `get_leads`/`get_leads_points` pagination) and back off on errors.

## Support

- API support: `api@upviral.com`
- Support center: `https://support.upviral.com/`

## Known gaps (flag to users)

- Per-endpoint request/response JSON bodies are **not published verbatim** (page is JS-rendered) — shapes above are indicative.
- No documented rate limits.
- No documented webhook signature/HMAC scheme.
- Historical docs say "Pro" tier for API; current plans are Starter/Business/Premium with API gated at **Business+**. Confirm in-app.
- No update/delete-contact method is documented in the public listing (only add/read/points). Confirm with support if you need destructive operations.
