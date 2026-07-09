# Spree Commerce Platform Guide

Full reference for the Spree Commerce headless commerce platform — modules and access surface, pricing/edition gates, data model, and quick-start recipes.

*Best-effort from research (2026-06). Re-verify pricing, edition gates, auth, and webhook-signature behavior against live docs at https://spreecommerce.org/docs.*

## What Spree is

Open-source (**BSD-3-Clause**), **API-first headless commerce framework** built on **Ruby on Rails**. You self-host the **Community Edition** for free (no per-sale fee) — running the Rails backend yourself — or run the **Enterprise Edition** (custom license + managed hosting). It ships a production-ready **Next.js storefront** separate from the commerce engine, REST APIs with **OpenAPI 3.0** specs, a fully-typed **TypeScript SDK** (`@spree/sdk`), and (5.5+) first-class **AI-agent tooling**.

Positioning: the **Ruby on Rails** counterpart to **Medusa** (Node/TS), **Saleor** (Python/Django, GraphQL), **Bagisto** (Laravel/PHP), and **Sylius** (Symfony/PHP) — and an open-source, self-hostable alternative to hosted SaaS like Shopify/BigCommerce. Built for **B2B, multi-vendor marketplace, multi-store/multi-tenant**, and DTC. The maker/GTM-engineer fit is the **self-hosted Community Edition**; Enterprise leans mid-market/enterprise.

Stack at a glance: **Ruby on Rails** backend, **PostgreSQL**, **Redis + Sidekiq** (background jobs), **MeiliSearch** (product search), **Next.js 16 / React 19 / Tailwind 4** storefront. Docker-ready; deploys to AWS/GCP/Azure/on-prem.

## Modules & access surface

"UI-only" means admin-dashboard-only with no API. Most resources are reachable through the **Platform API** and/or **Admin API**.

| Module | What it does | Access |
|---|---|---|
| **Products / Variants** | Catalog with properties, option types/values, rich media; variants carry price + stock | Platform / Admin / Store API |
| **Pricing & Price Lists** (5.3+) | Pricing engine: volume tiers, customer-specific pricing, time-based, per-market | Platform / Admin API |
| **Markets** | Cross-border selling — multi-currency, multi-language, region-specific tax rules | Platform / Admin API |
| **Sales Channels** (5.5) | Online store, POS, wholesale portal, mobile — per-channel catalogs, publication windows, order attribution | Platform / Admin API |
| **Orders / Line Items / Shipments** | Order management across channels, fulfillments, shipments | Platform / Admin / Store API |
| **Customers / Customer Groups** | Segmentation by group, order history, custom attributes; B2B buyer organizations | Platform / Admin API |
| **Promotions** | Rules-based discounts, coupons, gift cards, free shipping | Platform / Admin API |
| **Payments** | Provider-agnostic gateways (Stripe, Adyen, PayPal, …) via a **Payment Provider SDK** | Platform / Admin API |
| **Digital products / assets** | Sell + deliver downloadable goods (digital assets + links) | Platform / Store API (Digitals) |
| **Stock Locations / Reservations** (5.5) | Inventory across locations; stock reservations; rules-based **Order Routing** (5.5) | Platform / Admin API |
| **Multi-vendor marketplace** | Vendor dashboards, products, commission/payout controls | Platform API (Vendors) + UI |
| **Webhooks** | Outbound event delivery ("Webhooks 2.0" + Event Bus); subscribe + delivery log | Platform API (Webhook Subscribers/Events) |
| **CMS Pages / Menus** | Storefront content, navigation menus | Platform API |
| **Taxonomies / Taxons** | Category trees | Platform / Admin API |
| **Admin Dashboard** | Rails admin app with role-based permissions | UI (+ Admin API) |
| **AI-agent tooling** (5.5) | 25 agent skills, docs MCP server, Admin API CLI, generated CLAUDE.md/AGENTS.md | CLI / MCP / skills |

Official + community client tooling: **TypeScript SDK** (`@spree/sdk`); any HTTP client works against the REST + OpenAPI surface.

## Auth model (summary)

Four API layers, three auth schemes:

