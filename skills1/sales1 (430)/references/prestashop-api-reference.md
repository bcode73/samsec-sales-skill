<!-- Source: https://devdocs.prestashop-project.org/9/webservice/ (Getting started, Creating access, Testing access, Cheat sheet, Reference) — captured 2026-07-02 -->

# PrestaShop Webservice API Reference

PrestaShop exposes **a CRUD API, otherwise called a web service**, that lets third-party
tools read and write your shop's database. This file captures the API surface verbatim
from the PrestaShop 9 Developer Documentation, then enriches it with working developer
recipes (cURL + Python). Re-verify specifics against the live docs before relying on them.

> **Naming note:** PrestaShop calls this the **Webservice** (one word). It is a REST-style
> CRUD API returning **XML by default** (JSON is opt-in via `output_format=JSON`). It is
> **not** the same as the newer Symfony-based Admin API work; this Webservice is the
> long-standing, stable integration surface at `/api/`.

---

## 1. Enabling the Webservice

The webservice feature is **disabled by default** and must be activated before use.

**Via the back office:** Navigate to **Advanced Parameters → Web service** and set
**"Enable PrestaShop Webservice"** to **Yes**.

**Programmatically** (inside a module or override):

```php
<?php
Configuration::updateValue('PS_WEBSERVICE', 1);   // enable
// Configuration::updateValue('PS_WEBSERVICE', 0); // disable
```

---

## 2. Creating an access key

**Via the back office:** Advanced Parameters → Webservice → **Add new webservice key**.

Each key has:

- **Key** — a **32-character** unique identifier (click **Generate**, or supply your own 32-char value). This *is* the credential; there is no separate password.
- **Key description** — free-text note about the key's purpose.
- **Status** — enable/disable the key at any time.
- **Permissions** — per-resource rights (GET/View, POST/Add, PUT/Modify, DELETE, HEAD). Grant only what the integration needs.
- **Shop association** — in multistore mode, scope the key to specific shops.

**Programmatically:**

```php
<?php
$apiAccess = new WebserviceKey();
$apiAccess->key = 'GENERATE_A_COMPLEX_VALUE_WITH_32_CHARACTERS';
$apiAccess->save();

$permissions = [
  'customers' => ['GET' => 1, 'POST' => 1, 'PUT' => 1, 'PATCH' => 1, 'DELETE' => 1, 'HEAD' => 1],
  'orders'    => ['GET' => 1, 'POST' => 1, 'PUT' => 1, 'PATCH' => 1, 'DELETE' => 1, 'HEAD' => 1],
];
WebserviceKey::setPermissionForAccount($apiAccess->id, $permissions);
```

---

## 3. Endpoint & authentication

The API lives at **`/api/`** at the root of your PrestaShop install:

- Root install: `https://example.com/api/`
- Subfolder install: `https://example.com/prestashop/api/`

Authentication is **HTTP Basic**, where the **username is your 32-character API key** and
the **password is empty**.

**Three ways to authenticate:**

1. **Browser prompt** — the browser asks for credentials; enter the API key as the username, leave the password blank.
2. **Key in URL** *(NOT recommended — leaks the key into history/logs):*
   ```
   https://UCCLLQ9N2ARSHWCXLT74KUKSSK34BFKX@example.com/api/
   ```
3. **Authorization header (recommended)** — base64-encode `KEY:` (note the trailing colon):
   ```php
   <?php
   $apiKey = 'UCCLLQ9N2ARSHWCXLT74KUKSSK34BFKX';
   $authorizationKey = base64_encode($apiKey . ':');
   // Header: Authorization: Basic VUNDTExROU4yQVJTSFdDWExUNzRLVUtTU0szNEJGS1g6
   ```

> **⚠️ CGIPassAuth footgun.** On Apache/PHP-FPM the `Authorization` header is often
> **stripped** before PHP sees it, so every call 401s even with a valid key. Fix in
> `.htaccess` at the shop root:
> ```apache
> CGIPassAuth On
> ```
> or, if that directive is unavailable:
> ```apache
> SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
> ```

---

## 4. Root response — discovering resources

