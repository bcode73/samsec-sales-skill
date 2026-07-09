### OpenWeb Ninja APIs — Sales-Relevant Reference

OpenWeb Ninja provides 30+ REST APIs for real-time public web data extraction, including contact scraping, email search, local business data, web search, and social profile discovery.

> **Note**: API base URL, auth header, and per-API endpoint paths were re-verified against the live official API pages on 2026-06-13. Official docs: https://www.openwebninja.com/documentation. Individual API pages: https://www.openwebninja.com/api/{api-name}. Also available on the RapidAPI marketplace (RapidAPI uses its own `X-RapidAPI-Key` auth).

---

## Base URL

```
https://api.openwebninja.com/{api-name}/{endpoint}
```

Each API has its own path segment under `api.openwebninja.com`, e.g.:
- `https://api.openwebninja.com/website-contacts-scraper/scrape-contacts`
- `https://api.openwebninja.com/email-search/search-emails`
- `https://api.openwebninja.com/local-business-data/search`
- `https://api.openwebninja.com/realtime-web-search/search`
- `https://api.openwebninja.com/social-links-search/search-social-links`
- `https://api.openwebninja.com/jsearch/search-v2`
- `https://api.openwebninja.com/web-unblocker/request`

(Verified 2026-06-13 from the individual API pages at openwebninja.com/api/{api-name}.)

---

### Authentication

- **Direct portal (api.openwebninja.com)**: API key in the `x-api-key` header — `x-api-key: YOUR_API_KEY`. Get your key from the developer portal at https://app.openwebninja.com (no credit card required for the free tier). Confirmed across the Website Contacts Scraper, Email Search, Local Business Data, Real-Time Web Search, Social Links Search, JSearch, and Web Unblocker API pages on 2026-06-13.
- **RapidAPI**: `X-RapidAPI-Key` header (standard RapidAPI auth) when subscribed via the RapidAPI marketplace.

---

### Pricing Tiers

Most APIs share the same four-tier ladder plus pay-as-you-go (exact allocations and overage rates vary per API — see individual endpoints below). Prices below verified 2026-06-13:

| Tier | Price | Typical Allocation |
|---|---|---|
| Free | $0/mo | 50–500 requests/mo (e.g. Website Contacts/Email/Social Links 50, Real-Time Web Search & Web Unblocker 100, JSearch 200, Local Business Data 500) |
| Pro | $25/mo | 10K–20K requests/mo (+ ~$0.003/extra) |
| Ultra | $75/mo | 50K–100K requests/mo (+ ~$0.002/extra) |
| Mega | $150/mo | 200K–300K requests/mo (+ ~$0.001/extra) |
| Pay-As-You-Go | ~$0.005/req | Per-request pricing (varies by API) |

**Exception — Web Unblocker has higher quotas at the same prices**: Free 100, Pro $25/50K, Ultra $75/250K, Mega $150/1,000,000, PAYG $0.001/use; JS-rendered requests cost 5 credits each.

---

### Error Handling

Not documented in publicly available content. Standard HTTP status codes are expected. Check official docs for error response format and codes.

---

### Endpoints

---

#### 1. Website Contacts Scraper

Extract emails, phone numbers, and social media links from any domain.

**Endpoint**: `GET https://api.openwebninja.com/website-contacts-scraper/scrape-contacts`

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | Domain name(s) to scrape — supports up to 20 domains in a single request, comma-separated |

**Response fields**:

| Field | Type | Description |
|---|---|---|
| `domain` | string | The scraped domain |
| `query` | string | The submitted query |
| `emails` | array | List of email objects with `value` and `sources` |
| `phone_numbers` | array | List of phone number objects with `value` and `sources` |
| `facebook` | string | Facebook profile URL |
| `instagram` | string | Instagram profile URL |
| `tiktok` | string | TikTok profile URL |
| `snapchat` | string | Snapchat profile URL |
| `twitter` | string | Twitter/X profile URL |
| `linkedin` | string | LinkedIn profile URL |
| `github` | string | GitHub profile URL |
| `youtube` | string | YouTube profile URL |
| `pinterest` | string | Pinterest profile URL |

**Rate limits**:

| Tier | Rate |
|---|---|
| Free | 1 req/sec |
| Pro | 5 req/sec |
| Ultra | 10 req/sec |
| Mega | 20 req/sec |

**Pricing** (verified 2026-06-13): Free $0 (50/mo), Pro $25 (10K + $0.003/extra), Ultra $75 (50K + $0.002/extra), Mega $150 (200K + $0.001/extra), PAYG $0.005/req. Batch up to 20 domains per request.

---

#### 2. Email Search

Real-time web search for publicly available email addresses associated with a company or person.

**Endpoint**: `GET https://api.openwebninja.com/email-search/search-emails`

**Parameters**:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | Search query, e.g. "Car Dealer California USA" |
| `email_domain` | string | No | Filter results to a specific email domain (e.g. `gmail.com`) |

**Response**: JSON array of email address strings.

```json
["usaautodealers@gmail.com", "catanosautosales@gmail.com"]
```

