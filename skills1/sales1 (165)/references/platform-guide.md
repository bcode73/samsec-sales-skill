# Epom Platform Reference

## Overview

Epom is a hosted ad server and white-label DSP founded in 2010, serving 350+ clients across 40+ countries. It manages direct ad deals and programmatic inventory across web, mobile, in-app, and CTV channels. Primary differentiator: the REST API and dedicated support are included on every plan, and pricing scales by impressions with full feature parity across tiers. Note (verified 2026-06-13): full white-label branding, premium support, advanced analytics, and the SSP module are **paid add-ons** on the Ad Server — they are not bundled into the base plans.

## Capabilities & automation surface

| Module | What it does | Automation |
|--------|-------------|------------|
| **Ad Server** | Direct campaign management — advertisers, campaigns, banners, zones, targeting | API-accessible (full CRUD) |
| **DSP** | Programmatic buying — 50+ traffic sources, web/app/CTV | API-accessible (campaign management) |
| **SSP/RTB** | Sell inventory programmatically via real-time bidding | API-accessible (zone configuration) |
| **Analytics** | 40+ real-time and historical metrics, custom reports | API-accessible (report generation, export) |
| **Targeting** | Geo, device, browser, OS, channel, cookie, custom rules | API-accessible (rule CRUD) |
| **Auto-optimization** | CPA, CTR, eCPM optimization with eCPM weighting | UI-only (configure optimization goals) |
| **White-labeling** | Full brand customization — domain, logo, colors | UI-only (paid add-on, $250/mo) |
| **Referral program** | 13% revenue share for referred ad network clients | UI-only |
| **Brand safety** | Pixalate integration for fraud protection | UI-only (toggle in settings) |
| **Rich media templates** | 50+ pre-set templates for display, HTML5, native, video | UI-only (template library) |

## Pricing, limits & plan gates

### Ad Server

**Tiered pricing (verified 2026-06-13 from epom.com/pricing).** All plans carry an identical core
feature set and differ only by impression capacity. Annual billing saves ~15%.

| Plan | Price | Display + mobile-web impressions/mo | Video + HTML5 impressions/mo |
|------|-------|--------------------------------------|------------------------------|
| Light | from $250/mo | 8.5M | 250K |
| Growth | from $1000/mo | 40M | 2M |
| Pro | from $2500/mo | 150M | 7M |
| Enterprise | Custom ("Let's Talk") | Unlimited | Unlimited |

**Paid add-ons (NOT included in base plans — verified 2026-06-13):**

| Add-on | Price |
|--------|-------|
| White-label | $250/mo |
| Premium Support | $250/mo |
| Advanced Analytics | $500/mo |
| SSP Module | $0.001 per 1,000 requests |

> Correction (2026-06-13): white-labeling, premium support, advanced analytics, and the SSP module
> are **paid add-ons**, not bundled on all plans. The REST API and basic dedicated support are
> included in every plan; full white-label branding and premium support are billed separately.

| Feature | Included |
|---------|----------|
| Starting price | from $250/mo (Light) |
| Cost per 10M impressions | ~$224/mo (legacy comparison data — Light tier covers 8.5M) |
| API access | Included on all plans |
| RTB / SSP module | Paid add-on ($0.001 per 1,000 requests) |
| White-labeling | Paid add-on ($250/mo) |
| Support | Dedicated support included; Premium Support is a $250/mo add-on |
| Free trial | 14 days, 30M monthly impressions |
| Ad formats | Display, HTML5, native, video (VAST 4.3), rich media |
| Compliance | IAB, TCF 2.3 |
| Uptime SLA | 99.95% |
| Avg response time | 13ms |

### DSP

| Plan | Price | Capacity | Extras |
|------|-------|----------|--------|
| Light | $250/mo or 5% spend (whichever higher) | 5,000 QPS | 50+ SSPs, white-label, bidding autopilot, retargeting |
| Pro | $2,000/mo or 5% spend (whichever higher) | 5,000 QPS | + Custom SSP setup, bidstream data export, custom targeting |
| Enterprise | Custom | Unlimited QPS | + Priority support, custom feature development |

One-time $500 setup fee may apply. Recommended minimum ad spend: $2,000/mo for optimal results.

### Compared to competitors

| Feature | Epom | AdButler | Kevel |
|---------|------|----------|-------|
| Entry price | from $250/mo (Light, 8.5M impr) | ~$682/mo for 10M | Custom (enterprise) |
| API access | Included | Paid add-on | Included |
| RTB / SSP module | Paid add-on ($0.001/1k requests) | Paid add-on | N/A (API-first) |
| White-labeling | Paid add-on ($250/mo) | Not explicitly offered | N/A |
| Geo-targeting | Included | Paid add-on | Included |
| Support | All plans | Paid add-on on some tiers | Included |
| Self-serve portal | No | Yes | No (you build it) |
| MCP server | No | Yes | No |
| Email ad zones | Yes (image-only) | Yes (image-only) | Yes (image-only) |