- **Store API** (`/api/v3/store`) — customer-facing. **Publishable key** (`pk_xxx`, set on the SDK / sent as a header) identifies the store; per-cart operations carry an **order token**. Public catalog reads need no key.
- **Platform API** (`/api/v2/platform`) — machine-to-machine management. **OAuth 2.0 client-credentials**: create an OAuth app in **Admin → Apps → OAuth Applications**, then `POST {store_url}/spree_oauth/token` (`grant_type=client_credentials`, `client_id`, `client_secret`, `scope=admin`) → `Authorization: Bearer {access_token}`. JSON:API responses.
- **Admin API** (`/api/v3/admin`, open-sourced in 5.5) — read/write every back-office resource with **scoped API keys** (scope a key to specific resources so an integration only touches what it needs). Has its own TypeScript SDK + CLI client.
- **Storefront API v2** (`/api/v2/storefront`) — legacy JSON:API compatibility layer (introduced in Spree 3.7); newer projects use the Store API.

See `references/spree-api-reference.md` for verbatim auth/endpoint/webhook detail.

## Pricing & edition gates

*Best-effort (2026-06) — verify at https://spreecommerce.org/enterprise/.*

| Edition | Price | Notes |
|---|---|---|
| **Community Edition** | Free (BSD-3) | Self-host; no license or per-sale fee. You pay hosting + DevOps + development. Cloud hosting typically **~$200–2,000/mo** by traffic. Community support (GitHub issues + docs). |
| **Enterprise Edition** | Custom (annual license) | Often **5–6 figures/yr** in year one (comparable to Shopify Plus). Adds SSO (**SAML/OIDC**), encryption at-rest, advanced **B2B / multi-vendor marketplace / multi-tenant SaaS** modules, premium support, and **managed hosting**. Contact-sales quote scaled to scale/traffic. |

No public API rate-limit numbers are published for self-host (you set your own infra limits); Cloud/Enterprise apply their own. **Spree is not a Merchant of Record** — you own tax calculation/remittance (use Markets tax rules + a tax service).

## Data model (shapes, not prose)

<!-- Constructed from documented field lists + JSON:API conventions — verify against live API -->

Platform API order (JSON:API envelope; amounts are decimal strings in the store/market currency):

```json
{
  "data": {
    "id": "1",
    "type": "order",
    "attributes": {
      "number": "R123456789",
      "state": "complete",
      "payment_state": "paid",
      "shipment_state": "shipped",
      "total": "59.98",
      "currency": "USD",
      "email": "buyer@example.com",
      "completed_at": "2026-06-29T12:00:00.000Z"
    },
    "relationships": {
      "line_items": { "data": [{ "id": "10", "type": "line_item" }] },
      "shipments":  { "data": [{ "id": "5",  "type": "shipment"  }] }
    }
  }
}
```

Webhook subscriber (Platform API) and a delivered Webhook Event record:

```json
// POST /api/v2/platform/webhooks/subscribers  (request)
{ "subscriber": { "url": "https://example.com/hooks/spree", "active": true, "subscriptions": ["order.canceled"] } }

// Webhook Event (delivery log, GET /api/v2/platform/webhooks/events)
{
  "data": { "id": "99", "type": "event",
    "attributes": {
      "name": "order.canceled", "url": "https://example.com/hooks/spree",
      "success": true, "response_code": "200", "execution_time": 142, "request_errors": ""
    },
    "relationships": { "subscriber": { "data": { "id": "1", "type": "subscriber" } } } }
}
```

## Quick-start recipes

### Recipe 1 — Get a Platform API token, then list products (cURL)

```bash
# 1) Exchange OAuth app credentials for a token
TOKEN=$(curl -s -X POST https://your-store.example.com/spree_oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type":"client_credentials","client_id":"CLIENT_ID","client_secret":"CLIENT_SECRET","scope":"admin"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# 2) Use it on the Platform API
curl -s https://your-store.example.com/api/v2/platform/products \
  -H "Authorization: Bearer $TOKEN"
```

### Recipe 2 — Export all orders with JSON:API pagination (Python)

```python
import requests

BASE = "https://your-store.example.com"

def token():
    r = requests.post(f"{BASE}/spree_oauth/token", json={
        "grant_type": "client_credentials",
        "client_id": "CLIENT_ID", "client_secret": "CLIENT_SECRET", "scope": "admin",
    })
    r.raise_for_status()
    return r.json()["access_token"]

def all_orders():
    headers = {"Authorization": f"Bearer {token()}"}
    url = f"{BASE}/api/v2/platform/orders?page[size]=100"
    orders = []
    while url:
        r = requests.get(url, headers=headers)
        if r.status_code == 401:                 # token expired — refresh and retry
            headers["Authorization"] = f"Bearer {token()}"
            continue
        r.raise_for_status()
        body = r.json()
        orders += body["data"]
        url = body.get("links", {}).get("next")  # JSON:API cursor of pages
    return orders

print(f"Exported {len(all_orders())} orders")
```