`GET /api/` returns an XML document listing every resource the key can reach, with the
allowed HTTP verbs as attributes and links to blank/synopsis schemas:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
    <api shopName="Prestashop">
        <addresses xlink:href="http://example.com/api/addresses"
                   get="true" put="true" post="true" patch="true"
                   delete="true" head="true">
            <description>The Customer, Brand and Customer addresses</description>
            <schema xlink:href="http://example.com/api/addresses?schema=blank"
                    type="blank"/>
            <schema xlink:href="http://example.com/api/addresses?schema=synopsis"
                    type="synopsis"/>
        </addresses>
        <!-- ...one node per resource... -->
    </api>
</prestashop>
```

**Schemas for creating records:**

- `GET /api/{resource}?schema=blank` → empty XML template you fill in and POST.
- `GET /api/{resource}?schema=synopsis` → same template annotated with `required`, size limits, and format validators.

---

## 5. Cheat sheet — query parameters

All parameters are passed as **query strings regardless of the HTTP method**.

**Generic overrides:**

| Parameter | Purpose |
|---|---|
| `output_format` | Response format: `XML` (default) or `JSON`. |
| `ps_method` | Override the HTTP method when a client can't send it: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. |
| `language` | Return translatable fields in a language id, e.g. `language=3` or a set `language=[3\|5]`. |
| `id_shop` / `id_group_shop` | Target a shop or shop group when multistore is active. |

**List / filtering parameters:**

| Parameter | Purpose | Example |
|---|---|---|
| `display` | Which fields to return; `full` returns all. | `display=full` or `display=[id,reference,total_paid]` |
| `filter[field]` | Filter rows. Supports OR `[a\|b]`, interval `[min,max]`, literal, and `%pattern%`. | `filter[active]=1`, `filter[id]=[1,10]`, `filter[name]=[shirt]%` |
| `sort` | Order results, `field_ASC` / `field_DESC`. | `sort=[id_DESC]` |
| `limit` | Cap rows, or `start,count` for paging. | `limit=50` or `limit=100,50` |
| `date` | Set to `1` to enable `date_add`/`date_upd` range filters. | `date=1&filter[date_add]=[2026-01-01,2026-06-30]` |

There is **no cursor**; pagination is **offset-based** via `limit=start_index,count`.

---

## 6. Resources (verbatim from the Reference)

Every resource is under `/api/{resource}`. Verbs shown are those exposed by the Webservice.

| Resource | Description | HTTP Methods |
|----------|-------------|--------------|
| addresses | Customer, Manufacturer and Customer addresses | GET, POST, PUT, DELETE, HEAD |
| attachments | Product Attachments | GET, POST, PUT, DELETE, HEAD |
| attachments/file | Product Attachments files | GET, POST, PUT, DELETE, HEAD |
| carriers | Carriers that perform deliveries | GET, POST, PUT, DELETE, HEAD |
| cart_rules | Cart rules management (discount, promotions, …) | GET, POST, PUT, DELETE, HEAD |
| carts | Customer's carts | GET, POST, PUT, DELETE, HEAD |
| categories | Product categories | GET, POST, PUT, DELETE, HEAD |
| combinations | Product combinations | GET, POST, PUT, DELETE, HEAD |
| configurations | Shop configuration storage | GET, POST, PUT, DELETE, HEAD |
| contacts | Shop contacts | GET, POST, PUT, DELETE, HEAD |
| content_management_system | Content management system (CMS pages) | GET, POST, PUT, DELETE, HEAD |
| countries | Countries available on the shop | GET, POST, PUT, DELETE, HEAD |
| currencies | Currencies installed on the shop | GET, POST, PUT, DELETE, HEAD |
| customer_messages | Customer services messages | GET, POST, PUT, DELETE, HEAD |
| customer_threads | Customer services threads | GET, POST, PUT, DELETE, HEAD |
| customers | E-shop's customers | GET, POST, PUT, DELETE, HEAD |
| customizations | Product customizations | GET, POST, PUT, DELETE, HEAD |
| deliveries | Product deliveries | GET, POST, PUT, DELETE, HEAD |
| employees | Shop Employees | GET, POST, PUT, DELETE, HEAD |
| groups | Customer's groups | GET, POST, PUT, DELETE, HEAD |
| guests | Guests (customers not logged in) | GET, POST, PUT, DELETE, HEAD |
| image_types | Image types | GET, POST, PUT, DELETE, HEAD |
| images | Images | GET, POST, PUT, DELETE, HEAD |
| languages | Shop languages | GET, POST, PUT, DELETE, HEAD |
| manufacturers | Product manufacturers | GET, POST, PUT, DELETE, HEAD |
| messages | Customers messages | GET, POST, PUT, DELETE, HEAD |
| order_carriers | Order carriers | GET, POST, PUT, DELETE, HEAD |
| order_details | Details of an order | GET, POST, PUT, DELETE, HEAD |
| order_histories | Order histories | GET, POST, PUT, DELETE, HEAD |
| order_invoices | Order invoices | GET, POST, PUT, DELETE, HEAD |
| order_payments | Order payments | GET, POST, PUT, DELETE, HEAD |
| order_slip | Order slips (used for refund) | GET, POST, PUT, DELETE, HEAD |
| order_states | Order states (Waiting for transfer, Payment accepted, …) | GET, POST, PUT, DELETE, HEAD |
| orders | Customers orders | GET, POST, PUT, DELETE, HEAD |
| price_ranges | Price range | GET, POST, PUT, DELETE, HEAD |
| product_customization_fields | Product customization fields | GET, POST, PUT, DELETE, HEAD |
| product_feature_values | Product feature values | GET, POST, PUT, DELETE, HEAD |
| product_features | Product features | GET, POST, PUT, DELETE, HEAD |
| product_option_values | Product option values (S, M, L, … - White, Camel, …) | GET, POST, PUT, DELETE, HEAD |
| product_options | Product options (Size, Color, …) | GET, POST, PUT, DELETE, HEAD |
| product_suppliers | Product Suppliers | GET, POST, PUT, DELETE, HEAD |
| products | Products | GET, POST, PUT, DELETE, HEAD |
| search | Search resources | GET, POST only |
| shop_groups | Shop groups from multi-shop feature | GET, POST, PUT, DELETE, HEAD |
| shop_urls | Shop urls from multi-shop feature | GET, POST, PUT, DELETE, HEAD |
| shops | Shops from multi-shop feature | GET, POST, PUT, DELETE, HEAD |
| specific_price_rules | Specific price rules management | GET, POST, PUT, DELETE, HEAD |
| specific_prices | Specific price management | GET, POST, PUT, DELETE, HEAD |
| states | Available states of countries | GET, POST, PUT, DELETE, HEAD |
| stock_availables | Available quantities of products | GET, POST, PUT, PATCH |
| stock_movement_reasons | Stock movement reason | GET, POST, PUT, DELETE, HEAD |
| stock_movements | Stock movements management | GET, POST only |
| stocks | Stocks for products | GET, POST only |
| stores | Stores | GET, POST, PUT, DELETE, HEAD |
| suppliers | Product suppliers | GET, POST, PUT, DELETE, HEAD |
| supply_order_details | Supply Order Details | GET, POST only |
| supply_order_histories | Supply Order Histories | GET, POST only |
| supply_order_receipt_histories | Supply Order Receipt Histories | GET, POST only |
| supply_order_states | Supply Order States | GET, POST only |
| supply_orders | Supply Orders | GET, POST only |
| tags | Products tags | GET, POST, PUT, DELETE, HEAD |
| tax_rule_groups | Group of Tax rule, along with their name | GET, POST, PUT, DELETE, HEAD |
| tax_rules | Tax rules, to associate Tax with a country, zip code, … | GET, POST, PUT, DELETE, HEAD |
| taxes | Tax rate | GET, POST, PUT, DELETE, HEAD |
| translated_configurations | Shop configuration which are translated | GET, POST, PUT, DELETE, HEAD |
| warehouse_product_locations | Location of products in warehouses | GET, POST only |
| warehouses | Warehouses | GET, POST, PUT, PATCH, DELETE, HEAD |
| weight_ranges | Weight ranges for deliveries | GET, POST, PUT, DELETE, HEAD |
| zones | Countries zones | GET, POST, PUT, DELETE, HEAD |

(~70 resources; list current as of PrestaShop 9 docs.)

---

## 7. Auth quick-start (cURL)

```bash
# List the 10 most recent orders as JSON (only reference + total)
curl -s -u "UCCLLQ9N2ARSHWCXLT74KUKSSK34BFKX:" \
  "https://example.com/api/orders?output_format=JSON&display=[id,reference,total_paid]&sort=[id_DESC]&limit=10"

