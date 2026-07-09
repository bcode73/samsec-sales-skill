### Lobstr.io API — Comprehensive Reference

Lobstr.io provides a REST API for web scraping and lead generation through an async workflow: configure a scraping job (squid), feed it URLs/parameters, execute a run, and retrieve structured JSON results. The platform offers 50+ ready-made crawlers for common sources like Google Maps, LinkedIn, and more.

> **Note**: Re-verified 2026-06-13 against the live official docs at https://docs.lobstr.io/ (incl. https://docs.lobstr.io/llms-full.txt). Base URL, auth, rate limits, and webhook events are unchanged. The endpoint surface is larger than originally documented (delete/empty/chain, abort/stats/credits/download, accounts, crawlers, credits) and is reflected below. Credit cost is now variable per crawler/enrichment function (see Credits).

---

## Base URL

```
https://api.lobstr.io/v1/
```

---

### Authentication

Token-based authentication via the `Authorization` header.

```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/runs" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json"
```

---

### Rate Limits

| Endpoint | Limit | Window |
|---|---|---|
| `/v1/squids` | 120 requests | per minute |
| `/v1/tasks` | 90 requests | per minute |
| `/v1/runtasks` | 90 requests | per minute |
| `/v1/runs` | 120 requests | per minute |
| `/v1/results` | 2 requests | per second |

**Rate limit headers** (included in every response):

| Header | Description |
|---|---|
| `X-RateLimit-Limit` | Maximum requests allowed in the window |
| `X-RateLimit-Remaining` | Requests remaining in the current window |
| `X-RateLimit-Reset` | Timestamp when the window resets |
| `Retry-After` | Seconds to wait before retrying (on 429) |

**Rate limit error** (HTTP 429):
```json
{
  "error": "Rate limit exceeded...",
  "type": "RateLimitExceeded",
  "code": 429
}
```

---

### Async Workflow

Lobstr.io uses an asynchronous scraping workflow:

1. **Choose a crawler** — Select from 50+ ready-made crawlers or create your own
2. **Create a squid** — `POST /squids` to create a scraping configuration
3. **Configure settings** — `POST /squids/{id}` to set `params.country`, `params.language`, `params.max_results`, plus scheduling via `cron_expression` + `timezone`
4. **Add tasks** — `POST /tasks` to feed URLs or parameters (also supports CSV upload)
5. **Start a run** — `POST /runs` to execute the scraping job
6. **Check status** — `GET /runs/{id}` to poll run progress
7. **Retrieve results** — `GET /results` to get structured JSON output

---

### Endpoints

---

#### 1. Squids (Scraping Configurations)

Create and configure scraping jobs.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/squids` | List your squids |
| POST | `/v1/squids` | Create a new squid (scraping configuration) |
| GET | `/v1/squids/{squid_hash}` | Get squid details |
| POST | `/v1/squids/{squid_hash}` | Configure / update squid settings |
| DELETE | `/v1/squids/{squid_hash}` | Delete a squid |
| POST | `/v1/squids/{squid_hash}/empty` | Empty a squid (clear its tasks/results) |
| GET | `/v1/squids/{squid_hash}/chain` | Get squid chain (chained squids) |
| POST | `/v1/squids/{squid_hash}/chain` | Configure / update squid chain |
| DELETE | `/v1/squids/{squid_hash}/chain` | Delete squid chain |

**Configuration parameters** (on `POST /v1/squids/{squid_hash}`, inside a `params` object):

| Parameter | Type | Description |
|---|---|---|
| `country` | string | Target country for the scrape (e.g. `"United States"`) |
| `language` | string | Language preference (e.g. `"English (United States)"`) |
| `max_results` | int | Maximum number of results to collect |

Additional settable top-level fields include `name`, `concurrency`, `is_active`, `to_complete`, `export_unique_results`, `no_line_breaks`, `run_notify`, `cron_expression`, and `timezone` (the last two drive scheduled automation).

**Example — Create a squid**:
```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/squids" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json"
```

**Example — Configure a squid** (note `params` wrapper + `max_results`):
```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/squids/SQUID_HASH" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"params": {"max_results": 150, "country": "United States", "language": "English (United States)"}}'
```

---

#### 2. Tasks (Scrape Inputs)

Feed URLs or parameters into a squid for scraping.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/tasks` | List tasks for a squid |
| POST | `/v1/tasks` | Add URLs/parameters to scrape |
| GET | `/v1/tasks/{task_hash}` | Get a single task |
| DELETE | `/v1/tasks/{task_hash}` | Delete a task |
| POST | `/v1/tasks/upload` | Bulk-upload tasks (e.g. CSV) |
| GET | `/v1/tasks/upload/{upload_task_id}` | Check bulk-upload status |

