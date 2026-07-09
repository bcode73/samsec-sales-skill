# LitCommerce Platform Reference

## Overview

LitCommerce (litcommerce.com, by LitGroup — the LitExtension store-migration company) is a **multichannel listing & sync tool**: connect one **Main Store** (Shopify, WooCommerce, Wix, BigCommerce, Squarespace, or a CSV/XML/Google-Sheet file) to 20+ marketplaces and keep listings, price, inventory, and orders in sync from one dashboard, plus a separate **Product Feed** tool for exporting catalogs to ad/shopping/AI-search engines. It targets SMB and maker sellers expanding from a webstore onto marketplaces — the "Goldilocks" tier between toy cross-listers and enterprise systems (Linnworks/Rithum). Defining trait for integrators: **it has no public API or webhooks** — automation happens through feeds/CSV and at the Main Store layer.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| **Main Store connection** | One source of truth: Shopify / WooCommerce / Wix / BigCommerce / Squarespace, or a file (CSV/XML/Google Sheet) | UI connect (OAuth/app). File store re-imports on a schedule. |
| **Channel listing** | Create/publish listings to Amazon, eBay, Etsy, Walmart, TikTok Shop, Facebook Shops, Reverb, Faire, Temu, Shopee, Google | UI / bulk edit. Channel-native fields. **No API.** |
| **Listing templates & recipes** | Reusable listing rules per channel (eBay business policies, Etsy optimization, Amazon GTIN-exemption) | UI-only |
| **Inventory sync** | Main Store → channels, **every 15 min**; rules for buffers/min/max/fixed qty | UI-configured rules; runs automatically. **No API/webhook.** |
| **Price sync** | Main Store → channels with per-channel price modifiers + currency conversion | UI-configured; automatic |
| **Order sync** | Channel orders pulled into the Main Store / LitCommerce dashboard, **every 15 min**; sales reports | Orders land in the **Main Store** — read them via the store's API. **No LitCommerce API/webhook.** |
| **Product Feed tool** | Export catalog to 300+ ad/shopping platforms (Google, Meta, Pinterest, …); CSV/XML/JSON; multi-language/currency; **AI-search feeds (LLMs.txt, ChatGPT/OpenAI)** | Feed URLs + scheduled refresh (hourly on paid). Separate product. |
| **CSV/XML/Google-Sheet import** | Use a file as the Main Store; auth options on the source URL | The primary way to push external data *into* LitCommerce |
| **Storefront / site builder** | n/a — LitCommerce is not a store builder | UI-only (your Main Store owns the storefront) |

**No public REST API. No webhooks. No MCP server.** Verified against LitCommerce's own documentation. The only programmatic surfaces are (a) the **inbound CSV/XML/Google-Sheet import** (auth: none / Basic / Digest / auth-header token / Amazon S3) and (b) the **outbound Product Feed** export. Everything else is UI-configured automation that runs server-side on the 15-minute cycle.

## Pricing, limits & plan gates

*Best-effort — confirm current pricing on litcommerce.com/pricing.*

**Multichannel Listing Tool** (pay-as-you-go, by channels × listings; 20% off annual):

| Tier | ~Price/mo | Channels | Listings |
|---|---|---|---|
| Free trial | $0 (7 days) | full access | full access |
| Entry | $29 | 3 | 1,000 |
| Growth band | $49–$254 | 4–10 | 2,000–10,000 |
| Scale band | $259–$369 | 11–15 | 10,000–100,000 |
| Custom | negotiable | 15+ | 100,000+ |

- **Orders/month: unlimited** on all paid tiers. **Inventory/price/order sync interval: 15 minutes.**
- Plan-gated features (per pricing page): listing templates & recipes, single/multi listing edit mode, **AI-powered listing optimization (Etsy & eBay only)**, quick/scheduled auto-publish, bulk export/update, error reports, price & inventory modifiers, currency conversion, sales reports, live chat & email support.
- **Listing count is the gotcha:** variations multiply listings. 8,000 products with variants can exceed a 10,000-listing tier.

**Product Feed Tool** (separate product):
- **Free plan:** up to **2 feeds**, basic features, **no hourly sync**.
- **Paid:** hourly feed sync, AI Smart Setup, multi-language, currency conversion. No setup fees.

**No rate limits to manage** (no API). The 15-minute sync cadence is the effective throughput ceiling.

## Integrations

**Data-flow direction:**
- **Main Store → channels:** product data, price, inventory (one-directional for stock). LitCommerce *writes* listings and stock to marketplaces using their APIs.
- **Channels → Main Store:** orders are pulled from marketplaces and consolidated into the Main Store/LitCommerce dashboard. Fulfillment/tracking can sync back to the channel.
- **External → LitCommerce:** only via a **file Main Store** (CSV/XML/Google Sheet) it re-imports.
- **LitCommerce → external:** only via the **Product Feed** export (feed URL).

**Marketplaces/channels:** Amazon, eBay, Etsy, Walmart, TikTok Shop, Facebook Shops, Google (Shopping), Reverb, Faire, Temu, Shopee (+ "coming soon"). **Store platforms:** Shopify, WooCommerce, Wix, BigCommerce, Squarespace, Square (POS). **Shipping:** ShipStation (Shippo "coming soon").

**No native Zapier/Make app and no webhooks were found.** Treat LitCommerce as a closed sync engine: orchestrate around its endpoints (Main Store API + feed URL), not through it.

## Data model

LitCommerce does not publish a programmatic data model (no API). Conceptually the objects are:

