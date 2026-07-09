<!-- Source: https://litcommerce.com , https://litcommerce.com/pricing/ , https://help.litcommerce.com (LLM docs interface: help.litcommerce.com/feed-management/overview.md?ask=…) — captured 2026-06-29 -->

# LitCommerce Integration Reference

> **No public REST API. No webhooks. No MCP server.** This was confirmed against LitCommerce's own documentation, which states it "can't find information in the docs about a public, customer-facing REST API, webhooks, or other developer endpoints." LitCommerce uses each **marketplace's** API on your behalf; it does not expose one of its own. This file documents the surfaces you *can* automate around.

## TL;DR for integrators

| Want to… | How (since there's no LitCommerce API) |
|---|---|
| Push products/inventory *into* LitCommerce | Use a **file Main Store** — CSV/XML/Google Sheet at a URL LitCommerce re-imports on its sync cycle |
| Get marketplace **orders out** | Read them from your **Main Store's** API (Shopify/WooCommerce/BigCommerce) — LitCommerce writes channel orders there |
| Get a **catalog feed out** | Use the **Product Feed Tool** → a feed URL (CSV/XML/JSON), incl. Google/Meta/Pinterest + AI-search (LLMs.txt, ChatGPT/OpenAI) |
| React to a sale in real time | Subscribe to your **Main Store's** webhooks (e.g. WooCommerce HMAC order webhook) — LitCommerce emits none |
| Query the docs programmatically | LitCommerce's help center exposes an **LLM-friendly docs interface** (see below) |

## Inbound: CSV/XML/Google-Sheet import (the only "write" surface)

LitCommerce can use a **file** as the Main Store and re-import it on a schedule. The source URL supports these auth methods (per the docs):

- **No Authentication** — public URL
- **Basic & Digest Authentication** — username/password
- **Authentication header (server-generated token)** — a token header on the request
- **Amazon S3** — AWS Access Key ID + Secret Access Key

Auth quick-start (verify your feed is reachable the way LitCommerce fetches it):

```bash
# No auth
curl -sSL "https://files.example.com/catalog.csv" | head -5

# Basic auth
curl -u "$FEED_USER:$FEED_PASS" -sSL "https://files.example.com/catalog.csv" | head -5

# Auth header token
curl -H "Authorization: Bearer $FEED_TOKEN" -sSL "https://files.example.com/catalog.csv" | head -5
```

Representative import CSV shape (column headers are the mapping keys — keep them stable):

```csv
sku,title,price,quantity,gtin,description,image_link
TSHIRT-RED-L,Organic Cotton Tee,24.00,42,0123456789012,Soft organic tee,https://cdn.example.com/red-l.jpg
```
<!-- Constructed from docs — exact required columns vary by Main Store/channel; verify in-account -->

## Outbound: Product Feed export

The **Product Feed Tool** is a separate product. It emits a **feed URL** (CSV/XML/JSON) you register with the destination (Google Merchant Center, Meta Commerce Manager, Pinterest, etc.).

- Required attributes typically include: `id`, `title`, `description`, `link`, `image_link`, `price`, `availability`, `gtin`/`mpn`.
- Supports multi-language and multi-currency variants.
- **AI-search feeds:** dedicated templates for **LLMs.txt** and **ChatGPT/OpenAI** product feeds (for AI shopping/search visibility).
- **Free plan: no hourly sync** (slower refresh). Hourly refresh + AI Smart Setup are on paid feed plans.

## Channel authentication (handled inside LitCommerce, not exposed to you)

When you connect a marketplace, LitCommerce performs that platform's own auth — e.g. eBay/Amazon/Etsy/TikTok OAuth, Temu's **Access Token** from Temu Seller Center, Walmart API keys. These credentials live inside LitCommerce; there is no LitCommerce token you receive or call with. Connection failures are almost always a missing **marketplace-side permission** (Amazon Professional plan, eBay business policies, TikTok Shop region/warehouse) rather than a LitCommerce bug.

## Sync behavior (effective "API contract")

- **Interval:** automatic every **15 minutes** for inventory, price, and order sync. Near-time, **not real-time** — this is the throughput ceiling and the root cause of overselling during bursts.
- **Inventory direction:** **Main Store → channels** only. Edits made directly on a marketplace do **not** propagate back and are overwritten on the next cycle.
- **Inventory rules (applied in order):** percentage modifier vs Main Store qty → fixed qty for "No Manage Stock" products → max/min display qty → **set out-of-stock-at-N** (the buffer that prevents overselling).
- **Multi-location:** with Shopify as Main Store, you choose which location(s) feed channel inventory.
- **Orders:** channel orders are imported into the Main Store/dashboard; fulfillment/tracking can sync back to the channel.

## Help-docs LLM interface (useful for agents)

LitCommerce's help center publishes machine-readable docs endpoints (discovered on its 404 page):

- **Ask interface:** `GET https://help.litcommerce.com/{section}/overview.md?ask=<url-encoded question>` — returns a docs-grounded answer.
- **Sitemap:** `https://help.litcommerce.com/sitemap.md`
- **Full export:** `https://help.litcommerce.com/llms-full.txt` — entire docs corpus as text.

These are documentation aids, **not** a product API — they return help content, not store data.

## Gaps

- No published REST endpoints, base URL, auth scheme, pagination, rate limits, or error schema — because **there is no public API**.
- No webhook payload schema — **no webhooks exist**.
- No native Zapier/Make app surfaced in research (verify in-account if you need iPaaS; the supported automation point remains the Main Store).
- Exact import column requirements and feed attribute mappings are configured in-account and were not exhaustively documented publicly — verify against the live setup.