Tasks define what a squid should scrape. You can add them individually via the API or in bulk via CSV upload (`POST /v1/tasks/upload`, then poll the upload status endpoint).

**Example — Add tasks to a squid**:
```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/tasks" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "squid": "SQUID_ID",
    "urls": ["https://example.com/page1", "https://example.com/page2"]
  }'
```

---

#### 3. Runs (Job Execution)

Execute scraping jobs and monitor their progress.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/runs` | List runs |
| POST | `/v1/runs` | Start a scraping run |
| GET | `/v1/runs/{run_hash}` | Check run status |
| POST | `/v1/runs/{run_hash}/abort` | Abort a running job |
| GET | `/v1/runs/{run_hash}/stats` | Get run statistics |
| GET | `/v1/runs/{run_hash}/credits` | Get credits consumed by a run |
| GET | `/v1/runs/{run_hash}/download` | Download the run's results as a file |

**Run status lifecycle** (official): a run progresses `pending` → `running` → `uploading` → `done`, or transitions to `paused` / `aborted` / `error`. Runs are immutable once started but can be aborted. Poll `GET /v1/runs/{run_hash}` until a terminal state (`done`, `aborted`, or `error`).

**Example — Start a run**:
```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/runs" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "squid": "SQUID_ID"
  }'
```

**Example — Check run status**:
```bash
curl --request GET \
  --url "https://api.lobstr.io/v1/runs/RUN_ID" \
  --header "Authorization: Token YOUR_API_KEY"
```

---

#### 4. Results

Retrieve structured JSON output from completed runs.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/results` | Retrieve structured JSON results |

**Example — Get results**:
```bash
curl --request GET \
  --url "https://api.lobstr.io/v1/results?run=RUN_ID" \
  --header "Authorization: Token YOUR_API_KEY"
```

---

#### 5. Run Tasks (Task-Level Status)

Monitor individual task progress within a run.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/runtasks` | Check task-level status within a run |

Rate limited to 90 requests per minute.

---

#### 6. Accounts (Cookie-Based Login Sync)

Manage linked platform credentials (LinkedIn, Instagram, etc.) used by crawlers that scrape behind login walls. Accounts hold session cookies and can expire, requiring refresh.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/accounts` | List linked accounts |
| GET | `/v1/accounts/{account_hash}` | Get account details |
| DELETE | `/v1/accounts/{account_hash}` | Delete a linked account |
| POST | `/v1/accounts/{account_hash}/refresh` | Refresh cookies for an account |
| POST | `/v1/synchronize` | Sync an account (link to a squid) |
| GET | `/v1/synchronize/{sync_task_id}` | Check sync status |

---

#### 7. Crawlers (Ready-Made Scraper Catalog)

Discover the 50+ ready-made crawlers and their configurable parameters.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/crawlers` | List available crawlers |
| GET | `/v1/crawlers/{id}` | Get crawler details |
| GET | `/v1/crawlers/{id}/parameters` | Get a crawler's configurable parameters |
| GET | `/v1/crawlers/{id}/attributes` | Get a crawler's output attributes (result fields) |

---

#### 8. Credits & Account

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/me` | Get the authenticated user profile |
| GET | `/v1/credits/balance` | Get current credit balance |
| GET | `/v1/credits/modules` | Get credit-cost breakdown per module/function |

> **Credit model (changed):** Credits are **no longer a flat 1-per-result** charge. Per the official docs, "Each result collected consumes credits, with the rate depending on the crawler and any optional enrichment functions." As of a May 2026 update, "Credits are now tracked and reported per function" — base scraping and each enrichment function (e.g. email collection/validation) are billed and displayed separately. Use `GET /v1/runs/{run_hash}/credits` and `GET /v1/credits/modules` to see actual consumption.

