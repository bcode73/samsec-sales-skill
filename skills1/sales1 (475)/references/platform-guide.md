# Remerge Platform Guide

## Platform Overview

Remerge is a demand-side platform (DSP) custom-built for **in-app retargeting** — it serves ads to users inside other mobile apps (not on the mobile web). Founded 2014 in Berlin, 180+ employees, offices in Berlin, New York, Tokyo, Singapore, Seoul.

**What makes Remerge different from web retargeting (AdRoll, Criteo, Google Ads):**
- Targets users **inside apps**, not on websites or the mobile web
- Uses **Mobile Measurement Partner (MMP)** data (AppsFlyer, Adjust, Branch) instead of website pixels
- Segments based on **in-app events** (purchases, level completions, cart additions) not page views
- Deep links land users at specific in-app screens, not web pages
- Designed for mobile app verticals: gaming, e-commerce, delivery, finance

## Core Capabilities

### Audience Segmentation
- Real-time segmentation based on in-app activity via MMP event streams
- Segment types: first-time buyers, active users, churned/lapsed users, high-value users, custom event-based segments
- Segments update dynamically as new events stream in
- Recommended: share last 3 months of historical user data for initial segment building

### Campaign Types
- **Re-engagement**: Bring back lapsed users who haven't opened the app in X days
- **Retention**: Keep active users engaged with personalized offers
- **User acquisition**: Find new high-value users via lookalike modeling
- **Cross-promotion**: Promote other apps in your portfolio to existing users

### Dynamic Product Ads (DPAs)
- Auto-generated ads using product catalog data
- Personalized with products the user viewed, carted, or purchased
- Deep links to specific product pages inside the app
- Requires product feed integration

### Incrementality Measurement
- Randomized control trials: test group (sees ads) vs control group (does not)
- Measures true campaign lift beyond organic behavior
- Remerge's primary success metric — not just ROAS or CPA. Reports **iROAS** (incremental ROAS) and **iCPA** (incremental cost per action)
- Two named measurement methodologies:
  - **Ghost Bids** — tracks a control group via bids that *could* have been placed but were intentionally withheld
  - **Causal Impact** — measures incremental uplift without device IDs (ID-less measurement)
- Results typically show 40-60% of attributed conversions are truly incremental

### Creative Services
- In-house creative team available
- Static images required in 5 aspect ratio sizes + native ad background
- Dynamic creative optimization for DPAs
- Video ad formats supported

### Bidding and Optimization
- Efficient bidding algorithms optimized for in-app conversion events
- Bidding infrastructure processes **almost 6 million queries per second (QPS)** — claims "double the number of ad opportunities than the industry average"
- Access to **more than 1 million apps worldwide** / **up to 2.5 billion mobile users** through **26 supply partners (SSPs)**
- CPA, CPC, CPE, CPS, and ROAS pricing models available

## Privacy and Compliance

### iOS (ATT framework)
- Only 20-35% of iOS users allow IDFA tracking post-ATT
- Remerge processes available IDFAs for consenting users
- Reduced iOS retargeting scale is industry-wide, not Remerge-specific
- Exploring Privacy Sandbox on-device bidding (partnership with Verve Group)

### Android (Privacy Sandbox)
- Google phasing in Topics API and Attribution Reporting API
- Remerge adapting bidding and attribution to work within new constraints
- On-device bidding reduces reliance on device-level identifiers

### GDPR
- Remerge operates as a data processor
- Highest data protection level claimed
- Opt-out functionality available for end users

## Integrations

### Mobile Measurement Partners (MMPs)
- **AppsFlyer**: Premier Partner. Enable Remerge as an ad network in AppsFlyer → configure postbacks for install and in-app events → set up tracking links with campaign naming conventions
- **Adjust**: Certified partner. Configure callback URLs for events → enable Remerge module
- **Branch**: Universal Links and App Links support for deep linking
- Additional MMP / data partners listed on remerge.io/our-partners: **Kochava, mParticle, Singular, Airbridge, Adbrix, WiseTracker**, plus **SKAdNetwork** support

### CRM / Engagement Platforms
- **Braze**: Webhook integration. Send a GET request to `https://remerge.events/event` with user ID, device identifiers (IDFA/AAID), app IDs, `partner=braze`, `key`, `ts`, `non_app_event=true`, and a `data` event payload. HTTP 204 = success. Content-Type: application/json. Note: IDFA collection is optional in the Braze SDK and disabled by default, so iOS device IDs must be enabled (with consent) for the integration to populate `idfa`.
- Other platforms can integrate via the Event Tracking API

