<!-- Source: https://docs.saleor.io/api-usage/authentication -->
<!-- Source: https://docs.saleor.io/quickstart/api -->
<!-- Source: https://docs.saleor.io/developer/extending/webhooks/overview -->
<!-- Source: https://docs.saleor.io/developer/extending/webhooks/payload-signature -->
<!-- Source: https://docs.saleor.io/api-reference/ -->
<!-- Note: Saleor's docs are rendered client-side; the fetch tool returned condensed
     content. Endpoints, mutation names, header names, and signature behavior below are
     taken from the official docs above. Re-verify exact field shapes against the live
     GraphQL schema / API reference. -->

# Saleor API Reference

Saleor exposes a **single GraphQL endpoint** — there is no REST API.

- **Cloud:** `https://{your-store}.saleor.cloud/graphql/`
- **Self-host:** `http://localhost:8000/graphql/` (dev) or your app URL in prod
- **Schema/playground:** the GraphQL playground is available at the endpoint; the Dashboard also ships a GraphQL network inspector. Full API reference: https://docs.saleor.io/api-reference/

## Authentication & Authorization

Saleor uses **JWT** authentication. Two actor types:

1. **Users** (customers/staff) — short-lived access tokens for user-specific resources.
2. **Apps** (third-party integrations) — long-lived tokens for machine-to-machine operations.

### Header formats

```
Authorization: Bearer <access-token>
```

Alternative formats accepted:

```
Authorization: JWT <token>
Authorization-Bearer: <token>      # for proxy compatibility
```

### Authentication methods

- **Public access** — no token required for public data (e.g. retrieving product data).
- **Email & password** — the `tokenCreate` mutation accepts credentials and returns:
  - an **access token** (short-lived, **RS256-signed JWT**)
  - a **refresh token** (longer-lived; includes a `csrf_token` field, now deprecated)
- **Saleor Auth SDK** — TypeScript library for Next.js (App Router & Pages Router) that handles token storage + refresh automatically.
- **OpenID Connect (OIDC)** — two modes:
  - **SSO** — client receives the token directly from the identity provider.
  - **Legacy client mode** — Saleor acts as an OAuth2 proxy using `externalAuthenticationUrl`, `externalObtainAccessTokens`, and related mutations.
  - Required scopes: `openid`, `profile`, `email`, plus optional `saleor:<permission>` for permission delegation.
- **App authentication** — long-lived tokens issued on app installation/creation, passed in the same `Authorization` header as user tokens.

### Token management

- **Refresh:** `tokenRefresh` mutation with the refresh token returns a new access token (do not send the expired access token in the header).
- **Verify:** validate via the **JWKS** file at `https://<your-saleor-domain>/.well-known/jwks.json`, or call the `tokenVerify` mutation.
- **Deactivate:** `tokensDeactivateAll` invalidates all of a user's tokens.

### Dashboard app tokens

Apps that extend the dashboard are passed a special JWT whose effective permission set is the **intersection of the user's and the application's permissions** — letting the app frontend call the API on behalf of the user.

### Password login mode

`Shop.passwordLoginMode` controls password auth availability:

- `ENABLED` (default) — all users
- `CUSTOMERS_ONLY` — staff receive no permissions
- `DISABLED` — blocks password mutations entirely

Only **OIDC-authenticated** admins can restrict the mode; password-authenticated admins cannot.

### Security features

- **Login throttling** — IP-based blocking with exponential backoff (max 60 minutes).
- **Password-reset throttling** — one link per user per 15 minutes.
- Common error: `AUTHENTICATED_APP` — ensure a valid **app** token is attached for app-permissioned operations.

## API walkthrough (checkout → order)

The canonical flow from the quickstart:

