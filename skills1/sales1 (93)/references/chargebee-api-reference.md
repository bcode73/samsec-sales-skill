<!-- Source: https://apidocs.chargebee.com/docs/api (API v2 — Product Catalog 2.0), https://apidocs.chargebee.com/docs/api/subscriptions, https://apidocs.chargebee.com/docs/api/events, https://github.com/chargebee/agentkit -->
<!-- Captured 2026-06-29. Verbatim where copied from docs; JSON shapes marked "Constructed from docs" were assembled from documented field lists — verify against the live API. -->

# Chargebee API Reference

Chargebee exposes a REST-style HTTP API. There are **two API versions** (`v1` and `v2`); **v2 is current** and is what all new integrations should use. The version is part of the base URL.

> **Product Catalog matters.** The same API base serves both Product Catalog 1.0 (plans + addons) and 2.0 (items + item prices). The *endpoints and request params differ by catalog version* — a PC 1.0 call (`/plans`, `/addons`) will not work on a PC 2.0 site (`/items`, `/item_prices`). Confirm your site's catalog version before coding.

## Base URL

```
https://{site}.chargebee.com/api/v2/
```

Replace `{site}` with your Chargebee site name (e.g. `acme-test`). Test sites and live sites are **separate** `{site}` values with separate API keys.

## Authentication

HTTP **Basic Auth**: the **API key is the username** and the **password is empty**. All requests must use HTTPS.

```bash
# Simplest GET — list customers. Note the trailing colon: key as username, empty password.
curl https://{site}.chargebee.com/api/v2/customers \
  -u {api_key}:
```

