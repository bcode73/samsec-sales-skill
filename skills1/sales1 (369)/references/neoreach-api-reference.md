# NeoReach API Reference

## Overview

NeoReach provides a REST API for integrating influencer data into enterprise applications. Per the official API page (neoreach.com/api/): "Seamlessly integrate our social insights with your enterprise application via a standard REST API which accepts standard parameters to return JSON data." The API exposes 400+ custom data points / "400+ network endpoints" and access to "creator data, network stats, hashtag trends, content trends, demographics, insights, sponsorship data, brand data, and 100+ NeoReach custom endpoints."

**Supported platforms** (per official API page): YouTube, Twitter, Instagram, Facebook, Twitch, and TikTok.

**Important**: NeoReach does not publish public/self-serve API documentation (no Swagger/OpenAPI). API access, specs, authentication details, and endpoint documentation are provided only after a sales conversation (enterprise/Platform & API tier). The official API page lists capabilities and endpoint categories but no auth/base-URL/rate-limit details — those are shared during onboarding. Contact: team@neoreach.com. The information below combines the official API page with marketing materials and may not reflect the full API surface.

## Authentication

- **Method**: Not publicly documented — likely API key or OAuth (confirmed during onboarding)
- **Base URL**: Not publicly documented
- **Rate limits**: Not publicly documented

## Endpoint categories

The official API page (neoreach.com/api/) groups the API surface into four named endpoint categories:

- **Social Profile Information** end-points
- **Social Profile Analytics** end-points
- **Social Post** end-points
- **Social Audience** end-points

These cover the "mix and match" datasets used to assemble custom queries. Exact endpoint paths, HTTP methods, and parameters are not published and are provided during onboarding.

## Known API capabilities

Based on NeoReach's official API page and marketing materials, the API provides access to:

### Creator data
- Creator profiles and network statistics
- Hashtag and content trends
- Audience demographics and insights
- 100+ NeoReach custom data endpoints

### Sponsorship intelligence
- Sponsorship pricing data (historical and current)
- Historical price and ROI data for benchmarking
- Competitor spend analysis

### Discovery and matching
- Audience matching (find creators whose audience matches target demographics)
- Fast-growing influencer tracking (identify rising creators)
- Brand affinity data

### Fraud detection
- Programmatic access to fraud scoring
- Fake follower detection via API
- Engagement authenticity scoring

### Data integration
- 400+ custom data points for in-house tool integration
- JSON response format
- Standard REST parameters

## Integration patterns

### Dashboard integration
Pull NeoReach data into internal BI tools (Tableau, Looker, custom dashboards) for unified reporting across marketing channels.

### CRM enrichment
Enrich creator records in your CRM with NeoReach audience data, fraud scores, and historical performance metrics.

### Automated workflows
Use API data to trigger workflows — e.g., auto-flag creators whose fraud score exceeds a threshold, or auto-add rising creators to watchlists.

## Getting started

1. Contact NeoReach sales (team@neoreach.com / "Let's Chat!" on the API page) to discuss API access — API Access is listed under the Platform & API offering (asterisk indicates conditional availability) and the Enterprise offering
2. Request API documentation and sandbox/staging environment
3. Plan a proof-of-concept with a small subset of endpoints
4. Validate data quality and response formats before building production integrations

## Gaps

- No public Swagger/OpenAPI spec
- No documented SDKs or client libraries
- No webhook support documented
- No rate limit information available
- Authentication method not publicly disclosed
