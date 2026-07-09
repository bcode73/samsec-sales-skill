# Saleor Platform Guide

Full reference for the Saleor headless commerce platform — modules and access surface, pricing/plan gates, data model, and quick-start recipes.

*Best-effort from research (2026-06). Re-verify pricing, plan gates, auth, and webhook-signature behavior against live docs at https://docs.saleor.io.*

## What Saleor is

Open-source (**BSD-3-Clause**), **GraphQL-first** headless/composable commerce platform built on **Python/Django**. You self-host the core for free (no per-sale fee) or run it on **Saleor Cloud** (managed infra). There is **no REST API and no built-in storefront UI** — you build the storefront (commonly Next.js, with the official Saleor **Auth SDK** and **storefront** starter) against a single GraphQL endpoint, and you build/extend back-office logic with **Apps** (webhooks + dashboard extensions).

Positioning: a developer/maker-controlled alternative to Shopify/BigCommerce (hosted SaaS) and to Medusa/Vendure (other open-source headless engines), and a lighter alternative to commercetools/Adobe Commerce at the enterprise end. Saleor Cloud's commercial pricing leans mid-market/enterprise; the **self-hosted OSS path is the maker fit**.

## Modules & access surface

Every capability is reachable through the GraphQL API unless noted. "UI-only" means Dashboard-only with no API.

| Module | What it does | Access |
|---|---|---|
| **Products / Variants** | Catalog with dynamically defined **attributes**; **variants** carry inventory + pricing (checkout is keyed by variant ID) | GraphQL API |
| **Channels** | Sell across web/mobile/retail/agentic touchpoints; pricing, currency, and availability are **per-channel** | GraphQL API |
| **Checkout** | Multi-step mutation flow (create → addresses/email → delivery → payment → order) | GraphQL API |
| **Orders / Fulfillment** | Order management (OMS), fulfillments, refunds, `orderMarkAsPaid` | GraphQL API (mostly app-permissioned) |
| **Customers / Staff / Permissions** | Users, staff members, permission groups | GraphQL API |
| **Payments / Transactions** | Transactions API + payment **Apps** (sync webhooks delegate auth/capture to your provider) | GraphQL API + sync webhooks |
| **Taxes** | Tax calculation via **tax Apps** / sync webhooks (Avalara, custom) — **Saleor is NOT a Merchant of Record** | Sync webhooks / tax app |
| **Webhooks** | **160+ events**, sync + async, payloads shaped by GraphQL `subscription` | Configured on an App |
| **Apps framework** | Third-party + local apps, **45+ dashboard mount points** (UI extensions), App SDK | App SDK (TypeScript) |
| **PIM / metadata** | Product information management, custom `metadata`/`privateMetadata` on most objects | GraphQL API |
| **Configurator CLI** | Infrastructure-as-code for store config, CI/CD | CLI |
| **Observability** | **OpenTelemetry** request tracing | Self-host/Cloud config |
| **Dashboard** | React admin app (extensible via app mount points) | UI (+ extensions) |

Client languages with community/official tooling: **TypeScript, Python, PHP, Ruby, Go, Svelte, .NET** (GraphQL — use any HTTP/GraphQL client).

## Auth model (summary)

- **Single endpoint:** `https://{your-store}.saleor.cloud/graphql/` (Cloud) or `http://localhost:8000/graphql/` (self-host).
- **Public reads** (products, etc.) need **no token**.
- **Users:** `tokenCreate(email, password)` → short-lived **access token** (RS256 JWT) + **refresh token**. Refresh with `tokenRefresh`; verify with `tokenVerify`; invalidate all with `tokensDeactivateAll`.
- **Apps:** long-lived token issued at install/creation for machine-to-machine. Many management mutations require an **app** token + permission.
- **Header:** `Authorization: Bearer <token>` (or `Authorization: JWT <token>`; `Authorization-Bearer` for proxy compatibility).
- **Verification:** JWKS at `https://<domain>/.well-known/jwks.json`.
- **OIDC:** SSO (token straight from IdP) or legacy proxy mode (`externalAuthenticationUrl`, `externalObtainAccessTokens`); scopes `openid profile email` (+ optional `saleor:<permission>`).
- **`Shop.passwordLoginMode`:** `ENABLED` (default) / `CUSTOMERS_ONLY` / `DISABLED`; only OIDC-authenticated admins can tighten it.

See `references/saleor-api-reference.md` for verbatim auth/webhook detail.

## Pricing & plan gates

*Cloud pricing best-effort (2026-06) — verify at saleor.io/pricing.*

| Plan | Price | GMV / notes |
|---|---|---|
| **Self-hosted OSS** | Free (BSD-3) | No per-sale fee; you run Postgres + Redis/Celery + Django and own ops |
| **Sandbox (Cloud)** | Free | **Non-commercial** — prototyping/trials only |
| **Select** | ~$1,599/mo | Up to **$200k** monthly GMV; **0.8%** on GMV over the cap |
| **Volume** | ~$3,999/mo | Up to **$1M** monthly GMV; **0.4%** over the cap |
| **Enterprise** | Custom | Fee as low as **0.2%** on excess; best unit economics at scale |

