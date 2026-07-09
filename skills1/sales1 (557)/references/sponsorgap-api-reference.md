<!-- Source: https://sponsorgap.com — no public API documentation found -->

# SponsorGap API Reference

## Status

**No public API documentation found.** API documentation is not publicly published — it appears to be provided upon subscription or by contacting support. **Re-verified 2026-06-13 against sponsorgap.com/pricing:** API access is now tiered — **"Limited API access" starts on the Growth plan ($89/mo)** and **"Full API access" is on the Enterprise plan ($199/mo)**. (Previously the skill stated API was Business-tier-only; the tier was renamed Enterprise and a lower "Limited API" rung was added at Growth.)

## What is known

- **Access**: Limited API access from **Growth ($89/mo)**; Full API access from **Enterprise ($199/mo)** (re-verified 2026-06-13)
- **Limited vs Full**: The difference between "Limited" and "Full" API access is not documented publicly
- **Auth**: Unknown — likely API key or token-based
- **Base URL**: Unknown
- **Rate limits**: Unknown
- **Pagination**: Unknown

## Likely endpoints (inferred from UI features)

These endpoints are inferred from the platform's UI capabilities. **Do not rely on these — verify with SponsorGap support.**

| Likely endpoint | Description |
|---|---|
| Search/list brands | Query sponsor database by niche, industry, spend trend |
| Get brand details | Retrieve brand profile, sponsorship history, contacts |
| List newsletters | Search newsletters by niche, subscriber count, geography |
| Export sponsors | Bulk export sponsor data |
| Watchlist management | Add/remove brands from watchlist |

## iPaaS surface

- **Zapier**: No integration available
- **Make**: No integration available
- **MCP server**: None
- **Webhooks**: None

## Workaround options

1. **CSV export** (Pro+): Manual export for CRM import
2. **Contact SponsorGap support**: Request API documentation at Business tier
3. **Scrape the free search**: The free sponsorship search engine at sponsorgap.com provides limited brand data without authentication

## Gaps

- Full endpoint list unavailable
- Auth method undocumented
- Request/response schemas unknown
- Rate limits unknown
- Pagination pattern unknown
- Webhook support unknown (likely none)