### Setup Requirements for Any Campaign
1. MMP integration activated (event stream flowing to Remerge)
2. SDK integrated in your app (for performance data)
3. Deep links configured with trackable parameters
4. Historical user data shared (last 3 months recommended)
5. Creative assets provided (static in 5 aspect ratios minimum)

## API Reference

### Reporting API
- Pull JSON-based reports for active campaigns to internal BI on **daily granularity**
- Clients use cURL, internal API tools, or BI connectors
- **Base URL: `api.remerge.io`**
- **Authentication**: issue a sign-in request to `api.remerge.io` and copy the authorization token from the returning JSON response (e.g. `"J-QeJxyza7JH19QUDb4"`); requires a **Remerge API Key** (provided by your Remerge Account Manager) and a **Remerge Customer ID** (AppStore ID / Package Name / Google Play Store App ID)
- **Date range**: `start_date` / `end_date` default to 00:00 midnight of the given day. To query exactly one day, set `start_date` to that day and `end_date` to the next day. **Request one day of data at a time only.**
- **Six report dimensions**: Timestamp, Country, App, Campaign, Campaign Type, Related Ads
- **Data retention**: Remerge stores your data for **six months only**
- A separate **Campaign Cost Reporting via API** article covers pulling spend/cost data

### Event Tracking API
- Endpoint: `https://remerge.events/event`
- Method: GET (query-string parameters; the Braze webhook integration uses GET) — POST also documented for some integrations
- Send webhook events with user identifiers and event data
- Used for CRM integrations (Braze, etc.) and for forwarding in-app / attribution / BI / SKAdNetwork data
- Parameters (you must provide all **mandatory** ones): `app_id` (Android package or iOS App Store ID), `event` (event name, shown in the remerge.io dashboard), `partner`, `key` (webhook/partner key), `idfa` (iOS), `aaid` (Android), `country`, `device_name`, `os_name`, `os_version`, `ts` (Unix timestamp), `revenue`, `currency`, and a `data` JSON payload for additional metadata (URL-encoded; strings double-quoted per JSON spec)
- Non-app events (e.g. from Braze) pass `non_app_event=true`
- **Success response: HTTP 204**
- **Forwarding frequency**: all in-app events should be forwarded in **real time**; **App Open events every 10 minutes**
- Parameters with non-web-safe characters must be properly encoded

*Note: Remerge's full developer documentation lives at help.remerge.io. As of the 2026-06-13 re-verification the Reporting API and Event Tracking / Event Data Forwarding articles are publicly indexed and readable (no login required to view the docs), though obtaining an API Key / Customer ID still requires an active Remerge account.*

## Service Model

Remerge offers both:
- **Managed service**: Dedicated account team handles campaign optimization, creative, segmentation — primary offering
- **Self-service**: Available but less emphasized

**Pricing**: Not publicly available. Custom quotes based on campaign volume. Supports CPA, CPC, CPE, CPS, and Revshare/ROAS models across mobile display and video inventory.

## Competitor Comparison

| Feature | Remerge | Adikteev | Liftoff | Criteo |
|---|---|---|---|---|
| **Focus** | In-app retargeting (DSP) | App re-engagement + churn prediction | UA + retargeting (broader) | Ecommerce retargeting (web + app) |
| **Incrementality** | Core feature — randomized control trials | Available | Available | Available |
| **Creative** | In-house team + DPAs | In-house + interactive/video | Self-serve + managed | Dynamic Creative Optimization+ |
| **Privacy** | Privacy Sandbox partner (Verve Group) | Privacy-first focus | ID-less solutions | Large first-party publisher network |
| **Verticals** | Gaming, e-commerce, delivery | Gaming, e-commerce, finance | Gaming, e-commerce, apps | Primarily ecommerce |
| **Scale** | ~6M QPS, 1M+ apps, 2.5B users, 26 SSPs | Smaller but focused | Very large (Vungle + Liftoff merger) | Massive publisher network |
| **Pricing** | Custom, managed-service-first | Custom | Self-serve + managed | High minimums |

## Budget Allocation for App Retargeting

| App maturity | Retargeting budget (% of total UA+retargeting) | Focus |
|---|---|---|
| New app (<6 months) | 10-20% | Mostly UA, limited retargeting pool |
| Growing app (6-18 months) | 20-30% | Build retargeting as user base grows |
| Mature app (18+ months) | 30-50%+ | Retargeting often more efficient than new UA |

*Industry guidance: start with 20-30% of growth budget on retargeting, adjust based on incrementality results.*
