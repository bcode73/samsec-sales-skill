<!-- Source: https://developers.thrivecart.com/documentation/ -->
<!-- Source: https://developers.thrivecart.com/documentation/event_subscription/intro/ -->
<!-- Source: https://support.thrivecart.com/help/using-webhook-notifications/ -->
<!-- Captured 2026-06-27. Auth, rate limit, the Event-Subscription-vs-standard-webhook split, and the event
     list are from the official docs. Webhook payload JSON is CONSTRUCTED from documented fields + the
     standard ThriveCart notification format and marked — verify against a live webhook delivery. -->

# ThriveCart API & Webhooks Reference

ThriveCart's integration surface is built around **events** — most automations are driven by **webhooks**
(a purchase/refund/subscription event POSTed to your URL), plus a small REST API and an **Event
Subscription API** for targeted event delivery. Docs: `developers.thrivecart.com`; full reference with
code samples: `apidocs.thrivecart.com`. There's an official **PHP SDK** (Composer).

## Authentication

- **API tokens (your own account):** Settings → **API & webhooks** → **API tokens**. Use the token to call
  the REST API and to authenticate webhooks.
- **OAuth 2.0 (third-party apps):** register an application to access *other* users' accounts.
- **Rate limit:** **60 requests/minute per connected account** — contact support if you consistently exceed.

### Webhook auth (validation)

ThriveCart webhooks include a **secret** you set when configuring the notification. Validate every inbound
webhook by checking the posted `thrivecart_secret` (or signature field) against the secret you configured —
reject anything that doesn't match. (Confirm the exact field name in your account's webhook settings.)

## Standard webhooks vs Event Subscription API

- **Standard webhooks** (Settings → API & webhooks): one URL receives **all** events for the account. Simple,
  but you filter event types yourself.
- **Event Subscription API:** create an endpoint that receives **only the specific event types you subscribe
  to** — better for scaling and for third-party apps. Use this when you only care about, say, `order.success`.

## Event types

Driven by checkout activity:

| Group | Events |
|---|---|
| Orders | `order.success`, `order.refund`, `order.failed`, `order.partial_refund` |
| Subscriptions | `order.subscription_payment` (rebill), `order.subscription_cancelled`, `order.subscription_paused`, `order.subscription_resumed` |
| Funnel | upsell / downsell / bump purchase events |
| Affiliates | `affiliate.commission_earned`, affiliate approval/rejection, payout events |
| Carts | abandoned-cart events |

## Webhook payload (shape)

<!-- Constructed from the standard ThriveCart notification format — verify against a live delivery -->
```json
{
  "event": "order.success",
  "thrivecart_account": "yourname",
  "thrivecart_secret": "YOUR_CONFIGURED_SECRET",
  "mode": "live",
  "order_id": 123456,
  "invoice_id": "INV-123456",
  "customer": { "email": "buyer@example.com", "name": "Sam Rivera", "id": "cus_abc" },
  "order": {
    "total": "49.00", "currency": "USD",
    "charges": [ { "amount": "49.00", "tax": "0.00" } ]
  },
  "base_product": 7,
  "base_product_name": "Pro Course",
  "bumps": [], "upsells": [],
  "subscription": { "id": "sub_abc", "status": "active", "frequency": "monthly" }
}
```
> Field names/casing vary by event and account era — **always validate the `thrivecart_secret`** and treat
> the payload defensively. Match products by your configured **product id**, and dedupe on `order_id`.

### Verify + handle (Python, Flask)
```python
from flask import request, abort
SECRET = "YOUR_CONFIGURED_SECRET"
def thrivecart_webhook():
    data = request.form or request.get_json(silent=True) or {}
    if data.get("thrivecart_secret") != SECRET:   # reject spoofed posts
        abort(401)
    if data.get("event") == "order.success":
        grant_access(data["customer"]["email"], data.get("base_product"))
    elif data.get("event") == "order.subscription_cancelled":
        revoke_or_dunning(data["customer"]["email"])
    return "", 200
```

## REST API (read/manage)

Beyond webhooks, the REST API (token auth) exposes account data (products, orders/transactions, customers,
affiliates). Use it to reconcile or pull history. Generate exact calls from `apidocs.thrivecart.com` (cURL/
Node/PHP samples) or the PHP SDK.

```bash
# Shape only — confirm exact base path/endpoints in apidocs.thrivecart.com
curl -s "https://thrivecart.com/api/external/..." -H "Authorization: Bearer YOUR_API_TOKEN"
```

## Gaps / not documented here

- Exact REST base URL, endpoint paths, and full response schemas: the developer reference is partly JS-
  rendered — confirm at **apidocs.thrivecart.com** / the PHP SDK. The webhook payload above is constructed
  from the standard notification format.
- No published HMAC scheme; webhook authenticity is verified via the **shared `thrivecart_secret`** you
  configure — there is no signature header, so keep the secret private and validate it on every call.
- **No download/link protection** for delivered digital files — the API won't fix this; gate access in your
  own app off `order.success` if you need real protection.
- No MCP server found.