Pagination is **JSON:API page-based** (`page[number]` / `page[size]`); follow `links.next` until it's null rather than incrementing blindly.

### Recipe 3 — Store API cart flow (publishable key + order token)

```bash
# Create a cart (returns an order token in the response)
curl -X POST https://your-store.example.com/api/v3/store/cart \
  -H "Content-Type: application/json" \
  -H "X-Spree-Publishable-Key: pk_xxx"

# Add a line item to that cart (pass the order token for the cart)
curl -X POST https://your-store.example.com/api/v3/store/cart/add_item \
  -H "Content-Type: application/json" \
  -H "X-Spree-Publishable-Key: pk_xxx" \
  -H "X-Spree-Order-Token: ORDER_TOKEN" \
  -d '{"variant_id": "123", "quantity": 1}'
```

<!-- Header names (X-Spree-Publishable-Key / X-Spree-Order-Token) and Store-API paths are constructed from the documented publishable-key + order-token model — verify exact header + path against live Store API docs / the @spree/sdk client. -->

### Recipe 4 — Wire Spree into Claude Code / Cursor (AI-agent tooling)

```
# Docs MCP server — add this URL as a Connector in Claude Code (Connectors settings):
https://spreecommerce.org/docs/mcp

# Agent skills (best-effort — confirm the exact command in the live docs / spree/agent-skills repo):
npx skills add spree/agent-skills

# Admin API CLI — operate the whole back office (products/orders/customers/inventory/pricing/promotions)
# from the terminal so an agent can run the store without you hand-writing the HTTP layer first.
```

The skills teach an agent Spree's conventions (how to extend models safely, API shapes, checkout/pricing, **how to upgrade without breaking customizations**) and cut token use ~90% vs scanning Rails source. Scaffolded projects also generate a `CLAUDE.md`/`AGENTS.md`. Verify the exact install command and CLI name against the live "Using AI Tools for Development" docs.

## Integration patterns

- **Backend sync (CRM/warehouse):** authenticate with the **Platform API** OAuth token, pull `orders`/`customers`/`products` with JSON:API pagination, and store the JSON:API `id` + `type` as your join keys. Re-request the token on 401 (it expires). For near-real-time, prefer webhooks over polling.
- **Webhook listener:** create a **webhook subscriber** (`subscriptions: ["*"]` or specific events), verify deliveries against the live signature scheme (confirm before trusting — see SKILL Gotchas), gate the endpoint with a secret URL/header, and use the **Webhook Events** log to debug `response_code`/`request_errors`. Make handlers idempotent.
- **Storefront:** drive the **Store API** with a publishable key + per-cart order token, or use the official **Next.js storefront** + `@spree/sdk` rather than building the cart/checkout calls by hand.
- **Agent-driven ops:** for "let Claude Code build/run my store", start with the **agent skills + docs MCP server + Admin API CLI** instead of raw REST — they encode Spree's conventions and the safe upgrade path.

## When to pick Spree vs alternatives

- **vs Saleor** — both open-source + self-hostable + 0% fee. Spree = **Ruby on Rails + REST (OpenAPI) + native outbound webhooks**; Saleor = **Python/Django + GraphQL-first + native webhooks**. Choose by stack (Ruby vs Python) and API style (REST vs GraphQL).
- **vs Medusa** — both REST-ish + self-hostable. Spree = **Rails**; Medusa = **Node.js/TypeScript** with internal events/subscribers (no native webhook UI). Pick by language and whether you want built-in webhook delivery (Spree does).
- **vs Bagisto / Sylius** — those are PHP (Laravel / Symfony). Spree is the **Ruby/Rails** option. Pick by your team's language.
- **vs Shopify / BigCommerce** — those are hosted SaaS (no infra to run, app ecosystems) but charge fees and limit code-level control. Spree CE self-host gives full control + no per-sale fee at the cost of running a Rails stack.
