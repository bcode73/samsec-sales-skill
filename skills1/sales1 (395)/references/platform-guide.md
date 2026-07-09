# OpenWeb Ninja Platform Guide

## Website Contacts Scraper
- **What it does**: Extracts emails, phone numbers, and social profile links (Facebook, Instagram, TikTok, Snapchat, Twitter/X, LinkedIn, GitHub, YouTube, Pinterest) from any website domain. The `query` parameter accepts up to 20 domains in a single comma-separated request (batching).
- **Endpoint** (verified 2026-06-13): `GET https://api.openwebninja.com/website-contacts-scraper/scrape-contacts?query={domain}` with `x-api-key` header.
- **Response time**: 0.5-3 seconds per request
- **Key behavior**: Crawls the target domain in real time to discover publicly listed contact information — this is live scraping, not a pre-built database. Results vary based on what the website publicly exposes.
- **Use cases**: Enriching a list of target company domains with contact info, finding all publicly listed contact channels for a prospect, building outreach lists from website data

## Email Search
- **What it does**: Real-time web search for publicly available email addresses by query with an optional email domain filter. Returns an array of discovered email addresses.
- **Response time**: 1-2 seconds per request
- **Key behavior**: Searches the public web for indexed email addresses matching your query — results are limited to what is publicly available and indexed. This is not a verified email database; results should be validated before outreach.
- **Use cases**: Finding email addresses associated with a company name or person, discovering contact emails when you only have a name or keyword, supplementing other email finder tools with web-indexed results

## Local Business Data
- **What it does**: Search and retrieve businesses from Google Maps with 40+ fields including business ID, place ID, phone, website, address, ratings, review counts, opening hours, email contacts, social links, photos, reviews, and posts.
- **Supported operations**: Nearby search, bulk search, individual business details, reviews, photos, posts, autocomplete
- **Key behavior**: Each business returned in a search counts as a separate request against your quota — a search returning 20 businesses counts as 20 requests, not 1. Reviews, photos, and posts are separate endpoint calls.
- **Use cases**: Building local business prospect lists by category and geography, enriching account records with Google Maps data (ratings, reviews, hours), competitive analysis of businesses in a target area, finding business contact info (phone, email, website) at scale

## Social Links Search
- **What it does**: Finds social media profiles for companies or people across major platforms.
- **Use cases**: Enriching prospect records with social profile links, finding LinkedIn/Twitter profiles for outreach personalization, validating company identity across social platforms

## Real-Time Web Search
- **What it does**: Returns Google SERP results including organic results, AI Overviews, AI Mode (Gemini), videos, places, news, knowledge graph, People Also Ask, and related searches. Supports up to 500 results per query, localized by region and language.
- **Key behavior**: This is a SERP scraping API, not a traditional search engine — it fetches and structures Google's search results programmatically. Results include all SERP features (featured snippets, knowledge panels, etc.).
- **Use cases**: Competitive intelligence and brand monitoring, content research for sales enablement, finding prospects through search queries, monitoring industry news and trends at scale

## JSearch (Job Postings)
- **What it does**: Aggregates job postings from LinkedIn, Indeed, Glassdoor, ZipRecruiter, and more — 200M+ listings. Includes a Job Salary Data API.
- **Use cases**: Identifying companies that are hiring (buying signal for sales), researching target accounts' tech stack from job descriptions, competitive intelligence on hiring trends, recruiting and talent acquisition

## Product Data APIs
- **What it does**: Retrieves product data from Amazon, eBay, Walmart, and Costco — 35B+ product listings. Also includes Google Lens and Reverse Image Search.
- **Use cases**: Competitive pricing intelligence, market research for ecommerce prospects, identifying potential customers selling specific product categories

## Web Unblocker
- **What it does**: Fetches complete HTML of any website with JavaScript rendering, rotating proxies, and smart retries. Returns raw HTML, not structured data.
- **Key behavior**: This is a rendering/proxy service, not a scraper — you get raw HTML back and must parse it yourself. Use this when other APIs don't cover your target site, or when you need data from pages that block automated requests.
- **Use cases**: Accessing websites that block standard HTTP requests, scraping custom data from pages not covered by other OpenWeb Ninja APIs, fetching JavaScript-rendered content that requires a headless browser

## Finance Data
- **What it does**: Provides real-time data for stocks, cryptocurrency, and forex markets.
- **Use cases**: Monitoring prospect company stock performance as a conversation starter, tracking financial signals for target accounts, researching publicly traded prospects

## AI/LLM APIs
- **What it does**: Provides API access to Google AI Mode, Google Gemini, ChatGPT (unofficial), and Microsoft Copilot — all with web access capabilities.
- **Key behavior**: These are unofficial/wrapper APIs that provide programmatic access to AI services with web browsing. Availability and behavior may change without notice as underlying services update.
- **Use cases**: Automated research and summarization, generating insights from web data, augmenting sales intelligence workflows with AI analysis

## Other APIs
- **Zillow Real Estate** — property data and listings
- **Yelp Business Data** — business listings and reviews
- **Trustpilot Reviews** — company review data
- **Events Search** — discover events by keyword and location
- **Waze Data** — traffic and navigation data
- **Local Rank Tracker** — track local search rankings
- **Books Search** — book data aggregation
- **Forums Search** — search forum discussions
- **Shorts Search** — YouTube Shorts, TikTok, Instagram Reels
- **Image Search** — web image search results
- **News Data** — news article aggregation
- **Web Search Autocomplete** — search suggestion data

## Data model