```jsonc
// Main Store — your source of truth (Shopify/WooCommerce/file)
{
  "main_store": "shopify | woocommerce | wix | bigcommerce | squarespace | file",
  "product": {
    "sku": "TSHIRT-RED-L",
    "title": "Organic Cotton Tee",
    "price": 24.00,
    "quantity": 42,
    "identifiers": { "gtin": "0123456789012", "mpn": "TS-RED-L" },
    "variations": [ { "sku": "TSHIRT-RED-M", "quantity": 13 } ]
  }
}
```
<!-- Constructed from docs — verify against live behavior; LitCommerce exposes no API schema -->

```jsonc
// Channel listing — a product published to one channel, linked to the Main Store SKU
{
  "channel": "ebay | amazon | etsy | walmart | tiktok_shop | facebook",
  "linked_sku": "TSHIRT-RED-L",
  "channel_price": 26.40,            // after a per-channel price modifier (+10%)
  "channel_quantity": 41,            // after an inventory buffer rule (out-of-stock at 1)
  "template": "ebay-default",        // listing template / recipe applied
  "status": "active | error | ended"
}
```

```jsonc
// Inventory rule (configured in UI, applied in order)
{
  "percentage_modifier": 100,        // % of Main Store qty pushed to channel
  "fixed_qty_no_manage_stock": 999,  // qty for products not stock-managed
  "max_display_qty": 50,
  "min_display_qty": 0,
  "set_out_of_stock_at": 1           // the BUFFER that prevents overselling
}
```

```jsonc
// Order (pulled from channel into the Main Store) — read it via the STORE's API, not LitCommerce
{
  "source_channel": "amazon",
  "marketplace_order_id": "112-7654321-0000000",
  "main_store_order_id": 10482,      // LitCommerce writes it here; this is your integration point
  "line_items": [ { "sku": "TSHIRT-RED-L", "qty": 1 } ],
  "fulfillment": { "tracking": "1Z...", "carrier": "ups" }
}
```

## Quick-start recipes

Because there's no LitCommerce API, the "recipes" are about importing *into* it and reading data *out of the Main Store*.

### Recipe 1 — Feed an external catalog into LitCommerce via a file Main Store

Host a CSV (or Google Sheet published as CSV) and point LitCommerce at it as a **file Main Store**; it re-imports on a schedule. Supported source auth: none, Basic/Digest, an auth-header token, or Amazon S3.

```bash
# Verify your feed is reachable the way LitCommerce will fetch it (Basic auth example)
curl -u "$FEED_USER:$FEED_PASS" -sSL "https://files.example.com/catalog.csv" | head -5
# Expect a header row: sku,title,price,quantity,gtin,...
```

```python
# Generate the CSV LitCommerce will import (drive it from your own DB/ERP on a cron)
import csv
rows = [
    {"sku": "TSHIRT-RED-L", "title": "Organic Cotton Tee", "price": "24.00",
     "quantity": "42", "gtin": "0123456789012"},
]
with open("catalog.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["sku", "title", "price", "quantity", "gtin"])
    w.writeheader(); w.writerows(rows)
# Upload to your auth'd URL / S3; LitCommerce re-reads it on its sync cycle.
```
Gotcha: keep the column headers stable between imports — LitCommerce maps on the header row.

### Recipe 2 — Read consolidated multichannel orders (at the Main Store, not LitCommerce)

LitCommerce writes Amazon/eBay/Etsy orders into your Main Store. Pull them from the **store's** API.

```bash
# Shopify: orders LitCommerce created carry the channel as source/tags
curl -sS "https://$SHOP.myshopify.com/admin/api/2024-10/orders.json?status=any&limit=50" \
  -H "X-Shopify-Access-Token: $TOKEN"
```

```python
# WooCommerce: read orders + filter by the channel meta LitCommerce stamps
import requests
r = requests.get("https://store.example.com/wp-json/wc/v3/orders",
                 params={"per_page": 50},
                 auth=("ck_xxx", "cs_xxx"))
for o in r.json():
    print(o["id"], o.get("created_via"), o["line_items"][0]["sku"])
# Subscribe to WooCommerce HMAC-signed order webhooks for real-time CRM sync.
```
This is the supported path to a CRM/warehouse pipeline — LitCommerce itself emits no webhook.

### Recipe 3 — Publish a Google Shopping / AI-search feed

Use the **Product Feed Tool** (separate product). Map required attributes (id, title, description, link, image_link, price, availability, gtin), pick the destination template (Google Shopping, Meta catalog, Pinterest, or the **LLMs.txt / ChatGPT-OpenAI** AI-search feed), and set the refresh schedule (hourly requires a paid feed plan). The output is a feed **URL** you paste into Google Merchant Center / Meta Commerce Manager.

## Integration patterns

- **CRM/warehouse sync:** Don't wait for a LitCommerce webhook (none exists). Sync at the **Main Store**: Shopify/BigCommerce/WooCommerce order webhooks or scheduled API pulls, deduped on the marketplace order ID. LitCommerce's role is purely to land the channel order in the store.
- **Pushing inventory/products in:** Treat LitCommerce as a **pull-from-file** consumer. Publish a CSV/Sheet from your ERP/DB on a cron; LitCommerce re-imports it. There is no "create product" endpoint.
- **Oversell prevention:** Configure inventory rules so each channel goes out of stock at qty = 1–2. The 15-minute batch sync means buffers — not real-time calls — are the mitigation. For SKUs that must never oversell, reduce the channel's max display qty.
- **Reconciliation:** Because sync is one-directional and batched, run a periodic reconciliation that compares Main Store stock vs each channel's listed qty and flags drift; never hand-edit stock on a marketplace.
- **Reading "feed" vs "orders":** the Product Feed export is for **advertising/shopping engines**, not for getting your orders out — those two flows are unrelated.
