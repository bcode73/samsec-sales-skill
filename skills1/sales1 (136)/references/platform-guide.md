# Customers.ai Platform Reference

## Platform overview

Customers.ai (CustomersAI) is a B2C visitor identification and remarketing platform built primarily for Shopify brands using Klaviyo (Klaviyo is the lead integration and the basis for pricing). It identifies anonymous website visitors via the X-Ray pixel (claiming 60-70% identification rate vs Klaviyo's native 15-20%), scores visitor intent with the Alfred AI agent, includes the Inboxer deliverability suite to protect sender reputation, and offers Super CAPI server-side Meta conversions tracking. The platform also recovers shrinking ad retargeting audiences via first-party data for Meta, Google, and TikTok Ads. As of 2026-06-13 it also publishes native integrations for non-Klaviyo ESPs/CRMs (SendGrid, Sendlane, HighLevel, Salesforce, Mailchimp).

**Target audience**: Established Shopify brands ($500K-$2M+ GMV) with meaningful traffic volume, already running Klaviyo (or a supported ESP) with core flows in place. Not suitable for pre-revenue stores or low-traffic sites.

## Key modules

### X-Ray Pixel (Identity Resolution)

The core product. A JavaScript pixel installed on your Shopify store that identifies anonymous visitors and matches them to known consumer profiles.

- **How it works**: First-party+ data solution that extends beyond traditional cookie-based tracking. Connects customer actions across devices and browsers. When a visitor hits your site, X-Ray attempts to match them against Customers.ai's consumer database using multiple signals (IP, device fingerprinting, email hash matching, third-party data partnerships).
- **Match rate**: Claims 60-70% of site visitors identified (vs Klaviyo's 15-20%). Data accuracy between 65-85% (vs industry average of 5-30%).
- **What it captures**: Name, email, LinkedIn profile, customer journey data, cross-device browsing behavior, purchase intent signals.
- **Installation**: 10-minute setup via Shopify theme editor or Google Tag Manager. JavaScript snippet in `<head>` tag.
- **Output**: Identified visitors are synced directly to Klaviyo as profiles with full behavioral data.

### Alfred AI Agent

An AI agent that performs daily intent scoring on identified visitors.

- **Daily retraining**: Alfred analyzes all identified visitors daily and segments them into high, medium, and low purchase intent buckets.
- **Auto-suppression**: Automatically suppresses low-intent profiles in Klaviyo, reducing active contact count and ESP costs.
- **Compounding effect**: Effectiveness improves over time as Alfred trains on your specific customer behavior patterns.
- **Use case**: Reduce Klaviyo bill by only keeping high-intent identified visitors as active profiles.

### Inboxer Deliverability Suite

Four-component deliverability system included with all plans:

1. **Deliverability Booster Script**: JavaScript that optimizes email rendering and engagement signals.
2. **List Validation**: Cleans identified contacts to remove invalid/risky addresses before they enter Klaviyo flows.
3. **Inbox Warming**: Warms new domains/IPs for brands setting up dedicated sending infrastructure.
4. **Monitoring**: Tracks inbox placement rates and flags deliverability issues.

**Key claim**: Shifts emails from Promotions/Spam folders to Primary inbox. However, this is positioned as an optimization tool — it cannot fix severely damaged sender reputation.

### Ad Retargeting Audience Recovery

Recovers shrinking ad audiences caused by cookie deprecation and iOS privacy changes.

- **Supported platforms**: Meta Ads, Google Ads, TikTok Ads.
- **How it works**: Uses first-party identified visitor data to build ad audiences directly, bypassing third-party cookie limitations.
- **Benefit**: Brands that saw retargeting audiences shrink 40-60% after iOS 14.5+ can recover much of that reach.
- **Included**: On all plans alongside the free trial.

### Super CAPI (Server-Side Tracking) — NEW

A server-side conversions-tracking product for **Meta Ads** (also referred to as "Meta CAPI" on the site), added since the original skill research and now a first-class, separately-priced product in the pricing calculator alongside X-Ray and Alfred.

- **Purpose**: Send conversion events server-side to Meta to recover signal lost to browser/cookie restrictions (iOS, ad blockers), improving ad attribution and optimization.
- **Pricing**: Configured separately in the pricing calculator with sync-tier and data-retention options.
- **Relation to X-Ray**: Combines first-party identity data from X-Ray with server-side event delivery for stronger Meta Ads matching.

### Consumer Data Enrichment API

Separate API product for enriching contacts programmatically.

- **Data available**: Business and employment information, updated monthly. Can query by name, email, or phone.
- **Use case**: Enrich existing contacts or identified visitors with additional firmographic/demographic data.
- **Security**: Data encrypted before transmission.
- **Documentation**: Sparse — see `references/customersai-api-reference.md`.

## Pricing and limits

**Pricing model changed (verified 2026-06-13).** The official pricing page (customers.ai/pricing) is now a **custom calculator**, not a set of fixed published tiers. Quote: pricing "is based on your total Klaviyo profiles — every profile in your account, including suppressed and unsubscribed ones." Your quote is driven by:

- **Total Klaviyo profile count** (the primary input).
- **Product selection**: X-Ray (Identity Engine), Alfred (AI Audience Agent), and Super CAPI (Server-Side Tracking for Meta Ads) are each priced/configured separately, with signal-fidelity, sync-plan, and data-retention options.
- **Contract duration and billing period** (annual vs monthly).

There are **no longer fixed Starter/Grow/Scale plan names with public dollar amounts** on the live page — the site directs you to "Contact us for purchasing and custom pricing."

**Legacy tier reference (historical, third-party-sourced, no longer on the live pricing page):** Starter $600/mo (3,000 resolutions, $0.20 overage), Grow $900/mo (5,000, $0.18), Scale $1,500/mo (10,000, $0.15), Enterprise custom. Treat these as indicative of past resolution-based pricing only; do NOT quote them as current — the live model is profile-based and quoted by sales.

- **Free trial**: 7 days, up to 500 visitor resolutions, no credit card required (verified 2026-06-13).
- **ROI guarantee**: Customers.ai advertises an attributable-ROI-or-you-don't-pay guarantee. The number is stated inconsistently across their own pages at verification — the **pricing page says "4x ROI always guaranteed"** while the **homepage says "+5x directly attributable ROI."** Confirm the exact multiplier and attribution methodology in writing before relying on it.
- **All products include**: X-Ray pixel, Alfred AI, Inboxer suite, ad retargeting recovery, and ESP integration (Klaviyo lead, plus SendGrid/Sendlane/HighLevel/Salesforce).
- **Overage behavior**: Profile-based pricing replaces the old per-resolution overage model; per-resolution fees still apply for resolutions beyond plan allowance per sales. Monitor usage in dashboard.

**Economics check**: Pricing is now profile-based and quoted by sales rather than a published $600 entry tier, but the economics logic is unchanged — identified contacts must generate more incremental revenue than your monthly spend. With a typical ecommerce email revenue-per-contact, the platform generally needs $500K+ GMV and 50K+ monthly visitors for positive ROI; get a calculator quote tied to your actual Klaviyo profile count before committing.

## Integrations

| Integration | Type | Notes |
|---|---|---|
| **Klaviyo** | Native (primary) | Direct profile sync, behavioral data, flow triggers. Pricing is calculated off total Klaviyo profiles, so Klaviyo remains the lead ESP. |
| **Shopify** | Native | Primary commerce platform. Pixel installs via theme editor or GTM. |
| **Meta Ads** | Native | Ad retargeting audience recovery + Super CAPI server-side conversions tracking. |
| **Google Ads** | Native | Ad retargeting audience recovery. |
| **TikTok Ads** | Native | Ad retargeting audience recovery. |
| **SendGrid** | Native | Verified non-Klaviyo ESP integration (dedicated help-center article). |
| **Sendlane** | Native | Verified non-Klaviyo ESP integration (dedicated help-center article). |
| **HighLevel (GoHighLevel)** | Native | Verified CRM/ESP integration (dedicated help-center article). |
| **Salesforce** | Native | Listed as a supported connector on the Customers.ai site. |
| **Semrush / Triple Whale / Elevar / Blotout** | Native | Listed as analytics/martech connectors on the Customers.ai site. |

**ESP/CRM support is no longer Klaviyo-only.** As of 2026-06-13 verification, Customers.ai publishes dedicated integration help docs for SendGrid, Sendlane, and HighLevel, and lists Salesforce, Mailchimp, Google Sheets, and Zapier among supported connectors. Klaviyo remains the lead integration (and the basis for pricing), but it is not the sole ESP. Confirm WooCommerce / BigCommerce / custom-platform support directly — Shopify remains the primary commerce platform and no native non-Shopify commerce integration was confirmed at verification.

## Data model (API)

Legacy MobileMonkey API at `api.mobilemonkey.com`. Limited public endpoints:

- **Contact**: Identified visitor record with attributes (name, email, phone, city, custom fields). Referenced by numeric `contact_id`.
- **Update Contact**: `PATCH/PUT https://api.mobilemonkey.com/public/contacts/{contact_id}/` — update up to 10 attributes per request. Attributes must already exist.
- **Send JSON Message**: `POST https://api.mobilemonkey.com/public/contacts/{contact_id}/send_json_message` — send text, images, quick replies, galleries.
- **Lookup Users**: Endpoint to find contacts by criteria (used to get `contact_id` for other operations).
- **Swagger docs**: `https://api.mobilemonkey.com/swagger/dist/index.html`

The Consumer Data Enrichment API is a separate product with its own endpoints — details sparse, request access via customers.ai/api.

## Workflow setup

### First-time setup (10 minutes)

1. **Install X-Ray pixel**: Shopify Admin → Online Store → Themes → Edit Code → paste pixel in `theme.liquid` `<head>` tag. Or use Google Tag Manager.
2. **Connect Klaviyo**: In Customers.ai dashboard, connect your Klaviyo account via API key.
3. **Configure Alfred**: Set intent scoring thresholds (start permissive, tighten over time).
4. **Enable Inboxer**: Activate the deliverability booster script, list validation, and monitoring.
5. **Verify**: Visit your own store and check the Customers.ai dashboard for the visit.
6. **Monitor**: Watch deliverability metrics daily for the first 2 weeks.

### Migration from Retention.com or another visitor ID tool

1. **Export suppression list** from old tool (unsubscribes, bounces, complaints).
2. **Upload suppression list** to Customers.ai to prevent re-identifying known bad contacts.
3. **Install X-Ray pixel** (step 1 above).
4. **Request Data Detox** if your Klaviyo lists contain bad data from the previous tool — Customers.ai cleans up inaccurate profiles.
5. **Monitor deliverability** closely for 30 days. Identified contacts from the old tool may still be in Klaviyo flows.

### Optimizing Alfred thresholds

1. **Start permissive**: Let most identified visitors through for the first 2-4 weeks to gather baseline data.
2. **Review engagement**: After 2 weeks, check which intent buckets (high/medium/low) are actually engaging with emails.
3. **Tighten gradually**: Suppress the lowest-engaging bucket first (usually low-intent). Monitor Klaviyo costs and deliverability.
4. **Target ratio**: Aim to suppress 30-50% of identified visitors (the bottom of the intent distribution) while keeping the top 50-70% active.

## Deep dives

### Customers.ai vs competitors

| Factor | Customers.ai | Retention.com | RB2B | Opensend |
|---|---|---|---|---|
| **Focus** | B2C ecommerce (Shopify + Klaviyo) | B2C ecommerce (any ESP) | B2B sales | B2C multi-channel |
| **Accuracy** | 65-85% claimed | 15-25% independent reports | 35-45% (US, Pro+) | Varies |
| **Intent scoring** | Yes (Alfred, daily) | Limited | No | Limited |
| **Deliverability suite** | Yes (Inboxer, 4 tools) | No | N/A | No |
| **ESP support** | Klaviyo (lead) + SendGrid, Sendlane, HighLevel, Salesforce, Mailchimp | Multiple | N/A (CRM) | Multiple |
| **Ecommerce platform** | Shopify (primary) | Multiple | Any website | Multiple |
| **Ad retargeting** | Meta, Google, TikTok + Super CAPI (Meta server-side) | Via Klaviyo only | No | Meta, Google |
| **Starting price** | Custom (calculator by Klaviyo profile count) | $500/mo bundled | $79/mo | Varies |
| **Contract** | Monthly | Annual required | Monthly | Varies |
| **Geographic** | US focus | US only | US (person), global (company) | US focus |

### Case studies (from Customers.ai marketing)

- **Haverhill** (DTC jewelry): Generated nearly half the previous tool's revenue in one month after switching + completing data cleanup.
- **DFND**: 4.5x more revenue and 11x higher engagement/click rates.
- **Prana Pets**: 60-70% of website traffic identified.
- **Jordan Craig**: 4.6x higher revenue per recipient vs other identity solutions.

*Note: These are vendor-reported case studies. Actual results vary by traffic volume, audience, and existing Klaviyo infrastructure.*

### When NOT to use Customers.ai

- **Pre-revenue or early-stage stores** (<$50K GMV) — economics don't work at low traffic
- **Low-traffic, high-AOV stores** — too few resolutions to justify $600/mo
- **Non-Shopify stores** — Shopify is the primary commerce platform; confirm WooCommerce/BigCommerce/custom support directly before committing
- **Brands without core ESP flows** — you need welcome series, abandonment flows, and browse abandonment already running (in Klaviyo or a supported ESP) before adding identified visitors
- *(Note: non-Klaviyo ESP users are NO longer excluded — SendGrid, Sendlane, HighLevel, Salesforce and Mailchimp integrations now exist — but pricing is still calculated off Klaviyo profile count, so Klaviyo remains the path of least resistance.)*
- **International-heavy traffic** — identity resolution works primarily on US visitors
