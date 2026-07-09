# SponsorGap Platform Reference

## Overview

SponsorGap is a newsletter sponsorship intelligence platform with a database of 45,000+ brands (a live counter on the site; ~45,851 companies / "46k+" as of 2026-06-13, tracking 25k+ sponsorship deals across 3,300+ monitored newsletters). It helps newsletter creators find, research, and contact brands that actively sponsor newsletters. Launched 2021. Primary differentiator: GPT-powered sponsor matching with verified decision-maker contacts and real-time spend trend data.

## Capabilities & automation surface

| Capability | Description | Access |
|---|---|---|
| **Sponsor search** | Search 45K+ brands by niche, industry, company name | UI — free tier (5 hand-picked sponsors free, no card) |
| **GPT-powered matching** | AI recommends sponsors based on your newsletter niche | UI — Starter+ |
| **Niche filters** | Filter sponsors by industry (finance, tech, marketing, health, etc.) | UI — Starter+ |
| **Activity feed** | Real-time feed of sponsorship deals happening across newsletters | UI — Starter+ |
| **Verified contacts** | Decision-maker email + LinkedIn for sponsor outreach | UI — Pro+ |
| **Competitor monitoring** | Track which brands sponsor competitor newsletters, real-time alerts | UI — Pro+ |
| **Spend trends** | Brand sponsorship spending trajectory over time | UI — Pro+ |
| **Ad copy library** | Real newsletter ad examples from sponsors | UI — Pro+ |
| **Funding radar** | Recently-funded companies (higher sponsorship budget likelihood) | UI — Pro+ |
| **Rate calculator** | Benchmark sponsorship pricing by niche and list size | UI — free |
| **Outreach pipeline** | Track sponsor outreach status (contacted, replied, booked) | UI — Business |
| **CSV export** | Bulk export sponsor data | Export — Pro+ |
| **Bulk export** | Large-scale data export | Export — Business |
| **Full API** | Programmatic access to sponsor database | API — Business |
| **Sponsor calendar** | View open ad slots and scheduling | UI — Starter+ |
| **Watchlist** | Save and monitor specific brands | UI — Starter+ |
| **Custom reports** | Generate sponsor intelligence reports | UI — Business |
| **Weekly digest** | Email digest of sponsorship activity in your niche | Email — all tiers |

## Pricing, limits & plan gates

> **Re-verified 2026-06-13 against sponsorgap.com/pricing.** The three publisher tiers were **renamed**: the former Starter / Pro / Business are now **Starter / Growth / Enterprise** (prices unchanged at $39 / $89 / $199). **API access tiering changed**: "Limited API access" now starts at **Growth ($89)**, and **"Full API access"** is at **Enterprise ($199)** — the API is no longer Enterprise-only for all access. Team-member caps changed too (Growth now up to 5; Enterprise unlimited). A new **Managed Services** line was added (see below).

Publisher self-serve plans, as listed verbatim on the current pricing page:

| Plan | Price | Listed features (verbatim) |
|---|---|---|
| **Starter** | $39/mo | Browse 1,000+ sponsors; Add 1 team member; Basic contact information; Email support |
| **Growth** (Most Popular) | $89/mo | Everything in Starter, plus: Add up to 5 team members; Limited API access; Funding round intelligence; Priority support |
| **Enterprise** | $199/mo | Everything in Growth, plus: Unlimited team members; Full API access; AI-powered recommendations; Dedicated account manager; 24/7 phone support |

**Free entry point**: "Start free — no card needed." The free search engine surfaces "5 hand-picked sponsors with contact info — completely free" and lets you search 25k+ sponsor deals; full access to verified contact info, spend trends, competitor data and the full 45K+ sponsor database requires a paid plan.

**Managed Services** (done-for-you, separate from self-serve):

| Plan | Price | What's included (verbatim) |
|---|---|---|
| **Enterprise (Managed)** | $999/mo | Fixed price + 10% success fee; custom CRM building in Airtable; strategic outreach execution; weekly briefing & progress updates |
| **Enterprise Gold** | $2,999/mo | Same managed services as the $999 tier; no success fee — fixed price only |

**Feature gating note (partially unverified):** The current pricing page does NOT enumerate verified contacts, competitor monitoring, spend trends, the ad-copy library, or CSV/bulk export against specific named tiers. SponsorGap's own marketing confirms these are **paid** features (the free tier explicitly excludes them), and they have historically been associated with the $89 (now Growth) tier, but the exact tier each is gated to could not be confirmed line-by-line on the live pricing page as of 2026-06-13 — treat the per-tier rows below as best-effort until reconfirmed in-product.

| Feature | Starter ($39/mo) | Growth ($89/mo) | Enterprise ($199/mo) |
|---|---|---|---|
| Brand database access | 1,000+ sponsors | Full database | Full database |
| Niche filters & search | Yes | Yes | Yes |
| Basic contact information | Yes | Yes | Yes |
| **Verified contacts** (best-effort gate) | No | **Yes** | **Yes** |
| **Competitor monitoring** (best-effort gate) | No | **Yes** | **Yes** |
| **Spend trends** (best-effort gate) | No | **Yes** | **Yes** |
| **Funding round intelligence** | No | **Yes** | **Yes** |
| **CSV export** (best-effort gate) | No | **Yes** | **Yes** |
| **Team members** | 1 | **up to 5** | **Unlimited** |
| **API access** | No | **Limited** | **Full** |
| **AI-powered recommendations** | No | No | **Yes** |
| **Priority support** | No | **Yes** | Yes |
| **Dedicated account manager / 24-7 phone** | No | No | **Yes** |

