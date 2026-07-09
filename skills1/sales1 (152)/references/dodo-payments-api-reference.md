<!-- Source: https://docs.dodopayments.com/api-reference/introduction and docs.dodopayments.com/llms.txt + /developer-resources/webhooks (fetched 2026-06). Endpoint catalog is from the official docs llms.txt index; auth/base-URLs/rate-limits verbatim from the API intro. -->

# Dodo Payments API Reference

## What it is

Dodo Payments is a **Merchant of Record (MoR)** billing + payments platform: it sells on your behalf and assumes the **legal liability for global sales tax / VAT / GST** across 220+ countries / 40+ payment methods. Developer-first — full REST API, 9 SDKs, framework adapters, an MCP server, and a CLI.

## Base URLs

```
Test:  https://test.dodopayments.com
Live:  https://live.dodopayments.com
```

Use a **test-mode** API key against `test.` and switch the host + key for production.

## Authentication

Bearer token in the header:

```
Authorization: Bearer YOUR_API_KEY
```

Generate keys in the dashboard under **Developer → API Keys**; each key can be **read-only or read-write**. Keep keys server-side.

```bash
curl https://test.dodopayments.com/payments \
  -H "Authorization: Bearer $DODO_API_KEY"
```

## Rate limiting

Dual-window (burst/sec + sustained/min) by tier:

| Tier | Burst (req/sec) | Sustained (req/min) |
|------|-----------------|---------------------|
| Tier 0 (default) | 40 | 240 |
| Tier 1 | 100 | 1,000 |
| Tier 2 | 500 | 5,000 |
| Unauthenticated | 20 | 100 |

Read `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset`; a `429` means back off (exponential).

## Endpoints (catalog)

**Payments**
- `POST /payments` — Create One-Time Payment
- `GET /payments` — List Payments · `GET /payments/{id}` — Get Payment · `GET /payments/{id}/line-items` — Retrieve Line Items · `GET /invoices/payments/{id}` — Get Invoice

**Subscriptions**
- `POST /subscriptions` — Create · `GET /subscriptions` — List · `GET /subscriptions/{id}` — Get · `PATCH /subscriptions/{id}` — Update
- `POST /subscriptions/{id}/change-plan` — Change Plan (+ Preview / Cancel scheduled change) · `POST /subscriptions/{id}/charge` — Create on-demand Charge
- Usage history, retrieve credit usage, update payment method

**Products & Digital Delivery**
- `POST /products` — Create · `GET /products` — List · `GET /products/{id}` — Get · `PATCH /products/{id}` — Update · archive/unarchive · update images/files
- Localized prices (CRUD), short links (create/list)

**Customers**
- `POST /customers` · `GET /customers` · `GET /customers/{id}` · `PATCH /customers/{id}`
- `POST /customers/{id}/customer-portal/session` — hosted customer portal · payment methods (list/delete) · wallets + wallet ledger

**Checkout Sessions**
- `POST /checkouts` — Create Checkout Session · `GET /checkouts/{id}` — Get · Preview

**License Keys / Entitlements** (for software/digital products)
- License keys: create, get, activate, deactivate, get instance
- Entitlements: create/update/delete, list grants, revoke grant, fulfill license-key grant, upload/delete file

**Discounts** — create/get/update/delete, list, get-by-code, validate.
**Refunds** — `POST /refunds` create, list, get, get receipt.
**Disputes** — list, get detail.
**Payouts** — list, breakup details, retrieve breakup, download breakup CSV.
**Addons / Brands / Credit Entitlements / Balance Ledger** — full CRUD groups also exist.

All list endpoints paginate; see each endpoint's `.md` page for params and JSON. Full per-endpoint docs: `https://docs.dodopayments.com/api-reference/{group}/{endpoint}`.

## Webhooks

**Spec: Standard Webhooks.** Dodo POSTs events to your endpoint with these headers:

```
webhook-id
webhook-signature
webhook-timestamp
```

**Verify with the `standardwebhooks` library** (don't hand-roll). The signing secret comes from the dashboard (or `GET /webhooks/{id}/signing-key`). Verifying with the library checks the signature + timestamp (replay protection).

**Webhook management API:** `POST /webhooks` create, `GET /webhooks` list, `GET /webhooks/{id}` details, `PATCH /webhooks/{id}` update, `DELETE /webhooks/{id}`, plus get/update **headers** and get **signing-key**.

**Events** cover the resource lifecycle — payment (succeeded/failed), subscription (active/renewed/on-hold/cancelled/plan-changed), refund, dispute, and license-key events. Confirm the exact event-type strings in the **Webhooks** doc (`/developer-resources/webhooks`) before switching on them.

**Local testing:** the **Dodo CLI** (`dodo wh trigger`) forwards events to your local endpoint over a WebSocket, preserving signature headers — **test-mode keys only**. Note: CLI-mocked payloads are **unsigned**, so use the library's `unsafe_unwrap()` (not `unwrap()`) when testing with mocks.

## SDKs, adapters, MCP

- **Official SDKs:** TypeScript, Python, Go, PHP, Java, Kotlin, C#, Ruby, React Native.
- **Framework adapters** (checkout + webhook handlers): Next.js, Nuxt, Remix, SvelteKit, Astro, Bun, Express, Fastify, Hono, Tanstack, Convex, Better Auth, Supabase boilerplate.
- **Billing SDK** (React/ShadCN components) + Mobile SDKs (React Native).
- **MCP server** — for AI agents to call Dodo Payments; plus an "Agent Skills" resource.
- **Dodo CLI** — keys, webhook forwarding, scaffolding.

## Pricing (best-effort)

**4% + $0.40 per transaction**, no monthly/setup fee (Standard); Enterprise custom. As MoR, Dodo's fee covers global tax handling + remittance.

## Error handling

Standard HTTP error codes + a documented Error Codes page (`/api-reference/error-codes`); `429` for rate limits. Inspect the response body for the error type.
