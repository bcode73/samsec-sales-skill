<!-- Source: https://spreecommerce.org/docs/api-reference/introduction -->
<!-- Source: https://spreecommerce.org/docs/api-reference/platform/authentication -->
<!-- Source: https://spreecommerce.org/docs/api-reference/platform/webhook-subscribers -->
<!-- Source: https://spreecommerce.org/docs/api-reference/platform/webhook-events -->
<!-- Source: https://spreecommerce.org/docs/llms.txt -->
<!-- Source: https://github.com/spree/spree -->
<!-- Source: https://spreecommerce.org/announcing-spree-commerce-5-5/ -->
<!-- Note: Spree's docs site is rendered client-side and served via an llms.txt index; WebFetch
     returned condensed (summarized) content rather than pure verbatim HTML. Endpoint prefixes,
     resource lists, the OAuth flow, and webhook shapes below are taken from the official docs +
     GitHub README above. Re-verify exact request/response field shapes, header names, and the
     webhook signature scheme against the live OpenAPI specs (admin.yaml / store.yaml /
     platform.yaml / storefront.yaml) before relying on them. See ## Gaps. -->

# Spree Commerce API Reference

Spree exposes **REST APIs with OpenAPI 3.0 specs** (no first-party GraphQL for the core engine; the Storefront part has had community GraphQL). There are **four API layers**, each with its own base path and auth scheme.

| API | Base path | Audience | Auth |
|---|---|---|---|
| **Store API** | `/api/v3/store` | Storefront / customer apps | **Publishable key** (`pk_xxx`) + per-cart **order token**; public reads need none |
| **Platform API** | `/api/v2/platform` | Backend / third-party management | **OAuth 2.0 client-credentials** → `Authorization: Bearer` |
| **Admin API** | `/api/v3/admin` | Back-office automation (open-sourced in 5.5) | **Scoped API keys** (per-resource permissions) |
| **Storefront API v2** (legacy) | `/api/v2/storefront` | Older storefront integrations | Bearer/order-token (JSON:API) |

- **OpenAPI specs:** `admin.yaml`, `store.yaml`, `storefront.yaml`, `platform.yaml`, `oauth.yml`, `openapi.json` (published with the docs).
- **TypeScript SDK:** `@spree/sdk` (install via npm/yarn/pnpm; init with `publishableKey: 'pk_xxx'`).
- **Dev base URL example:** `http://localhost:3000/api/v3/store`.

## Platform API authentication (OAuth 2.0 — verbatim shape)

**Method:** OAuth 2.0, **client-credentials** flow.
**Token endpoint:** `POST {store_url}/spree_oauth/token`

**Setup:** create an OAuth application in the admin via **Apps → OAuth Applications**, then record the generated **Client ID** and **Client Secret**.

**Request body:**

```json
{
  "grant_type": "client_credentials",
  "client_id": "xxx",
  "client_secret": "xxx",
  "scope": "admin"
}
```

**Response:** an `access_token` you include on subsequent requests as:

```
Authorization: Bearer {access_token}
```

Docs quote: *"Platform API is meant to be used by external applications to perform operations within Spree. Because of that, it uses a different authentication schema than the Storefront API."* Tokens expire — request a new one (handle 401 by re-authenticating).

### Auth quick-start (cURL)