- Keys are **environment-specific** (a test key won't work on the live site and vice versa).
- Key types: **full-access**, **publishable** (client-side, limited), **read-only**. Use the least-privileged key for the job.

## Request / response format

- **Requests:** `application/x-www-form-urlencoded` (form-encoded), even for POST writes. Nested params use bracket / index notation (e.g. `subscription_items[item_price_id][0]=...`).
- **Responses:** JSON with an **envelope**:
  - Single resource: `{ "customer": { ... } }`
  - A create/update that touches several objects returns them all: `{ "subscription": {...}, "customer": {...}, "invoice": {...} }`
  - List: `{ "list": [ { "customer": {...} }, ... ], "next_offset": "..." }`
- **Timestamps:** Unix **epoch seconds** (e.g. `1620000000`). `resource_version` is a **timestamp in milliseconds** (used for ordering — see Events).
- **Money:** integer in the **smallest currency unit** (cents). `4900` = $49.00. (Zero-decimal currencies like JPY use the whole unit.)

## HTTP methods

- **GET** — read operations (retrieve, list).
- **POST** — **all** writes: create, update, **and delete** (Chargebee does not use PUT/PATCH/DELETE verbs).

## Pagination

Offset-based. Responses include `next_offset` when more results exist; pass it back as `offset`.

- Default page size: **10**. Maximum `limit`: **100**.
- `offset` is an opaque token — pass it verbatim, do not construct it.

```bash
curl https://{site}.chargebee.com/api/v2/subscriptions \
  -u {api_key}: \
  --data-urlencode "limit=100" \
  --data-urlencode "offset={next_offset}" -G
```

List endpoints also accept **filter operators**, e.g. `status[is]=active`, `created_at[after]=1620000000`, `sort_by[asc]=created_at`.

## Idempotency

Send a unique value in the **`chargebee-idempotency-key`** request header on create/charge calls. Retries that reuse the same key within the **idempotency window (~30 minutes)** return the original result instead of creating a duplicate. Essential for safe retries on 429/5xx — without it, a retried "create subscription" or "charge" can double-bill.

```bash
curl https://{site}.chargebee.com/api/v2/subscriptions \
  -u {api_key}: \
  -H "chargebee-idempotency-key: 0b9c1f2e-..." \
  --data-urlencode "subscription_items[item_price_id][0]=pro-USD-monthly" \
  --data-urlencode "customer_id=cust_8a1"
```

## Error codes

| HTTP | Meaning |
|------|---------|
| 2xx  | Success |
| 400  | Bad request (validation, param error) |
| 401  | Authentication failed (bad/empty API key) |
| 404  | Resource not found |
| 429  | Too many requests (rate limited) |
| 5xx  | Server error — retry with backoff |

Error response shape:

```json
{
  "message": "Sorry, we couldn't find that resource",
  "type": "invalid_request",
  "api_error_code": "resource_not_found",
  "error_code": "resource_not_found",
  "http_status_code": 404
}
```
<!-- Constructed from docs — verify against live API. Branch on `api_error_code`, not the human `message`. -->

## Rate limiting

A **429** signals you've exceeded the limit. Chargebee does not publish a single fixed number in the API overview (limits vary by site/plan and endpoint); treat 429 as a signal to **back off and retry** with exponential backoff + jitter, and make writes idempotent (above) so retries are safe.

## Subscriptions

`https://{site}.chargebee.com/api/v2/subscriptions`

Connects a **customer** to the products/services they pay for; describes billing frequency and charges. Max **900 subscriptions per customer**.

Key attributes (verbatim field list from docs):

- `id` (string, ≤50 chars) — unique, auto-generated if not supplied
- `customer_id` (string, required) — owning customer
- `currency_code` (ISO 4217)
- `status` (enum) — `future`, `in_trial`, `active`, `non_renewing`, `paused`, `cancelled`, `transferred`
- `billing_period` + `billing_period_unit` — cycle length and unit (`day`/`week`/`month`/`year`)
- `current_term_start` / `current_term_end` — current billing-period boundaries (epoch seconds)
- `next_billing_at` — next scheduled billing date
- `trial_start`, `trial_end` — trial window
- `mrr` — monthly recurring revenue (**updated asynchronously**)
- `auto_collection` — `on` / `off` (charge automatically vs invoice)
- `payment_source_id` — attached payment source
- `meta_data` — custom key/value JSON (≤65,535 chars)
- `has_scheduled_changes` — pending modifications flag

Sample subscription object (PC 2.0):

```json
{
  "subscription": {
    "id": "8avVGOkx8U1MX",
    "customer_id": "cust_8a1",
    "status": "active",
    "currency_code": "USD",
    "billing_period": 1,
    "billing_period_unit": "month",
    "current_term_start": 1620000000,
    "current_term_end": 1622592000,
    "next_billing_at": 1622592000,
    "mrr": 4900,
    "auto_collection": "on",
    "subscription_items": [
      { "item_price_id": "pro-USD-monthly", "item_type": "plan", "quantity": 1, "amount": 4900 }
    ]
  }
}
```
<!-- Constructed from docs — verify against live API. PC 1.0 sites use plan_id/plan_quantity instead of subscription_items. -->

Common operations (paths under the base URL):

| Operation | Method | Path |
|-----------|--------|------|
| Create (for a customer) | POST | `/customers/{customer_id}/subscription_for_items` |
| Retrieve | GET | `/subscriptions/{id}` |
| List | GET | `/subscriptions` |
| Update items | POST | `/subscriptions/{id}/update_for_items` |
| Change term end / cancel | POST | `/subscriptions/{id}/cancel_for_items` |
| Pause / resume | POST | `/subscriptions/{id}/pause`, `/subscriptions/{id}/resume` |

> On PC 1.0 the equivalents are `/subscriptions` (create), `/subscriptions/{id}` (update), `/subscriptions/{id}/cancel` — operating on `plan_id`/`addons` rather than `subscription_items`/`item_price_id`.

## Events & webhooks

`https://{site}.chargebee.com/api/v2/events`

An **event** records an important change. Event JSON shape:

- `id` (string, ≤40 chars) — unique event id (**dedupe on this**)
- `occurred_at` — when it happened (epoch seconds, UTC)
- `source` — origin: `admin_console`, `api`, `scheduled_job`, `hosted_page`, `portal`, `bulk_operation`, `migration`, etc.
- `event_type` — category of change (see below)
- `content` — JSON object containing the affected resources, **structured by API version**
- `api_version` — `v1` or `v2`; determines the `content` structure (**set your webhook to v2**)

```json
{
  "event": {
    "id": "ev_16BdDsSrlR4Dxxxx",
    "occurred_at": 1620000123,
    "source": "scheduled_job",
    "event_type": "subscription_renewed",
    "api_version": "v2",
    "content": {
      "subscription": { "id": "8avVGOkx8U1MX", "status": "active", "...": "..." },
      "customer": { "id": "cust_8a1", "...": "..." },
      "invoice": { "id": "inv_889", "...": "..." }
    }
  }
}
```
<!-- Constructed from docs — verify against live API. -->

Important event types (verbatim list): `subscription_created`, `subscription_activated`, `subscription_changed`, `subscription_cancelled`, `subscription_renewed`, `payment_succeeded`, `payment_failed`, `invoice_generated`. (Many more exist — `subscription_paused`, `payment_refunded`, `customer_changed`, `card_expiry_reminder`, etc.)

### Webhook configuration & security — there is NO HMAC signature

Unlike Stripe/Paddle, Chargebee webhooks are **not HMAC-signed**. Authenticity is established by:

1. **Basic auth on the webhook URL** — set a username/password in the Chargebee dashboard; Chargebee sends them as the HTTP Basic credentials.
2. **A random secret embedded in the URL** — e.g. `https://api.example.com/cb/{long-random-key}`.
3. **IP allowlisting** — restrict inbound traffic to Chargebee's published IP ranges.
4. **Verify by re-fetching** — call the Retrieve Event API (`GET /events/{id}`) and trust the API's copy over the POST body for anything sensitive.

### Delivery semantics (design for these)

- **Out of order:** delivery order is **not** guaranteed. Use the **`resource_version`** (ms timestamp) on the resource inside `content` — process an update only if its `resource_version` is **newer** than what you've stored.
- **Duplicates / retries:** non-2XX responses are **retried for ~2 days** with increasing delays (final retry lands ~3 days out in practice). **Dedupe on the event `id`**, keeping a processed-id store for **3+ days**.
- **Missed events:** webhooks can be missed entirely. **Reconcile** periodically by pulling current state via the API (e.g. `GET /subscriptions?updated_at[after]=...`).
- Respond **2XX quickly** and process asynchronously; slow endpoints get treated as failures and retried.

## MCP server / AgentKit (programmatic AI interface)

Chargebee ships **AgentKit** (`github.com/chargebee/agentkit`) which includes an official **MCP server** (`@chargebee/mcp`) — a local Node server (requires Node.js LTS) that bridges an MCP client (Claude Desktop, Claude Code, Cursor, Windsurf, Cline) to Chargebee. It surfaces docs/product answers and **context-aware code snippets** for Chargebee API integrations.

Typical install (verify current command in the repo):

```bash
# via the Chargebee AgentKit MCP package (Node LTS required)
npx -y @chargebee/mcp
# then register it with your MCP client (claude mcp add ...), passing your Chargebee site + API key
```

## Client libraries

Official SDKs: **Python, PHP, Ruby, Go, .NET, TypeScript/Node, Java**. They wrap auth, form-encoding, pagination, and idempotency. Prefer an SDK over hand-rolling form encoding.

## Gaps / to verify against live docs

- Exact per-plan/per-endpoint **rate-limit numbers** (overview only references 429).
- Full **PC 1.0 vs 2.0** endpoint/param differences (only the common ones are tabulated here).
- The published **IP ranges** for webhook allowlisting (check the dashboard / docs — they change).
- Current **AgentKit/MCP** install command and tool list (the repo is the source of truth).
