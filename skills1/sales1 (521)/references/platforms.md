# SEO Platforms Reference

## All-in-one SEO suites

### Semrush (has skill: `/sales-semrush`)
- **Best for**: All-in-one power users who need keyword research + site audit + rank tracking + content tools + API + AI visibility
- **Pricing**: Pro $139.95/mo, Guru $249.95/mo (content + historical data), Business $499.95/mo (API access)
- **Strengths**: Largest keyword database (27B keywords), Content Marketing Toolkit, AI Visibility Toolkit, MCP server for Claude Code, Zapier integration
- **Weaknesses**: Expensive entry point, API gated to Business plan ($500/mo), free trial auto-renews
- **Budget verdict**: Only worth it if you'll use 3+ modules regularly. For keyword research alone, cheaper options exist.

### Ahrefs (has skill: `/sales-ahrefs`)
- **Best for**: Backlink analysis and competitive link research — the gold standard for link data
- **Pricing**: Starter $29/mo (new entry tier, monthly-only — 1 project, 100 tracked keywords, no rank tracking), Lite $129/mo (~$108 annual, 500 monthly credits), Standard $249/mo, Advanced $449/mo, Enterprise from $1,499/mo (annual). Add-ons: Brand Radar (AI visibility) $199/mo, AI Content Helper $99, Report Builder $99. No free trial.
- **Strengths**: Best backlink index (freshness + historical), excellent Site Explorer, Content Explorer for content gap analysis, free Webmaster Tools for your own site
- **Developer surface**: REST **API v3** (`api.ahrefs.com/v3`, Bearer key, metered **API units**; v2 discontinued 2025-11-01) and an **official MCP server** (Claude/ChatGPT/Cursor, Lite+). It now also has **Brand Radar** for AI-search visibility (paid add-on). For API/MCP/units/v2-migration/pricing-credit help, use `/sales-ahrefs`.
- **Weaknesses**: No content optimization scoring (vs Surfer/Clearscope), no native Zapier/Make, **aggressive credit caps + API-unit metering + "suspicious activity" throttling**, higher cost than Semrush/SE Ranking; no affiliate program
- **Budget verdict**: Worth it if backlinks are your primary concern. For general SEO on a budget, Semrush or SE Ranking are more cost-effective.

### SE Ranking
- **Best for**: Best-value all-in-one — full feature set at a fraction of Semrush/Ahrefs pricing
- **Pricing**: As of 2026 the official site lists plans as Core / Growth / Enterprise (the older Essential / Pro / Business naming was retired). The default storefront prices in EUR (~Core €87.20/mo monthly or €109/mo annual; Growth €188/mo monthly or €235/mo annual; Enterprise custom). USD figures vary by region and have changed more than once in 2025-2026 — re-check seranking.com/prices for current numbers before quoting.
- **Strengths**: Keyword research, site audit, rank tracking, backlink checker, AI-powered features, white-label reports, 14-day free trial
- **Weaknesses**: Smaller keyword/backlink database than Semrush or Ahrefs, less recognized brand
- **Budget verdict**: Best pick for solopreneurs wanting an all-in-one under $60/mo.

### Moz
- **Best for**: Beginners who want guided SEO recommendations — Moz pioneered Domain Authority (DA)
- **Pricing**: Starter $49/mo, Standard $99/mo, Medium $179/mo, Large $299/mo
- **Strengths**: Domain Authority metric (industry standard), MozBar browser extension, beginner-friendly, strong community/learning resources
- **Weaknesses**: Smaller keyword and backlink databases, slower to add new features, less competitive analysis depth
- **Budget verdict**: Good starting point at $49/mo but SE Ranking offers more features for similar price.

### Mangools
- **Best for**: Budget-friendly keyword research with the best UI in the category
- **Pricing**: Mangools $29/mo (annual), Premium $44/mo, Agency $89/mo
- **Strengths**: 5 tools (KWFinder, SERPChecker, SERPWatcher, LinkMiner, SiteProfiler), beautiful UI, beginner-friendly, cheapest all-in-one
- **Weaknesses**: Smaller database than big players, limited site audit, no content optimization, basic backlink data
- **Budget verdict**: Best pick for solopreneurs under $30/mo who primarily need keyword research + rank tracking.

### Ubersuggest
- **Best for**: Cheapest entry point — also offers lifetime deals
- **Pricing**: Individual $29/mo, Business $49/mo, Enterprise $99/mo. Lifetime deals occasionally available ($290-990 one-time)
- **Strengths**: Keyword research, site audit, rank tracking, Chrome extension, lifetime purchase option eliminates ongoing costs
- **Weaknesses**: Smaller database, less accurate traffic estimates, owned by Neil Patel's agency (marketing-heavy UX), limited backlink data
- **Budget verdict**: Good if you can get a lifetime deal. Monthly pricing is similar to Mangools which offers more tools.

## Content optimization tools