| Object | Description | Key fields |
|--------|-------------|------------|
| **Business** | Google Maps business record | business_id, place_id, google_mid, name, phone_number, website, full_address, latitude, longitude, rating, review_count, opening_hours, email, facebook, instagram, twitter, linkedin, photos, reviews, posts |
| **Contact** | Scraped website contact info (Website Contacts Scraper) | domain, query, emails[{value,sources}], phone_numbers[{value,sources}], facebook, instagram, tiktok, snapchat, twitter, linkedin, github, youtube, pinterest |
| **Email** | Discovered email address | email, source, query, domain |
| **Review** | Business review | review_id, business_id, author, rating, text, date, language |
| **Photo** | Business photo | photo_id, business_id, url, caption |
| **Post** | Business post/update | post_id, business_id, text, date, media_url |
| **Search Result** | Web search result | title, url, snippet, position, domain, rich_snippet |
| **Job Listing** | Aggregated job posting | job_id, title, company, location, description, salary, source, date_posted, url |
| **Product** | Ecommerce product listing | product_id, title, price, rating, review_count, seller, url, image, platform |

## API quick reference

- **Access**: REST APIs via app.openwebninja.com portal or RapidAPI marketplace
- **Base URL** (direct portal, verified 2026-06-13): `https://api.openwebninja.com/{api-name}/{endpoint}` — each API has its own path segment (e.g. `/website-contacts-scraper/scrape-contacts`, `/local-business-data/search`, `/realtime-web-search/search`, `/jsearch/search-v2`)
- **Authentication** (verified 2026-06-13): direct portal uses the `x-api-key: YOUR_API_KEY` header; RapidAPI uses its own `X-RapidAPI-Key` header
- **Format**: JSON responses
- **Key note**: Each API is a separate product with its own subscription, endpoints, and rate limits. You subscribe to each API individually.
- **Code samples available**: JavaScript/Node.js, Python, Java, Ruby, cURL
- **Key endpoints** (verified 2026-06-13 from individual API pages):
  - Website Contacts Scraper: `GET /website-contacts-scraper/scrape-contacts?query=` — `query` accepts up to 20 comma-separated domains
  - Email Search: `GET /email-search/search-emails?query=&email_domain=` — returns a JSON array of email strings
  - Local Business Data: `GET /local-business-data/search` (+ nearby, reviews, photos, posts, autocomplete) — billed per object returned
  - Real-Time Web Search: `GET /realtime-web-search/search?q=` — up to 500 results, max 100 per request (paginate)
  - Social Links Search: `GET /social-links-search/search-social-links?query=` — Facebook/Instagram/TikTok/LinkedIn/Twitter/GitHub/YouTube/Pinterest/Snapchat
  - JSearch: `GET /jsearch/search-v2` — job search with filters, salary data
  - Web Unblocker: `/web-unblocker/request` — HTML fetch with `render_js`, `wait_for_selector`, `wait_until`; JS-rendered requests cost 5 credits

## Integrations

| Category | Details |
|----------|---------|
| **Marketplaces** | RapidAPI marketplace, API.market, Datarade |
| **Direct API** | REST API via app.openwebninja.com portal with API key auth |
| **Languages** | Code samples for JavaScript/Node.js, Python, Java, Ruby, cURL |
| **CRM/Tools** | No native CRM integrations — API-only, requires custom integration or middleware (Zapier, Make, n8n) to connect to CRM, spreadsheets, or other tools |

## Pricing (USD, verified 2026-06-13 against individual API pages at openwebninja.com/api/{api-name}; each API has its own subscription)

| Plan | Price | Requests/mo | Rate limit | Key notes |
|------|-------|-------------|------------|-----------|
| **Free** | $0 | 50-500 (varies by API) | 1/sec or 1,000/hr | No credit card required, evaluation only |
| **Pro** | $25/mo | 10,000-20,000 (+ ~$0.003/extra) | 5-10/sec | Per API subscription |
| **Ultra** | $75/mo | 50,000-100,000 (+ ~$0.002/extra) | 8-20/sec | Per API subscription |
| **Mega** | $150/mo | 200,000-300,000 (+ ~$0.001/extra) | 10-30/sec | Per API subscription |
| **Pay-as-you-go** | $0.001-0.005/req | — | 5-10/sec | Per-request billing |
| **Custom** | Contact sales (support@openwebninja.com) | Custom | Custom | Higher volumes |

**Key pricing notes**:
- **Each API is a separate subscription** — subscribing to Local Business Data does not give you access to Email Search or Web Unblocker. Plan your budget across all the APIs you need.
- **Request limits and rate limits vary by API** — Free tiers range from 50 (Website Contacts, Email Search, Social Links) to 100 (Real-Time Web Search, Web Unblocker), 200 (JSearch), or 500 (Local Business Data). Always check the specific API's pricing page.
- **Overage is metered per request above the monthly quota** at roughly $0.003 (Pro) / $0.002 (Ultra) / $0.001 (Mega), so monthly plans don't hard-stop — they bill overflow.
- **Web Unblocker is the pricing exception** — same $25/$75/$150 prices but far higher quotas (Free 100, Pro 50K, Ultra 250K, Mega 1,000,000), PAYG $0.001/use, and JS-rendered requests cost 5 credits each.
- **Local Business Data bills per object returned** (business/review/photo), not per request — a 20-result search costs 20 credits.
- **Pay-as-you-go is available per API** at ~$0.005 per request (Local Business Data $0.004/business; Web Unblocker $0.001/use), for variable usage without a monthly commitment.
- **Costs can add up quickly** if you subscribe to multiple APIs — e.g., subscribing to Pro on 4 APIs = $100/mo.