# -u "KEY:"  → HTTP Basic with an empty password (the trailing colon matters)
```

Response (`output_format=JSON`):

<!-- Constructed from docs — verify against live API -->
```json
{
  "orders": [
    { "id": 42, "reference": "XKBKNABJK", "total_paid": "72.900000" },
    { "id": 41, "reference": "OHSATSERP", "total_paid": "16.900000" }
  ]
}
```

---

## 8. Read → Create → Update flow

### 8a. Get one order (full)

```bash
curl -s -u "$PS_KEY:" \
  "https://example.com/api/orders/42?output_format=JSON&display=full"
```

<!-- Constructed from docs — verify against live API -->
```json
{
  "order": {
    "id": 42,
    "id_customer": "1",
    "id_cart": "17",
    "current_state": "3",
    "reference": "XKBKNABJK",
    "total_paid": "72.900000",
    "total_paid_real": "72.900000",
    "payment": "Bank transfer",
    "date_add": "2026-06-30 14:22:11",
    "associations": {
      "order_rows": [
        { "id": "1", "product_id": "1", "product_reference": "demo_1",
          "product_quantity": "1", "unit_price_tax_incl": "72.900000" }
      ]
    }
  }
}
```

### 8b. Create a product (XML is the native input)

Fetch the blank schema, fill it, POST it back. Translatable fields (like `name`) are
**per-language** — note the `<language id="1">` wrapper.

```bash
# 1. get the template
curl -s -u "$PS_KEY:" "https://example.com/api/products?schema=blank" -o product.xml