### Surfer SEO
- **Best for**: Real-time content optimization while writing — tells you what terms to include, ideal word count, structure
- **Pricing**: Plans were renamed in 2026 to Discovery / Standard / Pro / Peace of Mind / Enterprise (the older Essential / Scale / Scale AI tiers are gone). Storefront prices in EUR on annual billing: Discovery €49/mo, Standard €99/mo, Pro €182/mo, Peace of Mind €299/mo (adds API access + VIP support), Enterprise €999/mo. API access is now gated to the Peace of Mind tier.
- **Strengths**: Content Editor with NLP-based term suggestions, SERP Analyzer, integrates with Google Docs and WordPress
- **Weaknesses**: Not an all-in-one SEO tool — you still need keyword research and site audit elsewhere

### Clearscope
- **Best for**: Enterprise-grade content optimization — used by large content teams
- **Pricing**: Essentials $129/mo, Business $399/mo, Enterprise custom
- **Strengths**: Content grading, competitive analysis, Google Docs integration, team workflow
- **Weaknesses**: Expensive for solopreneurs, overkill for small sites

## WordPress SEO plugins

### Yoast SEO (has skill: `/sales-yoast`)
- **Best for**: Beginners who want guided setup — the original WordPress SEO plugin (13M+ installs)
- **Pricing**: Free (1 focus keyword), Premium $118.80/yr per site, AI+ $358.80/yr per site
- **Strengths**: Readability analysis, guided setup wizard, large community, Shopify version, llms.txt support
- **Weaknesses**: Per-site licensing (expensive for multiple sites), free version limited, heavier codebase than alternatives
- **Budget verdict**: Good for one site. Expensive for multiple sites — consider Rank Math or SEOPress.

### Rank Math
- **Best for**: Best free WordPress SEO plugin — more free features than any competitor
- **Pricing**: Free (now advertises unlimited focus keywords, redirects, 18 schema types, GSC integration), Pro $5.99/mo, Business $19.99/mo, Agency $44.99/mo (all billed annually)
- **Strengths**: Unlimited focus keywords free (vs 1 for Yoast), built-in redirect manager (free), 18+ schema types (free), GSC/GA4 integration (free), smaller codebase (faster), WooCommerce SEO (free)
- **Weaknesses**: Newer than Yoast (smaller community), Pro/Business features overlap with what Yoast Premium offers

### All in One SEO (AIOSEO)
- **Best for**: Agencies and multi-site owners — generous site limits on higher tiers
- **Pricing**: Basic $49.50/yr (1 site), Plus $99.50/yr (3 sites), Pro $199.50/yr (10 sites), Elite $299.50/yr (100 sites)
- **Strengths**: WooCommerce product schema, local SEO module, social media integration, link assistant
- **Weaknesses**: Free version is basic, premium required for most useful features

### SEOPress
- **Best for**: Developers who want clean, lightweight code — no ads or upsells
- **Pricing**: Free (generous), Pro $49/yr (1 site), $59/yr (5 sites), $149/yr (unlimited sites) — restructured Aug 2025; the single $49/yr unlimited-sites deal no longer exists
- **Strengths**: Lightweight, unlimited-sites tier available, no admin nag screens, clean code, white-label ready
- **Weaknesses**: Smaller community, fewer integrations, less hand-holding for beginners

## Free tools

### Google Search Console
- **What**: Google's official tool for monitoring search performance — impressions, clicks, positions, index coverage, crawl errors
- **Why essential**: Ground truth for how Google sees your site. Every other tool estimates; GSC measures.

### Ahrefs Webmaster Tools
- **What**: Free version of Ahrefs for your own verified site — site audit + backlink data
- **Limitations**: Only for sites you own (verified via GSC or DNS), no competitor research

### Screaming Frog SEO Spider
- **What**: Desktop crawler for technical SEO audits — finds broken links, redirect chains, duplicate titles, missing meta descriptions
- **Pricing**: Free (500 URL limit), Paid £199/yr (unlimited; priced in GBP with USD/EUR options at checkout, per-user license)
- **Why useful**: More thorough technical audits than cloud-based tools, runs locally

### AnswerThePublic
- **What**: Visual keyword research tool showing questions people ask about a topic
- **Pricing**: No free plan anymore. Starter $20/mo (or $99 one-time lifetime), Growth $99/mo ($490 lifetime), Business $199/mo ($990 lifetime)
- **Why useful**: Great for finding long-tail content ideas in question format

## Quick decision table

| Budget | Primary need | Recommended tool |
|---|---|---|
| $0 | Starting out | Google Search Console + Rank Math + Ubersuggest free |
| $29/mo | Keyword research | Mangools (or Ahrefs Starter $29/mo for backlink data) |
| ~$55-65/mo | All-in-one | SE Ranking (entry tier — verify current price/plan name) |
| $129/mo | Backlink focus | Ahrefs Lite |
| $140/mo | Everything + content + API | Semrush Pro |

## WordPress plugin quick decision

| Situation | Recommended plugin |
|---|---|
| One site, beginner, guided setup | Yoast Free or Premium |
| One site, want maximum free features | Rank Math Free |
| WooCommerce store, budget-conscious | Rank Math Free |
| Multiple sites, agency | AIOSEO Elite or SEOPress Pro |
| Developer, clean code, no bloat | SEOPress |
