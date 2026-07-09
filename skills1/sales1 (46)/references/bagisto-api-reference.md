# Bagisto API Reference

<!-- Source: https://api-docs.bagisto.com/api/graphql-api/introduction.html, https://api-docs.bagisto.com/api/rest-api/introduction.html, https://devdocs.bagisto.com/api/graphql-api.html, https://github.com/bagisto/headless-ecommerce (research 2026-06) -->

> Captured verbatim where possible from Bagisto's official API docs. Bagisto ships multiple API generations — sections are labeled. Re-verify against live docs before relying on exact headers/endpoints. Pricing/version notes are best-effort.

---

## Two API generations (read this first)

1. **Unified REST + GraphQL API** (current, api-docs.bagisto.com) — Shop/Admin split, `X-STOREFRONT-KEY` + Laravel Sanctum bearer auth, cart tokens. **Documented below as the primary surface.**
2. **Legacy standalone `bagisto/graphql-api`** (Mobikul headless package, devdocs.bagisto.com) — `/graphql` endpoint, **JWT** + `x-app-secret-key` header. Documented at the bottom under "Legacy headless GraphQL package."

Confirm which package is installed (`composer.json`) before quoting headers/endpoints.

---

## REST API (unified)

### Installation
```
composer require bagisto/rest-api
```
Configure `.env`:
```
SANCTUM_STATEFUL_DOMAINS=http://localhost/public
```
Run install:
```
php artisan bagisto-rest-api:install
```

### Base URL & endpoints
The REST API follows this pattern: `https://{your-domain.com}/api/{type}/{resource}`

Two main API layers exist:
- **Shop API** (`/api/shop/`) — Customer-facing operations
- **Admin API** (`/api/admin/`) — Administrative operations

Interactive API docs (Swagger/OpenAPI):
- **Admin API**: `http://localhost/public/api/admin/documentation`
- **Shop API**: `http://localhost/public/api/shop/documentation`

### Authentication

**Storefront Key (Shop API).** Every Shop API call requires the `X-STOREFRONT-KEY` header with a value like `pk_storefront_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`. This key is generated during installation or via:
```
php artisan bagisto-api:generate-key --name="My Mobile App"
```

**Bearer Token (authenticated routes).** Customer-scoped endpoints require a Laravel **Sanctum** bearer token in the `Authorization` header:
```
Authorization: Bearer 1|abcdef…
```
The system employs "Laravel Sanctum for secure token-based authentication." Obtain tokens via admin or customer credentials, then include in requests:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Accept: application/json" \
     http://localhost/public/api/v1/admin/get
```

**Guest cart token.** Guest customers can create a cart token via `POST /api/shop/cart-tokens` and pass it as `cart_token` in subsequent cart requests.

### Common headers

| Header | Required | Purpose |
|--------|----------|---------|
| `Accept` | Yes | `application/json` |
| `Content-Type` | On POST/PUT | `application/json` |
| `X-STOREFRONT-KEY` | Yes (Shop) | Storefront identifier |
| `Authorization` | Auth routes | Sanctum bearer token |
| `X-Locale` | Optional | Override locale (e.g., `en`, `fr`) |
| `X-Channel` | Optional | Override channel scope |
| `X-Currency` | Optional | Override currency formatting |

### HTTP methods

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Retrieve resources | `GET /api/shop/products` |
| `POST` | Create resource | `POST /api/shop/customers` |
| `PATCH` | Update resource | `PATCH /api/admin/products/1` |
| `DELETE` | Delete resource | `DELETE /api/admin/products/5` |

### Key resources available

**Shop API:**
- Products, categories, attributes, reviews
- Cart, checkout, orders
- Customer profiles, addresses
- Wishlist, compare, newsletter

**Admin API:**
- Product & category management
- Customer administration
- Order fulfillment, invoices, shipments
- Inventory, configuration, reports

### Pagination
Collection endpoints return a JSON array with metadata in response headers:
```
X-Total-Count: 137
X-Page: 2
X-Per-Page: 20
X-Total-Pages: 7
```
Query parameters: `?page=2&per_page=20` (capped at 50 items per page)

### Guest cart workflow
1. `POST /api/shop/cart-tokens` → receive `cartToken`
2. Include `"cart_token": "cT_5b3a1c…"` in body for subsequent cart operations
3. Pass token through checkout steps (address, shipping, payment, order placement)

### Example cURL request
```bash
curl "https://your-domain/api/shop/products?page=1&per_page=10" \
  -H "X-STOREFRONT-KEY: pk_storefront_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Accept: application/json"