# 2. POST the filled template
curl -s -u "$PS_KEY:" -X POST "https://example.com/api/products" \
  -H "Content-Type: text/xml" \
  --data-binary @product.xml
```

Minimal product body:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
  <product>
    <price>19.900000</price>
    <active>1</active>
    <state>1</state>
    <reference>sku-1001</reference>
    <link_rewrite><language id="1"><![CDATA[blue-widget]]></language></link_rewrite>
    <name><language id="1"><![CDATA[Blue Widget]]></language></name>
  </product>
</prestashop>
```

> `link_rewrite` **must be a clean slug** (lowercase, hyphenated) or you get a
> "is not valid" / pattern error. Setting stock is a **separate** call to
> `stock_availables` (see §8d) — the `products` resource doesn't own the quantity.

### 8c. Update — PUT replaces the whole entity

`PUT /api/{resource}/{id}` expects the **full representation**, not a partial patch. The
safe pattern is **GET → mutate → PUT the same document back** (keep the `<id>` node). For a
narrow field update on supported resources (e.g. `stock_availables`, `warehouses`), `PATCH`
is available.

```bash
curl -s -u "$PS_KEY:" -X PUT "https://example.com/api/products/1" \
  -H "Content-Type: text/xml" --data-binary @product_1_full.xml
```

### 8d. Set stock quantity

```bash
# find the stock_available row for the product, then PUT/PATCH the quantity
curl -s -u "$PS_KEY:" \
  "https://example.com/api/stock_availables?output_format=JSON&filter[id_product]=1&display=full"
# → PUT that row back with <quantity>25</quantity>
```

### 8e. Delete

```bash
curl -s -u "$PS_KEY:" -X DELETE "https://example.com/api/products/1"
# bulk: DELETE /api/products?id=[1,2,3]
```

---

## 9. Error responses

Errors come back in the response body in the requested format with an HTTP status.

<!-- Constructed from docs — verify against live API -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<prestashop>
  <errors>
    <error>
      <code><![CDATA[21]]></code>
      <message><![CDATA[Property product->link_rewrite is not valid]]></message>
    </error>
  </errors>
