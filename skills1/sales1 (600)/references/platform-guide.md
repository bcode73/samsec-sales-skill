# There's an AI for That (TAAFT) Platform Reference

## Platform overview

There's an AI for That (TAAFT) is the #1 AI tools aggregator by traffic and database size. Unlike category-browsing directories (Futurepedia, Altern), TAAFT uses a task-based discovery model — users type what they want to accomplish and get matched to AI tools that solve that problem. Founded and operated by Andrei, a solopreneur based in Bucharest, Romania. The platform functions as a media company generating revenue through submission fees, PPC ads, and newsletter sponsorships.

**Key stats** (from /get-featured/, verified 2026-06-13):
- 50,400 AI tools indexed
- 1,000+ use cases/task categories
- ~3,000,000 monthly unique visitors / 9,000,000 monthly page views / 300,000 daily page views
- 1.2M+ newsletter subscribers
- DR76 (dofollow backlinks)
- Average ad CTR ~1.3%
- Twitter: @theresanaiforit (platform), @imakecoolsites (Andrei)

> **Stat discrepancy:** the /launch/ submission page cites higher headline figures — **5M+ monthly visitors** and a **2.5M+ subscriber** newsletter — than the /get-featured/ page (3M visitors / 1.2M+ subscribers). Both are current official pages. Use the lower /get-featured/ numbers for conservative estimates; quote the /launch/ numbers only if you cite that page directly.

## Submission process

### Paid submission — two tiers

TAAFT's /launch/ page sells two one-time submission packages:

| Package | Cost | Est. clicks | Newsletter | Notes |
|---|---|---|---|---|
| **Maximum Exposure** | $347 one-time | 700 – 10,000+ | Guaranteed mention in the newsletter | The headline package; full visibility surface |
| **Website Only** | $49 one-time review fee | ~50 – 100 (first week, casual/discovery traffic) | Not guaranteed | Lower-cost "just released" listing only |

Submission flow:
1. Go to theresanaiforthat.com/launch/
2. Submit your AI tool with name, URL, description, and category
3. Pay the package fee ($347 or $49)
4. Manual review by TAAFT staff (average 1-2 day turnaround)
5. If approved: permanent listing with dofollow backlink
6. If rejected: automatic full refund ("if your AI doesn't get published")

**TAAFT-first launch bonus**: If your tool hasn't appeared on any other platform before submitting to TAAFT, you automatically receive a $300 PPC credit bonus. Against the $347 package this makes the effective cost ~$47 + free Featured ad credits.

### Free submission (monthly X thread)

TAAFT runs a thread on X (Twitter) once a month where indie makers can submit their tool for free. One tool from each thread is chosen and listed for free. Low odds but zero cost.

### What's included in a listing