## Integrations

- **CRM**: HubSpot, Salesforce (via API data export)
- **BI tools**: Tableau, Looker (via Analytics API export — HTML, CSV, PDF, XLSX, JSON)
- **DSP connections**: 50+ SSPs on the DSP side
- **Consent management**: TCF 2.3 compliant
- **Brand safety**: Pixalate integration
- **Audience data**: Lotame (DSP only)
- **No Zapier/Make** — API-only automation
- **No webhooks** documented
- **No MCP server**

## Data model

### Campaign hierarchy

```
Network Account
  └── Advertiser (company buying ads)
        └── Campaign (ad initiative with budget, dates, pricing model)
              └── Banner (creative asset — image, HTML5, video, rich media)

Publisher (site owner selling inventory)
  └── Site (website or app)
        └── Zone (ad placement on a page — header, sidebar, in-content)
              └── Placement (specific zone instance with targeting rules)
```

### Key objects (JSON shapes)

#### Advertiser
<!-- Constructed from docs — verify against live API -->
```json
{
  "id": 12345,
  "name": "Acme Corp",
  "contactName": "Jane Smith",
  "email": "jane@acme.com",
  "status": "active",
  "categoryId": 3,
  "shares": {
    "revenueShare": 0.7
  }
}
```

#### Campaign
<!-- Constructed from docs — verify against live API -->
```json
{
  "id": 67890,
  "advertiserId": 12345,
  "name": "Q1 Display Campaign",
  "status": "active",
  "startDate": "2026-01-01",
  "endDate": "2026-03-31",
  "pricingModel": "CPM",
  "price": 5.00,
  "budget": 10000.00,
  "impressionsLimit": 2000000,
  "clicksLimit": 50000,
  "securitySettings": {
    "enabled": true
  }
}
```

#### Analytics Report Response
<!-- Constructed from docs — verify against live API -->
```json
{
  "data": [
    {
      "date": "2026-01-15",
      "campaignId": 67890,
      "impressions": 45230,
      "clicks": 1205,
      "conversions": 34,
      "spend": 226.15,
      "eCPM": 5.00,
      "ctr": 0.0266,
      "cvr": 0.0282
    }
  ],
  "totals": {
    "impressions": 45230,
    "clicks": 1205,
    "conversions": 34,
    "spend": 226.15
  }
}
```

## Quick-start recipes

### Recipe 1: Create an advertiser and campaign via API

**Use case**: Automate campaign setup when a new sponsor signs up.

> Auth note (verified 2026-06-13): Epom auth is **MD5**, not HMAC — `hash = MD5(MD5(password) + timestamp)`,
> the `timestamp` is UNIX **milliseconds**, and `username`/`hash`/`timestamp` are URL **path** segments on
> `.do` endpoints (see the API reference). The JSON-body / query-string forms below are illustrative of the
> payload fields only; substitute the verified path-parameter auth and a real MD5 hash (`epom_hash()` in the
> Python helper). The exact advertiser/campaign management endpoint paths were not directly re-verified —
> confirm against help.epom.com/reference before relying on them.

**cURL**:
```bash
# Step 1: Create advertiser
curl -X POST "https://your-adserver.epom.com/rest-api/advertisers-update" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "hash": "MD5_HASH",
    "timestamp": "1716000000000",
    "name": "Acme Corp",
    "contactName": "Jane Smith",
    "email": "jane@acme.com"
  }'

# Step 2: Create campaign for that advertiser
curl -X POST "https://your-adserver.epom.com/rest-api/campaign-create" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "hash": "MD5_HASH",
    "timestamp": "1716000000000",
    "advertiserId": 12345,
    "name": "Q1 Display Campaign",
    "pricingModel": "CPM",
    "price": 5.00,
    "startDate": "2026-01-01",
    "endDate": "2026-03-31"
  }'
```

**Python**:
```python
import hashlib, time, requests

BASE = "https://n9999.epom.com/rest-api"   # your nXXXX subdomain or white-label domain
USERNAME = "your_username"
PASSWORD = "your_password"

def epom_hash():
    # VERIFIED: timestamp is UNIX MILLISECONDS; hash = MD5(MD5(password) + timestamp)
    ts = str(int(time.time() * 1000))
    pwd_md5 = hashlib.md5(PASSWORD.encode()).hexdigest()
    h = hashlib.md5((pwd_md5 + ts).encode()).hexdigest()
    return USERNAME, h, ts

# Auth credentials go in the URL PATH with a .do suffix (not the query string / not a header).
u, h, ts = epom_hash()
resp = requests.get(f"{BASE}/advertisers/{u}/{h}/{ts}.do")
print(resp.json())
```

