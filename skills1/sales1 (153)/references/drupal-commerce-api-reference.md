<!-- Source: https://www.drupalcommerce.org/ , https://www.drupal.org/docs/contributed-modules/commerce-api , https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module , https://www.drupal.org/docs/contributed-modules/api-authentication — captured 2026-07-04. Content is quoted/summarized from the official docs; representative JSON is marked as constructed. -->

# Drupal Commerce API — Reference

Drupal Commerce has no single bespoke REST API of its own. Instead it is consumed through **Drupal core
JSON:API** (which auto-exposes every entity, including all `commerce_*` entities) plus the contrib
**Commerce API / Commerce Cart API** module (which adds a headless-friendly cart & checkout layer and
order-transition webhooks). Authentication is provided by Drupal auth modules (Simple OAuth, basic_auth,
JWT).

## JSON:API (core) — base path & URL structure

Base path: **`/jsonapi`**. Resources follow:

```
GET | POST     /jsonapi/{entity_type}/{bundle}
GET            /jsonapi/{entity_type}/{bundle}/{uuid}
PATCH | DELETE /jsonapi/{entity_type}/{bundle}/{uuid}
```

Examples:
- `GET /jsonapi/commerce_product/default` — collection of products (bundle `default`)
- `POST /jsonapi/commerce_product/default` — create a product
- `PATCH /jsonapi/commerce_order/default/{uuid}` — update an order
- `DELETE /jsonapi/commerce_promotion/default/{uuid}` — delete a promotion

> "Note that there is _no_ URL at `/jsonapi/node`" — a collection endpoint must always include the
> bundle, because a single endpoint may not serve multiple resource types (per the JSON:API spec).

### HTTP methods
`GET` (retrieve), `POST` (create), `PATCH` (update), `DELETE` (remove). **PUT is not supported.**

### Headers
```
Accept: application/vnd.api+json
Content-Type: application/vnd.api+json
```

### Response codes
- `200 OK` — successful GET and PATCH
- `201 Created` — successful POST (includes the newly created resource)
- `204 No Content` — successful DELETE

### Query parameters
- **Filtering:** `?filter[…]` (e.g. `?filter[state]=completed`, plus grouped/nested filters)
- **Includes (embed relationships):** `?include=variations,stores`
- **Sparse fieldsets:** `?fields[commerce_product--default]=title,path`
- **Pagination:** `?page[offset]=` and `?page[limit]=` (offset-based; JSON:API default limit is ~50; a
  `links.next` cursor is returned for the next page)
- **Sorting:** `?sort=` / `?sort=-created`

### Response envelope
```json
{
  "data": {
    "type": "commerce_order--default",
    "id": "b7f2c9e1-a4d8-460f-bc3e-5a1029d7e6f4",
    "attributes": { "order_number": "10001", "state": "completed",
      "total_price": { "number": "29.99", "currency_code": "USD" } },
    "relationships": {
      "order_items": { "data": [ { "type": "commerce_order_item--default", "id": "…" } ] }
    }
  },
  "links": { "self": { "href": "https://store.example.com/jsonapi/commerce_order/default/…" } }
}
```
<!-- Constructed from JSON:API conventions — verify against live API -->

Key commerce resource types: `commerce_store`, `commerce_product`, `commerce_product_variation`,
`commerce_order`, `commerce_order_item`, `commerce_promotion`, `profile` (billing/shipping).

## Authentication

Drupal core JSON:API supports cookie auth by default; for decoupled/API clients you add an auth module:

### Simple OAuth (OAuth 2.0) — recommended for machine clients
Install the **Simple OAuth** module, create a **Consumer** (client) with scopes/roles, then:

`POST /oauth/token`

```bash
# password grant
curl -s "https://store.example.com/oauth/token" \
  -d grant_type=password -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET \
  -d username=api_user -d password=api_pass
# client_credentials grant
curl -s "https://store.example.com/oauth/token" \
  -d grant_type=client_credentials -d client_id=CLIENT_ID -d client_secret=CLIENT_SECRET
```
Response: `{ "token_type": "Bearer", "expires_in": 3600, "access_token": "…", "refresh_token": "…" }`.
Send `Authorization: Bearer <access_token>` on requests.

