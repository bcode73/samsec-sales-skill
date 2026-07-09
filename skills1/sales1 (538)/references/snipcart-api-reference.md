<!-- Source: https://docs.snipcart.com/v3/api-reference/introduction + /authentication + /v3/webhooks/introduction + /v3/webhooks/examples + /v3/mcp-server/basics (fetched 2026-07-04; docs are JS-rendered — captured via rendered fetch, some sections summarized where noted). -->

# Snipcart API Reference

## REST API basics

- Base URL: `https://app.snipcart.com/api`
- **Auth: HTTP Basic (RFC 7617) with the secret API key as the username and NO password** — base64 of `{apikey}:`. Keys are created per Test or Live mode and only reach that mode's data; multiple keys per account.

Verbatim examples from the authentication docs:

```bash
curl -H "Accept: application/json" \
  https://app.snipcart.com/api/orders \
  -u {YOUR_SECRET_API_KEY}:
```

```javascript
const secret = "YOUR_SECRET_API_KEY" + ":"
const request = await fetch('https://app.snipcart.com/api/orders', {
    headers: {
        'Authorization': `Basic ${btoa(secret)}`,
        'Accept': 'application/json'
    }
})
```

> Secret keys must never appear in source code, front-end assets, or be transmitted over insecure channels. Keys provide full account access.

### Resource groups (from the docs nav)

Orders · Notifications · Refunds · Customers · Discounts · User sessions · Products · Abandoned carts · Domains · Custom shipping methods.

Common calls:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/orders` | List orders (filterable by status, date) |
| GET | `/api/orders/{token}` | One order |
| PUT | `/api/orders/{token}` | Update order status / tracking |
| POST | `/api/orders/{token}/notifications` | Send a notification (e.g. tracking email) |
| POST | `/api/refunds` | Refund an order |
| GET | `/api/customers` · `/api/customers/{id}` | Customers |
| GET/POST/PUT/DELETE | `/api/discounts` | Discounts/coupons |
| GET | `/api/products` · `PUT /api/products/{id}` | Products seen by the crawler; stock updates |
| GET | `/api/carts/abandoned` | Abandoned carts |
| GET | `/api/requestvalidation/{token}` | Validate a webhook request token (see below) |

<!-- Paths beyond auth/webhooks assembled from the docs nav + MCP tool coverage — verify shapes at docs.snipcart.com/v3/api-reference before building. -->

Pagination on list endpoints: `offset` + `limit` query params with `totalItems` in responses. Rate limits are enforced but numbers aren't published — back off on 429.

## The product model (why "crawling" matters)

Snipcart products are **defined in your HTML** via buy-button attributes: `data-item-id`, `data-item-price`, `data-item-name`, `data-item-url` are **mandatory**. At checkout, Snipcart **crawls `data-item-url` on your site** to verify each product exists at that URL with the same price — this is the anti-tampering model (a buyer editing the DOM price gets caught at validation).

Consequences (from support threads — the platform's #1 error class):

- `product-crawling-failed` — the crawler couldn't find the product at `data-item-url`, the URL returned NotFound, or the price there didn't match the cart.
- JS-rendered pages (SPAs, headless CMS like Storyblok) can fail crawling because the crawler doesn't see client-rendered attributes → use a **JSON crawling endpoint** (serve the product definitions as JSON at a stable URL) or ensure SSR.
- Products can't be mutated dynamically with JavaScript after render — the crawler compares against what it fetches.
- The product URL must be on an **allowed domain** (configure domains in the dashboard) or validation rejects it.
- Price changes after a buyer carted an item force remove-and-re-add.

## Webhooks

- Configure in **Store Configurations → Webhooks**; multiple URLs separated by semicolons; each gets a POST with a JSON body and must answer `200`.
- Body carries an `eventName` (e.g. `order.completed`) plus the event content. Event categories: order events, subscription events, shipping events (rate requests), tax events (tax calculation callbacks).
- **Verification is a token callback, not an HMAC**: each request carries `X-Snipcart-RequestToken` (valid ~1 hour). Verify by calling back:

```bash
curl https://app.snipcart.com/api/requestvalidation/{token} \
  -u {YOUR_SECRET_API_KEY}:
# 200 = genuine Snipcart request; anything else = reject
```

- The dashboard keeps a **request-history page** with full HTTP details and a "Send this hook again" button — the built-in redelivery/testing tool. No automatic retry policy is documented; treat delivery as best-effort and reconcile via `GET /api/orders`.
- Shipping and tax webhooks are *synchronous* callbacks: Snipcart calls your endpoint during checkout and expects rates/taxes in the response.

## Official MCP Server (verbatim-sourced)

> The Snipcart MCP Server lets you manage your store through natural language using AI assistants like Claude, GPT (via Codex), or any MCP-compatible client.

- Hosted at `snipcart-mcp.azurewebsites.net` (Streamable HTTP).
- Auth: your **private API key** in a custom `X-Snipcart-Api-Key` header — same credential as the REST API; keep it secret. Rate-limited.
- **38 tools**: orders (list/view/status updates/notifications/digital-goods access), customers (search/view/update), products (browse/stock adjustments/archiving), discounts (coupon creation, multiple trigger types), refunds, abandoned-cart monitoring, custom shipping rates, domain configuration, order notes.
- Works with Claude Desktop, Claude Code, Cursor, Windsurf, Codex, GitHub Copilot — clients that support Streamable HTTP **with custom headers** (ChatGPT and Claude.ai web lack custom-header support).

## Gaps

- Docs are JS-rendered; per-endpoint request/response schemas weren't fully capturable — the auth and webhook-security sections above are verbatim, the endpoint table is assembled from the docs nav. Verify at docs.snipcart.com/v3/api-reference.
- No published rate-limit numbers; no documented webhook retry policy (manual re-send from the dashboard).
- Full webhook event list beyond `order.completed` and the shipping/tax callbacks wasn't retrievable from the rendered pages.
