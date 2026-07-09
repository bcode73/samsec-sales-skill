<!-- Source: https://docs.sellfy.com/article/127-webhooks and https://docs.sellfy.com/article/124-zapier (fetched 2026-06-29) -->

# Sellfy API & Automation Reference

> **There is NO public REST CRUD API.** Sellfy does not document endpoints for programmatically creating/reading/updating products, orders, or customers. The entire developer surface is **(1) outbound webhooks** and **(2) a Zapier API token**. Everything below reflects that. If you need a queryable commerce backend, Sellfy is the wrong tool — see the alternatives in `platform-guide.md`.

## Authentication (Zapier API token)

- The only token Sellfy issues is for **Zapier**. Create it at:
  `https://sellfy.com/user/integrations/apps/zapier` (Settings → Integrations).
- This token authenticates the Zapier connection only — it is **not** a general-purpose API key for arbitrary HTTP calls against documented endpoints (none are published).

## Webhooks

Setup: **Sellfy dashboard → Integrations → Webhooks → New** → provide a **title** and a **destination URL**. Sellfy sends an **HTTP POST** with a **JSON body** to that URL when the selected event occurs.

**No signature / HMAC.** The docs do not describe any signing or verification mechanism. Secure your endpoint with a secret URL path/token and source filtering; dedupe on the payload `id`.

### Event types

| Event | Fires when |
|---|---|
| **New Order** | Payment completes or order status changes |
| **Email Subscribe** | A customer joins the newsletter |
| **Email Unsubscribe** | A customer opts out |
| **Subscription Product Bought** | On initial purchase **and each renewal** |
| **Subscription Product Canceled** | When a subscription ends |
| **Cart Abandoned** | Buyer consents to emails but doesn't complete checkout |
| **Contact Form Submitted** | A store contact form is sent |

### Payloads (verbatim from docs)

Money fields are in **cents** (`449` = $4.49). Dates are **ISO 8601**. Example emails below are normalized to `buyer@example.com` (the live docs show a real example address; the field is `customer.email` / `payer_email` / `email`).

**New Order**
```json
{
    "id": "dmnVQFUm",
    "status": "COMPLETED",
    "currency": "USD",
    "amount": 449,
    "discount": {
        "amount": 499
    },
    "tax": {
        "amount": 0,
        "percents": 0
    },
    "customer": {
        "country": "US",
        "payment_type": "card",
        "email": "buyer@example.com",
        "ip": "127.0.0.1",
        "consent_to_newsletters": true,
        "name": "John Doe",
        "address": {
            "line1": "Wall street",
            "line2": "12-b7",
            "state": "NY",
            "country": "US",
            "city": "New York",
            "tax_number": "",
            "postal_code": "10105",
            "phone": "212-487-2939"
        }
    },
    "products": [
        {
            "id": "61d2ef5352ca3cdc80662cb1",
            "key": "uQsm",
            "name": "Icon set",
            "amount": 299,
            "discount": {
                "type": "coupon",
                "code": "25OFF",
                "amount": 25,
                "amount_type": "percentage",
                "amount_applied": 25,
                "currency": "USD"
            },
            "quantity": 1,
            "variant": {
                "id": "65782c83586fbb97ce6a8715",
                "name": "Outline set"
            }
        },
        {
            "id": "61d2ef5352ca3cdc80662cb4",
            "key": "QFUm",
            "type": "sale",
            "name": "Holiday cards",
            "amount": 0,
            "discount": {
                "type": "sale",
                "amount": 500,
                "amount_type": "fixed",
                "amount_applied": 399,
                "currency": "USD"
            },
            "quantity": 1,
            "variant": {
                "id": "65782c8b586fbb97ce6a8716",
                "name": "Small"
            }
        },
        {
            "id": "61d2ef5352ca3cdc80662cb7",
            "key": "dmnV",
            "name": "Awesome serif-font",
            "amount": 150,
            "discount": {},
            "quantity": 1,
            "variant": {
                "id": "65782c91586fbb97ce6a8717",
                "name": "Default"
            }
        }
    ],
    "date": "2022-01-12T11:57:59+00:00"
}
```
<!-- Cleaned one fetch artifact: "tax_number": "," in the scraped output is a malformed empty string; rendered here as "". Verify against live docs. -->

**Email Subscribe / Unsubscribe**
```json
{
  "customer": {
    "email": "buyer@example.com"
  },
  "date": "2018-01-17T12:28:00+00:00"
}
```

**Subscription Product Bought / Canceled**
```json
{
  "id": "61542a2a67cfd83cd57ae4bb",
  "payer_email": "buyer@example.com",
  "plan_name": "Subscription plan name",
  "plan_amount": 2000,
  "interval": "month",
  "product": {
    "id": "60e5b823221c469a8daede88",
    "key": "QFUm",
    "name": "Subscription product name"
  },
  "activated_at": "2022-05-28T23:17:05+00:00",
  "current_period_started_at": "2022-05-28T23:17:05+00:00",
  "current_period_ends_at": "2022-06-27T23:17:05+00:00"
}
```

**Cart Abandoned**
```json
{
    "id": "615c388dc14058fdfc5671ec",
    "payer_email": "buyer@example.com",
    "total": 968,
    "currency": "USD",
    "tax": {
      "percents": 21,
      "amount": 168
    },
    "sub_total": 1000,
    "last_interaction_at": "2022-05-28T17:17:05+00:00",
    "items": [
      {
        "price": 1000,
        "discount": 200,
        "total": 800,
        "product": {
          "id": "60e5b823221c469a8daede88",
          "key": "zmsy7q",
          "name": "Holiday cards",
          "selected_variant": "Default"
        },
        "sub_total": 1000
      }
    ]
}
```

**Contact Form Submitted**
```json
{
    "email": "buyer@example.com",
    "subject": "Email subject",
    "body": "Email body text",
    "sent_at": "2022-05-30T10:50:02+00:00"
}
```

## Zapier triggers & actions

**Triggers** (payment-event based — selected when configuring the Zap):
- Completed payment
- Refunds
- Reversed payments
- All events (leave the selection blank)

**Actions:** Sellfy is primarily a *trigger* source; the action side is whatever the 5,000+ apps in the Zapier directory expose (email, Sheets, CRM, Slack, etc.). Zapier **filtering** is supported to narrow which events proceed.

## Consuming events reliably (developer checklist)

1. **Respond 2xx fast** — do heavy work async so Sellfy doesn't treat the delivery as failed.
2. **Idempotency** — dedupe on `id` (orders/subscriptions/cart) or composite (`email`+`date`) for email/contact events; assume retries.
3. **Treat money as cents** — divide by 100 for display.
4. **No backfill** — there's no read API to re-fetch missed events. Persist every webhook on arrival; reconcile against the dashboard CSV export.
5. **No HMAC** — authenticate via a secret URL path/token + IP/UA allowlist; never grant entitlements on unverified payload contents alone.
6. **Subscription "Bought" = purchase + every renewal** — make grant/extend logic idempotent against `current_period_ends_at`.

## Gaps

- No documented base URL, REST endpoints, pagination, or rate limits — because there is no public REST API.
- No official SDK or MCP server. The `github.com/Sellfy` org hosts only test assignments and forks (no API client, OpenAPI spec, or embed library).
- Webhook retry/backoff behavior and exact delivery guarantees are not published — assume at-least-once with possible reordering and verify in-account.
