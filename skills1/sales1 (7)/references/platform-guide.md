# AdGlare Platform Reference

## Overview

AdGlare is a cloud-based ad server established in 2013, serving publishers, advertisers, and media agencies. Primary differentiator: premium hosted ad serving with cookieless targeting by design, 220+ serving nodes across 6 data centers, and support for display, native, VAST video, CTV, redirect, and catalog ad formats. GDPR/CCPA compliant, ISO 27001 certified.

**Important limitation**: AdGlare does NOT support email/newsletter ad zones. For email ad serving, use AdButler, AdSpeed, Broadstreet, or Revive Adserver.

## Capabilities & automation surface

| Module | What it does | Access |
|---|---|---|
| Campaign management | Create campaigns with targeting, flight dates, budgets, pacing | API-accessible (Enterprise) |
| Zone management | Create display, native, VAST, redirect, catalog zones | API-accessible (Enterprise) |
| Creative management | Upload image, HTML5, video, native creatives | API-accessible (Enterprise) |
| Workspace management | Multi-tenant workspaces for agencies | API-accessible (Enterprise) |
| Advertiser management | Create and manage advertiser accounts | API-accessible (Enterprise) |
| Ad targeting | Geo, device, OS, browser, language, time, frequency | Via campaign settings |
| Real-time reporting | Impressions, clicks, conversions, viewability, fill rates | Partial API (Enterprise) |
| Custom metrics | Personalized formulas for custom KPIs | UI-only |
| Custom dimensions | Track custom data points | Enterprise only, UI-only |
| Folders | Organize campaigns and zones | API-accessible (Enterprise) |
| Audit trails | Track all changes and actions | API-accessible (Enterprise) |
| Ad tag generation | JavaScript (async), iframe, JSON, VAST XML | UI — copy from zone settings |

## Zone types

AdGlare supports 5 zone formats:

1. **Display** — Traditional inline banners (sidebar, header, footer). Async JavaScript tags.
2. **VAST** — Video ads via VAST XML for compatible video players (pre/mid/post-roll).
3. **Redirect** — Link ads that redirect users to the landing page via HTTP 302.
4. **Native** — JSON-format ads for custom publisher rendering (title, description, image, CTA).
5. **Catalog** — Auto-generated ads from product catalog (for retail publishers).

**No email/newsletter zone type exists.**

## Pricing, limits & plan gates

<!-- Pricing is best-effort — verify at adglare.com/pricing -->

| Plan | Monthly impressions | Price/mo | Key features |
|---|---|---|---|
| Lite | 1,000,000 | €99 | Display, redirect, catalog zones; JS display ad API |
| Professional | 10,000,000 | €499 | + All Lite features, more volume, 1-year data retention |
| Enterprise | 10,000,000 | €649 | + Native ads & video (VAST/CTV), Management/Reporting/Decision APIs, custom metrics/dimensions, ML optimization, white-label, SSO, 3-year retention |
| Custom | Up to 10 billion | Contact sales | All Enterprise features, custom volume, 5-year retention |

**Plan-gated features** (per live pricing page, re-verified 2026-06-13):
- **Management API v2 / Reporting API / Ad Decision API**: Enterprise and Custom plans only. (The JavaScript display-ad API/ad tags are available on all plans.)
- **Native ads & video**: Enterprise and Custom plans only (Lite and Professional are display/redirect/catalog).
- **Custom metrics & custom dimensions, branded PDF reports, ML creative optimization, white-label, SSO**: Enterprise and Custom only.
- **Data retention**: Professional 1 year, Enterprise 3 years, Custom 5 years.

**Free trial**: 14 days, no credit card needed.

## API reference

**Base URL**: `https://{yourname}.api.adglare.app/v2` (Management API)
**Auth**: Bearer token (`Authorization: Bearer {api_key}`). API keys are created in **Settings => API Keys**, and each key can be scoped per-endpoint, per-HTTP-method, and locked to allow-listed server IPs.
**Format**: JSON request/response
**Plan requirement**: Management/Reporting/Decision APIs are Enterprise + Custom only (€649/mo+). JS display ad tags work on all plans.
**Note**: the Management API automates AdOps but does not serve ads — ad delivery uses the separate Ad Decision API.

### Authentication

```bash
curl -X GET "https://yourname.api.adglare.app/v2/workspaces" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

### Endpoints (CRUD)

| Resource | Endpoints | Key fields |
|---|---|---|
| Workspaces | GET/POST/PUT/DELETE `/workspaces` | name, timezone, currency |
| Campaigns | GET/POST/PUT/DELETE `/campaigns` (+`/{id}`) | create requires name, folder_id, ad_format (display/native/vast/redirect); PUT sets pricing {model CPM\|CPC, value}, pacing {event, period, speed, value}, delivery {start, end unix ts}, zone_ids, targeting |
| Creatives | GET/POST/PUT/DELETE `/campaigns/{id}/creatives` (+`/{id}`) | nested under campaign; create requires name, ad_type (varies by ad_format: image/code/video/zip/external, json, video/url/wrapper, url) |
| Zones | GET/POST/PUT/DELETE `/zones` (+`/{id}`) | create requires name, folder_id, ad_format; PUT sets data (display: ad_sizes/auto_refresh/lazy_loading, native: log_impression/max_ads, vast: vast_version 2.0–4.3) |
| Advertisers | CRUD available | Details in full API reference |
| Reports | GET available | Real-time, Data Shipping, Anomalies |
| Folders | CRUD available | Details in full API reference |
| Audit Trails | GET available | Details in full API reference |

### Campaign creation example

Create is minimal (name + folder + format); pricing/pacing/delivery/targeting are set on a follow-up PUT.

```bash
# 1. Create the campaign shell
curl -X POST "https://yourname.api.adglare.app/v2/campaigns" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Summer Promotion",
    "folder_id": 1,
    "ad_format": "display"
  }'