**Gotcha**: Auth is **MD5**, not HMAC. The `hash` and `timestamp` (UNIX **milliseconds**) go in the
URL path and the endpoint ends in `.do`. Recompute the hash for every request; stale timestamps are
rejected. (The exact path segments per resource come from help.epom.com/reference — analytics is the
canonical example: `/rest-api/analytics/{format}/{username}/{hash}/{timestamp}.do`.)

### Recipe 2: Pull analytics report into a dashboard

**Use case**: Export campaign metrics to Tableau, Looker, or a custom dashboard.

**cURL** (verified path-param + `.do` form; auth in the path, not the query string):
```bash
# range=CUSTOM uses customFrom/customTo (YYYY-MM-DD); format is one of HTML/CSV/PDF/XLSX/JSON
curl "https://n9999.epom.com/rest-api/analytics/JSON/your_username/MD5_HASH/1716000000000.do?\
range=CUSTOM&customFrom=2026-01-01&customTo=2026-01-31&\
groupBy=CAMPAIGN&groupRange=DAY"
```

**Python**:
```python
u, h, ts = epom_hash()
resp = requests.get(
    f"{BASE}/analytics/JSON/{u}/{h}/{ts}.do",
    params={
        "range": "CUSTOM",
        "customFrom": "2026-01-01",
        "customTo": "2026-01-31",
        "groupBy": "CAMPAIGN",     # SITE / ZONE / CAMPAIGN / COUNTRY / ...
        "groupRange": "DAY",       # NONE / HOUR / DAY / MONTH / YEAR
        # "statisticType": "IMPRESSIONS_LOG",  # optional: HADOOP_ADREQUESTS / IMPRESSIONS_LOG / CLICKS_LOG / CONVERSIONS_LOG
    },
)
for row in resp.json()["data"]:
    print(f"Campaign {row['campaignId']}: {row['impressions']} impr, {row['clicks']} clicks, ${row['spend']:.2f}")
```

**Gotcha**: Use `range`/`customFrom`/`customTo`/`groupBy` (verified param names) — not `dateFrom`/`dateTo`/`metrics`. The report returns 40+ metric columns; `groupBy` and `statisticType` shape it. Use `limit`/`offset` to paginate.

### Recipe 3: Serve an ad via placement API (email/web)

**Use case**: Request an ad for a newsletter or web placement.

**cURL**:
```bash
curl "https://your-adserver.epom.com/ads-api-v3?\
key=PLACEMENT_KEY&\
clientIp=203.0.113.42&\
requestUrl=https://myblog.com/article-1&\
format=json"
```

**Python**:
```python
resp = requests.get("https://your-adserver.epom.com/ads-api-v3", params={
    "key": "PLACEMENT_KEY",
    "clientIp": "203.0.113.42",
    "requestUrl": "https://myblog.com/article-1",
    "format": "json"
})
ad = resp.json()
# Insert ad["html"] or ad["imageUrl"] into your template
print(ad)
```

**Gotcha**: For email ads, use `format=json` and extract the image URL. Append a unique subscriber ID to the image URL to prevent Gmail from caching the same image across recipients.

## Integration patterns

### CRM/BI sync architecture

1. **Pull pattern**: Schedule Analytics API calls (hourly/daily) to export metrics. Filter by campaign, advertiser, geo, device, or date range.
2. **Export formats**: HTML, CSV, PDF, XLSX, JSON (verified — note XLSX, not XLS) — choose based on your BI tool's import capabilities.
3. **Field mapping**: Map Epom's `advertiserId` to your CRM's company record. Map `campaignId` to deal or opportunity.
4. **No webhooks**: Epom doesn't support push-based notifications. All integrations must poll the API.

### Batch pipeline pattern

1. **Pagination**: The Analytics report endpoint supports `limit` and `offset` query parameters (verified) — page through large datasets with these.
2. **Rate limits**: "High-frequency usage with generous rate thresholds" — specific limits adjustable per use case. Contact Epom support if you hit limits.
3. **Error handling**: 401 = auth error (recompute hash), 403 = permissions (check role), 200 = success.
4. **Retry strategy**: On 5xx errors, retry with exponential backoff (1s, 2s, 4s). On 401, recompute the MD5 hash with a fresh UNIX-milliseconds timestamp.
