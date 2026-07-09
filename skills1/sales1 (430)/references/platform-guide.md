# PrestaShop Platform Reference

## Overview

PrestaShop is a **long-running open-source, self-hosted PHP/MySQL commerce platform**
(founded 2007, France) aimed at developers, agencies, and technical merchants — the
European counterpart to WooCommerce/OpenCart/Magento. You **download and run the code
yourself** (PrestaShop **Classic**, free, licensed **OSL-3.0** for core / **AFL-3.0** for
modules), or buy the managed **Hosted** offer ("PrestaShop Ready"). Its differentiators
are a **300+ feature** back office out of the box, a large **module + theme Addons
marketplace**, a **hook system** for extensibility, and a stable **CRUD Webservice REST
API** at `/api/`. It is **not a Merchant of Record** — you own tax, hosting, and PCI scope.

## Capabilities & automation surface

| Module / capability | What it does | Automation surface |
|---|---|---|
| Catalog (products, combinations, features, options) | Products with variants ("combinations"), attributes, features, manufacturers, suppliers, categories | **API-accessible** (`products`, `combinations`, `product_options`, `categories`, …) |
| Stock / inventory | Per-product available quantity; optional Advanced Stock Management (warehouses, supply orders, movements) | **API-accessible** (`stock_availables` GET/PUT/PATCH; ASM resources GET/POST) |
| Orders & fulfillment | Orders, order details/rows, states, histories, invoices, slips (refunds), carriers | **API-accessible** (`orders`, `order_details`, `order_histories`, `order_states`, …) |
| Customers & addresses | Customers, groups, guests, addresses, customer-service threads/messages | **API-accessible** (`customers`, `groups`, `addresses`, `customer_threads`) |
| Carts | Live/abandoned carts, cart rules (discounts/promotions) | **API-accessible** (`carts`, `cart_rules`) |
| Pricing & tax | Specific prices, specific-price rules, taxes, tax rules, currencies, zones | **API-accessible** (`specific_prices`, `taxes`, `tax_rules`, `currencies`) |
| CMS content | CMS pages, contacts, stores | **API-accessible** (`content_management_system`, `contacts`, `stores`) |
| Multistore | One install, many shops/shop-groups/URLs | **API-accessible** (`shops`, `shop_groups`, `shop_urls`; scope calls with `id_shop`) |
| Images | Product/category/manufacturer images | **API-accessible** (`images`, `image_types` — binary upload) |
| Storefront theme & back-office pages | Themes (Smarty templates), admin UI | **UI-only** (build a theme/module; not a REST resource) |
| Payment / shipping modules | Stripe, PayPal, Klarna, Alma, carriers, etc. | **Module-based** (installed from Addons; behaviour configured in UI, extended via hooks) |
| Event notifications | React to order/stock/customer changes | **No native webhooks** — use a **module hook** or a 3rd-party "Webhooks" module, or poll |

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — re-verify against prestashop.com.*

- **PrestaShop Classic (open-source):** the software is **free**. Real cost is **hosting** (~$5–30/mo shared, $50–200/mo VPS/dedicated), a **domain** (~$10–20/yr), and any **paid modules/themes** from Addons (one-off or subscription; this is where budgets actually go). No per-sale platform fee — you only pay your payment processor.
- **PrestaShop Hosted ("Ready"):** ~**€29/mo** (~€24/mo billed annually) bundling hosting, support (email/chat/phone ~6 days/week), pre-installed modules, and a **free domain for year one**.
- **API limits:** the Webservice has **no published rate limit** — throughput is bounded by your server. Enable/keys are self-managed; scope each key's permissions per resource.
- **Plan gate to watch:** none on the *API* (it ships with core), but **Advanced Stock Management** must be enabled for warehouse/supply resources, and many capabilities (advanced marketing, some payment methods) are **paid modules**, not core.

## Integrations

- **Direction:** the Webservice is **bidirectional CRUD** but **pull-only for events** (no outbound webhooks in core).
- **Native connectors:** payment (PayPal/PrestaShop Checkout, Stripe, Klarna, Alma, Viva.com, Airwallex), marketing (Google, Klaviyo), social (Facebook/Instagram sync) — all delivered as **modules**.
- **iPaaS:** **Zapier** and **Make** both list a PrestaShop app (new-order/new-customer triggers, create-record actions). Several **Addons "Webhooks" modules** turn hooks into outbound HTTP POSTs.
- **CRM/warehouse sync:** read `orders`/`customers`/`stock_availables` on a schedule, or push via a module hook (`actionValidateOrder`, `actionObjectProductUpdateAfter`) — see the API reference §11.
- **Clients:** official **PHP `PrestaShopWebserviceLib`**, a documented **Postman** collection; unofficial Python/Node SDKs exist.

## Data model