**Key gate**: The jump from Starter to **Growth** unlocks the most critical features for active prospecting (verified contacts, competitor monitoring, spend trends) **plus limited API access and up to 5 seats**. **Enterprise** ($199) adds Full API access, AI-powered recommendations, unlimited seats, and white-glove support. For done-for-you prospecting, the Managed Services tiers ($999 / $2,999) build a custom Airtable CRM and run outreach for you.

## Integrations

- **API** — **Limited API access starts on Growth ($89/mo); Full API access on Enterprise ($199/mo)** (re-verified 2026-06-13 on the pricing page). No public API documentation is published — credentials/docs are provided on subscription or via support. The exact difference between "Limited" and "Full" API access is not documented publicly.
- **CSV export** (paid tiers): Export sponsor lists for import into CRM, outreach tools, or spreadsheets. (Specific gating tier not enumerated on the current pricing page.)
- **Airtable** — **Confirmed** as the CRM substrate for SponsorGap's **Managed Services** ($999 / $2,999/mo), where SponsorGap builds a custom CRM in Airtable for you. This is a done-for-you service, not a self-serve connector.
- **No Zapier/Make integration**: Data movement requires manual CSV export or API.
- **No webhooks**: No event-driven notifications available (not advertised on the site as of 2026-06-13).
- **No MCP server**: No Claude Code / LLM integration available.

## Data model

SponsorGap's core objects based on the platform's features:

### Brand/Sponsor object
```json
<!-- Constructed from docs — verify against live API -->
{
  "brand_name": "Notion",
  "industry": "software",
  "niche_tags": ["productivity", "project-management", "SaaS"],
  "sponsorship_count": 42,
  "spend_trend": "increasing",
  "last_sponsored": "2026-05-01",
  "newsletters_sponsored": ["The Hustle", "Morning Brew", "TLDR"],
  "contacts": [
    {
      "name": "Jane Smith",
      "title": "Head of Growth Marketing",
      "email": "jane@notion.so",
      "linkedin": "https://linkedin.com/in/janesmith"
    }
  ],
  "funding": {
    "last_round": "Series C",
    "amount": "$275M",
    "date": "2024-04-15"
  }
}
```

### Newsletter object (for brand-side search)
```json
<!-- Constructed from docs — verify against live API -->
{
  "newsletter_name": "TLDR",
  "niche": "technology",
  "subscriber_count": 1200000,
  "open_rate": 0.52,
  "geography": "US",
  "sponsors": ["Notion", "LinearB", "Neon"],
  "cpm_range": "$50-$80"
}
```

## Quick-start recipes

### Recipe 1: Build a sponsor target list (UI workflow)

**Trigger**: You're launching sponsorship sales and need a prospect list.

**Steps**:
1. Log in to SponsorGap → Go to sponsor search
2. Filter by your newsletter's niche (e.g., "fintech")
3. Sort by spend trend ("increasing") to find brands actively expanding sponsorship budgets
4. Add top 20-30 brands to your watchlist
5. Upgrade to Pro to unlock verified contacts
6. Export to CSV → import into your outreach tool (Mailshake, Lemlist, etc.)

**Gotcha**: Start with brands sponsoring similar-sized newsletters. Fortune 500 brands in your niche may have minimum audience requirements of 50K+.

### Recipe 2: Monitor competitor sponsorships (Pro tier)

**Trigger**: You want to know who sponsors competitor newsletters to pitch the same brands.

**Steps**:
1. Go to competitor monitoring → Add competitor newsletter names
2. Enable real-time alerts for new sponsor placements
3. When a new sponsor appears, check the ad copy library for the actual ad they ran
4. Use the brand's verified contact to reach out with a pitch that references their competitor placement
5. Use the rate calculator to price competitively

**Gotcha**: Don't copy competitor pricing blindly — your audience demographics and engagement rates determine your rate, not theirs.

### Recipe 3: API-based sponsor pipeline (Growth tier for limited API, Enterprise for full)

**Trigger**: You want to automate sponsor discovery and feed data into your CRM.

**Steps**:
1. Subscribe to **Growth ($89/mo)** for **Limited API access**, or **Enterprise ($199/mo)** for **Full API access**; contact SponsorGap support for API documentation and credentials
2. Query the API for brands in your niche with "increasing" spend trends
3. Filter for brands with recent funding (higher budget likelihood)
4. Push brand + contact data to your CRM (HubSpot, Attio, etc.)
5. Track deal stages in your CRM (SponsorGap has no self-serve outreach-pipeline feature on the current pricing page; for done-for-you outreach + a custom Airtable CRM, see Managed Services at $999/$2,999)

**Note**: API documentation is not publicly available. Limited API access is included from the Growth tier; full API access is at Enterprise. Request docs/credentials via support after subscribing.

## Integration patterns

### CRM sync (manual)
1. Export sponsors as CSV from SponsorGap (Pro+)
2. Map fields: brand name → company, contact email → email, contact name → contact, industry → custom field
3. Import into CRM
4. Set up a weekly export cadence to catch new sponsors

### Outreach tool pipeline
1. Export target sponsors with verified contacts
2. Import into cold email tool (Mailshake, Lemlist, Smartlead)
3. Create a sequence: pitch email → follow-up → break-up
4. Track responses in SponsorGap's outreach pipeline (Business) or in your CRM
5. Use ad copy library examples to personalize your pitch ("I saw your ad in {competitor newsletter}")
