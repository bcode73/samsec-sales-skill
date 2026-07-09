# Drupal Commerce Platform Reference

## Overview

Drupal Commerce is an open-source (GPL) commerce framework built **on Drupal** (PHP/Symfony),
maintained by **Centarro** since 2010. Its defining trait: **commerce objects are Drupal entities**
(stores, products, variations, orders, order items, promotions, customer profiles), so a store shares
one system with Drupal content, Layout Builder, Media, Views, and Search API. That makes it strong for
**content-heavy, custom-catalog, or unusual-checkout** stores — and a **developer/agency** build, not a
turnkey SaaS. It's headless-capable through Drupal core **JSON:API** plus the **Commerce API / Commerce
Cart API** contrib modules. Free/self-hosted; **not a Merchant of Record**.

## Capabilities & automation surface

| Capability | What it does | Automation surface |
|---|---|---|
| Stores | One or more stores (currency, tax, multi-store) | JSON:API `commerce_store`; `Commerce-Current-Store` header on Cart API |
| Products & variations | `commerce_product` + `commerce_product_variation` (SKUs, price, attributes) | JSON:API CRUD `/jsonapi/commerce_product/*` |
| Orders & order items | `commerce_order` + `commerce_order_item`, order state machine | JSON:API read; **Commerce API order-transition webhook**; event subscribers |
| Cart | Shopper cart (a draft order) | **Commerce Cart API** (cart token: get/add/update/remove/checkout) |
| Checkout | Configurable checkout flow (panes/steps) | Cart API checkout endpoints; flow config is admin-only |
| Payment | 100+ gateways (Stripe, PayPal, Braintree, Authorize.Net, Square) | Gateway plugins; capture/refund via order API |
| Promotions & coupons | `commerce_promotion` + coupons, offers/conditions | JSON:API CRUD |
| Customer profiles | Billing/shipping as `profile` entities | JSON:API `/jsonapi/profile/*` |
| Tax | Tax types/rates, EU VAT, etc. | Config + calculated on orders |

**Drupal-admin-only (no first-class API):** checkout-flow/pane layout, product-type/field definitions,
payment-gateway configuration, and Views/Layout Builder. Automate data and events, not store config.

## Pricing, limits & plan gates

*Best-effort from research (2026-07) — verify at drupalcommerce.org.*

- **Free and open-source (GPL), self-hosted.** No license fee; you cover hosting, dev, PCI scope, updates.
- **Real cost is the build:** Drupal/PHP developers, hosting (Drupal-tuned), and contrib-module
  integration — a professional build commonly runs into the thousands and up, versus a turnkey SaaS.
- **Rate limits:** none imposed by Drupal Commerce itself — throughput is bounded by your host/DB
  (and any reverse-proxy/CDN). Self-throttle bulk jobs.
- **Not a Merchant of Record:** the merchant owns VAT/GST/sales tax (tax module calculates; you remit).
- **Contrib dependencies:** headless cart (Commerce Cart API), OAuth (Simple OAuth), JWT are **contrib
  modules** you install; JSON:API is core but writes are gated by permissions.

## Integrations

- **Direction:** JSON:API is **bidirectional** (read + write, permission-gated) over commerce entities;
  the **Commerce Cart API** drives the buyer flow; **Commerce API webhooks** are outbound on order state
  transitions.
- **CRM/warehouse:** no native CRM; sync via JSON:API + webhooks/event subscribers, or contrib connectors.
- **Payments:** 100+ gateway modules. **Search:** Drupal Search API (+ Solr/Elasticsearch).
- **Headless/decoupled:** JSON:API + Commerce Cart API feed Next.js/Nuxt/Astro or native apps; configure
  **CORS** for browser consumers. Older core **REST** module is an alternative (needs custom normalizers).

## Data model

Entities are addressed by **UUID** in JSON:API URLs (they also have an internal integer `id`). Prices are
objects (`{ "number": "29.99", "currency_code": "USD" }`). Responses follow the **JSON:API** envelope
(`data`/`attributes`/`relationships`/`included`).

**Product (`GET /jsonapi/commerce_product/default/{uuid}`):**
```json
{
  "data": {
    "type": "commerce_product--default",
    "id": "7b1e2c34-9a8d-4f60-bc3e-5a1029d7e6f4",
    "attributes": {
      "title": "Pro License",
      "path": { "alias": "/pro-license" }
    },
    "relationships": {
      "variations": { "data": [ { "type": "commerce_product_variation--default", "id": "…" } ] },
      "stores": { "data": [ { "type": "commerce_store--online", "id": "…" } ] }
    }
  }
}
```
<!-- Constructed from JSON:API conventions — verify against live API -->