Add-ons (one-time, credited over year one): **Accelerator** ~$6,000 (= ~$500/mo credit), **Forward Deployed Engineering** ~$12,000 (= ~$1,000/mo credit). All Cloud tiers include solution-architect pairing + dedicated Slack support. **OSS ↔ Cloud migration** works between compatible versions.

## Data model (shapes, not prose)

A product with a variant (variants hold price + stock; checkout uses the **variant** ID):

```json
{
  "product": {
    "id": "UHJvZHVjdDox",
    "name": "Apple Juice",
    "channelListings": [{ "channel": { "slug": "default-channel" }, "isPublished": true }],
    "variants": [{
      "id": "UHJvZHVjdFZhcmlhbnQ6Mzgz",
      "name": "1l",
      "pricing": { "price": { "gross": { "amount": 5.0, "currency": "USD" } } },
      "quantityAvailable": 50
    }]
  }
}
```

Async webhook payload envelope (event + `subscription`-shaped data):

```json
{
  "event": "ORDER_CREATED",
  "data": { "order": { "id": "T3JkZXI6MQ==", "number": "1", "total": { "gross": { "amount": 25.0, "currency": "USD" } } } }
}
```

HTTP headers on every webhook delivery: `Saleor-Event`, `Saleor-Domain`, `Saleor-Signature`, `Saleor-Api-Url`.

## Quick-start recipes

### Recipe 1 — Query published products in a channel (no auth)

cURL:

```bash
curl -X POST https://your-store.saleor.cloud/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query":"query { products(first: 5, channel: \"default-channel\") { edges { node { id name variants { id name quantityAvailable } } } } }"}'
```

### Recipe 2 — App-token order export with cursor pagination (Python)

```python
import requests

URL = "https://your-store.saleor.cloud/graphql/"
HEADERS = {"Authorization": "Bearer YOUR_APP_TOKEN", "Content-Type": "application/json"}

QUERY = """
query Orders($cursor: String) {
  orders(first: 100, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges { node { id number created total { gross { amount currency } } } }
  }
}"""

cursor, all_orders = None, []
while True:
    r = requests.post(URL, json={"query": QUERY, "variables": {"cursor": cursor}}, headers=HEADERS)
    data = r.json()["data"]["orders"]
    all_orders += [e["node"] for e in data["edges"]]
    if not data["pageInfo"]["hasNextPage"]:
        break
    cursor = data["pageInfo"]["endCursor"]

print(f"Exported {len(all_orders)} orders")
```

`orders` requires an **App** token with `MANAGE_ORDERS`. Pagination is Relay-style cursors (`first`/`after` + `pageInfo`), not limit/offset.

### Recipe 3 — Minimal checkout → order flow (GraphQL)

```graphql
# 1) Create a checkout (variant IDs, not product IDs)
mutation {
  checkoutCreate(input: {
    channel: "default-channel",
    email: "buyer@example.com",
    lines: [{ quantity: 1, variantId: "UHJvZHVjdFZhcmlhbnQ6Mzgz" }]
  }) { checkout { id token } errors { field message } }
}

# 2) Set delivery method, 3) collect payment via a payment App / transactions, then:
# 4) Convert to an order — REQUIRES AN APP TOKEN
mutation {
  orderCreateFromCheckout(id: "Q2hlY2tvdXQ6...") {
    order { id number } errors { field message code }
  }
}

# 5) Mark paid
mutation { orderMarkAsPaid(id: "T3JkZXI6MQ==") { order { id isPaid } } }
```

### Recipe 4 — Verify a webhook (JWS RS256, the default) in Node.js

```js
import * as jose from "jose";

// rawBody must be the EXACT bytes Saleor sent (do not JSON.parse then re-stringify)
export async function verifySaleorWebhook(req, rawBody) {
  const jws = req.headers["saleor-signature"];          // detached JWS
  const domain = req.headers["saleor-domain"];
  const JWKS = jose.createRemoteJWKSet(new URL(`https://${domain}/.well-known/jwks.json`));
  const [protectedHeader, , signature] = jws.split(".");  // detached: middle is empty
  await jose.flattenedVerify(
    { protected: protectedHeader, payload: rawBody, signature },
    JWKS
  ); // throws if invalid
}
```

For HMAC-secret webhooks (deprecated): `echo -n "<raw-body>" | openssl dgst -sha256 -hmac "<secret>"` and compare to `Saleor-Signature`. In a Saleor App, prefer `withWebhookSignatureVerified()` from `@saleor/app-sdk`.

## When to pick Saleor vs alternatives

- **vs Medusa** — both open-source, self-hostable, 0% fee. Saleor = **Python/Django + GraphQL-first + native outbound webhooks (sync & async)**; Medusa = **Node.js/TS + REST + internal events/subscribers (no webhook UI)**. Choose by stack preference and whether you want built-in webhook delivery.
- **vs Vendure** — Vendure is TypeScript/NestJS + GraphQL (open-core, GPL); Saleor is Python/Django + GraphQL (BSD-3). Stack + license preference decides.
- **vs Shopify/BigCommerce** — those are hosted SaaS (no infra to run, app ecosystems) but charge fees and limit code-level control. Saleor self-host gives full control + no per-sale fee at the cost of running infra.
- **vs commercetools / Adobe Commerce** — those are enterprise composable platforms (high license cost, agency-led). Saleor self-host is far cheaper for a dev/maker team.