**Response time**: 1–2 seconds

**Rate limits**: Free 1,000 req/hr, Pro 5/sec, Ultra 10/sec, Mega 20/sec, PAYG 5/sec

**Pricing** (verified 2026-06-13): Free $0 (50/mo), Pro $25 (10K + $0.003/extra), Ultra $75 (50K + $0.002/extra), Mega $150 (200K + $0.001/extra), PAYG $0.005/req

---

#### 3. Local Business Data (Google Maps)

Search and retrieve detailed business information from Google Maps. Multiple endpoints for different data types.

**Base path**: `https://api.openwebninja.com/local-business-data/` (e.g. business search at `/local-business-data/search`).

**Endpoints**:

| Endpoint | Description |
|---|---|
| Business Search | Search businesses by query and location |
| Nearby Search | Find businesses near a geographic point |
| Reviews | Retrieve business reviews |
| Photos | Retrieve business photos |
| Posts | Retrieve business posts |
| Autocomplete | Location/business autocomplete suggestions |
| Bulk Search | Batch business search |

**Response fields** (40+ fields per business):

| Field | Type | Description |
|---|---|---|
| `business_id` | string | Unique business identifier |
| `place_id` | string | Google Place ID |
| `google_mid` | string | Google Maps ID |
| `name` | string | Business name |
| `phone_number` | string | Business phone number |
| `full_address` | string | Complete address |
| `latitude` | float | Geographic latitude |
| `longitude` | float | Geographic longitude |
| `rating` | float | Average rating |
| `review_count` | int | Number of reviews |
| `opening_hours` | object | Business hours |
| `email` | string | Business email (if available) |
| `facebook` | string | Facebook URL |
| `instagram` | string | Instagram URL |
| `twitter` | string | Twitter/X URL |
| `linkedin` | string | LinkedIn URL |
| `photos` | array | Business photos |
| `reviews` | array | Business reviews |
| `posts` | array | Business posts |

**Rate limits**:

| Tier | Rate |
|---|---|
| Free | 1,000 req/hr |
| Pro | 5 req/sec |
| Ultra | 8 req/sec |
| Mega | 10 req/sec |

**Billing**: per business, review, or photo OBJECT returned — not per API request. A search returning 20 businesses consumes 20 credits; extracting 100 reviews uses 100 credits.

**Pricing** (verified 2026-06-13): Free $0 (500 businesses/mo), Pro $25 (20K + $0.002/extra), Ultra $75 (100K + $0.001/extra), Mega $150 (300K + $0.0005/extra), PAYG $0.004/business

---

#### 4. Real-Time Web Search

Google SERP results including organic results, knowledge graph, AI overviews, AI Mode (Gemini-powered), videos, places, news, People Also Ask, and related searches.

**Endpoint**: `GET https://api.openwebninja.com/realtime-web-search/search` (primary query param is `q`).

**Capabilities**:

- Up to 500 organic results per query, but a maximum of 100 results in a single request (paginate to reach 500)
- Localized by region and language
- Bulk search support

**Result types**:

| Type | Description |
|---|---|
| Organic | Standard search results |
| Knowledge Graph | Entity/knowledge panel data |
| AI Overviews | Google AI-generated summaries |
| AI Mode | Google AI Mode results |
| Videos | Video results |
| Places | Local business results |
| News | News article results |
| People Also Ask | Related questions and answers |
| Related Searches | Suggested related queries |

**Response time**: 0.5–8 seconds depending on endpoint and parameters

**Rate limits**:

| Tier | Rate |
|---|---|
| Free | 1 req/sec |
| Pro | 10 req/sec |
| Ultra | 20 req/sec |
| Mega | 30 req/sec |

**Pricing** (verified 2026-06-13): Free $0 (100/mo), Pro $25 (10K + $0.003/extra), Ultra $75 (50K + $0.002/extra), Mega $150 (200K + $0.001/extra), PAYG $0.005/req

---

#### 5. Social Links Search

Find social media profiles for companies or people.

**Endpoint**: `GET https://api.openwebninja.com/social-links-search/search-social-links` (query param `query`, e.g. `query=John Smith`).

**Supported networks**: Facebook, Instagram, TikTok, LinkedIn, Twitter/X, GitHub, YouTube, Pinterest, Snapchat.

**Response fields**: results organized by platform, each a URL array — `facebook`, `instagram`, `twitter`, `linkedin`, `github`, `youtube`, `pinterest`, `tiktok`, `snapchat`.

**Response time**: 0.5–3 seconds.

**Rate limits**: Free 1/sec, Pro 5/sec, Ultra 10/sec, Mega 20/sec, PAYG 5/sec.

**Pricing** (verified 2026-06-13): Free $0 (50/mo), Pro $25 (10K + $0.003/extra), Ultra $75 (50K + $0.002/extra), Mega $150 (200K + $0.001/extra), PAYG $0.005/req.

---

#### 6. Web Unblocker

Fetch complete HTML from any webpage with JavaScript rendering, rotating proxies, and smart retries. Useful for scraping pages that block direct requests.