---

### Webhooks

Configure webhook delivery to receive notifications when run status changes.

**Configuration endpoint**: `POST /v1/delivery?squid={squid_hash}`

```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/delivery?squid=SQUID_HASH" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "webhook_fields": {
      "url": "https://your-app.com/lobstr-callback",
      "is_active": true,
      "events": {
        "run.running": true,
        "run.paused": true,
        "run.done": true,
        "run.error": true
      },
      "retry": true
    }
  }'
```

**Webhook events**:

| Event | Description |
|---|---|
| `run.running` | Run has started executing |
| `run.paused` | Run has been paused |
| `run.done` | Run completed successfully |
| `run.error` | Run encountered an error |

**Webhook payload** (JSON) — verbatim shape from official docs. Note the run hash is a 32-char hex string and the timestamp is `YYYY/MM/DD HH:MM:SS` (UTC), **not** ISO 8601:

```json
{
  "id": "c39b1922a5424c3c84a7cb2ec731bc5f",
  "object": "run",
  "event": "run.done",
  "squid": {
    "id": "8177beb16fdf4e0e8d4b2ba767d1ffb5",
    "name": "Google Maps Search Export (1)"
  },
  "timestamp": "2025/06/18 17:32:31"
}
```

**Signing**: As of 2026-06-13 the official webhook docs document **no** HMAC signature or signing-secret header — there is no payload signature to verify. Treat the endpoint URL as the only secret and validate the `squid.id` against an allowlist.

**Retry behavior**: Failed webhook deliveries are retried up to 3 times with a 15-minute delay between attempts. Your endpoint should respond with HTTP 200, 201, or 202 within 30 seconds.

---

### Other Delivery Methods

Beyond webhooks, Lobstr.io supports exporting results to:

- **Amazon S3** — Direct export to S3 buckets
- **Google Sheets** — Automatic sync to spreadsheets
- **SFTP** — File transfer to your server
- **Gmail notifications** — Email alerts on completion

---

### SDKs and Tools

| Tool | Install | Description |
|---|---|---|
| Python SDK | `pip install lobstrio-sdk` | Sync + async clients, typed models, auto-pagination, full API coverage |
| CLI | `pip install lobstrio` | Command-line interface — run scrapers, manage squids, download results |
| MCP Server | — | Model Context Protocol server connecting AI assistants (Claude/Cursor) to the lobstr.io API/docs |

---

### Ready-Made Crawlers

Lobstr.io provides 50+ pre-built crawlers for common scraping targets. Each crawler has a unique ID that you reference when creating squids.

**Example**: Google Maps Leads Scraper — ID: `4734d096159ef05210e0e1677e8be823`

---

## Quick Reference — Common Workflows

### Scrape Google Maps leads end-to-end
```bash
# Step 1: Create a squid using the Google Maps Leads Scraper
curl --request POST \
  --url "https://api.lobstr.io/v1/squids" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"crawler": "4734d096159ef05210e0e1677e8be823"}'

# Step 2: Configure the squid
curl --request POST \
  --url "https://api.lobstr.io/v1/squids/SQUID_ID" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"country": "US", "language": "en"}'

# Step 3: Add search tasks
curl --request POST \
  --url "https://api.lobstr.io/v1/tasks" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"squid": "SQUID_ID", "urls": ["restaurants in Austin TX"]}'

# Step 4: Start the run
curl --request POST \
  --url "https://api.lobstr.io/v1/runs" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"squid": "SQUID_ID"}'

# Step 5: Poll for status
curl --request GET \
  --url "https://api.lobstr.io/v1/runs/RUN_ID" \
  --header "Authorization: Token YOUR_API_KEY"

# Step 6: Retrieve results
curl --request GET \
  --url "https://api.lobstr.io/v1/results?run=RUN_ID" \
  --header "Authorization: Token YOUR_API_KEY"
```

### Set up webhook notifications
```bash
curl --request POST \
  --url "https://api.lobstr.io/v1/delivery?squid=SQUID_HASH" \
  --header "Authorization: Token YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "webhook_fields": {
      "url": "https://your-app.com/lobstr-callback",
      "is_active": true,
      "events": {
        "run.done": true,
        "run.error": true
      },
      "retry": true
    }
  }'
```