```

> Note: some legacy `bagisto/rest-api` builds expose `/api/v1/admin/...` and `/api/v1/shop/...` paths (see the `php artisan bagisto-rest-api:install` flow). Use the Swagger docs at `/api/{admin,shop}/documentation` on your install as the source of truth for exact paths.

---

## GraphQL API (unified)

### Endpoints
- **Main GraphQL endpoint**: `/api/graphql`
- **Interactive playground**: `/api/graphiql`

### Required headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Request format | `application/json` |
| `X-STOREFRONT-KEY` | Public API access | `pk_storefront_...` |
| `Authorization` | Authentication token | `Bearer TOKEN` |
| `X-LOCALE` | Localization context | `fr` |
| `X-CURRENCY` | Currency context | `EUR` |
| `X-CHANNEL` | Channel selection | `default` |

### API structure
- **Shop API** handles: product browsing, customer authentication, cart management, checkout, reviews, and wishlists.
- **Admin API** handles: product/category administration, customer management, order fulfillment, system configuration, and analytics.

### Authentication methods
- **Guest Checkout**: Use `createCartToken` mutation to receive a `cartToken` for the Authorization header.
- **Customer Login**: Execute `createCustomerLogin` mutation with email/password credentials to obtain an `apiToken`.
- **Token Verification**: Use `createVerifyToken` mutation to validate token validity.

### Response format
Responses follow JSON structure with `data` objects containing query results or `errors` arrays for failures, including validation details in extensions.

### Pagination
Cursor-based pagination using `first`/`after` parameters with `pageInfo` metadata for navigation.

### Customer login mutation (verbatim)
```graphql
mutation {
  createCustomerLogin(input: {
    email: "customer@example.com"
    password: "password123"
    deviceToken: "fcm_device_token_here"
  }) {
    token
    message
    success
    customer {
      id
      email
      firstName
      lastName
    }
  }
}
```

**Input fields**

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `email` | String | Yes | Customer's email address |
| `password` | String | Yes | Customer's password |
| `deviceToken` | String | No | FCM device token for push notifications. Only required if the Bagisto Push Notification package is installed |

**Response fields**
- `token`: JWT authentication token for subsequent API requests
- `message`: Status message
- `success`: Boolean indicating login success
- `customer`: Customer object with profile details

**Token usage:** `"Authorization": "Bearer <token>"`

**Error example:** `{"errors": {"email": ["Invalid email or password."]}}`

### Products query (example)
```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        name
        price
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

---

## Legacy headless GraphQL package (`bagisto/graphql-api`, Mobikul)

> Requires Bagisto **2.3.0+**. Developed with the Ucraft Team. This is the older standalone package — its auth differs from the unified API above.

### Installation
```bash
composer require bagisto/graphql-api
```
(or `composer require bagisto/graphql-api:dev-main`)

Update `bootstrap/app.php` to remove session and cookie middleware from the `web` group, then append them globally:
```php
use Illuminate\Session\Middleware\StartSession;
use Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse;

return Application::configure(basePath: dirname(__DIR__))
   ->withMiddleware(function (Middleware $middleware) {
      $middleware->removeFromGroup('web', [
          StartSession::class,
          AddQueuedCookiesToResponse::class
      ]);

      $middleware->append([
          StartSession::class,
          AddQueuedCookiesToResponse::class
      ]);
   })
```

Add to `.env`:
```properties
JWT_TTL=525600
JWT_SHOW_BLACKLIST_EXCEPTION=true
MOBIKUL_API_KEY=your-secure-api-key-here
```

Run installation:
```bash
php artisan bagisto-graphql:install
```

### Endpoints
- **GraphQL Playground:** `http://your-domain.com/graphiql`
- **API Endpoint:** `http://your-domain.com/graphql`

### Authentication
Uses **JWT** settings (configured by the `.env` vars above). An `APP_SECRET_KEY` is generated automatically during setup and stored in `.env`; include it in API calls as:
```
x-app-secret-key: generated-secret-key
```
Once authenticated, put the JWT in the request header: `Authorization: Bearer {token}`.

Example customer login (verbatim):
```graphql
mutation customerLogin {
  customerLogin(input: {
    email: "test@webkul.com"
    password: "admin123"
  }) {
    status
    success
    accessToken
    tokenType
    expiresIn
    customer {
      id
      firstName
      lastName
      email
    }
  }
}
```

### Performance
Cache the GraphQL schema for production (Bagisto's GraphQL is built on **Laravel Lighthouse**):
```
php artisan lighthouse:cache
```
Clear on schema change:
```
php artisan lighthouse:clear-cache
```

---

## Webhooks / outbound events

Bagisto **core has no native outbound webhook system** (no UI to register an external URL). Because it's a Laravel app, integrate by:
- **Laravel events/listeners** — e.g. listen for `checkout.order.save.after` (order placed), customer/registration events, etc., and make the outbound HTTP call yourself in the listener. Queue the listener so it doesn't block the request.
- **Polling** — schedule a job that calls `GET /api/admin/orders?per_page=50` and tracks the last-seen increment_id.
- **Community webhook packages** — third-party Bagisto/Webkul webhook extensions exist for some events; verify maintenance before depending on one.

You own delivery concerns (retries, signing, logging, idempotency) in all cases.

---

## Requirements & ops notes

- **Stack:** PHP (Laravel) + MySQL/MariaDB; Redis recommended for cache/sessions/queues; a queue worker for async listeners.
- **Latest line:** Bagisto 2.x (v2.4.x mid-2026); the API packages require Bagisto 2.3.0+.
- **License:** MIT (engine free forever).
- **Install footguns:** set `APP_URL` exactly (images/mixed-content), ensure `storage/` + `bootstrap/cache/` are writable, run `php artisan storage:link`, and build caches (`php artisan optimize`) for performance.