**Order (`GET /jsonapi/commerce_order/default/{uuid}`, trimmed):**
```json
{
  "data": {
    "type": "commerce_order--default",
    "id": "b7f2c9e1-a4d8-460f-bc3e-5a1029d7e6f4",
    "attributes": {
      "order_number": "10001",
      "state": "completed",
      "total_price": { "number": "29.99", "currency_code": "USD" },
      "mail": "ada@example.com"
    },
    "relationships": {
      "order_items": { "data": [ { "type": "commerce_order_item--default", "id": "…" } ] }
    }
  }
}
```
<!-- Constructed from JSON:API conventions — verify against live API -->

## Quick-start recipes

### Recipe 1 — Simple OAuth token + JSON:API read
Trigger: read commerce data from a script. Steps: install Simple OAuth, create a consumer, get a token, query.

```bash
# 1) Get an OAuth Bearer token (Simple OAuth)
curl -s "https://store.example.com/oauth/token" \
  -d grant_type=password -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET \
  -d username=api_user -d password=api_pass
# -> { "token_type":"Bearer", "expires_in":3600, "access_token":"eyJ0..." }

# 2) List products via JSON:API (note the bundle in the path; UUIDs address items)
curl -s "https://store.example.com/jsonapi/commerce_product/default?page[limit]=50&page[offset]=0" \
  -H "Authorization: Bearer eyJ0..." \
  -H "Accept: application/vnd.api+json"
```
```python
import requests
BASE = "https://store.example.com"

def token():
    r = requests.post(f"{BASE}/oauth/token", data={
        "grant_type": "password", "client_id": "CLIENT_ID", "client_secret": "CLIENT_SECRET",
        "username": "api_user", "password": "api_pass"}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def list_orders(tok, offset=0):
    r = requests.get(f"{BASE}/jsonapi/commerce_order/default",
        params={"page[limit]": 50, "page[offset]": offset},
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.api+json"}, timeout=30)
    r.raise_for_status()
    return r.json()  # {"data":[...], "links":{"next":...}}
```
Gotcha: a **403** here means the API user's Drupal **role** lacks the permission for that entity — grant
the specific permission, don't use a blanket admin role. A **401** means the token is missing/invalid.

### Recipe 2 — Headless add-to-cart (Commerce Cart API, no over-permissioning)
Trigger: a decoupled front end needs an anonymous cart. Steps: install Commerce Cart API, use a cart token.

```bash
# Add a purchasable entity (variation) to the cart; the module abstracts order/order_item creation.
curl -s -X POST "https://store.example.com/cart/add" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Accept: application/vnd.api+json" \
  -H "Commerce-Current-Store: <store-uuid>" \
  -d '{
        "data": [
          { "type": "commerce_product_variation--default", "id": "<variation-uuid>",
            "meta": { "quantity": 1 } }
        ]
      }'
# The response carries the cart (order) + a cart token; send that token on subsequent cart calls.
```
<!-- Constructed from Commerce Cart API docs — verify exact route/shape against live module -->
Gotcha: do **not** grant anonymous users *administer stores* to make raw JSON:API add-to-cart work —
that's the footgun the Cart API exists to avoid. Keep the anonymous role minimal; the cart token scopes access.

### Recipe 3 — Outbound order-event integration (webhook or event subscriber)
Trigger: notify a CRM when an order is placed/paid. Steps: prefer the Commerce API webhook; else code.

```php
// Drupal event subscriber (when a webhook doesn't fit) — react to the order 'place' transition.
namespace Drupal\my_module\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Drupal\state_machine\Event\WorkflowTransitionEvent;

class OrderPlacedSubscriber implements EventSubscriberInterface {
  public static function getSubscribedEvents(): array {
    return ['commerce_order.place.post_transition' => 'onPlace'];
  }
  public function onPlace(WorkflowTransitionEvent $event): void {
    $order = $event->getEntity();
    // POST $order->uuid() out to your CRM; make it idempotent (dedupe on the UUID).
  }
}
```
Gotcha: core Drupal has **no webhook UI** — the Commerce API module provides **order state-transition
webhooks**; otherwise use an event subscriber / the Webhooks or Rules module. Always keep a polling backup.

## Integration patterns

- **CRM/warehouse sync:** Commerce API order-transition webhook (or an event subscriber) for low latency
  + a nightly `page[offset]`/`page[limit]` paginated `/jsonapi/commerce_order/default` reconciliation
  pull. Verify/re-fetch by UUID, dedupe on the order UUID.
- **Headless storefront:** buyer flow through the **Commerce Cart API** (cart token + `Commerce-Current-Store`);
  catalog/content reads through JSON:API; keep OAuth secrets server-side and configure CORS for the browser.
- **Auth:** **Simple OAuth** Bearer for machine clients; assign a **least-privilege Drupal role** to the
  API user (403s are role/permission gaps, not auth failures). Basic auth/JWT are alternatives.
- **Batch/ETL:** JSON:API filtering (`?filter[…]`), includes (`?include=`), sparse fieldsets
  (`?fields[…]`), page with `page[offset]`/`page[limit]`; self-throttle since the ceiling is your host/DB.