### Other options
- **HTTP Basic** (`basic_auth` core module) — simplest, for trusted server-to-server.
- **JWT** (contrib) — authenticate with an existing external JWT or one obtained through the module.
- **Third-party providers** (Okta, Google, Microsoft Entra ID) via the API Authentication module.
- **CORS** must be configured (services.yml `cors.config`) for browser-based consumers.

### 401 vs 403
- `401 Unauthorized` — missing/invalid credentials (no token, expired token, OAuth not configured).
- `403 Forbidden` — authenticated, but the Drupal **role/permission** doesn't allow that entity or
  operation. Drupal access is per-permission — grant the specific permission to the API user's role.

## Commerce API / Commerce Cart API (contrib)

"The Commerce API module extends the JSON:API implementation provided by Drupal for the Commerce module
and its ecosystem." It abstracts the complex relationships between an order and its billing/shipping
profiles and lets you convert a purchasable entity into an order item and attach it to an order in one
call — the piece that makes headless cart/checkout practical (raw JSON:API add-to-cart otherwise
requires unsafe permissions).

Documented areas:
- **Store specification** — the **`Commerce-Current-Store`** header designates which store handles the
  operation in multi-store environments.
- **Cart & checkout operations** — cart token management, retrieving carts, adding items, modifying and
  removing cart items, and checkout.
- **Webhooks** — event notifications, specifically for **order state transitions**.

### Cart token
The Cart API issues a **cart token** representing the shopper's cart (a draft order) so anonymous users
can build a cart without broad entity permissions. Pass the token on subsequent cart requests.

### Representative cart add (shape may vary by module version)
```bash
curl -s -X POST "https://store.example.com/cart/add" \
  -H "Content-Type: application/vnd.api+json" -H "Accept: application/vnd.api+json" \
  -H "Commerce-Current-Store: <store-uuid>" \
  -d '{ "data": [ { "type": "commerce_product_variation--default", "id": "<variation-uuid>",
                    "meta": { "quantity": 1 } } ] }'
```
<!-- Constructed from Commerce Cart API docs — verify exact route/shape against the installed module version -->

### Webhooks
The Commerce API module can emit **order state-transition webhooks** to a configured endpoint. Treat the
delivery as a hint: re-fetch the order via `GET /jsonapi/commerce_order/default/{uuid}` before acting,
and keep a polling reconciliation backup. (Verify the exact payload shape and any signing header against
the installed module version — the public webhook subpage was unavailable at capture time; see Gaps.)

## Events (in-code, when a webhook doesn't fit)

Drupal Commerce dispatches Symfony events you can subscribe to in a custom module:
- Order state machine transitions, e.g. `commerce_order.place.post_transition`,
  `commerce_order.fulfill.post_transition` (via `state_machine`'s `WorkflowTransitionEvent`)
- `OrderEvents` constants (order paid/placed) and generic `hook_ENTITY_TYPE_insert`/`_update`
- Contrib **Webhooks** module or **Rules** + HTTP request action for no-/low-code outbound calls

## Rate limits

Drupal Commerce imposes **no API rate limit** — throughput is bounded by your Drupal host, database, and
any reverse proxy/CDN. Self-throttle bulk jobs; enable page/entity caching and a search backend
(Solr/Elasticsearch) for large catalogs.

## Errors

JSON:API errors return an `errors` array:
```json
{ "errors": [ { "status": "403", "title": "Forbidden",
  "detail": "The current user is not allowed to POST the selected resource." } ] }
```
<!-- Constructed from JSON:API error shape — verify against live API -->

## Gaps / verify against live docs

- The **Commerce Cart API** exact route names, request/response bodies, and cart-token mechanics evolve
  by module version — verify against the installed `commerce_api`/`commerce_cart_api` release.
- The **webhook payload shape and any signature/verification header** could not be captured (the docs
  subpage 302'd/404'd at capture time) — confirm against the module before relying on it; treat webhooks
  as hints and re-fetch by UUID.
- Full per-entity field schemas are defined by your Drupal field configuration; use `?fields[…]` and
  inspect the live `/jsonapi` responses for exact attribute names.