- Permanent tool page (listings don't expire)
- Dofollow backlink to your site (DR76)
- Searchable in TAAFT's task-based discovery
- Eligible for newsletter inclusion (editorial selection)
- Eligible for category/trending pages
- Screenshots, video embeds, and generation showcases

## Featured ads (PPC)

TAAFT offers a pay-per-click "Featured" section on the homepage and search results.

- **Pricing**: Bid-based — your position in the list is determined by your bid; higher bids get higher position in the Featured section
- **Billing**: Pay per click (PPC model). You commit to a click volume — **minimum 1,000 clicks, maximum 50,000 clicks** — and set a per-click bid. The page's worked example is **$2/click** (2,000 clicks = $4,000)
- **Placement**: Featured section is prominent on homepage and appears in relevant task searches; can produce "up to 60x more clicks"
- **Clicks route through TAAFT**: Featured clicks go to a TAAFT page first (with tracking), then to your site
- **Refunds**: ad/sponsorship spend is refundable provided the campaign hasn't started yet

### Strategy for Featured ads

1. Start with a low bid to establish baseline CTR
2. Test different task categories — some categories have more search volume
3. Monitor which searches trigger your Featured ad
4. Increase bids on high-converting categories
5. Use the $300 TAAFT-first bonus credits to test without risk

## Highlight listings

Separate from Featured ads — a Highlight subscription makes your organic listing stand out and pins it to the front page.

- **Pricing**: **$99/month**, recurring, cancellable anytime (verified on /get-featured/ 2026-06-13; previously quoted as "contact for pricing")
- **Effect**: "Up to 4x more clicks." Highlighted AIs stay on the front page for as long as the Highlight subscription is active
- **Clicks go directly to your site** ("highlighted listings also lead directly to the destination site"), unlike Featured ads which route through TAAFT — this matters because TAAFT reports that over half of users who open a regular listing never click through to the external site

## Newsletter

TAAFT's newsletter is one of the largest AI-focused newsletter audiences. The /get-featured/ page lists **1.2M+ subscribers**; the /launch/ page markets it as the "#1 AI newsletter on the planet" with **2.5M+ subscribers** — use 1.2M+ as the conservative figure.

- General newsletter inclusion is editorial — you can't buy a spot directly
- However, the **$347 Maximum Exposure package includes a guaranteed newsletter mention** (the $49 Website Only package does not)
- Being listed on TAAFT makes you eligible for newsletter features
- The newsletter covers trending tools, new categories, and curated picks
- Separate newsletter sponsorship slots may be available (contact TAAFT for rates)

## ChatGPT plugin / API

> **Status (verified 2026-06-13):** OpenAI officially discontinued ChatGPT plugins — new plugin chats stopped March 19, 2024 and all plugin chats were shut down April 9, 2024 — so TAAFT's ChatGPT *plugin* surface is effectively dead. The underlying `/api/search/` endpoint and `/openapi.json` still resolve on the domain but now sit behind a Cloudflare bot challenge (HTTP 403 / "Just a moment…" to scripted requests), so a documented public/programmatic search API can no longer be confirmed as openly callable. Treat the endpoint details below as historical/best-effort, not a supported integration. TAAFT has no public REST API, webhooks, or SDKs.

TAAFT historically exposed a search API that powered its ChatGPT plugin.

**Endpoint**: `GET https://theresanaiforthat.com/api/search/?q={query}` (now Cloudflare-gated)

**Response format** (JSON array):
```json
[
  {
    "name": "Example Name",
    "task": "Example Task",
    "url": "https://theresanaiforthat.com/ai/example/?ref=search&term=example&from=chatgpt",
    "use_case": "Example Use Case"
  }
]
```

**Auth**: Service-level bearer token (no user auth required)
**OpenAPI spec**: https://theresanaiforthat.com/openapi.json
**Contact for API**: plugin@theresanaiforthat.com

## TAAFT vs other AI directories

| Factor | TAAFT | Futurepedia | Altern | Toolify | PitchWall |
|---|---|---|---|---|---|
| Size | 50,400 tools | 5,700+ tools | 10,000+ tools | 20,000+ tools | 65,000+ products |
| Traffic | ~3M uniques/9M views/mo | ~2M/mo | ~5-28K/mo | High | Medium |
| DR | 76 | High (est.) | Unconfirmed | Varies | 60 (disputed) |
| Backlink | Dofollow | Dofollow | Dofollow | Varies | Disputed |
| Discovery | Task-based search | Category browse | Category browse (AI-only) | Trending/algorithm | AI product browse |
| Submission cost | $49 / $347 (free monthly thread) | $497 Verified | Free + featured tiers | Free | Free / $99 Premium |
| Newsletter | 1.2M+ subscribers | YouTube 2M+ subs | Weekly digest | Yes | 45K+ subscribers |
| Review | Manual (1-2 days) | 2 business days | Editorial (no SLA) | Unknown | 30+ days (free) |
| Best for | Maximum reach, task discovery | Education, YouTube exposure | Dev/AI agent tools | Trending tools | AI product discovery |
| Unique value | $300 first-launch PPC bonus | YouTube network, courses | Alternatives pages | Monthly visitor data | $1K Spotlight ads |

## Pricing summary

| Option | Cost | What you get |
|---|---|---|
| Maximum Exposure submission | $347 one-time | Permanent listing, dofollow backlink (DR76), 700-10K+ est. clicks, **guaranteed newsletter mention** |
| Website Only submission | $49 one-time | "Just released" listing only, ~50-100 est. first-week clicks, no guaranteed newsletter slot |
| TAAFT-first bonus | -$300 (credit) | PPC ad credits if your tool launches on TAAFT before any other platform |
| Featured (PPC) | Bid-based | Homepage + search Featured section, 1,000-50,000 clicks, ~$2/click example, pay per click |
| Highlight listing | $99/month | Front-page emphasis while active, "up to 4x more clicks," direct-to-site clicks, cancel anytime |
| Free X thread | $0 | Monthly thread, one winner chosen |

## Integrations

- **ChatGPT plugin**: Search TAAFT's database from within ChatGPT
- **Verified/authentic indicators**: Tools can display verification badges
- **UTM tracking**: Featured and organic clicks include tracking parameters
- **No native CRM/Zapier integrations**: TAAFT is a directory, not a marketing automation platform

## Contact

- **Submission/listing**: theresanaiforthat.com/launch/
- **Featured ads**: theresanaiforthat.com/get-featured/
- **API/plugin**: plugin@theresanaiforthat.com
- **Founder (Andrei)**: Twitter DMs @imakecoolsites
- **Platform Twitter**: @theresanaiforit