</prestashop>
```

Common statuses: **401** (bad/stripped key — see CGIPassAuth), **400** (validation /
malformed XML), **404** (unknown resource or id), **405** (verb not permitted for that
key/resource), **500** (server/module error). There is a **`?debug`** switch on non-prod
installs that returns a full stack trace.

---

## 10. Rate limits & retries

The Webservice publishes **no documented rate limit** — throughput is bounded by your own
server (PHP-FPM workers, DB). Treat it as a shared resource: **serialize writes**, batch
reads with `limit`, cache the resource list, and back off on `500`s (they usually mean the
DB or a module is under load, not that you were throttled). For large exports, page with
`limit=start,count` and a stable `sort=[id_ASC]`.

---

## 11. There are no native outbound webhooks

The Webservice is **pull-only** — there is no built-in "register a webhook URL" screen.
To get **push** notifications on events (new order, stock change, customer create) you have
two options:

1. **A module hook (native).** PrestaShop's extensibility is its **hook system**. A small
   custom module registers on a hook such as `actionValidateOrder`, `actionOrderStatusUpdate`,
   `actionObjectProductUpdateAfter`, `actionCustomerAccountAdd`, etc., and your PHP handler
   `fetch()`es/cURLs out to your CRM/warehouse/Slack. This is the reliable path.
2. **A third-party "Webhooks" module** from the Addons marketplace (several exist) that turns
   selected hooks into outbound HTTP POSTs with a JSON payload — no code, but verify its
   retry/signature behaviour before trusting it, and add your own shared-secret check.

If you can deploy neither, **poll** `orders?sort=[id_DESC]&filter[date_add]=[…]` on a
schedule and track the last-seen `id`.

Example order-hook module handler (conceptual):

```php
<?php
class MyWebhooks extends Module
{
    public function install() {
        return parent::install() && $this->registerHook('actionValidateOrder');
    }
    public function hookActionValidateOrder(array $params) {
        $order = $params['order'];
        $payload = json_encode(['id' => $order->id, 'reference' => $order->reference,
                                'total' => $order->total_paid]);
        $ch = curl_init('https://your-app.example.com/prestashop/order');
        curl_setopt_array($ch, [
            CURLOPT_POST => true, CURLOPT_POSTFIELDS => $payload,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json',
                                   'X-PS-Signature: '.hash_hmac('sha256', $payload, getenv('PS_HOOK_SECRET'))],
            CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5,
        ]);
        curl_exec($ch); curl_close($ch);
        // hooks run in-process during checkout — keep this fast; enqueue if it can be slow
    }
}
```

---

## 12. Python — order-export pipeline

```python
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://example.com/api"
KEY  = "UCCLLQ9N2ARSHWCXLT74KUKSSK34BFKX"
auth = HTTPBasicAuth(KEY, "")            # empty password

def fetch_orders(since_id=0, page=50):
    start = 0
    while True:
        r = requests.get(f"{BASE}/orders", auth=auth, params={
            "output_format": "JSON",
            "display": "[id,reference,current_state,total_paid,date_add]",
            "filter[id]": f"[{since_id+1},999999999]",
            "sort": "[id_ASC]",
            "limit": f"{start},{page}",
        }, timeout=30)
        r.raise_for_status()
        rows = r.json().get("orders", [])
        if not rows:
            break
        for o in rows:
            yield o
        start += page

for order in fetch_orders(since_id=0):
    print(order["id"], order["reference"], order["total_paid"])
```

---

## 13. Official clients & tooling

- **PHP:** the official **`PrestaShopWebserviceLib`** (`PrestaShopWebservice` class) wraps auth, XML (via SimpleXML), and CRUD — the documented first-party client.
- **Postman:** the docs ship a "Testing with Postman" tutorial + importable collection.
- **Community SDKs** exist for Python/Node (unofficial) — verify maintenance before use.
- **iPaaS:** Zapier and Make both list a PrestaShop app (triggers like new order/customer, actions to create records); several Addons "Webhooks" modules bridge hooks → HTTP.

---

## 14. Gaps / to verify against live docs

- Exact **synopsis** field-validator vocabulary per resource (required/size/format) — fetch `?schema=synopsis` per resource at integration time.
- Whether a given install exposes the **Advanced Stock Management** resources (`warehouses`, `supply_orders`, `stock_movements`) — these depend on ASM being enabled.
- The precise **JSON** shape of nested `associations` (order_rows, images) can differ by version — inspect a live `display=full` response.
- Any **module-added custom resources** (the Webservice is extensible via `addWebserviceResources`).