```bash
# Get a token
curl -X POST https://your-store.example.com/spree_oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"CLIENT_ID","client_secret":"CLIENT_SECRET","scope":"admin"}'

# Simplest authenticated GET
curl https://your-store.example.com/api/v2/platform/products \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Store API authentication

The **Store API** (`/api/v3/store`) is identified by a **publishable key** (`pk_xxx`) set on the `@spree/sdk` client (or sent as a header, e.g. `X-Spree-Publishable-Key`). Cart/checkout operations are tied to a per-cart **order token** returned when a cart is created (sent on subsequent cart calls, e.g. `X-Spree-Order-Token`). Public catalog reads require no key. <!-- header names constructed from the publishable-key + order-token model — confirm exact header names against live Store API docs / @spree/sdk -->

## Admin API authentication (5.5+)

The **Admin API** (`/api/v3/admin`) was **open-sourced in Spree 5.5**. It can *"read and write every back office resource"* — catalog, orders, customers, promotions, gift cards, webhooks, settings. It uses **scoped API keys**: you can scope a key to specific resources so an integration only accesses what it needs. It ships its own **TypeScript SDK** and a **command-line client** that lets developers (and AI agents) run the whole back office from the terminal.

## Resource inventory (from the docs index)

**Platform API resources** (`/api/v2/platform/...`):
Addresses, Adjustments, Classifications, CMS Pages/Sections, Countries, Data Feeds, Digital Assets/Links, Line Items, Menus, Option Types/Values, **Orders**, Payment Methods, **Products**, **Promotions**, Roles, **Shipments**, Shipping, States, Stock, Store Credits, Taxes, Taxonomies, **Users**, **Variants**, **Vendors**, **Webhook Events / Subscribers**, Wishlists, Zones.

**Admin API resources** (`/api/v3/admin/...`):
Allowed Origins, API Keys, Authentication, Categories, Channels, Custom Fields, Customer Groups, Customers, Exports, Fulfillments, Gift Cards, Markets, Option Types, **Orders**, **Payments**, **Pricing**, **Products**, **Promotions**, Settings, Staff, Stock Locations, **Variants**, **Webhooks**.

**Store API resources** (`/api/v3/store/...`):
Authentication, **Carts**, Customers, Digitals, Markets, **Orders**, Policies, **Product Catalog**, Wishlists.

**Storefront API v2 resources** (legacy, `/api/v2/storefront/...`):
Accounts, Addresses, Credit Cards, Orders, Adyen/Stripe Payments, Cart Operations, Checkout, Countries, Digital Downloads, Policies, Products, Taxons, Variants, Vendors, Wishlists.

## Webhooks

Spree has **native outbound webhooks** ("Webhooks 2.0" + an Event Bus, per the 5.5 README), managed through the **Platform API**.

### Subscribe

`GET /api/v2/platform/webhooks/subscribers` returns existing subscribers; create one with a `POST` to the same collection. A subscriber has a **`url`**, an **`active`** flag, and a **`subscriptions`** array — `["*"]` subscribes to **all** events, or list specific event names.

```json
// Subscriber (response shape, abbreviated)
{ "url": "https://example.com/hooks/spree", "active": true, "subscriptions": ["*"] }
```

### Events + delivery log

Every delivery is recorded as a **Webhook Event** (`GET /api/v2/platform/webhooks/events`):

```json
{
  "id": "<id>", "type": "event",
  "attributes": {
    "name": "order.canceled",        // event name (dot-namespaced: <resource>.<action>)
    "url": "https://example.com/hooks/spree",
    "success": true,
    "response_code": "200",
    "execution_time": 142,           // milliseconds
    "request_errors": ""             // error messages if delivery failed
  },
  "relationships": { "subscriber": { "data": { "id": "1", "type": "subscriber" } } }
}
```

**Confirmed event name (example):** `order.canceled`. The naming pattern is `<resource>.<action>` (e.g. `order.*`, `product.*`). The **full event list and the exact signature/HMAC scheme were not captured verbatim** — see ## Gaps.

## Pagination

Platform/Admin APIs are **JSON:API** — page with `page[number]` and `page[size]` query params and follow the `links.next` URL until it's `null`:

```
GET /api/v2/platform/orders?page[number]=2&page[size]=100
```

## Error shape

JSON:API error responses return an `errors` array; auth failures return **401** (re-authenticate — the OAuth token likely expired or you're using the wrong token type for the API). <!-- constructed from JSON:API conventions — verify exact body against live API -->

## AI-agent / MCP surface (primary programmatic interface for makers, 5.5+)

- **Docs MCP server:** `https://spreecommerce.org/docs/mcp` — add the URL as a Connector in Claude Code (Connectors settings); gives an AI assistant authoritative, up-to-date answers drawn from Spree's documentation.
- **Agent skills:** ~25 installable skills at `github.com/spree/agent-skills` (best-effort install: `npx skills add spree/agent-skills`) — work with Claude Code, Cursor, Copilot, Codex, Cline, Aider, Zed, Windsurf, OpenCode, and 60+ tools. They teach Spree conventions (extending models safely, API shapes, checkout/pricing, upgrading without breaking customizations) and cut token use ~90% vs scanning source.
- **Admin API CLI client:** a command-line client lets developers/agents run the whole back office (products, orders, customers, inventory, pricing, promotions) from the terminal.
- **LLM-ready docs:** `llms.txt` index, per-page Markdown, an offline npm docs package, and generated `CLAUDE.md`/`AGENTS.md` in scaffolded projects.

## Gaps

- **Webhook signature scheme not confirmed.** Whether deliveries are signed (HMAC vs JWS) and the exact header name weren't captured verbatim (docs JS-rendered). Verify against the live `platform.yaml` / webhooks docs before trusting a public listener; gate the endpoint with a secret in the meantime.
- **Full webhook event catalog not captured** — only `order.canceled` confirmed by example; the `<resource>.<action>` pattern is inferred.
- **Exact Store API header names** (`X-Spree-Publishable-Key` / `X-Spree-Order-Token`) and full request/response bodies for cart/checkout were constructed from the documented publishable-key + order-token model — confirm against live Store API docs or the `@spree/sdk` source.
- **Per-endpoint request/response field shapes** are illustrative (JSON:API conventions) — the authoritative source is the OpenAPI specs (`platform.yaml`, `store.yaml`, `admin.yaml`, `storefront.yaml`).
- **Rate limits** for self-host are not published (you set your own infra limits); Cloud/Enterprise apply their own.