1. **Load sample data** — Cloud: from instance settings; local: via quickstart config.
2. **Access GraphQL** — Dashboard playground (authenticated) or the public endpoint.
3–4. **Query products** — filter by price; fetch product detail incl. **variants** and media.
5. **`checkoutCreate`** — uses **variant IDs** (not product IDs), since variants carry inventory + pricing; pass a `channel`.
6. **Update checkout** — add shipping/billing addresses and customer email (can be batched).
7. **Delivery method** — assign a shipping/delivery method to the active checkout.
8. **Webhooks** — configure event subscriptions via Dashboard → Extensions → Add Extension (target URL + event filtering).
9. **`orderCreateFromCheckout`** — converts a checkout to an order. **Requires app-token authentication.**
10. **`orderMarkAsPaid`** — updates the order's balance/paid status.

Tools: official Postman collections (Saleor QA profile), the GraphQL network inspector, and the interactive API reference.

## Webhooks

Saleor has **native outbound webhooks** with **160+ events**, configured on an **App**.

### Synchronous vs asynchronous

- **Synchronous** events execute **during** the request that triggered them and **influence its response time** (used for taxes, shipping, payment — the response is consumed by Saleor).
- **Asynchronous** events fire **after** request processing completes (e.g. `ORDER_CREATED`, `PRODUCT_UPDATED`).

### Subscription syntax (shapes the payload)

```graphql
subscription {
  event {
    ... on ProductUpdated {
      product { id name }
    }
  }
}
```

### Payload format

```json
{
  "event": "PRODUCT_UPDATED",
  "data": {
    "object": { "id": "ID", "name": "NAME" }
  }
}
```

### Delivery headers

- `Saleor-Event` — event type
- `Saleor-Domain` — domain identifier
- `Saleor-Signature` — signature for verification
- `Saleor-Api-Url` — GraphQL endpoint URL

Custom headers allowed: `Authorization*` and `X-*` prefixes, **up to 5 per webhook**, max **998 characters** each.

### Time limits

Both sync and async deliveries have a **maximum 20-second total HTTP round trip**: up to **2 seconds** for the network connection and up to **18 seconds** for the response.

### Testing

`webhookDryRun` mutation tests **asynchronous** webhook payloads without sending real requests (synchronous events are not supported for dry-run).

## Webhook payload signature

The `Saleor-Signature` header is produced one of two ways:

1. **JWS signature using RS256 with payload detached** — used **when no `secretKey` was set** on the webhook (the **default / recommended** path). Verify with the public key fetched from `https://<your-backend-domain>/.well-known/jwks.json`.
2. **HMAC SHA-256** — used **when a `secretKey` was set**. **Deprecated.** Saleor computes the HMAC over the request body with the secret key.

### HMAC verification (deprecated path)

```bash
echo -n "<request-body>" | openssl dgst -sha256 -hmac "<secret-key>"
```

### JWS verification (default path), Node.js + `jose`

- Use the **raw body string** (not a parsed object).
- Fetch the JWKS from `/.well-known/jwks.json`.
- Split the detached JWS into protected header / (empty) payload / signature.
- Call `jose.flattenedVerify({ protected, payload: rawBody, signature }, JWKS)`.
- In Next.js, disable `bodyParser` to access the raw body.

### Saleor App SDK (recommended)

Use `withWebhookSignatureVerified()` middleware from `@saleor/app-sdk` for automatic validation in Saleor Apps. Supply the **raw body string**, not a parsed object.

## Pagination

List queries use **Relay-style cursor pagination**: `first` / `after` (and `last` / `before`), with `pageInfo { hasNextPage hasPreviousPage startCursor endCursor }` and `edges { node { ... } }`. Many catalog/listing queries are **channel-scoped** — pass a `channel` argument.

## Apps & extensibility

- **Apps** carry the webhooks + permissions for an integration; **45+ dashboard mount points** allow UI extensions.
- **App SDK** (`@saleor/app-sdk`, TypeScript) — build apps, verify webhook signatures, manage auth.
- **APL (Auth Persistence Layer)** — stores per-installation auth data for apps.
- **Configurator CLI** — infrastructure-as-code for store configuration + CI/CD.
- **OpenTelemetry** — request tracing/observability.

## Rate limits

Saleor Cloud applies request limits per plan (specific quotas not published verbatim here). Implement client-side throttling and exponential backoff on errors. Sync webhooks must respond within the ~20s round-trip window.
