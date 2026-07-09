# Modash Platform Guide

## Creator Discovery

Modash indexes every public profile with 1K+ followers across Instagram, TikTok, and YouTube — 350M+ creators total. No opt-in required.

### Search and filters
- **Keyword search** — find creators by bio keywords, hashtags, mentions, or content topics
- **AI Search** — describe the creator you need in natural language ("fitness influencers in Germany who post home workouts")
- **Demographic filters** — audience location, age, gender, language, interests
- **Performance filters** — follower count range, engagement rate, growth rate, average views
- **Brand collaboration history** — see which brands a creator has worked with
- **Lookalike search** — find creators similar to ones you already work with

### Audience analysis
- **Demographics** — audience location (country/city), age brackets, gender split, language
- **Fake follower detection** — identifies bot accounts and purchased followers with a percentage score
- **Engagement authenticity** — distinguishes real engagement from pods or bots
- **Audience overlap** — compare creators to avoid paying for redundant reach

### Creator profiles
- Performance metrics, audience breakdown, content samples, brand collaboration history
- Export to CSV for offline analysis
- Save to lists for campaign organization

## Campaign Management

Track influencer campaigns without requiring creators to sign up or install anything.

### Content tracking
- **Automatic detection** — Modash detects posts, stories, and reels mentioning your brand, using your hashtag, or tagging your account
- **No creator signup required** — tracking works passively via public content monitoring
- **Story archival** — captures ephemeral stories before they expire
- **Multi-platform** — track across Instagram, TikTok, and YouTube simultaneously

### Metrics and reporting
- **ROAS (Return on Ad Spend)** — revenue generated vs. creator cost
- **EMV (Earned Media Value)** — estimated value of organic impressions
- **CPM (Cost per Mille)** — cost per 1,000 impressions
- **Engagement** — likes, comments, shares, saves per post
- **Sales attribution** — track conversions via promo codes and affiliate links through Shopify
- **Live dashboard** — real-time campaign performance updates

## Shopify Integration

Deep native integration with Shopify for product gifting, affiliate tracking, and sales attribution.

### Product gifting
- Select products from your Shopify catalog to send to creators
- Creators receive a gifting link — they pick size/variant and enter shipping info
- Orders are auto-created in Shopify and fulfilled through your normal process
- No manual order entry or spreadsheet tracking needed

### Affiliate tracking
- Generate unique promo codes per creator automatically
- Track sales attributed to each creator via Shopify order data
- Calculate ROAS per creator, per campaign, or across your entire program
- Automated commission calculation based on attributed sales

### Promo codes
- Auto-generated unique codes per creator
- Set discount percentage or fixed amount
- Track usage and revenue per code in Modash dashboard

## Creator Payments

Pay influencers directly from Modash in 180+ countries.

- **Automated payouts** — set payment terms and pay creators based on campaign performance or flat fees
- **Multi-currency** — supports payments in local currencies across 180+ countries
- **Payment tracking** — see payment status, history, and outstanding balances per creator
- **Invoice management** — creators receive payment notifications and documentation

## Communications

Manage all creator communications in one place.

- **Gmail/Outlook sync** — connect your email to sync conversations with creators into Modash
- **Centralized inbox** — view all creator communications alongside their profile and campaign data
- **Templates** — save and reuse outreach templates with dynamic merge fields (creator name, handle, etc.)
- **Notes** — add internal notes to creator profiles for team collaboration

## Pricing

*Verified 2026-06-13 against modash.io/pricing. Usage-based scaling on all plans.*

| Plan | Annual price (billed yearly) | Monthly price | Profile opens/mo | Tracked creators | Email unlocks/mo | Team seats |
|---|---|---|---|---|---|---|
| Essentials | $199/mo ($2,388/yr) | $299/mo | 300 | 100 | 150 | 2 |
| Performance | $499/mo ($5,988/yr) | $599/mo | 800 | 250 | 400 | 5 |
| Enterprise | Custom (from $14,700/yr) | — | More | More | More | Customizable |

**Plan note** — the mid tier is named **Performance** (formerly "Pro"). Performance and Enterprise add "Influential fans" discovery (up to 6,000/mo), content downloads, campaign data exports, and payment processing.

**Usage-based scaling** — each plan has base limits for profile opens, tracked creators, email unlocks, and team seats. Overage pricing applies when you exceed your plan's limits.

**14-day free trial** — no credit card required; includes 20 profile views, 6 email unlocks, and 10 tracked creators.

## API

Modash offers two API product lines for building custom integrations and tools. API access is priced separately from the platform.

For detailed endpoint documentation, see `references/modash-api-reference.md`.

- **Discovery API** — search 380M+ creator profiles with filters, get audience demographics and performance metrics. Starting at $16,200/yr (3,000 credits/mo). **AI Search**, **Collaborations**, **Lookalikes**, and email/handle search are features *within* the Discovery API (not separate products).
- **Raw API** — live, unfiltered profile data for real-time monitoring. Starting at $10,000/yr (40,000 requests/mo).

**Base URL**: `https://api.modash.io/v1/` (e.g. `POST https://api.modash.io/v1/instagram/search`).

**Auth**: Bearer token via `Authorization: Bearer {token}` (or `access_token` body/query parameter). Get your token at marketer.modash.io/developer.
