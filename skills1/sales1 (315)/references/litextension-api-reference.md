<!-- Source: https://litextension.com + https://litextension.com/migration-guide (per-cart access guides), researched 2026-07-04. -->

# LitExtension Automation Surface

**No public API. No webhooks. No MCP server.** LitExtension is a hosted migration tool + service — you cannot script it from your own backend. This file documents what *does* exist programmatically around it.

## What "integration" means here

LitExtension's connectors consume **your store platforms' APIs** (or a bridge file). Preparing that access is the developer-facing work:

| Store type | Access LitExtension needs | Where documented |
|---|---|---|
| Shopify | Custom-app Admin API token with read scopes (write scopes on the target) | litextension.com/migration-guide/get-api-key.html |
| WooCommerce | REST API consumer key/secret | per-cart guide |
| BigCommerce / Wix / Squarespace / Ecwid / hosted carts | Platform API token per their guide | per-cart guides (get-api-{cart}.html) |
| Self-hosted carts without usable APIs (older OpenCart, PrestaShop, custom PHP) | **Bridge file** uploaded to the store webroot | migration-guide bridge instructions |

**Bridge-file security note**: the bridge is privileged code in your webroot granting LitExtension read (and on targets, write) access to store data. Upload it for the migration, verify the connection, and **delete it when the migration window closes**.

## Custom/API migration service

For custom sources (homegrown carts, SQL dumps, CSV/Excel/XML) LitExtension offers an "API Data Migration Service" — their engineers write the extraction/mapping against REST/SOAP/GraphQL sources. That's a service engagement, not a self-serve API.

## Programmatic alternatives (when you need real automation)

If the requirement is scriptable migration — repeatable runs, CI-driven, custom transforms — LitExtension is the wrong layer. Write against the platforms directly:

```bash
# Pattern: export from source API → transform → import via target API
# e.g. WooCommerce → Shopify
curl -u "$WC_KEY:$WC_SECRET" "https://old-store.com/wp-json/wc/v3/products?per_page=100&page=1"
# ...transform...
curl -X POST "https://your-store.myshopify.com/admin/api/2026-01/products.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_TOKEN" -H "Content-Type: application/json" -d @product.json
```

See `/sales-store-migration` for when a custom pipeline beats a tool, and the platform skills (`/sales-shopify`, `/sales-prestashop`, `/sales-bigcommerce`, …) for each store's API specifics.

## Gaps

- guide.litextension.com (their OpenAPI/migration-preparation docs subdomain) did not resolve at research time — if it returns, it documents source-connection preparation, not a public LitExtension API.
- Exact Smart Update window terms (~3 months, ~10% growth cap) and pricing are best-effort — confirm in-account.