**Endpoint**: `https://api.openwebninja.com/web-unblocker/request` (supports all major HTTP methods — GET, POST, PUT, DELETE, PATCH).

**Parameters**: `render_js` (run JS), `wait_for_selector` (CSS selector to wait on), `wait_for_timeout` (fixed delay), `wait_until` (`domloaded` | `load` | `networkidle`), `extra_retries`, plus custom headers and cookies.

**Response**: status code, HTML body, final URL, response headers, and cookies array.

**Capabilities**: full JavaScript rendering, rotating proxy infrastructure, smart retry logic, anti-bot bypass.

**Pricing** (verified 2026-06-13 — note these quotas DIFFER from the other APIs): Free $0 (100/mo), Pro $25 (50K), Ultra $75 (250K), Mega $150 (1,000,000), PAYG $0.001/use. **JS-rendered requests cost 5 request credits each** across all tiers. Rate limits: Free 1,000/hr, Pro 10/sec, Ultra 20/sec, Mega 30/sec, PAYG 10/sec.

---

#### 7. JSearch (Jobs API)

Access job postings aggregated from Google for Jobs and the public web — including LinkedIn, Indeed, Glassdoor, ZipRecruiter, and other major job boards. Companion Job Salary Data API available for compensation intelligence.

**Endpoint**: `GET https://api.openwebninja.com/jsearch/search-v2`

**Pricing** (verified 2026-06-13): Free $0 (200 requests/mo), Pro $25 (10K + $0.003/extra), Ultra $75 (50K + $0.002/extra), Mega $150 (200K + $0.001/extra), PAYG $0.005/use. Rate limits: Free 1,000/hr, Pro 5/sec, Ultra 10/sec, Mega 20/sec, PAYG 5/sec.

> Note: the official JSearch page sources from "Google for Jobs and the Public Web" and does NOT state an aggregate listing count. The "200M+ listings" figure used elsewhere in this skill is not confirmed on the current API page — treat it as marketing/approximate.

---

### Webhook Support

Not documented. No webhook or callback support found in publicly available content (re-checked 2026-06-13) — these are synchronous request/response REST APIs only.

---

### Known Documentation Gaps

| Gap | Details |
|---|---|
| Error codes | Specific error response format / codes not documented on public pages (standard HTTP statuses expected; custom plans via support@openwebninja.com) |
| Rate-limit headers | Whether `X-RateLimit-*` style headers are returned is not documented |
| Webhook support | None documented (request/response only) |
| JSearch listing count | Current API page does not state an aggregate job-listing total |

> Base URL (`api.openwebninja.com/{api-name}/...`), `x-api-key` auth, per-API endpoint paths, the Social Links Search endpoint, and pagination (Real-Time Web Search: 100 results/request, 500 max) were all CONFIRMED against the live API pages on 2026-06-13 and are no longer gaps.

---

## Quick Reference — Common Workflows

### Scrape contacts from a domain
```bash
# Direct portal auth: x-api-key header. `query` accepts up to 20 comma-separated domains.
curl --request GET \
  --url "https://api.openwebninja.com/website-contacts-scraper/scrape-contacts?query=example.com" \
  --header "x-api-key: yourApiKey"
```

**Response** (expected):
```json
{
  "domain": "example.com",
  "emails": [
    {"value": "john@example.com", "sources": ["https://example.com/contact"]},
    {"value": "sales@example.com", "sources": ["https://example.com/about"]}
  ],
  "phone_numbers": [
    {"value": "+1-555-0100", "sources": ["https://example.com/contact"]}
  ],
  "facebook": "https://facebook.com/example",
  "instagram": "https://instagram.com/example",
  "twitter": "https://twitter.com/example",
  "linkedin": "https://linkedin.com/company/example"
}
```

### Search for email addresses
```bash
curl --request GET \
  --url "https://api.openwebninja.com/email-search/search-emails?query=Acme%20Corp&email_domain=acme.com" \
  --header "x-api-key: yourApiKey"
```

**Response** (expected):
```json
["john@acme.com", "sales@acme.com", "info@acme.com"]
```

### Search local businesses
```bash
curl --request GET \
  --url "https://api.openwebninja.com/local-business-data/search?query=coffee+shops&location=San+Francisco" \
  --header "x-api-key: yourApiKey"
```

**Response** (expected — partial):
```json
{
  "data": [
    {
      "business_id": "abc123",
      "name": "Blue Bottle Coffee",
      "full_address": "66 Mint St, San Francisco, CA 94103",
      "phone_number": "+1-555-0123",
      "rating": 4.5,
      "review_count": 1200,
      "email": "sf@bluebottle.com",
      "linkedin": "https://linkedin.com/company/blue-bottle-coffee"
    }
  ]
}
```

### Real-time web search
```bash
# Primary query param is `q`. Max 100 results per request; paginate to reach the 500 cap.
curl --request GET \
  --url "https://api.openwebninja.com/realtime-web-search/search?q=enterprise+SaaS+companies+Series+B&limit=20" \
  --header "x-api-key: yourApiKey"
```