# 2. Configure it (returns the new id from step 1)
curl -X PUT "https://yourname.api.adglare.app/v2/campaigns/123" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": true,
    "zone_ids": [1],
    "pricing": { "model": "CPM", "value": 5.00 },
    "pacing":  { "event": "impressions", "period": "due_date", "speed": "spread", "value": 100000 },
    "delivery": { "start": 1717200000, "end": 1719792000 }
  }'
```

### Zone creation example

```bash
# Create the zone shell
curl -X POST "https://yourname.api.adglare.app/v2/zones" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Homepage Leaderboard",
    "folder_id": 1,
    "ad_format": "display"
  }'

# Configure format-specific data on PUT
curl -X PUT "https://yourname.api.adglare.app/v2/zones/1" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Homepage Leaderboard",
    "is_active": true,
    "folder_id": 1,
    "data": { "ad_sizes": ["728x90"], "auto_refresh": 0, "lazy_loading": true }
  }'
```

### Python quick-start

```python
import requests

BASE = "https://yourname.api.adglare.app/v2"
HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# List all campaigns
resp = requests.get(f"{BASE}/campaigns", headers=HEADERS)
campaigns = resp.json()

# Create a display zone (shell first, then configure with PUT)
zone = requests.post(f"{BASE}/zones", headers=HEADERS, json={
    "name": "Sidebar 300x250",
    "folder_id": 1,
    "ad_format": "display"
}).json()
requests.put(f"{BASE}/zones/{zone['id']}", headers=HEADERS, json={
    "name": "Sidebar 300x250",
    "is_active": True,
    "folder_id": 1,
    "data": {"ad_sizes": ["300x250"]}
})
```

### PHP helper class

AdGlare publishes a small PHP helper at `github.com/adglare/ad-server-api` (`AdGlareAPI.php`, GPL-3.0). Per its README it is scoped to **pulling statistical data** from the Ad Server API — it is not a full fluent CRUD SDK. For full automation, call the REST endpoints directly (Bearer auth + base URL above). No official SDK for other languages is published.

## Ad tag integration

### Display ad tag (async JavaScript)

```html
<!-- AdGlare async ad tag -->
<div id="adglare-zone-123"></div>
<script async src="https://yourname.adglare.app/zone/123.js"></script>
```

### Native ad (JSON endpoint)

Fetch JSON and render with your own template:

```javascript
fetch('https://yourname.adglare.app/zone/456/native')
  .then(r => r.json())
  .then(ad => {
    document.getElementById('native-ad').innerHTML = `
      <a href="${ad.click_url}">
        <img src="${ad.image}" alt="${ad.title}">
        <h3>${ad.title}</h3>
        <p>${ad.description}</p>
        <span>${ad.cta}</span>
      </a>
    `;
  });
```

### VAST video tag

Configure your video player with the VAST endpoint:

```html
<!-- JW Player example -->
<script>
jwplayer("player").setup({
  file: "https://example.com/video.mp4",
  advertising: {
    client: "vast",
    schedule: {
      preroll: { tag: "https://yourname.adglare.app/zone/789/vast" }
    }
  }
});
</script>
```

## Targeting options

- **Geo**: Country, region, city, postal code
- **Device**: Desktop, mobile, tablet
- **OS**: Windows, macOS, iOS, Android, Linux
- **Browser**: Chrome, Firefox, Safari, Edge
- **Language**: Browser language setting
- **Time**: Day-of-week, hour-of-day scheduling
- **Frequency**: Cap impressions per user per time period
- **Keywords**: Contextual keyword targeting

## Key differentiators

- **Cookieless by design** — GDPR/CCPA compliant without relying on third-party cookies
- **220+ serving nodes, 6 data centers** — low-latency global delivery
- **ISO 27001 certified** — enterprise-grade security
- **White-label capable** — custom branding for agencies
- **No email zones** — web, app, and video only (unlike AdButler, AdSpeed, Revive)

## Comparison with alternatives

| Feature | AdGlare | AdButler | AdSpeed | Revive |
|---|---|---|---|---|
| Starting price | €99/mo | $179/mo | $9.95/mo | Free (self-hosted) |
| Email newsletter zones | No | Yes | Yes | Yes |
| API access | Enterprise/Custom (€649/mo+); JS display API on all plans | All plans | All plans | All (XML-RPC) |
| Native ads | Enterprise/Custom | Yes | No | No |
| VAST/CTV video | Enterprise/Custom | Yes | Yes | Via plugin |
| Self-serve portal | No | Yes | Yes | No |
| Cookieless | Yes (by design) | Optional | No | No |
| MCP server | No | Yes | No | No |
