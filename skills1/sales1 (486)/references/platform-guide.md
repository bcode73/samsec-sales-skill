# Retention.com Platform Guide

## How Retention.com works

Retention.com identifies anonymous website visitors using a tracking pixel and third-party licensed data, converting them to known contacts (email, SMS) for remarketing. Founded by Adam Robinson (also CEO of RB2B) as GetEmails, rebranded to Retention.com. Bootstrapped to $22M+ ARR serving 1,500+ ecommerce brands.

**Key differentiator from RB2B**: Retention.com is B2C/ecommerce focused (Shopify, DTC brands, publishers). RB2B is B2B focused (person-level visitor ID for sales teams). Same founder, different products.

## Products

| Product | What it does | Key metric |
|---|---|---|
| Grow | Identifies anonymous visitors → adds to email/SMS lists | Claims 10x list growth |
| Reclaim | Captures abandonment events missed by Klaviyo, Elevar, other ESPs | +250% abandonment flow revenue (claimed) |

**How identity resolution works:**
1. Install tracking pixel on your site (JavaScript snippet)
2. Retention.com matches visitors against third-party licensed data
3. Matched visitors are identified with email and/or phone
4. Identified contacts are pushed to your ESP (Klaviyo, etc.) or SMS tool (Postscript, etc.)
5. You send abandonment recovery emails/SMS or add them to marketing flows

## Pricing

As of 2026-06-13, the official pricing page (retention.com/pricing) shows a **usage-based model**, not the older annual-contract tiers:

| Detail | Value |
|---|---|
| Model | Simple, usage-based — "$0.15/email" (per identified/delivered email) |
| Contract | "No annual contracts" — "Pay monthly, cancel anytime" / "No locked-in contracts" |
| Free trial | "14-day free trial · No credit card required" |
| Flexibility | "Seasonal flexibility built in" |
| Add-on | Abandoner identification upsell: "Get 70% more flow revenue by identifying your abandoners" |

*The per-email rate replaces the previous traffic-based monthly tiers ($500/$1,000–$1,500/$2,500/mo + $300/mo a la carte) and the annual-contract / no-trial terms. Many third-party aggregators (Capterra, etc.) still cite the old annual model — the official page is authoritative. Verify current rate at signup, as usage-based pricing can change.*

## Integrations

100+ integrations including:
- **Ecommerce**: Shopify (primary), WooCommerce, BigCommerce, custom sites
- **Email**: Klaviyo (primary), Mailchimp, ActiveCampaign, Omnisend, Brevo
- **SMS**: Postscript, Attentive, Klaviyo SMS
- **CDP/Data**: Segment, Snowflake
- **Ads**: Meta, Google Ads (retargeting audiences)

## Match rates and data quality

*Set realistic expectations — these are contentious numbers:*

- **Claimed match rate**: ~35% of anonymous visitors identified
- **Independent reports**: 16-25% is more typical
- **Data source**: Third-party licensed databases (not first-party opt-in)
- **Engagement quality**: Identified contacts engage at lower rates than organic subscribers (~3% CTR vs ~12% CTR for opted-in)
- **US-only**: Identity resolution database is US-focused

## Compliance

Retention.com operates on an **implicit consent model** — visitors are identified without explicit opt-in on your site. This is legally distinct from GDPR explicit consent.

- **CCPA compliant**: Provides opt-out mechanisms and privacy portal
- **CAN-SPAM compliant**: Identified contacts can be emailed under CAN-SPAM (US)
- **Not GDPR compliant**: Do NOT use for EU/UK visitors — requires explicit consent
- **Suppression management**: Upload suppression lists via dashboard or API
- **Database opt-out**: Global suppression available at retention.com/compliance

## API quick reference

Official docs: docs.retention.com (getting-started, authentication, reference). API keys are created in-dashboard at app.retention.com/api_details (My Account > API Details).

| Detail | Value |
|---|---|
| Base URL | `https://api.retention.com/api/v1/` |
| Auth | API Key + API ID. Headers `api-id` / `api-key`, OR body/query params `api_id` / `api_key`. Both required. |
| Rate limit | Up to 5 requests/day, ~40,000 emails per request (≈200K/day), rolling 24-hour window. Not for high-frequency querying (do not fetch more often than ~every 10 min). |
| Response | JSON. Status codes: 200 success, 400 bad request, 401 unauthorized. |
| Primary use | Suppression file uploads + account custom opt-out file uploads |

### Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/suppression` | POST | Upload new emails to suppress (so R! does not pass you contacts you already have) |
| `/api/v1/custom_optouts` | POST | Upload emails of individuals you do NOT want resolved |

**Request body (both endpoints, `multipart/form-data`):**
- `file` — CSV with a single column headed `email` (or `md5`); first row may be an ignored header
- `is_md5` — boolean, default `false`; set `true` if the file contains MD5-hashed emails

### Webhooks (Grow)

Set up under Integrations > Webhook. Delivers identified Grow contacts as JSON via **POST** to your URL. Auth is via your own custom headers OR body params (no built-in HMAC signing documented). **Webhooks do NOT offer automatic suppression** — you must suppress via the API or by uploading a CSV manually.

Default Grow payload fields (legacy plans may also include name/address):
```json
{
  "email": "test@retention.com",
  "email_domain": "@retention.com",
  "first_name": "First Name",
  "last_name": "Last Name",
  "clicked_at": "Mon, 28 Nov 2022 19:47:42 UTC +00:00",
  "landing_page_url": "https://yourwebsite.com",
  "landing_page_domain": "yourwebsite.com",
  "referrer": "https://some.referralurl.com",
  "page_title": "Page Title Here"
}
```

*The API is intentionally limited (upload-only — no read/query endpoints documented) — use the dashboard or native integrations for most operations.*

## Comparison with alternatives

| Feature | Retention.com | RB2B | Customers.ai | Opensend |
|---|---|---|---|---|
| Focus | B2C ecommerce | B2B sales | B2C + B2B | B2C ecommerce |
| Identification | Email + phone | Person + company | Email + phone + name | Email + postal |
| Match rate (claimed) | ~35% | Varies | Higher accuracy claimed | Varies |
| Pricing | From $500/mo | Free tier + paid | Custom | Custom |
| Contract | Annual required | Monthly available | Varies | Varies |
| US-only | Yes | Yes (person-level) | Yes | Yes |
| Founder | Adam Robinson | Adam Robinson | Larry Kim | — |
