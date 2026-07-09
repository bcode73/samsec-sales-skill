<!-- Source: https://information.broadstreetads.com/api-documentation/, https://github.com/broadstreetads/broadstreet-api-php (src/Broadstreet.php), and https://github.com/broadstreetads/broadstreet-ruby. Endpoint/auth/base-URL details re-verified 2026-06-13 from SDK source. -->

# Broadstreet API Reference

## Authentication

Broadstreet uses access token authentication. Obtain your token from:
https://my.broadstreetads.com/access-token

The access token is passed as a **query-string parameter** (`access_token={token}`), NOT as an HTTP header. Both official SDKs append it to the request URL/params — there is no Bearer/Authorization header. (Verified 2026-06-13 against the PHP and Ruby SDK source.)

**PHP SDK auth (token via constructor, sent as `?access_token=` on every request):**
```php
$client = new Broadstreet('YOUR_ACCESS_TOKEN');
```

## Base URL

`https://api.broadstreetads.com/api/{version}/`

The version segment is a single digit, not `v1`. The two official SDKs target different versions:
- **PHP SDK** (`broadstreet-api-php`): `API_VERSION = '0'` → base `https://api.broadstreetads.com/api/0/`
- **Ruby SDK** (`broadstreet-ruby`): paths prefixed `api/1/` → base `https://api.broadstreetads.com/api/1/`

Verified 2026-06-13 from the SDK source (`_buildRequestURL()` in PHP, `Faraday.new(:url => 'https://api.broadstreetads.com')` + `api/1/...` paths in Ruby). The previously documented `https://api.broadstreetads.com/v1/` was an inferred guess and is incorrect — use `/api/0/` (PHP) or `/api/1/` (Ruby).

Full interactive API documentation is available at:
https://api.broadstreetads.com/docs/v1/

**Note**: The API docs page is JS-rendered and cannot be fetched programmatically. Access it in a browser for the complete endpoint reference.

## Known Endpoints

The PHP SDK README only documents `createAdvertisement()`, but the SDK source (`src/Broadstreet.php`) exposes a full REST surface. Endpoints below are verified from the PHP SDK source (2026-06-13). Paths are relative to the base URL (`/api/0/`).

### Advertisements

| Method | HTTP | Path |
|--------|------|------|
| `createAdvertisement()` | POST | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements` |
| `getAdvertisement()` | GET | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements/{id}` |
| `updateAdvertisement()` | PUT | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements/{id}` |
| `deleteAdvertisement()` | DELETE | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements/{id}` |
| `getAdvertisementSource()` | GET | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements/{id}/source` |
| `setAdvertisementSource()` | POST | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements/{id}/source` |
| `getAdvertisementReport()` | GET | `/networks/{network_id}/advertisers/{advertiser_id}/advertisements/{id}/records` (accepts `start_date`, `end_date`) |
| `createProof()` | POST | `/advertisements/proof` |

`createAdvertisement()` params: `$network_id`, `$advertiser_id`, `$name`, `$type`, `$params` (options array).

**Advertisement types**: `image`, `text`, and others (full list in API docs)

### Advertisers

| Method | HTTP | Path |
|--------|------|------|
| `getAdvertisers()` | GET | `/networks/{network_id}/advertisers` |
| `getAdvertiser()` | GET | `/networks/{network_id}/advertisers/{id}` |
| `createAdvertiser()` | POST | `/networks/{network_id}/advertisers` |
| `deleteAdvertiser()` | DELETE | `/networks/{network_id}/advertisers/{id}` |

### Campaigns & Placements

| Method | HTTP | Path |
|--------|------|------|
| `createCampaign()` | POST | `/networks/{network_id}/advertisers/{advertiser_id}/campaigns` |
| `deleteCampaign()` | DELETE | `/networks/{network_id}/advertisers/{advertiser_id}/campaigns/{id}` |
| `createPlacement()` | POST | `/networks/{network_id}/advertisers/{advertiser_id}/campaigns/{campaign_id}/placements` |

### Networks & Zones

| Method | HTTP | Path |
|--------|------|------|
| `getNetworks()` | GET | `/networks` |
| `getNetwork()` | GET | `/networks/{id}` |
| `createNetwork()` | POST | `/networks` |
| `getNetworkZones()` | GET | `/networks/{network_id}/zones` |
| `createZone()` | POST | `/networks/{network_id}/zones` |
| `deleteZone()` | DELETE | `/networks/{network_id}/zones/{id}` |
| `magicImport()` | GET | `/networks/{network_id}/import` |

### Account / Misc

| Method | HTTP | Path |
|--------|------|------|
| `login()` | POST | `/sessions` (returns an access token) |
| `register()` | POST | `/users` |
| `getFonts()` | GET | `/fonts` |

**Note**: Ruby SDK paths can differ from PHP (e.g. Ruby exposes `api/1/advertisers/{id}` flat, while PHP nests advertisers under a network). Confirm the exact path against the SDK you use or the browser docs.

**Example — Create image advertisement:**
```php
$ad = $client->createAdvertisement(
    $network_id,
    $advertiser_id,
    'New Ad!',
    'image',
    array(
        'image_url' => 'https://cdn.example.com/banner.jpg',
        'click_url' => 'https://advertiser.com/landing'
    )
);
echo $ad->html;  // Ready-to-use HTML snippet
echo $ad->id;    // Advertisement ID
```

### Ad Serving (Zone Tags)

**Base URL for ad serving:**
- Click URL: `https://ad.broadstreetads.com/zone/{ZONE_ID}/click/{POSITION}`
- Image URL: `https://ad.broadstreetads.com/zone/{ZONE_ID}/image/{POSITION}`

**Parameters (appended as query strings):**

| Parameter | Description |
|-----------|-------------|
| `ds=true` | Daily shuffle — randomize ad rotation daily |
| `seed={id}` | Per-user shuffle — vary by subscriber while maintaining consistency |
| `kw=keyword1,keyword2` | Keyword targeting |
| `skw=true` | Soft keywords — non-tagged ads also eligible |
| `overflow=0` | Show blank pixel when zone is empty (instead of duplicating) |

**Position numbering**: When using the same zone multiple times in one page/email, increment the position number: `/click/0`, `/click/1`, `/click/2`, etc.

## SDKs

| SDK | Language | Repository |
|-----|----------|------------|
| broadstreet-api-php | PHP | https://github.com/broadstreetads/broadstreet-api-php |
| broadstreet-ruby | Ruby | https://github.com/broadstreetads/broadstreet-ruby |

## WordPress Plugin

- **Plugin**: https://wordpress.org/plugins/broadstreet/
- **Source**: https://github.com/broadstreetads/broadstreet-wp
- Handles zone placement, ad display, and sponsored content tracking

## Gaps

The endpoint list above is recovered from the open-source SDK source (PHP + Ruby). The browser-rendered docs at api.broadstreetads.com/docs/v1/ may list additional endpoints or params not surfaced in the SDKs. The following could not be determined from public sources:

- **Request/response format** — JSON assumed from SDK patterns but not confirmed for all endpoints
- **Pagination** — pattern unknown / not documented
- **Rate limits** — not documented in official sources or SDKs
- **Webhooks** — none documented
- **Exact field schemas** — request bodies and response objects are not fully documented per endpoint
- **Version differences** — PHP SDK uses `/api/0/`, Ruby SDK uses `/api/1/`; whether `/api/0/` and `/api/1/` differ in payloads is not documented

For complete API documentation, access https://api.broadstreetads.com/docs/v1/ in a browser or contact Broadstreet support.
