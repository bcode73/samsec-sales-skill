<!-- Source: https://api.foxy.io/docs (hAPI reference) + https://wiki.foxycart.com/v/2.0/webhooks (webhook details), fetched 2026-07-04. SDKs: github.com/Foxy/foxy-sdk (universal), github.com/Foxy/foxy-node-api. -->

# Foxy API Reference

## hAPI basics

- Base URL: `https://api.foxycart.com` (the docs live at api.foxy.io; both domains serve the hAPI).
- **Auth: OAuth 2.0** — create an OAuth client, then use client-credentials/refresh-token flows for tokens. Official SDKs (`@foxy.io/sdk` on npm — "Universal SDK for a full server-side and a limited in-browser access to Foxy hAPI") handle token management, HMAC signing utilities, and webhook verification.
- **Hypermedia (HATEOAS)**: responses embed link relations (`fx:customers`, `fx:transactions`, `fx:subscriptions`, …) — "Link Relationships are the key to Hypermedia APIs, and this is what you code your application to instead of specific remote procedure calls or hard-coded urls." Navigate by following links from the store resource, not by hardcoding paths.
- Methods: GET, POST, PUT (full update), PATCH (partial), DELETE, HEAD, OPTIONS.

Quick-start (token via your OAuth client, then follow links):

```bash
# Discover your store's link relations
curl "https://api.foxycart.com" \
  -H "Authorization: Bearer $FOXY_ACCESS_TOKEN" \
  -H "FOXY-API-VERSION: 1"
# → follow fx:store → fx:transactions / fx:subscriptions / fx:customers links
```

Key collections (via link relations on the store): transactions, subscriptions, customers, items, carts, coupons, webhooks, downloadables (digital goods), shipping/tax settings, template sets.

Pagination: collections return `offset`/`limit` style paging with `total_items`, plus `next`/`prev` hypermedia links — follow the links.

<!-- Collection list assembled from the hAPI reference nav and link relations — verify shapes at api.foxy.io/docs/reference before building. -->

## HMAC cart validation (anti-tampering for links/forms)

Foxy products are defined in **add-to-cart links and forms on your pages** — so without protection, a buyer could edit `price=25` in the URL/form. Foxy's answer is **HMAC product verification**: each product parameter is signed with your store's secret so the cart rejects modified values.

- "HMAC validation is recommended to prevent a malicious user from tampering with your add-to-cart links and forms."
- The signature is appended per-parameter (`||hash` style) — generate server-side at page-build time; the official SDKs include signing utilities (`@foxy.io/sdk` hmac helpers; pre-built serverless signers exist, e.g. `Foxy/foxy-node-netlify-functions`).
- Contrast with Snipcart, which validates by *crawling* your product URLs instead — Foxy's model works on fully static/CDN pages with no crawlable endpoint, but requires a signing step in your build or a serverless signer.

## Webhooks (JSON webhooks, current version — verbatim-sourced)

### Events

| Resource | Events |
|---|---|
| Transactions | `transaction/created`, `transaction/modified`, `transaction/captured`, `transaction/refunded`, `transaction/voided`, `transaction/refeed` |
| Subscriptions | `subscription/created`, `subscription/modified`, `subscription/cancelled`, `subscription/refeed` |
| Customers | `customer/created`, `customer/modified`, `customer/refeed` |
| Transaction log | `transaction_log/created`, `transaction_log/refeed` |
| Changelog | `changelog/created`, `changelog/refeed` |

Payloads are JSON in hAPI structure with embedded resources (transaction details, customer, items, payments, shipments, billing/shipping addresses), reflecting the resource's **state at send time**.

### Headers sent

- `Foxy-Webhook-Signature` — HMAC signature of the payload
- `Foxy-Webhook-Event` — event name
- `Foxy-Webhook-Refeed` — boolean, true when manually resent
- `Foxy-Store-ID` / `Foxy-Store-Domain`

### Signature verification (verbatim details)

> **Algorithm**: HMAC SHA256, hexadecimal format. **Key**: the webhook's encryption key (configured during setup). Generate a signature by computing the HMAC SHA256 hash of the raw payload body using your encryption key, then perform a secure comparison (not simple equality) against the header value.

```python
import hmac, hashlib, os

def verify(headers, raw_body: bytes) -> bool:
    digest = hmac.new(os.environ["FOXY_WEBHOOK_KEY"].encode(),
                      raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(headers.get("Foxy-Webhook-Signature", ""), digest)
```

### Retries & refeed (verbatim details)

> If the endpoint doesn't return a 200 within 1 minute, Foxy "will automatically reattempt to connect to your endpoint 11 more times within the following hour," with gradually increasing intervals. **After 12 consecutive failures, the webhook auto-deactivates.** Manual **refeed** is available from the admin transaction history (requests arrive with `Foxy-Webhook-Refeed: true`).

Legacy integrations: a Zapier webhook and a Webflow-specific webhook also exist alongside the JSON webhook.

## Errors & limits

- Rate limits aren't published in the captured docs — back off on 429s and keep clients single-purpose.
- OAuth tokens expire — SDKs refresh automatically; raw integrations must handle refresh-token rotation.

## Gaps

- Full per-resource field schemas live in the hAPI reference (api.foxy.io/docs/reference) and are too large to inline — the SDK types (`@foxy.io/sdk`) are the most reliable machine-readable schema source.
- Exact HMAC link-signing parameter format wasn't captured verbatim — use the SDK signing utilities rather than hand-rolling.
- Published rate-limit numbers: not found.