PrestaShop's API is a thin CRUD layer over its DB. **XML is the native format**; add
`output_format=JSON` for JSON. IDs are **integers**. Translatable fields (name,
link_rewrite, description) are **per-language** (`<language id="1">…`). Money is a
**decimal string** (e.g. `"72.900000"`), not integer cents.

**Product** (abridged, `display=full`):

<!-- Constructed from docs — verify against live API -->
```json
{
  "product": {
    "id": 1,
    "reference": "sku-1001",
    "price": "19.900000",
    "active": "1",
    "id_category_default": "2",
    "link_rewrite": [{ "id": "1", "value": "blue-widget" }],
    "name":         [{ "id": "1", "value": "Blue Widget" }],
    "associations": {
      "combinations":  [{ "id": "1" }],
      "categories":    [{ "id": "2" }],
      "images":        [{ "id": "5" }]
    }
  }
}
```

**Order** (abridged): `id`, `id_customer`, `id_cart`, `current_state`, `reference`,
`total_paid`, `payment`, `date_add`, and `associations.order_rows[]` (product_id,
product_quantity, unit_price_tax_incl). Stock lives on **`stock_availables`**
(`id_product`, `id_product_attribute`, `quantity`, `depends_on_stock`), **not** on the
product. Full JSON shapes and the create/update/delete flow are in
`references/prestashop-api-reference.md`.

## Quick-start recipes

### Recipe 1 — Nightly product/stock sync from your ERP (developer)

**Trigger:** cron. **Goal:** upsert products and set quantities.

```bash
# 1. auth check + discover verbs
curl -s -u "$PS_KEY:" "https://shop.example.com/api/?output_format=JSON" | head

# 2. update stock for product 1 (find its stock_available row, then PUT quantity)
curl -s -u "$PS_KEY:" \
  "https://shop.example.com/api/stock_availables?output_format=JSON&filter[id_product]=1&display=full"
# → mutate <quantity> and PUT the row back
```

```python
import requests
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth(PS_KEY, "")
# create a product from the blank schema (XML in), then verify via JSON out
tmpl = requests.get("https://shop.example.com/api/products", auth=auth,
                    params={"schema": "blank"}).text
# ...fill tmpl (set price, reference, name/link_rewrite per language)...
r = requests.post("https://shop.example.com/api/products", auth=auth,
                  data=tmpl.encode(), headers={"Content-Type": "text/xml"})
r.raise_for_status()
```

**Gotchas:** `link_rewrite`/`reference` must be clean slugs; PUT replaces the whole entity
(GET→mutate→PUT); set stock via `stock_availables`, not `products`.

### Recipe 2 — Push new orders to a CRM without webhooks (developer)

**Trigger:** order placed. **There is no webhook screen** — use a hook module.

- Create a tiny module registering `actionValidateOrder` (and `actionOrderStatusUpdate` for status changes). In the handler, cURL a JSON payload to your CRM with an **HMAC `X-PS-Signature`** header (see api-reference §11).
- Hooks run **in-process during checkout** — keep the call fast (short timeout) or enqueue and process out of band, so a slow CRM never blocks the buyer.
- **Fallback if you can't deploy a module:** poll `orders?sort=[id_DESC]&filter[date_add]=[…]` and track the last-seen `id`, or use a Zapier/Make "new order" trigger.

### Recipe 3 — Export orders to a warehouse (developer)

Page with `limit=start,count` + stable `sort=[id_ASC]`, request only the fields you need
with `display=[…]`, and use `output_format=JSON`. Full loop in api-reference §12.

## Integration patterns

- **Auth:** HTTP **Basic**, username = 32-char key, **password empty**. If every call 401s, add **`CGIPassAuth On`** to `.htaccess` — Apache/PHP-FPM strips the `Authorization` header otherwise (the #1 setup failure).
- **Reads:** `display` to trim fields, `filter[field]` (OR `[a|b]`, interval `[min,max]`, `%pattern%`), `sort=[field_ASC]`, `limit=start,count`. No cursor — offset paging only.
- **Writes:** POST/PUT take **XML** (fetch `?schema=blank` first); PUT is a **full replace**; `PATCH` only on select resources (`stock_availables`, `warehouses`). Bulk delete via `?id=[1,2,3]`.
- **Events → push:** module hook (reliable) or 3rd-party Webhooks module; otherwise poll. Always add your own shared-secret/HMAC on outbound calls — nothing is signed for you.
- **Multistore:** scope reads/writes with `id_shop` / `id_group_shop`; keys can be shop-scoped.
- **Ops reality:** you own PHP/MySQL. Match the **PHP version** to your PrestaShop version, keep overrides thin, and test the **1-Click Upgrade** on staging first — third-party modules and overrides are what break on major upgrades (1.6→1.7 Symfony shift, PHP 7→8 deprecations).
